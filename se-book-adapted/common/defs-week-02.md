{# Definitions for week-02. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-02.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable.
   Note: the deployment/DevOps terms below are first taught in the Week 1 deck
   (L1 slides 33–46), so the Week 1 chapter renders these boxes at first use. #}

<span id="def-ci-cd">

**CI/CD** is the pairing of two delivery practices: **continuous integration (CI)** — developers integrate code into a shared repository several times a day, each check-in verified by an automated build so problems are detected early — and **continuous delivery/deployment (CD)** — every good build is kept potentially ready for production release (delivery), or released automatically into production (deployment).

<sub>-- L1 slides 41–42</sub>

</span>

<span id="def-devops">

**DevOps** is a set of software development practices that combines software development (Dev) and operations (Ops), intending to reduce the time between committing a change and that change running in normal production, while ensuring high quality.

<sub>-- L1 slide 46, after Ebert et al., IEEE Software 2016</sub>

</span>

<span id="def-containerization">

**Containerization** is packaging an application together with only the OS processes and dependencies it needs, so it runs identically on any host that runs a container engine — lighter than a virtual machine, which carries a full guest OS.

<sub>-- L1 slides 32–33</sub>

</span>

<span id="def-blue-green-deployment">

**Blue-green deployment** is a release strategy that shifts traffic between two identical environments running different versions of the application, achieving near-zero downtime and easy rollback.

<sub>-- L1 slide 44</sub>

</span>

<span id="def-vibe-coding">

**Vibe coding** is building software primarily by prompting AI — compressing the distance from idea to prototype, requirement to interface, and prompt to implementation — while accepting weaker architecture, quality, and a larger verification burden.

<sub>-- L2 slide 11</sub>

</span>
