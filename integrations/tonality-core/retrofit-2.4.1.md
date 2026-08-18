---
id: tonality-core-retrofit-2.4.1
from: tonality-core
to: autonomous
status: verified
ball: none
filed: 2026-08-18
re: retrofit to kit 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
Retrofit to 2.4.1 complete. currency.py output at close:

```
kit currency — ~/Documents/tonality-core
  kit: 2.4.1   declared: 2.4.1   CURRENT
  nothing to do — re-running the retrofit is a no-op
```

Committed: f673813 on main. Pushed: no — pushes are the human's.

Notes for the verifier, since two of these are gate-behaviour findings rather
than repo content:

- This repo is a CONSUMER and has no `integrations/` of its own; briefs to it
  land in the provider's tree (`Tonality/integrations/tonality-core/`). The
  2.1.0 mailbox clause is written to state both topologies rather than assert
  the kit's default sentence, which would have been false here. Human-ratified
  at the approval pause.
- Prior-art Phase 0 is recorded N/A with rationale (DECISIONS #2): this repo is
  the second implementation of an engine whose prior-art position was settled
  upstream. The pre-ship IP re-scan bookend stays OPEN.
- `.claude/` hooks were deliberately not installed — out of scope for closing
  the delta, and `currency.py` does not check for them.

Two things worth propagating to the kit if they generalise:

1. **A repo can read leak-clean only because of the human's GLOBAL gitignore.**
   Here `.claude/settings.local.json` holds absolute home paths and was
   invisible to `git grep --untracked` purely because `~/.config/git/ignore`
   ignores it. Any clone without that rule reds immediately. Pinned in the
   repo's own `.gitignore`. Other repos in the fleet may be passing for the
   same accidental reason — a checklist item worth adding.
2. **The gate-fires probe is easy to mis-run in zsh.** A planted Windows
   identity path fired correctly but the assertion reported NOT FIRED, because
   `echo "$out"` interprets `\U` as a unicode escape and destroys the captured
   line. `printf '%s\n'` throughout. A harness bug looks exactly like a gate bug.
   (Recorded as this repo's LIBRARY L0005.)

---
**autonomous verification, 2026-08-18:** `verified` — tree reads CURRENT; declares 2.4.1 (notice claims 2.4.1). The repo was re-read; this line is the resident's, the text above is the filer's.
