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

*Deck: L7 — Microservice architecture.*

**The lecture starts where the monolith hurts: too large for one application.** A large codebase, slow deployment, multiple teams, and no independent scaling motivate the split; the migration picture fronts the decomposed MyEcom app with an {{ term("API gateway", "the single entry point that routes client requests to the microservices behind it") }}. (Slide 3.) → [W7.1]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c1)

**The {{ term("microservice architectural style", "structures one application as a suite of small, independently deployable services organized around business capabilities") }} gets a crisp definition: one application as a suite of small services.** (Slides 5–7.) → [W7.1]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c1), [W7.2]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c2)

- Each service offers a well-defined {{ term("business capability", "something the business does that delivers value — e.g., 'get a current stock list'; microservice boundaries align with capabilities") }}, is developed and deployed independently, and communicates through well-defined published interfaces.
- The four characteristics: organized around business capabilities, loosely coupled, small-team-owned, independently deployable.

**Business capabilities, not code layers, set the boundaries.** (Slides 8–10.) → [W7.2]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c2)

- The mom-and-pop retailer's warehouse and finance capabilities become cohesive services (Order, Payment, Checkout).
- Amazon's two-pizza teams own their services' whole lifecycle.
- Services share no code — {{ term("loose coupling", "services depend on each other only through published interfaces, so each can change, deploy, and fail independently") }} by construction.

**Every buy is priced.** Buys: deployability (ship credit without touching suppliers), scalability (service as unit of scaling), availability (fault isolation). Costs: performance (every call a network hop), integrity (data duplication across services), complexity (n services, n logs). Deployment patterns: instance per host, per container, or per VM. (Slides 11–14.) → [W7.3]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c3)

**Think-pair-share: does splitting help or hurt the errand platform?** 20× lunch traffic on errands and an independently changing credit mechanism argue for splitting; exactly-once credit transfer across multiple databases argues against. (Slide 15.) → [W7.3]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c3)

**Communication is synchronous or asynchronous.** Sync: REST over HTTPS, gRPC, and GraphQL — an API style where the client names exactly the fields it needs and one query returns just those (the invoice's `InvoicePaid` request). Async: publish-subscribe events and message queues — the same invoice transitions on receiving an event; Quiz 2's Grab-like app shows Design B surviving a Matching crash by storing the event in the middleware. (Slides 13, 31.) → [W7.4]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#W7-c4)

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
