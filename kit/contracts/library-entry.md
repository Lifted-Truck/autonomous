# Contract: LIBRARY entry format — `library-entry.2`

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
  "$id": "library-entry.2",
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

    "extra": {
      "type": "object",
      "description": "v2: unrecognized `label: value` segments, preserved verbatim. An unknown label must NOT quarantine an otherwise-valid entry (that cost promotion-grade content under v1) and must NOT be silently dropped (that loses data). Keeping it visible here is what lets a later ruling promote it to a real field.",
      "additionalProperties": {"type": "string"}
    }
  }
}
```

## Validation stance (for ingesting consumers)

**What still quarantines under v2** — the exhaustive list, so "be forgiving"
cannot creep into "accept anything":

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
