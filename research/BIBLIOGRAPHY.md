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

## 2026-07-11 — Landscape audit (monthly, first run)

Report: [proposals/2026-07-11.proposal.md](proposals/2026-07-11.proposal.md).
Six fan-out agents, each scoped to "what changed since <topic's last-checked
date>" (2026-07-08/07-10). Window was 1–3 days; most sources below predate
the strict window and are recorded because they are not yet cited in
`doctrine/`/`DESIGN.md`/`research/`, not because they are new-this-week.

**Multi-agent coordination:**
- Cognition, "Multi-Agents: What's Actually Working" (follow-up to "Don't
  Build Multi-Agents") — https://cognition.com/blog/multi-agents-working
  (fetch blocked, via search snippets)
- UIUC multi-agent token-multiplier study (4–220× range) — via
  https://www.augmentcode.com/guides/git-worktrees-parallel-ai-agent-execution
  (secondary; primary not located)
- RecursiveMAS (embedding-space agent communication, −34–75% tokens) —
  https://arxiv.org/abs/2604.25917 (via VentureBeat coverage)
- Overstory (worktree-fleet orchestrator, archived 2026-05-28, superseded by
  "Warren") — https://github.com/jayminwest/overstory
- "GasTown and the Two Kinds of Multi-Agent" — https://paddo.dev (commentary
  on Gas Town's operational-roles model)
- "$47K agent loop" postmortem (11-day unbounded live-messaging loop,
  Nov 2025 incident) — forensic writeups on dev.to/clyro.dev, ~Apr–Jun 2026
- Fleet (parallel coding-agent supervisor: Beads/Dolt queue, multi-backend
  coder routing, ask_human MCP, context-pressure termination) —
  https://github.com/sermakarevich/fleet (user-recovered from the audit's
  blocked HN thread; reviewed 2026-07-11 — conductor prior art, see ROADMAP)

**Agent memory & knowledge loops:**
- Claude Code changelog v2.1.204–207 —
  https://code.claude.com/docs/en/changelog (`/doctor` CLAUDE.md-trim check,
  2026-07-09; hook shell-injection hardening, 2026-07-11)
- FARMA: Forged Reasoning Attacks on LLM Agent Memory —
  https://arxiv.org/abs/2607.05029 (~2026-07-06, fetch blocked)
- WhisperBench: Stealthy Memory Injection in Persistent Personal Agents —
  https://arxiv.org/abs/2607.05189 (~2026-07-06, fetch blocked)
- GhostWriter: Memory Poisoning Attacks on LLM Agents —
  https://arxiv.org/abs/2607.06595 (~2026-07-06, fetch blocked)
- AgentPrizm "AgentMemory" product launch (2026-07-09) — market signal only,
  no stable primary URL found

**Governance, halting, and agentic safety:**
- Future of Life Institute, "AI Safety Index — Summer 2026" (2026-07-07) —
  https://futureoflife.org/ai-safety-index-summer-2026/
- Adversa AI, "GuardFall" open-source coding-agent guard bypass
  (2026-06-30) —
  https://thehackernews.com/2026/06/guardfall-exposes-open-source-ai-coding.html
- Claude Code GitHub Action permission-check bypass, patched in
  claude-code-action v1.0.94 (2026-06) —
  https://thehackernews.com/2026/06/claude-code-github-action-flaw-let-one.html
- Google DeepMind, "Securing internal systems against increasingly capable
  and imperfectly aligned AI" / AI Control Roadmap (2026-06-18) —
  https://deepmind.google/blog/securing-the-future-of-ai-agents/
- Sen. Mark Warner, discussion draft "AI AGENT Act" (2026-06-29) —
  https://www.warner.senate.gov/newsroom/press-releases/warner-unveils-discussion-draft-of-legislation-to-create-innovative-market-for-secure-artificial-intelligence-agents/
- Bank of England, agentic-AI trading "kill switch" feasibility study
  (2026-07-01) —
  https://www.resultsense.com/news/2026-07-01-boe-breeden-agentic-ai-kill-switch/
- Sysdig "agentic ransomware" claim (2026-07-02) — unverified, aggregator
  mentions only, no primary reached
- Cloud Security Alliance, "Autonomy Levels Framework" reversibility
  critique (~March 2026, fetch blocked) —
  labs.cloudsecurityalliance.org

**Verification and CI-as-arbiter:**
- METR, "GPT-5.6 Sol pre-deployment evaluation" (2026-06-26) —
  https://metr.org/blog/2026-06-26-gpt-5-6-sol/
- OpenAI, "Why we no longer evaluate against SWE-bench Verified"
  (2026-02-23) —
  https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/
- "Reward Hacking Benchmark (RHB)" (2026-05-04) —
  https://arxiv.org/abs/2605.02964
- "The Verification Horizon: No Silver Bullet for Coding Agent Rewards"
  (~2026-06) — https://arxiv.org/abs/2606.26300 (fetch blocked)
- "Auditing Reward Hackability in Code RL Training Environments" (~2026-06)
  — https://arxiv.org/abs/2606.16062 (fetch blocked)
- "Understanding Dominant Themes in Reviewing Agentic AI-authored Code"
  (2026-01) — https://arxiv.org/abs/2601.19287
- Code Review Agent Benchmark / c-CRAB (~2026-03) —
  https://arxiv.org/abs/2603.23448
- "Why Are Agentic Pull Requests Merged or Rejected? An Empirical Study"
  (2026-05) — https://arxiv.org/abs/2605.22534
- Trunk.io changelog (incremental flaky-test tooling, no confirmed
  in-window release) — https://trunk.io

**Context engineering and harness design:**
- Claude Code changelog v2.1.206 (2026-07-09) / v2.1.207 (2026-07-11) —
  https://code.claude.com/docs/en/changelog
- Practitioner critique of CLAUDE.md compliance (dev.to, date unconfirmed,
  fetch blocked) — dev.to/minatoplanb

**Open-scope — new categories:**
- OpenAI, GPT-5.6 tiered release (Sol/Terra/Luna) (2026-07-08/09) —
  https://openai.com/index/gpt-5-6/ ,
  https://openai.com/index/previewing-gpt-5-6-sol/ ,
  https://www.cnbc.com/2026/07/08/openai-expanding-gpt-5point6-ai-model-release-ending-government-limits.html
- xAI/Cursor, Grok 4.5 launch (2026-07-08) —
  https://x.ai/news/grok-4-5 , https://cursor.com/blog/grok-4-5 ,
  https://devops.com/spacexais-grok-4-5-undercuts-anthropic-and-openai-on-coding-agent-pricing/
- SpaceX to acquire Cursor/Anysphere, $60B (2026-06-16) —
  https://www.cnbc.com/2026/06/16/spacex-spcx-cursor-acquisition-ipo.html ,
  https://www.forbes.com/sites/sandycarter/2026/06/16/spacex-buys-cursor-in-largest-startup-acquisition-ever-at-60-billion/
- Anthropic, Fable 5 / Mythos 5 launch, export-control shutdown and reversal
  (2026-06-12 through 06-30) —
  https://www.washingtonpost.com/technology/2026/06/30/white-house-drops-export-controls-anthropics-mythos-fable-ai-models/
  , https://www.cnn.com/2026/06/30/tech/anthropic-export-control-ban-lifted-white-house
  , https://www.pbs.org/newshour/show/anthropic-disabled-fable-5-and-mythos-5-after-a-us-security-directive
- Anthropic, "Claude Sonnet 5" (2026-06-30) —
  https://www.anthropic.com/news/claude-sonnet-5
- METR, "Time Horizon 1.1" (2026-01-29/02-21) —
  https://metr.org/blog/2026-1-29-time-horizon-1-1/
- MCP release candidate — stateless protocol layer, Extensions framework
  (2026-07-28 RC) — https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/
- MCP donated to the Agentic AI Foundation / Linux Foundation (2025-12-09) —
  https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation
- Agent identity/payment protocol consolidation (Mastercard Agent Pay, Visa
  Trusted Agent Protocol, Google AP2, MCP-I, W3C Agent Identity Registry) —
  https://www.biometricupdate.com/202603/vendors-race-to-build-identity-stack-for-agentic-ai
  , https://www.w3.org/community/agent-identity/
- Vercel, "eve" durable-workflow agent framework (2026-06-17) —
  https://vercel.com/blog/introducing-eve
- AI-agent liability insurance market forming (Corgi, Testudo, Armilla,
  Klaimee) — https://www.factmr.com/report/ai-agent-liability-insurance-services-market

## 2026-07-13 — Human-AI epistemics (harvested, not web-researched)

Report: [2026-07-13-human-ai-epistemics-delegate52.md](2026-07-13-human-ai-epistemics-delegate52.md).
Source: the user's own methodology document "The Applied Epistemics of AI
Integration" (canonical in the sibling `ai-integration-methodology/` project),
NOT a web pass — so these are attributed to that document, and where it cites a
primary the primary is flagged for verification.

- DELEGATE-52 benchmark (19 models × 52 domains × 20 interactions; invisible
  failure in stronger models; ~80% of loss in sparse catastrophic collapses;
  agentic tools worsened performance ~6pts absent tight scoping) — attributed
  to "2026 Microsoft Research"; **primary URL not located / not verified in
  this harvest — landscape-audit TODO.**
- Illusion of explanatory depth (Rozenblit & Keil lineage) — via the doc.
- Attractor-basin / basin-escape account of LLM generation — the doc's own
  synthesis; mechanism-level, not a single citable paper.
- Seven-mode failure taxonomy (Consensus Trap, XY-at-scale, Competency Erosion,
  Invisible Dependency, Confidence Spiral, Translation Gap, Remediation Cliff)
  — the doc's framework.
