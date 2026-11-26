{% from "schedule/macros-fragment.md" import term, example with context %}
<h2 id="title">Week 4 — Architecture (I) & Product Backlog</h2>

<span id="prereqs">

This chapter builds on [Week 3]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c1) — requirements and quality attributes are the *inputs* architecture must satisfy — and on Week 1's deployment mechanisms (W1.4), the deployment targets that architectural deployment decisions allocate the system to.

</span>

<span id="outcomes">

* Can explain what software architecture is, and what makes components, connectors, and configuration its building blocks
* Can distinguish control flow from data flow, and call-and-return from message- and event-based interaction
* Can decompose a system into modules by horizontal (technical-layer) or vertical (business-domain) slicing
* Can assess a decomposition with coupling and cohesion vocabulary
* Can place an architectural style on the technical/domain × monolithic/distributed categorization, including the modular monolith

</span>

<div id="body">

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

**Architecture is where requirements stop being statements and start being structure.** The Week 4 deck ("High Level Design: Software Architecture") gives the definition and vocabulary, the two ways an arrow can mean something ({{ term("control flow", "the flow that reasons about computation order — how the focus of control moves through the execution") }} vs {{ term("data flow", "the flow that reasons about data availability, transformation, and latency — how data moves through computations") }}), the two ways components interact ({{ term("call-and-return", "interaction where control moves from one component to another and back — hierarchical or not") }} vs {{ term("messages", "data sent to a specific address; the recipient awaits messages and reacts to them") }} and {{ term("events", "data emitted when a component's state changes, for anyone listening — immutable and ordered") }}), and the two big decomposition questions (how is the code divided? how is it deployed?). The same lecture's second deck (L4-AlternativeExamplesForProductBacklog) supplies the fully-worked requirements that this chapter keeps using as the running example — FoC, the campus errand and pickup platform (see [Week 3]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#W3-c3)'s running example).

%%Deep dives into the layered style, MVC, and SPA are Week 6; event-driven architecture is Week 9; microservices are Weeks 7–8. This chapter covers exactly what the Week 4 deck covers.%%

## Core concepts

<span id="W4-c1"></span>

### W4.1 What is software architecture? ★

**Architecture is the set of decisions about a system's overall organization — made early, expensive to reverse, and visible to everyone who builds on it.**

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-software-architecture" trim />
</box>

**The definition has exactly three parts — here are all three at once.** Each component is drawn with what it *shows* the rest of the system (its externally visible properties) and nothing of what it hides; the arrows are the relationships (Source: definition per L4 slides 6–7; diagram created for this site — no diagram exists on the slides).

<mermaid>
flowchart LR
    subgraph ORD["Component: Order"]
        direction TB
        O["Order component"] -.- OS["provided: place order<br/>required: pay, reserve<br/>quality: auditable"]
    end
    subgraph PAY["Component: Payment"]
        direction TB
        P["Payment component"] -.- PS["provided: charge card<br/>required: bank gateway<br/>quality: secure"]
    end
    subgraph NOT["Component: Notification"]
        direction TB
        N["Notification component"] -.- NS["provided: send message<br/>required: template store<br/>quality: available"]
    end
    ORD -->|"③ relationship:<br/>call & return"| PAY
    ORD -.->|"③ relationship:<br/>message"| NOT
</mermaid>

%%Notation: each framed group is a component (① in the definition); the dashed sidecar beside it is that component's *externally visible properties* (②) — provided services, required services, quality guarantees; the labelled arrows are the relationships (③), solid for synchronous call & return, dashed for asynchronous message. The inner workings of each component are deliberately not drawn.%%

How to read it: in the errand platform, the Order component *shows* "place order" and "requires payment" to the rest of the system while hiding its errand-state code; Payment *shows* a secure charge service; and the Order→Payment relationship is call & return while Order→Notification is a fire-and-forget message — sent and forgotten, with no reply awaited (Week 9 defines the term). The three visible properties of Notification are all its consumers may depend on — which is exactly what lets its implementation change freely (W4.2 reads the same ideas on the platform's real component diagram).

**"Externally visible properties" is the load-bearing phrase.** The deck's shorthand: externally visible properties ≡ functionalities + NFR — exactly the artifacts Weeks 3 produces. Private details of a component's internals are not architectural (Source: L4 slide 4).

**Architecture design decisions are questions, and each maps to a later topic of this course.** How will structural components be decomposed into subcomponents? Is there a generic application architecture that can act as a template? What architectural patterns or styles can be used? What component organization will best deliver the NFR? What kind of deployment should the architecture support — single-core or multi-core, single- or multi-processor, stand-alone or distributed? (Source: L4 slide 7.)

**The deck gives a repeatable six-step process, refined in a loop.** (1) Identify architectural drivers — functional requirements, quality attributes, constraints; (2) choose a feature or capability; (3) propose a structure — layers, modules, components, data flow, responsibilities; (4) define boundaries and contracts — module interfaces, API endpoints, database interactions; (5) verify with requirements and refine decisions; (6) document the high-level design via an architecture diagram — then repeat as the software evolves (Source: L4 slide 8).

{% call example("FoC — naming the architectural drivers") %}
Step 1 on the errand platform: the drivers are the functional requirements (trusted users perform important actions; wallet credits move exactly once; couriers are matched one-per-errand), the quality attributes (dependability — nothing becomes inconsistent when services restart or messages arrive late; capacity — support the entire campus without slowing down), and the constraints (university email for accounts; the credit economy is closed). Steps 3–4 then propose a structure and contracts per capability — which is what Tutorial 2 rehearses (Source: L4-AlternativeExamplesForProductBacklog, order service F7, NFR; user service F2; L4-Architecture slide 8).
{% endcall %}

**Reference architectures and architectural patterns are the templates behind "numerous applications, same framework".** A reference architecture explains high-level structures of similar applications (e.g., web applications; the address-book developer guide's Logic/Storage/UI/Model organization) and leads to architectural patterns (Source: L4 slide 9).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-reference-architecture" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-architectural-pattern" trim />
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Which of these are architecture and which are detailed design? (a) FoC's wallet is a separate service with a documented API; (b) the wallet stores replay tags in a Redis hash versus a sorted set; (c) the edge proxy decodes JWTs and rejects missing or expired credentials.
<panel type="seamless" minimized header="%%Answer%%">

(a) Architecture — a component boundary with an externally visible contract. (b) Detailed design — internal to the wallet component. (c) Architecture — the edge proxy is a component whose externally visible behavior (reject with error code) other services rely on (Source: L4 slide 4; L4-AlternativeExamplesForProductBacklog user service F2.2, credit service NFR6).

</panel>

**Q2.** Why does the deck's architecture process loop back to "refine decisions" after verification?
<panel type="seamless" minimized header="%%Answer%%">

Because proposed structures are hypotheses: verification against the drivers (FRs, quality attributes, constraints) may show a boundary or contract that cannot deliver an NFR, so the structure is refined — and the loop repeats as the software evolves (Source: L4 slide 8).

</panel>

</panel>

<span id="W4-c2"></span>

### W4.2 Components, connectors, and configuration ★

**Architecture has exactly three building blocks — and one diagram convention for each.**

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-component" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-connector" trim />
</box>

**The configuration is the third building block — the arrangement the first two form.** (Source: L4 slide 6.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-configuration" trim />
</box>

The diagram below draws FoC's services with the notation this book uses everywhere: boxes are components/services, solid arrows are synchronous calls, dashed arrows are asynchronous messages or events, and cylinders are data stores.

<mermaid>
flowchart LR
    B["Browser"] -->|"sync call"| EP["Edge proxy<br/>(JWT check)"]
    EP -->|"sync call"| US["User service"]
    EP -->|"sync call"| OS["Order service"]
    OS -->|"sync call"| CS["Credit service"]
    CS -.->|"wallet events (Kafka replay tag)"| OS
    OS --- DB1[("orders data")]
    CS --- DB2[("credit ledger")]
    CS --- R[("Redis<br/>(replay tags)")]
</mermaid>

%%Notation: box = component/service; solid arrow = synchronous call; dashed arrow = asynchronous message or event; cylinder = data store.%%

How to read it for the running example: the browser calls the edge proxy, which verifies the JWT before anything else runs ("for every private screen/API call, the edge proxy shall decode the JWT and answer with an error code when the credential is absent, expired or wrong"); the order service calls the credit service synchronously to reserve credits, while wallet-change confirmations travel as Kafka messages carrying a replay tag — the dashed arrows — and each service keeps its own data store (Source: L4-AlternativeExamplesForProductBacklog, user service F2.2; credit service NFR6.1.1–6.1.2).

<box type="warning" seamless>

**Pitfall / trade-off:** A component is not a special programming construct — it is whatever unit the team agrees to treat as one part with one responsibility, and a connector arrow describes reliance, not necessarily a method call. Always say (in a legend or caption) what your arrows mean (Source: L4 slide 6; cf. the se-book's component discussion).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** In the FoC diagram above, identify one component, one connector of each kind, and one configuration fact.
<panel type="seamless" minimized header="%%Answer%%">

Component: the credit service. Synchronous connector: order service → credit service (reserve credits). Asynchronous connector: credit service → order service wallet events over Kafka. Configuration fact: the edge proxy sits in front of the services, and each service owns its own data store (Source: L4-AlternativeExamplesForProductBacklog F2.2, NFR6; L4 slide 6).

</panel>

</panel>

<span id="W4-c3"></span>

### W4.3 Control flow vs data flow ★

**The same arrow in an architecture diagram can mean two different things — and which one you mean decides what you can reason about.** The deck's setup: two components C1 and C2 joined by an arrow — "what does this arrow mean?" (Source: L4 slide 10).

**Control flow reasons about computation order.** It is how the *focus of control* moves throughout the execution; data may accompany control (Source: L4 slide 10).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-control-flow" trim />
</box>

**Data flow reasons about data availability, transformation, and latency.** It is how data moves through a collection of computations — and as data moves, control is activated (Source: L4 slide 10).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-data-flow" trim />
</box>

The deck's example is a language-processing system; the diagram below reads it both ways so you can see the difference on one picture.

<mermaid>
flowchart LR
    IN["Input"] --> SH["Circular shift"] --> AL["Alphabetizer"] --> OUT["Output"]
</mermaid>

%%Notation: each box is a processing component; read left-to-right the arrows as data flow (text becomes shifted lines, then a sorted index), and read the same arrows as control flow (the focus of control moves from input handling, to shifting, to alphabetizing, to output).%%

How to read it for the running example: "accept an errand" is control flow — the focus of control moves browser → edge proxy → order service → credit service and back. "an errand's state moves from posted to assigned to picked up to delivered" is data flow — the errand record is transformed as it passes through components, and each transformation activates the next step (Source: L4 slide 10; L4-AlternativeExamplesForProductBacklog, order service F7, credit service 5.4).

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** For each question, name the flow it belongs to: (a) "How long until the errand record reaches the courier's screen?"; (b) "Which component runs first when a courier taps accept?"
<panel type="seamless" minimized header="%%Answer%%">

(a) Data flow — data availability and latency. (b) Control flow — computation order (Source: L4 slide 10).

</panel>

</panel>

<span id="W4-c4"></span>

### W4.4 Call-and-return vs messages and events ★

**Components interact in two fundamentally different ways: one component drives, or components react.** The choice shapes reliability, coupling, and how you trace an NFR to code.

**Call and return is the style where control moves out and comes back.** Control moves from one component to another and back; it can be hierarchical (a master control calling subordinates — the deck's language-processing example) or non-hierarchical (objects calling each other's operations through a manager for a shared abstract data type (ADT) — slide 11's "Manager ADT" sketch). The deck's pointed question on this slide: *can you trace an NFR to code?* — with call-and-return, the path is explicit (Source: L4 slide 11).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-call-and-return" trim />
</box>

**Messages are data sent to a specific address.** In message-driven systems, each component has a unique address to which other components can send messages; each recipient awaits messages and reacts to them. Communication can be asynchronous or synchronous, point-to-point (Source: L4 slide 12).

**Events are data emitted for anyone listening.** An event is emitted by a component when its state changes — a record of something that has happened; events are immutable (cannot be changed or deleted), are ordered in their creation sequence, and are sent to publishing infrastructure where consumers may later retrieve them (Source: L4 slide 12).

The diagram below contrasts the three interaction shapes on one canvas — who initiates, and who must be listening.

<mermaid>
flowchart LR
    subgraph CR["Call & return"]
        A1["Caller"] -->|"call"| B1["Callee"]
        B1 -->|"return"| A1
    end
    subgraph MSG["Message"]
        A2["Sender"] -->|"to a specific address"| B2["Recipient<br/>(awaits messages)"]
    end
    subgraph EVT["Event"]
        P["Producer<br/>(state changes)"] -->|"emit, immutable, ordered"| BUS["Publishing infrastructure"]
        BUS -.->|"later retrieval"| S1["Consumer 1"]
        BUS -.-> S2["Consumer 2"]
    end
</mermaid>

%%Notation: boxes are components; solid arrows are interactions initiated now; dashed arrows are later, possibly-never consumption; in the event shape the sender does not know how many consumers exist.%%

How to read it for the course example: the Grab-like taxi-booking application in the deck maps booking operations onto events and messages — and the slide's tag names the quality attribute satisfied: **reliability** — a booking event recorded in the publishing infrastructure survives the momentary absence of any one consumer (Source: L4 slide 13). FoC's wallet uses the same logic: wallet-changing messages between the order and credit services carry a replay tag, and duplicates are "acknowledged as successful by sending the previous transfer result without updating balances" — exactly-once wallet effects over unreliable message delivery (Source: L4-AlternativeExamplesForProductBacklog, credit service NFR6).

<box type="warning" seamless>

**Pitfall / trade-off:** Call-and-return makes the NFR trace explicit but couples the caller to the callee's availability; messages and events decouple senders from receivers (and add reliability through infrastructure) but make the computation order indirect — Weeks 9–11 build out this trade-off in full.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Classify: (a) the order service asks the credit service to reserve credits and waits for the answer; (b) the credit service emits "DeliveryConfirmed" for anyone listening; (c) the browser sends a checkout request to one named endpoint.
<panel type="seamless" minimized header="%%Answer%%">

(a) Call and return (control moves out and back). (b) Event — emitted on state change, immutable, ordered, published for any consumer. (c) Message — data sent to a specific address whose recipient awaits and reacts (Source: L4 slides 11–12; L4-AlternativeExamplesForProductBacklog credit service 5.4, NFR6).

</panel>

**Q2.** Which properties of events make replay-tag-style recovery possible?
<panel type="seamless" minimized header="%%Answer%%">

Immutability (a recorded event cannot be silently altered) and ordering (creation sequence is preserved) — so duplicates and gaps are detectable, which is what a replay tag relies on (Source: L4 slide 12; L4-AlternativeExamplesForProductBacklog NFR6).

</panel>

</panel>

<span id="W4-c5"></span>

### W4.5 Decomposition, slicing, and modularity ★★

**"How do you break it up?" is the architecture question — and there are two perpendicular ways to slice the same system.**

**The deck's decomposition guidelines read like a checklist.** Divide and conquer; keep abstraction as high as possible; increase {{ term("cohesion", "the degree to which the facilities within a module belong together — higher is better") }}; reduce {{ term("coupling", "the degree to which one module depends on other modules — lower is better") }} where possible; reuse — design for reuse and reuse design; design for flexibility; and others (testability, defensive design, portability) (Source: L4 slide 14).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-modularity" trim />
</box>

**Modularity pays three ways — and all three payments come from the same source: the well-defined interface.** Parnas's classic paper (the deck lists the paper's expected benefits) promises shorter development time, product flexibility, and comprehensibility — not as three separate tricks, but as three consequences of one move: decompose into smaller chunks and specify APIs for their interactions, so that others depend only on an interface, never on the inside (Source: L4 slide 15; D. L. Parnas, *On the Criteria To Be Used in Decomposing Systems into Modules*, 1972).

<mermaid>
flowchart LR
    A["One big chunk:<br/>everything touches everything"] -->|"decompose +<br/>specify APIs"| B["Modules behind<br/>well-defined interfaces"]
    B -->|"interface = the only<br/>coordination point"| C1["① Managerial:<br/>separate groups, little communication<br/>→ shorter development time"]
    B -->|"inside can change<br/>behind the API"| C2["② Product flexibility:<br/>drastic change in one module,<br/>others untouched"]
    B -->|"read the API,<br/>skip the inside"| C3["③ Comprehensibility:<br/>study one module at a time"]
</mermaid>

%%Notation: the left node is the unmodular big-chunk design; the middle node is the decomposition — modules (hidden insides) each publishing a well-defined interface; the three right nodes are Parnas's expected benefits, each labelled with the *mechanism* that produces it.%%

How to read it: every benefit arrow names the same cause — an interface others can rely on. In the errand platform: **managerial** — Tutorial 2's milestone splits the platform into per-service modules precisely so team members can build with little cross-communication; **product flexibility** — the credit service's replay-tag choice (a Redis hash versus a sorted set) is a drastic internal change that touches no other module, because consumers see only the wallet API; **comprehensibility** — you can study the credit service one module at a time and reason about the whole wallet economy from its API alone (Sources: L4 slide 15; L4-AlternativeExamplesForProductBacklog credit service 5.2–5.4; Tutorial 2).

**Modularity is the precondition the rest of the course builds on.** Slicing decides *where* the module boundaries go (below), coupling and cohesion grade *how good* they are (W4.6), and every distributed style from W7 onward assumes you can draw them.

**Horizontal slicing cuts by technical layer: one slice = one layer, spanning every domain.** In the deck's errand-platform grid, the horizontal slice is a layer — presentation (Profile UI, Vendor list UI, Errand board UI, Wallet UI), API and controllers (/users, /vendors, /orders, /credits), business logic (auth & roles, catalog rules, lifecycle & expiry, reserve & transfer), persistence (users, vendors, orders, credit ledger tables) — the boundary follows the technology (Source: L4 slide 16).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-horizontal-slicing" trim />
</box>

**Vertical slicing cuts by business domain: one slice = one capability, top to bottom.** The same grid sliced vertically carves out everything needed for one capability — for "accept an errand": errand board UI → /orders endpoint → lifecycle & expiry logic → orders table — the boundary follows the domain, and the domain is "the problem space you are modeling and what the software is meant to address" (Source: L4 slides 16, 20).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-vertical-slicing" trim />
</box>

<mermaid>
flowchart TB
    subgraph HS["Horizontal slice — one layer, every domain"]
        direction LR
        P["Presentation:<br/>Profile UI · Vendor list UI · Errand board UI · Wallet UI"]
    end
    subgraph VS["Vertical slice — one capability, top to bottom"]
        direction TB
        V1["Errand board UI"] --> V2["/orders endpoint"] --> V3["Lifecycle & expiry logic"] --> V4["orders table"]
    end
    HS --- VS
</mermaid>

%%Notation: each box is one module of the errand platform; the top subgraph is a single layer containing every domain's presentation module; the bottom subgraph is one domain's full stack from UI to persistence; the plain line between the two subgraphs only places the two alternative slicings side by side for comparison — it is not a relationship between modules.%%

How to read it for the running example: the deck's grid has four domains (users, vendors, orders, credits) × four layers; highlighting the *presentation row* is horizontal slicing; highlighting the *orders column* top-to-bottom is vertical slicing. The same grid, two decompositions — which is why "how is the code divided?" is a style question, not a law (Source: L4 slide 16).

{% call example("L4 slide 16 — the deck's own slicing example") %}
The slide is titled "Decomposition, Componentizing & Packaging — e.g., your own project", and its grid is the errand platform: horizontal slicing is captioned "Boundary follows the technology. One slice = one layer, spanning every domain"; vertical slicing is captioned "Boundary follows the domain. One slice = one capability, top to bottom", with "Accept an errand" drawn as the vertical path (Source: L4 slide 16).
{% endcall %}

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** You want four teams to own the four domains end-to-end. Which slicing do you pick, and which guideline from the deck does that serve?
<panel type="seamless" minimized header="%%Answer%%">

Vertical slicing by business domain — each team owns one capability from UI to persistence; it serves "increase cohesion" (each module is one domain's facilities) and "reduce coupling" (domains interact through well-defined interfaces instead of shared layers) (Source: L4 slides 14, 16, 20).

</panel>

</panel>

<span id="W4-c6"></span>

### W4.6 Coupling and cohesion ★★

**Coupling and cohesion are the two dials every decomposition moves — push a module's cohesion up and its coupling to the rest typically falls; the vocabulary below is how you talk about the result.**

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-cohesion" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-coupling" trim />
</box>

**Cohesion types, best first — each step down the ladder is a weaker reason to call parts one module.** Functional (the strongest reason: the facilities perform one computation, with no side effects); layer (related services kept together, everything else kept out, in a strict hierarchy in which higher-level services can access only lower-level ones — accessing a service may result in side effects); communicational (facilities operating on the same data); sequential (procedures that work in sequence — the output of one is the input to the next); procedural (procedures merely called one after another); temporal (procedures used in the same general phase of execution, e.g., initialization or termination); utility (grouped only because no stronger form applies) (Source: L4 slide 17, quoting Lethbridge & Laganière, *Object-Oriented Software Engineering*, ch. 9).

<box type="info" seamless>

**%%'Layer' in "layer cohesion" is not the slicing layers of W4.5%% — and not the layered style of W6.2.** As a cohesion type, "layer" describes the *inside of one module*: its facilities are services arranged in a strict call hierarchy, where higher-level services access only lower-level ones. The W4.5 horizontal slice (presentation / API / business / persistence) divides the *whole system* into layers; layer cohesion grades *one module's* internals. A system organized in layers is the system-wide case of the same idea — which is why the two senses share a name (Source: L4 slide 17; Lethbridge & Laganière ch. 9).

</box>

<box type="info" seamless>

**The ladder's middle rungs all "keep procedures together" — tell the four neighbours apart by asking what connects the parts** (Source: L4 slide 17, after Lethbridge & Laganière ch. 9):

| Type | What connects the parts | Example |
|---|---|---|
| Communicational | The **same data** — facilities that operate on it, in no required order | The credit service groups load-bonus-credits, charge-the-difference, transfer, and refund — all facilities over the one credit ledger (L4-backlog deck, credit service) |
| Sequential | **Data flow** — one part's output is the next part's input | The wallet pipeline: replay-tag check → wallet operation → balance update and tag saved to Redis — each stage consumes the previous stage's output (L4-backlog deck, credit service NFR6.1–6.2.1) |
| Procedural | **Control-flow order** — parts called one after another within one procedure, each serving a different function; no data passes between them | An account-safety procedure: verify the user → disable the profile after 3 failed password or OTP attempts → email the re-enable link — three different functions, one procedure's order (L4-backlog deck, user service F2, N2.2.1–N2.2.2) |
| Temporal | **Clock time** — parts run in the same execution phase, regardless of order or data | %%external example%% A startup routine that loads the config, connects the database, and warms the cache — three unrelated tasks bundled because they all run at startup |

That ranking is also *why* the ladder orders the types as it does: each step down is a weaker reason to group — one computation (functional), then a strict service hierarchy (layer), then the same data (communicational), then data passing in sequence (sequential), then merely the same procedure (procedural), then merely the same time (temporal), then nothing left (utility).

</box>

**Coupling types, worst first.** Content (a component modifies another's internal data); common/global (all modules using one global variable are coupled to each other); control (one module passes a flag dictating what another does); data (modules share data via parameters); external (a dependency on elements outside the system — OS, shared libraries, hardware); temporal (bundled only because they happen at the same time — the between-modules counterpart of temporal cohesion above); inclusion/import (including a file or importing a package) (Source: L4 slide 18).

%%Each cohesion and coupling type above also has its own one-line entry in the [Glossary]({{baseUrl}}/se-book-adapted/glossary.html), so you can revise the ladder and the anti-patterns in one place.%%

{% call example("FoC — grading one interface with both dials") %}
The order service asks the credit service to reserve credits by passing errand and reward data through a documented API, and the credit service returns success or an error code. Cohesion: the credit service is functional — one computation (move held credits), no side effects beyond its ledger. Coupling: data coupling via parameters, not control coupling (the caller does not pass a flag dictating *how* to reserve). Contrast the anti-pattern: if the order service reached into the credit service's ledger tables directly, that would be content coupling — the worst kind (Source: L4-AlternativeExamplesForProductBacklog, credit service 5.2–5.4; L4 slides 17–18).
{% endcall %}

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Name the coupling type: (a) five services read one shared global config object; (b) a request handler passes `mode: "urgent"` so the downstream module picks a branch; (c) two cleanup jobs are grouped because they both run at midnight.
<panel type="seamless" minimized header="%%Answer%%">

(a) Common/global coupling. (b) Control coupling — passing information on what the other should do. (c) Temporal coupling — bundled only because they occur at the same time (Source: L4 slide 18).

</panel>

**Q2.** Which is the stronger cohesion, and why: a "user module" containing registration, profile pictures, and password hashing — or a "password hashing module"?
<panel type="seamless" minimized header="%%Answer%%">

The password-hashing module — functional cohesion: one computation, no side effects. The user module mixes concerns (registration, media, crypto), which the deck would classify at best communicational/procedural (Source: L4 slide 17).

</panel>

</panel>

<span id="W4-c7"></span>

### W4.7 Architectural styles: how code is divided and how it is deployed ★★

**Every architectural style answers the same two questions — how is the code divided, and how is the system deployed — and the answers form a 2×2 you should be able to fill in.**

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-architectural-style" trim />
</box>

**Dividing by technical concern groups layers of the stack; dividing by domain groups business capabilities.** Technical partitioning focuses on separation of concerns and may align with team expertise — frontend developers, backend developers, database administrators. Domain partitioning aligns logical components with the problem — customer, payment, shipping — and better aligns the system with the problem in hand (Source: L4 slide 20).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-technical-partitioning" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-domain-partitioning" trim />
</box>

**Deploying as one unit or as many is the second axis.** Monolithic: deploy all logical components as one unit; the application runs as one process. Distributed: the application consists of independent logical components running as individual processes that communicate over the network (Source: L4 slide 21).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-monolithic-deployment" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-distributed-deployment" trim />
</box>

<mermaid>
flowchart LR
    subgraph TP["Technical partitioning (layers)"]
        direction TB
        T1["Presentation"] --> T2["Services"] --> T3["Persistence"]
    end
    subgraph DP["Domain partitioning (capabilities)"]
        direction LR
        D1["Customer"] --- D2["Payment"] --- D3["Shipping"]
    end
    TP --- DP
</mermaid>

%%Notation: the left subgraph stacks technical layers (each layer is a module spanning every domain); the right subgraph places domain capabilities side by side (each capability is a module spanning every layer); the plain line between the subgraphs only sets the two alternative partitionings side by side — it is not a dependency.%%

How to read it for the running example: FoC's four services (users, suppliers, credits, orders) are domain partitioning — each is a business capability; a strict presentation/services/persistence layering shared by all four would be technical partitioning (Source: L4 slides 16, 20; L4-AlternativeExamplesForProductBacklog deck structure).

**The 2×2 categorization names the classical styles.** Monolithic × technical → {{ term("layered", "an architectural style organizing the system as layers with downward-only dependencies — deep-dived in Week 6") }}; monolithic × domain → **modular monolith**; distributed × technical → {{ term("event-driven", "a distributed style where components react to events rather than call each other — deep-dived in Week 9") }}; distributed × domain → {{ term("microservices", "a distributed style structuring one application as a suite of small independently deployable services — deep-dived in Weeks 7–8") }} (Source: L4 slide 22).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-modular-monolith" trim />
</box>

{% call example("L4 slide 22 — filling in the 2×2 for the errand platform") %}
Deploy FoC's four domain-partitioned services as separate processes talking over the network → microservices (distributed × domain). Package the same four modules into one deployable process with enforced internal boundaries → modular monolith (monolithic × domain). Organize the whole app as presentation → services → persistence in one process → layered (monolithic × technical). Route everything through events on a broker → event-driven (distributed × technical). Same requirements (Week 3), four different styles (Source: L4 slide 22; L4-AlternativeExamplesForProductBacklog deck structure).
{% endcall %}

**This chapter ends where the style deep-dives begin.** Week 6 unpacks the layered style, {{ term("MVC", "Model-View-Controller: an architectural style separating an interactive application into view, controller, and model (Week 6)") }}, and {{ term("SPAs", "single-page applications: a program downloaded into the browser that runs continuously there, fetching data without page refreshes (Week 6)") }}; Weeks 7–8 take on microservices; Week 9 covers event-driven architecture. The categorization above is the map that tells you which chapter to revisit when (Source: L4 slide 22; L6 topics slide).

<box type="warning" seamless>

**Pitfall / trade-off:** Styles are philosophies, not laws — "software is built for specific purpose". A startup's modular monolith can later split along its domain seams into microservices precisely because vertical slicing kept the boundaries meaningful (Source: L4 slides 19, 16, 22).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Fill in the 2×2: for each cell, name the style and one system from the course materials that exemplifies it.
<panel type="seamless" minimized header="%%Answer%%">

Monolithic × technical: layered (the classic web-app tier diagrams; Week 6's deep dive). Monolithic × domain: modular monolith (the errand platform packaged as one process). Distributed × technical: event-driven (message/event interaction over a broker; Week 9). Distributed × domain: microservices (FoC's four services as separate processes; Weeks 7–8) (Source: L4 slide 22).

</panel>

**Q2.** Your FoC prototype is a layered monolith and the campus load is growing. Which axis do you change first, and why?
<panel type="seamless" minimized header="%%Answer%%">

Either, deliberately: moving to a modular monolith (re-partition by domain within one deployment) preserves single-process deployability while preparing domain seams for later distribution; moving to distributed × domain (microservices) buys independent scaling at the cost of network communication complexity — the capacity NFR's "three Docker containers per microservice behind Nginx" shows the distributed choice already made (Source: L4 slides 21–22; L4-AlternativeExamplesForProductBacklog order service NFR).

</panel>

</panel>

<box type="info" seamless>

**Section summary**

* **Architecture = components, connectors, configuration — the externally visible side of each component** (W4.1–W4.2).
* **Every connector arrow means control flow or data flow, and every interaction is call-and-return or messages/events** (W4.3–W4.4).
* **Decomposition slices the system horizontally (technical layers) or vertically (business domains), and coupling/cohesion grade the result** (W4.5–W4.6).
* **Styles are the 2×2 of code division × deployment: layered, modular monolith, event-driven, microservices** (W4.7).

</box>

## Connections

* Architecture definition and building blocks ↔ L4 slides 4–9 ↔ the process Tutorial 2 rehearses (drivers → structure → contracts → verify).
* Components & connectors ↔ L4 slide 6 ↔ FoC's services, edge proxy, Kafka and Redis (L4-backlog deck) ↔ the notation reused in every later chapter's diagrams.
* Control vs data flow ↔ L4 slide 10 ↔ Week 9's data-flow emphasis (events) vs Week 6's call-oriented REST.
* Messages and events ↔ L4 slides 12–13 ↔ the Grab-like example (Quiz 2 also uses a Grab-like app) ↔ FoC's exactly-once wallet (NFR6).
* Slicing, modularity, coupling & cohesion ↔ L4 slides 14–18 ↔ Tutorial 2's backlog-to-structure step ↔ Weeks 7–8 (microservice decomposition).
* Styles ↔ L4 slides 19–22 ↔ W6 (layered, MVC, SPA), W7–W8 (microservices), W9 (event-driven).

## Further reading

All cited on the slides: Bass, Clements & Kazman, *Software Architecture in Practice* (2e) — the definition's source; Lethbridge & Laganière, *Object-Oriented Software Engineering*, ch. 9 — the cohesion and coupling tables; David Parnas's work on modularity; the se-education.org addressbook-level3 developer guide — the reference-architecture example.

## Summary

**Key takeaways**

* **Architecture is the structure of components, their externally visible properties, and their relationships — functionalities + NFRs.** (→ outcome 1)
* **Components, connectors, and configuration are the only building blocks; the notation says what each arrow means.** (→ outcome 1)
* **Arrows mean control flow or data flow; interactions are call-and-return or messages and events.** (→ outcome 2)
* **Messages go to addresses; events are immutable, ordered records emitted for anyone listening — the basis of reliable wallet effects.** (→ outcome 2)
* **Slice horizontally for layers, vertically for capabilities; modularity is the discipline that makes either work.** (→ outcome 3)
* **Coupling (lower is better) and cohesion (higher is better) are the grade of a decomposition.** (→ outcome 4)
* **Styles sit on a 2×2: technical/domain division × monolithic/distributed deployment.** (→ outcome 5)

**Key terms**

| Term | One-line definition | Unit |
|---|---|---|
| Software architecture | The structure(s) of components, their externally visible properties, and their relationships | [W4.1](#W4-c1) |
| Reference architecture | Explains the high-level structures of similar applications — many applications, one framework | [W4.1](#W4-c1) |
| Architectural pattern | An architectural solution forming the basis for design — application-specific problem, specific context, stated constraints | [W4.1](#W4-c1) |
| Component | An element modeling an application-specific function, responsibility, or task | [W4.2](#W4-c2) |
| Connector | An element modeling interactions among components, transferring control and/or data | [W4.2](#W4-c2) |
| Configuration | The topology or structure — the arrangement of components and connectors | [W4.2](#W4-c2) |
| Control flow | Reasons about computation order — how the focus of control moves; data may accompany it | [W4.3](#W4-c3) |
| Data flow | Reasons about data availability, transformation, and latency; as data moves, control is activated | [W4.3](#W4-c3) |
| Call and return | Interaction where control moves from one component to another and back — hierarchical or not | [W4.4](#W4-c4) |
| Message and event | A message is data sent to a specific address; an event is immutable, ordered data emitted for anyone listening (full definitions in Weeks 9–10) | [W4.4](#W4-c4) |
| Modularity | Decomposing into smaller chunks with well-defined interfaces (APIs) | [W4.5](#W4-c5) |
| Horizontal slicing | Cut by technical layer: one slice = one layer spanning every domain | [W4.5](#W4-c5) |
| Vertical slicing | Cut by business domain: one slice = one capability, top to bottom | [W4.5](#W4-c5) |
| Cohesion | How strongly a module's facilities belong together (higher is better) | [W4.6](#W4-c6) |
| Functional cohesion | Strongest form: facilities perform one computation, no side effects | [W4.6](#W4-c6) |
| Layer cohesion | Related services together in a strict hierarchy, higher levels accessing only lower ones | [W4.6](#W4-c6) |
| Communicational cohesion | Facilities operating on the same data kept together | [W4.6](#W4-c6) |
| Sequential cohesion | Procedures in sequence kept together — one's output is the next's input | [W4.6](#W4-c6) |
| Procedural cohesion | Procedures called one after another kept together | [W4.6](#W4-c6) |
| Temporal cohesion | Procedures used in the same execution phase (initialization, termination) kept together | [W4.6](#W4-c6) |
| Utility cohesion | Related utilities kept together when no stronger form applies | [W4.6](#W4-c6) |
| Coupling | How strongly modules depend on each other (lower is better) | [W4.6](#W4-c6) |
| Content coupling | Worst form: a component modifies another's internal data | [W4.6](#W4-c6) |
| Common/global coupling | All modules using the same global variable are coupled | [W4.6](#W4-c6) |
| Control coupling | One module passes a flag dictating what another should do | [W4.6](#W4-c6) |
| Data coupling | Modules share data via parameters — data, not instructions | [W4.6](#W4-c6) |
| External coupling | Dependency on elements outside the system — OS, shared libraries, hardware | [W4.6](#W4-c6) |
| Temporal coupling | Actions bundled only because they occur at the same time | [W4.6](#W4-c6) |
| Inclusion/import coupling | Coupling introduced by including a file or importing a package | [W4.6](#W4-c6) |
| Architectural style | A named philosophy constraining code division and deployment | [W4.7](#W4-c7) |
| Modular monolith | One deployed unit, domain-partitioned code with well-defined interfaces | [W4.7](#W4-c7) |
| Technical partitioning | Divide code by technical concern — presentation, services, persistence | [W4.7](#W4-c7) |
| Domain partitioning | Divide code by business domain — customer, payment, shipping | [W4.7](#W4-c7) |
| Monolithic deployment | All logical components deployed as one unit; the application runs as one process | [W4.7](#W4-c7) |
| Distributed deployment | Independent logical components run as individual processes communicating over the network | [W4.7](#W4-c7) |

%%Next: Week 5 brings the cloud-native paradigm (a guest lecture by Dell): what the styles of W4.7 look like when infrastructure itself is fluid — and Week 6 deep-dives the layered style, MVC, and REST.%%

</div>
