# Installing the doctrine on a machine

How to wire a machine's global `~/.claude/CLAUDE.md` to this repo's canonical
doctrine. Done on: `machinepriest` Mac (2026-07-10). Replicate on any other
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
reviewable), never by editing this file. The sections below are imported from
it and auto-loaded every session:

@~/Documents/Claude/autonomous/doctrine/DOCTRINE.md

@~/Documents/Claude/autonomous/doctrine/INTEGRATIONS.md
```

## 3. Install the `/spinup` command

```bash
mkdir -p ~/.claude/commands
cp ~/Documents/Claude/autonomous/kit/commands/spinup.md ~/.claude/commands/spinup.md
```

Canonical copy: `kit/commands/spinup.md` (re-copy after pulling changes to
it). Gives every session a `/spinup <path> — <what it is>` command that runs
the survey-first new-project procedure.

## 4. Verify

Start a fresh Claude Code session anywhere and ask what the development
doctrine says about (e.g.) the AI/deterministic boundary. If the answer
reflects [DOCTRINE.md](DOCTRINE.md), the imports resolved.

## Rules of the split

- **This repo owns**: portable doctrine, the integrations policy, everything
  a second machine should inherit identically.
- **The global file owns**: machine-local facts only (build quirks, local
  install paths, hardware-specific gotchas). Those sections differ per
  machine by design and are never synced.
- **Never edit doctrine in the global file** — the imports make any doctrine
  text there redundant, and redundant copies drift. Doctrine changes are
  commits to this repo; `git pull` propagates them to every machine.
