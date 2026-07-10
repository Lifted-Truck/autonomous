# kit — Harness Kit v2 ("the harness factory")

**Status: to build.** Spec: [DESIGN.md §6](../DESIGN.md). Replaces kit v1
(frozen at [archive/kit-v1/](../archive/kit-v1/)) per user mandate.

Shape: **one core + composable agent-type profiles**, where
`scaffold <profile> <target>` is runnable by a human OR by an agent
bootstrapping its own type.

- **Core layer** (every installation): layered CLAUDE.md + CODEMAP +
  .claudeignore; doctrine block + four-knowledge-systems firewall (from
  [scaffold-agentic-harness.prompt.md](scaffold-agentic-harness.prompt.md),
  canonical here); `./verify` contract (from [harness/](../harness/));
  ROADMAP + DECISIONS skeletons; hook set (PostToolUse format/lint,
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
