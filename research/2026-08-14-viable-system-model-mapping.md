# The Viable System Model, mapped onto this ecosystem

> **Provenance.** Authored by the autonomous standing-integrator session,
> 2026-08-14, at the human's direction after their reading of Stafford Beer
> ("I want to make sure it is taken into consideration in the architecture").
> Session model: Fable, explicitly human-selected via `/model` this session.
> Motivating decision: DECISIONS #47. Companion edit: DESIGN.md §4 vocabulary.
>
> **Epistemic note, per the gates tenet.** The flattering conclusion — "the
> architecture is already VSM-shaped, nothing to change" — was named as the
> hoped-for outcome *before* evaluation, and the mapping below was searched
> specifically for strain. Two genuine deficits survived that search (S4,
> algedonics), and one was demonstrated live during the analysis itself.

## Why VSM fits here at all

Beer's VSM (Brain of the Firm, 1972; The Heart of Enterprise, 1979;
Diagnosing the System for Organizations, 1985) models any viable system —
one able to maintain separate existence in a changing environment — as five
interacting systems plus two channels, recursively repeated at every level.
Its foundation is Ashby's Law of Requisite Variety: only variety can absorb
variety, so every regulator must attenuate environmental variety and amplify
its own.

This ecosystem is a one-human, many-agent operation: 62 repos of operational
variety against a single human's attention. That is a variety-engineering
problem in its purest form, and the framework converged on VSM's answers
empirically — nearly every incident in the July–August record is a failure
Beer named: transducer distortion (the "merged" said early), audit-channel
capture by self-report (the wrapper registry), missing algedonics (the 19-day
public leak), oscillation-adjacent channel ambiguity (day-resolution ball
dates), and a dead regulator indistinguishable from a healthy fleet (the
monitor crash). Adopting the vocabulary is adopting compression: these
lessons currently cost one incident each to re-derive.

## The mapping

| VSM | Beer's function | Realized here | Fidelity |
|---|---|---|---|
| S1 | Operating units, each themselves viable | Execution repos; territories within composites (Orrery engines, FOUNDATIONS modules) | Strong, incl. recursion: fleet → repo → territory. Manifests are per-level identity; ratification gates are per-level S5 closure |
| S2 | Anti-oscillation, shared protocol | INTEGRATIONS (`ball:` state machine — "exactly one accountable side" is anti-oscillation verbatim), versioned contracts, kit conventions, registry | Strongest system, deliberately built. Known fidelity gap: day-resolution exchange dates (`seq:` gap, bitten twice) |
| S3 | Inside-and-now cohesion; resource bargaining | The human + ROADMAP cross-track ordering constraints + the rung menu; the governor's authority ceiling (edits ROADMAP/memory/README, never product code) | Human-carried — **correctly at this scale**; Beer's centralization pathology is pre-blocked by writes-stay-home and territory autonomy |
| S3\* | Sporadic audit bypassing S1 self-report | monitor, leak_scan, ball_scan, sweep — the "derived at sweep time, never hand-maintained" rule | Strong and hard-won. The wrapper-registry bug was an S3\* failure in Beer's exact sense: the audit channel was reading S1's self-report (the registry) instead of ground truth |
| S4 | Outside-and-then; intelligence, adaptation | Landscape audit (monthly, cloud), prior-art bookend phases, research/ | **Thinnest system.** Demonstrated live 2026-08-14: the 2026-08 audit ran on schedule, opened PR #2 on 2026-08-10, and sat unsurfaced for four days — the organ works; the channel into S3/S5 does not exist |
| S5 | Identity, policy, closure | DOCTRINE.md `@import`ed into every session + human ratification gates + DECISIONS (append-only) | Strong. Beer: ethos must pervade — the import is literally that. Decision 12's separation of powers (standards home vs operational lead) guards the S5-collapses-into-S3 pathology |
| Algedonic | Pain signals bypassing the hierarchy | HIGH severity to the session brief; HALT sentinel (designed, unbuilt) | **Absent when unattended.** The 19-day public-repo leak — remote-visible the whole time — is the incident on record |

Pathology checklist (Diagnosing the System): S3 micromanagement — blocked by
construction. Weak S2 — no. Missing S3\* — no. S5 captured by operations —
guarded (Decision 12). **Missing S4 and missing algedonics — guilty**, the
two failures Beer identified as killing organizations slowly and invisibly.

## Two concepts adopted beyond the boxes

**POSIWID** — *the purpose of a system is what it does.* Already enforced
without the name: the status-prose rule, the README-truth tenet ("a repo
whose README lies about it is a bug of the same severity as a failing test"),
"a gate that has never fired is not known to be a gate" (Antiphon L0001),
and the monitor's own death (judged by what it did, the fleet-health system's
purpose was nothing). Standing audit question: *judged only by observed
behavior, what is this mechanism's purpose?*

**Requisite variety as the standing design test.** The attenuation chain
(62 repos → derived status → severity classes → dormancy/deferred states →
one-line session brief) and the amplification chain (one doctrine file →
every session; one kit → every repo; one hook → every prompt) are the
architecture. The August false-positive discipline — exchange-id threading,
monotonic closure, ours-only overdue, ball-token parsing, dormancy expiry —
was channel-capacity engineering: noise on an attenuator destroys its
requisite variety, because a channel nobody reads has none. Test for every
new mechanism: *attenuator or amplifier for the human channel, and what is
its noise floor?*

## Amendments (ratification queue — Decision 47 records the adoption of
vocabulary only; A–D are separate human calls)

- **A. S4 freshness + PR surfacing.** monitor gains an `S4-STALE` check
  (newest dated research artifact / unmerged `landscape-audit/*` branch older
  than ~35d → WARN) and open-PR surfacing for this repo (an open PR here is
  an obligation on the human; nothing currently reports it). The
  monitor-was-dead lesson applied to the intelligence organ itself.
- **B. "Outside & then" STATUS section.** Last audit date, unconsumed
  findings count, next run — beside the health rows. The S3–S4 confrontation
  made visible where the human already looks; zero new agents.
- **C. Environment-watch remit** added to the landscape audit prompt:
  protocol cadence (MCP), platform shifts (the TCC class), provider policy
  (the demotion incident class), CI pricing. All four burned the fleet once
  and were handled ad hoc.
- **D. Algedonic channel, remote-visible subset.** Weekly scheduled cloud
  job — deterministic script, no model in the signal path — checking
  GitHub-visible pain only: red default-branch CI across the roster,
  leak_scan on clones of public repos; notify on HIGH alone. Earned by the
  19-day leak. Honest scope: local-only pain still waits for a session hook
  or the declined FDA-cron trade.
- **E. Named non-adoptions.** No standing S4 agent; no S3 resource-bargaining
  machinery (that is the governor's controller half, correctly deferred until
  a fleet runs — metasystem grows with S1 variety); no five-box staff-function
  build-out (the classic VSM misuse); **no new doctrine tenet** (budget
  8729/9000 — this lives in DESIGN §4 and here, not always-loaded context).

## Where the mapping strains (recorded so it can be challenged)

- S3 resource allocation is entirely in the human's head. VSM calls that a
  gap; this analysis calls it correct until an actual fleet runs. Judgment,
  not derivation.
- Recursion is cleanest at fleet→repo. Repo→territory is genuinely exercised
  only by Orrery and FOUNDATIONS.
- The coherence-critic ≈ S4/S5-interface mapping is the loosest of the three
  governor correspondences; its "green is not coherent" is Beer's
  health-vs-viability distinction, but the critic reads inward (ROADMAP,
  contracts), not outward. Do not over-claim it as S4.

## Sources

- Beer, S. *Brain of the Firm* (1972); *The Heart of Enterprise* (1979);
  *Diagnosing the System for Organizations* (1985).
- Ashby, W.R. *An Introduction to Cybernetics* (1956) — requisite variety.
- Internal evidence: DECISIONS #33–#46; governor/ incident record 2026-07/08;
  research/2026-07-10-multiagent-systems-survey.md (stigmergy ≈ S2;
  harness-quality-outranks-head-count ≈ variety engineering).
