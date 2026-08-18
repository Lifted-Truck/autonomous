#!/usr/bin/env python3
"""render_checklist — the K4 checklist as a page the human keeps open.

Same derivation as retrofit_checklist.py (nothing stored; the fleet is
re-read every run) plus the process facts that decide WHICH repo next: is a
resident mid-flight (branch/dirty), is it public (a leak-gate retrofit is a
security fix there), does it have a remote at all. Rendered to HTML so it can
be re-published to the same artifact URL and refreshed by re-running.

Usage:  render_checklist.py > checklist.html
"""
import datetime, html, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")


def git(p, *a):
    return subprocess.run(["git", "-C", p, *a], capture_output=True, text=True).stdout.strip()


def gather():
    rows = json.loads(subprocess.run(
        [sys.executable, os.path.join(HERE, "sweep", "sweep.py"),
         "--registry", os.path.join(ROOT, "registry.json"), "list"],
        capture_output=True, text=True, check=True).stdout)
    out = []
    for r in rows:
        if not r["status"].get("git"):
            continue
        p = r["path"]
        c = json.loads(subprocess.run(
            [sys.executable, os.path.join(HERE, "currency.py"), p, "--json"],
            capture_output=True, text=True).stdout or "{}")
        mpath = os.path.join(p, "project.manifest.json")
        try:
            m = json.load(open(mpath, encoding="utf-8")) if os.path.isfile(mpath) else {}
        except ValueError:
            m = {}
        dormant = isinstance(m.get("dormant"), dict) and bool(m["dormant"].get("review_by"))
        base = [b for b in c.get("behind", []) if b["version"] == "2.0.0"]
        missing = base[0]["missing"] if base else []
        if dormant:
            grp = "DORMANT"
        elif c.get("current") and not c.get("declared_but_missing"):
            grp = "DONE"
        elif not missing:
            grp = "DECLARE"
        elif len(missing) <= 3:
            grp = "LIGHT"
        else:
            grp = "FULL"
        head = git(p, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD").rsplit("/", 1)[-1] or "main"
        branch = git(p, "rev-parse", "--abbrev-ref", "HEAD")
        dirty = bool(git(p, "status", "--porcelain"))
        remote = r["status"].get("remote")
        vis = None
        if remote:
            slug = remote.replace("https://github.com/", "").replace("git@github.com:", "").replace(".git", "")
            vis = subprocess.run(["gh", "repo", "view", slug, "--json", "visibility", "-q", ".visibility"],
                                 capture_output=True, text=True).stdout.strip() or None
        out.append(dict(name=r["name"], group=grp, missing=missing, branch=branch,
                        default=head, dirty=dirty, remote=bool(remote), visibility=vis))
    return out


def pending():
    """What is waiting on the HUMAN specifically — derived, never typed. Two
    classes, because they have different owners:

      staged   an edit exists in that repo's tree that nobody has committed.
               Batch-applied kit changes land here: writes stay home, so the
               script never commits in a repo it does not reside in.
      unpushed commits exist that the remote has not seen. Pushes are the
               human's by charter, so these accumulate until they act.
    """
    rows = json.loads(subprocess.run(
        [sys.executable, os.path.join(HERE, "sweep", "sweep.py"),
         "--registry", os.path.join(ROOT, "registry.json"), "list"],
        capture_output=True, text=True, check=True).stdout)
    sys.path.insert(0, HERE)
    import kit_sync
    staged, unpushed, unwired, missing = [], [], [], []
    for r in rows:
        if not r["status"].get("git"):
            continue
        p = r["path"]
        if git(p, "diff", "--name-only", "--", "verify"):
            staged.append(r["name"])
        n = git(p, "rev-list", "--count", "@{u}..HEAD")
        if n.isdigit() and int(n):
            unpushed.append((r["name"], int(n)))
        # Vendoring has TWO states that both look fine from a distance: files
        # present, and files reachable. A repo can carry a checksum-perfect
        # gate its ./verify never sources and be completely ungated, which is
        # the declared-vs-effective trap wearing a new costume.
        st = kit_sync.check(p)[0]
        vp = os.path.join(p, "verify")
        has_verify = os.path.isfile(vp) and os.access(vp, os.X_OK)
        if st == "current" and has_verify:
            with open(vp, encoding="utf-8", errors="ignore") as fh:
                if ".kit/kit-gates.sh" not in fh.read():
                    unwired.append(r["name"])
        elif st == "absent" and has_verify:
            missing.append(r["name"])
    return {"staged": sorted(staged), "unpushed": sorted(unpushed),
            "unwired": sorted(unwired), "missing": sorted(missing)}


ORDER = ["DECLARE", "LIGHT", "FULL", "DONE", "DORMANT"]
LABEL = {
    "DECLARE": ("Declare", "Zero baseline gaps. /retrofit writes kit_version and the ## Mailbox section, then reads “nothing to do”. Two minutes each."),
    "LIGHT":   ("Light", "One to three gaps — mostly the leak gate in ./verify or a CI workflow. Under an hour each."),
    "FULL":    ("Full", "Four or more gaps. The real procedure: gap survey, inferred manifest, the architecture-rung question, plan-then-pause for your approval."),
    "DONE":    ("Done", "Declares the current kit version and passes its own currency check."),
    "DORMANT": ("Dormant", "Declared dormant with a review date. Off the list until it wakes or the date passes (Decision 55)."),
}


def _todo_html(t):
    out = []
    if t["unwired"]:
        out.append('<h4>1 · Carrying the gate but not sourcing it — UNGATED</h4>'
                   '<p>These repos have a checksum-perfect <code>.kit/kit-gates.sh</code> that their '
                   '<code>./verify</code> never sources, so the leak gate does not run at all. '
                   '"Files installed" and "protection installed" are different facts and this page '
                   'now reports them separately — a sampled probe found one of these silent on a '
                   'planted identity path.</p><ul>'
                   + "".join(f'<li><code>{html.escape(n)}</code></li>' for n in t["unwired"])
                   + '</ul><p>Fix: <code>migrate_to_vendored.py . --apply</code>, or where it refuses, '
                   'add <code>. .kit/kit-gates.sh</code> by hand per '
                   '<code>kit/templates/verify.project</code>.</p>')
    if t["missing"]:
        out.append(f'<h4>{len(out)+1} · Has a ./verify but no vendored gate at all</h4>'
                   '<p>Never synced, or synced and then lost. One of these filed a check-in claiming '
                   '<code>current</code> while its <code>.kit/</code> does not exist — which is the '
                   'case the verification step exists to catch.</p><ul>'
                   + "".join(f'<li><code>{html.escape(n)}</code></li>' for n in t["missing"])
                   + '</ul><p>Fix: <code>kit_sync.py .</code> then wire it.</p>')
    if t["staged"]:
        out.append(f'<h4>{len(out)+1} · Uncommitted change to a repo\'s ./verify</h4>'
                   '<p>Left in the tree by a kit update or a migration; nothing is ever committed '
                   'in a repo whose residents are not us. Where the repo has since been migrated to '
                   'vendored gates, the older 2.3.0 patch is <em>subsumed</em> — the migration deletes '
                   'the block it patched, so only the migration diff is worth reading.</p><ul>'
                   + "".join(f'<li><code>{html.escape(n)}</code></li>' for n in t["staged"])
                   + '</ul><p>Per repo: <code>git diff verify</code>, then commit. '
                   'Repos with a live session may prefer to commit it themselves.</p>')
    if t["unpushed"]:
        # Standing state, NOT a today-list: this accumulates because pushes are
        # the human's by charter, and most of it is other residents' own work,
        # not anything this session touched. Presented as a backlog with a
        # count so it cannot masquerade as an urgent queue.
        tot = sum(c for _, c in t["unpushed"])
        big = ", ".join(f"{html.escape(n)} ({c})" for n, c in
                        sorted(t["unpushed"], key=lambda x: -x[1])[:4])
        out.append(f'<h4>Standing backlog · {len(t["unpushed"])} repos hold {tot} unpushed commit(s)</h4>'
                   f'<p>Not a queue for today, and not all from this session — agents commit, '
                   f'you push, so this accrues. Largest: {big}. '
                   f'Full list: <code>python3 kit/render_checklist.py</code> or '
                   f'<code>governor/monitor.py</code>.</p>')
    if not out:
        out.append('<p class="none">Nothing waiting: every repo with a ./verify carries the '
                   'vendored gate AND sources it.</p>')
    return "".join(out)


def safety(x):
    """The one thing that decides 'can I run this now'."""
    if x["group"] in ("DONE", "DORMANT"):
        return ("", "")
    if not x["remote"]:
        return ("no remote", "warn")
    if x["dirty"]:
        return ("dirty tree — resident is mid-edit", "warn")
    if x["branch"] != x["default"]:
        return (f"on {x['branch']} — resident is mid-flight", "warn")
    return ("clean, on default — run any time", "ok")


def render(data, todo=None):
    todo = todo or {"staged": [], "unpushed": [], "unwired": [], "missing": []}
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total = len(data)
    settled = sum(1 for x in data if x["group"] in ("DONE", "DORMANT"))
    ready = sum(1 for x in data if x["group"] in ("DECLARE", "LIGHT", "FULL") and safety(x)[1] == "ok")
    public_gaps = sum(1 for x in data if x["visibility"] == "PUBLIC" and "verify wires leak_gate" in x["missing"])
    counts = {g: sum(1 for x in data if x["group"] == g) for g in ORDER}

    def esc(s): return html.escape(str(s))

    def group_table(g):
        items = sorted([x for x in data if x["group"] == g], key=lambda x: (safety(x)[1] != "ok", len(x["missing"]), x["name"]))
        if not items:
            return ""
        title, blurb = LABEL[g]
        rows = []
        for x in items:
            s_text, s_kind = safety(x)
            gaps = ", ".join(x["missing"]) if x["missing"] else "—"
            vis = x["visibility"] or ("local" if not x["remote"] else "?")
            rows.append(f"""<tr class="row-{s_kind or 'settled'}">
  <td class="chip-cell"><span class="chip chip-{g.lower()}">{esc(title)}</span></td>
  <td class="repo"><code>{esc(x['name'])}</code>{' <span class="vis vis-public">public</span>' if vis=='PUBLIC' else ''}</td>
  <td class="gaps">{esc(gaps)}</td>
  <td class="safety safety-{s_kind or 'settled'}">{esc(s_text)}</td>
</tr>""")
        return f"""<section class="group" id="{g.lower()}">
  <header><h2>{esc(title)} <span class="count">{len(items)}</span></h2><p>{esc(blurb)}</p></header>
  <div class="scroll"><table>
    <thead><tr><th>State</th><th>Repo</th><th>Still missing</th><th>Safe to run now?</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table></div>
</section>"""

    return f"""<title>Retrofit Ledger</title>
<style>
:root {{
  --bg:#F5F4EF; --panel:#FFFFFF; --ink:#1B1D22; --ink-2:#6B6F7A; --line:#DDDCD4;
  --accent:#0F6E68; --accent-ink:#0B4F4B;
  --ok:#2E7D4F; --ok-bg:#E6F2EA; --warn:#B36B00; --warn-bg:#FBF0DC; --bad:#9A2F2F; --bad-bg:#F8E4E4;
  --declare:#0F6E68; --light:#B36B00; --full:#9A2F2F; --done:#2E7D4F; --dormant:#6B6F7A;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg:#16181C; --panel:#1E2126; --ink:#E8E7E1; --ink-2:#9A9EA8; --line:#2E323A;
  --accent:#4FB3AC; --accent-ink:#7ED0C9;
  --ok:#5CB57E; --ok-bg:#1B2E23; --warn:#E0A03A; --warn-bg:#332A18; --bad:#E06B6B; --bad-bg:#3A1F1F;
  --declare:#4FB3AC; --light:#E0A03A; --full:#E06B6B; --done:#5CB57E; --dormant:#9A9EA8;
}} }}
:root[data-theme="dark"] {{
  --bg:#16181C; --panel:#1E2126; --ink:#E8E7E1; --ink-2:#9A9EA8; --line:#2E323A;
  --accent:#4FB3AC; --accent-ink:#7ED0C9;
  --ok:#5CB57E; --ok-bg:#1B2E23; --warn:#E0A03A; --warn-bg:#332A18; --bad:#E06B6B; --bad-bg:#3A1F1F;
  --declare:#4FB3AC; --light:#E0A03A; --full:#E06B6B; --done:#5CB57E; --dormant:#9A9EA8;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font:15px/1.5 var(--sans); }}
.wrap {{ max-width:1080px; margin:0 auto; padding:40px 24px 80px; }}
h1 {{ font-size:28px; letter-spacing:-.01em; margin:0 0 4px; text-wrap:balance; }}
.sub {{ color:var(--ink-2); margin:0 0 28px; font-size:14px; }}
.sub code {{ font:13px var(--mono); }}
.summary {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin:0 0 36px; }}
.stat {{ background:var(--panel); border:1px solid var(--line); padding:14px 16px; }}
.stat .n {{ font-size:30px; font-weight:600; font-variant-numeric:tabular-nums; line-height:1; color:var(--accent-ink); }}
.stat .n.warn {{ color:var(--warn); }}
.stat .l {{ font-size:11px; letter-spacing:.06em; text-transform:uppercase; color:var(--ink-2); margin-top:6px; }}
.how {{ background:var(--panel); border-left:3px solid var(--accent); padding:14px 18px; margin:0 0 36px; }}
.how h3 {{ margin:0 0 8px; font-size:13px; letter-spacing:.06em; text-transform:uppercase; color:var(--accent-ink); }}
.how ol {{ margin:0; padding-left:20px; }} .how li {{ margin:4px 0; }}
.how code {{ font:13px var(--mono); background:var(--bg); padding:1px 5px; }}
.group {{ margin:0 0 36px; }}
.group header {{ display:flex; align-items:baseline; gap:12px; flex-wrap:wrap; margin:0 0 10px; }}
.group h2 {{ font-size:19px; margin:0; }}
.group h2 .count {{ font:600 13px var(--mono); color:var(--ink-2); margin-left:6px; }}
.group header p {{ margin:0; color:var(--ink-2); font-size:14px; max-width:68ch; flex-basis:100%; }}
.scroll {{ overflow-x:auto; border:1px solid var(--line); background:var(--panel); }}
table {{ border-collapse:collapse; width:100%; min-width:720px; }}
th {{ text-align:left; font-size:11px; letter-spacing:.06em; text-transform:uppercase; color:var(--ink-2); padding:10px 12px; border-bottom:1px solid var(--line); font-weight:600; }}
td {{ padding:9px 12px; border-bottom:1px solid var(--line); vertical-align:top; }}
tr:last-child td {{ border-bottom:0; }}
.chip {{ display:inline-block; font:600 11px var(--mono); letter-spacing:.04em; text-transform:uppercase; padding:2px 8px; border:1px solid currentColor; }}
.chip-declare {{ color:var(--declare); }} .chip-light {{ color:var(--light); }} .chip-full {{ color:var(--full); }}
.chip-done {{ color:var(--done); }} .chip-dormant {{ color:var(--dormant); }}
.repo code {{ font:13px var(--mono); }}
.vis {{ font:600 10px var(--mono); letter-spacing:.06em; text-transform:uppercase; margin-left:8px; padding:1px 6px; }}
.vis-public {{ color:var(--bad); background:var(--bad-bg); }}
.gaps {{ color:var(--ink-2); font:12.5px var(--mono); }}
.safety {{ font-size:13px; }}
.safety-ok {{ color:var(--ok); }} .safety-warn {{ color:var(--warn); }}
.row-warn td.repo {{ opacity:.85; }}
.todo {{ background:var(--panel); border:1px solid var(--warn); border-left:3px solid var(--warn); padding:14px 18px; margin:0 0 24px; }}
.todo h3 {{ margin:0 0 10px; font-size:13px; letter-spacing:.06em; text-transform:uppercase; color:var(--warn); }}
.todo h4 {{ margin:12px 0 4px; font-size:13px; }}
.todo p {{ margin:4px 0 6px; color:var(--ink-2); font-size:13.5px; max-width:74ch; }}
.todo ul {{ margin:4px 0; padding-left:20px; }} .todo li {{ margin:2px 0; font-size:13.5px; }}
.todo code {{ font:12.5px var(--mono); background:var(--bg); padding:1px 5px; }}
.todo .none {{ color:var(--ok); }}
.foot {{ color:var(--ink-2); font-size:13px; border-top:1px solid var(--line); padding-top:16px; margin-top:8px; }}
</style>
<div class="wrap">
<h1>Retrofit Ledger</h1>
<p class="sub">Derived from the fleet at <code>{now}</code> · nothing here is stored — every row is re-read from the repo. Refresh: <code>python3 kit/render_checklist.py</code>, then republish.</p>

<div class="summary">
  <div class="stat"><div class="n">{settled}<span style="font-size:16px;color:var(--ink-2)"> / {total}</span></div><div class="l">settled (done + dormant)</div></div>
  <div class="stat"><div class="n">{counts['DECLARE']}</div><div class="l">declare — two minutes each</div></div>
  <div class="stat"><div class="n">{counts['LIGHT']}</div><div class="l">light — under an hour</div></div>
  <div class="stat"><div class="n">{counts['FULL']}</div><div class="l">full retrofit</div></div>
  <div class="stat"><div class="n">{ready}</div><div class="l">safe to run right now</div></div>
  <div class="stat"><div class="n warn">{public_gaps}</div><div class="l">public repos without a leak gate</div></div>
</div>

<div class="todo">
  <h3>Before you resume — {len(todo['unwired']) + len(todo['missing'])} repo(s) not actually protected</h3>
  {_todo_html(todo)}
</div>

<div class="how">
  <h3>How to work this list</h3>
  <ol>
    <li>Pick a row whose <b>Safe to run now?</b> is green. A yellow row has a resident mid-flight — do it from <em>that</em> session, or after they merge.</li>
    <li>Open a session in the repo and run <code>/retrofit</code>. It shows the currency delta, plans, and <b>pauses for your approval</b> before writing anything.</li>
    <li>It closes by re-running the checker and requiring <code>nothing to do</code>. Commit; the push is yours.</li>
    <li>Regenerate this page. The row moves to <b>Done</b> because the repo <em>reads</em> as done — no tick-box, no notice.</li>
  </ol>
</div>

{''.join(group_table(g) for g in ORDER)}

<p class="foot">Groups: <b>Declare</b> = zero gaps, only the version + Mailbox section · <b>Light</b> = 1–3 gaps · <b>Full</b> = 4+ gaps, real survey. Public repos missing the leak gate are flagged because for them the retrofit is a security fix, not housekeeping. Source: <code>kit/retrofit_checklist.py</code>, <code>kit/currency.py</code>.</p>
</div>
"""


if __name__ == "__main__":
    sys.stdout.write(render(gather(), pending()))
