---
id: distillery-001
from: distillery
to: autonomous
status: filed
ball: provider
filed: 2026-07-10
respond-by: 2026-07-24
---

# Brief: LIBRARY entry contract + sweep primitive + stream hand-off points

## Need

distillery (the global memory system) sweeps every project's knowledge-loop
LIBRARY into an append-only stream and serves a distilled pool back to
curators. Three things needed from the standards side:

1. **A pinned LIBRARY entry schema.** The leaf entry format
   (`[Lxxxx] title | tier | added | tags | lesson | evidence | falsifier |
   supersedes` + audit-loop `origin:`) is currently defined by prose in two
   prompts. Distillery needs it declared as a versioned contract (a
   `library-entry.schema` artifact in kit v2 core) so ingest can validate
   records and reject malformed entries deterministically. Schema changes
   would then be versioned events (INTEGRATIONS rule 4), not silent drift.
2. **The sweep/SCAN primitive as a shared component.** Hash-ledgered
   skip-unchanged sweeping now has three consumers (audit loop, README
   sweeper, dispatch) and distillery would be the fourth. We'd rather consume
   than fork (see also dispatch-001, which requests the same — coordinate).
3. **Named hand-off points with autonomous's memory phases.** DESIGN P3
   (curator down-propagation) should consume distillery's distilled pool
   rather than building a second one. Requesting: P3's design names
   distillery as the pool provider, and the promotion-gate implementation
   (cross-proliferation standard, autonomous README §4c) lives in ONE place —
   proposal: gates implemented in distillery, spec stays canonical in
   autonomous doctrine.

## Contract tests offered

distillery will author: schema-validation fixtures (valid/malformed LIBRARY
entries), and a round-trip test (entry → stream record → provenance intact)
for the provider to review and land once the schema artifact exists.

## Migration impact

Existing LIBRARYs already conform in practice; declaring the schema is
formalization, not change. If validation surfaces nonconforming legacy
entries, distillery quarantines them (visible, non-blocking) rather than
rejecting the sweep.

## Notes

The audit loop (agent-knowledge-loop repo) stays canonical for vertical
promotion; distillery adds warehouse + analyst beside it. If the schema
artifact should live in agent-knowledge-loop instead of kit v2 core, that's
an acceptable response — distillery only needs ONE canonical home to pin.
