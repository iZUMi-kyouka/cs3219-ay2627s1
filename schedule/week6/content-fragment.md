<span id="summary">

**Organising question:** how do we classify and choose between the classical architectural styles — and what rules should govern communication between distributed parts? The first deck (L6-Architecture) builds the **style taxonomy** (code divided by technical vs domain concern; deployed as a single unit vs distributed units) and walks the classical styles: **layered, pipe-and-filter, modular monolith, MVC, and SPA**, closing with architecture-diagram guidelines. The second deck (L6-REST) introduces **REST** as an architectural style for distributed hypermedia systems: its six constraints, resources and representations, and when REST is not the right tool.

</span>

<span id="toc">

* [W6.1 Classifying architectural styles]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c1)
* [W6.2 Layered architecture]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c2)
* [W6.3 Pipe-and-filter]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c3)
* [W6.4 Modular monolith: package by domain]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c4)
* [W6.5 MVC and Web MVC]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c5)
* [W6.6 Single-page applications (SPA)]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c6)
* [W6.7 REST: an architectural style for the web]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c7)
* [W6.8 The REST constraints]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c8)
* [W6.9 Resources, representations, and content negotiation]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c9)
* [W6.10 REST: strengths, limits, and alternatives]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c10)
* [W6.11 Communicating the architecture: diagrams and the model-code gap]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c11)

</span>

<span id="lecture">

### Lecture

{% from "schedule/macros-fragment.md" import term, example with context %}

<panel type="seamless" expanded header="## %%[Deck 1 of 2]%% **L6 — Architecture: the classical styles**">

**Styles exist because software is built for a purpose — the lecture classifies them on two axes.** How is the code divided (technical concern vs domain/business concern), and how is the system deployed (single deployed unit vs distributed units)? (Slide 4.) → [W6.1]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c1)

**Layered architecture organizes code as layers with downward-only dependencies.** Buys: structure-enforced separation of concerns, modifiability within a layer (swap Oracle with MySQL), testability (mock the layer below). Costs: all-or-nothing deployability, no independent scaling, no feature ownership, change amplification. {{ term("Closed layers", "a layered design where interaction is allowed only between two consecutive layers") }} talk only to the next layer down; {{ term("open layers", "a layered design where any top layer may get service from any bottom layer") }} may skip. (Slides 6–8.) → [W6.2]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c2)

**Pipe-and-filter streams data through independent transformations.** Filters compute incrementally and share no state; pipes connect them. Buys: scalability (replicate a stateless filter), deployability, testability, reuse. Costs: latency per stage, no feedback until the sink, no native partial-failure handling. Suited to batch/stream transformation where throughput beats latency — e.g., the Azure Functions image pipeline (moderation → resizing → reorientation → watermarking → CDN). (Slides 9–12.) → [W6.3]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c3)

**The modular monolith re-divides a single deployable by business domain.** Each domain bundles its own UI, logic, and data; {{ term("coupling", "how strongly one part depends on another — tight coupling means changes in one force changes in the other") }} drops when modules expose explicit, narrow APIs and hide their implementations. Buys: domain-aligned teams, maintainability, testability, performance. Costs: reuse across modules, one-deployment scaling, fragile boundaries. (Slides 13–15.) → [W6.4]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c4)

**MVC separates the three concerns of an interactive app: view, controller, model.** (Slides 16–22.) → [W6.5]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c5)

- **Buys:** separation of concerns, extensibility (new view/controller pairs), testability.
- **Web MVC** maps them onto the server — the controller handles the HTTP request and prepares the view, the view renders the response, and the model is business logic + persistence — with page/front controllers for routing.
- **Costs:** multiple hops per view update and the fat controller.

**The SPA moves a program into the browser.** A JavaScript app downloaded once runs continuously, fetching data via {{ term("Ajax", "a browser technique where a script sends HTTP requests and handles responses in the background — no page refresh") }} (JSON instead of full HTML pages): fluid experience and less server rendering, but harder development, a JavaScript requirement, XSS exposure, and server-side re-enforcement of every authorization rule. (Slides 23–25.) → [W6.6]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c6)

**The deck closes on diagrams and the {{ term("model-code gap", "the distance between source code and architecture model — models reason about complexity and are never one-to-one mappings of code") }}.** Diagrams are free-form: big picture, shared vision, conversation focus, code map. Common defects: unexplained notation, ambiguous elements, mixed abstraction levels; the guidelines demand titles, legends, labeled lines, explicit elements. (Slides 26–31.) → [W6.11]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c11)

</panel>

<panel type="seamless" minimized header="## %%[Deck 2 of 2]%% **L6 — REST: an architectural style for the web**">

**{{ term("REST", "an architectural style for distributed hypermedia systems, defined by a set of constraints applied over HTTP") }} is a set of constraints for creating web services — not an architecture by itself.** Originated by Roy Fielding (principal author of the HTTP spec), it targets performance and scalability, simplicity of interaction, modifiability, reliability, and extensibility for distributed hypermedia systems. (Slides 3–5, 17.) → [W6.7]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c7)

**Six constraints, each with named reasons: client-server, stateless, cacheable, layered system, uniform interface, code-on-demand (optional).** Statelessness — every request fully self-contained, no server-side session — buys scalability, reliability, and monitoring. Cacheability lets clients reuse declared-cacheable responses. Layered systems let intermediaries (load balancers, caches) sit between client and server. (Slides 6–10, 15.) → [W6.8]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c8)

**The {{ term("uniform interface", "one standard way of interacting with a server: HTTP verbs, status codes, representations in the body") }} rests on resources and representations.**

- Anything can be a resource, identified by a stable URI
- Clients operate on representations (data + metadata)
- Content negotiation (Content-Type/Accept) reconciles one interface with many media types
- Self-describing messages and hypermedia links let representations expose state transitions (the paid order advertising `cancel` and `refund` links)

(Slides 11–14.) → [W6.9]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c9)

**REST's costs mirror its strengths.** Weak contract enforcement (no built-in typing), repetitive data from statelessness, and efficiency lost to standardized URIs; the closing table maps workload shapes — high-frequency calls, event-driven workflows, streaming, fan-out — to better alternatives (gRPC, event-driven architecture, WebSockets, pub-sub, queues). (Slides 16, 18.) → [W6.10]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html#W6-c10)

</panel>

</span>

<span id="tutorial-summary">

Tutorial 4 diagnoses **coupling** in a three-module system (content, control, common/global, temporal) and repairs each case, then uses the **intermodal shipping-container analogy** to define container, image, engine, and Docker — Week 5's containerization made precise.

</span>

<span id="tutorial">

### Tutorial 4

{% from "schedule/macros-fragment.md" import term, example with context %}

**What this tutorial practises:** identifying and reducing coupling (a Week 4 concept that Week 6's module boundaries depend on), and grounding the containerization ideas of Week 5 in precise definitions via the cargo-shipping analogy.

**Task 1 — Find the coupling, then break it**

Consider a system where (Source: Tutorial 4 sheet, Q1):

* i. Module A collects sensor data and writes it **directly to Module B's internal data structures** for processing.
* ii. Module B passes a **"mode" flag** to Module C to indicate whether results should be logged or displayed.
* iii. All three modules access a **global config variable** `systemStatus`.
* iv. The modules are **initialized together at boot**, even though some may not be initially needed.

**Task 1(a).** Identify the types of coupling present (there may be more than one).

<panel type="seamless" minimized header="%%Model answer%%">

| Component/Scenario | Type of coupling | Comment |
|---|---|---|
| A writes into B's internal data structures | **{{ term("Content coupling", "a component modifies the internal data of another — the worst coupling kind (Week 4)") }}** | Component modifies internal data of another |
| B passes a "mode" flag to C | **{{ term("Control coupling", "one module passes information on what another should do, e.g., a flag (Week 4)") }}** | Component controls the other by passing information |
| All three share the global `systemStatus` | **{{ term("Common/global coupling", "all modules using the same global variable are coupled to each other (Week 4)") }}** | Using global variables |
| All initialized together at boot | **{{ term("Temporal coupling", "actions bundled together only because they happen at the same time (Week 4)") }}** | Actions bundled together because they happen at the same time |

(A student addition the teaching team endorsed: the sensor dependency is **{{ term("external coupling", "a dependency on elements outside the system — OS, shared libraries, hardware (Week 4)") }}** — inevitable, since the system depends on sensor data.) (Source: Tutorial 4 model solution.)
</panel>

**Task 1(b).** Suggest one design modification per case to reduce coupling and make the system more modular.

<panel type="seamless" minimized header="%%Model answer%%">

* **Content** — expose a clean interface in B (e.g., an `updateData()` function) instead of allowing direct data access.
* **Control** — replace the flag with polymorphism/callbacks/event-driven logic so C decides its own behavior.
* **Common/global** — replace the global variable with a config manager with read-only access.
* **Temporal** — lazy initialization: start modules only when needed. (Source: Tutorial 4 model solution.)
</panel>

**Task 2 — From the "matrix of hell" to the shipping container**

Before the 1960s, global cargo moved as barrels, crates, and sacks — each needing different handling, storage, and transport. Transferring cargo between ships, trains, and trucks meant unpacking and repacking at every stage: the "matrix of hell".

**Task 2(a–b).** Was the core problem the goods themselves, or how they were packaged and handled? And what properties made the intermodal container such a powerful abstraction?

<panel type="seamless" minimized header="%%Model answer%%">

**(a)** A combination: the variety of goods added complexity, but the core problem was **how goods were packaged and handled** — no standardized interface between cargo and transport infrastructure, so every goods/packaging/transport combination had to be handled specially. **(b)** The container is **sealed and standard**: loadable with almost any cargo, never unpacked in transit, isolating contents from the transport system — the infrastructure only needs to know how to handle the container, not what is inside. (Source: Tutorial 4 model solution.)
</panel>

**Task 2(c–e).** Map the analogy onto software: what plays the role of the varied goods, the transport modes, and the container itself — and how do **container image**, **container**, and **container engine** differ?

<panel type="seamless" minimized header="%%Model answer%%">

**(c)** Many tech stacks ↔ many kinds of goods; different OSes/hardware environments ↔ different transport modes; both settings punish non-standard packaging — an app that works on one machine may fail on another due to missing or conflicting dependencies. **(d)**

- A **container image** is the read-only blueprint (file-system layout, commands, dependencies, configs) used to create containers and ensure consistent behavior across systems
- A **container** is a running instance of that image, isolated from host and other processes, communicating with the host OS kernel via the engine
- A **container engine** provides the runtime environment, the interface between the OS and the containers

**(e)** **Docker** is a container engine/platform for building, running, and managing containers (its daemon — a background service that actually builds and runs containers on the host — gives clients a client-server way to manage Docker objects). (Source: Tutorial 4 model solution.)
</panel>

**Task 2(f).** Describe, step by step, how an image, a container, and a container engine deploy a web application reliably across different machines.

<panel type="seamless" minimized header="%%Model answer%%">

1. Create a container image packaging the application, its runtime, and all required dependencies (e.g., from a Dockerfile — the text recipe listing the image's base system, files, and start command).
2. Transfer the image to the target machine (remote server or cloud instance), e.g., through a container image registry (a service that stores images so machines can pull them on demand, like Docker Hub).
3. Use a container engine (such as Docker) on the target machine to run the image.
4. Start a container — a running instance of the image in an isolated, predictable environment.
5. Manage and scale containers with the engine's tools (rapid startup, shutdown, replication as demand changes).

Because the image encapsulates everything the application needs, the **same image** runs across different machines, operating systems, and cloud providers — avoiding dependency conflicts. (Source: Tutorial 4 model solution.)
</panel>

**Materials:**

* %%Tutorial sheet (PDF kept offline)%%
* %%Model solution (PDF kept offline)%%

</span>
