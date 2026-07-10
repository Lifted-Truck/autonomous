#!/usr/bin/env bash
# Stop hook — continuous improvement of CLAUDE.md.
# The article: stop hooks that PROPOSE CLAUDE.md updates. A deterministic script
# can't read the session, so this is an opt-in nudge: when enabled, it reminds you
# (and Claude, on the next turn) to capture any new gotcha learned this session into
# the right CLAUDE.md. Disabled by default to avoid noise — enable by exporting
# CLAUDE_CAPTURE_REMINDER=1 (e.g. in your shell profile or .claude/settings.json env).
set -euo pipefail

[ "${CLAUDE_CAPTURE_REMINDER:-0}" = "1" ] || exit 0

echo "Reminder: if this session uncovered a non-obvious gotcha or convention, add it"
echo "to the nearest CLAUDE.md (root for project-wide, subdir for local) and delete"
echo "any constraint that's no longer true. Keep the root lean."
exit 0
