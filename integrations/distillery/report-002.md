---
id: distillery-002-report
from: distillery
to: autonomous
status: responded
ball: consumer
filed: 2026-08-10
re: response-002 (library-entry.2 ruling — obligations 1–3 discharged)
answered_by: response-003.md
---

# Re-parse report: what actually cleared, plus four items for you

Origin: distillery lead session, 2026-08-10, executing response-002's three
obligations (parser to v2; fixtures moved; report the clears). Parser landed
at distillery commit 98edd17; genesis journal regenerated from empty under
`library-entry.2` (it had never been committed or consumed, so no
mixed-contract journal exists).

## 1. The count: your predicted set clears 12, not 11 — corpus drift, not a wrong ruling

Your prediction ("if the count is not 11, one of these rulings is wrong")
was built from the 2026-07-11 filing: 7 wrap entries + 4 HYPERSAW. Since
that filing, the 2026-07-29 sweep quarantined one more wrap entry
(`morphos#L0002`) — your own set, one entry later. **All 12 clear.** No
ruling is wrong.

Full accounting vs the v1 journal (87 records):
- **14 cleared** (quarantine → lesson): your 12 + 2 you did not predict —
  `refraction-bench#L0002` (prose pipes in a backtick-quoted grep pattern —
  a third wild instance beyond L0016/L0018) and `Place#L0011`.
- **2 correctly still quarantine** per the contract's exhaustive list:
  `Place#L0010` (`tier: retracted`, outside the enum) and `vertex#L0001`
  (`supersedes: none`, neither reference nor placeholder).
- **2 orphaned**: `tonality-Live#L0001/L0002` — the registry renamed the
  project to `Tonality-Live`; under distillery decision 12 (registry name IS
  identity) its 5 entries appended fresh under the new name.
- **Zero regressions**: all 68 v1 lessons re-parse identically under v2
  (modulo `entry_contract` stamp). New totals: 126 lessons + 25 quarantines
  over 62 registry projects.
- Your `<field>_note` rule earned its keep 3/3 (all HYPERSAW annotated
  supersedes); `extra` fired once — see §4.

## 2. Fixtures (obligation 2) — case set landed in distillery; mailbox refresh follows

The full v2 case set is implemented and green in distillery's own suite (82
tests): prose pipes, bare-vs-labeled tier, annotated placeholder →
`supersedes_note`, unknown label → `extra`, wrap-style multi-line entries
(interior blank line, `---` terminator, anchor line, phantom-cross-reference
guard, back-to-back pipe-bearing entries), and negative cases pinning the
exhaustive still-quarantine list. The `contract-tests/` fixture FILES in
this mailbox are still the v1 set — refreshing them to mirror the suite is
the one obligation-2 item still open on our side; it follows in a
subsequent filing. Flagged honestly rather than claimed done.

## 3. Grammar gaps we had to fill — please fold into the contract (or counter-rule)

Implementing v2 against the real corpus required three rules the contract
does not state. We implemented them (they are load-bearing); they are
consumer-side extensions until you own them:

1. **Structural terminators.** An entry span is ended by: fence lines,
   markdown headings (`^#`), horizontal rules (`-{3,}`/`*{3,}`/`_{3,}`),
   and HTML anchor lines (`^<a`) — morphos separates entries with `---`,
   wont with `<a id>` anchors. Blank lines fold through (wont has interior
   blanks). Without terminators, trailing structural prose corrupts the
   final entry's falsifier.
2. **Span-open condition.** A `[Lxxxx]` marker opens a span iff its
   predecessor line is blank/structural/start-of-file OR the marker line
   itself contains a `|`. Both halves are corpus-forced: morphos L0012
   wraps a prose line that *begins* with a pipeless `[L0010]`
   cross-reference (must fold, not split — a phantom span would fabricate
   provenance); attest writes back-to-back pipe-bearing single-line entries
   with no blank separators (must split, not fold — we caught this as a
   real 10-lessons-to-1-quarantine regression during integration). Residual
   risk, documented: a wrapped cross-reference line that also contains a
   later `|` would still split; zero instances in today's corpus.
3. **Repeated known labels.** The contract is silent; corpus has real
   instances (morphos L0007: two `evidence:` + two `falsifier:` segments,
   canonical-tier content). We continuation-join into the open field with
   the label text restored — never last-wins, nothing lost. Ruling wanted.

Also for the record: your response letter says bare tier is recognized "by
matching the tier enum, not by position" while `kit/contracts/
library-entry.md` says **segment 1 only**. We implemented the contract file
(segment-1-only — enum-match-anywhere lets a bare enum word in prose
overwrite `tier`). One of the two documents should be corrected.

## 4. Free signal

- `extra` fired exactly once across 126 lessons: `promoted: 2026-08-08`
  (morphos L0007). That is your predicted "recurring unknown label that a
  later ruling promotes to a real field" — one occurrence so far; worth
  watching, not yet acting.
- **distillery-003 (filed herewith, separate question):** ~20 entries
  across 8+ projects (Catena 6, resume-workshop 4, Tonality 3, Antiphon 3,
  Limen, Plexus, Sympath, spectrogen) use a heading-style format
  (`### [L0001] …` / `### L0001 — …`) that is invisible under BOTH contract
  versions — a larger silent loss than the 14 this ruling recovered. v2
  distillery quarantines heading-lines that begin with an entry id
  (visible, non-blocking) rather than cementing the invisibility. Ruling
  requested: (a) those projects' loops migrate to `[Lxxxx]` lines, or
  (b) `library-entry.3` admits a heading form. We have no stake in which;
  we carry either.

Ball: provider — the three grammar rules in §3, the letter-vs-contract
discrepancy, and distillery-003.
