{% from "schedule/macros-fragment.md" import term, example with context %}
<h2>Week 1 — Software Development Processes</h2>

<span>None — this is the first chapter. It maps the terrain every later chapter explores.</span>

<span>

* Can explain why software engineering exists as a discipline and what the software crises were
* Can classify a software application by deployment mode, nature of code and data, and computation style
* Can describe a software process and locate Scrum and the product backlog within it
* Can compare deployment mechanisms — bare metal, virtual machines, containers, serverless — and when each fits
* Can explain what CI/CD and DevOps automate and name the common continuous-deployment strategies

</span>

<div>

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

**This chapter maps the terrain the rest of the course explores.** The Week 1 deck opens with a short course-introduction section (its "L0" slides), then covers software engineering as a discipline, types of applications, software processes, and the delivery pipeline that carries software to its users. Requirements (Week 3), architecture (Weeks 4–8), messaging (Weeks 9–11), and scalability (Week 12) all land on this map.

<box type="info" seamless>

**Course map** %%((Source: L1 slides 4–5 — the "L0" course-introduction section of the deck.))%%

**Lecture topics:** software applications, deployment & processes (1–2 lectures) · software requirements & quality attributes (1–2 lectures) · high-level design — software architecture (4–5 lectures) · communication and messaging patterns (2 lectures) · software scalability (1 lecture). Tutorials are aligned with the lecture topics.

**Assessment:** project 40% (design and development with a {{ term("microservice architecture", "an architectural style that decomposes an application into small, independently deployable services, one per business capability (defined in W1.1)") }}, software process, technical communication; teams of 4–5) · exam 40% (closed book; one A4 cheat sheet allowed) · quizzes 10% (up to six, during lecture slots) · participation 10%. Quizzes and the exam test the topics covered in lectures and tutorials — the same topics this site's chapters and self-checks cover.

</box>

## Core concepts

<span id="W1-c1"></span>

### W1.1 Software engineering and the software crisis ★

**Software engineering exists because building software outgrew what individual craftsmanship could handle.** By the 1960s, projects were routinely late, over budget, and unreliable — the "software crisis" in time, cost, and quality.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-software-crisis" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-software-engineering" trim />
</box>

**The first crisis (circa 1960s) triggered research and development in response.** Its impact was on time, cost, and quality; the response produced the sub-fields this course teaches: software development {{ term("process models", "the arrangement of development activities over time — what a software process prescribes (defined in W1.3)") }}, software architecture, design principles, testing methods, and design patterns (Source: L1 slide 13).

%%"...as long as there were no machines, programming was no problem at all; when we had a few weak computers, programming became a mild problem, and now we have gigantic computers, programming has become an equally gigantic problem." — Edsger Dijkstra, The Humble Programmer (EWD340), quoted on L1 slide 13%%

**A second crisis — "Software Crisis 2.0" (1970–now) — came from abundance, not scarcity.** Push factors: enormous advances in hardware, falling hardware costs, rising processing power, device proliferation, and an effectively infinite amount of available data. Pull factors: {{ term("digital natives", "people who grew up with digital technology and take it for granted") }} consuming technology. The responses named on the slide are exactly this course's syllabus: parallel processing, cloud computing, data analytics, security, IoT (Internet of Things — everyday devices such as sensors and cameras connected to the internet), edge computing (processing data on or near the device that produces it, instead of in a distant cloud data center), DevOps, CI/CD, and microservices (Source: L1 slide 14).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-software-crisis-2" trim />
</box>

{% call example("Quiz 1 Q3 — the farm that grew a crisis 2.0") %}
Quiz 1 describes a farm deploying many low-cost soil, weather, and irrigation sensors that generate a continuous stream of data, creating opportunities for automated farm-condition analysis software. This is a **push** factor: the large number of sensors deployed makes a large volume of data available to use and analyze — the technology push came first, and the software opportunity follows it (Quiz 1 Q3, model answer).
{% endcall %}

<box type="warning" seamless>

**Pitfall / trade-off:** Crisis 2.0's responses are not free wins. Cloud computing, microservices, and continuous deployment each trade a local gain (scale, speed of release) for new complexity — which is why the rest of this course spends weeks on when and how to apply them.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Give one push factor and one pull factor of Software Crisis 2.0, and name two lecture topics of this course that are responses to it.

<panel type="seamless" minimized header="%%Answer%%">

Push: hardware advances, cost reductions, device proliferation, or the infinite amount of available data. Pull: digital natives consuming technology. Responses covered in this course include cloud computing, DevOps/CI/CD, microservices, security, and edge computing (Source: L1 slide 14).

</panel>

**Q2.** Dijkstra blamed the crisis on machines becoming "gigantic". In one sentence, what changed between 1960 and the Crisis 2.0 era?

<panel type="seamless" minimized header="%%Answer%%">

The constraint flipped: in the 1960s the crisis was that software could not keep up with what machines could do (time/cost/quality); since 1970 the crisis is that abundant, cheap, connected hardware produces more data and computation than traditional software practice can exploit (Source: L1 slides 13–14).

</panel>

</panel>

<span id="W1-c2"></span>

### W1.2 Types of software applications ★

**"Different needs, different applications" — and different applications are not developed and deployed the same way.** Before choosing tools, processes, or architecture, characterize what kind of application you have (Source: L1 slides 15–16).

**Applications differ along four axes.** Nature of code and data: closed-source, open-source, and open-content — where open-content is the data-side sibling of open-source: material (text, media, datasets) that others may legally copy, modify, and redistribute, like Wikipedia's articles %%("open content" — dimmed: Wikipedia)%%, versus closed-source code you cannot inspect and open-source code you can. Deployment mode: desktop, embedded and edge, cloud-native. Clients: who and what consumes the software. Computation and response: real-time, concurrent, distributed (Source: L1 slide 16).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-open-content" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-embedded-software" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-real-time-system" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-concurrent-system" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-distributed-system" trim />
</box>

%%The deck lists sub-categories for the other three quadrants but pairs the **Clients** quadrant with a picture only: several client computers sending requests to one web server. Read the axis as "who or what consumes the software" — human users, other systems, or client devices calling your application the way those pictured machines call the web server. Tutorial 1's classification questions (Q1 A–C) exercise only the other three axes, so don't expect a ready-made checklist for this one.%%

{{ term("cloud computing", "software infrastructure hosted on an external data center, with software and services delivered over the internet") }} **Cloud computing comes in service models that differ in how much the vendor manages.**

- **IaaS** (e.g., AWS, Google Cloud) rents raw infrastructure
- **PaaS** (e.g., AWS Elastic Beanstalk, Heroku) hosts your application on a managed platform
- **SaaS** (e.g., Google Apps, Salesforce) delivers a finished application

(Source: L1 slide 17)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-cloud-computing" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-cloud-service-models" trim />
</box>

**Cloud-enabled is not cloud-native.** A {{ term("cloud-enabled", "a legacy enterprise application designed for local data centers but modified to run on the cloud, retaining most of its original features") }} application is a legacy enterprise system designed for local data centers but modified to run on the cloud, retaining most of its original features. A {{ term("cloud-native", "built for cloud environments: immutable infrastructure, microservices, APIs, containers, dynamic management") }} application is built, deployed, and managed for cloud computing environments from the start — its characteristic features are {{ term("immutable infrastructure", "treating servers as replaceable rather than repairable: replace a machine from a fixed image instead of patching it (Week 5)") }}, microservices-based design, API-driven interaction, {{ term("service mesh", "a dedicated infrastructure layer that manages service-to-service communication") }}, containers, and dynamic management, developed with CI/CD, DevOps, and serverless computing (Source: L1 slides 17–18).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-cloud-enabled" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-cloud-native" trim />
</box>

{% call example("L1 slide 19 — two designs for the same web app") %}
The deck contrasts an example cloud-native app design with an example monolithic web-app design for the same kind of product: the cloud-native version is decomposed into small services behind APIs, while the {{ term("monolith", "a system deployed as a single unit — Week 4 contrasts it with decomposed styles") }} runs everything in one deployable unit. The design you pick changes how you build, deploy, and scale — which is why application type is decided early (Source: L1 slide 19, image from Microsoft's cloud-native introduction).
{% endcall %}

{% call example("Tutorial 1 Q1 — four applications, four classifications") %}
Tutorial 1 asks you to classify one of four applications using the L1 axes. The teaching-team suggestions:

- **Smart-home security camera system** — embedded (local motion detection) plus cloud (storage, notifications) and real-time + concurrent + distributed
- **Global video streaming platform** — cloud-native, concurrent and distributed, latency-sensitive (latency is response delay; slow responses ruin a streaming experience)
- **Online banking platform** — cloud/cloud-enabled, concurrent and distributed, closed-source with private financial data
- **Industrial control system** — embedded, real-time, primarily closed-source

(Source: Tutorial 1, teaching-team suggestions Q1).
{% endcall %}

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Classify an online banking platform using the L1 axes: deployment mode, computation and response, and nature of code and data.

<panel type="seamless" minimized header="%%Answer%%">

Cloud (or cloud-enabled), concurrent and distributed (many transactions and regions at once), closed-source code with highly confidential data (Source: Tutorial 1 teaching-team suggestions Q1).

</panel>

</panel>

<span id="W1-c3"></span>

### W1.3 Software processes and the product backlog ★

**A process turns "writing code" into repeatable engineering.** Which process fits depends on the problem — the deck names six factors that shape the choice (Source: L1 slides 21–22).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-software-process" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-sdlc" trim />
</box>

**Six factors affect software development.** Requirements, the process itself (resources, time), criticality, people (competence), consequences, and technology (Source: L1 slide 22). ==A process is a means, not an end: the factors pick the process, not the other way round.==

**Scrum is an agile process built on iterative development with feedback loops.** Work happens in fixed sprints, opened by sprint planning; each sprint ends with a working increment that generates feedback, enabling quick response to changes (Source: L1 slide 23). The diagram below shows that loop and why it responds quickly to change.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-scrum" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-sprint" trim />
</box>

<mermaid>
flowchart LR
    PB["Product backlog<br/>(ordered requirements)"] --> SP["Sprint planning<br/>(pick top-priority items)"]
    SP --> S["Sprint<br/>(design, build, test)"]
    S --> INC["Working increment<br/>(+ demo & feedback)"]
    INC -. "feedback reorders the backlog" .-> PB
</mermaid>

%%Notation: each box is an activity or artifact of Scrum; solid arrows are the flow of work through one sprint; the dashed arrow is the feedback loop that carries what the increment revealed back into the backlog.%%

How to read it for the course example: PeerPrep's backlog lists F1 ("allow user to register using email/password") and its refinements as High priority for sprint 1, while F2.1 (authenticate before updating particulars) sits at Medium for sprint 2; after each sprint's demo, feedback can reorder what sprint planning picks next (Source: L1 slide 24; Quiz 1 Q6).

<box type="info" seamless>

**Telling apart — practice vs process (model) vs methodology.** One question separates them: **how much does the word bundle up?**

| Term | What it names | Course examples |
|---|---|---|
| **Practice** | One repeatable working habit or technique | Continuous integration, continuous delivery, infrastructure as code (L1 slide 48) |
| **Process / process model** | The arrangement of development activities over time — the L1 slide 13 response to the crisis was literally "software development process models" | Scrum's sprints with feedback loops; the generic phases (requirements → design → …) |
| **Methodology** | A named, bundled way of working: a process model plus the practices, roles, and tools that go with it | "Agile" as an umbrella; DevOps is closest in this course — the deck calls it "a set of software development practices" (L1 slide 46), i.e. a bundle, not a single habit |

Worked example: *continuous integration* is a **practice**; adopting it inside fixed sprints makes you follow a **process model** (Scrum); committing to sprints **plus** CI/CD, monitoring, and a Dev/Ops collaboration culture is adopting a **methodology**-scale bundle. Quiz and tutorial questions ask you to operate at the practice and process levels; don't let the words scare you into thinking they are four unrelated concepts.

</box>

**The {{ term("product backlog", "Scrum's single, ordered list of what to build — each entry with an id, description, priority, and planned sprint; formally defined in Week 3") }} is Scrum's single, ordered list of what to build.** Each entry carries an identifier, a description, a priority, and a planned sprint — which is what lets a team allocate work, sequence releases, and plan testing (Source: L1 slide 24; see Week 3 for requirements themselves).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-product-owner" trim />
</box>

<panel type="seamless" minimized header="%%What is a product backlog? (formally defined in Week 3)%%">

<include src="../../se-book-adapted/common/defs-week-03.md#def-product-backlog" trim />

</panel>

{% call example("L1 slide 24 — PeerPrep product backlog rows") %}
Product: PeerPrep — "to be the most awesome interview preparation platform". The backlog refines requirements at least two levels: F1 "PeerPrep should allow user to register using email/password" (High, sprint 1) refines into F1.1 "Validate email and password" (High, sprint 1), which refines further into "Password should be validated based on rules such as it should contain upper and lower case letters and numbers, minimum length, avoid dictionary attack etc.," (High, sprint 1). F2 "PeerPrep should store user information securely" refines into "Password should be salted hashed using SHA256 or equivalent algorithm" (High, sprint 1) — each row tagged with a priority and a planned sprint (Source: L1 slide 24). %%Minor typos in quoted slide text (e.g., the slide's "minumum length") have been silently corrected here.%%

%%Reading the security jargon in these rows (not on the slide): *hashing* a password stores a one-way scrambled digest of it instead of the password itself; *salted* hashing mixes random data in before hashing, so identical passwords still produce different digests; *SHA256* is a standard hash algorithm; a *dictionary attack* guesses passwords from lists of common words — which the validation rules above are designed to block.%%
{% endcall %}

<box type="warning" seamless>

**Pitfall / trade-off:** Iterating is not an excuse for an empty plan. Scrum responds to change *between* increments; inside a sprint the team still commits to planned backlog items — Quiz 1 makes exactly this distinction (a clinic re-prioritizes its backlog after a sprint demo because feedback from the working increment guides subsequent priorities, not because "agile teams must change all requirements after every sprint").
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** (From Quiz 1 Q6.) A prototype of an online appointment system is demonstrated after a two-week sprint. Clinic staff report that urgent appointments need a different booking flow, so the Product Owner reprioritizes the backlog for the next sprint. What is the best reason for changing the backlog instead of continuing the original plan unchanged?

<panel type="seamless" minimized header="%%Answer%%">

Iterative development uses feedback from a working increment to guide subsequent priorities (Quiz 1 Q6, model answer; cf. L1 slide 23).

</panel>

**Q2.** Your team is building a safety-critical machine controller (Tutorial 1, application D). Which of the six factors should dominate your process choice?

<panel type="seamless" minimized header="%%Answer%%">

Criticality (and consequences): strict timing constraints and the risk of physical harm call for more up-front rigor and verification than a low-stakes class project would need (Source: L1 slide 22; Tutorial 1 application D).

</panel>

</panel>

<span id="W1-c4"></span>

### W1.4 Deployment mechanisms: bare metal, VMs, containers, serverless ★

**Deployment decisions directly shape the quality attributes your users feel.** Deployment is the process between acquiring software and executing it; the deck lists {{ term("availability", "the proportion of time the system is up and able to serve requests — a quality attribute, distinct from reliability (defined in Week 3)") }}, performance, security, usability, interoperability, reusability, scalability, portability, and maintainability as the {{ term("quality attributes", "properties of the system — performance, security, usability… — whose combination defines software quality; usually stated as NFRs — non-functional requirements — (formally defined in Week 3)") }} it touches (Source: L1 slide 26).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-deployment" trim />
</box>

**Six deployment considerations each map to quality attributes.** The internet as a virtual worldwide marketplace — applications must reach users on many device and platform combinations, pushing designs toward cloud-nativity (the slide's stated consideration) → portability. Large-scale content delivery between endpoints → availability, performance. Heterogeneous platforms (OS/browser combinations) → interoperability. Dependency and change management ("uses" relationships, versions, compatibility) → maintainability. Coordination and communication among components (API design; synchronous vs asynchronous) → performance. Security (privacy, authentication, authorization, integrity) → security, usability — the slide pairs usability in deliberately: the security mechanisms users must operate (logins, one-time passwords, permission prompts) are part of what they experience, so hardening security taxes usability too (Source: L1 slides 28–29).

<panel type="seamless" minimized header="%%What are quality attributes? (formally defined in Week 3)%%">

<include src="../../se-book-adapted/common/defs-week-03.md#def-quality-attribute" trim />

<include src="../../se-book-adapted/common/defs-week-03.md#def-external-quality-attribute" trim />

<include src="../../se-book-adapted/common/defs-week-03.md#def-internal-quality-attribute" trim />

</panel>

**Three runtime stacks differ in what each application's owner must bring.** ("Tenant" is the multi-tenancy word for the party renting space on shared hardware — here, whoever owns each application.) The diagram below shows the same three applications deployed on bare metal, on virtual machines, and in containers (Source: L1 slide 30).

<mermaid>
flowchart TB
    subgraph BM["Bare metal"]
        A1["App 1"] --- O1["Host OS"]
        A2["App 2"] --- O1
        A3["App 3"] --- O1
        O1 --- H1["Hardware"]
    end
    subgraph VM["Virtual machines"]
        B1["App 1 + Guest OS"] --- HV["Hypervisor"]
        B2["App 2 + Guest OS"] --- HV
        B3["App 3 + Guest OS"] --- HV
        HV --- O2["Host OS"] --- H2["Hardware"]
    end
    subgraph CT["Containers"]
        C1["App 1"] --- CE["Container engine"]
        C2["App 2"] --- CE
        C3["App 3"] --- CE
        CE --- O3["Host OS"] --- H3["Hardware"]
    end    BM ~~~ VM
    VM ~~~ CT
</mermaid>

%%Notation: each box is a layer of the runtime stack; a plain line means "runs on top of", and the three applications sit side by side, each joined to the layer it runs on — as on the slide this diagram recreates. Read each stack bottom-up: hardware → host OS → the layer each tenant adds — nothing on bare metal, a hypervisor that carves the hardware into VMs (each with a full guest OS), only a shared container engine for containers.%%

How to read it for the course example: a smart-home security camera (Tutorial 1, application A) runs its local motion detection straight on the device — bare metal — because local processing needs predictable performance, while its cloud backend (storage, notifications) runs in containers (Source: Tutorial 1 teaching-team suggestions Q2).

**Bare metal buys control and pays in utilization.** Complete control and physical isolation are the upside; potentially wasted hardware resources, cost, scalability issues, and reduced developer productivity are the price (Source: L1 slide 31).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-bare-metal" trim />
</box>

**Virtual machines improve utilization by giving each application a full guest OS.** Reduced cost, flexibility, and scalability are the upside; a full OS still runs inside each VM, VMs are susceptible to {{ term("side-channel attacks", "attacks that extract secrets from physical implementation traces — timing, cache behavior — rather than from the algorithm itself") }}, and the {{ term("noisy neighbour", "one tenant's workload degrades another tenant's performance on the shared hardware") }} problem appears when workloads share hardware (Source: L1 slide 32).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-virtual-machine" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-hypervisor" trim />
</box>

**Containers are lighter than VMs — they include only the OS processes and dependencies the application needs.** This {{ term("containerization", "packaging an application with only the OS processes and dependencies it needs, to run identically on any host") }} gives better hardware utilization and rapid deployment:

- Write once, run anywhere
- Provision containers to run the applications
- Ideal for CI/CD and agile/DevOps practices

Deployments can target the whole system or elements within it, and can be monitored, rolled back, patched, or redeployed easily (Source: L1 slide 33).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-containerization" trim />
</box>

**A container image doubles as the environment description.** Including the runtime with the code caters to heterogeneous platforms (interoperability and portability), supports dependency and change management (maintainability), and manages the environment for both development and deployment — a Dockerfile describes that environment line by line (Source: L1 slide 34).

{% call example("L1 slide 34 — a Dockerfile as an environment description") %}
The deck's example Dockerfile starts `FROM python:3.10-slim`, sets the work directory, installs system dependencies (`build-essential`, `curl`) needed to compile machine-learning (ML) packages, installs `numpy pandas scikit-learn matplotlib seaborn`, copies the project files, and declares `CMD ["python"]`. Anyone who builds this image gets the same environment — that is the reproducibility and "write once run anywhere" claim made concrete (Source: L1 slide 34).
{% endcall %}

Image vs container: the **image** is the blueprint built from the Dockerfile; the **container** is a running instance of that image — one blueprint, many identical instances.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-container-image" trim />
</box>

**Containers are built to be orchestrated.** Containers alone are not suited to running complex applications — real systems need multiple containers doing specific tasks. An orchestrator (e.g., Kubernetes, working over containers built and run with Docker — the dominant container platform) integrates and coordinates the parts, scales the deployment up and down on demand, provides fault tolerance, and provides communication among the containers (Source: L1 slide 36).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-container-orchestration" trim />
</box>

**Serverless goes lighter still: you ship code, the provider runs it on demand.** In the {{ term("serverless", "a cloud-native model where developers package code and the provider provisions, scales, and manages the servers it runs on") }} model there are still servers — developers and enterprises just don't manage them. Applications deploy via containers managed by the platform, respond to demand by scaling automatically, and are metered on demand (no cost when idle), e.g., AWS Lambda. Serverless functions work on Function-as-a-Service (FaaS %%— the slide writes "FAAS"%%) with an event-driven execution model — they run when needed, are {{ term("stateless", "retaining no memory between runs: each invocation starts fresh — which is why continuous in-memory state does not fit serverless") }}, and are ephemeral with short execution times, e.g., batch processing of images and video or scheduled data compression (Source: L1 slides 37–38).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-serverless" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-serverless-function" trim />
</box>

%%"Event-driven" here is the execution-model sense: a function runs in response to a triggering event — an HTTP request, an uploaded image, a scheduled time — and sits idle otherwise. Week 9 uses the same phrase at architecture scale (event-driven architecture); the mechanism is the same idea, react to events instead of running continuously, so the Week 1 term is a preview, not a different concept.%%

<box type="warning" seamless>

**Pitfall / trade-off:** No mechanism wins everywhere. The deck's own "KIV" notes (Singapore-English shorthand for "keep in view" %%— dimmed: Wiktionary, Malaysian/Singaporean English%% — the deck's way of flagging points to keep in mind):

- Containers are not suitable for all applications and not for performance-critical applications (slide 33)
- VMs leak side channels and suffer noisy neighbours (slide 32)
- Bare metal wastes resources and slows developers (slide 31)

Tutorial 1 Q2–Q3 makes you argue the trade-off for a concrete app — e.g., serverless suits a streaming platform's thumbnail generation but never its main video delivery path.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** (From Quiz 1 Q4.) You are deploying an application testbed to test an app on different operating systems for cross-platform testing. Which deployment mechanism is best suited for this?

<panel type="seamless" minimized header="%%Answer%%">

Virtual machines — each guest OS gives you a different operating system on the same hardware, which is exactly what cross-platform testing needs (Quiz 1 Q4, model answer; cf. L1 slide 32).

</panel>

**Q2.** (From Quiz 1 Q8.) Which application is least suitable for typical serverless functions: image thumbnail generation on demand, a scheduled daily build-summary job, a real-time multiplayer game server holding continuous in-memory state and persistent connections, or an API that reads a user profile from a database?

<panel type="seamless" minimized header="%%Answer%%">

The real-time multiplayer game server — serverless functions are stateless and ephemeral with short execution times, so continuous in-memory state and persistent connections don't fit (Quiz 1 Q8, model answer; cf. L1 slide 38).

</panel>

</panel>

<span id="W1-c5"></span>

### W1.5 Software delivery: CI/CD pipelines, release strategies, DevOps ★

**Between "it works on my machine" and "users have the new version" sits a pipeline you design on purpose.** A {{ term("deployment pipeline", "an automated implementation of the application build, deploy, test, and release process") }} is an automated implementation of the application build, deploy, test, and release process; a CI/CD pipeline is the automated workflow that enables teams to build, test, and deploy code efficiently and reliably (Source: L1 slides 39–40).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-deployment-pipeline" trim />
</box>

**Continuous integration detects problems early by integrating small and often.** {{ term("continuous integration", "a practice where developers integrate code into a shared repository several times a day, each check-in verified by an automated build") }} requires developers to integrate code into a shared repository several times a day, with each check-in verified by an automated build (Source: L1 slide 41).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-ci-cd" trim />
</box>

**Continuous delivery keeps every good build releasable; continuous deployment releases it automatically.** Continuous delivery ensures every good build is potentially ready for production release; continuous deployment automates the release of a good build into the production environment. The payoff the deck claims: low-risk releases, faster time to market and early feedback, higher quality, lower cost (Source: L1 slides 41–42).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-continuous-delivery" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-continuous-deployment" trim />
</box>

**Release strategies trade downtime against risk.** In-place deployment stops each running unit (the slide says "module/compute" — a server or compute instance), installs the latest version on it, restarts, and validates — minimal infrastructure disturbance and cost, but availability suffers while the unit is down. Rolling deployment replaces the running infrastructure piece by piece (e.g., old containers replaced one-by-one by new ones) — but old and new versions coexist with no isolation, which complicates rollback. %%In-place vs rolling — tell them apart by asking *what gets replaced*: in-place reuses the same instances (stop → install → restart on each), so capacity dips during the update; rolling retires the instances themselves and brings up new ones one by one, so old and new versions coexist mid-rollout — which is exactly why rollback is complicated.%% Blue-green deployment shifts traffic between two identical environments running different versions — near-zero downtime and easy rollback. Canary deployment incrementally rolls out to a small subset of users first, shrinking the blast radius — the share of users a faulty new version can hurt before anyone intervenes — and enabling A/B testing (showing different variants to different user groups so their behavior can be compared) (Source: L1 slides 43–45).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-in-place-deployment" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-rolling-deployment" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-blue-green-deployment" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-canary-deployment" trim />
</box>

<box type="info" seamless>

**Telling apart — deployment *mechanism* vs release *strategy*.** One question separates them: **are you choosing what the software runs on, or how a new version replaces the old one?**

| | Deployment mechanism (W1.4) | Release strategy (W1.5) |
|---|---|---|
| The question it answers | What does the software run on, and how is it packaged? | How does the new version replace the old one in production? |
| Options in this course | Bare metal, virtual machines, containers (+ orchestration), serverless | In-place, rolling, blue-green, canary |
| Decided by | Hardware needs, control vs utilization, isolation | Downtime tolerance, rollback speed, risk exposure |

Worked example (Tutorial 1, application C — the online banking platform): the mechanism question (Q2) has two defensible answers — VMs for the core transaction services (the conservative choice; stronger separation between workloads) or containers for the stateless services; the strategy question (Q5) is answered **blue-green** because availability and rapid rollback matter most — two answers, to two different questions, about the same system. Changing the mechanism does not force a strategy change, and vice versa.

</box>

The diagram below places the strategies on the pipeline: everything before "release candidate" is continuous integration; the deploy step is where the strategy choice bites.

<mermaid>
flowchart LR
    C["Commit"] --> B["Build"] --> T["Automated tests"] --> G{"Pass?"}
    G -- "yes" --> R["Release candidate<br/>(potentially releasable)"]
    G -- "no" --> F["Fix & re-commit"] --> C
    R --> D["Deploy<br/>(in-place · rolling ·<br/>blue-green · canary)"]
    D --> P["Production"]
    P -. "monitor & feedback" .-> C
</mermaid>

%%Notation: solid arrows are the automated pipeline stages; the diamond is the pass/fail gate; the dashed arrow is the monitoring-and-feedback loop that closes delivery back to development.%%

How to read it for the course example: for the online banking platform of Tutorial 1 (application C), every commit is built and hit with transaction-correctness and security tests (the automated tests stage); only passing builds become release candidates; because incorrect releases have serious consequences, the team chooses **continuous delivery** (a human approval before release) and **blue-green** deployment for near-zero downtime and rapid rollback (Source: Tutorial 1 teaching-team suggestions Q4–Q5).

Blue-green is the strategy worth zooming into, because its mechanism is structural: release is a traffic switch between two identical environments, not an upgrade of anything.

<mermaid>
flowchart LR
    U["Users"] --> RT["Router"]
    subgraph BLUE["Blue — version 1.4 (live)"]
        B["App v1.4"]
    end
    subgraph GREEN["Green — version 1.5 (idle)"]
        G["App v1.5"]
    end
    RT -->|"all traffic today"| B
    RT -.->|"after switch: all traffic"| G
</mermaid>

%%Notation: the two framed environments are separate but identical deployments; the solid arrow is today's live traffic path; the dashed arrow is the same path after the switch — the router, not the application, is what changes.%%

How to read it: L1 slide 44 defines blue/green as "shift traffic between 2 identical environments … run different versions of the application in each", buying near-zero downtime and rollback. Walk it with Tutorial 1's banking platform: v1.4 serves all customers on blue while v1.5 is deployed and {{ term("smoke-tested", "given a quick round of basic checks that catches obvious breakage before deeper testing") }} on green; flipping the router moves everyone to v1.5 in one step, and if the new release misbehaves, flipping back restores v1.4 instantly — no redeploy, no downtime window (Source: L1 slide 44; Tutorial 1 teaching-team suggestions Q5).

**DevOps is the practice umbrella that makes the pipeline an organizational habit.** {{ term("DevOps", "a set of software development practices combining development (Dev) and operations (Ops) to reduce the time from commit to production at high quality") }} combines software development and operations, intending to reduce the time between committing a change and that change running in normal production, while ensuring high quality (Source: L1 slide 46).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-02.md#def-devops" trim />
</box>

**DevOps names its practices concretely.** Continuous integration, continuous delivery, continuous monitoring and logging, communication and collaboration, and {{ term("infrastructure as code", "managing and provisioning infrastructure through version-controlled configuration files, so environments are consistent and repeatable (defined in Week 5)") }}; new roles follow — e.g., site reliability engineers (SREs), who improve customer experience by creating software that improves the reliability of systems in production, fixing issues, responding to incidents, and taking on-call responsibilities (Source: L1 slide 48). The claimed benefits: speed of delivery, reliability, scale, and improved collaboration (Source: L1 slide 49).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-01.md#def-site-reliability-engineer" trim />
</box>

{% call example("Tutorial 1 Q5 — the same release, four strategies") %}
Tutorial 1 asks each application to pick a release strategy. The teaching-team suggestions:

- The smart-home camera system rolls firmware out **canary**-style to a subset of devices and halts if errors increase
- The streaming platform uses **canary** given millions of users
- The banking platform uses **blue-green** because availability and rapid rollback matter most
- The industrial control system uses **in-place** — stop safely, update, restart

(Source: Tutorial 1 teaching-team suggestions Q5)
{% endcall %}

<box type="warning" seamless>

**Pitfall / trade-off:** Continuous deployment is not always the goal. Firmware that affects physical devices, or releases where errors have serious consequences, argue for continuous *delivery* with a human approval step — exactly what Tutorial 1's teams concluded for the camera, banking, and industrial-control applications, while the streaming platform could deploy continuously (Source: Tutorial 1 teaching-team suggestions Q4).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** (Tutorial 1 Q4 style.) A developer has just committed a change. Name three things that should happen automatically before the change reaches users, and the problem each step detects or prevents.

<panel type="seamless" minimized header="%%Answer%%">

Any three of: build (detects compilation errors), automated unit/integration tests (detect logic regressions and broken contracts), static analysis (detects code-quality and vulnerability patterns), container image build (prevents environment drift — environments slowly becoming different from one another), staging deployment (a trial run in a production-like environment; detects deployment-specific failures). The model answers add application-specific steps: security tests for banking, timing/simulation tests for industrial control (Source: Tutorial 1 teaching-team suggestions Q4).

</panel>

**Q2.** Your streaming platform wants to try a new recommendation layout on 5% of users before committing. Which strategy, and why not blue-green?

<panel type="seamless" minimized header="%%Answer%%">

Canary deployment — it incrementally exposes a small subset of users and can double as A/B testing. Blue-green would expose all users to the new version at once (via a traffic shift between two environments), which defeats the 5% experiment (Source: L1 slide 45; Tutorial 1 teaching-team suggestions Q5).

</panel>

</panel>

<box type="info" seamless>

**Section summary**

* **Software engineering is the systematic, disciplined response to two software crises** — 1960s time/cost/quality, and Crisis 2.0's data-and-device abundance (W1.1).
* **Applications differ on four axes** — code/data nature, deployment mode, clients, computation style — and the axes drive the engineering choices that follow (W1.2).
* **A software process arranges SDLC activities;** Scrum runs them in feedback-looped sprints against an ordered product backlog (W1.3).
* **Deployment mechanisms are a utilization/control spectrum** — bare metal → VMs → containers → serverless — each buying something and paying for it (W1.4).
* **CI/CD plus a chosen release strategy plus DevOps practices turn releases from events into routine** (W1.5).

</box>

## Connections

* Software crisis and its responses ↔ L1 slides 12–14 ↔ Quiz 1 Q3 ↔ motivates every later week.
* Application types and cloud models ↔ L1 slides 15–20 ↔ Tutorial 1 Q1 (worked in Week 3's tutorial) ↔ application-specific quality attributes (Week 3).
* Processes, Scrum, product backlog ↔ L1 slides 21–24 ↔ Quiz 1 Q6 ↔ the product backlog takes center stage in Week 3 (requirements) and Week 4's backlog deck.
* Deployment mechanisms ↔ L1 slides 25–38 ↔ Tutorial 1 Q2–Q3 ↔ containerization and orchestration return in the cloud-native paradigm (Week 5).
* Delivery pipeline, CI/CD, strategies, DevOps ↔ L1 slides 39–50 ↔ Tutorial 1 Q4–Q5, Q7 ↔ deployability as a quality attribute (Week 3) and deployment decisions in architecture (Week 4).

## Further reading

All of the following are cited on the slides themselves: Dijkstra, *The Humble Programmer* (EWD340); Fitzgerald, *Software Crisis 2.0* (IEEE Computer, 2013); Humble & Farley, *Continuous Delivery*; the AWS blue-green deployments whitepaper; Fowler's *CanaryRelease* bliki; Ebert et al., *DevOps* (IEEE Software, 2016).

## Summary

**Key takeaways**

* **Software engineering is the systematic, disciplined response to two software crises — and this course's topics are that response, itemized.** (→ outcome 1)
* **Application type — code/data nature, deployment mode, clients, computation style — drives every later engineering choice.** (→ outcome 2)
* **A software process arranges SDLC activities; Scrum runs them as feedback-looped sprints against an ordered product backlog.** (→ outcome 3)
* **Deployment mechanisms form a utilization-vs-control spectrum — bare metal → VMs → containers → serverless — each buying something and paying for it.** (→ outcome 4)
* **CI/CD, a chosen release strategy, and DevOps practices turn releasing from an event into a routine.** (→ outcome 5)

**Key terms**

| Term | One-line definition | Unit |
|---|---|---|
| Software engineering | Systematic, disciplined, quantifiable approach to developing, operating, and maintaining software | [W1.1](#W1-c1) |
| Software crisis | The 1960s crisis in time, cost, and quality that triggered R&D into software engineering's sub-fields | [W1.1](#W1-c1) |
| Software Crisis 2.0 | The 1970–now crisis of abundance: push factors (hardware, data) and pull factors (digital natives) meet responses like cloud, DevOps, CI/CD, microservices | [W1.1](#W1-c1) |
| Cloud computing | On-demand delivery of computing resources over the network, pooled across users and billed by use (defined in Week 5) | [W1.2](#W1-c2) |
| Cloud service models | IaaS rents raw infrastructure, PaaS hosts your app on a managed platform, SaaS delivers a finished application | [W1.2](#W1-c2) |
| Cloud-enabled | Legacy enterprise application modified to run on the cloud, retaining most original features | [W1.2](#W1-c2) |
| Cloud-native | Built for cloud environments: immutable infrastructure, microservices, APIs, containers, dynamic management | [W1.2](#W1-c2) |
| Immutable infrastructure | Servers are replaceable, not repairable — replace from a fixed image instead of patching (Week 5) | [W1.2](#W1-c2) |
| Open-content | Material others may legally copy, modify, and redistribute — the data-side sibling of open-source | [W1.2](#W1-c2) |
| Embedded software | Software running inside a dedicated device, interacting with the hardware it controls or senses | [W1.2](#W1-c2) |
| Real-time | Must respond within strict timing constraints — a late answer is a failed answer | [W1.2](#W1-c2) |
| Concurrent | Handles many users or operations at the same time | [W1.2](#W1-c2) |
| Distributed | Components run on multiple networked machines and coordinate over the network | [W1.2](#W1-c2) |
| Software process | The structured set of activities used to develop, operate, and maintain software | [W1.3](#W1-c3) |
| SDLC | A product's life from conception through development, deployment, and operation to retirement | [W1.3](#W1-c3) |
| Scrum | Agile process built on iterative development with feedback loops: sprints ending in working increments | [W1.3](#W1-c3) |
| Sprint | One fixed-length Scrum iteration: sprint planning → design, build, test → working increment + demo | [W1.3](#W1-c3) |
| Product owner | Scrum role accountable for the product backlog's vision and priority ordering | [W1.3](#W1-c3) |
| Product backlog | The ordered list of requirements with type, id, description, priority, and planned sprint (formally defined in Week 3) | [W1.3](#W1-c3) |
| Deployment | The process between acquiring software and executing it | [W1.4](#W1-c4) |
| Quality attributes | Properties — performance, security, usability… — that deployment decisions trade against (formally defined in Week 3) | [W1.4](#W1-c4) |
| Bare metal | Applications run directly on hardware over a host OS: full control and isolation, wasted resources and cost | [W1.4](#W1-c4) |
| Virtual machine | A full software computer (guest OS on a hypervisor): better utilization, but side channels and noisy neighbours | [W1.4](#W1-c4) |
| Containerization | Packaging an application with only the OS processes and dependencies it needs | [W1.4](#W1-c4) |
| Container orchestration | Automated management of containers at scale — scheduling, scaling, self-healing (Kubernetes) (defined in Week 5) | [W1.4](#W1-c4) |
| Serverless | Developers ship code; the provider provisions, scales, and manages the servers it runs on | [W1.4](#W1-c4) |
| Serverless function | FaaS function with event-driven execution: runs when triggered, stateless, ephemeral | [W1.4](#W1-c4) |
| Deployment pipeline | Automated implementation of the build, deploy, test, and release process | [W1.5](#W1-c5) |
| CI/CD | Continuous integration, plus delivery (releasable builds) or deployment (automatic releases) | [W1.5](#W1-c5) |
| Continuous delivery | Every good build is potentially ready for production release | [W1.5](#W1-c5) |
| Continuous deployment | Good builds are released automatically into production | [W1.5](#W1-c5) |
| In-place deployment | Stop each unit, install, restart, validate — cheap, but availability dips while the unit is down | [W1.5](#W1-c5) |
| Rolling deployment | Replace instances one by one — old and new coexist, rollback is complicated | [W1.5](#W1-c5) |
| Blue-green deployment | Shifting traffic between two identical environments running different versions | [W1.5](#W1-c5) |
| Canary deployment | Incremental rollout to a small subset of users first; doubles as A/B testing | [W1.5](#W1-c5) |
| DevOps | Practices combining development and operations to shorten commit-to-production at high quality | [W1.5](#W1-c5) |
| Site reliability engineer | SRE — builds software that improves production reliability; fixes issues, responds to incidents, takes on-call | [W1.5](#W1-c5) |
| Infrastructure as code | Managing infrastructure through version-controlled configuration files (defined in Week 5) | [W1.5](#W1-c5) |

%%Next: Week 2 looks at the newest crisis-2.0 response of all — AI as a software engineering collaborator, from autocomplete to autonomous agents.%%

</div>
