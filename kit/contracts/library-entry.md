# Contract: LIBRARY entry format — `library-entry.1`

> Canonical schema for knowledge-loop LIBRARY.md entries, formalizing the
> format defined behaviorally in the knowledge-loop and audit-loop prompts
> (which remain canonical for *behavior*: gates, tiers, promotion rules).
> Consumers (distillery ingest, audit loop, curators) validate against THIS.
> Schema changes are versioned events per INTEGRATIONS rule 4 — bump the
> version, file notices to consumers, never drift silently.
> Requested by: integrations/distillery/brief.md (distillery-001).

## Line grammar (one entry per line in LIBRARY.md)

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
  "$id": "library-entry.1",
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
    "recurred":  {"type": "string"}
  }
}
```

## Validation stance (for ingesting consumers)

Malformed entries are **quarantined visibly, never silently dropped, and
never block the sweep** (a legacy LIBRARY with three bad lines yields N−3
records + 3 quarantine records carrying the raw line and the parse error).
INDEX.md lines are pointers, not entries — they are NOT governed by this
contract; the LIBRARY is the source of truth and INDEX↔LIBRARY consistency
is the knowledge loop's own atomic-write duty.
