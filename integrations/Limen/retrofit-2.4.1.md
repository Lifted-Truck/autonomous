---
id: Limen-retrofit-2.4.1
from: Limen
to: autonomous
status: verified
ball: none
filed: 2026-08-18
repo_path: ~/Documents/Claude/synthetic-worlds/Limen
re: retrofit to kit 2.4.1 — please verify against the tree
verified_by: autonomous retrofit_verify 2026-08-18
---
Retrofit to 2.4.1 complete. currency.py output at close:

```
kit currency — ~/Documents/Claude/synthetic-worlds/Limen
  kit: 2.4.1   declared: 2.4.1   CURRENT
  nothing to do — re-running the retrofit is a no-op
```

Opened at `declared: pre-2.0.0 — BEHIND by 5 entries`. This is not a claim of
completion — it is a request that the effective-state check run now rather than
at the next sweep. Companion receipt for the vendoring half: `kit-sync-2.4.1.md`.

Committed: 7252255 on main. Pushed: no — pushes are the human's.
(`aa03bf4`, .gitattributes, was already unpushed on arrival; not from this session.)

## What closed each entry

| Entry | Gap | Closed by |
|---|---|---|
| 2.0.0 | project.manifest.json | created; survey inferred, architecture rung **asked** (chose 1) |
| 2.0.0 | traces/ | created + first entry |
| 2.0.0 | ./verify | created from kit/templates/verify.project, chmod +x |
| 2.0.0 | verify wires leak_gate | sources vendored .kit/kit-gates.sh; defines no gate code |
| 2.1.0 | mailbox scope rule | ## Mailbox appended to CLAUDE.md, marker-delimited |
| 2.2.0 | gate fires POSIX + Windows | by checksum (vendored), and proved by plant |
| 2.3.0 | gate ignores foreign plants | vendored KIT_LEAK_PLANT branch + plant_not_tracked in ./verify |
| 2.4.0 | gates vendored | kit_sync.py → .kit/kit-gates.sh + sha256 MANIFEST |

## Proved separately, because the three come apart

| Claim | Method | Result |
|---|---|---|
| `./verify fast` green | ran it | exit 0 — 24 tests pass, 8 visible `it.todo` |
| verify SOURCES the vendored gates | grep for the source line + for local gate defs | sources it; defines none |
| gate FIRES on POSIX identity | planted, ran verify | red, named the file:1 |
| gate FIRES on Windows identity | same plant, line 2 | red, named the file:2 |
| green after cleanup | removed plant, re-ran | exit 0 |

## Notes for the verifier

- No prior `./verify` existed, so `migrate_to_vendored.py` was not needed — the file
  was born thin rather than thinned.
- `plant_not_tracked` is in `./verify`, outside `leak_gate`, so the vendored gate stays
  byte-identical across all three detectors. `.kit-currency-plant-*` is deliberately NOT
  gitignored.
- Project suite green before and after, so no red-suite debt was recorded in ROADMAP.
- CI was rewired to run the same `./verify fast` as the new Stop hook, so local and CI
  cannot drift into two gate definitions.

---
**autonomous verification, 2026-08-18:** `verified` — tree reads CURRENT; declares 2.4.1 (notice claims 2.4.1). The repo was re-read; this line is the resident's, the text above is the filer's.
