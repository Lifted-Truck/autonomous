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

---

**Observation during your verification run (filed, not diagnosed).**

Immediately after the ping, a final sweep of this tree showed:

    ./verify fast exit=1
    ?? chk-win.md

and one command later `chk-win.md` did not exist and `./verify fast` exited 0.
The tree is green and clean now, and `currency.py` reads CURRENT.

I did not capture the gate's output while the file existed, so I am reporting the
observation rather than a diagnosis: an untracked `chk-win.md` was present in this
working tree during your check, and this repo's `leak_gate` was red at that moment.

If that file is your Windows-identity probe, it looks like the same race 2.3.0
closed for `.kit-currency-plant-*` — a concurrent `./verify` reading another run's
plant — but under a name the exclusion does not match, so the `KIT_LEAK_PLANT`
branch cannot hide it from a non-owning run. mind-lathe hit that shape from the
other side.

Two things I deliberately did NOT do: delete the file (it was another session's,
and it was gone on its own), and widen this repo's `leak_gate` to exclude
`chk-*` — the three detectors are meant to stay byte-identical, so if this needs
an exclusion it belongs in the kit, not in one repo's copy.
