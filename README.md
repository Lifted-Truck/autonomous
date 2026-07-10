# autonomous

**The canonical home for a fully-autonomous development paradigm** — the
doctrine, harness kit, memory loops, and governor that let coordinated
parallel agents build correctness-critical software without colliding or
drifting — *and* the standards for ordinary single-agent projects, because
the fleet is an option here, never the default.

This README is the orientation document: a human should understand every
layer, protocol, and cycle from this file alone, without reading the
implementation. Deep links go to the canonical sources.

*Last verified current: 2026-07-10.*

---

## 1. The layers, bottom to top

```
┌─────────────────────────────────────────────────────────────────┐
│ 5 · GOVERNOR        watchdog (deterministic halts) · curator    │
│                     (memory) · coherence critic (fresh eyes)    │
├─────────────────────────────────────────────────────────────────┤
│ 4 · MEMORY LOOPS    per-project knowledge loop → promote-up     │
│                     audit loop → curator down-propagation       │
├─────────────────────────────────────────────────────────────────┤
│ 3 · COORDINATION    territories · contracts · task ledger ·     │
│     (fleet only)    merge queue · integrations policy           │
├─────────────────────────────────────────────────────────────────┤
│ 2 · OPERATING LOOP  implementer / verifier / critic ·           │
│                     ./verify oracle · traces · shift rhythm     │
├─────────────────────────────────────────────────────────────────┤
│ 1 · MECHANICAL      layered CLAUDE.md · hooks · CODEMAP ·       │
│     HARNESS         ROADMAP+DECISIONS · .claudeignore           │
├─────────────────────────────────────────────────────────────────┤
│ 0 · DOCTRINE        the standing rules every layer answers to   │
└─────────────────────────────────────────────────────────────────┘
```

Every project gets layers 0–2. Layer 3 exists only on the fleet rung.
Layers 4–5 are installed when a project's lifespan and autonomy earn them.

**Layer 0 — Doctrine** ([doctrine/DOCTRINE.md](doctrine/DOCTRINE.md)).
The standing rules: AI/deterministic boundary (AI proposes and judges, never
schedules/validates/measures), oracle discipline (gates never weaken to
pass), visual-first review, right-sized architecture, the living-README
clarity standard, reduce-never-invent. Machines' global `~/.claude/CLAUDE.md`
files import these — install per [doctrine/INSTALL-GLOBAL.md](doctrine/INSTALL-GLOBAL.md).

**Layer 1 — Mechanical harness** (kit v1 archived at
[archive/kit-v1/](archive/kit-v1/); v2 spec at [kit/](kit/)).
Deterministic enforcement of the boring stuff: format/lint on every edit
(PostToolUse hook), context injection at session start, lean layered
CLAUDE.md, append-only DECISIONS.md, phase-gated ROADMAP.md that outranks all
other docs.

**Layer 2 — Operating loop** ([harness/](harness/)).
The Generic Agent Harness: an **implementer** writes code inside a scoped
brief; a **verifier** runs the oracle and reports verbatim (never fixes); a
**critic** reviews adversarially in a fresh context (never edits). The
independence is the point — agents demonstrably overrate their own work.
Sessions run as **shifts**: fresh context, one task, verify, commit, journal
(traces/), handoff artifact, end. Structured handoffs beat long-running
compaction.

**Layer 3 — Coordination** (fleet rung only; [DESIGN.md](DESIGN.md) §2–3).
Work partitions into **organs**: bounded modules with hook-enforced write
territories, a versioned `contract/` dir as the only seam, and their own
resident layer-2 loop. Coordination is stigmergic — task ledger, contract
commits, serialized merge queue; **no live agent-to-agent messaging** (the
most fragile layer in every published system, deliberately excluded). New
edges between organs go through the PROPOSAL protocol; the dependency graph
is a committed artifact from which the boundary linter is generated.

**Layer 4 — Memory** ([loops/](loops/); standards in §4 below).

**Layer 5 — Governor** ([governor/](governor/); to build, spec DESIGN §4).
Three separable functions on the AI/deterministic split: a **watchdog**
(deterministic, no model calls — budgets, halt triggers, HALT sentinel every
agent's hooks obey), a **curator** (model judgment behind quarantined writes —
runs the memory loops, maintains READMEs), and a **coherence critic**
(fresh-context review against ROADMAP + contracts, because "green is not
coherent": CI proves main passes, not that N changes compose sensibly).

---

## 2. How a project comes to life (the spin-up protocol)

1. **Survey.** A standard, repeatable question list about scope — what it is,
   the architecture rung, the domain core, oracle shape, consumers, lifespan/
   autonomy tier (full list: [kit/README.md](kit/README.md)). Answers are
   committed as `project.manifest.json`.
2. **Deterministic scaffold.** Code — not model judgment — applies templates
   from the manifest: hooks, CLAUDE.md skeletons, verify stubs, only the
   modules the answers earned. Re-runnable: change an answer, re-run, diff.
3. **Architecture menu** (survey question 2, never defaulted):
   - **Rung 1 — single-threaded agent.** The default for most projects.
   - **Rung 2 — thread + read-only subagents / fresh-context verifier.**
     Earned by: read-heavy exploration, or correctness stakes that warrant an
     independent checker.
   - **Rung 3 — organ fleet.** Earned by: genuinely parallelizable *and
     verifiable* work, real seam count, value justifying ~15× token cost.
4. **Knowledge loop** seeded with the survey's tag vocabulary (§4a).
5. First ROADMAP phase and its gate are written before any code.

Escalate rungs only when the current rung is the demonstrated bottleneck.

---

## 3. The testing cycle (oracle discipline)

Every project exposes one interface: **`./verify <target>`** (contract:
[harness/README.md](harness/README.md)).

- **`fast`** — seconds: lint, typecheck, unit tests, cheap invariants.
  **Layer-0: deterministic, no model calls, blocks everything** — the Stop
  hook refuses to end a session on red; CI mirrors it.
- **`full`** — the whole gate: fast + integration + golden datasets +
  behavioral evals. **Layer-E items are measured, never blocking** — and
  never conflated with Layer-0 (guaranteed vs measured is stated, always).
- **`report`** — prints the last verify result without re-running.

Rules that never bend: gates are never weakened to pass (a wrong gate is
fixed deliberately, with a DECISIONS entry); gate definitions live outside
the implementing agent's write territory; **passing ≠ done** — done is oracle
green *and* acceptance criteria satisfied *and* a trace written, checked
separately. On the fleet rung, add: merge queue with required checks, flaky
quarantine from day one, and consumer-contract tests (§5) in the provider's
CI.

---

## 4. Memory: the standards

### 4a. Spinning up a knowledge loop (per-project)

**When: every project, at scaffold time — default-on** (Decision 11). The
loop costs three files and a write-gated session discipline; a quiet project
pays ~nothing, and early setup-era lessons are unrecoverable if never
captured. What scales with project scope is the heavier machinery (audit
threads, fleets, governor), never the loop itself.
**How:** run [loops/knowledge-loop/integrate-knowledge-loop.prompt.md](loops/knowledge-loop/integrate-knowledge-loop.prompt.md)
verbatim. It installs three files — CLAUDE.md protocol block, INDEX.md
(compact retrieval map, read in full), LIBRARY.md (durable lessons) — and
seeds exactly one real lesson. The per-session cycle is ORIENT (read INDEX,
pull only matching LIBRARY entries) → ACT → REFLECT ("what could a future
session not cheaply re-derive?") → WRITE (atomic LIBRARY+INDEX append).
Every lesson carries **evidence and a falsifier**; new lessons enter as
`candidate` and earn `canonical` on a second independent occurrence.
**The write gate:** prefer not writing over writing unverified — the loop
feeds its own output back as input, so one wrong lesson is reinforced
forever. In autonomous operation, REFLECT is hook-enforced, never voluntary.

### 4b. Spinning up an audit loop (cross-project harvest)

**When:** a parent directory has ≥2 children running knowledge loops.
**How:** (canonical: [agent-knowledge-loop](https://github.com/Lifted-Truck/agent-knowledge-loop))
1. Run `integrate-audit-loop.prompt.md` at the parent scope — installs the
   AUDIT-LOOP protocol block, INDEX/LIBRARY, and `AUDIT-STATE.json` (the
   hash ledger that makes passes incremental and idempotent).
2. Schedule `audit-loop.sh` (weekly cron, **propose-only mode**): it hashes
   each child's LIBRARY, skips unchanged children, and writes proposed
   promotions to `audit-runs/<date>.proposal.md` — never directly to the
   shared store. This is the staging-buffer defense from the memory-poisoning
   literature.
3. A human (later: the curator) reviews and applies proposals.

*Currently live on this machine:* weekly Sunday 9am cron over
`synthetic-worlds/`, config in `agent-knowledge-loop/audit-loop.config`.

### 4c. Cross-proliferating lessons between libraries (the promotion standard)

A lesson climbs only through gates that **tighten with altitude**:

- **Qualified at source** — `canonical` in its own project, OR the same
  pattern found *independently* by ≥2 siblings (shared-source convergence
  counts once, not twice).
- **Generalizes beyond origin** — promote the transferable pattern, never the
  project-specific fact. Litmus: can you state it without naming the origin's
  code? If not, it stays local.
- **Dedup over abstraction** — matching lessons merge (adding origins and
  evidence) rather than duplicate; concrete instances are preserved, because
  aggressive summarization measurably destroys the detail that makes lessons
  usable.
- **Provenance never dropped** — every promoted entry carries `origin:`
  back-links and its falsifier, so it can be traced and revoked. Supersede,
  don't erase.
- **The parent is the intersection of what is reusable, not the union of the
  children.** When in doubt, don't promote.

Downward proliferation (parent → specific children's CLAUDE.md) is the
curator's job — **targeted, never broadcast** (a CLAUDE.md holds roughly
100–150 instruction slots; selective memory beat comprehensive 39% vs 13% in
the research), slot-budgeted, and behind the same adversarial review. This
direction ships in Phase P3.

**The global memory is two pools** (Decision 11): an **append-only stream**
(warehouse — every candidate lesson from every sweep, dated, provenance
attached) and the **distilled pool** (mart — the top of the audit-loop
hierarchy). The stream is read *only* by a top-level analytical agent hunting
longitudinal patterns (recurrence, demote-recur cycles, cross-project failure
signatures); it is **never retrieval context for working agents**, and its
findings enter circulation only through the distilled pool's promotion gates.

---

## 5. Cross-project development (the integrations protocol)

Full policy: [doctrine/INTEGRATIONS.md](doctrine/INTEGRATIONS.md). The short
version:

- **Data plane:** providers publish `INTEGRATION.md`; consumers file
  file-based exchanges under `integrations/<project>/` —
  `brief.md → response.md → notice.md`. One boundary module per consumer;
  pinned versions; degrade visibly when the provider is absent.
- **Control plane (who commits, who PRs):** **writes stay home** — only a
  repo's residents ever commit to it, because visitors bypass the resident
  harness. Every exchange state has exactly one accountable side (`ball:`
  frontmatter). A cross-repo change is **two linked PRs**: provider lands
  first (implement, version, tag, notice), consumer lands second (bump pin,
  adapt boundary module, verify). Consumer contract tests are
  consumer-authored, resident-landed, and run in the provider's CI — so
  breaking a consumer fails the provider's build automatically.
- **Never blocked:** overdue balls escalate; meanwhile the consumer ships a
  visibly-degraded placeholder and proceeds.

---

## 6. Governance and halting (fleet rung)

Every consequential guard is **technically enforced, never prose** — the
entire incident record (prod-DB deletions, five-figure runaway loops) traces
to prompt-level-only guards. Concretely: budgets metered outside any agent's
process; freezes = revoked permissions; a `HALT` sentinel file that every
agent's PreToolUse hook checks, stopping the fleet within one tool call.

Halt triggers come in two severities (ranked list: DESIGN §4a):
**hard trips** (territory violation, budget ceiling, destructive-op gate,
wall-clock timeout) and **pause-and-escalate** (token-rate spike ≈ looping,
no-progress state-hash, oscillation/churn, CI regression, gate-weakening
attempt, PROPOSAL storm = the plan is wrong, stop coding). Halts are cheap
and non-shameful; escalation-on-uncertainty is rewarded. Autonomy is graded
by **reversibility of the change**, not trust in the model.

---

## 7. Map of this repo

| Path | What | Status |
|---|---|---|
| [DESIGN.md](DESIGN.md) | The full research-backed design | current |
| [ROADMAP.md](ROADMAP.md) | Phase gates (C0 current → P0…P4); single source of direction | current |
| [DECISIONS.md](DECISIONS.md) | Append-only decision log (10 on record) | current |
| [doctrine/](doctrine/) | Doctrine + integrations policy + global-install guide | current |
| [kit/](kit/) | Kit v2 "harness factory": survey → manifest → profiles | **to build** |
| [harness/](harness/) | Generic Agent Harness (layer 2) | imported, working |
| [loops/](loops/) | Memory loops (leaf here; audit loop → [agent-knowledge-loop](https://github.com/Lifted-Truck/agent-knowledge-loop)) | current |
| [governor/](governor/) | Watchdog · curator · coherence critic | **to build** (P0–P4) |
| [integrations/](integrations/) | Intake channel — one dir per consumer (briefs from `distillery`, `dispatch`) | live |
| [research/](research/) | The evidence base, citations preserved | current |
| [archive/kit-v1/](archive/kit-v1/) | Kit v1, frozen | archived |

**Sibling execution tracks** (own repos, sequenced in ROADMAP → Ecosystem
tracks): [`~/Documents/Claude/distillery/`](../distillery/) (global memory:
stream + analyst + distilled pool) · [`~/Documents/Claude/dispatch/`](../dispatch/)
(daily progress publishing). This repo governs; they execute.

## 8. Maintenance

Curated by a standing integrator role (currently Claude, per project memory):
canonical-copy discipline (one home per artifact; every other location is a
pointer), README freshness per the clarity standard, DECISIONS as the
append-only trail, periodic dedup sweeps. **If the same editable content
exists in two places, one of them is a bug — file it.**
