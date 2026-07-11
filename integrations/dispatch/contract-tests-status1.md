---
id: dispatch-001
artifact: contract-tests
status: fixtures-filed
ball: provider
filed: 2026-07-10
---

# Contract-test fixtures for `status.1` (dispatch-001, owed item)

Consumer-authored, for resident review and landing in autonomous CI, per
the dispatch-001 response §Contract tests. These three fixtures are live in
dispatch's own suite (`tests/fixtures/status1/` + 
`tests/unit/test_status_contract.py`, validator `dispatch/status.py`) — the
copies below are the proposal; land them against your validator however CI
prefers. Semantics they pin:

1. **valid.json** — the canonical example from `kit/contracts/status.md`
   parses with zero errors.
2. **quiet.json** — a quiet day is an explicit record (`quiet: true`,
   empty `recent` lists), never an absence; parses with zero errors.
3. **missing-field.json** — must be REJECTED, with at minimum these
   findings: missing required `quiet`; `last_verify` missing `ts`;
   `recent.commits[0]` missing `subject`; `recent.lessons` entry not
   matching `L\d{4}`.

## valid.json

```json
{
  "schema": "status.1",
  "project": "distillery",
  "ts": "2026-07-10T21:00:00Z",
  "roadmap_phase": {"id": "D1", "title": "The stream (deterministic ingest)", "gate_state": "open"},
  "last_verify": {"target": "fast", "exit": 0, "git": "03a4317", "ts": "2026-07-10T20:58:12Z"},
  "recent_since": "2026-07-09T21:00:00Z",
  "recent": {
    "commits": [{"hash": "03a4317", "subject": "D0 scaffold"}],
    "decisions": ["2"],
    "traces": ["2026-07-10-scaffold.md"],
    "lessons": []
  },
  "quiet": false
}
```

## quiet.json

```json
{
  "schema": "status.1",
  "project": "distillery",
  "ts": "2026-07-11T21:00:00Z",
  "roadmap_phase": {"id": "D1", "title": "The stream (deterministic ingest)", "gate_state": "open"},
  "last_verify": {"target": "fast", "exit": 0, "git": "03a4317", "ts": "2026-07-10T20:58:12Z"},
  "recent_since": "2026-07-10T21:00:00Z",
  "recent": {
    "commits": [],
    "decisions": [],
    "traces": [],
    "lessons": []
  },
  "quiet": true
}
```

## missing-field.json (must be rejected)

```json
{
  "schema": "status.1",
  "project": "distillery",
  "ts": "2026-07-10T21:00:00Z",
  "roadmap_phase": {"id": "D1", "title": "The stream (deterministic ingest)"},
  "last_verify": {"target": "fast", "exit": 0, "git": "03a4317"},
  "recent": {
    "commits": [{"hash": "03a4317"}],
    "lessons": ["not-a-lesson-id"]
  }
}
```

## Ratification note

dispatch ratifies the dispatch-001 response as shipped: `status.1` pinned,
no-`public`-flag delta accepted (flag layered in dispatch's watch.json),
`last_verify` lifted verbatim, sweep primitive consumed from
`kit/sweep/sweep.py` (dispatch keeps its own ledger file). E1 built against
schema + example; inferred-vs-declared marking live for repos without
writers. This filing closes the consumer-side owed item; ball returns to
provider for CI landing (no urgency — dispatch is not blocked).
