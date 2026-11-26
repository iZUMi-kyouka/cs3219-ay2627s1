{# Definitions for week-02. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-02.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable.
   Note: the deployment/DevOps terms below are first taught in the Week 1 deck
   (L1 slides 33–46), so the Week 1 chapter renders these boxes at first use. #}

<span id="def-ci-cd">

**CI/CD** is the pairing of two delivery practices: **continuous integration (CI)** — developers integrate code into a shared repository several times a day, each check-in verified by an automated build so problems are detected early — and **continuous delivery/deployment (CD)** — every good build is kept potentially ready for production release (delivery), or released automatically into production (deployment).

<sub>-- L1 slides 41–42</sub>

</span>

<span id="def-devops">

**DevOps** is a set of software development practices that combines software development (Dev) and operations (Ops), intending to reduce the time between committing a change and that change running in normal production, while ensuring high quality.

<sub>-- L1 slide 46, after Ebert et al., IEEE Software 2016</sub>

</span>

<span id="def-containerization">

**Containerization** is packaging an application together with only the OS processes and dependencies it needs, so it runs identically on any host that runs a container engine — lighter than a virtual machine, which carries a full guest OS.

<sub>-- L1 slides 32–33</sub>

</span>

<span id="def-blue-green-deployment">

**Blue-green deployment** is a release strategy that shifts traffic between two identical environments running different versions of the application, achieving near-zero downtime and easy rollback.

<sub>-- L1 slide 44</sub>

</span>

<span id="def-vibe-coding">

**Vibe coding** is building software primarily by prompting AI — compressing the distance from idea to prototype, requirement to interface, and prompt to implementation — while accepting weaker architecture, quality, and a larger verification burden.

<sub>-- L2 slide 11</sub>

</span>

<span id="def-automation">

**Automation** (AI mode) is the mode where AI handles repeated tasks whose steps are already known — automating them efficiently and reliably, every time (e.g., workflow automation such as CI/CD and infrastructure deployment).

<sub>-- L2 slide 3</sub>

</span>

<span id="def-pattern-detection">

**Pattern detection** (AI mode) is the mode that exploits rule-like structure in tasks: AI sifts through a gigantic codebase to detect vulnerabilities — e.g., identifying query patterns (recurring, rule-like code structures), or the repeating library-usage pattern behind a vulnerability.

<sub>-- L2 slide 3; Quiz 1 Q1</sub>

</span>

<span id="def-collaboration-ai">

**Collaboration** (AI mode) is turn-by-turn development: the AI offers suggestion, discussion, and refinement with humans, who review each step as it happens — e.g., code sequence prediction and generation, brainstorming code solutions, and rapid prototyping (Copilot, Copilot Chat).

<sub>-- L2 slides 3–4</sub>

</span>

<span id="def-delegation-ai">

**Delegation** (AI mode) moves the human review to the final output: the engineer states the desired outcome and the AI plans, executes (updating files, testing, fixing bugs, iterating), and presents the result for review — you review the final output, not the steps (e.g., Claude Code, Cursor).

<sub>-- L2 slide 3</sub>

</span>

<span id="def-orchestration-ai">

**Orchestration** (AI mode) coordinates several specialized agents in several roles: AI handles task decomposition, planning, and execution, while a human or an AI coordinates (e.g., CrewAI, LangGraph).

<sub>-- L2 slide 3</sub>

</span>

<span id="def-predictive-analytics">

**Predictive analytics** estimates a numeric likelihood or outcome from historical data — e.g., which component is most likely to fail in production, or which requirements are likely to be implemented successfully. Unlike pattern detection, it estimates likelihoods rather than matching usage patterns.

<sub>-- Quiz 1 Q1; L3 slide 34</sub>

</span>

<span id="def-gigo">

**Garbage in, garbage out (GIGO)** is the AI risk that output is only as good as your input: models can regurgitate bad code (more applicable to niche use cases), and correctness is not guaranteed — which reduces trust.

<sub>-- L2 slide 10</sub>

</span>

<span id="def-technical-debt">

**Technical debt** is the accumulated cost of shortcuts taken in code and design. Maintaining others' code is hard; maintaining automatically generated code is harder — so AI-assisted coding can increase technical debt.

<sub>-- L2 slide 10</sub>

</span>

<span id="def-autonomous-development">

**Autonomous development** is end-to-end software development carried out by LLM-based agents. It requires: access to tools and data; the ability to perform actions (e.g., retrieve an issue description); collaboration with and delegation of tasks to other agents; tracking of long-running tasks; and exchange of results in a predictable format.

<sub>-- L2 slide 12</sub>

</span>

<span id="def-mcp">

**MCP (Model Context Protocol)** standardizes how an AI application discovers and uses external tools — e.g., VS Code + Copilot connecting through an MCP connector to a GitHub MCP server exposing Git operations, files in the repo, and GraphQL APIs.

<sub>-- L2 slide 12</sub>

</span>

<span id="def-a2a">

**A2A (Agent-to-Agent protocol)** standardizes communication between independent AI agents.

<sub>-- L2 slide 12</sub>

</span>

<span id="def-llm">

An **LLM (large language model)** is an AI model trained on vast amounts of text and code to predict and generate language — the technology behind tools such as ChatGPT, GitHub Copilot, and Claude.

<sub>-- usage throughout L2 slides 2–12; term dimmed: Wikipedia, "Large language model"</sub>

</span>
