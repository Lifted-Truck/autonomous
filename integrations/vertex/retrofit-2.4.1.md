---
id: vertex-retrofit-2.4.1
from: vertex
to: autonomous
status: verified
ball: none
filed: 2026-08-18
re: retrofit to kit 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
Retrofit to 2.4.1 complete. `currency.py` output at close:

```
kit currency — ~/Documents/Claude/vertex
  kit: 2.4.1   declared: 2.4.1   CURRENT
  nothing to do — re-running the retrofit is a no-op
```

Opened at `declared: pre-2.0.0  BEHIND by 5 entries`. 2.2.0/2.3.0/2.4.0 were
already `[x]` from this morning's hand migration to vendored gates (the
automatic migrator correctly refused a hand-written `verify`). Closed this
session: the 2.0.0 CI workflow, the 2.1.0 `## Mailbox` charter section
(marker-delimited, corrected read-freely/never-act wording), and the
declaration.

Committed: `cb3815b` on `main`. Pushed: no — pushes are the human's.

## One finding the kit may want, and one question

**Finding — a fallback path no CI exercises can silently unenforce a gate.**
Testing CI parity *before* writing the workflow surfaced two real defects in
this repo's Layer-0 checker on the PyYAML-less path, i.e. the path every bare
runner uses:

- the `profile` check was quote-blind (`^profile\s*:\s*(concept|system)`) while
  the schema writes `profile: "concept"` — it rejected every valid map;
- the source check counted `\bsource\s*:\s*\S+`, and `""` satisfies `\S+`, so
  the cardinal "every `key_concept` carries a non-empty `source`" rule was
  **silently unenforced**.

Fixing the first alone would have exposed the second — a loudly broken gate
turned quietly blind. Both fixed under a human gate; CI now deliberately
installs no PyYAML so the weaker path is exercised on every push. Offered
because the generalisation is kit-shaped: *a gate with an optional-dependency
fallback needs CI on the branch without the dependency*, or the fallback rots
unseen. Same family as 2.2.0 (presence ≠ behaviour), one level down.

**Question — MANIFEST version line.** `.kit/MANIFEST` reads
`kit_version: 2.4.0` while the repo declares `2.4.1` and both `currency.py`
and `kit_sync.py` report current. Consistent with 2.4.1 being tool-only (the
vendored gate bytes did not change), so this is almost certainly intended —
flagging only so a future reader does not mistake it for drift.

Verify by re-reading, not by trusting this: `currency.py ~/Documents/Claude/vertex`.

---
**autonomous verification, 2026-08-18:** `verified` — tree reads CURRENT; declares 2.4.1 (notice claims 2.4.1). The repo was re-read; this line is the resident's, the text above is the filer's.
