# governor

**Status: to build** (Phases P0 skeleton → P4 complete). Spec:
[DESIGN.md §4](../DESIGN.md).

Three separable functions, split on the AI/deterministic boundary:

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
