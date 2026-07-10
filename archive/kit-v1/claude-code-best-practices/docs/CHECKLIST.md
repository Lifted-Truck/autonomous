# Getting-started checklist

The article's 10-step rollout, turned into a trackable list. The bootstrap does the
mechanical parts (marked ⚙️ auto); the rest are judgement calls only a human can make.

Copy this file into the target repo and check items off as you go.

- [ ] **1. Layered CLAUDE.md** ⚙️ auto — then edit: strip generic advice, keep only
      pointers + gotchas. Add a subdir `CLAUDE.md` to each major area with its own
      conventions.
- [ ] **2. Install an LSP** for the repo's primary language(s). Critical for
      multi-language codebases (C/C++/C#/Java) so Claude resolves symbols instead of
      pattern-matching identically named functions. (Manual — no file to scaffold.)
- [ ] **3. `.claudeignore`** ⚙️ auto — then review: exclude generated code, build
      artifacts, vendored deps, large fixtures. Commit it.
- [ ] **4. Initial skills** for specialized domains. ⚙️ a template skill is dropped in
      `.claude/skills/` — rename it, scope its description to the right paths, and
      write the actual procedure.
- [ ] **5. 1–2 pilot MCP servers** for internal tools (docs, tickets, search). ⚙️ a
      `.mcp.json` template is dropped in — wire it to a real server or delete it.
- [ ] **6. Assign config ownership.** Name a DRI in [GOVERNANCE.md](GOVERNANCE.md).
- [ ] **7. Code-review + governance policy.** Review Claude-generated code to the
      same standard as human code. Define approved skills/plugins. Start with limited
      access.
- [ ] **8. Plan rollout** with a dedicated infra owner before going broad.
- [ ] **9. Distribute via a plugin/marketplace** so every engineer gets an identical
      setup on day one. (This kit is the pre-plugin source of truth.)
- [ ] **10. Monitor & iterate quarterly.** Schedule the 3–6 month config review
      (GOVERNANCE.md review log).

## Verify the harness actually works

After bootstrapping, sanity-check the deterministic pieces:

- [ ] Make a trivial edit to a source file → confirm the **format/lint hook** ran.
- [ ] Start a fresh Claude session → confirm the **CODEMAP** shows up in context
      (SessionStart hook).
- [ ] Ask Claude to "map subsystem X without editing" → confirm the
      **codebase-mapper** subagent is used.
