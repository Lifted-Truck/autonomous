#!/usr/bin/env bash
# SessionStart hook — load team/project context dynamically at the start of a session.
# The article: start hooks load context so it's present without anyone @-mentioning it.
# Here we surface the code map. Extend this to pull in anything dynamic — current
# sprint, open incidents, a "what changed this week" note, etc. Stdout is added to
# the session context.
set -euo pipefail

if [ -f CODEMAP.md ]; then
  echo "## Project code map (auto-loaded by SessionStart hook)"
  echo
  cat CODEMAP.md
fi

# Example extension: surface a dynamic context file if your team maintains one.
# [ -f .claude/CONTEXT.dynamic.md ] && { echo; cat .claude/CONTEXT.dynamic.md; }

exit 0
