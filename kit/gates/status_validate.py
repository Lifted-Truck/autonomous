#!/usr/bin/env python3
"""status_validate — validator for the `status.1` STATUS surface contract.

Provenance: contract-test fixtures authored by dispatch (dispatch-001,
`contract-tests-status1.md`, filed 2026-07-10), consumer-authored and
resident-landed per INTEGRATIONS §3. Landed by autonomous as Decision 45.

WHY A TARGETED VALIDATOR AND NOT `jsonschema`: CI here installs nothing — the
workflow runs `./verify fast` on a bare interpreter. A dependency in the
CI-blocking path leaves two options when it is absent, and both are bad: fail
red for a reason unrelated to the change, or skip — and a skipped security-class
check is the blind-gate trap that governor/REPO-HYGIENE.md exists to forbid.
Layer-0 stays dependency-free, so this validates `status.1` specifically rather
than implementing a JSON Schema engine. `kit/contracts/status.md` remains the
normative schema; this is its executable half.

WHY IT RETURNS A LIST, NOT A BOOL: dispatch's third fixture pins error
GRANULARITY, not just rejection — `missing-field.json` must fail with at least
four *named* findings. That is a sharper contract than "is it valid," because it
catches a validator that rejects the right document for the wrong reason, which
would pass a pass/fail test while being useless to a consumer trying to repair
its own output.
"""

import re

_LESSON = re.compile(r"^L\d{4}$")
_TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")


def _req(obj, keys, where, out):
    for k in keys:
        if k not in obj:
            out.append(f"{where}: missing required `{k}`")


def validate(doc):
    """Return a list of finding strings. Empty list == valid `status.1`."""
    out = []
    if not isinstance(doc, dict):
        return ["root: not a JSON object"]

    _req(doc, ("schema", "project", "ts", "quiet"), "root", out)

    if "schema" in doc and doc["schema"] != "status.1":
        out.append(f"root.schema: expected 'status.1', got {doc['schema']!r}")
    if "project" in doc and not isinstance(doc["project"], str):
        out.append("root.project: not a string")
    if "ts" in doc and not (isinstance(doc["ts"], str) and _TS.match(doc["ts"])):
        out.append("root.ts: not an ISO-8601 date-time")
    # `quiet` is the field that distinguishes "collected, nothing changed" from
    # "never collected" (contract §Semantics). A missing one is not a default —
    # it destroys the only signal that separates a quiet day from an absent one.
    if "quiet" in doc and not isinstance(doc["quiet"], bool):
        out.append("root.quiet: not a boolean")

    rp = doc.get("roadmap_phase")
    if rp is not None:
        if not isinstance(rp, dict):
            out.append("roadmap_phase: not an object")
        else:
            _req(rp, ("id", "title"), "roadmap_phase", out)
            if "gate_state" in rp and rp["gate_state"] not in ("open", "green"):
                out.append(f"roadmap_phase.gate_state: not one of open|green "
                           f"({rp['gate_state']!r})")

    lv = doc.get("last_verify")
    if lv is not None:
        if not isinstance(lv, dict):
            out.append("last_verify: not an object")
        else:
            _req(lv, ("target", "exit", "git", "ts"), "last_verify", out)
            if "exit" in lv and not isinstance(lv["exit"], int):
                out.append("last_verify.exit: not an integer")

    if "recent_since" in doc and not (
            isinstance(doc["recent_since"], str) and _TS.match(doc["recent_since"])):
        out.append("recent_since: not an ISO-8601 date-time")

    rec = doc.get("recent")
    if rec is not None:
        if not isinstance(rec, dict):
            out.append("recent: not an object")
        else:
            commits = rec.get("commits")
            if commits is not None:
                if not isinstance(commits, list):
                    out.append("recent.commits: not an array")
                else:
                    for i, c in enumerate(commits):
                        if not isinstance(c, dict):
                            out.append(f"recent.commits[{i}]: not an object")
                            continue
                        _req(c, ("hash", "subject"), f"recent.commits[{i}]", out)
            for name in ("decisions", "traces"):
                v = rec.get(name)
                if v is not None:
                    if not isinstance(v, list):
                        out.append(f"recent.{name}: not an array")
                    elif not all(isinstance(x, str) for x in v):
                        out.append(f"recent.{name}: contains a non-string entry")
            lessons = rec.get("lessons")
            if lessons is not None:
                if not isinstance(lessons, list):
                    out.append("recent.lessons: not an array")
                else:
                    for i, l in enumerate(lessons):
                        if not (isinstance(l, str) and _LESSON.match(l)):
                            out.append(f"recent.lessons[{i}]: {l!r} does not match L\\d{{4}}")
    return out


if __name__ == "__main__":
    import json
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "STATUS.json"
    try:
        with open(path, encoding="utf-8") as f:
            findings = validate(json.load(f))
    except FileNotFoundError:
        print(f"skip  status: no {path}")
        sys.exit(0)
    except json.JSONDecodeError as exc:
        print(f"status: {path} is not valid JSON ({exc})")
        sys.exit(1)
    if findings:
        for f_ in findings:
            print(f"status: {f_}")
        sys.exit(1)
    print(f"ok    status: {path} validates against status.1")
