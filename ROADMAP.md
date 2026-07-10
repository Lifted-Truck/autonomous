# autonomous — ROADMAP

> **Single source of truth for project direction.** Any forward-looking
> statement anywhere else (README, DESIGN.md, docstrings) defers to this file.
> Phase gates are never weakened to pass. A phase closes only when its gate is
> green.

## Build sequence (phase-gated)

- **Phase C0 — Consolidation.** Pull the ad-hoc corpus into this repo;
  doctrine single-sourced; pointers wired (global CLAUDE.md, tombstones);
  pushed to the remote.
  *Gate: no editable artifact exists in two places (dedup sweep clean); global
  CLAUDE.md imports doctrine/ and a fresh session sees the doctrine; remote
  up to date.* **← current phase**
- **Phase P0 — Enforcement floor.** Territory PreToolUse hooks; HALT sentinel;
  watchdog skeleton (deterministic, no model calls); kit-v2 core layer.
  *Gate: adversarial tests — an agent instructed to write outside territory is
  blocked; HALT stops a running fleet mid-task; a budget trip fires from
  outside the agent process.*
- **Phase P1 — One organ, real loop.** Single organ + `./verify` + merge queue
  on a toy codebase; fresh-context shift rhythm; enforced reflection via Stop
  hook. *Gate: N unattended shifts complete tasks with zero human touches;
  every shift leaves journal + handoff artifact.*
- **Phase P2 — Two organs, one seam.** Contract dir; interface-first protocol;
  consumer contract tests; task ledger; graph.json + generated boundary
  linter. *Gate: a cross-organ change lands end-to-end via PROPOSAL → contract
  commit → both sides green → queue merge.*
- **Phase P3 — Memory + curator.** Leaf loops per organ; audit promote-up;
  curator down-propagation (targeted, slot-budgeted). *Gate: a lesson learned
  in organ A demonstrably changes organ B's behavior.*
- **Phase P4 — Full governor + first real project.** Coherence critic; metrics
  dashboard (visual-first STATUS); escalation paths. *Gate: a full simulated
  incident (injected oscillation, injected gate-weakening) is caught and
  halted without human detection.*

## Parallel track — Kit v2 ("the harness factory")

Built alongside P0–P2, since the phases consume its profiles as they emerge.
Spec: DESIGN.md §6. First profiles needed: `organ`, `watchdog`, `conductor`
(P0/P1); then `verifier`/`critic` (P1), `curator` (P3), `coherence-critic`
(P4). Kit v2 ships INSIGHTS v2: every prescription cites its evidence in
`research/`.

## Target consumers / applications

- The user's first target project (shape TBD — organ count and CI choices to
  be sanity-checked against it before P2).
- Every existing project at the Claude root, via kit-v2 retrofits.
- Tonality: first retrofit of the INTEGRATIONS §3 responsibility model.

## Deferred / demoted

- **Live agent-to-agent messaging** — deliberately excluded; published
  experience shows it is the most fragile layer and unnecessary at 3–8 agents
  (research/2026-07-10-coordination-isolation.md). Revisit only if the task
  ledger provably cannot express a needed interaction.
- **Beads-vs-minimal-ledger decision** — deferred to P2 when the ledger is
  actually needed.
- **Conductor substrate decision** (cron + headless `claude -p` vs
  agent-teams/Workflow vs supervisor daemon) — deferred to P0 entry.
- **Relocating the leaf knowledge-loop prompt into the agent-knowledge-loop
  repo** (it is that system's Level 0) — pending user decision; canonical here
  until then.
- **Global daily README-refresh loop** — a second global agent (cron,
  audit-loop-style: hash-ledgered, skip-unchanged, propose-or-apply) that
  sweeps repos whose content changed and refreshes their READMEs per the
  clarity standard. User floated 2026-07-10; deliberately parked — overlaps
  the curator's README duty (DESIGN §4b), so decide after P3 whether it's
  the curator generalized across repos or a separate lightweight sweeper.
