{% from "schedule/macros-fragment.md" import term, example with context %}
<span id="summary">

**How do applications that differ in platform, language and data format exchange information reliably across a network?** This week tours the Enterprise Integration Patterns (Hohpe & Woolf): how messages are **constructed** (command / document / event), carried on **channels** (point-to-point, pub-sub, request/reply, dead-letter), **routed** (content-based router, filters, splitter, aggregator, scatter-gather), **transformed** (translator, canonical data model), and consumed through **endpoints** — closing with when a request-reply interaction is truly asynchronous.

</span>

<span id="toc">

* [W11.1 Enterprise integration and the message broker]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c1)
* [W11.2 Message construction: command, document, event]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c2)
* [W11.3 Message channels]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c3)
* [W11.4 Message routing]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c4)
* [W11.5 Message transformation]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c5)
* [W11.6 Message endpoints]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c6)
* [W11.7 Asynchronicity in the request-reply pattern]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c7)

</span>

<span id="lecture">

### Lecture

**Messaging exists because distributed applications must communicate across platforms, languages, formats and unreliable networks.** The deck's shorthand: every D.A.D needs M.O.M — {{ term("message-oriented middleware", "software that provides messaging capabilities so applications can exchange messages without knowing each other's location, platform or implementation") }} takes care of seamless, loosely coupled communication (slides 4–5). The lecture's standing example: Modreg exports enrolment data as XML, Canvas works in CSV, and the middleware in between translates (L11 recording, ~[19:00]). Enterprise integration can be point-to-point, hub-and-spoke, or bus-based; only the message-based abstractions avoid the hub's central bottleneck (slide 7). → Chapter unit [W11.1]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c1).

**Enterprise Integration Patterns give the field a vendor-independent vocabulary.** 65 technology-independent patterns in six categories — construction, channels, routing, transformation, endpoints, systems management — that every MOM should support (slides 8–9, 14–15). → [W11.1]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c1).

**A message separates metadata (header, properties) from data (body), and the payload's intent names its kind: command, document or event.** Message = metadata + data; properties exist mostly for selection and filtering (slides 16–18). → [W11.2]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c2).

**Channels are one-directional roads between senders and receivers.** Request/reply therefore needs two channels, plus a return address and a correlation identifier to match replies to requests; special channels handle undeliverable messages (dead letter) and per-type data (data type channel) (slides 19–30). → [W11.3]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c3).

**Pub-sub channels broadcast; request-reply over pub-sub mixes a topic for requests with queues for replies.** Use it when several services work in parallel and their responses must be aggregated afterwards — the lecture's ride-hailing story: a drop-off request published to all nearby drivers, acceptances aggregated on a point-to-point response channel, losers' stale responses expiring into the dead letter channel (L11 recording, ~[72:00]) — and keep the topic-vs-queue difference straight (slides 31–32). → [W11.3]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c3).

**Routers encapsulate routing logic so senders need not know recipients.** Content-based routers route on message content, message filters drop non-matching messages with a single output, and context-based routers route on context (load balancing, failover) rather than content (slides 33–40). → [W11.4]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c4).

**The order-processing example composes the patterns into a pipes-and-filters flow: splitter → content-based router → inventories → aggregator → validated/invalid.** Pub-sub is the fork, the aggregator is the join, the content-based router is the condition; scatter-gather broadcasts and reassembles concurrently — the lecture's insurance-agent story (broadcast to insurers, aggregate each package, then aggregate the winners) is the two-aggregator case (L11 recording, ~[100:00]) (slides 46–53). → [W11.4]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c4).

**Transformation reconciles data formats: translators pairwise, or a canonical data model as the common format.** Pairwise translators multiply with every application and format change; producing and consuming a common format removes the explosion (slides 54–58). → [W11.5]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c5).

**Endpoints are the application-facing side of messaging: channel-specific, single-direction, and consuming either by polling or by reacting to arrival.** Polling consumer vs event-driven consumer, with throttling to control the consumption rate (slides 59–63). → [W11.6]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c6).

**The deck closes by recapping Week 10's open question: asynchronicity in the request-reply pattern.** Returning immediately is not enough — a caller that still depends on the reply to complete its operation is only {{ term("pseudo-asynchronous", "control returns early but the caller still depends on the reply — synchronous in terms of dependency") }} (slides 3, 20–26; Tutorial 8 Q1). → [W11.7]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c7).

<box type="tip" seamless>

**Deck structure at a glance:**

- Slides 4–15: motivation and the EIP landscape
- 16–18: message construction
- 19–32: channels
- 33–53: routing
- 54–58: transformation
- 59–63: endpoints
- 64: summary

Slides marked *Optional/Not examinable* (JMS message types, SQS lifecycle, RabbitMQ exchanges, SNS filtering) are vendor detail — skim for intuition, don't memorise.
</box>

</span>

<span id="tutorial-summary">

**Tutorial 8 practises judging asynchronicity by dependency and drawing message flows.** Q1 classifies pseudo-asynchronous vs truly asynchronous interactions; Q2 diagrams an order-management microservice system first with a synchronous chain, then with pub-sub events, and asks what each choice does to scalability — applying [W11.2–W11.7]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#core-concepts).

</span>

<span id="tutorial">

### Tutorial 8

Work the tasks in order — reveal each answer only after attempting it. Concepts used: [W11.2]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c2), [W11.3]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c3), [W11.4]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c4), [W11.7]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c7).

<panel type="seamless" header="## %%[Task 1]%% **Is it synchronous or asynchronous?**">

**Given (Tutorial 8 Q1):**

* *Module A* calls Module B via an HTTP API using a background process and immediately returns control to its own caller, though it will eventually depend on B's HTTP response to complete the overall operation. Module B might internally delegate the task to a worker thread and wait for a worker to finish before replying.
* *Module C* publishes a message to a queue consumed by Module D and immediately returns; the result is observed later via a separate notification.

**Based on observable behaviour from the caller's point of view, is each interaction synchronous or asynchronous — and is that classification truly accurate in both cases?** Draw a diagram of each interaction to justify your answer.

<panel type="seamless" minimized header="%%Answer (teaching team suggestions)%%">

**Module A → B is only pseudo-asynchronous.** At first glance it looks asynchronous because A immediately returns control to its caller. But A eventually depends on B's HTTP response to complete the overall operation — the system behaves *synchronously in terms of dependency*.

**Module C → D is truly asynchronous.** C publishes a message and does not depend on an immediate response from D; producer and consumer operate independently, and the result is observed later via a separate notification.

<mermaid>
sequenceDiagram
  participant A as Module A
  participant B as Module B
  A->>B: HTTP request (background process)
  Note over A: has returned to its caller...
  B-->>A: response — still needed<br/>to complete the operation
  participant C as Module C
  participant q as queue
  participant D as Module D
  C--)q: publish message
  Note over C: returns, operates independently of D
  q--)D: deliver
  Note over D: result observed later<br/>via separate notification
</mermaid>

%%Notation: solid arrows are synchronous calls, arrows with open heads are asynchronous messages; the notes show where each module's own work continues.%% A's timeline still hangs on B's reply; C's does not.

</panel>
</panel>

<panel type="seamless" minimized header="## %%[Task 2]%% **Microservices communication for an order-management application**">

**Given (Tutorial 8 Q2).** Illustrate, with high-level diagrams, the communication in two scenarios of an order-management application built from microservices (Customer, Product, Inventory, Order, Payment, Shipment, Notification). Annotate each interaction with its message style (e.g. *Request/Reply via HTTP*, *Pub-Sub via broker*); make reasonable assumptions where information is missing.

**Scenario 1.** The Order microservice acts as the controller for the end-to-end process flow, invoking the other services **synchronously in sequence**: Read customer info → read product details → read inventory → create order → create payment → create shipment → update inventory → create notification.

**Scenario 2.** Whenever the Customer microservice changes state (a customer record is created or updated), it publishes an event. Four services subscribe, each needing a different part of the new information — and all of them need it before the next order occurs:

- **Order** — the customer's *name*
- **Payment** — the *credit-card details*
- **Shipment** — the *mailing address*
- **Notification** — the *email address*

**Then:** write down observations about the scalability of Scenario 1. Would asynchronous messaging improve scalability compared to synchronous communication? How?

<panel type="seamless" minimized header="%%Answer — Scenario 1 diagram and observations%%">

<mermaid>
flowchart LR
  O["Order<br>(controller)"] -->|read customer info| C["Customer"]
  O -->|read product details| P["Product"]
  O -->|read inventory| I["Inventory"]
  O -->|create payment| Pay["Payment"]
  O -->|create shipment| S["Shipment"]
  O -->|update inventory| I
  O -->|create notification| N["Notification"]
</mermaid>

%%Notation: boxes are microservices and each solid arrow is one synchronous request/reply call in the sequence.%% Read the chain as a single blocking thread of calls: Order cannot take its next step until the previous service answers.

**Observations:** the current design is not horizontally scalable — every request occupies the whole chain, and the chain is only as fast and as available as its slowest, least available service. Synchronous interaction gives easier ordering, rollback/failure handling and atomicity, and tighter control coupling, but it is less robust (if a service goes down, the chain fails) and resources sit idle while waiting.

</panel>

<panel type="seamless" minimized header="%%Answer — Scenario 2 diagram%%">

<mermaid>
flowchart LR
  C["Customer"] -.->|"CustomerCreated / CustomerUpdated (event)"| b(("Broker"))
  b -.->|"pub-sub"| O["Order<br>needs name"]
  b -.->|"pub-sub"| Pay["Payment<br>needs card details"]
  b -.->|"pub-sub"| S["Shipment<br>needs mailing address"]
  b -.->|"pub-sub"| N["Notification<br>needs email"]
</mermaid>

%%Notation: the double circle is the broker, the dashed-topic fan-out is pub-sub delivery, and each labelled arrow states what the subscriber needs from the event.%% One publication reaches all four subscribers — the Customer service does not know who they are.

</panel>

<panel type="seamless" minimized header="%%Answer — Would asynchronous messaging improve scalability?%%">

**Yes — on five counts from the teaching team's suggestions:**

* **Decoupling components:** async components operate independently and can each scale based on its own demand and capacity; sync components are tightly coupled, requiring immediate responses, which creates bottlenecks.
* **Enhanced fault tolerance:** if a component is unavailable, messages can be queued and processed later; in sync designs unavailability causes immediate failures or degraded performance.
* **Scalable processing:** multiple consumers/workers can process queued messages or partitions in parallel, enabling horizontal scaling; sync processing is limited by the number of available threads or connections.
* **Improved resource utilization:** resources are not held up waiting for responses; in sync designs resources idle while waiting.
* **Better load management:** queues buffer requests during peak loads, absorbing bursts of traffic without overwhelming components such as the database; sudden spikes in sync designs cause latency or failures.

</panel>
</panel>

**Materials:**

* %%Tutorial sheet (PDF kept offline)%%
* %%Model solution (PDF kept offline)%%

</span>
