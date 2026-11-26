<span id="summary">

**Organising question:** once requirements say *what* and *how well*, how does architecture decide the system's overall structure — and how do you start specifying it for your own project?

Two decks:

- **The architecture deck** covers: the architecture definition (Bass/Clements/Kazman) and its building blocks (components, connectors, configuration); control vs data flow; call-and-return vs messages and events; decomposition, horizontal vs vertical slicing; modularity, coupling and cohesion; and the categorization of architectural styles (layered, modular monolith, event-driven, microservices).
- **The product-backlog deck** presents fully-worked example requirements for the errand/pickup platform, organized by service — the running example for Weeks 3–4 and Tutorial 2.

</span>

<span id="toc">

* [W4.1 What is software architecture?]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c1)
* [W4.2 Components, connectors, and configuration]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c2)
* [W4.3 Control flow vs data flow]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c3)
* [W4.4 Call-and-return vs messages and events]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c4)
* [W4.5 Decomposition, slicing, and modularity]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c5)
* [W4.6 Coupling and cohesion]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c6)
* [W4.7 Architectural styles: how code is divided and how it is deployed]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c7)

</span>

<span id="lecture">

### Lecture

{% from "schedule/macros-fragment.md" import term, example with context %}

<panel type="seamless" expanded header=":glyphicon-facetime-video: **Deck 1 — High Level Design: Software Architecture** %%*(slides 2–22)*%%">

**{{ term("software architecture", "the structure(s) of a system: components, their externally visible properties, and their relationships — the overall organization, a high-level design") }} is defined by Bass, Clements & Kazman: structure(s) = components + externally visible properties + relationships.** The deck's shorthand: externally visible properties ≡ functionalities + NFR — the overall organization, a high-level design (slide 4) → [W4.1]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c1).

**The building blocks are component, connector, and configuration.** (slide 6) → [W4.2]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c2):

- **Components** model application-specific responsibilities.
- **Connectors** model interactions for transfer of control and/or data.
- **Configuration** is the topology.

**Architectural design decisions are a question list.** Decomposition, templates, styles, the component organization that best delivers the NFR, and the deployment shape (slide 7) → [W4.1]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c1).

**Develop the architecture in a refineable loop.** Drivers (FRs, quality attributes, constraints) → choose a capability → propose a structure → define boundaries and contracts → verify with requirements → document via the architecture diagram; repeat as the software evolves (slide 8) → [W4.1]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c1).

**Reference architectures lead to architectural patterns.** Common frameworks for numerous applications (web apps; the address-book guide) (slide 9) → [W4.1]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c1).

**One arrow, two meanings: control flow and data flow.** Control flow reasons about computation order — how the focus of control moves; data flow reasons about data availability, transformation, and latency — and as data moves, control is activated (slide 10) → [W4.3]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c3).

**Call-and-return moves control out and back;** hierarchical (master control) or non-hierarchical (objects via an {{ term("ADT", "abstract data type: a data type defined by the operations it supports, not by its internal representation") }} manager) — with the pointed question: can you trace an NFR to code? (slide 11) → [W4.4]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c4).

**Messages go to a specific address; events are emitted for anyone listening.** Messages: unique addresses, recipients await and react. Events: emitted on state change, immutable, ordered, sent to publishing infrastructure (slide 12) → [W4.4]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c4).

**The Grab-like taxi-booking exercise maps operations to events/messages — quality attribute satisfied: reliability** (slide 13; the slide provides the instruction and the tag — the mapping is the exercise) → [W4.4]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c4).

**Decompose with guidelines: divide and conquer, high abstraction, more cohesion, less coupling, reuse, flexibility** (slide 14) → [W4.5]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c5).

**{{ term("Modularity", "decomposing a big chunk into smaller chunks with well-defined interfaces (APIs) — Parnas's way to manage complexity") }} (Parnas): decompose into smaller chunks with well-defined interfaces** — shorter development time, better flexibility, better comprehensibility (slide 15) → [W4.5]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c5).

**Slice horizontally (by technical layer — one layer, every domain) or vertically (by business domain — one capability, top to bottom).** The deck's grid is the errand platform: users, vendors, orders, credits × presentation, API, business logic, persistence (slide 16) → [W4.5]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c5).

**{{ term("Cohesion", "how strongly a module's facilities belong together — higher is better") }} types (functional → utility) and {{ term("coupling", "how strongly modules depend on each other — lower is better") }} types (content → import) grade the decomposition** (slides 17–18) → [W4.6]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c6).

**Styles follow philosophies, categorized by two questions: how is the code divided (technical vs domain) and how is it deployed (monolith vs distributed)?** The 2×2 names {{ term("layered", "monolithic × technical style: layers with downward-only dependencies (Week 6)") }}, {{ term("modular monolith", "monolithic × domain style: one deployed unit, domain-partitioned modules") }}, {{ term("event-driven", "distributed × technical style: components react to events (Week 9)") }}, and {{ term("microservices", "distributed × domain style: independently deployable domain services (Weeks 7–8)") }} (slides 19–22) → [W4.7]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c7).

</panel>

<panel type="seamless" minimized header=":glyphicon-facetime-video: **Deck 2 — Alternative Examples for Product Backlog** %%*(all slides — the errand platform)*%%">

**This deck is the course's fully-worked example requirements for the errand/pickup platform, organized by service.**

- **User service:** trusted users perform important actions (verify before editing a pickup place, withdrawing an errand, or confirming delivery; the edge proxy decodes JWTs on every private call), and account safety (disable a profile after 3 failed password or OTP attempts; re-enable via university-email verification link; collect only useful data).
- **Supplier service:** display every usable vendor and handover point when a requester starts an errand, with label and type; secure supplier administration (proper permissions, no confidential details on failed requests, extra protection on staff-only URLs).
- **Credit service:** wallet rewards (bonus credits after email verification, never double-loaded; reward changes while an errand waits; charge the difference; transfer on delivery confirmation; refund on removal, abandonment, or a missed pickup) and exactly-once wallet events (replay tags in Kafka headers, Redis-checked before wallet operations).
- **Order service:** replacement couriers (one outstanding errand per student; races rejected; a 10-minute freeze on the replacement screen with a stand-by queue) plus dependability and capacity NFRs (nothing inconsistent on restarts, late messages, or retries; the whole campus supported — three Docker containers per microservice behind {{ term("Nginx", "an open-source web server also used as a reverse proxy and load balancer") }} with Kubernetes auto-scaling).

%%This deck grounds Week 3's running example and Tutorial 2's milestone work; every quoted requirement in the [Week 3]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c3) and [Week 4]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c1) chapters cites it by service.%%

</panel>

</span>

<span id="tutorial-summary">

Tutorial 2 works your project Milestone D1 on the errand platform: draft functional and non-functional requirements (at least two levels of refinement) to scope the project, plan it on a Gantt chart, and — optionally — build a backlog for a new product (ClassPulse) and elicit its requirements with an LLM.

</span>

<span id="tutorial">

### Tutorial 2

{% from "schedule/macros-fragment.md" import term, example with context %}

**What this practises:** turning a project description (must-have Mx and nice-to-have Nx features) into a traced, prioritized {{ term("product backlog", "the ordered list of a product's requirements, each with type, identifier, description, priority, and planned sprint (Week 3)") }} (W3.3), planning the work with concrete dates, and — optionally — LLM-assisted elicitation (W3.7, W2.2). Prerequisite: read the project document fully before starting. Come prepared: finish Question 1 quickly so you can enjoy Question 2.

**Materials:**

* %%Tutorial sheet (PDF kept offline)%%

%%No model solution was provided for this tutorial — your team's answers are the deliverable, discussed in class.%%

**Question 1, Task 1.1 — Draft the backlog.** From the project description's Mx and Nx features, draft functional requirements and related non-functional requirements (see L3-Requirements for examples) — this forms your project scope. Detail the high-level Mx/Nx requirements with at least two levels of refinement. If time permits, prioritize the requirements and draft an execution plan.

<box type="tip" seamless>

**What a strong answer looks like** (from the tutorial's appendix and the L3 examples): rows like `F1: Support user account creation` → `F1.1: New users can create an account using their username, email and password` → `F1.1.1: The system should ensure that the account being created has a unique username and email to prevent duplicates` (High, sprint 1); supplier rows like `F2.1: The system should display the suppliers with name and category visible when the user is logged in` — with the product-centric wording preferred over the usage-centric "Users can view supplier name and category when logged in"; NFRs like `N1.1: Support an initial capacity of up to 30000 registered users` and `N2.1.1: Response time for all page loads should take no more than 2 seconds` — measurable, so verifiable. The errand-platform deck shows the target end-state for two refinements down (e.g., wallet events with replay tags for exactly-once effects).

</box>

**Question 1, Task 1.2 — Plan it.** Develop a Gantt chart — a timeline bar chart with one row per activity and bars spanning its planned start and end dates — (or an equivalent) for the project's aspects (must-haves, nice-to-haves). It need not be refined, but it must have concrete dates/weeks of the semester — not "Sprint 1, Sprint 2". During the tutorial: discuss the plan and the risks to achieving it; collect mitigation ideas.

**Question 2 [Optional] — ClassPulse, a fresh backlog.** A web platform to help instructors visualize class participation and engagement in real time (attendance, quiz submissions, chat and assignment interactions; trend identification; shareable visualizations).

* **Task 2.1:** develop a product backlog of 5–10 functional requirements (labelled, tabular, no user stories), prioritize them and explain why; then up to three NFRs tied to those FRs, each with a 1–2 sentence application-specific description.
* **Task 2.2:** provide the product context to your favourite LLM and *elicit* requirements interactively (don't ask for a list). Assign a persona (end user, teacher, year-1 students), probe for details, refinements, pain points, constraints, and exceptions that lead to NFRs; seek importance ratings for planning. Document what probing changed about response quality.

<box type="tip" seamless>

**Connecting Question 2 to the lectures:** Task 2.1 rehearses W3.3 (backlog, usage- vs product-centric wording, priorities); Task 2.2 rehearses W3.7's AI-in-requirements-engineering uses (persona specification, contextual questions) with W3.7's caveat attached: don't simply trust the black box — outputs are non-deterministic and unexplainable.

</box>

</span>
