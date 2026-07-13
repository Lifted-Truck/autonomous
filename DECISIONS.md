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
11. **Memory loops are default-on for every project; the global memory is
    two pools** (2026-07-10, user proposal, adopted — supersedes the
    "offer when long-lived" stance inherited from the interactive-era loop
    doc). Every scaffolded project gets the knowledge loop in the kit CORE
    (cost ≈ zero on quiet projects; early lessons are unrecoverable if not
    captured; uniformity is what makes sweeping automatable — the write gate,
    not absence of the loop, is the bloat safeguard). Global memory =
    (a) an **append-only stream** (warehouse): every candidate lesson from
    every sweep, dated, with provenance — read ONLY by a top-level analytical
    agent, NEVER retrieval context for working agents (the 13%-vs-39%
    bloat finding); enables longitudinal analysis (recurrence, demote-recur
    cycles, cross-project failure signatures) that per-sweep convergence
    detection structurally misses; (b) the **distilled pool** (mart): the
    top of the existing audit-loop hierarchy, entered only through its
    promotion gates. Heavy machinery (audit threads, fleets, governor)
    remains earned; the loop itself is not.
12. **Two execution projects opened as ecosystem tracks: `distillery`
    (global memory) and `dispatch` (progress publishing)** (2026-07-10).
    Scaffolded with the Generic Agent Harness, provisional manifests
    (human ratifies at D0/E0 gates), and intake briefs filed here through
    the integrations channel (dispatch-001, distillery-001 — first live use
    of the protocol, incl. the mailbox exception now written into
    INTEGRATIONS §3). Decision-in-principle, gated post-D4/P3: distillery
    becomes the ecosystem's OPERATIONAL lead (the analyst seeds the
    ecosystem curator/governor) while autonomous remains the standards/
    doctrine/kit home — separation of powers between the body that defines
    gates and the entity operating under them. Rejected: autonomous as
    operational lead (conflates standards with operation; its residency is
    meta-level by design).
23. **Model routing is now a DOCTRINE tenet (loaded every session), with an
    explicit Fable-subagent prohibition** (2026-07-13, after a project
    accidentally spawned Fable sub-agents). Root cause: model routing lived
    only here in DECISIONS (16–18), so sessions in other projects never loaded
    it. Fix: added a "Model routing (tiers are human-gated)" tenet to
    doctrine/DOCTRINE.md — which the global CLAUDE.md imports, so it now loads
    everywhere — plus a direct hard-rule line in the global CLAUDE.md itself
    (belt-and-suspenders for a safety rule). Rule: Fable is never used for
    sub-agents or auto-selected for any role unless the human explicitly asks
    in that session; leads→Opus, subagents→Sonnet, scout/verbatim→Haiku;
    tier changes are always the human's deliberate call. Supersedes nothing;
    promotes 16–18 from decisions to loaded doctrine.

24. **Correction to #23: the Fable rule lives ONLY in DOCTRINE.md, not
    duplicated in the global CLAUDE.md** (2026-07-13). #23 also added a direct
    hard-rule line to the global `~/.claude/CLAUDE.md` — that violated
    INSTALL-GLOBAL.md's "never edit doctrine in the global file; redundant
    copies drift" split rule, AND it does not propagate (global files are
    machine-local, never synced). Removed it. The DOCTRINE.md tenet + the
    `@import` every machine's global file already carries is the single source
    and the propagation mechanism: a machine gets the rule by `git pull` on
    autonomous — nothing to hand-edit per machine. The "belt-and-suspenders"
    instinct was wrong here: if the import fails, ALL doctrine fails visibly,
    so one duplicated rule buys nothing.

22. **Licensing: public showcases get PolyForm NC; private commercial
    candidates stay unlicensed until productization** (2026-07-13, human).
    Tonality + Audiology carry PolyForm Noncommercial 1.0.0 (grant NC use,
    reserve commercial to the owner). The private music repos get NO license
    deliberately — a license grants rights, and you don't grant rights on
    something you may sell; private + unlicensed = all-rights-reserved =
    maximum optionality; choose a license per product at the productization
    decision. Rejected: applying PolyForm NC to the private repos too (would
    grant NC rights that could undercut a future paid product). Detail:
    VISIBILITY.md → Licensing decisions.

21. **Repo visibility policy: novel music IP private, infra/methodology public**
    (2026-07-13, human). Disclosure is irreversible and starts patent clocks;
    private preserves optionality at ~zero cost. Music/audio devices → private
    by default (Tonality + Audiology kept public as resume showcase);
    infrastructure + the methodology → public (portfolio/credibility);
    client-confidential → private. Full policy + the actionable per-repo list:
    VISIBILITY.md. Sweep gained an opt-in `--visibility` gh check (network;
    outside the deterministic core). Corrected a prior error: harness-grader
    is PRIVATE, not public (I had conflated remote-presence with public-ness).
    Visibility changes are the human's to run (`gh repo edit … --visibility …`)
    — an access-control action, not mine.

20. **Human-epistemics methodology is a sibling project; its grounding is
    harvested here** (2026-07-13, user-approved "do both"). The user's document
    "The Applied Epistemics of AI Integration" is scaffolded as its own project
    (`ai-integration-methodology/`, rung 1) — the human-epistemic half of the
    practice, distinct from autonomous's agentic/deterministic half and carrying
    a consulting-product identity. autonomous harvested only the citable
    grounding: research/2026-07-13-human-ai-epistemics-delegate52.md (DELEGATE-52
    + a seven-mode failure taxonomy, each mapped to the doctrine it validates)
    and a new doctrine tenet "Human epistemic discipline at the gates" (the
    human's share of friction the machine can't enforce). DELEGATE-52's primary
    is flagged attributed-not-verified — booked for the next landscape audit.
    Rejected: merging the methodology into autonomous (blurs two sharp things;
    mixes a business offering into dev infrastructure).

19. **`/spinup --composite` variant adopted** (2026-07-13, user-approved).
    The composite-project pattern (umbrella repo + shared contract + N
    contract-bound module territories under a `modules_dir/`, rung 2→3 by
    default) is now canonical in ONBOARDING Part 2 and wired into the spinup
    command. It is the organ model applied intra-repo (territory = subdir, not
    a repo). First worked example: Orrery (DECISIONS there #5–9). Rejected:
    repo-per-module for composites (forces a freely-changing seam into a
    cross-repo versioned contract — see Orrery #6). Kit-v2 will formalize the
    `composite` manifest schema.

13. **Replication/onboarding instructions live in this repo (ONBOARDING.md),
    not a separate overview repo** (2026-07-10). An overview repo would have
    to describe this repo's content — duplication, hence drift — and the
    other machine's first step is already "clone autonomous"
    (INSTALL-GLOBAL.md). Rejected: separate repo; docs inside distillery/
    dispatch (they're execution tracks, not the front door). Noted
    dependency: replicating the execution tracks on another machine requires
    them to get remotes first (pending user's visibility call).
    [Resolved 2026-07-10: remotes created — github.com/Lifted-Truck/
    distillery and /dispatch, both pushed.]
14. **Ecosystem sweep/watch allowlist is canonical in `registry.json`**
    (2026-07-10, user-specified). Scope: `~/Documents/Claude` immediate
    children minus `Projects`, with `synthetic-worlds` as a GROUP (its ~16
    children are each independent projects); plus `~/Documents/Tonality`,
    `tonality-core`, `tonality-Live`, `substack2pdf`, `ableton-wrangle`.
    Rule-based (self-maintaining as folders are added), not enumerated.
    Harness/loop status is DERIVED at sweep time, never hand-maintained —
    un-normalized projects are swept-and-marked, so normalization is an
    incremental visible retrofit, never a sweep blocker. Per-consumer flags
    (dispatch `public:`) layer in consumer configs. Rejected: per-consumer
    duplicate rosters (drift) and hand-maintained status fields (stale by
    construction).
15. **First kit-v2 contracts shipped: `library-entry.1` and `status.1`, plus
    the sweep primitive** (2026-07-10, answering briefs distillery-001 and
    dispatch-001; both balls returned to consumers). Contracts live in
    `kit/contracts/` (one canonical home; loop prompts stay canonical for
    behavior); sweep lives in `kit/sweep/` (stdlib-only, tested, registry-
    driven, consumer-owned ledgers). `public:` deliberately excluded from
    STATUS — publishability is consumer policy (a project can't flag itself
    into a publication). This repo now runs its own `./verify` (fast: sweep
    tests + artifact parsing + structure; full: +live-registry smoke — 42
    projects resolve). D0/E0 manifests treated as ratified per user
    go-ahead; D1/E1 are the open fronts.
16. **Model-tier selection is human-gated, ecosystem-wide** (2026-07-11,
    user mandate). The governor/watchdog/conductor never auto-swaps model
    tiers, and automated threat-analysis / security-scanner integrations
    that can trigger provider-side model demotion are excluded from the
    stack — the user has tripped such a demotion before and escalating or
    changing models is always their explicit decision. Any candidate tool
    carrying such a component is flagged for human review, never silently
    adopted. (Context: review of the `fleet` supervisor repo — its
    mechanisms are catalogued as conductor prior art in ROADMAP; its
    multi-backend model routing would, if ever adopted, keep tier
    selection human-gated per this decision.)
17. **Interim model-routing defaults** (2026-07-11, user): top-level/lead
    agents default to the **latest Opus**; subagents default to the
    **latest Sonnet**; **Haiku** is pinned for verbatim-report and
    read-only-scout class tasks (the harness `verifier` — run the oracle,
    report verbatim, localize the failure — and the built-in Explore
    scout, which is already Haiku). Model-tier upgrades beyond these
    defaults are the user's explicit per-session call (Decision 16).
    Revisit when the user changes plan/lineup; partially resolves DESIGN
    §8 open question 5 for the interim.
18. **Clarifies 17 — Opus covers top AND mid-level agents** (2026-07-11,
    user). The dividing line is role shape, not hierarchy depth: **Opus for
    judgment-bearing roles** (lead sessions, organ leads, critic,
    coherence-critic, curator promotion judgment, distillery analyst);
    **Sonnet for scoped execution** (implementer-class: build to a brief
    with acceptance criteria); **Haiku for verbatim-fidelity/scout roles**
    (verifier, Explore). The harness trio already conforms (critic was
    always Opus); future kit-v2 profiles pin per this rule.
