{# Definitions for week-01. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-01.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable. #}

<span id="def-software-engineering">

**Software engineering** is the application of a systematic, disciplined, quantifiable approach to the development, operation, and maintenance of software.

<sub>-- IEEE Standard Glossary of Software Engineering Terminology, quoted on L1 slide 13</sub>

</span>

<span id="def-software-process">

A **software process** is the structured set of activities a team follows to develop, operate, and maintain software — typically requirements, design, implementation, testing, deployment, and maintenance. A process model prescribes how those activities are arranged, for example Scrum's iterative sprints with feedback loops.

<sub>-- cf. IEEE definition of software engineering, L1 slides 13, 22–24</sub>

</span>

<span id="def-sdlc">

The **software development life cycle (SDLC)** is the full life of a software product, from initial conception through development, deployment, and operation, to maintenance and eventual retirement. A software process describes how the team organizes work across those life-cycle phases.

<sub>-- cf. L1 slides 13, 22, 26</sub>

</span>

<span id="def-software-crisis">

The **software crisis** is the 1960s mismatch between what software projects delivered and what was needed: its impact was on time, cost, and quality. The response — R&D in software engineering — produced the sub-fields this course teaches: software development process models, software architecture, design principles, testing methods, and design patterns.

<sub>-- L1 slide 13; Dijkstra, The Humble Programmer (EWD340)</sub>

</span>

<span id="def-software-crisis-2">

**Software Crisis 2.0** (1970–now) is the second software crisis, driven by abundance rather than scarcity: push factors (advances in hardware, reductions in hardware costs, increases in processing power, device proliferation, an effectively infinite amount of data available) and pull factors (digital natives consuming technology) create lots of data and lots of computation. Named responses include parallel processing, cloud computing, data analytics, security, IoT, edge computing, DevOps, CI/CD, and microservices.

<sub>-- L1 slide 14, after Fitzgerald, Software Crisis 2.0 (IEEE Computer, 2013)</sub>

</span>

<span id="def-cloud-service-models">

The **cloud service models** — IaaS, PaaS, and SaaS — differ in how much of the stack the vendor manages: **IaaS** rents raw infrastructure (e.g., AWS, Google Cloud); **PaaS** hosts your application on a managed platform (e.g., AWS Elastic Beanstalk, Heroku); **SaaS** delivers a finished application (e.g., Google Apps, Salesforce).

<sub>-- L1 slide 17</sub>

</span>

<span id="def-cloud-enabled">

**Cloud-enabled** describes legacy enterprise applications designed for local data centres but modified to run on the cloud, retaining most of their original features — as opposed to cloud-native applications, which are built for cloud environments from the start.

<sub>-- L1 slide 17</sub>

</span>

<span id="def-open-content">

**Open-content** is material — text, media, datasets — that others may legally copy, modify, and redistribute; it is the data-side sibling of open-source (code you may inspect) and the opposite of closed-source (code you cannot).

<sub>-- L1 slide 16; e.g., Wikipedia's articles</sub>

</span>

<span id="def-embedded-software">

**Embedded software** is software that runs inside a dedicated device and interacts directly with the hardware it controls or senses — the "embedded & edge" deployment mode, e.g., a smart-home camera's local motion detection or an industrial control system.

<sub>-- L1 slide 16; Tutorial 1 applications A and D</sub>

</span>

<span id="def-real-time-system">

A **real-time** system must respond to stimuli within strict timing constraints — a late answer is a failed answer, e.g., software controlling machinery in a manufacturing plant.

<sub>-- L1 slide 16; Tutorial 1 application D</sub>

</span>

<span id="def-concurrent-system">

A **concurrent** system handles many users or operations at the same time, e.g., a global streaming platform accessed by millions of users concurrently.

<sub>-- L1 slide 16; Tutorial 1 application B</sub>

</span>

<span id="def-distributed-system">

A **distributed** system's components run on multiple networked machines and coordinate over the network, e.g., cameras that process motion locally while cloud services store video and send notifications.

<sub>-- L1 slide 16; Tutorial 1 application A</sub>

</span>

<span id="def-scrum">

**Scrum** is an agile software process built on iterative development with feedback loops: work happens in fixed sprints, opened by sprint planning, and each sprint ends with a working increment that generates feedback — enabling quick response to changes.

<sub>-- L1 slide 23</sub>

</span>

<span id="def-sprint">

A **sprint** is one fixed-length iteration of Scrum: sprint planning picks the top-priority items from the product backlog, the team designs, builds, and tests them, and the sprint ends with a working increment (+ demo & feedback).

<sub>-- L1 slide 23</sub>

</span>

<span id="def-product-owner">

The **product owner** is the Scrum role accountable for the product backlog — the product vision and the ordering of its priorities — e.g., reprioritizing the backlog after a sprint demo revealed new needs.

<sub>-- L1 slide 24; Quiz 1 Q6</sub>

</span>

<span id="def-deployment">

**Deployment** is the process between the acquisition of software and its execution — the activities that make the software available for use after development. Deployment decisions affect quality attributes such as availability, performance, security, usability, interoperability, reusability, scalability, portability, and maintainability.

<sub>-- L1 slide 26, after Humble & Farley, Continuous Delivery</sub>

</span>

<span id="def-bare-metal">

**Bare metal** deployment runs applications directly on the hardware, on top of only a host OS: complete control and physical isolation are the upside; potentially wasted hardware resources, cost, scalability issues, and reduced developer productivity are the price.

<sub>-- L1 slide 31</sub>

</span>

<span id="def-virtual-machine">

A **virtual machine (VM)** is a full software computer — its own guest OS — running on a hypervisor above the host OS and hardware. VMs improve resource utilization (reduced cost, flexibility, scalability), but a full OS still runs inside each VM, VMs are susceptible to side-channel attacks, and the "noisy neighbour" problem appears when workloads share hardware.

<sub>-- L1 slide 32</sub>

</span>

<span id="def-serverless">

**Serverless** is a cloud-native development model in which there are still servers — developers and enterprises just don't manage them: developers package the code in containers, the platform deploys the application in those containers and scales it automatically with demand, and economics are metered on demand (no cost when idle), e.g., AWS Lambda.

<sub>-- L1 slide 37</sub>

</span>

<span id="def-serverless-function">

A **serverless function** works on Function-As-A-Service (FAAS) with an event-driven execution model: the provider manages the physical servers and dynamically allocates resources, the function runs when needed, and it is stateless and ephemeral with short execution times — e.g., batch processing of images and video, scheduled data compression.

<sub>-- L1 slide 38</sub>

</span>

<span id="def-deployment-pipeline">

A **deployment pipeline** is an automated implementation of the application's build, deploy, test, and release process; a CI/CD pipeline is the automated workflow that enables teams to build, test, and deploy code efficiently and reliably.

<sub>-- L1 slides 39–40</sub>

</span>

<span id="def-continuous-delivery">

**Continuous delivery** ensures that every good build is potentially ready for production release — software can be released into production at any given time.

<sub>-- L1 slides 41–42</sub>

</span>

<span id="def-continuous-deployment">

**Continuous deployment** automates the release of a good build into the production environment — code changes are released automatically into production.

<sub>-- L1 slides 41–42</sub>

</span>

<span id="def-in-place-deployment">

**In-place deployment** stops each running module/compute, installs the latest version, then starts and validates it: minimal disturbance to the infrastructure and reduced infrastructure cost, but availability suffers while the unit is down (e.g., AWS Beanstalk's one-at-a-time, half-at-a-time, all-at-once mechanisms).

<sub>-- L1 slide 43</sub>

</span>

<span id="def-rolling-deployment">

**Rolling deployment** replaces the previous version by completely replacing the infrastructure it runs on — e.g., containers running the old version replaced one-by-one by containers running the new version. There is no isolation between old and new versions, which complicates rollback.

<sub>-- L1 slide 43</sub>

</span>

<span id="def-canary-deployment">

**Canary deployment** reduces the risk of deployment by incrementally deploying the new version, starting with a small subset of users (a.k.a. incremental rollout) — a variant of blue-green deployment that can double as A/B testing.

<sub>-- L1 slide 45</sub>

</span>

<span id="def-site-reliability-engineer">

A **site reliability engineer (SRE)** improves customer experience by creating software that improves the reliability of systems in production — fixing issues, responding to incidents, and taking on-call responsibilities, rather than only building new features.

<sub>-- L1 slide 48</sub>

</span>
