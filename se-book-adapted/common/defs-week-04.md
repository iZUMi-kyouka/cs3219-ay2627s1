{# Definitions for week-04. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-04.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable. #}

<span id="def-software-architecture">

The **software architecture** of a program or computing system is the structure or structures of the system, which comprise software components, the externally visible properties of those components, and the relationships among them. Externally visible properties ≡ functionalities + NFR; in short, the architecture is the overall organization of the system — a high-level design.

<sub>-- Bass, Clements & Kazman, *Software Architecture in Practice* (2e), quoted on L4 slide 4</sub>

</span>

<span id="def-component">

A **component** is an element that models an application-specific function, responsibility, requirement, task, or process.

<sub>-- L4 slide 6</sub>

</span>

<span id="def-connector">

A **connector** is an element that models interactions among components for the purpose of transfer of control and/or data.

<sub>-- L4 slide 6</sub>

</span>

<span id="def-architectural-style">

An **architectural style** is a named philosophy for organizing a system: it constrains how the code is divided (by technical concern or by business domain) and how the system is deployed (as a single deployed unit or as distributed units).

<sub>-- L4 slides 19–22</sub>

</span>

<span id="def-coupling">

**Coupling** is the degree to which one module depends on other modules. The deck's types: content (a component modifies another's internal data), common/global (shared global variables), control (one module passes a flag dictating what another does), data (sharing data via parameters), external (dependencies outside the system, e.g., OS or hardware), temporal (bundled only because they occur at the same time), and inclusion/import. Lower coupling is better.

<sub>-- L4 slide 18, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-cohesion">

**Cohesion** is the degree to which the facilities within a module belong together. The deck's types: functional (one computation, no side effects), layer (related services together in a strict hierarchy), communicational (operating on the same data), sequential (output of one is input to the next), procedural (called one after another), temporal (same execution phase, e.g., initialization), and utility (grouped only because nothing stronger applies). Higher cohesion is better.

<sub>-- L4 slide 17, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-modularity">

**Modularity** is decomposing a big chunk into smaller chunks with well-defined interfaces (APIs) — a way to manage the complexity of a problem by breaking it into smaller manageable modules, allocating functions to modules and specifying APIs for their interactions. Modularization buys shorter development time, better flexibility, and better comprehensibility.

<sub>-- L4 slide 15, after David Parnas</sub>

</span>

<span id="def-modular-monolith">

A **modular monolith** is a system deployed as a single unit — a monolith — whose code is partitioned by business domain into modules with well-defined interfaces: domain partitioning combined with monolithic deployment.

<sub>-- L4 slide 22 (categorization summary)</sub>

</span>

<span id="def-configuration">

**The configuration** of an architecture is its topology or structure — the arrangement of the system's components and connectors. An architecture = components + connectors + configuration.

<sub>-- L4 slide 6</sub>

</span>

<span id="def-reference-architecture">

A **reference architecture** explains the high-level structures of similar applications — numerous applications, same framework (e.g., web applications; the address-book developer guide's Logic/Storage/UI/Model organization) — and leads to architectural patterns.

<sub>-- L4 slide 9</sub>

</span>

<span id="def-architectural-pattern">

An **architectural pattern** is an architectural solution that forms the basis for architectural design: it addresses an application-specific problem within a specific context, adhering to a set of limitations and constraints.

<sub>-- L4 slide 9</sub>

</span>

<span id="def-control-flow">

**Control flow** is the flow that reasons about computation order — how the focus of control moves throughout the execution; data may accompany control.

<sub>-- L4 slide 10</sub>

</span>

<span id="def-data-flow">

**Data flow** is the flow that reasons about data availability, transformation, and latency — how data moves through a collection of computations; as data moves, control is activated.

<sub>-- L4 slide 10</sub>

</span>

<span id="def-call-and-return">

**Call and return** is the interaction style in which control moves from one component to another and back. It can be hierarchical (a master control calling subordinates) or non-hierarchical (objects calling each other's operations — e.g., through a manager for a shared abstract data type (ADT)).

<sub>-- L4 slide 11</sub>

</span>

<span id="def-horizontal-slicing">

**Horizontal slicing** cuts a system by technical layer: one slice is one layer — presentation, API, business logic, persistence — spanning every business domain; the boundary follows the technology.

<sub>-- L4 slide 16</sub>

</span>

<span id="def-vertical-slicing">

**Vertical slicing** cuts a system by business domain: one slice is one capability carried top to bottom — UI → endpoint → logic → persistence; the boundary follows the domain.

<sub>-- L4 slides 16, 20</sub>

</span>

<span id="def-functional-cohesion">

**Functional cohesion** is the strongest form of cohesion: the facilities in the module perform only one computation, with no side effects.

<sub>-- L4 slide 17, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-layer-cohesion">

**Layer cohesion** keeps related services together and everything else out, in a strict hierarchy in which higher-level services can access only lower-level services; accessing a service may result in side effects. (As a cohesion type, "layer" describes the inside of one module — not the system-wide layers of the layered style.)

<sub>-- L4 slide 17, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-communicational-cohesion">

**Communicational cohesion** keeps together the facilities that operate on the same data.

<sub>-- L4 slide 17, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-sequential-cohesion">

**Sequential cohesion** keeps together a set of procedures that work in sequence to perform some computation — the output of one is the input to the next.

<sub>-- L4 slide 17, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-procedural-cohesion">

**Procedural cohesion** keeps together a set of procedures that are called one after another.

<sub>-- L4 slide 17, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-temporal-cohesion">

**Temporal cohesion** keeps together procedures used in the same general phase of execution, such as initialization or termination.

<sub>-- L4 slide 17, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-utility-cohesion">

**Utility cohesion** keeps together related utilities when there is no way to group them using a stronger form of cohesion.

<sub>-- L4 slide 17, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-content-coupling">

**Content coupling** is the worst form of coupling: a component modifies the internal data of another component.

<sub>-- L4 slide 18, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-common-global-coupling">

**Common/global coupling** couples all the modules that use the same global variable to each other.

<sub>-- L4 slide 18, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-control-coupling">

**Control coupling** is one module (A) directly controlling another (B) by passing information on what B should do — e.g., using a "flag" that defines what B should do.

<sub>-- L4 slide 18, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-data-coupling">

**Data coupling** is one module sharing data with another — e.g., via passing parameters. Weaker than control coupling: the caller passes data, not instructions.

<sub>-- L4 slide 18, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-external-coupling">

**External coupling** is a dependency that exists on elements outside the scope of the system, such as the operating system, shared libraries, or the hardware.

<sub>-- L4 slide 18, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-temporal-coupling">

**Temporal coupling** bundles two actions together just because they happen to occur at the same time.

<sub>-- L4 slide 18, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-import-coupling">

**Inclusion/import coupling** is the coupling introduced by including a file or importing a package.

<sub>-- L4 slide 18, from Lethbridge & Laganière, ch. 9</sub>

</span>

<span id="def-technical-partitioning">

**Technical partitioning** divides code by technical concern — presentation, services, persistence — focusing on separation of concerns and possibly aligning with team expertise (frontend developers, backend developers, database administrators).

<sub>-- L4 slide 20</sub>

</span>

<span id="def-domain-partitioning">

**Domain partitioning** divides code by domain (business) concern — customer, payment, shipping — so that logical components map to the problem and better align the system with the problem in hand.

<sub>-- L4 slide 20</sub>

</span>

<span id="def-monolithic-deployment">

**Monolithic deployment** deploys all the logical components that make up the application as one unit: the application runs as one process.

<sub>-- L4 slide 21</sub>

</span>

<span id="def-distributed-deployment">

**Distributed deployment** runs the application as independent logical components: each runs as an individual process and the components communicate over the network.

<sub>-- L4 slide 21</sub>

</span>

<span id="def-abstract-data-type">

An **abstract data type (ADT)** is a data type defined by the operations it supports and what they mean, rather than by how the data is stored internally — code that uses an ADT depends only on that operation interface, never on the representation behind it.

%%Source: L4 slide 11's "Manager ADT" sketch (objects calling each other's operations through a manager for a shared ADT); the deck names the sketch without defining the term — standard definition, e.g. Lethbridge & Laganière, *Object-Oriented Software Engineering*.%%

</span>

<span id="def-nginx">

**Nginx** is an open-source web server that is also widely used as a reverse proxy and load balancer: client requests arrive at Nginx, which forwards them to the application instances behind it — the pattern of the capacity NFR "three Docker containers per microservice behind Nginx".

%%Source: named in the L4-AlternativeExamplesForProductBacklog deck's order-service capacity NFR (the deck names Nginx without defining it — standard definition).%%

</span>
