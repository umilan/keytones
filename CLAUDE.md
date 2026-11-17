# Keytones

Single-file PWA: everything lives in `index.html`, served by GitHub Pages from `main`.

## Version number

The app shows its version next to the title: `<span class="app-version" id="app-version">vX.Y</span>` in `index.html`.

Before every push to `main`, bump it:
- new feature or visible change: minor (`v1.0` → `v1.1`)
- a bigger change the user calls a new version: major (`v1.9` → `v2.0`)

Bump once per push, in the same commit as the change (or the last commit of the push).

## Documentation wiki (LLM-maintained)

Project knowledge lives in `docs/`, following the "LLM wiki" pattern: the agent writes and
maintains the wiki; people read it and add sources.

- `docs/raw/` — **immutable sources** (commit-history snapshots, hardware manuals, user reports,
  bench runs). Never edit; add a new file. `docs/raw/README.md` lists them. The app
  (`index.html`) and `bench/` are also sources, kept where they are.
- `docs/wiki/` — **the wiki**: one markdown page per topic, written by the agent.
  - `index.md` — catalog: one line per page (link + summary). Read it first; keep it in sync.
  - `log.md` — append-only history: `## [YYYY-MM-DD] <ingest|query|lint> | <subject>` + what changed.
- This section is the **schema**: conventions and workflows below.

### Page conventions
- Front matter: `title`, `summary` (one line, same as in `index.md`), `sources` (raw files /
  code it is based on), `updated` (app version it describes).
- Plain words first, then specifics (defaults, constants, function names). Tables for settings.
- Link between pages with relative links (`[Colors](colors.md)`), never absolute URLs.
- State facts the code or a source supports; when unsure, say so on the page.
- Lower-case, hyphenated file names (`audio-sources.md`). One topic per page; split when a page
  passes ~150 lines.

### Workflows
- **Ingest** (a new source, or a code change): put the source in `docs/raw/` if it's external;
  read it; update every affected page (often several) and their `updated` version; add new
  pages for new topics; update `index.md`; append a `log.md` entry.
  **Every push that changes app behaviour also updates the wiki** in the same commit — the
  pages for the touched features, their `updated` version, and `log.md`.
- **Query**: answer from `index.md` → relevant pages (→ code only if the wiki lacks it). If the
  answer is reusable, file it back into a page and log it.
- **Lint** (when asked, or every ~10 versions): check pages against `index.html` (defaults,
  settings list vs `SETTING_INFO`, removed features), broken links, pages missing from
  `index.md`, contradictions between pages, stale `updated` versions; fix and log.
