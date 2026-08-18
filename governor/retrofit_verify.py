#!/usr/bin/env python3
"""retrofit_verify — the receiving half of /retrofit Step 6.

A repo finishes a retrofit and files a notice into autonomous's mailbox
carrying its own currency output. This does the only thing that makes that
notice worth anything: RE-READS the repo with currency.py and compares. The
notice is a claim; the tree is the evidence; the verdict is the diff between
them.

  match     → notice frontmatter set to `status: verified`, `ball: none`
  mismatch  → `status: disputed`, and the differences written under the
              notice as a resident section — the filer's words untouched
  no repo   → `status: unresolvable` (registry cannot find the sender)

Deterministic, no model calls. Run by hand, by the session brief, or by the
sweep. Idempotent: an already-verified notice is skipped.

Usage:  retrofit_verify.py [--registry ../registry.json] [--dry]
"""
import argparse, datetime, glob, json, os, re, subprocess, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.join(_HERE, "..")
sys.path.insert(0, os.path.join(_ROOT, "kit", "sweep"))
import sweep  # noqa: E402

_FM = re.compile(r"\A---\n(.*?)\n---\n", re.S)
_ID = re.compile(r"^id:\s*(\S+)-(?:retrofit|kit-sync)-(\S+)\s*$", re.M)


def _repo_path_for(sender, registry):
    want = sender.lower()
    for p in sweep.resolve(registry):
        if p["name"].lower().split("/")[-1] == want:
            return p["path"]
    return None


def _currency(path):
    r = subprocess.run([sys.executable, os.path.join(_ROOT, "kit", "currency.py"), path, "--json"],
                       capture_output=True, text=True, timeout=180)
    return json.loads(r.stdout or "{}")


def verify_all(registry, dry=False, today=None, mail_root=None):
    """mail_root defaults to this repo's integrations/. Tests pass a tempdir:
    currency's gate-check runs the sender's ./verify, and when the sender is
    autonomous that verify re-runs THIS module's tests, whose teardown would
    wipe a shared fixture directory mid-run."""
    today = (today or datetime.date.today()).isoformat()
    mail_root = mail_root or os.path.join(_ROOT, "integrations")
    out = []
    notices = sorted(glob.glob(os.path.join(mail_root, "*", "retrofit-*.md"))
                     + glob.glob(os.path.join(mail_root, "*", "kit-sync-*.md")))
    for f in notices:
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        m = _FM.match(text)
        if not m:
            continue
        fm = m.group(1)
        if re.search(r"^status:\s*(verified|disputed|unresolvable)", fm, re.M):
            continue                                   # already judged
        idm = _ID.search(fm)
        if not idm:
            continue
        sender, claimed = idm.group(1), idm.group(2)
        path = _repo_path_for(sender, registry)
        if not path:
            verdict, note = "unresolvable", f"registry has no repo named {sender}"
        else:
            # A kit-sync receipt is a narrower claim than a retrofit notice: it
            # says the VENDORED MECHANISM is current, not that the whole repo
            # is. Judge it on that, or every sync would read `disputed` for
            # substance gaps it never claimed to close.
            if "kit-sync" in os.path.basename(f):
                sys.path.insert(0, os.path.join(_ROOT, "kit"))
                import kit_sync
                st, _d = kit_sync.check(path)
                # A receipt names the directory it actually wrote. If that is not
                # the repo the registry knows by that name, the run targeted
                # somewhere else and its `current` is about a different tree —
                # silent before, disputed now.
                declared_path = re.search(r"^repo_path:\s*(\S+)\s*$", fm, re.M)
                mismatch = (declared_path and
                            os.path.realpath(os.path.expanduser(declared_path.group(1)))
                            != os.path.realpath(path))
                if mismatch:
                    verdict = "disputed"
                    note = (f"receipt was written for {declared_path.group(1)}, but the "
                            f"registry has {sender} at a different path — the run "
                            f"targeted another directory")
                # version-stale = canonical bytes with an older version LINE, the
                # normal state after a tool-only bump. The mechanism is current;
                # only the label lags. Disputing it would have called two correct
                # repos wrong (harness-grader, vertex) the moment the state was
                # introduced — which it did, for one run.
                elif st in ("current", "version-stale") and kit_sync.kit_version() == claimed:
                    verdict, note = "verified", f".kit/ matches canonical at {claimed} (hash)"
                else:
                    verdict, note = "disputed", (f"kit_sync reads {st!r}; kit is at "
                                                 f"{kit_sync.kit_version()}, notice claims {claimed}")
                out.append({"file": f, "sender": sender, "claimed": claimed,
                            "verdict": verdict, "note": note})
                if not dry:
                    _stamp(f, text, m, verdict, note, today)
                continue
            c = _currency(path)
            # Verdict keys on the EFFECTIVE state (current, nothing missing), not
            # on the declared string equalling the claim: a repo declaring 2.2.0
            # is current against a tool-only 2.2.1, and the tree is truthful.
            # The declared/claimed pair is reported either way — as prose.
            # Judge the notice against the version it CLAIMS, not the kit's
            # latest. babysynth closed correctly at 2.4.1 and was disputed the
            # moment 2.5.0 shipped — punished for a release postdating its own
            # work. Left alone, every kit bump would false-dispute every repo
            # that had just finished. Versions ABOVE the claim are news;
            # `declared_but_missing` spans every version <= declared, so it is
            # the real test of whether the claim holds.
            sys.path.insert(0, os.path.join(_ROOT, "kit"))
            from currency import parse_version          # semver, not string compare
            behind = [b["version"] for b in c.get("behind", [])]
            newer = [v for v in behind if parse_version(v) > parse_version(claimed)]
            declared = c.get("declared") or "pre-2.0.0"
            # `>=`, not `==`: a repo may ADVANCE past its own notice — babysynth
            # filed at 2.4.1, then 2.5.0 landed mid-session with its single
            # requirement already met, so it advanced the declaration. Demanding
            # equality would dispute a repo for being MORE current than it
            # claimed, which is the mirror of the bug fixed an hour earlier.
            advanced = parse_version(declared) > parse_version(claimed)
            if (parse_version(declared) >= parse_version(claimed)
                    and not c.get("declared_but_missing")):
                verdict = "verified"
                note = f"tree satisfies {claimed} in full"
                if advanced:
                    note += f"; since advanced to {declared}"
                if newer:
                    note += f"; the kit has since moved on ({', '.join(newer)}) — not a defect"
            else:
                bits = [f"tree declares {c.get('declared')!r}, notice claims {claimed!r}"]
                at_or_below = [v for v in behind if v <= claimed]
                if at_or_below:
                    bits.append(f"BEHIND at or below its own claim: {at_or_below}")
                if c.get("declared_but_missing"):
                    bits.append(f"declared but missing: {c['declared_but_missing']}")
                verdict, note = "disputed", "; ".join(bits)
        # Decision 66: a session now closes on a BRANCH with an open PR, so the
        # tree read here may be that branch — or `main`, if they switched back,
        # in which case the work is real and simply invisible from here. Name
        # the ref that was read, so a dispute is never mistaken for absent work.
        branch = subprocess.run(["git", "-C", path, "rev-parse", "--abbrev-ref", "HEAD"],
                                capture_output=True, text=True).stdout.strip() if path else ""
        if branch and verdict == "disputed":
            note += (f" [read branch {branch}; if this work sits in an unmerged PR, "
                     f"this passes once it merges or that branch is checked out]")
        out.append({"file": f, "sender": sender, "branch": branch,
                    "claimed": claimed, "verdict": verdict, "note": note})
        if dry:
            continue
        _stamp(f, text, m, verdict, note, today)
    return out


def _stamp(path, text, m, verdict, note, today):
    """Frontmatter is protocol state and the RESIDENT owns it (Decision 56);
    the body is the filer's and is appended to, never edited."""
    fm = m.group(1)
    fm = re.sub(r"^status:.*$", f"status: {verdict}", fm, count=1, flags=re.M)
    fm = re.sub(r"^ball:.*$", "ball: none", fm, count=1, flags=re.M)
    fm += f"\nverified_by: autonomous retrofit_verify {today}"
    stamp = (f"\n\n---\n**autonomous verification, {today}:** `{verdict}` — {note}. "
             f"The repo was re-read; this line is the resident's, the text above "
             f"is the filer's.\n")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("---\n" + fm + "\n---\n" + text[m.end():].rstrip("\n") + stamp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", default=os.path.join(_ROOT, "registry.json"))
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    reg = json.load(open(a.registry, encoding="utf-8"))
    res = verify_all(reg, dry=a.dry)
    if not res:
        print("retrofit_verify: no unjudged notices")
        return 0
    for r in res:
        print(f"  {r['verdict']:12} {r['sender']:28} claims {r['claimed']:8} — {r['note']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
