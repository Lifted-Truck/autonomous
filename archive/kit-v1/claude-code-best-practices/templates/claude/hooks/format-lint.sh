#!/usr/bin/env bash
# PostToolUse hook — deterministic format/lint of the file Claude just edited.
# The article: enforce linting/formatting via hooks, not instructions the model
# might skip. Receives the tool-call JSON on stdin; extracts the file path; runs the
# matching formatter if it's installed. Exits 0 always (never blocks the edit).
set -euo pipefail

payload="$(cat)"

# Extract file_path from the JSON payload (jq if available, else a portable fallback).
if command -v jq >/dev/null 2>&1; then
  file="$(printf '%s' "$payload" | jq -r '.tool_input.file_path // empty')"
else
  file="$(printf '%s' "$payload" | grep -o '"file_path"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n1 | sed 's/.*:[[:space:]]*"//; s/"$//')"
fi

[ -z "${file:-}" ] && exit 0
[ ! -f "$file" ] && exit 0

run() { command -v "$1" >/dev/null 2>&1 && "$@" >/dev/null 2>&1 || true; }

case "$file" in
  *.ts|*.tsx|*.js|*.jsx|*.json|*.css|*.md) run npx --no-install prettier --write "$file" ;;
  *.py)        run ruff format "$file"; run ruff check --fix "$file" ;;
  *.go)        run gofmt -w "$file" ;;
  *.rs)        run rustfmt "$file" ;;
  *.c|*.cc|*.cpp|*.h|*.hpp) run clang-format -i "$file" ;;
  *.cs)        run dotnet format --include "$file" ;;
  *)           : ;;  # unknown type — nothing to do
esac

exit 0
