<span id="summary">

**Organising question:** how is AI changing the way software is engineered — and where does human judgment stay essential?

The lecture ("Recent trends in software engineering: AI in SE — autocomplete to autonomous agents") covers:

* five ways AI improves engineers' efficiency: automation, pattern detection, collaboration, delegation, orchestration
* AI across the SDLC: code generation, testing, maintenance — and requirements engineering
* real-world evidence (the Hou et al. LLM4SE — LLMs for software engineering — survey, Russo 2024, DORA 2025) and the risks: garbage-in-garbage-out, traceability, data safety, vulnerabilities, technical debt
* vibe coding and its trade-offs, and what autonomous development needs (MCP and A2A protocols)

</span>

<span id="toc">

* [W2.1 AI across the software engineering workflow]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c1)
* [W2.2 AI in the SDLC: from code generation to requirements]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c2)
* [W2.3 What the evidence and the risks say]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c3)
* [W2.4 From assistants to autonomous development: MCP and A2A]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c4)

</span>

<span id="lecture">

### Lecture

**AI improves engineers' efficiency in five modes, and the review point moves with each mode.** From least to most autonomy (slides 3–4):

* **Automation** handles repeated tasks (CI/CD, infrastructure deployment)
* **Pattern detection** exploits rule-like structure (sifting codebases for vulnerabilities)
* **Collaboration** is turn-by-turn (Copilot, Copilot Chat)
* **Delegation** moves review to the final output (Claude Code, Cursor)
* **Orchestration** coordinates specialized agents (CrewAI, LangGraph)

→ [W2.1]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c1).

<panel type="seamless" minimized header="%%What is each AI mode?%%">

<include src="../../se-book-adapted/common/defs-week-02.md#def-automation" trim />

<include src="../../se-book-adapted/common/defs-week-02.md#def-pattern-detection" trim />

<include src="../../se-book-adapted/common/defs-week-02.md#def-collaboration-ai" trim />

<include src="../../se-book-adapted/common/defs-week-02.md#def-delegation-ai" trim />

<include src="../../se-book-adapted/common/defs-week-02.md#def-orchestration-ai" trim />

</panel>

**Pattern detection is the deck's worked example.** Vulnerabilities come from repeating patterns — the demo flags a `strcpy` buffer overflow and Copilot Autofix patches it to `strncpy` with explicit null-termination. The mechanism combines expert knowledge, weak evidence at scale, and deductive/inductive reasoning (slide 4) → [W2.2]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c2).

**The productivity claims are broad and concrete.** Autocompletion and boilerplate generation, generating/explaining code and configs and docs, code translation (legacy to Python), vulnerability detection and fixing, test generation and coverage, agentic bug-fixing (slide 5) → [W2.2]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c2).

**AI's reach now spans the whole SDLC.** Circa 2024 each phase needed its own tool; now one multi-agent session (W2.1's orchestration mode) can cover several phases — and the survey evidence maps uses in development, requirements engineering, quality assurance (QA), maintenance, and management (slides 6–7) → [W2.2]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c2).

**The evidence is genuinely mixed.** (slides 8–9)

* **Reported benefits (Russo 2024):** faster mundane tasks, faster understanding/testing/debugging, documentation help
* **Reported limitations:** limited applicability, questionable effectiveness, correction overhead, prompt learning curves, and dependency/complacency
* **DORA's ~4900-response report** rounds out the picture

→ [W2.3]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c3).

**The risks have names — learn them.** (slides 10)

* **Garbage in, garbage out** — output is only as good as your input
* **Traceability of the source** — licenses; some tools flag training data
* **Data safety** — Samsung's ChatGPT ban
* **Susceptibility to planted vulnerabilities**
* **Increasing technical debt**

→ [W2.3]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c3).

<panel type="seamless" minimized header="%%What are GIGO and technical debt?%%">

<include src="../../se-book-adapted/common/defs-week-02.md#def-gigo" trim />

<include src="../../se-book-adapted/common/defs-week-02.md#def-technical-debt" trim />

</panel>

**Vibe coding compresses idea-to-implementation distance — for a price.** (slide 11)

* **Benefits:** rapid prototyping, MVPs, lower barriers, faster design exploration
* **Costs:** inconsistent architecture, weaker security/performance/maintainability, and more review/rework burden

→ [W2.3]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c3).

<panel type="seamless" minimized header="%%What is vibe coding?%%">

<include src="../../se-book-adapted/common/defs-week-02.md#def-vibe-coding" trim />

</panel>

**Autonomy is gated by plumbing, not intelligence.** End-to-end development needs tool/data access, actions, delegation, long-running task tracking, and predictable result formats — MCP standardizes tool discovery and use (VS Code + Copilot → MCP connector → GitHub MCP server), A2A standardizes agent-to-agent communication (slide 12) → [W2.4]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#W2-c4).

<panel type="seamless" minimized header="%%What are MCP and A2A?%%">

<include src="../../se-book-adapted/common/defs-week-02.md#def-mcp" trim />

<include src="../../se-book-adapted/common/defs-week-02.md#def-a2a" trim />

</panel>

</span>
