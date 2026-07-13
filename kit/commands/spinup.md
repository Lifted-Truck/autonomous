---
description: Scaffold a new project via the ecosystem spin-up procedure (survey → manifest → harness)
---

Spin up a new project: $ARGUMENTS

(Arguments — both optional: a target directory and a one-line description of
what the project is. **If no directory is given, the target is the current
working directory** — the normal case when the session was opened inside the
new folder. Before scaffolding into the cwd, confirm it is the intended
fresh project root: empty or near-empty, not inside an existing project or
one of the ecosystem repos; if in doubt, ask. If the description is missing,
ask for it — it seeds the survey's first question.)

**Composite?** If the arguments include `--composite`, or the project is one
deployable made of several modules behind a shared seam (a plugin hosting
engines, an app with plugins, a monorepo built together), follow
`ONBOARDING.md` → Part 2 → "Composite projects" instead (the five moves:
promote the seam to the contract; root charter + per-module sub-charters; a
`composite` manifest block with a `modules_dir`; record doc precedence; rung
2→3 by default). Worked reference: `~/Documents/Claude/synthetic-worlds/Orrery`.
Otherwise, the standard procedure:

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

Gotcha: the Write tool does not set the exec bit — `chmod +x verify
.claude/hooks/*.sh` before running the oracle, or `./verify` fails
`permission denied`.

Finish by reporting: the manifest for ratification, the green
`./verify fast` output, and (if ecosystem-facing) which briefs were filed
and whether the project should be registered in autonomous's ecosystem
tracks. Reference implementations: `~/Documents/Claude/distillery/`,
`~/Documents/Claude/dispatch/`.
