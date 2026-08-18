# Prompt: Run the cross-project AUDIT loop at this scope

You are performing one **harvest pass** of the hierarchical knowledge loop at the
current parent scope (a directory whose immediate children each run their own
loop, or are themselves parent scopes). You promote the *cross-applicable* lessons
from the children UP into this scope's `LIBRARY.md`, so siblings cross-learn.

Prerequisite: this scope has already been set up by `integrate-audit-loop.prompt.md`
(it has `CLAUDE.md` with an `AUDIT-LOOP` block, `INDEX.md`, `LIBRARY.md`, and
`AUDIT-STATE.json`). If not, run that first.

**Design stance (why this is careful, not a log-append).** Promotion grants write
access to a shared, high-trust scope that many child sessions will later read as
authoritative — so a wrong promotion is amplified across every sibling, and drift
stays below any single-entry check. Treat every promotion as an **untrusted write
to a high-privilege store**: trust is *earned at the boundary* via independent
corroboration and provenance, **never inherited** from the fact that a trusted
loop proposed it. And a lesson is not "learned" merely by being logged — see
Lifecycle below.

---

## Run modes
- **apply** (default, on-demand with a human present): perform all steps, writing
  to `LIBRARY.md` / `INDEX.md` / `AUDIT-STATE.json`.
- **propose-only** (used by the weekly cron): do Steps 1–4's *analysis*, but do
  **not** mutate `LIBRARY.md`, `INDEX.md`, or `AUDIT-STATE.json`. Instead write the
  proposed promotions/merges/demotions — each as a ready-to-paste entry with its
  origins, tier, and rationale — to `./audit-runs/<YYYY-MM-DD>.proposal.md`, then
  stop. This is the staging buffer: promotion into the shared, high-trust store
  stays behind human approval (the poisoning literature's strongest recommendation
  for a promote-up loop). If the harness sets `AUDIT_MODE=propose-only` or the
  invocation says "propose only", use this mode.

## Step 1 — SCAN (deterministic; skip unchanged)
1. Read `AUDIT-STATE.json`.
2. For each immediate child directory that has a `LIBRARY.md`, compute
   `shasum -a 256 <child>/LIBRARY.md | cut -c1-16`.
3. A child is **in scope for this pass** iff its hash differs from the ledger (new
   or changed). Skip unchanged children entirely — do not re-read, do not
   re-promote. List which children are in scope and which are skipped.
4. Also record any child that lost its `LIBRARY.md` (set hash null) and any new
   child directory.

## Step 2 — JUDGE (the promotion gate)
For each in-scope child: read its `INDEX.md`, then read only the entries that are
new or changed since the ledger's record (compare against the `promotions` map —
entries already mapped to a `this#Lxxxx` are done unless their text changed).

A child lesson is **promotable** only if ALL of these hold:

- **Qualified at source** — it is `canonical` at the child, **OR** the same pattern
  appears **independently** in ≥2 children. "Independently" means the siblings did
  **not** inherit it from the same shared source (same brief, same engine notice,
  the same upstream doc). Convergence from a *shared* source is one observation
  wearing two hats — it counts once, not twice. [quorum defeats single-source
  poisoning; corroboration must be independent]
- **Generalises beyond origin** — a future session on an *unrelated* sibling would
  benefit. Promote the transferable **pattern**, not the project-specific fact.
  Litmus: could you state the lesson without naming the origin project's code? If
  not, it stays local.
- **Not already covered here** — if it matches an existing entry, MERGE (Step 3),
  don't duplicate.

Do **not** promote: one-off facts, project-local file paths/APIs, anything you are
unsure generalises. **Prefer not promoting over promoting unverified** — when in
doubt, leave it in the child. The parent is the *intersection of what is reusable*,
not the union of the children's libraries.

## Step 3 — WRITE (atomic; dedup over abstraction)
For each promotable lesson:

- **Merge if it matches an existing parent entry.** Add the new `origin:` back-link
  and evidence to the existing entry rather than writing a second one. If the merge
  pushes an entry to ≥2 *independent* origins, it may cross `candidate → canonical`.
- **Preserve the concrete instance — do not over-summarise.** Abstract only to the
  transferable pattern in the `lesson:` field, but keep each origin's specifics in
  `evidence:` and the `origin:` back-links. (Aggressive summarisation measurably
  destroys the detail that makes a lesson usable — lossless dedup beats lossy
  abstraction.)
- **Write both files in one change.** Append the entry to `LIBRARY.md` (leaf
  template + required `origin:`), add its one-line `INDEX.md` pointer. Never touch
  one without the other. Allocate the id from `AUDIT-STATE.json.next_id`.

Entry template:
`[Lxxxx] <title> | tier | added: YYYY-MM-DD | tags: … | origin: <child>#Lxxxx[, …] | lesson: … | evidence: … | falsifier: … | supersedes: …`

## Step 4 — LIFECYCLE, RECURRENCE & SUPERSESSION
- **Lifecycle (logging ≠ learning).** A single-origin promotion enters
  `tier: candidate` — *quarantined*: recorded, but low-trust. It earns
  `tier: canonical` only via a second **independent** origin or human review. A
  promotion is only truly "learned" when it changes downstream behaviour; today
  that means it is visible to child sessions (ancestor `CLAUDE.md`/`INDEX.md`
  auto-load) — when down-propagation or an enforcing hook/test is wired, bind the
  lesson to it and note the binding.
- **Recurrence → escalate.** If a child logs a *new* lesson whose failure
  signature matches one already `canonical` here, that is evidence the lesson was
  logged but not institutionalised — do not just add an origin; flag it (append
  `| recurred: YYYY-MM-DD (child#Lxxxx)`) and consider escalating it to the next
  level up or binding it to an enforcing artifact.
- **Supersession (invalidate, don't erase).** If present evidence contradicts a
  promoted lesson, **demote it here** (tier → `candidate`, or mark superseded via
  the `supersedes:` chain) and note the demotion at the origin child. Keep the
  history — never silently delete a promoted entry.

## Step 5 — LEDGER (make the pass idempotent)
Update `AUDIT-STATE.json`:
- new/updated child hashes and `audited` dates; null hashes + notes for children
  without a `LIBRARY.md`;
- `next_id` advanced past any ids you allocated;
- a `promotions` record per new entry: `{id, origins[], tier, reason, added}`, and
  for merges, the added origin(s);
- `last_audit` = today.
A child entry already in the `promotions` map is never promoted again unless its
source text changed.

## Step 6 — REPORT
Summarise: children scanned / skipped, entries considered, what was promoted or
merged (with origins and tier), what you deliberately did **not** promote and why,
any demotions/recurrences, and the new `LIBRARY.md` entry count. If it now exceeds
~30 entries, note that consolidation is due.

---

### Anti-poisoning checklist (run before writing)
- [ ] Every promotion is qualified at source (canonical OR ≥2 **independent** origins).
- [ ] Every promotion generalises (states the pattern without the origin's code).
- [ ] Every entry carries `origin:` provenance and a `falsifier:`.
- [ ] New single-origin entries enter quarantined (`candidate`), not `canonical`.
- [ ] When unsure, it stayed in the child (default-deny).
- [ ] Merges preserved each origin's concrete instance (no lossy over-summary).
