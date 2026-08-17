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

<!-- Next entries append BELOW, newest last, so the migration order reads
     top-to-bottom. K2 (intake/), K3 (session-boundary artifacts) will land
     here as 2.1.0 / 2.2.0 when they ship. -->
