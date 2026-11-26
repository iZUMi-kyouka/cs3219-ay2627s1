{# Definitions for week-08. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-08.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable. #}

<span id="def-domain">

**Domain** — the problem space that a business occupies and provides a solution for. E.g., the FoC platform's domain is peer-to-peer campus errands.
%%(Source: L8 slides 2–3.)%%

</span>

<span id="def-subdomain">

**Subdomain** — a component of the main domain, belonging to the problem space, that focuses on one specific set of responsibilities and typically reflects part of the business organization's structure. E.g., errand fulfillment, closed credit economy, campus vendors, identity.
%%(Source: L8 slide 3.)%%

</span>

<span id="def-bounded-context">

**Bounded context** — a highly cohesive boundary that includes the input, output, events, requirements, processes, and data models relevant to one subdomain. It belongs to the solution space; ideally it aligns completely with its subdomain, but it is designed, not discovered.
%%(Source: L8 slide 3.)%%

</span>

<span id="def-ubiquitous-language">

**Ubiquitous language** — a shared vocabulary between domain experts and developers, valid inside a bounded context. The same word can mean different things in different contexts: *Student* in the Identity context is an account holder with a verified email and password, while in the Order context a student is a requestor or a courier.
%%(Source: L8 slide 3.)%%

</span>

<span id="def-event-storming">

**Event storming** — a lightweight workshop practice for discovering microservices: identify the domain events that record state changes, then the commands that cause them, the aggregates the commands work on, and the policies that react to events.
%%(Source: L8 slides 2, 4.)%%

</span>

<span id="def-database-per-service">

**Database-server-per-service pattern** — each microservice has its own database server that no other service touches directly. It enforces loose coupling, allows scaling at the database level, and lets each service choose or replace its database technology freely.
%%(Source: L8 slides 6, 8.)%%

</span>

<span id="def-shared-database">

**Shared database pattern** — multiple services read and write one common database. It is an antipattern for microservices: it creates development-time coupling (schema changes need team coordination), runtime interference (services overwrite each other's data), and forces one database technology on all services.
%%(Source: L8 slide 10.)%%

</span>

<span id="def-data-lake">

**Data lake** — a read-only, queryable data sink holding (copies of) data from several microservices, indexed for queryability. Owner services stream their data-change events into it via a messaging infrastructure, so cross-service queries never touch the services' own databases.
%%(Source: L8 slide 11.)%%

</span>

<span id="def-saga">

**Saga** — a sequence of local transactions in which each service performs its operation and initiates the next step through events or messages. Every step registers a compensating action (recorded on a *routing slip* — the coordination record that travels with the work and lists each remaining step and its undo) that is executed if a later step fails, bringing the system to a reasonably compensated state — not necessarily the original one.
%%(Source: L8 slides 13–15.)%%

</span>

<span id="def-event-sourcing">

**Event sourcing** — a data storage pattern where state changes are stored as immutable events in an append-only log, and the current state is derived by applying the historical events, in sequence, to an initial state or snapshot.
%%(Source: L8 slides 17–19.)%%

</span>

<span id="def-cqrs">

**CQRS** (command–query responsibility segregation) — a pattern that separates the write path (commands, which change application state and return no data) from the read path (queries, which return data and change nothing), giving each its own model and often its own database. CQRS does not require events or event sourcing; they are just mostly used together.
%%(Source: L8 slides 22, 25–26; L9 slide 2.)%%

</span>

<span id="def-materialized-view">

**Materialized view** — a view (table) that contains the results of some predefined query, precomputed and stored. It is a performance optimization: instead of computing a query when a user needs data, the answer is stored and kept up to date.
%%(Source: L8 slides 23–24.)%%

</span>

<span id="def-api-gateway">

**API gateway** — a server that is the single entry point into a microservice system. It encapsulates the internal system architecture and provides an API tailored to each client, and may also handle authentication, monitoring, load balancing, and caching.
%%(Source: L8 slide 31.)%%

</span>

<span id="def-orchestration">

**Orchestration** — a way of coordinating a multi-service process that relies on a central "brain" to guide and drive the process, telling each participating service what to do next.
%%(Source: L8 slide 32.)%%

</span>

<span id="def-choreography">

**Choreography** — a way of coordinating a multi-service process that informs each part of the system of its job and lets it work out the details, typically by having each service react to events published by the others.
%%(Source: L8 slide 32.)%%

</span>

<span id="def-service-registry">

**Service registry** — a database of available service instances and their locations. Service instances register on startup and deregister on shutdown; clients or routers query the registry to find an instance to call.
%%(Source: L8 slides 34, 36.)%%

</span>

<span id="def-domain-event">

**Domain event** — an event that records a state change in the business domain, named in the past tense (e.g., `ErrandPosted`, `CreditReserved`). It is the starting artifact of event storming and the currency of event-driven communication.
%%(Source: L7 slides 38–41; L8 slide 4; Quiz 4 Q2.)%%

</span>

<span id="def-policy">

**Policy** — a business rule that reacts to a domain event and triggers a command, of the form "when … then …" (e.g., when `ErrandCompleted` then `SettleCredits`). In event storming, it is the policies that delimit the consistent contexts.
%%(Source: L8 slide 4; L7 slides 38–41; Quiz 3 Q5.)%%

</span>

<span id="def-atomicity">

**Atomicity** — the all-or-nothing property of a transaction: either every change in the group is applied or none is, so no observer sees a half-done operation (e.g., a paid booking must create the reservation *and* charge the card — both or neither).
%%(Source: L8 slide 10 (the ACID properties); Quiz 3 Q2.)%%

</span>

<span id="def-eventual-consistency">

**Eventual consistency** — the consistency guarantee of a saga-coordinated design: temporary inconsistency between services is allowed while the business process runs, provided the system is guaranteed to reach a consistent state eventually, through completed steps or compensating actions.
%%(Source: Tutorial 7 solutions Q1; L8 slides 13–15.)%%

</span>

<span id="def-request-sync-response">

**Request/sync response** — an interprocess communication style in which the client makes a request to a service and waits for the response before continuing (e.g., *Get passenger info*: TripManagement calls PassengerManagement and waits).
%%(Source: L8 slide 30; Quiz 3 Q10.)%%

</span>

<span id="def-notification-one-way">

**Notification (one-way request)** — an interprocess communication style in which the client sends a request and no reply is expected or sent (e.g., *Notify passenger*: DriverManagement tells PassengerManagement, and that is the whole conversation).
%%(Source: L8 slide 30; Quiz 3 Q10.)%%

</span>

<span id="def-request-async-response">

**Request/async response** — an interprocess communication style in which the client sends a request and the service replies asynchronously, later (e.g., *Trip created*: TripManagement asks Dispatcher and the answer comes back when it is ready).
%%(Source: L8 slide 30; Quiz 3 Q10.)%%

</span>

<span id="def-client-side-discovery">

**Client-side discovery** — a service-discovery style in which the client queries the service registry itself, determines the network locations of the available instances, and uses a load-balancing algorithm to pick one.
%%(Source: L8 slide 34; Quiz 3 Q3.)%%

</span>

<span id="def-server-side-discovery">

**Server-side discovery** — a service-discovery style in which the client sends the request to a load balancer, which queries the service registry and routes each request to an available instance (e.g., NGINX Plus, AWS Elastic Load Balancer).
%%(Source: L8 slide 35.)%%

</span>
