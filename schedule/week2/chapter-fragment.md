{% from "schedule/macros-fragment.md" import term, example with context %}
<h2>Week 2 — Modern Software Engineering</h2>

<span>

This chapter builds on [Week 1]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c1): software processes, CI/CD, and DevOps — AI-assisted automation plugs straight into that pipeline. No other background is needed.

</span>

<span>

* Can name the five ways AI improves software engineers' efficiency and place concrete tools on that spectrum
* Can describe where AI contributes across the SDLC, from code generation to requirements engineering
* Can explain the evidence for and the risks of AI-assisted engineering, including vibe coding and technical debt
* Can explain what autonomous development needs and what the MCP and A2A protocols standardize
* Can describe the developer's role in AI-assisted engineering — specify and verify, own architecture and design, orchestrate, and guard quality

</span>

<div>

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

**This chapter is about the newest trend in software engineering: AI as an engineering collaborator.** The Week 2 deck is titled "Recent Trends in Software Engineering: AI in SE — autocomplete to autonomous agents", and that arc structures everything: AI started by completing your lines of code and now plans, executes, and reviews whole tasks. The engineering judgment you are building in this course — processes (Week 1), requirements (Week 3), architecture (Week 4) — is exactly what AI does not replace.

## Core concepts

<span id="W2-c1"></span>

### W2.1 AI across the software engineering workflow ★

**AI improves software engineers' efficiency in five modes, and the modes differ in where the human review happens.** The deck's arc — autocomplete to autonomous agents — is really a story about the review point moving later in the workflow (Source: L2 slides 2–3).

**Automation handles repeated tasks you already know how to do.** The task is repeated, and what needs to be done is known — AI automates it efficiently and reliably, every time; e.g., workflow automation such as {{ term("CI/CD", "the automated build–test–release pipeline: continuous integration plus continuous delivery/deployment (defined in Week 1)") }} and infrastructure deployment (Source: L2 slide 3). The lecture's caveat: automation does not need AI — if you know exactly what to do, a plain script does it, and AI is just one way to write that script (L2 recording, ~[50:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-automation" trim />
</box>

**Pattern detection exploits structure that rules can express.** The task adheres to some rules, so AI sifts through a gigantic codebase to detect vulnerabilities — e.g., identifying query patterns: recurring, rule-like code structures; the unsafe `strcpy` buffer copy the deck dissects on slide 4 is one such pattern (Source: L2 slide 3).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-pattern-detection" trim />
</box>

**Collaboration is turn-by-turn development with a human reviewing each step.** AI contributes code sequence prediction and generation, brainstorming code solutions, and rapid prototyping (e.g., Copilot, ChatGPT); in its turn-by-turn form it offers suggestion, discussion, and refinement with humans, who review each step as it happens (e.g., Copilot Chat) (Source: L2 slides 3–4).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-collaboration-ai" trim />
</box>

**Delegation moves the review to the final output.** The engineer states the desired outcome; the AI plans, executes (updating files, testing, fixing bugs, iterating), and presents for review — you review the final output, not the steps (e.g., Claude Code, Cursor) (Source: L2 slide 3).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-delegation-ai" trim />
</box>

**Orchestration coordinates several specialized agents in several roles.** AI handles task decomposition, planning, and execution; a human or an AI coordinates — e.g., CrewAI, LangGraph (Source: L2 slide 3). Here an *agent* is an AI system that can plan and take actions toward a goal — running tools, editing files, calling other agents %%dimmed: Wikipedia, "Software agent"; the term recurs through W2.2's multi-agent sessions and W2.4's A2A protocol%%.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-orchestration-ai" trim />
</box>

{% call example("L2 recording ~[55:00] — one real delegation: the deployment that would not deploy") %}
Confronted with a failing deployment, the professor pointed an agent at the repository with one instruction — "this is not getting deployed, find out why" — and waited. About 40 minutes later it reported a diagnosis nobody had guessed: the code compiled fine on Windows, but the deployment ran from WSL, and the Git authentication token was not being passed from Windows to WSL. It then produced the fix step by step — create a fine-grained token for repo and pages access, set it as an environment variable instead of putting it in the code, rerun the same command from the same location — warned that its suggestion would break if anything changed first, and it worked (L2 recording, ~[55:00]–[60:00]).

That is delegation in W2.1's sense: a stated intent, autonomous planning and execution, a reviewed final result — and a reminder that the human still has to judge whether the diagnosis is credible.
{% endcall %}

**The modes arrived in historical order, and each moved the review point later.**

* **Autocomplete** — predicting your next lines in an IDE — enabled rapid prototyping
* **Turn-by-turn development** — write a comment, get the whole method — was 2024's "revolutionary" collaboration step, alongside Copilot Chat
* **Delegation and orchestration** arrived in the last year or so

(L2 recording, ~[50:00]–[55:00])

The diagram below places the five modes on one axis — how much the AI does before a human looks — because that axis decides what kind of mistake you can catch, and when.

<mermaid>
flowchart LR
    A["Automation<br/>(CI/CD, infra deployment)"] --> B["Pattern detection<br/>(vulnerability & query patterns)"]
    B --> C["Collaboration<br/>(Copilot, Copilot Chat)"]
    C --> D["Delegation<br/>(Claude Code, Cursor)"]
    D --> E["Orchestration<br/>(CrewAI, LangGraph)"]
    A -. "human knows each step" .-> A
    B -. "human acts on the flagged patterns" .-> B
    C -. "human reviews each step" .-> C
    D -. "human reviews final output" .-> D
    E -. "human (or AI) coordinates agents" .-> E
</mermaid>

%%Notation: each box is one mode of AI involvement; solid arrows run from less to more autonomy; the dashed annotations state where the human stays in the loop for that mode.%%

How to read it for the course example: in this course's project you might automate builds and deployment (automation), let a tool flag vulnerable dependency usage across services (pattern detection), brainstorm a validation rule with Copilot Chat (collaboration), and hand Claude Code a ticket to implement end-to-end (delegation) — reviewing the diff before merge in every mode (Source: L2 slide 3; Tutorial 1 optional Q6 asks exactly this kind of choice).

**Not every AI application is one of the five modes — predictive analytics estimates instead of matching.** Where pattern detection finds the repeating structure itself, predictive analytics estimates a numeric likelihood or outcome from historical data (Source: Quiz 1 Q1; L3 slide 34).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-predictive-analytics" trim />
</box>

Quiz 1 Q1 turns the difference into a distractor: estimating which component is *most likely to fail in production* is predictive analytics; finding the other components with *similar vulnerable usage patterns* is pattern detection — the task's rule-like structure is what makes pattern detection the right fit (Quiz 1 Q1, model answer).

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

**AI's contribution now spans every phase of the {{ term("SDLC", "software development life cycle — from conception through development, deployment, and operation to retirement (defined in Week 1)") }}, not just writing code.** The deck maps the real-world usage of {{ term("LLMs", "large language models — AI models trained on vast text and code corpora to predict and generate text (ChatGPT, Copilot, and Claude are LLMs)") }} in software engineering by phase — development, requirements engineering, quality assurance, maintenance, and management (Source: L2 slides 6–7).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-llm" trim />
</box>

**The integration changed shape quickly.** Circa 2024, each SDLC phase needed a separate agent, tool, or interaction; now a single multi-agent session — W2.1's orchestration mode — can cover several phases in one continuous task (Source: L2 slide 6).

**In development, the wins are code generation, completion, search, summarization, understanding, and translation.** Productivity gains claimed for assistants include autocompletion and boilerplate generation, generating and explaining code, configs and docs, code translation (e.g., legacy code to Python), detecting and fixing vulnerabilities, generating tests and improving coverage, and agentic coding — AI agents (W2.1) acting autonomously — that automatically fixes bugs (Source: L2 slides 5, 7).

{% call example("L2 slide 4 — pattern detection that patches a real buffer overflow") %}
GitHub's vulnerability-detection work observes that vulnerabilities are caused by single repeating patterns, and exploits ML (machine learning) plus expert knowledge to find them. The deck's example is a C function that copies input into a 16-byte buffer with `strcpy` — a classic overflow pattern. The mechanism (code snippet → probability of vulnerability → alert) flags it, and Copilot Autofix (GitHub Copilot's automatic vulnerability-fixing feature) produces a patch that switches to `strncpy(buffer, input, sizeof(buffer) - 1)` and null-terminates the buffer.

%%Why the original is unsafe: `strcpy` copies until the input's end marker without checking the 16-byte limit, so a longer input writes past the buffer's end — that is the overflow. The patch caps the copy at `sizeof(buffer) - 1`, and the explicit final-byte assignment (`buffer[15] = '\0'`) keeps the string validly terminated.%%

The mechanism components are worth remembering: encoded expert knowledge, large volumes of weak evidence, pattern detection, deductive and inductive reasoning, and higher-level features (Source: L2 slide 4).
%%Read the slide's nouns as one recipe (site reading of the GitHub post the slide cites): encoded expert knowledge = rules security experts write by hand; large volumes of weak evidence = huge numbers of low-confidence signals (code that merely looks possibly vulnerable) as training material; deductive and inductive reasoning = concluding from those rules and from the data; higher-level features = code characteristics aggregated above the raw text.%%
{% endcall %}

**Requirements engineering, QA, maintenance, and management each have their own AI uses.** Requirements: classification, analysis and evaluation, elicitation — e.g., LLMREI (Korn et al., 2025 — a research system, not a product) automates requirements-elicitation interviews with LLMs (connect this to Week 3's "AI in requirements engineering" material, which shows elicitation, refinement, tagging, and ambiguity-detection uses). Quality assurance: vulnerability detection and test generation. Maintenance: program repair, review, debugging. Management: effort estimation (Source: L2 slide 7; L3 slides 33–34).

**The lecture's evidence point on elicitation: the interviewer is becoming a bot.** In 2024 AI was barely used for requirements elicitation — users should still tell what they want — but orchestration now has AI conducting the interview, and a measured comparison found humans and AI make the same kinds of mistakes translating a user's statement into a requirement specification (L2 recording, ~[60:00]–[65:00]).

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Map each use to its SDLC phase: (a) generating unit tests for a service; (b) classifying incoming feature requests; (c) automated program repair; (d) estimating effort for a release.

<panel type="seamless" minimized header="%%Answer%%">

(a) Quality assurance (test generation). (b) Requirements engineering (classification). (c) Software maintenance (program repair). (d) Software management (effort estimation) (Source: L2 slide 7).

</panel>

</panel>

<span id="W2-c3"></span>

### W2.3 What the evidence and the risks say ★★

**The empirical picture is mixed: real time savings on mundane work, real friction everywhere else.** The deck cites three sources — a systematic literature review of LLMs for software engineering (Hou et al. 2024), a study of generative-AI adoption (Russo 2024), and the DORA (DevOps Research and Assessment) *State of AI-assisted Software Development* report (~4900 responses) (Source: L2 slides 7–9).

**Reported benefits concentrate on speed for well-understood work.**

- Reducing time on mundane tasks (automating simple tasks, boilerplate code)
- Understanding, testing, and debugging code faster (code summaries, identifying problems, generating automated test scripts)
- Documentation help — automating and ensuring correctness of documentation

(Source: L2 slide 8)

**Reported limitations are the mirror image.**

- Limited applicability (niche tasks and internal codebases)
- Questionable effectiveness (is the response accurate?)
- Additional time required to ensure correctness (fixing minor errors, mandatory code review)
- A learning curve (easy to use, hard to master the prompts)
- Creating dependency and complacency

(Source: L2 slide 8)

**The lecture adds two headline numbers to the mixed picture.** A benchmark over public Node.js and Python repositories found that 96.2% of raised issues can be fixed by AI without human intervention — impressive and, as the professor put it, scary (L2 recording, ~[60:00]). And the lecture cites, from the DORA survey of ~4900 practitioners, that 71% rely on AI when writing new code — the survey's most common use %%dimmed: dora.dev, State of AI-assisted Software Development 2025%% (L2 recording, ~[65:00]).

**The deck names five risk classes — know them by name.** Garbage in, garbage out (output is only as good as your input; regurgitation of bad code, more applicable to niche use cases; correctness is not guaranteed, which reduces trust). Traceability of the source (not all code can be used as is — license terms, correctness — though some tools flag training data, e.g., Amazon CodeWhisperer). Data safety (confidential data may leak — e.g., Samsung bans ChatGPT). Susceptibility to vulnerabilities (bad actors can plant malicious code in the public domain used for training). Increasing technical debt (maintaining others' code is hard; maintaining automatically generated code is harder) (Source: L2 slide 10).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-gigo" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-technical-debt" trim />
</box>

**GIGO has acquired a feedback loop.** Because AI now generates much of the code that trains later models, "we don't know how much garbage is going in" (L2 recording, ~[65:00]). The verification gap makes it worse: in Sonar's State of Code survey of 1,100+ developers, 96% do not fully trust AI-generated code, yet only 48% always verify it before committing %%dimmed: sonarsource.com, State of Code Developer Survey%% — the gap the lecture drove home with this survey (L2 recording, ~[65:00]).

{% call example("L2 slide 10 — the leak that got a company to ban a chatbot") %}
The data-safety risk is not hypothetical: the deck cites Samsung banning ChatGPT after confidential data could be leaked through prompts. %%External detail beyond the slide (dimmed: 2023 press coverage, e.g., Reuters): Samsung engineers had pasted confidential source code and meeting notes into ChatGPT, and the company then banned generative-AI tools on company devices — exactly the leak path the slide warns about.%% For this course's project team, the equivalent rule is simple — never paste unreleased code, credentials, or user data into a public AI tool (Source: L2 slide 10).

The lecture adds a qualification: the ban itself likely did not last — companies that need generative AI deploy internal chatbots instead, so the practical rule is "no confidential code into public tools," not "no AI at all" (L2 recording, ~[70:00]).
{% endcall %}

{% call example("L2 recording ~[65:00] — the visualization feature that had to be scrapped") %}
The professor's industry team once built a drag-and-drop usage-visualization feature — genuinely hard to do at the time — and customers loved the demo. Then the code scan required for certification flagged it: the visualization code had come from a publicly available tutorial whose license forbade commercial use. The feature was scrapped entirely, and the product shipped three months late (L2 recording, ~[65:00]–[70:00]).

%%The AI-era lesson: whatever code is available can end up in training data — if your build pulls in code whose source can be contested, the problem surfaces at certification time, with customers already happy.%%
{% endcall %}

**Vibe coding compresses the distance from idea to implementation — and that compression has a price.** Its benefits: compressed distance from idea to prototype, requirement to interface, prompt to implementation, and feedback to revised feature; hence rapid prototyping and {{ term("MVP", "minimum viable product — the smallest build that delivers enough value to test the idea with real users") }} development, lower barriers for non-specialists and domain experts, and faster exploration of alternative designs. Its costs: inconsistent architecture, reduced security, performance, and maintainability, and an increased review, verification, and rework burden (Source: L2 slide 11). The lecture's caution in one line: "there is more than one way to do it — and more than one way to screw it." The safe pattern is generate, test, update — staying in control; the failure mode is "do this and go away," where drift from the intended architecture makes the code hard to maintain and the technical debt compounds. Use it to the extent that it helps you, not harms you (L2 recording, ~[70:00]).

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

**End-to-end autonomous development needs more than a good model — it needs plumbing.** For LLMs to carry out software development end to end, the deck lists five requirements:

- Access to tools and data
- The ability to perform actions (e.g., retrieve an issue description)
- Collaboration with and delegation of tasks to other agents
- Tracking of long-running tasks
- Exchange of results in a predictable format

(Source: L2 slide 12)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-autonomous-development" trim />
</box>

**Two protocols standardize the plumbing.** {{ term("MCP", "Model Context Protocol — standardizes how an AI application discovers and uses external tools") }} standardizes how AI applications discover and use external tools; {{ term("A2A", "Agent-to-Agent protocol — standardizes communication between independent AI agents") }} standardizes communication between independent AI agents (Source: L2 slide 12). The lecture keeps the roles straight: MCP is a protocol, not a model — it does nothing by itself beyond specifying how the sides talk, and under the hood that conversation is JSON-RPC 2.0 messaging %%dimmed: modelcontextprotocol.io specification%% (L2 recording, ~[70:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-mcp" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-a2a" trim />
</box>

{% call example("L2 slide 12 — one MCP chain, end to end") %}
The deck's example chain: VS Code + Copilot connects through an MCP connector to a GitHub MCP server, which exposes Git operations, files in the repo, and GraphQL APIs to the model. The model did not gain coding skill from MCP — it gained standardized reach into the tools where software actually lives (Source: L2 slide 12).

For A2A, the lecture's (fictitious but buildable) workflow: a developer tells one agent "fix the login bug," which delegates to specialized agents — code analysis, implementation, testing, security — all of them reaching GitHub through MCP (L2 recording, ~[70:00]).
{% endcall %}

**Autonomy is a spectrum you manage, not a switch you flip.** The five modes of W2.1 are the same spectrum seen from the workflow side: as delegation and orchestration grow, the five requirements above (tools, actions, delegation, tracking, predictable formats) are what make the output reviewable at all (Source: L2 slides 3, 12).

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** An agent must (a) read files from your repository, (b) hand a task to another vendor's agent. Which protocol covers (a) and which covers (b)?

<panel type="seamless" minimized header="%%Answer%%">

(a) MCP — standardized discovery and use of external tools (a GitHub MCP server exposing repo files and Git operations). (b) A2A — standardized communication between independent AI agents (Source: L2 slide 12).

</panel>

</panel>

<span id="W2-c5"></span>

### W2.5 The developer's role when AI does the typing ★★

**If agents can carry tasks end to end, what remains for you is exactly what this course teaches.** The lecture closed with a think-pair-share on this question — the class answered first, then the professor gave his own list, deliberately kept off the deck slide (L2 recording, ~[75:00]–[80:00]).

<panel type="seamless" minimized header="%%Asked in lecture: if an agent can do the whole task, what is the developer's role?%%">

Student answers: specify and verify · take responsibility for everything that happens · improve the agentic workflow · keep sight of the big picture · prevent scope creep · manage tokens (costs).

</panel>

**The professor's list of what humans keep doing better:**

* **Interpret needs and decipher requirements** — an AI can paraphrase the text of a requirement, but only a human who received it from the field knows what it actually means
* **Own the architecture and design** — otherwise vibe coding drifts the design; this is W2.3's technical-debt risk at its source
* **Plan for long-term evolution and maintenance** — AI finishes the task in front of it; nothing guarantees it plans for the next one
* **Orchestrate** — decompose the problem and provide proper context: "if you are specific enough in what you're asking, you get reasonably good results; if you ask anyhow, it'll also give anyhow"
* **Be the quality guardian** — ensure code is reviewed and only what belongs in the product goes in; done consistently, this also manages technical debt

(L2 recording, ~[75:00]–[80:00])

**The industry's one-line summary: hire people smart enough to know they need to adapt.** That is what the professor's industry colleagues said they now look for, in various forms. To the student worry "if AI can do everything, what do I learn?", his advice: let AI do the task, then spend the time you saved learning what it did — so you do not surrender your autonomy and agency. A closing data point: a January survey found 65% of respondents expected their roles to be redefined by the end of 2026 (L2 recording, ~[80:00]).

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Which of these is on the lecture's list of what humans keep doing better than AI: writing boilerplate faster, deciphering what a field requirement actually means, generating unit tests, or managing token costs?

<panel type="seamless" minimized header="%%Answer%%">

Deciphering what a field requirement actually means — interpreting intent, not text, is the human's job. Generating tests and boilerplate are AI strengths; token management is an operational concern, not one of the professor's listed roles (Source: L2 recording, ~[75:00]–[80:00]).

</panel>

</panel>

<box type="info" seamless>

**Section summary**

* **AI helps in five modes — automation, pattern detection, collaboration, delegation, orchestration — differing in where human review happens** (W2.1).
* **AI now contributes across the whole SDLC**, from code generation and testing to requirements engineering and effort estimation (W2.2).
* **The evidence shows speed on mundane work but real friction; the named risks are GIGO, traceability, data safety, vulnerabilities, and technical debt** (W2.3).
* **Vibe coding compresses idea-to-implementation distance at the price of architecture, quality, and rework burden** (W2.3).
* **Autonomous development is gated by plumbing, not intelligence: MCP standardizes tool use, A2A standardizes agent-to-agent communication** (W2.4).
* **The developer's role moves up the stack — interpret requirements, own design, orchestrate, guard quality — and the durable skill is adaptability** (W2.5).

</box>

## Connections

* AI modes and risks ↔ L2 slides 2–12 ↔ Quiz 1 Q1–Q2 ↔ Tutorial 1 optional Q6 (where would AI help your application most?).
* Automation and workflow AI ↔ L2 slide 3 ↔ the CI/CD pipeline of Week 1 (W1.5, including its blue-green deployment diagram) — automation was valuable before AI.
* AI in requirements engineering ↔ L2 slides 6–7 ↔ L3 slides 33–34, detailed in Week 3 (W3.7), rehearsed in Tutorial 2 Task 2.2 (eliciting requirements from an LLM).
* Trust, verification, and responsibility ↔ L2 slides 10–11 ↔ the L0 AI-usage policy (L1 slide 7) and the review duties in Week 4's architecture decisions.
* The developer's evolving role ↔ L2 recording ~[75:00]–[80:00] ↔ Quiz 1 Q2 (skill erosion) ↔ the architecture ownership of Week 4.

## Further reading

All of the following are cited on the slides: Hou et al., *Large language models for software engineering: a systematic literature review* (ACM Transactions on Software Engineering and Methodology — TOSEM — 2024); Russo, *Navigating the complexity of generative AI adoption in software engineering* (TOSEM 2024); the DORA *State of AI-assisted Software Development* report (2025); the GitHub engineering blog post on leveraging ML to find security vulnerabilities; the MCP and A2A protocol specifications.

## Summary

**Key takeaways**

* **AI helps in five modes — automation, pattern detection, collaboration, delegation, orchestration — differing in where the human review happens.** (→ outcome 1)
* **AI contributes across the whole SDLC, from code generation to requirements engineering, with pattern detection the deck's worked example.** (→ outcome 2)
* **The evidence shows speed on mundane work but real friction; the named risks are GIGO, traceability, data safety, vulnerabilities, and technical debt — and vibe coding trades prototyping speed for architecture, quality, and rework.** (→ outcome 3)
* **Autonomous development is gated by plumbing, not intelligence: MCP standardizes tool use, A2A standardizes agent-to-agent communication.** (→ outcome 4)
* **AI shifts the developer's role up the stack — interpret requirements, own architecture, orchestrate, guard quality — with adaptability the durable skill.** (→ outcome 5)

**Key terms**

| Term | One-line definition | Unit |
|---|---|---|
| Automation (AI) | Handles repeated tasks whose steps are known — efficiently and reliably, every time | [W2.1](#W2-c1) |
| Pattern detection (AI) | Exploits rule-like structure — e.g., sifting a codebase for vulnerability patterns | [W2.1](#W2-c1) |
| Collaboration (AI) | Turn-by-turn development with a human reviewing each step (Copilot, Copilot Chat) | [W2.1](#W2-c1) |
| Delegation (AI) | Engineer states the outcome; AI plans, executes, and presents the result for review | [W2.1](#W2-c1) |
| Orchestration (AI) | Several specialized agents in several roles; AI decomposes and plans, human or AI coordinates | [W2.1](#W2-c1) |
| Predictive analytics | Estimates likelihoods from historical data (which component fails next) — not pattern matching | [W2.1](#W2-c1) |
| Vibe coding | Building software by prompting, compressing idea-to-implementation distance at a quality cost | [W2.3](#W2-c3) |
| Garbage in, garbage out | Output is only as good as your input; correctness not guaranteed, so trust is reduced | [W2.3](#W2-c3) |
| Technical debt | Accumulated cost of shortcuts; AI-generated code is harder to maintain than others' code | [W2.3](#W2-c3) |
| Autonomous development | End-to-end development by LLM agents — needs tools, actions, delegation, tracking, predictable formats | [W2.4](#W2-c4) |
| MCP | Protocol standardizing how AI applications discover and use external tools | [W2.4](#W2-c4) |
| A2A | Protocol standardizing communication between independent AI agents | [W2.4](#W2-c4) |

%%Next: Week 3 turns to the input side of everything AI builds — requirements and quality attributes, with the errand platform as the running example.%%

</div>
