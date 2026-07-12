---
description: Catch an EXISTING repo up to the ecosystem scaffolding (gap survey → inferred manifest → non-destructive harness retrofit)
---

Retrofit this existing project: $ARGUMENTS

(Arguments — both optional: a target directory and a one-line description.
**If no directory is given, the target is the current working directory.**
Sanity-check the opposite of /spinup: the target SHOULD be an existing
project with real content; if it looks empty/greenfield, suggest /spinup
instead and stop.)

Follow the canonical procedure at
`~/Documents/Claude/autonomous/ONBOARDING.md` → Part 2 → "Retrofitting an
EXISTING project" — all five steps, exactly. Four behaviors are
non-negotiable:

1. **Infer before asking.** Gap-survey the repo read-only first; propose
   survey answers derived from the code and ask only what code cannot show
   (the architecture rung is still asked, never defaulted).
2. **Plan, then pause for approval before writing anything.** An existing
   repo is working state; list every create-vs-modify up front.
3. **Append, never rewrite.** Marker-delimited insertions only; existing
   content wins conflicts pending a human ruling; re-running must be a
   no-op.
4. **Never break what works — or hide what doesn't.** `./verify` wraps the
   existing test/lint commands; currently-red tests are quarantined and
   recorded in ROADMAP as explicit debt, never deleted, never silently
   gated on, never "fixed" by weakening.

Finish by reporting: the before/after gap table (this is the visual for the
review beat), the manifest for ratification, green `./verify fast` output,
and any briefs filed. Reference for the target end-state:
`~/Documents/Claude/distillery/`, `~/Documents/Claude/dispatch/`.
