#!/usr/bin/env python3
"""kit_sync — install or check a repo's VENDORED kit files.

The distribution half of the mechanism/substance split (2026-08-18). Kit
MECHANISM (gate code, hooks) is vendored into each repo's `.kit/` and pinned
by checksum; kit SUBSTANCE (charter, ROADMAP, DECISIONS, LIBRARY) stays a
judgment-bearing retrofit. Only mechanism goes through here.

Why this exists, concretely: `leak_gate` was copied into every repo by hand
and had drifted into TEN distinct implementations, NINE of them missing the
Windows identity pattern, while every one of those repos declared a
kit_version. Copying is why. The version was a claim about a copy, and a copy
can lie — so `currency.py` had to plant identity paths inside foreign repos
and run their oracle to find out the truth, which is where today's whole
defect family came from (record clobber, plant collision, ignore-blinding).
A checksum answers the same question in microseconds and cannot collide with
anything.

  install:  kit_sync.py <repo>            writes .kit/ + .kit/MANIFEST
  check  :  kit_sync.py <repo> --check    compares hashes, writes nothing
  fleet  :  kit_sync.py --all [--check]   every repo in the registry

Never commits: these are other residents' repos, and writes stay home. The
files it writes are deterministic, so a resident's in-flight work cannot be
buried by them and they cannot be buried by it.
"""
import argparse, hashlib, json, os, shutil, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, "..")

# Vendored set: kit-OWNED mechanism only. A file listed here is machine-owned
# in every consuming repo — never hand-edited there, never project-specific.
VENDORED = ["kit-gates.sh"]


def _sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def kit_version():
    with open(os.path.join(_HERE, "VERSION"), encoding="utf-8") as fh:
        return fh.read().strip()


def canonical():
    """{filename: (abs_source_path, sha256)} for the kit's current mechanism."""
    out = {}
    for name in VENDORED:
        p = os.path.join(_HERE, "vendor", name)
        out[name] = (p, _sha(p))
    return out


def check(repo):
    """Compare a repo's vendored files against the kit. Pure read.

    Returns (status, details) where status is one of:
      current   every vendored file matches the kit's current bytes
      stale     present but differs — a plain kit_sync away
      edited    MANIFEST disagrees with the repo's own files (local edit)
      absent    no .kit/ at all — this repo predates vendoring
    """
    kd = os.path.join(repo, ".kit")
    man = os.path.join(kd, "MANIFEST")
    if not os.path.isdir(kd) or not os.path.isfile(man):
        return "absent", {}
    listed = {}
    declared = None
    with open(man, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith("kit_version:"):
                declared = line.split(":", 1)[1].strip()
            elif line and not line.startswith("#"):
                sha, name = line.split(None, 1)
                listed[name.strip()] = sha
    can = canonical()
    stale, edited = [], []
    for name, (_, want) in can.items():
        local = os.path.join(kd, name)
        if not os.path.isfile(local):
            stale.append(name); continue
        actual = _sha(local)
        if listed.get(name) not in (None, actual):
            edited.append(name)          # file != what MANIFEST claims
        elif actual != want:
            stale.append(name)           # honest copy, but an old version
    if edited:
        return "edited", {"files": edited, "declared": declared}
    if stale:
        return "stale", {"files": stale, "declared": declared}
    return "current", {"declared": declared}


def install(repo):
    kd = os.path.join(repo, ".kit")
    os.makedirs(kd, exist_ok=True)
    lines = [f"kit_version: {kit_version()}",
             "# KIT-OWNED. Written by kit_sync.py — do not hand-edit these files.",
             "# ./verify recomputes these hashes and goes red if they disagree."]
    for name, (src, sha) in sorted(canonical().items()):
        shutil.copy2(src, os.path.join(kd, name))
        os.chmod(os.path.join(kd, name), 0o644)
        lines.append(f"{sha}  {name}")
    with open(os.path.join(kd, "MANIFEST"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return check(repo)[0]


def _repos(registry):
    sys.path.insert(0, os.path.join(_HERE, "sweep"))
    import sweep
    with open(registry, encoding="utf-8") as fh:
        return [(p["name"], p["path"]) for p in sweep.resolve(json.load(fh))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--registry", default=os.path.join(_ROOT, "registry.json"))
    a = ap.parse_args()
    targets = _repos(a.registry) if a.all else [(os.path.basename(os.path.abspath(a.repo)), a.repo)]
    if not a.all and not a.repo:
        ap.error("give a repo path or --all")
    counts = {}
    for name, path in targets:
        st, d = check(path)
        if not a.check and st in ("stale", "absent", "edited"):
            st = install(path) + " (synced)"
        counts[st.split()[0]] = counts.get(st.split()[0], 0) + 1
        note = ""
        if d.get("files"):
            note = " — " + ", ".join(d["files"])
        if a.all and st.startswith("current"):
            continue                      # only report what needs attention
        print(f"  {st:18} {name}{note}")
    print("kit_sync: " + ", ".join(f"{v} {k}" for k, v in sorted(counts.items()))
          + (f"   (kit {kit_version()})"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
