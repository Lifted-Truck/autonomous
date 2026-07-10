# The article, distilled → mapped to artifacts

Source: [_How Claude Code works in large codebases: best practices and where to
start_](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start).

Each insight below names the file in this kit that operationalizes it. The point of
the kit is that you never have to re-derive these from the article — the defaults
already encode them.

| # | Insight | Operationalized by |
|---|---------|--------------------|
| 1 | **Layered CLAUDE.md.** Root = big picture; subdir = local conventions. Loaded additively as Claude traverses directories. | `templates/CLAUDE.root.md`, `templates/CLAUDE.subdir.md` |
| 2 | **Keep root lean.** "Pointers and critical gotchas only; everything else drifts into noise." | Structure of `CLAUDE.root.md` (sparse sections, gotcha-first) |
| 3 | **Scope to subdirectories, not the repo root.** Specify test/lint commands per subdirectory. | Bootstrap can target a subdir; `CLAUDE.subdir.md` carries local commands |
| 4 | **`.claudeignore`, version-controlled.** Exclude generated files/artifacts so everyone gets a consistent setup. | `templates/.claudeignore` |
| 5 | **Lightweight codebase map.** A markdown table of contents for unconventional structures. | `templates/CODEMAP.md` |
| 6 | **Hooks enforce determinism.** Lint/format via hooks, not instructions Claude might skip. | `templates/claude/hooks/format-lint.*` (PostToolUse) |
| 7 | **Start hooks load context dynamically.** | `templates/claude/hooks/session-start-context.*` (SessionStart → prints CODEMAP) |
| 8 | **Stop hooks propose CLAUDE.md updates** (continuous improvement). | `templates/claude/hooks/stop-capture-learnings.*` (Stop → reminder/capture) |
| 9 | **Skills: progressive disclosure + path-scoped.** Activate only in relevant areas; don't bloat every session. | `templates/claude/skills/example-domain/SKILL.md` |
| 10 | **Read-only subagents for mapping.** Split exploration from editing in isolated instances. | `templates/claude/agents/codebase-mapper.md` |
| 11 | **MCP servers** connect Claude to internal tools, docs, ticketing, analytics. | `templates/claude/.mcp.json` |
| 12 | **LSP for symbol-level precision**, especially multi-language (C/C++/C#/Java). | Documented step in `CHECKLIST.md` (no single file to scaffold) |
| 13 | **Ownership: a DRI** for Claude Code config; cross-functional governance. | `docs/GOVERNANCE.md` |
| 14 | **Govern approved skills/plugins**, review like human code, start small. | `docs/GOVERNANCE.md` |
| 15 | **Review config every 3–6 months**; remove constraints for resolved model limits. | `docs/GOVERNANCE.md` review log + README maintenance note |
| 16 | **Plugins bundle skills+hooks+MCP** for org-wide distribution. | This whole kit is the pre-plugin form; see GOVERNANCE "packaging" note |

## The one principle to remember

> The harness determines how Claude Code performs more than the model alone.

So treat this config as real infrastructure: own it, version it, review it, and
delete from it as aggressively as you add. A lean, current harness beats a sprawling
stale one.
