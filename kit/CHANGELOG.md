# kit CHANGELOG — every entry names the retrofit action it implies

> Semver in `kit/VERSION`. A repo records the version it was scaffolded or
> last retrofit at in `project.manifest.json` → `kit_version`. `/retrofit`
> reads that field and applies every entry BELOW it, in order, as a migration
> — never a re-scaffold. A repo with no `kit_version` is `pre-2.0.0`, not
> "current": absence of a declaration is never read as up-to-date (that
> silence is exactly how the wrapper registry hid five repos).
>
> Entry format: version · date · what changed · **retrofit action** (what
> `/retrofit` does to a repo below this version) · verify gate if any.

## 2.0.0 — 2026-08-17 — baseline

The state of the kit at the moment it gained a version. Everything a
kit-v2 core install carries as of this date:

- Layered CLAUDE.md, ROADMAP.md (phase-gated; Prior-Art bookends per
  Decision 30), DECISIONS.md (append-only), `project.manifest.json`
  (survey answers + composite territory registry; NO status prose per
  Decision 28), INDEX.md + LIBRARY.md (`library-entry.3`), `traces/`,
  `./verify` (`fast|full|report`) carrying the `leak_gate`
  (POSIX + Windows identity paths, `.leakcheck-allow`), CI mirroring the
  Stop hook (`kit/templates/ci.github.yml`, Decision 31 economics),
  `.gitattributes` LF (Decision 34), `contract_gate` for composites
  (Decision 43), `status_validate` fixtures (Decision 45).
- **Retrofit action:** a repo with no `kit_version` gets the K0 survey (which
  of the above are present), then `kit_version: "2.0.0"` written into its
  manifest ONLY when all baseline items are present. Partial installs record
  `kit_version: "pre-2.0.0"` plus the gap list in ROADMAP as explicit debt.
- **Verify gate:** none new — the baseline is what `./verify fast` already
  checks where the repo has one.

## 2.0.1 — 2026-08-17 — /retrofit is a CHANGELOG-driven migration (K1)

- `kit/currency.py` — deterministic: reads a repo's declared `kit_version`,
  diffs against this file, emits the ordered delta with a presence check per
  requirement. `REQUIREMENTS` in that file is the GATE for each version;
  the prose here is the explanation. A test pins that every version here has
  a row there.
- `/retrofit` opens by running it and works the delta; closes by running it
  again and requiring `nothing to do`. Idempotence is checked, not hoped.
- A repo may declare current while missing items (autonomous did, for one
  hour, on the day it declared): reported as drift, louder than behind.
- **Retrofit action:** none for the repo — this entry changes the TOOL, not
  what a repo must contain. Repos at 2.0.0 are unaffected and stay 2.0.0;
  the version bump is a patch so `currency.py` does not report 46 repos
  behind by an entry that asks nothing of them.
- **Verify gate:** autonomous's own `./verify fast` runs the currency tests
  and its own currency check.

## 2.1.0 — 2026-08-17 — mailbox scope rule in every charter (K1 follow-on)

- Every repo's `CLAUDE.md` states, in its own words, **which mailbox is its
  own and that other repos' exchanges are not its business** — the three
  questions in INTEGRATIONS §3 "Scope" (who owes me / did anyone answer me /
  should I act on X↔Y).
- **Retrofit action:** append a `## Mailbox` section to `CLAUDE.md` naming
  (a) `integrations/` in THIS repo as the only place briefs to us land,
  (b) that responses to OUR briefs live in the PROVIDER's tree and must be
  pulled and read, (c) that exchanges between other repos may be READ freely
  but never ACTED on or raised to the human as ours — if one concerns us, we
  file a brief. (Corrected 2026-08-18 per hypersaw-001/002: an earlier draft
  said "ignored", which over-reached into informational quarantine; a repo that
  retrofit before the correction should re-read this clause.)
  Marker-delimited, append-only; if a `## Mailbox` section already exists,
  leave it alone and report the difference.
- **Verify gate:** none — this is a charter statement, and gating prose on
  grep would reward the words over the understanding. The behavioural gate is
  the scoped session brief, which only ever shows a repo its own obligations.
- **Why:** on 2026-08-17 agents in several unrelated projects each warned the
  human about one brief in autonomous's mailbox. Tooling caused it; the rule
  was never written down either way.

## 2.2.0 — 2026-08-18 — the leak gate must FIRE, not merely exist (spectral-morph-001)

- `currency.py` now asserts gate BEHAVIOUR: it plants a POSIX identity path
  and a Windows identity path in a scratch file inside the repo, runs the
  repo's own `./verify fast`, and requires the gate to name the file. The
  plant is created and removed inside one call. Previously it checked that
  `verify` CONTAINED the string `leak_gate` — a presence check on the gate's
  name, and the one place the kit violated its own "assert the effective state"
  rule. `harness/verify` — the template every new project is born from —
  shipped a POSIX-only pattern for a month and read as compliant.
- **Retrofit action:** if either plant fails to fire, replace the repo's
  `leak_gate` pattern with `autonomous/verify`'s (both identity forms, both
  placeholder exclusions). Three detectors, one policy: `verify`,
  `harness/verify`, `governor/leak_scan.py` carry the same regex.
- **Verify gate:** the two `gate-fires:` checks. A repo already declaring
  2.0.0/2.1.0 on a POSIX-only gate now reads BEHIND — correct, and this entry is
  what makes that a migration rather than a silent tightening.

<!-- Next entries append BELOW, newest last, so the migration order reads
     top-to-bottom. K2 (intake/), K3 (session-boundary artifacts) will land
     here as 2.1.0 / 2.2.0 when they ship. -->
