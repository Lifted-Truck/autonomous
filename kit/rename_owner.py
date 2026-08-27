#!/usr/bin/env python3
"""rename_owner — coordinate a GitHub account rename across the fleet.

Two jobs, deliberately narrow:

  --check                      scan: remotes per repo, plus every file
                               reference to the old owner, split LIVE vs
                               RECORD (records are history and stay)
  --apply --new-owner X        rewrite each repo's REMOTE URLs to the new
                               owner. Local git config only — no tracked file
                               is touched, nothing is committed, and it is
                               reversible by re-running with the old name.

Why remotes get rewritten even though GitHub redirects them: a redirect is a
COURTESY that survives only while nobody claims the old name and creates a
repo at the old path. The plan parks the old name precisely to protect the
redirect — but a fleet that DEPENDS on a redirect is one parked-account
mistake away from 44 broken remotes. Point at the real name; keep the
redirect for strangers' links, not our own plumbing.

Writes-stay-home note: a remote URL is machine-local plumbing (.git/config),
not repo content — the same class of thing as running `gh pr list` there.
No resident's tracked tree is modified by --apply.

BRAND vs URL, the distinction that keeps plugins alive: `com.lifted-truck.*`
bundle identifiers, `AUV2_MANUFACTURER_NAME`, JUCE `COMPANY_NAME`, and the
prose company name "Lifted Truck" are PRODUCT identity, pinned by doctrine
(CONVENTIONS.md §Audio plugins). Changing a bundle ID makes every installed
plugin read as a DIFFERENT plugin and breaks saved DAW sessions. The account
rename touches none of it; this tool classifies those lines KEEP so no
session greps its way into rewriting them.

RECORD vs LIVE: dispatch's day archives, DECISIONS.md, traces/, research/,
briefs/, integrations/ and LIBRARY.md quote history — the old name in them is
TRUE (it is what the remote was called then) and rewriting records is
falsification, not maintenance. Everything else is live and should be fixed
by each repo's own session in its next close.
"""
import argparse, json, os, re, subprocess, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, "..")
sys.path.insert(0, os.path.join(_HERE, "sweep"))
import sweep  # noqa: E402

_RECORD = re.compile(
    r"(^|/)(DECISIONS\.md|LIBRARY\.md|CHANGELOG[^/]*|traces/|research/|briefs/"
    r"|integrations/|\d{4}-\d{2}-\d{2}[^/]*\.json)")


def _repos(registry):
    with open(registry, encoding="utf-8") as fh:
        return [p for p in sweep.resolve(json.load(fh))
                if os.path.isdir(os.path.join(p["path"], ".git"))]


_BRAND = re.compile(r"com\.lifted[- ]?truck|MANUFACTURER|COMPANY_NAME"
                    r"|Lifted Truck", re.I)


def check(registry, old_owner):
    pat = old_owner.replace("-", "[- ]?")
    out = []
    for p in _repos(registry):
        remotes = subprocess.run(["git", "-C", p["path"], "remote", "-v"],
                                 capture_output=True, text=True).stdout
        has_old = old_owner.lower() in remotes.lower()
        r = subprocess.run(["git", "-C", p["path"], "grep", "-rIn", "--untracked",
                            "-iE", pat], capture_output=True, text=True, timeout=60)
        live, rec, brand = set(), set(), set()
        for line in r.stdout.splitlines():
            if not line:
                continue
            f, rest = line.split(":", 1)
            if _RECORD.search(f):
                rec.add(f)
            elif _BRAND.search(rest) and "github.com" not in rest.lower():
                brand.add(f)               # product identity — KEEP (doctrine)
            else:
                live.add(f)
        if has_old or live or rec or brand:
            out.append({"repo": p["name"], "remote_old": has_old,
                        "live": sorted(live), "records": sorted(rec),
                        "brand": sorted(brand)})
    return out


def apply_remotes(registry, old_owner, new_owner):
    done, skipped = [], []
    for p in _repos(registry):
        r = subprocess.run(["git", "-C", p["path"], "remote", "-v"],
                           capture_output=True, text=True).stdout
        names = {l.split()[0] for l in r.splitlines() if l.strip()}
        touched = False
        for name in sorted(names):
            url = subprocess.run(["git", "-C", p["path"], "remote", "get-url", name],
                                 capture_output=True, text=True).stdout.strip()
            # Case-insensitive match, protocol preserved exactly: the fleet has
            # both https:// and git@ forms and each repo keeps its own.
            new_url = re.sub(re.escape(old_owner), new_owner, url, flags=re.I)
            if new_url != url:
                subprocess.run(["git", "-C", p["path"], "remote", "set-url",
                                name, new_url], check=True, capture_output=True)
                touched = True
        (done if touched else skipped).append(p["name"])
    return done, skipped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="scan only (this is also the default with no flags)")
    ap.add_argument("--old-owner", default="Lifted-Truck")
    ap.add_argument("--new-owner")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--registry", default=os.path.join(_ROOT, "registry.json"))
    a = ap.parse_args()
    if a.apply:
        if not a.new_owner:
            ap.error("--apply requires --new-owner")
        done, _ = apply_remotes(a.registry, a.old_owner, a.new_owner)
        print(f"remotes rewritten in {len(done)} repos -> {a.new_owner}")
        for n in done:
            print(f"   {n}")
        print("\nVerify one: git -C <repo> remote -v && git -C <repo> fetch --dry-run")
        return 0
    rows = check(a.registry, a.old_owner)
    tot_live = sum(len(r["live"]) for r in rows)
    tot_rec = sum(len(r["records"]) for r in rows)
    tot_brand = sum(len(r.get("brand", [])) for r in rows)
    n_rem = sum(1 for r in rows if r["remote_old"])
    print(f"rename_owner --check ({a.old_owner})\n")
    print(f"  remotes still on old owner : {n_rem} repos")
    print(f"  LIVE file references       : {tot_live} files (fix in each repo's next close)")
    print(f"  RECORD references          : {tot_rec} files (history — LEAVE; rewriting is falsification)")
    print(f"  BRAND / product identity   : {tot_brand} files (bundle IDs, manufacturer — KEEP, doctrine-pinned)\n")
    for r in sorted(rows, key=lambda x: -len(x["live"])):
        if r["live"]:
            print(f"   {r['repo']:34} {len(r['live']):2} live: {', '.join(r['live'][:3])}"
                  + (" …" if len(r["live"]) > 3 else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
