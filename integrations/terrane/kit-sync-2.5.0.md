---
id: terrane-kit-sync-2.5.0
from: terrane
to: autonomous
status: filed
ball: provider
repo_path: ~/Documents/Claude/synthetic-worlds/terrane
re: kit_sync to 2.5.0 — please verify against the tree
---
kit_sync reports `version-stale` at kit 2.5.0 for `~/Documents/Claude/synthetic-worlds/terrane`.

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

## Why this receipt does not read `current`

`kit_sync --notify` is READ-ONLY: it reports the state it finds and never
changes it, because a report must not change what it reports. So this state
(`version-stale`) will persist until someone runs the write step. The order is:

    python3 <kit>/kit_sync.py <repo>     # WRITE: sync .kit/ + MANIFEST
    git add .kit && git commit           # your repo, your commit
    python3 <kit>/kit_sync.py <repo> --notify   # REPORT: file this receipt

Filed as-is because an accurate report of a stale tree is worth more than a
tidy one — but it is not the finished state, and autonomous will dispute it.

## From the filer

Retrofit from pre-2.0.0 (behind by 5). Notable: .kit/ was already vendored and checksum-current but UNTRACKED and UNSOURCED — no ./verify existed to source it — so the repo would have read current by checksum while completely unprotected in a clone or CI. Now committed and sourced. Kit advanced to 2.5.0 mid-session; .gitattributes was already tracked, so that was a declaration bump only. Committed c56d5dc on main; not pushed (pushes are the human's).
