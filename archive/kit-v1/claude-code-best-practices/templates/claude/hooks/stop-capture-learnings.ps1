# Stop hook (PowerShell) — continuous improvement of CLAUDE.md.
# Opt-in nudge to capture newly-learned gotchas into the right CLAUDE.md. Disabled by
# default; enable by setting the env var CLAUDE_CAPTURE_REMINDER=1.
$ErrorActionPreference = 'SilentlyContinue'

if ($env:CLAUDE_CAPTURE_REMINDER -ne '1') { exit 0 }

"Reminder: if this session uncovered a non-obvious gotcha or convention, add it"
"to the nearest CLAUDE.md (root for project-wide, subdir for local) and delete"
"any constraint that's no longer true. Keep the root lean."
exit 0
