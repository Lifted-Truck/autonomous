---
id: attest-kit-sync-2.4.1
from: attest
to: autonomous
status: verified
ball: none
repo_path: ~/Documents/Claude/attest
re: kit_sync to 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
kit_sync reports `current` at kit 2.4.1 for `~/Documents/Claude/attest`.

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

Retrofit from pre-2.0.0, behind by 5. No ./verify existed, so migrate_to_vendored SKIPped and verify was written from kit/templates/verify.project with the project gates wired by hand (ruff + pytest -m layer0). Layer-E deliberately NOT in the oracle: it makes billed calls and the truth contract says Layer-E is measured, never gated. The 83-row decisions table moved out of ROADMAP.md into DECISIONS.md verbatim.

---
**autonomous verification, 2026-08-18:** `verified` — .kit/ matches canonical at 2.4.1 (hash). The repo was re-read; this line is the resident's, the text above is the filer's.
