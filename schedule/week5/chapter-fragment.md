{% from "schedule/macros-fragment.md" import term, example with context %}
<h2 id="title">Week 5 — Cloud-Native Paradigm (Guest Lecture)</h2>

<span id="prereqs">

**Prerequisites:** [Week 4 — Architecture (I) & Product Backlog]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html): software architecture, components and connectors, the monolith and the modular monolith.
</span>

<span id="outcomes">

**Learning outcomes:**

* **Can** explain what a cloud abstracts, and distinguish cloud computing (where software runs) from cloud native (how software is built and run). — [W5.1](#W5-c1), [W5.2](#W5-c2)
* **Can** explain the limitations of a monolithic application and how microservices address them. — [W5.3](#W5-c3)
* **Can** explain what a container is and why containerization is a powerful abstraction for deployment. — [W5.4](#W5-c4)
* **Can** explain what container orchestration (Kubernetes) adds: pods, deployments, self-healing, and horizontal scaling. — [W5.5](#W5-c5)
* **Can** explain immutable infrastructure and infrastructure as code, and contrast declarative with imperative provisioning. — [W5.6](#W5-c6)
</span>

<div id="body">

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

<box type="info" seamless>

This chapter is based on the **Week 5 guest lecture — "The Cloud Native Paradigm Shift" — delivered by a practitioner from Dell Technologies** (AI Innovation Hub, 20+ years across software development, DevOps, and operations). Slide citations below refer to that deck, shortened to "L5".
</box>

## Core concepts

<span id="W5-c1"></span>

### W5.1 The cloud is an abstraction ★

**You cannot reason about {{ term("cloud native", "an approach to building and running applications that exploits the advantages of the cloud computing delivery model") }} software until you see the cloud as an abstraction, not a place.** "The cloud" hides pools of compute, storage, and networking behind interfaces you can program against. What the abstraction hides determines what your architecture must handle itself.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-cloud-computing" trim />
</box>

**How it works:**

**A cloud is a shared pool of resources exposed as self-service, elastic, metered services.** Because the provider pools and measures the resources, you can get more capacity on demand and pay only for what you use — the six characteristics in the definition. (Source: L5 slides 4–5, Dell guest lecture.)

**Distributed systems are not new; what the cloud changed is who manages the infrastructure.** The earliest distributed apps already separated three tiers of logic on different machines: presentation logic on the client, application logic on an app server, and data access logic plus data storage on a database server. (Source: L5 slides 11–12, Dell guest lecture.)

{% call example("L5 slide 12 — the early-days three-tier distributed app") %}
A retail company runs a desktop client that talks to an application server, which talks to a database server. The client holds the **presentation logic** (screens, input forms), the app server holds the **application logic** (business rules), and the database server holds the **data access logic** and the **data storage**. The company owns and patches all three machines itself. The functionality is identical to a modern cloud deployment — what changed under the cloud abstraction is who owns the machines and how capacity is obtained.
{% endcall %}

**As software and teams grew, the questions the infrastructure must answer got harder, not easier.** The lecture traces software complexity rising over time and asks how we can respond to market changes and business needs, keep the service always available, and keep quality of service high — while "we can't write software fast enough". (Source: L5 slides 13–14, Dell guest lecture.)

**Distributing an app sets four design considerations that the architecture must satisfy.** The lecture states them directly (Source: L5 slide 16, Dell guest lecture):

* An app should not be tied to a specific host or network.
* The end user should not be affected by a hardware or software failure.
* An app should still be accessible as its workload increases.
* There should not be any downtime when rolling out new updates to the app.

**The four considerations are met by hiding layers, and the stack makes the hiding literal.** Each layer of the cloud-native stack exists to abstract the one beneath it — which is why an app written against the top layers is "not tied to a specific host" without anyone rewriting it (Source: L1 slide 20 stack; L5 slides 3–5, 16, 41, Dell guest lecture).

<mermaid>
flowchart TB
    APP["Applications & development<br/>(your services)"] --> OBS["Observability & analysis"]
    OBS --> ORCH["Orchestration & management<br/>(e.g. Kubernetes)"]
    ORCH --> RUN["Runtime<br/>(containers)"]
    RUN --> PROV["Provisioning<br/>(infrastructure as code)"]
    PROV --> INFRA["Infrastructure<br/>(compute, network, storage)"]
</mermaid>

%%Notation: each box is one layer of the cloud-native application stack (L1 slide 20); a solid arrow means "runs on top of / abstracts away the layer below". Read bottom-up: physical infrastructure, provisioned by code, given a container runtime, orchestrated, observed, and finally hosting your applications.%%

How to read it: the guest lecture opens with "a cloud is an abstraction" (L5 slide 3) — and the joke in the "There is no cloud, it's just someone else's computer" comic is that somewhere the bottom layer is still real hardware. Walk it with the lecture's own example (L5 slide 41): your Payment, Product, Inventory and Cart services live at the top; Kubernetes hides which compute/network/storage they run on — so "not tied to a specific host" (slide 16, design consideration 1) is the top layers being free to move because the bottom layers are abstracted.

<box type="warning" seamless>
**Pitfall:** treating "the cloud" as just someone else's server. If you lift an existing single-host application into the cloud without redesigning it, you pay cloud prices for datacenter behavior: it is still tied to a specific host, still fails with that host, and still needs downtime for updates — none of the four design considerations above are met.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** A teammate says "we moved to the cloud, so our app is cloud native." What is wrong with that claim?
<panel type="seamless" minimized header="%%Answer%%">

Cloud computing describes **where** the software runs (on-demand, pooled, metered resources); cloud native describes **how** it is built and run (containers, microservices, immutable infrastructure, declarative APIs — W5.2). Renting VMs for an unmodified monolith uses the delivery model without exploiting it.
</panel>

**Q2.** Name the four design considerations for distributed apps given in the lecture, and say which one a "no-downtime deployment" addresses.
<panel type="seamless" minimized header="%%Answer%%">

Not tied to a specific host or network; the end user is unaffected by hardware/software failure; accessible as workload increases; no downtime when rolling out updates. The last consideration is the one no-downtime deployment addresses.
</panel>

</panel>

<span id="W5-c2"></span>

### W5.2 Cloud computing vs cloud native ★

**Cloud computing and cloud native answer two different questions — where versus how — and confusing them is the most common conceptual error in this topic.** Cloud computing is a delivery model for resources. Cloud native is an approach to building and running applications that exploits that delivery model.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-cloud-native" trim />
</box>

**How it works:**

**Cloud native is defined by what it enables, and the lecture names five target qualities.** Scalability, loose coupling, resilience, manageability, and observability — these are the reasons to go cloud native. (Source: L5 slide 8, Dell guest lecture.)

**The approach is realized through a specific set of enablers.** Containers, service meshes, microservices, immutable infrastructure, and declarative APIs are the lecture's "how to be cloud native" checklist; W5.3–W5.6 cover the ones this course develops in depth. (Source: L5 slides 9–10, Dell guest lecture.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-service-mesh" trim />
</box>

**The five qualities answer the pressures W5.1 traced.** Scalability answers the design consideration "accessible as workload increases"; resilience answers "the end user should not be affected by a failure"; manageability and observability answer the pace challenge — "how can we respond to market changes and business needs?" (slide 14); loose coupling is what makes the others achievable at all. (Source: L5 slides 8, 14, 16, Dell guest lecture.)

{% call example("L5 slide 6 — the CNCF definition, read closely") %}
The lecture quotes the CNCF definition in full: cloud native technologies "empower organizations to build and run **scalable applications** in modern, **dynamic environments** such as public, private, and hybrid clouds. **Containers, service meshes, microservices, immutable infrastructure, and declarative APIs** exemplify this approach. These techniques enable **loosely coupled systems** that are **resilient, manageable, and observable**. Combined with robust automation, they allow engineers to make high-impact changes frequently and predictably with minimal toil." Every bolded phrase is one of the lecture's reasons or enablers — the definition is a compressed map of the whole lecture.
{% endcall %}

<box type="tip" seamless>
**Tip:** when revising, keep the two-column contrast from the lecture: cloud computing → **where** (resource pooling, rapid elasticity, broad network access, pay-as-you-go, on-demand self-service, measured service); cloud native → **how** (architecture: containers, microservices, immutable infrastructure, declarative APIs). Assessment questions often test exactly this distinction. (Source: L5 slides 4–5, Dell guest lecture.)
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Sort these six items into "cloud computing characteristic" or "cloud native enabler": resource pooling; containers; pay-as-you-go; microservices; rapid elasticity; immutable infrastructure.
<panel type="seamless" minimized header="%%Answer%%">

Cloud computing characteristics: resource pooling, pay-as-you-go, rapid elasticity. Cloud native enablers: containers, microservices, immutable infrastructure.
</panel>

**Q2.** Which of the five "why go cloud native" qualities would you invoke to argue for a service mesh?
<panel type="seamless" minimized header="%%Answer%%">

Service meshes primarily support manageability and observability (traffic management and telemetry between services), and they reinforce loose coupling by moving communication concerns out of application code. Any of those, well-argued, is acceptable.
</panel>

</panel>

<span id="W5-c3"></span>

### W5.3 From monolith to microservices ★

**The monolith's limitations are the strongest motivation for the cloud-native style, and the lecture builds microservices as their direct answer.** Understanding what a monolith cannot do tells you exactly what problem microservices solve — and what new problems they create.

**How it works:**

**A monolithic app is one unit of deployment running as a single service.** All functionality — login, registration, catalog, reviews, cart, payment — lives in one process backed by one database, so all functionalities and processes are tightly {{ term("coupled", "coupling measures how strongly one part depends on another; tight coupling means changes in one part force changes in the other") }}. (Source: L5 slides 18–20, Dell guest lecture.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-monolith" trim />
</box>

**The lecture lists seven limitations of a monolithic app.** One unit of deployment; all functionalities and processes tightly coupled; running as a single service; adding new features becomes more complex over time; lock-in to a particular technology stack; low fault tolerance; scaling limitations. (Source: L5 slide 20, Dell guest lecture.)

**A {{ term("microservice", "an independently deployable service modeled around a business domain") }} is the unit that fixes deployability, coupling, and scaling.** The lecture defines microservices as independently deployable services modeled around a business domain — small and lightweight, communicating with one another via APIs over standard network protocols (HTTP, and AMQP — the Advanced Message Queuing Protocol that message brokers speak; Weeks 9–11 cover it), and technology-agnostic. (Source: L5 slide 21, Dell guest lecture.) %%The microservice style is developed in depth in the Week 7 chapter.%%

**Why microservices: the lecture's list of buys is a point-by-point inversion of the monolith's limits.** Faster startup time and better testability (small units); independent deployability (no all-or-nothing releases); independent scalability (scale one service, not the whole app); improved fault isolation (one service failing does not take down the rest); technology-agnostic (no stack lock-in). (Source: L5 slide 22, Dell guest lecture.)

**Structurally, monoliths and microservices differ in coupling and cohesion.** Monoliths: tight coupling, low {{ term("cohesion", "cohesion measures how strongly related the functionality inside one part is; low cohesion means unrelated duties share one part") }}. Microservices: loose coupling, high cohesion. (Source: L5 slides 23–24, Dell guest lecture.)

{% call example("L5 slides 18–19 vs 25 — the shopping app, before and after") %}
The lecture uses one running example. **Before:** a monolith containing User Login, Registration, Product Catalog, User Reviews, Shopping Cart, and Payment in a single deployable unit over a single database. **After:** a microservice architecture where each capability becomes its own service — login, registration, catalog, reviews, cart, payment — and each service gets **its own database**. The lecture then immediately warns: "We have created a new problem here" — six services and six databases are harder to host, connect, and operate than one unit, which is exactly the problem W5.4 and W5.5 address. (Source: L5 slides 25–26, Dell guest lecture.)
{% endcall %}

The diagram below contrasts the two structures and shows why hosting becomes the new problem: one unit over one database becomes six services over six databases, each needing to be deployed and run somewhere.

<mermaid>
flowchart LR
  subgraph monolith["Monolith — one deployable unit"]
    direction TB
    app["User Login · Registration · Product Catalog · User Reviews · Shopping Cart · Payment"]
    db[(One shared database)]
    app --> db
  end
  subgraph micro["Microservices — one service per business capability"]
    direction TB
    login["Login service"] --> dbl[(DB)]
    reg["Registration service"] --> dbr[(DB)]
    cat["Catalog service"] --> dbc[(DB)]
    rev["Reviews service"] --> dbv[(DB)]
    cart["Cart service"] --> dbt[(DB)]
    pay["Payment service"] --> dbp[(DB)]
  end
</mermaid>

%%Notation: boxes are components or services, cylinders are data stores, and a solid arrow is a synchronous call or data access.%% To read it: on the left, all six capabilities ship together as one unit touching one shared database — a fault or a deployment in any capability affects all of them. On the right, each capability owns its service and its data, so payment can be deployed, scaled, or repaired alone; the cost is six deployables and six databases to host and operate, which is the "new problem" the lecture names.

<box type="warning" seamless>
**Pitfall:** treating microservices as automatically better. Splitting the shopping app multiplies deployment units and data stores; unless you also solve hosting, orchestration, and data consistency (W5.5 and Week 8), you inherit operational complexity without the buys.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** The monolith is "one unit of deployment". Why does that make scaling limited?
<panel type="seamless" minimized header="%%Answer%%">

You can only replicate the whole unit. If payment is the hot spot, you must scale login, catalog, reviews, and cart along with it, paying for resources those capabilities do not need. Microservices make the service the unit of scaling.
</panel>

**Q2.** In the lecture's monolith-vs-microservices table, which pairing replaces "tight coupling / low cohesion"?
<panel type="seamless" minimized header="%%Answer%%">

Loose coupling and high cohesion — each service keeps strongly related functionality together (cohesion) while depending on other services only through APIs (loose coupling).
</panel>

</panel>

<span id="W5-c4"></span>

### W5.4 Containers ★

**Once an application is split into many small services, you need a standard way to package and run each one anywhere — that is exactly what a container is.** The lecture poses the question "where do we host them?" for a monolith (on an OS, in a VM) and answers it for microservices with containers. (Source: L5 slides 27–29, Dell guest lecture.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-container" trim />
</box>

**How it works:**

**A container bundles the full runtime context of one application.** The lecture draws a container as three stacked layers: the app, the app's libraries and dependencies, and the language runtime — everything the code needs, and nothing of the host. (Source: L5 slide 30, Dell guest lecture.)

**{{ term("Docker", "an open-source containerization platform that packages applications into portable container images") }} made this packaging an industry standard.** Docker launched in 2013 and created the industry standard for containers, delivering seamless portability — build once, run anywhere — in a lightweight, cloud-agnostic way. (Source: L5 slide 32, Dell guest lecture.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-docker" trim />
</box>

{% call example("L5 slides 30 and 51 — 'My Spring Boot App' as a container") %}
A team writes a Spring Boot payment service. The container image holds the Spring Boot app, its app libraries and dependencies (the JARs it needs), and the Java language runtime. Because the image carries its own runtime, the same image runs identically on a developer's laptop and on a cloud host — "build once, run anywhere". This is the same payment service the lecture later runs as a Payment Pod in W5.5.
{% endcall %}

**The lecture's five container benefits are abstractions doing work.** Separation of responsibility (developers define what runs; the platform defines where it runs); workload portability; application isolation; greater resource efficiency; and improved developer productivity. (Source: L5 slide 33, Dell guest lecture.)

**Tutorial 4 develops the same idea with the shipping-container analogy.** Just as the intermodal container let 1960s shipping move almost any cargo between ship, train, and truck without unpacking — because transport infrastructure only needed to know how to handle the container, not what was inside — a software container lets any application move between laptop, datacenter, and cloud because the host only needs to know how to run containers. The tutorial also separates **container image** (the blueprint: what goes in the container), **container** (a running instance of that image), and **container engine** (the runtime that builds and manages containers — Docker is one), then walks through deploying a web app with them. See the [Week 6 tutorial]({{baseUrl}}/schedule/week6/tutorial.html) and its model solution. (Source: Tutorial 4 Q2 and model solution.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-container-image" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-container-engine" trim />
</box>

<box type="warning" seamless>
**Pitfall:** a container is not a virtual machine. A VM virtualizes hardware and carries a whole guest OS; a container packages an application against its runtime and shares the host OS kernel. The lecture's hosting ladder — monolith on an OS, in a VM, in a container — gets lighter and starts faster at each step. (Source: L5 slide 28, Dell guest lecture.)
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Which property of the intermodal shipping container corresponds to "abstracts applications from the environment in which they actually run"?
<panel type="seamless" minimized header="%%Answer%%">

Isolation plus a standard interface: the container seals its contents off from the transport system, and the infrastructure only handles the standard container — never the cargo inside. Likewise the host runs the standard container without knowing the app's dependencies.
</panel>

**Q2.** A service runs fine on your machine but fails on the server with a missing library. Which container claim from the lecture addresses this, and how?
<panel type="seamless" minimized header="%%Answer%%">

"Abstracts applications from the environment in which they actually run" (L5 slide 31): the missing library is part of the image's dependencies, so the same image that worked on your machine carries it to the server — build once, run anywhere.
</panel>

</panel>

<span id="W5-c5"></span>

### W5.5 Orchestrating containers with Kubernetes ★★

**Containers solve packaging, but dozens of containers create container sprawl — a new set of challenges that container orchestration exists to solve.** The lecture moves from "what is a container" to "who restarts, balances, and scales the many containers our services now need". (Source: L5 slides 34–37, Dell guest lecture.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-container-orchestration" trim />
</box>

**How it works:**

**{{ term("Kubernetes", "a container orchestration platform: an environment for running distributed apps on containers at scale") }} is the orchestration platform the lecture centers on.** Kubernetes was originally developed by Google, open-sourced in 2014, is the flagship project of the Cloud Native Computing Foundation, and defines a common set of resources and an API for manipulating them. (Source: L5 slide 39, Dell guest lecture.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-kubernetes" trim />
</box>

**Kubernetes does not manage containers directly; it manages {{ term("pods", "the smallest deployable unit in Kubernetes; a container resides inside a pod, which has a unique IP address in the cluster") }}.** The lecture's app becomes a Payment Pod, a Product Pod, an Inventory Pod, and a Shopping Cart Pod. (Source: L5 slides 50–54, Dell guest lecture.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-pod" trim />
</box>

**A {{ term("deployment", "a Kubernetes resource that declares the desired number of pod replicas and enforces it") }} declares how many replicas of a pod you want — and the cluster enforces it.** When the single Payment Pod dies, the Payment Deployment (replicas = 1) notices the gap and starts a replacement: self-healing. (Source: L5 slides 56–58, Dell guest lecture.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-kubernetes-deployment" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-self-healing" trim />
</box>

**Self-healing is a reconcile loop, not a one-off fix.** Kubernetes runs control loops — non-terminating loops that regulate the state of the system — driving **desired state = actual state**; controllers such as the Deployment Controller and Job Controller each own one kind of resource. (Source: L5 slide 59, Dell guest lecture.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-reconcile-loop" trim />
</box>

**Scaling is changing the declared replica count.** Under high traffic, the Payment Deployment goes from replicas = 1 to replicas = 3, and three Payment Pods run: {{ term("horizontal scaling", "scaling by adding more instances (replicas) of the service, rather than a bigger machine — Week 12 develops scaling in full") }}, declared rather than manual. (Source: L5 slides 60–64, Dell guest lecture.)

{% call example("L5 slides 54–64 — the payment service through one afternoon") %}
The lecture's app has four pods: Payment, Product, Inventory, Shopping Cart. During the lunch-hour rush, payment requests queue up. The team raises the Payment Deployment's `replicas` from 1 to 3; the reconcile loop schedules two more Payment Pods, and traffic spreads across three replicas. Shortly after, one Payment Pod crashes; the loop notices actual state (2 pods) ≠ desired state (3 pods) and starts a replacement within seconds — users notice nothing. This one scenario exercises horizontal scaling, self-healing, and the reconcile loop at once.
{% endcall %}

**The deepest payoff: Kubernetes abstracts away the infrastructure itself.** Apps sit on Kubernetes, and Kubernetes sits on pools of compute, network, and storage — so applications stop being tied to specific hosts, which is the first design consideration from W5.1. Kubernetes runs on data centers, cloud, bare metal, VMs, even PCs and laptops: "Kubernetes everywhere". (Source: L5 slides 41 and 65–66, Dell guest lecture.)

The diagram below shows the two-layer abstraction the lecture builds: you declare services to Kubernetes; Kubernetes borrows whatever compute, network, and storage it needs.

<mermaid>
flowchart TB
  subgraph services["What you declare: your services"]
    pay["Payment pod"]
    prod["Product pod"]
    inv["Inventory pod"]
    cart["Shopping Cart pod"]
  end
  subgraph k8s["What reconciles them: Kubernetes"]
    dep["Deployments · reconcile loop · scheduling"]
  end
  subgraph infra["What gets abstracted away: infrastructure"]
    compute["Compute"]
    network["Network"]
    storage["Storage"]
  end
  services --> k8s
  k8s --- infra
</mermaid>

%%Notation: boxes are services or platform components; a solid arrow is a dependency (the upper layer runs on the lower one); the plain link between Kubernetes and infrastructure marks the boundary the abstraction hides.%% To read it: the four pods are what the team **declares** ("payment, replicas = 3"), not what the team places. Kubernetes owns the middle layer — deployments, the reconcile loop, scheduling — so when a pod dies or traffic spikes, the fix happens below the line where services are declared, on whatever compute, network, and storage the cluster borrows at that moment. In the lecture's example, the crashed Payment Pod is simply rescheduled onto different infrastructure with no change to what the team declared.

<box type="warning" seamless>
**Pitfall:** reading Kubernetes as a reason to skip architecture. Orchestration automates hosting concerns (restarts, scaling, rollouts); it does not decide service boundaries, data ownership, or communication styles. Those remain design decisions — the distributed-systems fallacies the lecture points to (the network is reliable, bandwidth is infinite, …) are still yours to design around. (Source: L5 slides 37 and 40, Dell guest lecture.)
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** A Payment Pod crashes and a replacement is running thirty seconds later. Which concept explains the replacement — and which component performed it?
<panel type="seamless" minimized header="%%Answer%%">

Self-healing, performed by the reconcile loop: the Payment Deployment's controller observed actual state (0 pods) ≠ desired state (replicas = 1) and scheduled a replacement pod.
</panel>

**Q2.** Why does the lecture say Kubernetes "abstracts away the infrastructure"? Name the two layers it places between your app and the machines.
<panel type="seamless" minimized header="%%Answer%%">

Because you no longer bind apps to hosts: layer one is Kubernetes (deployments, reconcile loop, scheduling), layer two is the pooled compute/network/storage it schedules onto. The app is declared once and runs on whatever resources the cluster provides.
</panel>

</panel>

<span id="W5-c6"></span>

### W5.6 Immutable infrastructure and IaC ★★

**Cloud-native operations stop treating servers as pets to nurse and start treating them as cattle to replace — and infrastructure as code is what makes replacing them routine.** This is the last enabler pair in the lecture, and the one that connects hosting back to the automation ideas of modern software engineering. (Source: L5 slides 42–49, Dell guest lecture.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-immutable-infrastructure" trim />
</box>

**How it works:**

**Mutable infrastructure is the traditional habit the lecture warns against.** Computers and software systems have traditionally been treated as mutable infrastructure: incremental updates such as system and software patches are applied across a period of time, which leads to inconsistencies and dependencies on the underlying infrastructure. (Source: L5 slide 42, Dell guest lecture.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-mutable-infrastructure" trim />
</box>

**{{ term("pets vs cattle", "the operations metaphor: unique, nursed servers (pets) vs identical, numbered instances that are replaced when sick (cattle)") }} names the two operation styles.** Pets are unique (Max, Milo, Lucky…), cared for, and nursed back to health when sick. Cattle are similar (Cow-1, Cow-2, Cow-3…), assigned ID numbers, and replaced with another when one gets sick. Immutable infrastructure is the cattle model: do not patch a sick server — replace it. (Source: L5 slide 43, Dell guest lecture.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-pets-vs-cattle" trim />
</box>

**The shift from pets to cattle is the shift from repairing unique machines to replacing interchangeable ones.**

<mermaid>
flowchart LR
    subgraph PETS["Pets — treated as unique"]
        direction LR
        P1["server 'Max'"] -->|"gets sick"| P2["nurse back<br/>to health"] --> P1
    end
    subgraph CATTLE["Cattle — treated as identical"]
        direction LR
        C1["cow-1"] -->|"gets sick"| C2["replace with<br/>another instance"] --> C3["cow-2"]
    end
</mermaid>

%%Notation: each box is a server (or herd member); solid arrows are the operator's reaction to failure. Left: diagnose and repair the same machine (mutable infrastructure). Right: discard and re-create from the golden image — the one versioned image every replica is built from (immutable infrastructure).%%

How to read it: in the lecture's Kubernetes world this is concrete: a Payment Pod is cattle — when it dies (L5 slide 57), the Deployment does not nurse it but starts a fresh identical Pod from the image (slide 58), which is the self-healing loop drawn in the W5.5 reconcile diagram. Immutable infrastructure (W5.6) is what makes the right-hand flow cheap: images are reproducible, so replacement *is* the repair.

{% call example("L5 slides 42–43 vs the Payment Deployment — the same shift twice") %}
Under the pets model, the team's production app server "Hermes" has been patched for three years; when it misbehaves, someone logs in and fixes it, and nobody else knows exactly what is on it. %%external example%% Under the cattle model, the Payment Deployment declares replicas = 3; when one pod misbehaves, it is destroyed and replaced from the same image, so every replica is identical. The lecture's self-healing (W5.5) is only possible because the infrastructure is immutable: a replacement built from a fixed image is guaranteed to match the healthy replicas.
{% endcall %}

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-infrastructure-as-code" trim />
</box>

**IaC turns the cattle model into a repeatable process.** Managing and provisioning infrastructure is automated using configuration files that are codified and documented — human readable, machine consumable, and reproducible. (Source: L5 slide 45, Dell guest lecture.)

**The lecture's IaC benefits read like a quality-attribute list for infrastructure.** Rapid deployment of complex environments; reduced configuration drift; consistent, predictable, repeatable, reusable, maintainable environments; source control as a single source of truth for your infrastructure; and a critical component of DevOps and CI/CD. (Source: L5 slide 46, Dell guest lecture.)

**IaC files are usually declarative, and that matters architecturally.** The lecture contrasts the declarative approach — declare the end state you want, as Kubernetes manifests (the declarative files that describe your pods and deployments) do — with the imperative approach — script the individual steps to reach it. Declarative fits the reconcile loop of W5.5: the loop can only drive desired state = actual state if desired state is written down as data. (Source: L5 slides 45–47, Dell guest lecture.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-05.md#def-declarative-approach" trim />
</box>

<box type="warning" seamless>
**Pitfall:** keeping "one special" server outside the code. A hand-patched machine that is not described in configuration files is a pet in a cattle herd: it cannot be reproduced, it drifts from the declared state, and the reconcile loop has nothing to reconcile it against.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Your cluster's database VM has been patched in place for two years. Name the anti-pattern and the practice that replaces it.
<panel type="seamless" minimized header="%%Answer%%">

Mutable infrastructure — the "pet" style. Replace it with immutable infrastructure: build a fresh instance from a versioned image/configuration and replace, not patch, using IaC so the process is reproducible.
</panel>

**Q2.** Why does the lecture call IaC "a critical component of DevOps and CI/CD"?
<panel type="seamless" minimized header="%%Answer%%">

Because CI/CD automates building, testing, and releasing software; IaC extends the same pipeline discipline (version-controlled files, review, repeatable execution) to the environments that software runs in — environments become releasable artifacts too.
</panel>

</panel>

<box type="info" seamless>

**Section summary:**

* **The cloud is an abstraction** over pooled compute, storage, and networking; **cloud computing** says where resources come from, **cloud native** says how apps must be built to exploit them (W5.1–W5.2).
* **Microservices answer the monolith's limits** — one deployment unit, tight coupling, low fault tolerance, scaling limits — with independently deployable, technology-agnostic services, at the price of many deployables and data stores (W5.3).
* **Containers standardize what runs; Kubernetes standardizes where and how many** — pods, deployments, reconcile loops, horizontal scaling, infrastructure abstracted away (W5.4–W5.5).
* **Immutable infrastructure + IaC make operations repeatable** — replace, don't patch; declare, don't script (W5.6).
</box>

## Connections

| Concept | Lecture | Tutorial | Other weeks |
|---|---|---|---|
| Cloud as abstraction; design considerations for distributed apps | L5 slides 3–16 | Tutorial 3 Q1 (NewsTrack component architecture) | W4 (architecture, components) |
| Cloud computing vs cloud native | L5 slides 4–10 | — | W12 (scalability as a quality attribute) |
| Monolith limits → microservices | L5 slides 15–26 | Tutorial 3 Q1 (separating source-dependent from pure-processing components) | W7 (microservice style, DDD) |
| Containers, images, Docker | L5 slides 27–33 | Tutorial 4 Q2 (cargo-container analogy; image vs container vs engine) | W6 (deployment), W7 (service-per-container deployment) |
| Orchestration: pods, deployments, self-healing, scaling | L5 slides 34–41, 50–66 | — | W7 (independent deployability), W12 (scaling) |
| Immutable infrastructure, IaC, declarative vs imperative | L5 slides 42–49 | — | W2 (modern software engineering, CI/CD) |

## Further reading

* CNCF's full cloud-native definition (quoted on L5 slide 6): [github.com/cncf/toc — DEFINITION.md](https://github.com/cncf/toc/blob/main/DEFINITION.md)
* Kubernetes basics — pods and deployments (extends L5 slides 50–64): [kubernetes.io — Pods](https://kubernetes.io/docs/concepts/workloads/pods/) and [kubernetes.io — Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
* The Google Kubernetes comic the lecture cites for orchestration and declarative-vs-imperative (L5 slides 37, 47–49): [cloud.google.com — Kubernetes comic](https://cloud.google.com/kubernetes-engine/kubernetes-comic)
* State of Kubernetes 2025 findings quoted on L5 slides 69–70: [spectrocloud.com — State of Kubernetes 2025](https://www.spectrocloud.com/state-of-kubernetes-2025)

## Summary

**Key takeaways:**

* **The cloud is an abstraction** over pooled, on-demand compute, storage, and networking, and distributing an app brings four design considerations: no host lock-in, user unaffected by failure, accessible under growing load, no-downtime updates. (W5.1)
* **Cloud computing is the delivery model (where); cloud native is the architecture (how)** — containers, microservices, immutable infrastructure, and declarative APIs, aimed at scalability, loose coupling, resilience, manageability, and observability. (W5.2)
* **A microservice is an independently deployable service modeled around a business domain**, fixing the monolith's deployability, coupling, fault-tolerance, and scaling limits — while creating a hosting problem of its own. (W5.3)
* **A container packages an app with its full runtime context** — build once, run anywhere — making it the standard unit of cloud-native deployment. (W5.4)
* **Container orchestration (Kubernetes) manages containers at scale** through pods, deployments, reconcile loops, self-healing, and horizontal scaling, abstracting the infrastructure away. (W5.5)
* **Immutable infrastructure and IaC make operations repeatable**: replace rather than patch, and declare rather than script. (W5.6)

**Key terms:**

| Term | Definition | Unit |
|---|---|---|
| Cloud computing | On-demand, pooled, metered delivery of computing resources over the network | [W5.1](#W5-c1) |
| Cloud native | An approach to building and running applications that exploits the cloud computing delivery model | [W5.2](#W5-c2) |
| Service mesh | A dedicated infrastructure layer for service-to-service traffic management and telemetry, kept out of application code | [W5.2](#W5-c2) |
| Monolith | One unit of deployment running as a single service — all functionality in one process over one database | [W5.3](#W5-c3) |
| Microservice | An independently deployable service modeled around a business domain (full treatment in Week 7) | [W5.3](#W5-c3) |
| Container | A standardized unit packaging an app with all its dependencies, abstracting it from the environment | [W5.4](#W5-c4) |
| Container image | The read-only blueprint (filesystem, commands, dependencies, config) from which containers are created | [W5.4](#W5-c4) |
| Container engine | The runtime that builds, runs, and manages containers — the interface between host OS and containers | [W5.4](#W5-c4) |
| Docker | The open-source containerization platform (2013) that created the industry standard — build once, run anywhere | [W5.4](#W5-c4) |
| Container orchestration | Automated management of containers at scale: discovery, rollouts, auto-scaling, self-healing | [W5.5](#W5-c5) |
| Kubernetes | The container orchestration platform for running distributed apps on containers at scale (CNCF flagship) | [W5.5](#W5-c5) |
| Pod (Kubernetes) | The smallest deployable unit in Kubernetes; a container resides inside a pod with a unique cluster IP | [W5.5](#W5-c5) |
| Deployment (Kubernetes) | A declaration of the desired number of pod replicas, enforced by a reconcile loop | [W5.5](#W5-c5) |
| Self-healing | A failed pod is automatically replaced: actual state is reconciled back to the declared desired state | [W5.5](#W5-c5) |
| Reconcile loop | A non-terminating control loop driving desired state = actual state; Kubernetes controllers own one resource kind each | [W5.5](#W5-c5) |
| Horizontal scaling | Scaling by adding replicas of the service (full treatment in Week 12) | [W5.5](#W5-c5) |
| Immutable infrastructure | Servers as replaceable, not repairable: replace from a fixed image instead of patching | [W5.6](#W5-c6) |
| Mutable infrastructure | The traditional patch-in-place habit — incremental updates cause inconsistencies and hidden dependencies | [W5.6](#W5-c6) |
| Pets vs cattle | Operation metaphor: unique, nursed servers (pets) vs identical, replaced instances (cattle) | [W5.6](#W5-c6) |
| Infrastructure as code | Managing infrastructure through version-controlled, reproducible configuration files | [W5.6](#W5-c6) |
| Declarative approach | Declare the end state and let the platform reconcile toward it — vs scripting the steps (imperative) | [W5.6](#W5-c6) |

%%Next: [Week 6]({{baseUrl}}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html) turns from where software runs to how it is organized, classifying the classical architectural styles and introducing REST — the uniform interface that the services you just containerized will speak.%%
</div>
