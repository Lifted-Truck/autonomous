# Project-type conventions (portable; read on demand)

> Conventions specific to a KIND of project. Synced across machines (this is
> the doctrine repo) but deliberately NOT auto-loaded — context budget,
> Decision 28. Read the relevant section when working on that project type.
> The pointer lives in DOCTRINE.md.

## Audio plugins (VST / AU / CLAP)

- **Brand — every plugin ships under the company/manufacturer name
  "Lifted Truck".** JUCE `COMPANY_NAME "Lifted Truck"`, the AU/VST3
  manufacturer field, and the bundle-identifier prefix
  `com.LiftedTruck.<Plugin>`. Applies to all VST/AU/CLAP builds, forward-going;
  already-shipped plugins conform only via a deliberate per-repo cleanup.
  (The machine-local BUILD process — toolchain, codesign seal, `auval` — stays
  in the global `~/.claude/CLAUDE.md`; only the portable brand fact lives here,
  so it syncs to every machine that builds plugins.)
