# research — the evidence base

Reports preserved verbatim (with URLs) as the citable foundation for design
choices and kit-v2's INSIGHTS. Summaries live in [DESIGN.md](../DESIGN.md);
these are the sources.

**[BIBLIOGRAPHY.md](BIBLIOGRAPHY.md)** is the dated ledger of every research
pass and its sources — the landscape-audit loop (ROADMAP deferred) appends to
it and reads its per-topic last-checked dates.

- [2026-07-10-multiagent-systems-survey.md](2026-07-10-multiagent-systems-survey.md)
  — what worked/failed across Anthropic, Cognition/Devin, MetaGPT/ChatDev/
  AutoGen/CAMEL, SWE-agent, OpenHands, AgentCoder, MAST, Factory, Sweep,
  Gas Town/Beads, Ralph loops, worktree fleets. 12 load-bearing lessons.
- [2026-07-10-coordination-isolation.md](2026-07-10-coordination-isolation.md)
  — worktrees, merge queues, boundary linters, contracts (interface-first,
  Pact/CDC), stigmergy/blackboard, CI-as-arbiter and its holes, team
  topologies. Recommended minimal stack for 3–8 agents.
- [2026-07-10-memory-governance.md](2026-07-10-memory-governance.md)
  — memory architectures (MemGPT, Generative Agents, Reflexion, Voyager),
  Claude Code practices, context rot, bloat/poisoning numbers; circuit
  breakers, lab guidance, incident record, governor metrics, ranked halt
  triggers.
- **Audit-loop research** (2026-07-08) — canonical in
  [agent-knowledge-loop](https://github.com/Lifted-Truck/agent-knowledge-loop)
  (`audit-loop-research.md`): promote-up loops across LLM-memory and
  human-organization literatures; memory-poisoning defenses; the 12 design
  principles.
