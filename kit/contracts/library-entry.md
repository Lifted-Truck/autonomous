# Contract: LIBRARY entry format — `library-entry.3`

> **v3 (2026-08-10)** — rules distillery's `report-002` §3 and `distillery-003`.
> Same governing principle as v2: **the parser's job is to lose nothing; the
> promotion gate's job is to judge.** Four changes, three of which formalize
> rules distillery had already been forced to invent to implement v2 against the
> real corpus (so they cost consumers nothing to adopt — they are already live):
>
> 1. **Structural terminators** end an entry span (§Span boundaries).
> 2. **Span-open condition** — a `[Lxxxx]` marker opens a span only under stated
>    conditions, so a prose cross-reference cannot fabricate a phantom entry.
> 3. **Repeated known labels** continuation-join; never last-wins.
> 4. **NEW: block form admitted on READ.** ~20 entries across 8+ projects were
>    invisible under v1 AND v2 — a larger silent loss than v2's ruling recovered.
>    The line form stays canonical for writing.
>
> **Correction to the distillery-002 response letter:** that letter said the bare
> tier is recognized "by matching the tier enum, not by position." That was
> wrong; this contract said segment-1 AND enum-match, and distillery implemented
> the contract. Enum-match-anywhere would let a bare enum word in prose overwrite
> `tier`. The contract text is and was normative; the letter was the error.

## Span boundaries (v3)

An entry span begins at a span-opening marker and ends at the next one, or at a
**structural terminator**, whichever comes first:

- a fence line (```` ``` ````)
- a markdown heading (`^#`) — *unless* it is itself a span-opening marker
- a horizontal rule (`^-{3,}`, `^\*{3,}`, `^_{3,}`)
- an HTML anchor line (`^<a`)

Blank lines **fold through** — they do not end a span. Corpus-forced: `morphos`
separates entries with `---`, `wont` with `<a id="Lxxxx">` anchors, and `wont`
has interior blank lines inside single entries. Without terminators, trailing
structural prose is absorbed into the final entry's `falsifier`.

### Span-open condition

A `[Lxxxx]` marker opens a span **iff** its predecessor line is blank,
structural, or start-of-file, **OR** the marker line itself contains a `|`.

Both halves are corpus-forced and pull in opposite directions:

- `morphos` L0012 wraps a prose line *beginning* with a pipeless `[L0010]`
  cross-reference. It must **fold**, not split — a phantom span there would
  fabricate provenance, inventing an entry that was never written.
- `attest` writes back-to-back pipe-bearing single-line entries with no blank
  separator. They must **split**, not fold — distillery caught this as a real
  10-lessons-to-1-quarantine regression during integration.

**Residual risk, documented rather than hidden:** a wrapped cross-reference line
that *also* contains a later `|` would still split. Zero instances in the current
corpus. The structural fix is a distinct cross-reference syntax — `[[Lxxxx]]`
for references, `[Lxxxx]` only for entry markers — which HYPERSAW already uses
for some references. It is **not** ruled here because the corpus is mixed
(HYPERSAW writes both forms; `morphos` writes only the single form), so
mandating it would strand existing prose. Prefer `[[Lxxxx]]` in new writing; the
heuristic above is the compatibility path, not the destination.

### Repeated known labels

A label that appears more than once in an entry **continuation-joins** into the
open field, with the repeated label text restored — never last-wins. Corpus:
`morphos` L0007 carries two `evidence:` and two `falsifier:` segments in
canonical-tier content. Last-wins would silently discard half of a promoted
entry's evidence, which is the failure mode this whole contract exists to
prevent.

## Block form (v3, READ-side only)

An entry may also be written as a **heading-delimited block**. Recognized shapes,
all present in the corpus:

```
### [L0001] Title here          # Catena, Limen  — bracketed id + title
### L0001 — Title here          # Antiphon       — bare id, em-dash, title
### L0001                       # resume-workshop — bare id, title on next line
```

- The marker is `^#{2,6}\s+\[?L\d{4}\]?`. Such a heading **terminates** any open
  span and **opens** a new one (this is the stated exception in §Span boundaries).
- `title` is the heading remainder with a leading `—`/`-` stripped; if the
  remainder is empty, the first non-empty following line is the title.
- Fields carry the **same label set**, in any of these delimiters:
  `| label: value`, `**label:** value`, `- **label:** value`. Middot (`·`)
  separates inline bold fields.

**Why admitted rather than migrated.** The alternative was for 8+ projects to
migrate their loops. Writes stay home, so that needs 8 independent residents to
act, and every entry stays invisible until the last one does — an indefinite
tail on content that is *complete*. These entries are not malformed: `Antiphon`,
`Catena`, `Limen` and `resume-workshop` all carry `lesson`, `evidence` and
`falsifier`, serialized with markdown bold instead of pipes. Nothing about them
is missing; only the delimiter differs. Rejecting complete content over its
delimiter is the same misplaced rigor v2 rejected.

**The line form remains canonical for writing.** Knowledge-loop templates emit
`[Lxxxx] … | … |`; block form is accepted, never generated. Liberal in what it
accepts, conservative in what it emits — so the corpus converges without anyone
being forced to migrate on a deadline.

> **v2 (2026-07-31)** — rules the five questions filed in distillery-002.
> Governing principle, and the reason every ruling went the way it did:
> **the parser's job is to lose nothing; the promotion gate's job is to judge.**
> A format strictness that destroys promotion-grade content is misplaced rigor,
> not discipline. This is a grammar fix, NOT a weakened gate — the quality gate
> (tier promotion, falsifier required, evidence required) is untouched, and the
> things that still quarantine are listed explicitly below.
>
> Changes from v1, all consumer-visible:
> 1. Entry boundary is the `[Lxxxx]` marker, **not** the newline (multi-line
>    entries are valid).
> 2. Unlabeled `|` segments **continue the open field** (literal pipes in prose
>    are legal — `|x[n]-x[n-1]|` is mathematics, not a delimiter error).
> 3. Both tier forms accepted: bare `| canonical |` and `| tier: canonical |`.
> 4. Placeholder-with-annotation on an optional field → field absent, annotation
>    **preserved** as `<field>_note`.
> 5. Unknown labeled segments → preserved under `extra`, entry stays valid.


> Canonical schema for knowledge-loop LIBRARY.md entries, formalizing the
> format defined behaviorally in the knowledge-loop and audit-loop prompts
> (which remain canonical for *behavior*: gates, tiers, promotion rules).
> Consumers (distillery ingest, audit loop, curators) validate against THIS.
> Schema changes are versioned events per INTEGRATIONS rule 4 — bump the
> version, file notices to consumers, never drift silently.
> Requested by: integrations/distillery/brief.md (distillery-001).

## Entry grammar (v2 — entries are marker-delimited, not line-delimited)

**An entry begins at a line matching `^\[L\d{4}\]` and ends at the next such
line (or the end of the block).** Interior newlines fold to single spaces. This
is why: three projects (`morphos`, `edgewise`, `wont`) wrap entries across
physical lines, and their 7 entries quarantined under v1 for a formatting habit
that costs no information. Marker-delimiting makes them valid with **no work by
their residents** — and it subsumes the "continuation-line marker" option
distillery offered, without adding a marker to remember.

### Segment rules

Split the entry on `|`, then:

- **Segment 0** → `id` + `title`.
- **Segment 1**, only if it matches the tier enum exactly → `tier` (the bare
  form). Matching against the enum rather than against position is load-bearing:
  a title containing a literal `|` would otherwise have its tail silently
  promoted to tier.
- A segment matching `^\s*(tier|added|tags|origin|lesson|evidence|falsifier|supersedes|recurred)\s*:`
  **opens** that field.
- **Any other segment appends to the currently-open field**, with the `|` that
  split it restored. This is what makes prose pipes legal.
- Unknown `label: value` segments → collected under `extra` (see below).

### Placeholders and annotations

On an **optional** field (`origin`, `supersedes`, `recurred`), a value matching
`^[—–-]\s*(.*)$` means **the field is absent**. If the remainder is non-empty it
is preserved as `<field>_note` — never discarded. Real entries write
`supersedes: — (refines L0002 with a third cause)` and
`supersedes: — (generalises [[L0014]], which stays as the spectral case)`;
those are genuine graph edges the schema has no other slot for, and dropping
them would delete exactly the relational knowledge the warehouse exists to
accumulate.

On a **required** field, a placeholder still **quarantines**. That is
deliberate: `falsifier: —` is a missing falsifier, and the falsifier requirement
is a quality gate, not a formatting convention.

## v1 line grammar (retained for reference)

```
[Lxxxx] <title> | <tier> | added: YYYY-MM-DD | tags: <t1, t2, …> [| origin: <child>#Lxxxx[, …]] | lesson: <text> | evidence: <text> | falsifier: <text> [| supersedes: Lxxxx] [| recurred: YYYY-MM-DD (<child>#Lxxxx)]
```

- `id` — `L` + 4 digits, unique within the file, never reused.
- `title` — short; everything before the first `|`.
- `tier` — `candidate` | `canonical`. (Fleet contexts add `proliferated`;
  that tier is curator-granted only — see autonomous README §4c.)
- `added` — ISO date.
- `tags` — comma-separated, from the project's declared tag vocabulary.
- `origin` — REQUIRED on promoted (parent-scope) entries: back-links
  `<child>#Lxxxx`, comma-separated, never dropped. Absent on leaf entries.
- `lesson` — the transferable statement (context + forces, not bare fix).
- `evidence` — concrete instance(s); preserved verbatim on merges.
- `falsifier` — what observation would disprove this lesson. REQUIRED.
- `supersedes` — optional; supersede, never delete (invalidate-don't-erase).
- `recurred` — optional; set when a matching failure signature reappears
  after canonicalization (the logged-but-not-institutionalized flag).

## Parsed form (JSON Schema, draft-07)

```json
{
  "$id": "library-entry.3",
  "type": "object",
  "required": ["id", "title", "tier", "added", "tags", "lesson", "evidence", "falsifier"],
  "properties": {
    "id":        {"type": "string", "pattern": "^L\\d{4}$"},
    "title":     {"type": "string", "minLength": 1},
    "tier":      {"enum": ["candidate", "canonical", "proliferated"]},
    "added":     {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"},
    "tags":      {"type": "array", "items": {"type": "string"}, "minItems": 1},
    "origin":    {"type": "array", "items": {"type": "string", "pattern": "^[^#]+#L\\d{4}$"}},
    "lesson":    {"type": "string", "minLength": 1},
    "evidence":  {"type": "string", "minLength": 1},
    "falsifier": {"type": "string", "minLength": 1},
    "supersedes": {"type": "string", "pattern": "^L\\d{4}$"},
    "recurred":  {"type": "string"},

    "origin_note":     {"type": "string"},
    "supersedes_note": {"type": "string"},
    "recurred_note":   {"type": "string"},

    "entry_form": {
      "enum": ["line", "block"],
      "description": "v3: which serialization this entry was READ from. Line is canonical for writing; block is accepted so ~20 complete entries across 8+ projects stop being invisible. Recorded so a later migration can find them without re-parsing."
    },

    "extra": {
      "type": "object",
      "description": "v2: unrecognized `label: value` segments, preserved verbatim. An unknown label must NOT quarantine an otherwise-valid entry (that cost promotion-grade content under v1) and must NOT be silently dropped (that loses data). Keeping it visible here is what lets a later ruling promote it to a real field.",
      "additionalProperties": {"type": "string"}
    }
  }
}
```

## Validation stance (for ingesting consumers)

**What still quarantines — the exhaustive list, UNCHANGED from v2 to v3**, so
"be forgiving" cannot creep into "accept anything". v3 admits three new
*delimiters* and one new *layout*; it admits no new absence. Verified against
the corpus before ruling: every heading-form entry v3 newly accepts carries
`lesson`, `evidence` and `falsifier` already. Had they not, the answer would
have been migration, not admission — a format that cannot express a required
field is not a format variant:

1. A malformed or missing `[Lxxxx]` marker, or a duplicate id within a file.
2. A missing REQUIRED field (`title`, `tier`, `added`, `tags`, `lesson`,
   `evidence`, `falsifier`).
3. A REQUIRED field whose value is a placeholder (`—`, `-`, empty).
4. A `tier` outside the enum, a malformed `added` date, or an `origin`/
   `supersedes` value that is neither a valid `L\d{4}` reference nor a
   placeholder.

Everything v2 newly accepts is a *formatting* variation that carries the same
information. Everything v2 still rejects is *missing information*. If a future
ruling blurs that line, it is weakening the gate and should be refused.

Malformed entries are **quarantined visibly, never silently dropped, and
never block the sweep** (a legacy LIBRARY with three bad lines yields N−3
records + 3 quarantine records carrying the raw line and the parse error).
INDEX.md lines are pointers, not entries — they are NOT governed by this
contract; the LIBRARY is the source of truth and INDEX↔LIBRARY consistency
is the knowledge loop's own atomic-write duty.
