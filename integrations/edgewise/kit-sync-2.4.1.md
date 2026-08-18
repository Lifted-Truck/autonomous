---
id: edgewise-kit-sync-2.4.1
from: edgewise
to: autonomous
status: filed
ball: provider
repo_path: ~/Documents/Claude/synthetic-worlds/edgewise
re: kit_sync to 2.4.1 — please verify against the tree
---
kit_sync reports `current` at kit 2.4.1 for `~/Documents/Claude/synthetic-worlds/edgewise`.

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

Retrofit pre-2.0.0 -> 2.4.1 by the EDGEWISE resident. All 5 CHANGELOG entries closed. ./verify is project-owned over vendored gates and wraps the pre-existing TS oracle (E1-E4); nothing was red so nothing was quarantined. Gate-fires proved on both POSIX and Windows plants. Committed db78122 on main; NOT pushed (pushes are the human's).
