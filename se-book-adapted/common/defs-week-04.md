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
