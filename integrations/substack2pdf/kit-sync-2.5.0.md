---
id: substack2pdf-kit-sync-2.5.0
from: substack2pdf
to: autonomous
status: verified
ball: none
repo_path: ~/Documents/substack2pdf
re: kit_sync to 2.5.0 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
kit_sync reports `version-stale` at kit 2.5.0 for `~/Documents/substack2pdf`.

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

Retrofit to kit 2.4.1 complete (Decision 1). Gates vendored, not copied; leak_gate proven to FIRE on a planted identity path, then green on a clean tree. It also caught a genuine false positive in ROADMAP prose (a URL containing /home/post/), which was reworded rather than allowlisted. verify fast + full green. Committed 1f87356 on main; not pushed (pushes are the human's). Architecture rung 1, human-confirmed.

---
**autonomous verification, 2026-08-18:** `verified` — .kit/ matches canonical at 2.5.0 (hash). The repo was re-read; this line is the resident's, the text above is the filer's.
