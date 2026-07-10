# {{PROJECT_NAME}}

> Root CLAUDE.md — **pointers and critical gotchas only.** Everything else belongs in
> a subdirectory CLAUDE.md or [CODEMAP.md](CODEMAP.md). If a line isn't a pointer or a
> gotcha, it drifts into noise — cut it.

## What this is

_One or two sentences. What the project does and who uses it._

## Map

See [CODEMAP.md](CODEMAP.md) for the directory tour. Major areas each have their own
`CLAUDE.md` with local conventions — Claude loads those additively as it navigates.

## Commands

- Test: `{{TEST_CMD}}`
- Lint: `{{LINT_CMD}}`
- Format: `{{FORMAT_CMD}}`

_(Override per-subdirectory in that subdir's CLAUDE.md when the commands differ.)_

## Gotchas

> The high-value section. List the non-obvious things that bite people. Delete each
> one when it stops being true.

- _e.g. "Generated code lives in `gen/` — never edit it by hand; run `{{FORMAT_CMD}}`."_
- _e.g. "Two functions named `process()` exist; rely on the LSP, not grep."_

## Conventions

- _Only conventions that aren't already enforced by the linter/formatter._
- _If a hook enforces it deterministically, you don't need to write it here._
