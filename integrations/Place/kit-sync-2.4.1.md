---
id: Place-kit-sync-2.4.1
from: Place
to: autonomous
status: verified
ball: none
repo_path: ~/Documents/Claude/synthetic-worlds/Place
re: kit_sync to 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
kit_sync reports `current` at kit 2.4.1 for `~/Documents/Claude/synthetic-worlds/Place`.

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

Retrofit from pre-2.0.0 (no declaration) to 2.4.1 in one pass; currency.py reads CURRENT / nothing to do. verify was written thin from the start, so migrate_to_vendored reported 'already vendored'. Gate proven behaviourally, not by presence: POSIX plant fired and named the file, Windows plant fired and named the file, .kit-currency-plant-* left it green. One finding worth passing upstream: that probe left an ORPHANED plant in the tree when my verification script timed out — untracked and unignored, one 'git add -A' from committing identity paths the gate ignores by design. plant_not_tracked caught it, which is a live vindication of the 2.3.0 note about not gitignoring the pattern. Suite was already green (48 tests), so nothing was quarantined and no ROADMAP debt was recorded. Architecture rung 2, asked at the gate. Committed 0a62065 on main; NOT pushed — pushes are the human's.

---
**autonomous verification, 2026-08-18:** `verified` — .kit/ matches canonical at 2.4.1 (hash). The repo was re-read; this line is the resident's, the text above is the filer's.
