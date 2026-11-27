{% from "schedule/macros-fragment.md" import term, example, icon_outcome with context %}
<h2>Week 11 — Messaging</h2>

<span>

This chapter builds on [Week 9 — Event-Driven Architecture]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#core-concepts) (events, fire-and-forget) and [Week 10 — Asynchronous Communication]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#core-concepts) (messages, persistence, pub-sub). You should know the difference between a message and an event — *intent matters* — before reading on.

</span>

<span>

{{ icon_outcome }} **Can explain why enterprise integration uses messaging and name the EIP categories** (W11.1)

{{ icon_outcome }} **Can choose the right message payload — command, document or event — for an interaction** (W11.2)

{{ icon_outcome }} **Can design message channels, including request-reply with a return address and correlation identifier, and dead-letter handling** (W11.3, W11.7)

{{ icon_outcome }} **Can select and compose routing patterns — content-based router, message filter, splitter, aggregator, scatter-gather, pipes-and-filters — for a given message flow** (W11.4)

{{ icon_outcome }} **Can explain how messages are transformed between formats and how applications connect to a messaging system** (W11.5, W11.6)

</span>

<div>

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

%%A standing disclaimer from the lecture (L11 recording, ~[5:00]): this deck says "messaging", "channel", and "event" loosely, but Week 10's truth holds — a topic is publish–subscribe reaching every subscriber, a message has a designated recipient. The patterns are collectively called *messaging* patterns, hence the loose usage.%%

## Core concepts

<span id="W11-c1"></span>

<panel type="seamless" minimized header="**W11.1 Enterprise integration and the message broker ★**">


**Once an application is split across the network, the hard problem is no longer the components themselves but making them talk to each other.** The lecture's shorthand: every D.A.D (Distributed Application Development) needs M.O.M. (Source: L11 slides 4–5.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-message-broker" trim />
</box>

**An event *store* and an event *broker* optimize for different things — one system can be both.** A store's goal is retention: it keeps messages until configured otherwise (retain-forever is a legitimate setting). A broker's goal is throughput: passing information on to consumers as efficiently as possible. Kafka deliberately does both — receive an event, broadcast it, and store it (L11 recording, ~[13:00]).

**Applications that must integrate rarely speak the same language.** They run on different platforms, use different programming languages and data formats, and the network between them is unreliable. They also change at different times, so the integration must cope with change in an application, its protocol, or its data format. (Source: L11 slide 5 — the Modreg ↔ Canvas example.)

{% call example("L11 recording ~[23:00] — three faces of heterogeneity in one ride-hailing app") %}
The backend is Spring Boot, the front end React Native — different platforms, languages, and data formats. Even a coordinate pair must be agreed: `lat,long` or `long,lat` — swap the two and a "one degree" value puts the car in the wrong city. The *protocol* evolves too: ride-hailing started with a flat flag-down fare, then introduced surge pricing when demand spikes — same entity (money), different charging rules. And every participant needs a common understanding: an ETA query returning `5` means five *minutes* only because both sides agreed it does (L11 recording, ~[23:00]–[26:00]).
{% endcall %}

**Enterprise integration has three classic topologies, and only one of them ages well** (Source: L11 slide 7):

- **Point-to-point** integration connects every pair of applications directly.
- **Hub-and-spoke** routes everything through a central mediator, which becomes a central point of failure and a bottleneck.
- **The enterprise service bus** gives every application a message-based abstraction for connecting to apps and data.

**Enterprise Integration Patterns (EIP) are a technology-independent catalogue of solutions to common integration problems.** EIP gives developers and architects a shared vocabulary for describing integrations, independent of any vendor. The catalogue is the 2003 book *Enterprise Integration Patterns* by Gregor Hohpe and Bobby Woolf — the deck's cited source (L11 slide 4). The catalogue documents 65 patterns in six categories — message construction, message channels, message routing, message transformation, message endpoints, and system management — and every MOM is expected to support these capabilities. (Source: L11 slides 8, 14–15.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-enterprise-integration-patterns" trim />
</box>

%%Many messaging products implement EIP under their own feature names — e.g. JMS (the Java Message Service, Java's messaging standard — defined in W10.3) providers such as Apache ActiveMQ, and Amazon MQ, SQS (Simple Queue Service) and SNS (Simple Notification Service). The deck marks the vendor-specific slides optional/not examinable: SQS message lifecycle (slide 13), JMS message types (slide 18), the JMS request/reply example (slide 21), SQS dead-letter mechanics (slide 28), RabbitMQ's direct exchange (slide 30), and SNS message filtering (slides 41–45). The recording's naming table makes the pattern/vendor split vivid (L11 recording, ~[40:00]): the *publish–subscribe channel* pattern is called a topic by JMS and RabbitMQ, a subject by TIBCO — the pattern is the stable thing; vendor names come and go.%%

**A message broker buffers messages and hides the network from both sides.** It passes information between software components while minimising how much they need to know about each other, buffers incoming messages, and shields applications from many operating-system and network complexities. (Source: L11 slides 11, 64.)

The diagram below contrasts direct point-to-point integration with integration through a broker, which is what the rest of this chapter assumes.

<mermaid>
flowchart LR
  subgraph direct["Point-to-point (slide 7)"]
    direction LR
    M["Modreg"] --- C["Canvas"]
    M --- L["Library system"]
    C --- L
  end
  subgraph mom["Via a message broker (slide 11)"]
    direction LR
    m["Modreg"] -.-> b(("Messaging<br>system"))
    c["Canvas"] -.-> b
    l["Library system"] -.-> b
    b -.-> d1["dest 1"]
    b -.-> d2["dest 2"]
  end
</mermaid>

%%Notation: a box is an application, a solid line is a direct point-to-point integration (the link is mutual, so no arrowheads), a dashed arrow is an asynchronous message sent through the messaging system, and the double circle is the broker/MOM.%%

How to read it: with three applications, point-to-point already needs every pair wired together, and adding a fourth application means touching all of them. In the broker version each application only knows the broker — exactly the loosely coupled setup the deck recommends for integrations like Modreg ↔ Canvas.

{% call example("Modreg ↔ Canvas (L11 slides 5–7)") %}
Modreg (course registration) and Canvas (learning management) are separate systems with different platforms, programming languages and data formats, yet grades and enrolment data must flow between them. A messaging broker between them takes care of seamless communication: each side speaks to the broker in an agreed message format instead of calling the other system directly over an unreliable network. The recording makes the format clash concrete: Modreg exports enrolment data as XML while Canvas works with CSV — something in between must translate (L11 recording, ~[19:00]). It also lists the pre-messaging integration media: a file drop (one side converts to a format the other reads) and a shared database — an anti-pattern *within* microservices, where it reintroduces coupling, but still a legitimate mechanism between two independent applications (L11 recording, ~[20:00]).
{% endcall %}

The professor's analogy for what the middleware buys you (L11 recording, ~[30:00]): mailing a parcel abroad, you package it, affix a stamp, and drop it in a post box — how the destination country routes, addresses, and delivers it, down to the last mile, is none of your concern. The postal system is the middleware: it abstracts the delivery machinery away behind a simple drop-off contract.

<box type="warning" seamless>

**Pitfall:** hub-and-spoke looks like a broker, but the hub is a *mediator* — every integration between applications passes through it, making it a central point of failure and a bottleneck (L11 slide 7). A messaging broker differs: it buffers messages, so a temporarily unavailable receiver does not block the sender.

**The recording sharpens the hub-vs-bus line.** In hub-and-spoke, the *application* is responsible for producing a data format the other side understands (L11 recording, ~[33:00]); an enterprise service bus takes over transformation itself, alongside routing, orchestration, message passing, and security — which is why the ESB is "a more formidable solution" than a plain hub (L11 recording, ~[34:00]).

</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** A teammate proposes connecting ten applications with point-to-point integrations "because it is simplest". What two problems does the deck predict?
<panel type="seamless" minimized header="%%Answer%%">
The number of integrations grows with every pair of applications, and each new application must be wired into all existing ones. Worse, every integration hard-codes knowledge of the other side's platform, language and format, so any change ripples across the mesh. A broker decouples senders from receivers and buffers messages (L11 slides 7, 11, 64).
</panel>

**Q2.** Why does the deck call EIP "vendor independent", and why does that matter?
<panel type="seamless" minimized header="%%Answer%%">
EIP are technology-independent solutions with agreed names, so many vendors implement them as product features (e.g. Amazon MQ, SQS, SNS). Because the *patterns* stay fixed, you can swap the messaging product behind them with minimal code change (L11 slides 8–10).
</panel>

**Q3.** "If the broker eliminates coupling, where does the coupling go?" *(Asked in lecture.)*
<panel type="seamless" minimized header="%%Answer%%">
You remove the *direct* coupling between the two parties and add coupling to the messaging system instead — the applications now depend on the broker. The payoff (L11 recording, ~[42:00]): because every broker implements the same patterns, swapping one vendor for another needs minimal changes — the API surface is small and stable ("get is get", whether the broker is RabbitMQ or Kafka).
</panel>

</panel>

</panel>
<span id="W11-c2"></span>

<panel type="seamless" minimized header="**W11.2 Message construction: command, document, event ★**">


**The payload you put in a message decides what the receiver may do with it — confuse an instruction with a record, and the receiver does the wrong thing.** That distinction is examined directly: Quiz 4 Q1 asks you to redesign a mislabelled message.

**A message separates metadata from data** (Source: L11 slides 16–17):

- The *header* specifies the type of information being transmitted, its origin, destination, size and other structural information.
- The *body* carries the actual information.
- Optional *properties* are used mostly for message selection and filtering.

%%The deck's three kinds are JMS terms (L11 slides 16–17): *application-related* properties are set by your code, *provider-related* ones by the messaging vendor, and *standard* ones — such as JMSXDeliveryCount, the JMS-specified count of delivery attempts for a message — are defined by the JMS specification itself.%% The deck summarises: message = metadata + data.

**There are three kinds of payload, and they differ in intent** (Source: L11 slide 17; L13 slides 5–7):

- A **command** tells the receiver to do something.
- A **document** gives the receiver data to process at its own discretion.
- An **event** notifies the receiver that something has happened.

This is the same "message vs event — intent matters!" line from Weeks 9–10, now completed with commands and documents.

<box type="info" seamless>

**Tell the three payload kinds apart with one question: what should the receiver *do* with this message — act, process at its discretion, or just know?**

| Payload kind | The receiver should… | Is a reply expected? | Course example |
|---|---|---|---|
| **Command** | Act — perform the instruction | Maybe — request-reply is common, but no data *value* returns (W9.1) | `ReserveEquipment` → the Reservation service checks availability and reserves or rejects (Quiz 4 Q1) |
| **Document** | Process the data at its own discretion | No | The purchase-order document translated to XML for the order-management system (W11.5) |
| **Event** | Just *know* — react if it cares | No — it records a completed fact | `EquipmentReserved`, published only after a reservation succeeds (Quiz 4 Q1) |

**Two nearby taxonomies are easily confused with this one.** (1) W10.2's event-vs-message table classifies by the *sender's* intent — a broadcast fact vs a directed request; the payload kinds above say what a message can carry: a command is W10's "request to be executed", an event message is W10's event, and the document kind is the addition Week 11 makes. W10's *query* is not a fourth kind here: a query travels as a command message whose instruction is "answer this query", with the answer coming back as the reply %%L11 slide 17 lists only command/document/event; L10 slide 13 defined query as the second half of a message%%. (2) W9.1's four views (discovery, storage, structure, content) are roles one event artifact plays in *design*, not payload kinds — `EquipmentReserved` stays one event whether you view it as a notification or as event-carried state transfer (W9's content view).

</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-message-construction" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-command-message" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-document-message" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-event-message" trim />
</box>

- An event invites consumers to react
- A command obliges one receiver to act
- A document merely informs

{% call example("EquipmentReserved vs ReserveEquipment (Quiz 4 Q1)") %}
A university equipment platform sends a message named EquipmentReserved to the Reservation service, which is *expected to check availability and either reserve the equipment or reject the request*. As named, the message is an event — a record of a reservation that already succeeded — so it cannot carry an instruction. The correct redesign is a ReserveEquipment **command** for the request; the Reservation service publishes EquipmentReserved as an **event** only after a reservation succeeds.
{% endcall %}

<box type="warning" seamless>

**Pitfall:** sending an event and expecting an action, or a command that consumers treat as optional news. If the sender needs something done, send a command to a specific receiver; if the sender is only announcing a completed fact, publish an event (Quiz 4 Q1; L11 slide 17).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Classify each payload: (a) "OrderConfirmed — the order has been paid and packed"; (b) "ReserveInventoryItem SKU-123 ×2"; (c) "Invoice PDF for order 42".
<panel type="seamless" minimized header="%%Answer%%">
(a) Event — a record that something has happened. (b) Command — an instruction to a specific receiver. (c) Document — data for the receiver to process (L11 slide 17).
</panel>

**Q2.** Which part of a message do message filters typically inspect, and why are properties "optional"?
<panel type="seamless" minimized header="%%Answer%%">
The filter's criteria are applied to the message content — the EIP definition matches on what the message *contains*, which is why the message filter is a content-based router (L11 slide 37). Properties are optional because they exist mostly to *support* that selection and filtering (L11 slide 17) — e.g. in AWS SNS each subscriber sets a *subscription filter policy*, and SNS pushes to it only messages whose attributes match the policy %%L11 slides 41–45, optional vendor detail%% — not to carry the payload itself.
</panel>

</panel>

</panel>
<span id="W11-c3"></span>

<panel type="seamless" minimized header="**W11.3 Message channels ★**">


**A message needs a road: collaborating senders and receivers exchange messages only through channels they both know.** A channel is the conduit between them. The deck's slide heading calls channels "message queues" because the queue is the channel shape you meet first (and the one vendor APIs name); in general a channel comes in two shapes — a queue (point-to-point: one consumer per message) and a topic (publish-subscribe: all subscribers) — as the next paragraph makes precise. (Source: L11 slides 19–20, 31–32.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-message-channel" trim />
</box>

**A channel transmits messages in one direction, so a two-way exchange needs two channels.** In the request/reply setup, the requestor sends a request message on the request channel and the replier answers on a separate reply channel. (Source: L11 slide 20.) %%The recording flags this as a fix over the uploaded deck (L11 recording, ~[49:00]): the slide said "two-way channel"; the corrected statement is *two one-way channels*.%%

**Point-to-point and publish-subscribe channels differ in who receives a message.** On a point-to-point channel, exactly one consumer consumes each message. On a publish-subscribe channel, any message published to a topic is immediately received by all subscribers of the topic — used when multiple parties are interested in the same messages. A pub-sub *request-response* variant uses a pub-sub channel for the requests but a point-to-point channel for the responses, so one requester can collect and aggregate replies from many parallel workers. (Source: L11 slides 19, 31–32, and 39 — the single-consumer property is in the slide-39 comparison table.)

{% call example("L11 recording ~[72:00] — pub-sub request–response in a ride-hailing app") %}
A drop-off request is *published* to all nearby drivers — pub-sub, with no direct reply mechanism. The drivers' acceptances flow back over a point-to-point response channel into an aggregator, which picks the winning driver and notifies the customer. The losers' stale responses carry a deliberately short time to live — not the hours-scale TTL of batch systems — and end in the dead letter channel. The request vanishing from a driver's screen a few moments later is the system saying "no longer available" (L11 recording, ~[72:00]–[74:00]).
{% endcall %}

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-point-to-point-channel" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-publish-subscribe-channel" trim />
</box>

<box type="info" seamless>

**Two different things are called "point-to-point" — a wiring of applications and a delivery shape of a channel.** One question tells them apart: is it describing how *applications* are connected, or how *one message* is delivered?

| Term | What it describes | What it means | Course example |
|---|---|---|---|
| Point-to-point **integration** (L11 slide 7) | Topology between applications | Every pair of applications connects directly, each link hard-coding knowledge of the other side — with ten applications that is 45 pairwise integrations (10×9/2) %%count derived; the slide shows the mesh as a figure%% | The Modreg ↔ Canvas ↔ Library mesh in W11.1's diagram |
| Point-to-point **channel** (L11 slides 19, 39) | Delivery on one channel | Exactly one consumer consumes each message, even if several consumers listen — implemented by a queue | The `ReserveEquipment` command on a queue: exactly one reservation worker picks it up |

The deck's slide-50 heading "pub/sub, P2P, aggregator, content-based router" uses the second sense — the same "point-to-point" as the queue column of W10.2's event-vs-message table.

</box>

The delivery difference is drawn side by side in [W10.2 — Events vs messages]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#W10-c2): the topic fans one published message out to every subscriber, the queue hands each message to exactly one consumer. On the equipment platform of Quiz 4, the `OrderReady` event would travel on a topic so that every interested service receives it, while a `ReserveEquipment` command travels on a queue so that exactly one reservation worker picks it up.

<box type="info" seamless>

**Queue, topic, exchange — one question separates the three: who receives a message that enters the construct?**

| Construct | Who receives the message | Course example |
|---|---|---|
| **Queue** (point-to-point channel) | Exactly one of its consumers — each message is handed to a single receiver, which is what lets competing consumers share the load | `ReserveEquipment` on a queue — exactly one reservation worker picks it up |
| **Topic** (publish-subscribe channel) | Every current subscriber receives a copy | `OrderReady` on a topic — every interested service receives it |
| **Exchange** (RabbitMQ; optional slide 30) | Nobody itself — an exchange is a *routing rule* that forwards each incoming message to the queues bound to it, matching the message's routing key against their binding keys | The deck's `pdf_events` direct exchange: a message with routing key `pdf_create` goes only to the queue bound with binding key `pdf_create` |

%%Vendor detail (slide 30, marked optional): a *fanout* exchange copies a message to all bound queues — topic-like delivery; a *direct* exchange matches keys — filter-like selection. Per eaipatterns.com's RabbitMQ example, "exchanges are a concept which is distinct from a queue".%%

</box>

**The request carries a return address; the reply carries a correlation identifier.** The return address tells the replier *where* to send the reply. To match a reply to its request when many requests are outstanding, the request carries a unique request ID and the replier copies it into the reply as the correlation ID; the requestor matches each reply to the request that caused it. (Source: L11 slides 23–25.)

The recording's return-address scenario shows the reply need not come back to the requestor (L11 recording, ~[53:00]): a payment-processing component sets `ReplyTo` to the *warehouse* channel, so its "payment received" acknowledgement doubles as the trigger for "pack this item". The address is a logical abstraction — in JMS, a `Destination` object, not an IP address — and when several requesters share one request channel, each supplies its own reply channel, so the replier answers each on the channel it named.

Two responsibilities make the correlation match work (L11 recording, ~[58:00]): the *replier* copies the request's message ID into the reply's correlation ID, and the *requestor* matches each arriving reply to its outstanding request — the same bookkeeping W10.1 assigned to the sender of asynchronous notifications. Because replies can arrive out of order, a sequence number works well as the identifier: send requests 1, 2, 3 and each reply carries its number back, however shuffled. One request can even fan into several replies — the recording's media example: one request answered by both the video stream and the recommendation list, each routed to the right part of the application by the shared correlation ID (L11 recording, ~[56:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-return-address" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-correlation-identifier" trim />
</box>

{% call example("A request and its reply, message by message (L11 slide 22)") %}
In the deck's request/reply log, the sent request has `Message ID: ...6.2.1.1`, `Correl. ID: null` and `Reply to: jms/ReplyQueue`. The reply arrives with a *different* message ID (`...5.2.1.1`) but `Correl. ID: ...6.2.1.1` — exactly the request's ID — which is how the requestor knows which outstanding request it answers. The request could even be sent while the replier was not running: the message is persisted on the channel until the replier consumes it.
{% endcall %}

**Channels also have defined failure behaviour.** An invalid message channel receives messages a receiver cannot interpret; a dead letter channel receives messages the messaging system cannot deliver — instead of retrying failing messages until they expire, move them to a dead-letter queue (DLQ) after a few attempts, then *redrive* them once the cause is fixed — %%redrive is AWS's term (L11 slide 28) for moving the messages from the DLQ back to the source queue, or to another queue, for another processing attempt%%. A data type channel carries one data type per channel, so the receiver knows the type from the channel it arrived on. (Source: L11 slides 27–29.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-invalid-message-channel" trim />
</box>

Why park an unusable message instead of discarding it (L11 recording, ~[64:00])? Two reasons: administrators can later debug *why* it failed, and a downstream consumer that simply finds nothing may crash — a message routed to the invalid channel degrades the flow gracefully instead. The recording's instance: a translation step expecting to turn Modreg's XML into JSON fails, the XML lands in the invalid channel, and everything downstream of the failure keeps running.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-dead-letter-channel" trim />
</box>

The recording fills in the dead-letter mechanics (L11 recording, ~[65:00]): every message carries a *time to live* (TTL) — how long the system keeps trying before giving up (say, six hours). If delivery is still failing when the TTL expires — network down, receiver crashed — the message moves to the dead letter channel. From there, the messaging system can be configured to revive and retry it after a set interval, and to give up entirely after a maximum lifetime. Because every expired message lands in the DLQ, counting them doubles as a downtime statistic.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-redrive" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-data-type-channel" trim />
</box>

The recording's data type channel (L11 recording, ~[68:00]): a media application moves video on a video channel and advertisement data on an advertisement channel — an ad arriving on the video channel would be an *invalid* message. One type per channel lets each consumer optimize entirely for its data type; RabbitMQ's direct exchange (W10.3) is the concrete manifestation.

**When a request causes a reply that is itself another request, the chain can be retraced.** Request-reply chaining keeps the correlation of replies back to the original request — e.g. for auditing. (Source: L11 slide 26.)

The recording shows why chaining earns its keep (L11 recording, ~[61:00]): an order flows through payment, warehouse, fulfilment, and shipping, every reply correlated back to the original order ID — so a missing reply *localizes* the failure ("nothing came back after this hop"), the whole chain is auditable, and when an order fails, the compensation pathway is traceable — the bookkeeping a saga's compensating actions (W8.2) sit on top of. The recording places correlation IDs at "slightly below the saga pattern, far above TCP" on the abstraction ladder (L11 recording, ~[62:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-request-reply-chaining" trim />
</box>

<box type="warning" seamless>

**Pitfall:** trying to send the reply back on the request channel. A channel is one-directional; without a separate reply channel — plus return address and correlation ID — the reply either never arrives or cannot be matched to the right request when several are outstanding (L11 slides 20–25).

</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Why does request/reply need two channels while fire-and-forget needs one?
<panel type="seamless" minimized header="%%Answer%%">
A channel transmits in one direction only. Fire-and-forget sends one message and moves on; request-reply must also carry the reply back, which requires a second channel plus a return address in the request (L11 slides 20, 23).
</panel>

**Q2.** An SQS consumer crashes *while* processing a message. What happens next, and when should the message land in the DLQ?
<panel type="seamless" minimized header="%%Answer%%">
The message becomes visible again after the visibility timeout — the period during which a fetched message is hidden from other consumers — its receive count increases, and once the count reaches the configured limit the message moves to the designated dead-letter queue; from there it can be redriven to the source queue after the fault is fixed (L11 slide 28 — optional vendor detail, but the DLQ idea itself is examinable: slide 27).
</panel>

</panel>

</panel>
<span id="W11-c4"></span>

<panel type="seamless" minimized header="**W11.4 Message routing ★**">


**Without routing logic, every sender must know every recipient; routers move that knowledge out of the sender and into reusable components.** A message router consumes messages from one channel and reinserts them into different channels depending on a set of conditions — either the sender decides where each message goes, or a component like this decides for it, reducing the sender's workload. Simple routers connect one inbound channel to one or more outbound channels; composed routers combine several simple routers into more complex flows. (Source: L11 slides 34–35.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-message-router" trim />
</box>

**A content-based router routes on what the message contains.** It examines the message content and sends it to a channel based on the data in it, decoupling sender from receiver — but it must know all possible recipients, so any change in the recipient list means a change in the router. (Source: L11 slide 36.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-content-based-router" trim />
</box>

The recording's routing scenario (L11 recording, ~[84:00]): an online order for gadgets *and* widgets arrives, but the widget processor handles only widgets and the gadget processor only gadgets — so the router inspects the order content and sends widget lines to the widget inventory's channel and gadget lines to the gadget inventory's channel. The price of that convenience (L11 recording, ~[85:00]): the router must know every recipient and its capabilities. RabbitMQ's direct exchange from W10.3 — routing a `pdf_process` key to the PDF-processing queue — is the same shape at vendor scale.

**A message filter is a content-based router with a single output channel.** Messages matching its criteria are routed on; the rest are discarded. (Source: L11 slide 37.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-message-filter" trim />
</box>

<box type="info" seamless>

**"Filter" appears in three senses this week — the tell-apart question is: does it act on whole messages, or on data items inside one message?**

| Sense | Acts on | What it does | Where you meet it |
|---|---|---|---|
| **Message filter** (a routing pattern) | Whole messages | Passes matching messages on, discards the rest — a content-based router with a single output channel | W11.4's widget promotion |
| **Filter** in pipes-and-filters | Whole messages | Any single-purpose processing step: splitter, router, translator and aggregator are all "filters" connected by channels ("pipes") | W11.4's order-processing chain; Quiz 2's "resize filter" is a step like this |
| **Content filter** (a transformation pattern) | Data items inside one message | Removes data items the receiver does not need, keeps the message itself | W11.5 |

So when the EIP catalogue calls the aggregator "a stateful filter", that is the second sense — a step in a chain, not a message filter: it discards nothing, it waits for a complete correlated set and publishes one combined message.

</box>

{% call example("The widget promotion (L11 slide 38)") %}
An order-processing system runs a November promotion — all widgets are 10 % off — and must send the promo only to the intended audience, e.g. customers who prefer widgets. A message filter on the notification channel passes through messages whose content matches the criteria (e.g. `prefers=widgets`) and discards the rest, so uninterested customers never see the promotion.
{% endcall %}

**Content-based routing and pub-sub with filters are near substitutes — choose by who controls the routing.** The deck's comparison (Source: L11 slide 39):

| Aspect | Content-based router | Pub-sub channel + message filter |
|---|---|---|
| Who receives each message | Exactly one consumer | More than one consumer can consume a message |
| Control | Central control and maintenance — predictive routing | Distributed control and maintenance — reactive filtering |
| Participant knowledge | Router needs to know participants; updated when they change | No knowledge of participants required; adding/removing is easy |
| Typical use | Business transactions, e.g. orders | Event notifications / informational messages |
| Fits best | Queue-based channels | Publish-subscribe channels |

%%The deck's shorthand: *predictive* because the router decides ahead of time, from its central knowledge of recipients, which channel each kind of message goes to; *reactive* because nothing upstream decides — subscribers react to whatever arrives and filter it themselves.%%

The recording builds the pub-sub-plus-filter alternative out explicitly (L11 recording, ~[89:00]): duplicate every incoming message onto all the channels, and put a filter in front of each queue — the widget filter passes widgets and drops gadgets, the gadget filter does the reverse. To the messaging system it is duplication and broadcast; to each recipient it is filtering and acceptance.

**Some routing decisions do not look at content at all.** A context-based router chooses the destination from the *context* — commonly for load balancing, testing or failover, e.g. re-routing messages to another processing component when one fails. (Source: L11 slide 40.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-context-based-router" trim />
</box>

The recording's load-balancing instance (L11 recording, ~[91:00]): the router watches the *outbound queue's* fullness — system context, not message content — and detours traffic to another recipient when pushing further would drop messages.

**Splitter, aggregator and scatter-gather reshape message streams** (Source: L11 slides 47–48, 52):

- A **splitter** turns a single message into multiple messages (one per order item).
- An **aggregator** — a special filter — collects correlated messages and publishes one aggregated message once a complete set has arrived.
- **Scatter-gather** broadcasts one message to many participants concurrently and reassembles their replies into one message.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-splitter" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-aggregator" trim />
</box>

Concretely (L11 recording, ~[95:00]): three quotation replies arrive carrying correlation ID 100, and one carries 101; the aggregator groups by the ID, and once the set for 100 is complete, publishes the reconstructed message — say, the combined order status — downstream.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-scatter-gather" trim />
</box>

{% call example("L11 recording ~[100:00] — the insurance agent as scatter-gather") %}
You ask an agent for the best combination of investment, health, and life cover. The agent scatters the request to several insurers in parallel, and each replies with a full package of quotes, which a first aggregator reassembles. Comparing the packages, the agent picks the best provider *per category* and hands you one recommendation — a second aggregator combining the winners ("for investment, provider A; for health and life, provider B"). Two gathers, two aggregators (L11 recording, ~[100:00]–[104:00]).
{% endcall %}

<box type="info" seamless>

**Splitter and scatter-gather both fan out and recombine — one question tells them apart: is the fan-out over the pieces of one message, or over many recipients of one request?**

| | Splitter (+ aggregator) | Scatter-gather |
|---|---|---|
| What fans out | The *content*: one composite message is cut into per-part messages (one per order item) | The *recipients*: the same full request is sent concurrently to many participants |
| Each receiver processes | One part of the original | The whole request |
| Re-join | The aggregator correlates the per-part results back into one message (e.g. by order ID) | The gather side aggregates the *replies* into a single response |
| Course example | Tutorial 9 Q3: order with multiple items → one message per item → inventories → single confirmation | EIP's order example: request quotes from all suppliers of an out-of-stock item, then aggregate the quotes to pick the best |

That is also why the deck's combined example (slide 53) needs *two* aggregators: one inside the scatter-gather to gather each branch's replies, and one after the splitter flow to recombine the per-item results.

</box>

**Composing these patterns gives you pipes-and-filters: a chain of single-purpose steps connected by channels.**

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-pipes-and-filters" trim />
</box>

The deck's order-processing example composes exactly this chain, and the diagram below shows how the pieces fit.

<mermaid>
flowchart TB
  o["New order<br>(3 items)"] -.-> ch1[["NEW_ORDER"]]
  ch1 -.-> sp["Splitter"]
  sp -.-> cbr["Content-based<br>router"]
  cbr -.-> w["Widget inventory"]
  cbr -.-> g["Gadget inventory"]
  w -.-> ag["Aggregator<br>(correlate by order ID)"]
  g -.-> ag
  ag -.-> cbr2["Content-based<br>router"]
  cbr2 -.-> v[["VALIDATED_ORDER"]]
  cbr2 -.-> i[["INVALID_ORDER"]]
</mermaid>

%%Notation: boxes are pattern components or systems, parallelograms are channels, dashed arrows are asynchronous messages. The two routers make different decisions: the first routes per item, the second routes the aggregated result.%%

How to read it:

- **Split:** one composite order is split into item messages.
- **Route:** each item is routed to the inventory system that owns its category.
- **Aggregate:** the aggregator correlates the item results back into a single order message.
- **Validate:** a content-based router forwards validated orders to VALIDATED_ORDER and everything else to INVALID_ORDER, where an exception process notifies the customer.

In the deck's fuller version of this chain (slide 51), a pub-sub channel plays the *fork*, the aggregator the *join*, and the content-based router the *condition* over the aggregated result; the diagram above draws the fork as the per-item content-based router of slide 49 instead.

{% call example("Tutorial 9 Q3 — multi-item order → inventories → confirmation") %}
Tutorial 9 Q3 poses the same design task: an e-commerce system receives an order with multiple items and must route each item to the correct inventory system, then recombine the results into a single confirmation. The model solution is the same chain — splitter (one message per item), content-based router (route on item type or location), aggregator (combine "confirmed"/"out of stock" replies into one Order Confirmation), which also yields parallel item processing (Tutorial 9 solutions, Q3; cf. L11 slide 49).
{% endcall %}

<box type="warning" seamless>

**Pitfall:** the content-based router's knowledge of recipients is a coupling point — "changes in recipient list ⇒ change in content-based router" (L11 slide 36). If many independently-owned consumers must each decide for themselves, prefer pub-sub with message filters, accepting distributed, reactive filtering (L11 slide 39).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** A new consumer subscribes to your topic with its own filter. What changes in a content-based-router design vs a pub-sub + message-filter design?
<panel type="seamless" minimized header="%%Answer%%">
With a content-based router, the router's configuration must be updated to include the new route. With pub-sub + message filter, nothing upstream changes — the new subscriber just subscribes and applies its filter (Tutorial 9 Q2; L11 slide 39).
</panel>

**Q2.** Why does the deck's scatter-gather example need *two* aggregators?
<panel type="seamless" minimized header="%%Answer%%">
One aggregator reassembles the replies gathered from the participants of the scatter (the per-branch results), and the second combines the branch results into the single overall outcome — two levels of correlation, two aggregators (L11 slides 52–53).
</panel>

**Q3.** (Quiz 4 Q6.) A certificate may be issued only when *attendance confirmed* and *payment settled* are both true. The two facts arrive on separate streams, in either order, each carrying the booking ID. How do you decide when to issue it without assuming cross-stream order?
<panel type="seamless" minimized header="%%Answer%%">
Treat the two facts as **correlated messages**: store the first one by booking ID; when the second fact with the same ID arrives, the aggregator has a complete set and emits the issue-certificate command. The correlation key is the booking ID; neither stream's order is assumed, and per-partition ordering (W9.4) does not help across the two streams (Quiz 4 Q6; L11 slide 48).
</panel>

</panel>

</panel>
<span id="W11-c5"></span>

<panel type="seamless" minimized header="**W11.5 Message transformation ★★**">


**Systems that agree to exchange messages still disagree on formats — someone has to translate, or every pair must.** Message transformation exists because communicating systems use different data formats. (Source: L11 slides 54–55.)

**A message translator encapsulates the conversion between two formats.** It sits between client and service and converts messages from one format into the other, so neither side changes. (Source: L11 slide 55.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-message-translator" trim />
</box>

%%The recording adds the operational argument for putting the translator in the middleware (L11 recording, ~[26:00]): when one application changes its data format, the translation is updated at the middleware — the application on the other side never notices.%%

{% call example("EDI 850 → XML order (L11 slide 56)") %}
An EDI 850 purchase-order record must reach an order-management system that speaks XML over HTTP and uses its own Order object definition. %%EDI stands for *Electronic Data Interchange*, and 850 is the purchase-order document of ANSI X12, the US standard family for electronic business documents — as the slide's own "850-to-PurchaseOrder" label says. (The deck's footnote expands EDI as "Electronic Data Invoice", but the 850 is a purchase order, not an invoice.)%% A message translator (EDI-to-XML, 850-to-PurchaseOrder) — with a channel adapter handling the transport-layer difference — converts the incoming EDI record into the XML document the order system expects, without changing either system.
{% endcall %}

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-channel-adapter" trim />
</box>

**Pairwise translators do not scale to many applications.** With many communicating applications you need one translator per pair, every format change touches all translators involved, and each new application needs translators to all existing ones — so instead produce and consume using a common format. (Source: L11 slide 57.)

**The canonical data model is that common format: an extra level of indirection between every system's own format.** Each system translates its data into the canonical syntax when sending, and translates the canonical syntax into its own format when receiving. (Source: L11 slide 58.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-canonical-data-model" trim />
</box>

The recording's deliberately plain canonical format (L11 recording, ~[105:00]): CSV. Senders translate whatever they have — XML, JSON, raw text — into CSV; the broker knows only CSV and converts it onward, say to a Python dictionary for one consumer and back to XML for another. Each side learns exactly one format instead of every other side's.

<mermaid>
flowchart LR
  subgraph pairwise["Translator between each pair"]
    a1["App A"] --- t1["Xlator"] --- b1["App B"]
    b1 --- t2["Xlator"] --- c1["App C"]
    a1 --- t3["Xlator"] --- c1
  end
  subgraph cdm["Canonical data model"]
    a2["App A"] --- cf(("Canonical<br>format")) --- b2["App B"]
    c2["App C"] --- cf
  end
</mermaid>

%%Notation: boxes are applications, the double-circle is the shared canonical format, and each solid line is a translation hop (mutual, so no arrowheads). On the left every pair needs its own translator; on the right each application translates only to and from one canonical format.%%

How to read it: adding application D costs three new translators on the left but exactly one on the right — one canonical-format adapter. That is the indirection the deck recommends for large integration landscapes.

**Two transformation patterns adjust the *contents* of a message rather than its format.** The content filter removes data items the receiver does not need; the content enricher adds data items the message needs but does not carry, usually by looking them up elsewhere. (Source: eaipatterns.com message-transformation patterns %%— the external catalog the deck links at L11 slide 15%%.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-content-filter" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-content-enricher" trim />
</box>

{% call example("A content enricher (external example)") %}
An OrderItem message arriving at the shipping service carries only `sku` and `quantity`; an enricher looks up the package weight for the SKU from the catalogue and adds `weightKg` before the message reaches the shipping service, which cannot compute postage without it. %%External example — not from the course decks.%%
{% endcall %}

<box type="warning" seamless>

**Pitfall:** letting translators multiply. Translators are dependent on the message formats on both sides, so a format change ripples through every translator that mentions it — the reason the deck concludes "produce and consume using common format!" (L11 slide 57).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Four applications exchange data pairwise today. A fifth joins. How many new translators are needed with pairwise translation vs a canonical data model?
<panel type="seamless" minimized header="%%Answer%%">
Pairwise: one new translator to each existing application — four new translators. Canonical: one adapter to the canonical format (L11 slides 57–58).
</panel>

**Q2.** A downstream service only needs `orderId` and `status`, but the event carries the full customer record. Which pattern applies, and what is its counterpart?
<panel type="seamless" minimized header="%%Answer%%">
A content filter strips the unneeded data items before the message is passed on; its counterpart, the content enricher, adds missing data items instead (eaipatterns.com message-transformation patterns %%— linked from L11 slide 15%%).
</panel>

</panel>

</panel>
<span id="W11-c6"></span>

<panel type="seamless" minimized header="**W11.6 Message endpoints ★★**">


**The messaging system does the routing, but *your* application still needs code to connect to it — that code is the endpoint.** A message endpoint is the interface between an application and a messaging system: it encapsulates the messaging APIs (e.g. JMS) and is custom to both the application and the messaging system's client API, so the rest of the application knows little about message formats, channels, or other messaging details. (Source: L11 slide 60.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-message-endpoint" trim />
</box>

**Endpoints are channel-specific and one-directional.** One endpoint instance either sends or receives — not both — and a single application uses multiple endpoints to interface with multiple channels. In JMS the two endpoint types are MessageProducer (sending) and MessageConsumer (receiving). (Source: L11 slides 60–61.)

**A receiving endpoint either polls or reacts.** A polling consumer proactively reads messages when it is ready to consume them (e.g. RabbitMQ's `basic.get`); an event-driven consumer processes a message reactively on arrival (e.g. `basic.consume`). A related concept is throttling: the application controls the rate at which it consumes messages. (Source: L11 slides 61–63.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-polling-consumer" trim />
</box>

The recording plays out the polling loop (L11 recording, ~[108:00]): the application asks "any message?" — the broker answers "no" — again "no" — until finally "yes", and only then does processing begin. The event-driven consumer inverts this: register readiness once, and each message is handed over as it lands.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-event-driven-consumer" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-throttling" trim />
</box>

{% call example("Growing queue in front of a slow filter (Quiz 2 Q7)") %}
An image-processing system built as a pipe-and-filter architecture reveals a CPU-heavy resize filter with a growing job queue in front of it while other components sit idle. The queue is a channel; each resize filter is a consumer endpoint reading from it. Adding *extra resize filters consuming from the same job queue* — competing consumers polling the same channel — scales exactly the overloaded stage instead of the whole system (Quiz 2 Q7; cf. the Messaging Endpoints pattern map, L11 slide 15).
{% endcall %}

<box type="warning" seamless>

**Pitfall:** letting one endpoint instance both send and receive, or sharing one endpoint across several channels. Endpoints are channel-specific and single-direction; violating that couples unrelated message flows inside one component (L11 slides 60–61).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Your batch job should only consume messages when the database has spare capacity. Which consumer type fits, and which extra concept?
<panel type="seamless" minimized header="%%Answer%%">
A polling consumer — it proactively reads when *it* is ready — combined with throttling to control the consumption rate (L11 slides 61–62).
</panel>

</panel>

</panel>
<span id="W11-c7"></span>

<panel type="seamless" minimized header="**W11.7 Asynchronicity in the request-reply pattern ★**">


**"Returned immediately" is not the same as "asynchronous" — what matters is whether the sender still depends on the reply to finish its work.** The lecture opens by recapping exactly this distinction from Week 10 (Source: L11 slide 3; L13 slide 5), and Tutorial 8 Q1 examines it.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-request-reply" trim />
</box>

**Request-reply can be implemented synchronously or asynchronously, and only the dependency decides.** In the synchronous form the sender blocks until the reply arrives. Over messaging, the requestor sends the request (with a return address), releases the thread, and matches replies by correlation ID — the interaction is asynchronous at the transport level. But a sender that must still *use* the reply to complete its operation has only *hidden* the wait. (Source: L11 slides 20–25.)

**The deck's shorthand for the hidden wait is pseudo-asynchronous.** The system behaves synchronously in terms of dependency, even though control returned to the caller early.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-11.md#def-pseudo-asynchronous" trim />
</box>

{% call example("Tutorial 8 Q1 — Module A↔B vs Module C↔D") %}
Scenario 1: "Module A calls Module B via an HTTP API using a background process and immediately returns control to its own caller, though it will eventually depend on B's HTTP response to complete the overall operation." At first glance asynchronous — but because A eventually depends on B's response to complete the operation, it is *pseudo-asynchronous*: synchronous in terms of dependency. Scenario 2: "Module C publishes a message to a queue consumed by Module D and immediately returns; the result is observed later via a separate notification." Here C does not depend on an immediate response from D — producer and consumer operate independently — so this is truly asynchronous (Tutorial 8 sheet and solutions, Q1).
{% endcall %}

The two diagrams below contrast the interactions; read the difference in what each sender does *after* handing off its work.

**Scenario 1 — Module A↔B (pseudo-asynchronous):**

<mermaid>
sequenceDiagram
  participant caller as A's caller
  participant A as Module A
  participant B as Module B
  caller->>A: start operation
  A--)caller: return immediately
  Note over A: background process calls B...
  A->>B: HTTP request
  B-->>A: response (needed to finish)
  Note over A: completes operation later
</mermaid>

**Scenario 2 — Module C↔D (truly asynchronous):**

<mermaid>
sequenceDiagram
  participant C as Module C
  participant q as queue
  participant D as Module D
  C--)q: message
  Note over C: returns, independent of D
  q--)D: deliver message
  Note over D: result observed later via separate notification
</mermaid>

%%Notation: in both diagrams solid arrows are synchronous calls, arrows with open heads are asynchronous messages, the dashed arrow with a closed head is the awaited HTTP reply, and notes mark where each module continues its own work. A's timeline still bends around B's response; C's does not.%%

How to read it: both A and C "return immediately", but A's overall operation cannot complete until B answers, while C never waits for D at all — the notification that carries the result arrives whenever it arrives (Tutorial 8 solutions, Q1).

<box type="warning" seamless>

**Pitfall:** classifying an interaction by its technology instead of its dependency. A queue can carry a pseudo-asynchronous request-reply, and HTTP can be used fire-and-forget. Ask what the sender waits for, not which protocol carries the bytes (Tutorial 9 Q1 hint; Tutorial 8 solutions, Q1).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Research asks Archive to locate an old dataset; the search may take hours; Research must continue other work and later associate each reply with the correct search. Which design fits, and which W11.3 mechanism makes it work?
<panel type="seamless" minimized header="%%Answer%%">
Send an asynchronous query to Archive and include a request identifier that Archive returns with its reply — the correlation identifier (Quiz 4 Q7; W11.3, L11 slides 24–25).
</panel>

**Q2.** A service receives a request, spins up a worker, returns a job ID, and its *caller's* workflow cannot proceed until the worker's result is merged back. Truly asynchronous or pseudo-asynchronous?
<panel type="seamless" minimized header="%%Answer%%">
Pseudo-asynchronous: control returned early, but the caller still depends on the reply to complete the operation, so the system behaves synchronously in terms of dependency (Tutorial 8 solutions, Q1).
</panel>

</panel>

<box type="info" seamless>

##### Section summary

* **Messaging solves heterogeneous integration**: a broker connects applications that differ in platform, language and format, and buffers messages so the network's failures stay inside the messaging layer (W11.1).
* **Construct messages by intent** — command, document, event — and carry them on channels that match the delivery shape: point-to-point for exactly one consumer, pub-sub for all subscribers (W11.2–W11.3).
* **Route and transform messages with named patterns** — content-based router, message filter, splitter, aggregator, scatter-gather, translator, canonical data model — so senders stay decoupled from recipients (W11.4–W11.5).
* **Connect applications through endpoints** (polling vs event-driven), and judge "asynchronous" by dependency, not by technology (W11.6–W11.7).
</box>

</div>

</panel>
## Key terms

| Term | Definition | Unit |
|---|---|---|
| Enterprise Integration Patterns (EIP) | Vendor-independent catalogue of 65 integration patterns in six categories | [W11.1](#W11-c1) |
| Message broker (MOM) | Middleware that passes and buffers messages between components that need not know each other | [W11.1](#W11-c1) |
| Message construction | Choosing what a message contains and what the receiver should do: command, document or event payload | [W11.2](#W11-c2) |
| Command message | Payload telling the receiver to perform an action | [W11.2](#W11-c2) |
| Document message | Payload giving the receiver data to process at its discretion | [W11.2](#W11-c2) |
| Event message | Payload notifying the receiver that something has happened | [W11.2](#W11-c2) |
| Message channel | A conduit (queue or topic) connecting collaborating senders and receivers; one-directional | [W11.3](#W11-c3) |
| Point-to-point channel | Channel on which exactly one consumer consumes each message | [W11.3](#W11-c3) |
| Publish-subscribe channel | A channel where every message published to a topic is received by all its subscribers | [W11.3](#W11-c3) |
| Return address | Part of a request telling the replier where to send the reply | [W11.3](#W11-c3) |
| Correlation identifier | A token copied from request to reply so the requestor can match them | [W11.3](#W11-c3) |
| Request-reply chaining | Keeping correlation IDs across a chain of request-reply exchanges, to retrace the path | [W11.3](#W11-c3) |
| Invalid message channel | Channel receiving messages a receiver cannot interpret | [W11.3](#W11-c3) |
| Dead letter channel (DLQ) | A channel holding messages that could not be delivered or processed, for later redrive | [W11.3](#W11-c3) |
| Redrive | Moving messages from the DLQ back to a queue for another attempt, once the cause is fixed | [W11.3](#W11-c3) |
| Data type channel | One channel per data type, so the receiver knows the type from the channel | [W11.3](#W11-c3) |
| Message router | Component that consumes messages from one channel and reinserts them into others by conditions | [W11.4](#W11-c4) |
| Content-based router | A router that sends each message to a channel chosen from the message's content | [W11.4](#W11-c4) |
| Message filter | A content-based router with one output channel that discards non-matching messages | [W11.4](#W11-c4) |
| Context-based router | Router deciding the destination from context (load balancing, failover), not content | [W11.4](#W11-c4) |
| Splitter | Turns one message into multiple per-part messages | [W11.4](#W11-c4) |
| Aggregator | Collects correlated messages and publishes one aggregated message | [W11.4](#W11-c4) |
| Scatter-gather | Broadcasts one request to many participants concurrently and reassembles their replies | [W11.4](#W11-c4) |
| Pipes and filters | Single-purpose processing steps (filters) chained by channels (pipes) | [W11.4](#W11-c4) |
| Message translator | A component encapsulating the conversion of messages between two formats | [W11.5](#W11-c5) |
| Channel adapter | Converts between transport layers so a component works in a different context | [W11.5](#W11-c5) |
| Canonical data model | A common intermediate format every system translates to and from | [W11.5](#W11-c5) |
| Content filter | Transformation that removes data items the receiver does not need | [W11.5](#W11-c5) |
| Content enricher | Transformation that adds data items the message needs but does not carry | [W11.5](#W11-c5) |
| Message endpoint | The interface between an application and a messaging system, encapsulating its API | [W11.6](#W11-c6) |
| Polling consumer | Consumer that proactively reads messages when it is ready | [W11.6](#W11-c6) |
| Event-driven consumer | Consumer that reacts to a message's arrival | [W11.6](#W11-c6) |
| Throttling | Receiver-side control on the message consumption rate | [W11.6](#W11-c6) |
| Request-reply | Async messaging pattern using a return address and correlation identifier instead of blocking | [W11.7](#W11-c7) |
| Pseudo-asynchronous | Control returns early but the caller still depends on the reply — synchronous in dependency | [W11.7](#W11-c7) |

## Connections

| Concept | Lecture deck | Tutorial | Other weeks |
|---|---|---|---|
| Message vs event intent | L11 slides 3, 17 | T8 Q1 | W9 (events, EDA); W10 (message vs event) |
| Broker / MOM | L11 slides 5–13 | — | W5 (cloud-native messaging services); W10 (async communication) |
| Payload kinds (command/document/event) | L11 slides 16–18 | — | Quiz 4 Q1 |
| Channels, return address, correlation ID | L11 slides 19–30 | T8 Q1; T9 Q4 (DLQ) | W10 (persistent communication) |
| Pub-sub channels | L11 slides 31–32 | T8 Q2 (scenario 2) | W9 (pub-sub dispatch); W10 (pub-sub) |
| Routing patterns | L11 slides 33–53 | T9 Q2, Q3 | W6 (pipe-and-filter style); Quiz 2 Q7–Q8 |
| Transformation | L11 slides 54–58 | — | W8 (bounded contexts ↔ canonical data model) |
| Endpoints | L11 slides 59–63 | — | W12 (scaling consumers) |
| Request-reply asynchronicity | L11 slides 3, 20–26 | T8 Q1 | W10 (sync/async taxonomy); Quiz 4 Q7 |

## Summary

**Key takeaways:**

* **Enterprise integration uses a message broker** because applications differ in platform, language and format, and a broker buffers messages while decoupling the parties (W11.1).
* **A message's payload kind — command, document or event — encodes its intent**, and choosing it wrong makes receivers do the wrong thing (W11.2).
* **Channels shape delivery**: one-directional, point-to-point vs pub-sub, with return address and correlation identifier for request-reply and dead-letter channels for failures (W11.3).
* **Routers move routing knowledge out of senders**, and composing splitter → router → aggregator yields pipes-and-filters flows (W11.4).
* **Translators and the canonical data model reconcile formats** without pairwise explosion; content filter and enricher trim or complete payloads (W11.5).
* **Applications meet messaging systems through one-directional, channel-specific endpoints**, consuming by polling or by event (W11.6).
* **Asynchronicity is about dependency, not technology**: a caller that still needs the reply is only pseudo-asynchronous (W11.7).

**Key terms:** see the table above — each row links back to the unit that introduces the term.

%%Next: Week 12 asks what happens when load grows — scalability — and reuses this week's queues and consumers as buffers and scaling units. See [Week 12 — Scalability]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html).%%

## Further reading

* Enterprise Integration Patterns catalogue — <http://www.eaipatterns.com> (the 65-pattern map on L11 slides 14–15)
* Oracle: Introduction to the Java Message Service — <https://www.oracle.com/technical-resources/articles/java/intro-java-message-service.html> (L11 slide 12)
* Amazon SQS dead-letter queues — <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html> (L11 slide 28)
* Simplifying pub-sub messaging with Amazon SNS message filtering — <https://aws.amazon.com/blogs/compute/simplify-pubsub-messaging-with-amazon-sns-message-filtering/> (L11 slides 41–45)
