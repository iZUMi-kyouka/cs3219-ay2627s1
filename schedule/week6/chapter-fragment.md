{% from "schedule/macros-fragment.md" import term, example with context %}
<h2 id="title">Week 6 — Architecture (II) & REST</h2>

<span id="prereqs">

**Prerequisites:** [Week 4 — Architecture (I) & Product Backlog]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html) (software architecture, components and connectors, the modular monolith) and [Week 5 — Cloud-Native Paradigm]({{baseUrl}}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html) (deployment, containers). Tutorial 4's coupling types are assumed in W6.4.
</span>

<span id="outcomes">

**Learning outcomes:**

* **Can** classify an architectural style along two axes — how the code is divided (technical vs domain concern) and how the system is deployed (single unit vs distributed units). — [W6.1](#W6-c1)
* **Can** explain the buys and costs of the classical styles — layered, pipe-and-filter, modular monolith, MVC, and SPA — and choose between them for a given system. — [W6.2](#W6-c2)–[W6.6](#W6-c6)
* **Can** explain REST as an architectural style, apply its six constraints, and identify resources, representations, and the uniform interface in a RESTful API. — [W6.7](#W6-c7)–[W6.9](#W6-c9)
* **Can** argue when REST is not the right tool and name better-fitting alternatives. — [W6.10](#W6-c10)
* **Can** critique an architecture diagram against the course's guidelines and explain the model-code gap. — [W6.11](#W6-c11)
</span>

<div id="body">

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

## Core concepts

<span id="W6-c1"></span>

### W6.1 Classifying architectural styles ★

**Every {{ term("architectural style", "a reusable way of organizing the major parts of a system") }} answers the same two questions — how is the code divided, and how is it deployed — so learning the taxonomy tells you where each new style lives.** The lecture introduces styles as "many software architectural styles exist — each follows a specific philosophy", because software is built for a specific purpose. (Source: L6-Architecture slide 4.)

**How it works:**

**The first axis is how the code is divided: by technical concern or by domain (business) concern.** A technical division groups code by what it does technically (presentation, business logic, persistence); a domain division groups code by what it is about (orders, recipes, inventory). (Source: L6-Architecture slide 4.)

**The second axis is how the system is deployed: one single deployed unit or several distributed units.** This axis decides your deployment story: one artifact to ship, or many services to host and connect — the question Week 5's containers and orchestration answered for the distributed case. (Source: L6-Architecture slide 4.)

**The four combinations place this course's styles on a map.** Layered (technical, single unit); modular monolith (domain, single unit); event-driven (technical, distributed); microservices (domain, distributed). (Source: L6-Architecture slide 4; the same map reappears as the recap of L7 slide 2 and L4 slide 22 — both place event-driven under the *technical* division, since an event-driven decomposition groups components by their role in the data flow — producers, consumers, transforming stages — not by business domain.)

The diagram below places the styles on the two axes; it is the map the rest of the chapter fills in.

<mermaid>
flowchart TB
  subgraph single["Single deployed unit"]
    layered["Layered — divided by technical concern"]
    mm["Modular monolith — divided by domain concern"]
  end
  subgraph distributed["Distributed units"]
    ms["Microservices — divided by domain concern"]
    ed["Event-driven — divided by technical concern<br/>(components = stages of the data flow)"]
  end
</mermaid>

%%Notation: each box names one architectural style and the axis positions are carried in the box labels; the two subgraphs are the deployment axis (single vs distributed), and within each, the labels carry the code-division axis (technical vs domain).%% To read it: a layered web app kept in one deployable sits top-left (technical division, single unit); the Smart Kitchen app from Quiz 2, split into recipes and inventory modules inside one artifact, sits bottom-left (domain division, single unit); a microservices system sits bottom-right (domain division, many deployables) — which is where Week 7 goes.

<box type="tip" seamless>
**Tip:** when you meet an unfamiliar style, locate it on the two axes first. "Is this a way of dividing code, a way of deploying, or both?" — the question almost always sharpens the comparison the exam asks for.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** A team splits its app into `ui`, `logic`, and `storage` packages within one deployable. A second team splits its app into `ordering`, `payment`, and `delivery` services. Place both on the two axes.
<panel type="seamless" minimized header="%%Answer%%">

Team 1: technical division, single deployed unit (layered). Team 2: domain division, distributed units (microservices-like). The code-division axis, not the number of deployables, is what separates them conceptually.
</panel>

</panel>

<span id="W6-c2"></span>

### W6.2 Layered architecture ★

**Layering is the default way engineers organize a codebase, and its costs — not its benefits — are what exam questions probe.** The style supports independent development and evolution of the system's parts by giving each layer one distinct responsibility. (Source: L6-Architecture slides 6–8.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-layered-architecture" trim />
</box>

**How it works:**

**Layers differ in how strictly they enforce interaction rules.** A *closed* (strict) layer architecture allows interaction only between two consecutive layers; an *open* layer architecture lets any top layer get service from any bottom layer. The lecture's diagram marks the layer interfaces (I-1, I-2, I-3) between Presentation, Business, and Data. (Source: L6-Architecture slide 8.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-closed-layer-architecture" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-open-layer-architecture" trim />
</box>

**Layers are not tiers.** A layer is a logical division inside the software; a tier is a part deployed separately — the lecture's "typical examples: 2-tiered/3-tiered/n-tiered" depend on how you have packaged the application code. (Source: L6-Architecture slide 6.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-tier" trim />
</box>

**The style buys structure-enforced separation of concerns, modifiability, and testability.** You can swap technologies within a layer without affecting other layers — e.g., swap Oracle DB with MySQL — and you can test a layer by mocking the layer below. (Source: L6-Architecture slide 7.)

**The costs are deployment and ownership, and one feature change ripples through all layers.** Deployability is all-or-nothing; no independent scaling; no feature ownership (teams are organized by layers, not features); change amplification — one feature change impacts all layers. The lecture's slide also lists what layering *doesn't* impact — usability, for instance: choosing to layer reshapes the code's structure and packaging, not the user experience. (Source: L6-Architecture slide 7.)

{% call example("Quiz 2 Q2 — bypassing the Business layer to speed up reports") %}
In a closed-layered application, a developer proposes letting the Presentation layer query the Data layer directly for read-only reports, bypassing the Business layer (which performs authorization checks). This opens the layers for one shortcut: the Presentation layer now depends on the Data layer's schema, so the system **can no longer swap the database technology easily** — the modifiability buy of layering is traded away for one page's latency. (Source: Quiz 2, Q2.)
{% endcall %}

The diagram shows the closed-layer rule: each layer talks only to the one below, through an interface.

<mermaid>
flowchart TB
  p["Presentation layer"] -->|"I-1"| b["Business layer"]
  b -->|"I-2"| d["Data layer"]
  d -->|"I-3"| db[(Database)]
</mermaid>

%%Notation: boxes are layers (components), solid arrows are allowed calls, and the labeled edges I-1…I-3 are the layer interfaces.%% To read it: a request for a report enters at Presentation, is authorized and computed in Business, and is served from Data — never skipping a level. If the Presentation layer drew an extra arrow straight to the Database (the Quiz 2 Q2 change), the Business layer's authorization would be bypassed and the Data layer's schema would become public to the UI. %%Slide 8's own diagram is captioned as an *open* layer architecture; the one drawn here is the *closed* variant — the default reading of "layered", and the one the Quiz 2 Q2 shortcut would open.%%

<box type="warning" seamless>
**Pitfall:** treating "3-tier" as a synonym for "3-layer". Tiering is about deployment packaging; layering is about code organization. One codebase can be layered without being distributed, and a distributed system can still be layered inside each service.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Name two buys and two costs of layered architecture from the lecture.
<panel type="seamless" minimized header="%%Answer%%">

Buys: structure-enforced separation of concerns; modifiability within the layer (swap Oracle with MySQL); testability (mock the layer below). Costs: all-or-nothing deployability; no independent scaling; no feature ownership; change amplification. Any two of each.
</panel>

**Q2.** What is the most significant consequence of opening a closed layered design (Quiz 2 Q2)?
<panel type="seamless" minimized header="%%Answer%%">

The system can no longer swap the database technology easily — upper layers now depend on the Data layer's internals, destroying the layer-swap flexibility that was layering's main buy.
</panel>

</panel>

<span id="W6-c3"></span>

### W6.3 Pipe-and-filter ★

**When the work is a stream of data to transform rather than a user to serve, pipe-and-filter divides the task into replaceable, replicable steps.** Data enters the system and flows through the components one at a time until it reaches a final destination (the data sink), with a series of transformations applied on the way. (Source: L6-Architecture slide 9.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-pipe-and-filter" trim />
</box>

**How it works:**

**The style has exactly two kinds of components and one kind of connector.** Components: filters, data source, data sink — each with a set of inputs (read) and outputs (produce). Connectors: pipes, each transmitting one filter's outputs to another filter's inputs. (Source: L6-Architecture slide 9.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-filter" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-pipe" trim />
</box>

**A filter is independent and incremental.** It transforms the input streams, computes incrementally so output begins before the input is fully consumed, and shares no state with other filters. (Source: L6-Architecture slide 9.)

**The style fits batch and stream transformation, not rich user interaction.** Data flows in streams — good for images, audio, video, or batch data; good for limited user interaction like batch processing. (Source: L6-Architecture slide 10.)

**Its buys come from filter independence; its costs come from the pipeline's shape.** Buys: scalability (stateless filters can be replicated), deployability (replace any filter as long as the data-format contract holds), testability (no side effects — independent mocking), and reuse (the same filter in another pipeline). Costs: latency grows with every stage (plus data transformation); usability suffers (no feedback until you check the sink); partial failures are not handled natively. Choose it when the work involves batch/stream transformation and throughput matters more than latency. (Source: L6-Architecture slide 12.)

{% call example("L6-Architecture slide 11 — an image-processing pipeline on Azure Functions") %}
An image-processing pipeline: an uploaded photo (data source) flows through Azure storage **queues** (pipes) into Azure **functions** (filters) for content moderation, resizing, reorientation, and watermarking, ending at content delivery network (CDN) publication (data sink). Each function reads a defined format and produces a defined format, so the watermarking filter can be replaced or replicated without touching the others.
{% endcall %}

{% call example("Quiz 2 Q7 — the CPU-heavy resize filter") %}
Monitoring an image-processing pipeline shows the resize filter is CPU-heavy with a growing job queue in front of it, and the other components are mostly idle. Because filters are stateless and independent, the right fix is to **add extra resize filters consuming from the same job queue** — replicate the bottleneck stage. Moving logic into the idle pipe, buying a bigger machine, or merging stages would not use the style's actual buy. (Source: Quiz 2, Q7.)
{% endcall %}

The diagram traces the Azure image pipeline from source to sink; note the pipes are queues, not calls.

<mermaid>
flowchart LR
  src(["Photo uploaded<br/>(data source)"]) -->|"pipe:<br/>storage queue"| f1["Content moderation"]
  f1 -->|"pipe"| f2["Resizing"]
  f2 -->|"pipe"| f3["Reorientation"]
  f3 -->|"pipe"| f4["Watermarking"]
  f4 -->|"pipe"| sink(["CDN publication<br/>(data sink)"])
</mermaid>

%%Notation: rounded boxes are the data source and data sink, rectangles are filters, and labeled solid arrows are pipes transmitting data in a defined format.%% To read it: a photo enters at the source and is transformed one stage at a time — moderated, resized, reoriented, watermarked — until it lands in the sink. Because each stage only knows the data format, Quiz 2's fix (replicating the slow resize filter behind the same queue) changes one box and no arrows.

<box type="warning" seamless>
**Pitfall:** choosing pipe-and-filter for an interactive feature. A user editing a booking wants immediate feedback; a pipeline gives none until the data reaches the sink (the lecture's "usability — no feedback until we check the sink") and every stage adds latency. (Source: L6-Architecture slide 12.)
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Why does statelessness of filters buy scalability?
<panel type="seamless" minimized header="%%Answer%%">

A stateless filter keeps no data between items, so any number of replicas can consume from the same pipe in parallel — the Quiz 2 Q7 fix — without coordination or shared state.
</panel>

**Q2.** Which architectural style is best suited for non-user-centric interactions like data transformation, and why?
<panel type="seamless" minimized header="%%Answer%%">

Pipe-and-filter: data flows in streams through independent transformations, throughput matters more than latency, and user feedback is not required. (Source: Quiz 2, Q8.)
</panel>

</panel>

<span id="W6-c4"></span>

### W6.4 Modular monolith: package by domain ★★

**The modular monolith keeps one deployable but changes the dividing lines from technical concerns to business domains — and that single change buys feature ownership.** Where the layered architecture separates by technical concern, the modular monolith separates by domain (business) concern, with individual domains making up the modules. (Source: L6-Architecture slide 13.)

**How it works:**

**Packaging by domain puts each module's UI, logic, and data side by side.** The lecture's diagram contrasts the two packagings: package-by-technical stacks Presentation/Workflow/Persistence across all features; package-by-business-concern gives the Order domain its own UI, "place order" workflow, and order data, the Recipe domain its own, and so on. (Source: L6-Architecture slide 13.)

**Discipline is what keeps the modules modular: replace implicit access with explicit, narrow contracts.** Each domain exposes a small API and hides its implementation, so modules cannot reach into each other's internals. (Source: L6-Architecture slide 14.)

**The buys are business alignment; the costs are reuse and scaling.** Buys: deployability due to domain partitioning, cross-functional teams specializing in domains, better alignment with the business problem, maintainability (domain-specific code is easier to maintain), testability (the team understands the domain — better testing of scenarios and edge cases), and performance (one process, no distributed communication). Costs: reusability suffers (hard to reuse across modules due to domain-level dependencies), scalability (one deployment, no independent scaling), and fragile boundaries — functionality may accidentally spawn across modules. (Source: L6-Architecture slide 15.)

**The {{ term("modular monolith", "a single deployable unit organized internally into well-defined components, here packaged by business domain") }} is the springboard to microservices: Week 7 asks exactly when splitting it helps or hurts.** (Source: L7 slide 15.)

{% call example("Quiz 2 Q4–Q5 — Smart Kitchen's recipes and inventory modules") %}
Smart Kitchen is a modular monolith. The **recipes module** stores dish instructions and ingredient requirements; the **inventory module** tracks available ingredients, their quantities, and expiration dates. They are separate modules because **they represent separate business domains with different responsibilities** — not because they need different languages or separate servers. When a user opens a pancake recipe, the app checks whether enough eggs and flour are available by calling the inventory module, and **inventory returns the result via its availability-check API** — explicit, narrow contracts between domains, never recipes reading inventory's tables directly. (Source: Quiz 2, Q4–Q5.)
{% endcall %}

<box type="warning" seamless>
**Pitfall:** letting boundaries blur. The lecture's "fragile boundaries" cost is the modular monolith's characteristic failure: a feature is implemented inside the wrong module or reaches around a module's API, and the codebase silently degrades back into a tangle — with none of the deployment simplicity lost and none of the domain alignment gained.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** In one sentence each: what does the layered style divide by, and what does the modular monolith divide by?
<panel type="seamless" minimized header="%%Answer%%">

Layered: technical concern (presentation, workflow/logic, persistence). Modular monolith: domain (business) concern — order, recipe, inventory domains each bundling their own UI, logic, and data.
</panel>

**Q2.** Smart Kitchen's recipe module needs to know if ingredients are available. Which integration is in the spirit of the style — and which is a boundary violation?
<panel type="seamless" minimized header="%%Answer%%">

In spirit: call inventory's availability-check API (explicit, narrow contract). Violation: recipes reading the inventory tables directly (implicit access into another domain's data — Quiz 2 Q5's wrong options).
</panel>

</panel>

<span id="W6-c5"></span>

### W6.5 MVC and Web MVC ★

**MVC exists because UI-heavy programs mix three concerns that change for different reasons — what is shown, what input means, and what is true.** The style separates code into three components and is mostly applicable to programs with (G)UIs: mobile apps, games, web apps. (Source: L6-Architecture slide 18.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-mvc" trim />
</box>

**How it works:**

**Each component owns one concern.** The view holds the widgets in the UI (buttons, text boxes); the controller coordinates between the model and the view; the model represents the business logic and the state of the system. (Source: L6-Architecture slide 18.)

**The benefits are separation of concerns, extensibility, and testability.** SOC — separation of concerns — between data storage, data handling, data visualization, and user interaction; a new view/controller pair can be added for a new interface medium, or new functionality added to the model independently; components are easy to mock. (Source: L6-Architecture slide 19.)

**Web MVC assigns the three roles across the client-server split.** The server holds the model; the controller handles the user's HTTP request, selects the model, and prepares the view; the view renders the HTTP response (in ASP.net, ASP files are HTML templates with server-side scripts); the model is business logic + persistence, possibly via ORM, and must manage concurrent modifications. (Source: L6-Architecture slide 20.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-web-mvc" trim />
</box>

**Controllers grow extra machinery at web scale: page controllers and front controllers.** The controller maps requests to handlers; usually split as a page controller (handles the requests for one specific page) and a front controller (a single entry point that receives *all* HTTP requests and maps each to its handler — middleware can sometimes play this role). (Source: L6-Architecture slide 21.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-page-controller" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-front-controller" trim />
</box>

**The style's costs are hops and fat controllers.** Performance: multiple hops for a single view update; the "fat controller" anti-pattern — because requests flow through the controller, new logic tends to accumulate there. The buys: usability (the model never calls back the view, so any number of views can serve one model) and modifiability (replace view or model independently). (Source: L6-Architecture slide 22.)

{% call example("L6-Architecture slides 17 and 20 — the search form, MVC-style") %}
A client submits `<form action="search" method="post">`. The web server's controller receives the POST, asks the model (business logic + persistence) to run the search, selects a view template, and the view renders the HTML result page returned to the browser. Quiz 2 Q6 shows a diagram of exactly this shape — client request handled by a coordinating controller over a model and returned through a view — and asks which style it represents: the answer is **MVC**.
{% endcall %}

The diagram follows one HTTP request through Web MVC's three components.

<mermaid>
flowchart LR
  br(["Browser (client)"]) -->|"1. HTTP request"| c["Controller"]
  c -->|"2. select / update"| m["Model — business logic + persistence"]
  c -->|"3. prepare"| v["View — renders the response"]
  v -->|"4. HTML response"| br
</mermaid>

%%Notation: boxes are MVC components (the rounded box is the client), solid arrows are the request's path, and the numbers give the order of one request.%% To read it: for the search form, the browser's POST (1) reaches the controller, which selects and updates the model (2) and prepares the view (3); the view renders the result page and the browser receives HTML (4). The model never talks to the browser directly — that indirection is what lets a second view (say, JSON for a mobile client) reuse the same model.

<box type="warning" seamless>
**Pitfall:** the fat controller. Because every request flows through the controller, it is tempting to put validation, business rules, and persistence calls there; the lecture names this as the style's characteristic cost, and the fix is to keep the controller coordinating — logic belongs in the model.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Which MVC component would you change to add a mobile-friendly interface without touching business logic?
<panel type="seamless" minimized header="%%Answer%%">

Add a new view (and its controller pair) — the lecture's extensibility buy: "a new view/controller pair can be added for a new interface medium" while the model is reused unchanged.
</panel>

**Q2.** In Web MVC, what are the page controller and front controller each responsible for?
<panel type="seamless" minimized header="%%Answer%%">

Page controller: handles requests for a specific page. Front controller: the single entry point that receives all HTTP requests and maps each to its handler; middleware can sometimes play this role.
</panel>

</panel>

<span id="W6-c6"></span>

### W6.6 Single-page applications (SPA) ★

**The SPA trades page refreshes for a program that lives in the browser — better experience, new security bill.** The lecture sets it up by contrasting two web-app flows: the classic form POST (HTML page back, more refreshes, more server work) versus the {{ term("Ajax", "a browser technique where a script sends HTTP requests and processes responses in the background — no page refresh") }} flow (a script posts in the background, JSON comes back, fewer refreshes). (Source: L6-Architecture slide 23.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-ajax" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-spa" trim />
</box>

**A single-page application moves UI generation into the browser, so the server stops sending pages and starts sending data.**

<mermaid>
flowchart LR
    BR["Browser:<br/>single page +<br/>MV* engine"] -->|"1. load page (once)"| WS["Web server"]
    BR -->|"2. JSON over HTTPS<br/>(API calls)"| API["Application server:<br/>business services, data"]
    API -.->|"JSON responses"| BR
</mermaid>

%%Notation: the left box is what runs in the browser after the first load; the right boxes are server-side; the solid arrow ① is the one-time page download, ② and the dashed reply are the ongoing data exchanges — no further HTML documents.%%

How to read it: this is the rightmost column of L4 slide 5 ("client-side MV* web application — focus on client-side customization", JSON data crossing the wire) drawn as a flow. Walk it with the errand platform modernised: the vendor's browser downloads the errand board app once; accepting an errand then calls `POST /orders/{id}/accept` and gets a JSON status back — the client's MV* engine (MVC and its variants) re-renders the board locally with no page reload. Compare with the classic form-POST flow that opened this unit (slide 23): the same user goal now costs one small data exchange instead of a full page round trip, and the server's MVC splits into a JSON API plus a client-side view layer — which is precisely why W6.7 then asks what constraints a *well-behaved* API should satisfy.

**How it works:**

**The SPA moves rendering work to the client.** A JavaScript program is downloaded into the browser and continuously runs there, sending queries and retrieving data in the background without refreshing the webpage. (Source: L6-Architecture slide 24.)

**The advantages are user-facing.** A fluid experience, bandwidth saved, and reduced perceived latency. (Source: L6-Architecture slide 24.)

**The disadvantages are developer-facing.** Harder to develop, needs JavaScript, and vulnerable to XSS attacks. (Source: L6-Architecture slide 24.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-xss" trim />
</box>

**The buys/costs table sharpens the trade.** Buys: usability (no full page reloads), scalability (rendering cost moves to the client; the server sends JSON only), reduced perceived latency (after initial load, data loads in the background). Costs: security (XSS vulnerability; reduced client-side trust — tokens held client-side can be attacked), so every authorization rule must be re-enforced on the server side; and initial performance (larger initial download). (Source: L6-Architecture slide 25.)

{% call example("L6-Architecture slide 23 — the same search, Ajax-style") %}
The same search form now carries a `<script>` block that calls `ajax.post()` and handles the `.response()`. The initial GET returns the page (the SPA program); the search itself is an Ajax POST that returns JSON text, which the in-browser program renders — no page refresh. The server's work per interaction drops from "render a whole HTML result page" to "send JSON".
{% endcall %}

<box type="warning" seamless>
**Pitfall:** trusting the client because it renders the UI. An SPA holds tokens and renders screens locally, but the lecture's rule stands: **every authorization rule must be re-enforced on the server side** — the client can always be tampered with.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Why does an SPA buy server-side scalability?
<panel type="seamless" minimized header="%%Answer%%">

Rendering cost shifts to the client; the server sends JSON only instead of full HTML pages, so each request does less work on the server.
</panel>

**Q2.** Name the SPA cost that has no classic-web-app equivalent.
<panel type="seamless" minimized header="%%Answer%%">

Client-side security exposure: XSS vulnerability and reduced client-side trust (client-held tokens can be attacked), which forces every authorization rule to be re-enforced server-side.
</panel>

</panel>

<box type="info" seamless>

**Section summary — classical styles:**

* **Two axes classify every style**: code division (technical vs domain) × deployment (single unit vs distributed) (W6.1).
* **Layered** buys separation of concerns, swap-ability, and testability, and costs all-or-nothing deployment, scaling, and feature ownership; closed vs open layers decide how strict the rule is (W6.2).
* **Pipe-and-filter** buys replicability and replaceability for stream transformation, and costs latency and feedback (W6.3).
* **Modular monolith** re-divides a single deployable by business domain behind narrow APIs — aligned with the business but one deployment, fragile boundaries (W6.4).
* **MVC/SPA** organize the UI side: MVC separates view/controller/model; the SPA moves rendering into the browser for fluidity, paying in security (W6.5–W6.6).
</box>

<span id="W6-c7"></span>

### W6.7 REST: an architectural style for the web ★

**REST is the style that made the web's API layer uniform: one set of constraints, exploited everywhere, for any client.** It was originated by Roy Thomas Fielding — principal author of the HTTP specification and co-founder of the Apache HTTP server — in his dissertation *Architectural Styles and the Design of Network-based Software Architectures*. (Source: L6-REST slide 3.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-rest" trim />
</box>

**How it works:**

**REST is a set of constraints, not an architecture by itself.** The lecture is explicit: it defines "a set of rules to be used for creating web services" — not an architecture by itself — with the intention of providing uniform interoperability between different applications on the internet. (Source: L6-REST slides 4 and 17.)

**REST targets five quality improvements.** Performance and scalability, simplicity of interaction, modifiability, reliability, and extensibility. (Source: L6-REST slide 3.)

**The word "hypermedia" in the definition is doing real work.** Hypertext is text with hyperlinks to other text; multimedia integrates text, audio, video, and graphics; hypermedia is the nonlinear medium combining them with hyperlinks. REST constrains the transfer of representations *of hypermedia* — which is why links inside representations matter later in W6.9. (Source: L6-REST slide 5.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-hypermedia" trim />
</box>

**REST exploits HTTP's native capabilities rather than inventing its own protocol.** HTTP requests the access and use of data; the style uses GET, PUT, POST, DELETE natively — the uniform interface of W6.8. (Source: L6-REST slide 4.)

<box type="tip" seamless>
**Tip:** keep the lecture's two-line summary handy: "REST provides a set of guidelines and constraints to develop web services — not an architecture by itself", and its constraints are "quite broad-based; can be used to develop many kinds of web applications". (Source: L6-REST slide 17.)
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Is "our system uses REST" an architecture decision or a style choice — and what is the difference?
<panel type="seamless" minimized header="%%Answer%%">

A style choice. REST is a set of constraints for creating web services, not an architecture by itself (L6-REST slides 4, 17); the concrete architecture — which services exist, how they deploy — is still yours to design under those constraints.
</panel>

</panel>

<span id="W6-c8"></span>

### W6.8 The REST constraints ★

**The six constraints are REST's whole content — each buys specific qualities, and each has a cost you can name.** The lecture's overview slide lists them around the word REST: client-server, stateless, cacheable, layered system, uniform interface, and code-on-demand. (Source: L6-REST slide 6.)

**How it works — constraint by constraint:**

**Client-server: separate the concerns of storing data and presenting it.** REST applications should have a client-server architecture: the client requests resources, the server holds them; the client is not concerned with data storage, the server not with user interface or user state — improving the portability of the UI and the scalability of server components, so both evolve independently. (Source: L6-REST slide 7.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-client-server-constraint" trim />
</box>

**Stateless: every request must stand entirely on its own.** Each interaction has to be entirely self-contained — full information in query params, headers, or URI; no client state or "session" kept on the server, so the server is bound by the number of concurrent requests, not the number of clients. This improves scalability (the server quickly frees resources), reliability (recovery from partial failures), and monitoring (analyze one request in isolation). (Source: L6-REST slide 8.)

{% call example("L6-REST slide 8 — the professor who does not remember you") %}
A student messages: "Prof, I'm John, Team 3, I need to change the presentation slot." The server-side professor — stateless — replies "Errm! Who are you? Which course?" because nothing from earlier messages is remembered. The stateless client must resend the full context every time: "Prof, to SDA course, I'm John from Team 3, I need to change the presentation slot." Every request carries its whole world; that is the stateless constraint, with its cost — repetitive data sent in a series of queries.
{% endcall %}

**Cacheable: responses declare whether — and for how long — they may be reused.** The server's response states if the data is cacheable (and for how long) or not; the client returns cached data for subsequent equivalent requests, potentially eliminating interactions and improving efficiency and user-perceived performance. The minus: the client can receive stale data. (Source: L6-REST slide 9.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-cacheable" trim />
</box>

**Layered system: each layer sees only its immediate neighbor.** The application is organized as a (network) layered system; intermediaries may improve availability and performance ({{ term("load balancing", "distributing requests across multiple server instances — Week 12 develops it in full") }}, caching) and provide data transformation and filtering — at the cost of overall system complexity. (Source: L6-REST slide 10.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-rest-layered-system" trim />
</box>

**Uniform interface: one way in, for every client.** There should be a uniform way of interacting with a given server irrespective of device or application type — generality applied to the component interface. Implementations are decoupled from the services they provide; interactions exploit HTTP requests (GET, PUT, POST, DELETE) and responses (status codes like 200 OK, 404 NOT FOUND), with the HTTP body transferring the resource representation. (Source: L6-REST slide 11.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-statelessness" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-uniform-interface" trim />
</box>

**Code-on-demand (optional): extend the client by downloading executable code.** Applets and JavaScript code are the lecture's examples — it simplifies the client from having to pre-implement all functionality and allows extensibility. It is the one constraint REST marks optional. (Source: L6-REST slide 15.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-code-on-demand" trim />
</box>

The diagram shows how statelessness, cacheability, and layering combine in one request path.

<mermaid>
flowchart LR
  c1["Client 1"] -->|"GET /orders/123 (full context in request)"| lb["Load balancer — layered intermediary"]
  c2["Client 2"] -->|"GET /orders/123 (full context in request)"| lb
  lb -->|"cache hit"| ch["Shared cache"]
  lb -->|"cache miss"| s1["REST server 1 — stateless"]
  lb -->|"cache miss"| s2["REST server 2 — stateless"]
  s1 --> db[(Orders database)]
  s2 --> db
</mermaid>

%%Notation: boxes are components (clients, intermediaries, servers), the cylinder is a data store, solid arrows are synchronous HTTP calls, and the edge labels carry the constraint each hop exercises.%% To read it: both clients send the same request with **all needed context inside it** (stateless), so the load balancer (layered system — a neighbor each side never sees beyond) may route either request to any server replica. The response was marked cacheable, so the shared cache can answer repeats without touching a server (cacheability) — this is exactly Quiz 2 Q9's fix for a latency-and-database-load problem: add an application-layer load balancer and shared caching layer, not server-side sessions, which would violate statelessness.

<box type="warning" seamless>
**Pitfall:** reaching for server-side sessions when traffic hurts. Quiz 2 Q9's wrong answers are the tempting ones — introducing server-side HTTP sessions breaks statelessness (servers become bound to clients, not requests); moving business logic into the client abandons the server's role. Stay within the constraints: cache + load balance.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Name the six REST constraints and say which one is optional.
<panel type="seamless" minimized header="%%Answer%%">

Client-server, stateless, cacheable, layered system, uniform interface, code-on-demand — code-on-demand is the optional one.
</panel>

**Q2.** A teammate proposes storing the logged-in user's cart in a server-side session to "make requests faster". Which constraint does this violate, and what does the server lose?
<panel type="seamless" minimized header="%%Answer%%">

Statelessness. The server becomes bound to the number of clients interacting rather than the number of concurrent requests — it can no longer quickly free resources (scalability), easily recover from partial failures (reliability), or analyze a request in isolation (monitoring).
</panel>

**Q3.** Which constraint lets a client survive a server crash-and-restart between two requests?
<panel type="seamless" minimized header="%%Answer%%">

Statelessness — no session is kept on the server, so any replica (or a restarted one) can serve the next self-contained request; the lecture lists recovery from partial failures as a statelessness reason.
</panel>

</panel>

<span id="W6-c9"></span>

### W6.9 Resources, representations, and content negotiation ★★

**The uniform interface needs something uniform to point at — REST's answer is the resource, addressed by URI and exchanged as representations.** The lecture unpacks the uniform interface into resource orientation, self-describing messages, and hypermedia links. (Source: L6-REST slides 12–14.)

**How it works:**

**Anything can be a resource — it is the key abstraction of information in REST.** A document, an image, a user; a resource is a conceptual mapping to a set of entities, identified using stable, global, unique resource identifiers — e.g., `/device-management/managed-devices/{device-id}`. (Source: L6-REST slide 12.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-resource" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-uri" trim />
</box>

**Clients operate on representations, not on the resource itself.** A representation consists of data plus metadata describing the data; the client holding a representation has enough information to modify the resource on the server — e.g., `HTTP DELETE /device-management/managed-devices/{device-id}`. (Source: L6-REST slide 12.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-representation" trim />
</box>

<box type="tip" seamless>
**Tip:** {{ term("content negotiation", "the HTTP mechanism by which clients request a preferred representation format and the server chooses the appropriate one") }} answers the natural follow-up — how does one uniform interface carry text, images, video, and PDFs? The Content-Type header (MIME types) specifies the representation format; clients request preferred formats via `Accept:`; binary media travel as binary streams over HTTP. Example from the lecture: `GET /document/lecture5` with `Accept: application/pdf`. (Source: L6-REST slide 13.)
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-content-negotiation" trim />
</box>

**Messages must be self-describing.** Each message includes enough information to describe how to process it, so the server can easily analyze the request; components can fully understand resources or relevant states just by inspecting representations. (Source: L6-REST slide 14.)

**Hypermedia drives application state: representations carry links.** The representations exchanged should be linked — clients discover and obtain resources from the links, and the links expose new resources and application state transitions. (Source: L6-REST slide 14.)

{% call example("L6-REST slide 14 — a paid order that tells you what it can do next") %}
A client fetches an order and receives:

```json
{
  "id": 123,
  "status": "PAID",
  "links": {
    "self": "/orders/123",
    "cancel": "/orders/123/cancellation",
    "refund": "/orders/123/refunds"
  }
}
```

The representation is self-describing (the client reads `status: "PAID"` without extra knowledge) and hypermedia-driven: because the order is paid, it advertises `cancel` and `refund` links and no `pay` link — the possible state transitions are discoverable from the representation itself, not from out-of-band documentation.
{% endcall %}

<box type="warning" seamless>
**Pitfall:** designing URIs around operations instead of resources. `POST /cancel-order-123` hides what the system manages; the lecture's shape — a resource identified by a stable URI, manipulated through the uniform verbs (`DELETE /orders/123/cancellation`-style paths) — is what keeps clients decoupled from server implementations.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Distinguish resource and representation in one sentence each.
<panel type="seamless" minimized header="%%Answer%%">

Resource: the key abstraction of information — a conceptual mapping to a set of entities, identified by a stable, global, unique URI. Representation: the data + metadata actually exchanged, from which a client can understand (and modify) the resource's state.
</panel>

**Q2.** In the order JSON above, which part makes the message self-describing, and which part is hypermedia?
<panel type="seamless" minimized header="%%Answer%%">

Self-describing: the message carries its own processing information — `id`, `status` (and the Content-Type header outside the body). Hypermedia: the `links` object, which exposes the state transitions (`cancel`, `refund`) the client may follow next.
</panel>

</panel>

<span id="W6-c10"></span>

### W6.10 REST: strengths, limits, and alternatives ★★

**REST's strengths and weaknesses come from the same source — its generic, uniform, stateless web plumbing — so knowing when *not* to use it is part of knowing REST.** (Source: L6-REST slide 16.)

**How it works:**

**The advantages are the constraints' buys restated.** Less tightly coupled systems; scalability, usability, accessibility, and "mashup-ability" (one service's data can be mixed with another's in a new application); new media types can be added without breaking clients. (Source: L6-REST slide 16.)

**The disadvantages are the constraints' costs restated.** Weak contract enforcement — no built-in typing, runtime errors; statelessness can decrease network performance by re-sending data in series of queries; and using URIs can degrade efficiency, because information travels in a standardized form rather than one tuned to a specific application's needs. (Source: L6-REST slide 16.)

{% call example("Quiz 2 Q10 — the price of a standardized form") %}
"Using URIs to transfer information in a standardized form can **degrade efficiency relative to formats tuned specifically to one application's needs**." A bespoke binary format could pack the same booking data smaller and faster; REST trades that per-application efficiency for uniform interoperability — the lecture's disadvantage, verbatim, as an exam item. (Source: Quiz 2, Q10; L6-REST slide 16.)
{% endcall %}

**The lecture gives a scenario table of when REST is not the right tool — each row names the better alternative and why.** (Source: L6-REST slide 18.)

| Scenario | Why REST becomes problematic | Better alternative |
|---|---|---|
| High-frequency service-to-service calls | HTTP + JSON overhead; repeated serialization; TCP connection costs | gRPC (binary, HTTP/2, strong typing) |
| Event-driven workflows (Order placed → Payment → Inventory → Shipping) | REST enforces synchronous request–response coupling | Event-driven architecture (Kafka, RabbitMQ, SNS/SQS) |
| Long-running business processes (sagas) | Hard to coordinate distributed transactions via REST | Event-driven + message choreography |
| Real-time streaming (live updates, telemetry) | Request–response requires polling | WebSockets, push-based mechanisms, Kafka streams |
| Fan-out communication (one update, many consumers) | Multiple REST calls or tight orchestration | Publish–subscribe messaging |
| Service autonomy and resilience | Synchronous dependency chains (A waits for B) | Asynchronous messaging |
| High-scale write-heavy systems | Request bottlenecks | Message queues with buffering |
| Complex aggregation across services | Chatty APIs, over-fetching | Event-driven materialized views / CQRS |
| Intermittently connected systems (IoT, edge) | Requires immediate availability | Store-and-forward messaging |

%%Jargon in the table (terms from L6-REST slide 18): a *saga* runs a long-running business process as a sequence of local steps with compensating actions; *CQRS* (command–query responsibility segregation) keeps separate write-side and read-side models; a *materialized view* is a precomputed read model kept up to date from events; *store-and-forward* queues messages until a disconnected party reconnects; *WebSockets* is a persistent, two-way connection over which the server can push updates to the client without the client polling — the push-based answer to the polling cost in that row. The messaging rows are developed in Weeks 9–11.%%

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-grpc" trim />
</box>

{% call example("Quiz 2 Q1 — the Grab-like app, Design A vs Design B") %}
In a Grab-like ride-hailing app, **Design A** has Booking make a synchronous call-and-return to Matching; **Design B** has Booking publish a `BookingRequested` event to the middleware. During peak hours the Matching component crashes for two minutes. Design B **offers reliability by storing the event in the middleware until Matching becomes available** — Booking does not wait, and nothing is lost. Design A's synchronous coupling is precisely the "REST enforces synchronous request–response coupling" row above; the async alternative is Week 9's event-driven architecture. (Source: Quiz 2, Q1; L6-REST slide 18.)
{% endcall %}

<box type="warning" seamless>
**Pitfall:** reading the table as "REST is bad". Each row is a workload shape where REST's synchronous, request–response, human-readable plumbing is the wrong fit — for web APIs consumed by heterogeneous clients, REST's uniformity is exactly the point. Match the style to the interaction, not to fashion.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Your payment service calls the ledger service 50,000 times per second with small typed payloads. Which row of the lecture's table applies, and what is the fix?
<panel type="seamless" minimized header="%%Answer%%">

High-frequency service-to-service calls: HTTP+JSON overhead, repeated serialization, TCP connection costs. Fix: gRPC — binary encoding, multiplexed HTTP/2, strong typing.
</panel>

**Q2.** Booking must trigger Payment, Inventory, and Shipping only when an order is placed, and none of them may block Booking. Why is pure REST the wrong shape here?
<panel type="seamless" minimized header="%%Answer%%">

REST enforces synchronous request–response coupling: Booking would need to call each service and wait (or tightly orchestrate). The table's fix is an event-driven workflow — publish the event and let interested services react (the Grab-like Design B of Quiz 2 Q1).
</panel>

</panel>

<span id="W6-c11"></span>

### W6.11 Communicating the architecture: diagrams and the model-code gap ★★

**An architecture that lives only in code cannot be argued about — the lecture closes with how to draw the big picture and why a diagram is never the code itself.** Architecture diagrams are free-form diagrams: the big picture of what is being built, a shared vision of the team, a focus for technical conversations, a map for navigating the source code, a communication tool for people outside the team, and an onboarding accelerator. (Source: L6-Architecture slide 27.)

**How it works:**

**The model-code gap is the distance between your source code and your architecture model — reduce it, never expect to close it.** Quiz 2 states the correct reading: **architecture models help us reason about complexity and scale and cannot be treated as one-to-one mappings to source code**; models must not be made extensional — turned into a one-to-one mirror of the code — to "eliminate" the gap, and design decisions are not all executable. (Source: L6-Architecture slide 26; Quiz 2, Q3.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-06.md#def-model-code-gap" trim />
</box>

**Diagrams fail in predictable ways.** Notation not explained or inconsistent; ambiguous purpose or meaning of elements; missing or ambiguous relationships; generic terms like "business logic"; omitted technology choices; mixed levels of abstraction; too much or too little detail; no context or logical starting point. (Source: L6-Architecture slide 30.)

**The guidelines are a checklist you can apply to any diagram you draw this semester.** Title and label the diagram; include a legend explaining the notation (meaning of arrows/lines); make acronyms understandable or explained; make elements explicit, described in 1–2 lines; label lines and keep them consistent with directional and relationship intent (unidirectional, dependency, dataflow or control flow, technology protocol). (Source: L6-Architecture slide 31.)

{% call example("Quiz 2 Q6 — reading someone else's diagram") %}
Quiz 2 shows an architecture diagram for an image-sharing application and asks what it "can potentially be representing". The diagram's shape — a coordinating component between user input, data/state, and rendered output — matches **MVC**. The exercise is model-reading: the diagram does not name MVC anywhere; you classify it by structure, the same skill the guidelines assume on the drawing side. (Source: Quiz 2, Q6.)
{% endcall %}

<box type="warning" seamless>
**Pitfall:** trusting a diagram because it looks tidy. A tidy diagram with an unexplained color code, mixed abstraction levels, and unlabeled arrows communicates confidence it has not earned — apply the slide-31 checklist before you believe or present one.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Which statement about the model-code gap is correct, and why?
<panel type="seamless" minimized header="%%Answer%%">

"Architecture models help us reason about complexity and scale and cannot be treated as one-to-one mappings to source code" (Quiz 2 Q3). Models intentionally abstract; forcing them to be extensional or executable destroys the reasoning power that is their purpose.
</panel>

**Q2.** List four defects from the lecture's "diagrams often suffer from…" slide that you would check before submitting an architecture diagram.
<panel type="seamless" minimized header="%%Answer%%">

Any four: unexplained/inconsistent notation; ambiguous element purpose/meaning; missing or ambiguous relationships; generic terms ("business logic"); omitted technology choices; mixed abstraction levels; too much/too little detail; no context or starting point.
</panel>

</panel>

<box type="info" seamless>

**Section summary — REST and communication:**

* **REST is a constraint set, not an architecture**: client-server, stateless, cacheable, layered system, uniform interface, optional code-on-demand (W6.7–W6.8).
* **Statelessness + cacheability + layering compose**: self-contained requests let intermediaries route and cache freely — the Quiz 2 Q9 fix (W6.8).
* **Resources addressed by URIs, exchanged as representations**, with content negotiation and hypermedia links making messages self-describing (W6.9).
* **REST's uniformity costs efficiency and synchrony**; for high-frequency calls, event-driven workflows, streaming, and fan-out, the lecture's table names better-fitting alternatives (W6.10).
* **Diagrams are the architecture's user interface** — apply the guidelines, and treat the model-code gap as permanent by design (W6.11).
</box>

## Connections

| Concept | Lecture | Tutorial | Other weeks |
|---|---|---|---|
| Style taxonomy (division × deployment) | L6-Architecture slide 4 | Tutorial 4 Q1 (coupling between modules) | W7 (microservices = domain × distributed) |
| Layered architecture; closed vs open layers | L6-Architecture slides 6–8 | — | W4 (styles intro), Quiz 2 Q2 |
| Pipe-and-filter | L6-Architecture slides 9–12 | Tutorial 3 Q1 (NewsTrack pipeline) | W9 (event-driven), Quiz 2 Q7–Q8 |
| Modular monolith by domain | L6-Architecture slides 13–15 | — | W4 (modular monolith), W7 (splitting it), Quiz 2 Q4–Q5 |
| MVC, Web MVC, SPA | L6-Architecture slides 16–25 | — | Quiz 2 Q6 |
| REST style and constraints | L6-REST slides 3–15 | — | W7 (service communication), Quiz 2 Q9 |
| Resources/representations; when REST is not right | L6-REST slides 12–18 | — | W9–W11 (EDA, async, messaging), Quiz 2 Q1, Q10 |
| Architecture diagrams, model-code gap | L6-Architecture slides 26–31 | — | W4 (architecture views), Quiz 2 Q3, Q6 |

## Further reading

* Roy Fielding's dissertation, *Architectural Styles and the Design of Network-based Software Architectures* (L6-REST slide 3): [ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm](https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)
* Microsoft Azure Architecture Center — Pipes and Filters pattern (source of L6-Architecture slide 11): [learn.microsoft.com/en-us/azure/architecture/patterns/pipes-and-filters](https://learn.microsoft.com/en-us/azure/architecture/patterns/pipes-and-filters)
* Simon Brown, *Software Architecture for Developers* (referenced on L6-Architecture slide 27) and the C4 model: [c4model.com](https://c4model.com/)
* George Fairbanks on the model-code gap (L6-Architecture slide 26): [georgefairbanks.com/software-architecture/model-code-gap/](https://www.georgefairbanks.com/software-architecture/model-code-gap/)

## Summary

**Key takeaways:**

* **Classify styles on two axes** — how code is divided (technical vs domain) and how it deploys (single unit vs distributed). (W6.1)
* **Layering points dependencies downward** — buys separation of concerns, layer swaps, and testability; costs all-or-nothing deployment, no independent scaling, no feature ownership, and change amplification. (W6.2)
* **Pipe-and-filter turns a task into independent transformations on a stream** — filters are stateless and replaceable, so bottleneck stages replicate; latency grows per stage and feedback waits for the sink. (W6.3)
* **The modular monolith packages a single deployable by business domain behind narrow APIs** — business-aligned and testable, with fragile boundaries as the price. (W6.4)
* **MVC separates view, controller, and model** — extensible and testable, but hop-heavy and prone to fat controllers. (W6.5)
* **The SPA moves rendering into the browser** — fluid and server-scalable, but XSS-exposed and re-authorized server-side. (W6.6)
* **REST is a constraint set for distributed hypermedia systems, not an architecture by itself.** (W6.7)
* **The six constraints each buy qualities**: client-server, stateless, cacheable, layered system, uniform interface, optional code-on-demand — and statelessness + cacheability + layering compose into the Quiz 2 Q9 fix. (W6.8)
* **Resources addressed by URIs are exchanged as representations**, with content negotiation and hypermedia links making messages self-describing. (W6.9)
* **REST's uniformity costs efficiency and synchrony**; for high-frequency calls, event-driven workflows, streaming, and fan-out, the lecture's table names better-fitting alternatives. (W6.10)
* **Diagrams are the architecture's user interface** — apply the guidelines, and treat the model-code gap as permanent by design. (W6.11)

**Key terms:**

| Term | Definition | Unit |
|---|---|---|
| Architectural style | A reusable way of organizing the major parts of a system (defined in Week 4) | [W6.1](#W6-c1) |
| Layered architecture | Layers of components with dependencies pointing downward, each layer one responsibility | [W6.2](#W6-c2) |
| Closed layer architecture | Interaction only between two consecutive layers — the strict default | [W6.2](#W6-c2) |
| Open layer architecture | Any top layer may get service from any bottom layer, skipping intermediates | [W6.2](#W6-c2) |
| Tier | A part deployed separately — a packaging division; a layer is a logical division | [W6.2](#W6-c2) |
| Pipe-and-filter | Independent transforming filters connected by pipes; no shared filter state | [W6.3](#W6-c3) |
| Filter | A self-contained processing step: transforms input streams, computes incrementally, shares no state | [W6.3](#W6-c3) |
| Pipe | The connector transmitting one filter's outputs to another filter's inputs in a defined format | [W6.3](#W6-c3) |
| Modular monolith | One deployable organized internally into domain modules behind explicit APIs (defined in Week 4) | [W6.4](#W6-c4) |
| MVC | View + controller + model separation for interactive applications | [W6.5](#W6-c5) |
| Web MVC | MVC on the web: server holds the model; controller handles the request and prepares the view; view renders | [W6.5](#W6-c5) |
| Page controller | Handles the requests for one specific page | [W6.5](#W6-c5) |
| Front controller | The single entry point receiving all HTTP requests and mapping each to its handler | [W6.5](#W6-c5) |
| SPA | A browser-resident program that fetches data in the background without page refreshes | [W6.6](#W6-c6) |
| Ajax | Script-driven background HTTP requests and responses — no page refresh | [W6.6](#W6-c6) |
| Cross-site scripting (XSS) | Malicious code running in the victim's browser — why SPA authorization is re-enforced server-side | [W6.6](#W6-c6) |
| REST | Constraint set for distributed hypermedia systems over HTTP | [W6.7](#W6-c7) |
| Hypermedia | The nonlinear medium combining text, graphics, audio, video, and hyperlinks | [W6.7](#W6-c7) |
| Client-server constraint | Separate storing data (server) from presenting it (client); both evolve independently | [W6.8](#W6-c8) |
| Statelessness | Every request self-contained; no client session state on the server | [W6.8](#W6-c8) |
| Cacheable constraint | Responses declare reuse; clients may serve cached copies — possibly stale | [W6.8](#W6-c8) |
| Layered system (REST) | Each layer sees only its immediate neighbor; intermediaries balance load and cache | [W6.8](#W6-c8) |
| Uniform interface | One standard interaction way: HTTP verbs, status codes, body representations | [W6.8](#W6-c8) |
| Code-on-demand | REST's optional constraint: extend the client by downloading executable code | [W6.8](#W6-c8) |
| Resource | REST's key abstraction of information — a conceptual mapping to entities, addressed by a stable URI | [W6.9](#W6-c9) |
| Uniform resource identifier (URI) | The stable, global, unique identifier addressing a resource | [W6.9](#W6-c9) |
| Representation | Data + metadata exchanged; enough for the client to understand and modify the resource | [W6.9](#W6-c9) |
| Content negotiation | Client requests a preferred representation format; server chooses the appropriate one | [W6.9](#W6-c9) |
| gRPC | Binary, HTTP/2, strongly-typed RPC framework for high-frequency service-to-service calls | [W6.10](#W6-c10) |
| Model-code gap | The distance between source code and architecture model — reducible, not removable | [W6.11](#W6-c11) |

%%Next: [Week 7]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html) takes the modular monolith from W6.4 and asks when to split it: the microservice style, its trade-offs against the monolith, and the domain-driven design toolkit — domains, bounded contexts, aggregates — for finding the seams.%%
</div>
