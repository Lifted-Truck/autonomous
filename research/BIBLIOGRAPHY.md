# Research bibliography (dated ledger)

Running, dated record of every research pass and its primary sources. Each
pass appends a dated section; entries are one line each and link the full
report where the source is discussed. The landscape-audit loop (ROADMAP
deferred) consumes and extends this file — its per-topic "last checked" dates
live here.

**Convention:** a source appears under the date it was consulted. Re-consulting
under a later pass gets a new entry (consensus drift is the point of dating).

---

## 2026-07-08 — Promote-up knowledge loops (audit-loop research)

~50 primary sources across LLM-agent memory and human-organization
lessons-learned literatures (Army AAR/CALL, GAO, SRE postmortem culture,
pattern languages, SECI, CoP, Spotify model, golden paths, Tech Radar/ADR;
Generative Agents, ExpeL, AWM, RAPTOR, G-Memory, Agent-KB, H²R, Zep/Graphiti,
LongMemEval; PoisonedRAG, AgentPoison, MINJA, RobustRAG, OWASP ASI06).
Canonical annotated list: `audit-loop-research.md` in
[agent-knowledge-loop](https://github.com/Lifted-Truck/agent-knowledge-loop)
(not duplicated here).

## 2026-07-10 — Multi-agent systems survey

Report: [2026-07-10-multiagent-systems-survey.md](2026-07-10-multiagent-systems-survey.md)

**Anthropic first-party:**
- How we built our multi-agent research system — https://www.anthropic.com/engineering/multi-agent-research-system
- Effective context engineering for AI agents — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Effective harnesses for long-running agents — https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Harness design for long-running app development — https://www.anthropic.com/engineering/harness-design-long-running-apps (coverage: https://www.infoq.com/news/2026/04/anthropic-three-agent-harness-ai/)
- Claude Code best practices — https://code.claude.com/docs/en/best-practices

**Cognition / the debate:**
- Don't Build Multi-Agents (Walden Yan) — https://cognition.ai/blog/dont-build-multi-agents
- LangChain: How and when to build multi-agent systems — https://blog.langchain.com/how-and-when-to-build-multi-agent-systems/
- Devin independent eval coverage — https://www.theregister.com/2025/01/23/ai_developer_devin_poor_reviews/ · https://futurism.com/first-ai-software-engineer-devin-bungling-tasks
- Devin's 2025 Performance Review — https://cognition.ai/blog/devin-annual-performance-review-2025

**Academic / OSS:**
- MetaGPT — https://arxiv.org/abs/2308.00352
- ChatDev — https://arxiv.org/abs/2307.07924 (failure analysis: https://christophermeiklejohn.com/ai/agents/mas-series/2026/04/26/mas-series-03-wave-one.html)
- CAMEL — https://arxiv.org/abs/2303.17760
- AutoGen — https://arxiv.org/abs/2308.08155
- SWE-agent (ACI) — https://arxiv.org/abs/2405.15793
- OpenHands — https://arxiv.org/html/2511.03690v1
- AgentCoder — https://arxiv.org/abs/2312.13010
- MAST: Why Do Multi-Agent LLM Systems Fail? — https://arxiv.org/abs/2503.13657

**Industry fleets:**
- Factory.ai Code Droid technical report — https://factory.ai/news/code-droid-technical-report
- Sweep (postmortem signals) — https://github.com/sweepai/sweep · https://news.ycombinator.com/item?id=43490121
- Gas Town (Steve Yegge) — https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04
- Ralph Wiggum loops — https://ghuntley.com/ralph/ · https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md · https://www.theregister.com/2026/01/27/ralph_wiggum_claude_loops/
- Worktree fleet experience — https://www.developersdigest.tech/blog/git-worktrees-claude-code-parallel-agents-guide · https://medium.com/@ooi_yee_fei/parallel-ai-development-with-git-worktrees-f2524afc3e33 · https://addyosmani.com/blog/claude-code-agent-teams/

## 2026-07-10 — Coordination & isolation mechanics

Report: [2026-07-10-coordination-isolation.md](2026-07-10-coordination-isolation.md)

**Isolation & merging:**
- Claude Code worktrees — https://code.claude.com/docs/en/worktrees
- Git worktrees for parallel agents — https://www.augmentcode.com/guides/git-worktrees-parallel-ai-agent-execution · https://www.mindstudio.ai/blog/parallel-ai-coding-agents-git-worktrees
- bors-ng — https://github.com/bors-ng/bors-ng
- Origin of merge queues — https://mergify.com/blog/the-origin-story-of-merge-queues
- Merge Queues Were Built for Humans (Danjou; "green is not coherent") — https://julien.danjou.info/blog/merge-queues-built-for-humans/
- Outgrowing GitHub merge queue — https://trunk.io/blog/outgrowing-github-merge-queue

**Boundaries & contracts:**
- Nx enforce-module-boundaries — https://nx.dev/docs/features/enforce-module-boundaries (approaches compared: https://www.stefanos-lignos.dev/posts/nx-module-boundaries)
- The shared library is a lie — https://dev.to/abdelaaziz_ouakala/the-shared-library-is-a-lie-fixing-your-nx-monorepo-architecture-3mie
- Coordinating multiple Claude Code agents (interface-first) — https://dev.to/alanwest/how-to-coordinate-multiple-claude-code-agents-without-losing-your-mind-1i9f
- Pact / consumer-driven contracts — https://docs.pact.io/ · https://pactflow.io/what-is-consumer-driven-contract-testing/
- Schema-registry contract testing — https://oneuptime.com/blog/post/2026-01-30-schema-registry-contract-testing/view
- Contracts Over Classes — https://medium.com/software-architecture-in-the-age-of-ai/contracts-over-classes-architecting-for-ai-understanding-not-just-developer-comfort-646882ebb93c

**Communication & task ledgers:**
- tick-md (markdown coordination) — https://purplehorizons.io/blog/tick-md-multi-agent-coordination-markdown
- Markdown as agent task format — https://dev.to/battyterm/the-case-for-markdown-as-your-agents-task-format-6mp
- Beads — https://betterstack.com/community/guides/ai/beads-issue-tracker-ai-agents/ · https://ianbull.com/posts/beads/
- LLM blackboard systems — https://arxiv.org/abs/2510.01285 · CodeCRDT https://arxiv.org/pdf/2510.18893

**CI as arbiter:**
- Code Review Is Dead (verification not approval) — https://blog.codacy.com/code-review-is-dead-why-ai-generated-code-needs-verification-not-human-approval
- Quality gates for AI-generated code — https://axiomstudio.ai/blog/quality-gates-for-ai-generated-code-automated-review-and-compliance
- Flaky quarantine — https://trunk.io/flaky-tests · https://flakyguard.com/blog/how-to-quarantine-flaky-tests · https://www.atlassian.com/blog/atlassian-engineering/taming-test-flakiness-how-we-built-a-scalable-tool-to-detect-and-manage-flaky-tests

**Topologies:**
- Team Topologies in the AI era — https://prommer.net/en/tech/guides/team-topologies-ai-era/ · https://prompt-pals.com/blog/team-topology-for-ai-agents
- Conway's law for agentic AI — https://medium.com/@amine.aitelharraj/-3eb5cd3dbcea

## 2026-07-10 — Memory & governance

Report: [2026-07-10-memory-governance.md](2026-07-10-memory-governance.md)

**Memory architectures:**
- MemGPT/Letta — https://lin-guanguo.github.io/llm-memory-research/letta.research/ · survey https://serokell.io/blog/design-patterns-for-long-term-memory-in-llm-powered-architectures
- Generative Agents — https://ar5iv.labs.arxiv.org/html/2304.03442
- Reflexion (failure post-mortems, +11pts) — https://medium.com/@Micheal-Lanham/memory-not-magic-what-agents-actually-remember-between-sessions-c05dadb53dc7
- Voyager (executable skill library) — https://arxiv.org/abs/2305.16291 · https://voyager.minedojo.org/

**Claude Code / context practices:**
- Claude Code memory docs — https://code.claude.com/docs/en/memory · slot-ceiling guide https://skillsplayground.com/guides/claude-code-memory/
- Auto-memory + hooks — https://yuanchang.org/en/posts/claude-code-auto-memory-and-hooks/ · https://medium.com/data-science-collective/claude-code-memory-management-the-complete-guide-2026-b0df6300c4e8
- Context rot (Chroma) — https://www.trychroma.com/research/context-rot · https://particula.tech/blog/chroma-context-rot-long-context-degradation

**Knowledge sharing & failure modes:**
- Agent knowledge-base anatomy — https://www.infoworld.com/article/4091400/anatomy-of-an-ai-agent-knowledge-base.html · https://ai.riera.co.uk/architecture/multi_agent_knowledgeops/
- Docs-as-code freshness — https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2 · https://openai.com/index/harness-engineering/ · https://dev.to/itlackey/building-agent-knowledge-bases-that-actually-scale-23pb
- Memory bloat (13% vs 39%) — https://tianpan.co/blog/2026-04-12-the-forgetting-problem-when-agent-memory-becomes-a-liability · https://arxiv.org/html/2603.11768v1
- Stale facts / poisoning — https://arxiv.org/pdf/2606.01435 · MemoryGraft https://arxiv.org/pdf/2512.16962
- Safety erosion with memory age — https://arxiv.org/html/2605.17830v1

**Governance & halting:**
- Circuit breakers — https://dev.to/waxell/ai-agent-circuit-breakers-the-reliability-pattern-production-teams-are-missing-5bpg · https://fountaincity.tech/resources/blog/ai-agent-cost-circuit-breaker/ · rate-based https://www.baristalabs.io/blog/ai-agent-spend-circuit-breaker
- Loop/no-progress detection — https://docs.bswen.com/blog/2026-03-11-prevent-ai-agent-infinite-loops/ · https://falconer.com/guides/agent-loops/
- Anthropic trustworthy-agents framework — https://www.anthropic.com/news/our-framework-for-developing-safe-and-trustworthy-agents · https://www.anthropic.com/research/trustworthy-agents
- Anthropic measuring agent autonomy — https://www.anthropic.com/research/measuring-agent-autonomy
- OpenAI Practices for Governing Agentic AI — https://openai.com/index/practices-for-governing-agentic-ai-systems/
- DeepMind safely interruptible agents — https://intelligence.org/files/Interruptibility.pdf
- Replit incident — https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/ · https://medium.com/@neerupujari5/inside-the-replit-ai-catastrophe-438e0f63b21c
- Runaway costs — https://www.supra-wall.com/en/learn/ai-agent-runaway-costs · https://www.nexgismo.com/blog/ai-agent-budget-guards-stop-runaway-api-costs · https://devtoolpicks.com/blog/ai-agents-runaway-claude-code-bills-overnight-2026
- GitClear code-quality data — https://www.gitclear.com/ai_assistant_code_quality_2025_research · https://www.gitclear.com/the_ai_code_quality_maintainability_gap
- Agent metrics — https://www.augmentcode.com/tools/autonomous-development-metrics-kpis-that-matter-for-ai-assisted-engineering-teams · https://www.braintrust.dev/articles/ai-agent-evaluation-framework
