<span id="summary">

**Organising question:** when does splitting a modular monolith into microservices help — and how do you find the seams? This week's lecture defines the **microservice architectural style** (services organized around business capabilities, loosely coupled, owned by small teams, independently deployable), weighs the **monolith-vs-microservices trade-offs**, and introduces **domain-driven design** — domains, sub-domains, bounded contexts, ubiquitous language, aggregates — plus **event storming** as the practice for identifying microservice boundaries.

</span>

<span id="toc">

* [W7.1 The microservice architectural style]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c1)
* [W7.2 Organized around business capabilities]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c2)
* [W7.3 Monolith vs microservices: the trade-offs]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c3)
* [W7.4 How microservices communicate]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c4)
* [W7.5 Domain-driven design: domain, sub-domain, domain model]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c5)
* [W7.6 Bounded contexts and the ubiquitous language]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c6)
* [W7.7 Aggregates: the consistency unit of DDD]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c7)
* [W7.8 Identifying microservices: DDD and event storming]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c8)

</span>

<span id="lecture">

### Lecture

{% from "schedule/macros-fragment.md" import term, example with context %}

*Deck: L7 — Microservice architecture.* %%The DDD and event-storming halves of week 7 are in the recorded segments L7-DDD and L7-EventStorming; their content is woven into units W7.5–W7.8 below.%%

**The lecture starts where the monolith hurts: too large for one application.** A large codebase, slow deployment, multiple teams, and no independent scaling motivate the split; the migration picture fronts the decomposed MyEcom app with an {{ term("API gateway", "the single entry point that routes client requests to the microservices behind it") }}. (Slide 3.) → [W7.1]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c1)

**The {{ term("microservice architectural style", "structures one application as a suite of small, independently deployable services organized around business capabilities") }} gets a crisp definition: one application as a suite of small services.** (Slides 5–7.) → [W7.1]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c1), [W7.2]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c2)

- Each service offers a well-defined {{ term("business capability", "something the business does that delivers value — e.g., 'get a current stock list'; microservice boundaries align with capabilities") }}, is developed and deployed independently, and communicates through well-defined published interfaces.
- The four characteristics: organized around business capabilities, loosely coupled, small-team-owned, independently deployable.

**Business capabilities, not code layers, set the boundaries.** (Slides 8–10.) → [W7.2]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c2)

- The mom-and-pop retailer's warehouse and finance capabilities become cohesive services (Order, Payment, Checkout) — finance never touches stock levels, the warehouse never sets salaries.
- Amazon's two-pizza teams own their services' whole lifecycle — and the lecture grounds small cross-functional teams in {{ term("Conway's Law", "organizations produce designs that copy their communication structures — the product mirrors the teams that built it") }} (L7 recording, ~[41:00]).
- Services share no code — {{ term("loose coupling", "services depend on each other only through published interfaces, so each can change, deploy, and fail independently") }} by construction — which is also what makes them reusable: lift the customer-management service out of e-commerce into private banking, or the payment service into a hobby class's fee charging (L7 recording, ~[25:00]).

**Every buy is priced.** Buys: deployability (ship credit without touching suppliers), scalability (service as unit of scaling — give Kubernetes a criterion, e.g., "spawn another pod past 60% load", and it enforces it), availability (fault isolation: a dead supplier service blocks new orders, not credit transfers for completed ones — and multiple instances behind a gateway degrade performance, not availability). Costs: performance (every call a network hop — split authn/authz/profile and a profile update hops through all three), integrity (data duplication across services), complexity (n services, n logs). Deployment patterns: instance per host, per container, or per VM — with the lecture's pricing of each (bare metal wastes idle resources; a container pushed into a cloud VM "may not be the best use of resources"). (Slides 11–14; L7 recording, ~[45:00–56:00].) → [W7.3]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c3)

**Think-pair-share: does splitting help or hurt the errand platform?** 20× lunch traffic on errands and an independently changing credit mechanism (buy or loan credits) argue for splitting; exactly-once — idempotent — credit transfer across multiple databases argues against (integrity becomes *your* job: idempotency and eventual consistency, no longer the database's). The room's verdicts, with corrections: 20× traffic → *scalability*, not availability; credit changes → independent develop *and* deploy; VM→containers → complexity ("debugging a distributed application becomes a nightmare"). Takeaway: "your microservice is not a silver bullet — it's a trade-off, like any other architecture decision." (Slide 15; L7 recording, ~[60:00–66:00].) → [W7.3]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c3)

**Communication happens through contracts, synchronously or asynchronously.** The contract ("your request should contain all these things") is the interface — as long as it doesn't change, the mechanism is well-defined. Sync: REST over HTTPS, gRPC, and GraphQL — the caller blocks itself until the response (REST's missing type checking is why gRPC/GraphQL exist alongside it); the invoice's `InvoicePaid` request. Async: publish-subscribe events and message queues — an event bus or queue in between notifies the consumer, and the same invoice transitions on receiving an event; Quiz 2's Grab-like app shows Design B surviving a Matching crash by storing the event in the middleware. (Slides 13, 31; L7 recording, ~[49:00–52:00].) → [W7.4]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c4)

**Then the toolkit for finding seams: {{ term("domain-driven design", "a domain-centric approach that keeps the domain model isolated from technical complexities") }}.** (Slides 16–20.) → [W7.5]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c5)

- The domain is the problem space.
- A domain model keeps only what the application needs — retain stations and interchanges, ignore tunnel depth.
- Complex systems decompose into sub-domains — core (build), supporting (build/outsource), generic (buy).

**{{ term("Bounded contexts", "the explicit boundary within which a domain model exists") }} make sub-domains buildable, with a language to match.**

- Each context holds its own model
- The {{ term("ubiquitous language", "shared business terms used by experts and developers in conversation, requirements, design, and code — one meaning per context") }} gives one meaning per term per context (Customer in Sales ≠ Customer in Support)
- Contexts collaborate as shared kernel, upstream–downstream, conformist, or supplier–customer — and should interact the way the real domain does: data coupling beats stamp coupling, events are loosest (`OrderPlaced`)

(Slides 21–32.) → [W7.6]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c6)

**{{ term("Aggregates", "clusters of related objects treated as one unit for data changes — a root plus consistency and transactional boundaries") }} are the consistency unit inside a context.** A cluster of related objects with a root (public interface) and boundaries: consistency (outsiders only read; change via the interface) and transactional (all or none) — Ticket with its Messages and Attachments. (Slides 33–34.) → [W7.7]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c7)

**Identifying services: three DDD constructs, SRP, and {{ term("event storming", "a lightweight workshop tracing commands → aggregates → events → policies to find boundaries") }} — with cautions.** (Slides 35–43.) → [W7.8]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c8)

- Use sub-domains, bounded contexts, and aggregates to define service candidates.
- Decompose by verb (Shipping service) or noun (Account service).
- Storm the domain: commands → aggregates → events → policies → boundaries.
- None of the mappings is 1:1 — group by business capability and cohesion, and expect boundaries to evolve.

</span>
