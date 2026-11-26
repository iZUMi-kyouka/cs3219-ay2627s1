<span id="summary">

**Organising question:** what does it mean for an application to be *cloud native* — and how is that different from merely running it in the cloud? This week's **guest lecture by Dell Technologies** ("The Cloud Native Paradigm Shift") separates **cloud computing** (a delivery model: *where* software runs) from the **cloud-native paradigm** (an architecture: *how* software is built and run), then walks through its enablers: microservices, containers, container orchestration with Kubernetes, and immutable infrastructure with IaC.

</span>

<span id="toc">

* [W5.1 The cloud is an abstraction]({{baseUrl}}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html#W5-c1)
* [W5.2 Cloud computing vs cloud native]({{baseUrl}}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html#W5-c2)
* [W5.3 From monolith to microservices]({{baseUrl}}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html#W5-c3)
* [W5.4 Containers]({{baseUrl}}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html#W5-c4)
* [W5.5 Orchestrating containers with Kubernetes]({{baseUrl}}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html#W5-c5)
* [W5.6 Immutable infrastructure and IaC]({{baseUrl}}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html#W5-c6)

</span>

<span id="lecture">

### Lecture

{% from "schedule/macros-fragment.md" import term, example with context %}

*Guest lecture: "The Cloud Native Paradigm Shift" — Dell Technologies (L5).*

**The cloud is an abstraction, and the lecture starts by deflating the buzzword.** A cloud hides pools of compute, storage, and networking behind self-service, elastic, metered interfaces — the six characteristics on the opening comparison slide. Distributed apps long predates the cloud; what changed is who owns the machines. (Slides 3, 11–14.)

**Cloud computing and cloud native are not the same thing: one is *where*, the other is *how*.** The lecture's contrast slide puts cloud computing's characteristics (resource pooling, rapid elasticity, broad network access, pay-as-you-go, on-demand self-service, measured service) on one side and cloud native's architecture on the other, defining {{ term("cloud native", "an approach to building and running applications that exploits the advantages of the cloud computing delivery model") }} as "an approach to building and running applications that exploits the advantages of the Cloud Computing delivery model". (Slides 4–5.) → [W5.2]({{baseUrl}}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html#W5-c2)

**The CNCF (Cloud Native Computing Foundation) definition compresses the whole lecture into one sentence.** Containers, {{ term("service meshes", "dedicated infrastructure layers for managing service-to-service communication — traffic management and telemetry — kept out of application code") }}, microservices, immutable infrastructure, and declarative APIs enable loosely coupled systems that are resilient, manageable, and observable — the five qualities the lecture then lists as *why* to go cloud native. (Slides 6–8.) → [W5.2]({{baseUrl}}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html#W5-c2)

**The monolith's seven limitations motivate the split.** One unit of deployment, tight coupling across all functionalities, a single service, feature work that gets harder over time, technology lock-in, low fault tolerance, and scaling limits; {{ term("microservices", "independently deployable services modeled around business domains") }} answer each limitation with independently deployable, technology-agnostic services modeled around business domains — tight coupling/low cohesion becomes loose coupling/high cohesion. (Slides 15–26.) → [W5.3]({{baseUrl}}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html#W5-c3)

**Containers answer "where do we host them?".** A {{ term("container", "a standardized unit packaging an app with all its dependencies, abstracting it from the environment it runs in") }} packages the app, its libraries, and its language runtime as a standardized unit that abstracts the application from the environment it runs in; Docker (2013) made that packaging the industry standard — build once, run anywhere. (Slides 27–33.) → [W5.4]({{baseUrl}}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html#W5-c4)

**Container sprawl creates a new set of challenges, answered by orchestration.** The {{ term("container orchestration", "automated management of containers at scale: discovery, rollouts, auto-scaling, self-healing, secret/config management") }} story centers on {{ term("Kubernetes", "a container orchestration platform for running distributed apps on containers at scale") }}: {{ term("pods", "the smallest deployable units in Kubernetes; a container resides inside a pod with a unique cluster IP") }} are the smallest deployable units, a {{ term("Deployment", "a Kubernetes resource declaring the desired pod replica count, enforced by the cluster") }} declares the desired replica count, and a {{ term("reconcile loop", "a non-terminating control loop that keeps driving actual state toward the declared desired state") }} drives desired state = actual state — giving self-healing and {{ term("horizontal scaling", "scaling by adding more instances (replicas) of the service, rather than a bigger machine") }} (the Payment Deployment goes from replicas = 1 to 3 under high traffic). (Slides 34–41, 50–66.) → [W5.5]({{baseUrl}}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html#W5-c5)

**Infrastructure itself becomes abstracted away — and immutable.** Apps sit on Kubernetes, which sits on pools of compute/network/storage; servers stop being {{ term("pets", "in the pets-vs-cattle metaphor: unique, cared-for servers that are nursed back to health when sick") }} (unique, nursed) and become {{ term("cattle", "in the pets-vs-cattle metaphor: identical, numbered instances replaced with another when one gets sick") }} (identical, replaced), and {{ term("infrastructure as code", "managing infrastructure through version-controlled, reproducible configuration files") }} makes environments reproducible, declarative, and version-controlled. (Slides 41–49.) → [W5.6]({{baseUrl}}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html#W5-c6)

**The lecture closes with where the ecosystem is heading.** Kubernetes everywhere (data centers, cloud, {{ term("bare metal", "directly on physical hardware, with only a host OS — no virtualization layer (Week 1)") }}, VMs, laptops), and 2025 survey findings: AI workloads as the top growth driver, multi-cloud (running across several cloud providers at once) as the default model, cost as the top pain point. (Slides 65–70.)

</span>

<span id="tutorial-summary">

Tutorial 3 designs a **component-level architecture for NewsTrack** (separating data-source-dependent components from independent processing logic) and revisits **requirements quality** by critiquing the ClassPulse requirements from Tutorial 2.

</span>

<span id="tutorial">

### Tutorial 3

{% from "schedule/macros-fragment.md" import term, example with context %}

**What this tutorial practises:** moving from requirements to a high-level (component-level) architecture — deciding which components depend on particular data sources and which are pure processing logic — and revisiting Week 3's requirements heuristics on a fresh set of requirements. Task 2 reuses the ClassPulse platform brought forward from Tutorial 2.

**Task 1 — NewsTrack: design a component-level architecture**

Jeff Gate, a project manager at PeoplesCollective, wants a tool that **collects news articles from different online sources, processes the text, and provides summaries and sentiment scores**. The initial requirements (Source: Tutorial 3 sheet, Q1 — quoted): NewsTrack should accept a set of news sources (RSS feeds or APIs) and extract articles for the following cases:

* for each article, show the original source and publication date, a cleaned text version (ads, boilerplate, stopwords removed), an automatically generated summary (short form), and a sentiment classification;
* allow users to search articles by keyword and display matched summaries with sentiment tags;
* show aggregated statistics: sentiment distribution for a day/week, top keywords across all sources, most active sources by article count;
* support separate CLI commands for each component of the processing pipeline, e.g., `newstrack fetch –source <rss_url>` (collect and store raw articles), apply text cleaning, generate summary for article, run sentiment analysis on a set, show aggregated trends.

**Task 1(a).** Give a high-level (component-level) architecture. Your design should clearly identify components that are **dependent on particular data sources** (RSS feeds or APIs) versus **independent processing logic**, and should aim to **minimize changes if a new data source is swapped in**.

<panel type="seamless" minimized header="%%Model answer%%">

Model the system as a **pipeline of independent processing components**, with all source dependence isolated in one fetch component:

* a **News Communicator** component that talks to the outside world — containing source-specific subcomponents such as a **request builder** and a **parser**;
* a **Cleaner** (ads, boilerplate, stopwords removed), a **Summarizer**, and a **Sentiment Analyzer** — each consuming the output of the previous component, independent of where the articles came from;
* a **Search** component over the stored articles, and an **Aggregator** for the distribution/keyword/activity statistics;
* a data store for raw and processed articles.

Distinguish **data flow** (articles flowing fetch → clean → summarize → classify → store) from **control flow** (the CLI commands that trigger each stage) — the distinction the teaching team highlights, and a Week 4 concept ([W4.3]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c3)). Because every data-source-specific detail hides behind the News Communicator's interface, swapping a data source touches only that component.
</panel>

**Task 1(b).** How would you need to change the architecture if the underlying data sources changed from RSS feeds to direct API integrations (e.g., New York Times API, Guardian API)?

<panel type="seamless" minimized header="%%Model answer%%">

Only the **subcomponents of the News Communicator** change (e.g., the request builder and parser must speak each API's format); the rest of the pipeline — Cleaner, Summarizer, Sentiment Analyzer, Aggregator — is unaffected. (Source: Tutorial 3 model solution.) There are many valid architectures; the point is that source dependence is confined to one replaceable component.
</panel>

**Task 2 — ClassPulse: critique the requirements** *(brought forward and remixed from Tutorial 2)*

ClassPulse helps educators visualize class participation and engagement statistics in real time, collecting data from attendance, quiz submissions, chat interactions, and assignment submissions. The proposed requirements are on the tutorial sheet (FR1–FR7 and NFR1–NFR3):

* FR1: "ClassPulse shall record a student's attendance for a course when an instructor marks the student as present or absent, together with the course, student, and attendance timestamp."
* FR2: "ClassPulse shall collect attendance, quiz submissions, chat interactions, and assignment submissions, calculate engagement scores, identify trends, and display the results in real time."
* FR3: "The system shall identify students who are falling behind and notify instructors early so that they can take appropriate action."
* FR4: "Instructors shall be able to select a visualization and share it with students enrolled in the relevant course. Students shall be able to view visualizations shared with them."
* FR5: "ClassPulse shall use advanced analytics and artificial intelligence to identify disengaged learners and recommend the best teaching strategies."
* FR6: "The dashboard shall load quickly and allow instructors to filter, sort, export, and share engagement information."
* FR7: "Only authorized instructors shall be able to view class engagement statistics, while students shall only be able to view their own statistics and visualizations explicitly shared with them."
* NFR1: "ClassPulse shall be fast, reliable, secure, user-friendly, and available at all times."
* NFR2: "ClassPulse shall use a cloud database and WebSockets to update engagement statistics within one second for many simultaneous users."
* NFR3: "Under a defined workload of 100 simultaneously active instructors, at least 95% of dashboard requests shall return updated engagement data within two seconds, measured from the request being received by the server to the response being returned."

(%%Tutorial 3 sheet, quoted — the PDF is kept offline%%.)

**Task 2.1.** Some requirements are poorly written. Identify them, and suggest changes.

<panel type="seamless" minimized header="%%Model answer — functional requirements%%">

* **FR1 — strong.** Testable as written: a verification run needs to check only that "present" and "absent" are the only statuses the system records.
* **FR2 — weak.** Undefined terms ("trends", "engagement scores", "real time"); combines too many responsibilities — decompose into separate data collection, metric calculation, trend visualization, and update latency (the last becoming an NFR).
* **FR3 — weak.** Not testable; "falling behind", "early", "appropriate action" undefined; state the detection rule and the notification behaviour separately.
* **FR4 — okay.** Reword to be system-centric rather than user-centric; split into at least one requirement for instructors and one for students.
* **FR5 — weak.** "Advanced analytics and AI" are implementation choices, not system behaviour; split into multiple functionalities.
* **FR6 — weak.** "Load quickly" alludes to a quality attribute — convert to an NFR; overlaps FR4; split.
* **FR7 — weak.** Define access-control terms in a glossary; reword system-centric; split per user.
</panel>

<panel type="seamless" minimized header="%%Model answer — non-functional requirements%%">

* **NFR1 — weak.** Lists several vague quality attributes ("fast, reliable, secure, user-friendly, available at all times") that are not testable; split into separate, quantified NFRs.
* **NFR2 — weak.** Specifies the implementation mechanism (cloud database, WebSockets — a browser–server technology for pushing updates to the page without the client polling) rather than the quality attribute; inadequate performance criteria.
* **NFR3 — strong.** Well-specified and testable (100 simultaneous instructors, 95% of dashboard requests within two seconds, measurement stated); could further define "simultaneous" and the request being measured. (Source: Tutorial 3 model solution.)
</panel>

**Task 2.2 (optional).** Elicit requirements from an LLM: give it the product context and a persona, probe for pain points, constraints, and exceptions that lead to NFRs, and record how the quality of responses changed with different probing styles and tones. Document your experience in the shared slide deck.

**Materials:**

* %%Tutorial sheet (PDF kept offline)%%
* %%Model solution (PDF kept offline)%%

</span>
