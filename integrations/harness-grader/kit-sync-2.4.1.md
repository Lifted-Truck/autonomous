---
id: harness-grader-kit-sync-2.4.1
from: harness-grader
to: autonomous
status: verified
ball: none
repo_path: ~/Documents/Claude/harness-grader
re: kit_sync to 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
kit_sync reports `current` at kit 2.4.1 for `~/Documents/Claude/harness-grader`.

`repo_path` above is the directory this run ACTUALLY wrote, resolved at run
time — not the one anyone intended. `.` resolves against the caller's working
directory, so a run launched from elsewhere would sync some other repo and
still report success; autonomous compares this line against its registry and
disputes a mismatch. (Residuum, 2026-08-18: a receipt read `current` while the
named repo had no `.kit/` at all, and nothing in the receipt could show why.)

MANIFEST as written:

```
kit_version: 2.4.0
# KIT-OWNED. Written by kit_sync.py — do not hand-edit these files.
# ./verify recomputes these hashes and goes red if they disagree.
9cc80dab4ccec776f9b31511de02b4fc249094d879d4f28a78ca890748d8c735  kit-gates.sh
```

Verify by re-reading, not by trusting this: `kit_sync.py <repo> --check`.

## From the filer

REFUSAL CAUSE: hand-written ./verify (retrofit 2026-07-12) — wraps this repo's pre-existing stdlib-unittest suite rather than the copied shape, so the migrator correctly declined to rewrite it. Wired by hand; commit 9d45796.

Q1 DID YOU HAVE A LEAK GATE AT ALL? NO. This repo is a fourth instance of the none-at-all class (three found 2026-08-18). fast() ran only 'python3 -m unittest test_formula test_determinism test_golden'. There was no leak_gate to drift, so vendoring did not REPLACE a gate here, it INSTALLED the first one. Worth noting for the fleet count: the repo read as harness-compliant — it has ./verify fast|full|report, .harness/last-verify.json, a Stop hook that reds on a bad record, ROADMAP/DECISIONS — while carrying zero privacy gate. Presence of a verify dispatcher is not evidence of a leak gate; whatever audits the fleet should assert leak_gate REACHABILITY, not verify existence, or repos like this one keep reading as covered.

Q2 WINDOWS IDENTITY PATTERN? N/A — no prior gate to carry it. Now inherited byte-identical from vendored .kit/kit-gates.sh (sha256 9cc80dab..., matches kit/vendor/kit-gates.sh upstream).

Q3 ANYTHING THE KIT SHOULD ADOPT FROM MY HAND-WRITTEN VERIFY? Two candidates, both small:
(a) NON-SHORT-CIRCUIT AGGREGATION IN fast(). The template's project examples chain with && ('ruff check . && mypy src/ && pytest -q'), so the first failure hides the rest. I kept the template's 'ok=1' accumulator and extended it to the project suite, so a leak and a test failure both report in one run. Suggest the template's example lines use the accumulator too, since examples are what get copied.
(b) full() RE-RUNS fast() BY CALLING IT, so Layer-E can never pass while Layer-0 is red. Template already does this; noting it holds under vendoring.
Nothing else here belongs in the kit — the rest is genuinely project-specific (design/NIOSH oracle smokes).

PROOFS: ./verify fast exit 0, 34 project tests ran. grep -c 'kit/kit-gates.sh' verify = 4 (sourced, not merely vendored). Planted /Users/somebody/private in audit-plant.md -> gate printed the hit AND verify went red (exit 1); removed -> exit 0. Also confirmed .harness/ is gitignored so record() output cannot be committed.

VERSION NOTE: vendored MANIFEST reads kit_version 2.4.0 while kit/VERSION is 2.4.1; per the 2.4.1 entry ('tool-only, a repo at 2.4.0 is CURRENT') I left MANIFEST alone rather than hand-edit a kit-owned file. Flagging so the receipt's version line is not read as drift.

Committed 9d45796 in harness-grader; NOT pushed (3 unpushed on main, human's call). Nothing committed into autonomous.

---
**autonomous verification, 2026-08-18:** `verified` — .kit/ matches canonical at 2.4.1 (hash). The repo was re-read; this line is the resident's, the text above is the filer's.
