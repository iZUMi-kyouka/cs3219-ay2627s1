{% from "schedule/macros-fragment.md" import term, example with context %}
<h2>Week 10 — Asynchronous Communication</h2>

<span>

Builds on **Week 9** — events, fire-and-forget communication, EDA, and event-driven microservices ([W9.1]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c1)–[W9.4]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c4)) — and on the interprocess communication styles of [W8.4]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c4). Tutorial 7 exercises sagas ([W8.2]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c2)), CQRS ([W8.3]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c3)), and choreography/orchestration ([W8.4]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c4)) across these weeks.
</span>

<span>

* **Can** contrast synchronous and asynchronous communication and design asynchronicity inside a request–reply API.
* **Can** decide between an event and a message from the sender's intent, and state the channel and ownership consequences.
* **Can** choose point-to-point vs publish–subscribe communication and describe how brokers (Kafka, AMQP/RabbitMQ) realize each.
* **Can** classify communication as persistent or transient, combine it with (a)synchronicity, and reason about the guarantees each combination gives.
</span>

<div>

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

**This week takes the asynchronous world of Week 9 and asks three sharper questions about it.** Event or message — what is the sender's *intent* (slides 9–18)? One receiver or many — point-to-point queue or broadcast topic (slides 19–29)? Persistent or transient — does the communication survive a receiver that is down (slides 31–34)? It also finishes the synchronous/asynchronous contrast the last two weeks started (slides 4–8). Source for the whole chapter unless stated otherwise: L10 slides.

## Core concepts

<span id="W10-c1"></span>

<panel type="seamless" minimized header="**W10.1 Synchronous vs asynchronous communication ★**">


**Every inter-service call is a bet on the other side being up — sync or async decides who waits, and who handles the failure.** This unit pins down the two styles the last two weeks have been using informally.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-10.md#def-synchronous-communication" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-10.md#def-asynchronous-communication" trim />
</box>

| | Synchronous (request–reply) | Asynchronous |
|---|---|---|
| Who waits | Sender waits for the response | Sender skips the wait and continues executing |
| Coupling | Tightly coupled | Loosely coupled |
| Overhead | Connection overhead | Need notification; sender must map each incoming notification back to the request that caused it (correlation — see Quiz 4 Q7) %%— not the DDD "context mapping" of Weeks 7–8%% |
| Failure handling | Sender learns of failure immediately and has to handle it | Failures surface later, in different places, per consumer — error handling is more complex and fragmented (W9.2; L9 slide 16) |
| Reach | One receiver at a time | Enables one-to-many sends |
| Protocol examples | HTTP/HTTPS | AMQP |

%%The mapping burden has a classroom face (L10 recording, ~[24:00]): if you ask ten questions during a lecture and I answer them in whatever order they surface, answering is my whole job — recognizing which answer belongs to which of your questions is yours. A correlation identifier is exactly that bookkeeping, done on the sender's side.%%

<panel type="seamless" minimized header="%%What is loose coupling?%%">

<include src="../../se-book-adapted/common/defs-week-07.md#def-loose-coupling" trim />

</panel>

{% call example("L10 slide 5 — the login call") %}
A login action is synchronous by nature: the caller must get a reply — "authenticated" or "rejected" — before it can proceed. Contrast the fire-and-forget world of Week 9, where the Order service publishes `DeliveryConfirmed` and moves on without waiting for the Notification service.
{% endcall %}

**HTTP/HTTPS is the canonical synchronous request–reply protocol.** A client, typically a web browser, sends a request for a resource to a server, and the server sends back a response corresponding to the resource — or an error message if it cannot process the request. The resource can be a simple HTML file returned verbatim, or a program generating the response dynamically (slide 6).

**Synchronous communication carries connection overhead — the channel must be kept alive for the whole conversation.** The classic picture is a telephone call: both parties are online start to finish, and even when a provider (an ISP) does the maintaining, the overhead is real (L10 recording, ~[21:00]).

**Between services, WebSockets are the canonical keep-alive channel.** The protocol terminates a socket that stays silent too long, so the two sides exchange heartbeat messages — "I am alive" / "I am also alive" — for as long as the channel is needed (L10 recording, ~[22:00]).

**Failure handling in synchronous communication is the sender's job.** The receiver does not even know it was supposed to receive something, so a sender that gets no response retries the request — up to a configured limit, or with the exponential-backoff schedule TCP/IP uses (L10 recording, ~[23:00]).

#### Asynchronicity inside request–reply

%%Telling apart — fire-and-forget vs asynchronous request–reply. One distinguishing question: **does the sender eventually get a response?** Fire-and-forget (W9.2): no — the sender publishes and never expects an answer, so there is nothing to correlate (`DeliveryConfirmed` → the Order service moves on forever). Asynchronous request–reply (this unit): yes — the response comes *later*, so the design must carry a status endpoint to ask "done yet?" and a request identifier to match replies to requests (Quiz 4 Q7). Both are asynchronous — the sender never blocks — they differ only in whether a reply exists to wait for.%%

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-10.md#def-async-request-reply" trim />
</box>

**A slow backend does not force the caller to wait — the async request–reply pattern decouples backend processing from the requester while the requester still gets a clear response.** The trick is to reply *immediately* with a promise instead of a result (slides 7–8, from the Microsoft Azure async-request-reply pattern). The sequence below traces one request through that pattern, from submission to the final redirect.

<mermaid>
sequenceDiagram
    participant C as Client
    participant A as Async API endpoint
    participant Q as Queue
    participant W as Background worker
    participant S as Status endpoint
    C->>A: Submit long-running request
    A--)Q: Put work on queue (async)
    A-->>C: HTTP 202 Accepted<br/>+ status-endpoint link
    Q--)W: Deliver queued work (async)
    W->>S: Write result / status
    C->>S: Poll: HTTP GET status
    S-->>C: 202 (still pending, with ETA)
    C->>S: Poll again
    S-->>C: 302 Found — redirect<br/>to resource
    C->>S: Fetch resource at the link
</mermaid>

%%Notation: `->>` is a synchronous HTTP call and `-->>` its HTTP reply — the dashed reply from the API endpoint is the immediate 202 acknowledgment; `--)` marks the asynchronous hops, drawn without reply because nobody waits on them: the endpoint drops the work on the queue and moves on, and the queue later hands the work to the background worker.%%

How to read it: the client sends a request and gets **HTTP 202 (Accepted)** plus a link to a status endpoint; while work is pending, polling the status endpoint also returns 202; when the work completes, the status endpoint returns **302 (Found)** redirecting to the resource, which the client then fetches. If the request was invalid in the first place, the API replies immediately with an error code such as **HTTP 400 (Bad Request)** (slides 7–8).

<panel type="seamless" minimized header=":glyphicon-question-sign: **Common question — isn't a WebSocket asynchronous, then?**">

The channel itself is synchronous: the connection must be kept alive with heartbeats for as long as you want to use it. You can run a synchronous call over a WebSocket, or place an event bus on it so events are picked up as they arrive — either way the underlying socket needs its lifeline maintained (asked in lecture; L10 recording, ~[26:00]). %%Grounding: RFC 6455 gives WebSocket ping/pong control frames, and servers and proxies reap idle sockets — heartbeats keep the channel alive.%%

</panel>

{% call example("L10 recording ~[28:00] — Canvas bulk download") %}
Downloading all team submissions at semester's end: each deck is 2–20 MB and the files sit in S3 buckets behind Canvas, which must fetch them, zip them, and stage the result — minutes of work. Choosing "download all" returns immediately with a "files are downloading" notice, and the lecturer goes on grading other things while Canvas works in the background. Note what the pattern does *not* do: HTTPS itself stays synchronous — "HTTP cannot be made asynchronous". What changes is that client and backend are decoupled for the processing duration, with the client satisfied by an acknowledgment that the request is being processed (L10 recording, ~[30:00]).
{% endcall %}

{% call example("Quiz 4 Q7 — an async query must be correlatable") %}
The Research service asks the Archive service to locate an old dataset; the search may take hours, and Research must continue other work and later associate each reply with the correct search. Sending the locate-dataset request asynchronously is right — but treating "the next reply" as the result of the latest search is wrong when several searches can be in flight. The fitting design: send an asynchronous query to Archive **and include a request identifier** that Archive returns with its reply. (Source: Quiz 4, Question 7.)
{% endcall %}

<box type="warning" seamless>

**Pitfall — async by default is not free.** The pattern adds a status endpoint, polling traffic, and correlation identifiers to design for. Choose synchronous when the caller genuinely needs the answer to proceed (login, slide 5); go asynchronous when it can continue — and then design the notification handling the definition demands: a way to map each incoming notification back to the request it answers, via a {{ term("correlation identifier", "a token the requestor assigns as a unique request ID and the replier copies into the reply, so replies can be matched to requests — defined in W11.3") }} (Quiz 4 Q7's request identifier) (slide 5).

**Pitfall — poll periodically, not frantically.** Polling the status endpoint every second while doing nothing else is *busy waiting* — the operating-system term for cycling without useful work — and wastes the client's resources. The pattern intends the client to continue its own work and check back periodically (L10 recording, ~[32:00]).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Tutorial 7 Q1: in the FoC errand workflow, what replaces the monolith's atomic database transaction when create-and-reserve spans the Order and Credit services?
<panel type="seamless" minimized header="%%Answer%%">Coordination across services: the Order service works with the Credit service (synchronously for the reservation, or via messages/events), temporary inconsistency is allowed, and the system must reach a consistent state eventually — with a saga compensating if a step fails (Tutorial 7 Q1; W8.2).</panel>

**Q2.** Why does the async request–reply pattern return 202 rather than 200?
<panel type="seamless" minimized header="%%Answer%%">202 (Accepted) says *the request was accepted for processing but is not complete* — an honest answer while the background worker works; 200 would promise a result that does not exist yet (slide 7).</panel>

**Q3.** Which two pieces must accompany a long-lived asynchronous query so replies can be matched to requests?
<panel type="seamless" minimized header="%%Answer%%">A status endpoint (where to ask "is it done?") and a request identifier returned with the reply (which search does this answer?) — Quiz 4 Q7.</panel>

</panel>

</panel>
<span id="W10-c2"></span>

<panel type="seamless" minimized header="**W10.2 Events vs messages: intent matters ★**">


**Same broker, same wire, same asynchronous mechanics — what makes an event an event is the *intent* with which it is sent.** Getting this classification right decides receivers, channels, and who owns what.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-10.md#def-message" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-event" trim />
</box>

**The two constructs share three properties and differ in one.** Both utilize asynchronous communication, facilitate decoupling of services, and carry some information from one service to the other for the second to consume — *the intent with which a message or event is sent makes the difference* (slide 12). Typical realizations: Kafka as the event broker, RabbitMQ and AWS SQS as messaging systems — and Redis, or RabbitMQ itself, can be configured to play either role (L10 recording, ~[40:00]).

| | Event | Message |
|---|---|---|
| What it carries | A **fact** — a state change; something that happened in the past | A **request to be executed** — a command (perform an action) or a query (get data) |
| Delivery | **Broadcast** to other services (pub–sub — publish–subscribe: one sender, many subscribers; treated fully in W10.3) | **Point-to-point** between two services |
| Broker construct | **Topic** (e.g., Kafka, an event broker) | **Queue** (e.g., AWS SQS — Amazon's Simple Queue Service, a message broker) |
| Who receives | Both/All subscribed services receive the same event | The only service the message is addressed to |

(Source: L10 slide 13.)

**On an architecture diagram, the verb tense is the tell.** Events are stated in the past tense — `OrderPlaced`, `PaymentRejected`, `OrderShipped` — because they report what already happened (L10 recording, ~[37:00]).

**Messages read as instructions, and the distinction carries into code.** Message names are commands — `NotifyCustomer`, `ShipOrder`, `ApplyPayment` — and when you translate the architecture into code, an event travels as a payload the consumer reacts to, while a command typically becomes a call to the service that performs it (L10 recording, ~[38:00]).

**Ownership follows the channel — and it flips between the two.** For events, the **publisher owns the event payload and the underlying channel (topic)** on which events get published — e.g., a Content service owns the topic on which new content is published and the payload of that event. For messages, the **receiver owns the message payload and the underlying channel (queue)** — e.g., a Payment service decides on which queue payment messages must be sent, and what details are needed for payments to be initiated (slide 15).

{% call example("L10 recording ~[55:00] — the receiver dictates what it accepts, and where") %}
A Payment service is configured to receive Singapore-dollar payments from Singapore-issued cards. A tourist offers a USD Amex. Taken to its strictest, the receiver refuses: "I accept SGD only — converting is your problem." And if the payment system had several gateways — SGD-only, global, Amex-only — the receiver dictates *which channel* each kind of payment message must be sent to. That is message ownership in action: the receiver owns the payload because it works on it, and owns the channel because it dictates where the work arrives. (In practice, other mechanisms handle the conversion — the point is the receiver's right to dictate.)
{% endcall %}

The diagram puts the two side by side — the exact contrast the deck draws on slide 13.

<mermaid>
flowchart TB
    subgraph TOPIC["Event — broadcast via topic"]
        S1["Service 1"] -.->|"publishes event"| T[("Topic")]
        T -.->|"same event"| R1["Service 2"]
        T -.->|"same event"| R2["Service 3"]
    end
    subgraph QUEUE["Message — point-to-point via queue"]
        S2["Service 1"] -.->|"sends message"| Q[("Queue")]
        Q -.->|"the only receiver"| R3["Service 2"]
    end
</mermaid>

%%Notation: a rectangle is a service and a cylinder is the broker channel (topic above, queue below); dashed arrows are asynchronous deliveries; note the fan-out on the topic versus the single addressed delivery on the queue.%%

How to read it: Service 1 broadcasts one fact and both subscribing services receive the same event; in the lower half, Service 1 hands a *task* to exactly one receiver — there is no "everyone who cares", because the sender named its target (L10 slide 13).

{% call example("L10 slide 16 — e-commerce: which construct, and why") %}
Services: Order, Inventory, Payment, Notification, Analytics, Shipping — plus the Loyalty Points service that the deck's last step names without listing here.

* Customer places an order → `OrderPlaced`: a **fact** → topic → **event** (Inventory, Analytics, Shipping, Notification react independently).
* Order service triggers payment → `ProcessPayment`: a **command** → queue → **message** (only Payment should handle it; broadcasting would be incorrect).
* Payment succeeds → `PaymentConfirmed`: a **fact** → topic → **event** (Order, Shipping, and Notification all independently want to know).
* Shipping assigns a courier → `AssignCourier`: a **command** → queue → **message** (directed to one specific courier-assignment service).
* Package delivered → `OrderDelivered`: a **fact** → topic → **event** (Analytics, Loyalty Points, Notification react independently).

Events handle the *reactive* flow; messages handle *reliable task handoff*.
{% endcall %}

**The same business requirement can be wired either way — deliberately.** The deck's tenant-deletion scenario: a tenant manager service must ensure all domain services delete (or anonymize) tenant-specific data, and the Notification service must send a confirmation email (slides 17–18).

* **Messages all the way:** the tenant manager sends messages to each individual domain service to take action; once all confirm, it sends a message to the notification service.
* **Event first, message last:** the tenant manager fires a `TenantDeleted` event; all domain services react and report deletion status; once the manager has all confirmations, it sends a *message* to the notification service to notify the user.

Note the shape of both answers: the *fan-out* is intent (event vs messages), and the *email to the user* is a directed task handed to one service — a message either way.

The recording works through the trade-offs the slides only imply (L10 recording, ~[60:00]–[68:00]):

* **Event-only can mis-order the flow.** Consumers process at different speeds, so the Notification service may react to `TenantDeleted` and email the user *before* the slower domain services have finished deleting the tenant's data — the business requirement's *sequence* is not enforced, only its eventual outcome.
* **Messages-all-the-way enforces the sequence, at a price.** Individual commands to every service, each responding on a shared return channel, let the tenant manager wait for all confirmations before directing Notification — but that is many API-style requests where one cheap event publication would do.
* **The hybrid buys both.** The event drives the fan-out, a message channel collects the confirmations to enforce sequencing, and the final directed message goes to Notification.
* **The W8.4 vocabulary names the difference.** Firing an event and letting each service decide what to do is **choreography**; issuing explicit commands that dictate *when* each service acts is **orchestration** — "sending commands is kind of a telltale sign that it is an orchestration" (L10 recording, ~[68:00]).

<box type="warning" seamless>

**Pitfall — mislabeling intent corrupts the design.** Broadcast a command and you get races ("let whichever receives it first become the reservation authority" — the wrong answer to Quiz 4 Q1); masquerade a command as a past-tense event and consumers react to something that never happened. And per slide 14's warning, the *constructs* can be used either way — "message going to a topic & event going to a queue" is possible, which is exactly why you must reason from intent, not from the channel name.
</box>

<box type="info" seamless>

**Two senses of "message" — which one is in play?** In this unit's technical vocabulary, a **message** is the command/query construct: a *request to be executed*, sent point-to-point to one receiver over a queue, owned by the receiver — an event is the *other* construct (a past-tense fact, broadcast on a topic, owned by the publisher). In broader industry usage, "message" means any payload sent between services — events included. The deck flags this itself (slide 14: "the terms can be used either way, when referring to one specific thing => confusing"). So: within W10 arguments (ownership, channels, intent), use the narrow sense; when reading Kafka documentation or W9's prose, expect the broad sense, and classify the payload by *intent*, not by the word. The recording adds a decoding rule for casual reading (L10 recording, ~[53:00]): the channel names out the construct — "a message sent to a topic" means an *event* on a pub-sub topic, and "an event sent to the queue" means a *message* on a queue; topic ⇒ pub-sub ⇒ events, queue ⇒ messages.

</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** In the equipment-platform redesign (Quiz 4 Q1), why must `EquipmentReserved` be published only *after* the reservation succeeds?
<panel type="seamless" minimized header="%%Answer%%">Because the event is a fact — a state change that already happened. Publishing it before the action would announce a fiction; the *request* belongs in a `ReserveEquipment` command to the Reservation service (Quiz 4 Q1; L10 slide 13).</panel>

**Q2.** A new analytics service wants order data. With an `OrderPlaced` event, what changes? With per-service messages, what changes?
<panel type="seamless" minimized header="%%Answer%%">With the event: one new subscription — the publisher (Order service) owns the topic and need not change. With messages: the sender must now know about and message one more receiver — coupling the sender to every interested party (L10 slide 15's ownership rule).</panel>

**Q3.** Who owns the queue in the payment example, and what does that ownership include?
<panel type="seamless" minimized header="%%Answer%%">The Payment service (the receiver): it decides on which queue payment requests must be sent and what details they must carry (L10 slide 15).</panel>

</panel>

</panel>
<span id="W10-c3"></span>

<panel type="seamless" minimized header="**W10.3 Single vs multiple receivers ★**">


**How many services must react decides the channel — and the channel decides ordering, scaling, and delivery guarantees.** Point-to-point and pub/sub are the two receiver topologies (slide 20).

**Single receiver means point-to-point: exactly one consumer, and the message is processed just once.** A message queue is like a buffer: you put messages in and retrieve messages from it; any given message is consumed by one receiver (unicasting), and messages are not copied to other receivers (slides 20, 24).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-10.md#def-queue" trim />
</box>

**Multiple receivers mean pub/sub: one sender's communication is available to many subscribers.** A message can also be published to a topic — a broadcasting station: anyone interested can subscribe, and send–receive operations are controlled by configuration — who subscribes to a topic is set up as configuration on the broker rather than named in the sender's code (the deck's phrase, slide 21). Publishers are aka producers, senders, or observables; subscribers are aka consumers, receivers, or observers (slides 20–21) — the last pair borrows the Observer design pattern's names (a subject notifies its observers), so "observable" is just the thing being watched — the event source — and the "observer" is what gets notified. The recording adds the boundary difference: in the Observer pattern everything happens inside one process, whereas pub/sub decouples the same roles across the network (L10 recording, ~[73:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-10.md#def-topic" trim />
</box>

<box type="important" seamless>

**You can — and will — have both.** Sync and async communication coexist in one architecture/application, and so do queues and topics: commands flow point-to-point while facts fan out (slide 20; L10 slide 16's e-commerce table).

</box>

**Two mechanisms reach many receivers — broadcast and multicast.** Pub/sub *broadcast* pushes one event to the broker, which notifies every subscriber. *Multicast* keeps the message construct: the sender explicitly copies the message to each designated receiver, and uninterested services are never bothered — RabbitMQ's fanout exchange is exactly this copying behavior (L10 recording, ~[70:00]).

**Kafka realizes pub/sub as a distributed log.** Kafka is a distributed message streaming platform using publish–subscribe, developed at LinkedIn and donated to the Apache Foundation (slide 22).

* Producers publish to a *topic*, identified by name.
* The topic is broken into *partitions* (P1, P2, P3).
* Each broker (Kafka server) delivers messages to the right consumer.
* Brokers coordinate as a cluster, and you can add brokers without downtime — horizontal scaling.

A unit of data within Kafka is called an event, events are categorized into topics, and **all events produced with a given key are written to the same partition** (slide 23) — the *key* is a field the producer stamps on each event (e.g. `orderId`); Kafka uses it to pick a partition consistently, which is why every event about the same order lands on one partition (Quiz 4 Q9).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-10.md#def-kafka" trim />
</box>

The recording grounds the constructs physically (L10 recording, ~[74:00]): brokers are the cluster's servers and host the topics — and a topic is purely *logical*, an identifier that must map onto real storage. Its **partitions are the physical manifestation**: log files, fast-access databases, or in-memory structures, with a producer typically writing to one partition. Configure one topic with one partition and you have reduced Kafka to an ordinary messaging system. Because the cluster accepts added brokers without downtime, retention can be extended as far as policy allows — which is what makes Kafka usable as the event store in CQRS (W8.3). %%Retention grounding: Kafka's shipped default is *finite* — `log.retention.hours=168`, i.e. 7 days (Confluent's retention documentation). The lecture cites 14 days (L10 recording, ~[76:00]); the precise number is a configuration choice — the teaching point is that the default is finite, not forever.%%

{% call example("Quiz 4 Q9 — the partition key is the ordering fix") %}
CampusEats publishes `OrderReady` then `OrderCollected` per order to a Kafka topic with three fixed partitions — but assigns partitions *without* using an order identifier, so `OrderCollected` can be processed before `OrderReady` for the same order. The fix that keeps three partitions and restores per-order order: **use `orderId` as the event key**, with a consistent mapping sending all events of the same order to the same partition. (Source: Quiz 4, Question 9.)
{% endcall %}

{% call example("L10 recording ~[46:00] — four order events, three partitions, three speeds") %}
A service emits `OrderPlaced`, `PaymentReceived`, `OrderFulfilled`, `OrderDelivered` to an *orders* topic with three partitions and no key — so Kafka hands them out round-robin: P0, P1, P2, P0. Three consumers in the consumer group each read one partition, on differing hardware, at 1, 5, and 2 events per second. The receiver service can then observe `OrderPlaced`, `OrderFulfilled`, `PaymentReceived`, `OrderDelivered` — business-flow nonsense caused purely by processing-speed skew, since each partition preserves its own order but the partitions run independently. Each consumer tracks an **offset** — its position in its partition (W10.3's topic definition) — so when the event at offset 3 arrives while the group's cursor sits at 1, the consumer knows to wait for event 2. Under heavy load this skew is real; under normal conditions partitions keep up and it rarely bites (L10 recording, ~[50:00]). %%Round-robin grounding: the no-key default partitioner historically assigns partitions round-robin; recent Kafka clients use a sticky variant that fills one partition's batch before switching — the ordering consequence is the same (Confluent, partitioner docs).%%
{% endcall %}

**AMQP realizes the queue world as a protocol.** AMQP is an asynchronous communication protocol — an open standard — enabling conforming client applications to communicate with conforming messaging middleware brokers. It is a peer-to-peer protocol — "peer-to-peer" in the protocol sense only: two endpoints communicating as equal parties, one playing the client application, the other a trusted message routing and delivery service, the broker (slide 25). That is unrelated to FoC being a *peer-to-peer platform* in the application sense (W8.1) — same words, different layers.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-10.md#def-amqp" trim />
</box>

<box type="info" seamless>

**Four words the deck separates (slide 10) — and they keep the naming straight.** A **protocol** is a set of rules for communication (AMQP). A **standard** is a protocol approved by an authority (the slide names IEEE, W3C) and adopted by many parties — AMQP is an open standard; protocols can also be non-standard, like JMS (the Java Message Service, the messaging specification for the Java platform). A **specification** is the formally written form of a protocol that vendors follow (Java provides the JMS specification). An **implementation** is a vendor's working mechanism for using a protocol — the slide's examples are ActiveMQ and Kafka. That is why "Kafka" and "AMQP/RabbitMQ" can sit in one breath: Kafka is an implementation (of its own messaging protocol); RabbitMQ is an implementation *of AMQP*.

</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-10.md#def-protocol" trim />
</box>

* **The AMQP model (slide 26):**
  * Messages are published to *exchanges* (think post offices or mailboxes).
  * Exchanges distribute message copies to *queues*.
  * The broker then delivers messages to consumers subscribed to the queues, or consumers fetch/pull messages on demand.
* **Routing:** the exchange routes each message based on its *bindings* — a binding is the rule that links a queue to an exchange, and the *routing key* is the message attribute the exchange checks against each binding (usually the queue's name) (slides 27–28). Multiple brokers can talk to each other to get a message to its recipient.

**RabbitMQ is the reference implementation of that model.** The message flow:

1. A producer publishes a message to an exchange.
2. The exchange receives it and is responsible for routing.
3. The exchange routes messages into queues depending on message attributes — e.g., the routing key.
4. Messages stay in the queue until handled by a consumer.
5. The consumer handles the message.

Exchange types: **direct** (route to queues whose binding key exactly matches the routing key), **fanout** (route to all queues bound to it), **topic** (wildcard match between routing key and binding pattern, e.g. `us.#` matches `us.stocks` and `us.sports`), **header** (route on message headers) (slides 28–29).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-10.md#def-rabbitmq" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-10.md#def-exchange" trim />
</box>

**Message queue systems give you asynchronous *persistent* communication — with honesty about the guarantees.** The sender is only guaranteed that the message will eventually be inserted into the recipient's queue; there is no guarantee on when — or if — it will be read and processed by the receiver (slide 30). The recording motivates the queue with the four sender/receiver liveness combinations (L10 recording, ~[88:00]):

* **Both active** — the queue merely buffers the message briefly.
* **Sender active, receiver passive** — the queue *is* the persistence, holding messages until the receiver wakes.
* **Sender done, receiver waking** — the queue replays messages in the order they were sent.
* **Both gone** — the queue holds everything until a receiver arrives.

In all four, the guarantee is the same: the message **will** be delivered — never *when*. Persistence is the next unit's subject.

<box type="warning" seamless>

**Pitfall — ordering is a per-partition promise, not a topic-wide one.** Topics allow non-sequential processing across partitions (slide 14), and Quiz 4 Q8's reviewer is wrong to call unequal partition speeds an ordering violation — per-partition ordering says nothing about processing order across partitions. When relative order within a group matters, key those events to one partition (Quiz 4 Q9).

</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** `ProcessPayment` must reach exactly one service exactly once. Which construct, and which Kafka/AMQP realization?
<panel type="seamless" minimized header="%%Answer%%">A message via a queue (point-to-point; single receiver, not copied) — e.g., AWS SQS-style queuing on the L10 slide 13 framing, or an AMQP exchange routing to one queue in RabbitMQ.</panel>

**Q2.** In RabbitMQ, which exchange type would deliver a `sports_news` message to every queue bound to it? And which matches `us.#` against `us.stocks`?
<panel type="seamless" minimized header="%%Answer%%">Fanout delivers to all bound queues; the topic exchange does the wildcard match (slide 29).</panel>

**Q3.** Why does adding Kafka brokers scale the system horizontally without downtime?
<panel type="seamless" minimized header="%%Answer%%">Because the topic's partitions are spread over brokers that coordinate as a cluster; new brokers take over partitions and traffic without a stop — the deck's horizontal-scaling point (slide 22).</panel>

**Q4.** The design needs exactly one service to act on an information item that other services could also use. Message or event? *(Asked in lecture.)*
<panel type="seamless" minimized header="%%Answer%%">Either, deliberately. A message to the one designated receiver — or multicast copies to a fixed list — if the recipient set is fixed and known. An event with a single subscriber configured if the information may matter to others later. The lecture's rule of thumb (L10 recording, ~[59:00]): information meant for a designated recipient ⇒ message; information other services can use ⇒ event — or accept replicating individual messages to each receiver.</panel>

</panel>

</panel>
<span id="W10-c4"></span>

<panel type="seamless" minimized header="**W10.4 Persistent vs transient communication ★★**">


**When the receiver is down, persistence decides whether "offline" means "later" or "never".** This is the third axis of component communication, and it combines with the first two.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-10.md#def-persistent-communication" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-10.md#def-transient-communication" trim />
</box>

The recording reaches for the postal past to make store-and-forward concrete (L10 recording, ~[90:00]): a letter rides with a courier to a post office, is *stored* there, and waits until the next courier picks it up for the next hop — repeated until the addressee collects it. Email literalizes the metaphor: POP — the *Post Office Protocol* — keeps a delivered message in the mailbox until your client (e.g. Thunderbird) reads it, and you can configure whether a copy stays in the mailbox afterwards; until the client reads, the message simply waits.

The diagram shows the two delivery disciplines end to end.

<mermaid>
flowchart LR
    subgraph PERSIST["Persistent — store-and-forward"]
        direction LR
        A["Sender"] -->|"store at each hop"| H1[("Hop 1<br/>holds message")]
        H1 -->|"forward when ready"| H2[("Receiver's queue<br/>holds until taken")]
        H2 -->|"deliver"| B["Receiver (may be down now,<br/>receives later)"]
    end
    subgraph TRANSIENT["Transient — buffer only while alive"]
        direction LR
        C["Sender"] -->|"buffer briefly"| R["Router / receiver"]
        R -->|"deliver if up"| D["Receiver (must be running)"]
        R -.->|"discard if next host down"| X["✗ message lost"]
    end
</mermaid>

%%Notation: rectangles are endpoints, cylinders are stores that hold messages, solid arrows are deliveries, and the dashed arrow is the transient world's failure mode — discarding.%%

How to read it: on top, every hop stores the message until the next node is ready — the email model: the message outlives the sender and receiver being offline at the same moment. Below, the buffer exists only while the applications execute; if the next host is down, the message is discarded — the TCP/IP router model (L10 slide 32).

**Every combination of persistence and synchronicity has a distinct guarantee.** (Source: L10 slide 33.)

| Combination | What happens |
|---|---|
| **Persistent async** | Sender keeps executing without blocking; the message may take an arbitrary time to arrive; the sender may or may not be running by delivery time; disks or memory queues persist it; **delivery is eventually guaranteed** |
| **Persistent sync** | Sender blocks until an **ack of receipt** (not delivery/response); the message persists in the receiver's queue (or any router) for an arbitrary time |
| **Transient async** | Sender continues (non-blocking); the **receiver must be running** or the message is discarded; same if any router on the way is down |
| **Transient sync** | Sender blocks — in a **spectrum of three strengths**, weakest to strongest in what it confirms: **receipt-based** (blocks until an ack is received; says nothing about processing having started), **delivery-based** (blocks until the receiver *takes delivery*; processing then continues asynchronously, so — unlike response-based blocking — the wait ends at **delivery**, not when the reply comes back), **response-based** (blocks until the full reply — traditional RPC: *remote procedure call*, calling a remote service as if it were a local function; W6's gRPC is its modern realization) |

%%Citation — the delivery-based label "essentially an asynchronous RPC" follows Coulouris et al., *Distributed Systems*: in that reading "delivery" (handing the message to the receiver) and "processing" (the reply) are distinct milestones, which is exactly the gap this cell exploits.%%

{% call example("L10 slide 34 — one example per corner") %}
Email systems are persistent and asynchronous. Messaging/chat apps are persistent and synchronous (the message is stored, but you block on the exchange). UDP (User Datagram Protocol) communication is transient and asynchronous — no store, no wait. Traditional RPC (remote procedure call) is transient and synchronous — the reply *is* the delivery.
{% endcall %}

{% call example("Quiz 4 Q10 — persistence is not a deadline") %}
A transport operator requires every submitted incident to be analyzed within five minutes. Its broker reliably retains incident messages while the analysis service is offline — but the service can stay offline for an hour. An engineer claims persistence alone satisfies the five-minute requirement. The engineer is **incorrect**: persistence protects *pending work*, but the deadline also requires sufficient availability and processing capacity. (Source: Quiz 4, Question 10.)
{% endcall %}

**Putting the three axes together.** Component communication varies on **synchronous or asynchronous**, **single or multiple receivers**, and **persistent or transient** — and any cell of that grid is a legitimate design, e.g. persistent-async email, persistent-sync chat, transient-async UDP, transient-sync RPC (slide 34). Within one application you may mix cells freely (slide 20).

<box type="warning" seamless>

**Pitfall — "persistent" is about *storage*, not *timeliness* or *processing*.** A persistent queue guarantees the message eventually reaches the recipient's queue; it guarantees neither *when* it is read, *whether* it is processed (slide 30), nor that a business deadline (five minutes, Quiz 4 Q10) is met without capacity behind the queue.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Classify: (a) email, (b) UDP, (c) traditional RPC on the three axes.
<panel type="seamless" minimized header="%%Answer%%">(a) persistent, asynchronous, single receiver (one mailbox). (b) transient, asynchronous. (c) transient, synchronous, receipt→delivery→response-based blocking (slides 33–34).</panel>

**Q2.** A persistent-async message is accepted by the broker. The receiver stays down for a week. Is the message lost? Was the sender blocked?
<panel type="seamless" minimized header="%%Answer%%">Not lost — persistence stores it at intermediate hops until the receiver is ready, and delivery is eventually guaranteed. The sender was not blocked: persistent-async senders keep executing (slide 33).</panel>

**Q3.** Which blocking flavor is "traditional RPC", and what does its ack actually tell you in the receipt-based variant?
<panel type="seamless" minimized header="%%Answer%%">Response-based blocking is traditional RPC — the client waits for the whole reply. Receipt-based blocking only confirms an ack was received; it says nothing about whether the process started on the receiver (slide 33).</panel>

</panel>

<box type="info" seamless>

**Section summary**

* **Sync means wait; async means continue** — and asynchronicity can be built *into* request–reply with 202 Accepted, a status endpoint, and correlation identifiers.
* **Intent classifies the payload:** a past-tense fact broadcast on a topic is an event; an imperative request handed to one receiver on a queue is a message — and ownership of payload and channel flips accordingly.
* **Receivers choose the topology:** exactly-one-consumer queues (unicast, FIFO) vs broadcasting topics (pub/sub, per-partition ordering; Kafka and AMQP/RabbitMQ are the reference realizations).
* **Persistence is the third axis:** store-and-forward survives outages and guarantees eventual delivery; transient buffers vanish with their applications — and neither persistence nor asynchronicity is a timeliness or capacity guarantee.
</box>

</panel>
## Key terms

<span id="W10-key-terms"></span>

| Term | Definition | Unit |
|---|---|---|
| Synchronous communication | Request–reply; sender waits; tightly coupled | [W10.1](#W10-c1) |
| Asynchronous communication | Lag between send and receive; sender continues; loosely coupled | [W10.1](#W10-c1) |
| Async request–reply | 202 Accepted + status endpoint + polling + redirect for long-running work | [W10.1](#W10-c1) |
| Message | A command/query *request* sent point-to-point to one receiver | [W10.2](#W10-c2) |
| Event | A past-tense fact, broadcast to all subscribers | [W10.2](#W10-c2) |
| Topic | One-to-many channel; per-partition ordering only | [W10.3](#W10-c3) |
| Queue | Single-receiver FIFO channel; messages not copied | [W10.3](#W10-c3) |
| Publish–subscribe | Broadcasting-station topology with many subscribers | [W10.3](#W10-c3) |
| AMQP | Open async messaging protocol: publishers → exchanges → queues → consumers | [W10.3](#W10-c3) |
| Kafka | Distributed pub/sub streaming platform: topics → partitions over a broker cluster | [W10.3](#W10-c3) |
| Exchange | AMQP routing step matching routing keys to bound queues (direct/fanout/topic/header) | [W10.3](#W10-c3) |
| Protocol / standard / specification / implementation | Rules for communication; approved by an authority; formally written; vendor's working mechanism | [W10.3](#W10-c3) |
| Persistent communication | Store-and-forward; survives inactive senders/receivers | [W10.4](#W10-c4) |
| Transient communication | Buffered only while applications execute; discarded if undeliverable | [W10.4](#W10-c4) |

## Connections

| Concept | Lecture | Tutorial | Other weeks / quizzes |
|---|---|---|---|
| Sync vs async | L10 slides 4–8 | Tutorial 7 Q1 (sync API calls + async events in FoC) | W9.2 (fire-and-forget); Quiz 4 Q7 |
| Events vs messages | L10 slides 9–18 | Tutorial 7 Q3 (streams feed services) | W9.1 (event vs command vs query); Quiz 4 Q1 |
| Topic vs queue, Kafka, AMQP | L10 slides 10, 19–30 | — | W9.3–W9.4 (broker semantics); Quiz 4 Q8, Q9 |
| Persistent vs transient | L10 slides 31–34 | — | Quiz 4 Q4, Q10; W12 (scalability of the broker) |

## Further reading

* Microsoft Azure, [Async request-reply pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/async-request-reply) — source of the 202/status-endpoint slides (L10 slides 7–8).
* [CloudAMQP, RabbitMQ for beginners](https://www.cloudamqp.com/blog/part1-rabbitmq-for-beginners-what-is-rabbitmq.html) — source of the exchange-type slides (L10 slides 28–29).
* Confluent, [*Kafka: The Definitive Guide*](https://www.confluent.io/resources/kafka-the-definitive-guide/) — cited on L10 slides 22–23.
* The se-book's [event-driven architecture page](https://se-edu.github.io/se-book/architecture/architecturalStyles/eventDriven/) — publish–subscribe framing.

## Summary

**Key takeaways** (one per outcome):

* **Synchronous communication makes the caller wait and own the failure; asynchronous lets it continue** — and long-running work keeps a clean request–reply facade via 202 Accepted, a status endpoint, and correlation identifiers.
* **Intent is the classifier:** a broadcast past-tense fact (event, topic, publisher-owned) vs a directed request to act or fetch (message — command or query — queue, receiver-owned); the tenant-deletion scenario shows the same requirement wired deliberately either way.
* **Receiver count picks the topology:** single-receiver unicast queues vs many-subscriber pub/sub topics, realized by Kafka (partitioned logs, key-based placement, horizontal scaling) and AMQP/RabbitMQ (exchanges, bindings, routing keys) — with ordering guaranteed only per partition.
* **Persistence is orthogonal and survivable:**
  * Store-and-forward keeps messages across outages and guarantees eventual delivery.
  * Transient buffers discard on failure.
  * The 2×2 with (a)synchronicity — from email to RPC — each carries its own precise guarantee.

Key terms: see the [Key terms table](#W10-key-terms) above, each linked to its unit.

%%Next: Week 11 — Messaging. The broker constructs of this week (topics, queues, exchanges, partitions) become the system's backbone; W11's messaging chapter builds directly on W10.2–W10.4.%%

</div>
