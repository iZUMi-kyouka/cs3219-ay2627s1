{# Definitions for week-07. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-07.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable. #}

<span id="def-microservice">

**A microservice** is an independently deployable service modeled around a business domain: it offers a well-defined business capability, is small and lightweight, is owned by a small team, and communicates with other services through well-defined, published interfaces.

%%Source: L7 slides 5–7 (first introduced in L5 slide 21, guest lecture by Dell).%%

</span>

<span id="def-microservice-architecture">

**Microservice architecture** is an architectural style that structures an application as a collection of services that are organized around business capabilities, loosely coupled, owned by small teams, and independently deployable — a suite of small services that work with each other to form a bigger solution.

%%Source: L7 slides 5–7.%%

</span>

<span id="def-loose-coupling">

**Loose coupling** is the design property in which components depend on each other only through small, published interfaces and share no internals — no shared code, databases, or implementation knowledge — so each component can change, deploy, and fail without forcing changes on the others.

%%Source: L7 slides 7 and 10; L5 slides 23–24 (guest lecture by Dell).%%

</span>

<span id="def-ddd">

**Domain-driven design (DDD)** is a domain-centric approach to software design for complex problem domains: a collection of patterns, principles, and practices that keeps the domain model isolated from technical complexities so that the software closely reflects business needs.

%%Source: L7 slide 20.%%

</span>

<span id="def-domain-model">

**A domain model** is an abstraction of the problem domain — a view of the domain containing only the information necessary to solve the problem in the context of the application. It is not the reality; deciding what to retain and what to ignore is the modeling act.

%%Source: L7 slides 17–18.%%

</span>

<span id="def-subdomain">

**A sub-domain** is a logical separation of the domain: a cohesive unit of business functionality focused on a specific set of responsibilities, typically reflecting part of the business organization's structure. Sub-domains are classified as **core** (the key differentiator — build in-house), **supporting** (related but not a differentiator — build or outsource), or **generic** (not specific to the business — buy off-the-shelf).

%%Source: L7 slides 18–19.%%

</span>

<span id="def-bounded-context">

**A bounded context** is an explicit boundary within which a domain model exists: a highly cohesive boundary including the input, output, events, requirements, processes, and data models relevant to a sub-domain. Bounded contexts belong to the solution space and ideally align with sub-domains of the problem space.

%%Source: L7 slides 21 and 32.%%

</span>

<span id="def-ubiquitous-language">

**A ubiquitous language** is a shared language between domain experts and developers, built from business terms and used in conversations, requirements, design, and code — scoped to a bounded context, with one meaning per term inside that context. The same word can mean something else in another context.

%%Source: L7 slides 22–23.%%

</span>

<span id="def-aggregate">

**An aggregate** is a cluster of related objects treated as a single unit for the purpose of data changes. It has a **root** — the parent entity that forms the aggregate's public interface — and **boundaries**: a consistency boundary (everything outside may only read the aggregate's state; state changes only through the public interface) and a transactional boundary (any change either all succeeds or none succeeds).

%%Source: L7 slide 33.%%

</span>

<span id="def-business-capability">

A **business capability** is something the business does (or can do) that delivers value — e.g., a warehouse providing "get a current stock list", finance providing "set up payroll for a new recruit" or "monthly accounts". Microservice boundaries are closely aligned with business capabilities.

%%Source: L7 slides 8–9.%%

</span>

<span id="def-two-pizza-team">

A **two-pizza team** is a small, cross-functional team — small enough that two pizzas feed it — organized around capabilities and owning the whole lifecycle of its services (Amazon's example).

%%Source: L7 slide 10.%%

</span>

<span id="def-service-instance-per-host">

**Service instance per host** is the deployment pattern that runs each service instance in isolation on its own host.

%%Source: L7 slides 11–12.%%

</span>

<span id="def-service-instance-per-container">

**Service instance per container** is the deployment pattern that runs each service instance in its own container, packaged as a container image holding the application and the libraries required to run the service.

%%Source: L7 slides 11–12.%%

</span>

<span id="def-service-instance-per-vm">

**Service instance per VM** is the deployment pattern that packages each service as a virtual machine image (e.g., an Amazon EC2 AMI — Amazon Machine Image) and launches each service instance as a VM from that image.

%%Source: L7 slides 11–12.%%

</span>

<span id="def-stamp-coupling">

**Stamp coupling** is the coupling in which one component passes an entire data structure to another component that needs only part of it — e.g., sharing the entire order with the Warehouse service when only some fields are needed for picking.

%%Source: L7 slides 27–28.%%

</span>

<span id="def-shared-kernel">

A **shared kernel** is the collaboration pattern in which two bounded contexts, developed independently, jointly own a small shared subset of the model and coordinate changes to it.

%%Source: L7 slides 24–25.%%

</span>

<span id="def-upstream-downstream">

An **upstream–downstream** relationship is the provider–consumer collaboration between bounded contexts: the upstream context publishes an API (e.g., the Order context publishes an Order API) and the downstream context fetches or subscribes to it (e.g., the Recommendation context).

%%Source: L7 slides 25–26.%%

</span>

<span id="def-conformist">

A **conformist** relationship is the downstream strategy in which the downstream adopts the upstream's published model as-is, with no influence over the format.

%%Source: L7 slide 26.%%

</span>

<span id="def-supplier-customer">

A **supplier–customer** relationship is the upstream–downstream collaboration in which the upstream designs the API with the downstream's needs in mind.

%%Source: L7 slide 26.%%

</span>

<span id="def-single-responsibility-principle">

The **single-responsibility principle (SRP)** asks that each service have only a small set of responsibilities — applied when decomposing microservices by verb or use case (a Shipping service responsible for shipping complete orders) or by noun/resource (an Account service responsible for all operations on user accounts).

%%Source: L7 slide 36.%%

</span>

<span id="def-domain-event">

A **domain event** is an event that occurs in the domain and is relevant to it — a record of a state change. Event storming starts from domain events that come from real business needs, not from technical data operations (CRUD).

%%Source: L7 slides 38, 43.%%

</span>

<span id="def-policy">

A **policy** is the rule that links an event back to a command — "when event X, then command Y" (e.g., when the payment card is submitted, then confirm the order). In event storming, policies separate the boundaries.

%%Source: L7 slide 41.%%

</span>
