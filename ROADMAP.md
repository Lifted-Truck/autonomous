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

## Ecosystem tracks (parallel development across repos)

The broader structure the phases above serve. Each track is a separate repo
with its own ROADMAP; this section owns only the cross-track sequencing and
seams. Exchanges between tracks go through `integrations/` per the
INTEGRATIONS policy.

- **Track A — autonomous (this repo): standards + kit + governor.**
  Phases C0/P0–P4 above and kit v2. Provides: doctrine, kit core (incl. the
  STATUS surface and LIBRARY entry schema — briefs dispatch-001 /
  distillery-001, both ball: provider, respond-by 2026-07-24), the sweep/SCAN
  primitive extraction, harness profiles.
- **Track B — distillery (`~/Documents/Claude/distillery/`): global memory.**
  The two-pool system (Decision 11): append-only stream + analyst + distilled
  pool. Phases D0–D4 in its ROADMAP. Seams: consumes LIBRARY schema + sweep
  primitive (Track A); autonomous P3 down-propagation consumes its distilled
  pool (gates implemented there, spec canonical here — per distillery-001).
- **Track C — dispatch (`~/Documents/Claude/dispatch/`): progress publishing.**
  Deterministic collector → FACTS → styled digest → fenced AI narration →
  human-gated publish. Phases E0–E4 in its ROADMAP. Seams: consumes the
  STATUS surface (Track A; degrades visibly until it ships); later consumes
  distillery lesson-highlights (needs D4).
- **Track D — landscape audit (no repo; runs against Track A).** Monthly
  propose-only research pass over the external field (see Deferred);
  bibliography is its ledger.

**Cross-track ordering constraints (the only ones):**
1. Kit v2 core's STATUS + LIBRARY-schema artifacts unblock dispatch E1
   (fully) and distillery D1 (validation half) — answer both briefs early.
2. The sweep primitive should be extracted ONCE (Track A, from
   agent-knowledge-loop's SCAN) before D1/E1 build their own — or D1/E1
   build minimal local versions behind the same interface and swap in
   (degrade-visibly rule applies to internal seams too).
3. autonomous P3 must NOT build a second distilled pool — it consumes
   Track B's (D4).
4. Everything else proceeds in parallel without coordination.

**Ecosystem-lead milestone (decision-in-principle, gated).** Once distillery
D4 + autonomous P3 are green, evaluate promoting **distillery to operational
lead** of the ecosystem — the analyst is the natural seed of the
ecosystem-level curator/governor, and the operator should be a separate
entity from the standards body (separation of powers: the repo that defines
gates shouldn't be the one operating under them day-to-day). autonomous
remains the doctrine/kit/protocol home either way. Gate for the handoff: the
distillery analyst has produced ≥N ratified promotions with zero poisoning
incidents, and the governor's curator role runs against distillery pools in
a full simulated cycle.

## Parallel track — Kit v2 ("the harness factory")

Built alongside P0–P2, since the phases consume its profiles as they emerge.
Spec: DESIGN.md §6. First profiles needed: `organ`, `watchdog`, `conductor`
(P0/P1); then `verifier`/`critic` (P1), `curator` (P3), `coherence-critic`
(P4). Kit v2 ships INSIGHTS v2: every prescription cites its evidence in
`research/`.

**Shipped so far** (2026-07-10, answering distillery-001 + dispatch-001):
`kit/contracts/library-entry.md` (v1), `kit/contracts/status.md` (v1),
`kit/sweep/` (the shared SCAN primitive, tested, wired into this repo's
`./verify`). Next kit items: the STATUS writer (`write-status` + hook
wiring), the survey→manifest scaffolder, first profiles.

## Target consumers / applications

- The user's first target project (shape TBD — organ count and CI choices to
  be sanity-checked against it before P2).
- Every existing project at the Claude root, via kit-v2 retrofits.
- Tonality: first retrofit of the INTEGRATIONS §3 responsibility model.
- **The daily-digest publisher** (separate project, user 2026-07-10): watches
  all development projects and produces a styled end-of-day progress summary
  for the user's website. A pure READ consumer of this repo's substrate —
  traces/, DECISIONS, ROADMAP phase status, git history — which makes it the
  first external consumer-driven contract on the kit's status surface: its
  intake brief should specify exactly what machine-readable status every
  project must expose, and that spec lands in kit-v2 core (a STATUS
  artifact). Shares SCAN mechanics (hash ledger, skip-unchanged) with the
  audit loop and README sweeper; obeys writes-stay-home (never commits to
  watched repos). Overlaps the governor's STATUS.md duty — the digest should
  be a *rendering* of the same data, not a second collector.

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
- **Landscape audit (meta-audit of the protocol itself)** — a scheduled
  research pass (recommend monthly, not weekly: consensus moves slowly and
  research fan-outs are expensive) that re-surveys the external landscape and
  recommends protocol changes. Shape: the audit loop's mechanics pointed
  outward — a ledger in research/BIBLIOGRAPHY.md of per-topic last-checked
  dates; fan-out research agents, one per doctrine tenet / protocol area;
  diff findings against doctrine/ + DESIGN.md; output a dated
  `research/proposals/<date>.proposal.md` (propose-only — doctrine changes
  are NEVER auto-applied; human ratifies, DECISIONS records). Each run
  appends its sources to the bibliography. Complements kit-v1's
  GOVERNANCE.md config-review idea ("when new models resolve constraints,
  delete old guardrails") — deleting stale doctrine is an explicit output,
  not just adding. **Deployment recommendation (2026-07-10): a scheduled
  CLOUD routine, independent of P0 plumbing** — its inputs are web + this
  GitHub repo only, and its output is a PR (the propose-only staging buffer,
  mechanically enforced). Boundary rule for all routines: cloud for
  web+GitHub-input work; local cron for anything touching the local project
  tree (audit loop, distillery sweeps, dispatch collection). Run zero:
  2026-07-10 (this repo's founding research; bibliography is the ledger).
