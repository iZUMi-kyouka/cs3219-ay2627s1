{# Definitions for week-10. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-10.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable. #}

<span id="def-synchronous-communication">

**Synchronous communication** (request–reply) — components or services exchange information at the same time: the sender sends a request and waits for the receiver's response before doing anything else. It couples sender and receiver tightly, adds connection overhead, and leaves failure handling to the sender.
%%(Source: L10 slide 5.)%%

</span>

<span id="def-asynchronous-communication">

**Asynchronous communication** — communication that has a lag between when a message is sent and when the receiver receives, interprets, or responds to it. It enables the independent functioning of sender and receiver and one-to-many sends, coupling them loosely — at the price of needing notification handling.
%%(Source: L10 slide 5.)%%

</span>

<span id="def-message">

**Message** — a construct carrying a *request to be executed* by another service: a command (perform some action) or a query (get some data), sent point-to-point to exactly one receiver. Intent — not wire format — is what distinguishes a message from an event.
%%(Source: L10 slides 12–13.)%%

</span>

<span id="def-topic">

**Topic** — a broker channel that enables one-to-many communication, reaching multiple subscribers simultaneously. Within a single partition, processing order is maintained through a unique offset per event; with multiple partitions, receive order may differ from send order.
%%(Source: L10 slide 14.)%%

</span>

<span id="def-queue">

**Queue** — a broker channel that buffers messages for a single receiver: it follows first-in-first-out, each message is consumed by exactly one receiver, and messages are not copied to other receivers.
%%(Source: L10 slides 14, 24.)%%

</span>

<span id="def-persistent-communication">

**Persistent communication** (aka store-and-forward delivery) — messages are stored at each intermediate hop along the way until the next node is ready to take delivery; the message survives sender or receiver inactivity. E.g., email systems.
%%(Source: L10 slide 32.)%%

</span>

<span id="def-transient-communication">

**Transient communication** — messages are buffered only for small periods of time (as long as the sending/receiving applications are executing); if the message cannot be delivered or the next host is down, it is discarded. Sender and receiver must both be active. E.g., a typical network router (general TCP/IP communication).
%%(Source: L10 slide 32.)%%

</span>

<span id="def-async-request-reply">

**Asynchronous request–reply** — a pattern for long-running work kept behind a request–reply facade: the API accepts the request, queues it for a background worker, and answers immediately with **HTTP 202 (Accepted)** plus a link to a *status endpoint*; the client polls the status endpoint (202 while pending), and on completion receives **302 (Found)** redirecting to the resource. An invalid request is rejected immediately (e.g. HTTP 400 Bad Request).
%%(Source: L10 slides 7–8; Quiz 4 Q7.)%%

</span>

<span id="def-kafka">

**Kafka** — a distributed message streaming platform that uses publish–subscribe, developed at LinkedIn and donated to the Apache Foundation: producers publish events to named topics, topics are broken into partitions spread over a cluster of brokers that deliver messages to consumers, and brokers can be added without downtime — horizontal scaling.
%%(Source: L10 slides 22–23.)%%

</span>

<span id="def-amqp">

**AMQP** (Advanced Message Queuing Protocol) — an open-standard asynchronous messaging protocol enabling conforming client applications to communicate with conforming messaging middleware brokers: messages are published to exchanges, which route copies to queues, from which consumers receive or fetch them.
%%(Source: L10 slides 25–27.)%%

</span>

<span id="def-exchange">

**Exchange** (AMQP/RabbitMQ) — the routing step of the AMQP model: it receives published messages and routes copies into the queues bound to it, matching message attributes (e.g., the routing key) against each queue's binding. Exchange types: **direct** (exact key match), **fanout** (all bound queues), **topic** (wildcard match, e.g. `us.#` matches `us.stocks`), **header** (route on message headers).
%%(Source: L10 slides 26, 28–29.)%%

</span>

<span id="def-protocol">

**Protocol** — a set of rules for communication (e.g., AMQP). A **standard** is a protocol approved by an authority (the slide names IEEE, W3C) and adopted by many parties — protocols can also be non-standard (e.g., JMS). A **specification** is the formally written form of a protocol that vendors follow (Java provides the JMS specification). An **implementation** is a vendor's working mechanism for using the protocol (e.g., ActiveMQ, Kafka).
%%(Source: L10 slide 10.)%%

</span>
