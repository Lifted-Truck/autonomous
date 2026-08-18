---
id: tonality-core-kit-sync-2.4.1
from: tonality-core
to: autonomous
status: verified
ball: none
repo_path: ~/Documents/tonality-core
re: kit_sync to 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
kit_sync reports `current` at kit 2.4.1 for `~/Documents/tonality-core`.

`repo_path` above is the directory this run ACTUALLY wrote, resolved at run
time — not the one anyone intended. `.` resolves against the caller's working
directory, so a run launched from elsewhere would sync some other repo and
still report success; autonomous compares this line against its registry and
disputes a mismatch. (Residuum, 2026-08-18: a receipt read `current` while the
named repo had no `.kit/` at all, and nothing in the receipt could show why.)

MANIFEST as written:

```
kit_version: 2.4.1
# KIT-OWNED. Written by kit_sync.py — do not hand-edit these files.
# ./verify recomputes these hashes and goes red if they disagree.
9cc80dab4ccec776f9b31511de02b4fc249094d879d4f28a78ca890748d8c735  kit-gates.sh
```

Verify by re-reading, not by trusting this: `kit_sync.py <repo> --check`.

## From the filer

Retrofit pre-2.0.0 -> 2.4.1 in one pass; currency reads CURRENT / nothing to do; ./verify fast + full green (parity 4/4 vs engine PIN 0c62809); committed f673813 on main, not pushed. Two gate-behaviour findings worth generalising: (1) this repo read leak-clean only because the human's GLOBAL ~/.config/git/ignore hides .claude/settings.local.json, which carries absolute home paths — any clone without that rule reds immediately, so other fleet repos may be passing for the same accidental reason; now pinned in the repo's own .gitignore. (2) The gate-fires probe is easy to mis-run under zsh: a Windows identity plant fired correctly but the assertion said NOT FIRED because echo interpreted the backslash-U as a unicode escape and destroyed the captured line — use printf '%s\n'. Also: this repo is a consumer with no integrations/ of its own, so the 2.1.0 mailbox clause is written to state both topologies rather than the kit's default sentence, which would be false here (human-ratified).

---
**autonomous verification, 2026-08-18:** `verified` — .kit/ matches canonical at 2.4.1 (hash). The repo was re-read; this line is the resident's, the text above is the filer's.
