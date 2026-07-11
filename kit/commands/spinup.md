---
description: Scaffold a new project via the ecosystem spin-up procedure (survey → manifest → harness)
---

Spin up a new project: $ARGUMENTS

(If the arguments don't include a target directory and a one-line description
of what the project is, ask for whichever is missing before doing anything.)

Follow the canonical procedure at
`~/Documents/Claude/autonomous/ONBOARDING.md` → Part 2 → "Replicating the
structure for a NEW project (until kit v2 ships)" — all eight steps, exactly.
Two behaviors are non-negotiable:

1. **Survey first, scaffold second.** Conduct the 9-question spin-up survey
   (`autonomous/kit/README.md`) interactively with the human; write
   `project.manifest.json` before creating anything else. Never skip or
   backfill the survey.
2. **The architecture rung is asked, never defaulted** (doctrine: right-size
   the agent architecture). Present the three-rung menu with what earns
   each; single-thread is the normal answer, not the fallback.

Finish by reporting: the manifest for ratification, the green
`./verify fast` output, and (if ecosystem-facing) which briefs were filed
and whether the project should be registered in autonomous's ecosystem
tracks. Reference implementations: `~/Documents/Claude/distillery/`,
`~/Documents/Claude/dispatch/`.
