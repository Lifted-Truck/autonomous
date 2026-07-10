# SessionStart hook (PowerShell) — load project context dynamically at session start.
# Surfaces the code map so it's in context without an @-mention. Extend to pull in
# anything dynamic (current sprint, open incidents, recent changes). Stdout is added
# to the session context.
$ErrorActionPreference = 'SilentlyContinue'

if (Test-Path CODEMAP.md) {
  "## Project code map (auto-loaded by SessionStart hook)`n"
  Get-Content CODEMAP.md -Raw
}

# Example extension: surface a dynamic context file if your team maintains one.
# if (Test-Path .claude/CONTEXT.dynamic.md) { "`n"; Get-Content .claude/CONTEXT.dynamic.md -Raw }

exit 0
