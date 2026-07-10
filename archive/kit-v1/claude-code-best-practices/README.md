# claude-optimization

A reusable scaffolding kit that operationalizes [_How Claude Code works in large
codebases_](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start).

The article's core claim: **the harness determines how Claude Code performs more
than the model alone.** This kit is that harness, packaged so you can drop it into
any repo in one command and tune from there.

## What's in the box

```
claude-optimization/
├── README.md                  ← you are here
├── bootstrap.ps1              ← Windows / PowerShell installer
├── bootstrap.sh               ← macOS / Linux / Git-Bash installer
├── docs/
│   ├── INSIGHTS.md            ← the article distilled → mapped to each artifact
│   ├── CHECKLIST.md           ← the 10-step getting-started checklist, trackable
│   └── GOVERNANCE.md          ← DRI, review cadence, approved-skills register
└── templates/                 ← everything the bootstrap copies into a target repo
    ├── CLAUDE.root.md         ← lean top-level CLAUDE.md (pointers + gotchas only)
    ├── CLAUDE.subdir.md       ← per-directory CLAUDE.md (local conventions)
    ├── CODEMAP.md             ← lightweight markdown table of contents
    ├── .claudeignore          ← version-controlled exclusion rules
    └── claude/                ← becomes the repo's .claude/ directory
        ├── settings.json      ← hooks wired up (format/lint, session-start, stop)
        ├── hooks/             ← .sh and .ps1 versions of each hook
        ├── skills/            ← path-scoped skill template (progressive disclosure)
        ├── agents/            ← read-only codebase-mapper subagent
        └── .mcp.json          ← MCP server config template
```

## Quick start

Operationalize the current repo (run from inside the kit):

```powershell
# Windows
.\bootstrap.ps1 -TargetPath C:\path\to\your\repo

# macOS / Linux
./bootstrap.sh /path/to/your/repo
```

The bootstrap is **non-destructive** — it skips any file that already exists unless
you pass `-Force` / `--force`. Run with `-DryRun` / `--dry-run` first to see exactly
what it would create.

It auto-detects project type (node, python, rust, go, dotnet, cpp) and fills in test,
lint, and format commands. Everything it writes is a starting point — open each file
and tighten it to the actual repo.

## After bootstrapping

1. Edit the generated `CLAUDE.md` — strip anything generic, keep only pointers and
   gotchas. See [docs/INSIGHTS.md](docs/INSIGHTS.md) for the "why".
2. Fill in `CODEMAP.md` with the real top-level structure.
3. Work through [docs/CHECKLIST.md](docs/CHECKLIST.md).
4. Assign an owner using [docs/GOVERNANCE.md](docs/GOVERNANCE.md).

## Maintaining the kit itself

Re-review every 3–6 months as models improve (the article's cadence). When a new
model resolves a limitation, delete the CLAUDE.md constraint that compensated for it
— here in the templates, so every future bootstrap inherits the fix.
