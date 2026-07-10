# Survey: Real-World Multi-Agent / Autonomous Software Development Systems

> Research agent report, 2026-07-10. Commissioned for the autonomous-paradigm
> infrastructure design (see ../DESIGN.md). Web research; URLs preserved.

## 1. Anthropic (first-party engineering)

### "How we built our multi-agent research system" (June 2025)
https://www.anthropic.com/engineering/multi-agent-research-system
**Coordination:** Orchestrator-worker. A lead agent plans with extended thinking, decomposes the query, and spawns 3-5 parallel subagents, each with its own context window, explicit objective, output format, tool guidance, and task boundaries; results funnel back through the lead, with the plan persisted to external memory before context truncation.
**Lessons:** Parallelism cut research time up to 90% and multi-agent beat single-agent Opus by 90.2% on their internal eval — but only because research is a *read/parallel-search* task. Costs are brutal: agents use ~4x chat tokens, multi-agent ~15x; token spend explains ~80% of performance variance. Failure modes: vague delegation → duplicated work; 50 subagents spawned for trivial queries; endless searching for nonexistent facts; no way to steer running subagents; "minor system failures are catastrophic" without durable execution/resumption; debugging demands full production tracing. Fixes were mostly *prompt-embedded heuristics* (explicit effort-scaling rules, delegation criteria) not hard rules.

### "Effective context engineering for AI agents" (Sept 2025)
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
**Coordination:** Not a system, but the doctrine underlying all of Anthropic's designs: context is a finite attention budget that suffers "context rot" as it fills.
**Lessons:** Three long-horizon techniques — compaction, structured note-taking (external memory files), and subagents whose whole purpose is *context isolation*: explore in a clean window, return a condensed summary. Just-in-time retrieval via lightweight identifiers beats pre-loading everything. Subagents are justified when parallel *exploration* pays; not for parallel writing.

### "Effective harnesses for long-running agents" (Nov 2025)
https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
**Coordination:** Sequential shifts, not parallel agents: an initializer agent sets up the environment (git repo, JSON feature list with 200+ items all `passes: false`, progress log, init script), then a coding agent runs session after session, one feature per session, leaving mergeable state.
**Lessons:** Compaction alone is insufficient for multi-day work — full context resets against structured handoff artifacts (like onboarding a new shift engineer) are what work. Observed failures: premature victory declaration (fixed by explicit pass/fail feature tracking), undocumented half-done work (fixed by mandatory commits/progress updates), doomed one-shot mega-attempts (fixed by prompting for incremental scope), claiming features work without testing (fixed by Puppeteer end-to-end checks).

### "Harness design for long-running application development" (2026 follow-up; see also InfoQ coverage)
https://www.anthropic.com/engineering/harness-design-long-running-apps · https://www.infoq.com/news/2026/04/anthropic-three-agent-harness-ai/
**Coordination:** Three agents — Planner (spec expansion), Generator (implements, negotiates "sprint contracts"), Evaluator (drives the running app via Playwright and grades it).
**Lessons:** The decisive upgrade was *separating evaluation from generation*: agents "confidently praise" their own mediocre work, so the grader must not be the author — and even then, unaided Claude was "a poor QA agent" until the evaluator prompt was iterated. Full resets beat compaction again ("context anxiety" persisted under compaction on Sonnet 4.5). Better results, significantly higher cost.

### Claude Code best practices (subagents, parallel sessions)
https://code.claude.com/docs/en/best-practices
**Coordination:** Single main thread by default; subagents for read-heavy investigation and adversarial review in fresh contexts; horizontal scale via git worktrees, headless `claude -p` fan-out over file lists, Writer/Reviewer paired sessions, and (newer) agent teams.
**Lessons:** Everything derives from one constraint — context fills and performance degrades. The single most load-bearing practice: "give Claude a check it can run" (tests, build, screenshot diff), escalating from prompt-level to Stop hooks to a fresh-context verification subagent, and demand *evidence* not assertions. Fresh-context review beats self-review because the reviewer isn't biased toward code it just wrote; but over-eager reviewers hallucinate gaps, so scope them to correctness only. Fan-out recipe: test the prompt on 2-3 files, then run on 2,000.

## 2. Cognition and the counterarguments

### "Don't Build Multi-Agents" (Walden Yan, June 2025)
https://cognition.ai/blog/dont-build-multi-agents
**Coordination (advocated):** Single-threaded linear agent carrying full history; for very long tasks, a dedicated context-compression model distills the trace. Two principles: share full agent traces (not summaries of messages), and remember that *actions carry implicit decisions* — parallel agents making unshared decisions produce conflicting work.
**Lessons:** The Flappy Bird example: two subagents each misinterpret their slice (Mario-style background, wrong-looking bird) and the merge agent inherits irreconcilable assumptions. They note Claude Code's then-design (subagents only *answer questions*, never write in parallel) and the death of edit-apply model splits as supporting evidence. Verdict circa 2025: parallel-writing multi-agents are fragile; reliability comes from one agent seeing everything.

### The reconciliation: LangChain, "How and when to build multi-agent systems"
https://blog.langchain.com/how-and-when-to-build-multi-agent-systems/
Resolves the apparent Cognition-vs-Anthropic contradiction: **read tasks parallelize; write tasks don't.** Anthropic's system parallelizes *research* (reads, merged by one writer); Devin does *coding* (writes, where merging divergent outputs coherently is the hard part). Both camps agree the real discipline is context engineering.

### Devin in practice
- Answer.AI independent evaluation (via https://www.theregister.com/2025/01/23/ai_developer_devin_poor_reviews/ , https://futurism.com/first-ai-software-engineer-devin-bungling-tasks): 3/20 tasks succeeded, 14 failed; worst property was *unpredictability* — no way to tell in advance which tasks would fail, and Devin spent days pursuing impossible paths instead of recognizing blockers.
- Cognition's own "Devin's 2025 Performance Review" (https://cognition.ai/blog/devin-annual-performance-review-2025): sweet spot is "clear upfront requirements + verifiable outcome + junior-engineer 4-8h scope." PR merge rate rose 34% → 67%; 20x speedups on mechanical security fixes and migrations. Fails at ambiguity and mid-task requirement changes; human verification stays mandatory wherever quality isn't mechanically checkable. Parallelism pays *after* scoping: "a fleet of Devins can execute on every repo in parallel" for uniform tasks (migrations, doc generation across 400k repos).

## 3. Academic / OSS systems

### MetaGPT (ICLR 2024)
https://arxiv.org/abs/2308.00352
**Coordination:** "Code = SOP(Team)" — waterfall roles (PM, Architect, Engineer, QA) exchanging *structured artifacts* (PRDs, design docs, interface definitions) through a shared message pool with publish-subscribe, instead of free-form chat.
**Lessons:** Structured documents drastically reduce information distortion versus dialogue; executable feedback (run the code, feed errors back) added +4-5% Pass@1 — verification mattered more than the org chart. 85.9%/87.7% on HumanEval/MBPP; on its SoftwareDev benchmark it beat ChatDev with fewer human revisions (0.83 vs 2.5/project). Rigid SOP = no recovery path when the pipeline derails.

### ChatDev (ACL 2024)
https://arxiv.org/abs/2307.07924
**Coordination:** Virtual software company; waterfall phases decomposed into pairwise "chat chains"; "communicative dehallucination" (ask clarifying questions before answering) to cut coding hallucinations.
**Lessons:** Produced only toy software (avg ~131 LoC); when a pairwise chat fails to converge in 10 rounds the system simply stops — no escalation, no stuck-detection (see analysis: https://christophermeiklejohn.com/ai/agents/mas-series/2026/04/26/mas-series-03-wave-one.html). Demonstrated that role-play alone doesn't add capability; dehallucination-by-clarification was the one durable idea.

### CAMEL (NeurIPS 2023)
https://arxiv.org/abs/2303.17760
**Coordination:** Two agents role-play user/assistant, held in character by "inception prompting."
**Lessons:** Canonical catalog of conversational-coordination failures — role flipping, instruction repetition, vague replies, infinite loops — with only prompt-level mitigations and no structural enforcement. The field's takeaway: free-text agent-to-agent chat is an unreliable protocol; treat inter-agent communication like an API.

### AutoGen (Microsoft)
https://arxiv.org/abs/2308.08155
**Coordination:** "Conversation programming" — conversable agents composed into sequential, group-chat, or nested patterns; framework is unopinionated plumbing.
**Lessons:** Aged better than SOP frameworks precisely because it doesn't prescribe an architecture, but group chats routinely exhibited infinite death-spirals (coder regenerates the same broken code 50 times), goal drift, and breakdown past ~10-15 sequential steps unless termination/verification logic was added by the builder.

### SWE-agent (Princeton, 2024)
https://arxiv.org/abs/2405.15793
**Coordination:** Single agent; the innovation is the **Agent-Computer Interface** — purpose-built file viewer, search, and edit commands with guardrails (e.g., lint-on-edit).
**Lessons:** Interface design *is* performance: a good ACI raised SWE-bench scores more than model or prompt changes. Foundational evidence that harness > head-count.

### OpenHands (ex-OpenDevin)
https://arxiv.org/html/2511.03690v1
**Coordination:** Single agent with bash/editor/browser (CodeAct: actions expressed as executable Python), controller-agent-runtime separation; SDK is stateless and event-sourced.
**Lessons:** Their production lessons are software-engineering ones: event-sourced state for reproducibility and fault recovery, immutable config, strict core/application separation. They stayed single-agent for coding; multi-agent delegation experiments were largely retired as not worth the complexity.

### AgentCoder (2023/24)
https://arxiv.org/abs/2312.13010
**Coordination:** Exactly three agents — programmer, *independent* test designer, test executor — in a refinement loop.
**Lessons:** 96.3% pass@1 on HumanEval at 56.9K tokens vs MetaGPT's 138K and ChatDev's 183K: the minimal decomposition that separates test-writing from code-writing beats elaborate role hierarchies on both quality and cost. Independence of the tester is the active ingredient (self-written tests overfit).

### "Why Do Multi-Agent LLM Systems Fail?" (MAST, NeurIPS 2025)
https://arxiv.org/abs/2503.13657
**Coordination (studied):** 7 MAS frameworks, 1,600+ annotated traces, 14 failure modes in 3 classes.
**Lessons:** SOTA open-source MAS fail 41-87% of the time; ~42% of failures are *specification* problems, ~37% inter-agent misalignment, ~21% weak verification. Empirical confirmation that most "multi-agent failures" are actually spec and verification failures — org-chart redesign doesn't fix them.

## 4. Industry fleets and swarms

### Factory.ai
https://factory.ai/news/code-droid-technical-report
**Coordination:** Droids (Code, Reliability, Knowledge) over a shared enterprise context layer (HyperCode codebase model, ByteRank retrieval, live Jira/GitHub/Slack indexing); multi-model sampling with selection; three graded autonomy levels (approve-everything → auto-apply reversible changes → full autonomy).
**Lessons:** Context beyond code is the moat — "giving agents only code is like onboarding an engineer by throwing them into a codebase." Fleet economics work on uniform, verifiable work (a 4-month migration compressed to 3.5 days). Autonomy is granted by *reversibility* of the change, not by trust in the model.

### Sweep
https://github.com/sweepai/sweep · https://news.ycombinator.com/item?id=43490121
**Coordination:** Async GitHub issue → PR agent (2023-24), later abandoned for a JetBrains in-IDE assistant.
**Lessons (postmortem):** Needed a well-defined spec to exceed ~90% task success, but developers won't write specs — they want to iterate live with the agent; async agents that take minutes lose the user's attention. The spec bottleneck killed the autonomous product shape, not model capability.

### Steve Yegge's Gas Town / Beads (Dec 2025-2026)
https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04 · https://sourcegraph.com (Beads: git-backed issue graph, Oct 2025)
**Coordination:** 20-30 Claude instances in fixed civic roles — Mayor (dispatch), ephemeral Polecats (produce MRs in isolated worktrees, then die), a Refinery (serialized merge queue that rebases as baseline drifts), Witness (unsticks stuck workers), Deacon (health patrols). All durable state lives in Beads (issues-as-JSON in git); workflows are persistent "molecules" that survive crashes and context exhaustion via handoff to fresh sessions.
**Lessons:** What it genuinely solves: durable memory, session handoff, merge serialization, and audit trail — claimed million-step workflows (20-disc Hanoi) via externalized state. What it admits: bugs fixed 2-3 times redundantly, fixes lost, agents ignoring their prompts, constant "hands-on-the-wheel" supervision — throughput-over-consistency by design. The architecture is an existence proof that *git + an external work graph + a serialized merge point* is the coordination substrate, and that a human overseer is still load-bearing.

### Ralph Wiggum loops (Geoffrey Huntley, 2025)
https://ghuntley.com/ralph/ · https://github.com/anthropics/claude-code/blob/main/plugins/ralph-wiggum/README.md · https://www.theregister.com/2026/01/27/ralph_wiggum_claude_loops/
**Coordination:** `while :; do cat PROMPT.md | claude ; done` — no orchestration at all; state lives entirely in the repo and PROMPT/plan files; every iteration is a fresh context.
**Lessons:** Fresh context per iteration is *the point*, not a side effect — it sidesteps context rot entirely and converts persistence into the repo. Whole projects (a compiler, ports of codebases) shipped this way; Anthropic productized it as the ralph-wiggum plugin and /loop. Weakness: needs a deterministic completion signal or it loops forever / declares false victory; failures are tolerated as "data."

### Worktree-based parallelism (community experience reports)
https://www.developersdigest.tech/blog/git-worktrees-claude-code-parallel-agents-guide · https://medium.com/@ooi_yee_fei/parallel-ai-development-with-git-worktrees-f2524afc3e33 · https://addyosmani.com/blog/claude-code-agent-teams/
**Lessons:** Without isolation, "every single time" multi-agent runs produced dirty trees and agents clobbering each other; one report describes a parallel agent silently breaking the shared test harness so all other agents' work looked regressed. Worktrees fix filesystem collisions but not *semantic* collisions: dependent tasks can't actually parallelize, and shared mutable resources (one dev database, migrations) reintroduce coupling that no worktree isolates. Claude Code's later "agent teams" added the missing layer: shared task list, messaging, and a lead.

---

## Synthesis: the load-bearing lessons for a fully-autonomous parallel dev system

1. **Parallelize reads, serialize writes.** Fan out research/exploration/testing; keep one decision-making writer per artifact, or serialize merges through a single queue. (LangChain read/write analysis; Anthropic research system; Cognition "Don't Build Multi-Agents"; Gas Town's Refinery.)
2. **Actions carry implicit decisions — so share full traces or don't share the task.** Parallel writers with partial context produce coherently wrong, unmergeable work (Flappy Bird/Mario). If subagents must write, give them non-overlapping, dependency-free scopes. (Cognition; worktree experience reports.)
3. **The verifier must not be the author, and it must be a *check the agent can run*.** Agents confidently praise their own mediocre work; independent test-designer/evaluator agents in fresh contexts, executable feedback, and evidence-not-assertion are the highest-ROI additions in nearly every system. (Anthropic three-agent harness; AgentCoder; MetaGPT executable feedback; Claude Code best practices; MAST's 21% verification failures.)
4. **Most "multi-agent failures" are specification failures.** ~42% in MAST; Sweep died on the spec bottleneck; Devin succeeds only with clear upfront requirements; Anthropic's subagents duplicated work until delegation included objective, format, tools, and boundaries. Spend design budget on task decomposition contracts, not roles. (MAST; Sweep; Cognition Devin review; Anthropic research system.)
5. **Context is the binding resource; engineer it explicitly.** Context rot degrades everything; use fresh contexts aggressively (subagents for exploration, /clear, Ralph's loop-with-fresh-context), and for multi-day work prefer **full resets against structured handoff artifacts** over compaction. (Anthropic context-engineering + both harness posts; Ralph Wiggum.)
6. **Externalize all coordination state into durable, git-native artifacts.** Feature lists with explicit pass/fail, progress logs, issue graphs (Beads), plans-in-repo — the filesystem/git is the shared memory; the model is stateless. This is what makes crashes, handoffs, and million-step workflows survivable. (Anthropic initializer/coder harness; Gas Town/Beads; Ralph.)
7. **Isolate the filesystem per agent (worktrees) but know it doesn't solve semantic conflicts.** Worktrees + a serialized merge point eliminate clobbering; shared DBs, migrations, test harnesses, and cross-task dependencies still couple agents and must be scheduled, not parallelized. (Worktree reports; Gas Town; Claude Code agent teams.)
8. **Structured artifacts beat free-form chat as the inter-agent protocol.** PRD/interface docs, JSON task objects, and typed messages reduce distortion; free-text role-play yields role flipping, loops, and cascading hallucination. Treat agent-to-agent communication like an API. (MetaGPT vs ChatDev/CAMEL; AutoGen loop failures.)
9. **Harness/interface design outranks agent count.** A better agent-computer interface (SWE-agent's ACI) or a better single-agent harness moved benchmarks more than adding roles; the minimal 3-agent AgentCoder beat elaborate companies at a third of the token cost; model upgrades beat token-budget doubling. (SWE-agent; AgentCoder; Anthropic research system.)
10. **Budget for the token multiplier and match architecture to task value.** Multi-agent ≈ 15x chat tokens; use swarms only where the task's value and verifiability justify it (migrations, security-fix fleets, uniform repo-wide changes), single-threaded agents elsewhere. (Anthropic research system; Devin performance review; Factory migrations.)
11. **Design for unpredictability: durable execution, tracing, reversibility-graded autonomy.** You cannot predict which tasks fail (Answer.AI on Devin); minor infra failures are catastrophic mid-run; so you need resumability, full production traces for debugging non-determinism, and autonomy tiers keyed to how reversible the change is. (Anthropic research system; Answer.AI/Devin; Factory autonomy levels.)
12. **Detect "stuck" and "falsely done" as first-class states.** Systems fail by looping (AutoGen death spirals), stopping without escalation (ChatDev's 10-round cutoff), declaring premature victory (Anthropic harness), or grinding for days on impossible tasks (Devin). Every loop needs an explicit completion oracle, a stuck-detector/escalation path (Gas Town's Witness), and a cap. (AutoGen; ChatDev; Anthropic harness; Devin; Gas Town.)

**Meta-lesson:** the systems that work treat the *model as a replaceable worker inside a deterministic scaffold* — externalized state in git, contracts for task scope, independent executable verification, serialized merges — while the systems that failed tried to get coordination from conversation and role-play.
