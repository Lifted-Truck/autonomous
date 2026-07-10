# Development doctrine (applies to all projects)

> Canonical home of the cross-project doctrine. The global `~/.claude/CLAUDE.md`
> imports this file; do not duplicate its content elsewhere — propose changes
> here (they are then versioned and reviewable). Machine-local facts (e.g.
> build quirks of one machine) stay in the global file, not here.

## Visual-first review
When presenting completed work, a PR, or any review request, lead with a visual
presentation — a self-contained HTML report, Artifact, screenshot set, or live
demo — sufficient to evaluate the change WITHOUT reading code. Code diving is
the fallback, not the default. Include: what changed, evidence it works (test
output, renders, before/after), and any open questions.

## Harness by default
"The harness determines performance more than the model." For any new or
adopted repo, apply the harness kit (canonical: `kit/` in the autonomous repo):
- Layered CLAUDE.md: lean root (pointers + gotchas only), subdir files for local conventions
- Hooks for determinism (format/lint via PostToolUse, not instructions), CODEMAP.md, .claudeignore
- Decision logs (DECISIONS.md, append-only) and phase-gated roadmaps (ROADMAP.md outranks other docs)
- Delete stale constraints as aggressively as you add new ones

## Knowledge loop
The knowledge loop (CLAUDE.md/INDEX.md/LIBRARY.md self-improving loop —
canonical: `loops/knowledge-loop/`) installs per-project durable lessons with
an anti-poisoning write gate. Offer it when a project becomes long-lived or
accumulates hard-won lessons. The cross-project audit loop (canonical:
github.com/Lifted-Truck/agent-knowledge-loop) harvests and promotes lessons
up a tree of projects.

## AI/deterministic boundary
AI may interpret language, propose, and judge; AI may NOT be in the path of
scheduling, metrics, validation, or signal processing. Deterministic code
decides; seeded RNG, no wall-clock reads in cores, reproducible outputs.

## Oracle discipline
Tests gate phases; gates are never weakened to pass. Prefer two layers:
Layer-0 (deterministic, CI-blocking, no model calls) and Layer-E (behavioral
evals, measured but non-blocking). Never conflate guaranteed with measured —
state which is which.

## Architecture defaults
Pure, framework-free cores; UI/IO/time live in thin adapters. Swappable
backend seams (prefer engine, fall back locally). Safety by construction
(caps, preallocation, frozen IDs), not by vigilance.

## Reduce, never invent
When behavior is ambiguous, ask rather than guess, and record the resolution
in the decision log. A "reasonable guess" is a signal to ask.

## Cross-project interaction
All cross-project/cross-repo development follows the integrations policy in
[INTEGRATIONS.md](INTEGRATIONS.md) — including the commit/PR responsibility
model (writes stay home; ball-state exchanges; provider-first linked PRs).
