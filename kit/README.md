# kit — Harness Kit v2 ("the harness factory")

**Status: to build.** Spec: [DESIGN.md §6](../DESIGN.md). Replaces kit v1
(frozen at [archive/kit-v1/](../archive/kit-v1/)) per user mandate.

Shape: **one core + composable agent-type profiles**, where
`scaffold <profile> <target>` is runnable by a human OR by an agent
bootstrapping its own type.

**Front door: the spin-up survey.** When a new project directory is created,
the scaffold conducts a standard, repeatable interview — a fixed question
list about scope — and writes the answers to a committed
`project.manifest.json`. Deterministic scaffolding then runs FROM the
manifest (AI conducts the interview; deterministic code applies the
templates — the AI/deterministic boundary applied to setup itself). The
manifest is re-runnable: change an answer, re-run scaffold, review the diff.
Draft question list (refine during the v2 build):

1. **What is it?** library/engine · app · service · pipeline · experiment
2. **Architecture rung** (the menu, never defaulted): single thread ·
   thread + subagents/verifier · organ fleet — with what earns each rung
3. **Domain core**: the hard exact logic an LLM must never own (drives the
   deterministic-boundary wiring and golden-oracle choice)
4. **Oracle shape**: strict pinned goldens vs invariants-only; CI matrix vs
   single-version smoke
5. **Second implementation planned?** (→ port-pin module)
6. **Consumers / is it a consumer?** (→ integrations channel + INTEGRATIONS
   policy wiring)
7. **Parallel audit thread earned?** (→ audit-thread profile)
8. **Knowledge-loop tags**: the 3–6 categories of hard-won knowledge worth
   accumulating here
9. **Lifespan & autonomy tier**: throwaway experiment vs long-lived; how much
   unattended operation is intended (drives governance strictness)

Each answer maps to a deterministic action (install module X, wire hook Y,
seed file Z) — the survey is the human-facing face of the manifest, and the
manifest is the machine-facing face of the survey.

**The architecture menu** (doctrine: right-size the agent architecture) is
question 2: single-threaded agent → thread + subagents/verifier → organ
fleet. The fleet is a visible option at the outset, never the default.
Profiles beyond `organ` install only on the rung that needs them.

- **Core layer** (every installation): layered CLAUDE.md + CODEMAP +
  .claudeignore; doctrine block + four-knowledge-systems firewall (from
  [scaffold-agentic-harness.prompt.md](scaffold-agentic-harness.prompt.md),
  canonical here); `./verify` contract (from [harness/](../harness/));
  ROADMAP + DECISIONS skeletons; **the knowledge loop, default-on**
  (Decision 11 — tags seeded from survey Q8; the write gate is the bloat
  safeguard, not absence of the loop); hook set (PostToolUse format/lint,
  SessionStart context, PreToolUse territory + HALT + destructive-op guard,
  Stop enforced-reflection + red-suite gate).
- **Profiles** (each = agent definition + permissions + hooks + CLAUDE.md
  template + memory seed + verify wiring + territory manifest): `organ`,
  `verifier`, `critic`, `scout`, `audit-thread`, `curator`, `watchdog`,
  `coherence-critic`, `conductor`. Each profile documents when it's earned,
  what it may never do, and its handoff artifact format.
- **INSIGHTS v2**: every prescription cites its evidence in
  [research/](../research/).

Known v1→v2 deltas already identified: reflection-trigger default is
mode-dependent (voluntary interactive / hook-enforced autonomous); the Stop
hook's "can't read the session" caveat is outdated (transcript access exists);
boundary constraints move from prose to PreToolUse hooks + CI linters.
