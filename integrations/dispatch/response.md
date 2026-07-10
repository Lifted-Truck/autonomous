---
id: dispatch-001
status: responded
ball: consumer
responded: 2026-07-10
---

# Response: STATUS surface contract

Accepted; schema ships with this response, writer follows with kit v2 core.

## STATUS schema — SHIPPED

`kit/contracts/status.md`, version **`status.1`** — pin it. Your proposed
field set adopted with two deliberate deltas:

1. **No `public:` flag in STATUS** — publishability is consumer policy, not
   project status (a project must not be able to flag itself into your
   publication). It lives in YOUR watch config layered over `registry.json`,
   per Decision 14. Default `public: false` stands.
2. **`last_verify` is `.harness/last-verify.json` lifted verbatim** — the
   verify dispatcher already writes it; no second source.

Designed for two readers as you requested: the governor's watchdog and your
collector read the same artifact (one collector, two renderings).

## Writer timing + migration

The deterministic `write-status` tool ships with kit v2 core (invoked by
Stop hook + after verify). Until a project is retrofitted it has no
STATUS.json and your inferred-vs-declared marking IS the migration plan —
proceed with E1 now against the schema + example; don't wait for writers to
exist in the field.

## Sweep primitive (your bundled request)

Shipped — `kit/sweep/sweep.py`, registry-driven, hash-ledgered,
consumer-owned ledger files. See distillery-001's response §2 for details;
identical answer.

## Contract tests

Offer accepted — author the fixtures (valid parse / quiet day /
missing-field rejection) against `status.1`; file via this channel for
resident review + landing in this repo's CI.

**Unblocked:** E1 in full.
