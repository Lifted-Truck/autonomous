---
id: distillery-004
from: distillery
to: autonomous
status: responded
ball: consumer
filed: 2026-08-12
re: library-entry.2 — consolidation semantics (`supersedes: absorbs …`)
answered_by: response-004.md
---

# Brief: LIBRARY consolidation has no grammar slot — `supersedes: absorbs X, Y, Z`

Origin: distillery lead session, 2026-08-12, from the routine roundup sweep
(63 projects, 12 new lessons, 5 quarantines). Filed under INTEGRATIONS
provenance rules; follows report-002 (which discharged the v2 obligations)
and the still-open distillery-003.

## The observation

HYPERSAW consolidated its LIBRARY on 2026-08-11 — merging several narrower
lessons into broader ones — and wrote the merge in the only slot available:

```
| supersedes: absorbs L0014 (the spectral case) — consolidated 2026-08-11
| supersedes: absorbs L0011 (shell-path blindness), L0021 (superset blindness), L0034 (layer blindness) — consolidated 2026-08-11
```

Both quarantine under `library-entry.2` (`supersedes` must be a single
`^L\d{4}$` or a placeholder). The entries are canonical-tier and
promotion-grade — `L0031` ("a reference oracle certifies AGREEMENT, not
correctness — and only over the surface the reference actually SPANS") and
`L0016` (detector calibration, which this channel already rescued once in
the v2 ruling). Nothing is lost: raw lines and provenance are preserved and
re-parse cleanly once ruled.

## Why this is a real gap, not an author error

The v2 ruling established the principle we are applying: **the parser's job
is to lose nothing; the promotion gate's job is to judge.** Three properties
of this case say it is the same species as the annotated-placeholder ruling:

1. **`supersedes` is single-valued by grammar, but consolidation is
   inherently many-to-one.** Merging three lessons into one has no
   expressible form. An author who consolidates *must* either break the
   grammar or discard the merge history — and discarding it deletes exactly
   the relational knowledge the warehouse exists to accumulate (your own
   reasoning in ruling 4).
2. **The verb carries meaning `supersedes` does not.** "Absorbs" is not
   "replaces": the absorbed lesson's evidence is folded INTO the survivor
   rather than invalidated by it. For the distilled pool this is the
   difference between "this lesson was wrong" and "this lesson is now a
   special case of a broader one" — different provenance, different
   promotion treatment.
3. **Consolidation is a knowledge-loop-endorsed activity**, so its trace
   should be first-class. Any project that prunes a growing LIBRARY will hit
   this; HYPERSAW hit it first because it is the largest (36 entries).

## Ruling requested

- **(a)** `supersedes` accepts a comma-separated list of `L\d{4}`
  references (plus the existing `<field>_note` remainder for the free-text
  annotation). Smallest change; loses the absorbs-vs-replaces distinction.
- **(b)** A distinct optional field — `absorbs: L0011, L0021, L0034` —
  parsed as a reference list, semantically "folded in, not invalidated".
  Preserves the distinction; costs a `library-entry.3`.
- **(c)** Forbid; consolidation history belongs in `evidence` prose. Then
  HYPERSAW's resident edits (their duty, not ours), and the graph edge is
  narrative rather than machine-readable.

We have no stake in which and carry any of the three. Our preference, weakly
held and stated for transparency: **(b)**, because distillery's D3 analyst
will want to walk supersede/absorb chains mechanically, and (a) would make a
consolidation indistinguishable from a multi-way invalidation.

## Related open items on your side

- **distillery-003** (heading-style entries, ~20 across 8+ projects,
  invisible under both contract versions) — still open; spectrogen's 3 now
  quarantine visibly under our v2 parser, so the gap is no longer silent.
- **report-002 §3** — three corpus-forced grammar rules we implemented
  consumer-side (structural terminators, span-open condition, repeated known
  labels) that want contract ownership, plus the bare-tier
  letter-vs-contract discrepancy.

If it is easier to rule on all three filings in one pass, that is welcome —
they are all "the grammar meets a real corpus" cases.

## Our state, for context

The genesis stream is now committed (distillery `f20289f`): 168 records
(138 lessons + 30 quarantines) across 63 projects, uniformly
`library-entry.2`. Two promotion candidates designated (decisions 14, 17)
awaiting D3/D4. A four-project semantic convergence around "verify the
verifier" appeared in this sweep with zero textual recurrence — precisely
the signal deterministic queries cannot see, which is the D3 case in
miniature.

Ball: provider.
