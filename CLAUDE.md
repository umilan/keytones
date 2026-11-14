# Keymap (keytones)

Single-file PWA: everything lives in `index.html`, served by GitHub Pages from `main`.

## Version number

The app shows its version next to the title: `<span class="app-version" id="app-version">vX.Y</span>` in `index.html`.

Before every push to `main`, bump it:
- new feature or visible change: minor (`v1.0` → `v1.1`)
- a bigger change the user calls a new version: major (`v1.9` → `v2.0`)

Bump once per push, in the same commit as the change (or the last commit of the push).
