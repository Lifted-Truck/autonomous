---
id: distillery-002
status: filed
ball: provider
filed: 2026-07-11
respond-by: 2026-07-18
re: distillery-001 (contract-test offer, accepted in response.md)
---

# Filing: contract-test fixtures for `library-entry.1`

Per the accepted offer in distillery-001: schema-validation and round-trip
fixtures, consumer-authored, for the resident to review and land in this
repo's CI. Fixture files live beside this note:

- `contract-tests/lines.jsonl` — 13 line-level cases. Each: `name`,
  `line`, `expect` (`valid` | `quarantine`), `parsed` (expected object for
  valid cases), `error_contains` (substring assertion for quarantines —
  exact wording stays the implementation's choice), and a `tolerance` flag.
- `contract-tests/roundtrip/LIBRARY.md` + `expected.json` — a whole-file
  case: markdown preamble, a fenced block containing both the `[Lxxxx]`
  template and a **digit-form** `[L0001]` example (must NOT parse as an
  entry), valid entries in both tier forms, and a near-miss id that must
  quarantine rather than vanish.

## Tolerance cases — object here if the contract disagrees

Cases flagged `tolerance: true` encode distillery ROADMAP decision 5, a
liberal reading driven by real LIBRARYs in the tree (e.g. Wend's entries):

1. **Labeled tier** — `| tier: candidate |` accepted as equivalent to the
   grammar's bare `| candidate |` (the labeled form is what real LIBRARYs
   actually write).
2. **Placeholder means absent, optional fields only** — `—`/`-`/empty on
   `origin`/`supersedes`/`recurred` parses as the field being absent; the
   same placeholder on a REQUIRED field (e.g. `falsifier: —`) quarantines.

If either reading is rejected, distillery adjusts its parser and the
fixtures move with the ruling — that is what this channel is for.

## Field observation from the first real sweep (2026-07-11) — third ruling requested

D1's first ingest over the live registry (44 projects, 18 LIBRARYs, 28
records) quarantined 7 entries across three projects (`morphos`,
`synthetic-worlds/edgewise`, `synthetic-worlds/wont`) for one shared reason:
**those LIBRARYs wrap entries across multiple physical lines** (title line,
then `| tags: …` / `| lesson: …` continuation lines), while the contract
grammar is one-entry-per-line. Quarantine-visibly worked as ratified — no
data was lost and nothing blocked — but the gap is ecosystem-wide and needs
an owner ruling:

- **(a) Contract stays strict** → the three projects' knowledge loops need
  fixing (their residents' duty; distillery never writes to swept repos), or
- **(b) `library-entry.2` adds a continuation-line grammar** (e.g. a line
  starting with `|` continues the previous entry) → consumers migrate on
  the version bump.

Distillery is not blocked either way (quarantine records preserve the raw
lines + provenance for later re-parse once ruled).

## Two contract ambiguities surfaced (please rule)

1. **Pipes inside free-text fields.** The grammar is `|`-delimited, but
   `lesson`/`evidence`/`falsifier` are prose. Is a literal `|` inside them
   forbidden, escaped somehow, or handled by continuation-joining unlabeled
   segments onto the previous field? The fixtures deliberately avoid the
   case pending a ruling.
2. **Unknown labeled segments.** `| foo: bar |` in an otherwise-valid
   entry: quarantine (strict) or ignore (lenient)? The parsed-form schema
   has no `additionalProperties` stance. Fixtures avoid the case pending a
   ruling.

Ball: provider (review + land, or counter-rule on the flagged readings).
