{% from "schedule/macros-fragment.md" import term, example with context %}
<h2>Week 7 — Microservices (I)</h2>

<span>

**Prerequisites:** [Week 4 — Architecture (I)]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html) (coupling and cohesion, modular monolith) and [Week 6 — Architecture (II) & REST]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html) (the style taxonomy, REST as the service communication style). Week 5's containers are the deployment backdrop for independent deployability.
</span>

<span>

**Learning outcomes:**

* **Can** define the microservice architectural style, its four defining characteristics, and what drives the move from a monolith. — [W7.1](#W7-c1)
* **Can** explain "organized around business capabilities" and "owned by a small team" in concrete terms. — [W7.2](#W7-c2)
* **Can** weigh the monolith-vs-microservices trade-offs for a concrete system and argue whether splitting helps or hurts. — [W7.3](#W7-c3)
* **Can** compare synchronous and asynchronous communication between services and choose appropriately. — [W7.4](#W7-c4)
* **Can** explain domain, sub-domain (core/supporting/generic), and domain model, and their role in domain-driven design. — [W7.5](#W7-c5)
* **Can** identify bounded contexts, apply a ubiquitous language, and describe how contexts collaborate. — [W7.6](#W7-c6)
* **Can** explain aggregates, their root and boundaries, and why they are the consistency unit of DDD. — [W7.7](#W7-c7)
* **Can** use sub-domains, bounded contexts, aggregates, and event storming to identify microservice boundaries — and state the cautions. — [W7.8](#W7-c8)
</span>

<div>

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.

</box>

## Core concepts

<span id="W7-c1"></span>

### W7.1 The microservice architectural style ★

**When one application grows too large for one team, one codebase, and one deployment, the microservice style is the lecture's structural answer.** The lecture sets the scene with the question: what happens when the system becomes too large for a single application? A large codebase, slow deployment, multiple teams involved, and scaling issues — no independent scaling. (Source: L7 slide 3.)

%%The professor's standing joke (L7 recording, ~[4:00]): asked about *any* design decision, "it reduces coupling and increases cohesion" is never wrong — but it earns no marks until you say *how*. Keep the two words; supply the mechanism.%%

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-microservice-architecture" trim />
</box>

**How it works:**

**A microservices application is a single application delivered as a suite of small services.** (Source: L7 slide 5):

- Each microservice offers a well-defined business capability.
- Each is developed and deployed independently.
- The services communicate through well-defined mechanisms and published interfaces.

**The building blocks are a collection of small networked services — each with a limited scope — that work with each other.** Together they form the bigger solution: the lecture notes real systems run 1000+ microservices. (Source: L7 slide 6.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-microservice" trim />
</box>

**Four characteristics define the style: organized around business capabilities, loosely coupled, owned by a small team, independently deployable.** (Source: L7 slide 7 — after Richardson & Smith, *Microservices: From Design to Deployment*.) The lecture notes the count varies — some sources say five — but all the variants subsume into these four (L7 recording, ~[25:00]). W7.2 develops the first and third; W7.3 the costs and buys; W7.4 the communication.

**The lecture positions the style on two axes you already have: how you partition the code, and how many processes you deploy.** (Source: L7 recording, ~[13:00].) Partition by technical layer and deploy as one process and you get the classical styles of W6 — partition by domain concern and deploy distributed and you arrive at microservices:

| | **Deployed as one process** | **Deployed as distributed processes** |
|---|---|---|
| **Code partitioned by technical layer** | Layered, pipe-and-filter (W6) | Event-driven (W9) |
| **Code partitioned by domain concern** | Modular monolith (W6.4) | **Microservices — this week** |

%%Table after L7 recording, ~[13:00–15:00]: "monolithic, partitioned technically → layered, pipe-and-filter; monolithic, partitioned by domain → modular monolith; distributed, partitioned technically → event-driven; distributed, partitioned by domain → microservices."%%

**Each service has a deliberately limited scope — one functional requirement, or a tight group of them.** The lecture's rule of thumb: take a functional requirement — or a logical grouping of closely related ones — implement it, and that is the scope of one service; together the services still form one bigger solution. (Source: L7 recording, ~[28:00].)

{% call example("L7 recording, ~[29:00] — Netflix's poster-child services") %}
The lecture calls Netflix the poster child of microservices: 1000+ of them, each with a very small scope. One service's entire job is *create a main menu list of movies* — build the list that shows up in the menu, nothing else. Another is *use watch history to recommend videos you may like* — it does not manage the watch history (some other service owns that) and does not care what happens after the recommendation is shown. Limited scope, single functionality — and the thousand pieces together are one application.
{% endcall %}

<panel type="seamless" header=":glyphicon-question-sign: **Common question (asked in lecture)**">

**"Doing only one thing — isn't that just separation of concerns?"**

<panel type="seamless" minimized header="%%Answer%%">

Both, at different levels (L7 recording, ~[32:00], asked in lecture). A user service manages *users* — that is one concern, separated from orders and payments (separation of concerns). But inside that concern sit several *responsibilities*: profile updates, user data, authentication, authorization — and the {{ term("single-responsibility principle", "each service should have only one reason to change — adapted from the class-level rule; defined in W7.8") }} is what splits *within* the concern. Strictly, SRP's definition applies to a single class ("one reason to change"); the lecture adapts it to services: a service should have only one reason to change. The project nudge that came with it: most D1 user services bundle profile + authentication + authorization, and you *could* keep splitting (even authn and authz apart) — "be reasonable" about project time, but know that the scope is already wide.

</panel>

</panel>

**The migration shape is monolith → API gateway → services.** The lecture's diagram fronts the decomposed MyEcom application with an {{ term("API gateway", "the single entry point that receives client requests and routes them to the microservices behind it") }}: the client talks to the gateway, the gateway talks to the Customer, Shipping, and Payment services — each service carrying its own presentation, business logic, and persistence, which the diagram notes "can be layered, pipe-and-filter (P&F), MVC…". (Source: L7 slide 3.)

{% call example("L7 slide 3 — MyEcom, before and after the split") %}
Before: one **Monolith Server** holds the whole MyEcom application — presentation, business logic, persistence — and every client request lands on it. After: an API gateway receives requests and forwards them to the **Customer**, **Shipping**, and **Payment** microservices, each owning its own slice of presentation, business logic, and persistence and communicating over REST. The style inside each service is unchanged — what changed is the deployment and ownership boundary around each business capability.
{% endcall %}

The diagram shows the migration from one deployable to capability-owned services behind a gateway.

<mermaid>
flowchart LR
  cl(["Client"]) --> gw["API gateway"]
  subgraph before["Before — one deployable"]
    mon["Monolith Server — presentation · business logic · persistence"]
  end
  subgraph after["After — one service per capability"]
    c["Customer service"] 
    s["Shipping service"]
    p["Payment service"]
  end
  gw -.->|"routes requests"| c
  gw -.-> s
  gw -.-> p
</mermaid>

%%Notation: boxes are services (the rounded box is the client), dashed arrows are routed requests, and the subgraphs contrast the before and after deployment structures.%% To read it: in the before picture, a rush of payment traffic loads the whole monolith because everything ships as one unit (Week 5's scaling limitation). In the after picture, the gateway is the only public entrance; behind it, each capability can deploy, scale, and fail on its own — and no service knows another's internals.

<box type="warning" seamless>

**Pitfall:** hearing "small" and splitting by technical layer. A "persistence microservice" shared by every feature recreates the monolith's coupling across the network. The style's services are cut along business capabilities (W7.2), not along code layers (W6.2's layered style is a *within-service* option — the lecture's own diagram notes each service can be layered, pipe-and-filter, or MVC).

</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** State the four characteristics of the microservice style from the lecture.

<panel type="seamless" minimized header="%%Answer%%">

- Organized around business capabilities.
- Loosely coupled.
- Owned by a small team.
- Independently deployable.

(Source: L7 slide 7.)
</panel>

**Q2.** What four pressures does the lecture list as the moment to consider splitting a monolith?

<panel type="seamless" minimized header="%%Answer%%">

- Large codebase.
- Slow deployment.
- Multiple teams involved.
- Scaling issues (no independent scaling).

(Source: L7 slide 3.)
</panel>

</panel>

<span id="W7-c2"></span>

### W7.2 Organized around business capabilities ★

**Microservice boundaries follow the business, not the code — a service is a business capability with a team attached.** "A microservice offers a well-defined business capability", and microservice boundaries are closely aligned with business capabilities. (Source: L7 slides 8–9.)

**How it works:**

**Cohesion is the test: the features in a microservice should be highly related.** Each microservice has a responsibility allocated — the lecture draws Order, Payment, and Checkout as separate cohesive services. (Source: L7 slide 9.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-business-capability" trim />
</box>

**Services are owned by small teams that own the whole lifecycle.** (Source: L7 slide 10):

- Service decisions are independently made and handled by small teams.
- The lecture cites Amazon's **two-pizza teams** — small enough that two pizzas feed them.
- Teams are cross-functional, organized around capabilities, and own the whole lifecycle of their services.

**Why small and cross-functional? Because the product inherits the team's shape.** The lecture grounds the small-team rule in Conway's observation about teams and system structure (L7 recording, ~[41:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-conways-law" trim />
</box>

{% call example("L7 recording, ~[42:00] — three team shapes, three architectures") %}
A team of database administrators will naturally build something persistence-heavy — put those people together and you get a persistence layer. Add a team strong in Python and API development and you get a solid back-end team. A *layered* architecture falls straight out of that team structure. A cross-functional team — someone who knows the domain, someone who knows the tech stack, someone who knows how communication works, someone who can handle deployment — can own a whole capability end-to-end: the lecture's Shipping service, developed and operated by one such team. The professor's caution: the point is not "two pizzas, therefore small" — it is reducing dependence on each other, both in the code base and in team capabilities.
{% endcall %}

**Independence has a technical face: services share no code or implementation.** Services do not need to share any of their code with other services, and there is minimal dependence on each other — loose coupling by construction. (Source: L7 slides 7 and 10.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-loose-coupling" trim />
</box>

{% call example("L7 slides 8–9 + L7 recording, ~[35:00] — the mom-and-pop retailer goes online") %}
A brick-and-mortar retailer switches to online retail. The **domain** is everything from warehouse to reception desk, finance to ordering. The **warehouse** manages orders being shipped out, returns, and new stock — and may expose the capability "get a current stock list"; **finance** manages payroll, produces reports, and manages company accounts — exposing "monthly accounts" or "set up payroll for a new recruit". Each area is a business capability first; the services that implement them (e.g., Order, Payment, Checkout) inherit those boundaries, and each is cohesive — every feature inside it relates to that capability. The lecture's cohesion check: your finance service is not going to deal with how much stock of some item you have, and your warehouse does not manage anyone's salary — well-defined capabilities, well separated.
{% endcall %}

**"Well-defined" capability means an exact boundary: the service does everything up to a point, and past that point it is someone else's problem.** You establish where your responsibility ends, and you do not step over it. (Source: L7 recording, ~[37:00].)

{% call example("L7 recording, ~[38:00] — where the order service ends and the credit service begins") %}
From the D1 discussions: how do credits get transferred after an order is marked complete? The order service's job runs through the order's states and ends the moment it can say **"my order is completed"** — it may announce that in any way it likes, because it is independent. The credit service picks up that signal and owns everything after it: transferring the credits. Neither tells the other its job — the order service does not say "now go transfer", and the credit service does not say "mark it complete so I can transfer". If the order service went on to *do* the credit transfer, it would be operating on a different entity (credit) than the one it owns — "poking your nose elsewhere", which is exactly what we call coupling.
{% endcall %}

<box type="warning" seamless>

**Pitfall:** confusing "business capability" with "business department". The capability is what the business *does* (ship orders, settle payments), not necessarily how the org chart currently groups people — the lecture's own warehouse/finance example cuts across desk boundaries. Let cohesion of the capability decide, then let teams form around it.

</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Why does the lecture say services "do not need to share any of their code" — what style property does that buy?

<panel type="seamless" minimized header="%%Answer%%">

Loose coupling: with no shared code or implementation, each service (and its team) can change, deploy, and be replaced independently — a change in one service forces no change in another.
</panel>

**Q2.** A proposed "User Database service" that all features read from — capability-aligned or not?

<panel type="seamless" minimized header="%%Answer%%">

Not capability-aligned: it is a technical resource, not a well-defined business capability, and every feature depending on it re-couples the whole system to one unit (the monolith problem re-created at the data layer).
</panel>

</panel>

<span id="W7-c3"></span>

### W7.3 Monolith vs microservices: the trade-offs ★

**Splitting is not a free win: the lecture prices every buy in microservices with a matching cost.** Deciding whether to split means weighing both columns for *your* system — the lecture's own think-pair-share (think alone, discuss in pairs, share with the room) drills exactly this. (Source: L7 slides 14–15.)

**How it works:**

**The buys: deployability, scalability, and availability.** (Source: L7 slide 14):

- **Deployability** — separate deployables and pipelines; ship the credit service without updating supplier services.
- **Scalability** — the service is the unit of scaling; scale the order service during peak periods. The lecture makes it concrete: define a criterion (e.g., spawn another pod when load passes 60%) and let Kubernetes enforce it — "during peak times if you want to scale your order service, go ahead, scale it; others don't bother" (L7 recording, ~[54:00]).
- **Availability** — fault isolation and redundancy; a down supplier service doesn't impact credit settlement. (Source: L7 slide 14.)

**The costs: performance, integrity, and complexity.** (Source: L7 slide 14):

- **Performance** — latency and timeouts: every call is a network hop, and a down service keeps others waiting. And performance can cut both ways: splitting the user service into authentication, authorization, and profile management means a profile update now hops through authentication ("is this a valid user?"), then authorization ("may this user make changes?"), then profile management — each hop adds latency, where the monolith's single database call had none (L7 recording, ~[56:00]).
- **Integrity** — each service owns its data, and potential data duplication causes inconsistencies. (This is *data* integrity — the consistency sense, W3.5 — not the security sub-concern "protection against unauthorized modification".)
- **Complexity** — distributed debugging and the need for observability (being able to infer what the system is doing inside from what it emits outside — logs, metrics, traces): with *n* services you get *n* logs, so traceability is harder.

{% call example("L7 recording, ~[55:00] — what fault isolation buys when the supplier service dies") %}
If the supplier service goes down, you cannot select a supplier for *new* orders — but for orders already completed, credit transfers continue: the credit service's availability is untouched. Two further levers exist. You can let the platform auto-spawn the dead service (deploy it in Kubernetes so it restarts on death) — the in-flight transaction may have to be repeated, but the service as a whole is available again. And for a critical service you can run multiple instances behind a gateway: one instance dies, the gateway routes to the others — "it might be slower, the performance might degrade, but availability is not affected."
{% endcall %}

%%The follow-on lecture names the operation independent deployability enables: hot swapping — when a service fails or must be replaced, take it out and put another in *while the system keeps running* (L8 recording, ~[5:00]). Machines don't come with hot-swapping parts; architectures can be designed so their services do.%%

**Modular monolith and microservices can share the same internal boundaries — what changes is how many things you deploy and who owns them.**

<mermaid>
flowchart TB
    subgraph MM["Modular monolith — one deployable, module boundaries in code"]
        direction LR
        M1["Search module"]
        M2["Reservation module"]
        M3["Notification module"]
        MDB[("One shared DB")]
        M1 --- M2 --- M3
        M3 --- MDB
    end
    subgraph MS["Microservices — one deployable per capability"]
        direction LR
        S1["Search svc<br/>team A"] --- SDB[("Search DB")]
        S2["Reservation svc<br/>team B"] --- RDB[("Reservation DB")]
        S3["Notification svc<br/>team C"] --- NDB[("Notification DB")]
        S1 -.- S2 -.- S3
    end
    MM ~~~ MS
</mermaid>

%%Notation: the top panel's plain lines are in-process calls and data access inside one deployment unit (boundaries are compile-time only); the bottom panel's services are separately deployed, each with its own store and owning team; a dashed line between services is a two-way API/message conversation (asynchronous messaging; the exchange runs both ways, so no arrowheads).%%

How to read it: walk it with Quiz 3's platform: the team *already* has the modular-monolith top panel — search, reservation, notification as modules over one {{ term("ACID", "the transaction properties — atomic, consistent, isolated, durable: a transaction's changes apply all-or-nothing across everything it touches") }} transaction.
Moving down changes three practical things:

- **Deploys** go from one unit to three (search can be scaled alone — Quiz 3 Q1's answer)
- **Data** goes from one transaction that is atomic, consistent, isolated, durable — all-or-nothing across modules — to per-service stores whose cross-service atomicity must be *designed* (Quiz 3 Q2 says: don't split while cross-module atomicity cannot be relaxed and no design has yet demonstrated how to preserve it)
- **Ownership** splits per capability (Quiz 3 Q3's coordination pain)

The diagram shows structure, not superiority — the bottom panel is only better when those three costs buy something you need. (Structure after L5 slides 23–25, Dell guest lecture, and L9 slide 26; the data angle is W5.3's diagram.)

**Independently deployable does not mean centrally hosted: each service carries its own deployment, resource, scaling, and monitoring requirements.** The lecture names three deployment patterns — service instance per host (each instance isolated on its own host — a host being a physical or virtual machine), service instance per container (each instance in its own container image — the Week 5 mechanism), and service instance per VM (each service packaged as a virtual-machine image, e.g., an Amazon EC2 AMI — Amazon Machine Image; EC2 is Amazon's cloud virtual-machine service). (Source: L7 slides 11–12.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-service-instance-per-host" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-service-instance-per-container" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-service-instance-per-vm" trim />
</box>

**The lecture also prices the patterns themselves.** Instance per host runs on the bare-metal machine from L1 — isolated and independently working, but you waste resources when the service under-uses the machine and pay dearly when it needs more. And instance per VM often arises ad hoc: you develop a container, are told to deploy to the cloud, so you push the container into a cloud VM and call the service "on the cloud" — "nothing wrong in doing that", but it may not be the best use of resources. (Source: L7 recording, ~[45:00–47:00].)

{% call example("L7 slide 15 + L7 recording, ~[60:00–66:00] — the errand platform (FoC): does splitting help or hurt?") %}
Assume the errand platform was designed as a modular monolith — the lecture's own setup: "a Django backend naturally gives you a modular monolithic approach" — and the team then weighs four observed drivers:

1. Errands see **20× traffic during lunch**, while the supplier catalogue is quite static
2. The **credit mechanism undergoes changes** — the starting 100 credits prove insufficient, so people can buy or loan credits — while other mechanisms stay unchanged
3. After errand completion, **credit transfer should be idempotent** — it happens exactly once — and splitting moves from a single DB to multiple DBs
4. Deployment moves from one Amazon image (one VM) to multiple containers

Weighing them, with the lecture room's verdicts:

- **(1) argues for splitting** — the class first guessed "availability"; the correction: the attribute at work is *scalability* — the errand service scales independently (~[62:00], asked in lecture).
- **(2) argues for splitting** — and not because of deployment alone: it is independently *develop* *and* deploy the credit mechanism (~[64:00]).
- **(3) argues against** — with a single database you delegate integrity to the database; as microservices, idempotency and eventual consistency become *your* responsibility — a harder problem (~[65:00]).
- **(4) is a net cost** — independently scalable, yes, but "debugging a distributed application... becomes a nightmare": the complexity cost (~[66:00]).

The verdict depends on which costs your requirements cannot afford — which is the point of the exercise.
{% endcall %}

<panel type="seamless" header=":glyphicon-question-sign: **Common question (asked in lecture)**">

**"Doesn't the database already guarantee the exactly-once credit transfer?"**

<panel type="seamless" minimized header="%%Answer%%">

Only while the transfer is one local transaction in one database (L7 recording, ~[65:00], asked in lecture). There you delegate integrity to the database, which manages the ACID properties for you. Once credits live in a separate service's own database, the guarantee is yours to design: the transfer must be **idempotent** (running it twice has the same effect as running it once) and the system must accept {{ term("eventual consistency", "after a distributed update, services may briefly disagree but converge once updates stop — defined in Week 8") }} — "that becomes a harder problem to deal with", which is exactly the integrity cost W7.3 prices.

</panel>

</panel>

<box type="warning" seamless>

**Pitfall:** collecting the buys and ignoring the price. The errand platform's exactly-once credit transfer is the lecture's warning: splitting one database into many converts a local transaction into a distributed one. If your hardest requirement is integrity rather than scale or release speed, the monolith may be the *right* answer — "monolith" is a deployment choice, not a defect (W6.4). And the lecture's closing verdict: "your microservice is not a silver bullet... it's a trade-off, again, like any other architecture decision" — if independent scaling is critical to you, go ahead; if it is not, pause and think (L7 recording, ~[66:00]).

</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** For each buy, name the matching cost from the lecture: deployability ↔ ?, scalability ↔ ?, availability ↔ ?

<panel type="seamless" minimized header="%%Answer%%">

Deployability (separate pipelines) ↔ performance (every call is a network hop; a down service keeps others waiting). Scalability (service as unit of scaling) ↔ integrity (data duplication across services causes inconsistencies). Availability (fault isolation) ↔ complexity (n services, n logs — harder traceability, distributed debugging). (Source: L7 slide 14.)
</panel>

**Q2.** Which of the errand platform's four drivers argues *against* splitting, and why?

<panel type="seamless" minimized header="%%Answer%%">

Exactly-once credit transfer: with a single DB, the transfer is one local transaction; across multiple service databases it becomes a distributed-transaction problem — the integrity cost of microservices.
</panel>

</panel>

<span id="W7-c4"></span>

### W7.4 How microservices communicate ★

**Independently deployable services must still talk to each other — through well-defined mechanisms, synchronously or asynchronously, and the choice changes what happens when a service is down.** The lecture's invoice example contrasts the two modes directly. (Source: L7 slide 13.)

**How it works:**

**"Well-defined" communication means an agreed contract, and the contract — not the code — is the interface.** The lecture: establish the contract ("if I have to render certain services to you, your request should contain all these things" — what you are dealing with, what operation you want, what the new value is), and as long as the contract does not change, you have a well-defined mechanism — whether it is a RESTful API or an event mechanism. (Source: L7 recording, ~[49:00].)

**{{ term("Synchronous", "communication where the caller waits for the callee's answer before moving on — defined in full in Week 10") }} patterns: the caller waits.** RESTful APIs over HTTPS, gRPC services (glossed in W6.10's alternatives table), GraphQL interfaces (an API style where the client asks for exactly the fields it needs in one query) — the lecture's list for request-style integration between services. (Source: L7 slide 13.) The lecture's mechanics: when A calls B, A *blocks itself* — it does nothing else until B responds; internet speeds make it undramatic, but the caller is still blocked. And REST's known gaps (e.g., no type checking) are why the same list also offers gRPC and GraphQL. (L7 recording, ~[50:00].)

**{{ term("Asynchronous", "communication where the sender moves on without waiting — events and message queues; defined in full in Week 10") }} patterns: the caller moves on.** Event-based communication — e.g., publish-subscribe events, where a publisher emits an event and every interested subscriber receives it (developed in Week 9) — and message queues (the lecture names Kafka — a distributed event-streaming platform, Week 10's subject — and Amazon SNS — Amazon's managed publish–subscribe notification service — in the bounded-context integration slide). (Source: L7 slides 13 and 31.) Asynchronous communication needs an intermediary in between — an event bus or a queue: the publisher emits and continues, and the intermediary notifies the consumer that something is pending. (L7 recording, ~[51:00].)

{% call example("L7 slide 13 + L7 recording, ~[50:00] — one invoice, two interaction styles") %}
A Payment service handles an invoice held by the Finance service. **(a) Synchronous:** Payment sends `InvoicePaid` as a request via the API, initiating a state transition in the invoice — and until Finance answers, the Payment service blocks itself and does nothing else. **(b) Asynchronous:** Payment creates an event — "order received, give me an invoice" — with a structured payload, puts it on the intermediary (an event bus or a queue), and moves on. The intermediary notifies Finance that something is pending; Finance picks the event up, generates the invoice, puts it back on the bus, and continues with its own work. The bus then notifies Payment — "your invoice is ready" — and Payment picks it up and proceeds. No blocking anywhere: each service works until it has something to pick up. (Walkthrough: L7 recording, ~[50:00–52:00].)
{% endcall %}

{% call example("Quiz 2 Q1 — the Grab-like app: what survives a two-minute crash?") %}
In a Grab-like ride-hailing app, **Design A**: Booking makes a synchronous call-and-return to Matching. **Design B**: Booking publishes a `BookingRequested` event to the middleware (Quiz 2's shorthand for the messaging infrastructure between services — a message queue or broker that stores and forwards events). When the Matching component crashes for two minutes at peak, **Design B offers reliability by storing the event in the middleware until Matching becomes available** — Booking is never blocked, nothing is lost. In Design A, Booking's call fails or hangs while Matching is down: the synchronous dependency chain is the availability cost W7.3 named. (Source: Quiz 2, Q1.)
{% endcall %}

The diagram stacks the two interaction styles, (a) above (b), for the same business event.

<mermaid>
flowchart TB
  subgraph sync["(a) Synchronous — request via API"]
    pay1["Payment service"] -->|"InvoicePaid (waits for reply)"| fin1["Finance service"]
  end
  subgraph async["(b) Asynchronous — event via queue"]
    pay2["Payment service"] -.->|"publishes InvoicePaid"| q[["Queue"]]
    q -.->|"consumes when able"| fin2["Finance service"]
  end  sync ~~~ async
</mermaid>

%%Notation: boxes are services, the double-struck box is a message queue (a data store for in-flight messages), solid arrows are synchronous calls where the caller waits, and dashed arrows are asynchronous messages the sender does not wait on.%% To read it: in (a), the Payment service cannot proceed until Finance answers — a Finance outage becomes a Payment outage (Design A of the Grab-like app). In (b), Payment publishes `InvoicePaid` and returns immediately; the queue holds the message until Finance is back (Design B) — looser coupling bought with eventual processing and more moving parts.

<box type="warning" seamless>

**Pitfall:** defaulting to synchronous REST everywhere because it is familiar. Every synchronous dependency is a failure dependency: if A waits for B, B's downtime and latency budget become A's. The lecture's own when-not-REST table (W6.10) says event-driven workflows are where REST's request–response coupling becomes the problem.

</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Name two synchronous and two asynchronous communication patterns from the lecture.

<panel type="seamless" minimized header="%%Answer%%">

Synchronous: RESTful API over HTTPS, gRPC, GraphQL. Asynchronous: publish-subscribe events; message queues (Kafka, Amazon SNS). (Source: L7 slides 13, 31.)
</panel>

**Q2.** In the Grab-like app, why does Design B keep working while Matching is down?

<panel type="seamless" minimized header="%%Answer%%">

The middleware stores the `BookingRequested` event until Matching becomes available — Booking neither waits nor loses the request; processing is deferred, not dropped. (Source: Quiz 2, Q1.)
</panel>

</panel>

<span id="W7-c5"></span>

### W7.5 Domain-driven design: domain, sub-domain, domain model ★

**Before you can cut services along business lines, you need a vocabulary for the business — that is what domain-driven design provides.** DDD is a domain-centric approach to software design for complex problem domains, a collection of patterns, principles, and practices that keeps the domain model isolated from technical complexities so software closely reflects business needs. (Source: L7 slide 20.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-ddd" trim />
</box>

<panel type="seamless" minimized header="%%Common question: why are microservices often drawn as hexagons?%%">

Because of **hexagonal architecture** (also called **ports and adapters**), one of the common architectures that put the domain at the center (L7-DDD recording, ~[5:00–10:00]):

* The domain model sits at the **center** of the hexagon.
* Everything technical — databases, user interfaces, message queues — connects to that center through **adapters**, which handle the translation.
* The business logic does not depend on those technologies; the adapters do.

Layered architecture expresses the same priority differently (a distinct *domain layer* holds the core business logic, separate from UI, application, and infrastructure), and the modular monolith (W6.4) already divides code by domain. Microservices inherit the hexagon picture: each service has its own domain logic at its core and connects to the outside world — including other services — only through well-defined interfaces. The lecture's example: a supplier service manages suppliers, but must ensure only administrators can add or delete supplier data — it enforces that by *calling a user service through its interface*, never by reaching into the user service's internals (L7-DDD recording, ~[10:00]).

</panel>

**How it works:**

**The {{ term("domain", "the problem space the business occupies — its rules, processes, ideas, and terminology; per the deck it exists regardless of the existence of the business (full definition: L7 slide 32)") }} is the problem space; the domain model is your abstraction of it.** The domain identifies the main business problem you intend to solve — the critical, fundamental concept behind the business, a specific area of functionality or business capability; requirements come from the domain. A {{ term("domain model", "an abstraction of the problem domain containing only the information necessary to solve the problem in this application's context") }} represents a view of that problem domain — an abstraction, not the reality. (Source: L7 slide 17.) "Exists regardless of the business" is meant literally, in the course's own terms: the delivery domain existed before FoC, and it would exist without FoC (L7-DDD recording, ~[24:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-domain-model" trim />
</box>

**Modeling means deciding what to ignore.** The lecture's railway illustration: ignore how deep the tunnel is, the crossover points, the speed of the train — retain stations and interchanges. The model contains only the information necessary to solve the problem in the context of the application. (Source: L7 slide 17.) The payoff of ignoring well: because the tube map keeps stations, connections, and interchanges, you can treat the network as a graph — compute shortest paths, plan routes — "because you modeled the problem at the right level of abstraction" (L7-DDD recording, ~[3:00]).

{% call example("L7-DDD recording, ~[2:00] — students and instructors in the domain, users in the solution") %}
A university course-management domain contains **students** and **instructors** — that is what the problem space has. The implementation may not create a Student class and an Instructor class at all: it may represent everyone as a **User** distinguished by a role. That is a decision on the solution side. The domain describes the problem; the implementation describes the solution — and the domain model is the bridge you design between them.
{% endcall %}

**Complex systems get many models, not one unified model: sub-domains.** When analyzing complex systems, avoid seeking a single unified domain model for the entire system — a complex system is fundamentally a collection of multiple domain models. A sub-domain is a logical separation of the domain: cohesive units of business functionality. The online retailer's sub-domains: product, order, invoicing, shipping, inventory, forecasting. (Source: L7 slides 18–19.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-subdomain" trim />
</box>

**Sub-domain classification decides build, buy, or outsource.** Core sub-domains are the key differentiator and the most valuable part — usually developed in-house. Supporting sub-domains relate to what the business does but are not differentiators — build or outsource. Generic sub-domains are not specific to the business — implemented using off-the-shelf software. (Source: L7 slide 19.)

{% call example("L7 slides 18–19 — the online retailer's six sub-domains") %}
For the online retailer, the lecture maps six sub-domains: product, order, invoicing, shipping, inventory, forecasting — and classifies **product** as the core sub-domain (the differentiator: build in-house), the rest as supporting or generic depending on how differentiating they are (build/outsource — or buy, e.g., a forecasting package). The same analysis tells a microservices team where its scarcest engineering attention belongs: the core.
{% endcall %}

{% call example("L7-DDD recording, ~[5:00] — what is FoC's core sub-domain?") %}
Delivery apps let people order food from restaurants or courier small packages — so *handling delivery* is not what makes FoC valuable. The value is in managing the **errand lifecycle**: courier–requester matching, and credit escrow and settlement. Errand and credit management are therefore FoC's core sub-domain — "the unique selling point" that must be designed and built carefully. At the other end of the classification: authentication, which every application needs but no application needs custom-built (a third-party service such as Google Sign-in would do), is generic. The classification tells you what you must build, what you can buy or outsource, and where to invest your best engineering effort.
{% endcall %}

**Keeping the domain model isolated from technical complexity is older than microservices — layered, modular monolith, and hexagonal architectures all express it.** You do not start by saying "we have a team of database developers, so let's build database components"; you start by asking what the domain needs, then build solutions for those needs. (Source: L7-DDD recording, ~[6:00].)

{% call example("L7-DDD recording, ~[7:00] — ports and adapters: why microservices are drawn as hexagons") %}
In {{ term("hexagonal architecture", "ports and adapters: the domain model sits at the center, and every technical concern connects to it through adapters — Cockburn, 2005") }}, the domain model sits at the center of the hexagon; databases, user interfaces, and message queues connect to that center through **adapters** that do the translation, so the business logic does not depend on those technologies. This is why microservices are so often drawn as hexagons: each service keeps its domain logic at its core and touches the outside world — including other services — only through well-defined interfaces. The lecture's course example: the supplier service must ensure only administrators can add or delete supplier data, and it does so by *calling the user service through its interface* — never by reaching into the user service's internals.

%%Hexagonal architecture (ports and adapters) is Alistair Cockburn's (2005): [alistair.cockburn.us/Hexagonal-architecture](https://alistair.cockburn.us/hexagonal-architecture/).%%

{% endcall %}

The diagram decomposes one business domain into classified sub-domains.

<mermaid>
flowchart LR
  dom(["Domain: online retailer (problem space)"])
  dom --> prod["Product — core: build in-house"]
  dom --> order["Order — supporting: build or outsource"]
  dom --> inv["Invoicing — supporting: build or outsource"]
  dom --> ship["Shipping — supporting: build or outsource"]
  dom --> stock["Inventory — supporting: build or outsource"]
  dom --> fc["Forecasting — generic: buy off-the-shelf"]
</mermaid>

%%Notation: the rounded box is the domain (the whole problem space); rectangles are sub-domains (cohesive units of business functionality); each label carries the lecture's classification and the build/buy decision it drives. The deck fixes only Product = core; the supporting/generic labels on the other five apply slide 19's build/buy logic to this retailer — another business could classify the same sub-domain differently.%% To read it: the retailer does not model "retail" as one thing — it cuts the problem space into cohesive pieces, then spends in-house engineering where the business differentiates (product) and buys where it does not (forecasting). Those seams are the candidates for microservice boundaries in W7.8.

<box type="warning" seamless>

**Pitfall:** modeling the whole business as one model "for consistency". The lecture's warning is explicit — a complex system is a collection of multiple domain models; forcing a single unified model couples every future change to every other.

</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Distinguish domain, sub-domain, and domain model in one line each.

<panel type="seamless" minimized header="%%Answer%%">

Domain: the problem space the business occupies — rules, processes, ideas, terminology (L7 slide 32: it exists regardless of the existence of the business). Sub-domain: a cohesive logical separation of that domain (product, order, invoicing…). Domain model: the abstraction of (a view of) the domain or sub-domain containing only what the application needs.
</panel>

**Q2.** Your team's forecasting module is useful but identical across companies. Build or buy, and which sub-domain class is that?

<panel type="seamless" minimized header="%%Answer%%">

Buy — it is a generic sub-domain: not specific to the business, implemented using off-the-shelf software. (Source: L7 slide 19.)
</panel>

</panel>

<span id="W7-c6"></span>

### W7.6 Bounded contexts and the ubiquitous language ★

**Sub-domains are problem-space slices; bounded contexts are where they become buildable — and where a shared language makes them ownable by one small team.** The lecture pairs the two deliberately: a sub-domain is closely aligned with its bounded context. (Source: L7 slide 21.) Close alignment is the *ideal* — "close alignment usually indicates that the modeling has been done well" — but it is not always the reality: one e-commerce bounded context can cover several sub-domains (L7-DDD recording, ~[10:00, ~28:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-bounded-context" trim />
</box>

**How it works:**

**A bounded context lets a sub-domain be implemented and executed at runtime: the sub-domain lives in the problem space (the business as it is), and the bounded context is where it lands in the solution space (the software you build).** In the errand platform, the user-management sub-domain (identity and access) becomes a bounded context containing what a login needs: username, password, one-time code — the model exists *inside* the boundary. (Source: L7 slide 21.)

**A {{ term("ubiquitous language", "a shared business-terms language used by domain experts and developers in conversation, requirements, design, and code — scoped to one bounded context") }} has one meaning per term inside a context — and the same word may mean something else in another.** "Customer" in the Sales context is not "Customer" in the Support context; the language is scoped to a bounded context. (Source: L7 slide 22.) The lecture's edge-detector: *when a term starts to mean different things to different people, you have probably found the edge of a bounded context* (L7-DDD recording, ~[12:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-ubiquitous-language" trim />
</box>

**The language must reach the code — if a name isn't a term the domain expert would recognize, rename it.** The lecture's example makes business jargon explicit in code: `Guaranteed30MinuteDeliveryOffer.after(PizzaDelivered)` sends a coupon to the customer when delivery time exceeds thirty minutes — business expert jargon, ubiquitous language, and technical jargon meeting in one class name. (Source: L7 slide 23.) The recorded segment walks the full loop: the developer describes the rule *back to the expert in business words* — "a pizza is delivered; was the guaranteed 30-minute delivery offer time exceeded? if yes, send a coupon to the customer" — no database tables, no status codes, so the expert can follow it and confirm it is right; when both sides use the same words, misunderstandings surface early, before they become bugs. And the language is built deliberately: the team keeps business terms that give insight into the model and drops terms from either side that do not help solve the problem. (L7-DDD recording, ~[11:00–12:00].)

**Contexts must collaborate, and the lecture names the patterns.** Capture the collaborations between bounded contexts (online retail store: Authentication, Fulfillment, Product catalog, Checkout, Payment, Accounting). Two contexts developed independently but jointly owning a small shared part of the model is a **shared kernel** (a common-coupling alert — W4.6); a provider–consumer split is **upstream–downstream** (Order context publishes an Order API; the Recommendation context fetches order information). (Source: L7 slides 24–25.) The lecture's contrast makes the shared kernel non-trivial: let the Recommendation context read the Order database directly and you no longer have a shared kernel — you have a {{ term("shared database", "two contexts coupled through one database — an anti-pattern in large applications; defined in Week 8") }}, coupled through storage rather than through an agreed model: if the order team changes the schema, Recommendation breaks without warning, and the order team may not even know it has a dependent. (L7-DDD recording, ~[15:00].)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-shared-kernel" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-upstream-downstream" trim />
</box>

**Downstream strategies: conform, or ask the upstream to accommodate.** In a **conformist** relationship the downstream adopts the upstream's published model as-is, with no influence over the format; in a **supplier–customer** relationship the upstream designs the API with the downstream's needs in mind. (Source: L7 slide 26.) The lecture's conformist example is a *published order store*: the Order context publishes a fixed view — order ID, customer ID, quantity, SKU — as a published copy separate from its internal database (so this is not the shared database above), and the Recommendation context adapts its own logic to that model. The difference between the two strategies is *influence*: in supplier–customer the downstream can shape the interface; in conformist it cannot. And the upstream–downstream payoff: the Order context can change its internal storage freely as long as the API stays the same. (L7-DDD recording, ~[16:00–17:00].)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-conformist" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-supplier-customer" trim />
</box>

**How contexts interact should model how the real domain interacts — how we do it matters.**
When Order Processing hands fulfillment data to the Warehouse:

- Sharing the *entire* order structure is {{ term("stamp coupling", "one component passes an entire data structure to another that needs only part of it") }}
- Sharing just the needed order fields (and only then the customer information) is {{ term("data coupling", "components share only the specific data items actually needed") }}
- Decoupling fully, Order Processing can produce an `OrderPlaced` **event** that the Warehouse consumes — reacting when the event is seen

(Source: L7 slides 27–30.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-stamp-coupling" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-data-coupling" trim />
</box>

{% call example("L7 slides 27–30 + L7-DDD recording, ~[18:00–22:00] — four ways to tell the warehouse about an order") %}
A customer places an order; the warehouse must pick, package, and send items. Option (a): pass the **entire order structure** — customer ID, payment value, card number, items — stamp coupling; the warehouse receives data it has no use for (the payment details are a needless security exposure), and it now depends on the *whole record's structure*, so any field the order team adds, removes, or renames can break it even if it never uses that field. Option (b): share **just the order information** the warehouse needs — customer ID and items; the payment information no longer leaves the order context (data coupling), though the warehouse still calls the customer service for the shipping address. Option (c): order processing **fetches the customer information itself** and sends one *pick-and-send* instruction — name, address, email, items; the warehouse no longer depends on the customer service at all, and every element in the instruction is something it uses — still data coupling, but one dependency fewer; the interaction is still synchronous, so a slow or unavailable warehouse holds up order processing. Option (d): Order Processing **produces an `OrderPlaced` event** whose payload carries the destination and the items; the Warehouse subscribes and reacts — no call, no wait, producer and consumer need not know about each other or be available at the same time, and *any other context* interested in new orders can subscribe without Order Processing changing a line. The loosest option, and the one that matches how the real domain works: the warehouse does not ask for orders; it reacts to new ones.
{% endcall %}

<box type="warning" seamless>

**Pitfall:** letting one context's model leak into another's. A shared kernel is a deliberate, small, jointly-owned subset — not an excuse for common coupling across the system; and when the upstream will not accommodate you, the conformist choice (adopt its model as-is) is still cheaper than a translation layer nobody maintains.

</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Why is "Customer" allowed to mean two different things in one system?

<panel type="seamless" minimized header="%%Answer%%">

Because a ubiquitous language is scoped to a bounded context: within one context each term has one meaning; the same word can mean something else in another context (Sales-Customer vs Support-Customer).
</panel>

**Q2.** Which context-interaction option from the lecture has the loosest coupling, and what does it cost?

<panel type="seamless" minimized header="%%Answer%%">

Option (d) — Order Processing publishes an `OrderPlaced` event that the Warehouse consumes: no direct call, no shared structure. The cost is asynchronous processing (the warehouse reacts when it sees the event) and the infrastructure to carry events (L7 slide 31: pub-sub or message queues).
</panel>

</panel>

<span id="W7-c7"></span>

### W7.7 Aggregates: the consistency unit of DDD ★★

**Inside a bounded context, the aggregate is the unit you may change atomically — get it wrong and either your data is inconsistent or your locks are everywhere.** The lecture calls the aggregate "the consistency unit in DDD". (Source: L7 slide 33.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-aggregate" trim />
</box>

**How it works:**

**An aggregate is a hierarchy of entities — business objects the system tracks individually, each with its own identity — with a root.** An entity is an object with its own identity that *persists over time* — an order, a support ticket (L7-DDD recording, ~[25:00]). The aggregate root is the parent entity of the cluster and its public interface; everything outside interacts through it. (Source: L7 slide 33.)

**The boundaries are two boundaries in one.** The consistency boundary: from a visibility and operation perspective, all processes or objects external to the aggregate may only *read* its state — state can only be modified by executing methods of the aggregate's public interface. The transactional boundary: from a transaction perspective, any change to the aggregate either all succeeds or none succeeds. (Source: L7 slide 33.)

**A well-designed aggregate comes from the business and is cohesive.** It is derived from a business requirement and has high functional cohesion — e.g., Ticket in the Ticket service, where one Ticket aggregates its Messages and Attachments. (Source: L7 slide 33.)

{% call example("L7 slide 33 + L7-DDD recording, ~[26:00] — the Ticket service's Ticket aggregate") %}
In the Ticket service, the aggregate is **Ticket** (the root): one Ticket holds `1..*` (UML for "one or more") Messages and their Attachments. External code may read the ticket and its messages, but to add a message it must call the Ticket's public interface — never insert into the message list directly. The transactional boundary in the lecture's words: "if adding a message with two attachments fails halfway, none of the change is kept" — no message, no attachments. If "close ticket and archive attachments" is one operation, the transactional boundary guarantees it all happens or nothing does — tickets are never left half-closed.
{% endcall %}

**Aggregates and bounded contexts are both "collections of things" — but the things are fundamentally different.** The lecture's mnemonic: *aggregates are what you work with; bounded contexts are what you are trying to do* — aggregates define the business entity models (the central business objects, with their data and rules) inside a bounded context, and bounded contexts implement business sub-domains. (Source: L7 slide 34; L7-DDD recording, ~[28:00].)

<box type="warning" seamless>

**Pitfall:** treating every entity as its own aggregate. If Message were an aggregate root, "close ticket" could not be one transaction, and invariants — rules that must hold at every moment — spanning ticket and messages ("a closed ticket has no open messages") would live outside any boundary — the exact inconsistency the aggregate exists to prevent.

</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** State the two boundaries of an aggregate and what each one guarantees.

<panel type="seamless" minimized header="%%Answer%%">

Consistency boundary: outsiders only read; state changes only via the aggregate root's public interface (visibility/operation perspective). Transactional boundary: any change all-succeeds or none-succeeds (transaction perspective).
</panel>

**Q2.** Why is Ticket (not Message) the right root in the Ticket service?

<panel type="seamless" minimized header="%%Answer%%">

The business operations and invariants belong to the ticket as a whole (closing a ticket affects its messages and attachments); a well-designed aggregate is derived from a business requirement and has high functional cohesion — Ticket is that unit.
</panel>

</panel>

<span id="W7-c8"></span>

### W7.8 Identifying microservices: DDD and event storming ★★

**Ad-hoc service boundaries drift into scope creep (functionality silently expanding beyond what was planned), low cohesion, and high coupling — the lecture's answer is to derive boundaries from the domain, then confirm them with event storming.** (Source: L7 slides 16, 37.) The recorded segment starts from the anti-pattern itself: a reasonable-looking start is to group backlog entries into services — but grouping features ad hoc "can introduce coupling knowingly or unknowingly"; the service accumulates responsibilities that do not belong to it, and as it does, its cohesion drops and its coupling with the rest of the system rises (L7-DDD recording, ~[0:30]).

**How it works:**

**Three DDD constructs feed service identification.** Use sub-domains: each subdomain corresponds to a different part of the business — define services corresponding to subdomains (the online store's product catalog, inventory management, order management, delivery management). Use bounded contexts: microservices are bounded contexts — with the caution that **not all bounded contexts are necessarily microservices**, and some have wide functionalities. Use aggregates: a well-designed aggregate exhibits many characteristics of a well-designed microservice — derived from business requirements, high functional cohesion, typically loosely coupled. (Source: L7 slide 35.)

**Then apply the {{ term("single-responsibility principle", "each service should have only a small set of responsibilities") }} (SRP) and decompose deliberately.** Each service should have only a small set of responsibilities. Decompose by **verb or use case** — a Shipping service responsible for shipping complete orders; or by **noun/resource** — an Account service responsible for all operations on user accounts. Also consider team size, technologies, and scalability/availability/security requirements; it is possible to further decompose a service, or to combine two into one. (Source: L7 slide 36.) You also have discretion in how you draw the contexts themselves: the recorded segment's online store groups **Checkout and Fulfillment** into one bounded context, "perhaps because they are implemented in the same code base and changed together" — apply SRP to keep contexts small, well-defined, and focused, since how you draw the boundaries reflects how you will implement the system (L7-DDD recording, ~[14:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-single-responsibility-principle" trim />
</box>

**{{ term("Event storming", "a lightweight workshop that traces commands → aggregates → events → policies to find service boundaries — full treatment in Week 8") }} finds the same boundaries from the dynamics side.** A lightweight, industry-common process (Source: L7 slides 38–41):

- **Domain events** are events that occur in the domain and matter — they record state changes. They represent *facts*: the record that something did happen — and in microservices they often become the integration points between services (L7-EventStorming recording, ~[3:00]).
- **Commands** cause the events and are issued by a user or an external system. They represent *intent* — the desire to make something happen — and they often cross service boundaries as API calls or messages that initiate a business process (L7-EventStorming recording, ~[3:00–4:00]).
- A command works **on an aggregate** to make an event happen. The aggregate holds the business rules and validation logic: a *Confirm order* command operates on the order-processing aggregate, which validates the order, checks inventory, calculates totals — and only when everything is valid does it produce an *Order confirmed* event (L7-EventStorming recording, ~[4:00]).
- A **policy** links events back to commands — *when* the payment card is submitted, *then* confirm the order. This has to happen in sequence: the order cannot be confirmed until the payment is secured — a business rule governing how the system behaves (L7-EventStorming recording, ~[5:00]).

**A policy that crosses a cluster boundary is a boundary candidate — and the event's payload tells you what data crosses it.** The lecture: when you see a policy connecting an event from one context to a command in another context, "you're seeing a potential boundary between microservices" — and the event must carry enough for the consuming context to act (the *payment authorized* event must say *which order* to confirm), which is how event schemas get designed. (Source: L7-EventStorming recording, ~[6:00].)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-domain-event" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-policy" trim />
</box>

**Drawing the boundaries is the payoff.** Draw boundaries that delimit each consistent context — the relations and communication between contexts follow, and **these boundaries give you microservice boundaries**. A bounded context solves one problem and can contain more than one aggregate: the lecture's example puts an **order aggregate** and a **shipment aggregate** in the same order-management bounded context, because they share a ubiquitous language and collaborate closely to deliver one capability (managing customer orders from placement through delivery) — group aggregates into a context when they change together and deliver value together. (Source: L7 slide 42; L7-EventStorming recording, ~[8:00].)

**Event storming is a discovery process — "brainstorming with events" — not a transcription of what you already know.** Working the event timeline with domain experts uncovers edge cases, missing workflows, and hidden complexity, surfacing requirements that might otherwise be discovered only late in development. (Source: L7-EventStorming recording, ~[9:00].)

**And the cautions the lecture stamps on the whole method.** (Source: L7 slide 43):

- Start with business events, not CRUD (create, read, update, delete — the basic data-table operations) — focus on domain events from real business needs, not technical data operations. The recorded segment's upgrade: instead of an *update user* operation, storm *password changed* or *shipping address modified* — business-centric events carry the intent that CRUD lacks (L7-EventStorming recording, ~[9:00]).
- Not always true: one aggregate = one microservice.
- Not always true: one bounded context = one microservice — aggregates and bounded contexts *inform* service boundaries but don't map 1:1 always. Nor should you split just because you have multiple aggregates: every extra boundary buys networking calls, eventual consistency, and distributed-transaction overhead — weigh the costs and benefits (L7-EventStorming recording, ~[10:00]).
- Group by business capability and cohesion.
- Microservice boundaries evolve over time. The lecture calls your storming output "a hypothesis, an informed starting point": split or merge services as production teaches you, and make the boundary decisions consciously, on evidence and clear reasoning — "rather than by accident or by blindly following rules like one aggregate, one service" (L7-EventStorming recording, ~[10:00]).

{% call example("L7 slides 38–42 — storming the errand platform's credit flow") %}
Work the wall left to right. Domain event: `CreditsTransferred` (records a state change in the credit ledger — the running record of each account's credit balance and transfers). What caused it? A command, `Transfer credits`, issued after an errand is completed. What did the command act on? The **Credit aggregate** (root: the credit account). What policy follows? *When* `ErrandCompleted` *then* `Transfer credits` — one event triggering another command. And the policy fixes the payload: `ErrandCompleted` reaching the credit context must identify the errand and the two parties — the payload *is* the data contract across that boundary. When the same wall shows credit events clustering separately from errand-matching events and catalogue events, draw boundaries around each consistent cluster: those bounded contexts — errand matching, credit, catalogue — are the microservice boundary candidates, exactly the seams the W7.3 trade-off discussion weighed.
{% endcall %}

The diagram reads one stripe of an event-storming wall left to right.

<mermaid>
flowchart LR
  u(["User /<br>external system"]) -->|"issues"| cmd["Command:<br>Transfer credits"]
  cmd -->|"acts on"| agg["Aggregate:<br>Credit account"]
  agg -->|"records"| ev["Event:<br>CreditsTransferred"]
  ev -.->|"policy: when<br>CreditsTransferred<br>then Confirm order"| cmd2["Command:<br>Confirm order"]
</mermaid>

%%Notation: the rounded box is the actor, rectangles are command/aggregate/event artifacts, solid arrows show causation, and the dashed arrow is a policy linking one event to the next command.%% To read it: a user or external system issues `Transfer credits`; the command acts on the Credit aggregate (the consistency unit from W7.7) and produces `CreditsTransferred`; the policy "when CreditsTransferred then Confirm order" fires the next command — chains of exactly this shape, drawn on one wall, are what event storming produces; where the chains cluster consistently, you draw a boundary, and that boundary is a microservice candidate.

<box type="warning" seamless>

**Pitfall:** mapping aggregates or bounded contexts 1:1 onto services. The lecture repeats the caution twice: a bounded context may contain multiple aggregates; boundaries inform services, they do not *equal* them — group by business capability and cohesion, and expect boundaries to evolve over time.

</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Give one verb-based and one noun-based service decomposition from the lecture.

<panel type="seamless" minimized header="%%Answer%%">

Verb/use case: a Shipping service responsible for shipping complete orders. Noun/resource: an Account service responsible for managing user accounts. (Source: L7 slide 36.)
</panel>

**Q2.** In event storming, what are the roles of a command, an event, an aggregate, and a policy?

<panel type="seamless" minimized header="%%Answer%%">

Command: issued by a user or external system; causes events. Event: a domain-relevant state change. Aggregate: the cluster of objects the command acts on to make the event happen (the consistency unit). Policy: the "when event then command" rule linking one event to the next command (e.g., when the payment card is submitted, then confirm the order).
</panel>

**Q3.** Why does the lecture warn against starting event storming from CRUD operations?

<panel type="seamless" minimized header="%%Answer%%">

Because command/event must come from a business need: CRUD items are technical data operations, not domain events — starting from them produces technical boundaries instead of business-capability boundaries.
</panel>

**Q4.** What does a policy connecting an event in one context to a command in another tell you?

<panel type="seamless" minimized header="%%Answer%%">

That you are looking at a potential boundary between microservices — the policy crosses two contexts' concerns — and the event's payload (it must carry enough for the consuming context to act, e.g., *which order* to confirm) defines the data contract across that boundary. (Source: L7-EventStorming recording, ~[6:00].)
</panel>

</panel>

<box type="info" seamless>

**Section summary:**

* **Microservices = independently deployable, loosely coupled, small-team-owned services organized around business capabilities**, entered via an API gateway (W7.1–W7.2).
* **Every buy has a price**: independent deployability/scaling/availability vs network-hop performance, data-integrity risk, and observability complexity (W7.3).
* **Communication is a design decision**: synchronous REST/gRPC/GraphQL couples caller and callee; events and queues defer and decouple (W7.4).
* **DDD supplies the seams**: domain → sub-domains (core/supporting/generic) → bounded contexts with a ubiquitous language → aggregates as consistency units (W7.5–W7.7).
* **Boundaries come from the domain, not the org chart or the ER (entity–relationship — database-schema) diagram**: sub-domains + bounded contexts + aggregates, verified by event storming, grouped by capability — never mapped 1:1 by formula (W7.8).

</box>

## Connections

| Concept | Lecture | Tutorial | Other weeks |
|---|---|---|---|
| Microservice style; four characteristics | L7 slides 3–10 | — | W5 (microservices as cloud-native enablers), W6.1 (taxonomy quadrant) |
| Trade-offs monolith vs microservices | L7 slides 11–15 | — | W6.4 (modular monolith), W12 (scaling), Quiz 2 Q4–Q5 |
| Sync vs async communication; deployment patterns | L7 slides 11–13, 31 | — | W6.8–W6.10 (REST + when-not-REST), W9 (EDA), W10 (async), Quiz 2 Q1 |
| Domain, sub-domain, domain model; core/supporting/generic | L7 slides 17–20 | — | W3 (requirements from the domain) |
| Bounded contexts, ubiquitous language, context collaboration | L7 slides 21–32 | — | W4 (coupling — stamp/data coupling), W8 (microservices II) |
| Aggregates (root, consistency/transactional boundaries) | L7 slides 33–34 | — | W8 (microservices II) |
| Identifying services; event storming | L7 slides 16, 35–43 | — | W9 (events), Quiz 2 (service design items) |

## Further reading

* Chris Richardson & Floyd Smith, *Microservices: From Design to Deployment* — the lecture's cited source for the style characteristics (L7 slide 7).
* Eric Evans, *Domain-Driven Design* — the reference the lecture cites (L7 slide 4).
* Scott Millett, *The Anatomy of Domain-Driven Design* (L7 slide 4): [leanpub.com/theanatomyofdomaindrivendesign](https://leanpub.com/theanatomyofdomaindrivendesign)
* Event storming, as practiced in industry (L7 slide 38): [eventstorming.com](https://www.eventstorming.com/)

## Summary

**Key takeaways:**

* **The microservice style structures one application as a suite of small, independently deployable services** — organized around business capabilities, loosely coupled, owned by small teams — typically fronted by an API gateway. (W7.1)
* **Boundaries follow business capabilities, and cohesion is the test** — each service is one well-defined capability with a small team owning its whole lifecycle. (W7.2)
* **Splitting trades costs for buys**: deployability, scalability, availability gained; network-hop performance, data integrity, and observability complexity paid — decide per system (the errand platform's exactly-once credits). (W7.3)
* **Communication style is architectural**: synchronous calls couple caller and callee; events and queues let a down Matching service miss nothing (the Grab-like Design B). (W7.4)
* **DDD starts from the problem space**: domain → sub-domains classified core/supporting/generic (build/buy/outsource) → domain models that deliberately ignore most of reality. (W7.5)
* **Bounded contexts make sub-domains buildable**, each with its own ubiquitous language and named collaboration patterns (shared kernel, upstream–downstream, conformist, supplier–customer) — with data coupling preferred over stamp coupling, events loosest of all. (W7.6)
* **Aggregates are the consistency unit**: a root plus consistency and transactional boundaries, derived from business requirements. (W7.7)
* **Service boundaries are derived, then verified**: sub-domains, bounded contexts, and aggregates inform them; event storming (commands → aggregates → events → policies) confirms them; none of the mappings is 1:1, and boundaries evolve. (W7.8)

**Key terms:**

| Term | Definition | Unit |
|---|---|---|
| Microservice | An independently deployable service modeled around a business domain, owned by a small team | [W7.1](#W7-c1) |
| Microservice architecture | The style structuring an application as a collection of such services forming one solution | [W7.1](#W7-c1) |
| API gateway | The single entry point routing client requests to the services behind it (defined in Week 8) | [W7.1](#W7-c1) |
| Business capability | Something the business does that delivers value — the unit microservice boundaries align with | [W7.2](#W7-c2) |
| Two-pizza team | A small cross-functional team, small enough that two pizzas feed it, owning its services' whole lifecycle | [W7.2](#W7-c2) |
| Loose coupling | Depending on others only through small published interfaces — no shared internals | [W7.2](#W7-c2) |
| Conway's Law | Organizations produce designs that copy their communication structures — the product mirrors the teams | [W7.2](#W7-c2) |
| Service instance per host | Run each service instance in isolation on its own host | [W7.3](#W7-c3) |
| Service instance per container | Run each service instance in its own container, packaged as a container image | [W7.3](#W7-c3) |
| Service instance per VM | Package each service as a VM image (e.g., an Amazon EC2 AMI) and launch instances from it | [W7.3](#W7-c3) |
| Domain-driven design (DDD) | Domain-centric design approach keeping the model isolated from technical complexity | [W7.5](#W7-c5) |
| Domain model | An abstraction of the problem domain with only the information the application needs | [W7.5](#W7-c5) |
| Hexagonal architecture | Ports and adapters: the domain model at the center, technical concerns connected through adapters | [W7.5](#W7-c5) |
| Sub-domain | A cohesive logical separation of the domain — core, supporting, or generic | [W7.5](#W7-c5) |
| Bounded context | The explicit boundary within which a domain model exists (solution space) | [W7.6](#W7-c6) |
| Ubiquitous language | Shared business-terms language, scoped to one bounded context | [W7.6](#W7-c6) |
| Shared kernel | Two independently developed contexts jointly own a small shared subset of the model | [W7.6](#W7-c6) |
| Upstream–downstream | Provider–consumer collaboration: the upstream publishes an API, the downstream fetches it | [W7.6](#W7-c6) |
| Conformist | The downstream adopts the upstream's published model as-is, no influence over the format | [W7.6](#W7-c6) |
| Supplier–customer | The upstream designs the API with the downstream's needs in mind | [W7.6](#W7-c6) |
| Stamp coupling | Passing an entire data structure where the receiver needs only part of it | [W7.6](#W7-c6) |
| Aggregate | A cluster of objects changed as one unit — root plus consistency and transactional boundaries | [W7.7](#W7-c7) |
| Single-responsibility principle | Each service has only a small set of responsibilities; decompose by verb or by noun | [W7.8](#W7-c8) |
| Domain event | An event occurring in the domain that matters — a record of a state change, from a business need | [W7.8](#W7-c8) |
| Policy | The "when event then command" rule linking one event to the next command | [W7.8](#W7-c8) |
| Event storming | Lightweight workshop tracing commands → aggregates → events → policies to find boundaries (defined in Week 8) | [W7.8](#W7-c8) |

%%Next: [Week 8]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html) continues microservices (II), building on the seams you can now find — how services are realized, owned, and operated once the boundaries from W7.8 are drawn.%%
</div>
