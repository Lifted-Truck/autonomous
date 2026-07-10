# Contract: project STATUS surface — `status.1`

> Canonical schema for the machine-readable status artifact every
> harness-scaffolded project exposes at `STATUS.json` (project root,
> git-tracked). Written ONLY by deterministic tooling (verify's record step,
> Stop-hook, ROADMAP parser) — never by model judgment. One collector's
> output, many renderings: the governor's watchdog and dispatch's digests
> read the SAME artifact.
> Requested by: integrations/dispatch/brief.md (dispatch-001).

## Schema (JSON Schema, draft-07)

```json
{
  "$id": "status.1",
  "type": "object",
  "required": ["schema", "project", "ts", "quiet"],
  "properties": {
    "schema":  {"const": "status.1"},
    "project": {"type": "string"},
    "ts":      {"type": "string", "format": "date-time"},
    "roadmap_phase": {
      "type": "object",
      "required": ["id", "title"],
      "properties": {
        "id":    {"type": "string"},
        "title": {"type": "string"},
        "gate_state": {"enum": ["open", "green"]}
      }
    },
    "last_verify": {
      "type": "object",
      "required": ["target", "exit", "git", "ts"],
      "properties": {
        "target": {"type": "string"},
        "exit":   {"type": "integer"},
        "git":    {"type": "string"},
        "ts":     {"type": "string"}
      }
    },
    "recent_since": {"type": "string", "format": "date-time"},
    "recent": {
      "type": "object",
      "properties": {
        "commits":   {"type": "array", "items": {"type": "object", "required": ["hash", "subject"], "properties": {"hash": {"type": "string"}, "subject": {"type": "string"}}}},
        "decisions": {"type": "array", "items": {"type": "string"}},
        "traces":    {"type": "array", "items": {"type": "string"}},
        "lessons":   {"type": "array", "items": {"type": "string", "pattern": "^L\\d{4}$"}}
      }
    },
    "quiet": {"type": "boolean"}
  }
}
```

## Semantics

- **`quiet: true`** means "collected and nothing changed since
  `recent_since`" — an explicit record, never an absence. A missing
  STATUS.json means *this project has no status surface yet*; consumers
  degrade visibly (infer from git, mark facts inferred-vs-declared).
- **`last_verify`** is `.harness/last-verify.json` verbatim — the verify
  dispatcher already writes it; the STATUS writer lifts it (single source).
- **No `public:` flag, deliberately.** Publishability is consumer policy,
  not project status — it lives in dispatch's watch config layered over the
  ecosystem roster (registry.json; Decision 14). A project cannot flag
  itself into someone's publication.
- **Writer ships with kit v2 core** (a deterministic `bin/write-status`
  invoked by the Stop hook and after verify runs). Until a project is
  retrofitted, it simply has no STATUS.json and consumers infer — the
  degrade-visibly path is the migration plan.

## Example

```json
{
  "schema": "status.1",
  "project": "distillery",
  "ts": "2026-07-10T21:00:00Z",
  "roadmap_phase": {"id": "D1", "title": "The stream (deterministic ingest)", "gate_state": "open"},
  "last_verify": {"target": "fast", "exit": 0, "git": "03a4317", "ts": "2026-07-10T20:58:12Z"},
  "recent_since": "2026-07-09T21:00:00Z",
  "recent": {
    "commits": [{"hash": "03a4317", "subject": "D0 scaffold"}],
    "decisions": ["2"],
    "traces": ["2026-07-10-scaffold.md"],
    "lessons": []
  },
  "quiet": false
}
```
