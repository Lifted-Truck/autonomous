# Generic Agent Harness

A project-agnostic Claude Code harness. Opus leads; Sonnet does the labor; an
oracle gates everything. The harness is the invariant — each project supplies
exactly three variable parts:

1. **`./verify`** — the oracle entrypoint (project implements the targets)
2. **`ROADMAP.md`** — the single source of truth (project fills it in)
3. **`CLAUDE.md` §Domain** — project-specific context (everything above §Domain
   is identical across repos)

Everything else — agents, hooks, settings, the provenance skill — is copied
verbatim and never edited per-project. If you find yourself editing the
invariant layer for one repo, that's a signal the change belongs in the
harness for all repos (update the template, re-sync) or in §Domain.

## Layout

```
project/
├── CLAUDE.md                     # charter: invariants + §Domain
├── ROADMAP.md                    # SSOT: queue, acceptance criteria, status
├── verify                        # oracle dispatcher: fast | full | report
├── traces/                       # append-only decision log (one file per change)
├── .harness/                     # machine state (last-verify.json); gitignore optional
└── .claude/
    ├── settings.json             # permissions + hooks
    ├── agents/
    │   ├── implementer.md        # sonnet — writes code inside a scoped brief
    │   ├── verifier.md           # sonnet — runs the oracle, reports verbatim
    │   └── critic.md             # opus  — adversarial read-only review
    ├── hooks/
    │   ├── pretool-deny.sh       # blocks destructive bash
    │   ├── posttool-dirty.sh     # marks tree dirty after edits
    │   └── stop-gate.sh          # blocks session end while oracle is red
    └── skills/
        └── provenance/SKILL.md   # trace discipline, preloaded into implementer
```

## Model routing

- **Lead session:** run `/model opusplan` — Opus for plan mode, automatic
  switch to Sonnet for execution. Use plain `opus` only for sessions that are
  pure architecture (no implementation expected).
- **Subagents:** pinned in frontmatter — `implementer` on `sonnet`,
  `verifier` on `haiku` (verbatim gate-reporting needs no more; a precise
  red is cheap), `critic` on `opus` with `effort: high`.
- **Cost ceiling:** export `CLAUDE_CODE_SUBAGENT_MODEL=sonnet` to force every
  subagent (including critic) down to Sonnet for budget-constrained sessions.
  Frontmatter loses to the env var, which is the point.
- Built-in **Explore** (Haiku, read-only) already covers codebase scouting;
  no custom scout agent is defined. Don't reinvent it.

## The operating loop

1. **Plan (Opus).** Lead reads ROADMAP.md, picks the top queue item, drafts a
   brief: files in scope, acceptance criteria (copied from ROADMAP, never
   paraphrased), verify target. You approve the plan.
2. **Implement (Sonnet).** Lead delegates to `implementer` with the full brief
   in the delegation prompt (subagents see nothing else — no conversation
   history). Implementer edits, runs `./verify fast`, returns diff summary +
   verbatim verify output, writes a trace entry.
3. **Verify (Sonnet).** Lead delegates to `verifier`, which runs
   `./verify full` and reports verbatim. Verifier never fixes anything.
4. **Critique (Opus).** For risky or architectural changes, lead delegates to
   `critic` for adversarial review against ROADMAP acceptance criteria and
   CLAUDE.md invariants. Critic proposes minimal deltas, edits nothing.
5. **Close (Opus + you).** Lead updates ROADMAP.md (it is the only agent
   permitted to), summarizes with provenance, you ratify. The Stop hook
   refuses to let the session end with a red oracle or a dirty-but-unverified
   tree.

Escalation ladder: single session → subagents (this harness) → agent teams
(experimental; only when workers genuinely need to talk to *each other*, not
just report up). Subagent-heavy workflows can run ~7x the tokens of a single
thread — delegate for isolation and parallelism, not out of habit.

## Install into a project

```bash
cp -r claude-harness/.claude claude-harness/CLAUDE.md claude-harness/verify \
      claude-harness/ROADMAP.md  your-project/
mkdir -p your-project/traces your-project/.harness
chmod +x your-project/verify your-project/.claude/hooks/*.sh
# then: fill CLAUDE.md §Domain, fill ROADMAP.md, implement verify targets
```

## The verify contract

`./verify <target>` is the only interface the harness knows. Targets:

- `fast` — seconds, not minutes. Lint, typecheck, unit tests, cheap invariant
  checks. This is Layer-0: it runs constantly and blocks everything.
- `full` — the whole gate: fast + integration + golden datasets + perceptual /
  end-to-end evals (Layer-E). Run before closing a queue item.
- `report` — prints `.harness/last-verify.json` (target, exit code, timestamp,
  git hash) without re-running.

Exit code is the truth: 0 green, nonzero red. Anything the oracle can't check
is by definition an open question in ROADMAP.md, not a claim of correctness.
**Passing ≠ done** — done is oracle green *and* acceptance criteria satisfied
*and* a trace written. The three are checked separately on purpose.
