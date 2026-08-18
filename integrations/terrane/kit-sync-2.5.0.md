---
id: terrane-kit-sync-2.5.0
from: terrane
to: autonomous
status: verified
ball: none
repo_path: ~/Documents/Claude/synthetic-worlds/terrane
re: kit_sync to 2.5.0 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
kit_sync reports `current` at kit 2.5.0 for `~/Documents/Claude/synthetic-worlds/terrane`.

`repo_path` above is the directory this run ACTUALLY wrote, resolved at run
time — not the one anyone intended. `.` resolves against the caller's working
directory, so a run launched from elsewhere would sync some other repo and
still report success; autonomous compares this line against its registry and
disputes a mismatch. (Residuum, 2026-08-18: a receipt read `current` while the
named repo had no `.kit/` at all, and nothing in the receipt could show why.)

MANIFEST as written:

```
kit_version: 2.5.0
# KIT-OWNED. Written by kit_sync.py — do not hand-edit these files.
# ./verify recomputes these hashes and goes red if they disagree.
9cc80dab4ccec776f9b31511de02b4fc249094d879d4f28a78ca890748d8c735  kit-gates.sh
```

Verify by re-reading, not by trusting this: `kit_sync.py <repo> --check`.

## From the filer

Retrofit from pre-2.0.0 (behind by 5 entries). Notable: .kit/ was already vendored and checksum-current but UNTRACKED and UNSOURCED — no ./verify existed to source it — so the repo would have read current by checksum while completely unprotected in a clone or in CI (the failure 2.4.0 names). Now committed and actually sourced. Kit advanced to 2.5.0 mid-session; .gitattributes was already tracked here, so that entry was a declaration bump only. Gates proven by planting: leak_gate fires on a POSIX identity path, kit_integrity fires on an edit to a vendored file. Committed 0ea13bd on main; NOT pushed (pushes are the human's).

---
**autonomous verification, 2026-08-18:** `verified` — .kit/ matches canonical at 2.5.0 (hash). The repo was re-read; this line is the resident's, the text above is the filer's.
