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

**A requirement is a condition or capability — of the user, the system, or the document that records them.** The IEEE definition covers all three; Sommerville's gloss adds that requirements are a specification of what should be implemented, possibly constraining the development process itself (slide 3) → [W3.1]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c1).

**Requirements development loops: elicit, analyze, specify, validate.** Each phase has its verb — discover; clarify and close gaps; rewrite; re-evaluate, confirm and correct — and validation feeds corrections back (slide 4) → [W3.1]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c1).

**Requirements have many sources beyond interviews.** Documents, focus groups and product champions, questionnaires (pilot first!), event-response tables, observation of users at work, and prototyping (slide 5) → [W3.1]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c1).

**The same capability can be stated usage-centrically or product-centrically, and refinement goes at least two levels.** The image-upload examples and the FoC user-management refinement show both (slides 6, 8) → [W3.2–W3.3]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c3).

**FRs say what the system does; NFRs say how well.** "The passenger shall be able to print boarding passes…" vs "Mean time between failure >= 9000 hrs" (slide 9) → [W3.2]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c2).

**A combination of quality attributes defines software quality; external attributes are user-felt, internal ones are design-perceived.** The taxonomy spans availability to interoperability (slides 10–11) → [W3.4]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c4).

**Different applications emphasize different attributes, and deployment strategy is an attribute decision.** Embedded vs web vs desktop lists; blue-green and Docker+Kubernetes as attribute-supporting choices (slides 12–13) → [W3.4]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c4).

**Five attributes get the deep treatment.** Security (confidentiality, integrity, authentication/authorization/auditing), performance (responsiveness; replicated databases, caches; monolith vs microservices), scalability (horizontal vs vertical), deployability (deployment frequency, change failure rate, MTTR), usability (effort to input, operate, decipher) (slides 14–22) → [W3.5]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c5).

**Attributes trade off, and the trade-offs are directional.** The conflict table drives pairwise prioritization; the healthcare examples show the same NFR list weighted differently (slides 23–25) → [W3.6]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c6).

**Requirements are managed artifacts.** Traceability fields (type, id, description, priority, sprint), validation vs verification with informal and formal methods, textual and visual documents, the microservice requirement template, the management process loop, and AI in RE — with the warning not to trust the black box (slides 26–34) → [W3.7]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c7).

</span>

<span id="tutorial-summary">

Tutorial 1 applies Week 1's material (application classification, deployment mechanisms, serverless, CI/CD, release strategies) to one of four applications — smart-home cameras, video streaming, online banking, industrial control — chosen by your group.

</span>

<span id="tutorial">

### Tutorial 1

**What this practises:** classifying an application (L1 application types), choosing a deployment mechanism and serverless fit, walking a change through CI/CD, and picking a release strategy — then defending each choice's trade-offs. Work with your group on **one** application (A–D) throughout.

**Materials:**

* %%Tutorial sheet (PDF kept offline)%%
* %%Model solution (PDF kept offline)%%

**Question 1 — Classify your application (L1 axes).** Is it primarily desktop, embedded, or cloud-native? Real-time, concurrent, and/or distributed? What is the nature of its code and data?
<panel type="seamless" minimized header="%%Teaching-team suggestions%%">

A (smart-home cameras): embedded + cloud; real-time + concurrent + distributed; closed-source, private data. B (video streaming): cloud-native; concurrent + distributed; latency-sensitive; mostly closed-source. C (online banking): cloud/cloud-enabled; concurrent + distributed; closed-source, private financial data. D (industrial control): embedded; real-time; primarily closed-source.

</panel>

**Question 2 — Choose a deployment mechanism.** Which of bare metal, virtual machines, or containers fits the main deployed component? What fits it? Why are the others inappropriate? What disadvantages must you manage? *(Optional: does every part need the same mechanism?)*
<panel type="seamless" minimized header="%%Teaching-team suggestions%%">

A: bare metal for the cameras (predictable local processing), containers for the cloud backend; disadvantage — firmware rollback is harder. B: containers (huge distributed workload, many releases, scaling, heterogeneous infrastructure); disadvantage — network complexity and monitoring at scale. C: VMs for core transaction services is a defensible, conservative choice (strong separation, environment control), containers defensible for stateless services; disadvantage — VM overhead and slower scaling. D: bare metal (max control, predictable hardware access for timing-critical operations); disadvantage — inflexibility, lower hardware utilization.

</panel>

**Question 3 — Would serverless fit any component?** Whole, as a supporting function, or not at all — and why?
<panel type="seamless" minimized header="%%Teaching-team suggestions%%">

A: yes, as supporting functions (motion alerts, snapshot processing); never the continuous local detection. B: yes, for event-driven side jobs (thumbnails, notifications); never the main video delivery path. C: limited supporting functions (process notifications); core transaction processing cannot be serverless. D: no — real-time machinery control shouldn't be serverless.

</panel>

**Question 4 — From commit to user.** (a) Name three things that should happen automatically after a developer commits (CI), and the problem each detects or prevents. (b) Continuous delivery or continuous deployment — which would you choose?
<panel type="seamless" minimized header="%%Teaching-team suggestions%%">

(a) Application-specific automated steps: A — camera-cloud connectivity test, firmware update test; B — load/concurrency, playback and API integration tests; C — transaction correctness, security tests; D — timing/deadline tests, simulations. Each catches the failure class that matters for that application before users see it. (b) A: delivery (risky firmware affecting physical devices; cloud updates can deploy). B: deployment (huge online service; rapid feedback after rollout). C: delivery (incorrect releases have serious consequences). D: delivery (affects physical equipment).

</panel>

**Question 5 — Choose a release strategy.** Is some downtime acceptable? Is rapid rollback important? Does the feature only need testing on a subset of users? Defend your choice against the alternatives.
<panel type="seamless" minimized header="%%Teaching-team suggestions%%">

A: canary — firmware to a subset of devices; stop rollout if errors increase. B: canary — best for several million users. C: blue-green — availability needs and rapid rollback matter most. D: in-place — stop safely, update, restart.

</panel>

<box type="info" seamless>

**Optional questions** (do them if time permits; they are good self-study): Q6 — pick the workflow step where generative AI would have the greatest impact for your application (connects to Week 2). Q7 — pick the two DevOps practices that matter most for your application, give a concrete example of what your DevOps team would do, and map the practices to the Agile manifesto values.

</box>

Worked answers for every question (teaching-team suggestions and annotated student solutions for all four applications): %%Model solution (PDF kept offline)%%.

</span>
