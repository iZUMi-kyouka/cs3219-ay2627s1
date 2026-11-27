<span id="summary">

**Organising question:** what does the discipline of software engineering actually cover, and how do application types, processes, and deployment choices shape the software we run?

The deck opens with the L0 course introduction — the course map (lecture topics and assessment) — then covers:

* software engineering as a response to the software crises (1960s, and Crisis 2.0)
* types of software applications and cloud models (IaaS/PaaS/SaaS; cloud-enabled vs cloud-native)
* software processes: generic phases, factors, Scrum, and the product backlog
* deployment mechanisms: bare metal, virtual machines, containers, serverless
* software delivery: deployment pipelines, CI/CD, release strategies (in-place, rolling, blue-green, canary), and DevOps

</span>

<span id="toc">

* [W1.1 Software engineering and the software crisis]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c1)
* [W1.2 Types of software applications]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c2)
* [W1.3 Software processes and the product backlog]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c3)
* [W1.4 Deployment mechanisms: bare metal, VMs, containers, serverless]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c4)
* [W1.5 Software delivery: CI/CD pipelines, release strategies, DevOps]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c5)

</span>

<span id="lecture">

### Lecture

%%Enrichments from the lecture recording — explanations, analogies, and Q&A — are woven into the linked chapter units, marked "(L1 recording, ~[MM:SS])". Course-administration content (attendance, quiz logistics, team formation, the feedback form, the textbook list) is not course content and is omitted. Note: the deck's delivery/CI-CD/DevOps slides (pp. 39–50) were taught at the start of the L2 recording — their enrichments live in the chapter's [W1.5 unit]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c5).%%

<panel type="seamless" minimized header=":glyphicon-facetime-video: **Part 0 — Course introduction** %%*(slides 1–10)*%%">

**The teaching team and the course shape come first.** Lecture topics: applications/deployment/processes (1–2 lectures), requirements & quality attributes (1–2), software architecture (4–5), communication and messaging patterns (2), scalability (1) — with tutorials aligned to the lecture topics (slide 4).

**Assessment:**

* **Project 40%** — microservice-architecture design and development, process, technical communication; teams of 4–5
* **Exam 40%** — closed book, one A4 cheat sheet
* **Quizzes 10%** — up to six, in lecture slots
* **Participation 10%**

The deck also sets its (Gen = generative) AI usage policy: you choose the collaboration mode, and you are responsible for everything you submit — undisclosed AI-generated work counts as plagiarism (slide 7).

%%These slides are context, not exam content; the site deliberately keeps no admin or grading pages — the course map lives in the [Week 1 chapter]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html).%%

</panel>

<panel type="seamless" expanded header=":glyphicon-facetime-video: **Main deck — Software applications, deployment, and processes** %%*(slides 11–51)*%%">

**Software engineering is a response to software crises.** The IEEE defines it as a systematic, disciplined, quantifiable approach to development, operation, and maintenance of software. The 1960s crisis hit time, cost, and quality, and Dijkstra blamed machines that became "gigantic" (slides 12–13) → [W1.1]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c1).

**Software Crisis 2.0 (1970–now) is driven by data and device abundance.** Push factors (hardware advances, cost reductions, device proliferation, infinite data) meet pull factors (digital natives — people who grew up with digital technology), and the responses are this course's syllabus: cloud computing, data analytics, security, IoT (internet-connected devices), edge computing (processing near the device), DevOps, CI/CD, microservices (slide 14) → [W1.1]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c1).

**Applications differ on four axes, so they are not developed and deployed the same way.** Nature of code and data, deployment mode, clients, and computation/response style (slide 16) → [W1.2]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c2).

**Cloud computing is rented infrastructure delivered over the internet.** IaaS/PaaS/SaaS models differ in what the vendor manages. Cloud-enabled (adapted legacy) is not cloud-native (built for the cloud: microservices, containers, APIs, immutable infrastructure) (slides 17–19) → [W1.2]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c2).

<panel type="seamless" minimized header="%%What are the cloud service models?%%">

<include src="../../se-book-adapted/common/defs-week-01.md#def-cloud-service-models" trim />

</panel>

<panel type="seamless" minimized header="%%Cloud-enabled vs cloud-native — what is the difference?%%">

<include src="../../se-book-adapted/common/defs-week-01.md#def-cloud-enabled" trim />

<include src="../../se-book-adapted/common/defs-week-05.md#def-cloud-native" trim />

</panel>

**A software process arranges development into manageable activities.** Six factors shape the choice (requirements, resources/time, criticality, people, consequences, technology). Scrum is the agile answer — iterative development with feedback loops (slides 21–23) → [W1.3]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c3).

<panel type="seamless" minimized header="%%What is Scrum?%%">

<include src="../../se-book-adapted/common/defs-week-01.md#def-scrum" trim />

<include src="../../se-book-adapted/common/defs-week-01.md#def-sprint" trim />

</panel>

**The product backlog makes the process concrete.** PeerPrep's backlog shows requirements refined to 2–3 levels, each with a priority and a planned sprint (slide 24) → [W1.3]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c3). Requirements themselves arrive in Week 3.

<panel type="seamless" minimized header="%%What is a product backlog?%%">

<include src="../../se-book-adapted/common/defs-week-03.md#def-product-backlog" trim />

</panel>

**Deployment decisions affect the quality attributes users feel.** Six deployment considerations map onto portability, availability, performance, interoperability, maintainability, security, and usability (slides 25–29) → [W1.4]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c4).

**Deployment mechanisms trade control for utilization.** From most control to most utilization:

* **Bare metal** — applications run directly on the hardware: full control, wasted resources
* **Virtual machines** — better utilization, but a full guest OS each; side channels, noisy neighbours
* **Containers** — lightest packaging; ideal for CI/CD
* **Orchestration** — Kubernetes coordinates and scales containers
* **Serverless** — you ship code, the provider runs it on demand

(slides 30–38) → [W1.4]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c4).

<panel type="seamless" minimized header="%%What is each deployment mechanism?%%">

<include src="../../se-book-adapted/common/defs-week-01.md#def-bare-metal" trim />

<include src="../../se-book-adapted/common/defs-week-01.md#def-virtual-machine" trim />

<include src="../../se-book-adapted/common/defs-week-02.md#def-containerization" trim />

<include src="../../se-book-adapted/common/defs-week-01.md#def-serverless" trim />

</panel>

**Delivery is a pipeline, not an event.** A deployment pipeline automates build–deploy–test–release:

* **Continuous integration** verifies every check-in
* **Continuous delivery** keeps good builds releasable
* **Continuous deployment** releases automatically

(slides 39–42) → [W1.5]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c5).

<panel type="seamless" minimized header="%%What is CI/CD?%%">

<include src="../../se-book-adapted/common/defs-week-02.md#def-ci-cd" trim />

<include src="../../se-book-adapted/common/defs-week-01.md#def-continuous-delivery" trim />

<include src="../../se-book-adapted/common/defs-week-01.md#def-continuous-deployment" trim />

</panel>

**Release strategies trade downtime against risk.** In-place, rolling, blue-green (two identical environments; near-zero downtime), and canary (incremental rollout, A/B testing) (slides 43–45) → [W1.5]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c5).

<panel type="seamless" minimized header="%%What is each release strategy?%%">

<include src="../../se-book-adapted/common/defs-week-01.md#def-in-place-deployment" trim />

<include src="../../se-book-adapted/common/defs-week-01.md#def-rolling-deployment" trim />

<include src="../../se-book-adapted/common/defs-week-02.md#def-blue-green-deployment" trim />

<include src="../../se-book-adapted/common/defs-week-01.md#def-canary-deployment" trim />

</panel>

**DevOps makes the pipeline an organizational habit.** Combining Dev and Ops reduces commit-to-production time at high quality, via CI, CD, monitoring and logging, collaboration, and infrastructure as code — with benefits in speed, reliability, scale, and collaboration (slides 46–50) → [W1.5]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c5).

<panel type="seamless" minimized header="%%What is DevOps?%%">

<include src="../../se-book-adapted/common/defs-week-02.md#def-devops" trim />

</panel>

</panel>

</span>
