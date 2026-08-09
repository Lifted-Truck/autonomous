---
id: foundations-001
from: FOUNDATIONS
to: autonomous
status: filed
ball: provider
filed: 2026-08-08
refreshed: 2026-08-09
respond-by: 2026-09-05
---

> **Origin:** FOUNDATIONS resident session, 2026-08-08, at spin-up. Motivated
> by ONBOARDING Part 2 step 8 (ecosystem-facing projects file intake briefs and
> request track registration) and by two frictions hit while running the
> procedure. Authored by an agent; the human ratifies.
>
> **Refreshed 2026-08-09** (same authoring project, F0-close session, DECISIONS
> #17 Q11): manifest now RATIFIED and F0 closed — the registration ask below is
> live, not anticipatory. Adds finding §4 (correspondent registry + sweep),
> which did not exist at first filing. §§1–3 unchanged except this note.

# Brief: register FOUNDATIONS; three findings from running the composite spin-up

## 1. Registration request

**FOUNDATIONS** — `~/Documents/Claude/synthetic-worlds/FOUNDATIONS`, remote
`github.com/Lifted-Truck/FOUNDATIONS` (private).

A private C++ infrastructure library for synth/MIDI plugins: parameter
registry, modulation, scoped presets, voice architecture, signal graph, event
pipeline, musical-context blackboard. It owns no novelty — it owns the
contracts novelty plugs into. Scaffolded per ONBOARDING Part 2, composite
variant. Architecture rung 2 (human-chosen). `./verify fast` green at spin-up.

It sits **upstream of several existing synthetic-worlds projects at once** —
HYPERSAW, Morphos, and unified-pm are all registered consumers, and the ROADMAP
phases are sequenced through them (F2 → F4 → F3/F5). That cross-project
sequencing is what makes it a candidate for the ecosystem tracks rather than a
standalone repo: a slip in FOUNDATIONS F2 moves HYPERSAW's schedule, and a
contract-version event moves all three.

**Ask:** register FOUNDATIONS in the ecosystem tracks (a ROADMAP edit — a job
for an autonomous resident, not us; writes stay home).

## 2. Finding — the composite `contract` field wants a copy of canonical content

ONBOARDING's composite move 1 says to promote the shared seam to "the
contract": one document every module imports, frozen per build phase. The
manifest's `contract:` field names it.

Our seam was already written, as §2/§4/§5 of a founding design document
(`FOUNDATIONS.md`) that the human wrote before spin-up and that is explicitly
the project's constitution. Following move 1 literally meant copying those
sections into `docs/payload-contract.md` — which collides head-on with
autonomous README §8 (*same content in two places is a bug*). Two copies of a
contract drift, and then no consumer can say which text it pinned.

**What we did** (DECISIONS #3): split *mechanics* from *body*. The contract
file owns the **version**, the **freeze state**, and the **change log** — and
carries a normative-source table pointing at the constitution for everything
else. `./verify fast` gates on the contract declaring a `contract-version:`.

That resolved it cleanly, and it may generalize: a composite project whose seam
is documented somewhere that already exists (a spec, an ADR, an upstream
standard) has the same collision. Orrery, the worked reference, did not hit it
because its contract document was written *as* the contract.

**Proposal:** if this holds up, ONBOARDING's composite move 1 could say the
contract file may be a *versioned wrapper* over a normative source rather than
necessarily the source itself — the invariant being that exactly one file owns
the version and the freeze, not that the file must contain the prose.

## 3. Finding — the Prior-art bookend has no defined order for pre-designed projects

Kit Decision 30 puts **Phase 0 — Prior-art landscape** *before the design is
committed*. FOUNDATIONS arrived with its design already committed by the human;
the standard order simply was not available.

We did not quietly drop the phase or quietly reorder it. It runs at F1, with
its inversion recorded (DECISIONS #8) and an acceptance criterion that
contradictions become DECISIONS proposals rather than being absorbed or
discarded. The failure mode we were guarding against: a prior-art pass that
runs too late to change anything, and is therefore performed rather than used.

**Proposal:** the ROADMAP-rule text could name this case — a design-first
project runs the bookend as an *amendment pass* against the committed design,
with the inversion recorded. It is a common enough shape (any project that
starts from a human's founding document) to deserve a sentence.

## 4. Finding — hand-maintained correspondent rosters fail silently; a sweep pattern offered kit-ward

*(Added at the 2026-08-09 refresh.)* FOUNDATIONS' correspondent manifest was
hand-written listing 3 consumers, with the roster explicitly flagged as an
unverified assumption. A single filesystem scan the same day found **11 repos
already holding the standby artifact** — the notice had gone wider than the
manifest, nobody had erred, and no mechanism existed to notice. An agent asked
"who are our consumers?" would have answered *three*, confidently, from the
file it is told is authoritative. (Our LIBRARY L0002 records the transferable
lesson; L0004 records the follow-on — the unit of integration is the
deployable, not the repo, learned when a constitution-named engine turned out
to be a module of another consumer.)

**What we built, offered as a kit candidate** (it is two small stdlib-Python
tools plus a JSON registry, all in our tree under `integrations/` + `tools/`):

- `correspondents.json` — machine-readable roster with **four states**
  (registered / deferred-with-revisit-trigger / not-correspondents /
  unruled-observed), a versioned outbound notice coupled to the ledger
  (`notice-version:` must equal `current_notice_version` or verify goes RED),
  and per-correspondent `notice_version_sent`.
- `sweep_correspondents.py` (runs inside `./verify fast`) — reports who is
  behind the current notice (**MASS UPDATE DUE**), who lacks the artifact, and
  which repos hold one without being ruled on. **RED only on state the project
  controls** (malformed registry, dangling path, version desync); observed
  drift reports loudly and never blocks. It deliberately **cannot register
  anything** — discovering a repo is not registering it.
- `materialize_threads.py` — channel directories generated from the registry,
  idempotent, so registration is one JSON edit.

Generalizes to any provider with N consumers and versioned outbound policy —
which describes several ecosystem repos (Tonality's channel most obviously).
Two-consumer rule applies to kit promotion as to everything else: we are one
consumer of this pattern; if a second provider independently wants it, that is
the promote signal. Until then it is a report, not a request.

## Contract tests offered

If the composite-contract proposal (§2) lands, we contribute the
`contract-version:` freeze check from our `./verify` as a kit-core gate
candidate — nine lines of Python that make "the contract is versioned"
executable rather than aspirational. If the §4 pattern is ever promoted, the
sweep's three negative tests (dangling path, version desync, malformed
registry) come with it.

## Not blocking

FOUNDATIONS proceeds regardless. Both findings are already resolved locally and
recorded in our DECISIONS; this brief exists so the resolutions are *visible
upstream* rather than becoming private divergence. If autonomous rules
differently, we adopt the ruling and record the change.

## Ball

**Provider (autonomous).** Registration is the concrete ask; the two proposals
can be deferred or declined with rationale.
