{% from "schedule/macros-fragment.md" import term, example with context %}
<h2 id="title">Week 2 — Modern Software Engineering</h2>

<span id="prereqs">

This chapter builds on [Week 1]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c1): software processes, CI/CD, and DevOps — AI-assisted automation plugs straight into that pipeline. No other background is needed.

</span>

<span id="outcomes">

* Can name the five ways AI improves software engineers' efficiency and place concrete tools on that spectrum
* Can describe where AI contributes across the SDLC, from code generation to requirements engineering
* Can explain the evidence for and the risks of AI-assisted engineering, including vibe coding and technical debt
* Can explain what autonomous development needs and what the MCP and A2A protocols standardize

</span>

<div id="body">

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

**This chapter is about the newest trend in software engineering: AI as an engineering collaborator.** The Week 2 deck is titled "Recent Trends in Software Engineering: AI in SE — autocomplete to autonomous agents", and that arc structures everything: AI started by completing your lines of code and now plans, executes, and reviews whole tasks. The engineering judgment you are building in this course — processes (Week 1), requirements (Week 3), architecture (Week 4) — is exactly what AI does not replace.

## Core concepts

<span id="W2-c1"></span>

### W2.1 AI across the software engineering workflow ★

**AI improves software engineers' efficiency in five modes, and the modes differ in where the human review happens.** The deck's arc — autocomplete to autonomous agents — is really a story about the review point moving later in the workflow (Source: L2 slides 2–3).

**Automation handles repeated tasks you already know how to do.** The task is repeated, and what needs to be done is known — AI automates it efficiently and reliably, every time; e.g., workflow automation such as CI/CD and infrastructure deployment (Source: L2 slide 3).

**Pattern detection exploits structure that rules can express.** The task adheres to some rules, so AI sifts through a gigantic codebase to detect vulnerabilities — e.g., identifying query patterns (Source: L2 slide 3).

**Collaboration is turn-by-turn development with a human reviewing each step.** AI contributes code sequence prediction and generation, brainstorming code solutions, and rapid prototyping (e.g., Copilot, ChatGPT); in its turn-by-turn form it offers suggestion, discussion, and refinement with humans, who review each step as it happens (e.g., Copilot Chat) (Source: L2 slides 3–4).

**Delegation moves the review to the final output.** The engineer states the desired outcome; the AI plans, executes (updating files, testing, fixing bugs, iterating), and presents for review — you review the final output, not the steps (e.g., Claude Code, Cursor) (Source: L2 slide 3).

**Orchestration coordinates several specialized agents in several roles.** AI handles task decomposition, planning, and execution; a human or an AI coordinates — e.g., CrewAI, LangGraph (Source: L2 slide 3).

The diagram below places the five modes on one axis — how much the AI does before a human looks — because that axis decides what kind of mistake you can catch, and when.

<mermaid>
flowchart LR
    A["Automation<br/>(CI/CD, infra deployment)"] --> B["Pattern detection<br/>(vulnerability & query patterns)"]
    B --> C["Collaboration<br/>(Copilot, Copilot Chat)"]
    C --> D["Delegation<br/>(Claude Code, Cursor)"]
    D --> E["Orchestration<br/>(CrewAI, LangGraph)"]
    A -. "human knows each step" .-> A
    D -. "human reviews final output" .-> D
    E -. "human (or AI) coordinates agents" .-> E
</mermaid>

%%Notation: each box is one mode of AI involvement; solid arrows run from less to more autonomy; the dashed annotations state where the human stays in the loop for that mode.%%

How to read it for the course example: in this course's project you might automate builds and deployment (automation), let a tool flag vulnerable dependency usage across services (pattern detection), brainstorm a validation rule with Copilot Chat (collaboration), and hand Claude Code a ticket to implement end-to-end (delegation) — reviewing the diff before merge in every mode (Source: L2 slide 3; Tutorial 1 optional Q6 asks exactly this kind of choice).

<box type="warning" seamless>

**Pitfall / trade-off:** The mode can move the review point, but never the responsibility. The L0 policy quoted in Week 1 applies unchanged: you are responsible for anything you submit, and undisclosed or unattributed AI-generated work is plagiarism (Source: L1 slide 7).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** (From Quiz 1 Q1.) You are a security engineer reviewing an application of seven components. In one component you discover a vulnerability from the unsafe use of a third-party library; the same library is used by several other components, though the implementations may differ. Which AI/ML application is most appropriate for finding similar vulnerable usage in the other components?
<panel type="seamless" minimized header="%%Answer%%">

Pattern detection to identify similar library-usage patterns across the components — the task adheres to rules (the repeating usage pattern), which is exactly pattern detection's fit. Predictive analytics — estimating a numeric likelihood (e.g., of a fault) from historical data — estimates likelihoods; it does not match usage patterns (Quiz 1 Q1, model answer; cf. L2 slide 3).

</panel>

**Q2.** Where does the human review happen in delegation that does not happen in collaboration?
<panel type="seamless" minimized header="%%Answer%%">

In collaboration the human reviews each step as it happens (turn-by-turn); in delegation the human reviews only the final output after the AI has planned, executed, and iterated (Source: L2 slide 3).

</panel>

</panel>

<span id="W2-c2"></span>

### W2.2 AI in the SDLC: from code generation to requirements ★★

**AI's contribution now spans every phase of the SDLC, not just writing code.** The deck maps the real-world usage of LLMs in software engineering by phase — development, requirements engineering, quality assurance, maintenance, and management (Source: L2 slides 6–7).

**The integration changed shape quickly.** Circa 2024, each SDLC phase needed a separate agent, tool, or interaction; now a single multi-agent session can cover several phases in one continuous task (Source: L2 slide 6).

**In development, the wins are code generation, completion, search, summarization, understanding, and translation.** Productivity gains claimed for assistants include autocompletion and boilerplate generation, generating and explaining code, configs and docs, code translation (e.g., legacy code to Python), detecting and fixing vulnerabilities, generating tests and improving coverage, and agentic coding that automatically fixes bugs (Source: L2 slides 5, 7).

{% call example("L2 slide 4 — pattern detection that patches a real buffer overflow") %}
GitHub's vulnerability-detection work observes that vulnerabilities are caused by single repeating patterns, and exploits ML plus expert knowledge to find them. The deck's example is a C function that copies input into a 16-byte buffer with `strcpy` — a classic overflow pattern. The mechanism (code snippet → probability of vulnerability → alert) flags it, and Copilot Autofix produces a patch that switches to `strncpy(buffer, input, sizeof(buffer) - 1)` and null-terminates the buffer. The mechanism components are worth remembering: encoded expert knowledge, large volumes of weak evidence, pattern detection, deductive and inductive reasoning, and higher-level features (Source: L2 slide 4).
{% endcall %}

**Requirements engineering, QA, maintenance, and management each have their own AI uses.** Requirements: classification, analysis and evaluation, elicitation — e.g., LLMREI automates requirements-elicitation interviews with LLMs (connect this to Week 3's "AI in requirements engineering" material, which shows elicitation, refinement, tagging, and ambiguity-detection uses). Quality assurance: vulnerability detection and test generation. Maintenance: program repair, review, debugging. Management: effort estimation (Source: L2 slide 7; L3 slides 33–34).

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Map each use to its SDLC phase: (a) generating unit tests for a service; (b) classifying incoming feature requests; (c) automated program repair; (d) estimating effort for a release.
<panel type="seamless" minimized header="%%Answer%%">

(a) Quality assurance (test generation). (b) Requirements engineering (classification). (c) Software maintenance (program repair). (d) Software management (effort estimation) (Source: L2 slide 7).

</panel>

</panel>

<span id="W2-c3"></span>

### W2.3 What the evidence and the risks say ★★

**The empirical picture is mixed: real time savings on mundane work, real friction everywhere else.** The deck cites three sources — a systematic literature review of LLMs for software engineering (Hou et al. 2024), a study of generative-AI adoption (Russo 2024), and the DORA *State of AI-assisted Software Development* report (~4900 responses) (Source: L2 slides 7–9).

**Reported benefits concentrate on speed for well-understood work.** Reducing time on mundane tasks (automating simple tasks, boilerplate code); understanding, testing, and debugging code faster (code summaries, identifying problems, generating automated test scripts); and documentation help — automating and ensuring correctness of documentation (Source: L2 slide 8).

**Reported limitations are the mirror image.** Limited applicability (niche tasks and internal codebases); questionable effectiveness (is the response accurate?); additional time required to ensure correctness (fixing minor errors, mandatory code review); a learning curve (easy to use, hard to master the prompts); and creating dependency and complacency (Source: L2 slide 8).

**The deck names five risk classes — know them by name.** Garbage in, garbage out (output is only as good as your input; regurgitation of bad code, more applicable to niche use cases; correctness is not guaranteed, which reduces trust). Traceability of the source (not all code can be used as is — license terms, correctness — though some tools flag training data, e.g., Amazon CodeWhisperer). Data safety (confidential data may leak — e.g., Samsung bans ChatGPT). Susceptibility to vulnerabilities (bad actors can plant malicious code in the public domain used for training). Increasing technical debt (maintaining others' code is hard; maintaining automatically generated code is harder) (Source: L2 slide 10).

{% call example("L2 slide 10 — the leak that got a company to ban a chatbot") %}
The data-safety risk is not hypothetical: the deck cites Samsung banning ChatGPT after confidential data could be leaked through prompts. For this course's project team, the equivalent rule is simple — never paste unreleased code, credentials, or user data into a public AI tool (Source: L2 slide 10).
{% endcall %}

**Vibe coding compresses the distance from idea to implementation — and that compression has a price.** Its benefits: compressed distance from idea to prototype, requirement to interface, prompt to implementation, and feedback to revised feature; hence rapid prototyping and MVP development, lower barriers for non-specialists and domain experts, and faster exploration of alternative designs. Its costs: inconsistent architecture, reduced security, performance, and maintainability, and an increased review, verification, and rework burden (Source: L2 slide 11).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-vibe-coding" trim />
</box>

<box type="warning" seamless>

**Pitfall / trade-off:** The long-term risk Quiz 1 probes is skill erosion: if AI tools handle compilation, testing, debugging, reviewing, and merging, the most serious long-term danger is that developers lose the ability to detect design, architectural, and maintainability problems — precisely the judgment this course teaches (Quiz 1 Q2, model answer; L2 slide 10).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** (From Quiz 1 Q2.) Claude and other AI tools handle compilation, testing, debugging, reviewing, and merging code. What is the most serious long-term risk?
<panel type="seamless" minimized header="%%Answer%%">

Developers lose the ability to detect design, architectural, and maintainability problems — the other options (less routine practice, longer tests, more precise prompts) are costs, not the systemic risk (Quiz 1 Q2, model answer).

</panel>

**Q2.** Your teammate vibe-codes a working errand-platform prototype in two days and wants to ship it. Name one benefit this speed bought and two costs the team now owes.
<panel type="seamless" minimized header="%%Answer%%">

Benefit: rapid prototyping / a testable MVP that pulls feedback forward (idea → prototype distance compressed). Costs: any two of inconsistent architecture, weakened security/performance/maintainability, and a larger review, verification, and rework burden (Source: L2 slide 11).

</panel>

</panel>

<span id="W2-c4"></span>

### W2.4 From assistants to autonomous development: MCP and A2A ★★★

**End-to-end autonomous development needs more than a good model — it needs plumbing.** For LLMs to carry out software development end to end, the deck lists five requirements: access to tools and data; the ability to perform actions (e.g., retrieve an issue description); collaboration with and delegation of tasks to other agents; tracking of long-running tasks; and exchange of results in a predictable format (Source: L2 slide 12).

**Two protocols standardize the plumbing.** {{ term("MCP", "Model Context Protocol — standardizes how an AI application discovers and uses external tools") }} standardizes how AI applications discover and use external tools; {{ term("A2A", "Agent-to-Agent protocol — standardizes communication between independent AI agents") }} standardizes communication between independent AI agents (Source: L2 slide 12).

{% call example("L2 slide 12 — one MCP chain, end to end") %}
The deck's example chain: VS Code + Copilot connects through an MCP connector to a GitHub MCP server, which exposes Git operations, files in the repo, and GraphQL APIs to the model. The model did not gain coding skill from MCP — it gained standardized reach into the tools where software actually lives (Source: L2 slide 12).
{% endcall %}

**Autonomy is a spectrum you manage, not a switch you flip.** The five modes of W2.1 are the same spectrum seen from the workflow side: as delegation and orchestration grow, the five requirements above (tools, actions, delegation, tracking, predictable formats) are what make the output reviewable at all (Source: L2 slides 3, 12).

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** An agent must (a) read files from your repository, (b) hand a task to another vendor's agent. Which protocol covers (a) and which covers (b)?
<panel type="seamless" minimized header="%%Answer%%">

(a) MCP — standardized discovery and use of external tools (a GitHub MCP server exposing repo files and Git operations). (b) A2A — standardized communication between independent AI agents (Source: L2 slide 12).

</panel>

</panel>

<box type="info" seamless>

**Section summary**

* **AI helps in five modes — automation, pattern detection, collaboration, delegation, orchestration — differing in where human review happens** (W2.1).
* **AI now contributes across the whole SDLC**, from code generation and testing to requirements engineering and effort estimation (W2.2).
* **The evidence shows speed on mundane work but real friction; the named risks are GIGO, traceability, data safety, vulnerabilities, and technical debt** (W2.3).
* **Vibe coding compresses idea-to-implementation distance at the price of architecture, quality, and rework burden** (W2.3).
* **Autonomous development is gated by plumbing, not intelligence: MCP standardizes tool use, A2A standardizes agent-to-agent communication** (W2.4).

</box>

## Connections

* AI modes and risks ↔ L2 slides 2–12 ↔ Quiz 1 Q1–Q2 ↔ Tutorial 1 optional Q6 (where would AI help your application most?).
* Automation and workflow AI ↔ L2 slide 3 ↔ the CI/CD pipeline of Week 1 (W1.5, including its blue-green deployment diagram) — automation was valuable before AI.
* AI in requirements engineering ↔ L2 slides 6–7 ↔ L3 slides 33–34, detailed in Week 3 (W3.6), rehearsed in Tutorial 2 Task 2.2 (eliciting requirements from an LLM).
* Trust, verification, and responsibility ↔ L2 slides 10–11 ↔ the L0 AI-usage policy (L1 slide 7) and the review duties in Week 4's architecture decisions.

## Further reading

All of the following are cited on the slides: Hou et al., *Large language models for software engineering: a systematic literature review* (TOSEM 2024); Russo, *Navigating the complexity of generative AI adoption in software engineering* (TOSEM 2024); the DORA *State of AI-assisted Software Development* report (2025); the GitHub engineering blog post on leveraging ML to find security vulnerabilities; the MCP and A2A protocol specifications.

## Summary

**Key takeaways**

* **AI helps in five modes — automation, pattern detection, collaboration, delegation, orchestration — differing in where the human review happens.** (→ outcome 1)
* **AI contributes across the whole SDLC, from code generation to requirements engineering, with pattern detection the deck's worked example.** (→ outcome 2)
* **The evidence shows speed on mundane work but real friction; the named risks are GIGO, traceability, data safety, vulnerabilities, and technical debt — and vibe coding trades prototyping speed for architecture, quality, and rework.** (→ outcome 3)
* **Autonomous development is gated by plumbing, not intelligence: MCP standardizes tool use, A2A standardizes agent-to-agent communication.** (→ outcome 4)

**Key terms**

| Term | One-line definition | Unit |
|---|---|---|
| Pattern detection (AI) | Exploiting rule-like structure in tasks — e.g., sifting a codebase for vulnerability patterns | [W2.1](#W2-c1) |
| Delegation (AI) | Engineer states the outcome; AI plans, executes, and presents the result for review | [W2.1](#W2-c1) |
| Vibe coding | Building software by prompting, compressing idea-to-implementation distance at a quality cost | [W2.3](#W2-c3) |
| MCP | Protocol standardizing how AI applications discover and use external tools | [W2.4](#W2-c4) |
| A2A | Protocol standardizing communication between independent AI agents | [W2.4](#W2-c4) |

%%Next: Week 3 turns to the input side of everything AI builds — requirements and quality attributes, with the errand platform as the running example.%%

</div>
