{% from "schedule/macros-fragment.md" import term, example with context %}
<span id="summary">

**What happens when load grows — and how do we design for it *before* it does?** L12 treats scalability as a quality attribute (recapping L3), then walks the levers: measuring scale with percentiles, replicating vs optimizing, vertical vs horizontal scaling, load balancing and stateless design, scaling the data tier (caching, read replicas, partitioning, distributed databases), multi-tier scaling and swim lanes — summarized by the scale cube.

</span>

<span id="toc">

* [W12.1 Scalability as a quality attribute]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c1)
* [W12.2 Measuring scale: percentiles and bottlenecks]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c2)
* [W12.3 Two strategies to scale — and why late scaling hurts]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c3)
* [W12.4 Vertical vs horizontal scaling]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c4)
* [W12.5 Load balancing and stateless design]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c5)
* [W12.6 Scaling the data tier]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c6)
* [W12.7 Multi-tier scaling, responsiveness, and fault isolation]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c7)
* [W12.8 The scale cube]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c8)

</span>

<span id="lecture">

### Lecture

**Scalability is the property of a system to handle a growing amount of work by adding resources — and "growth" has dimensions.** Requests per time window, data volume, and stable response times; load is not constant (a streaming service at 9 pm vs 5 am), so autoscaling must scale *down* as well as up (slides 3–6). → Chapter unit [W12.1]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c1).

**Response time is a distribution, and percentiles are how you specify it.** P50 = typical experience, P95 = the standard {{ term("service-level-objective", "a measurable target for a service level, e.g. a percentile response time held over a window — defined in W12.2") }} threshold, P99 = worst case; e.g. "95% of successful browse errand requests complete in <200 ms" (slide 7). → [W12.2]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c2).

**Two strategies: replicate resources for throughput, or optimize what you have.** And scaling post-hoc is expensive — downtime, hardware, rewrites — so scalability is an architectural decision incorporated from the beginning (slides 8–9). → [W12.3]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c3).

**Systems start as single-server monoliths, which are fine until request load grows.** Then either scale up — a bigger instance, simple but capped — or scale out — N replicas each handling ~R/N requests, which requires a load balancer and a session store (slides 10–12). → [W12.4]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c4).

**The load balancer keeps replicas equally busy; stateless services make that possible.** Because consecutive requests from one client hit different instances, session state must live in a shared session store — stateless services are cheap to replicate (slides 13–14). → [W12.5]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c5).

**After the services, the database is the bottleneck.** Cache frequently read data (Redis/Memcached), add read replicas with asynchronous replication, partition tables horizontally (by key) or vertically (static vs dynamic columns), or move to distributed databases (slides 15–20). → [W12.6]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c6).

**Scale processing with multiple tiers, and buy responsiveness with queues.** Separate load-balanced, cached tiers per client type (the {{ term("BFF", "backend-for-frontend: each frontend gets its own purpose-built, separately scaled backend tier — defined in W12.7") }} variant), a core service owning DB access; acknowledge writes into a queue and persist afterwards, since writing to a queue is faster than writing to the DB (slides 20–22). → [W12.7]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c7).

**Swim lanes (pods) contain failures inside a boundary** — easier fault detection, fault isolation, region-specific requirements, faster customer-specific response (slide 23). → [W12.7]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c7).

**The scale cube compresses everything: X = copies behind a balancer, Y = functional decomposition, Z = data partitioning.** The axes compose — and Quiz 3's room-booking answer is Y (extract search) then X (scale its instances on demand) (slide 24). → [W12.8]({{baseUrl}}/se-book-adapted/chapters/week-12-scalability.html#W12-c8).

<box type="tip" seamless>

**Deck structure at a glance:**

- Slide 3: recap from L3
- 4–9: what scalability is and why early planning matters
- 10–15: scale up/scale out and the stateless design
- 16–20: caching and database scaling
- 21–23: multi-tier, responsiveness, swim lanes
- 24: the scale cube

The exam-focused slide list for this deck is short — slides 3–24 (L13 study guide).
</box>

</span>

<span id="tutorial-summary">

**Tutorial 9 revises Weeks 10–11, not L12**: it classifies interactions on the three async-communication dimensions (Q1), compares content-based routing with pub-sub + message filters (Q2), composes splitter/router/aggregator for a multi-item order (Q3), and works through dead-letter queues (Q4) — applying [W11.3–W11.4]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#core-concepts) and [W10]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#core-concepts).

</span>

<span id="tutorial">

### Tutorial 9

Work the tasks in order — reveal each answer only after attempting it. Concepts used: [W10.1–W10.2]({{baseUrl}}/se-book-adapted/chapters/week-10-asynchronous-communication.html#core-concepts), [W11.3]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c3), [W11.4]({{baseUrl}}/se-book-adapted/chapters/week-11-messaging.html#W11-c4).

<panel type="seamless" header="## %%[Task 1]%% **Classify three interactions on the async-communication taxonomy**">

**Given (Tutorial 9 Q1).** For each scenario: (i) categorise it into all THREE dimensions from the L10 taxonomy; (ii) explain the classification; (iii) what happens if a receiver is unavailable when communication occurs? (iv) identify an anti-pattern amongst the three and justify.

* **A.** A distributed database leader receives a write command. The leader thread blocks while sending the log entry to multiple replica nodes. It waits until most node disks confirm they have written the entry before unblocking and acknowledging success to the client.
* **B.** A user submits login credentials to an authentication service and waits for the response.
* **C.** A live chat application broadcasts typing indicators to multiple connected users. Offline subscribers miss these updates.

<panel type="seamless" minimized header="%%Answer (teaching team suggestions)%%">

| Scenario | Synchrony | Persistence | Cardinality |
|---|---|---|---|
| A | Synchronous — the leader blocks until most replicas confirm the write | Persistent — the entry is stored and can be delivered to replicas that are temporarily offline | Multiple receivers — one leader to many replica nodes |
| B | Synchronous — the client waits for the response | Transient — the request is not stored for future delivery | Single receiver — the authentication service |
| C | Asynchronous — the publisher does not wait for subscribers | Transient — updates are not stored for later delivery | Multiple receivers — broadcast to many subscribers |

**If a receiver is unavailable:**

- **A** — the entry remains stored and reaches the replica when it reconnects (if too many replicas are down, the leader stays blocked and the write eventually fails).
- **B** — the request fails or times out and the client must retry.
- **C** — unavailable subscribers simply miss the update, so it is not delivered retrospectively.

**Anti-pattern:** A's blocking synchronous multicast — the sender's progress is coupled to multiple receivers, giving higher latency and lower throughput. (In a distributed database this trade-off may be justified by consistency requirements.)

</panel>
</panel>

<panel type="seamless" header="## %%[Task 2]%% **Who controls the routing logic?**">

**Given (Tutorial 9 Q2).** Fill in the table comparing a Content-Based Router with Pub-Sub + Message Filter:

| Aspect | Content-Based Router | Pub-Sub + Message Filter |
|---|---|---|
| Who controls the routing logic? | ? | ? |
| When a new consumer joins, what changes? | ? | ? |
| Example use case | ? | ? |

<panel type="seamless" minimized header="%%Answer (teaching team suggestions)%%">

| Aspect | Content-Based Router | Pub-Sub + Message Filter |
|---|---|---|
| Who controls the routing logic? | A centralized routing component inspects message content and decides where to send it | Each subscriber defines its own filter; routing is distributed and reactive |
| When a new consumer joins, what changes? | The router's configuration must be updated to include the new route or condition | No change to the publisher — the new subscriber just subscribes and applies a filter |
| Example use case | Business transactions, e.g. order messages routed to the correct department | Event notifications, e.g. a logging service subscribing only to error events |

</panel>
</panel>

<panel type="seamless" header="## %%[Task 3]%% **Route a multi-item order to the right inventories**">

**Given (Tutorial 9 Q3).** You are building part of an e-commerce system that takes orders and updates the respective inventories. An order arrives with multiple items. Design a message flow so that each item is processed by the correct inventory system and the results are recombined into a single confirmation — identifying the messaging pattern at each stage (e.g. scatter-gather, splitter, aggregator, router) and drawing the diagram.

<panel type="seamless" minimized header="%%Answer (teaching team model solution)%%">

One possible solution — splitter, then content-based router, then aggregator:

1. **Message splitter** — takes one order message with multiple items and splits it into multiple order-item messages; each item may be processed separately.
2. **Content-based router** — routes each order item to the apt inventory system based on the item's type or location.
3. **Message aggregator** — collects the responses (e.g. *item confirmed* / *item out of stock*) from all inventory systems; once all parts are received, combines them into a single Order Confirmation message.

<mermaid>
flowchart TB
  o["New order (N items)"] -.-> ch1[["NEW_ORDER"]]
  ch1 -.-> sp["Splitter<br>(one message per item)"]
  sp -.-> cbr["Content-based router<br>(route on item category)"]
  cbr -.-> w["Widget inventory"]
  cbr -.-> g["Gadget inventory"]
  cbr -.-> inv[["Invalid items<br>(unknown category)"]]
  w -.-> ag["Aggregator<br>(correlate by order ID)"]
  g -.-> ag
  ag -.-> out[["Order confirmation<br>(INVENTORY_STATUS)"]]
</mermaid>

%%Notation: boxes are pattern components or systems, parallelograms are channels, dashed arrows are asynchronous messages.%% One composite order fans out per item, is routed per category, and the per-item results are correlated back into one confirmation — giving parallel message processing and reliable order-level confirmation (same shape as L11 slide 49).

</panel>
</panel>

<panel type="seamless" header="## %%[Task 4]%% **Dead-letter queues**">

**Given (Tutorial 9 Q4).** What is a dead letter queue (DLQ) and why do systems like Amazon SQS use it? In what scenarios might you redrive messages from the DLQ? How do you detect or handle "stuck" or repeatedly failing messages?

<panel type="seamless" minimized header="%%Answer (teaching team suggestions)%%">

* **What:** a special queue storing messages that could not be successfully processed or delivered — it prevents repeated retries from blocking or crashing the system, and supports fault tolerance by isolating potentially problematic messages.
* **How it works (SQS):** when a consumer retrieves a message it becomes invisible for a timeout period; if the consumer crashes or fails to delete the message, it reappears and the receive count increases; after exceeding the configured retry limit, the message moves to the DLQ.
* **When to redrive:** after identifying and resolving the cause of failure — e.g. a consumer bug or a temporary dependency outage — messages can be redriven from the DLQ back to the source queue.
* **How to detect failing/stuck messages:** monitor DLQ size and message counts; use message properties (e.g. retry count) and logs to track failure frequency; alert on DLQ trends; for a stuck message check consumer logs, receive count and visibility timeout, fix the cause, then retry.

</panel>
</panel>

**Materials:**

* %%Tutorial sheet (PDF kept offline)%%
* %%Model solution (PDF kept offline)%%

</span>
