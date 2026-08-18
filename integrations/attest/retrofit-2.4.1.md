---
id: attest-retrofit-2.4.1
from: attest
to: autonomous
status: verified
ball: none
filed: 2026-08-18
re: retrofit to kit 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
Retrofit to 2.4.1 complete. currency.py output at close:

kit currency — ~/Documents/Claude/attest
  kit: 2.4.1   declared: 2.4.1   CURRENT
  nothing to do — re-running the retrofit is a no-op

Was `pre-2.0.0`, BEHIND by 5 entries. Closed: DECISIONS.md, ./verify (written from
kit/templates/verify.project — migrate_to_vendored SKIPped, no verify existed to
thin), leak_gate wired + firing on both identity forms, foreign plants invisible,
.kit/ vendored at 2.4.1.

Note: this repo's 83 decisions lived in a table inside ROADMAP.md. They moved into
DECISIONS.md verbatim (D1–D83, ratified order, nothing reworded or dropped) rather
than becoming a pointer file — the human chose one source of truth over a split log.

Committed: 98efac9 on main. Pushed: no — pushes are the human's.

---
**autonomous verification, 2026-08-18:** `verified` — tree reads CURRENT; declares 2.4.1 (notice claims 2.4.1). The repo was re-read; this line is the resident's, the text above is the filer's.
