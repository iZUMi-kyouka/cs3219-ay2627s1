{# Definitions for week-09. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-09.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable. #}

<span id="def-event">

**Event** — a recording of something that has happened within the scope of the business system: a fact about a state change. Events act as both data and as a means of asynchronous communication between services.
%%(Source: L9 slides 5–6.)%%

</span>

<span id="def-initiating-event">

**Initiating event** — an event that originates from an end user and typically kicks off a business process.
%%(Source: L9 slide 7.)%%

</span>

<span id="def-derived-event">

**Derived event** — an internal event generated in response to an initiating event: a software component responds to the initiating event and in turn broadcasts what it did to the rest of the system, within the scope of that initiating event.
%%(Source: L9 slide 8.)%%

</span>

<span id="def-command">

**Command** — a request for an action to be performed, expressed as intent in the imperative mood (e.g., `ChargeCard`) and sent to a specific receiver; it changes application state and returns no data.
%%(Source: L8 slides 4, 25; L9 slide 9.)%%

</span>

<span id="def-query">

**Query** — a request that asks for the current state and needs a reply, but does not change state (e.g., `GetBalance`).
%%(Source: L9 slide 9.)%%

</span>

<span id="def-event-notification">

**Event notification** — an event in its "something happened" role: it carries only a small amount of data, and consumers that need more must obtain it from the source. One of the four views of an event.
%%(Source: L9 slide 5, from Fowler; Quiz 4 Q3.)%%

</span>

<span id="def-event-carried-state-transfer">

**Event-carried state transfer** — an event in its "here is the data" role: the event carries the data consumers need, so they can work without calling the producer back. The other content-side view of an event.
%%(Source: L9 slide 5, from Fowler.)%%

</span>

<span id="def-fire-and-forget">

**Fire-and-forget communication** — asynchronous communication in which the sender broadcasts information and moves on: it does not wait for a response, nor does it care whether the other components are available.
%%(Source: L9 slide 13.)%%

</span>

<span id="def-event-driven-architecture">

**Event-driven architecture (EDA)** — a software architectural design pattern in which decoupled applications (or components) asynchronously communicate by issuing and consuming events via an event broker; communication is through events, and events drive the system.
%%(Source: L9 slides 20, 23.)%%

</span>

<span id="def-event-broker">

**Event broker** (aka event bus) — an intermediary that receives events from producers, holds them (in queues or partitions), and provides them to consumers that subscribe to topics of interest. It facilitates loose coupling: producers and consumers need not know each other's identity or location.
%%(Source: L9 slides 21–23.)%%

</span>

<span id="def-pub-sub">

**Publish–subscribe (pub/sub)** — a messaging pattern following the event-driven structure: event producers are publishers, event consumers are subscribers, and a broker delivers published events to every subscriber of the topic (e.g., Kafka pub/sub).
%%(Source: L9 slide 24.)%%

</span>

<span id="def-event-stream">

**Event stream** — a partitioned, append-only sequence of related events published by one producing microservice, the owner of every event on that stream; consumers read it sequentially using offsets.
%%(Source: L9 slides 32, 35–38.)%%

</span>

<span id="def-event-driven-microservice">

**Event-driven microservice** — a small application built to fulfill a specific bounded context that communicates by consuming events from one or more input event streams and producing events to other output event streams.
%%(Source: L9 slides 32, 42.)%%

</span>

<span id="def-event-sourcing">

**Event sourcing** — a storage approach in which events are the source of truth: state is never stored directly, but reconstructed by replaying the stored events in order.
%%(Source: L9 slide 5; L8 slides 17–19.)%%

</span>

<span id="def-cqrs">

**CQRS** (command–query responsibility segregation) — a pattern that keeps a separate model for writes (commands) and reads (queries). It does not always need events or event sourcing — they are just mostly used together.
%%(Source: L9 slides 2, 5; L8 slides 22–26.)%%

</span>

<span id="def-temporal-decoupling">

**Temporal coupling** — the dependency between components that must be up at the same time for communication to work. Fire-and-forget communication removes it: producer and consumer do not need to be available simultaneously — the removal is often called temporal decoupling.
%%(Source: L9 slide 17; Quiz 4 Q4.)%%

</span>

<span id="def-latency">

**Latency** — the delay between sending a request and receiving (or completing) its response. Synchronous communication creates latency that slows the system, because the sender waits.
%%(Source: L9 slide 25; Quiz 2 Q1; Quiz 3 Q10.)%%

</span>

<span id="def-event-key">

**Event key** — the key half of a key–value event: it identifies and routes the event, supports aggregation on the unique ID, and decides partition placement (all events produced with a given key are written to the same partition). By key, events come in three types: **unkeyed** (no key — a singular statement of fact), **entity** (keyed on the entity's unique ID — a continual history of that entity's state), and **keyed** (a key that does not represent an entity, used to guarantee data locality within a partition).
%%(Source: L9 slide 10; L10 slide 23; Quiz 4 Q9.)%%

</span>

<span id="def-immutability">

**Immutability (of event data)** — published events cannot be modified: there is no mechanism that can change event data once it is published; the only way to alter previous data is to publish a new event with the updated data.
%%(Source: L9 slide 37; L8 slide 18.)%%

</span>

<span id="def-offset">

**Offset** — the auto-incrementing index-ID of the last event a consumer has read in a partition. To consume, a service seeks to its offset, scans sequentially in publication order, and periodically records its new offset in the partition.
%%(Source: L9 slides 35–37; Quiz 4 Q8–Q9.)%%

</span>

<span id="def-partition">

**Partition** — one substream of an event stream: an append-only log into which the broker places events (by key). Data in a partition is strictly ordered and served in exactly the published order; partitions enable parallel reading and writing, and per-partition ordering says nothing about processing order across partitions.
%%(Source: L9 slides 37–39; Quiz 4 Q8–Q9.)%%

</span>

<span id="def-consumer-group">

**Consumer group** — a set of load-balanced consumers that share the partitions of a stream between them, so the group's consumption capacity scales with its members; rate limits are applied to producers, consumers, and groups.
%%(Source: L9 slides 39–40.)%%

</span>

<span id="def-infinite-retention">

**Infinite retention** — the broker property that an event stream retains its events for an infinite period of time, if so configured; it is foundational for maintaining state in an event stream.
%%(Source: L9 slide 38; Quiz 4 Q4 (a seven-day retention window).)%%

</span>

<span id="def-replayability">

**Replayability** — the broker property that any consumer can read whatever data it requires from the beginning of the stream; it provides the basis for the single source of truth and for communicating state between microservices.
%%(Source: L9 slide 38.)%%

</span>
