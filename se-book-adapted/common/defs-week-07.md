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
