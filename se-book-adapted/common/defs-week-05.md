{# Definitions for week-05. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-05.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable. #}

<span id="def-cloud-computing">

**Cloud computing** is a model for on-demand delivery of computing resources — compute, storage, networking, and services — over the network, pooled across many users and billed by use. Its essential characteristics are on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service, and pay-as-you-go pricing.

%%Source: L5 slides 4–5 (guest lecture by Dell).%%

</span>

<span id="def-cloud-native">

**Cloud native** is an approach to building and running applications that exploits the advantages of the cloud computing delivery model. Cloud native technologies — containers, service meshes, microservices, immutable infrastructure, and declarative APIs — enable loosely coupled systems that are resilient, manageable, and observable.

%%Source: L5 slides 5–9 (guest lecture by Dell), quoting the Cloud Native Computing Foundation definition.%%

</span>

<span id="def-container">

**A container** is a standardized unit for developing, deploying, and distributing software: it packages an application together with everything it needs to run — language runtime, libraries, executables, and configuration — and abstracts the application from the environment it runs in.

%%Source: L5 slides 30–31 (guest lecture by Dell).%%

</span>

<span id="def-container-orchestration">

**Container orchestration** is the automated management of containers at scale: service discovery and load balancing, storage orchestration, automated rollouts and rollbacks, auto-scaling, self-healing, and secret and configuration management. Kubernetes is the dominant orchestration platform.

%%Source: L5 slides 38–39 (guest lecture by Dell).%%

</span>

<span id="def-immutable-infrastructure">

**Immutable infrastructure** treats servers as replaceable rather than repairable: instead of applying incremental updates to a long-lived machine, you replace the machine with a fresh instance built from a fixed image. This avoids the inconsistencies and hidden dependencies that accumulate when running systems are patched in place.

%%Source: L5 slides 42–43 (guest lecture by Dell).%%

</span>

<span id="def-infrastructure-as-code">

**Infrastructure as code (IaC)** is the practice of managing and provisioning infrastructure through configuration files that are human-readable, machine-consumable, and version-controlled, so that environments are consistent, predictable, repeatable, and reproducible.

%%Source: L5 slides 45–46 (guest lecture by Dell).%%

</span>

<span id="def-monolith">

A **monolith** (monolithic application) is one unit of deployment running as a single service: all functionality — login, registration, catalog, reviews, cart, payment — lives in one process, typically backed by one database. The lecture's seven limitations: one unit of deployment; all functionalities and processes tightly coupled; running as a single service; adding features becomes more complex over time; lock-in to a technology stack; low fault tolerance; scaling limitations.

%%Source: L5 slides 18–20 (guest lecture by Dell).%%

</span>

<span id="def-service-mesh">

A **service mesh** is a dedicated infrastructure layer for managing service-to-service communication — traffic management and telemetry between services — kept out of application code; the lecture names it among the cloud-native enablers.

%%Source: L5 slides 9–10 (guest lecture by Dell); characterized in the W5.2 self-check.%%

</span>

<span id="def-docker">

**Docker** is an open-source containerization platform, launched in 2013, that created the industry standard for containers: seamless portability — build once, run anywhere — in a lightweight, cloud-agnostic way.

%%Source: L5 slide 32 (guest lecture by Dell).%%

</span>

<span id="def-container-image">

A **container image** is the read-only blueprint from which containers are created — the file-system layout, commands, dependencies, and configuration — ensuring consistent behavior of the same image across systems.

%%Source: Tutorial 4 model solution (Q2d), with L5 slide 30 (guest lecture by Dell).%%

</span>

<span id="def-container-engine">

A **container engine** provides the runtime environment and the interface between the host OS and the containers: it builds, runs, and manages containers — Docker is one.

%%Source: Tutorial 4 model solution (Q2d–e).%%

</span>

<span id="def-container-sprawl">

**Container sprawl** is the proliferation of so many containers — one problem the microservices split creates — that manually hosting, restarting, and scaling them becomes impractical; container orchestration exists to answer it.

%%Source: L5 slides 34–37 (guest lecture by Dell).%%

</span>

<span id="def-kubernetes">

**Kubernetes** is a container orchestration platform — an environment for running distributed apps on containers at scale. Originally developed by Google and open-sourced in 2014, it is the flagship project of the Cloud Native Computing Foundation (CNCF) and defines a common set of resources and an API for manipulating them.

%%Source: L5 slide 39 (guest lecture by Dell).%%

</span>

<span id="def-pod">

A **pod** is the smallest deployable unit in Kubernetes: Kubernetes does not manage containers directly — a container resides inside a pod, which manages the container and has a unique IP address within the Kubernetes cluster.

%%Source: L5 slides 50–54 (guest lecture by Dell).%%

</span>

<span id="def-kubernetes-deployment">

A **Kubernetes deployment** declares the desired number of pod replicas and enforces the declaration: when a pod dies, the deployment notices the gap and starts a replacement (self-healing); scaling means changing the declared replica count (horizontal scaling).

%%Source: L5 slides 56–64 (guest lecture by Dell).%%

</span>

<span id="def-self-healing">

**Self-healing** is the orchestration behavior in which a failed pod is automatically replaced: the deployment's controller observes that actual state no longer matches desired state and schedules a fresh replica within seconds.

%%Source: L5 slides 56–58 (guest lecture by Dell).%%

</span>

<span id="def-reconcile-loop">

A **reconcile loop** is a control loop — a non-terminating loop that regulates the state of the system by driving desired state = actual state. Kubernetes controllers (e.g., the Deployment Controller and Job Controller, run by the kube-controller-manager) each own one kind of resource.

%%Source: L5 slide 59 (guest lecture by Dell).%%

</span>

<span id="def-mutable-infrastructure">

**Mutable infrastructure** is the traditional treatment of computers and software systems as repairable: incremental updates such as system and software patches are applied across a period of time, which leads to inconsistencies and dependencies on the underlying infrastructure.

%%Source: L5 slide 42 (guest lecture by Dell).%%

</span>

<span id="def-pets-vs-cattle">

**Pets vs cattle** is the operations metaphor for the two infrastructure styles: pets are unique (Max, Milo, Lucky…), cared for, and nursed back to health when sick; cattle are similar (Cow-1, Cow-2, Cow-3…), assigned ID numbers, and replaced with another instance when one gets sick. Immutable infrastructure is the cattle model.

%%Source: L5 slide 43 (guest lecture by Dell).%%

</span>

<span id="def-declarative-approach">

The **declarative approach** declares the end state you want — as Kubernetes manifests and IaC configuration files do — and lets the platform reconcile reality toward it; the **imperative approach** scripts the individual steps to reach the state. Declarative fits the reconcile loop: the loop can only drive desired state = actual state if the desired state is written down as data.

%%Source: L5 slides 45–47 (guest lecture by Dell).%%

</span>
