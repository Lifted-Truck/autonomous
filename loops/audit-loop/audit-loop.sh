#!/usr/bin/env bash
# audit-loop.sh — run the cross-project AUDIT loop (propose-only by default) at
# each configured parent scope.
#
# For each scope it runs the Claude CLI headless with run-audit-loop.prompt.md in
# PROPOSE-ONLY mode: the model analyses the children and writes a dated proposal to
# <scope>/audit-runs/, but does NOT mutate the authoritative LIBRARY.md / INDEX.md /
# AUDIT-STATE.json. You review the proposal and apply on-demand. This keeps
# promotion into the shared, high-trust store behind human approval — the
# staging-buffer defense from the memory-poisoning literature.
#
# Configuration (set via environment, or a local `audit-loop.config` next to this
# script — see audit-loop.config.example; that file is git-ignored):
#   AKL_SCOPES       space/newline-separated ABSOLUTE paths to parent scopes  (REQUIRED)
#   AKL_PROMPT_DIR   dir holding run-audit-loop.prompt.md   (default: this script's dir)
#   AKL_CLAUDE_BIN   path to the claude CLI                 (default: first on PATH)
#   AKL_MODEL        model id                               (default: claude-opus-4-8)
#
# Usage:
#   ./audit-loop.sh                 # propose-only for all configured scopes
#   AUDIT_APPLY=1 ./audit-loop.sh   # apply mode — writes to the real store
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Load optional local config (git-ignored) for machine-specific settings.
[ -f "$SCRIPT_DIR/audit-loop.config" ] && . "$SCRIPT_DIR/audit-loop.config"

PROMPT_DIR="${AKL_PROMPT_DIR:-$SCRIPT_DIR}"
PROMPT="$PROMPT_DIR/run-audit-loop.prompt.md"
CLAUDE_BIN="${AKL_CLAUDE_BIN:-$(command -v claude || true)}"
MODEL="${AKL_MODEL:-claude-opus-4-8}"

# Parse scopes (space- or newline-separated) into an array.
read -r -a SCOPES <<< "${AKL_SCOPES:-}"

if [ -z "${CLAUDE_BIN:-}" ]; then
  echo "audit-loop: claude CLI not found. Set AKL_CLAUDE_BIN or add 'claude' to PATH." >&2; exit 2
fi
if [ ! -f "$PROMPT" ]; then
  echo "audit-loop: prompt not found at $PROMPT. Set AKL_PROMPT_DIR to the dir holding run-audit-loop.prompt.md." >&2; exit 2
fi
if [ "${#SCOPES[@]}" -eq 0 ]; then
  echo "audit-loop: no scopes configured. Set AKL_SCOPES (env) or create $SCRIPT_DIR/audit-loop.config." >&2
  echo "  example: export AKL_SCOPES=\"\$HOME/projects/group-a \$HOME/projects/group-b\"" >&2
  exit 2
fi

STAMP="$(date +%F)"

for scope in "${SCOPES[@]}"; do
  [ -d "$scope" ] || { echo "skip: $scope (missing)"; continue; }
  [ -f "$scope/AUDIT-STATE.json" ] || { echo "skip: $scope (no audit loop installed)"; continue; }
  mkdir -p "$scope/audit-runs"
  log="$scope/audit-runs/${STAMP}.run.log"

  if [ "${AUDIT_APPLY:-0}" = "1" ]; then
    mode="apply"; directive="RUN MODE: apply."
  else
    mode="propose-only"; directive="RUN MODE: propose-only. Do NOT modify LIBRARY.md, INDEX.md, or AUDIT-STATE.json; write proposed changes to ./audit-runs/${STAMP}.proposal.md and stop."
  fi

  echo "[$(date '+%F %T')] audit ($mode): $scope" | tee -a "$log"
  ( cd "$scope" && "$CLAUDE_BIN" -p "$(cat "$PROMPT")

$directive" \
      --model "$MODEL" \
      --dangerously-skip-permissions ) >>"$log" 2>&1 \
    && echo "[$(date '+%F %T')] done: see audit-runs/${STAMP}.proposal.md" | tee -a "$log" \
    || echo "[$(date '+%F %T')] FAILED (exit $?) — see $log" | tee -a "$log"
done
