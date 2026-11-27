{% from "schedule/macros-fragment.md" import term with context %}
<span id="summary">

**What if services stopped calling each other and simply announced what happened?** The lecture defines the event (four views), distinguishes initiating from derived events and events from commands and queries, explains fire-and-forget asynchronous communication and its trade-offs, then assembles event-driven architecture: producers, event broker, consumers — and the event-driven microservices that result, including how event brokers store and order events. The material was delivered in two recordings: the main lecture (slides 2–18) and companion recorded videos (slides 19–43).

</span>

<span id="toc">

* [W9.1 Events: the four views]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c1)
* [W9.2 Fire-and-forget asynchronous communication]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c2)
* [W9.3 Event-driven architecture]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c3)
* [W9.4 Event-driven microservices]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c4)

</span>

<span id="lecture">

### Lecture

**The lecture opens with one clarification you should carry all week: CQRS doesn't always need events or event sourcing — they are just mostly used together.** Slide 2. → [W9.1]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c1)

**An event is a fact — anything that happens within the business system — and it doubles as data and as a means of asynchronous communication.** Receiving an invoice, booking a room, pushing a commit. The deck then shows the **four views of an event**: event storming (discover microservices), event sourcing (reconstruct state by replaying), CQRS (separate write/read models), and the content pair — event notification ("something happened", small data) vs event-carried state transfer (the event carries the data consumers need). Slides 4–6 → [W9.1]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c1)

**Every process has one initiating event and a cascade of derived ones.** An initiating event originates from an end user and kicks off the business process; a derived event is broadcast by a component reacting within the scope of that initiating event — Quiz 4 Q2's `RequestSubmitted` → `EligibilityConfirmed` → `EquipmentReserved` chain is exactly this. Slides 7–8 → [W9.1]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c1)

**Intent separates the three communication kinds: command (imperative, to a specific receiver), event (past-tense fact, broadcast), query (asks state, needs a reply).** Quiz 4 Q1 makes the point stick: a message named `EquipmentReserved` that expects the receiver to check availability and reserve is a command mislabeled as an event — redesign it as `ReserveEquipment` + a post-success `EquipmentReserved`. Slide 9 → [W9.1]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c1)

**Events are key–value pairs, and their payload size is a design decision.** Unkeyed, entity, and keyed events (slide 10); the FoC `DeliveryConfirmed` event keyed by `errandId` serves four consumers with different data needs — credit transfer, notifications, rating prompts, dashboards (slide 11). → [W9.1]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c1)

**Asynchronous communication is fire-and-forget: fire the event, forget about waiting.** The sender doesn't wait for a response nor care whether receivers are up — the opposite of synchronous communication's must-wait rule. The recording quantified the gain (600 ms + 1200 ms of waiting becomes an immediate acknowledgement) and named the cost twice over: fragmented error handling, and the "both sides forget" failure mode that motivates the broker (L9 recording, ~[44:00]–[48:00]). Compensation actions fired as events close the loop — a saga riding on choreography (L9 recording, ~[52:00]). Gains: responsiveness, availability. Cost: more complex/fragmented error handling. Events remove temporal and identity/location coupling but add coupling on the event format and the intermediary. Slides 12–18 → [W9.2]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c2)

**EDA is the architecture that results: decoupled applications communicating asynchronously by issuing and consuming events via an event broker.** Producers publish, the broker holds and routes by {{ term("topic", "a broker channel enabling one-to-many communication: every subscriber receives the message — defined in W10.3") }}, consumers subscribe and act; location and identity transparency throughout (slides 20–24). The recorded videos add the analogy — EDA is the observer pattern applied across a network through a broker — and the data-ownership picture: the basket service updates its own store from the catalog's `PriceUpdated` event, never the catalog's database (L9 recorded videos, ~[04:00]–[05:00]). Compared with microservices: EDA is async-first, treats bounded contexts as nice-to-have (foundational for microservices), and processes *events* — what happened — rather than *requests* — what needs to happen (slides 25–27; the design test: are you announcing a fact or asking for work? L9 recorded videos, ~[07:00]). → [W9.3]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c3)

**Event-driven microservices are the hybrid: microservice boundaries plus event wiring.** A service that accepts an order, validates it, applies payment, and adjusts inventory is acceptable in EDA but violates single responsibility in microservice architecture; split it, give each service its own data, wire by events (slides 29–31). The recorded videos run the review explicitly — event wiring present, cohesion violated (payment and inventory inside order submission), data ownership violated (email service reading its database) — so the design is *not* yet event-driven microservices until the split (L9 recorded videos, ~[07:00]–[08:30]). Each event stream has exactly one producing owner; consumers read input streams and produce output streams (slide 32). → [W9.4]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c4)

**The event broker is a store as much as a pipe: an immutable, append-only, ordered log with offsets, partitions, retention, and replay.**
- Consumers track their {{ term("offset", "the index-ID of the last event read in a partition; consumers scan sequentially from it — defined in W9.4") }} per {{ term("partition", "an append-only substream of a stream, strictly ordered within — defined in W9.4") }} and read sequentially — a stopped consumer resumes from its offset, tracked at the consumer-group level so two members never process the same event (L9 recorded videos, ~[13:00])
- Immutability means corrections are new events
- Partitions enable parallel scaling — no global sequence to coordinate, and the broker buffers traffic spikes so producers keep publishing while consumers are slow (L9 recorded videos, ~[14:00]–[14:30])
- A retained log is not a work queue: reading never removes an event, where a queue deletes on acknowledgement (L9 recorded videos, ~[12:00])

(slides 33–43, delivered in the companion recorded videos)

The balance sheet (slide 41): performance, scalability, maintainability, evolvability, fault tolerance — against complexity and test effort. Events wear two hats: notification (trigger action) and replication (copy data) — the payment service consuming `OrderPlaced` and publishing `PaymentSucceeded`/`PaymentFailed` is the recorded worked example (L9 recorded videos, ~[16:00]) (slides 42–43). → [W9.4]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c4)

</span>

<span id="tutorial-summary">

**Tutorial 6 runs the full discovery pipeline:** deriving subdomains, bounded contexts, and aggregates for a bank-account system (applying W8.1), then event-storming a monolithic food-delivery platform into microservices (applying W8.1 + W9.1).

</span>

<span id="tutorial">

### Tutorial 6

**What it practises:** DDD decomposition — subdomains and bounded contexts from requirements, then a domain model with aggregates (Q1) — and event storming as the bridge from a monolith's events to microservice candidates (Q2).

**Q1 — Bank account system.** Requirements: (1) a customer can register with full name, phone number, NRIC; (2) deposit funds; (3) withdraw funds; (4) close an account only if the balance is zero; (5) no withdrawing more than existing funds; (6) bank managers can get account details; (7) bank managers can get customer details.

**I.** Define the sub-domains and bounded contexts.
<panel type="seamless" minimized header="%%Answer%%">**Customer management** subdomain (type: supporting — or generic with good reasoning; the DDD types are *core* = the capability that differentiates the business, *supporting* = needed for the business but not differentiating, *generic* = commodity functionality such as identity or email — Quiz 3 Q4 uses the same core/supporting distinction): registers and maintains customer details (full name, phone, NRIC) and provides customer details to bank managers — solves requirements 1 and 7; its ideal bounded context is the *customer management context*. **Bank account management** subdomain (type: **core**): opens accounts, deposits and withdraws funds, maintains balances, closes accounts, and provides account details to managers — solves requirements 1–6; its ideal bounded context is the *bank account management context*. (One student team framed the domain as "Bank Account Management" with these two subdomains — also accepted with reasoning.)</panel>

**II.** Design the domain model with aggregates (any notation).
<panel type="seamless" minimized header="%%Answer%%">Two aggregates: **Customer** (aggregate root: Customer; objects: customerID, name, phone, identity; actions: register, get details) and **Bank Account** (aggregate root: Bank Account; objects: accountID, customerID, balance, status; actions: open, deposit, withdraw, close, get details). Compare your diagram with the model solution PDF.</panel>

**Q2 — Event-storming a food-delivery monolith.** The platform covers user accounts, restaurant listings, placing food orders, payments, and managing deliveries. Your team has already brainstormed the events (step 1 of event storming). Continue: identify **commands, policies, aggregates, and bounded contexts**, and present the microservices that result.
<panel type="seamless" minimized header="%%Answer sketch%%">Work the W9.1 stages in order: (1) events — already brainstormed (e.g., order placed, payment made, food ready, order picked up, order delivered); (2) commands that cause them (place order, make payment, mark ready, assign courier…) and the policies that react ("when payment made then notify restaurant"); (3) aggregates the commands act on (Order, Payment, Restaurant, Delivery, User); (4) draw a bounded context around each cohesive cluster — the clusters *are* your microservice candidates (Accounts, Restaurants, Ordering, Payments, Delivery). The model solution shows the diagram at each stage; compare your team's whiteboard pass against it.</panel>

**Materials:**

* %%Tutorial sheet (PDF kept offline)%%
* %%Model solution (PDF kept offline)%%

</span>
