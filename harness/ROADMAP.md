# ROADMAP — {{PROJECT_NAME}}

Single source of truth. Only the lead session (or the human) edits this file.
State lives here; conversations are ephemeral.

## Status

- **Phase:** {{e.g. prototype / hardening / shipped-maintenance}}
- **Oracle:** {{what ./verify fast and full currently cover; known gaps}}
- **Last human ratification:** {{date — when a human last reviewed this file}}

## Invariants under active protection

<!-- Duplicated from CLAUDE.md §Domain only when an invariant is at risk from
     current queue items; otherwise just point to the charter. -->

## Queue

<!-- One block per item. An item without acceptance criteria is not workable —
     writing the criteria IS the first task. IDs are permanent; never reuse. -->

### Q-001 — {{title}}
- **Status:** open | in-progress | blocked | done (trace: <file>)
- **Scope:** {{files/modules}}
- **Acceptance criteria:**
  1. {{machine-checkable where possible; name the verify gate that checks it}}
  2. {{...}}
- **Out of scope:** {{explicit exclusions}}
- **Open questions:** {{...}}

## Decision log

<!-- One line per ratified decision, newest first, linking to traces/. -->
- {{YYYY-MM-DD}} — {{decision}} (trace: {{file}})

## Graduation criteria

<!-- Your prototype→agent-queue handoff test, made explicit per-project:
     this project graduates from interactive prototyping to autonomous queue
     work when the remaining open questions are infrastructure problems
     rather than audible/perceptual/judgment ones. List what's still in the
     judgment column. -->
