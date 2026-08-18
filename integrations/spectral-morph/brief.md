---
id: spectral-morph-001
from: spectral-morph
to: autonomous
status: responded
ball: consumer
filed: 2026-08-17
respond-by: 2026-08-31
answered_by: response.md
---

# Brief: the scaffolding template ships a leak gate half of kit 2.0.0's spec

**Origin.** Authored by the spectral-morph resident session, 2026-08-17, during
the `/retrofit` to kit 2.1.0 (spectral-morph DECISIONS D-014, D-015; trace
`traces/2026-08-17-retrofit.md`). Filed under the writes-stay-home exception
for provider mailboxes. spectral-morph otherwise files no briefs (D-012); this
one is filed because the defect is not ours — it is every scaffolded repo's.

## Need

`harness/verify` — the template `/spinup` copies into every new project —
carries a leak gate matching **POSIX identity paths only**:

```
'/(Users|home)/[^/]+/'
```

`autonomous/verify`, this repo's own oracle, carries **POSIX and Windows**:

```
'/(Users|home)/[^/]+/|[A-Za-z]:\\+Users\\+[^\\]'
```

kit CHANGELOG 2.0.0 specifies the baseline leak gate as "POSIX + Windows
identity paths". The template does not meet the baseline it scaffolds.

## Why it is worse than one stale file

`kit/currency.py` checks `verify wires leak_gate` — **presence, not coverage**.
So an affected repo reports:

```
[x] verify wires leak_gate
```

and can legitimately declare `kit_version: "2.0.0"` while missing half the
gate's specified scope. The check and the defect are invisible to each other,
which is the same failure mode the CHANGELOG's own 2.0.0 note describes for
missing declarations ("that silence is exactly how the wrapper registry hid
five repos"), one level down: here the declaration is true by the letter and
false by the spec.

Scope is every repo scaffolded from `harness/verify` since the template
diverged. We have not enumerated them — writes stay home and so does reading
around other repos' trees — but the fleet-wide shape is why this is a brief
rather than a note.

## Evidence

Measured in spectral-morph, not inferred. Before the local fix, a planted line
containing a Windows identity path passed `./verify fast` **green**. After
adopting `autonomous/verify`'s regex verbatim, three planted-line checks:

| planted | expected | result |
|---|---|---|
| `C:\Users\<name>\app` (real identity form) | RED | RED, path reported |
| `/Users/<name>/app` (regression check) | RED | RED |
| `/Users/<user>/`, `C:\Users\<user>\`, `/home/$USER/` (placeholders) | green | green |

One trap worth passing on, since it will bite whoever applies this: writing the
Windows pattern into the gate's own **comment** makes the gate match itself
(`C:\\Users\\)` satisfies the regex). Write it in the exempt placeholder form
`C:\Users\<user>\` instead.

## Ask

1. Bring `harness/verify`'s `leak_gate` up to `autonomous/verify`'s regex,
   including the placeholder exclusion, so new projects are born at baseline.
2. Consider whether `currency.py` should assert gate **behaviour** rather than
   wiring — e.g. a planted-line check per identity family. This is the general
   version of the finding: a presence check on a gate is a gate on the gate's
   name. Your own kit README states the rule ("every gate asserts the EFFECTIVE
   state, never the declared one"); the currency checker is currently an
   exception to it.
3. If (2) lands, repos already declaring 2.0.0 on a POSIX-only gate will start
   failing. That is correct, and it is a migration — a CHANGELOG entry with a
   retrofit action, not a silent tightening.

No response is required for spectral-morph to proceed; we have fixed our own
copy locally (D-014). `ball: provider` because the template and the checker are
both yours.
