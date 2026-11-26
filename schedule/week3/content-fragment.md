<span id="summary">

**Organising question:** how do we pin down what a system must do and how well it must do it — before any design is committed?

The lecture ("Software Requirements & Quality Attributes") covers:

* what requirements are (IEEE definition) and their development phases: elicitation → analysis → specification → validation
* functional vs non-functional requirements; usage-centric vs product-centric specification; the product backlog
* quality attributes: external vs internal; security, performance, scalability, deployability, usability; application-specific attributes
* requirement trade-offs, prioritization, traceability, validation & verification, documentation, requirements management, and AI in requirements engineering

</span>

<span id="toc">

* [W3.1 Requirements and their development]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c1)
* [W3.2 Functional vs non-functional requirements]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c2)
* [W3.3 Specifying requirements: usage-centric vs product-centric, and the product backlog]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c3)
* [W3.4 Quality attributes: external vs internal]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c4)
* [W3.5 Key quality attributes in depth]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c5)
* [W3.6 Requirement trade-offs]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c6)
* [W3.7 Validating, documenting and managing requirements]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c7)

</span>

<span id="lecture">

### Lecture

**A requirement is a condition or capability — of the user, the system, or the document that records them.** The IEEE definition covers all three. A second gloss — due to Sommerville & Sawyer (slide 3; Ian Sommerville is the author of the classic software-engineering textbook) — adds that requirements are a specification of what should be implemented, possibly constraining the development process itself (slide 3) → [W3.1]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c1).

<panel type="seamless" minimized header="%%What is a requirement?%%">

<include src="../../se-book-adapted/common/defs-week-03.md#def-requirement" trim />

</panel>

**Requirements development loops: elicit, analyze, specify, validate.** Each phase has its verb, and validation feeds corrections back (slide 4) → [W3.1]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c1):

* **Elicitation** — discover
* **Analysis** — clarify and close gaps
* **Specification** — rewrite
* **Validation** — re-evaluate, confirm and correct

<panel type="seamless" minimized header="%%What does each phase do?%%">

<include src="../../se-book-adapted/common/defs-week-03.md#def-elicitation" trim />

<include src="../../se-book-adapted/common/defs-week-03.md#def-requirements-analysis" trim />

<include src="../../se-book-adapted/common/defs-week-03.md#def-specification" trim />

<include src="../../se-book-adapted/common/defs-week-03.md#def-requirements-validation" trim />

</panel>

**Requirements have many sources beyond interviews.** Documents, focus groups and product champions, questionnaires (pilot first!), event-response tables, observation of users at work, and prototyping (slide 5) → [W3.1]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c1).

**The same capability can be stated usage-centrically or product-centrically, and refinement goes at least two levels.** The image-upload examples and the FoC user-management refinement show both (slides 6, 8) → [W3.2–W3.3]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c3).

**FRs say what the system does; NFRs say how well.** "The passenger shall be able to print boarding passes…" vs "Mean time between failure >= 9000 hrs" (slide 9) → [W3.2]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c2).

<panel type="seamless" minimized header="%%What are FRs and NFRs?%%">

<include src="../../se-book-adapted/common/defs-week-03.md#def-functional-requirement" trim />

<include src="../../se-book-adapted/common/defs-week-03.md#def-non-functional-requirement" trim />

</panel>

**A combination of quality attributes defines software quality; external attributes are user-felt, internal ones are design-perceived.** The taxonomy spans availability to interoperability (slides 10–11) → [W3.4]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c4).

<panel type="seamless" minimized header="%%What is a quality attribute — and external vs internal?%%">

<include src="../../se-book-adapted/common/defs-week-03.md#def-quality-attribute" trim />

<include src="../../se-book-adapted/common/defs-week-03.md#def-external-quality-attribute" trim />

<include src="../../se-book-adapted/common/defs-week-03.md#def-internal-quality-attribute" trim />

</panel>

**Different applications emphasize different attributes, and deployment strategy is an attribute decision.** (slides 12–13) → [W3.4]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c4)

* **Embedded, web, and desktop software** each carry a prescribed attribute list
* **Blue-green deployment and Docker+Kubernetes** are the deck's attribute-supporting deployment choices

<panel type="seamless" minimized header="%%What is blue-green deployment — and what is container orchestration?%%">

<include src="../../se-book-adapted/common/defs-week-02.md#def-blue-green-deployment" trim />

<include src="../../se-book-adapted/common/defs-week-05.md#def-container-orchestration" trim />

</panel>

**Five attributes get the deep treatment.** (slides 14–22) → [W3.5]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c5)

* **Security** — confidentiality, integrity, authentication/authorization/auditing
* **Performance** — responsiveness; replicated databases, caches; monolith vs microservices
* **Scalability** — horizontal vs vertical
* **Deployability** — deployment frequency, change failure rate, MTTR — mean time to repair
* **Usability** — effort to input, operate, decipher

<panel type="seamless" minimized header="%%What does each attribute measure?%%">

<include src="../../se-book-adapted/common/defs-week-03.md#def-security" trim />

<include src="../../se-book-adapted/common/defs-week-03.md#def-performance" trim />

<include src="../../se-book-adapted/common/defs-week-12.md#def-scalability" trim />

<include src="../../se-book-adapted/common/defs-week-03.md#def-deployability" trim />

<include src="../../se-book-adapted/common/defs-week-03.md#def-usability" trim />

</panel>

**Attributes trade off, and the trade-offs are directional.** The conflict table drives pairwise prioritization. The healthcare examples show the same NFR list weighted differently (slides 23–25) → [W3.6]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c6).

<panel type="seamless" minimized header="%%What is a requirement trade-off — and pair-wise prioritization?%%">

<include src="../../se-book-adapted/common/defs-week-03.md#def-requirement-tradeoff" trim />

<include src="../../se-book-adapted/common/defs-week-03.md#def-pairwise-prioritization" trim />

</panel>

**Requirements are managed artifacts.** Traceability fields (type, id, description, priority, sprint), validation vs verification with informal and formal methods, textual and visual documents, the microservice requirement template, the management process loop, and AI in RE — with the warning not to trust the black box (slides 26–34) → [W3.7]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c7).

<panel type="seamless" minimized header="%%What are traceability, verification, and requirements management?%%">

<include src="../../se-book-adapted/common/defs-week-03.md#def-requirement-traceability" trim />

<include src="../../se-book-adapted/common/defs-week-03.md#def-requirement-verification" trim />

<include src="../../se-book-adapted/common/defs-week-03.md#def-requirements-management" trim />

</panel>

</span>

<span id="tutorial-summary">

Tutorial 1 applies Week 1's material (application classification, deployment mechanisms, serverless, CI/CD, release strategies) to one of four applications — smart-home cameras, video streaming, online banking, industrial control — chosen by your group.

</span>

<span id="tutorial">

### Tutorial 1

**What this practises:** classifying an application (L1 application types), choosing a deployment mechanism and serverless fit, walking a change through CI/CD, and picking a release strategy — then defending each choice's trade-offs. Work with your group on **one** application (A–D) throughout.

<panel type="seamless" minimized header="%%What is each Week 1 term used here?%%">

<include src="../../se-book-adapted/common/defs-week-01.md#def-bare-metal" trim />

<include src="../../se-book-adapted/common/defs-week-01.md#def-virtual-machine" trim />

<include src="../../se-book-adapted/common/defs-week-02.md#def-containerization" trim />

<include src="../../se-book-adapted/common/defs-week-01.md#def-serverless-function" trim />

<include src="../../se-book-adapted/common/defs-week-02.md#def-ci-cd" trim />

</panel>

<panel type="seamless" minimized header="%%What is each release strategy?%%">

<include src="../../se-book-adapted/common/defs-week-01.md#def-in-place-deployment" trim />

<include src="../../se-book-adapted/common/defs-week-01.md#def-rolling-deployment" trim />

<include src="../../se-book-adapted/common/defs-week-02.md#def-blue-green-deployment" trim />

<include src="../../se-book-adapted/common/defs-week-01.md#def-canary-deployment" trim />

</panel>

**Materials:**

* %%Tutorial sheet (PDF kept offline)%%
* %%Model solution (PDF kept offline)%%

**Question 1 — Classify your application (L1 axes).** Is it primarily desktop, embedded, or cloud-native? Real-time, concurrent, and/or distributed? What is the nature of its code and data?

<panel type="seamless" minimized header="%%Teaching-team suggestions%%">

* **A (smart-home cameras):** embedded + cloud; real-time + concurrent + distributed; closed-source, private data.
* **B (video streaming):** cloud-native; concurrent + distributed; latency-sensitive; mostly closed-source.
* **C (online banking):** cloud/cloud-enabled; concurrent + distributed; closed-source, private financial data.
* **D (industrial control):** embedded; real-time; primarily closed-source.

</panel>

**Question 2 — Choose a deployment mechanism.** Which of bare metal, virtual machines, or containers fits the main deployed component? What fits it? Why are the others inappropriate? What disadvantages must you manage? *(Optional: does every part need the same mechanism?)*

<panel type="seamless" minimized header="%%Teaching-team suggestions%%">

* **A:** bare metal for the cameras (predictable local processing), containers for the cloud backend; disadvantage — firmware rollback is harder.
* **B:** containers (huge distributed workload, many releases, scaling, heterogeneous infrastructure); disadvantage — network complexity and monitoring at scale.
* **C:** VMs for core transaction services is a defensible, conservative choice (strong separation, environment control), containers defensible for stateless services; disadvantage — VM overhead and slower scaling.
* **D:** bare metal (max control, predictable hardware access for timing-critical operations); disadvantage — inflexibility, lower hardware utilization.

</panel>

**Question 3 — Would serverless fit any component?** Whole, as a supporting function, or not at all — and why?

<panel type="seamless" minimized header="%%Teaching-team suggestions%%">

* **A:** yes, as supporting functions (motion alerts, snapshot processing); never the continuous local detection.
* **B:** yes, for event-driven side jobs (thumbnails, notifications); never the main video delivery path.
* **C:** limited supporting functions (process notifications); core transaction processing cannot be serverless.
* **D:** no — real-time machinery control shouldn't be serverless.

</panel>

**Question 4 — From commit to user.** (a) Name three things that should happen automatically after a developer commits (CI), and the problem each detects or prevents. (b) Continuous delivery or continuous deployment — which would you choose?

<panel type="seamless" minimized header="%%Teaching-team suggestions%%">

(a) Application-specific automated steps:

* **A** — camera-cloud connectivity test, firmware update test
* **B** — load/concurrency, playback and API integration tests
* **C** — transaction correctness, security tests
* **D** — timing/deadline tests, simulations

Each catches the failure class that matters for that application before users see it.

(b) Delivery vs deployment:

* **A: delivery** — risky firmware affecting physical devices; cloud updates can deploy
* **B: deployment** — huge online service; rapid feedback after rollout
* **C: delivery** — incorrect releases have serious consequences
* **D: delivery** — affects physical equipment

</panel>

**Question 5 — Choose a release strategy.** Is some downtime acceptable? Is rapid rollback important? Does the feature only need testing on a subset of users? Defend your choice against the alternatives.

<panel type="seamless" minimized header="%%Teaching-team suggestions%%">

* **A: canary** — firmware to a subset of devices; stop rollout if errors increase.
* **B: canary** — best for several million users.
* **C: blue-green** — availability needs and rapid rollback matter most.
* **D: in-place** — stop safely, update, restart.

</panel>

<box type="info" seamless>

**Optional questions** (do them if time permits; they are good self-study): Q6 — pick the workflow step where generative AI would have the greatest impact for your application (connects to Week 2). Q7 — pick the two DevOps practices that matter most for your application, give a concrete example of what your DevOps team would do, and map the practices to the Agile manifesto values.

</box>

Worked answers for every question (teaching-team suggestions and annotated student solutions for all four applications): %%Model solution (PDF kept offline)%%.

</span>
