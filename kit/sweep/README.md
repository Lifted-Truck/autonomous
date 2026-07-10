# sweep — the shared SCAN primitive

Registry-driven project enumeration + derived status + hash-ledgered change
detection, extracted as ONE component (Decision 14 semantics; requested by
distillery-001 and dispatch-001 — previously each consumer was set to fork
the audit loop's SCAN step).

Deterministic by contract: stdlib-only, no model calls, no wall-clock in
outputs, stable ordering, idempotent (`changed` after `--update-ledger` is
empty until content actually changes; hashes are content-based, not mtime).

```bash
# who's in scope, with derived harness/loop status
python3 sweep.py --registry ../../registry.json list

# what changed since the last pass (the audit-loop SCAN semantics)
python3 sweep.py --registry ../../registry.json changed \
    --ledger ~/.cache/my-consumer.ledger.json \
    --targets LIBRARY.md INDEX.md --update-ledger
```

Consumers keep their OWN ledger file (a distillery ingest and a dispatch
collection are independent cursors over the same registry). Tests:
`python3 -m unittest discover -s kit/sweep` — run by this repo's `./verify`.
