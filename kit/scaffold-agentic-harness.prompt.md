# Prompt: Scaffold the agentic harness into this project

You are setting up (or retrofitting) a project so that **autonomous agents can build
correctness-critical work in it at volume without colliding or drifting from the
design.** This is the reusable scaffolding distilled from a project that ran a fleet
of agent threads for nine months. Treat it as a one-time setup task that composes
three layers:

1. **Mechanical harness** — hooks, layered CLAUDE.md, CODEMAP, ignore rules.
   *Installed by the best-practices kit — you invoke it, you don't re-derive it.*
2. **Self-improving knowledge loop** — CLAUDE.md/INDEX.md/LIBRARY.md.
   *Installed by the knowledge-loop prompt — you invoke it verbatim.*
3. **This layer** — the doctrine, the determinism/oracle gates, the four-way
   epistemic firewall, and (optionally) the multi-thread coordination model.

The two composable installers live alongside this file:
- Mechanical harness → `~/Documents/Claude/claude-code-best-practices/claude-code-best-practices/bootstrap.sh`
- Knowledge loop → `~/Documents/Claude/integrate-knowledge-loop.prompt.md`

## Operating contract (how you run this)

- **Adapt, never transplant.** Everything below is a *pattern*, not a fixture. Name
  the project's own domain, stack, and "domain core"; strip anything that doesn't
  apply. Copying another project's specifics verbatim is the failure mode this prompt
  exists to prevent.
- **Tier to project size.** The Core module is for every larger project. The
  Coordination modules are opt-in — propose them only when the project's shape earns
  them (a second implementation, external consumers, a parallel audit).
- **Phased and idempotent.** Survey → Plan → Apply → Verify. Do **not** write any
  files until Phase 3. Every block you insert is delimited by `<!-- MARKER:START -->` /
  `<!-- MARKER:END -->`; re-running replaces only what's between the markers. Never
  clobber existing content; never overwrite a file you didn't create without showing
  the diff first.
- **Reduce, don't invent.** When project behavior is ambiguous, ask rather than guess,
  and record the resolution in the decision log. A "reasonable guess" is a signal to ask.

---

## Phase 1 — SURVEY (read-only)

1. Inspect the repo root. Report which of these already exist: `CLAUDE.md`,
   `ROADMAP.md`, `CODEMAP.md`, `.claudeignore`, `.claude/settings.json`, `INDEX.md`,
   `LIBRARY.md`, `.github/workflows/`, a test suite, a golden/snapshot directory.
2. Detect the stack (language, test runner, formatter/linter, package manager) and
   the run commands. Note whether there is **no bare interpreter** quirk (e.g. a venv
   that must be called explicitly) — capture the exact invocation.
3. Interview the user for the project's shape (ask only what you can't infer):
   - **What is it?** A library/engine, an app, a service, a pipeline?
   - **The domain core** — what is the hard, exact logic this project owns that an LLM
     is bad at (combinatorics, numerics, parsing, state machines)? This is what the
     *deterministic* side must own end-to-end.
   - **Second implementation?** Will there be a port / reimplementation / native build
     that must stay in parity? (→ Port-pin module)
   - **Consumers?** Will other projects or agents depend on this one's output surface?
     Is this project itself a *consumer* of a shared engine? (→ Integration module)
   - **Parallel audit?** Is it worth a separate thread that hunts for bugs/regressions
     independently of the dev loop? (→ Audit module)
4. Report the 3–6 categories of hard-won knowledge worth accumulating here (these seed
   the knowledge loop's retrieval tags in Phase 3).

## Phase 2 — PLAN (propose, don't write)

Present a short plan naming which files you create vs. modify, then a **module menu**
with your recommended default (install / skip) and a one-line rationale each:

**Core (recommend for every larger project):**
- **A. Doctrine block** → appended to root `CLAUDE.md`.
- **B. Determinism & oracle gates** → test-layer conventions + CI + (if the domain
  core has stable outputs) a golden/conformance harness.
- **C. Epistemic firewall** → `ROADMAP.md` decision log + the four-knowledge-systems
  scope-boundary, wired to the knowledge loop.
- **D. Mechanical harness** → run the best-practices `bootstrap.sh`.
- **E. Knowledge loop** → run `integrate-knowledge-loop.prompt.md`.

**Coordination (opt-in, only if Phase 1 earned it):**
- **F. Audit thread** — separate worktree, own checks dir fenced out of the dev suite,
  files findings as issues.
- **G. Port-pin** — a fingerprint of the surface a second implementation vendors, with
  a test that fails on drift.
- **H. Integration channel** — an `integrations/` brief↔response protocol for
  consumers, plus the shared-engine boundary rules.

Also decide two forks (state your default):
- (a) Golden/oracle: **strict pinned outputs** vs. **invariant checks only** — pick
  strict when outputs are deterministic and stable; invariants when they're fuzzy.
- (b) CI: **blocking on a version matrix** vs. **single-version smoke** — default to
  blocking-on-matrix for anything correctness-critical.

**Pause for confirmation before Phase 3.**

## Phase 3 — APPLY (write, idempotently)

Execute in this order so later layers can see earlier ones:

1. **Mechanical harness (D).** Run the best-practices bootstrap against the repo root
   (`bootstrap.sh <repo>`; `--dry-run` first). It is non-destructive. Then tighten the
   generated root `CLAUDE.md` to pointers + gotchas only, and fill `CODEMAP.md` with
   the real structure.
2. **Doctrine (A).** Insert the DOCTRINE block (below) into root `CLAUDE.md` between
   its markers, with every `<PLACEHOLDER>` resolved to this project's specifics. Delete
   any tenet that genuinely doesn't apply — and say which and why.
3. **Epistemic firewall (C).** Create `ROADMAP.md` from the skeleton (below) if missing;
   seed it with the decisions already made this session. Insert the
   FOUR-KNOWLEDGE-SYSTEMS block into root `CLAUDE.md`.
4. **Determinism & oracle gates (B).** Add the test-layer conventions; if fork (a) is
   strict, create the golden harness and wire "one case per public entry point, total
   coverage by construction." Add/confirm the CI workflow per fork (b).
5. **Knowledge loop (E).** Run `integrate-knowledge-loop.prompt.md` verbatim (it has
   its own phases and markers). Feed it the retrieval tags from Phase 1.
6. **Coordination modules (F/G/H)** only if approved — use the templates below.

Show a summary of every file created/modified.

## Phase 4 — VERIFY

- Run the test suite and confirm the Stop hook blocks on a red suite (introduce a
  trivial temporary failure, confirm the block, revert).
- Confirm CI config is valid and mirrors the local gate.
- Confirm every `INDEX.md` id resolves to a `LIBRARY.md` anchor and back.
- Restate in a few sentences: what an agent's *next* session in this repo will read
  first, what gates its work must pass, and where each kind of fact is written.

---

# Blocks to insert verbatim (resolve every `<PLACEHOLDER>`)

## DOCTRINE block → root CLAUDE.md

<!-- DOCTRINE:START -->
## Doctrine (standing rules — a rule an agent can forget is worthless, so each names its enforcement)

- **The AI / deterministic boundary.** AI may interpret language, propose, and judge.
  AI may **not** sit in the path of scheduling, metrics, validation, or
  <DOMAIN-CRITICAL-PATH, e.g. signal processing / money movement / ranking>.
  Deterministic code decides. *Enforced by:* seeded RNG, no wall-clock reads in cores,
  pure framework-free cores with IO/time/UI in thin adapters, reproducible outputs.

- **Reduce, never invent.** Derive results from primitives and explicit rules, not
  stored answers the code can't show its work for. Handed missing information, a
  function **errors — it does not guess**; on ambiguity, ask and record the resolution.
  *Enforced by:* <the operation that must raise rather than fabricate — name it>.

- **Oracle discipline.** Tests gate progress; gates are never weakened to pass. Keep
  two layers and never conflate them: **Layer-0** deterministic, CI-blocking, no model
  calls; **Layer-E** behavioral/measured, non-blocking. State which is which.
  *Enforced by:* `<blocking test path>` vs. `<fenced eval path>`.

- **Surface uncertainty; don't fabricate confidence.** Where more than one reading is
  valid, return them ranked with the evidence for each; a confident wrong answer is
  worse than a surfaced uncertainty. Report deterministic facts as the single values
  they are. *Enforced by:* <ranked-candidates + margin/flag on interpretive results —
  or delete this tenet if the project has no interpretive surface>.

- **Harness by default.** If it must happen every time, a machine makes it happen — not
  a reminder in prose. *Enforced by:* the Stop hook and CI below.

- **Visual-first review.** Every capability change ships a self-contained visual (HTML
  report, artifact, screenshot set, or live demo) sufficient to evaluate it *without
  reading the diff*. Code diving is the fallback. *Enforced by:* `docs/reviews/`.

- **Architecture defaults.** Immutable, hashable core objects; typed result structures,
  never ad-hoc dicts; swappable backend seams that prefer a shared engine and fall back
  locally behind the same API, surfacing which source answered.
<!-- DOCTRINE:END -->

## FOUR-KNOWLEDGE-SYSTEMS block → root CLAUDE.md

<!-- KNOWLEDGE-SYSTEMS:START -->
## Where each kind of fact is written (keep these disjoint — a write to the wrong one is a bug)

This project separates four knowledge systems on purpose; keeping them disjoint is what
prevents drift. Before writing anything down, decide which system owns it:

- **ROADMAP.md** owns *decisions and plans* — the build sequence, decisions on record,
  phase gates, deferred scope. A new decision or a "what to build next" is a ROADMAP
  edit. It is the single source of truth for direction; any forward-looking statement
  elsewhere defers to it.
- **CLAUDE.md (layered) + the code** own *structure facts* — where things live, layer
  rules, local conventions. Root stays lean (pointers + gotchas); per-directory files
  hold local conventions. No forward-looking plans here — link a ROADMAP phase instead.
- **`~/.claude/…/memory/`** owns *this operator's private, machine-local* cross-session
  state. Never committed; never travels to other agents/threads.
- **INDEX.md + LIBRARY.md** own *repo-shared agent-process lessons* — hard-won "how to
  work in this repo without re-tripping a wire," committed so every thread inherits it.
  A lesson belongs here **only if none of the three above own it.**

**Anti-poisoning write gate** (governs LIBRARY): this loop feeds its own output back as
input, so a wrong lesson written once is reinforced forever. Prefer not writing over
writing unverified; every lesson states what would falsify it; if a retrieved lesson
contradicts present evidence, trust the evidence and demote the lesson.
<!-- KNOWLEDGE-SYSTEMS:END -->

## ROADMAP.md skeleton (create if missing)

```markdown
# <Project> — ROADMAP

> **Single source of truth for project direction.** The build sequence, decisions on
> record, target consumers, and deferred/demoted scope all live here. Any forward-looking
> statement anywhere else (README, CLAUDE.md, docstrings) defers to this file. When you
> make or reject a planning decision, fold it in *in the same PR* — an unrecorded
> decision isn't decided.

## Build sequence (phase-gated)
Phase gates are never weakened to pass. A phase closes only when its gate is green.
- **Phase 1 — <name>.** Gate: <the exact test/fixture set that proves it>.
- **Phase 2 — <name>.** Gate: …

## Decisions on record (append-only)
Each entry: the decision, the alternative rejected, and why. Never rewrite history;
supersede with a new numbered entry.
1. **<Decision>** — <one line: what and why; what was rejected>.

## Target consumers / applications
<who depends on this and what they need — drives what "shipped" means>

## Deferred / demoted
<explicitly out of scope, with the reason, so it isn't silently re-litigated>
```

## Determinism & oracle gates (module B — apply to the test layer)

```
- Core objects immutable and hashable; results are typed structures with a to_dict()/
  serialize seam, never ad-hoc dicts.
- Cores are seeded and wall-clock-free: no time.now()/Date.now()/random-without-seed in
  any module on the decision path. Time and randomness enter through adapters.
- Stop hook (from the mechanical harness) runs the suite and BLOCKS session end on red.
- CI mirrors the Stop hook and is blocking <on the version matrix per fork (b)>.
- If fork (a) = strict golden: one deterministic, input-fixed case per public entry
  point, replayed against a committed golden file; floats compared at a fixed tolerance;
  coverage total by construction (a meta-test fails if an entry point has no case).
  Regenerate the golden in the SAME change that alters behavior, so the diff is visible.
- Never weaken a gate to make it pass. If a gate is wrong, fix the gate deliberately and
  record why in the decision log.
```

---

# Coordination modules (opt-in — install only what Phase 1 earned)

The principle across all three: **each parallel thread gets its own locus, a write
boundary it cannot cross, and one mechanical channel to signal back. Coordination is a
property of the structure, not a task on anyone's list — no thread must remember to tell
another anything.**

## F. Audit thread
- Runs in its **own git worktree**, not the dev checkout (`git worktree add ../<proj>-audit -b audit main`).
- Writes **only** under `audit/`; never edits source, tests, ROADMAP, or CLAUDE.md.
- Its checks live in `audit/checks/` and are **fenced out of the dev suite** (e.g.
  `testpaths = ["tests"]`) so a dev fix can never redden an audit check in the Stop hook,
  and vice-versa. CI runs both as separate jobs.
- Findings are filed as **issues** (severity-labeled, each citing the contract violated).
  A proven invariant is promoted into the dev suite only via a reviewed change.
- Contract file: `audit/AUDIT.md`.

## G. Port-pin (second implementation in parity)
- A committed `pin.json` **fingerprints exactly the surface** the second implementation
  vendors — hash **only the fields that are exactly reproducible across platforms**
  (integer/bit arithmetic). Exclude transcendental/iterative floats: an exact hash of
  them is machine-specific (rounding is not robustly safe — values straddle boundaries).
- A test compares the live surface against the pin on **every suite run** and fails on
  drift, with a message telling the author what to do.
- On an intentional change the contract forces the loop closed: regenerate the pin,
  commit it in the **same** change, and file a notice on the integration channel.
- Contract file: `port/PORT.md`.

## H. Integration channel (consumers ↔ this project)
- One directory per consumer under `integrations/<project>/`; exchanges are **files**
  (`brief.md` → `response.md` → `notice.md`), because files persist across sessions,
  devices, and agent handoffs where a chat relay is triaged and forgotten.
- Triage flow: verify "already shipped" claims in code, write the response, and **fold
  durable outcomes into ROADMAP.md in the same change.** Decisions never live in
  `integrations/` — it records exchanges; ROADMAP records what was decided.
- **Shared-engine rules** (when this project is an engine consumed by others, or is
  itself a consumer of one):
  1. **One boundary module** per consumer is the only code that knows the engine's wire
     format; everything downstream consumes normalized data.
  2. **Consume-when-connected, degrade visibly.** Work with the engine absent; prefer it,
     fall back locally behind the *same* API, always surface which source answered.
  3. **Never reimplement the engine's domain core.** Trivial documented fallbacks only.
  4. **Pin versions.** Empirical priors/models/schemas are versioned; a default flip
     upstream can silently move scales you calibrated against. Pin what you depend on.
  5. **Design around shipped capabilities; make gaps visible.** File an intake brief for
     a missing capability; ship a visibly-minimal placeholder that marks the swap-in point.
  6. **Hot paths never call the engine.** Real-time threads stay engine-free; call from
     offline/UI threads or freeze results into a loaded-at-start artifact.
  7. **Consume plural outputs.** Keep ranked candidates and margins; collapse to one
     answer only when the application truly needs one.
  8. **Canonical data at the boundary, presentation at the edge.** The boundary carries
     canonical numeric/ID form; labels, spelling, and language render in the client.
- Contract file: `integrations/README.md`.

---

## Composition note (the three prompts, in order)

1. **best-practices `bootstrap.sh`** — the mechanical floor (hooks, layered CLAUDE.md,
   CODEMAP, ignore rules). Run first.
2. **this prompt** — doctrine, oracle gates, ROADMAP decision log, epistemic firewall,
   optional coordination threads. Layered on top.
3. **`integrate-knowledge-loop.prompt.md`** — the self-improving loop. Run last, so its
   first seeded lesson can be something true you learned wiring up (1) and (2).

Re-running any of the three is safe: all edits are marker-delimited and non-destructive.
Delete stale constraints as aggressively as you add new ones — the harness is only as
good as its accuracy.
