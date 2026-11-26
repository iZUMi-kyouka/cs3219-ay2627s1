{% from "schedule/macros-fragment.md" import term with context %}
<span id="summary">

**How exactly should asynchronous components talk — and what does each choice promise?** The lecture finishes the sync/async contrast (including asynchronicity *inside* request–reply), separates events from messages by sender intent, contrasts single-receiver queues with pub/sub topics (Kafka, AMQP/RabbitMQ), and maps persistent vs transient communication — the three axes of component communication.

</span>

<span id="toc">

* [W10.1 Synchronous vs asynchronous communication]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#W10-c1)
* [W10.2 Events vs messages: intent matters]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#W10-c2)
* [W10.3 Single vs multiple receivers]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#W10-c3)
* [W10.4 Persistent vs transient communication]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#W10-c4)

</span>

<span id="lecture">

### Lecture

**Synchronous means request–reply: the caller sends and waits, tightly coupled, with connection overhead and failure handling on the sender.** Asynchronous means a lag between sending and receiving/interpreting/responding — sender and receiver function independently, one-to-many becomes possible, coupling is loose, and the cost is notification handling. HTTP/HTTPS is the sync exemplar; AMQP the async one. Slides 4–6 → [W10.1]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#W10-c1)

**A slow backend need not hold the caller hostage: the async request–reply pattern returns HTTP 202 (Accepted) with a link to a status endpoint.** The client polls the status endpoint (202 while pending), gets a 302 redirect to the resource when the background worker finishes, and invalid requests are rejected at once with 4xx. Slides 7–8 → [W10.1]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#W10-c1)

**Is an event the same as a message? Is a topic the same as a queue? No — intent makes the difference.** Both constructs are asynchronous, decouple services, and carry information; but an *event* is a fact — a past-tense state change broadcast over a **topic** ({{ term("topic", "a broker channel enabling one-to-many communication: every subscriber receives the message — defined in W10.3") }}, Kafka, pub–sub) — while a *message* carries a *request to be executed* (command or query) point-to-point over a **queue** ({{ term("queue", "a broker channel that buffers messages for a single receiver, first-in-first-out — defined in W10.3") }}, AWS SQS). Slides 9–13 → [W10.2]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#W10-c2)

**Ownership flips with the construct: the publisher owns the event and its topic; the receiver owns the message and its queue.** The e-commerce walkthrough assigns every flow: `OrderPlaced` → event, `ProcessPayment` → message, `PaymentConfirmed` → event, `AssignCourier` → message, `OrderDelivered` — events handle the reactive flow, messages handle reliable task handoff. The tenant-deletion scenario then shows the same requirement wired with messages-to-each-service or an event-broadcast-plus-final-message. Slides 14–18 → [W10.2]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#W10-c2)

**Single receiver = point-to-point (exactly one consumer, processed once, not copied); multiple receivers = pub/sub broadcast.** A message queue is a buffer with unicast semantics; a topic is a broadcasting station anyone can subscribe to — and both sync & async can coexist in one architecture. Slides 19–21, 24 → [W10.3]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#W10-c3)

**Kafka realizes pub/sub as a distributed, horizontally scalable log of topics and partitions** — all events with a given key land on the same partition (Quiz 4 Q9's ordering fix; Quiz 4 Q8 explains why cross-partition reordering is no violation). **AMQP realizes the queue world**: publishers → exchanges → queues → consumers, with bindings and routing keys — and RabbitMQ's direct, fanout, topic, and header exchange types. Slides 10, 22–29 → [W10.3]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#W10-c3)

**Persistence is the third axis: store-and-forward keeps messages at each hop until delivered (email); transient buffers discard when the next host is down (TCP/IP routing).** The 2×2 with synchronicity has a distinct guarantee per cell — persistent-async (eventual delivery), persistent-sync (block until receipt-ack), transient-async (discard if receiver down), transient-sync (receipt-, delivery-, or response-based blocking — traditional RPC) — with email, chat, UDP, and RPC as the corner examples. Message queue systems are persistent-async, guaranteeing eventual insertion into the recipient's queue — but not when, or if, it is processed. Slides 30–34 → [W10.4]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#W10-c4)

</span>

<span id="tutorial-summary">

**Tutorial 7 assembles Weeks 8–10 on the FoC platform:** monolith vs microservices for the errand create→accept workflow plus saga compensation (Q1), a CQRS order flow across validation, tax, and email services (Q2), and choreographed vs orchestrated A→B→C workflows over event streams (Q3).

</span>

<span id="tutorial">

### Tutorial 7

**What it practises:** comparing monolithic and microservice designs of one business workflow with saga-style compensation (applying W8.2), drawing a CQRS write/read split (applying W8.3), and choreography vs orchestration with event streams (applying W8.4 + W10.3).

**Q1 — Errand workflow, monolith vs microservices, then sagas.** How does the workflow from *creating* an errand request to *accepting* it in FoC differ between a monolithic and a microservices-based approach — components, interactions, consistency? Then: how would the **Saga pattern** apply, which **compensating actions** restore a consistent state, and give a specific failure with its compensation.
<panel type="seamless" minimized header="%%Answer%%">**Monolith:** one app, one shared database — create = validate requestor/supplier/location, create order, reserve credits; accept = verify eligibility, check errand open, assign courier; consistency via atomic database transactions. **Microservices:** User service verifies requester and courier, Supplier service validates locations, Order service creates/validates/assigns, Credit service checks and reserves credits; services communicate synchronously (API calls) and asynchronously (messages/events); consistency is coordinated across services — temporary inconsistency allowed, eventual consistency required. **Saga:** Order (errand `PENDING`) → Credit (`RESERVE` credits) → Order (mark `OPEN`); if the last step fails, compensate: Credit `RELEASE`s reserved credits, Order marks the errand `CANCELLED`. Full table of action/compensation pairs in the solution PDF.</panel>

**Q2 — CQRS in an order flow.** Illustrate the service communication and use of CQRS: an order is accepted in the *order service*, picked up by the *validation service* and validated; sales tax is added by the *Tax service*; information for an email is made available to the *Email service*; the updated order goes back to the orders service, where it can be queried via the **orders view** (hint: CQRS); after a confirmation email, the user clicks through to the order.
<panel type="seamless" minimized header="%%Answer sketch%%">Write path: order service records the accepted order (command side); validation, tax, and email services pick it up and enrich it in sequence. Read path: the orders *view* is a read model derived from the order events — queries hit the view, never the write model directly; the confirmation email links the user to that view. The model solution's diagram shows this split; compare with the [W8.3](../../se-book-adapted/chapters/week-08-microservices-ii.html#W8-c3) CQRS figure.</panel>

**Q3 — Choreography vs orchestration.**
**(a)** Draw a **choreographed** workflow where services A, B, C interact with a dependent workflow A → B → C, each fed by Event Streams 1, 2, 3 respectively.
<panel type="seamless" minimized header="%%Answer%%">Stream 1 → Service A; A publishes → Stream 2 → Service B; B publishes → Stream 3 → Service C. No coordinator: each service reacts to its input stream.</panel>
**(b)** The workflow must become A → C → B (C before B). Redraw — and what changes or is a concern for the event streams and services?
<panel type="seamless" minimized header="%%Answer%%">Rewire the streams: Stream 1 → Service A; A publishes → Stream 3 → Service C; C publishes → Stream 2 → Service B. The concern: the *wiring is the workflow* — changing order means re-plumbing which stream feeds which service (and checking each service's expectations of its input), whereas an orchestrator would change in one place.</panel>
**(c)** Draw an **orchestrated** equivalent, with an Input Stream feeding the Orchestrator and an Output Stream exiting it.
<panel type="seamless" minimized header="%%Answer%%">Input Stream → **Orchestrator**; the orchestrator drives A, then B, then C (collecting their results) and writes to the Output Stream. Compare with the [W8.4](../../se-book-adapted/chapters/week-08-microservices-ii.html#W8-c4) two-panel diagram.</panel>

**Materials:**

* %%Tutorial sheet (PDF kept offline)%%
* %%Model solution (PDF kept offline)%%

</span>
