{# Definitions for week-03. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-03.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable. #}

<span id="def-requirement">

A **requirement** is a condition or capability needed by a user to solve a problem or achieve an objective, or a condition or capability that must be met or possessed by a system to satisfy a contract, standard, specification, or other formally imposed document — or a documented representation of either.

<sub>-- IEEE, quoted on L3 slide 3</sub>

</span>

<span id="def-functional-requirement">

A **functional requirement (FR)** specifies something the system should do — typically a behavior or function, e.g., "The passenger shall be able to print boarding passes for all flight segments for which she has checked in."

<sub>-- L3 slide 9</sub>

</span>

<span id="def-non-functional-requirement">

A **non-functional requirement (NFR)** describes a constraint on the system or its development that is not directly related to specific functionality — it describes how well the system works, e.g., "Mean time between failure ≥ 9000 hrs."

<sub>-- L3 slide 9</sub>

</span>

<span id="def-quality-attribute">

A **quality attribute** is a property of the system — such as performance, scalability, security, or usability — that contributes to its quality; a combination of quality attributes defines the software quality, and they are usually stated as non-functional requirements.

<sub>-- L3 slide 10</sub>

</span>

<span id="def-availability">

**Availability** is the proportion of time a system is operational and able to serve requests when required — a measured quality attribute, usually stated over a window (e.g., the share of a month in which the service answers requests). It is a different attribute from **reliability** (W3.5): reliability is about how long the system keeps working correctly, availability about the fraction of time it is usable — a system can be available but unreliable (it fails often but restarts quickly) or reliable but unavailable (it rarely fails but is down for a long maintenance window). Blue-green deployment buys availability by removing the downtime window (W1.5); a single point of failure destroys it (W12.4).

%%Source: L3 slide 10 lists availability in the quality-attribute taxonomy without defining it; standard definition after ISO/IEC 25010:2011 (availability as the degree to which a system is operational and accessible when required for use) and IEEE Std 610.12.%%

</span>

<span id="def-safety">

**Safety** is the quality attribute of a system not causing harm to life or property — being bug-free is not the same as being safe. Safety matters where software failure has physical stakes: a controller regulating wall pressure in a chemical plant is safety-critical, because software that fails to control the pressure can let it build until the plant explodes.

%%Source: L3 slide 10 lists safety in the taxonomy without defining it; definition and example from the lecture discussion (L3 recording, ~[55:00]).%%

</span>

<span id="def-requirement-tradeoff">

A **requirement trade-off** is a design situation in which improving one quality attribute degrades another — e.g., adding redundant checks and backups improves reliability but makes the system slower and costlier — forcing prioritization under resource constraints.

<sub>-- L3 slide 23</sub>

</span>

<span id="def-product-backlog">

A **product backlog** is the ordered list of a product's requirements, each with a type, a unique identifier, a description, a priority, and a planned sprint; it allows work allocation, developing test specifications, and design development.

<sub>-- L3 slides 7, 26</sub>

</span>

<span id="def-elicitation">

**Requirements elicitation** discovers requirements — e.g., by interview, workshop, document analysis, or prototyping.

<sub>-- L3 slide 4</sub>

</span>

<span id="def-requirements-analysis">

**Requirements analysis** analyzes, decomposes, derives, and understands requirements, negotiates them, and identifies gaps.

<sub>-- L3 slide 4</sub>

</span>

<span id="def-specification">

**Requirements specification** produces written and illustrated requirements for comprehension, review, and use.

<sub>-- L3 slide 4</sub>

</span>

<span id="def-requirements-validation">

**Requirements validation** confirms the correct set of requirements — the set that traces back to business objectives and will enable developers to build a solution; corrections feed back into elicitation.

<sub>-- L3 slides 4, 28</sub>

</span>

<span id="def-event-response-table">

An **event-response table** is an elicitation source that identifies external stimuli and describes the system's responses to each.

<sub>-- L3 slide 5</sub>

</span>

<span id="def-usage-centric-requirement">

A **usage-centric requirement** states a capability from the user's point of view — "As a user, I can upload an image into the system so that I can showcase my photography skills to the world."

<sub>-- L3 slide 6; Quiz 1 Q9</sub>

</span>

<span id="def-product-centric-requirement">

A **product-centric requirement** states what the system will do — "The system will support a range of graphic file formats up to 20 mb in size" — and is refined into testable system statements.

<sub>-- L3 slide 6; Quiz 1 Q9</sub>

</span>

<span id="def-requirement-refinement">

**Requirement refinement** decomposes a requirement into child requirements at least two levels deep — from capability ("allow user to register using email/password") to testable rule ("password should contain upper and lower case letters and numbers, minimum length, avoid dictionary attack").

<sub>-- L3 slides 6, 8</sub>

</span>

<span id="def-software-requirements-specification">

A **software requirements specification (SRS)** is a traditional textual requirements document that only records what is to be done in the project — unlike the product backlog, it is not by itself a planning tool for sequencing the work. It is typically a large, static artifact mixing in design and team-allocation decisions: developed once, signed off, and rarely updated — which suits stable, contract-driven projects more than modern evolving products.

<sub>-- L3 slide 29; static-artifact critique from the lecture (L3 recording, ~[35:00])</sub>

</span>

<span id="def-requirement-traceability">

**Requirement traceability** gives each requirement a type, a unique identifier, a brief high-level description, a priority, and other information (e.g., sprint-id), and traces it to use-case, design-document, code-module, and test-case references.

<sub>-- L3 slide 26</sub>

</span>

<span id="def-external-quality-attribute">

An **external quality attribute** is observed when the software is executing and impacts the user's experience — it develops the user's perception of software quality.

<sub>-- L3 slide 11</sub>

</span>

<span id="def-internal-quality-attribute">

An **internal quality attribute** is not directly observed when the software is executing — it is perceived by the developers and maintainers, and encompasses aspects of design that may impact external attributes.

<sub>-- L3 slide 11</sub>

</span>

<span id="def-security">

**Security** is the system's ability to resist unauthorized use while still providing its services to legitimate users. Core concerns: confidentiality and integrity; it relies on authentication, authorization, and auditing. Record security requirements early in the product cycle, and make them specific and testable.

<sub>-- L3 slide 14</sub>

</span>

<span id="def-confidentiality">

**Confidentiality** protects data against unauthorized disclosure or access.

<sub>-- L3 slide 14</sub>

</span>

<span id="def-integrity">

**Integrity** protects data against unauthorized modification — the security sense used in W3.5. The same word names a *design quality* in Week 7: when several services each own a copy of data, integrity is the property that the copies stay consistent (no duplicate or contradictory records) — the sense behind the microservices trade-off "Integrity — each service owns its data … potential data duplication causes inconsistencies" (W7.3; L7 slide 14).

<sub>-- L3 slide 14; W7 sense: L7 slide 14</sub>

</span>

<span id="def-authentication">

**Authentication** establishes who the user is — e.g., the preferred strategy for resolving forgotten passwords, addressing account lockouts, expiring inactive sessions, and re-authenticating critical transactions.

<sub>-- L3 slide 14</sub>

</span>

<span id="def-authorization">

**Authorization** decides what an authenticated user is allowed to do.

<sub>-- L3 slide 14</sub>

</span>

<span id="def-auditing">

**Auditing** records actions so misuse can be detected or investigated — specifying what activity should be logged, at what level of detail, and who should have access to the logs.

<sub>-- L3 slide 14</sub>

</span>

<span id="def-performance">

**Performance** primarily encompasses the responsiveness of the system; low performance means unhappy users, and in real-time systems it can impact safety. Performance requirements affect the choice of architecture (monolithic vs microservices), design, and deployment, plus hardware and network choices.

<sub>-- L3 slides 15–17</sub>

</span>

<span id="def-caching">

**Caching** stores frequently accessed data closer to the user — high-speed, typically transient storage holding a subset of the data (e.g., Amazon ElastiCache, Redis) — one approach to improving performance.

<sub>-- L3 slide 18</sub>

</span>

<span id="def-deployability">

**Deployability** is the ease and speed of getting software to production — software allocated to an environment for execution within a predictable, acceptable amount of time and effort. It is measured by deployment frequency, change failure rate, and MTTR, and is impacted by CI/CD, containerization, DevOps, and architectural decisions such as serverless and microservices.

<sub>-- L3 slide 21</sub>

</span>

<span id="def-usability">

**Usability** measures the effort required to prepare input, operate, and decipher the output of the software — e.g., average time to specify inputs, number of interactions to get information, time to complete a task, user errors or trials needed, and waiting time. It packs in ease of learning (meaningful messages, verbose prompts, tooltips) and ease of use (customizations, autocompletion, autocorrection, scriptable).

<sub>-- L3 slide 22</sub>

</span>

<span id="def-reliability">

**Reliability** is the ability of the system to keep working correctly over time. The deck's trade-off table shows the cost: improving reliability by introducing redundant checks, backups, and recovery routines makes the system slower and more resource-hungry, degrading efficiency.

<sub>-- Quiz 1 Q7; L3 slide 23</sub>

</span>

<span id="def-interoperability">

**Interoperability** is the ability of the system to operate with other systems. The deck's trade-off table shows the cost: improving interoperability by allowing open data exchange and API access can expose the system to more vulnerabilities, weakening security.

<sub>-- Quiz 1 Q7; L3 slide 23</sub>

</span>

<span id="def-efficiency">

**Efficiency** is how well the system uses its resources — doing its work without waste of time, hardware, or money. It is the attribute that pays for reliability's redundant checks, backups, and recovery routines.

<sub>-- Quiz 1 Q7; L3 slide 23</sub>

</span>

<span id="def-pairwise-prioritization">

**Pair-wise prioritization** compares requirements (or quality attributes) two at a time to force an order: for each pair, ask "if we could fund only one of these two, which one?" — the more important item wins the head-to-head, and tallying the wins across all pairs yields the overall ranking, with the consistent losers exposing the nice-to-haves. One concrete scoring from the lecture: each favored comparison earns 1 point, each indifference 0.5, each loss 0 — tally the scores and pick the top items (e.g., the top four for a four-member team). Feasibility takes priority: an infeasible requirement is dropped before it is ranked.

%%Scoring detail: L3 recording, ~[89:00].%%
<sub>-- L3 slides 23, 25</sub>

</span>

<span id="def-moscow-prioritization">

**MoSCoW prioritization** sorts requirements into four classes — **must have** (needed for the product to succeed), **should have** (valued but not necessary), **could have** (nice to have), and **will not have** (explicitly excluded this time) — so the team agrees on what it is deliberately *not* doing, not only what it is doing.

%%Source: named in the lecture (L3 recording, ~[87:00]) and in the prioritization reference linked on L3 slide 23. Wording after Atlassian, "Product prioritization frameworks" (tertiary source).%%

</span>

<span id="def-requirement-verification">

**Requirements verification** checks whether you have written the requirements right: the requirements have the desirable properties — completeness, correctness, feasibility, prioritization, unambiguity. It is done informally (peer desk-check, pass-around, walkthrough) or formally (inspection — a formal process with a checklist).

<sub>-- L3 slide 28</sub>

</span>

<span id="def-requirements-management">

**Requirements management** is the loop of collecting initial requirements from stakeholders; analyzing; defining and recording; prioritizing; agreeing on and approving; tracing to work items; querying stakeholders after implementation on needed changes; utilizing test management to verify and validate; assessing the impact of changes; revising; and documenting changes.

<sub>-- L3 slide 32, after IBM</sub>

</span>
