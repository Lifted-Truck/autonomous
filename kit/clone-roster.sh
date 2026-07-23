#!/usr/bin/env bash
# clone-roster — reproduce the roster's directory layout on a second machine.
#
# WHY a script and not "clone them all into one folder": the registry, the
# doctrine `@import`, and every cross-repo path assume a specific RELATIVE
# layout (groups nest — `synthetic-worlds/Orrery`, not `Orrery`). Flattening it
# silently breaks the sweep, the monitor, and every integrations brief path.
#
# Run it AFTER cloning `autonomous` itself, from inside that clone:
#   ./kit/clone-roster.sh            # print the plan, clone nothing
#   ./kit/clone-roster.sh --run      # actually clone
#
# Repos with no remote, and roster entries that aren't git repos at all, are
# reported as SKIP — they exist only on the origin machine and no clone can
# reach them. Moving one means giving it a remote first (or copying it by
# hand); the script names them rather than letting them vanish quietly.
set -euo pipefail

cd "$(dirname "$0")/.."
DEST="${CLONE_ROOT:-$(cd .. && pwd)}"   # default: the dir holding this clone
RUN=0
[ "${1:-}" = "--run" ] && RUN=1

python3 kit/sweep/sweep.py --registry registry.json list \
| python3 -c '
import json, sys, os
dest = sys.argv[1]
rows = json.load(sys.stdin)
todo, skip = [], []
for r in rows:
    remote = r["status"].get("remote")
    # Rebuild the path RELATIVE to the roster root so it is machine-portable:
    # the recorded absolute path is the origin machine identity, never reused.
    # `name` ALREADY carries the group prefix for grouped entries
    # (group="synthetic-worlds", name="synthetic-worlds/Antiphon") — joining
    # the two doubles it into a path that no clone can land in.
    rel = r["name"]
    (todo if remote else skip).append((rel, remote, r["status"].get("git")))
for rel, remote, _ in todo:
    print(f"CLONE\t{rel}\t{remote}")
for rel, _, isgit in skip:
    why = "git repo, but NO REMOTE" if isgit else "not a git repo"
    print(f"SKIP\t{rel}\t{why}")
' "$DEST" > /tmp/roster-plan.$$

clones=$(grep -c '^CLONE' /tmp/roster-plan.$$ || true)
skips=$(grep -c '^SKIP' /tmp/roster-plan.$$ || true)

if [ "$RUN" -eq 0 ]; then
  echo "PLAN — destination root: $DEST"
  echo
  sed 's/^/  /' /tmp/roster-plan.$$
  echo
  echo "  $clones cloneable, $skips unreachable (origin-machine only)."
  echo "  Re-run with --run to execute."
  rm -f /tmp/roster-plan.$$
  exit 0
fi

while IFS=$'\t' read -r kind rel arg; do
  [ "$kind" = "CLONE" ] || continue
  target="$DEST/$rel"
  if [ -d "$target/.git" ]; then
    echo "== $rel — already present, pulling"
    git -C "$target" pull --ff-only || echo "   (pull skipped — not fast-forward)"
  else
    echo "== $rel"
    mkdir -p "$(dirname "$target")"
    git clone --quiet "$arg" "$target"
  fi
done < /tmp/roster-plan.$$

echo
echo "Unreachable (exist only on the origin machine):"
grep '^SKIP' /tmp/roster-plan.$$ | cut -f2,3 | sed 's/^/  /'
rm -f /tmp/roster-plan.$$
