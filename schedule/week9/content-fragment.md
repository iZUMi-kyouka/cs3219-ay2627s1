<span id="summary">

**What if services stopped calling each other and simply announced what happened?** The lecture defines the event (four views), distinguishes initiating from derived events and events from commands and queries, explains fire-and-forget asynchronous communication and its trade-offs, then assembles event-driven architecture: producers, event broker, consumers — and the event-driven microservices that result, including how event brokers store and order events.

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

**Asynchronous communication is fire-and-forget: fire the event, forget about waiting.** The sender doesn't wait for a response nor care whether receivers are up — the opposite of synchronous communication's must-wait rule. Gains: responsiveness, availability. Cost: more complex/fragmented error handling. Events remove temporal and identity/location coupling but add coupling on the event format. Slides 12–18 → [W9.2]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c2)

**EDA is the architecture that results: decoupled applications communicating asynchronously by issuing and consuming events via an event broker.** Producers publish, the broker holds and routes by topic, consumers subscribe and act; location and identity transparency throughout (slides 20–24). Compared with microservices: EDA is async-first, treats bounded contexts as nice-to-have (foundational for microservices), and processes *events* — what happened — rather than *requests* — what needs to happen (slides 25–27). → [W9.3]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c3)

**Event-driven microservices are the hybrid: microservice boundaries plus event wiring.** A service that accepts an order, validates it, applies payment, and adjusts inventory is acceptable in EDA but violates single responsibility in microservice architecture; split it, give each service its own data, wire by events (slides 29–31). Each event stream has exactly one producing owner; consumers read input streams and produce output streams (slide 32). → [W9.4]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c4)

**The event broker is a store as much as a pipe: an immutable, append-only, ordered log with offsets, partitions, retention, and replay.** Consumers track their offset per partition and read sequentially; immutability means corrections are new events; partitions enable parallel scaling (slides 33–40). The balance sheet (slide 41): performance, scalability, maintainability, evolvability, fault tolerance — against complexity and test effort. Events wear two hats: notification (trigger action) and replication (copy data) (slides 42–43). → [W9.4]({{baseUrl}}/se-book-adapted/chapters/week-09-event-driven-architecture.html#W9-c4)

</span>

<span id="tutorial-summary">

**Tutorial 6 runs the full discovery pipeline:** deriving subdomains, bounded contexts, and aggregates for a bank-account system (applying W8.1), then event-storming a monolithic food-delivery platform into microservices (applying W8.1 + W9.1).

</span>

<span id="tutorial">

### Tutorial 6

**What it practises:** DDD decomposition — subdomains and bounded contexts from requirements, then a domain model with aggregates (Q1) — and event storming as the bridge from a monolith's events to microservice candidates (Q2).

**Q1 — Bank account system.** Requirements: (1) a customer can register with full name, phone number, NRIC; (2) deposit funds; (3) withdraw funds; (4) close an account only if the balance is zero; (5) no withdrawing more than existing funds; (6) bank managers can get account details; (7) bank managers can get customer details.

**I.** Define the sub-domains and bounded contexts.
<panel type="seamless" minimized header="%%Answer%%">**Customer management** subdomain (type: supporting — or generic with good reasoning): registers and maintains customer details (full name, phone, NRIC) and provides customer details to bank managers — solves requirements 1 and 7; its ideal bounded context is the *customer management context*. **Bank account management** subdomain (type: **core**): opens accounts, deposits and withdraws funds, maintains balances, closes accounts, and provides account details to managers — solves requirements 1–6; its ideal bounded context is the *bank account management context*. (One student team framed the domain as "Bank Account Management" with these two subdomains — also accepted with reasoning.)</panel>

**II.** Design the domain model with aggregates (any notation).
<panel type="seamless" minimized header="%%Answer%%">Two aggregates: **Customer** (aggregate root: Customer; objects: customerID, name, phone, identity; actions: register, get details) and **Bank Account** (aggregate root: Bank Account; objects: accountID, customerID, balance, status; actions: open, deposit, withdraw, close, get details). Compare your diagram with the model solution PDF.</panel>

**Q2 — Event-storming a food-delivery monolith.** The platform covers user accounts, restaurant listings, placing food orders, payments, and managing deliveries. Your team has already brainstormed the events (step 1 of event storming). Continue: identify **commands, policies, aggregates, and bounded contexts**, and present the microservices that result.
<panel type="seamless" minimized header="%%Answer sketch%%">Work the W9.1 stages in order: (1) events — already brainstormed (e.g., order placed, payment made, food ready, order picked up, order delivered); (2) commands that cause them (place order, make payment, mark ready, assign courier…) and the policies that react ("when payment made then notify restaurant"); (3) aggregates the commands act on (Order, Payment, Restaurant, Delivery, User); (4) draw a bounded context around each cohesive cluster — the clusters *are* your microservice candidates (Accounts, Restaurants, Ordering, Payments, Delivery). The model solution shows the diagram at each stage; compare your team's whiteboard pass against it.</panel>

**Materials:**

* %%Tutorial sheet (PDF kept offline)%%
* %%Model solution (PDF kept offline)%%

</span>
