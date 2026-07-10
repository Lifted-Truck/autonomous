# autonomous

**The canonical home for a fully-autonomous development paradigm** — the
doctrine, harness kit, loops, and governor that let coordinated parallel
agents build correctness-critical software without colliding or drifting.

Everything here follows one rule: **every artifact has exactly one canonical
home; every other location is a pointer.** This repo is that home for the
infrastructure below (or the pointer to the component repo that is).

## Map

| Path | What it is | Status |
|---|---|---|
| [DESIGN.md](DESIGN.md) | The consolidated infrastructure design (research-backed) | current |
| [ROADMAP.md](ROADMAP.md) | Phase-gated build sequence — single source of truth for direction | current |
| [DECISIONS.md](DECISIONS.md) | Append-only decision log | current |
| [doctrine/](doctrine/) | Cross-project doctrine + integrations policy. Global `~/.claude/CLAUDE.md` imports these. | current |
| [kit/](kit/) | Harness kit v2 ("the harness factory": core + agent-type profiles) | **to build** — v2 spec in DESIGN §6; the layer-3 scaffold prompt lives here |
| [harness/](harness/) | The Generic Agent Harness (verify contract, implementer/verifier/critic trio, hooks) — the intra-organ operating loop | imported from master-harness |
| [loops/](loops/) | Memory loops. Leaf knowledge loop is canonical here; the cross-project audit loop is canonical at [agent-knowledge-loop](https://github.com/Lifted-Truck/agent-knowledge-loop) | current |
| [governor/](governor/) | Watchdog + curator + coherence critic | **to build** — spec in DESIGN §4 |
| [research/](research/) | The evidence base: research reports with primary-source citations | current |
| [archive/kit-v1/](archive/kit-v1/) | Best-practices kit v1, frozen for reference during the v2 build | archived |

## The design in one paragraph

Models are replaceable workers inside a deterministic scaffold. Work is
partitioned into **organs** — bounded modules with enforced write territories,
versioned contracts as their only seams, and a resident
implementer/verifier/critic loop run in fresh-context shifts. Coordination is
stigmergic (task ledger + contract commits + serialized merge queue — no live
agent-to-agent messaging). Memory runs as per-organ knowledge loops harvested
upward by an audit loop and proliferated downward by a curator, behind
anti-poisoning gates. A **governor** — deterministic watchdog (halt triggers,
budgets, enforced outside any agent's process), model curator, and
fresh-context coherence critic — keeps the fleet honest, and every
consequential guard is technically enforced, never prose. See
[DESIGN.md](DESIGN.md) for the full design and
[research/](research/) for why each choice is what it is.

## Maintenance

This repo is curated by a standing integrator role (currently Claude, per the
project memory): canonical-copy discipline, README freshness, DECISIONS as the
append-only trail, periodic dedup sweeps. If you find the same content in two
places, one of them is a bug — file it.
