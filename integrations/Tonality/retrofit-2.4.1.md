---
id: Tonality-retrofit-2.4.1
from: Tonality
to: autonomous
status: verified
ball: none
filed: 2026-08-18
re: retrofit to kit 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---

Retrofit to 2.4.1 complete. currency.py output at close:

```
kit currency — ~/Documents/Tonality
  kit: 2.4.1   declared: 2.4.1   CURRENT
  nothing to do — re-running the retrofit is a no-op
```

Committed: 4e2a55b on retrofit-kit-2.4.1 (retrofit itself f411ea8). Pushed: no — pushes are the human's.

Opened BEHIND by 5 entries (declared pre-2.0.0). Closed all of them:
2.4.0 vendored (kit_sync + migrate), which answered 2.2.0/2.3.0 by
checksum; 2.0.0 baseline gained ./verify, project.manifest.json,
DECISIONS.md and traces/; 2.1.0 gained a marker-delimited ## Mailbox.

Gate behaviour proven rather than asserted: ./verify SOURCES
.kit/kit-gates.sh (no gate code copied into the repo), POSIX and Windows
identity plants each fire and name the file, a TRACKED
.kit-currency-plant-* fires plant_not_tracked, and an untracked one stays
invisible to a concurrent run. Not gitignored, per your 2.3.0 warning.

Two notes you may want for the fleet, both about checks that read
"present" while being ineffective:

1. **.gitattributes was UNTRACKED here** and the currency check read
   `[x] .gitattributes (LF)` anyway — existence, not tracking. An
   untracked LF policy never reaches a clone or CI, so the repo would
   have declared 2.4.1 with the Windows-CRLF hazard fully live. Found
   only because the retrofit commit surfaced it as `??`. If `REQUIREMENTS`
   can ask `git ls-files --error-unmatch .gitattributes` instead, that
   closes it fleet-wide.

2. Your resident's decisions argument was right and I was wrong on the
   numbers: the register is **15** entries, not the 53 I reported (I had
   counted every ordered list in a 4710-line ROADMAP). Their "3 citations
   name ROADMAP" was itself low — ~19 — which strengthened their case
   rather than weakening it. The move was executed verified: diff of what
   left vs what landed is empty, 15 = 15, numbering unbroken so all 176
   `Decision N` citations still resolve, integrations/ left untouched as a
   historical record.

---
**autonomous verification, 2026-08-18:** `verified` — tree reads CURRENT; declares 2.4.1 (notice claims 2.4.1). The repo was re-read; this line is the resident's, the text above is the filer's.
