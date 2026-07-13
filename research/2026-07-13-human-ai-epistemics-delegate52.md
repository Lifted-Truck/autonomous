# Human-AI collaboration epistemics + DELEGATE-52 — doctrine grounding

> Harvested 2026-07-13 from the user's own methodology document, "The Applied
> Epistemics of AI Integration" (canonical home:
> `ai-integration-methodology/` — the sibling human-epistemics project). That
> document is the *proximate* source for everything below.
>
> **Provenance flag (honest, per this repo's own standard):** the DELEGATE-52
> study is cited by the methodology doc as a 2026 Microsoft Research benchmark;
> its primary has NOT been independently verified in this harvest. Treat the
> specific figures as attributed-not-confirmed until a landscape-audit pass
> verifies the primary (a good task for the next monthly run — added to the
> watch-list). The *doctrine mappings* below stand regardless of the exact
> percentages, because they restate mechanisms this repo already holds.

## Why this belongs in autonomous's evidence base

autonomous governs the **agentic/deterministic** half of the practice (AI as a
replaceable worker inside a deterministic scaffold). The methodology doc governs
the **human-epistemic** half (AI as a cognitive prosthetic for a motivated
human). They are siblings. This report harvests the parts of the human-side
document that are *citable grounding* for autonomous's existing doctrine — it
does not import the methodology itself.

## DELEGATE-52 (as reported by the methodology doc)

Tested 19 models across 52 professional domains on delegated document workflows
over 20 consecutive interactions. Reported findings:
- Top frontier models corrupted ~25% of document content by workflow end;
  all-model average ~50% degradation. Only 1 of 52 domains (Python) cleared a
  98% "ready" threshold.
- **Stronger models fail *invisibly*** — they keep the document looking
  complete while rewriting facts, structure, values, labels, relationships.
  Weaker models fail visibly (obvious gaps). → the better the model, the harder
  the failure is to detect.
- **Failure is catastrophic, not gradual** — ~80% of degradation came from
  sparse but severe single-interaction collapses (≥10% lost at once), not
  steady accumulation.
- **Agentic tools *worsened* performance** by ~6 points on average — models
  can't reliably write ad-hoc programs across diverse domains, so they fall
  back to rewriting whole files. The mitigation identified: **tightly scoped,
  domain-specific tools.**

## The seven failure taxonomy (from the doc) → what autonomous doctrine each validates

| Failure mode | autonomous mechanism it grounds |
|---|---|
| **Consensus Trap** (AI recommends the popular, not the right) | "reduce, never invent"; the survey's explicit architecture-rung choice (don't default) |
| **XY Problem at scale** (fast, polished answer to the wrong question) | spec-first survey (MAST's ~42% spec-failure finding, research/2026-07-10-multiagent-systems-survey.md); ROADMAP gates on acceptance criteria, not activity |
| **Competency Erosion** / **Invisible Dependency** | the human stays the ratifier at named gates; degrade-visibly (INTEGRATIONS rule 2); "what breaks if this disappears?" is the AI/deterministic boundary question |
| **Confidence Spiral** (fluent output replaces verification) | oracle discipline (passing ≠ done; evidence not assertion); the coherence critic ("green is not coherent") |
| **Translation Gap** (impressive deliverables that don't connect to action) | visual-first review; living-README clarity standard |
| **Remediation Cliff** (build faster than you can supervise; catastrophic collapse) | watchdog halt triggers (budget/rate/oscillation); bounded phase-gates; fresh-context shifts |

The cross-cutting empirical point — **stronger models fail invisibly, and
agentic tools help only when tightly scoped** — is the single strongest external
validation of two load-bearing autonomous choices: (1) the **coherence critic**
exists precisely because polished-but-wrong survives CI; (2) the
**organ/territory/contract** structure and the **AI/deterministic boundary** are
the "tightly scoped, domain-specific tools" the study found necessary.

## Human-side principles worth promoting to doctrine

These have no current home in autonomous, which is strong on *machine-enforced*
friction and near-silent on the *human's* obligations at the ratification gates:

- **The governing principle:** "your greatest barrier to the truth is that which
  you wish to be true." Before asking, surface the outcome you're hoping for, so
  you can be suspicious when you arrive at it. A conclusion that arrives
  comfortably is a signal to examine it, not to accept it.
- **Friction is a feature.** Uninterrupted flow is the condition under which
  epistemic drift accelerates; adversarial stress-testing and deliberate
  interrogation of comfort are designed-in, not failures of smoothness. (This is
  the human-side twin of the fresh-context critic and adversarial verification.)
- **Deliberate, anchored compression.** When conversations condense into
  shorthand, drift goes invisible; periodically re-check that compressed forms
  still faithfully represent their foundations. (The human-side twin of the
  knowledge-loop write gate + consolidation discipline.)
- **Basin escape / attractor basins:** typical framing → consensus output (deep
  grooves); novel framing → constructive mode (flatter distributions). The
  landscape-audit and research fan-outs already exploit this; worth stating as
  the *why* behind novel-framing prompt design.

→ Folded into DOCTRINE.md as the tenet "Human epistemic discipline at the gates"
(the machine-enforced friction was always there; this names the human's share).
