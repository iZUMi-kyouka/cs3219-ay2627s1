<span id="summary">

**Organising question:** how is AI changing the way software is engineered — and where does human judgment stay essential?

The lecture ("Recent trends in software engineering: AI in SE — autocomplete to autonomous agents") covers:

* five ways AI improves engineers' efficiency: automation, pattern detection, collaboration, delegation, orchestration
* AI across the SDLC: code generation, testing, maintenance — and requirements engineering
* real-world evidence (LLM4SE survey, Russo 2024, DORA 2025) and the risks: garbage-in-garbage-out, traceability, data safety, vulnerabilities, technical debt
* vibe coding and its trade-offs; what autonomous development needs (MCP and A2A protocols)

</span>

<span id="toc">

* [W2.1 AI across the software engineering workflow]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c1)
* [W2.2 AI in the SDLC: from code generation to requirements]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c2)
* [W2.3 What the evidence and the risks say]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c3)
* [W2.4 From assistants to autonomous development: MCP and A2A]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c4)

</span>

<span id="lecture">

### Lecture

**AI improves engineers' efficiency in five modes, and the review point moves with each mode.** Automation handles repeated tasks (CI/CD, infrastructure deployment); pattern detection exploits rule-like structure (sifting codebases for vulnerabilities); collaboration is turn-by-turn (Copilot, Copilot Chat); delegation moves review to the final output (Claude Code, Cursor); orchestration coordinates specialized agents (CrewAI, LangGraph) (slides 3–4) → [W2.1]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c1).

**Pattern detection is the deck's worked example.** Vulnerabilities come from repeating patterns — the demo flags a `strcpy` buffer overflow and Copilot Autofix patches it to `strncpy` with explicit null-termination; the mechanism combines expert knowledge, weak evidence at scale, and deductive/inductive reasoning (slide 4) → [W2.2]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c2).

**The productivity claims are broad and concrete.** Autocompletion and boilerplate generation, generating/explaining code and configs and docs, code translation (legacy to Python), vulnerability detection and fixing, test generation and coverage, agentic bug-fixing (slide 5) → [W2.2]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c2).

**AI's reach now spans the whole SDLC.** Circa 2024 each phase needed its own tool; now one multi-agent session can cover several phases — and the survey evidence maps uses in development, requirements engineering, QA, maintenance, and management (slides 6–7) → [W2.2]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c2).

**The evidence is genuinely mixed.** Russo 2024: faster mundane tasks, faster understanding/testing/debugging, documentation help — against limited applicability, questionable effectiveness, correction overhead, prompt learning curves, and dependency/complacency; DORA's ~4900-response report rounds out the picture (slides 8–9) → [W2.3]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c3).

**The risks have names — learn them.** Garbage in garbage out; traceability of the source (licenses; some tools flag training data); data safety (Samsung's ChatGPT ban); susceptibility to planted vulnerabilities; increasing technical debt (slides 10) → [W2.3]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c3).

**Vibe coding compresses idea-to-implementation distance — for a price.** Rapid prototyping, MVPs, lower barriers, faster design exploration; but inconsistent architecture, weaker security/performance/maintainability, and more review/rework burden (slide 11) → [W2.3]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c3).

**Autonomy is gated by plumbing, not intelligence.** End-to-end development needs tool/data access, actions, delegation, long-running task tracking, and predictable result formats — MCP standardizes tool discovery and use (VS Code + Copilot → MCP connector → GitHub MCP server), A2A standardizes agent-to-agent communication (slide 12) → [W2.4]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c4).

</span>
