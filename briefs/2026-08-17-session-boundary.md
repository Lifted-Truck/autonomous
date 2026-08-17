# Brief: Session-Boundary Commands and Open-Session Registry

**To:** the autonomous agent (github.com/Lifted-Truck/autonomous)
**From:** Julian, via a design conversation on 2026-08-17
**Status:** recommendation, not spec. Interpret, propose, and confirm before building. Where this brief conflicts with existing doctrine, doctrine wins and the conflict should be surfaced.

## 1. Purpose

Add three per-project slash commands that bound a working session — `/wakeup`, `/breakdown`, and `/reorient` — plus a small cross-machine registry of currently open sessions. The goal is that every session starts from a summarized, agreed-upon state and ends with loose ends tied, the reflection log updated, and next steps queued, and that Julian can see at the end of a night which projects still need closing.

This is a direct application of the VSM / recursive-governance direction. The same protocol runs at the project level and, later, at the ecosystem level over the projects. Design it so that recursion is possible from the start even if only the project level ships now.

## 2. Vocabulary

- **Session**: one bounded stretch of work in one repo, opened by `/wakeup` and closed by `/breakdown`.
- **SESSION.md**: per-repo hot-state artifact written by `/breakdown`, read by `/wakeup` and `/reorient`. The only prior-session context the next session trusts.
- **Reflection log**: per-repo, append-only stream of open questions, half-thoughts, and things Julian wants to hold between sessions. Distinct from DECISIONS.md (decisions) and distillery (lessons). Pruned by `/wakeup`.
- **Registry**: cross-machine store of *which sessions are currently open*. Contains no content. Lives outside any project.

## 3. The three commands

All three share one underlying routine: **read current state and render it**. They differ only in what they are permitted to write. Build the shared routine first; the commands are thin wrappers over it.

The shared read set, in priority order: SESSION.md, ROADMAP.md (current phase), DECISIONS.md (tail), the reflection log, `./verify fast` result, `git status` and recent diff, recent entries under `traces/`.

### `/wakeup` — full open

Reads the shared state, then:

1. Pulls the registry, checks for a stale row for this repo (see §5, unclean shutdown).
2. Renders a short state summary: where the project is, what changed last session, verify status, what is ready to work on.
3. Prunes the reflection log: each entry either graduates (to DECISIONS.md, ROADMAP.md, or an issue), stays with a note, or is dropped. Propose; Julian confirms.
4. Surveys Julian **only if there is genuine ambiguity** — multiple ready threads, a stale or contradicted plan, red verify, or an unresolved reflection entry that blocks the obvious next move. Otherwise state the assumed starting point and proceed. A survey that fires every time will be skipped.
5. Writes a registry row for this session and pushes.

Permitted writes: registry (open row), reflection log (prune edits), and any graduation targets Julian confirms.

### `/breakdown` — full close

Reads the shared state, then:

1. Runs the organizational protocol: `./verify fast`, README/ROADMAP drift check, uncommitted work, orphaned traces, TODOs left in code that should be in ROADMAP.
2. Ties up loose ends it can tie up deterministically; lists the ones it cannot.
3. Surveys Julian with **three prompts, no more**: what did today decide that is not yet in DECISIONS.md; what is the loose thread you are most likely to forget; what is the first move next session. Everything else should be derivable from the diff, traces, and verify.
4. Appends to the reflection log; appends confirmed decisions to DECISIONS.md.
5. Writes SESSION.md: state summary, next-first-move, open threads, verify status, pointer to the session's traces.
6. Removes the registry row and pushes.
7. If other rows remain open in the registry, closes with a one-line reminder: "Still open: X, Y."

Permitted writes: everything above, plus commits if doctrine already allows the agent to commit in this repo. Never weakens gates.

### `/reorient` — reload the frame, leave the ledger alone

Reads the shared state and re-renders the summary and next move. Lets Julian redirect. Does **not** survey deeply, does **not** touch the registry, and does **not** write to the reflection log unless Julian explicitly says something worth writing.

Triggers: after unclean shutdown (offered by `/wakeup`), mid-session after a break or context drift, and after compaction or a fresh context window when the agent itself has lost the thread. The last is the expected common case — treat this as a deterministic re-priming step for the model.

## 4. The registry

**What it is:** a directory of one file per open session, not one file of rows. Concurrent opens on different machines never touch the same path; merges are trivial.

**Where:** Julian's private website repo, since both machines already pull it. Each machine's `~/.claude/CLAUDE.md` gets a redirect pointing at the local clone path. If git becomes annoying as a live store, the same shape moves to a hosted key-value store later without changing the contract — design the interface so that swap is one module.

**Row schema (one file per session):** `repo`, `session_id`, `machine`, `opened_at`, `last_heartbeat`. Nothing else. No summaries, no content. Key by `session_id`, not by repo, so two concurrent sessions in one repo (a fleet job and Julian) are legible rather than a collision.

**Freshness is owned by the commands, not by Julian:** `/wakeup` pulls before reading; `/breakdown` pushes after writing. Registry writes are trivial and idempotent — implement them as a small deterministic script with no model in the loop.

**Contract for dispatch and distillery:** they read only closed-session artifacts (SESSION.md, reflection logs, traces). They never read the live registry, so they cannot race a running build.

**Side benefit:** open-count and session duration over time is a cheap health signal for the fractal. Too many long-open sessions is variety overload at the System 3 level. Worth surfacing in dispatch eventually; not in scope now.

## 5. Edge cases to design for now

**Unclean shutdown.** `/wakeup` finds a stale row for its own repo. Treat as unclean: reconstruct what it can from diff and traces, offer `/reorient` first, then run an abbreviated `/breakdown` (write SESSION.md, close the row) before opening the new session. Never silently overwrite a stale row.

**Concurrent sessions in one repo.** Rows keyed by `session_id`. SESSION.md is written by whichever `/breakdown` runs last; earlier closes should append rather than replace open-thread lists. Follow the concurrency requirement already recorded from the `pborenstein/handoff` review: any hot-state pattern is either bounded to single-session work or redesigned to survive concurrency.

**Registry unreachable.** `/wakeup` proceeds with a warning and a local marker; `/breakdown` queues the close and retries. Never block a session on the registry.

**Reflection log growth.** Pruned every `/wakeup`. Entries have a `raised_on` date; anything unaddressed for N sessions gets flagged for graduate-or-drop rather than allowed to accumulate.

## 6. Doctrine alignment (check these, do not assume)

- AI/deterministic boundary: state *rendering* and surveys are AI; registry writes, verify runs, and log pruning bookkeeping are deterministic scripts.
- Oracle discipline: `/breakdown` runs `./verify`; a red verify is reported, never hidden, and does not block close.
- Writes stay home: no command writes into another repo. The registry is the single sanctioned cross-repo write and it carries no content.
- Right-sized agents: all three commands are single-thread. Do not spawn subagents for a session boundary.
- Living README: `/breakdown` checks README drift as part of the organizational protocol.

## 7. Suggested build order

1. Shared state-read-and-render routine (§3 preamble). This is what everything else calls.
2. `/reorient` — it is the shared routine with no writes, so it validates the routine cheaply.
3. Registry script and CLAUDE.md redirect on both machines.
4. `/wakeup`.
5. `/breakdown`.
6. Retrofit into existing repos via `/retrofit`; add to `/spinup` template.
7. Later: ecosystem-level `/wakeup` and `/breakdown` in dispatch that fan out over open registry rows.

## 8. Open questions for Julian

- Command names: `/wakeup` `/breakdown` `/reorient` are placeholders — confirm or rename.
- Should `/breakdown` be allowed to commit and push project work, or only its own artifacts?
- Heartbeat: should long sessions refresh `last_heartbeat` periodically, or is `opened_at` enough for now?
- Where exactly does the reflection log live — a new file at repo root, or a section of an existing knowledge-loop file (INDEX.md/LIBRARY.md)?
