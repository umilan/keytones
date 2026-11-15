#!/usr/bin/env python3
"""Keytones detection bench — runs the real app on known audio.

For every (clip, algorithm) pair it opens index.html in headless Chromium
with a fake microphone that plays the clip's WAV, so the audio goes through
exactly the same path as a real mic (AudioContext -> gain -> AnalyserNode ->
detector -> Stability -> active notes). The app is not modified: the bench
wraps runDetection() from outside and logs every detection frame:

    [t_ms, input_rms, raw_pitch_classes, final_pitch_classes, detect_ms]

raw  = what the algorithm returned this frame (before Stability)
final = the notes the app treats as sounding (lastNote / activePolyNotes)

Logs are scored by score.py against the clip's JSON truth.

    python3 bench/make_fixtures.py
    python3 bench/run.py                         # all clips x all algorithms
    python3 bench/run.py --algos yin,multif0 --clips triads,mono_piano
    python3 bench/run.py --speed 5 --stability 1 # different Settings
"""
import argparse
import asyncio
import functools
import http.server
import json
import os
import socketserver
import threading
import time

from playwright.async_api import async_playwright

import score

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIX = os.path.join(HERE, 'fixtures')
ALL_ALGOS = ['fft', 'acf', 'amdf', 'yin', 'mpm', 'hpcp', 'nnls', 'cqtnmf', 'multif0']

# runs inside the page once it has loaded: stop the default mic, apply the
# bench settings, wrap the detection loop with a logger, then reopen the mic
# (which restarts the fake-mic file from its beginning)
SETUP_JS = """
async ({algo, settings, gainDb}) => {
  stopMic();
  agcTick = () => {};                                    // the 10 s auto-gain would change the level mid-test
  Object.assign(detection, settings);
  setMicGain(gainDb);
  setPitchAlgo(algo);
  const log = window.__ktLog = [];
  let raw = null;
  const pc = f => ((Math.round(12 * Math.log2(f / C0_HZ)) % 12) + 12) % 12;
  const origMono = detectPitch, origPoly = detectPitchPoly, origRun = runDetection;
  detectPitch = sr => { const r = origMono(sr); raw = r ? [pc(r.freq)] : []; return r; };
  detectPitchPoly = sr => { const r = origPoly(sr); raw = [...new Set(r.map(x => pc(x.freq)))]; return r; };
  runDetection = () => {
    if (!analyser) return;
    const t = performance.now();
    raw = [];                                           // stays empty when the gate blocks the frame
    const level = rms(getTimeFrame());
    origRun();
    const t1 = performance.now();
    const fin = POLY_ALGOS.has(pitchAlgo) ? [...activePolyNotes.keys()] : (lastNote >= 0 ? [lastNote] : []);
    log.push([+t.toFixed(1), +level.toFixed(6), raw, fin, +(t1 - t).toFixed(2)]);
  };
  await startMic();
  await audioCtx.resume();
  return { sampleRate: audioCtx.sampleRate, state: audioCtx.state, mic: micActive };
}
"""


def serve(root):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Quiet, directory=root)
    httpd = socketserver.ThreadingTCPServer(('127.0.0.1', 0), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


async def run_one(pw, url, wav, duration, algo, settings, gain_db):
    browser = await pw.chromium.launch(args=[
        '--use-fake-ui-for-media-stream',
        '--use-fake-device-for-media-stream',
        f'--use-file-for-fake-audio-capture={wav}%noloop',
        '--autoplay-policy=no-user-gesture-required',
    ])
    try:
        page = await browser.new_page(viewport={'width': 1000, 'height': 700})
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        await page.goto(url)
        await page.wait_for_function('typeof startMic === "function" && document.readyState === "complete"')
        await page.wait_for_timeout(300)
        info = await page.evaluate(SETUP_JS, {'algo': algo, 'settings': settings, 'gainDb': gain_db})
        await page.wait_for_timeout(int((duration + 0.6) * 1000))
        log = await page.evaluate('window.__ktLog')
        return {'info': info, 'log': log, 'errors': errors}
    finally:
        await browser.close()


async def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--algos', default=','.join(ALL_ALGOS))
    ap.add_argument('--clips', default='', help='comma list (default: every clip in fixtures/)')
    ap.add_argument('--speed', type=int, default=3, help='Settings > Speed 1-5 (app default 3)')
    ap.add_argument('--gate', type=float, default=-40, help='Settings > Gate dB (app default -40)')
    ap.add_argument('--confidence', type=float, default=50, help='Settings > Confidence 0-100 (app default 50)')
    ap.add_argument('--stability', type=int, default=2, help='Settings > Stability frames (app default 2)')
    ap.add_argument('--gain', type=float, default=6, help='mic gain dB (default +6: puts the clips mid-way in the level range the app\'s auto-gain aims for)')
    ap.add_argument('--parallel', type=int, default=2, help='browsers at once (keep <= CPU cores: timing is real-time)')
    ap.add_argument('--out', default=os.path.join(HERE, 'results'))
    ap.add_argument('--app', default=ROOT, help='folder with the index.html to test (e.g. a git worktree of an older version)')
    a = ap.parse_args()

    algos = a.algos.split(',')
    clips = a.clips.split(',') if a.clips else sorted(f[:-5] for f in os.listdir(FIX) if f.endswith('.json'))
    settings = {'speed': a.speed, 'gateDb': a.gate, 'confidence': a.confidence, 'stability': a.stability}
    stamp = time.strftime('%Y%m%d-%H%M%S')
    out_dir = os.path.join(a.out, stamp)
    os.makedirs(os.path.join(out_dir, 'logs'), exist_ok=True)

    with open(os.path.join(a.app, 'index.html')) as f:
        html = f.read()
    version = html.split('id="app-version">', 1)[1].split('<', 1)[0]

    httpd, port = serve(a.app)
    url = f'http://127.0.0.1:{port}/index.html'
    sem = asyncio.Semaphore(a.parallel)
    results = []
    jobs = [(c, al) for c in clips for al in algos]
    done = 0
    t_start = time.time()

    async with async_playwright() as pw:
        async def job(clip, algo):
            nonlocal done
            async with sem:
                truth = json.load(open(os.path.join(FIX, clip + '.json')))
                wav = os.path.join(FIX, clip + '.wav')
                r = await run_one(pw, url, wav, truth['duration'], algo, settings, a.gain)
                with open(os.path.join(out_dir, 'logs', f'{clip}__{algo}.json'), 'w') as f:
                    json.dump(r, f)
                m = score.score(r['log'], truth, a.gain)
                m.update(clip=clip, algo=algo, errors=r['errors'])
                results.append(m)
                done += 1
                print(f'[{done:3d}/{len(jobs)}] {clip:15s} {algo:8s} F1 {score._f(m["f1"])}  settled {score._f(m["f1_settled"])}'
                      f'  onset {score.fmt_ms(m["onset_median_ms"])}  ghost {m["ghost_pct"]:.0f}%'
                      f'  align {m["align_err_db"]:.1f}dB' + (f'  ERR {r["errors"][0][:60]}' if r['errors'] else ''),
                      flush=True)
        await asyncio.gather(*(job(c, al) for c, al in jobs))

    httpd.shutdown()
    meta = {'version': version, 'settings': settings, 'gain_db': a.gain, 'algos': algos, 'clips': clips,
            'started': stamp, 'wall_s': round(time.time() - t_start)}
    with open(os.path.join(out_dir, 'results.json'), 'w') as f:
        json.dump({'meta': meta, 'results': results}, f, indent=1)
    report = score.report(meta, results)
    with open(os.path.join(out_dir, 'summary.md'), 'w') as f:
        f.write(report)
    print('\n' + report)
    print(f'written to {out_dir}')


if __name__ == '__main__':
    asyncio.run(main())
