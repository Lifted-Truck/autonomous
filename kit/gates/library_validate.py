#!/usr/bin/env python3
"""library_validate — does a LIBRARY entry conform to `library-entry.3`?

The gap HYPERSAW named on 2026-08-18: `test_library_contract` proves the
contract is self-consistent, and `contract_gate` proves a contract declares a
version — but NOTHING checked an actual entry against the contract. They
emitted `absorbs:` correctly and had to say so as an unverified claim, because
no v3 parser exists to disagree with them (distillery is still on v2).

That is the same class as the bug they caught: a rule with nothing able to
exercise it. Same precedent as `status_validate` — a targeted, dependency-free
validator living beside the contract, NOT a second ingester. distillery's
parser turns a corpus into records; this answers one question about one entry,
so the two cannot drift into rival implementations.

Deliberately partial, and the docstring says so rather than the code implying
otherwise: this validates the LINE form's field grammar — the segment rules
that the absorbs bug lived in. Span boundaries and block form are the
ingester's problem and are not attempted here.

Usage:  library_validate.py <LIBRARY.md> [--json]
Exit 0 = every entry conforms · 1 = findings · 2 = unreadable
"""

import json
import re
import sys

LABELS = ("tier", "added", "tags", "origin", "lesson", "evidence",
          "falsifier", "supersedes", "absorbs", "recurred")
REQUIRED = ("title", "tier", "added", "tags", "lesson", "evidence", "falsifier")
TIERS = ("candidate", "canonical", "proliferated")

_MARKER = re.compile(r"^\[(L\d{4})\]\s*(.*)$")
_LABEL = re.compile(rf"^\s*({'|'.join(LABELS)})\s*:\s*(.*)$", re.S)
_REF = re.compile(r"^L\d{4}$")
# `origin` is a BACK-link to a child scope and carries a different shape —
# `<child>#Lxxxx` (contract JSON Schema). Applying the local-reference
# pattern to it made this validator report autonomous's own correct L0001
# as broken on its first run.
_ORIGIN_REF = re.compile(r"^[^#]+#L\d{4}$")
_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_PLACEHOLDER = re.compile(r"^[—–-]\s*(.*)$", re.S)
# Reference-list fields: every element must resolve, or the graph edge is a lie.
_REF_LISTS = {"absorbs"}
_ORIGIN_LISTS = {"origin"}
_REF_SINGLE = {"supersedes"}


def parse_entry(line):
    """One line-form entry -> (fields dict, findings list)."""
    out, bad = {}, []
    m = _MARKER.match(line.strip())
    if not m:
        return out, ["no [Lxxxx] marker at line start"]
    out["id"] = m.group(1)
    segs = m.group(2).split("|")

    out["title"] = segs[0].strip()
    open_field = None
    for i, seg in enumerate(segs[1:], start=1):
        lm = _LABEL.match(seg)
        if lm:
            open_field = lm.group(1)
            out[open_field] = lm.group(2).strip()
            continue
        # An UNKNOWN `label: value` segment goes to `extra` — it does not
        # continue the open field (contract §Segment rules). Folding it in made
        # this validator report HYPERSAW's valid `added:` as malformed, because
        # a trailing `consolidated:` got glued onto the date.
        if re.match(r"^\s*[A-Za-z_][\w-]*\s*:", seg):
            out.setdefault("extra", {})
            open_field = None
            continue
        bare = seg.strip()
        # Segment 1 only, and only if it IS a tier — matching by position alone
        # would let a title's tail become the tier (contract §Segment rules).
        if i == 1 and open_field is None and bare in TIERS:
            out["tier"] = bare
            continue
        if open_field:                       # continuation: restore the pipe
            out[open_field] = f"{out[open_field]} |{seg}".strip()
        elif bare:
            bad.append(f"segment {i} opens no field and continues none: {bare[:40]!r}")
    return out, bad


def validate_entry(line):
    f, findings = parse_entry(line)
    if not f.get("id"):
        return findings
    where = f["id"]

    for req in REQUIRED:
        v = f.get(req, "")
        if not v:
            findings.append(f"{where}: missing required `{req}`")
        elif _PLACEHOLDER.match(v) and req != "title":
            # A placeholder on a REQUIRED field is missing information, not a
            # formatting variation — the line v3 draws and must keep drawing.
            findings.append(f"{where}.{req}: placeholder on a required field")

    if f.get("tier") and f["tier"] not in TIERS:
        findings.append(f"{where}.tier: {f['tier']!r} not in {TIERS}")
    if f.get("added") and not _DATE.match(f["added"]):
        findings.append(f"{where}.added: {f['added']!r} is not YYYY-MM-DD")

    for name in _REF_SINGLE | _REF_LISTS | _ORIGIN_LISTS:
        raw = f.get(name)
        if not raw:
            continue
        if _PLACEHOLDER.match(raw):
            continue                          # absent + preserved as <field>_note
        body = raw.split("—")[0].split("–")[0]   # annotation lives behind the dash
        parts = [p.strip() for p in body.split(",") if p.strip()]
        if not parts:
            findings.append(f"{where}.{name}: no reference before the annotation")
        pat = _ORIGIN_REF if name in _ORIGIN_LISTS else _REF
        shape = "<child>#Lxxxx" if name in _ORIGIN_LISTS else "L\\d{4}"
        bad_parts = [p for p in parts if not pat.match(p)]
        if bad_parts:
            # ONE finding per field, not per comma-separated fragment: a prose
            # value split on its own commas produced three findings for one
            # defect, which is the noise that gets a checker ignored.
            findings.append(f"{where}.{name}: value is neither a {shape} "
                            f"reference nor a placeholder ({raw[:50]!r})")
            continue
        if name in _REF_SINGLE and len(parts) > 1:
            findings.append(f"{where}.{name}: single-valued, got {len(parts)} "
                            f"— consolidation belongs in `absorbs`")
    return findings


def validate_file(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if _MARKER.match(line.strip()):
                for f in validate_entry(line):
                    out.append({"line": n, "finding": f})
    return out


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip().splitlines()[-3], file=sys.stderr)
        return 2
    try:
        findings = validate_file(sys.argv[1])
    except OSError as exc:
        print(f"library_validate: {exc}", file=sys.stderr)
        return 2
    if "--json" in sys.argv:
        print(json.dumps(findings, indent=2))
    else:
        for f in findings:
            print(f"  line {f['line']}: {f['finding']}")
        print(f"library_validate: {len(findings)} finding(s) in {sys.argv[1]}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
