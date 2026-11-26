{% from "schedule/macros-fragment.md" import term, example with context %}
<h2>Week 8 — Microservices (II)</h2>

<span>

Builds on **Week 4** (architecture and deployment styles), **Week 6** (architecture II, REST) and especially **Week 7** — the microservice style, its principles, and the first look at domain-driven design. Tutorial 5 consolidates the diagramming and REST skills those weeks taught.
</span>

<span>

* **Can** explain DDD's problem-space/solution-space split — domain, subdomain, bounded context — and use event storming to propose microservice candidates.
* **Can** choose among the data patterns — database-server-per-service, shared database, data lake, saga — and justify the trade-offs for a given system.
* **Can** explain event sourcing and CQRS, how they combine, and what each buys and costs.
* **Can** describe the supporting patterns — interprocess communication styles, API gateway, orchestration vs choreography, service discovery — and where each applies.

</span>

<div>

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

**This chapter completes the {{ term("microservice", "an independently deployable service modeled around a business domain") }} toolkit.** Week 7 asked *what* a microservice is; this week asks how to carve them out of a business (DDD, event storming) and which patterns keep them decoupled once carved (data patterns, event sourcing, CQRS, gateway and discovery). Source for the whole chapter unless stated otherwise: L8 slides.

## Core concepts

<span id="W8-c1"></span>

### W8.1 Domain-driven design: from domain to bounded context ★

**Microservices fail when they are cut along technical layers instead of business lines, so you need a disciplined way to find the cuts.** {{ term("domain-driven design", "an approach to software design that models a system around the business domain, its subdomains, and bounded contexts") }} (DDD) supplies that discipline: it names the problem space first (domains and subdomains) and only then designs the solution space (bounded contexts).

<panel type="seamless" minimized header="%%What is domain-driven design?%%">

<include src="../../se-book-adapted/common/defs-week-07.md#def-ddd" trim />

</panel>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-domain" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-subdomain" trim />
</box>

**Subdomains are where microservice candidates come from.** Each subdomain focuses on one set of responsibilities and typically mirrors part of the business organization's structure, so a subdomain boundary is cohesive inside and loosely coupled outside — exactly the shape a microservice needs.

{% call example("L8 slides 2–3 — the FoC errand platform") %}
The FoC domain is **peer-to-peer campus errands**; its problem space is "gigs" — in the gig-economy sense: small, one-off jobs that someone else performs for pay, which is exactly what an FoC errand is. Within that domain sit subdomains such as **errand fulfillment**, the **closed credit economy**, **campus vendors**, and **identity**. Each is a candidate for its own microservice, owned by a small team and deployable on its own.
{% endcall %}

**Bounded contexts are the solution-space twin of subdomains.** You design one bounded context per subdomain implementation, and it gathers everything that implementation needs.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-bounded-context" trim />
</box>

**Ideally a bounded context and its subdomain align completely — but they live in different spaces.** Subdomains are discovered from the business (problem perspective); bounded contexts are engineered by you (solution perspective) and may split or merge subdomains as the design demands.

{% call example("L8 slide 3 — user authentication inside the Identity subdomain") %}
In the FoC Identity subdomain, *user authentication* and *access control* are two bounded contexts of the subdomain's implementation: each has its own inputs, events, processes, and data models, even though both serve the one "identity" responsibility.
{% endcall %}

**A ubiquitous language keeps each context internally consistent.** A shared vocabulary between domain experts and developers lets them talk without translation — and accepting that a word changes meaning when you cross a context boundary is part of the design, not a defect.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-ubiquitous-language" trim />
</box>

The diagram below draws the two contexts slide 3 names, side by side: each is a designed boundary of the solution space, and the same word, `Student`, deliberately means a different thing inside each.

<mermaid>
flowchart TB
    subgraph ORDER["Bounded context: Order — a designed boundary (solution space)"]
        direction LR
        O["Student =<br/>requestor or courier"]
    end
    subgraph IDENTITY["Bounded context: Identity — a designed boundary (solution space)"]
        direction LR
        I["Student =<br/>account holder with verified<br/>email and password"]
    end
</mermaid>

%%Notation: each framed area is one bounded context — a boundary you design in the solution space, gathering its own input, output, events, processes, and data models; the same word appearing in both frames with two different glosses is the point, not a defect.%%

How to read it: L8 slide 3 gives both glosses — "Student in Identity is an account holder with verified email and password; Student in Order context is a requestor or courier" — and supplies the reason the frames must exist: with one shared `Student` model, the Order side and the Identity side would fight over one table and one meaning. Each framed context is also a microservice candidate in the sense of W7 — the context boundary, not the org chart, is what you deploy around — and Quiz 3 Q4 tests exactly this distinction: "Payments and Notifications are subdomains in the business problem space; explicit model boundaries define bounded contexts in the software solution" (Source: L8 slide 3; Quiz 3 Q4).

#### Event storming: a lightweight practice to discover microservices

**Event storming finds microservice candidates by storming through the business as a chain of things that happened.** It needs no tooling beyond a wall and sticky notes, which is why the deck calls it lightweight (L8 slides 2, 4).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-event-storming" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-domain-event" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-aggregate" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-policy" trim />
</box>

**How it works:**

* **Start with domain events — the things that happened.** For FoC: `ErrandPosted`, `CreditReserved`, `ErrandCompleted` (slide 4).
* **Commands cause events.** A {{ term("command", "a request for an action to be performed, expressed as intent in the imperative mood and sent to a specific receiver; it changes application state and returns no data — defined in W9.1") }} is an instruction to change something, e.g. `PostErrand` or `SettleCredits` (slide 4).
* **Commands work on aggregates.** `PostErrand` creates an `Errand`; `Errand` and `Wallet` are aggregates (slide 4).
* **A policy reacts to an event and triggers a command — "when … then …".** E.g., when `ErrandCompleted` then `SettleCredits` (slide 4).
* **Clusters of aggregates, commands, and policies become your microservice candidates.** Everything one aggregate family needs lives in one service; everything else talks to it through events.

The diagram below shows the storming output for the FoC credit economy — read it as the chain of cause and effect the workshop would stick on the wall.

<mermaid>
flowchart TB
    PE["PostErrand<br/>(command)"] -->|"acts on"| AG["Errand<br/>(aggregate)"]
    AG -.->|"ErrandPosted<br/>(event)"| VENDOR["Campus vendors service"]
    CO["CompleteErrand<br/>(command)"] -->|"acts on"| AG
    AG -.->|"ErrandCompleted<br/>(event)"| POL{"Policy:<br/>when ErrandCompleted<br/>then SettleCredits"}
    POL -->|"triggers"| SC["SettleCredits<br/>(command)"]
    SC -->|"acts on"| WAL["Wallet<br/>(aggregate)"]
    WAL -.->|"CreditReserved<br/>(event)"| LEDGER["Credit service"]
</mermaid>

%%Notation: a rectangle is a command or an aggregate; the diamond is a policy; a solid arrow is synchronous control flow — a command acting on an aggregate, or a policy triggering the next command; a dashed arrow is a domain event published to the rest of the system.%%

How to read it: a command acts on an aggregate, the aggregate records an event, and a policy listening to that event fires the next command — so `PostErrand → Errand → … → ErrandCompleted → SettleCredits → Wallet → CreditReserved` is one storming pass over errand fulfillment and the credit economy. Each aggregate family plus its commands and policies is a microservice candidate: an *Order* service around `Errand`, a *Credit* service around `Wallet` (Source: L8 slide 4; Tutorial 6 — you will meet it in Week 9 — repeats these steps on a food-delivery platform).

<box type="warning" seamless>

**Pitfall — a subdomain is not a bounded context.** The subdomain belongs to the problem space and is discovered; the bounded context belongs to the solution space and is designed. Treating the business org chart as your service diagram, or letting one word ("Student") keep two meanings inside one context, are the two classic failures of a first DDD attempt (L8 slide 3).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** FoC's *closed credit economy* — is that a subdomain or a bounded context? And what would the corresponding bounded context be?
<panel type="seamless" minimized header="%%Answer%%">A subdomain: it is a component of the problem space with its own responsibilities. Its implementation — e.g. a Wallet context holding the `Wallet` aggregate, `SettleCredits`, and the credit events — is the bounded context.</panel>

**Q2.** In event storming, which artifact reacts, which causes, and which is acted on?
<panel type="seamless" minimized header="%%Answer%%">Policies react to events; commands cause events; commands act on aggregates. Chain: event → policy → command → aggregate → next event.</panel>

**Q3.** Why can `Student` safely mean "account holder" in Identity and "requestor or courier" in Order?
<panel type="seamless" minimized header="%%Answer%%">Because the two models live in different bounded contexts, each with its own ubiquitous language; the word is only ambiguous if you let one model leak across the boundary (L8 slide 3).</panel>

</panel>

<span id="W8-c2"></span>

### W8.2 Data patterns: owning, querying, and reconciling data ★★

**A microservice you cannot deploy independently is not a microservice, and a shared table is the classic threat to that independence.** The deck's guiding question is "what is the barrier for independent deployment?" — and its guideline answers it: microservices must own their data (L8 slide 6).

**How the data patterns fit together:**

* **Data independence means services must not modify the same data — not that each runs its own database cluster.** The deck is explicit: independence can also be achieved inside one database via RBAC (role-based access control) database users with per-table permissions, private tables per service, or a private schema per service (L8 slide 9).
* **Queries that must join several services' data get a read-only copy: the data lake.** Owner services stream data-change events into the lake, which is indexed for queryability (L8 slide 11).
* **Business processes that span several services' writes get the saga pattern: local transactions plus compensating actions.** There is no distributed ACID transaction to reach for (L8 slides 12–15).
* **The shared database "solution" reintroduces every coupling you split the monolith to remove — it is an antipattern.** (L8 slide 10.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-database-per-service" trim />
</box>

**Database-per-service buys loose coupling and per-service freedom.** Each service scales its database independently and may pick or replace the database technology that fits its access pattern — a search index for one service, a relational store for another (L8 slide 8).

<panel type="seamless" minimized header="%%What is loose coupling?%%">

<include src="../../se-book-adapted/common/defs-week-07.md#def-loose-coupling" trim />

</panel>

<box type="warning" seamless>

**Trade-off — the pattern has costs.**

* Different kinds of databases must be operated.
* A large application sees an explosion in the number of databases.
* The setup is expensive to manage (L8 slide 8).

Weaker forms of independence (private tables, schemas, RBAC users) trade some of that freedom for fewer moving parts (L8 slide 9).
</box>

**The shared database is what the guideline rules out.** It tempts because some transactions need data owned by other services, some queries must join data owned by multiple services, and one database enforces ACID properties (atomicity, consistency, isolation, durability) across them all — but the coupling costs are exactly the ones microservices exist to avoid.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-atomicity" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-shared-database" trim />
</box>

The comparison below is the decision the guideline forces on you.

<mermaid>
flowchart TB
    subgraph OWNED["Database-server-per-service (slides 8–9)"]
        direction LR
        FS["Flight search"] --- D1[("Search DB")]
        RS["Reservations"] --- D2[("Reservation DB")]
        FT["Flight tracking"] --- D3[("Tracking DB")]
    end
    subgraph SHARED["Shared database — antipattern (slide 10)"]
        direction LR
        FS2["Flight search"] --- D4[("One shared DB")]
        RS2["Reservations"] --- D4
        FT2["Flight tracking"] --- D4
    end
</mermaid>

%%Notation: a rectangle is a service, a cylinder is a data store, and a plain solid line is direct data access.%%

How to read it: on the left, each flight-domain service touches only its own store, so a schema change or a technology swap in Reservations cannot break Flight search. On the right, all three write one store — the schema change now needs all three teams to coordinate (development-time coupling), their writes can conflict at runtime, and one engine must satisfy three different access patterns (L8 slide 10).

{% call example("L8 slide 9 — data independence without separate servers") %}
The same flight platform can keep one database server yet stay independent: create different database users with specific read/write permissions on their own tables (RBAC), or give each of Flight search, Reservations, and Flight tracking its own private set of tables, or its own private schema within the shared server %%("schema" here: a named namespace of tables inside one database — a stronger separation than private tables, since the names in different schemas cannot collide)%%.
{% endcall %}

#### The data lake: queries across services

**Some queries must join data owned by multiple services, and the data lake answers them without breaking ownership.** The lake is a shared, read-only space; each owner streams its relevant data into it.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-data-lake" trim />
</box>

**Streaming, not direct reads, keeps the ownership rule intact.** Owner microservices push data-change events through a messaging infrastructure such as RabbitMQ or Kafka into the lake; a consumer such as an Analytics service queries the lake, never the owners (L8 slide 11).

<panel type="seamless" minimized header="%%What are RabbitMQ and Kafka?%%">

<include src="../../se-book-adapted/common/defs-week-10.md#def-rabbitmq" trim />

<include src="../../se-book-adapted/common/defs-week-10.md#def-kafka" trim />

</panel>

{% call example("L8 slide 11 — analytics over three flight services") %}
Flight search, Reservations, and Flight tracking each own their own database. For cross-service analytics dashboards %%("delivery-time dashboards" is the FoC variant of this slide's Analytics service — see the Week 9 chapter)%%, all three stream their data-change events into one data sink (the data lake); the Analytics service queries that lake instead of joining three live databases.
{% endcall %}

#### The saga: transactions across services

**When a business process must modify data owned by several services, the saga replaces the missing ACID transaction with compensation.** Booking a flight seat touches payments (possibly with loyalty points), seat reservation, and notifications — three services, three databases, "all or none" required (L8 slide 12).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-saga" trim />
</box>

**How it works:**

* **Every step of the transaction defines a compensating action, registered on a routing slip passed along to the next step.** The routing slip is simply the running list that travels *with* the transaction from service to service — each step adds its undo entry to it — so if a later step fails, whoever holds the slip knows exactly which compensations to run %%("routing slip" in the Enterprise Integration Patterns sense — Hohpe & Woolf: the list of steps rides in the message itself)%%. (L8 slide 13.)
* **If a later step fails, the routing slip kicks off the compensating actions of all completed steps.** (L8 slide 13.)
* **A saga does not promise to return to the initial state — only to a reasonably compensated one.** Saga ≠ ACID transaction (L8 slide 13).
* **Order the steps so the hard-to-compensate ones go last.** If the business rule allows, put notification at the very end of the process to avoid sending lots of correction messages (L8 slide 15).

{% call example("L8 slides 12–14 — booking a flight seat") %}
The booking saga books payment, reserves the seat, and notifies the customer. If the seat reservation fails after payment succeeded, the compensation initiates a refund — which "completes in some time". If the failure happens after the notification was sent, the only compensation is to send a *new* message asking the customer to discard the previous one — which is why notifications move to the end of the saga.
{% endcall %}

{% call example("Tutorial 7 (Week 10) Q1 — reserving credits for an FoC errand") %}
In the microservices design of the errand workflow, the Order service (errand `PENDING`) asks the Credit service to reserve credits, then tries to mark the errand `OPEN`. If that last local step fails, the compensation runs: the Credit service releases the reserved credits and the Order service marks the errand `CANCELLED`. (Source: Tutorial 7 solutions, Q1.)
{% endcall %}

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-eventual-consistency" trim />
</box>

The sequence below traces that FoC saga, including its compensation phase.

<mermaid>
sequenceDiagram
    participant O as Order service
    participant C as Credit service
    O->>C: Reserve credits (local tx 1)
    C-->>O: Credits reserved
    O->>O: Mark errand OPEN (local tx 2) — fails
    Note over O,C: Compensation phase
    C->>C: Release reserved credits
    O->>O: Mark errand CANCELLED
</mermaid>

%%Notation: in sequence diagrams a solid arrow is a synchronous step and a dashed arrow is its reply; `Note over` marks the compensation phase; each participant is a service with its own database.%%

How to read it: top to bottom in time order — the two forward steps (reserve, then open) each write only their own service's store; the failure of step 2 triggers the routing slip, and the compensations run back down the list. The end state (`CANCELLED` errand, credits released) is consistent, but it is *not* the state before the saga began (L8 slide 13; Tutorial 7 Q1).

<box type="warning" seamless>

**Pitfall — a saga is not an ACID transaction.** Intermediate states are visible to other services while the saga runs, compensation can itself fail or lag, and the "undo" of a notification is another notification. Choose the step order deliberately and design compensations for a reasonably compensated state, not a time machine (L8 slides 13, 15).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Three services must produce a joined report nightly. Why is the shared database the wrong fix, and what is the deck's alternative?
<panel type="seamless" minimized header="%%Answer%%">A shared database couples the three at development time (schema changes need coordination), at runtime (writes interfere), and forces one technology on all. The alternative is a data lake: each service streams data-change events into a read-only, query-optimized sink that the report queries (L8 slides 10–11).</panel>

**Q2.** Does database-per-service require one database *server* per service?
<panel type="seamless" minimized header="%%Answer%%">No. Data independence means services must not modify the same data; it can also be enforced with RBAC database users, private tables per service, or a private schema per service (L8 slide 9).</panel>

**Q3.** In the flight-booking saga, why does notification go last?
<panel type="seamless" minimized header="%%Answer%%">A sent message can only be "compensated" by another message asking the customer to ignore the first; moving the hard-to-compensate step to the end minimizes correction messages (L8 slide 15).</panel>

</panel>

<span id="W8-c3"></span>

### W8.3 Event sourcing and CQRS ★★

**Once services stop sharing tables, "current state" needs a source of truth you can trust — and the log of what happened is that source.** Event sourcing makes the log the storage; CQRS splits the readers from the writers (L8 slides 17–28).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-event-sourcing" trim />
</box>

**Event sourcing stores facts, not state.** In relational or NoSQL modeling %%(NoSQL: the non-relational database family — document, key–value, column, and graph stores)%% you usually store *the state* of something; in event sourcing you store the facts — the incremental changes — and the current state becomes a derivative, a value calculated from the sequence of events (L8 slides 17, 20).

{% call example("L8 slide 17 — recording a chess game") %}
A chess score sheet does not store a picture of the board after every move; it records the moves. The state of the board at any moment is the sum of all moves that have happened — replay the moves and you get the position back.
{% endcall %}

**Events are immutable, timestamped, and stored in creation order — so the log is a complete audit of exactly what the system did.** "Something that has happened" cannot be edited; you can rederive the current state by rewinding the log and replaying the events in order, which also gives you "undo" for free (L8 slide 18).

{% call example("L8 slides 19, 21 — an event-sourced order pipeline") %}
In an event-sourced order processing system, `OrderPlaced`, `PaymentReceived`, and `OrderShipped` are appended as they happen. When a customer places an order, the order request is stored as an event in the log *before* validation happens; when the order is validated, that outcome is appended as an entirely new event rather than overwriting the existing order. To determine the current order status, all relevant events are played from the beginning, reconstructing the order state; a database attached to the resulting event stream derives an event-sourced view of current orders.
{% endcall %}

The diagram shows the write path appending to the log and the read path replaying it into a view — the "command/write in (1) and query/read in (4)" note on slide 21.

<mermaid>
flowchart LR
    R["Client"] -->|"PlaceOrder (command — write)"| W["Order service"]
    W -->|"append"| L[("Event log:<br/>OrderPlaced → OrderValidated → …")]
    L -->|"replay in order"| V[("Orders view<br/>(current state)")]
    R -->|"GetOrders (query — read)"| V
</mermaid>

%%Notation: a cylinder is a store; solid arrows are the command (write) and query (read) paths; the arrow from log to view is the replay that derives the view.%%

How to read it: writes only ever append to the log on the left; the view on the right is not written to directly but derived by replaying events in order. If the view is lost or wrong, rebuild it from the log — the log is the source of truth (L8 slides 18–21).

#### CQRS: separating the write path from the read path

**CQRS takes that split and makes it a first-class architectural decision.** The write path and the read path get different models, and often different databases.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-cqrs" trim />
</box>

**Commands and queries are different animals.** Commands are operations that change application state and return no data — the methods with side effects; queries return data but do not change application state (L8 slide 25, from Bertrand Meyer's command–query separation).

**The split buys two things: recoverability and independent optimization.** Should something go wrong, the internal state of the database can be recovered from the log; and writes and reads can be optimized independently, because nothing forces one model to serve both (L8 slide 22).

**One write model can push data into many read models.** Writes go into Kafka on the command side rather than updating a table directly; the event stream is transformed to suit each query, typically with KSQL (a SQL-like language for querying Kafka's streams, per the slide's Confluent source) and materialized as a precomputed view. The underlying events are decoupled from each view, so each can be scaled independently — and read models can live in any database, or a range of different databases (L8 slides 23–24).

<panel type="seamless" minimized header="%%What is Kafka?%%">

<include src="../../se-book-adapted/common/defs-week-10.md#def-kafka" trim />

</panel>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-materialized-view" trim />
</box>

<box type="important" seamless>

**CQRS does not always need events or event sourcing — they are just mostly used together.** You can segregate commands from queries with plain CRUD (create, read, update, delete — the basic data-table operations) on two stores; event sourcing simply makes the write side a natural, ready-made event feed for the read side. (Source: L9 slide 2, the deck's own clarification.)
</box>

<box type="info" seamless>

**Telling apart — event sourcing vs CQRS vs materialized view.** One distinguishing question: **which lever does the pattern pull — what is *stored*, what is *separated*, what is *precomputed*?**

| | Event sourcing | CQRS | Materialized view |
|---|---|---|---|
| The lever it pulls | **What is stored:** the append-only log of facts, not the current state | **What is separated:** the write model (commands) from the read model (queries) | **What is precomputed:** the result of a predefined query, stored instead of computed on demand |
| State of the world without it | You'd store current state and overwrite it | One model serves reads and writes | Queries are computed live when asked |
| Needs the others? | No — it's a storage choice | No — CQRS "fits well with" event styles but is not defined by them (Fowler's CQRS bliki); L9 slide 2: "CQRS doesn't always need events/event sourcing" | No — a plain database can have one |
| Course example | The order log: `OrderPlaced` → `OrderValidated` appended, never overwritten (L8 slide 21) | Tutorial 7 Q2: the order service writes; the validation, tax, and email services each enrich the order; queries hit the *orders view* | The *orders view* itself — the read model derived from the order events (Tutorial 7 Q2; the concept from L8 slides 23–24) |

They combine naturally — the event log (sourcing) is a ready-made feed from which read models (CQRS) materialize their views — but each can be adopted alone, and the slide 21 note "command/write in (1), query/read in (4)" is where all three meet.

</box>

{% call example("Tutorial 7 (Week 10) Q2 — CQRS in an order-acceptance flow") %}
An order is accepted in the *orders* service (write path: the order event is recorded). A validation service picks it up and validates it, a Tax service adds sales tax, and an Email service is given the information for a confirmation email. The updated order flows back to the orders service, where it can be queried via the *orders view* — a read model derived from the order events. The user clicks through from the confirmation email to that view. (Source: Tutorial 7 sheet, Q2.)
{% endcall %}

<box type="warning" seamless>

**Pitfall — derived views lag the log.** A materialized view is only as fresh as its last computation, and an event-sourced view is derived by replaying events; a query answered from the read path can trail the most recent write. Design consumers of the view for that gap instead of promising read-your-writes consistency — the guarantee that a user sees the results of their own latest write on their very next read — everywhere (L8 slides 21, 23–24).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** In an event-sourced system, how do you answer "what is this order's status?"
<panel type="seamless" minimized header="%%Answer%%">Replay the order's events from the beginning (or from the last snapshot — a saved intermediate state that replay resumes from) — `OrderPlaced` → `PaymentReceived` → `OrderShipped` — and the resulting state is the status. You never read a "status column", because there isn't one (L8 slide 19).</panel>

**Q2.** A colleague asks why `ChargeCard` and `GetBalance` cannot live in the same model. Answer in one sentence each.
<panel type="seamless" minimized header="%%Answer%%">`ChargeCard` is a command: it changes state and returns no data. `GetBalance` is a query: it returns data and changes nothing. CQRS exists precisely because optimizing one model for both is what couples their scaling and recovery (L8 slides 22, 25).</panel>

**Q3.** True or false: adopting CQRS forces you to adopt event sourcing.
<panel type="seamless" minimized header="%%Answer%%">False. CQRS doesn't always need events/event sourcing — they are just mostly used together (L9 slide 2).</panel>

</panel>

<span id="W8-c4"></span>

### W8.4 Communication, gateway, and discovery patterns ★★★

**Well-carved services still need to find each other and talk — without the wiring recreating the monolith.** This unit collects the supporting patterns the deck groups under "other patterns": how services interact, how clients enter the system, how processes are coordinated, and how services are located (L8 slides 29–37).

#### Interprocess communication styles

**Three interaction styles cover the ways one service calls another.** (Source: L8 slide 30, from Richardson & Smith, *Microservices: From Design to Deployment*.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-request-sync-response" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-notification-one-way" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-request-async-response" trim />
</box>

* **Request/sync response** — the client makes a request to a service and waits for the response. E.g., *Get passenger info*: TripManagement calls PassengerManagement and waits.
* **Notification (one-way request)** — the client sends a request; no reply is expected or sent. E.g., *Notify passenger*: DriverManagement tells PassengerManagement, and that is the whole conversation.
* **Request/async response** — the client sends a request and the service replies asynchronously. E.g., *Trip created*: TripManagement asks Dispatcher, and the answer comes back later.

%%"Notification" is doing double duty in this chapter — don't conflate the two uses. In the style list above, **notification is a one-way request from one service to another**: DriverManagement tells PassengerManagement something, and the *services* are both ends of the conversation. In the flight-booking saga (W8.2), "notifications" are the *customer-facing messages* a notification service eventually sends — a downstream job that the one-way style might trigger, not the style itself.%%

**This menu previews Weeks 9–10.** Asynchronous communication (notification, request/async response) is exactly what event-driven architecture builds on; the synchronous style is the request–reply world of Week 6's REST APIs.

#### The API gateway

**Clients should not need to know the internal topology of your microservices.** The gateway hides it behind one door.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-api-gateway" trim />
</box>

{% call example("Tutorial 5 Q1 — the supplier repository SPA") %}
Tutorial 5 asks you to architect a single-page application performing CRUD operations on campus suppliers, vendors, and landmarks. A natural shape is the SPA calling one API gateway, which routes to the supplier service (and authentication, monitoring, etc. handled at the door) — the tutorial's hint, "understand the different ways a user can interact with the system", is precisely the gateway's job of tailoring the API to each client interaction. Many valid diagrams exist; the solution notes the important parts are the supplier service and the CRUD operations. (Source: Tutorial 5 sheet and solutions, Q1.)
{% endcall %}

#### Orchestration vs choreography

**Given a process that spans several services, you must decide who holds the workflow.** The deck's one-line contrast: orchestration relies on a central "brain" to guide and drive the process; choreography informs each part of the system of its job and lets it work out the details (L8 slide 32, from Sam Newman's *Building Microservices*).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-orchestration" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-choreography" trim />
</box>

The diagram contrasts the two on the same A → B → C workflow — the exact shape Tutorial 7 (Week 10) Q3 asks you to draw.

<mermaid>
flowchart TB
    subgraph ORCH["Orchestration — a central brain drives"]
        direction TB
        direction LR
        IN["Input stream"] --> ORC["Orchestrator"]
        ORC -->|"1. do your step"| A1["Service A"]
        ORC -->|"2. then you"| B1["Service B"]
        ORC -->|"3. then you"| C1["Service C"]
        A1 -.->|"done"| ORC
        B1 -.->|"done"| ORC
        C1 -.->|"done"| OUT["Output stream"]
    end
    subgraph CHOR["Choreography — each part reacts"]
        direction LR
        S1["Event stream 1"] --> A2["Service A"]
        A2 -.->|"publishes to stream 2"| B2["Service B"]
        B2 -.->|"publishes to stream 3"| C2["Service C"]
    end
    ORCH ~~~ CHOR
</mermaid>

%%Notation: rectangles are services (or the orchestrator); solid arrows are synchronous instructions from the orchestrator; dashed arrows are asynchronous events on streams.%%

How to read it: in the orchestration half, the workflow lives in one place — the orchestrator calls A, then B, then C and collects their acknowledgments. In the choreography half, no one holds the workflow: A reacts to stream 1 and publishes to stream 2, B reacts to stream 2 and publishes to stream 3, C reacts to stream 3. Reordering B and C in the choreographed version means rewiring who publishes to which stream — the concern Tutorial 7 (Week 10) Q3(b) asks you to spot (L8 slide 32; Tutorial 7 sheet, Q3).

#### Service discovery

**Services are deployed, scaled, and replaced dynamically, so callers need the current location of instances — the IP address and port — before any call can happen.** The API gateway (or any client) faces this on every request (L8 slide 33).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-service-registry" trim />
</box>

**Two discovery styles put the registry lookup on different sides of the call.**

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-client-side-discovery" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-08.md#def-server-side-discovery" trim />
</box>

* **Client-side discovery** — the client queries the service registry, determines the network locations of the available instances, and uses a load-balancing algorithm %%load balancing: spreading requests across multiple instances so no single one is overwhelmed; Week 12 develops it in full%% to pick one (L8 slide 34).
* **Server-side discovery** — the client makes a request to a load balancer; the load balancer queries the registry and routes each request to an available instance, e.g. NGINX Plus (a commercial version of the widely used NGINX web server, sold with load-balancing features) or an AWS Elastic Load Balancer (ELB — Amazon's managed service that automatically distributes incoming traffic across multiple targets such as EC2 instances and containers) (L8 slide 35).

**Registration comes in two flavors.** With self-registration, service instances register themselves on startup and deregister on shutdown; with third-party registration, a registrar does it on their behalf. Registries in practice include Apache Zookeeper, Consul, and Etcd %%all distributed infrastructure tools commonly repurposed as registries: Zookeeper is a distributed coordination service, while Consul and Etcd are distributed key–value stores that keep one entry per service instance%% — and some systems (Kubernetes, Marathon, AWS ELB) have an implicit registry built in %%they track the instances they deploy themselves, so no separate registry product is needed%% (L8 slides 36–37).

<box type="warning" seamless>

**Pitfall — the gateway and the orchestrator are concentration points.** A gateway is the single entry point: convenient for clients, but everything depends on it. An orchestrator is the single brain: the workflow is easy to see and change, but the brain must scale and stay available. The deck itself flags the patterns it did not cover — backend-for-frontend, circuit breaker, retry, timeout, service mesh, observability — which exist largely to harden these concentration points (L8 slides 31–32, 39).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** *Notify passenger* (DriverManagement → PassengerManagement, no reply) — which of the three interprocess styles is that, and what would change if it were request/async response?
<panel type="seamless" minimized header="%%Answer%%">It is a notification (one-way request): nothing is expected back. Request/async response would have PassengerManagement send some reply later — so the caller needs a way to correlate the eventual response with its request (L8 slide 30).</panel>

**Q2.** Your client team complains they must know the address of every service. Which pattern fixes it, and where does the registry lookup happen in its two flavors?
<panel type="seamless" minimized header="%%Answer%%">Service discovery behind an API gateway. Client-side: the client queries the registry and load-balances itself; server-side: the client calls a load balancer, which queries the registry and routes (L8 slides 31, 34–35).</panel>

**Q3.** Tutorial 7 (Week 10) Q3(b): the workflow A → B → C must become A → C → B. In the choreographed design, what changes?
<panel type="seamless" minimized header="%%Answer%%">The event streams must be rewired: A now publishes to the stream C consumes, and C's output feeds B — the "workflow" lives in those wirings, so changing the order means re-plumbing streams (and re-checking what each service expects), whereas in orchestration you change the orchestrator's script (Tutorial 7 sheet, Q3).</panel>

**Q4.** (Quiz 4 Q5.) A media platform has no orchestrator. Conversion charges the card (`ConversionPaid`), then fails permanently and publishes `ConversionFailed`. Who refunds, and how is each service's data ownership preserved?
<panel type="seamless" minimized header="%%Answer%%">Payment subscribes to `ConversionFailed` and issues the refund **under its own rules**, then publishes `PaymentRefunded`. That is a saga's compensating action (W8.2) carried out by *choreography* (W8.4): the failure event is the trigger, no central brain orders the refund, and Conversion never touches Payment's charge records — so each service still owns its data (L8 slide 32; Quiz 4 Q5).</panel>

</panel>

<box type="info" seamless>

**Section summary**

* **DDD gives microservice carving its vocabulary:**
  * Subdomains are the problem-space cuts.
  * Bounded contexts are the solution-space designs that become services.
  * Event storming finds both via events → commands → aggregates → policies.
* **Data independence is the line in the sand:**
  * Own your data (per-service database or weaker variants).
  * Never share a database.
  * Answer cross-service queries from a data lake.
  * Coordinate cross-service writes with sagas of local transactions and compensations.
* **Event sourcing stores facts, CQRS splits readers from writers** — and CQRS does not require event sourcing; they are just mostly used together.
* **The supporting patterns wire it up:** three interprocess styles, an API gateway as the single tailored entry point, orchestration vs choreography for process control, and service discovery via a registry.
</box>

## Key terms

| Term | Definition | Unit |
|---|---|---|
| Domain-driven design | Design approach that models the business domain — its subdomains and bounded contexts — before designing the solution | [W8.1](#W8-c1) |
| Domain | The problem space a business occupies and provides a solution for | [W8.1](#W8-c1) |
| Subdomain | A problem-space component of the domain with one set of responsibilities | [W8.1](#W8-c1) |
| Bounded context | The solution-space boundary of inputs, outputs, events, processes, and data models for one subdomain | [W8.1](#W8-c1) |
| Ubiquitous language | Shared expert–developer vocabulary, valid within one bounded context | [W8.1](#W8-c1) |
| Event storming | Lightweight workshop practice: events → commands → aggregates → policies → microservice candidates | [W8.1](#W8-c1) |
| Domain event | A recorded state change in the business, named in the past tense — event storming's starting artifact | [W8.1](#W8-c1) |
| Policy | Business rule that reacts to an event and triggers a command ("when … then …"); delimits consistent contexts | [W8.1](#W8-c1) |
| Database-server-per-service | Each service owns its database server; no direct cross-service data access | [W8.2](#W8-c2) |
| Shared database | One database written by several services — an antipattern for microservices | [W8.2](#W8-c2) |
| Atomicity | All-or-nothing: every change in a transaction applies or none does | [W8.2](#W8-c2) |
| Eventual consistency | Temporary inconsistency allowed while a saga runs; the system reaches a consistent state eventually | [W8.2](#W8-c2) |
| Data lake | Read-only, queryable sink of data streamed from owner services | [W8.2](#W8-c2) |
| Saga | Sequence of local transactions with registered compensating actions, coordinated via events/messages | [W8.2](#W8-c2) |
| Event sourcing | Store state changes as immutable events in an append-only log; derive state by replay | [W8.3](#W8-c3) |
| CQRS | Separate the write path (commands) from the read path (queries), each with its own model | [W8.3](#W8-c3) |
| Materialized view | Precomputed, stored result of a predefined query | [W8.3](#W8-c3) |
| API gateway | Single entry point that encapsulates the system and tailors APIs per client | [W8.4](#W8-c4) |
| Orchestration | Central "brain" drives a multi-service process | [W8.4](#W8-c4) |
| Choreography | Each part knows its job and reacts to events; no central brain | [W8.4](#W8-c4) |
| Service registry | Database of service instances and locations, kept current by (de)registration | [W8.4](#W8-c4) |
| Request/sync response | Caller sends a request and waits for the response | [W8.4](#W8-c4) |
| Notification (one-way request) | Request sent; no reply expected or sent | [W8.4](#W8-c4) |
| Request/async response | Request sent; the reply comes back later | [W8.4](#W8-c4) |
| Client-side discovery | Client queries the service registry and load-balances itself | [W8.4](#W8-c4) |
| Server-side discovery | Load balancer queries the registry and routes each request | [W8.4](#W8-c4) |

## Connections

| Concept | Lecture | Tutorial | Other weeks |
|---|---|---|---|
| Domain / subdomain / bounded context | L8 slides 2–3 | Tutorial 6 Q1 (bank subdomains; Week 9) | Week 7 (DDD introduced) |
| Event storming | L8 slide 4 | Tutorial 6 Q2 (food delivery; Week 9) | Week 9 (events as the EDA currency) |
| Data ownership / database-per-service | L8 slides 6–9 | — | Week 9 slide 22 ("observe database-per-service here") |
| Shared database, data lake, saga | L8 slides 10–15 | Tutorial 7 Q1 (FoC saga; Week 10) | Week 12 (scalability of stores) |
| Event sourcing, CQRS | L8 slides 17–28 | Tutorial 7 Q2 (orders view; Week 10) | Week 9 (two of the four views of an event) |
| Interprocess communication styles | L8 slide 30 | — | Weeks 9–10 (async becomes the default) |
| API gateway, orchestration/choreography, discovery | L8 slides 31–37 | Tutorial 5 Q1 (SPA architecture), Tutorial 7 Q3 (A→B→C; Week 10) | Week 6 (REST request–reply) |

## Further reading

* Martin Fowler, [Microservices](https://martinfowler.com/microservices/) and [CQRS](https://martinfowler.com/bliki/CQRS.html) — cited on L8 slide 5.
* Chris Richardson & Floyd Smith, [*Microservices: From Design to Deployment*](https://www.nginx.com/blog/introduction-to-microservices/) — source of the communication, gateway, and discovery slides (L8 slides 30–37).
* Sam Newman, *Building Microservices* — source of the orchestration vs choreography contrast (L8 slide 32).
* [Microsoft Azure — Saga pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/saga) — image source on L8 slide 15.
* [microservices.io](https://microservices.io/patterns/client-side-discovery.html) — client-side, server-side discovery and service registry patterns (L8 slide 33).
* The se-book's [event-driven architecture page](https://se-edu.github.io/se-book/architecture/architecturalStyles/eventDriven/) — the style Week 9 builds on.

## Summary

**Key takeaways** (one per outcome):

* **You can carve a system into microservices by design, not by accident:** subdomains name the problem-space cuts, bounded contexts design the solution-space boundaries, and event storming turns a wall of events, commands, aggregates, and policies into service candidates.
* **Data patterns are what make independence real:** own your data (database-per-service or its weaker variants), refuse the shared database, stream cross-service queries into a data lake, and reconcile cross-service writes with sagas and compensating actions.
* **Event sourcing and CQRS restructure storage around what happened:** facts in an append-only log with state derived by replay, and separate write/read models — knowing the two are *mostly*, not always, used together.
* **The supporting patterns complete the wiring:** sync/one-way/async communication styles, an API gateway as the tailored front door, orchestration or choreography for process control, and registry-based discovery for dynamic locations.

Key terms: see the [Key terms table](#key-terms) above, each linked to its unit.

%%Next: Week 9 — Event-driven architecture. The event storming artifacts of W8.1 become real messages, event sourcing and CQRS become two of the four views of an event, and fire-and-forget communication replaces the request–reply habit.%%

</div>
