#!/usr/bin/env python3
"""sweep — the shared SCAN primitive: registry-driven project enumeration,
derived status, and hash-ledgered change detection.

Deterministic by contract: no model calls, no wall-clock in outputs, stable
ordering, idempotent re-runs (unchanged inputs -> identical output, and a
`changed` pass against a fresh ledger update is empty).

Consumers: audit loop, distillery ingest (D1), dispatch collector (E1),
README sweeper. Semantics follow registry.json: rule-based roots with
excludes; groups recurse exactly one level; status is DERIVED, never stored.

Usage:
  sweep.py --registry registry.json list
  sweep.py --registry registry.json changed --ledger .ledger.json \
           --targets LIBRARY.md INDEX.md [--update-ledger]

Output: JSON on stdout. Exit 0 on success, 2 on bad invocation/registry.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys


def _expand(path):
    return os.path.abspath(os.path.expanduser(path))


def resolve(registry):
    """Registry rules -> ordered list of {name, path, group} project dicts."""
    projects = []
    for rule in registry.get("rules", []):
        if "project" in rule:
            path = _expand(rule["project"])
            projects.append(
                {"name": os.path.basename(path), "path": path, "group": None}
            )
        elif "root" in rule:
            root = _expand(rule["root"])
            if not os.path.isdir(root):
                continue
            exclude = set(rule.get("exclude", []))
            groups = set(rule.get("groups", []))
            for child in sorted(os.listdir(root)):
                cpath = os.path.join(root, child)
                if not os.path.isdir(cpath) or child in exclude or child.startswith("."):
                    continue
                if child in groups:
                    for gchild in sorted(os.listdir(cpath)):
                        gpath = os.path.join(cpath, gchild)
                        if os.path.isdir(gpath) and not gchild.startswith("."):
                            projects.append(
                                {"name": child + "/" + gchild, "path": gpath, "group": child}
                            )
                else:
                    projects.append({"name": child, "path": cpath, "group": None})
    return projects


def derive_status(path):
    """Presence checks only — status is derived at sweep time, never stored."""
    def has(*rel):
        return os.path.exists(os.path.join(path, *rel))

    remote = None
    if has(".git"):
        # Narrow except: a repo with no 'origin' exits non-zero (expected) ->
        # None. A missing git binary is a real environment fault -> surface it.
        try:
            remote = subprocess.check_output(
                ["git", "-C", path, "remote", "get-url", "origin"],
                stderr=subprocess.DEVNULL,
            ).decode().strip() or None
        except subprocess.CalledProcessError:
            remote = None

    return {
        "git": has(".git"),
        "remote": remote,  # None = local-only; a URL = has a remote (public/private not inferred)
        "claude_md": has("CLAUDE.md"),
        "verify": has("verify"),
        "roadmap": has("ROADMAP.md"),
        "library": has("LIBRARY.md"),
        "traces": has("traces"),
        "manifest": has("project.manifest.json"),
        "status_surface": has("STATUS.json"),
    }


def content_hash(path, targets):
    """Stable 16-hex digest over the target files that exist; None if none do."""
    parts = []
    for target in sorted(targets):
        fpath = os.path.join(path, target)
        if os.path.isfile(fpath):
            h = hashlib.sha256()
            with open(fpath, "rb") as f:
                h.update(f.read())
            parts.append(target + ":" + h.hexdigest()[:16])
    if not parts:
        return None
    return hashlib.sha256("\n".join(parts).encode()).hexdigest()[:16]


def sweep(registry, targets=None, ledger=None):
    """Full pass: enumerate, derive status, and (if targets) diff vs ledger."""
    ledger = ledger or {}
    records = []
    for proj in resolve(registry):
        rec = dict(proj)
        rec["status"] = derive_status(proj["path"])
        if targets is not None:
            rec["hash"] = content_hash(proj["path"], targets)
            rec["changed"] = rec["hash"] != ledger.get(proj["name"])
        records.append(rec)
    return records


def _load_json(path, what):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError) as exc:
        print("sweep: cannot read %s %s: %s" % (what, path, exc), file=sys.stderr)
        sys.exit(2)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="sweep")
    ap.add_argument("--registry", required=True)
    ap.add_argument("command", choices=["list", "changed"])
    ap.add_argument("--ledger")
    ap.add_argument("--targets", nargs="+", default=["LIBRARY.md"])
    ap.add_argument("--update-ledger", action="store_true")
    args = ap.parse_args(argv)

    registry = _load_json(args.registry, "registry")

    if args.command == "list":
        records = sweep(registry)
    else:
        if not args.ledger:
            print("sweep: changed requires --ledger", file=sys.stderr)
            sys.exit(2)
        ledger = _load_json(args.ledger, "ledger") if os.path.exists(args.ledger) else {}
        records = sweep(registry, targets=args.targets, ledger=ledger)
        if args.update_ledger:
            new_ledger = {r["name"]: r["hash"] for r in records}
            with open(args.ledger, "w") as f:
                json.dump(new_ledger, f, indent=2, sort_keys=True)
                f.write("\n")

    json.dump(records, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
