# Research: hierarchical "promote-up" knowledge loops for coding agents

Synthesis behind the cross-project **audit loop** (see `integrate-audit-loop.prompt.md`
/ `run-audit-loop.prompt.md`). Compiled 2026-07-08 from a fan-out of research
agents across two literatures: LLM-agent memory research, and human-organisation
lessons-learned systems. Every claim below traces to a primary source; URLs kept.

## The one finding both literatures converge on
**Capturing and disseminating a lesson is the easy 80%; the loop's value is
entirely in the hard 20% — acting on it and not corrupting the shared pool.** The
US Army calls the failure "lessons observed, never learned": GAO documented the
same fratricide problems "identified two years earlier [and] yet to be corrected"
at the Gulf War ([GAO NSIAD-93-231](https://www.gao.gov/products/nsiad-93-231);
[NSIAD-95-152 "…Largely Untapped"](https://www.gao.gov/products/nsiad-95-152)).
NATO/CALL encode it as a hard rule: an observation **"does NOT become a lesson
learned until behavior has changed"** (AR 11-33 §4-5). Google SRE: "an unreviewed
postmortem might as well never have existed"
([SRE Book ch.15](https://sre.google/sre-book/postmortem-culture/)).
→ Our loop's honest scope: v1 *disseminates* (promotes into a retrieved store);
*verified downstream behaviour change* is the deferred next phase.

## Human-org prior art (the battle-tested analogues)
- **Army AAR → CALL.** OIL taxonomy: Observation → Insight → Lesson → *Lesson
  Learned*, with a maturity ladder and a hard **validation gate owned by the
  scope that would change — never by the observer** (AR 11-33 §4-8:
  "collecting OIL does not solve the Army's problems"). **Subsidiarity**: resolve
  at the *lowest* echelon with authority; escalate only on failure. CALL is a
  neutral pipeline that owns the archive but **not** the decision to
  institutionalise. ([CALL Services Handbook 15-11](https://api.army.mil/e2/c/downloads/2023/01/19/ab6f3bd5/15-11-call-services-handbook-jun-15-public.pdf))
  → maps to our `candidate→canonical`, `origin:` provenance, and the
  altitude-tightening gate.
- **Alexander / GoF pattern languages.** A lesson is reusable only if it names its
  **context + forces**, not just a solution. "Use connection pooling" is noise;
  context+forces+consequences is matchable. ([Timeless Way](https://en.wikipedia.org/wiki/The_Timeless_Way_of_Building))
  → our entry keeps `lesson`+`evidence`+`falsifier`; promote in forces-bearing form.
- **Nonaka SECI.** Knowledge amplifies individual→group→org via externalise→combine;
  but critics (Gourlay) warn it **conflates transfer with creation** — guard against
  "copy-up masquerading as learning." ([SECI critiques](https://en.wikipedia.org/wiki/SECI_model_of_knowledge_dimensions))
- **Communities of Practice (Wenger).** participation ↔ reification: a promoted doc
  **rots without re-validation.** → staleness pass.
- **Spotify guilds/chapters** — a *cross-cutting* knowledge axis distinct from the
  hierarchy — but the model "never fully worked even at Spotify"; autonomy without
  an alignment/dedup step = chaos. ([Failed #SquadGoals](https://www.jeremiahlee.com/posts/failed-squad-goals/))
  → a future "guild" (sibling-to-sibling) axis, not only vertical.
- **Golden paths / Team Topologies.** Promote only what children **pull** by
  repeated demand (not parent-push "knowledge bias"); keep the promoted surface
  thin; adoption is earned, not mandated. ([TT "Misuses of Platform Teams"](https://teamtopologies.com/news-blogs-newsletters/2024/11/24/revisiting-team-topologies-misuses-of-platform-teams))
- **Tech Radar / ADR.** Promotion isn't binary — staged confidence rings
  (Assess→Trial→Adopt→**Hold**); record *why* each promotion happened, immutably.

## Agent-memory prior art (transferable mechanisms)
- **Generative Agents** — reflection triggered on accumulated *importance*, insights
  **cite their source records**. ([2304.03442](https://arxiv.org/abs/2304.03442))
- **ExpeL** — the most direct analogue: extract insights by contrasting
  **success-across-different-tasks**; pool governed by add/upvote/downvote with
  **decay-to-zero** (self-eviction). ([2308.10144](https://arxiv.org/abs/2308.10144))
- **AWM** — promote by **abstracting concrete values into typed variables**; keep
  human-curated vs self-induced lessons in **separate provenance tiers** (merging
  them was measurably worse). ([2409.07429](https://arxiv.org/abs/2409.07429))
- **RAPTOR** — recursive embed→cluster→**summarise** bottom-up; retrieve at the
  level matching the query. The literal template for a hierarchy — but its own best
  config abandons top-down traversal for a flat/collapsed index (keep leaves
  reachable). ([2401.18059](https://arxiv.org/abs/2401.18059))
- **G-Memory / Agent-KB / H²R** — closest published "promote-up" systems: **three
  tiers** (raw trajectory → condensed experience → promoted insight) with
  level-specific retrieval and a **disagreement/veto gate** so a promoted lesson
  can't override a child's live reasoning. ([2506.07398](https://arxiv.org/abs/2506.07398), [2507.06229](https://arxiv.org/abs/2507.06229), [2509.12810](https://arxiv.org/abs/2509.12810))
- **Zep/Graphiti** — **bi-temporal** edges (when true vs when recorded);
  **invalidate, don't overwrite** — supersede a lesson without losing history.
  ([2501.13956](https://arxiv.org/abs/2501.13956))
- **Empirical caution (LongMemEval / consolidation study)** — aggressive
  summarisation *destroys usable detail*: S-tier accuracy 78.4%→48.4%;
  **dedup beat summarisation.** → prefer lossless dedup + keep the instance via
  `origin:`, don't over-abstract. ([2605.08538](https://arxiv.org/html/2605.08538))

## Memory poisoning — why promotion is the strictest write-gate
Promotion is an **ingestion event into a shared, high-trust store**; a poisoned
lesson reaches every child, and blast radius grows with altitude.
- **PoisonedRAG**: ~5 malicious docs in a 10k corpus → >90% targeted corruption
  ([2402.07867](https://arxiv.org/abs/2402.07867)). **AgentPoison**: >80% attack
  success at <0.1% poison rate; root cause = retrieval trusts memory with **no
  provenance check** ([2407.12784](https://arxiv.org/abs/2407.12784)).
- **MINJA / Gemini persistent-memory injection**: poison arrives **laundered
  through the agent's own trusted output** — so an ACL on "who may write" is not
  enough ([2503.03704](https://arxiv.org/abs/2503.03704);
  [Rehberger](https://embracethered.com/blog/posts/2025/gemini-memory-persistence-prompt-injection/)).
- Defenses that map onto our gate: **staging buffer + write-approval** (never
  direct-to-live), **independent quorum** (RobustRAG isolate-then-aggregate,
  [2405.15556](https://arxiv.org/abs/2405.15556)), **provenance**, **default-deny +
  quarantine with decay** (OWASP ASI06). Perplexity/dedup filters are insufficient
  alone. Curiously, a **well-populated correct memory is itself a defense** (ASR
  62%→~7% once legit memories exist) — another reason to keep the parent curated.

## The 12 design principles → how our loop implements each
1. **Context+forces, not bare solution** → entry keeps lesson/evidence/falsifier; promote in forces form.
2. **Recurs across siblings** → ≥2-**independent**-sibling convergence gate.
3. **Demand-pull, not parent-push** → up-only harvest; parent = intersection of reusable.
4. **Abstract the concrete out** → "promote the pattern, not the project fact."
5. **Tighten with altitude** → group: generality/convergence; top: ≥2 groups / 3+ projects.
6. **Dedup / cluster-then-summarise** → merge convergent siblings into one entry; dedup > abstraction.
7. **Provenance back-links** → required `origin: child#Lxxxx`, never dropped.
8. **Strictest write-gate = security boundary** → default-deny, quarantine (`candidate`), independence.
9. **Curated vs self-generated kept apart** → tier + origin distinguish; carried upward.
10. **The judge is the bottleneck** → AI judges promotion; SCAN/LEDGER/id-alloc stay deterministic.
11. **Lessons decay** → staleness pass in consolidation; falsifier re-checked; supersede-don't-erase.
12. **Close the loop (verify adoption) + guild axis** → *deferred, documented* as the honest next phase.

## Skeptic's flags
KG-memory benchmarks are vendor-heavy/self-reported (durable idea = the tiering,
not the leaderboard). Spotify model is the most-copied *and* most-debunked here.
SECI is paradigmatic but criticised. Several 2026-stamped arXiv IDs are unvetted
preprints — treated as directional only. Every agent-memory technique is proven on
clean-oracle benchmarks; "inject all lessons into context" is a prototype, not an
architecture — retrieval-scoped pools (our INDEX-first) are the real requirement.
