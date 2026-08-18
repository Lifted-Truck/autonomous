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
_ID = re.compile(r"^id:\s*(\S+)-retrofit-(\S+)\s*$", re.M)


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
    for f in sorted(glob.glob(os.path.join(mail_root, "*", "retrofit-*.md"))):
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
            c = _currency(path)
            # Verdict keys on the EFFECTIVE state (current, nothing missing), not
            # on the declared string equalling the claim: a repo declaring 2.2.0
            # is current against a tool-only 2.2.1, and the tree is truthful.
            # The declared/claimed pair is reported either way — as prose.
            if c.get("current") and not c.get("declared_but_missing"):
                verdict, note = "verified", (f"tree reads CURRENT; declares "
                                             f"{c.get('declared')} (notice claims {claimed})")
            else:
                bits = [f"tree declares {c.get('declared')!r}, notice claims {claimed!r}"]
                if not c.get("current"):
                    behind = [b["version"] for b in c.get("behind", [])]
                    bits.append(f"tree is BEHIND: {behind}")
                if c.get("declared_but_missing"):
                    bits.append(f"declared but missing: {c['declared_but_missing']}")
                verdict, note = "disputed", "; ".join(bits)
        out.append({"file": f, "sender": sender,
                    "claimed": claimed, "verdict": verdict, "note": note})
        if dry:
            continue
        # Frontmatter is protocol state and the RESIDENT owns it (Decision 56);
        # the body is the filer's and is appended to, never edited.
        fm2 = re.sub(r"^status:.*$", f"status: {verdict}", fm, count=1, flags=re.M)
        fm2 = re.sub(r"^ball:.*$", "ball: none", fm2, count=1, flags=re.M)
        fm2 += f"\nverified_by: autonomous retrofit_verify {today}"
        body = text[m.end():]
        stamp = (f"\n\n---\n**autonomous verification, {today}:** `{verdict}` — {note}. "
                 f"The tree was re-read with `kit/currency.py`; this line is the resident's, "
                 f"the text above is the filer's.\n")
        with open(f, "w", encoding="utf-8") as fh:
            fh.write("---\n" + fm2 + "\n---\n" + body.rstrip("\n") + stamp)
    return out


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
