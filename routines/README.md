# routines — scheduled processes that operate on this repo

Prompt files for recurring routines, versioned here so they're reviewable,
diffable, and portable across machines/substrates.

## landscape-audit (monthly, propose-only)

Two variants of the SAME process — run one per month, not both:

| Variant | Where it runs | File |
|---|---|---|
| Local scheduled task | The primary machine's Claude app (`monthly-landscape-audit`, 9am on the 10th; catches up on next launch if the app was closed) | Task-local SKILL.md at `~/.claude/scheduled-tasks/monthly-landscape-audit/` |
| Cloud | A Claude Code cloud routine, or a GitHub Actions cron running Claude Code headless | [landscape-audit.cloud.prompt.md](landscape-audit.cloud.prompt.md) |

Both produce the identical artifact: a PR with
`research/proposals/<date>.proposal.md` (DELETIONS section required) + a
dated bibliography append. Neither ever merges its own PR.

**To run the cloud variant via GitHub Actions**, a minimal workflow shape
(not installed — add deliberately, with `ANTHROPIC_API_KEY` in repo
secrets, and disable the local task's schedule to avoid double runs):

```yaml
# .github/workflows/landscape-audit.yml (example — not active)
name: landscape-audit
on:
  schedule: [{cron: "0 9 10 * *"}]   # UTC in Actions, unlike local tasks
  workflow_dispatch: {}
permissions: {contents: write, pull-requests: write}
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm install -g @anthropic-ai/claude-code
      - run: claude -p "$(cat routines/landscape-audit.cloud.prompt.md)" --permission-mode acceptEdits
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Canonical-copy note:** the process definition effectively exists in two
places (the local task's stored prompt and the cloud prompt file). Tolerated
for now because the local task is mid-testing; once testing settles, the
clean fix is to thin the local task's prompt down to "pull the repo and
execute routines/landscape-audit.cloud.prompt.md, skipping the cloud-setup
section" — making THIS file the single canonical definition. Flagged as a
dedup item; see DECISIONS.md.
