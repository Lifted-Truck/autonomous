# Prompt: Integrate a cross-project AUDIT loop at this scope

You are installing a **hierarchical, self-improving audit loop** at a *parent
scope* — a directory whose immediate children each run their own knowledge loop
(or are themselves parent scopes). This audit loop sits ABOVE those per-project
loops: it does not reflect on primary work; it **harvests the cross-applicable
lessons from the children and centralises them here**, so siblings cross-learn and
the whole tree self-optimises. It never overrides a child's loop.

This is the parent-scope companion to `integrate-knowledge-loop.prompt.md` (which
installs the *leaf* loop). The two share one entry format on purpose, so the loop
is **self-similar**: whatever procedure a scope uses to harvest a leaf, its own
parent later uses to harvest it. Run this once per parent scope you want to light
up (e.g. a group directory of related projects, then the workspace root that
contains all your groups).

Work in four phases. **Do NOT write any files until Phase 3.**

## Phase 1 — SURVEY (read-only)
1. Confirm you are at the intended parent scope. List the immediate child
   directories and, for each, whether it has a `LIBRARY.md` (a loop-enabled child)
   or not. Children may be leaves OR lower parent scopes — both are harvested
   identically.
2. Report which of `CLAUDE.md` / `INDEX.md` / `LIBRARY.md` / `AUDIT-STATE.json`
   already exist here. If `CLAUDE.md` exists, summarise what it currently
   instructs (you will append, never rewrite).
3. Skim each child's `INDEX.md` to estimate the harvest surface: how many entries
   exist, and note any lesson that already appears (in substance) in ≥2 children —
   those convergences are your first, strongest promotion candidates.

## Phase 2 — PLAN (propose, don't write)
Present a short plan:
- Which files you will create vs. modify here.
- The promotion gate you will apply *at this level* (see the block below), and how
  it is tighter than the level beneath it. State the level number.
- Your first-pass list of promotion candidates from Phase 1 — for each: the child
  origin(s), whether it qualifies by canonical-tier or by ≥2-sibling convergence,
  and the transferable *pattern* (not the project-specific fact) you would promote.
- Confirm you will seed exactly the promotions that already qualify — no
  fabricated filler.

Pause for confirmation before Phase 3.

## Phase 3 — APPLY (write, idempotently)
On approval:
- If `CLAUDE.md` exists here, insert the PROTOCOL block below between the markers
  `<!-- AUDIT-LOOP:START -->` and `<!-- AUDIT-LOOP:END -->`; if those markers
  already exist, replace only what is between them (re-running is safe). If
  `CLAUDE.md` does not exist, create it with a one-paragraph scope header plus the
  block.
- Create `INDEX.md`, `LIBRARY.md`, and `AUDIT-STATE.json` only if missing (formats
  below). Seed LIBRARY with only the promotions that genuinely qualify now, each
  carrying its `origin:` back-link(s); add matching INDEX pointers. Never modify
  INDEX without LIBRARY, or vice versa.
- Record every seeded promotion and every child's current `LIBRARY.md` hash in
  `AUDIT-STATE.json`.

## Phase 4 — VERIFY
- Confirm every INDEX id resolves to a LIBRARY anchor and back, and every promoted
  entry's `origin:` points at a real child entry id.
- Confirm `AUDIT-STATE.json` lists every immediate child (with a null hash + note
  for those without a LIBRARY) and that its `promotions` map matches the seeded
  entries.
- Restate, in two sentences, how a future audit run (`run-audit-loop.prompt.md`)
  will behave here: which children it will skip (unchanged hash) and how it decides
  to promote.

---

## PROTOCOL block (insert verbatim into this scope's CLAUDE.md)

<!-- AUDIT-LOOP:START -->
## Cross-Project Audit Loop

A meta-layer ABOVE the per-project knowledge loops. It never overrides a child's
loop; it reads their outputs and promotes what is reusable. Run on demand or on a
cadence via `run-audit-loop.prompt.md`.

### The run (deterministic mechanics, judged promotions)
1. **SCAN** — For each immediate child with a `LIBRARY.md`, hash the file and
   compare to `AUDIT-STATE.json`. Only new/changed children are considered;
   unchanged children are skipped (no re-processing, no re-promotion).
2. **JUDGE** — For each new/changed child, read its INDEX then its entries. A
   child lesson is **promotable** only if ALL hold: (a) it is `canonical` at the
   child OR the same pattern appears independently in ≥2 children (convergence);
   (b) it generalises beyond its origin — a session on an *unrelated* sibling would
   benefit; promote the transferable *pattern*, not the project-specific fact;
   (c) it is not already covered here — if it matches an existing entry, merge (add
   the new origin + evidence) instead of duplicating, and a crossing of the ≥2
   threshold may bump that entry `candidate → canonical`.
3. **WRITE (atomic)** — Append the promoted lesson to `LIBRARY.md`, rewritten to
   its transferable core with `origin: <child>#Lxxxx[, …]`, plus its `INDEX.md`
   pointer in the same change. Single-origin promotions enter `tier: candidate`;
   convergent (≥2 origins) may enter `canonical`.
4. **LEDGER** — Update `AUDIT-STATE.json`: child hashes, `audited` date, and a
   `child#Lxxxx → this#Lxxxx` promotion record. A child entry already mapped is
   never promoted twice.

### Promotion gate — tightens as you ascend
- **Group level:** promote on generality OR ≥2-sibling convergence.
- **Top level:** promote only what is proven across ≥2 groups / 3+ projects —
  universal engineering lessons (the altitude of the global `~/.claude/CLAUDE.md`).
- **Anti-dilution:** the parent is NOT the union of child libraries; it is the
  *intersection of what is reusable*. If a lesson would only ever help its origin,
  it stays put. When in doubt, do not promote.
- **Anti-poisoning (inherited):** a wrong promotion is amplified across every
  sibling. Prefer not promoting over promoting unverified; every entry keeps its
  falsifier; a promoted lesson contradicted by present evidence is demoted here and
  the demotion noted at the origin.

### Provenance & recursion
Every entry carries `origin:` and never loses it. This scope's LIBRARY uses the
leaf entry format, so the level above harvests THIS scope with the identical
procedure — the loop is self-similar at every level.
<!-- AUDIT-LOOP:END -->

---

## File formats

**LIBRARY.md** — leaf entry template plus a required `origin:` field:
`[Lxxxx] <title> | tier | added: YYYY-MM-DD | tags: … | origin: <child>#Lxxxx[, …] | lesson: … | evidence: … | falsifier: … | supersedes: …`

**INDEX.md** — one line per entry: `id — tags — hook (origins)`.

**AUDIT-STATE.json**:
```json
{
  "schema": "audit-state.1",
  "scope": "<dirname>",
  "level": <int>,
  "last_audit": "YYYY-MM-DD",
  "next_id": <int>,
  "children": {
    "<child>": { "library_hash": "<sha256-16>", "audited": "YYYY-MM-DD" },
    "<child-without-loop>": { "library_hash": null, "note": "no LIBRARY.md" }
  },
  "promotions": [
    { "id": "Lxxxx", "origins": ["<child>#Lxxxx"], "tier": "candidate|canonical", "reason": "…", "added": "YYYY-MM-DD" }
  ]
}
```
Hash a child with: `shasum -a 256 <child>/LIBRARY.md | cut -c1-16`.
