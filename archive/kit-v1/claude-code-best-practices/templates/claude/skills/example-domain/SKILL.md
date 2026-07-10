---
name: example-domain
description: >-
  REPLACE THIS. A path-scoped skill template. Write a description that names the
  exact trigger so the skill activates only in the relevant area — e.g. "Use when
  modifying database migrations under db/migrations. Covers our naming convention,
  reversibility rules, and the review checklist." Progressive disclosure: this file
  stays out of context until the description matches the task, so be specific about
  WHEN to use and WHEN to skip.
---

# Example domain skill

> This is a template. Rename the folder, rewrite the frontmatter `description`
> (that's what controls triggering), and replace the body with the real procedure.

## When to use

- Specific paths / file types this applies to (e.g. `src/payments/**`).
- The concrete task that should trigger it.

## When NOT to use

- Adjacent cases that look similar but should be handled differently.

## Procedure

1. _Step._
2. _Step._

## Conventions / gotchas for this domain

- _The domain-specific knowledge that's too detailed for CLAUDE.md but essential
  when you're actually doing this task._

## Reference (progressive disclosure)

Keep this SKILL.md short. Put long material (schemas, examples, checklists) in
sibling files and link them so they load only when needed:

- `./reference.md` — _detailed reference, loaded on demand_
