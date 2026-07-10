# claude-code-best-practices (the `claude-optimization` kit)

> **Note on this file.** This is the CLAUDE.md for the *kit itself* — the maintainer's
> guide. It is deliberately **verbose**, because editing the kit is meta-work and the
> reasoning behind each piece matters. This is the opposite of the advice the kit
> *ships* (`templates/CLAUDE.root.md` tells consumers to keep their root lean). Don't
> "fix" this file to be terse — the verbosity is intentional and scoped to maintainers.

## What this project is

A reusable scaffolding kit that operationalizes the Anthropic article
[_How Claude Code works in large codebases_](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start).
You run a bootstrap script and it drops a pre-wired Claude Code harness (CLAUDE.md,
hooks, skills, subagent, MCP config, `.claudeignore`, code map) into any target repo.

The kit is **not** itself a Claude Code harness for a product — it is a *factory* that
stamps harnesses into other repos. Keep that distinction in mind: there are two
audiences for the files here.

1. **Maintainers** (you, editing this kit) → guided by *this* CLAUDE.md.
2. **Consumers** (a repo that got bootstrapped) → guided by the files under
   `templates/`, which are written in the consumer's voice.

## Repository layout

```
claude-optimization/
├── CLAUDE.md            ← this file (maintainer guide; verbose on purpose)
├── README.md            ← consumer-facing overview + quick start
├── bootstrap.ps1        ← Windows/PowerShell installer
├── bootstrap.sh         ← macOS/Linux/Git-Bash installer (must stay in sync with .ps1)
├── docs/
│   ├── INSIGHTS.md      ← article distilled → table mapping each insight to its file
│   ├── CHECKLIST.md     ← the 10-step rollout, trackable
│   └── GOVERNANCE.md    ← DRI, approved-skills register, review-log template
└── templates/           ← EVERYTHING the bootstrap copies into a target repo
    ├── CLAUDE.root.md   ← becomes the target's root CLAUDE.md  (SUBSTITUTED)
    ├── CLAUDE.subdir.md ← per-directory CLAUDE.md template      (SUBSTITUTED)
    ├── CODEMAP.md       ← lightweight table of contents          (SUBSTITUTED)
    ├── .claudeignore    ← exclusion rules                        (copied as-is)
    └── claude/          ← becomes the target's .claude/ dir (plus .mcp.json → repo root)
        ├── settings.json                  ← hook registrations   (SUBSTITUTED)
        ├── .mcp.json                      ← MCP servers; deploys to TARGET ROOT, not .claude/
        ├── hooks/
        │   ├── format-lint.{sh,ps1}            ← PostToolUse: format/lint edited file
        │   ├── session-start-context.{sh,ps1} ← SessionStart: inject CODEMAP into context
        │   └── stop-capture-learnings.{sh,ps1}← Stop: opt-in capture reminder
        ├── skills/example-domain/SKILL.md ← path-scoped skill template
        └── agents/codebase-mapper.md      ← read-only mapper subagent
```

## How the bootstrap works (mental model)

Both `bootstrap.ps1` and `bootstrap.sh` do the same four things. They are a
**copy-and-substitute installer** — no source code in the target is touched.

1. **Detect project type** from a marker file in the target:
   `package.json`→node · `pyproject.toml`/`requirements.txt`→python · `Cargo.toml`→rust ·
   `go.mod`→go · `*.sln`/`*.csproj`→dotnet · `CMakeLists.txt`→cpp · else `unknown`.
   This sets `TEST_CMD`, `LINT_CMD`, `FORMAT_CMD` defaults.
2. **Build hook command strings** for the chosen `--shell` (`pwsh` → `pwsh -NoProfile
   -File .claude/hooks/<n>.ps1`; `sh` → `bash .claude/hooks/<n>.sh`).
3. **Deploy** each template to its destination, **substituting placeholders** in the
   files marked SUBSTITUTED above.
4. **Report** what was written/skipped, then print next steps.

### Behavioral guarantees (don't break these when editing)

- **Non-destructive by default.** A destination that already exists is **skipped**
  unless `-Force`/`--force`. This is what makes re-running safe.
- **`-DryRun`/`--dry-run` writes nothing** — it only prints the plan.
- **Idempotent.** Running twice changes nothing the second time (verified in tests).
- The two scripts must stay **feature-equivalent**. If you change detection, the
  placeholder set, or the deploy list in one, mirror it in the other.

### The placeholder contract

Templates use `{{DOUBLE_BRACE}}` tokens. The full set, substituted by both scripts:

| Token | Filled with |
|-------|-------------|
| `{{PROJECT_NAME}}` | `-ProjectName`, else the target folder's leaf name |
| `{{PROJECT_TYPE}}` | detected type (node/python/…/unknown) |
| `{{TEST_CMD}}` `{{LINT_CMD}}` `{{FORMAT_CMD}}` | per-type defaults |
| `{{FORMAT_LINT_HOOK}}` `{{SESSION_START_HOOK}}` `{{STOP_HOOK}}` | shell-specific hook command strings |

**If you add a new placeholder**, you must update it in BOTH scripts: the `$subs`
hashtable in `bootstrap.ps1` and the `subst()` sed block in `bootstrap.sh`. A token
left unfilled ships literally (e.g. `{{FOO}}`) into the consumer's repo — that's the
failure mode to watch for.

### The deploy list

The mapping of `templates/...` → `target/...` lives in two places:
- `bootstrap.ps1`: the `Deploy <src> <dst> <substitute>` calls near the bottom.
- `bootstrap.sh`: the `deploy <src> <dst> <substitute>` calls near the bottom.

Two destinations are **not** a 1:1 path mirror — note them:
- `templates/claude/.mcp.json` → **`<target>/.mcp.json`** (repo root, because that's
  where Claude Code reads project MCP config — NOT `.claude/.mcp.json`).
- `templates/CLAUDE.subdir.md` → **`<target>/.claude/templates/CLAUDE.subdir.md`**
  (it's a reference the consumer copies into subdirs later, not an active file).

Hooks deploy only the variant matching `--shell` (`.ps1` for pwsh, `.sh` for sh). The
`.sh` variants get `chmod +x` by the bash installer.

## Common maintainer tasks

- **Add a new template file the bootstrap should install:** put it under `templates/`,
  then add a `Deploy`/`deploy` line in BOTH scripts (decide substitute yes/no).
- **Support a new language:** add a branch to the detection `if/elseif` chain in BOTH
  scripts, and add the file-extension case to BOTH `format-lint` hooks.
- **Change a hook's behavior:** edit the `.sh` AND `.ps1` versions together; they must
  behave identically. Hooks must always `exit 0` (never block Claude's edits).
- **Re-test after any change:** see "Verifying changes" below.

## Conventions

- Markdown wraps at ~90 cols; tables for any insight→artifact mapping.
- Template files speak in the **consumer's** voice and are full of `_replace me_`
  prompts on purpose — resist the urge to make them concrete; specificity is the
  consumer's job.
- Keep `docs/INSIGHTS.md` as the canonical article↔artifact map. If you add an
  artifact, add its row there too.
- Everything is plain PowerShell + POSIX sh + Markdown + JSON. No build step, no
  dependencies, nothing to compile.

## Gotchas

- **Two scripts, one behavior.** The #1 way to break this kit is editing one installer
  and forgetting the other. Detection, placeholders, and the deploy list all live in
  both.
- **`.mcp.json` destination is the repo root**, not `.claude/`. Easy to get wrong.
- **JSON templates must stay valid after substitution.** `settings.json` is
  substituted; the hook command strings contain no quotes/backslashes, so they're
  JSON-safe — keep it that way (forward slashes in hook paths, even on Windows).
- **The Stop hook is intentionally a no-op by default** (opt-in via
  `CLAUDE_CAPTURE_REMINDER=1`). A deterministic hook can't read the session to truly
  "propose" CLAUDE.md edits, so it's an honest reminder, not theater. Don't
  reimplement it as if it could analyze the conversation.
- **`templates/.claudeignore` and `templates/claude/.mcp.json` are real dotfiles in
  this repo.** Make sure git actually tracks them (the kit's own `.gitignore` must not
  exclude them).

## Verifying changes

There are no unit tests; verification is a dry-run + real-run against a throwaway
target. From the kit root (PowerShell):

```powershell
$t = Join-Path $env:TEMP 'co-test'; Remove-Item $t -Recurse -Force -EA SilentlyContinue
New-Item -ItemType Directory -Force $t | Out-Null
'{ "name": "demo" }' | Set-Content (Join-Path $t 'package.json')   # fake a node repo
.\bootstrap.ps1 -TargetPath $t -DryRun     # 1. preview — writes nothing
.\bootstrap.ps1 -TargetPath $t             # 2. real run
.\bootstrap.ps1 -TargetPath $t             # 3. re-run → everything should "skip"
Get-Content "$t\.claude\settings.json" -Raw | ConvertFrom-Json   # 4. JSON still valid?
Get-ChildItem $t -Recurse -Force | Where-Object { -not $_.PSIsContainer }
Remove-Item $t -Recurse -Force
```

Check that: detection prints the right type, placeholders are all filled (grep the
output for any literal `{{`), and the re-run reports only skips.

## Commands

There is nothing to build, lint, or test in the traditional sense. The "test" is the
verification recipe above. Project type of this repo itself: docs + scripts (no
package manager).

## Remote

GitHub: <https://github.com/Lifted-Truck/claude-code-best-practices>
