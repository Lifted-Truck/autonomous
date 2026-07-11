# ONBOARDING — replicating and working in this ecosystem

For a **human** setting up a new machine, and for an **agent** arriving in
any of these repos for the first time. This is a map with procedures — every
standard it mentions is canonical somewhere else and deep-linked; if this
file and a linked file disagree, the linked file wins.

*Last verified current: 2026-07-10.*

## The ecosystem at a glance

One standards repo governs; execution repos do the work; exchanges between
them are files, not conversations.

| Repo | Role | Remote |
|---|---|---|
| **autonomous** (this repo) | Standards: doctrine, integrations policy, harness kit, governor spec, ecosystem roadmap | github.com/Lifted-Truck/autonomous |
| **agent-knowledge-loop** | The cross-project audit loop (promote-up memory) | github.com/Lifted-Truck/agent-knowledge-loop |
| **distillery** | Global memory: append-only stream + analyst + distilled pool | github.com/Lifted-Truck/distillery |
| **dispatch** | Daily progress publishing: collector → FACTS → digest → gated publish | github.com/Lifted-Truck/dispatch |

Cross-repo sequencing: [ROADMAP.md → Ecosystem tracks](ROADMAP.md).
The design and its evidence: [DESIGN.md](DESIGN.md), [research/](research/).
The full orientation to layers/protocols/cycles: [README.md](README.md).

---

## Part 1 — As a human

### Setting up a new machine

1. **Clone the standards repo to the canonical path** (the doctrine imports
   assume it):
   ```bash
   git clone https://github.com/Lifted-Truck/autonomous.git ~/Documents/Claude/autonomous
   ```
2. **Wire the global CLAUDE.md** — follow
   [doctrine/INSTALL-GLOBAL.md](doctrine/INSTALL-GLOBAL.md) (paste one block,
   verify a fresh session sees the doctrine). Machine-local sections of your
   global file stay machine-local; never copy them between machines.
3. **Clone the audit loop:**
   ```bash
   git clone https://github.com/Lifted-Truck/agent-knowledge-loop.git ~/Documents/Claude/agent-knowledge-loop
   ```
4. **Clone the execution tracks:**
   ```bash
   git clone https://github.com/Lifted-Truck/distillery.git ~/Documents/Claude/distillery
   git clone https://github.com/Lifted-Truck/dispatch.git   ~/Documents/Claude/dispatch
   ```
5. **Optional — the weekly audit-loop cron.** Copy
   `agent-knowledge-loop/audit-loop.config.example` →
   `audit-loop.config` (same dir, git-ignored, machine-local scopes), then:
   ```
   0 9 * * 0 $HOME/Documents/Claude/agent-knowledge-loop/audit-loop.sh >> $HOME/Documents/Claude/audit-loop.cron.log 2>&1
   ```
   It is propose-only by design — it never mutates shared stores.
6. **Verify:** start a fresh Claude Code session anywhere; ask what the
   doctrine says about the AI/deterministic boundary; confirm the answer
   matches [doctrine/DOCTRINE.md](doctrine/DOCTRINE.md).

### Working day-to-day

- **You are the ratifier.** The system is built so agents propose and you
  decide at named gates: project manifests (phase-0 gates), integration
  briefs' responses, memory promotions (audit-run proposals), doctrine
  changes (landscape-audit proposals), and anything published or
  irreversible. Saying *no* is cheap and expected.
- **Where things are decided:** each repo's ROADMAP.md is its single source
  of direction; DECISIONS.md is the append-only record. If you decide
  something in conversation, it isn't decided until it's in those files.
- **Starting a new project:** ask an agent to run the spin-up survey
  ([kit/README.md](kit/README.md) — 9 questions) and scaffold from your
  answers. The architecture menu is question 2; a fleet is never the default.
- **Asking one project for something another owns:** that's an integrations
  brief, not a chat request — see Part 2's cross-repo section; the mechanics
  are identical for humans.

---

## Part 2 — As an agent

### Your first ten minutes in any repo here

Read, in order: `README.md` (what this is) → `ROADMAP.md` (what's next and
what proves it done) → `DECISIONS.md` (what's already settled — do not
re-litigate) → `CLAUDE.md` (your charter; §Domain holds the invariants a
critic will check you against) → `INDEX.md` if present (pull only matching
LIBRARY lessons). Then run `./verify report` to see the oracle's last state.

### Rules of residency (condensed; canonical sources linked)

1. **ROADMAP.md outranks everything**, including the conversation. Ambiguous
   or missing acceptance criteria? Surfacing that gap IS the deliverable —
   grounded refusal is a success class ([harness charter](harness/CLAUDE.md)).
2. **Oracle discipline** ([README §3](README.md)): `./verify fast` after any
   change set, `full` before closing an item; report output verbatim; red
   halts forward work; never weaken a gate without a recorded human decision.
   Passing ≠ done — done = green + acceptance criteria + trace written.
3. **Writes stay home** ([doctrine/INTEGRATIONS.md](doctrine/INTEGRATIONS.md)):
   never commit to a repo you're not resident in. One exception: filing
   exchange files in a provider's `integrations/<your-project>/` slot.
4. **Memory loop duty**: every project runs the knowledge loop
   ([README §4a](README.md)) — ORIENT before acting, REFLECT before ending;
   the write gate is strict (evidence + falsifier, prefer not writing over
   writing unverified; if nothing qualifies, write nothing).
5. **Provenance**: nontrivial claims cite file/line, a verify run, or a
   ROADMAP entry; merged changes get a `traces/` entry.
6. **Human gates**: deleting files, public-interface changes, editing
   `./verify`, new dependencies, git beyond add/commit, anything §Domain
   protects, anything outward-facing (publishing, remote pushes to new
   places) — stop and ask.
7. **Review beats are visual-first** ([doctrine](doctrine/DOCTRINE.md)):
   at any gate — phase close, ratification request, PR — lead with a visual
   presentation sufficient to evaluate the work without reading code; the
   diff is the fallback, never the ask.
8. **Respect the AI/deterministic boundary**: if you find yourself doing
   scheduling, metrics, validation, or collection "by judgment," stop — that
   belongs in code you should write instead.

### Working across repos (the integrations protocol, quickstart)

Need something from another project? File a brief at
`<provider>/integrations/<your-project>/brief.md` with frontmatter
(`id`, `status`, `ball`, `filed`, `respond-by`) — live examples:
[integrations/dispatch/brief.md](integrations/dispatch/brief.md),
[integrations/distillery/brief.md](integrations/distillery/brief.md).
The `ball:` field always names the one side that owes the next move. Never
wait blocked: ship a visibly-degraded placeholder behind the same interface
and proceed. Cross-repo changes land as two linked PRs, provider first.
Full policy: [doctrine/INTEGRATIONS.md](doctrine/INTEGRATIONS.md).

### Replicating the project structure for a NEW project (until kit v2 ships)

Shortcut: the `/spinup` command (installed per INSTALL-GLOBAL step 3) wraps
this procedure; the doctrine also instructs any session asked to "start a
new project" to land here. The procedure itself, mirroring what built
`distillery`/`dispatch` (use them as reference implementations):

1. Conduct the spin-up survey with the human ([kit/README.md](kit/README.md),
   9 questions); write answers to `project.manifest.json`, marked
   provisional until ratified.
2. Copy the harness: `autonomous/harness/.claude` → `.claude/`,
   `autonomous/harness/verify` → `./verify` (chmod +x). Implement `fast()`
   with at least a structure/manifest sanity check — a green-from-day-zero
   oracle, honestly scoped, beats an aspirational red one.
3. Write `CLAUDE.md` from [harness/CLAUDE.md](harness/CLAUDE.md): the
   invariant layer verbatim, §Domain filled (what it is, stack, invariants,
   protected paths, verify targets — under ~60 lines).
4. Write `ROADMAP.md`: phase-gated, each gate an executable/checkable
   condition; open questions listed as blocking-ask-the-human.
5. Write `README.md` per the clarity standard ([doctrine/DOCTRINE.md](doctrine/DOCTRINE.md)):
   orientation without code-diving, a dated "last verified" line, status
   markers on anything unbuilt.
6. Install the knowledge loop:
   [loops/knowledge-loop/integrate-knowledge-loop.prompt.md](loops/knowledge-loop/integrate-knowledge-loop.prompt.md),
   tags from survey Q8.
7. `mkdir traces/` (+ pointer README), `.gitignore` (`.harness/`,
   `.claude/settings.local.json`), `git init -b main`, initial commit, run
   `./verify fast` — green before the first commit lands.
8. If it participates in the ecosystem: file its intake brief(s) with
   providers, and ask a resident of autonomous to register it in the
   ecosystem tracks (that's a ROADMAP edit — governor/resident-only).

### What not to do

- Don't edit doctrine in any global CLAUDE.md — propose changes in this
  repo (versioned, reviewable).
- Don't copy canonical content into a second editable location — link it.
  Same content in two places is a bug ([README §8](README.md)).
- Don't add memory outside the loop's write gate, don't broadcast lessons
  (proliferation is the curator's targeted job), and never expose
  distillery's raw stream to a working context.
- Don't escalate the architecture rung because parallelism sounds faster —
  the burden of proof runs the other way (Decision 8).

---

## Replication checklist (the short version)

**Human, new machine:** clone autonomous → INSTALL-GLOBAL → clone
agent-knowledge-loop → clone tracks (needs remotes) → optional cron →
fresh-session doctrine check.

**Agent, new repo:** README → ROADMAP → DECISIONS → CLAUDE.md → INDEX →
`./verify report`; then work the top ready ROADMAP item under the rules of
residency.

**Agent, new project:** survey → manifest → harness copy → charter →
phase-gated ROADMAP → README → knowledge loop → git init + green verify →
briefs + track registration if ecosystem-facing.
