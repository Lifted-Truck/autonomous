# Claude Code governance

Fill this in per repo (or per org). It's deliberately short — governance that nobody
reads is worse than none.

## Directly Responsible Individual (DRI)

| Role | Person | Notes |
|------|--------|-------|
| Claude Code config DRI | _TBD_ | Owns CLAUDE.md, hooks, skills, `.mcp.json` |
| Security reviewer | _TBD_ | Approves new MCP servers + hooks that run commands |
| Governance contact | _TBD_ | For larger orgs: the "agent manager" role |

## Approved skills & plugins register

Only skills/plugins listed here are sanctioned for this repo. Adding one requires
DRI sign-off.

| Skill / plugin | Purpose | Path scope | Approved by | Date |
|----------------|---------|-----------|-------------|------|
| _example-domain_ | _replace me_ | _src/..._ | _TBD_ | _TBD_ |

## Code-review policy

- Claude-generated changes are reviewed to the **same standard as human-written code.**
- Hooks that execute shell commands and new MCP servers get a **security review**
  before merge (they run with the developer's privileges).
- Start with **limited access**; expand scope as confidence builds.

## Config review log (every 3–6 months)

When a new model resolves a limitation, **delete** the CLAUDE.md constraint that
compensated for it — don't let stale guardrails accumulate. Record each review:

| Date | Reviewer | Model baseline | Constraints removed | Notes |
|------|----------|----------------|--------------------|-------|
| _TBD_ | _TBD_ | _e.g. Opus 4.8_ | _none yet_ | _initial setup_ |

## Packaging for distribution (optional)

To give every engineer an identical day-one setup, promote this `.claude/` config
into a **plugin** and serve it from an internal marketplace. The kit's `templates/`
directory is the source of truth; bump it there, then re-publish.
