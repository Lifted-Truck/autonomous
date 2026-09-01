#!/usr/bin/env python3
"""batch_close — the ecosystem-level /breakdown, for when per-repo is untenable.

Brief §7 step 7 (an ecosystem `/breakdown` that fans out over open sessions),
built because 39 repos needed closing and 39 sessions is not an evening.

THE DESIGN CONSTRAINT, which decides everything else: `/breakdown`'s value is
SESSION.md, and SESSION.md is "the only prior-session context the next session
trusts" (brief §2). Three of `/breakdown`'s six steps need a human — what today
decided, the thread you would forget, the first move next session — and no
batch can answer them. So this closes only what can be closed HONESTLY, and
the SESSION.md it writes is stamped `closed: mechanical` and says in its own
text that no survey was taken. A batch that wrote a normal-looking SESSION.md
would poison exactly the artifact the next session relies on, which is worse
than leaving the session open.

Triage, per repo:

  mechanical    nothing outstanding that only its session could explain —
                kit-owned edits, and/or a branch whose work is committed.
                Safe to close from here.
  needs-session its OWN uncommitted source changes, or a red oracle. Only its
                session knows what that work is, and a red verify is a finding
                a human should see, not a thing to sweep past.
  clean         nothing to close.

Writes into other repos, so it is a sanctioned batch like `kit_sync --all`:
dry by default, `--apply` required, never merges, never invents content.

  batch_close.py [--apply] [--registry ...]
"""
import argparse, datetime, json, os, subprocess, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, "..", "..")
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_ROOT, "kit", "sweep"))
import state as session_state  # noqa: E402
import sweep                   # noqa: E402

# Files this repo's own batch tools write into other trees. Their presence is
# not the repo's work-in-progress, so it does not make a close "needs-session".
KIT_OWNED = (".kit/", "project.manifest.json", ".harness/")


def _git(repo, *a, default=""):
    r = subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True, timeout=30)
    return r.stdout.strip() if r.returncode == 0 else default


def _dirty(repo):
    raw = subprocess.run(["git", "-C", repo, "status", "--porcelain"],
                         capture_output=True, text=True, timeout=30).stdout
    return [l.split(maxsplit=1)[-1].strip('"') for l in raw.splitlines() if l.strip()]


def triage(repo):
    """(category, facts). Pure read — decides nothing, writes nothing."""
    branch = _git(repo, "rev-parse", "--abbrev-ref", "HEAD")
    # Without a remote there is NO canonical default branch to compare against,
    # so do not guess one. The old code fell back to "main" and therefore
    # triaged a perfectly clean repo on `master` as `mechanical` — it would
    # have opened a session close on a repo with nothing to close. Invisible on
    # this fleet (everything is `main`) and caught only by CI, whose runner
    # inits at `master`: an environment assumption baked into a default.
    origin_head = _git(repo, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD")
    head = origin_head.rsplit("/", 1)[-1] if origin_head else branch
    dirty = _dirty(repo)
    theirs = [f for f in dirty if not f.startswith(KIT_OWNED)]
    n = _git(repo, "rev-list", "--count", "@{u}..HEAD", default="0")
    unpushed = int(n) if n.isdigit() else 0
    verify = session_state._verify_state(repo)
    facts = {"branch": branch, "default": head, "kit_owned": len(dirty) - len(theirs),
             "theirs": theirs, "unpushed": unpushed, "verify": verify,
             "has_remote": bool(_git(repo, "remote"))}
    if theirs:
        return "needs-session", facts
    if verify.get("recorded") and verify.get("exit") not in (0, None) \
            and not verify.get("stale"):
        return "needs-session", facts        # a red oracle is a finding, not litter
    if branch == head and not dirty and not unpushed:
        return "clean", facts
    return "mechanical", facts


SESSION_TEMPLATE = """# SESSION.md — {repo}

> **closed: mechanical** on {date} by `batch_close.py` from the standards repo.
> **No survey was taken.** The three questions a real `/breakdown` asks — what
> today decided, the loose thread most easily forgotten, the first move next
> session — are unanswered here, because no human was asked and this tool will
> not invent them. Treat this file as a STATE SNAPSHOT, not a handoff. If you
> are the next session and you need intent, read the diff and `traces/`, and
> say plainly that you are reconstructing.

## State at close

- branch: `{branch}` (default `{default}`)
- oracle: {verify}
- kit-owned files staged by this close: {kit_owned}
- unpushed commits at close: {unpushed}

## Open threads

Unknown — not surveyed. See the PR opened by this close, if any.
"""


def close_one(repo, name, apply=False, today=None):
    """Mechanical close. Stages kit-owned files, writes an honest SESSION.md,
    opens a PR if there is a remote. Never merges, never commits work that is
    not kit-owned or already committed."""
    cat, facts = triage(repo)
    if cat != "mechanical":
        return {"repo": name, "action": "skipped", "why": cat, "facts": facts}
    date = (today or datetime.date.today()).isoformat()
    plan = {"repo": name, "action": "close", "branch": facts["branch"],
            "stage": facts["kit_owned"], "unpushed": facts["unpushed"]}
    if not apply:
        return plan
    v = facts["verify"]
    body = SESSION_TEMPLATE.format(
        repo=name, date=date, branch=facts["branch"], default=facts["default"],
        verify=("no recorded run" if not v.get("recorded")
                else f"exit {v.get('exit')} ({v.get('note')})"),
        kit_owned=facts["kit_owned"], unpushed=facts["unpushed"])
    with open(os.path.join(repo, "SESSION.md"), "w", encoding="utf-8") as fh:
        fh.write(body)
    branch = facts["branch"]
    if branch == facts["default"]:
        branch = f"chore/session-close-{date}"
        subprocess.run(["git", "-C", repo, "switch", "-c", branch],
                       capture_output=True, timeout=30)
    # Stage ONLY paths that exist. `git add a b c` fails wholesale on a missing
    # pathspec and stages NOTHING — so passing project.manifest.json to a repo
    # without one made the entire close a silent no-op that still reported
    # success. Caught by the test that asserts what actually got committed,
    # which is the only assertion that could have caught it.
    paths = [f for f in ("SESSION.md", ".kit", "project.manifest.json")
             if os.path.exists(os.path.join(repo, f))]
    before = _git(repo, "rev-parse", "HEAD")
    subprocess.run(["git", "-C", repo, "add", *paths], capture_output=True, timeout=30)
    subprocess.run(["git", "-C", repo, "commit", "-m",
                    f"Session close ({date}), mechanical: SESSION.md + kit-owned files\n\n"
                    f"Closed in batch from the standards repo because per-repo close was\n"
                    f"untenable at this scale. NO survey was taken and SESSION.md says so.\n"],
                   capture_output=True, timeout=30)
    after = _git(repo, "rev-parse", "HEAD")
    if after == before:
        # Never report a close that did not happen.
        plan["action"] = "FAILED"
        plan["why"] = "commit did not land (nothing staged?)"
        return plan
    plan["committed"] = after[:7]
    if facts["has_remote"]:
        subprocess.run(["git", "-C", repo, "push", "-u", "origin", "HEAD"],
                       capture_output=True, timeout=120)
        pr = subprocess.run(["gh", "pr", "create", "--fill"], cwd=repo,
                            capture_output=True, text=True, timeout=120)
        plan["pr"] = (pr.stdout or pr.stderr).strip().splitlines()[-1:] or ["(none)"]
    else:
        plan["pr"] = ["no remote — commit is local"]
    return plan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--registry", default=os.path.join(_ROOT, "registry.json"))
    a = ap.parse_args()
    with open(a.registry, encoding="utf-8") as fh:
        projects = sweep.resolve(json.load(fh))
    buckets = {"mechanical": [], "needs-session": [], "clean": []}
    for p in projects:
        if not os.path.isdir(os.path.join(p["path"], ".git")):
            continue
        cat, facts = triage(p["path"])
        buckets[cat].append((p["name"], p["path"], facts))
    print(f"batch_close — {'APPLY' if a.apply else 'DRY RUN'}\n")
    print(f"  mechanical    {len(buckets['mechanical']):3}  closeable from here")
    print(f"  needs-session {len(buckets['needs-session']):3}  their own work, or a red oracle")
    print(f"  clean         {len(buckets['clean']):3}  nothing to close\n")
    for name, path, facts in buckets["needs-session"]:
        why = (", ".join(facts["theirs"][:3]) if facts["theirs"]
               else f"verify exit {facts['verify'].get('exit')}")
        print(f"  HUMAN  {name:34} {why}")
    print()
    for name, path, _ in buckets["mechanical"]:
        r = close_one(path, name, apply=a.apply)
        extra = (f"-> {r.get('pr', [''])[0]}" if a.apply else
                 f"(stage {r['stage']} kit-owned, branch {r['branch']})")
        print(f"  {'closed' if a.apply else 'would':7} {name:34} {extra}")
    if not a.apply:
        print("\n  dry run — pass --apply. Nothing was written.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
