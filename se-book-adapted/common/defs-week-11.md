{# Definitions for week-11. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-11.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable. #}

<span id="def-message-construction">

**Message construction** is the choice of what a message should contain and what the receiver should do with it. The three payload kinds are the **command message** (tells the receiver to do something), the **document message** (gives the receiver data to process) and the **event message** (notifies the receiver that something has happened).

(Sources: L11 slides 16–18; Enterprise Integration Patterns, eaipatterns.com.)

</span>

<span id="def-pipes-and-filters">

**Pipes and filters** is a message-flow pattern that connects single-purpose processing steps (*filters*) with message channels (*pipes*): each filter consumes a message, performs one transformation or routing decision, and passes the result to the next filter. A splitter feeding a content-based router feeding an aggregator is a pipes-and-filters flow.

(Sources: L11 slides 15, 46–51; Enterprise Integration Patterns, eaipatterns.com.)

</span>

<span id="def-content-filter">

**Content filter** is a message-transformation pattern that removes data items the receiver does not need from a message before passing it on, so that each message carries only what its consumer requires.

(Sources: L11 slide 15 (pattern map); Enterprise Integration Patterns, eaipatterns.com.)

</span>

<span id="def-content-enricher">

**Content enricher** is a message-transformation pattern that adds data items a message needs but does not carry, typically by looking them up from another source, before passing the message on.

(Sources: L11 slide 15 (pattern map); Enterprise Integration Patterns, eaipatterns.com.)

</span>

<span id="def-message-router">

**Message router** — a component that consumes messages from one message channel and reinserts them into different message channels depending on a set of conditions, encapsulating the routing logic so the sender's workload is reduced. Simple routers connect one inbound channel to one or more outbound channels; composed routers combine several simple routers into more complex flows.

(Sources: L11 slides 34–35.)

</span>

<span id="def-content-based-router">

**Content-based router** — a router that examines the message content and routes each message onto a channel chosen from the data contained in it, decoupling sender from receiver. It must know all possible recipients and their capabilities, so a change in the recipient list means a change in the router.

(Sources: L11 slide 36.)

</span>

<span id="def-message-filter">

**Message filter** — a content-based router with a single output channel: messages whose content matches the filter's criteria are routed on; the rest are discarded.

(Sources: L11 slide 37.)

</span>

<span id="def-context-based-router">

**Context-based router** — a router that decides the message's destination from the *context* rather than the message content — commonly for load balancing, testing, or failover (e.g., re-routing messages to another processing component when one fails).

(Sources: L11 slide 40.)

</span>

<span id="def-splitter">

**Splitter** — a message-flow pattern that turns a single message into multiple messages, one per part (e.g., one order message with N items becomes N order-item messages, each routable separately); it is not a router itself.

(Sources: L11 slide 47.)

</span>

<span id="def-aggregator">

**Aggregator** — a stateful filter that receives a stream of messages, identifies the correlated ones (e.g., by order ID), and — once a complete set of correlated messages has arrived — collects the information from each and publishes a single aggregated message to the output channel.

(Sources: L11 slide 48.)

</span>

<span id="def-scatter-gather">

**Scatter-gather** — a routing pattern that broadcasts one message to a number of participants concurrently and reassembles (aggregates) their replies into a single message; ideal for requesting responses from multiple parties, e.g. quotes from all suppliers of an out-of-stock item.

(Sources: L11 slide 52.)

</span>

<span id="def-message-translator">

**Message translator** — a component that encapsulates the conversion of messages between two data formats, sitting between client and service so neither side has to change.

(Sources: L11 slides 55–56.)

</span>

<span id="def-channel-adapter">

**Channel adapter** — a pattern that converts between different transport layers: an adapter converts the interface of a component into another interface so it can be used in a different context (e.g., the transport-layer adapter beside an EDI-to-XML translator).

(Sources: L11 slide 56.)

</span>

<span id="def-canonical-data-model">

**Canonical data model** — a common intermediate format that provides an additional level of indirection between applications' individual data formats: each system translates its data into the canonical syntax when sending and out of it when receiving, replacing the unmanageable one-translator-per-pair explosion with one adapter per system.

(Sources: L11 slides 57–58.)

</span>

<span id="def-message-endpoint">

**Message endpoint** — the interface between an application and a messaging system: it encapsulates the messaging APIs (e.g., JMS) and is custom to both the application and the messaging system's client API, so the rest of the application knows little about message formats, channels, or other messaging details. Endpoints are channel-specific and one-directional — one instance either sends or receives, not both.

(Sources: L11 slides 60–61.)

</span>

<span id="def-polling-consumer">

**Polling consumer** — a receiving endpoint that proactively reads messages when *it* is ready to consume them (e.g., RabbitMQ's `basic.get`).

(Sources: L11 slides 61–62.)

</span>

<span id="def-event-driven-consumer">

**Event-driven consumer** — a receiving endpoint that reacts to a message's arrival, processing it as an event that triggers the receiver into action (e.g., RabbitMQ's `basic.consume`).

(Sources: L11 slide 63.)

</span>

<span id="def-throttling">

**Throttling** — a receiver-side control on the rate at which an application consumes messages, so consumption matches the application's current capacity.

(Sources: L11 slide 61.)

</span>

<span id="def-pseudo-asynchronous">

**Pseudo-asynchronous** — an interaction that returns control to the caller immediately but is still synchronous in terms of *dependency*: the caller cannot complete its overall operation until the reply arrives (e.g., Module A returning at once while a background process waits on B's HTTP response it still needs). Judge asynchronicity by dependency, not by technology.

(Sources: L11 slides 3, 20–25; Tutorial 8 Q1.)

</span>

<span id="def-request-reply">

**Request-reply** is an asynchronous messaging pattern in which a requestor sends a request message on one channel — carrying a *return address* saying where the reply should go — and later matches the reply message to the request using a *correlation identifier*, instead of blocking on a synchronous call.

(Sources: L11 slides 20–25; Enterprise Integration Patterns, eaipatterns.com.)

</span>

<span id="def-enterprise-integration-patterns">

**Enterprise Integration Patterns (EIP)** — a technology-independent catalogue of 65 solutions to common integration problems (Hohpe & Woolf), organised in six categories: message construction, message channels, message routing, message transformation, message endpoints, and system management. EIP give developers and architects a shared, vendor-independent vocabulary for describing integrations.

(Sources: L11 slides 8, 14–15; Enterprise Integration Patterns, eaipatterns.com.)

</span>

<span id="def-message-broker">

**Message broker** (aka MOM — message-oriented middleware) — software that provides messaging capabilities so applications can exchange messages without knowing each other's location, platform, or implementation: it passes information between components while minimising how much they need to know about each other, buffers incoming messages, and shields applications from many operating-system and network complexities.

(Sources: L11 slides 11, 64.)

</span>

<span id="def-command-message">

**Command message** — a message whose payload tells the receiver to perform some action (e.g., `ReserveEquipment` to the Reservation service); a reply is typically expected (request-reply).

(Sources: L11 slides 16–18; Quiz 4 Q1.)

</span>

<span id="def-document-message">

**Document message** — a message whose payload gives the receiver data to process at its own discretion; no reply is expected (e.g., the purchase-order document translated to XML for the order-management system).

(Sources: L11 slides 16–18, 56.)

</span>

<span id="def-event-message">

**Event message** — a message whose payload notifies the receiver that something has happened — a completed fact the receiver may react to (e.g., `EquipmentReserved`, published only after a reservation succeeds).

(Sources: L11 slides 16–18; Quiz 4 Q1.)

</span>

<span id="def-message-channel">

**Message channel** — the conduit that connects collaborating senders and receivers and carries messages between them: a queue (point-to-point — exactly one consumer per message) or a topic (publish–subscribe — all subscribers). A channel transmits messages in one direction, so a two-way exchange needs two channels.

(Sources: L11 slides 19–20, 31–32.)

</span>

<span id="def-point-to-point-channel">

**Point-to-point channel** — a channel (a queue) on which exactly one consumer consumes each message, even if several consumers listen on it — the shape that lets competing consumers share the load.

(Sources: L11 slides 20, 31–32; L10 slide 24.)

</span>

<span id="def-publish-subscribe-channel">

**Publish–subscribe channel** — a channel (a topic) on which any message published is immediately received by all subscribers of the topic; used when multiple parties are interested in the same messages. A pub-sub *request–response* variant uses a pub-sub channel for the requests but a point-to-point channel for the responses.

(Sources: L11 slides 31–32.)

</span>

<span id="def-return-address">

**Return address** — the part of a request message that tells the replier where to send the reply (e.g., the request's `Reply to: jms/ReplyQueue` field).

(Sources: L11 slides 22–23.)

</span>

<span id="def-correlation-identifier">

**Correlation identifier** — a token the requestor assigns as a unique request ID (different from all currently outstanding requests) and the replier copies into the reply, so the requestor can match each reply to the request that caused it.

(Sources: L11 slides 24–25; Quiz 4 Q7.)

</span>

<span id="def-request-reply-chaining">

**Request-reply chaining** — keeping the correlation of a chain of request-reply exchanges (a request causes a reply that is itself another request, and so on), so the path of messages can be retraced from the latest reply back to the original request — e.g., for auditing.

(Sources: L11 slide 26.)

</span>

<span id="def-invalid-message-channel">

**Invalid message channel** — a channel that receives messages a receiver cannot interpret, so erroneous messages are moved aside instead of blocking or crashing the receiver.

(Sources: L11 slide 27.)

</span>

<span id="def-dead-letter-channel">

**Dead letter channel** (dead-letter queue, DLQ) — a channel that receives messages the messaging system cannot deliver or that repeatedly fail processing: instead of retrying failing messages until they expire, move them to the dead-letter queue after a few processing attempts.

(Sources: L11 slide 27; Tutorial 9 Q4.)

</span>

<span id="def-redrive">

**Redrive** — moving messages from a dead-letter queue back to the source queue (or to another configured queue) for another processing attempt, once the cause of the failures has been found and fixed. (AWS SQS's term for managing the lifecycle of unconsumed messages.)

(Sources: L11 slide 28; Tutorial 9 Q4.)

</span>

<span id="def-data-type-channel">

**Data type channel** — one channel per data type: all messages on a given channel contain the same type of data, so the receiver knows the type from the channel a message arrived on; the sender, knowing the type, selects the appropriate channel.

(Sources: L11 slide 29.)

</span>
