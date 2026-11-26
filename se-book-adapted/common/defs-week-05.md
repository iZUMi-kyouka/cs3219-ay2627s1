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
