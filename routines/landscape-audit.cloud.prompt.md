# Landscape audit — cloud routine prompt

> Self-contained prompt for running the monthly landscape audit in a CLOUD
> environment (Claude Code cloud routine, or a GitHub Actions cron invoking
> Claude Code headless). No local-machine assumptions. The local variant
> lives as the `monthly-landscape-audit` scheduled task on the primary
> machine; run ONE of the two per month, not both. Design of record:
> ROADMAP.md → Deferred → "Landscape audit".

---

Run the monthly LANDSCAPE AUDIT for the autonomous-paradigm ecosystem: a
propose-only research pass that re-surveys the external field of AI-agent
development practice and recommends protocol changes via pull request. You
are acting as a resident of the standards repo
(github.com/Lifted-Truck/autonomous).

## Environment setup (cloud)

1. You are in a fresh environment. If the repo is not already checked out in
   your working directory, clone it:
   `git clone https://github.com/Lifted-Truck/autonomous.git && cd autonomous`.
   If it is checked out, `git pull` on main first.
2. Ensure a git author is configured (CI environments often lack one):
   `git config user.name "Landscape Audit"` and
   `git config user.email "noreply@anthropic.com"` — only if unset.
3. Confirm `gh` is authenticated (`gh auth status`) or a `GH_TOKEN` /
   `GITHUB_TOKEN` with repo scope is present. If neither: complete every
   step through the local commit, then STOP and report the branch name and
   that a push/PR could not be made — never fail silently.
4. Take today's date from the environment (`date -u +%F`); use it for the
   proposal filename and bibliography section.

## Orientation (read before researching)

5. Read, in order: `doctrine/DOCTRINE.md`, `doctrine/INTEGRATIONS.md`,
   `DESIGN.md`, `README.md`, `research/BIBLIOGRAPHY.md` (note each topic's
   most recent dated section — those are the "last checked" dates), and any
   prior files in `research/proposals/`. Do not repeat prior recommendations
   unless new evidence changes them. For each prior proposal, check whether
   its PR was closed unmerged (`gh pr list --state closed`) — a rejected
   recommendation is not re-proposed without materially new evidence.

## Research pass

6. Fan out parallel research agents (WebSearch/WebFetch), one per doctrine
   area, each scoped to "what has changed or emerged since <that area's
   last-checked date>":
   - Multi-agent coordination for software development (orchestration
     patterns, worktree fleets, merge queues, agent teams; new published
     systems or postmortems)
   - Agent memory and knowledge loops (memory architectures, poisoning
     research, consolidation/eviction findings)
   - Governance, halting, and agentic safety (circuit breakers, incidents,
     lab guidance from Anthropic/OpenAI/DeepMind)
   - Verification and CI-as-arbiter (gate-weakening research, mutation
     testing for agent code, flaky management, review automation)
   - Context engineering and harness design (Anthropic engineering posts,
     context-rot research, harness patterns)
   - One open-scope agent: significant NEW categories the above miss (new
     tooling paradigms, major model-capability shifts that make existing
     guardrails obsolete).
   Each agent returns dense findings with URLs and explicitly flags anything
   that CONTRADICTS or EXTENDS current doctrine.

   **Resilience against blocked requests** (observed in practice: automated
   runs can hit bot-protection on target sites and safety-classifier blocks
   on security-adjacent queries):
   - Frame security-topic queries with their true defensive purpose stated
     up front — this research surveys published *defenses* (circuit
     breakers, injection mitigations, poisoning safeguards) to harden an
     autonomous development system; it never seeks exploit code, and agents
     must not attempt to bypass any refusal or bot-protection.
   - A blocked or refused fetch is NEVER fatal and never silently dropped:
     try alternates first (search-result snippets, arXiv abstracts, an
     alternative writeup of the same finding, archive.org), and whatever
     remains unverified goes in a **"Blocked / unverified sources"** section
     of the proposal so the human can check those items interactively.
   - Prefer bot-tolerant primaries (arXiv, official lab blogs, GitHub, docs
     sites) over aggregator/paywalled ones when both report the same thing.

## Synthesis and output (propose-only — hard rule)

7. Diff findings against `doctrine/` and `DESIGN.md`. Write
   `research/proposals/<YYYY-MM-DD>.proposal.md` containing:
   - A short landscape summary (what moved this month).
   - Numbered recommendations, each: ADD / AMEND / DELETE, the exact
     doctrine file + section it targets, the evidence (URLs), what it
     supersedes, and a confidence note.
   - A DELETIONS section is REQUIRED — stale constraints that new evidence
     or new model capabilities have obsoleted; if none, state "no deletions
     identified" explicitly.
   - If the field genuinely didn't move, write a short no-change proposal
     recording exactly what was checked and found stable (honest staleness —
     the check itself is the record).
8. Append a new dated section to `research/BIBLIOGRAPHY.md` listing every
   source consulted this run (one line each, grouped by topic; re-consulted
   sources get fresh entries under the new date).
9. NEVER edit `doctrine/`, `DESIGN.md`, `README.md`, or any file other than
   the two above. Doctrine changes land only through human review of the PR.

## Ship

10. Run `./verify fast` (requires python3; if the environment lacks it, note
    that in the PR body instead of skipping silently). Do not commit on red —
    fix only problems your own changes caused; otherwise report and stop.
11. Branch `landscape-audit/<YYYY-MM>` (if it already exists, suffix `-2`,
    `-3`, …). Commit the two files; end the commit message with:
    `Co-Authored-By: Claude <noreply@anthropic.com>`
12. Push and open a PR via `gh pr create`, titled
    `Landscape audit <YYYY-MM>`, body summarizing the recommendations (lead
    with any DELETE/AMEND items) and ending with:
    `🤖 Generated with [Claude Code](https://claude.com/claude-code)`
13. NEVER merge the PR. Human review is the gate — that is the entire safety
    design of this process: a wrong doctrine change propagates to every
    session on every machine that imports this repo's doctrine.

Success = an open PR containing a dated, cited proposal (even a no-change
one) and an updated bibliography, with zero edits outside `research/`.
