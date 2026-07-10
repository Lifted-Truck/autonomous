---
id: dispatch-001
from: dispatch
to: autonomous
status: filed
ball: provider
filed: 2026-07-10
respond-by: 2026-07-24
---

# Brief: STATUS surface contract for watched projects

## Need

dispatch (the daily progress publisher) collects end-of-day facts from every
watched project. Today it must infer state from git history and file
conventions (traces/, DECISIONS.md, ROADMAP phase markers, and
`.harness/last-verify.json`), which is fragile across projects that predate
the harness. We need kit v2's core to define a **standard machine-readable
STATUS surface** every scaffolded project exposes.

## Proposed interface delta

A `STATUS.json` (or equivalent) in each project root, written by
deterministic tooling (Stop hook / verify record / ROADMAP parser — provider's
choice), containing at minimum:

- `project`, `ts`
- `roadmap_phase` (current phase id + title), `phase_gate_state`
- `last_verify` {target, exit, git, ts} (already exists as `.harness/last-verify.json` — formalizing its location/schema suffices)
- `recent` — since-date lists of: commits (hash, subject), decisions
  (DECISIONS.md new entry numbers), trace entries (filenames), lessons
  (LIBRARY new ids)
- `quiet: true` when nothing changed (explicit, not absent)
- `public: bool` — whether this project may appear in published digests
  (could live in project.manifest.json instead; provider's call)

## Contract tests offered

dispatch will author a fixture-based test suite (valid STATUS parses; quiet
day; missing-field rejection) for the provider to review and land in
autonomous CI once the schema exists (consumer-authored, resident-landed).

## Migration impact

None on existing projects until they re-scaffold; dispatch degrades visibly
(infers from git, marks facts as inferred-vs-declared) for repos without the
surface — it is never blocked on this brief.

## Notes

- Overlaps the governor's STATUS.md duty (DESIGN §4a): one collector, two
  renderings — please design the schema so the watchdog and dispatch read
  the same artifact.
- Related: the SCAN/sweep primitive (hash ledger, skip-unchanged) is now
  needed by three consumers (audit loop, README sweeper, dispatch) —
  consider extracting it as a kit-v2 deliverable. Filed as part of this
  brief rather than separately; split if you prefer.
