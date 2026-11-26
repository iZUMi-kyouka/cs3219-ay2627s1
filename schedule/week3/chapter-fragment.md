{% from "schedule/macros-fragment.md" import term, example with context %}
<h2 id="title">Week 3 — Requirements</h2>

<span id="prereqs">

This chapter builds on [Week 1]({{baseUrl}}/se-book-adapted/chapters/week-01-software-development-processes.html#W1-c3)'s software process and product backlog (W1.3): requirements are what fills that backlog. No other background is needed.

</span>

<span id="outcomes">

* Can explain what a requirement is and walk a requirement through elicitation, analysis, specification, and validation
* Can distinguish functional from non-functional requirements and write requirements in usage-centric and product-centric form
* Can build a two-level product backlog with priorities, sprints, and traceable identifiers for a concrete product
* Can classify quality attributes as external or internal and specify security, performance, scalability, deployability, and usability requirements
* Can analyze quality-attribute trade-offs and choose what to prioritize under constraints

</span>

<div id="body">

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

<box type="info" seamless>

**The running example — FoC, a campus errand and pickup platform.** Students (requesters) post errands — e.g., collecting an order from a campus vendor — and couriers accept and deliver them for credits held in a wallet. Vendors (suppliers) and their handover points are administered by the platform; users register with university email and password. This is the project-style platform used in the course's example decks and Tutorial 2: its requirements are organized by {{ term("microservice", "an independently deployable service modelled around a business domain") }} — a **user service** (accounts, trust), a **supplier service** (vendors and pickup points), a **credit service** (the wallet), and an **order service** (errand lifecycle, courier matching) (Source: L4-AlternativeExamplesForProductBacklog deck, all slides; Tutorial 2 appendix). When a requirement below is quoted from that deck, it names the service.
</box>

## Core concepts

<span id="W3-c1"></span>

### W3.1 Requirements and their development ★

**Everything the team builds traces back to requirements — get them wrong and the best architecture delivers the wrong product.** A requirement is defined broadly enough to cover users' needs, system obligations, and the documents that record them.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-requirement" trim />
</box>

**Requirements development has four phases, and they loop.** {{ term("elicitation", "discovering requirements, e.g., by interview, workshop, document analysis, or prototyping") }} discovers requirements; {{ term("analysis", "analyzing, decomposing, deriving, and negotiating requirements, and identifying gaps") }} clarifies and closes gaps; {{ term("specification", "writing and illustrating requirements for comprehension, review, and use") }} rewrites them so others can review and use them; {{ term("validation", "confirming the correct set of requirements that will enable developers to build a solution") }} re-evaluates and confirms and corrects — feeding back to elicitation (Source: L3 slide 4).

<mermaid>
flowchart LR
    E["Elicitation<br/>discover"] --> A["Analysis<br/>clarify, close gaps"]
    A --> S["Specification<br/>rewrite"]
    S --> V["Validation<br/>re-evaluate, confirm & correct"]
    V -. "gaps & corrections" .-> E
</mermaid>

%%Notation: each box is one phase of requirements development; solid arrows show the forward path of a requirement; the dashed arrow is the rework loop — validation sends you back with what it found.%%

How to read it for the running example: FoC's "a student profile will be disabled after 3 failed password or OTP attempts" did not appear fully formed — someone elicited the account-safety concern from the platform's rules, analyzed it into a testable rule, wrote it into the user-service backlog, and validated that 3 (not 5) attempts matches the intended balance of safety and usability (Source: L4-AlternativeExamplesForProductBacklog, user service N2.2.1; L3 slide 4).

**Requirements come from many kinds of sources, not just stakeholders' first sentences.** The deck lists documents (descriptions of current or competing products, standards or regulations, help-desk problem reports), interviews (focus groups, use-case workshops, product champions), questionnaires and marketing surveys (run a pilot first — difficult to ask clear questions), event-response tables (identify external stimuli and describe system responses), observation (watch users do their jobs; workflow diagrams, "day in the life" studies), and prototyping (useful for requirements, design, and implementation) (Source: L3 slide 5).

{% call example("FoC — the same requirement surfacing from three sources") %}
For FoC, the wallet-refund rule ("if the requester removes the errand, the courier leaves it, or the pickup time is missed, the charged credits should be returned") could surface from all three source kinds: help-desk problem reports after a courier no-show leaves credits stuck, an interview with the campus office that owns the credit economy, and an event-response table listing the stimulus "courier marks delivered" against the response "held credits transfer to the courier" (Source: requirement quoted from L4-AlternativeExamplesForProductBacklog, credit service 5.5; source types from L3 slide 5).
{% endcall %}

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** A teammate says "requirements are just what the customer asks for on day one". Which part of the requirements-development loop does this ignore, and what does that loop contribute?
<panel type="seamless" minimized header="%%Answer%%">

It ignores analysis (decompose, derive, negotiate; identify gaps), specification (rewrite for comprehension, review, and use), and validation (confirm the correct set that enables developers to build a solution) — the loop is what turns raw stakeholder wishes into a buildable, reviewed set (Source: L3 slide 4).

</panel>

**Q2.** You must find out how campus vendors actually hand over orders today. Which two elicitation sources fit best, and why?
<panel type="seamless" minimized header="%%Answer%%">

Observation (watch users do their jobs; "day in the life" studies, workflow diagrams) and interviews (e.g., a product champion per vendor) — the knowledge is tacit and practiced, so watching and asking beats questionnaires (Source: L3 slide 5).

</panel>

</panel>

<span id="W3-c2"></span>

### W3.2 Functional vs non-functional requirements ★

**The FR/NFR split answers two different questions: what must the system do, and how well must it do it.** Mixing them up is how teams ship complete-but-unusable systems.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-functional-requirement" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-non-functional-requirement" trim />
</box>

**FRs specify behavior; NFRs constrain how the system works and is built.** An FR "specifies something the system should do — typically, specify a behavior or function". An NFR "describes something not directly related to the functionality of the system — may describe how well the system works — can include other attributes too (see quality attributes later)": reliability, efficiency, usability (Source: L3 slide 9).

**The same capability can generate both an FR and NFRs.** FoC's errand flow shows this: F7.1 ("a student should only be matched to one outstanding errand, and any race condition in reassignment should be shown and rejected") is functional; its sibling NFR ("publishing an errand, replacing a courier, recording pickup, holding or releasing credits, completing delivery and sending notifications shall never become inconsistent when services restart, messages arrive late or operations are retried") constrains how well that behavior must hold (Source: L4-AlternativeExamplesForProductBacklog, order service F7.1 and NFR).

<box type="info" seamless>

**Telling apart — FR vs NFR.** One distinguishing question: **does the sentence state something the system *does*, or a bound on *how well / under what constraints* it does it?** The se-book's pair: "The system should allow a user to search for a book by its title" (what it does → FR) vs "The search should return results within two seconds" (how well → NFR).

Two traps the definitions don't warn you about:

| Trap | Example from the course | Why it bites |
|---|---|---|
| **Topic ≠ type.** A security-flavored sentence can still be an FR | "FoC should only store hashed email address in the database" (L3 slide 8) — an **F**-numbered backlog row | It specifies a *behavior* of the user service; the security *concern* doesn't make it an NFR |
| **The same subject changes type with the verb.** | "The system validates passwords" (FR — a behavior) vs "Password checks must complete in under 100 ms" (NFR — a bound on that behavior) | What gets constrained decides the class, not the subject matter |

Test each sentence against the se-book wording: FR = "what the system should do"; NFR = "the constraints under which the system is developed and operated" — and remember the W3.2 rule that only measurable NFRs can be verified.

</box>

{% call example("L3 slide 9 — one airline, one FR, one NFR") %}
FR: "The passenger shall be able to print boarding passes for all flight segments for which she has checked in" — a behavior the system must offer. NFR: "Mean time between failure >= 9000 hrs" — a constraint on how reliably the system runs, with no single feature attached (Source: L3 slide 9).
{% endcall %}

**Write NFRs in measurable terms where possible.** A testable NFR lets the requirement be verified or tested objectively — Quiz 1 makes exactly this point: NFRs are stated in measurable terms "to allow the requirement to be verified or tested objectively" (Quiz 1 Q5, model answer). FoC's NFRs do this: "Support an initial capacity of up to 30000 registered users", "Response time for all page loads should take no more than 2 seconds", "A student profile will be disabled after 3 failed password or OTP attempts" (Source: Tutorial 2 appendix N1.1, N2.1.1; L4-AlternativeExamplesForProductBacklog N2.2.1).

<box type="warning" seamless>

**Pitfall / trade-off:** NFRs are easier to miss because stakeholders think of features first — and a web application that is too slow or insecure fails even with all the right functionality. Mine for NFRs deliberately: Tutorial 2 Task 2.2 has you probe for "hidden information such as pain points, constraints, and exceptions that will lead to NFRs".
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Classify each FoC requirement as FR or NFR: (a) "The system loads bonus credits into every account after university email verification"; (b) "Only useful information should be collected and old activity data should be removed when no longer required"; (c) "An errand should be frozen for 10 minutes when a courier opens the replacement screen".
<panel type="seamless" minimized header="%%Answer%%">

(a) FR — a behavior the credit service performs. (b) NFR — privacy/data constraint (user service N2.1.2), not a feature. (c) FR — defined behavior of the order service's replacement flow (Source: L4-AlternativeExamplesForProductBacklog, credit service 5.1; user service N2.1.2; order service F7.2).

</panel>

**Q2.** (From Quiz 1 Q9.) Which of these are written in a usage-centric manner: (I) "As a user, I can upload images to the portal for others to view"; (II) "The portal will only support JPEG images of max 5MB"; (III) "A unique public link will be given to users to share their uploaded images"; (IV) "The portal shall store all images in a secure cloud service"; (V) "As a user, I can edit or delete my uploaded images at any time"?
<panel type="seamless" minimized header="%%Answer%%">

I, III, and V — they state the capability from the user's point of view. II and IV are product-centric system statements (Quiz 1 Q9, model answer; see W3.3 for the two styles).

</panel>

</panel>

<span id="W3-c3"></span>

### W3.3 Specifying requirements: usage-centric vs product-centric, and the product backlog ★★

**There are two legitimate ways to state the same capability — and the product backlog is where both live, organized for planning.** Choose the view per requirement deliberately.

**Usage-centric requirements state the capability from the user's point of view.** "As a user, I can upload an image into the system so that I can showcase my photography skills to the world"; "As a user, I can upload a 20 mb image file into the system so that I can retain the original image without loss of quality" (Source: L3 slide 6).

**Product-centric requirements state what the system will do.** "The system will support a range of graphic file formats up to 20 mb in size", refined to "The system will support the following file formats: jpeg, png, tiff, bmp" and "The system will support a maximum resolution of 5184 × 3888 pixels" (Source: L3 slide 6).

**Refinement goes at least two levels, from capability to testable rule.** FoC's user management does this in public: F1 "FoC should allow user to register using email/password" refines to F1.1 "FoC should validate email and password", which refines to "Password should be validated based on rules such as it should contain upper and lower case letters and numbers, minimum length, avoid dictionary attack etc.," — and F2 "FoC should store user information securely" refines to "Password should be salted hashed using SHA256 or equivalent algorithm" and "FoC should only store hashed email address in the database" (Source: L3 slide 8).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-product-backlog" trim />
</box>

**Why a backlog?** It allows work allocation, developing test specifications, and design development — and unlike a traditional software requirements specification (SRS — W3.7 documents it among the textual requirement documents), which "only records what is to be done in the project", the product backlog "tells a team what needs to be done and can be used as a planning tool for sequencing the work" (Source: L3 slides 7, 29).

**Every backlog row carries traceability fields.** In FoC: type (FR/NFR), identifier (F1, F1.1, F1.1.1, F2 … N1, N1.1 …), description (the documented requirement), priority (H/M/L or 1/2/3), and sprint ID (the planned sprint/iteration); requirements should also be traced to use-case, design-document, code-module, and test-case references (Source: L3 slide 26).

{% call example("Tutorial 2 appendix — the errand platform's backlog rows, quoted") %}
The tutorial's appendix shows the granularity expected for the project (FoC): "F1: Support user account creation" (High, sprint 1) → "F1.1: New users can create an account using their username, email and password" → "F1.1.1: The system should ensure that the account being created has a unique username and email to prevent duplicates"; "F2: Support viewing suppliers" → "F2.1: The system should display the suppliers with name and category visible when the user is logged in" (High, sprint 1) → "F2.1.1: The system should display the supplier details, such as descriptions, opening hours, etc., when the user selects a supplier" (Medium, sprint 1); "F3: Support managing orders" → "F3.1: FoC should allow creating an errand request" (High, sprint 2) → "F3.1.1: FoC should check if there are sufficient credits in the user's wallet to create an errand" (Medium, sprint 2); "F4: Support a closed credit economy on the platform" → "F4.1: The system should assign users with X number of credits when they first sign up" (High, sprint 3). NFRs follow the same pattern: "N1: Performance - Capacity" → "N1.1: Support an initial capacity of up to 30000 registered users" → "N1.1.1: Support data capacity increase up to 10x the initial planned user base" (Medium, sprint 1); "N2: Performance - Responsiveness" → "N2.1: FoC should have a responsive UI" → "N2.1.1: Response time for all page loads should take no more than 2 seconds" (Medium, sprint 1). The appendix also notes that "F2.1: Users can view supplier name and category when logged in" (usage-centric) and "F2.1: The system should display the supplier name and category when logged in" (product-centric) name the same capability — the product-centric wording defines the desired behavior better (Source: Tutorial 2 appendix).
{% endcall %}

<box type="warning" seamless>

**Pitfall / trade-off:** Usage-centric wording is easy to write and easy to get wrong — "users can access supplier details" does not say what the system must show. Tutorial 2's appendix marks the product-centric restatement as the better specification of desired behaviour; use usage-centric statements to capture the need, then refine them into product-centric, testable rows (Source: Tutorial 2 appendix notes on F2.1 and F2.1.1).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Rewrite this usage-centric requirement product-centrically, two levels deep: "As a courier, I can accept an errand so that I can earn credits."
<panel type="seamless" minimized header="%%Answer%%">

Sample answer (Tutorial 2 pattern): F: "Support accepting errands by couriers" → F.x: "The system should allow a logged-in courier to accept an errand that is waiting for a courier" → F.x.y: "The system should reject the accept request with an error code if the user is not an allowed courier" — mirroring the deck's trust rule F2.1 (Source: Tutorial 2 appendix F2; L4-AlternativeExamplesForProductBacklog, user service F2.1).

</panel>

**Q2.** Why does "F2.1: Users can view supplier name and category when logged in" need refinement before it can drive a test?
<panel type="seamless" minimized header="%%Answer%%">

It does not say what the system displays, where, or under which conditions — the product-centric refinement ("the system should display the suppliers with name and category visible when the user is logged in") makes the observable result explicit, which is what makes it testable (Source: Tutorial 2 appendix note on F2.1).

</panel>

</panel>

<span id="W3-c4"></span>

### W3.4 Quality attributes: external vs internal ★

**Quality attributes are how NFRs get named, measured, and traded — and the external/internal split decides who feels them.**

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-quality-attribute" trim />
</box>

**A combination of quality attributes defines software quality, and they are usually non-functional requirements.** The deck's taxonomy includes availability, performance, efficiency, scalability, robustness, safety, security, reliability, integrity, verifiability, deployability, compatibility, installability, portability, maintainability, usability, testability, modifiability, reusability, and interoperability (Source: L3 slide 10).

**External attributes are observed when the software executes and shape the user's perception of quality.** Internal attributes are not directly observed during execution — developers and maintainers perceive them, and they encompass design aspects that may impact external attributes (Source: L3 slide 11).

<box type="info" seamless>

**Telling apart — external vs internal attribute.** One distinguishing question: **who can observe it — the user while the software runs, or the team by looking at the design and artifacts?**

| | External | Internal |
|---|---|---|
| Observable by | Users, while the software executes | Developers/maintainers, from the design and code |
| Felt as | The user's perception of quality | Nothing directly — it surfaces through the external attributes it enables |
| Course example | 2-second page loads (Tutorial 2 appendix N2.1.1); profile lockout after 3 failed attempts (L4 user-service N2.2.1) | Salted-hashed password storage; testability of the wallet service |

The connection is the point: an internal attribute is a *design property that may impact an external one* — the hashing (internal) is what the account security users feel (external) is made of. When classifying, ask who observes the sentence as written; "the team inspects the design" marks it internal even when users eventually benefit.

</box>

{% call example("FoC — one attribute, two sides") %}
Scalability has an external side users feel ("the application must support the entire campus without slowing down" — order service NFR) and an internal side developers choose (run three Docker containers per microservice behind Nginx and enable Kubernetes auto-scaling — an architecture decision made to deliver the external claim) (Source: L4-AlternativeExamplesForProductBacklog, order service NFR "Capacity").
{% endcall %}

**Different application types emphasize different attributes.** Embedded software: performance, efficiency, reliability, robustness, safety, security. Web applications: availability, integrity, interoperability, performance, scalability, security, usability. Desktop and mobile software: performance, security, usability (Source: L3 slide 13).

**Deployment choices are quality-attribute decisions.** The deck asks what attributes blue-green deployment and Docker + Kubernetes support: blue-green buys availability (near-zero downtime) and fast rollback; containerized orchestration buys scalability and deployability — matching Week 1's deployment mechanisms (Source: L3 slide 12; see W1.4–W1.5).

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Classify as external or internal: (a) 2-second page loads; (b) salted-hashed password storage; (c) profile lockout after 3 failed attempts; (d) testability of the wallet service.
<panel type="seamless" minimized header="%%Answer%%">

External: (a) users feel response time; (c) users experience the lockout. Internal: (b) perceived by developers/maintainers (a design property that impacts the external security users feel); (d) perceived by the team, impacts how safely external behavior can be changed (Source: L3 slide 11; requirements from L4-AlternativeExamplesForProductBacklog N2.2.1 and Tutorial 2 appendix).

</panel>

</panel>

<span id="W3-c5"></span>

### W3.5 Key quality attributes in depth ★★

**Five attributes do most of the work in this course — security, performance, scalability, deployability, usability — and each has named concerns, measures, and design consequences.**

**Security is the system's ability to resist unauthorized use while still serving legitimate users.** Core concerns: confidentiality (protect data against unauthorized disclosure/access) and integrity (protect data against unauthorized modification); it relies on authentication, authorization, and auditing — who is the user, what are they allowed to do, and record actions so misuse can be detected or investigated (Source: L3 slide 14).

{% call example("FoC — security requirements at three layers") %}
The user service's NFRs secure accounts: "A student profile will be disabled after 3 failed password or OTP attempts" (authentication), with re-enable "by clicking a verification link sent to the university email" (recovery); "Confidential account information in storage must be strongly protected" (confidentiality); "Only useful information should be collected and old activity data should be removed when no longer required" (privacy). The user service's FRs add authorization: "Before a user edits a pickup place, withdraws an errand or marks delivery confirmed, the backend should verify that the user is allowed and return an error code otherwise", and the edge proxy — the entry-point service that fronts the platform's other services, from the FoC architecture in the example decks — "shall decode the JWT and answer with an error code when the credential is absent, expired or wrong" (a JWT — JSON Web Token — is a signed token that proves who the caller is; the proxy checks it before any request passes inward %%— dimmed: RFC 7519%%). The supplier service adds auditing-minded rules: "No confidential details should appear when a supplier request fails" and "Extra protection must be added to staff-only supplier URLs" (Source: L4-AlternativeExamplesForProductBacklog, user service F2, N2; supplier service NFR3).
{% endcall %}

**Performance is primarily responsiveness, and its requirements reach into architecture and hardware.** Low performance means unhappy users; in real-time systems it can impact safety (an overloaded system may miss critical alerts). Stringent query response times may demand replicated databases; latency requirements may lead to deploying caches; and performance requirements affect the choice between monolithic and microservice architectures, plus hardware and network choices (Source: L3 slides 15–17).

**Caching is the deck's worked performance technique.** Caching stores frequently accessed data closer to the user — high-speed, typically transient storage holding a subset of data (e.g., Amazon ElastiCache, Redis) (Source: L3 slide 18).

<mermaid>
flowchart LR
    U["Users"] --> APP["Application"] --> CACHE["Cache<br/>(frequently accessed subset)"]
    CACHE --> DB[("Data store")]
    APP -. "cache miss" .-> DB
</mermaid>

%%Notation: boxes are components; the cylinder is a data store (the notation used across this book); solid arrows are the request path; the dashed arrow is the fallback path on a cache miss.%%

How to read it for the running example: FoC's credit service keeps replay tags in Redis — markers that let the service recognize a wallet message it has already processed (W3.7's template example walks the full mechanism) — with the deck's rule "Redis shall save every tag after the balance update has finished", so the wallet check reads Redis (fast, hot) before touching the database, exactly the cache-in-front-of-store shape above (Source: L4-AlternativeExamplesForProductBacklog, credit service NFR6.1.2; L3 slide 18).

**Scalability is the ability to accommodate growth in usage — and it has both hardware and software consequences.** Growth can be more users, more deployment locations, more transactions. Hardware scaling adds disk capacity; software scaling may mean architecting for parallel and distributed computing. You cannot always future-proof, but an estimate of growth helps (Source: L3 slide 19).

**Two scaling directions trade resilience against simplicity.** Vertical scaling adds capability to existing machines (upgrade and swap to a better configuration): easier to maintain, but a single point of failure. Horizontal scaling adds machines (nodes): more resilience and fault tolerance, but more cost and complexity — e.g., Kubernetes horizontal pod autoscaling. Microservices designed small, focused, and independently deployable suit horizontal scaling (Source: L3 slide 20). FoC's capacity NFR makes the horizontal choice explicitly: "run three Docker containers for each microservice behind Nginx and enable Kubernetes auto-scaling" — three equivalent nodes behind a front proxy, consistent with the Kubernetes HPA example on the slide (Source: L4-AlternativeExamplesForProductBacklog, order service NFR). Week 12 redraws this same contrast on the room-booking platform and adds what scale-out needs to actually work — a load balancer and a session store (see [W12.4]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c4)).

<box type="info" seamless>

**Telling apart — requirement vs design decision.** One distinguishing question: **does the sentence pin down a *need the product must fulfill*, or a *choice about how to fulfill it*?**

| | Requirement | Design decision |
|---|---|---|
| States | A capability or bound the product must meet | A concrete way the system will be built to meet it |
| Passes the test | Survives a change of solution ("we could do this differently and still satisfy it") | Tied to a specific technology, component, or structure |
| FoC example | "The application must support the entire campus without slowing down" (order-service capacity NFR) | "Run three Docker containers for each microservice behind Nginx and enable Kubernetes auto-scaling" |

The FoC capacity pair shows how they travel together: the requirement is the *bound* (campus-scale load without slowdown); the container/proxy/auto-scaling split is the design *decision made to deliver it* — the chapter itself calls it "an architecture decision made to deliver the external claim" (W3.4) and "the stated design consequence" (self-check). Course requirement documents do record such decisions (the L3 service template even asks "what data does the service deal with", which invites them); the skill being tested is knowing which part is the *constraint* — so when a quiz asks you to *satisfy* a requirement, answer with the need it states, not the mechanism quoted alongside it.

</box>

**Deployability is the ease and speed of getting software to production.** Software may be allocated to an environment for execution within a predictable, acceptable amount of time and effort; measures include deployment frequency, change failure rate, and MTTR (mean time to repair); the processes and strategies that impact it are CI/CD, containerization, DevOps, and architectural decisions such as serverless and microservices (Source: L3 slide 21 — all of which Week 1 covered as mechanisms).

**Usability measures the effort to prepare input, operate, and decipher output.** Measures include average time to specify inputs, number of interactions to get information, time to complete a task, user errors or trials needed, and waiting time; ease of learning (meaningful messages, verbose prompts, tooltips) and ease of use (customizations, autocompletion, autocorrection, scriptable) (Source: L3 slide 22).

{% call example("FoC — usability vs security, in one rule") %}
"A student profile will be disabled after 3 failed password or OTP attempts" is a security rule with a usability cost: a student who fat-fingers their password three times loses access until they click a verification link in their university email. The rule's balance (3 attempts; self-service recovery) is a usability decision as much as a security one (Source: L4-AlternativeExamplesForProductBacklog, user service N2.2.1–N2.2.2; L3 slides 14, 22).
{% endcall %}

<box type="warning" seamless>

**Pitfall / trade-off:** Attributes conflict by nature, not by bad luck — the next unit makes the conflicts explicit. When you write an NFR, ask what other attribute it silently taxes (Source: L3 slide 23).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** For each FoC requirement, name the attribute and one measure you would use: (a) "Response time for all page loads should take no more than 2 seconds"; (b) "The web browser shall generate the replay tag and place it in the Kafka message header" (Kafka — a distributed message streaming platform the course introduces properly in Week 10; here just read it as "the channel the wallet update travels on"); (c) "The application must support the entire campus without slowing down".
<panel type="seamless" minimized header="%%Answer%%">

(a) Performance — measure response time per page load against the 2-second bound. (b) Security/integrity — exactly-once wallet events: each wallet update takes effect once and only once, even if the same message arrives twice; measure duplicated wallet messages processed as errors (the replay-tag mechanism). (c) Scalability — measure users/transactions supported without SLA breach; note the stated design consequence (3 containers per microservice, Kubernetes auto-scaling) (Source: Tutorial 2 appendix N2.1.1; L4-AlternativeExamplesForProductBacklog credit service NFR6.1.1 and order service NFR).

</panel>

**Q2.** Why can deployability be measured by deployment frequency, change failure rate, and MTTR — but not by "the system is easy to deploy"?
<panel type="seamless" minimized header="%%Answer%%">

Those three are observable quantities; "easy to deploy" is not. Measurable statements can be verified or tested objectively — the same principle Quiz 1 Q5 tests for NFRs (Source: L3 slide 21; Quiz 1 Q5).

</panel>

</panel>

<span id="W3-c6"></span>

### W3.6 Requirement trade-offs ★★

**Improving one quality attribute often degrades another — so attribute selection is a prioritization problem, not a wish list.**

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-requirement-tradeoff" trim />
</box>

**Every quality attribute you improve is bought by paying somewhere else — architecture is the act of choosing where to pay.** The diagram shows the shape of that bargain: one design decision moves two quality attributes in opposite directions.

<mermaid>
flowchart TB
    subgraph SEESAW["One design decision, two quality attributes"]
        direction LR
        L["Improve<br/>scalability"] --- F["fulcrum:<br/>the design decision"] --- R["Cost & complexity<br/>degrade"]
    end
</mermaid>

%%Notation: the two pans are quality attributes pushed by one design decision (the fulcrum); the lower pan is the attribute that pays. The picture is a metaphor — read it as "this decision helps the left, hurts the right".%%

How to read it: with Quiz 3's room-booking platform, extracting the search module as an independently scaled microservice lifts *scalability* (the summer load is absorbed by more search instances) but pays in *cost and complexity* — more deployables, more moving parts — which is exactly why the quiz's correct answer ties the split to demand ("increase its instances based on demand", Quiz 3 Q1). L3's tables give you the vocabulary of the pans: an embedded system cares about performance and safety, a web app about performance, scalability and security (L3 slide 13) — and the seesaw reminds you that adding security checks also adds latency, so the architect must say *which* side they are choosing to load.

**Why trade-offs exist — two different pressures the slide keeps separate.** Project constraints (resource limits, few skilled engineers, budgets and time, technical limitations) force you to *prioritize* which attributes to fund — the slide's arrow points at planning and resource allocation. Attribute conflicts are the other pressure: improving one attribute can genuinely degrade another, which is what the slide's table records. The deck works from a sample prioritization table for an airport check-in kiosk (Figure 14-1 on L3 slide 23, offline with the slide PDFs): rows are attributes, each carries a priority **Score** (Security 7, Integrity 6, Usability 5 … Verifiability 1, Robustness 1), and the cell symbols give the direction of influence — a "plus" (drawn `^` in the figure) means improving the row attribute improves the column attribute; a "minus" (drawn `<`) means improving the row attribute degrades the column one (Source: L3 slide 23).

**The conflicts are directional, and Quiz 1 tests two of them.** Improving interoperability by allowing open data exchange and API access can expose the system to more vulnerabilities, weakening security; improving reliability by introducing redundant checks, backups, and recovery routines makes the system slower and more resource-hungry, degrading efficiency (Quiz 1 Q7, model answer; Source: L3 slide 23).

{% call example("L3 slide 24 — the same four NFRs, two very different systems") %}
The healthcare examples pair two scenarios that both list performance, scalability, usability, and deployability as NFRs, yet weight them differently: an A&E (accident & emergency) bedside clinical decision support system for patient triage, versus a national health-record platform for citizens' health data — both list the same four NFRs (performance, scalability, usability, deployability), and the slide's point is that the same list serves both because the weighting differs with the context: the bedside tool lives or dies on instant response, the national platform on serving huge populations dependably. %%The full slide (L3, offline) shows the two lists verbatim.%% The lesson: the attribute list is generic; the prioritization is what makes it a requirement (Source: L3 slide 24).
{% endcall %}

**Trade-off analysis needs a common language and structure.** Use quality models and frameworks that provide a common language and structure for describing, measuring, and comparing quality attributes — e.g., pair-wise prioritization; feasibility takes priority (Source: L3 slide 23).

**For FoC, pairwise prioritization identifies the nice-to-haves.** The deck asks: "You can use pair-wise prioritization to identify the Nice-to-haves in FoC" — comparing requirements two at a time to force an order, which is exactly what sprint planning needs (Source: L3 slide 25).

<box type="warning" seamless>

**Pitfall / trade-off:** Feasibility takes priority — a required-but-infeasible attribute combination is a plan to fail. Tutorial 2 Task 1.1 has you prioritize and draft an execution plan precisely so these conflicts surface before development (Source: L3 slide 23; Tutorial 2 Task 1.1).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** (From Quiz 1 Q7.) Improving interoperability by allowing open data exchange and API access can expose the system to more vulnerabilities, weakening ___; improving ___ by introducing redundant checks, backups and recovery routines can make the system slower and consume more resources.
<panel type="seamless" minimized header="%%Answer%%">

Security; reliability (Quiz 1 Q7, model answer).

</panel>

**Q2.** FoC's lockout rule (disable after 3 failed attempts) trades which attribute against which? Name a mitigation the requirements already contain.
<panel type="seamless" minimized header="%%Answer%%">

Security (protect accounts against unauthorized access) is bought at a usability cost (legitimate students locked out). The mitigation is already in the requirements: the profile "can be enabled again by clicking a verification link sent to the university email" — self-service recovery shortens the usability penalty (Source: L4-AlternativeExamplesForProductBacklog, user service N2.2.1–N2.2.2).

</panel>

</panel>

<span id="W3-c7"></span>

### W3.7 Validating, documenting and managing requirements ★★

**Requirements are managed artifacts: they are verified for quality, recorded in documents, traced to work items, and revised as the product learns.**

**Validation and verification ask different questions.** Validation: whether you have written the *right* requirements — do they trace back to business objectives? Verification: whether you have written the requirements *right* — do they have the desirable properties: completeness, correctness, feasibility, prioritization, unambiguity? Methods: informal (peer desk-check, pass-around, walkthrough) and formal (inspection — a formal process with a checklist) (Source: L3 slide 28).

**Requirement documents come in textual and visual forms.** Textual: vision and scope document, use case document, software requirements specification (SRS), product backlog. Visual: structured analysis models (data flow diagram, entity-relationship diagram, state-transition diagram, dialog map — a state-transition diagram drawn over the user-interface dialogs, showing which screens can follow which %%— dimmed: Wiegers & Beatty, *Software Requirements*%%) and object-oriented analysis models (e.g., object-oriented domain models — conceptual models of the problem-domain's things, their properties, and relations; for FoC: students, errands, wallets, vendors. Week 8 develops this idea as domain-driven design) (Source: L3 slide 29).

**A template keeps service requirements complete.** The deck's microservice template asks three questions of every service: what can the system/service do (functionality), how well should the service perform (NFRs), and what data does the service deal with — customizable (e.g., add more NFRs) (Source: L3 slides 30–31).

{% call example("The template applied to FoC's credit service") %}
What it can do: load bonus credits after university email verification; accept reward changes while an errand waits for a courier; charge the difference when the reward increases; transfer charged credits to the courier on delivery confirmation; refund held credits when an errand is removed, abandoned, or missed. How well it performs: exactly-once wallet events — every wallet-changing message carries a replay tag, duplicates are acknowledged without updating balances. What data: wallet balances, replay tags (stored in Redis), credit ledger entries (Source: L4-AlternativeExamplesForProductBacklog, credit service 5.1–5.5, NFR6; template from L3 slide 30).
{% endcall %}

**Requirements management is a loop, not a phase.** Collect initial requirements from stakeholders; analyze; define and record; prioritize; agree on and approve; trace requirements to work items; query stakeholders after implementation on needed changes; utilize test management to verify and validate; assess the impact of changes; revise; document changes. Tools range from spreadsheets to GitHub, Jira, JAMA, RequisitePro (Source: L3 slide 32).

**AI now assists requirements engineering — with the same caveat as Week 2.** Uses: elicitation (persona specification — acting as a domain expert or user; contextual information — questions relevant to the product context), analysis (requirement refinement — identify sub-tasks/sub-features; automated templating and tagging), automated tagging and categorization by type and priority (better traceability, e.g., automated tracing of tests to requirements), natural language processing (identify ambiguity, conflicting requirements; fill missing requirements; fix inconsistencies), and predictive analytics (which requirements are likely to be implemented successfully — helping identify and prioritize). The deck's warning: don't simply trust the black box — be aware of non-deterministic outputs and non-explainable chains of thought (Source: L3 slides 33–34; Tutorial 2 Task 2.2 rehearses the elicitation use).

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Your reviewer marks FoC's "The system should display the suppliers with name and category visible when the user is logged in" as "clear". Which verification property does the refined child requirement "The system should display the supplier details, such as descriptions, opening hours, etc., when the user selects a supplier" add?
<panel type="seamless" minimized header="%%Answer%%">

Completeness (it says what details, and when) and testability — the observable result is explicit, so a test can settle whether it is met (Source: Tutorial 2 appendix F2.1.1; L3 slide 28).

</panel>

**Q2.** Tutorial 2 Task 2.2 has you elicit ClassPulse requirements from an LLM by probing with personas and "what if" scenarios. Which AI-in-RE use does this rehearse, and what is the deck's caveat?
<panel type="seamless" minimized header="%%Answer%%">

Elicitation — persona specification (the LLM acts as end user or teacher) and contextual information (questions relevant to the product context). Caveat: don't simply trust the black box — outputs are non-deterministic and the chain of thought is not explainable (Source: L3 slide 33; Tutorial 2 Task 2.2).

</panel>

</panel>

<box type="info" seamless>

**Section summary**

* **Requirements development loops through elicitation, analysis, specification, and validation** (W3.1).
* **FRs say what the system does; NFRs say how well — and NFRs must be measurable to be verifiable** (W3.2).
* **The product backlog organizes requirements into traced, prioritized, sprint-planned rows** (W3.3).
* **Quality attributes split external (user-felt) from internal (design-perceived), and five attributes carry most of the weight** (W3.4–W3.5).
* **Attributes trade off against each other; feasibility takes priority** (W3.6).
* **Requirements are validated, documented, traced, and managed — increasingly with AI assistance, never with blind trust** (W3.7).

</box>

## Connections

* Requirements development, FR/NFR, usage/product-centric ↔ L3 slides 3–9 ↔ Tutorial 1 Q1 (characterize an application) ↔ Quiz 1 Q5, Q9.
* Product backlog and refinement ↔ L3 slides 6–8, 26 ↔ L1 slide 24 (PeerPrep, W1.3) ↔ Tutorial 2 Task 1.1 (the errand platform's own backlog) ↔ Scrum's sprint planning (W1.3).
* Quality attributes ↔ L3 slides 10–22 ↔ W1.4–W1.5 (deployment mechanisms and strategies as attribute decisions) ↔ W12 (scalability deep dive).
* Trade-offs ↔ L3 slides 23–25 ↔ Quiz 1 Q7 ↔ the prioritization step of Tutorial 2 Task 1.1.
* Validation, documentation, management, AI in RE ↔ L3 slides 28–34 ↔ W2.2 (AI across the SDLC) ↔ Tutorial 2 Task 2.2 (LLM-assisted elicitation for ClassPulse).

## Further reading

All cited on the slides: the IEEE Standard Glossary definition of requirements; Wiegers & Beatty, *Software Requirements* (source of the validation/verification and quality-of-requirements lists); Chris Richardson's microservice requirement template (microservices.io); IBM's requirements-management overview; Ronanki et al. and Arora et al. on generative AI in requirements engineering.

## Summary

**Key takeaways**

* **Requirements are conditions or capabilities — developed in a loop, not gathered once.** (→ outcome 1)
* **FRs specify behavior; NFRs specify how well, and only measurable NFRs can be verified.** (→ outcome 2)
* **A product backlog turns requirements into a traced, prioritized, sprint-planned plan.** (→ outcome 3)
* **Quality attributes are named, measurable properties — external ones are user-felt, internal ones are design-perceived.** (→ outcome 4)
* **Security, performance, scalability, deployability, and usability each carry named concerns, measures, and design consequences.** (→ outcome 4)
* **Attributes trade off; prioritization under constraints is the engineering act.** (→ outcome 5)
* **Requirements are validated, documented, traced, and managed — increasingly with AI assistance, never with blind trust.** (→ outcome 1)

**Key terms**

| Term | One-line definition | Unit |
|---|---|---|
| Requirement | A condition or capability needed by a user or that must be met by a system — or its documented representation | [W3.1](#W3-c1) |
| Functional requirement | Specifies something the system should do | [W3.2](#W3-c2) |
| Non-functional requirement | A constraint on how well the system works, not directly tied to functionality | [W3.2](#W3-c2) |
| Product backlog | The ordered list of requirements with type, id, description, priority, and planned sprint | [W3.3](#W3-c3) |
| Quality attribute | A property (performance, security, usability…) whose combination defines software quality | [W3.4](#W3-c4) |
| Requirement trade-off | Improving one quality attribute degrades another | [W3.6](#W3-c6) |

%%Next: Week 4 moves up a level of abstraction — architecture: once you know *what* to build and *how well*, architecture decides the system's overall structure that delivers it.%%

</div>
