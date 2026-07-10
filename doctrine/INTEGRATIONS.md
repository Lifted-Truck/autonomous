# Integrations policy — cross-project interaction & development

> Canonical, project-agnostic policy for any project consuming or providing a
> shared capability (a "provider" engine and its "consumer" projects), and for
> any pair of repos doing coordinated work. Generalized from the Tonality ↔
> client-projects protocol (Audiology, TERRANE, Wend, AURICLE) and extended
> with an explicit **responsibility model** (§3) closing the commit/PR
> ownership gap for autonomous, complex interacting workflows.

## 1. The eight boundary rules

1. **One boundary module per consumer.** A single seam file is the ONLY code
   that imports the provider's SDK or knows its wire format; everything
   downstream consumes normalized data. Design it as a data-contract boundary,
   not a network boundary.
2. **Consume-when-connected, degrade visibly.** The consumer core must work
   with the provider absent. Prefer the provider, fall back locally behind the
   SAME API surface, and always surface which source answered (badge/counter/
   flag) — degraded mode is never silent.
3. **Never reimplement the provider's domain core.** The hard combinatorics,
   analysis, and judgment logic the provider owns stay in the provider.
   Permitted local duplication: trivial fallbacks (~15 lines, documented as
   degraded, instrumented) or explicitly temporary duplicates carrying a
   deletion plan.
4. **Pin versions.** Empirical priors, models, and schemas are versioned; a
   default flip upstream can silently change scales your calibration depends
   on. Pin what you depend on, document why, and stamp schema versions on
   interchange records.
5. **Design around shipped capabilities; make gaps visible.** Check the
   provider's integration spec before designing. For a missing capability,
   file an intake brief, then ship a visibly-minimal derived placeholder that
   documents the swap-in point — don't quietly grow a parallel engine.
6. **Hot paths never call the provider.** Real-time threads (audio, physics,
   input handling) stay provider-free; call from UI/offline threads, or freeze
   results into a contract artifact / control curve loaded at start.
7. **Consume plural outputs.** Keep ranked candidates, margins, and ambiguity
   flags; treat margin as a continuous confidence/control signal. Collapse to
   a single answer only when the application truly needs one.
8. **Canonical data at the boundary, presentation at the edge.** The boundary
   carries the provider's canonical numeric/ID representation; naming,
   spelling, labels, and language are rendered by the client's display layer.

## 2. The exchange channel (data plane)

- The provider publishes an integration spec (`INTEGRATION.md`) and an intake
  channel: one directory per consumer under `integrations/<project>/`.
- Exchanges are **files** (`brief.md` → `response.md` → `notice.md`) — files
  persist across sessions, devices, and agent handoffs where a chat relay is
  triaged and forgotten.
- Decisions never live in `integrations/` — it records exchanges; each repo's
  ROADMAP/DECISIONS records what was decided, folded in *in the same change*.

## 3. The responsibility model (control plane) — who commits, who PRs

Closes the gap the original protocol left implicit. Built on one rule:

### Rule zero: writes stay home
**Only a project's own resident agents (or its human) ever commit to it.**
No visiting commits — not as a trust matter, but because a visiting agent
does not run the resident harness (hooks, CLAUDE.md, verify gates, knowledge
loop), so its commits bypass the local immune system. A consumer wanting a
provider change files a brief; the provider's residents implement it.

### The ball: every exchange step has exactly one accountable side
Exchange files carry frontmatter: `id`, `status`, `ball`, `respond-by`.
The exchange is a state machine — at no state do both (or neither) sides own
the next move:

| State | Artifact | Ball |
|---|---|---|
| Brief filed | `brief.md` (need, proposed interface delta, contract tests offered, respond-by) | **provider** |
| Response | `response.md` (accept / counter-design / defer-with-rationale) | **consumer** (ratify or refine) |
| Implementation | provider-side PR(s), contract version bump, tag | **provider** |
| Notice | `notice.md` (shipped version, migration notes) | **consumer** (integrate, bump pin, verify) |
| Closed | consumer confirms green in notice thread; both ROADMAPs updated | — |

### Cross-repo change = two linked PRs, never one
- **Provider lands first:** implements, versions the contract (semver), tags,
  files the notice. Its PR cites the brief ID.
- **Consumer lands second:** bumps its pin, adapts its boundary module
  (ideally the only file that changes), verifies against its own gates. Its
  PR cites the same brief ID.
- Never a single PR spanning repos; never a consumer-authored PR against the
  provider. The brief ID in both commit histories makes the audit trail
  bidirectional.

### Consumer-driven contract tests cross the boundary as proposals
The consumer *proposes* a contract test suite in its brief — this is what "I
rely on X" means, executably. The provider's resident reviews and commits it
into provider CI. Consumer-authored, resident-landed: writes stay home, and
the consumer's expectations now gate the provider's future changes
automatically. Breaking a consumer contract fails the **provider's** build —
coordination without conversation.

### Deadlock, drift, and the reverse direction
- Briefs carry `respond-by`; an overdue ball escalates to the human (or the
  governor, where one runs). The consumer is never blocked meanwhile: it
  follows rule 2 (visible degraded placeholder) and proceeds.
- Conflicting briefs from multiple consumers are the provider's arbitration;
  version pinning means unchosen consumers stay on the old contract rather
  than being broken.
- Provider-initiated changes (deprecations, default flips) travel as notices
  with a migration window and `ball: consumer` — the same machine run
  backwards. A default flip without a notice is a policy violation.
- **Freeze = revoked permission, not an instruction.** Any "do not touch X"
  state is enforced by credentials/hooks/branch protection, never by prose.

### Self-similarity
This policy is the inter-repo instance of the intra-repo organ protocol
(DESIGN.md §3): territory = repo, PROPOSAL = brief, contract commit =
versioned release, merge queue = each repo's own. The same state machine
governs organ↔organ, repo↔repo, and fleet↔fleet exchanges.

## 4. Instance registry

- **Tonality** (music-theory engine): `~/Documents/Tonality/` (Python package
  `mts`). `INTEGRATION.md` there is the authoritative spec; briefs in
  `~/Documents/Tonality/integrations/<project>/`. Three transports, ONE data
  contract: Python import (`from mts.analysis import ...`), MCP
  (`python -m mts.mcp`, 43 tools), HTTP bridge (`python -m mts.mcp.bridge` →
  `http://127.0.0.1:8012`). Domain core (rule 3): harmonic combinatorics —
  set-class/DFT/prime form, voice-leading distance+mapping, key induction,
  chord naming, cadence logic. Versioned priors (rule 4): key profiles
  `kk-1982.1` vs `tkp-cbms.1` — an upstream default flip changed margin
  scales, so margin-calibrated consumers pin explicitly. Canonical boundary
  data (rule 8): pitch-class / MIDI integers; note spelling (F# vs Gb) is
  display-layer. **Retrofit target:** Tonality's protocol predates §3; its
  integrations/ channel should adopt ball-state frontmatter and the
  linked-PR rule.
