# Decisions on record (append-only)

Each entry: the decision, the alternative rejected, and why. Never rewrite
history; supersede with a new numbered entry.

1. **`autonomous/` is the canonical home for all harness infrastructure**
   (2026-07-10). Everything ad-hoc at the Claude root consolidates here or is
   pointed at from here; old locations become tombstone pointers. Rejected:
   leaving artifacts distributed with an index — drift between copies was
   already observed (audit-loop root files vs published package).
2. **Component repos stay canonical where already published** (2026-07-10).
   The audit loop's canonical home remains
   github.com/Lifted-Truck/agent-knowledge-loop (already public, newer than
   the root copies); this repo points at it. Rejected: importing it here —
   would create a second editable source of published content.
3. **Kit v2 replaces kit v1 outright** (2026-07-10, user mandate). v1 frozen
   in `archive/kit-v1/`. v2 shape: core + agent-type profiles that agents can
   scaffold for their own type (DESIGN §6). Rejected: incremental v1 updates —
   v1 is single-threaded-era and the user prefers a research-backed rebuild.
4. **Doctrine is single-sourced in `doctrine/` and imported by the global
   CLAUDE.md via `@` imports** (2026-07-10). Machine-local facts stay in the
   global file. Rejected: duplication (drifts) and bare pointers (loses
   auto-load).
5. **Integrations responsibility model: writes stay home** (2026-07-10).
   Only residents commit to a repo; cross-repo work = two linked PRs,
   provider lands first, consumer bumps pin second; exchanges carry a `ball:`
   field so exactly one side owns the next move; consumer contract tests are
   consumer-authored but resident-landed. Closes the commit/PR ownership gap
   in the Tonality-era protocol. Rejected: visiting commits (bypass the
   resident harness) and single cross-repo PRs (no such primitive exists,
   and responsibility blurs).
6. **Remote: github.com/Lifted-Truck/autonomous, currently PUBLIC**
   (2026-07-10). Visibility was the repo's state at consolidation time;
   flagged to the user — flip to private is a one-click change if desired.
7. **Research reports are preserved verbatim in `research/`** (2026-07-10),
   as the citable evidence base for kit v2's INSIGHTS and future design
   arguments. Summaries live in DESIGN.md; the reports are the source.
8. **Multi-agent is a visible option at project structuring, never the
   default** (2026-07-10, user mandate). Kit v2's scaffold opens with an
   explicit architecture menu (single thread / thread + subagents / organ
   fleet), each rung earned by project shape. Rejected: fleet-by-default —
   contradicts the token economics and the harness-outranks-head-count
   evidence.
9. **Clarity standard: every system keeps a living README** (2026-07-10,
   user mandate). Human-orientable without reading code; freshness maintained
   on a loop; staleness visible, never hidden. A possible global daily
   README-refresh agent is parked in ROADMAP deferred, not decided.
10. **Kit v2 opens with a standard spin-up survey → committed manifest →
    deterministic scaffolding** (2026-07-10, user proposal, adopted). A fixed
    repeatable question list captures project scope; answers land in
    `project.manifest.json`; deterministic code applies templates from the
    manifest. Rationale: MAST found ~42% of multi-agent failures are
    specification failures — the survey moves spec capture to the cheapest
    possible moment (before any code exists), and answers-as-data makes
    scaffolding idempotent, diffable, and re-runnable. Rejected: free-form
    setup conversations (unrepeatable, answers evaporate) and fully-auto
    detection (guesses exactly the things only the human knows — "reduce,
    never invent").
