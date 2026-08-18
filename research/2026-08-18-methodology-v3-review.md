# Review: AI-integration methodology master v3, against this repo

> **Provenance.** autonomous standing integrator session, 2026-08-18, Fable
> (human-selected). Reviewing the human's internal methodology master (v3), dropped for
> review "in case it can help us inform the next steps." **The source is NOT in
> this repo** — it is an internal document (client engagements, pricing,
> positioning) and this repo is public; it lives in the private working tree
> of `ai-integration-methodology`, gitignored there too. This review quotes
> only doctrine-level content. The document itself is the human's
> and is not edited here; findings that touch it are recommendations back.
>
> **Gate discipline, applied to the reviewer.** The outcome I hoped for was
> *"fully consistent, validates six weeks of work."* It flatters my own
> output, so I looked for where it strains. Three places found; recorded
> first, agreement second.

## Where it strains

**1. Two claims about the machine side describe designs, not shipped things,
in the present tense.** Part VI: *"the halt sentinel every agent's hooks obey,
budgets metered outside any agent's process."* Neither exists. `HALT` lives in
DESIGN §4 and ROADMAP P0; Decision 32 deferred the governor's controller half
until a fleet exists to govern, and none does. Budgets are not metered
anywhere. Part IV's *"failure post-mortems are enforced by hook"* is closer —
`harness/.claude/hooks/stop-gate.sh` exists — but the *fleet's* enforced
post-mortem is the knowledge-loop write gate, which is a rule, not a hook.

This matters more than a citation slip. The document's own Part IV says
"technically enforced, never prose" and "passing is not done"; its Part I
warns that fluent output looks like finished work. A master document that
states designed things as built is the exact drift it warns clients about,
turned inward. **Recommendation:** Part VI distinguishes *shipped* from
*designed*, the way DESIGN.md does. The shipped list is strong enough not to
need the designed items borrowed into it.

**2. It is written before the last 48 hours, and they name a failure class it
does not have.** Decisions 53–59, six consecutive entries, are all one
shape: a mechanism that could not fire, or fired to the wrong party — an
amendment whose gate could never trigger, a delivery channel that carried
nothing, a brief that over-broadcast, a validator that cried wolf on first
run and would have passed 12/12 if neutered. The document's failure taxonomy
(Part II) is about *human* adoption; its machine-side analogs are correct but
they are all *content* failures (wrong lesson, wrong tier, drifted document).
The class this week produced is a **channel** failure: the check exists, the
rule exists, and nothing connects them to the thing they were for. HYPERSAW's
formulation is the sharpest available and belongs in Part IV:

> *A check that cannot fire reads exactly like a check that passes.*

with its two corollaries from LIBRARY L0002 and L0005 — a detector is not
known to be a detector until planted-bad fires and planted-good stays quiet;
and a must-read-zero control needs a paired corruption or it cannot fail.
This is not a new tenet; it is the missing *procedural* half of "technically
enforced, never prose." Enforcement that is never exercised is prose with a
shebang.

**3. Stage 3 locates the perimeter but does not name the DIRECTION of error.**
The document treats mislocation symmetrically. This repo's record is not
symmetric: every perimeter error on file put the model on the *deterministic*
side (a "reasonable guess" where a rule belonged; monitor reading self-report
instead of ground truth), and the fix was always the same direction. The
asymmetry is worth one sentence in Stage 3, because it changes the default:
*when unsure which side of the perimeter a sub-problem falls, place it on the
deterministic side and let the LLM propose to it — the reverse error is the
one that fails silently.*

## Where it is right, and what that changes here

**The document's central move — the same principle enforced on both sides of
the human/machine boundary — is correct, and this repo is its proof.** Part
IV's Perimeter Doctrine is a faithful restatement of DOCTRINE.md; the five
stages each carry a genuine structural counterpart from the kit (survey,
provenance typing, boundary rule + rung, oracle + reversibility, visual-first
+ living README). Nothing there is decorative. Two things follow for Phase R:

- **Phase R already has half its philosophical frame.** The recursive-VSM
  frame (Decision 51) needs a statement of what is invariant across levels;
  Part IV's "the machine enforces the friction the human can't sustain; the
  human owns the friction the machine can't provide" IS that statement,
  applied at the human/machine boundary. Phase R's job is to show it also
  holds at every project/group/fleet boundary — same principle, one more
  recursion. The frame should cite this document rather than restate it.
- **The "first writer walks a coverage surface" claim (HYPERSAW, Decision 57)
  is a Part III entry the document lacks.** Its "AI as structured adversary"
  is the closest item. The stronger version, from evidence: an adversary that
  merely *reviews* shares the author's assumptions; the party that must
  *write against* the artifact traverses surface neither the author nor the
  first reader ever walks. It is falsifiable and it is what produced four bug
  finds in two days. Worth adding, attributed.

**Part I's self-indoctrination paragraph applies to THIS conversation.** Six
weeks, one integrator session, an in-group vocabulary (balls, territories,
S3\*, "assert the effective state") that has condensed into shorthand. The
document's own remedy is periodic re-anchoring against foundations. This
review is one; the human's amendment of the INTEGRATIONS protocol — done by
the human, from HYPERSAW's evidence, not by me — is a better one.

## Recommendations back to the document (not applied; the human's)

1. Part VI: split *shipped* from *designed*. HALT and budget metering are
   designed.
2. Part IV: add "a check that cannot fire reads exactly like a check that
   passes," with the plant-known-bad and paired-control corollaries. Cite
   HYPERSAW L0032 / autonomous L0002, L0005.
3. Stage 3: name the direction of perimeter error and its default.
4. Part III: add first-writer coverage as a distinct positive-case item.
5. Part VI's own-systems list: the standards repo's proof is now stronger than
   stated — 59 decisions, each with the alternative rejected; a monitor that
   was dead and is now gated against being dead; a contract on its third
   version driven by consumer briefs. "The doctrine ships software" is true
   and undersold.

## What this changes in the queue

Nothing reorders. Phase R gets a citation and half its frame for free. The
`.gitattributes` batch, K2, and the seven retrofits are unchanged.
