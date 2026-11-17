# Raw source: git history

Snapshot of `git log` (oldest first, full messages) taken at v1.93 (commit f2e48ed), 2026-11-17. Immutable — re-snapshot into a new file instead of editing.

## c369bd1 · 2026-08-30

Initial commit: Keymap PWA

## 9af1389 · 2026-08-30

Add index.html redirect for GitHub Pages

## 5a52a41 · 2026-08-30

Fix layout overlap with iPhone Dynamic Island / notch

Add CSS env(safe-area-inset-*) handling so the topbar, keyboard,
mic strip, and settings panel stay clear of the Dynamic Island/notch
and the home-indicator area on iPhones with viewport-fit=cover.


## 6910373 · 2026-08-30

Fix silent audio on iPhone when Ring/Silent switch is on

WebKit routes AudioContext output through the "ambient" audio session
category, which the hardware mute switch silences. Play a real (silent)
looping HTMLAudioElement on the user's first touch/click/keydown to
switch iOS to the "playback" category instead, so notes are still
audible with the switch on.


## e2051f9 · 2026-08-30

Consolidate app into index.html, restructure Settings panel

Rename keymap.html to index.html (update manifest start_url) so the
app lives directly at the root with no redirect stub, and restructure
the Settings panel into BEHAVIOR/AUDIO/MIDI sections with expanded
controls (algorithm default, sound octave, gain trim, MIDI channels,
MIDI out transpose). Merged on top of the iPhone audio/notch fixes
already on main.


## 5a52267 · 2026-08-30

Settings panel pushes content instead of overlaying it

Replace the fixed-overlay panel (position:fixed + translateX + dark
backdrop) with an in-flow flex sibling of #app that animates width
instead of sliding over the top. #app now shrinks via flex to make
room, and the piano/bars re-run their layout live during the slide
(ResizeObserver) so they visibly stretch with it rather than jumping.

The topbar's existing narrow-width fallback (which relocates decay/oct
into the panel) is now also triggered by the panel's own push, not
just window resizes, and #app clips instead of letting rows that no
longer fit bleed into the panel — previously masked by the overlay.


## 4afadfd · 2026-08-30

Fix corrupted Settings panel CSS

The #settings-panel/#settings-panel.open/.sp-header rules had gotten
mangled (missing selector, duplicated/truncated declarations,
stray hardcoded colors), so the whole settings panel rendered
completely unstyled — default serif font, white selects, no dark
theme. Rewrote the block cleanly.


## 7052a32 · 2026-08-30

Make whole settings header close the panel

The close affordance was just the small ✕ button; now clicking
anywhere in the header (title included) closes it too.


## 3c925c4 · 2026-08-30

Link Settings > Gain with the topbar GAIN drag

They were two independent multipliers stacked on top of each other
(a 0-300% drag and a separate -100..+1000dB trim). Made them the same
control: the dB list's option values are the % they map to (relabeled
to a realistic -inf..+9.5dB range matching what 0-300% can express),
and both directions sync through the existing setMicGain().


## 2124de4 · 2026-08-30

Remove redundant CONTROLS relocation section from Settings

Decay and MIDI out transpose already have their own rows in the
BEHAVIOR/MIDI sections, so the old narrow-window fallback that moved
the topbar's Decay/Oct controls into a duplicate CONTROLS slot was
redundant. Removed it (HTML, CSS, and initResponsiveTopbar()) — the
topbar controls just stay put now (#app's overflow:hidden already
clips them if a window gets too narrow to fit everything).

Also label the MIDI out transpose options in octaves ("-2 oct",
"0 oct", "+3 oct", ...) instead of bare numbers.


## a08e3e2 · 2026-08-30

Add Launchkey MK3 pad lighting (output only)

Recreates one octave of Launchpad's piano-layout pad mapping (bottom
row = white keys, top row = black keys, gapped at E-F/B-C, C
duplicated at both row ends) on the Launchkey's 2x8 Session-mode pad
grid, and lights whichever notes are currently sounding — mic-detected
or played in-app — the same way Launchpad's Programmer Mode does,
hooking into the same sendMidiNote() funnel so no other code needed
to change.

Protocol per the Launchkey [MK3] Programmer's Reference Guide: DAW
mode on/off is channel 16 note 0Ch (9F/8F 0C 7Fh/00h), pad colours are
plain Note On messages on channel 1 (stationary colour) with velocity
= palette index (0=off, 1=dim grey, 5=red, 45=blue — confirmed against
the guide's own worked examples). Unlike Launchpad, this is output
only (no pad-press input handling), and only works when the
Launchkey's *DAW* MIDI port (not its plain performance port) is
selected as MIDI Out in Settings — noted in a code comment since I
can't verify port naming without the actual hardware. Verified the
byte sequences and pad/colour mapping against a mocked MIDI output;
untested on real hardware.


## d231ff3 · 2026-08-30

Force Launchkey pads into Session mode on DAW-mode entry

DAW mode defaults the pads to Session layout, but only if nothing else
switched them since — a user could have left the pads in Drum/Custom/
Scale mode from a prior standalone session. Explicitly send the pad-
mode CC (channel 16, CC 03h = 02h/Session) so the app's pad addresses
are always valid regardless of prior device state.


## 3e87258 · 2026-08-30

Fix mic never connecting: mic-note-name/freq were HTML-commented out

Leftover corruption from the earlier keymap.html -> index.html 3-way
merge (same root cause as the settings-panel CSS corruption fixed
before, just in a different spot this time — an HTML comment, which
the earlier brace-balance check couldn't catch). Four elements inside
#mic-strip (both .mic-sep dividers, #mic-note-name, #mic-note-freq)
were wrapped in <!-- --> and so never existed in the DOM.

startMic() calls setMicUI('connecting', ...) as its very first line,
outside any try/catch, which sets nameEl.textContent on the (null)
#mic-note-name — throwing before the function ever reaches
getUserMedia(). Since nothing awaits/catches startMic() at the call
site, this became a silent unhandled rejection: no permission prompt,
no error shown, mic just never connects. Un-commented the elements.

Also improved the actual error handling: the catch block was silently
swallowing whatever error DID happen (wrong device, permission denied,
no getUserMedia support) into one generic "Mic unavailable" message
with no way to tell which — added console.error logging and surface
the real error name in the status text instead.

Scanned the rest of the file for any other similar orphaned HTML
comments; found none.


## 53e9699 · 2026-08-30

Fix algorithm picker: three CSS rules had merged into one broken rule

Same corruption source as the last two fixes (the keymap.html ->
index.html 3-way merge) — .algo-native-select, #mic-note-name, and
#mic-note-freq had been spliced into a single rule with a stray
display:none (twice), a truncated `appearance: no`/`transition: co`,
and duplicated properties. display:none on .algo-native-select made
the whole picker unclickable — "this picker doesn't work" — since
that's the actual (invisible, opacity:0) <select> overlaying the
"MF0" badge that makes it respond to taps at all. Restored the three
rules to their original, pre-merge form.

Also fixed a second, unrelated corruption in #app: an unterminated
comment (missing its opening /*) leaked two lines of text as invalid
CSS and duplicated display/flex-direction — from my own edit earlier
this session, not the old merge.

Ran two systematic scans across the whole stylesheet (duplicate
property names within a single rule, and /* */ comment balance) to
catch any other instances of either pattern — none found.


## 1554fdb · 2026-08-30

Gain: dB-native slider aligned with Settings, plus auto-gain

Gain is now dB-canonical everywhere (micGainDb replaces micGainPct):
the topbar's GAIN drag stays a continuous slider but displays/operates
in dB now, matching Settings > Gain exactly (both drive the same
setMicGain(), same as before). Range widened from the old 0-300%
(~-inf..+9.5dB — a hard ceiling) to a full -40..+40dB, since that
ceiling is the most likely reason bars stop responding once the mic
is on: quiet input just couldn't be boosted enough to cross the
polyphonic detector's score threshold, so no notes ever registered
and outerCounts never moved (confirmed the render()/bar-DOM path
itself is fine by feeding it synthetic counts directly).

Also added a lightweight auto-gain: the browser's own AGC is already
turned off on the getUserMedia constraints (it distorts levels
unpredictably for pitch detection), so every ~10s now nudge micGainDb
by 3dB toward a healthy meter range instead, based on a real running
average rather than one frame. Verified the boost/cut/no-op logic and
the drag<->Settings sync directly.


## 51160fd · 2026-08-30

Remove topbar OCT control and mic note-name/freq display

MIDI out transpose already lives in Settings, so the topbar OCT
stepper was redundant. shiftMidiOctave() keeps working (Settings'
transpose select still drives it), just no longer syncs a DOM element
that no longer exists. Note-name/frequency display in the mic strip
is gone too, along with its now-dead CSS and the note-name coloring
logic in setMicUI() that only existed to serve it.

Also, per feedback on this pass:
- Shortened all mic-status labels (WAIT/ON/LIVE/N/A/MUTED instead of
  "Connecting...", "Mic unavailable", etc.), including the getUserMedia
  error paths — now just the bare error name instead of a wrapped
  sentence, console.error still has the full detail.
- The mic status badge's own background now doubles as a live level
  meter (a green fill sized to the same rms-based percentage the
  separate meter bar already used), instead of that being the only
  place the input level shows.
- Removed the divider between the level meter and the algorithm
  picker in the mic strip (and its now-unused .mic-sep rule, since
  nothing referenced that class anymore).


## 58c7647 · 2026-08-30

Extend live-level fill to the whole mic badge, not just the text

Moved the level-based background from #mic-status to #mic-badge (the
dot included), with var(--surface) layered underneath as a second
background so the unfilled portion still shows the badge's normal
color instead of the page bleeding through. Added overflow:hidden on
.mic-badge so the fill respects the pill's rounded corners.


## 4e17576 · 2026-08-30

Move mic/gain to topbar, add responsive algorithm button group

- Removed the green mic-dot blink animation and the separate
  horizontal level-track bar (the mic badge's own background fill,
  added last pass, already shows live level).
- Moved #mic-badge and #gain-ctrl out of the mic strip and into the
  topbar, next to Decay.
- The mic strip (now otherwise empty) hosts a new responsive
  algorithm picker: the existing compact "MF0 v" badge on narrow
  screens, or a full horizontal button group — one button per
  algorithm, current one highlighted in the app's active-key orange —
  once there's enough room, measured via ResizeObserver the same way
  the keyboard/topbar responsive logic elsewhere in this file already
  works. Both pickers share the same setPitchAlgo() sync point, so
  algorithm changes from either stay in lockstep with Settings too.

Also fixed a real regression this surfaced: with mic/gain added, the
topbar can overflow on narrow windows, and since it was the last
child, #settings-btn — the only way to reach Settings — was the first
thing to get clipped off-screen by #app's overflow:hidden, unreachable.
Made #topbar horizontally scrollable (scrollbar hidden) instead, so
nothing in it is ever unreachable, only requires a swipe.


## 9fed69a · 2026-08-30

Relabel algorithms as M1-M5/P1-P4/T1 everywhere

Replaced the technical acronyms (FFT/ACF/AMDF/YIN/MPM/HPCP/NNLS/
CQTNMF/MF0/TEST) with a systematic scheme in the button group, both
select dropdowns, and the compact badge: M for monophonic, P for
polyphonic, T for test, numbered in existing list order. Kept the
real algorithm name as each control's title tooltip so the detail
isn't lost, just no longer in the primary label.


## a37cf54 · 2026-08-30

Algorithm picker: full names in dropdowns, neutral grouped buttons

Dropdown options now read "M1 FFT Peak", "M2 Autocorrelation (ACF)",
etc. instead of a bare ID with the name hidden in a tooltip.

Button group: dropped the orange --active-bg accent for the selected
state in favor of the same dim/full-text convention used elsewhere in
the app (var(--dim) idle, var(--text) + var(--surface-strong) active —
no color). Also merged the individually-bordered pill buttons into one
segmented control — a single outer border on the group, hairline
dividers between buttons instead of gaps — so there's no wasted margin
between them.


## 7c78251 · 2026-08-31

Add OFF algorithm option; show full label in the compact picker

New "OFF" entry (button group, both dropdowns) pauses detection
entirely — runDetection() now no-ops while pitchAlgo === 'off', so the
mic can stay connected (level meter, gain, AGC all keep running)
without any note ever registering. Also fixed a latent gap switching
to it exposed: setPitchAlgo() already released a stuck poly note on
switch but never a stuck mono one (lastNote) — harmless before since
the next detection tick would always clean it up eventually, but OFF
means that tick never comes, so it's released explicitly now.

The compact "M1 v"-style badge (shown when the button group doesn't
fit) now displays the full label — "M2 Autocorrelation (ACF)" instead
of just "M2" — since it stretches to the row's full width anyway, with
ellipsis truncation as a safety net if a label is ever too long for
the space.


## 68daac8 · 2026-11-10

Auto-select connected Launchpad/Launchkey as MIDI in/out

When no device is remembered (or the remembered one isn't plugged in),
pick a known Novation controller automatically, including on hot-plug.
Launchkey output uses its DAW port (needed for pad lighting); everything
else uses the plain MIDI port. An explicit None choice is respected.


## 5094966 · 2026-11-10

Default audio in/out to the device's built-in mic and speakers

With nothing chosen, pick the Mac's built-in mic/speakers (never a
Continuity iPhone mic), or the iPhone's own mic on iPhone, instead of
whatever the OS default is. Devices are listed on load when mic
permission persists, and after the mic starts. An explicit Default
pick is respected. The AudioContext is no longer created just to set
the output.


## 4fb7e06 · 2026-11-14

Highlight the latest detected note in yellow (Settings toggle)

In mic mode the most recently detected note is drawn yellow on its key
and its bar until a different note is detected or the counts reset.
Settings > Behavior > Latest note yellow turns it off; the choice is
remembered per browser. On by default.


## 12a2e94 · 2026-11-14

Show app version (v1.0) next to the title

Adds CLAUDE.md with the rule to bump it before every push to main.


## cadc144 · 2026-11-14

Rename app to Keytones, "tones" in the bar red; v1.1

Updates the header, page title, home-screen name and manifest. Saved
settings keep their old storage keys, so nothing is lost.


## d8c1839 · 2026-11-14

Add Noise gate, Confidence and Stability sliders (Settings > Detection); v1.2

- Noise gate (-80..-20 dB): minimum input level before detecting. Replaces
  the fixed RMS gate and FFT peak gate, and now also applies to the
  polyphonic algorithms (which had no gate and fired on pure noise).
- Confidence (0..100%): scales each algorithm's own certainty threshold;
  50% equals the previous fixed values.
- Stability (1..6 frames): consecutive frames a note must hold before it
  counts; now applies to polyphonic algorithms too.
- Gate level shown as a yellow tick on the mic level meter. Values are
  remembered per browser; Reset detection restores defaults.


## 26d9f61 · 2026-11-14

Gain up to +100 dB, Visualisation settings section, latest-note colour picker; v1.3

- Manual gain (topbar drag and Settings) now goes to +100 dB; auto-gain
  still stops at +40 dB.
- New Settings > VISUALISATION section with Decay, Latest note and
  Press states, moved out of BEHAVIOR.
- Latest note is now a picker: off / yellow / white / green / cyan
  (an earlier unchecked yellow box carries over as off).


## 1909b75 · 2026-11-14

Reorder Settings: Behavior, Detection, Visualisation, Audio, MIDI; v1.4


## d8646e5 · 2026-11-14

Sliders for Decay, Gain, Sound octave and MIDI out transpose; v1.5

They replace the dropdowns, update live, and stay in sync with the
topbar DECAY/GAIN drags and the Z/X octave keys. Slider rows get the
same height as dropdown rows.


## 0e8ed20 · 2026-11-14

Keep landscape iPhone UI clear of the notch; Side padding slider; v1.6

- The whole app (bars and keyboard too, not just the top bar and mic
  strip) is now inset by the left/right safe areas.
- The closed Settings panel no longer leaves a visible strip beside the
  notch (it kept its right inset at width 0).
- Settings > Visualisation > Side padding (0-80 px) adds extra margin on
  both sides; remembered per browser.


## 7063ef3 · 2026-11-14

Settings close button: same box and icon size as the settings button; v1.7


## 9aed88f · 2026-11-14

Swipe right on the Settings panel to close it; v1.8

The panel follows the finger and closes past a quarter of its width or
on a quick flick, otherwise springs back. Sliders, dropdowns and buttons
keep their own drags, and vertical scrolling is unchanged.


## 84d09ab · 2026-11-14

Top bar never scrolls: short labels on narrow screens; v1.9

When the full top bar doesn't fit (portrait phones), it switches to
KT / DCY / G with tighter spacing, then tighter padding, and only on
very narrow phones (~320 px with a long gain value) hides the version.
Re-checked on resize and whenever a value's text changes.


## 873cf5d · 2026-11-14

Mic on by default, default gain +50 dB; v1.10

The mic starts listening on page load. The AudioContext can start
suspended without a user gesture, so it's resumed on the first tap or
key press instead of blocking mic start-up.


## 806330c · 2026-11-14

Settings > COLORS: one palette shared by the app, Launchpad and Launchkey; v1.11

Pick colours for Notes, Latest note, Bar hit flash, C notes, Exact
octave and Pressed pad from red/orange/yellow/green/cyan/blue/purple/
magenta/white. Each palette colour has matched web RGB, Launchpad RGB
and Launchkey palette values, so the same choice looks the same on
screen and on the controllers. The latest note is now also shown in its
colour on Launchpad and Launchkey pads. Changes repaint a connected
controller immediately; colours are remembered, with a Reset button.
The earlier Latest note picker moves here and keeps its value.


## 0db3344 · 2026-11-14

Halftone glow slider for Launchpad sharps, now in both layouts; v1.12

The idle sharp/flat pads were only lit (dim white) in the fretboard
layout. They now glow in the piano layout too, with Settings >
Visualisation > Halftone glow (LP) setting the brightness (0-100 %,
default 22 % = the previous level). Changes repaint the Launchpad live.


## 7e8d7aa · 2026-11-14

Remove the bar hit flash and its colour setting; v1.13


## 4228ef5 · 2026-11-14

Move Gain into Settings > Detection, above Noise gate; v1.14


## 1790d47 · 2026-11-14

Colors: 'none' option for every role; v1.15

none = no highlight: Launchpad/Launchkey pads keep their idle colour
(C pads look like the others, no exact-octave or pressed colour), and on
screen Notes falls back to a neutral grey so bars stay readable. The
Latest note 'off' value carries over as 'none'.


## fbc8be3 · 2026-11-14

Halftone glow moves to Colors; new Natural glow slider for the other pads; v1.16

Natural glow (LP) sets the idle brightness of the natural-note pads
(0-100 %, default 3 % = the previous fixed level). Both glow sliders
are independent, update the Launchpad live and are remembered.


## 2dd8f85 · 2026-11-14

Swipe in from the right screen edge to open Settings; v1.17

Touches starting in the outer 18 px are reserved for the gesture, so the
key or bar underneath doesn't play; the panel opens after ~40 px of
mostly-horizontal leftward movement.


## 6ef6bf6 · 2026-11-14

Fix Settings labels overlapping their values on iOS landscape; v1.18

iOS was enlarging text in landscape (no text-size-adjust), so one-word
labels like Confidence ran into the value. Text size is now fixed, the
label never shrinks below its longest word, and the slider narrows instead.


## 29fb566 · 2026-11-14

Full range detection: exact-octave Launchpad pad uses the Latest note colour; v1.19

With full range on, the latest note's exact-octave pad is drawn in the
Latest note colour while its other octaves keep the Notes colour; other
still-sounding notes keep the Exact octave colour on their exact pad.
With 1 oct, every octave of the latest note uses the Latest colour, as
before.


## 0e2e8db · 2026-11-14

Fix crackle in generated sound: limiter bus, click-free release; v1.20

- All synth voices now go through a master limiter, so chords and held
  notes can't sum past full scale and clip (6 sine notes peaked ~1.8,
  now ~0.89).
- Note release holds the current level (cancelAndHoldAtTime) before
  fading, instead of re-reading .value, which can jump on Safari.
- Finished voices are disconnected, and the AudioContext uses a
  'balanced' latency hint for fewer dropouts on phones.


## 8eb6e83 · 2026-11-14

iOS crackle: open the mic before creating the AudioContext, at the mic's sample rate; v1.21

Opening the mic switches the iOS audio session; a context created before
that keeps the old settings and has to resample, which crackles. The mic
now opens first and the context is created at the mic track's sample
rate (an earlier context at another rate is replaced while nothing is
sounding).


## 2640046 · 2026-11-14

Settings > View: show an on-screen Launchpad instead of the bars; v1.22

The on-screen Launchpad Mini (9x9 with top/side buttons) shows exactly
what the app sends to a real Launchpad - same layout, colours, fades,
exact-octave and latest-note pads - and works without one connected.
Tapping it behaves like the real device: pads play notes, arrows shift
octave/transpose, Keys/User switch layout, side buttons pick the
waveform, Stop Solo Mute resets. With a real Launchpad connected both
stay in sync. The choice is remembered.


## 24828a3 · 2026-11-14

On-screen Launchpad: remove the frame and its paddings; v1.23


## 77e5fd5 · 2026-11-14

Algorithm row fills the strip edge to edge (no padding); v1.24

The buttons now cover the whole strip, which is also the keyboard resize
handle, so a press on a button turns into a resize once it moves 8 px
up or down (and then doesn't pick the algorithm). The compact picker on
narrow screens keeps a small side margin.


## 9dd6212 · 2026-11-14

On-screen Launchpad: no background behind or around the grid; v1.25


## eac0992 · 2026-11-14

Stop the Latest note colour flickering with chord algorithms; v1.26

Chord detection (P1-P4) can drop a held note for a frame and report it
again, which counted as a new note and moved the Latest colour every
time. A note now only becomes the latest after 600 ms of silence, and
of several new notes in one frame the strongest wins.


## e8679d7 · 2026-11-14

Settings > Audio > Phone call mode (off by default); v1.27

Off: the mic opens without call-style processing (echo cancellation,
noise suppression, auto gain) - also for the device-list probe, which
used the browser defaults - and on iOS 17+ the audio session switches
back to plain playback whenever the mic is off. On: call-style
processing, which picks up less of the app's own sound. Switching it
reopens the mic; the choice is remembered.


## 841d1bd · 2026-11-14

Latest note colour stays pinned on Launchpad/Launchkey, like the key and bar; v1.28

The on-screen key and bar keep the Latest colour until another note
becomes the latest, but on the controllers it faded out with the decay
(and the Launchkey dropped it on note-off), so the yellow was missing or
on a different note there. It now stays at full on the controllers too,
the previous latest is always repainted back, and it survives layout,
glow and colour repaints.


## fe792c8 · 2026-11-14

Keyboard mirrors the Launchpad's exact-octave colour (full range); v1.29

With full range detection in mic mode, every detected note's key now
glows in the Exact octave colour and fades exactly like its exact-octave
Launchpad pad; the latest note keeps its solid Latest colour. Note
fade state is tracked even without a Launchpad connected.


## b502bcd · 2026-11-14

Full range: the latest note fades like the exact-octave notes; v1.30

With full range detection the latest note is no longer pinned: its key
and its exact-octave Launchpad pad glow in the Latest colour and fade
with Decay exactly like the green exact-octave notes, then disappear.
With 1 oct the latest note stays pinned as before.


## 07aa7a1 · 2026-11-14

Press states becomes the Pressed pad colour picker (none = off); v1.31

The separate Press states yes/no setting is gone: Settings > Colors >
Pressed pad (LP) now decides both whether a pressed Launchpad pad lights
up and in which colour. Default none, matching the old default of no.


## 7296075 · 2026-11-14

Tap anywhere on the app to close Settings; v1.32

While Settings is open, a transparent layer covers the app area: a tap
there closes the panel and doesn't also play a key or press a button.


## 0dd390a · 2026-11-14

Full range: only the latest note is marked (yellow); Exact octave colour removed; v1.33

In full range mode the latest note's exact-octave pad and its key glow in
the Latest colour and fade; other detected notes are no longer marked in
a separate exact-octave colour (their pads use the Notes colour like all
their octaves). The Exact octave colour setting is gone; the Stop Solo
Mute button keeps a fixed purple.


## b905e70 · 2026-11-14

Latest note also follows the keys you play, with the mic on or off; v1.34

Tapping an on-screen key, the computer keyboard or a MIDI-in note now
makes it the latest note (yellow on the key, bar and Launchpad), and the
latest note is shown with the mic muted too. Launchpad pad presses keep
their own Pressed pad colour and don't move it.


## f6b1ac3 · 2026-11-14

Several latest notes at once for chords; v1.35

Notes that start within 250 ms of each other count as one chord and are
all shown in the Latest colour (keys, bars, Launchpad, Launchkey) -
from the chord algorithms (P1-P4) and when you play a chord on the keys
or a MIDI keyboard. The next note or chord after a pause replaces them.
Single-note algorithms still mark one note.


## c55f7ea · 2026-11-14

Clearer names in Settings > Colors; v1.36

Notes -> Sounding notes, Latest note -> Newest notes; controller-only
settings grouped under 'Pads · Launchpad / Launchkey': C pads, Pad press,
Idle sharp/flat pads, Idle natural pads (no more LP/LK suffixes), with a
note on which apply to the app vs the controllers.


## 0e7004d · 2026-11-15

Launchpad piano layout: the C at the right end of a row is the next octave; v1.37

Each row of the piano layout ends with a second C, which was treated as
the same octave as the C at the row's start - so it lit up as the exact
octave together with it and played the lower C. It is now the C one
octave up (the same note as the first C of the row above).


## 72beb04 · 2026-11-15

Reset (Stop Solo Mute / title tap) also clears the Launchpad and keys; v1.38

Reset only cleared the bars: the Launchpad pads (real and on-screen),
the Launchkey and the key glow kept fading, and the newest notes stayed
marked when the mic was off. Now everything is cleared, except notes
that are still being held or heard.


## 2fa984c · 2026-11-15

On-screen Launchpad: unlit pads are transparent; v1.39

The gaps in the piano layout (and any pad that is fully off) are no
longer drawn as dark squares.


## 476aa67 · 2026-11-15

Launchpad: idle waveform side buttons dim grey like the arrows, not blue; v1.40

Applies to the real Launchpad and the on-screen one.


## fd70189 · 2026-11-15

Reset button (Stop Solo Mute): white, shown as an X on the on-screen Launchpad; v1.41


## 8f74dbd · 2026-11-15

Faster detection: Speed slider (Settings > Detection), newest audio; v1.42

- Time-domain detectors (M2-M5, P3) now analyse the newest 2048 samples
  of the buffer instead of the oldest, removing up to ~130 ms of lag.
- New Speed slider (1-5): detection interval 100->25 ms, spectrum size
  8192->2048 and smoothing 0.8->0.2. Default 3 (50 ms, 4096). Measured
  time to detect a new note: YIN 262 ms -> ~95-145 ms, Multi-F0
  ~690-790 ms -> ~190 ms at 3, ~70-80 ms at 5. Higher speeds are less
  accurate for low notes and chords.


## 1291d3e · 2026-11-15

Mic badge keeps a fixed width (ON / LIVE / MUTED no longer resize it); v1.43


## d653abf · 2026-11-15

Mic badge: always LIVE; green = listening, orange = a note is heard; v1.44

The badge no longer switches between ON and LIVE. The dot and the level
fill turn orange while a note is being detected and green otherwise.


## 9fc2071 · 2026-11-15

Noise gate slider shows the live mic level; v1.45

While Settings is open the gate slider's track fills up to the current
input level (after gain, same scale as the gate): green when the sound
gets through the gate, grey when it's below it.


## be8bd02 · 2026-11-15

Remove the noise-gate tick from the mic badge (showed as yellow edges); v1.46

The gate is shown in the Noise gate slider's live meter now.


## a36ed10 · 2026-11-15

Per-note detection confidence; option: bar opacity = confidence; v1.47

Every detector now reports how certain it is (0-1): YIN 1-d', MPM
clarity, ACF correlation, AMDF dip depth, FFT peak height above the
gate, HPCP/NNLS/CQT relative strength, Multi-F0 relative harmonic
score. The last confidence per note is kept, and Settings >
Visualisation > Bar opacity = confidence (off by default) draws each
bar at that opacity in mic mode. Reset clears it.


## 07c3833 · 2026-11-15

Remove the Side padding setting; v1.48

The notch / safe-area insets are still kept clear automatically.


## e684d17 · 2026-11-15

Decay no longer shrinks notes that are still sounding; v1.49

At Decay 100% a held key or a note the mic still hears lost its bar
every second. Decay now only applies to notes that have stopped; a held
key's time keeps growing normally until it's released.


## d6e889b · 2026-11-15

Info icons with explanations for every setting; v1.50

Each Settings label has an (i) icon: hovering it with a mouse or tapping
it shows a short explanation in a floating tip; tapping elsewhere or
scrolling hides it. Tapping the icon doesn't change the setting. The
long help paragraphs under Detection and Colors are replaced by these.


## 4404ecf · 2026-11-15

Settings: Visualisation before Detection; v1.51


## 9d7390b · 2026-11-15

Settings > View: grouped switch (Bars | Launchpad) instead of a dropdown; v1.52


## a0fde73 · 2026-11-15

Tap-outside-to-close Settings only on phone-sized screens; v1.53

On wider screens (over 760 px) the app next to the open panel stays
fully usable; on phones a tap on the app still closes the panel.


## e333dd2 · 2026-11-15

Computer keyboard reaches further: K L ; ' (+ O P ] \) play the next octave; v1.54

Keys are now matched by physical position (e.code), so the layout works
the same on QWERTY, QWERTZ and other keyboards. Home row A..' plays
C D E F G A B C D E F, the row above W E T Y U O P ] the sharps, the
right-hand keys one octave up. Z/X still shift the octave; shortcuts
with Cmd/Ctrl/Alt and typing in text fields are left alone.


## 850ff36 · 2026-11-15

Topbar view toggle between GAIN and Settings: grid/keys icon switches Bars <-> Launchpad view; v1.55


## 4881c48 · 2026-11-15

Settings: Detection + Algorithm move into the Detection section (Behavior section removed); v1.56


## 508e0d0 · 2026-11-15

Settings: 'Noise gate' renamed to 'Gate'; v1.57


## 2f1c04d · 2026-11-15

Settings panel 400px wide on desktop (mouse + window >= 900px), phones keep 300px; v1.58


## 20c5eab · 2026-11-15

Detection bench (bench/): runs the real app on synthetic labelled clips via Chrome's fake mic, logs every detection frame, scores F1 / latency / ghost notes / level sensitivity per algorithm; baseline for v1.58; v1.59


## 5305330 · 2026-11-15

Chord detection: noise-floor-relative spectral peaks shared by the polyphonic algorithms; v1.60

- Multi-F0 rewritten on harmonic peaks: works at any input level (was deaf below ~-12 dBFS),
  chord F1 0.18 -> 1.00, range down to E1, claims its upper partials so bass notes don't
  spawn extra notes
- NNLS / CQT+NMF keep only pitches backed by real peaks: no notes from noise (was 100%),
  far fewer neighbouring-semitone extras (wrong notes 57% -> 20%, 51% -> 10%)
- HPCP uses the same peaks: works from -30 dBFS (was -12)
- mains hum (peaks on multiples of 50/60 Hz) is filtered out
- bench: hum scored separately from pink noise, compare.py, multi-run reports


## 81fcd8b · 2026-11-15

Bench: synthetic distorted band clips (power chords, open chords, palm mutes + bass + drums), --app to test older versions, band column in reports; band results for v1.60; v1.61


## 8968406 · 2026-11-15

Algorithm cards: hover an algorithm button (long-press on touch) or Settings > Algorithm ⓘ for what it does, 1-5 star ratings (single notes, chords, full band, speed, noise & hum, quiet input, CPU) from the bench, best-for and watch-out notes; v1.62


## c6388e6 · 2026-11-15

Algorithm cards keep one size: every section takes the height of its tallest version across all cards (re-measured when the width changes), so moving along the buttons doesn't make the card jump; v1.63


## ed64b00 · 2026-11-15

Settings > Visualisation > Bars show: Live (sounding now, height = confidence, yellow = clearly strongest), Time (how long each note sounded, now also with the mic), Count (how often it started — the old mic behaviour), Chroma (energy per note name before detection, detected in yellow); v1.64


## 3bc8783 · 2026-11-15

Keyboard mirrors the bars in Bars show: Live / Chroma (yellow = the bars' yellow notes, red = other sounding notes) instead of the newest-note marking; detected notes always get a visible Chroma bar; v1.65


## 8fb7eec · 2026-11-15

Colors: new defaults (C pads white, pad press magenta, idle ♯/♭ pads 15%, idle natural pads 50%), Newest notes listed above Sounding notes, Reset colors also resets the idle pad levels; v1.66


## b057668 · 2026-11-15

Notes played from the keys, computer keyboard or MIDI in light their exact-octave pad in the Pad press colour (Launchpad view and real Launchpad), and held piano keys use the Pad press colour too, in both views; v1.67


## 659cc0c · 2026-11-15

Mouse / touchpad glide: hold the button and move across the keys, bar columns or on-screen Launchpad pads to play each note in turn (previous one released); v1.68


## 9a4613b · 2026-11-15

View picker: Piano | Pi-auto | LP. Pi-auto = one bar per real note (C3, C4…) over a piano strip; starts as one octave, the first note picks the octave, notes outside the range add whole octaves (only grows, clicking the title resets to 12 bars); all Bars show modes work per note; the strip plays exact octaves with mouse glide; v1.69


## cac4c2e · 2026-11-15

Smooth Decay: runs every display frame with a time-based factor (same speed per second, no 1-second steps); real Launchpad fades repainted at most every 50 ms; v1.70


## b43561a · 2026-11-15

Settings > Detection > Listen to: Mic | App sound | Mic + app sound — routes the app's own synth output straight into the detector (no mic, fixed level) to check detection accuracy on known notes; badge shows APP; v1.71


## e1adc89 · 2026-11-15

Settings > Detection: audio file player (load wav/mp3…, play/pause, ±15 s, time slider); Listen to: Audio file feeds it straight into the detector (and plays it); loading a file switches to it and turns detection on; badge shows FILE; v1.72


## 528b381 · 2026-11-15

Audio file player shows only with Listen to: Audio file; v1.73


## f3b7c05 · 2026-11-15

File player: accepts video and more audio formats (mp4, mov, webm, mkv, m4a, flac, ogg, opus, aiff…, via the browser's own decoders — no added code size); unplayable files say so; v1.74


## a756825 · 2026-11-15

Computer keyboard plays notes with the Settings panel open (a focused dropdown / slider / button no longer blocks it; letter keys don't change the focused dropdown); v1.75


## 3deb44a · 2026-11-15

Live bars fall back at the Decay rate after their note stops (peak hold), in Piano and Pi-auto; label shows the level now; reset clears them; v1.76


## fcdf13d · 2026-11-15

Bar opacity = confidence in Pi-auto too (Time / Count), per real note; works with detection on from mic, app sound or file; clearer setting explanation; v1.77


## a77310d · 2026-11-15

Settings that have no effect right now are greyed out with the reason on hover / tap: Gain (+ topbar GAIN), Phone call mode, Audio in (Listen to: App sound / Audio file), Bars show (LP view), Bar opacity = confidence (LP view, Live, Chroma, detection off); v1.78


## e2269d4 · 2026-11-15

Colors: the colour preview sits inside each dropdown, before the colour name; v1.79


## c15bddc · 2026-11-15

Newest fades (Settings > Colors, default 2 s): a newest note blends from the Newest into the Sounding colour over time on bars (Time / Count, Piano + Pi-auto), keys and Launchpad pads; key colour changes cross-fade (pressing stays instant); v1.80


## 9080fe5 · 2026-11-16

Settings > Colors > Transition slider (off–1.5 s, default 0.4 s): cross-fade time for key and bar colour changes; Reset colors restores it; v1.81


## 76e20c5 · 2026-11-16

Transition also on the pads: real Launchpad and LP view cross-fade colour changes in 50 ms steps over the Transition time; a note lighting up and pad presses stay instant; v1.82


## d9beb5d · 2026-11-16

Settings > Detection: Speed moved below Gain and Gate; Gate level meter is white (gets through) / grey (blocked) instead of green; v1.83


## ded0b11 · 2026-11-16

Topbar: status dot moved left of the app title; separate mute button right of GAIN (mic icon / red crossed-out mic when muted); narrowest phones hide the status badge; v1.84


## ada7258 · 2026-11-16

Bars show defaults to Live; v1.85


## 92f8484 · 2026-11-16

Settings > Visualisation > Keys: Piano (white/black) or Like bars (idle keys take the bar columns' colours, black keys with the same 25% shade); also the Pi-auto strip; v1.86


## 321d4fa · 2026-11-16

Listen to gets None (= detection off); the topbar mute button is replaced by a mini Listen-to picker with icons (None, Mic, App sound, Mic + app sound, Audio file), in sync with Settings, the badge and Settings > Mic; Mic + app sound falls back to the app sound when there is no mic; v1.87


## 0737fd5 · 2026-11-16

Listen-to sheet in the top bar shows icon + name for each choice, aligned under the button's right edge; v1.88


## 627dd5e · 2026-11-16

Pressed + detected notes flash between the Pad press and detected colours; v1.89

A note you're holding (keys, computer keyboard, MIDI in, Launchpad pad)
that detection also hears now alternates every 250 ms between the Pad
press colour and its detected colour (Sounding, or Newest when it's the
newest note) - on the keys, the Pi-auto strip and the Launchpad pads.
Held keys also keep the Pad press colour while the bars mark them.


## 0fef0bb · 2026-11-16

Faster flashing (100 ms), and bars flash too; v1.90

A pressed + detected note now flashes every 100 ms between the Pad press
colour and its detected colour on the keys, the bars (12-note and
Pi-auto) and the Launchpad pads (real and on-screen); colour fades are
skipped while a bar flashes.


## 512e391 · 2026-11-16

No Decay afterglow for played notes; v1.91

A note you play (on-screen keys, computer keyboard, MIDI in) no longer
lingers on its key and Launchpad pads after release - they go straight
back. Decay still applies to the bars and to what detection hears.


## 1feabf9 · 2026-11-16

Keys fade with Decay exactly like the Launchpad pads; v1.92

Every detected note's key now glows in the Sounding colour (Newest for
the newest note) and fades with Decay in step with its Launchpad pads,
instead of only the newest note in full range. While the bars mark a
note live, the key keeps that colour; the fade takes over once it stops.


## f2e48ed · 2026-11-16

Finger glide on touch screens: slide across keys, bars, the Pi-auto strip and on-screen Launchpad pads; v1.93

Draw-playing only worked with a mouse / touchpad. Now each finger can
slide too: the note under it plays and the previous one is released;
lifting the finger releases the last one. Works with several fingers.


