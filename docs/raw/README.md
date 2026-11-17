# raw/ — immutable sources

Source material the wiki is built from. **Never edit a file here**: add a new
file instead (e.g. a newer snapshot next to an older one). The wiki pages in
`../wiki/` cite these files by name.

| file | what |
|---|---|
| `git-history-v1.93.md` | every commit message from v0 to v1.93 — the decision log |

Also treated as raw sources (kept where they live, not copied):

| path | what |
|---|---|
| `../../index.html` | the app itself — ground truth for behaviour and defaults |
| `../../bench/README.md`, `../../bench/baseline-v*.md`, `../../bench/band-v*.md` | detection bench method and measured results |
| `../../CLAUDE.md` | project rules (versioning, this wiki's schema) |

To ingest something new (a hardware manual, a user report, a screenshot
description, a new bench run): drop it here with a descriptive name, then
follow the **Ingest** workflow in `../../CLAUDE.md`.
