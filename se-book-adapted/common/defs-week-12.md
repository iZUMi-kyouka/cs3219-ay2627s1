{# Definitions for week-12. Owned by the agent populating this week.
   Each definition lives in its own anchored span; chapters include it:
   <box type="definition" seamless><include src="common/defs-week-12.md#def-<term>" trim /></box>
   se-book phrasing: short, testable, no filler. Cite the course source where applicable. #}

<span id="def-scalability">

**Scalability** is the property of a system to handle a growing amount of work by adding resources to the system. The growth may be in requests processed per time window or in the amount of data managed, while response times stay stable and consistent.

(Sources: L12 slides 4–6; recap of L3, slide 3.)

</span>

<span id="def-vertical-scaling">

**Vertical scaling (scale up)** adds capability to the machines a system is deployed on — e.g. more CPU or memory on the same node — without adding more nodes. It is simple but capped by the hardware limits of a single machine.

(Sources: L12 slides 3, 11.)

</span>

<span id="def-horizontal-scaling">

**Horizontal scaling (scale out)** adds additional machines (nodes) running copies of the service, so that requests are distributed across the replicas. With N replicas and R requests, each server processes about R/N requests.

(Sources: L12 slides 3, 12.)

</span>

<span id="def-load-balancing">

**Load balancing** sends all user requests to a component that chooses which service replica will process each request — aiming to keep every replica equally busy — and relays the responses back to the clients.

(Sources: L12 slide 13.)

</span>

<span id="def-stateless-service">

**Stateless service** is a service whose API implementation retains no state associated with an individual client's session, so any replica can process any request. Session state is kept in a shared session store that every replica can access, which is what makes stateless services cheap to replicate.

(Sources: L12 slide 14.)

</span>

<span id="def-autoscaling">

**Autoscaling** — automatically growing or shrinking a system's capacity on a metric (e.g., CPU usage, queue length) so capacity follows the load up *and* down — load is not constant (a streaming service at 9 pm faces far more load than at 5 am).

(Sources: L12 slide 6.)

</span>

<span id="def-percentile">

**Percentile** (P50/P95/P99) — a point on the response-time distribution: P50 (the median) is a typical user's experience; P95 means 95% of requests are faster than this number — a standard threshold for service-level objectives; P99 captures the worst-case scenarios. Response time is a distribution, not a number.

(Sources: L12 slide 7.)

</span>

<span id="def-service-level-objective">

**Service-level objective (SLO)** — a measurable target for a service level that a team commits to, typically written on percentile response times held over a window — e.g., 95% of successful browse errand requests complete in under 200 ms in a 7-day window.

An SLO is the *internal* target a team commits to; a **service-level agreement (SLA)** is the *contractual* promise made to a customer. The lecture's requirements are SLOs — "SLA" is not the deck's word for them.

(Sources: L12 slide 7.)

</span>

<span id="def-tail-latency">

**Tail latency** — the response times of the slowest few percent of requests, beyond the P95/P99 thresholds. The users at the tail are the ones who notice, which is why service-level objectives are written on tail percentiles rather than on the average.

(Sources: L12 slide 7.)

</span>

<span id="def-bottleneck">

**Bottleneck** — the slowest shared component that limits the whole system's response time or throughput (e.g., the single overloaded server, the one database every replica shares). Measure first, then plan the scaling strategy — scaling the wrong component buys nothing.

(Sources: L12 slides 7, 10, 15; Quiz 3 Q1.)

</span>

<span id="def-replicating-resources">

**Replicating resources** — the scaling strategy of adding copies of what you have to provide more capacity to handle requests, increasing throughput. One of the two levers; the other is optimizing the available resources.

(Sources: L12 slide 8.)

</span>

<span id="def-optimizing-resources">

**Optimizing the available resources** — the scaling strategy of getting more out of the same hardware: more efficient algorithms, extra indices to speed up queries, rewriting a server in a faster programming language (e.g., Facebook developed HipHop, a compiler for PHP).

(Sources: L12 slide 8.)

</span>

<span id="def-throughput">

**Throughput** — the amount of work a system processes per unit time (e.g., requests per second); replicating resources to add capacity increases it.

(Sources: L12 slide 8.)

</span>

<span id="def-single-point-of-failure">

**Single point of failure** — a component whose failure takes the whole system down because no replica can take over (e.g., the single machine of scale-up, the single primary database). Horizontal scaling and read replicas exist to remove it.

(Sources: L12 slides 11, 17.)

</span>

<span id="def-session-store">

**Session store** — shared storage holding users' session state, accessible from every service replica. Because the load balancer sends consecutive requests from the same client to different instances, session state must live here rather than inside any replica.

(Sources: L12 slide 14.)

</span>

<span id="def-caching">

**Caching** — storing recently retrieved and commonly accessed database results in memory (e.g., Redis, Memcached) so future requests read from the cache instead of placing a burden on the database: check the distributed cache first and return immediately; on a miss, query the database, load the results into the cache, then return — and decide, based on the nature of the data, when to remove or invalidate cached results to prevent stale ones.

(Sources: L12 slide 16.)

</span>

<span id="def-read-replica">

**Read replica** — a secondary database node that receives changes from the primary by asynchronous replication and serves reads (possibly from other regions, to support global clients). Writes go only to the primary, so replicas add read capacity and locality — not write capacity.

(Sources: L12 slide 17.)

</span>

<span id="def-partitioning">

**Partitioning** (sharding) — splitting one logical table across several physical stores: horizontal partitioning allocates rows to partitions by a partitioning strategy (e.g., value-based, a hash of the primary key); vertical partitioning partitions by columns (e.g., static read-only data apart from dynamic data). Each partition — shard — runs the same code on a subset of the data.

(Sources: L12 slides 18, 24.)

</span>

<span id="def-distributed-database">

**Distributed database** — a database scaled by adding storage nodes: data is stored across multiple disks and queried by multiple database engines that put up a logical unified front to the application; it also improves availability.

(Sources: L12 slides 19–20.)

</span>

<span id="def-backend-for-frontend">

**Backend-for-frontend (BFF)** — a multi-tier scaling variant in which each frontend gets its own purpose-built backend tier (the web tier serving web clients, the mobile tier serving mobile clients), shaped for that client's needs and scaled on that client's load; all tiers use a core service that provides database access.

(Sources: L12 slide 21.)

</span>

<span id="def-swim-lane">

**Swim lane** (pod) — a boundary placing a group of services so that any failure within the boundary is contained and not propagated outside it. Advantages: easy fault detection within the lane, fault isolation, meeting region-specific requirements, faster customer-specific response. (The scalability literature's term — not a Kubernetes pod.)

(Sources: L12 slide 23.)

</span>

<span id="def-scale-cube">

**Scale cube** — the three-axis summary of scaling strategies: **X-axis** — horizontal scaling, running multiple copies of the application behind a load balancer; **Y-axis** — functional decomposition, splitting the application into multiple different functions/services; **Z-axis** — running the same code on a subset of the data (data partitioning, e.g., segmented by customer category or geography). The axes compose.

(Sources: L12 slide 24.)

</span>
