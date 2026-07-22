# governor

**Status: ~10% — the deterministic watchdog-MONITOR is real; the fleet
CONTROLLER is deferred until a running organ fleet exists to govern.** Spec:
[DESIGN.md §4](../DESIGN.md).

## What's real now (run these)
- **`monitor.py`** — deterministic fleet-health sweep, no model calls. One
  command for "how is the fleet doing?": per-repo leaks, un-gated `./verify`,
  no-CI, stale READMEs, manifest status-prose (Decision 28), harness gaps →
  a STATUS dashboard + severity summary.
  `python3 governor/monitor.py --registry registry.json --out governor/STATUS.md`
  (STATUS.md is gitignored — it names private repos; regenerate on demand.)
- **`leak_scan.py`** — the privacy watchdog `monitor` builds on (absolute
  paths / username in tracked files; kept consistent with the `./verify`
  leak_gate — two detectors, one policy).
- **`HISTORY-REMEDIATION.md`** — the leaked-history purge runbook.

The `HALT` sentinel, watchdog loop, and conductor below are DESIGN, not built
— they govern a running organ fleet, and there is none yet.

## The full design — three functions on the AI/deterministic boundary:

- **Watchdog** — deterministic, no model calls, runs every tick. Metrics
  (token-rate, state-hash progress, churn, whack-a-mole, test trajectory),
  two-severity halt triggers (hard trips vs pause-and-escalate), `HALT`
  sentinel enforced by every agent's PreToolUse hook. Budgets enforced
  OUTSIDE any agent's process.
- **Curator** — model judgment behind quarantined writes. Runs the audit
  loop vertically + targeted down-propagation into specific organs'
  CLAUDE.md (slot-budgeted). Deterministic lint pass before any model pass.
- **Coherence critic** — fresh-context read-only review each cycle against
  ROADMAP + contracts ("green is not coherent" — the residual hole no
  mechanism closes). Findings become ledger issues, never direct edits.

Authority ceiling: the governor edits only ROADMAP, graph.json, memory files,
README, STATUS — never product code.
