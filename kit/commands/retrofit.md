---
description: Bring an EXISTING repo to the current kit version — a CHANGELOG-driven migration (currency check → gap plan → pause → append-only apply → declare), idempotent by construction
---

Retrofit this existing project: $ARGUMENTS

(Arguments — both optional: a target directory and a one-line description.
**If no directory is given, the target is the current working directory.**
Sanity-check the opposite of /spinup: the target SHOULD be an existing
project with real content; if it looks empty/greenfield, suggest /spinup
instead and stop.)

## Step 0 — currency, deterministically, before you read anything else

Run the kit's currency checker FIRST and paste its output into your first
message. It is the only source of truth for *what this retrofit is for*:

    python3 ~/Documents/Claude/autonomous/kit/currency.py <target>

It prints the kit version, the repo's DECLARED `kit_version` (absence reads
as `pre-2.0.0` — never as current), and the ordered list of CHANGELOG entries
the repo is behind, each with a presence check per requirement. Three
outcomes, and they decide the whole session:

- **CURRENT, nothing to do** → say so and STOP. Re-running the retrofit on a
  current repo is a no-op by construction. Do not "improve" anything.
- **CURRENT but `declares X but is missing: …`** → the declaration is false.
  That is drift, and it is louder than being behind: restore the missing
  items (append-only, per step 4) or, if they were removed deliberately,
  lower the declaration and record why in DECISIONS. Never leave a false
  declaration standing.
- **BEHIND by N entries** → the entries, in order, ARE the plan. Every
  `[ ]` is a gap to close; every `[x]` is done and MUST NOT be touched.
  Read `~/Documents/Claude/autonomous/kit/CHANGELOG.md` for each entry's
  **retrofit action** — that text is what you apply.

Then follow the canonical procedure at
`~/Documents/Claude/autonomous/ONBOARDING.md` → Part 2 → "Retrofitting an
EXISTING project" — all five steps, exactly, with the currency delta as the
gap table. Five behaviors are non-negotiable and unchanged:

1. **Infer before asking.** Gap-survey the repo read-only first; propose
   survey answers derived from the code and ask only what code cannot show
   (the architecture rung is still asked, never defaulted).
2. **Plan, then pause for approval before writing anything.** An existing
   repo is working state; list every create-vs-modify up front, keyed to
   the CHANGELOG entry that requires it.
3. **Append, never rewrite.** Marker-delimited insertions only; existing
   content wins conflicts pending a human ruling; re-running must be a
   no-op — and now that is CHECKED, not hoped: run `currency.py` again at
   the end and it must print `nothing to do`.
4. **Never break what works — or hide what doesn't.** `./verify` wraps the
   existing test/lint commands; currently-red tests are quarantined and
   recorded in ROADMAP as explicit debt, never deleted, never silently
   gated on, never "fixed" by weakening.
5. **Foreign/exported scaffolds: standard mechanisms, project substance**
   (the override clause — full text in ONBOARDING). Where a chat-exported kit
   overlaps the ecosystem kit, the kit's MECHANISMS replace the exported ones
   (verify, charter layout, ROADMAP/DECISIONS, loop, hooks, CI); the exported
   kit's project-specific SUBSTANCE is migrated into standard slots (§Domain,
   ROADMAP, DECISIONS, LIBRARY seeds, bespoke checks → verify targets) BEFORE
   anything is deleted. Unmappable content is surfaced to the human, never
   silently discarded. Map first, replace second, delete only what's mapped.

## Step 5 — declare, then prove the declaration

Only when EVERY `[ ]` in the delta is `[x]`: write `"kit_version": "<kit
version>"` into `project.manifest.json`. A partial retrofit writes
`"kit_version": "pre-<version>"` and records the remaining gaps in ROADMAP as
explicit debt — a repo never declares a version it does not meet. Then run
`currency.py` once more: it must say CURRENT with nothing missing. If it
does not, the retrofit is not done, whatever the diff looks like.

## Gotchas (each cost a real run)

- The Write tool does NOT set the exec bit: `chmod +x verify
  .claude/hooks/*.sh` or the oracle fails `permission denied` and — worse —
  `currency.py` correctly reports `./verify` as missing (it checks
  executability, not existence).
- `git grep -E` is POSIX ERE — no `\s`, `\d`, `\b` in any gate you write.
  Plant a known-bad line and watch the gate fire before you trust it
  (autonomous LIBRARY L0002).
- Every gate asserts the EFFECTIVE state, never the declared one (kit
  README, gate rule). The retrofit's own closing check is an instance:
  `currency.py` reads the tree, not your summary of it.

Finish by reporting: the currency output before and after (this is the
visual for the review beat — the `[ ]`→`[x]` delta), the manifest for
ratification, green `./verify fast` output, and any briefs filed. Reference
for the target end-state: `~/Documents/Claude/autonomous/` itself (declares
2.0.0 and passes its own checker), `~/Documents/Claude/distillery/`.
