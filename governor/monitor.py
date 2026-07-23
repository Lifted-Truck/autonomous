#!/usr/bin/env python3
"""monitor — the governor's deterministic fleet-health watchdog.

Rolls up per-repo health checks across the roster into a STATUS dashboard +
severity summary, so "how is the fleet doing?" is one command instead of the
manual audits. NO model calls (AI/deterministic boundary — the watchdog is
deterministic by contract). Read-only across the roster; writes only its own
STATUS.md (writes-stay-home).

This is the watchdog-as-MONITOR — the earned half of the governor. The
fleet-CONTROLLER half (HALT sentinel, conductor, coherence critic) waits for a
running organ fleet to govern; there is none yet, so it is not built.

Per-repo checks:
  LEAK     (HIGH) machine-absolute paths / username in tracked files (leak_scan)
  UNGATED  (WARN) ./verify exists but no leak_gate wired into it
  NO-CI    (WARN) has a remote but no .github/workflows/*.yml
  STALE    (WARN) README 'Last verified' missing or older than --stale-days
  STATUS-PROSE (WARN) manifest 'status' carries progress content (Decision 28:
                 phase state belongs in ROADMAP, not the manifest)
  GAPS     (INFO) missing harness files (claude_md/roadmap/traces/manifest/library)

Usage:
  monitor.py --registry ../registry.json [--stale-days 30]
             [--today YYYY-MM-DD] [--out governor/STATUS.md] [--json]
"""

import argparse
import datetime
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "kit", "sweep"))
import sweep        # noqa: E402  (roster enumeration + derive_status)
sys.path.insert(0, _HERE)
import leak_scan    # noqa: E402  (the leak content scan, kept consistent with the gate)

# Progress content that belongs in ROADMAP, not the manifest status field
# (Decision 28). Case-sensitive DONE/CLOSED + the ✅/🟡 status glyphs catch real
# status prose; a short "RATIFIED <date>"/"see ROADMAP" pointer does not — and
# incidental refs like "O0 gate" must NOT trip it, so we do not match phase ids.
_STATUS_PROSE = re.compile(r"\bDONE\b|\bCLOSED\b|\bIMPLEMENTED\b|[✅🟡]")
_LAST_VERIFIED = re.compile(r"[Ll]ast verified[^:\n]*:\s*(\d{4}-\d{2}-\d{2})")


def _read(path, *rel):
    p = os.path.join(path, *rel)
    try:
        with open(p, encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return None


def readme_last_verified(path):
    """The ISO date on the README's 'Last verified' line, or None if absent."""
    text = _read(path, "README.md")
    if text is None:
        return None
    m = _LAST_VERIFIED.search(text)
    return m.group(1) if m else None


def days_since(datestr, today):
    y, m, d = (int(x) for x in datestr.split("-"))
    return (today - datetime.date(y, m, d)).days


def manifest_status_prose(path):
    """The offending snippet if the manifest status carries progress content,
    else None. A long field is a smell even without a keyword (the pre-Dec-28
    Orrery status was 447 chars); the pointer form ('see ROADMAP') is short."""
    text = _read(path, "project.manifest.json")
    if text is None:
        return None
    try:
        status = json.loads(text).get("status", "")
    except ValueError:
        return None
    if _STATUS_PROSE.search(status) or len(status) > 250:
        return status[:90]
    return None


def verify_has_leak_gate(path):
    """True/False if a ./verify exists (does it wire leak_gate?), None if none."""
    text = _read(path, "verify")
    return None if text is None else ("leak_gate" in text)


def has_ci(path):
    d = os.path.join(path, ".github", "workflows")
    return os.path.isdir(d) and any(
        f.endswith((".yml", ".yaml")) for f in os.listdir(d)
    )


def check_repo(proj, today, stale_days):
    """All checks for one repo -> {check: (severity, detail)}. Read-only."""
    path = proj["path"]
    out = {}
    st = sweep.derive_status(path)
    if not st["git"]:
        return out  # non-git dirs carry no history to leak or gate

    # Identity leak (the actual username in tracked files) is HIGH — fix now.
    # A generic /Users/<other>/ path (a foreign example, a leak-detection test
    # literal) is WARN: review or allowlist, but it isn't YOUR identity leaking.
    leaks = leak_scan.scan_repo(path)
    if any(lbl == "local username" for _, lbl, _ in leaks):
        n = sum(1 for _, lbl, _ in leaks if lbl == "local username")
        out["LEAK"] = ("HIGH", f"username in {n} tracked line(s)")
    elif any(lbl == "absolute home path" for _, lbl, _ in leaks):
        out["PATH"] = ("WARN", "generic /Users path — review or allowlist")

    gated = verify_has_leak_gate(path)
    if gated is False:
        out["UNGATED"] = ("WARN", "./verify has no leak_gate")

    if st.get("remote") and not has_ci(path):
        out["NO-CI"] = ("WARN", "remote but no .github/workflows")

    lv = readme_last_verified(path)
    if lv is None:
        if st["claude_md"] or st["roadmap"]:      # a harnessed repo should have one
            out["STALE"] = ("WARN", "README has no 'Last verified' line")
    elif days_since(lv, today) > stale_days:
        out["STALE"] = ("WARN", f"README {days_since(lv, today)}d stale (last {lv})")

    prose = manifest_status_prose(path)
    if prose:
        out["STATUS-PROSE"] = ("WARN", "manifest status carries progress content")

    gaps = [k for k in ("claude_md", "roadmap", "traces", "manifest", "library")
            if not st.get(k)]
    if gaps and (st["claude_md"] or st["verify"]):  # only for partially-harnessed repos
        out["GAPS"] = ("INFO", "missing " + ",".join(gaps))
    return out


def render_status(rows, today, stale_days):
    sev = {"HIGH": 0, "WARN": 0, "INFO": 0}
    for _, checks in rows:
        for c in checks.values():
            sev[c[0]] += 1
    lines = [
        "# Fleet health — governor watchdog (deterministic monitor)",
        "",
        f"*Generated {today.isoformat()} · stale threshold {stale_days}d · "
        f"no model calls.* Run: `python3 governor/monitor.py --registry registry.json`",
        "",
        f"**{sev['HIGH']} HIGH · {sev['WARN']} WARN · {sev['INFO']} INFO** "
        f"across {len(rows)} repos.",
        "",
        "| repo | findings |",
        "|---|---|",
    ]
    order = {"HIGH": 0, "WARN": 1, "INFO": 2}
    flagged = [(n, c) for n, c in rows if c]
    flagged.sort(key=lambda r: min(order[v[0]] for v in r[1].values()))
    for name, checks in flagged:
        parts = sorted(checks.items(), key=lambda kv: order[kv[1][0]])
        cells = " · ".join(f"**{k}** {v[1]}" if v[0] == "HIGH" else f"{k} ({v[1]})"
                           for k, v in parts)
        lines.append(f"| {name} | {cells} |")
    if not flagged:
        lines.append("| — | fleet clean ✓ |")
    lines.append("")
    lines.append("Severities: HIGH = fix now (privacy leak). WARN = policy "
                 "drift (ungated / no-CI / stale README / manifest status prose). "
                 "INFO = incomplete harness. Un-flagged repos passed every check.")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(prog="monitor")
    ap.add_argument("--registry", required=True)
    ap.add_argument("--stale-days", type=int, default=30)
    ap.add_argument("--today", help="ISO date override (default: system date)")
    ap.add_argument("--out", default=None, help="write STATUS markdown here")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    today = (datetime.date.fromisoformat(args.today) if args.today
             else datetime.date.today())
    registry = json.load(open(args.registry))
    rows = [(p["name"], check_repo(p, today, args.stale_days))
            for p in sweep.resolve(registry)]

    if args.json:
        json.dump({n: c for n, c in rows}, sys.stdout, indent=2, sort_keys=True)
        sys.stdout.write("\n")
        return 0

    md = render_status(rows, today, args.stale_days)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(md)
    # compact stdout summary (the dashboard is the file)
    sev = {"HIGH": 0, "WARN": 0, "INFO": 0}
    for _, c in rows:
        for v in c.values():
            sev[v[0]] += 1
    print(f"monitor: {sev['HIGH']} HIGH · {sev['WARN']} WARN · {sev['INFO']} INFO "
          f"across {len(rows)} repos"
          + (f" → {args.out}" if args.out else " (use --out to write STATUS.md)"))
    for name, checks in rows:
        hi = [k for k, v in checks.items() if v[0] == "HIGH"]
        if hi:
            print(f"  HIGH  {name}: {', '.join(hi)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
