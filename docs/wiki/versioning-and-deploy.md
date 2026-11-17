---
title: Versioning and deploy
summary: Version bump rule, branches, GitHub Pages deploy.
sources: [CLAUDE.md, raw/git-history-v1.93.md]
updated: v1.93
---

# Versioning and deploy

- The title shows `vX.Y` (`#app-version`). **Every push to `main` bumps it** — minor for any
  change, major only when the user calls it a new version (rule in [`CLAUDE.md`](../../CLAUDE.md)).
- `main` is deployed by GitHub Pages to <https://umilan.github.io/keytones/> within ~1–2 minutes
  (Actions → "pages build and deployment"). A superseded deploy shows as *cancelled* — normal.
- Commit messages describe the change and its reason; they are the decision log
  (snapshot in [`raw/git-history-v1.93.md`](../raw/git-history-v1.93.md)).
- Related repo: `umilan/keytones-ios` (Swift `KeytonesEngine` package, separate work).
