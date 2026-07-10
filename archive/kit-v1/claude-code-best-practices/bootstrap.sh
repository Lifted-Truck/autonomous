#!/usr/bin/env bash
# Drop the claude-optimization harness into a target repo.
# Detects project type, fills test/lint/format commands and hook invocations, copies
# templates in. Non-destructive: existing files are skipped unless --force.
#
# Usage: ./bootstrap.sh <target-path> [--name NAME] [--shell sh|pwsh] [--force] [--dry-run]
set -euo pipefail

KIT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TPL="$KIT/templates"

TARGET=""; NAME=""; SHELL_KIND="sh"; FORCE=0; DRY=0
while [ $# -gt 0 ]; do
  case "$1" in
    --name)    NAME="$2"; shift 2 ;;
    --shell)   SHELL_KIND="$2"; shift 2 ;;
    --force)   FORCE=1; shift ;;
    --dry-run) DRY=1; shift ;;
    -h|--help) sed -n '2,9p' "$0"; exit 0 ;;
    *)         TARGET="$1"; shift ;;
  esac
done

[ -n "$TARGET" ] || { echo "error: target path required" >&2; exit 1; }
[ -d "$TARGET" ] || { echo "error: target does not exist: $TARGET" >&2; exit 1; }
TARGET="$(cd "$TARGET" && pwd)"
[ -n "$NAME" ] || NAME="$(basename "$TARGET")"

# --- Detect project type & commands -----------------------------------------
TYPE=unknown; TEST='<configure test cmd>'; LINT='<configure lint cmd>'; FMT='<configure format cmd>'
if   [ -f "$TARGET/package.json" ];                                     then TYPE=node;   TEST='npm test';      LINT='npm run lint';  FMT='npx prettier --write .'
elif [ -f "$TARGET/pyproject.toml" ] || [ -f "$TARGET/requirements.txt" ]; then TYPE=python; TEST='pytest';   LINT='ruff check .';  FMT='ruff format .'
elif [ -f "$TARGET/Cargo.toml" ];                                       then TYPE=rust;   TEST='cargo test';   LINT='cargo clippy';  FMT='cargo fmt'
elif [ -f "$TARGET/go.mod" ];                                           then TYPE=go;     TEST='go test ./...';LINT='go vet ./...';  FMT='gofmt -w .'
elif ls "$TARGET"/*.sln "$TARGET"/*.csproj >/dev/null 2>&1;             then TYPE=dotnet; TEST='dotnet test';  LINT='dotnet build';  FMT='dotnet format'
elif [ -f "$TARGET/CMakeLists.txt" ];                                   then TYPE=cpp;    TEST='ctest';        LINT='clang-tidy';    FMT='clang-format -i'
fi

# --- Hook command strings ----------------------------------------------------
if [ "$SHELL_KIND" = "pwsh" ]; then
  hookcmd() { echo "pwsh -NoProfile -File .claude/hooks/$1.ps1"; }
  EXT=ps1
else
  hookcmd() { echo "bash .claude/hooks/$1.sh"; }
  EXT=sh
fi

echo "claude-optimization bootstrap"
echo "  target : $TARGET"
echo "  project: $NAME  (detected type: $TYPE)"
echo "  shell  : $SHELL_KIND$([ $DRY -eq 1 ] && echo '   [DRY RUN]')"
echo ""

# --- Copy engine -------------------------------------------------------------
# subst <infile> <outfile>  — apply placeholder substitutions
subst() {
  sed -e "s|{{PROJECT_NAME}}|$NAME|g" \
      -e "s|{{PROJECT_TYPE}}|$TYPE|g" \
      -e "s|{{TEST_CMD}}|$TEST|g" \
      -e "s|{{LINT_CMD}}|$LINT|g" \
      -e "s|{{FORMAT_CMD}}|$FMT|g" \
      -e "s|{{FORMAT_LINT_HOOK}}|$(hookcmd format-lint)|g" \
      -e "s|{{SESSION_START_HOOK}}|$(hookcmd session-start-context)|g" \
      -e "s|{{STOP_HOOK}}|$(hookcmd stop-capture-learnings)|g" \
      "$1" > "$2"
}

# deploy <srcRel> <dstRel> <substitute:0|1>
deploy() {
  local src="$TPL/$1" dst="$TARGET/$2" do_subst="$3"
  [ -f "$src" ] || { echo "  ! missing template: $1"; return; }
  if [ -e "$dst" ] && [ $FORCE -eq 0 ]; then echo "  skip   $2 (exists)"; return; fi
  local action; [ -e "$dst" ] && action=over || action=write
  if [ $DRY -eq 1 ]; then echo "  $action  $2"; return; fi
  mkdir -p "$(dirname "$dst")"
  if [ "$do_subst" = "1" ]; then subst "$src" "$dst"; else cp "$src" "$dst"; fi
  echo "  $action  $2"
}

deploy 'CLAUDE.root.md' 'CLAUDE.md'     1
deploy 'CODEMAP.md'     'CODEMAP.md'    1
deploy '.claudeignore'  '.claudeignore' 0

deploy 'claude/settings.json'                  '.claude/settings.json'                  1
deploy 'claude/.mcp.json'                      '.mcp.json'                              0
deploy 'claude/agents/codebase-mapper.md'      '.claude/agents/codebase-mapper.md'      0
deploy 'claude/skills/example-domain/SKILL.md' '.claude/skills/example-domain/SKILL.md' 0
deploy 'CLAUDE.subdir.md'                      '.claude/templates/CLAUDE.subdir.md'     1

for n in format-lint session-start-context stop-capture-learnings; do
  deploy "claude/hooks/$n.$EXT" ".claude/hooks/$n.$EXT" 0
  [ $DRY -eq 0 ] && [ "$EXT" = "sh" ] && [ -f "$TARGET/.claude/hooks/$n.sh" ] && chmod +x "$TARGET/.claude/hooks/$n.sh" || true
done

echo ""
echo "Done. Next:"
echo "  1. Edit $NAME/CLAUDE.md  — keep it to pointers + gotchas."
echo "  2. Fill in CODEMAP.md with the real layout."
echo "  3. Work through the kit's docs/CHECKLIST.md and assign an owner in docs/GOVERNANCE.md."
[ "$TYPE" = "unknown" ] && echo "  !  Project type not detected — set test/lint/format commands in CLAUDE.md manually."
