#!/usr/bin/env node
/* Ensemble bench, part 1: record. Runs every chord algorithm (P1–P4) on the SAME
   detection frames of each clip, so their outputs can be fused offline
   (bench/ensemble.py). Same path as bench/run.py: headless Chromium, a fake mic
   playing the clip, the real app. The app runs P4 (multi-F0) as usual; the
   detectPitchPoly() wrapper also calls P1–P3 on that frame and logs all four.

   node bench/ensemble_run.js [--clips a,b] [--parallel 2] [--gain 6]
   → bench/results/ensemble-<stamp>/<clip>.json  { info, truthFile, frames: [[t, level, {algo: [[pc, conf, oct]…]}, {algo: ms}]] }
   Needs bench/fixtures (python3 bench/make_fixtures.py) and Node's playwright. */
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');

const HERE = __dirname, ROOT = path.dirname(HERE), FIX = path.join(HERE, 'fixtures');
const ALGOS = ['hpcp', 'nnls', 'cqtnmf', 'multif0'];
const arg = (k, d) => { const i = process.argv.indexOf('--' + k); return i > 0 ? process.argv[i + 1] : d; };
const clips = arg('clips', '') ? arg('clips').split(',') : fs.readdirSync(FIX).filter(f => f.endsWith('.json')).map(f => f.slice(0, -5)).sort();
const parallel = +arg('parallel', 2), gainDb = +arg('gain', 6);
const settings = { speed: 3, gateDb: -40, confidence: 50, stability: 2 }; // app defaults, as bench/run.py

const SETUP_JS = `async ({ algos, settings, gainDb }) => {
  stopMic();
  agcTick = () => {};
  Object.assign(detection, settings);
  setMicGain(gainDb);
  setPitchAlgo('multif0');
  const log = window.__ktLog = [];
  const orig = detectPitchPoly, origRun = runDetection;
  let frame = null;
  detectPitchPoly = sr => {
    const keep = pitchAlgo, out = {}, ms = {};
    let ret = [];
    for (const a of algos) {
      pitchAlgo = a;
      const t0 = performance.now();
      const r = orig(sr);
      ms[a] = +(performance.now() - t0).toFixed(2);
      out[a] = r.map(x => { const n = Math.round(12 * Math.log2(x.freq / C0_HZ)); return [((n % 12) + 12) % 12, +(x.conf ?? 1).toFixed(3), Math.floor(n / 12)]; });
      if (a === keep) ret = r;
    }
    pitchAlgo = keep;
    frame = [out, ms];
    return ret;
  };
  runDetection = () => {
    if (!analyser) return;
    const t = performance.now();
    frame = null; // stays null when the gate blocks the frame
    const level = rms(getTimeFrame());
    origRun();
    log.push([+t.toFixed(1), +level.toFixed(6), frame ? frame[0] : {}, frame ? frame[1] : {}]);
  };
  await startMic();
  await audioCtx.resume();
  return { sampleRate: audioCtx.sampleRate, mic: micActive };
}`;

function serve() {
  return new Promise(res => {
    const srv = http.createServer((req, rsp) => {
      const f = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
      if (!f.startsWith(ROOT) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { rsp.writeHead(404); rsp.end(); return; }
      rsp.writeHead(200, { 'Content-Type': f.endsWith('.html') ? 'text/html' : 'application/octet-stream' });
      fs.createReadStream(f).pipe(rsp);
    }).listen(0, '127.0.0.1', () => res(srv));
  });
}

(async () => {
  const srv = await serve(), url = `http://127.0.0.1:${srv.address().port}/index.html`;
  const stamp = new Date().toISOString().replace(/[-:]/g, '').slice(0, 15).replace('T', '-');
  const out = path.join(HERE, 'results', 'ensemble-' + stamp);
  fs.mkdirSync(out, { recursive: true });
  const queue = [...clips];
  const worker = async () => {
    while (queue.length) {
      const clip = queue.shift();
      const truth = JSON.parse(fs.readFileSync(path.join(FIX, clip + '.json')));
      const b = await chromium.launch({ args: ['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream',
        `--use-file-for-fake-audio-capture=${path.join(FIX, clip + '.wav')}%noloop`, '--autoplay-policy=no-user-gesture-required'] });
      try {
        const p = await b.newPage({ viewport: { width: 1000, height: 700 } });
        const errors = []; p.on('pageerror', e => errors.push(String(e)));
        await p.goto(url);
        await p.waitForFunction('typeof startMic === "function" && document.readyState === "complete"');
        await p.waitForTimeout(300);
        const info = await p.evaluate(`(${SETUP_JS})(${JSON.stringify({ algos: ALGOS, settings, gainDb })})`);
        await p.waitForTimeout(Math.round((truth.duration + 0.6) * 1000));
        const frames = await p.evaluate('window.__ktLog');
        fs.writeFileSync(path.join(out, clip + '.json'), JSON.stringify({ info, errors, gainDb, settings, frames }));
        console.log(`${clip.padEnd(15)} ${frames.length} frames ${errors.length ? 'ERR ' + errors[0] : ''}`);
      } finally { await b.close(); }
    }
  };
  await Promise.all(Array.from({ length: parallel }, worker));
  srv.close();
  console.log('written to ' + out);
})();
