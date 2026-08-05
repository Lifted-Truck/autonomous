---
id: antiphon-001
from: antiphon
to: autonomous
status: filed
ball: provider
filed: 2026-07-14
respond-by: 2026-07-28
---

# Brief: list ANTIPHON in the Execution-project registry (as deliberately dormant)

**Origin.** Authored by the ANTIPHON lead session, 2026-07-14, at ANTIPHON's
spin-up ratification gate. Motivating decisions: ANTIPHON `DECISIONS.md` D7
(precedence ruling that defined the repo's scope), D8 (single-thread rung), and
D10 (starter-kit triage completed). Trace:
`antiphon/traces/2026-07-13-spinup-scaffolding.md`. Filed at human direction
during the ratification beat — the same trigger under which HYPERSAW was
registered.

## Need

ANTIPHON was spun up on 2026-07-13 via `/spinup` and pushed to
github.com/Lifted-Truck/antiphon. It is already in ecosystem scope
automatically — `registry.json`'s `synthetic-worlds` group rule covers
immediate children, and `derived_status` means consumers derive its harness
state at sweep time. **No registry.json change is requested or needed.**

What is requested is the separate, discretionary listing in
`ROADMAP.md` → *Execution-project registry* (the section currently holding
HYPERSAW, "listed so the governor and audits know they exist, not for
cross-track sequencing").

The reason to list ANTIPHON is the inverse of the usual one. It is **green and
deliberately inactive**: `./verify fast` passes, CI passes, and no feature work
will happen for an indefinite period because three spin-up conditions are
unmet by design. To a governor or audit reading activity signals, a repo with a
green oracle and no commits is indistinguishable from an abandoned one. The
registry entry is what makes "dormant on purpose" legible without anyone
opening the repo.

## Proposed delta

One entry appended to the Execution-project registry list, matching HYPERSAW's
shape. Suggested text (edit freely — the resident owns the wording):

> - **ANTIPHON** (`~/Documents/Claude/synthetic-worlds/Antiphon/`, public:
>   github.com/Lifted-Truck/antiphon) — quantized harmonic companion for
>   Ableton Live (live regime only; the offline harmonizer is Wend's
>   `harmonize` mode). Spun up 2026-07-13 via `/spinup`; rung 1 (single
>   thread); CI mirrors the Stop hook (`verify fast`; Layer-E needs a live
>   Ableton set and is not runnable on a runner). **Status: deliberately
>   dormant** — feature work is gated on three unmet spin-up conditions (Wend
>   H2 passes; a demonstrated live-regime need; a measured quantization
>   ceiling). Green oracle, no activity expected. Future consumer of **Wend**
>   (frozen `HarmonicSpine` + pinned voice stage) and **Tonality** (analysis
>   slices); briefs deliberately unfiled until the conditions hold. Manifest
>   ratification pending as of filing.

## What is NOT requested

- No `registry.json` edit (already covered by the group rule).
- No cross-track sequencing. ANTIPHON is a leaf consumer; it feeds back only
  through the `synthetic-worlds` scope's knowledge-loop harvest.
- No action on the Wend/Tonality briefs. Those are ANTIPHON→provider exchanges
  and are intentionally unfiled: filing them now would put a ball in a
  provider's court for work that must not start yet. Noted here only so the
  absence reads as a decision rather than an oversight.

## Contract tests offered

None applicable — this is a registry listing, not an interface change. If
autonomous would prefer dormancy to be a *machine-readable* field rather than
registry prose (e.g. a `status`/`dormant` key in `project.manifest.json` that
sweeps can read), ANTIPHON will implement whatever shape you specify and offer
a fixture test for it. That may be the better long-term answer: this brief is
prose because no such field exists today, and a second dormant project would
make the gap structural.

## Migration impact

None. Nothing consumes this list programmatically today.

## Notes

- **Writes stay home:** this file is a mailbox write under the exception in
  INTEGRATIONS §3 (same-machine direct write to `integrations/<consumer>/`).
  It is left **uncommitted** — committing it to autonomous is a resident
  action, as is the ROADMAP edit itself.
- Low urgency. `respond-by` is set two weeks out, but nothing in ANTIPHON is
  blocked on this and the ball can sit — declining is a perfectly good outcome
  if the registry is meant only for actively-building projects. In that case a
  one-line response saying so would be useful: it settles whether dormant
  projects belong there at all, which is the general question behind this
  specific ask.
