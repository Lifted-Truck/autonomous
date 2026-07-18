# Installing the doctrine on a machine

How to wire a machine's global `~/.claude/CLAUDE.md` to this repo's canonical
doctrine. First installed 2026-07-10. Replicate on any other
machine in two steps.

## 1. Clone the repo to the same path

```bash
git clone https://github.com/Lifted-Truck/autonomous.git ~/Documents/Claude/autonomous
```

The `@` imports below use this absolute location. If you must clone elsewhere,
adjust the import paths to match.

## 2. Add this block to `~/.claude/CLAUDE.md`

Paste verbatim (this is exactly the block installed on the first machine).
Put it at the top, before any machine-local sections:

```markdown
## Canonical infrastructure (single source)

All cross-project doctrine, the harness kit, memory loops, and the governor
live in **`~/Documents/Claude/autonomous/`** (github.com/Lifted-Truck/autonomous).
That repo is the canonical home; propose doctrine changes there (versioned,
reviewable), never by editing this file. The doctrine below is imported and
auto-loaded every session. (INTEGRATIONS.md is deliberately NOT auto-loaded —
context budget; its doctrine tenet says to read it at the start of any
cross-repo work.)

@~/Documents/Claude/autonomous/doctrine/DOCTRINE.md
```

## 3. Install the commands

```bash
mkdir -p ~/.claude/commands
cp ~/Documents/Claude/autonomous/kit/commands/*.md ~/.claude/commands/
```

Canonical copies: `kit/commands/` (re-copy after pulling changes). Gives
every session `/spinup [path —] <what it is>` (survey-first NEW-project
procedure) and `/retrofit [path]` (gap-survey catch-up for EXISTING repos);
with no path both target the current working directory (the Claude Code
Desktop open-in-folder case).

## 4. Verify

Start a fresh Claude Code session anywhere and ask what the development
doctrine says about (e.g.) the AI/deterministic boundary. If the answer
reflects [DOCTRINE.md](DOCTRINE.md), the imports resolved.

## 5. Keeping an ALREADY-INSTALLED machine current

`git pull` on this repo propagates doctrine automatically (the `@import`
reads the pulled file). The ONE thing a pull cannot update is the pasted
block in your machine-local `~/.claude/CLAUDE.md` itself. When the block
changes here, re-paste §2 on each installed machine. Block changelog:

- **2026-07-16** — INTEGRATIONS.md removed from the auto-load imports
  (context budget, Decision 28). If your global file still contains
  `@…/doctrine/INTEGRATIONS.md`, delete that line and replace the paragraph
  above the import with §2's current text.
- 2026-07-10 — initial block.

## Rules of the split

- **This repo owns**: portable doctrine, the integrations policy, everything
  a second machine should inherit identically.
- **The global file owns**: machine-local facts only (build quirks, local
  install paths, hardware-specific gotchas). Those sections differ per
  machine by design and are never synced.
- **Never edit doctrine in the global file** — the imports make any doctrine
  text there redundant, and redundant copies drift. Doctrine changes are
  commits to this repo; `git pull` propagates them to every machine.
