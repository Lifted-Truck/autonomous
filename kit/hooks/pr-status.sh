#!/usr/bin/env bash
# pr-status — UserPromptSubmit hook. Injects the REAL git/PR state of the cwd
# repo into the agent's context before it answers.
#
# WHY THIS EXISTS: without it, the agent learns a PR merged only when the human
# says "merged" — so the human has to remember, and an early "merged" (said
# while checks were still running) puts the agent to work on a false premise.
# Both failure modes are the same bug: a human recollection standing in for a
# machine-checkable fact. Doctrine: deterministic code decides, AI interprets.
#
# FAIL-OPEN, DELIBERATELY. Every failure path exits 0 and silent. This is an
# OBSERVER, not a gate — the fail-CLOSED rule in governor/REPO-HYGIENE.md
# applies to gates, where refusing to pass is the whole point. Here, blocking
# a prompt because `gh` was slow would be the defect.
#
# Output: a JSON object on stdout with hookSpecificOutput.additionalContext.
# Silence (no output) when there's nothing the agent needs to know.
# NO `set -e`, and deliberately NO `trap ... ERR`. An ERR trap looks like the
# safe choice here and is the opposite: it fires on ORDINARY non-zero exits —
# `git symbolic-ref refs/remotes/origin/HEAD` returns 1 whenever origin/HEAD
# isn't set locally, which is the common case. The first version of this hook
# trapped that and exited silently on every prompt in every repo, i.e. the
# fail-open guard produced fail-silent-always. Probes are guarded explicitly
# with `|| true` / `|| emit_nothing` instead, one at a time.
set -uo pipefail

emit_nothing() { exit 0; }

# --- cheap local guards, no network ------------------------------------------
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || emit_nothing
command -v gh >/dev/null 2>&1 || emit_nothing
command -v jq >/dev/null 2>&1 || emit_nothing
git remote get-url origin >/dev/null 2>&1 || emit_nothing

ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || emit_nothing
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null) || emit_nothing

# --- cache: this runs on EVERY prompt, so a cold `gh` call per turn is a tax --
# Keyed by repo+branch; TTL short enough that a merge landing mid-session is
# noticed quickly, long enough that a burst of prompts costs one network call.
TTL=${PR_STATUS_TTL:-60}
CACHE_DIR="${TMPDIR:-/tmp}/claude-pr-status"
mkdir -p "$CACHE_DIR" 2>/dev/null || emit_nothing
KEY=$(printf '%s@%s' "$ROOT" "$BRANCH" | tr -c 'A-Za-z0-9' '_')
CACHE="$CACHE_DIR/$KEY"

cache_fresh() {
  [ -f "$CACHE" ] || return 1
  # `find -newermt` isn't portable to Git Bash; compare mtime numerically.
  local now mtime
  now=$(date +%s 2>/dev/null) || return 1
  mtime=$(stat -f %m "$CACHE" 2>/dev/null || stat -c %Y "$CACHE" 2>/dev/null) || return 1
  [ $((now - mtime)) -lt "$TTL" ]
}

if cache_fresh; then
  cat "$CACHE"
  exit 0
fi

# --- local facts (free) ------------------------------------------------------
DIRTY=""
git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null || DIRTY=" · UNCOMMITTED changes"

# origin/HEAD is frequently absent in a plain `git clone`d repo, so this cannot
# be the only source of the base branch name — fall back to whichever of
# main/master actually exists as a remote ref.
BASE=$(git symbolic-ref --quiet refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || true)
if [ -z "$BASE" ]; then
  if git show-ref --verify --quiet refs/remotes/origin/main; then BASE=main
  elif git show-ref --verify --quiet refs/remotes/origin/master; then BASE=master
  else BASE=""; fi
fi

SYNC=""
if [ -n "$BASE" ] && counts=$(git rev-list --left-right --count "origin/$BASE...HEAD" 2>/dev/null); then
  behind=$(printf '%s' "$counts" | cut -f1)
  ahead=$(printf '%s' "$counts" | cut -f2)
  case "$behind" in ''|*[!0-9]*) behind=0 ;; esac
  case "$ahead"  in ''|*[!0-9]*) ahead=0  ;; esac
  [ "$behind" -gt 0 ] && SYNC="$SYNC · ${behind} behind origin/$BASE — PULL before branching"
  [ "$ahead" -gt 0 ]  && SYNC="$SYNC · ${ahead} unpushed"
fi

# --- remote facts (one network call) -----------------------------------------
# Ask for THIS branch's PR. Exits nonzero when the branch has no PR, which is
# the common, uninteresting case — hence `|| true` rather than a failure path.
PR_JSON=$(gh pr view --json number,title,state,mergedAt,mergeable,url,statusCheckRollup 2>/dev/null || true)

LINE=""
if [ -n "$PR_JSON" ]; then
  LINE=$(printf '%s' "$PR_JSON" | jq -r '
    def checks:
      if (.statusCheckRollup // empty | length) == 0 then "no checks"
      else
        ([.statusCheckRollup[] | (.conclusion // .state // "PENDING")]) as $c
        | if   ($c | any(. == "FAILURE" or . == "TIMED_OUT" or . == "CANCELLED")) then "checks FAILING"
          elif ($c | any(. == "PENDING" or . == "IN_PROGRESS" or . == "QUEUED" or . == "")) then "checks RUNNING"
          else "checks passing" end
      end;
    "PR #\(.number) \"\(.title)\" is \(.state)"
    + (if .state == "MERGED" then " (merged \(.mergedAt))"
       elif .state == "OPEN" then " · \(checks) · mergeable=\(.mergeable // "UNKNOWN")"
       else "" end)
  ' 2>/dev/null || true)
fi

if [ -z "$LINE" ]; then
  # No PR for this branch. The other thing worth knowing: PRs merged recently
  # that this checkout may not have pulled yet.
  RECENT=$(gh pr list --state merged --limit 3 --json number,title,mergedAt \
           --jq '[.[] | "#\(.number) \(.title) (merged \(.mergedAt))"] | join("; ")' 2>/dev/null || true)
  [ -n "$RECENT" ] && LINE="no PR for this branch · recently merged: $RECENT"
fi

[ -z "$LINE$SYNC$DIRTY" ] && emit_nothing

CTX="git/PR state (read directly, do NOT rely on the user's recollection of merge status): repo $(basename "$ROOT") · branch $BRANCH${SYNC}${DIRTY} · ${LINE:-no open PR}"

printf '%s' "$CTX" | jq -Rs '{
  hookSpecificOutput: {
    hookEventName: "UserPromptSubmit",
    additionalContext: .
  },
  suppressOutput: true
}' > "$CACHE" 2>/dev/null || emit_nothing

cat "$CACHE"
