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

## New projects: survey before scaffold
When asked to create, start, or scaffold a new project (any phrasing), do not
improvise a structure: follow the new-project procedure in the autonomous
repo's ONBOARDING.md (Part 2) — the 9-question spin-up survey comes first,
its answers land in `project.manifest.json`, and the architecture rung is
asked, never defaulted. The `/spinup` command wraps this.

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

## Human epistemic discipline at the gates
The machine enforces friction (oracles, hooks, fresh-context critics); the
human owns the friction the machine can't. At every ratification gate: surface
the outcome you're hoping for BEFORE you evaluate, so you can be suspicious
when you arrive at it — "your greatest barrier to the truth is that which you
wish to be true." A conclusion that arrives comfortably is a signal to examine
it more closely, not to accept it. Uninterrupted flow is where epistemic drift
accelerates, so adversarial stress-testing and interrogation of comfort are
designed-in, not failures of smoothness. When conversations compress into
shorthand, periodically re-anchor it against its foundations — drift hides in
compression. (Grounding: research/2026-07-13-human-ai-epistemics-delegate52.md;
the deeper treatment is the sibling human-epistemics project. Empirically,
stronger models fail *invisibly* — polished output that is subtly wrong — which
is exactly why a comfortable-looking result earns more scrutiny, not less.)

## Right-size the agent architecture (multi-agent is an option, never a default)
At project structuring time, the architecture menu is presented explicitly and
chosen deliberately: (1) single-threaded agent, (2) single thread + read-only
subagents / fresh-context verifier, (3) organ fleet (the full autonomous
paradigm). Each rung is *earned* by the project's shape — parallelizable
verifiable work, genuine seam count, value that justifies the ~15× token
multiplier — never assumed. Escalate a rung only when the current one is the
demonstrated bottleneck; the evidence base says harness quality outranks
head-count (research/2026-07-10-multiagent-systems-survey.md, lessons 9–10).

## Model routing (pin explicitly; cap at Opus)
Two rules, because the failure mode is silent inheritance of the wrong tier:
1. **Pin every agent explicitly; never inherit.** Each sub-agent's model is set
   at spawn (frontmatter or the spawn call), never left to inherit the
   session/parent default — inheritance is exactly how the wrong tier
   propagates without anyone choosing it.
2. **Never exceed the latest Opus.** The latest Opus is the default ceiling.
   Anything above it — the Claude 5 flagship family (e.g. Fable) or any future
   above-Opus tier — is used ONLY when the human explicitly asks in the current
   session. No project or template reaches above Opus by default.

Default tiers under that ceiling: judgment-bearing roles (leads, critics,
curators, analysts) → latest Opus; scoped-execution sub-agents → Sonnet;
verbatim-report / scout roles → Haiku. Tier selection, escalation, or change is
always the human's deliberate call, never a side effect of a default, template,
or tooling (and never via integrations that could trigger provider-side tier
changes).

## Clarity standard (living README)
Every system keeps a current, human-readable README: what it is, the map, the
status — sufficient for a human to orient WITHOUT reading code or history.
README freshness is maintained on a loop (curator duty where a curator runs;
session-end discipline otherwise), and staleness is visible, never hidden —
a dated "last verified" line beats silent rot. A repo whose README lies about
it is a bug of the same severity as a failing test.

## Cross-project interaction
All cross-project/cross-repo development follows the integrations policy in
[INTEGRATIONS.md](INTEGRATIONS.md) — including the commit/PR responsibility
model (writes stay home; ball-state exchanges; provider-first linked PRs).
