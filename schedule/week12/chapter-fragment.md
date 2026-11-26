{% from "schedule/macros-fragment.md" import term, example, icon_outcome with context %}
<h2 id="title">Week 12 — Scalability</h2>

<span id="prereqs">

This chapter builds on [Week 3 — Requirements]({{baseUrl}}/se-book-adapted/chapters/week-03-requirements.html#core-concepts) (scalability as a quality attribute), [Week 4 — Architecture (I)]({{baseUrl}}/se-book-adapted/chapters/week-04-architecture-i.html#core-concepts) (the modular monolith) and [Week 7 — Microservices (I)]({{baseUrl}}/se-book-adapted/chapters/week-07-microservices-i.html#core-concepts) (extracting services). Week 11's queues and consumers return here as buffers and scaling units.

</span>

<span id="outcomes">

{{ icon_outcome }} **Can explain scalability as a quality attribute and name the dimensions a system can scale in** (W12.1)

{{ icon_outcome }} **Can measure scale with percentile response-time metrics and use them to find the bottleneck** (W12.2)

{{ icon_outcome }} **Can choose between replicating and optimizing resources, and argue why scaling must be planned early** (W12.3)

{{ icon_outcome }} **Can compare vertical and horizontal scaling and design a stateless, load-balanced deployment** (W12.4, W12.5)

{{ icon_outcome }} **Can scale the data tier with caching, read replicas, partitioning and distributed databases, and place a given system on the scale cube** (W12.6–W12.8)

</span>

<div id="body">

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

## Core concepts

<span id="W12-c1"></span>

### W12.1 Scalability as a quality attribute ★

**Traffic is not a fixed property of a system — a design that works at launch can fail at peak, so scalability must be treated as a requirement, not an afterthought.** The lecture recaps Week 3: scalability as a quality attribute has both hardware and software consequences — scaling to accommodate increased incoming data may mean adding disk capacity, while scaling to accommodate more transactions could mean architecting the application for parallel and distributed computing. (Source: L12 slide 3.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-03.md#def-quality-attribute" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-12.md#def-scalability" trim />
</box>

**A system can scale in several dimensions of operations, specific to the application.** The deck names three: the number of requests that can be processed in a given time window, the amount of data that can be managed and processed, and keeping response times stable and consistent as requests increase — which is where scalability meets performance. The added resources are CPU, memory, and servers. (Source: L12 slide 6.)

**Load is not constant, so scaling has a down direction too.** A streaming service at 9 pm faces far more load than at 5 am; autoscaling on a metric — CPU usage, queue length — grows and shrinks capacity with demand. (Source: L12 slide 6.)

**Growth is easiest to see with a physical analogy: add kiosks, or add stores.** A supermarket chain handles more shoppers by adding checkout kiosks (more capacity in one place) or more stores (more places); the software behind it faces exactly the same two levers. (Source: L12 slide 5.)

{% call example("The room-booking platform faces summer (Quiz 3 Q1)") %}
"A room-booking platform is developed as a modular monolith, containing search, reservation, and notification modules. At the start of summer, search consumes 80% of the system resources, while reservation and notification modules consume 5% each, just sufficient to keep the application running. Search uses a separate indexing to make it efficient. The team maintaining this software wants to scale the system to handle the increased load during summer." Everything that follows in this chapter zooms in on this decision — which scaling change best handles summer while keeping capital and operational costs low (Quiz 3 Q1).
{% endcall %}

<box type="warning" seamless>

**Pitfall:** stating "the system must scale" as a requirement. Like any quality attribute, a scalability requirement must be measurable — e.g. a request rate to sustain, a percentile response time to hold — otherwise it cannot be verified or used to choose a design (L3; L12 slide 7).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Which dimension of scalability does each growth stress: (a) the listings table triples in size; (b) bookings per minute triple; (c) search stays equally fast at triple the bookings?
<panel type="seamless" minimized header="%%Answer%%">
(a) amount of data that can be managed and processed; (b) number of requests processed per time window; (c) maintaining stable, consistent response times as requests increase (L12 slide 6).
</panel>

**Q2.** In the room-booking scenario, why is "5% each" for reservation and notification the interesting detail?
<panel type="seamless" minimized header="%%Answer%%">
Because capacity added anywhere else is mostly wasted: 90% of the load comes from search, so replicating the whole monolith gives reservation and notification replicas they do not need — the scaling decision should follow where the load actually is (Quiz 3 Q1).
</panel>

</panel>

<span id="W12-c2"></span>

### W12.2 Measuring scale: percentiles and bottlenecks ★★

**Response time is a distribution, not a number — and the users at the tail are the ones who notice.** An average response time of 2 s under normal load can still leave 1 in 100 users waiting 10 s. (Source: L12 slide 7.)

**Percentile metrics describe the distribution from typical to worst case.** P50 (the median) is a typical user's experience; P95 means 95% of requests are faster than this number — a standard threshold for service-level objectives; P99 captures the worst-case scenarios. (Source: L12 slide 7.)

%%Two terms in that sentence: a *service-level objective* (SLO) is a measurable target for a service level — e.g. a percentile response time held over a window — that a team commits to (Wikipedia: "a target value or range of values for a service level"); the errand requirement below is one. And "the tail" means the slowest few percent of the response-time distribution: P99 says 99% of requests beat the threshold, so the slowest 1% live *beyond* it — it is not the single worst request.%%

{% call example("Errand platform browse SLA (L12 slide 7)") %}
The deck phrases a measurable requirement for the errand platform: "95% of successful browse errand requests complete in <200 ms; 99% complete in <500 ms, in a 7-day window." Two percentiles plus a window — that is a requirement you can measure, alert on, and use to plan scaling.
{% endcall %}

**Measure first, then plan the scaling strategy: the slowest shared component is the bottleneck.** Percentile metrics tell you *where* the tail latency comes from; scaling the wrong component buys nothing. (Source: L12 slide 7.)

<box type="warning" seamless>

**Pitfall:** optimizing the average. A change that improves P50 while P95 explodes has made the system *worse* for the users who were already worst served — service-level objectives are written on tail percentiles for this reason (L12 slide 7).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** "P50 = 1 s, P95 = 5 s, P99 = 50 s." What does each number tell you, and which one would you put in a service-level objective?
<panel type="seamless" minimized header="%%Answer%%">
P50 = 1 s: the median request — a typical user's experience. P95 = 5 s: 95% of requests are faster; the standard SLO threshold. P99 = 50 s: 99% are faster; worst-case scenarios are specified with it. The SLO threshold is P95 (L12 slide 7).
</panel>

</panel>

<span id="W12-c3"></span>

### W12.3 Two strategies to scale — and why late scaling hurts ★★

**There are only two levers: add copies of what you have, or make what you have work less.** Replicating resources provides more capacity to handle requests and increases throughput; optimizing the available resources gets more out of the same hardware — more efficient algorithms, extra indices to speed up queries, rewriting a server in a faster programming language (e.g. Facebook developed HipHop, a compiler for PHP). (Source: L12 slide 8.)

**Scaling after deployment is expensive: downtime, hardware cost, and redesign.** The deck's hypothetical: a web server handling 100 requests/second must handle 100,000 — upgrading the database server takes 15 hours and a more powerful machine, schema updates to handle request hotspots mean a DB redesign, and the rapid-development Ruby web server must be reimplemented in C++ to be efficient and scalable. (Source: L12 slide 9.)

**Scalability is an architectural decision, incorporated from the beginning.** You must estimate the evolution of the software over time: resources and effort costs are tied to scalability from day one. (Source: L12 slide 9.)

<box type="warning" seamless>

**Pitfall:** the two extremes of the same mistake — ignoring growth until the rewrite is forced, and splitting the system "for scale" when no scaling requirement exists. Quiz 3 Q2 makes the second point: with "no scaling or release requirement that necessitates this split" and atomicity that "cannot be relaxed", the right call is to retain the current design until the proposed design demonstrates how atomicity is preserved.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Adding an index to speed up a slow query — which of the two scaling strategies is that?
<panel type="seamless" minimized header="%%Answer%%">
Optimizing the available resources — better use of existing capacity, no new copies (L12 slide 8).
</panel>

**Q2.** The room-booking team proposes splitting reservation and payment into separate databases "because independent databases are good practice in microservices", with no scaling or release requirement and non-negotiable atomicity. What is the best-supported decision?
<panel type="seamless" minimized header="%%Answer%%">
Retain the current design until the proposed design demonstrates how atomicity is preserved — there is no requirement that necessitates the split, and a database transaction currently enforces "both or neither" (Quiz 3 Q2).
</panel>

</panel>

<span id="W12-c4"></span>

### W12.4 Vertical vs horizontal scaling ★

**Scale up or scale out — the choice shapes everything that follows.** Vertical scaling adds capability to the machines a system is deployed on; horizontal scaling adds additional machines running copies of the service. (Source: L12 slide 3.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-12.md#def-vertical-scaling" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-12.md#def-horizontal-scaling" trim />
</box>

**Systems start small and monolithic, and that is fine — until it isn't.** A typical n-tiered web application hosted on a single server is a monolith, which grows in complexity as it becomes feature-rich; it is good enough while request loads stay relatively low. When the load grows, performance drops — latency increases because CPU and memory cannot handle concurrent requests — and the single server becomes the bottleneck. (Source: L12 slide 10.)

**Scale up: pay money, keep the architecture.** Upgrading the service hardware — e.g. from a t3.xlarge instance (4 CPU, 16 GB) to a t3.2xlarge (8 CPU, 32 GB) — is simple, money is the only cost, and larger workloads are supported seamlessly; but there are hard limits on how many CPUs and how much memory one machine can have. (Source: L12 slide 11.)

**Scale out: replicate the service and share the requests.** Run multiple copies on multiple nodes; with N replicas and R requests, each server processes ~R/N requests. This needs two more elements in the design: a load balancer and a session store. (Source: L12 slide 12.)

<box type="info" seamless>

**Scale up vs scale out — what each costs and what caps each:**

| | Scale up (vertical) | Scale out (horizontal) |
|---|---|---|
| You add | Capability to the machines you have (CPU, memory) | Machines running copies of the service |
| What caps it | The single machine's limits — there is a largest instance, and the box remains a single point of failure (L12 slide 11) | Nothing in the count — but every copy carries the whole system, so capacity spent on non-hot parts is wasted (AKF: "data sets have to be replicated in their entirety"; Quiz 3's ~5% modules), and it needs the W12.5 elements: load balancer + session store |

Whichever direction you pick, deciding it late is the expensive part — W12.3's downtime, hardware and redesign are the price of scaling post-hoc.

</box>

The diagram contrasts the two moves for the room-booking monolith.

<mermaid>
flowchart TB
  subgraph up["Scale up (slide 11)"]
    u1["Room-booking monolith<br>search + reservation + notification"] --> db1[("Bookings DB")]
    note1["bigger machine:<br>more CPU / memory"] -.-> u1
  end
  subgraph out["Scale out (slide 12)"]
    lb["Load balancer"] --> r1["Replica 1"]
    lb --> r2["Replica 2"]
    lb --> r3["Replica 3"]
  end
</mermaid>

%%Notation: a box is a deployed service copy, the cylinder is a data store, solid arrows are synchronous request flow, and the dashed arrow annotates the hardware upgrade. On the left there is still one (bigger) machine; on the right N replicas each handle ~R/N requests.%%

How to read it: the room-booking monolith can ride out summer on a bigger machine (scale up) — simple, but one box still caps both capacity and failure tolerance — or be replicated behind a load balancer (scale out), which grows capacity by adding boxes (Quiz 3 Q1's first option). The two elements that make the scale-out half actually work — the load balancer's routing and a shared session store for stateless replicas — are the subject of W12.5 below.

<box type="warning" seamless>

**Pitfall:** scaling out a *monolith* replicates its inefficiencies. The room-booking monolith is 90% search load; replicating the whole application behind a load balancer gives reservation and notification replicas they do not need — Quiz 3 marks it inferior to extracting search and scaling *its* instances (Quiz 3 Q1).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Your service runs on the largest instance your cloud offers and still falls over at peak. Which scaling direction is left, and what two design elements does it require?
<panel type="seamless" minimized header="%%Answer%%">
Horizontal scaling — there are limits on the CPU and memory you can add to one machine (L12 slide 11). It requires a load balancer and a session store (L12 slide 12).
</panel>

</panel>

<span id="W12-c5"></span>

### W12.5 Load balancing and stateless design ★

**Replicas are useless unless something spreads the work evenly — and services only share work if they carry no private state.** These two design elements are what make horizontal scaling actually work. (Source: L12 slides 12–14.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-12.md#def-load-balancing" trim />
</box>

**The load balancer is the single front door.** All user requests are sent to it; it chooses which service replica processes each request, aiming to keep each replica equally busy, and relays responses back to the client. Off-the-shelf solutions exist — e.g. Nginx, or cloud-provider load balancing such as AWS elastic load balancing. (Source: L12 slide 13; %%the LB-vs-proxy-vs-reverse-proxy comparison is marked non-examinable%%.)

**Effective balancing requires stateless services.** When a user accesses the application, the service creates a user session to track session state and the sequence of user interactions. But the load balancer sends consecutive requests from the same client to *different* service instances — so the API implementation must not retain state associated with an individual client's session. (Source: L12 slide 14.)

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-12.md#def-stateless-service" trim />
</box>

**Session state moves out of the service and into a session store.** Any service replica must be able to access the session state when it receives a request that is part of a user session — that is the session store's job. The payoff: **stateless services are cheap to replicate** (Source: L12 slide 14.)

<box type="info" seamless>

**Stateless vs stateful — one question: if this request lands on a replica that has never seen this client, can it be served?**

| | Stateful service | Stateless service |
|---|---|---|
| Where session state lives | Inside the instance (memory, local cache) | Outside the instance — the shared session store (or the client) |
| Are replicas interchangeable? | No — only the replica holding the state can serve that client's next request | Yes — any replica can serve any request |
| Effect on scaling out | The balancer cannot route freely; uneven state breaks the R/N evenness | Cheap to replicate — add or remove instances at will |

The failure mode is exactly self-check Q1's static variable: roles stored in one replica's memory make that replica the only one that can serve the client.

</box>

<mermaid>
flowchart LR
  u["Client"] -- "request 1, 2, 3..." --> lb["Load balancer"]
  lb --> s1["Search replica 1"]
  lb --> s2["Search replica 2"]
  lb --> s3["Search replica 3"]
  s1 -- "read/write session state" --> st[("Session store")]
  s2 -- "read/write session state" --> st
  s3 -- "read/write session state" --> st
</mermaid>

%%Notation: boxes are services, the cylinder is the shared session store, solid arrows are synchronous requests. Consecutive requests from one client may land on different replicas — which is exactly why session state cannot live inside a replica.%%

How to read it: the room-booking platform's search module, once extracted, scales by adding replicas behind a load balancer; because the search service keeps no per-client session state — the session store holds it — any replica can serve any request, and "increase its instances based on demand" becomes a configuration change, not a redesign (Quiz 3 Q1's correct option).

<box type="warning" seamless>

**Pitfall:** hiding state in the instance "just for convenience" — a login token in server memory, a shopping cart in a local cache. The next request may hit a different replica, and the balancer cannot keep replicas equally busy if some hold session state others lack (L12 slide 14). Note the echo from Week 6: REST's statelessness is the same design commitment at the protocol level.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** A teammate stores the logged-in user's roles in a static variable of the search service to "save a lookup". What breaks first when you scale out?
<panel type="seamless" minimized header="%%Answer%%">
Requests routed to other replicas cannot see that variable — the service is no longer stateless, so replicas are not interchangeable. Session state belongs in the shared session store (L12 slide 14).
</panel>

**Q2.** Why does the load balancer *want* to send consecutive requests from the same client to different instances?
<panel type="seamless" minimized header="%%Answer%%">
To keep each replica equally busy — even distribution is what makes R/N requests per replica (and the capacity math) hold (L12 slides 12–13).
</panel>

</panel>

<span id="W12-c6"></span>

### W12.6 Scaling the data tier ★★

**After you scale out the services, the shared database is the next bottleneck — a single database's capability limits response time.** Potential solutions: query the database infrequently by using caching, or scale out the database itself. (Source: L12 slide 15.)

**Caching keeps frequently read, rarely changed data out of the database's critical path.** A cache stores recently retrieved and commonly accessed database results in memory — e.g. Redis or Memcached — so future requests read from the cache instead. The processing logic changes: for frequently read data that changes rarely, check the distributed cache first and return immediately; on a miss, query the database, load the results into the cache, then return — and decide, based on the nature of the data, when to remove or invalidate cached results to prevent stale results. (Source: L12 slide 16.)

**Read replicas share the read load but not the write load.** Configure one or more nodes as read replicas of the main database: writes go only to the primary, and changes are asynchronously replicated to the secondaries — which may live in different regions to serve global clients. Scale-up alone eventually fails: the DB exceeds the processing capability of a single node, low-latency access is needed from clients spread around the globe, and a single node is a single point of failure. (Source: L12 slide 17.)

**Partitioning splits one logical table across several physical stores.** Horizontal partitioning splits a logical table into multiple physical partitions, allocating rows by a partitioning strategy — e.g. value-based or a hash of the primary key. Vertical partitioning partitions by columns — e.g. storing static, read-only data apart from dynamic data. (Source: L12 slide 18.)

<box type="info" seamless>

**"Vertical" and "horizontal" scale two different things in this chapter — the *machines* (W12.4) and the *table* (here).** The shared adjective is coincidental; the tell-apart question is: *one machine or many, or — if we are inside a table — rows or columns?*

| Phrase | Acts on | Splitting by | Course example |
|---|---|---|---|
| Vertical **scaling** (scale up) | The machines the system runs on | Nothing is split — one machine gets more capability | t3.xlarge → t3.2xlarge (W12.4) |
| Horizontal **scaling** (scale out) | The number of machines | Nothing is split — more machines run copies | Search replicas behind a load balancer (W12.5) |
| Horizontal **partitioning** | One logical table | Rows, allocated by a partitioning strategy (value, hash of the key) | Bookings table split by city — the scale cube's Z-axis (W12.8) |
| Vertical **partitioning** | One logical table | Columns (static/read-only vs dynamic data) | Room attributes stored apart from booking state (self-check Q1d) |

</box>

**Distributed databases add storage nodes and put up a single logical front.** Data is stored across multiple disks and queried by multiple database engines that present a unified face to the application, which also improves availability. (Source: L12 slides 19–20.)

The diagram shows the options layered onto the room-booking data tier.

<mermaid>
flowchart TB
  s["Search service"] -- "check cache" --> c[("Cache<br>(Redis)")]
  c -- "miss" --> pri[("Primary DB")]
  s -- "reads (listings, availability)" --> rr[("Read replica")]
  pri -- "async replication" --> rr
  subgraph partition["or partition by city (Z-axis)"]
    p1[("Bookings: city A–K")]
    p2[("Bookings: city L–Z")]
  end
  pri -. "or split the table (Z-axis)" .-> partition
</mermaid>

%%Notation: cylinders are data stores, solid arrows are synchronous reads/writes, and the dashed arrow marks an alternative restructuring. The cache answers repeat reads; the read replica absorbs read load; the partitions split the table by a key.%%

How to read it: the room-booking platform's search is read-heavy — exactly the case for a cache in front of the primary (slide 16) plus read replicas for the listing data (slide 17). If one database still limits response time, the listings table can be partitioned horizontally, e.g. by city (slide 18) — the Z-axis of the scale cube in W12.8.

{% call example("Search already has its own index (Quiz 3 Q1)") %}
The quiz notes that "search uses a separate indexing to make it efficient." That index is a data-tier scaling structure in miniature: the expensive read path (search) reads a purpose-built structure instead of hammering the primary tables — the same instinct as caching and partitioning, applied inside the application.
{% endcall %}

<box type="warning" seamless>

**Pitfall:** stale caches and write bottlenecks. A cache of data that changes often serves stale results unless invalidated (slide 16), and read replicas do not add write capacity — all writes still funnel to the primary, which is why the deck moves on to partitioning and distributed databases (slide 17–19).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Match each fix to its scaling mechanism: (a) Redis in front of the DB; (b) secondaries in another region; (c) bookings table split by hash of booking ID; (d) static room attributes stored separately from dynamic booking state.
<panel type="seamless" minimized header="%%Answer%%">
(a) caching — query the DB infrequently; (b) read replicas, asynchronously replicated to other regions; (c) horizontal partitioning (rows by partitioning strategy); (d) vertical partitioning (columns: static vs dynamic data) (L12 slides 16–18).
</panel>

**Q2.** Why don't read replicas help a write-heavy workload?
<panel type="seamless" minimized header="%%Answer%%">
Writes are only possible to the primary; secondaries receive changes by asynchronous replication. Replicas add read capacity and locality, not write capacity (L12 slide 17).
</panel>

</panel>

<span id="W12-c7"></span>

### W12.7 Multi-tier scaling, responsiveness, and fault isolation ★★★

**Replicate and cache at every tier, and the tiers can scale independently.** In a multi-tiered application, the service calls one or more dependent services that are each replicated and load-balanced — extending the stateless, load-balanced, cached architecture. Different tiers can serve different clients: e.g. separate replicas for web clients and mobile clients, each scaled independently depending on its load; all services use a core service that provides database access. A common variant is the backend-for-frontend (BFF) pattern — each frontend gets its own purpose-built backend tier (the web tier serving web clients, the mobile tier serving mobile clients), shaped for that client's needs and scaled on that client's load. (Source: L12 slides 20–21.)

<mermaid>
flowchart TB
  w["Web clients"] --> wlb["LB"] --> web["Web service replicas<br>(cached)"]
  m["Mobile clients"] --> mlb["LB"] --> mob["Mobile service replicas<br>(cached)"]
  web --> core["Core service<br>(DB access)"]
  mob --> core
  core --> db[("Database")]
</mermaid>

%%Notation: boxes are services (each set behind its own load balancer), the cylinder is the database, solid arrows are synchronous calls. Each client-facing tier is its own scaling unit; only the core service touches the database.%%

How to read it: the room-booking platform could serve web and mobile searchers through separate load-balanced tiers — mobile search bursts scale the mobile tier without touching reservation — while both tiers share one core service that owns database access (L12 slides 20–21).

**Queues buy responsiveness: acknowledge fast, persist later.** Using caching or messaging brokers, a service can respond without fully persisting in the database — e.g. an address update at checkout time should be persisted, but checkout should not be stalled. Event data is sent to the service, which acknowledges receipt and concurrently stores the data in a remote queue for subsequent writing to the database — writing to the queue is faster than writing to the DB. (Source: L12 slide 22 — this is Week 11's messaging doing scalability work.)

**Swim lanes contain failures the way partitions contain data.** A swim lane (or pod) architecture places a group of services within a boundary so that any failure within the boundary is contained and not propagated outside it. %%Here "pod" is the scalability literature's term (AKF, the slide's cited source) for such a fault-isolated grouping of services — often a customer segment, as in the scale cube's Z-axis shards; it is not the Kubernetes pod object.%% Advantages: easy fault detection within the lane, fault isolation, meeting region-specific requirements, and faster response times from a customer-specific perspective. (Source: L12 slide 23.)

<box type="warning" seamless>

**Pitfall:** queue-based responsiveness trades durability semantics for latency — the write is acknowledged before it is persisted in the database, so the queue becomes critical state that must itself be reliable (L12 slide 22).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Mobile search traffic triples while web traffic is flat. Which multi-tier design decision pays off, and which pattern is the common variant?
<panel type="seamless" minimized header="%%Answer%%">
Separate load-balanced replicas per client type — each tier scales independently depending on its load; the common variant is backend-for-frontend (L12 slides 20–21).
</panel>

**Q2.** Checkout must not stall, but the address change must not be lost either. What does the deck prescribe?
<panel type="seamless" minimized header="%%Answer%%">
Acknowledge the update immediately and store it in a remote queue for subsequent writing to the database — writing to the queue is faster than writing to the DB (L12 slide 22).
</panel>

</panel>

<span id="W12-c8"></span>

### W12.8 The scale cube ★★★

**Every strategy in this chapter is one move on a three-axis cube — and the axes compose.** Each axis is a specific strategy of scaling (Source: L12 slide 24):

* **X-axis — horizontal scaling:** run multiple copies of the application behind a load balancer (W12.4–W12.5).
* **Y-axis — functional decomposition:** split the application into multiple different functions/services (the modular monolith → microservices move of Weeks 4 and 7).
* **Z-axis — data partitioning:** run the same code on a subset of the data, distributing data storage — e.g. segment by customer category or geography (W12.6).

<box type="info" seamless>

**Tell the three axes apart with one question: after the move, what code runs on what data?**

| Axis | You add… | So the pieces run… | What it costs | Room-booking example |
|---|---|---|---|---|
| **X — replicate** | Identical copies of the *same* code, behind a load balancer (the load balancing of W12.5) | The same code on the *whole* data set, in every copy | Every copy carries everything — replicas on non-hot parts are wasted (Quiz 3: reservation/notification copies get ~5% load each) | Three monolith copies behind a balancer |
| **Y — decompose** | New boundaries: the application is split into different functions/services | *Different* code, each part on its own data (AKF: "dissimilar things" split along noun/verb boundaries) | Distributed-systems work — and the cut must follow domain lines (Weeks 4, 7–8) | Extract search, reservation, notification as services |
| **Z — partition data** | Nothing to the code — each shard runs the *same* code on a *subset* of the data | The same code on less data per node | Shards must balance; cross-shard queries get harder (W12.6) | Listings table partitioned by city |

Load balancing itself is not an axis — it is the mechanism that makes X-axis replication usable.

</box>

<mermaid>
flowchart TD
  o["Room-booking platform<br>(modular monolith)"]
  o -- "X: replicate" --> x["N monolith copies<br>behind a load balancer"]
  o -- "Y: decompose" --> y["Search · Reservation · Notification<br>as independent services"]
  y -- "X: replicate one service" --> yx["Search instances scaled<br>on demand (Quiz 3 answer)"]
  o -- "Z: partition data" --> z["Same code, subset of data:<br>listings by city / region"]
</mermaid>

%%Notation: the starting box is the system; each labelled arrow is one axis of the scale cube; solid arrows show composition — axes are applied on top of each other.%%

How to read it: from the room-booking monolith you can go out along X (replicate everything), along Y (extract search, reservation, notification as services), or along Z (partition the listings data). Quiz 3's correct answer is **Y then X**: extract search as an independent microservice — the module consuming 80% of resources, which already has its own indexing — and increase *its* instances based on demand, keeping capital and operational costs low because only the hot module is replicated. The wrong answers are also on the cube: replicating the whole application is X without Y (wasted replicas), and moving search to a larger machine is scale-up (capped, single point of failure).

<box type="info" seamless>

**Why this closes the course arc:** Y-axis decomposition is precisely the monolith → modular monolith → microservices story of Weeks 4–7; X-axis replication is this week's load balancing; Z-axis partitioning is the data-tier scaling of W12.6. One cube ties architecture and scalability together.
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Classify on the cube: (a) three copies of the reservation service behind an LB; (b) bookings sharded by customer region; (c) splitting the monolith into search/reservation/notification services.
<panel type="seamless" minimized header="%%Answer%%">
(a) X-axis — horizontal copies behind a load balancer; (b) Z-axis — same code on a subset of data, segmented by geography; (c) Y-axis — functional decomposition (L12 slide 24).
</panel>

**Q2.** Quiz 3 Q1 asks for the change that handles summer load "while keeping the capital expenditure and operational costs low". Which cube path is that, and why do the alternatives cost more?
<panel type="seamless" minimized header="%%Answer%%">
Y then X: extract search as an independent microservice and increase its instances based on demand. Replicating the whole monolith (X alone) pays for reservation/notification replicas that use ~5% each; a larger machine for search (scale-up) hits hardware limits and keeps a single point of failure; extracting the *small* modules leaves search — the actual bottleneck — un-scaled (Quiz 3 Q1).
</panel>

</panel>

<box type="info" seamless>

##### Section summary

* **Scalability is a measurable quality attribute** with growth dimensions — request rate, data volume, stable response times — and load that rises *and* falls (W12.1).
* **Percentiles (P50/P95/P99) turn "slow" into a number**, locate the bottleneck, and are what service-level objectives are written against (W12.2).
* **Replicate or optimize — and decide early**: post-hoc scaling costs downtime, hardware and redesign, so scalability is an architectural decision from the beginning (W12.3).
* **Scale up is simple but capped; scale out is uncapped but needs a load balancer and stateless services** with a shared session store (W12.4–W12.5).
* **Then scale the data tier** — cache, read replicas, partition, distribute — and compose all of it on the scale cube (W12.6–W12.8).
</box>

</div>

## Key terms

| Term | Definition | Unit |
|---|---|---|
| Scalability | Handling a growing amount of work by adding resources, while response times stay stable | [W12.1](#W12-c1) |
| Vertical scaling (scale up) | Adding capability (CPU, memory) to the machines the system runs on | [W12.4](#W12-c4) |
| Horizontal scaling (scale out) | Adding machines running copies of the service; each handles ~R/N requests | [W12.4](#W12-c4) |
| Load balancing | A front door that chooses which replica processes each request, keeping replicas equally busy | [W12.5](#W12-c5) |
| Stateless service | A service retaining no per-client session state, so any replica can serve any request | [W12.5](#W12-c5) |
| Session store | Shared storage of session state accessible from every replica | [W12.5](#W12-c5) |
| Caching | Keeping recently retrieved, commonly accessed results in memory to spare the database | [W12.6](#W12-c6) |
| Read replica | A secondary node receiving asynchronously replicated changes; reads only | [W12.6](#W12-c6) |
| Partitioning | Splitting a logical table across physical stores — horizontally by rows, vertically by columns | [W12.6](#W12-c6) |
| Swim lane / pod | A boundary grouping services so failures inside do not propagate outside | [W12.7](#W12-c7) |
| Scale cube | X = replicate copies, Y = functional decomposition, Z = data partitioning | [W12.8](#W12-c8) |

## Connections

| Concept | Lecture deck | Tutorial | Other weeks / quizzes |
|---|---|---|---|
| Scalability as a quality attribute | L12 slides 3, 4–6 | — | W3 (NFRs, trade-offs); W6 (REST statelessness) |
| Percentiles and SLOs | L12 slide 7 | — | Errand platform (L4/Tutorial 2) |
| Replicate vs optimize; early decisions | L12 slides 8–9 | — | Quiz 3 Q2 (don't split without a scaling requirement) |
| Scale up vs scale out | L12 slides 10–12 | — | Quiz 3 Q1 options |
| Load balancer, session store, stateless design | L12 slides 12–14 | — | W6 (REST stateless); W5 (cloud-native autoscaling) |
| Data-tier scaling: cache, replicas, partitioning, distributed DB | L12 slides 15–20 | — | Quiz 3 Q1 (search's separate indexing) |
| Multi-tier scaling, BFF, queue-based responsiveness | L12 slides 20–22 | — | W11 (queues, consumers); W7 (services) |
| Swim lanes / fault isolation | L12 slide 23 | — | W5 (cloud regions) |
| Scale cube | L12 slide 24 | — | Quiz 3 Q1 (Y + X); W4 (modular monolith); W7 (microservices) |

## Summary

**Key takeaways:**

* **Scalability means handling growth in requests, data and response-time stability by adding resources** — and load varies, so scale down too (W12.1).
* **P50/P95/P99 make performance measurable** and tell you where the bottleneck is before you spend on it (W12.2).
* **Replicating and optimizing are the two levers**, and scaling late costs downtime and redesign — decide architecturally, early (W12.3).
* **Vertical scaling buys a bigger box; horizontal scaling buys N boxes** — plus a load balancer and a session store (W12.4).
* **Stateless services behind a load balancer are cheap to replicate** because session state lives in the session store (W12.5).
* **The data tier scales by caching, read replicas, partitioning and distributed databases** — each fixing a different limit (W12.6).
* **Tiers, queues and swim lanes compose the same ideas**, and the scale cube summarizes every move (W12.7–W12.8).

**Key terms:** see the table above — each row links back to the unit that introduces the term.

%%Next: this is the last technical topic — Week 13 recaps the whole course and maps it to the four quizzes. See [Week 13 — Course Recap]({{baseUrl}}/se-book-adapted/chapters/week-13-course-recap.html).%%

## Further reading

* Vertical scaling vs horizontal scaling — <https://www.cockroachlabs.com/blog/vertical-scaling-vs-horizontal-scaling/> (L12 slide 3)
* Scale cube — <https://akfpartners.com/growth-blog/scale-cube> (L12 slide 24)
* Fault isolation (swim lanes) — <https://akfpartners.com/growth-blog/fault-isolation-swim-lane> (L12 slide 23)
