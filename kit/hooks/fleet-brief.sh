#!/usr/bin/env bash
# fleet-brief — SessionStart hook. Surfaces the governor's sweep where the human
# actually is, instead of in a file nobody opens.
#
# WHY NOT RUN THE SWEEP HERE: monitor takes ~4s over 62 repos. Four seconds on
# every session start is a tax that gets the hook disabled, and a disabled hook
# reports nothing — which looks exactly like a healthy fleet. So this reads the
# CACHE and reports its age; the scheduled job does the work.
#
# WHY REPORT THE AGE: a stale dashboard is the failure this whole thing exists
# to prevent. monitor was dead for days and reported nothing, which was
# indistinguishable from clean. A cache with no freshness signal repeats that
# exactly, so the age is stated even when the news is good.
#
# Fail-OPEN: an observer, not a gate (cf. governor/REPO-HYGIENE.md, where
# fail-CLOSED is right because refusing to pass IS the point).
set -uo pipefail

REPO="${AUTONOMOUS_HOME:-$HOME/Documents/Claude/autonomous}"
STATUS="$REPO/governor/STATUS.md"
[ -f "$STATUS" ] || exit 0

now=$(date +%s 2>/dev/null) || exit 0
mtime=$(stat -f %m "$STATUS" 2>/dev/null || stat -c %Y "$STATUS" 2>/dev/null) || exit 0
age_h=$(( (now - mtime) / 3600 ))

# Only the actionable lines. A summary that restates 56 WARNs every session is
# noise, and noise is how a real finding gets skipped.
overdue=$(grep -c '^- \*\*[0-9]*d overdue\*\*' "$STATUS" 2>/dev/null || echo 0)
uncommitted=$(sed -n '/### Uncommitted mailbox writes/,/^### /p' "$STATUS" 2>/dev/null | grep -c '^- `' || echo 0)
high=$(grep -cE '^\| *HIGH' "$STATUS" 2>/dev/null || echo 0)
# S4 (VSM amendment A): the intelligence organ's delivery state. Reported by
# NAME, not count — "1 S4 finding" tells the human nothing, "S4-UNMERGED"
# tells them the audit ran and nobody read it. The 2026-08 audit sat four days.
s4=$(sed -n '/## Outside & then/,/^## /p' "$STATUS" 2>/dev/null \
     | grep -oE '`(S4-[A-Z]+|OPEN-PR)`' | tr -d '`' | sort -u | tr '\n' ',' | sed 's/,$//; s/,/, /g')

msg=""
[ "$overdue" -gt 0 ] 2>/dev/null && msg="$msg ${overdue} OVERDUE exchange(s);"
[ "$uncommitted" -gt 0 ] 2>/dev/null && msg="$msg ${uncommitted} uncommitted mailbox write(s);"
[ "$high" -gt 0 ] 2>/dev/null && msg="$msg ${high} HIGH finding(s);"
[ -n "$s4" ] && msg="$msg S4: ${s4};"

# Stale cache is itself worth saying: >48h means the scheduled sweep is not
# running, and every number below is therefore unreliable.
[ "$age_h" -gt 48 ] && msg="$msg sweep cache is ${age_h}h old — the scheduled job may not be running;"

[ -z "$msg" ] && exit 0

printf '%s' "Governor fleet sweep (${age_h}h old):${msg%;} — see governor/STATUS.md. Surfaced automatically; not necessarily this session's work." \
  | jq -Rs '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:.}}' 2>/dev/null || true
