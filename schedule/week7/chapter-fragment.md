{% from "schedule/macros-fragment.md" import term, example with context %}
<h2 id="title">Week 7 — Microservices (I)</h2>

<span id="prereqs">

**Prerequisites:** [Week 4 — Architecture (I)]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html) (coupling and cohesion, modular monolith) and [Week 6 — Architecture (II) & REST]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html) (the style taxonomy, REST as the service communication style). Week 5's containers are the deployment backdrop for independent deployability.
</span>

<span id="outcomes">

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

<div id="body">

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

## Core concepts

<span id="W7-c1"></span>

### W7.1 The microservice architectural style ★

**When one application grows too large for one team, one codebase, and one deployment, the microservice style is the lecture's structural answer.** The lecture sets the scene with the question: what happens when the system becomes too large for a single application? A large codebase, slow deployment, multiple teams involved, and scaling issues — no independent scaling. (Source: L7 slide 3.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-microservice-architecture" trim />
</box>

**How it works:**

**A microservices application is a single application delivered as a suite of small services.** Each microservice offers a well-defined business capability; each is developed and deployed independently; and the services communicate through well-defined mechanisms and published interfaces. (Source: L7 slide 5.)

**The building blocks are a collection of small networked services — each with a limited scope — that work with each other.** Together they form the bigger solution: the lecture notes real systems run 1000+ microservices. (Source: L7 slide 6.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-microservice" trim />
</box>

**Four characteristics define the style: organized around business capabilities, loosely coupled, owned by a small team, independently deployable.** (Source: L7 slide 7 — after Richardson & Smith, *Microservices: From Design to Deployment*.) W7.2 develops the first and third; W7.3 the costs and buys; W7.4 the communication.

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

Organized around business capabilities; loosely coupled; owned by a small team; independently deployable. (Source: L7 slide 7.)
</panel>

**Q2.** What four pressures does the lecture list as the moment to consider splitting a monolith?
<panel type="seamless" minimized header="%%Answer%%">

Large codebase; slow deployment; multiple teams involved; scaling issues (no independent scaling). (Source: L7 slide 3.)
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

**Services are owned by small teams that own the whole lifecycle.** Service decisions are independently made and handled by small teams; the lecture cites Amazon's two-pizza teams — small enough that two pizzas feed them; cross-functional, organized around capabilities, and owning the whole lifecycle of their services. (Source: L7 slide 10.)

**Independence has a technical face: services share no code or implementation.** Services do not need to share any of their code with other services, and there is minimal dependence on each other — loose coupling by construction. (Source: L7 slides 7 and 10.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-loose-coupling" trim />
</box>

{% call example("L7 slides 8–9 — the mom-and-pop retailer goes online") %}
A brick-and-mortar retailer switches to online retail. The **domain** is everything from warehouse to reception desk, finance to ordering. The **warehouse** manages orders being shipped out, returns, and new stock — and may expose the capability "get a current stock list"; **finance** manages payroll, produces reports, and manages company accounts — exposing "monthly accounts" or "set up payroll for a new recruit". Each area is a business capability first; the services that implement them (e.g., Order, Payment, Checkout) inherit those boundaries, and each is cohesive — every feature inside it relates to that capability.
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

**The buys: deployability, scalability, and availability.** Deployability — separate deployables and pipelines; ship the credit service without updating supplier services. Scalability — the service is the unit of scaling; scale the order service during peak periods. Availability — fault isolation and redundancy; a down supplier service doesn't impact credit settlement. (Source: L7 slide 14.)

**The costs: performance, integrity, and complexity.** Performance — latency and timeouts: every call is a network hop, and a down service keeps others waiting. Integrity — each service owns its data, and potential data duplication causes inconsistencies. Complexity — distributed debugging and the need for observability: with *n* services you get *n* logs, so traceability is harder. (Source: L7 slide 14.)

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

How to read it: walk it with Quiz 3's platform: the team *already* has the modular-monolith top panel — search, reservation, notification as modules over one {{ term("ACID", "the transaction properties — atomic, consistent, isolated, durable: a transaction's changes apply all-or-nothing across everything it touches") }} transaction. Moving down changes three practical things: deploys go from one unit to three (search can be scaled alone — Quiz 3 Q1's answer); data goes from one transaction that is atomic, consistent, isolated, durable — all-or-nothing across modules — to per-service stores whose cross-service atomicity must be *designed* (Quiz 3 Q2 says: don't split while cross-module atomicity cannot be relaxed and no design has yet demonstrated how to preserve it); and ownership splits per capability (Quiz 3 Q3's coordination pain). The diagram shows structure, not superiority — the bottom panel is only better when those three costs buy something you need. (Structure after L5 slides 23–25, Dell guest lecture, and L9 slide 26; the data angle is W5.3's diagram.)

**Independently deployable does not mean centrally hosted: each service carries its own deployment, resource, scaling, and monitoring requirements.** The lecture names three deployment patterns — service instance per host (each instance isolated on its own host), service instance per container (each instance in its own container image — the Week 5 mechanism), and service instance per VM (each service packaged as a VM image, e.g., an Amazon EC2 AMI — Amazon Machine Image). (Source: L7 slides 11–12.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-service-instance-per-host" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-service-instance-per-container" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-service-instance-per-vm" trim />
</box>

{% call example("L7 slide 15 — the errand platform (FoC): does splitting help or hurt?") %}
Assume the errand platform was designed as a modular monolith, and the team considers microservices because of four observed drivers: (1) errands see **20× traffic during lunch**, while the supplier catalogue is quite static; (2) the **credit mechanism undergoes changes** (e.g., implementing paid credits) while other mechanisms stay unchanged; (3) after errand completion, **credits should be transferred exactly once** — and splitting moves from a single DB to multiple DBs; (4) deployment moves from one VM to multiple containers. Weighing them: (1) argues for splitting (independent scaling of the errand service); (2) argues for splitting (independent deployability of credit); (3) argues against (exactly-once is easy in one database, hard across several — the integrity cost); (4) is neutral-to-costly (more moving parts to orchestrate). The verdict depends on which costs your requirements cannot afford — which is the point of the exercise.
{% endcall %}

<box type="warning" seamless>
**Pitfall:** collecting the buys and ignoring the price. The errand platform's exactly-once credit transfer is the lecture's warning: splitting one database into many converts a local transaction into a distributed one. If your hardest requirement is integrity rather than scale or release speed, the monolith may be the *right* answer — "monolith" is a deployment choice, not a defect (W6.4).
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

**{{ term("Synchronous", "communication where the caller waits for the callee's answer before moving on — defined in full in Week 10") }} patterns: the caller waits.** RESTful APIs over HTTPS, gRPC services (glossed in W6.10's alternatives table), GraphQL interfaces (an API style where the client asks for exactly the fields it needs in one query) — the lecture's list for request-style integration between services. (Source: L7 slide 13.)

**{{ term("Asynchronous", "communication where the sender moves on without waiting — events and message queues; defined in full in Week 10") }} patterns: the caller moves on.** Event-based communication — e.g., publish-subscribe events — and message queues (the lecture names Kafka and Amazon SNS — Amazon's managed publish–subscribe notification service — in the bounded-context integration slide). (Source: L7 slides 13 and 31.)

{% call example("L7 slide 13 — one invoice, two interaction styles") %}
A Payment service handles an invoice held by the Finance service. **(a) Synchronous:** the Payment service sends `InvoicePaid` as a request via the API, initiating a state transition in the invoice — Finance must be up and answer. **(b) Asynchronous:** the invoice changes state when it *receives an event*; Payment publishes to a queue and Finance consumes it when it can — neither waits for the other.
{% endcall %}

{% call example("Quiz 2 Q1 — the Grab-like app: what survives a two-minute crash?") %}
In a Grab-like ride-hailing app, **Design A**: Booking makes a synchronous call-and-return to Matching. **Design B**: Booking publishes a `BookingRequested` event to the middleware. When the Matching component crashes for two minutes at peak, **Design B offers reliability by storing the event in the middleware until Matching becomes available** — Booking is never blocked, nothing is lost. In Design A, Booking's call fails or hangs while Matching is down: the synchronous dependency chain is the availability cost W7.3 named. (Source: Quiz 2, Q1.)
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

**How it works:**

**The {{ term("domain", "the problem space the business occupies — its rules, processes, ideas, and terminology; it exists regardless of the software (defined in full in Week 8)") }} is the problem space; the domain model is your abstraction of it.** The domain identifies the main business problem you intend to solve — the critical, fundamental concept behind the business, a specific area of functionality or business capability; requirements come from the domain. A {{ term("domain model", "an abstraction of the problem domain containing only the information necessary to solve the problem in this application's context") }} represents a view of that problem domain — an abstraction, not the reality. (Source: L7 slide 17.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-domain-model" trim />
</box>

**Modeling means deciding what to ignore.** The lecture's railway illustration: ignore how deep the tunnel is, the crossover points, the speed of the train — retain stations and interchanges. The model contains only the information necessary to solve the problem in the context of the application. (Source: L7 slide 17.)

**Complex systems get many models, not one unified model: sub-domains.** When analyzing complex systems, avoid seeking a single unified domain model for the entire system — a complex system is fundamentally a collection of multiple domain models. A sub-domain is a logical separation of the domain: cohesive units of business functionality. The online retailer's sub-domains: product, order, invoicing, shipping, inventory, forecasting. (Source: L7 slides 18–19.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-subdomain" trim />
</box>

**Sub-domain classification decides build, buy, or outsource.** Core sub-domains are the key differentiator and the most valuable part — usually developed in-house. Supporting sub-domains relate to what the business does but are not differentiators — build or outsource. Generic sub-domains are not specific to the business — implemented using off-the-shelf software. (Source: L7 slide 19.)

{% call example("L7 slides 18–19 — the online retailer's six sub-domains") %}
For the online retailer, the lecture maps six sub-domains: product, order, invoicing, shipping, inventory, forecasting — and classifies **product** as the core sub-domain (the differentiator: build in-house), the rest as supporting or generic depending on how differentiating they are (build/outsource — or buy, e.g., a forecasting package). The same analysis tells a microservices team where its scarcest engineering attention belongs: the core.
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

%%Notation: the rounded box is the domain (the whole problem space); rectangles are sub-domains (cohesive units of business functionality); each label carries the lecture's classification and the build/buy decision it drives.%% To read it: the retailer does not model "retail" as one thing — it cuts the problem space into cohesive pieces, then spends in-house engineering where the business differentiates (product) and buys where it does not (forecasting). Those seams are the candidates for microservice boundaries in W7.8.

<box type="warning" seamless>
**Pitfall:** modeling the whole business as one model "for consistency". The lecture's warning is explicit — a complex system is a collection of multiple domain models; forcing a single unified model couples every future change to every other.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Distinguish domain, sub-domain, and domain model in one line each.
<panel type="seamless" minimized header="%%Answer%%">

Domain: the problem space the business occupies — rules, processes, ideas, terminology (exists regardless of the software). Sub-domain: a cohesive logical separation of that domain (product, order, invoicing…). Domain model: the abstraction of (a view of) the domain or sub-domain containing only what the application needs.
</panel>

**Q2.** Your team's forecasting module is useful but identical across companies. Build or buy, and which sub-domain class is that?
<panel type="seamless" minimized header="%%Answer%%">

Buy — it is a generic sub-domain: not specific to the business, implemented using off-the-shelf software. (Source: L7 slide 19.)
</panel>

</panel>

<span id="W7-c6"></span>

### W7.6 Bounded contexts and the ubiquitous language ★

**Sub-domains are problem-space slices; bounded contexts are where they become buildable — and where a shared language makes them ownable by one small team.** The lecture pairs the two deliberately: a sub-domain is closely aligned with its bounded context. (Source: L7 slide 21.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-bounded-context" trim />
</box>

**How it works:**

**A bounded context lets a sub-domain be implemented and executed at runtime.** In the errand platform, the user-management sub-domain (identity and access) becomes a bounded context containing what a login needs: username, password, one-time code — the model exists *inside* the boundary. (Source: L7 slide 21.)

**A {{ term("ubiquitous language", "a shared business-terms language used by domain experts and developers in conversation, requirements, design, and code — scoped to one bounded context") }} has one meaning per term inside a context — and the same word may mean something else in another.** "Customer" in the Sales context is not "Customer" in the Support context; the language is scoped to a bounded context. (Source: L7 slide 22.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-ubiquitous-language" trim />
</box>

**The language must reach the code — if a name isn't a term the domain expert would recognize, rename it.** The lecture's example makes business jargon explicit in code: `Guaranteed30MinuteDeliveryOffer.after(PizzaDelivered)` sends a coupon to the customer when delivery time exceeds thirty minutes — business expert jargon, ubiquitous language, and technical jargon meeting in one class name. (Source: L7 slide 23.)

**Contexts must collaborate, and the lecture names the patterns.** Capture the collaborations between bounded contexts (online retail store: Authentication, Fulfillment, Product catalog, Checkout, Payment, Accounting). Two contexts developed independently but jointly owning a small shared part of the model is a **shared kernel** (a common-coupling alert — W4.6); a provider–consumer split is **upstream–downstream** (Order context publishes an Order API; the Recommendation context fetches order information). (Source: L7 slides 24–25.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-shared-kernel" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-upstream-downstream" trim />
</box>

**Downstream strategies: conform, or ask the upstream to accommodate.** In a **conformist** relationship the downstream adopts the upstream's published model as-is, with no influence over the format; in a **supplier–customer** relationship the upstream designs the API with the downstream's needs in mind. (Source: L7 slide 26.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-conformist" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-supplier-customer" trim />
</box>

**How contexts interact should model how the real domain interacts — how we do it matters.** When Order Processing hands fulfillment data to the Warehouse: sharing the *entire* order structure is {{ term("stamp coupling", "one component passes an entire data structure to another that needs only part of it") }}; sharing just the needed order fields (and only then the customer information) is {{ term("data coupling", "components share only the specific data items actually needed") }}; and decoupling fully, Order Processing can produce an `OrderPlaced` **event** that the Warehouse consumes — reacting when the event is seen. (Source: L7 slides 27–30.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-stamp-coupling" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-data-coupling" trim />
</box>

{% call example("L7 slides 27–30 — four ways to tell the warehouse about an order") %}
A customer places an order; the warehouse needs to pick, package, and send items. Option (a): pass the **entire order structure** — stamp coupling; the warehouse now depends on order internals it never uses. Option (b): share **just the order information** the warehouse needs — data coupling. Option (c): add the customer information too — still data coupling, but more than the picking task requires. Option (d): Order Processing **produces an `OrderPlaced` event** and the Warehouse consumes it — the loosest option, and the one that matches how the real domain works: the warehouse does not ask for orders; it reacts to new ones.
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

**An aggregate is a hierarchy of entities with a root.** The aggregate root is the parent entity of the cluster and its public interface; everything outside interacts through it. (Source: L7 slide 33.)

**The boundaries are two boundaries in one.** The consistency boundary: from a visibility and operation perspective, all processes or objects external to the aggregate may only *read* its state — state can only be modified by executing methods of the aggregate's public interface. The transactional boundary: from a transaction perspective, any change to the aggregate either all succeeds or none succeeds. (Source: L7 slide 33.)

**A well-designed aggregate comes from the business and is cohesive.** It is derived from a business requirement and has high functional cohesion — e.g., Ticket in the Ticket service, where one Ticket aggregates its Messages and Attachments. (Source: L7 slide 33.)

{% call example("L7 slide 33 — the Ticket service's Ticket aggregate") %}
In the Ticket service, the aggregate is **Ticket** (the root): one Ticket holds `1..*` (UML for "one or more") Messages and their Attachments. External code may read the ticket and its messages, but to add a message it must call the Ticket's public interface — never insert into the message list directly. If "close ticket and archive attachments" is one operation, the transactional boundary guarantees it all happens or nothing does — tickets are never left half-closed.
{% endcall %}

**Aggregates and bounded contexts are both "collections of things" — but the things are fundamentally different.** Aggregates define business entity models — the central business objects within a bounded context; bounded contexts correspond to business sub-domains. (Source: L7 slide 34.)

<box type="warning" seamless>
**Pitfall:** treating every entity as its own aggregate. If Message were an aggregate root, "close ticket" could not be one transaction, and invariants spanning ticket and messages ("a closed ticket has no open messages") would live outside any boundary — the exact inconsistency the aggregate exists to prevent.
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

**Ad-hoc service boundaries drift into scope creep, low cohesion, and high coupling — the lecture's answer is to derive boundaries from the domain, then confirm them with event storming.** (Source: L7 slides 16, 37.)

**How it works:**

**Three DDD constructs feed service identification.** Use sub-domains: each subdomain corresponds to a different part of the business — define services corresponding to subdomains (the online store's product catalog, inventory management, order management, delivery management). Use bounded contexts: microservices are bounded contexts — with the caution that **not all bounded contexts are necessarily microservices**, and some have wide functionalities. Use aggregates: a well-designed aggregate exhibits many characteristics of a well-designed microservice — derived from business requirements, high functional cohesion, typically loosely coupled. (Source: L7 slide 35.)

**Then apply the {{ term("single-responsibility principle", "each service should have only a small set of responsibilities") }} (SRP) and decompose deliberately.** Each service should have only a small set of responsibilities. Decompose by **verb or use case** — a Shipping service responsible for shipping complete orders; or by **noun/resource** — an Account service responsible for all operations on user accounts. Also consider team size, technologies, and scalability/availability/security requirements; it is possible to further decompose a service, or to combine two into one. (Source: L7 slide 36.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-single-responsibility-principle" trim />
</box>

**{{ term("Event storming", "a lightweight workshop that traces commands → aggregates → events → policies to find service boundaries — full treatment in Week 8") }} finds the same boundaries from the dynamics side.** A lightweight, industry-common process: **domain events** are events that occur in the domain and matter — they record state changes; **commands** cause the events and are issued by a user or an external system; a command works **on an aggregate** to make an event happen; a **policy** links events back to commands — *when* the payment card is submitted, *then* confirm the order. (Source: L7 slides 38–41.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-domain-event" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-07.md#def-policy" trim />
</box>

**Drawing the boundaries is the payoff.** Draw boundaries that delimit each consistent context — the relations and communication between contexts follow, and **these boundaries give you microservice boundaries**. A bounded context solves one problem and can contain more than one aggregate. (Source: L7 slide 42.)

**And the cautions the lecture stamps on the whole method.** Start with business events, not CRUD (create, read, update, delete — the basic data-table operations) — focus on domain events from real business needs, not technical data operations. Not always true: one aggregate = one microservice; not always true: one bounded context = one microservice — aggregates and bounded contexts *inform* service boundaries but don't map 1:1 always. Group by business capability and cohesion; and microservice boundaries evolve over time. (Source: L7 slide 43.)

{% call example("L7 slides 38–42 — storming the errand platform's credit flow") %}
Work the wall left to right. Domain event: `CreditsTransferred` (records a state change in the credit ledger). What caused it? A command, `Transfer credits`, issued after an errand is completed. What did the command act on? The **Credit aggregate** (root: the credit account). What policy follows? *When* `ErrandCompleted` *then* `Transfer credits` — one event triggering another command. When the same wall shows credit events clustering separately from errand-matching events and catalogue events, draw boundaries around each consistent cluster: those bounded contexts — errand matching, credit, catalogue — are the microservice boundary candidates, exactly the seams the W7.3 trade-off discussion weighed.
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

</panel>

<box type="info" seamless>

**Section summary:**

* **Microservices = independently deployable, loosely coupled, small-team-owned services organized around business capabilities**, entered via an API gateway (W7.1–W7.2).
* **Every buy has a price**: independent deployability/scaling/availability vs network-hop performance, data-integrity risk, and observability complexity (W7.3).
* **Communication is a design decision**: synchronous REST/gRPC/GraphQL couples caller and callee; events and queues defer and decouple (W7.4).
* **DDD supplies the seams**: domain → sub-domains (core/supporting/generic) → bounded contexts with a ubiquitous language → aggregates as consistency units (W7.5–W7.7).
* **Boundaries come from the domain, not the org chart or the ER diagram**: sub-domains + bounded contexts + aggregates, verified by event storming, grouped by capability — never mapped 1:1 by formula (W7.8).
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
| Service instance per host | Run each service instance in isolation on its own host | [W7.3](#W7-c3) |
| Service instance per container | Run each service instance in its own container, packaged as a container image | [W7.3](#W7-c3) |
| Service instance per VM | Package each service as a VM image (e.g., an Amazon EC2 AMI) and launch instances from it | [W7.3](#W7-c3) |
| Domain-driven design (DDD) | Domain-centric design approach keeping the model isolated from technical complexity | [W7.5](#W7-c5) |
| Domain model | An abstraction of the problem domain with only the information the application needs | [W7.5](#W7-c5) |
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
