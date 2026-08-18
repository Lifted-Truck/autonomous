#!/usr/bin/env python3
"""render_checklist — the K4 checklist as a page the human keeps open.

Same derivation as retrofit_checklist.py (nothing stored; the fleet is
re-read every run) plus the process facts that decide WHICH repo next: is a
resident mid-flight (branch/dirty), is it public (a leak-gate retrofit is a
security fix there), does it have a remote at all. Rendered to HTML so it can
be re-published to the same artifact URL and refreshed by re-running.

Usage:  render_checklist.py > checklist.html
"""
import datetime, html, json, os, re, subprocess, sys

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
        elif c.get("current"):
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
            "unwired": sorted(unwired), "missing": sorted(missing),
            "prs": open_prs()}


def open_prs():
    """PRs awaiting the human's merge. One search per OWNER, not per repo.

    Decision 66 moved the human's queue from `git push` to `gh pr merge`, so
    this is now the action list rather than a backlog note. Best-effort: no
    network, no gh, or no auth returns an empty list rather than failing the
    page — a ledger that will not render because GitHub is down is worse than
    one missing a section, and the section says when it could not look.
    """
    owners, out = set(), []
    rows = json.loads(subprocess.run(
        [sys.executable, os.path.join(HERE, "sweep", "sweep.py"),
         "--registry", os.path.join(ROOT, "registry.json"), "list"],
        capture_output=True, text=True, check=True).stdout)
    for r in rows:
        remote = (r["status"] or {}).get("remote") or ""
        m = re.search(r"github\.com[:/]([^/]+)/", remote)
        if m:
            owners.add(m.group(1))
    for o in sorted(owners):
        try:
            raw = subprocess.run(
                ["gh", "search", "prs", "--owner", o, "--state", "open", "--limit", "60",
                 "--json", "repository,number,title,url"],
                capture_output=True, text=True, timeout=45).stdout
            for pr in json.loads(raw or "[]"):
                out.append({"repo": pr["repository"]["name"], "number": pr["number"],
                            "title": pr["title"], "url": pr["url"]})
        except Exception:
            continue
    return sorted(out, key=lambda x: (x["repo"], x["number"]))


_PLANT_PATH = "/" + "Users" + "/somebody/private"   # assembled: this gate greps itself

WIRE_PROMPT = """From the autonomous resident, 2026-08-18 (Decision 65). Your repo carries the
vendored kit gates at .kit/kit-gates.sh but your ./verify never sources them,
so the leak gate does not run at all — you are ungated right now. You have no
leak_gate of your own to migrate, so this is added by hand, not by the script.

1. In ./verify, after HARNESS_DIR is set, add:

   if [ -r .kit/kit-gates.sh ]; then
     . .kit/kit-gates.sh
   else
     echo "verify: .kit/kit-gates.sh missing - run kit_sync.py" >&2
     exit 1
   fi

   A missing .kit/ must be a hard exit, never a degraded run.

2. In fast(), alongside your existing checks:
     kit_integrity || ok=1
     leak_gate     || ok=1
   Keep every project gate you already have; they are yours.

3. Prove all three, because they come apart:
   - ./verify fast is green
   - grep -c 'kit/kit-gates.sh' verify   is >= 1
   - it FIRES:
       printf 'x {plant}\\n' > audit-plant.md
       ./verify fast 2>&1 | grep audit-plant.md    # must print a hit
       rm audit-plant.md

   In your check-in, SAY the gate fired - do not quote the planted path; a
   notice quoting it trips the leak gate in the public repo it lands in.

Finish with a PR, not a commit left on main:
   git switch -c chore/wire-kit-gates
   git push -u origin HEAD && gh pr create --fill
Put the evidence in the PR body. Do NOT merge - merges are the human's.
No remote? Commit on main and say so. Then check in:
   python3 ~/Documents/Claude/autonomous/kit/kit_sync.py . --notify
""".replace("{plant}", _PLANT_PATH)

RETROFIT_PROMPT = """From the autonomous resident, 2026-08-18. Please bring this repo up to the
current kit version:

   /retrofit

It runs kit/currency.py first, shows you the exact delta, and PAUSES for
approval before writing anything. Gate code is vendored now, never copied -
step 4b runs kit_sync.py and thins ./verify. Finish on a branch with a PR
(git push -u origin HEAD && gh pr create --fill) rather than a commit left on
main - do NOT merge, that is the human's. Then check in with
kit_sync.py . --notify so autonomous can verify against your tree.

It also TIDIES the tree it finds (step 4c): kit-owned leftovers get staged
into its PR, an untracked .kit/ gets added, stranded commits on main move onto
the branch, stray probe plants are deleted. Project work in progress is left
alone and named in the report, never absorbed. You should not have to
reconcile repo state by hand.
"""


def actions(data, todo):
    """What the HUMAN does next, ordered by consequence — not by repo class.

    The page used to be organised the way the fleet is organised, which is the
    resident's mental model, not the human's. A human has exactly three kinds
    of move: relay a prompt to a repo's session, run something themselves, or
    wait. Everything else is reference.
    """
    by = {x["name"]: x for x in data}
    out = []
    if todo["unwired"] or todo["missing"]:
        repos = sorted(set(todo["unwired"]) | set(todo["missing"]))
        out.append({
            "kind": "relay", "urgency": "now",
            "title": "Wire the leak gate in these repos — they are ungated",
            "why": ("They carry a checksum-perfect copy of the gate that their ./verify "
                    "never sources, so nothing runs. A sampled probe caught one silent on "
                    "a planted identity path. Neither has a gate of its own to migrate, so "
                    "this is hand-wiring, not a script."),
            "repos": repos, "payload": WIRE_PROMPT})
    ready = [x for x in data if x["group"] == "DECLARE" and safety(x)[1] == "ok"]
    if ready:
        out.append({
            "kind": "relay", "urgency": "quick",
            "title": "Run /retrofit — zero gaps, about two minutes each",
            "why": ("These have every baseline item already. The retrofit writes the kit "
                    "version and the Mailbox section, vendors the gates, and stops."),
            "repos": sorted(x["name"] for x in ready), "payload": RETROFIT_PROMPT})
    if todo["staged"]:
        out.append({
            "kind": "run", "urgency": "whenever",
            "title": "Review and commit an uncommitted ./verify change",
            "why": ("Left by a kit update. Nothing is ever committed in a repo whose "
                    "residents are not us. Where the repo has since been migrated, the "
                    "older patch is subsumed — only the migration diff is worth reading."),
            "repos": todo["staged"],
            "payload": "\n".join(f"cd ~/Documents/Claude/{n} && git diff verify"
                                  for n in todo["staged"])})
    rest = [x for x in data if x["group"] in ("LIGHT", "FULL") and safety(x)[1] == "ok"]
    if rest:
        out.append({
            "kind": "relay", "urgency": "bulk",
            "title": "Run /retrofit — real gaps, longer sessions",
            "why": ("Each needs a survey and your approval on the architecture rung. "
                    "Work them in any order; the ones marked public are a security fix "
                    "rather than housekeeping."),
            "repos": sorted(x["name"] for x in rest), "payload": RETROFIT_PROMPT})
    waiting = sorted(x["name"] for x in data
                     if x["group"] in ("DECLARE", "LIGHT", "FULL") and safety(x)[1] == "warn")
    if waiting:
        out.append({
            "kind": "wait", "urgency": "none",
            "title": "Nothing to do — a resident is mid-flight",
            "why": ("Dirty tree or a working branch. Ask that session to run /retrofit "
                    "when it lands, or wait. Reaching in is what buries work."),
            "repos": waiting, "payload": None})
    if todo.get("prs"):
        out.append({
            "kind": "run", "urgency": "review",
            "title": f"Review and merge {len(todo['prs'])} open PR(s)",
            "why": ("Merging is yours and always was. Each PR carries its own evidence in "
                    "the body — that is the review surface a bare commit never had."),
            "repos": [f"{p['repo']}#{p['number']}" for p in todo["prs"]],
            "payload": "\n".join(f"gh pr view {p['url']}   # {p['title'][:60]}"
                                  for p in todo["prs"])})
    if todo["unpushed"]:
        tot = sum(c for _, c in todo["unpushed"])
        out.append({
            "kind": "relay", "urgency": "backlog",
            "title": f"Ask for a PR — {tot} commits sit on main in {len(todo['unpushed'])} repos",
            "why": ("These predate Decision 66, when sessions stopped at a local commit and "
                    "left you to find and push each one. Ask each session to move its work "
                    "onto a branch and open a PR; pushing them yourself works too, but then "
                    "you are pushing code you have not reviewed, which is the half of the "
                    "problem that was worse than the keystrokes."),
            "repos": [f"{n} ({c})" for n, c in sorted(todo["unpushed"], key=lambda t: -t[1])],
            "payload": ("From the autonomous resident, 2026-08-18 (Decision 66). You have "
                        "commits on main that were never pushed. Please move them onto a "
                        "branch and open a PR instead:\n\n"
                        "  git switch -c chore/<slug>\n"
                        "  git push -u origin HEAD && gh pr create --fill\n\n"
                        "Put the evidence in the PR body. Do NOT merge - merges are the "
                        "human's. If the repo has no remote, say so and leave it committed.")})
    return out


ORDER = ["DECLARE", "LIGHT", "FULL", "DONE", "DORMANT"]
LABEL = {
    "DECLARE": ("Declare", "Zero baseline gaps; only a later entry's requirement is unmet. Small, scoped work — usually one file."),
    "LIGHT":   ("Light", "One to three gaps — mostly the leak gate in ./verify or a CI workflow. Under an hour each."),
    "FULL":    ("Full", "Four or more gaps. The real procedure: gap survey, inferred manifest, the architecture-rung question, plan-then-pause for your approval."),
    "DONE":    ("Done", "Declares the current kit version and passes its own currency check."),
    "DORMANT": ("Dormant", "Declared dormant with a review date. Off the list until it wakes or the date passes (Decision 55)."),
}


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


def _actions_html(acts):
    kinds = {"relay": ("Relay", "Paste into that repo's Claude session"),
             "run": ("You", "Run in your terminal"),
             "wait": ("Wait", "No action — a resident holds it")}
    cards = []
    for i, a in enumerate(acts, 1):
        label, hint = kinds[a["kind"]]
        repos = "".join(f"<code>{html.escape(r)}</code>" for r in a["repos"])
        pay = ""
        if a["payload"]:
            pid = f"p{i}"
            pay = (f'<div class="copywrap"><button class="copy" data-t="{pid}">Copy</button>'
                   f'<pre id="{pid}">{html.escape(a["payload"])}</pre></div>')
        cards.append(f"""<article class="act act-{a['kind']}">
  <header><span class="kind kind-{a['kind']}">{label}</span>
    <h3>{i}. {html.escape(a['title'])}</h3></header>
  <p class="hint">{hint} · {len(a['repos'])} repo(s)</p>
  <p class="why">{html.escape(a['why'])}</p>
  <div class="repos">{repos}</div>
  {pay}
</article>""")
    return "".join(cards)


def render(data, todo=None):
    todo = todo or {"staged": [], "unpushed": [], "unwired": [], "missing": []}
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    acts = actions(data, todo)
    n_relay = sum(1 for a in acts if a["kind"] == "relay")
    n_run = sum(1 for a in acts if a["kind"] == "run")
    n_wait = sum(1 for a in acts if a["kind"] == "wait")
    n_ungated = len(todo["unwired"]) + len(todo["missing"])
    # An ungated repo is the only number here that is a live risk rather than a
    # queue depth; colour it as such and let zero read as calm.
    warnungated = " warn" if n_ungated else ""
    warnrelay = " warn" if any(a["urgency"] == "now" for a in acts) else ""
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
.secttl {{ font-size:13px; letter-spacing:.08em; text-transform:uppercase; color:var(--ink-2);
  margin:34px 0 4px; padding-bottom:8px; border-bottom:1px solid var(--line); }}
.sectsub {{ color:var(--ink-2); font-size:13.5px; max-width:74ch; margin:0 0 20px; }}
.act {{ background:var(--panel); border:1px solid var(--line); border-left:3px solid var(--line);
  padding:16px 18px; margin:0 0 14px; }}
.act-relay {{ border-left-color:var(--accent); }}
.act-run {{ border-left-color:var(--warn); }}
.act-wait {{ border-left-color:var(--line); opacity:.8; }}
.act header {{ display:flex; align-items:baseline; gap:10px; flex-wrap:wrap; }}
.act h3 {{ font-size:16.5px; margin:0; text-wrap:balance; }}
.kind {{ font:600 10px var(--mono); letter-spacing:.08em; text-transform:uppercase;
  padding:3px 8px; border:1px solid currentColor; white-space:nowrap; }}
.kind-relay {{ color:var(--accent); }} .kind-run {{ color:var(--warn); }} .kind-wait {{ color:var(--ink-2); }}
.hint {{ margin:6px 0 0; font:600 11px var(--mono); letter-spacing:.04em; color:var(--ink-2);
  text-transform:uppercase; }}
.why {{ margin:8px 0 10px; font-size:14px; color:var(--ink); max-width:76ch; }}
.repos {{ display:flex; flex-wrap:wrap; gap:6px; margin:0 0 10px; }}
.repos code {{ font:12px var(--mono); background:var(--bg); border:1px solid var(--line);
  padding:2px 7px; }}
.copywrap {{ position:relative; }}
.copywrap pre {{ margin:0; padding:14px 16px; background:var(--bg); border:1px solid var(--line);
  overflow-x:auto; font:12.5px/1.55 var(--mono); white-space:pre; }}
button.copy {{ position:absolute; top:8px; right:8px; font:600 10px var(--mono);
  letter-spacing:.06em; text-transform:uppercase; padding:5px 10px; cursor:pointer;
  color:var(--accent); background:var(--panel); border:1px solid var(--accent); }}
button.copy:hover, button.copy:focus-visible {{ background:var(--accent); color:var(--panel); }}
button.copy:focus-visible {{ outline:2px solid var(--accent-ink); outline-offset:2px; }}
.foot {{ color:var(--ink-2); font-size:13px; border-top:1px solid var(--line); padding-top:16px; margin-top:8px; }}
</style>
<div class="wrap">
<h1>Retrofit Ledger</h1>
<p class="sub">Derived from the fleet at <code>{now}</code> · nothing here is stored — every row is re-read from the repo. Refresh: <code>python3 kit/render_checklist.py</code>, then republish.</p>

<div class="summary">
  <div class="stat"><div class="n{warnrelay}">{n_relay}</div><div class="l">to relay to a session</div></div>
  <div class="stat"><div class="n">{n_run}</div><div class="l">for you to run</div></div>
  <div class="stat"><div class="n">{n_wait}</div><div class="l">waiting on a resident</div></div>
  <div class="stat"><div class="n{warnungated}">{n_ungated}</div><div class="l">ungated right now</div></div>
</div>

<h2 class="secttl">What to do next</h2>
<p class="sectsub">In order. Each card says who acts — you, or a repo's session — and gives the exact text. Nothing here is stored; re-running the generator re-reads every repo.</p>
{_actions_html(acts)}

<h2 class="secttl">Reference — full fleet state</h2>
<p class="sectsub">The same repos, grouped by how much work a retrofit is. You should not need this to act; it is here to answer "why is that repo in that list".</p>

<div class="summary">
  <div class="stat"><div class="n">{settled}<span style="font-size:16px;color:var(--ink-2)"> / {total}</span></div><div class="l">settled (done + dormant)</div></div>
  <div class="stat"><div class="n">{counts['DECLARE']}</div><div class="l">declare — two minutes each</div></div>
  <div class="stat"><div class="n">{counts['LIGHT']}</div><div class="l">light — under an hour</div></div>
  <div class="stat"><div class="n">{counts['FULL']}</div><div class="l">full retrofit</div></div>
  <div class="stat"><div class="n warn">{public_gaps}</div><div class="l">public repos without a leak gate</div></div>
</div>

{''.join(group_table(g) for g in ORDER)}

<script>
document.querySelectorAll("button.copy").forEach(function (b) {{
  b.addEventListener("click", function () {{
    var el = document.getElementById(b.dataset.t);
    navigator.clipboard.writeText(el.textContent).then(function () {{
      var was = b.textContent; b.textContent = "Copied";
      setTimeout(function () {{ b.textContent = was; }}, 1400);
    }});
  }});
}});
</script>
<p class="foot">Groups: <b>Declare</b> = zero gaps, only the version + Mailbox section · <b>Light</b> = 1–3 gaps · <b>Full</b> = 4+ gaps, real survey. Public repos missing the leak gate are flagged because for them the retrofit is a security fix, not housekeeping. Source: <code>kit/retrofit_checklist.py</code>, <code>kit/currency.py</code>.</p>
</div>
"""


if __name__ == "__main__":
    sys.stdout.write(render(gather(), pending()))
