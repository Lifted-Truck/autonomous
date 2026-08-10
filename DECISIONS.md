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

28. **Context budget: always-on load slimmed ~40%, with a verify-enforced
    ceiling** (2026-07-16, human-approved after a measured audit: ~5k tokens
    auto-loaded per session, vs the ~100–150-instruction-slot ceiling in
    research/2026-07-10-memory-governance.md). Four changes: (a) INTEGRATIONS
    .md is NO LONGER auto-loaded globally — its doctrine tenet says read it at
    the start of cross-repo work (JIT retrieval per our own research);
    (b) doctrine tenets "survey before scaffold" + "right-size architecture"
    merged into one "Project structuring" tenet (15→14); DOCTRINE.md now has a
    9000-char budget ENFORCED by ./verify — over budget means merge or delete
    a tenet (the landscape audit's DELETIONS section is the pruning organ);
    (c) the charter template's invariant layer no longer restates
    globally-loaded doctrine (reduce-never-invent, visual-first removed;
    doctrine-applies-on-top stated once); (d) manifest rule: NO status prose —
    manifests hold survey answers + territory registry; phase state lives in
    ROADMAP only (observed drift engine: Orrery's 447-char status field
    re-edited in parallel with its ROADMAP). Rejected: leaving growth
    unchecked (addition must be paid for by subtraction, or doctrine becomes
    noise).
46. **`library-entry.3`: block form admitted on read; distillery's three
    corpus-forced rules adopted; a response letter is never normative**
    (2026-08-10, ruling report-002 §3 + distillery-003). Three adoptions cost
    consumers nothing — structural terminators, the span-open condition, and
    repeated-label continuation-join were already live in distillery, invented
    because implementing v2 against the real corpus required them. Leaving them
    consumer-side is how a contract and its only implementation drift apart
    while both look healthy. The span-open residual risk is recorded, not
    hidden; the structural fix (`[[Lxxxx]]` for cross-refs) is named as the
    destination but NOT ruled, because the corpus is mixed and mandating it
    today strands existing prose.
    **distillery-003 — block form.** ~20 entries across 8+ projects were
    invisible under v1 AND v2, a larger silent loss than v2's ruling recovered.
    It is not one heading form but THREE serializations (bracketed id, bare
    id + em-dash, bare id with the title on the next line) with fields as
    `**label:**`, `- **label:**`, or `| label:`. The check that decided it: do
    they carry the REQUIRED fields, or is this a format that cannot express one?
    Verified against all four projects — every one carries lesson, evidence and
    falsifier. Had they not, the answer would have been migration, because a
    format that cannot express a required field is not a format variant.
    Admitted on READ; line form stays canonical on WRITE. Rejected migration:
    it needs 8 independent residents under writes-stay-home, with every entry
    invisible until the last one acts. The exhaustive still-quarantines list is
    UNCHANGED v2→v3 and the contract now says so — v3 admits new delimiters and
    one new layout, no new absence.
    **Correction on the record:** the distillery-002 response letter said bare
    tier matches "by enum, not by position"; the contract said segment-1 AND
    enum-match. distillery implemented the contract and flagged the discrepancy.
    The letter was wrong — enum-match-anywhere lets a bare enum word in prose
    overwrite `tier`, silent corruption rather than a parse failure. General
    rule now stated in the contract: **the contract file is normative; a
    response letter never is.**

45. **`status.1` contract tests landed in CI; the contract has zero producers**
    (2026-08-09, closing dispatch-001's owed item, 16 days past respond-by).
    dispatch's three fixtures landed verbatim with a stdlib validator
    (`kit/gates/status_validate.py`) wired into `./verify fast`. Two design
    calls. (a) **Returns a list of findings, not a bool** — their third fixture
    pins error GRANULARITY (four *named* findings), which is a materially
    stronger contract than "must be rejected": it catches a validator that
    rejects the right document for the wrong reason, which passes a pass/fail
    test while being useless to a consumer repairing its own output.
    (b) **Targeted validator, not a JSON Schema engine, zero dependencies** —
    this CI installs nothing, so a `jsonschema` dep would be red-for-unrelated-
    reasons or skipped, and a skipped check is the blind-gate trap
    (REPO-HYGIENE). `kit/contracts/status.md` stays normative.
    **The finding the filing surfaced:** swept all 62 repos — NONE emit
    `STATUS.json`, including autonomous, which authored the contract. The writer
    "ships with kit v2 core" and kit v2 is not open, so `status.1` has been
    frozen a month with a schema, an example, one consumer built against it and
    **no producer anywhere**. A contract validated only from the consumer side is
    untested in the direction that matters: nobody has tried to EMIT one and
    discovered the schema asks for something a real project cannot cheaply
    produce. Writer deliberately NOT built here — it is kit-v2 scope and
    building ahead of the kit is how a "temporary" second implementation becomes
    permanent — but the gap is now on the record rather than implicit in a
    degrade-visibly clause that has only ever run in the degraded direction.

44. **Registry paths are case-checked; `path_case_mismatch` reported, never
    auto-corrected** (2026-08-09, from FOUNDATIONS' foundations-001 four-state
    note). They flagged `Morphos`/`morphos` and warned a cross-platform roster
    sweep will hit it, failing in the worst way — a false alarm on the first
    run, when the reader is deciding whether to trust the tool. We had it live:
    `registry.json` carried `~/Documents/tonality-Live` against `Tonality-Live`
    on disk. macOS is case-INSENSITIVE but case-PRESERVING so it resolved
    silently; Linux CI would not, and a second machine is being set up this
    week. Entry corrected; `sweep.derive_status` now reports the disk spelling
    with a test. REPORTED, not auto-corrected — which spelling is canonical is
    the human's call, same stance as `nested_repos`. Chose reporting over
    FOUNDATIONS' `(st_dev, st_ino)` identity comparison deliberately: identity
    RESOLVES the mismatch invisibly, right for a sweep that must not cry wolf,
    but here it is a portability bug worth fixing rather than tolerating. Their
    roster must survive a rename; ours must survive a clone.

43. **`contract_gate` landed as kit-core; second consumer established
    empirically, not by argument** (2026-08-09, foundations-001 proposal).
    FOUNDATIONS offered the enforcement half of Decision 39 — does the file the
    manifest names as the contract declare a version — deliberately narrow: no
    semver ordering, no bump-detection, no prose reading, because Decision 39's
    second half (*was the freeze respected?*) is a human ruling and stays one.
    Landed at `kit/gates/contract_gate.py`. Their two-consumer caveat was
    honest but their proposed answer ("the second consumer is the doctrine
    itself") is self-ratifying — a rule wanting its own enforcement is not
    independent evidence. The real second consumer is empirical: **Orrery, the
    composite worked reference, declares no `contract-version:`**, while its own
    manifest says Lathe pins a version and files briefs for deltas — a live
    pinning relationship against a contract with nothing to pin. FOUNDATIONS
    explicitly refused to check Orrery ("it is not my tree, and if it does not,
    that is a finding for its residents rather than a stick to hand you"), which
    was the correct call; checking it is autonomous's scope. Four negative tests
    re-implemented rather than cited — a gate landed on someone else's word is a
    gate nobody has run — plus one added: prose mentioning `contract-version:`
    mid-line must FAIL, pinning the anchor a future "simplification" would drop.
    Kit changes reach existing repos only on retrofit, so nothing breaks today;
    the Orrery finding is filed separately.

42. **Overdue-`ball:` detection, and why the sweep runs from a session hook
    rather than a scheduler** (2026-08-09). The INTEGRATIONS `ball:` field
    assigns responsibility and nothing escalated it: three exchanges surfaced
    in one week only because the human mentioned them (distillery-002, 13 days
    past respond-by with named content blocked; two mailbox writes untracked
    ~12 days each). `governor/ball_scan.py` now sweeps every repo's mailbox.
    Four modelling rules, each forced by a false positive on the FIRST real
    run — the module is only useful if it is read, so every one of these is
    really a defence against noise: (a) the unit is the exchange **id**, not
    the file — an opening `brief.md` keeps `ball: provider` forever and the
    answer lands in a sibling, so per-file evaluation reports every answered
    thread as permanently overdue; (b) **closure is monotonic** and beats
    date-ordering — antiphon-001 read as 12d overdue while CLOSED because its
    ratification carried the same date as the response it closed; (c) overdue
    is computed **only when the ball is ours** — a respond-by binds the holder,
    so once we answer it is satisfied, not breached; (d) only files that ASSERT
    a ball may determine who holds it — FOUNDATIONS' `ball: none` informational
    note, filed 34 seconds after a real proposal, masked a live ask. Reported
    in its OWN STATUS section, never folded into the ~56-WARN pile, since an
    obligation buried there is findable only by someone already looking.
    **Scheduling: rejected launchd/cron after trying it.** macOS TCC protects
    `~/Documents` and a LaunchAgent does not inherit Full Disk Access, so the
    job returned "Operation not permitted" (exit 512) while STATUS.md kept the
    mtime of a manual run — installed-looking, fresh-looking, doing nothing.
    Granting FDA to a bare interpreter is a worse trade. Instead: a synchronous
    SessionStart hook reads the cache (instant) and an `async` one refreshes it
    (~4s, off the critical path), so the sweep runs with the file access a
    session already has and needs no scheduler. Freshness gap is one session
    and the brief prints the cache age, so staleness is visible rather than
    assumed — the failure that killed the monitor silently for days.

41. **Correspondent-roster sweep: promote signal MET by convergent independent
    derivation; kit-v2 candidate, build deferred** (2026-08-09, foundations-001
    §4). FOUNDATIONS offered a four-state correspondent registry + drift sweep
    as a report, not a request, correctly noting the two-consumer rule left it
    at one consumer. The second consumer is THIS repo, unknown to them: on
    2026-07-27 `registry.json` was found pointing at wrapper directories, and
    five repos — including PUBLIC `audiology`, carrying a machine-identity leak
    for 19 days — were invisible to leak_scan/monitor/clone-roster while the
    roster reported their names as present. Both fixes converged on the same
    shape AND the same deliberate restraint: detect drift, report loudly,
    **never mutate the roster** ("discovering a repo is not registering it" /
    "surfaced, never auto-adopted"). Convergent design under independent
    derivation is the strongest signal the two-consumer rule can produce, and
    neither party could see it alone — which is itself an argument for filing
    resolved-locally findings upstream. Generalization frozen: a hand-maintained
    roster of relationships drifts from reality silently; the countermeasure is
    a deterministic declared-vs-observed sweep that blocks only on
    project-controlled state and cannot mutate the roster. NOT built today —
    kit v2 is not open, and a half-generalized version is worse than two working
    specific ones. FOUNDATIONS' `deferred-with-revisit-trigger` state is the
    piece autonomous lacks: without it the same finding re-surfaces every sweep
    and trains the reader to skip it.

40. **Prior-art bookend inverts for design-first projects, on the record**
    (2026-08-09, foundations-001 §3, ACCEPTED). Decision 30 put Phase 0
    prior-art before the design is committed; a project arriving with a human's
    founding document cannot run that order. Ruling: run it as an AMENDMENT
    PASS against the committed design, inversion recorded in DECISIONS, plus one
    acceptance criterion that is the load-bearing part — **contradictions become
    DECISIONS proposals, never absorbed or discarded**. Without that criterion a
    late pass is *performed rather than used*, and the failure is invisible
    because both produce the same artifact. Rejected: dropping the phase
    (loses it) and silently reordering (loses the record that it was inverted).
    Evidence the form bites, verified rather than accepted: FOUNDATIONS' F1
    produced 8 proposals against an already-committed constitution.

39. **A composite contract file may be a versioned WRAPPER over a normative
    source** (2026-08-09, foundations-001 §2, ACCEPTED). ONBOARDING composite
    move 1 implied the contract document must contain the seam's prose;
    FOUNDATIONS' seam was already §2/§4/§5 of a human-written constitution, so
    following it literally meant duplicating canonical content — a bug under
    README §8, and two copies of a contract drift until no consumer can say
    which text it pinned. Ruling: the invariant is that **exactly one file owns
    the version and the freeze state**, not that it holds the prose; a
    normative-source table satisfies move 1. Move 1 conflated "one place to pin"
    with "one place the text lives" because Orrery — the only worked reference —
    had a contract written AS the contract, so nothing forced the distinction. A
    single worked example is a weak generalization. FOUNDATIONS' offered
    `contract-version:` freeze check accepted as a kit-core gate candidate:
    prose is the reminder, the gate is the enforcement.

38. **FOUNDATIONS registered in the ecosystem tracks; execution projects are no
    longer assumed to be leaves** (2026-08-09, brief foundations-001).
    Registered per the HYPERSAW/ANTIPHON shape. `registry.json` needed no edit —
    verified rather than accepted, the `synthetic-worlds` group rule already
    resolves it with a full harness. But the Execution-project registry's own
    preamble describes its entries as leaves that "feed back only through their
    group scope's knowledge-loop harvest," and FOUNDATIONS is upstream of eight
    registered consumers: its F2 gates HYPERSAW's extraction and a
    contract-version event is an eight-way fan-out. Registering it under a
    description false about it would have been the drift this protocol exists to
    prevent, so a fifth cross-track ordering constraint was added — the first in
    that list originating in an execution project rather than Track A. The leaf
    assumption still holds for every other entry; it needed naming, not silent
    amendment.

37. **`library-entry.2`: the parser loses nothing, the promotion gate judges**
    (2026-07-31, ruling distillery-002 — 13 days past respond-by). Five open
    questions, one principle. A `|`-delimited format that forbids `|` in prose
    is not strict, it is broken (CSV without quoting): HYPERSAW L0016
    quarantined because its lesson contains `|x[n]-x[n-1]|`, absolute-value
    notation in a DSP lesson, and L0016 is domain-general promotion-grade
    content. Rulings: (1) entry boundary is the `[Lxxxx]` marker not the
    newline — fixes morphos/edgewise/wont's 7 wrapped entries with zero
    resident work and needs no continuation character; (2) unlabeled segments
    continue the open field — rejected escaping, which requires every author to
    remember and fails silently when they don't; (3) both tier forms accepted,
    but the bare form is recognized by ENUM MATCH not position, else a title
    containing `|` silently corrupts `tier` (worse than quarantining);
    (4) annotated placeholders → field absent + annotation preserved as
    `<field>_note`, rejecting distillery's option (b) because those annotations
    are real graph edges ("generalises [[L0014]]") and dropping them deletes
    the relational knowledge the warehouse exists to hold; (5) unknown labels →
    `extra{}`, neither quarantining a good entry nor dropping data.
    **Explicitly NOT a weakened gate**: everything newly accepted is a
    formatting variation carrying identical information; everything still
    rejected is missing information, and the contract now lists the four
    quarantining cases exhaustively so forgiveness cannot creep. Falsifier and
    evidence requirements untouched.

36. **Dormancy is a machine-readable, EXPIRING manifest field** (2026-07-28,
    responding to brief `antiphon-001`). ANTIPHON asked to be listed in
    ROADMAP's execution-project registry as deliberately dormant, so a green
    oracle with no commits would not read as abandoned. Granted — but the
    listing alone does not solve the stated problem: `governor/monitor.py` does
    not read ROADMAP.md, so prose is legible to humans and invisible to the
    governor. ANTIPHON trips `STALE` on 2026-08-12 regardless. So dormancy is
    now `project.manifest.json` → `dormant {since, reason, review_by}`, honored
    by monitor. **`review_by` is required**: a permanent flag is how abandoned
    repos hide, so a live declaration suppresses STALE at INFO, an expired one
    raises DORMANT-EXPIRED at WARN *and* restores STALE, and one missing
    `review_by` is ignored entirely — the incomplete form fails toward noise,
    never toward silence. Defers the activity signal only; LEAK/UNGATED/NO-CI
    still fire, because a dormant repo can still be insecure. The brief itself
    proposed this as the better answer; it was right.

35. **monitor gets per-repo fault isolation after one manifest killed it**
    (2026-07-28). `manifest_status_prose` assumed `status` was a string;
    `juce-rag` ships a structured `{"ratified":…, "note":…}` — arguably the
    better shape — and the TypeError took down the entire fleet dashboard. A
    crashed monitor reports nothing, which is indistinguishable from a healthy
    fleet: the precise silent failure the tool exists to catch. Two fixes, and
    the second matters more: (a) flatten dict/list statuses and scan the strings
    inside, so structure cannot smuggle prose past the check either; (b) wrap
    each repo's checks so an unexpected shape yields a HIGH `MONITOR-ERROR` row
    for that repo instead of killing the run. One repo's schema choice must
    never be able to blind the whole sweep. Found only because a brief required
    running monitor — it had been silently dead.

34. **Cross-platform portability made a gate, not a habit** (2026-07-23,
    prompted by the human cloning the roster onto a Windows machine). Three
    silent-failure vectors closed before the clone rather than after:
    (a) **the leak gates were POSIX-only** — `/(Users|home)/<name>/` cannot
    match `C:\Users\<name>\`, so identity committed FROM Windows would have
    passed every gate. Both detectors (bash `leak_gate`, `leak_scan.py`) now
    carry the drive-letter form, with `\\+` so the escaped variant that lands
    in JSON matches too; `USERNAME` added alongside `USER` for the username
    check. (b) **CRLF** — Git for Windows' `core.autocrlf=true` default
    rewrites checkouts, so identical content has different bytes and every
    byte-comparison gate (`content_hash`, hash ledgers, goldens) fails for a
    reason unrelated to the change; a CRLF shebang also kills `./verify` with
    a bare "command not found". Fixed by a committed `.gitattributes`
    (`* text=auto eol=lf`), which beats a global git setting because it
    travels with the repo. (c) **INSTALL-GLOBAL was macOS-only** — new §6
    covers shell (Git Bash, not PowerShell), `python3` availability, clone
    layout for the `~` import, and the Mac-only AU/`auval` exclusion.
    Verified by running the new pattern against known-bad input in raw,
    escaped, and drive-letter forms BEFORE trusting it (the `\s` lesson);
    the test also caught the gate flagging its own explanatory comment, fixed
    by rewriting the comment rather than allowlisting the gate file —
    allowlisting `verify` would blind the gate to real leaks in it.
    Not yet done: `.gitattributes` exists only here; the fleet-wide rollout
    rides the mass-retrofit, and the 22 non-cloneable dirs (3 git-no-remote,
    19 not git) will simply be absent on the Windows machine.
33. **REPO-HYGIENE.md adopted as the canonical security-sweep spec**
    (2026-07-20, human "adopt repo-hygiene"). Moved root → `governor/`; folded
    in the review corrections: (a) secrets scans FAIL-CLOSED on a missing tool,
    never skip (the blind-gate trap that bit us twice); (b) tiered — the
    deps-free `leak_gate` is the Layer-0 CI core, gitleaks/rg live in the
    pre-commit hook + pre-publication audit, not the CI-blocking gate; (c)
    reconciled with the shipped code (leak_gate/leak_scan/monitor/allowlist are
    now its implementation, not a divergent parallel). New content: the
    binary-file gap — `git grep -I` skips binaries, so `.pyc`/EXIF/notebook
    leaks pass every text gate (the tracked-`.pyc` incident, Decision 32's
    cleanup); defense is gitignore/strip, not scan. Doctrine tenet + governor
    README point at it. Allowlisted at the new path so it doesn't trip its own
    gate. Rejected: adopting the doc as-written (its `command -v gitleaks ||
    skip` was fail-open — the exact failure the review caught).

32. **Governor built as the watchdog-MONITOR first; controller deferred**
    (2026-07-20, human "do it"). `governor/monitor.py`: a deterministic
    (no-model) fleet-health sweep — per-repo leaks, un-gated verify, no-CI,
    stale README, manifest status-prose (Dec 28), harness gaps → STATUS
    dashboard. Earned NOW (this session kept hitting these by hand); the
    HALT-sentinel/conductor/coherence-critic stay deferred (no running organ
    fleet to govern — building the control room for an idle factory is the
    speculative escalation the doctrine forbids). First real run caught a
    LEAK regression: Tonality's paths, fixed at commit ca47050, were
    REINTRODUCED by later CLAUDE.md regeneration and went uncaught because
    Tonality is UN-GATED — validating both the monitor and "un-gated repos are
    where leaks recur." Fixed a consistency bug: `leak_scan.py` had drifted
    from the `./verify` leak_gate (missing the `%`/`@` placeholder filters +
    the .leakcheck-allow honoring) → the monitor false-flagged repos the gate
    passed; re-synced, with a comment that the two detectors must stay
    consistent. STATUS.md gitignored (it names private repos — committing it
    to public autonomous would be the cross-repo leak the monitor hunts).

31. **CI-minutes budget: economical triggers, cancel superseded, heavy builds
    stay local** (2026-07-20, after the human hit the free-tier private-repo
    Actions limit). Only PRIVATE repos spend minutes (2000/mo free; public
    unlimited); the drain is private + heavy (JUCE/C++/`auval` — macOS runners
    at ~10× Linux). Kit CI template now defaults: triggers = PRs + push-to-main
    only (feature-branch feedback still via the PR), `concurrency` cancels
    superseded runs, `paths-ignore` skips docs-only, and `verify full` (auval/
    codesign) stays out of CI (local/human). Contrast Decision 26 (get CI
    running everywhere) — this is HOW, economically. Rejected: on-every-push
    everywhere (what exhausted the quota) and moving heavy repos public just
    for free minutes (visibility is an IP decision, not a CI one — VISIBILITY.md).
    Retrofit propagates the economical template; existing repos' agents adopt it.

30. **ROADMAP carries Prior-Art bookend phases (agent swarm)** (2026-07-18,
    user). Every scaffolded ROADMAP includes an EARLY "Phase 0 — Prior-art
    landscape" (fan-out research before the design is committed: existing
    solutions, papers, patents, competing products, failure modes → reflected
    in design + DECISIONS) and a LATE "pre-ship Prior-art & IP re-scan"
    (re-run before public release; patent/IP landscape for anything
    commercializable, per the disclosure-timing asymmetry in VISIBILITY.md).
    Findings live in `docs/prior-art.md`, dated + cited. In the ROADMAP
    skeleton (kit/scaffold-agentic-harness.prompt.md). Rationale: the swarm
    reaches adjacent domains a single searcher misses (basin-escape, per the
    methodology research); early prevents reinventing/landmines, late catches
    drift + protects IP before the irreversible act of disclosure. Kit-level,
    not a doctrine tenet (budget; it's a ROADMAP-artifact rule).

29. **Foreign-scaffold override clause: standard mechanisms, project
    substance** (2026-07-16, user). Chat-exported kits (a Claude session
    exporting a starter scaffold) conflict with the spinup/retrofit protocol.
    Reconciliation rule, now in ONBOARDING + /retrofit: for any function the
    ecosystem kit provides, the kit's mechanism REPLACES the exported one
    (two half-compatible mechanisms = drift by construction); the exported
    kit's project-specific substance is MIGRATED into standard slots
    (§Domain, ROADMAP, DECISIONS, LIBRARY seeds, bespoke checks → verify
    targets) BEFORE anything is deleted; unmappable content is surfaced to
    the human, never silently discarded. Map first, replace second, delete
    only what has been mapped. Rejected: letting exported conventions stand
    alongside kit conventions (dual mechanisms) and wholesale replacement
    (destroys idiosyncratic project value — often the bespoke checks).

27. **Privacy is enforced by a gate, not a sweep** (2026-07-13). `leak_gate` is
    now kit-core: a self-contained bash function in every project's `./verify`
    (so it blocks the Stop hook AND CI from one artifact — a repo must be
    verifiable without autonomous cloned, hence the deliberate copy rather than
    a shared import). Doctrine tenet added: "Never commit machine identity."
    `governor/leak_scan.py` demoted to fleet *backstop* (un-gated repos +
    cross-repo private-name exposure, which a per-repo gate structurally cannot
    see). Rationale: a monthly sweep leaves a leak live for up to 30 days; a
    commit-time gate makes it zero. History remediation: see
    governor/HISTORY-REMEDIATION.md — verdict is "don't, except dispatch (whose
    bad blobs are unpushed, so rewriting is free)"; a rewrite cannot un-expose
    what is already public, so it buys little at real cost.
    **Self-audit (uncomfortable, recorded):** autonomous itself is 3/8 on the
    harness it defines — missing CLAUDE.md, manifest, knowledge loop, traces,
    hooks — violating its own Decision 11. Retrofitting the standards repo is
    now a tracked task; the session's real lessons (exec-bit, bare-except
    swallowing an import error, `\s` dead in POSIX ERE) currently have no
    durable in-repo home, which is exactly what a LIBRARY is for.

26. **CI is a kit-core property: GitHub Actions runs `./verify fast` on every
    push/PR** (2026-07-13, user goal "every project runs CI"). Not new checks —
    the cloud runs the project's one oracle, mirroring the local Stop-hook gate.
    Reference workflow added to autonomous (`.github/workflows/ci.yml`);
    template at `kit/templates/ci.github.yml` ships via `/spinup`, retrofits
    via `/retrofit`. Nuances recorded: needs a remote; `verify full` runs in CI
    only where the runner supports it (audio-plugin auval/codesign is macOS-only
    + human-run → CI `fast` only); private repos draw Actions-minutes quota.
    Rollout respects writes-stay-home: each repo's residents add their own
    workflow (autonomous done as reference; others via their agents or explicit
    human authorization). This is also the required-checks foundation the P2
    merge queue assumes.

25. **Model-routing rule generalized: pin explicitly + cap at Opus**
    (2026-07-13, human — "better than 'never Fable'"). Supersedes the
    Fable-specific framing of #23. Two rules attacking the actual failure mode
    (silent inheritance): (1) every agent's model is PINNED at spawn, never
    inherited from the session/parent default; (2) never exceed the latest
    Opus — the Claude 5 flagship family (Fable) or any future above-Opus tier
    is used only on explicit human request. Durable (a ceiling, not a name
    that goes stale) and root-cause (the accident was an inherited tier, not a
    named one). In DOCTRINE.md "Model routing (pin explicitly; cap at Opus)".

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
