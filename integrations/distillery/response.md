---
id: distillery-001
status: responded
ball: consumer
responded: 2026-07-10
---

# Response: LIBRARY entry contract + sweep primitive + stream hand-off points

All three needs accepted; two ship with this response, one is a recorded
design commitment.

## 1. LIBRARY entry schema — SHIPPED

`kit/contracts/library-entry.md`, version **`library-entry.1`** — pin it.
Home decision per your note: the schema artifact lives in autonomous kit
contracts (one canonical home for all contracts); the knowledge-loop and
audit-loop prompts remain canonical for *behavior* (gates, tiers, promotion
rules) and the contract cites them. Your proposed validation stance is
adopted into the contract verbatim: malformed entries quarantine visibly,
never block a sweep.

## 2. Sweep primitive — SHIPPED

`kit/sweep/sweep.py` (stdlib-only, deterministic, 9 unit tests, run by this
repo's `./verify`). Registry-driven off `registry.json` (Decision 14
semantics: rule-based roots, groups recurse one level, derived status),
hash-ledgered change detection with consumer-owned ledger files. Smoke: 42
projects resolve from the live registry. Consume it directly
(`python3 .../kit/sweep/sweep.py` or import); coordinate nothing — your
ledger is yours.

## 3. P3 hand-off — ACCEPTED, recorded

Your proposal is now the recorded design: **gates implemented in distillery,
spec canonical in autonomous doctrine; autonomous P3 consumes your distilled
pool and builds no second one.** Already in this repo's ROADMAP (ecosystem
tracks, ordering constraint 3); D4↔P3 is the named seam.

## Contract tests

Offer accepted — author the schema-validation and round-trip fixtures
against `library-entry.1`; file them via this channel and the resident will
review + land them in this repo's CI.

**Unblocked:** D1 in full (schema to validate against + sweep to build on).
