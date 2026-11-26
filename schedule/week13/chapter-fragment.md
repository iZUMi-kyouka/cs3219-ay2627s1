{% from "schedule/macros-fragment.md" import icon_outcome with context %}
<h2 id="title">Week 13 — Course Recap</h2>

<span id="prereqs">

This chapter recaps the whole course, so every chapter is a prerequisite. If a through-line below feels shaky, follow its links back to the defining chapter before moving on.

</span>

<span id="outcomes">

{{ icon_outcome }} **Can state the course's one-line thesis — architecture serves requirements — and name its four through-lines** (W13.1)

{{ icon_outcome }} **Can trace the architecture through-line from monolith to modular monolith to microservices, and the communication through-line from synchronous calls to asynchronous messages** (W13.2, W13.3)

{{ icon_outcome }} **Can place any design decision from the course on the scale cube** (W13.4)

{{ icon_outcome }} **Can retell the whole course as one system's evolution, and use the four past quizzes as targeted self-tests** (W13.5, W13.6)

</span>

<div id="body">

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

## Core concepts

<span id="W13-c1"></span>

### W13.1 The course in one line: architecture serves requirements ★

**Every design decision in this course traces back to a requirement, and most of the consequential ones trace back to a quality attribute.** The recap deck begins where the course began — types of applications, requirements, quality attributes — because architecture choices, design decisions, deployment decisions, and processes and practices all "depend on the application, the audience, the resources available, the skill sets" (L13 slides 2, 12).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-quality-attribute" trim />
</box>

**Quality attributes buy their improvements with trade-offs.** Improving interoperability by opening data exchange and API access can weaken security; improving reliability with redundant checks, backups and recovery routines costs efficiency (Quiz 1 Q7). That is why measurable non-functional requirements — not vague adjectives — are what make architecture decidable (Week 3).

**The deck's practical tips are the thesis in imperative form.** Use "sane" boundaries without overdoing it; use the right level of coupling; keep things that belong together together, and apart if they belong apart; don't surprise the people who consume your design or code; document the decisions and the evolution (L13 slide 13).

<box type="tip" seamless>

**Revise from:** [Week 3 — Requirements]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#core-concepts) and [Week 2 — Modern Software Engineering]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#core-concepts) (why modern practice and AI-assisted engineering change how requirements and quality are engineered).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** A teammate says "we should use microservices everywhere because it's modern". Which course through-line does that answer skip?
<panel type="seamless" minimized header="%%Answer%%">
Requirements and quality attributes: the style must be chosen for the application's needs — scalability, release independence, team structure — not for modernity. L13 slide 12: architecture choices depend on the application, audience, resources and skills.
</panel>

</panel>

<span id="W13-c2"></span>

### W13.2 Through-line 1 — architecture: monolith → modular monolith → microservices ★

**The course's first through-line is how code gets partitioned and deployed: technical partitioning, domain partitioning, then distribution.** The recap deck sorts the styles you have studied by exactly this axis (L13 slide 2) — and the site already owns that map, so it is not redrawn here: the canonical 2×2 of deployment (single vs distributed) × partitioning (technical vs domain) is drawn once in [W4.7 — Architectural styles]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#W4-c7) and toured style by style from [W6.1 — Classifying architectural styles]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c1).

**Modularity was the enabling concept, coupling and cohesion the quality criteria.** Week 4's definitions carry through every later week: microservices are the extreme of high cohesion and low coupling; the modular monolith is domain-partitioned but deployed as one unit — the Smart Kitchen app of Quiz 2 splits recipes and inventory into separate modules because they are separate business domains, yet deploys them as one; REST (Week 6) pushes statelessness and a uniform interface so that web systems scale and evolve. → [Week 4 — Architecture (I)]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#core-concepts), [Week 6 — Architecture (II) & REST]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#core-concepts).

**Microservices are identified with domain-driven design and event storming.** Subdomains become bounded contexts in the solution space; event storming surfaces events, commands and policies — with policies delimiting consistent contexts (Quiz 3 Q4–Q6). The model-code gap stays real: architecture models help us reason about complexity and scale and are not one-to-one maps of the source code (Quiz 2 Q3). → [Week 7 — Microservices (I)]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#core-concepts), [Week 8 — Microservices (II)]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#core-concepts).

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Classify by partitioning: (a) a layered app; (b) Smart Kitchen (recipes + inventory modules, one deployment); (c) TripBook's Guides/Payments/Notifications services.
<panel type="seamless" minimized header="%%Answer%%">
(a) technical; (b) domain — modular monolith; (c) domain *and* distributed — microservices (L13 slide 2; Quiz 2 Q4–Q5; Quiz 3 Q7–Q8).
</panel>

</panel>

<span id="W13-c3"></span>

### W13.3 Through-line 2 — communication: sync → async → events → messages ★

**The second through-line is what happens between the pieces once you cut them apart.** Week 10's taxonomy (synchrony, persistence, cardinality) and Week 9's events set up Week 11's engineering patterns; the recap deck compresses this into one slide: message vs event — *intent matters*; pub-sub; messaging; asynchronicity in the request-reply pattern; architect based on business needs (L13 slides 4–7).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-event-driven-architecture" trim />
</box>

**Synchronous communication couples the caller to the callee's availability; asynchronous communication and events break that coupling.** In the Grab-like app of Quiz 2, Booking's synchronous call to Matching fails with it, while publishing a BookingRequested event lets the middleware hold the event until Matching recovers — reliability by persistence, not by retrying a dead call.

**Events and messages differ in intent, and both need names that say which they are.** An event records that something happened (EquipmentReserved *after* a reservation succeeds); a command instructs (ReserveEquipment); a document carries data to process (Week 11's message construction). Quiz 4 Q1 turns exactly this distinction into a redesign question.

<box type="info" seamless>

**Each step of the sync → async → events → messages through-line is separated from its neighbour by exactly one question:**

| Adjacent pair | The single question that separates them | Course example |
|---|---|---|
| Synchronous → asynchronous | Does the sender *depend on the reply* to complete its work — not: does control return early? | Module A's background-process HTTP call still depends on B's response — pseudo-asynchronous; C's queue publish does not — truly asynchronous (Tutorial 8 Q1, W11.7) |
| Asynchronous request-reply → event | Does the sender expect a *specific* receiver to act and answer — or is it announcing a completed fact to whoever cares? | Research → Archive query carrying a request identifier (Quiz 4 Q7) vs publishing `EquipmentReserved` (Quiz 4 Q1) |
| Event → other message | Is the payload a fact (event) or a request/instruction for a receiver (command, document)? | `EquipmentReserved` (event) vs `ReserveEquipment` (command) — Quiz 4 Q1; W11.2 |

Pub-sub is not a fourth style in this line — it is the *delivery mechanics* (W11.3) on which both events and pub-sub request-reply ride.

</box>

**Fire-and-forget is the default posture of event-driven microservices — but request-reply survives, asynchronously.** When Research asks Archive to find a dataset that may take hours, the asynchronous query carries a request identifier so the reply can be matched — Week 11's return address and correlation identifier doing Week 10's asynchronous work (Quiz 4 Q7). → [Week 9 — Event-Driven Architecture]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#core-concepts), [Week 10 — Asynchronous Communication]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#core-concepts), [Week 11 — Messaging]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#core-concepts).

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** For each interaction, name the communication style: (a) Checkout requests a final quote from Pricing and waits; (b) Checkout tells Notification to send a receipt and expects no reply; (c) Checkout asks Dispatch to arrange a collection and continues; Dispatch replies later with details.
<panel type="seamless" minimized header="%%Answer%%">
(a) synchronous request/response; (b) one-way notification (fire-and-forget); (c) asynchronous request/response (Quiz 3 Q10).
</panel>

</panel>

<span id="W13-c4"></span>

### W13.4 Through-line 3 — scaling: the scale cube ★

**The third through-line asks what happens when any of the above works — and load arrives.** The recap deck's scalability lens is exactly Week 12: the scale cube, scaling databases, scale out, multi-tier scaling (L13 slide 8).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-12.md#def-scalability" trim />
</box>

**The cube's three axes recapitulate the whole course:** X — run multiple copies behind a load balancer (needs the stateless design of Weeks 6 and 12); Y — functional decomposition, the monolith → modular monolith → microservices move of Weeks 4 and 7; Z — run the same code on a subset of the data, the partitioning of Week 12's data tier. → [Week 12 — Scalability]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#core-concepts).

**Scalability decisions are architectural decisions made early** — scaling post-hoc costs downtime, hardware and rewrites (Week 12) — and they respect the atomicity and ownership boundaries established by the domain partition (Quiz 3 Q2: no scaling requirement, no demonstrated atomicity story, no split).

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** The room-booking platform's search consumes 80% of resources. Which cube moves does Quiz 3's correct answer combine, and why is pure X inferior?
<panel type="seamless" minimized header="%%Answer%%">
Y then X: extract search as an independent microservice (functional decomposition), then increase *its* instances based on demand (horizontal scaling of just the hot service). Pure X — replicating the whole monolith behind a load balancer — wastes replicas on the 5% modules and scales the bottleneck only indirectly (Quiz 3 Q1; L12 slide 24).
</panel>

</panel>

<span id="W13-c5"></span>

### W13.5 The whole course in one picture ★

**One system, evolved four times, touches every week of the course.** The diagram below evolves the room-booking platform — the running example of Quiz 3 — from a single-server monolith to an event-driven microservice system, annotating each stage with the course concept that justifies it and the communication style that era uses.

<mermaid>
flowchart LR
  subgraph s1["1 · Monolith (W4)"]
    m["Search · Reservation · Notification<br>one deployment, one server"]
  end
  subgraph s2["2 · Modular monolith (W4)"]
    mm["Search · Reservation · Notification<br>domain modules, one deployment<br>(search: separate index)"]
  end
  subgraph s3["3 · Microservices (W7, W12)"]
    ms["Search service<br>N instances on demand"] --- lb["Load balancer<br>+ session store"]
    res["Reservation"] --- ntf["Notification"]
    ms -- "sync call (W6/W10)" --> res
  end
  subgraph s4["4 · Event-driven (W9–W11)"]
    r2["Reservation"] -- "ReservationCreated (event)" --> b(("Broker"))
    b -- pub-sub --> n2["Notification"]
    b -- pub-sub --> a["Analytics"]
  end
  s1 ==>|"decompose: Y (still one deployment)"| s2
  s2 ==>|"distribute + replicate: Y then X"| s3
  s3 ==>|"adopt events + messaging (not a cube axis)"| s4
</mermaid>

%%Notation: each framed stage is one architecture era of the same platform; boxes are components/services, the double circle is the message broker, solid arrows are synchronous calls, and dashed arrows are asynchronous messages/events. The thick arrows show the moves between stages: the first two are scale-cube moves (W12.8 — Y-axis decomposition, then distribution with X-axis replication of the hot service), while the last is a communication-architecture change (Weeks 9–11), not a cube axis.%%

How to read it: stage 1 is the n-tier monolith on one server — fine until summer load arrives (W12.1). Stage 2 partitions by domain but keeps one deployment — the modular monolith, where search already has its own index (Quiz 3 Q1). Stage 3 extracts the 80%-hot module and scales *its* instances behind a load balancer with a session store — Quiz 3's correct answer, built from W12.4–W12.5. Stage 4 completes the arc: reservation publishes events that notification and analytics consume independently, commands still go where action is needed — Weeks 9–11's communication patterns, the same patterns as Quiz 4's EquipmentReserved redesign.

**Retelling the course this way is the exam skill.** Given any scenario — a monolith under load, a modular monolith with a hot module, services that must not block each other — you can name the stage you are in, the axis that moves you forward, and the communication style each stage implies.

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** A teammate proposes jumping the room-booking platform straight from stage 1 to stage 4 "to be modern". Name two things that proposal skips.
<panel type="seamless" minimized header="%%Answer%%">
The domain partitioning that tells you *which* services to extract (stage 2, W4/W7–W8), and the measured scaling need that justifies distribution at all (stage 3, W12) — with no scaling or release requirement, Quiz 3 Q2 says retain the design until the proposal demonstrates how atomicity is preserved.
</panel>

</panel>

<span id="W13-c6"></span>

### W13.6 Exam preparation: the four quizzes and what each examines ★

**The four past quizzes are the highest-yield revision material: each maps to a block of chapters, and each question style reappears.** The exam is closed-book with one A4 cheat sheet (no attachments); formats are MCQ, short answers and drawing — and the deck's answering advice is to keep short answers short and state your assumptions where applicable (L13 slide 10).

<box type="tip" seamless>

**How to use a quiz:** sit it closed-book, 30 minutes, before checking anything. Mark which chapter each question came from; revise that chapter's core-concepts section for the ones you missed; only then re-attempt. The links below point at the papers — the *what each examines* notes tell you where to revise.
</box>

**%%Quiz 1 (PDF kept offline)%% — Weeks 1–5 (mainly 2, 3, 5).** AI in software engineering: pattern detection to find similar vulnerable library usage across components, the risks of AI-assisted development, push/pull factors for AI adoption; deployment mechanisms (a virtual machine for a cross-platform testbed); requirements and quality attributes: measurable NFRs, usage-centric requirements, quality-attribute trade-offs (interoperability vs security; reliability vs efficiency); agile backlog reprioritization from working increments; serverless suitability. Revise: [W2]({{baseUrl}}/se-book-adapted/chapters/week-02-modern-software-engineering.html#core-concepts), [W3]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#core-concepts), [W5]({{baseUrl}}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html#core-concepts), [W1]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#core-concepts).

**%%Quiz 2 (PDF kept offline)%% — Weeks 4–7 and 9–10.** The Grab-like app: synchronous call-and-return vs publishing a BookingRequested event while Matching is down (reliability via middleware persistence). Also: closed vs open layers (bypassing the business layer couples presentation to the data layer), the model–code gap, the modular monolith (Smart Kitchen: separate business domains; module APIs, not shared tables), recognizing MVC and pipe-and-filter diagrams, fixing a pipe-and-filter bottleneck by adding filters to the overloaded queue, REST (statelessness, cacheable responses, load balancer + shared caching, URI standardization trade-offs). Revise: [W4]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#core-concepts), [W6]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#core-concepts), [W7]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#core-concepts), [W9]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#core-concepts), [W10]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#core-concepts).

**%%Quiz 3 (PDF kept offline)%% — Weeks 7–10 and 12.** The room-booking platform: extract search (80% of resources) as an independent microservice and increase its instances based on demand (the scale cube, Y then X); retain the design until an atomicity-breaking split is justified; combining over-fragmented pricing services; DDD (subdomains in the problem space vs bounded contexts in the solution; policies delimit consistent contexts in event storming; a jointly governed shared model for common rules); sagas (a reasonably compensated state; ordering reserve → charge → register → notify); CQRS-breaking API signatures; the sync/async/one-way classification. Revise: [W7]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#core-concepts), [W8]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#core-concepts), [W9]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#core-concepts), [W10]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#core-concepts), [W12]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#core-concepts).

**%%Quiz 4 (PDF kept offline)%% — Weeks 9–11.** The equipment platform: EquipmentReserved is a completed-action event, so the request must be a ReserveEquipment command with the event published only after success; initiating vs derived events; thin events that force consumers to call back create hidden dependencies; temporal decoupling (keep accepting uploads; the broker retains events through outages); choreographed compensation (Payment reacts to ConversionFailed under its own rules); aggregating two facts by booking ID before acting; asynchronous request-reply with a request identifier; per-partition ordering vs cross-partition order; persistence alone does not meet a processing deadline — availability and capacity are still needed. Revise: [W9]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#core-concepts), [W10]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#core-concepts), [W11]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#core-concepts).

<box type="tip" seamless>

**Study guide — slides to focus on per deck (L13 slide 11).** Skim these first when time is short:

| Deck | Slides to focus on |
|---|---|
| L1 Software dev processes | 13, 14, 16–18, 22–24, 26–47, 49 |
| L2 Modern SE | 3–5, 7, 8, 10–12 |
| L3 Requirements | 3–24, 26, 28, 29, 33, 34 |
| L4 Architecture | 4, 6, 8–12, 14–22, 27–28, 30–38, 41 |
| L5 Cloud-native (guest lecture, Dell) | 11–16, 18–20, 30–33, 35, 38–42, 44–46, 49–52, 54–59, 64 |
| L6 Architecture | 4, 6–10, 12–15, 17–26 |
| L6 REST | 4–18 |
| L7 Microservices | 3, 5–14, 17–43 |
| L8 Microservices | 6, 8–15, 17–25, 30–37 |
| L9 EDA | 5–11, 13–17, 20–27, 29–32, 34–43 |
| L10 Async communication | 5–8, 10, 12–18, 20–30, 32–33 |
| L11 Messaging | 5, 6–8, 11–12, 15, 17, 20, 22–27, 29, 31–32, 34–40, 46–58, 60–64 |
| L12 Scalability | 3–24 |

All decks are linked from their week pages under [Schedule]({{baseUrl}}/schedule/index.html).
</box>

<box type="info" seamless>

##### Section summary

* **Four quizzes cover the four blocks**: W1–5 (foundations, requirements, cloud), W4–7+9–10 (styles, REST, the sync/event choice), W7–10+12 (microservices, DDD, sagas, scalability), W9–11 (EDA, async, messaging).
* **Revise by through-line, not by week**: requirements → architecture → communication → scaling, using the core-concepts sections linked above.
* **Practise drawing**: the exam includes diagrams — the evolution diagram of W13.5 and the EIP chains of W11.4 are the two most reusable shapes.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Without opening the papers: which quiz would you attempt to self-test the ReserveEquipment redesign, and which for the scale cube?
<panel type="seamless" minimized header="%%Answer%%">
Quiz 4 for the command/event redesign (Weeks 9–11); Quiz 3 for the scale cube and the extract-and-scale decision (Weeks 7–10, 12).
</panel>

</panel>

<box type="info" seamless>

##### Section summary

* **The course has four through-lines**: requirements & quality attributes → architecture (monolith → modular monolith → microservices) → communication (sync → async, events, messages, EIPs) → scaling (the scale cube) (W13.1–W13.4).
* **One evolution diagram retells the course**: the same platform passes through monolith, modular monolith, scaled microservices, and event-driven stages — each move justified by a requirement (W13.5).
* **The four quizzes are the self-test instrument**, each mapped to its chapters above (W13.6).
</box>

</div>

## Key terms

This is a recap chapter — the terms below are defined once, in their own weeks. The table maps each to its home chapter for revision.

| Term | Recap in one line | Defined in |
|---|---|---|
| Quality attribute | A measurable, trade-off-bearing property like scalability, security, reliability | [Week 3]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#core-concepts) |
| Modular monolith | Domain-partitioned modules inside one deployment | [Week 4]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#core-concepts) |
| Microservice | Independently deployable service modelled around a business domain | [Week 7]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#core-concepts) |
| Bounded context | Explicit model boundary within which business terms have consistent meaning | [Week 8]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#core-concepts) |
| Event-driven architecture | Work triggered by events rather than direct calls | [Week 9]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#core-concepts) |
| Asynchronous communication | Sender proceeds without waiting for the receiver | [Week 10]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#core-concepts) |
| Message construction | Command / document / event payload choice | [Week 11]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#core-concepts) |
| Scalability | Handling growth by adding resources, with stable response times | [Week 12]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#core-concepts) |
| Scale cube | X replicate · Y decompose · Z partition data | [Week 12]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#core-concepts) |

## Connections

| Concept | Lecture deck | Tutorial | Other weeks |
|---|---|---|---|
| Requirements & quality attributes | L13 slides 2, 12 | — | W1–W3; Quiz 1 |
| Architecture styles & partitioning | L13 slide 2 | — | W4–W6; Quizzes 1–2 |
| Microservices, DDD, event storming | L13 slide 3 | — | W7–W8; Quiz 3 |
| EDA, events, fire-and-forget vs sync | L13 slide 4 | — | W9; Quizzes 2–4 |
| Async communication, pub-sub, messaging | L13 slides 5–7 | — | W10–W11; Quizzes 2–4 |
| Scalability lens (cube, DB, multi-tier) | L13 slide 8 | — | W12; Quiz 3 |
| Core skills & practical tips | L13 slides 12–13 | — | All weeks |

## Summary

**Key takeaways:**

* **Architecture serves requirements**: every style, pattern and deployment choice answers a measurable need and pays in trade-offs (W13.1).
* **Code partitioning explains the architecture arc**: technical (layered) → domain (modular monolith) → distributed (microservices, event-driven) (W13.2).
* **Communication decouples in stages**: synchronous calls, then events and messages — with intent (command/document/event) deciding the shape (W13.3).
* **Scaling composes on three axes**: replicate (X), decompose (Y), partition data (Z) — and it is an architectural decision made early (W13.4).
* **One system's evolution retells the course**: monolith → modular monolith → scaled microservices → event-driven (W13.5).
* **The four quizzes map the course into four self-test blocks** — use them closed-book, then revise by through-line (W13.6).

**Key terms:** see the table above — each row links back to the chapter that defines the term.

%%Next: this is the final chapter. Sit the four quizzes under [Past quizzes]({{baseUrl}}/se-book-adapted/index.html#quizzes), revise the through-lines you missed, and give the [Full book]({{baseUrl}}/se-book-adapted/print.html) one continuous read as a last pass.%%

## Further reading

* All lecture decks are linked from their week pages — see the [full-semester timeline]({{baseUrl}}/schedule/index.html).
* SE Toolbox guides — <https://sds-edu.github.io/toolbox> (mentioned in L13 slide 14 as the course's practical companion).
