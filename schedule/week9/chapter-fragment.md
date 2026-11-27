{% from "schedule/macros-fragment.md" import term, example with context %}
<h2>Week 9 — Event-Driven Architecture</h2>

<span>

Builds on **Weeks 7–8** — the microservice style, DDD and event storming, and event sourcing and CQRS — and on the communication styles previewed in [W8.4]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c4). Tutorial 6 exercises both the Week 8 DDD toolkit and this week's event thinking.
</span>

<span>

* **Can** explain what an event is, its four views, and how initiating events differ from derived events and from commands and queries.
* **Can** reason about fire-and-forget communication — what it decouples, what it costs, and when the trade-off is worth it.
* **Can** describe the components of event-driven architecture and contrast EDA with microservice architecture.
* **Can** design event-driven microservices using event-stream semantics — ownership, ordering, partitioning, replay — and weigh their trade-offs.
</span>

<div>

<box type="important" seamless>

**Revision priority:** ★ = core; ★★ = supporting detail; ★★★ = extension; ★★★★ = optional context.
</box>

**This week swaps requests for announcements.** Instead of service A calling service B and waiting, A publishes a record of what happened and whoever cares reacts. The lecture builds that idea in four steps: what events are (slides 4–11), how fire-and-forget communication works and what it costs (slides 12–18), what event-driven architecture is (slides 19–27), and how microservices communicate purely through events (slides 28–43). Source for the whole chapter unless stated otherwise: L9 slides.

## Core concepts

<span id="W9-c1"></span>

### W9.1 Events: the four views ★

**Everything in this week — and much of the next — hangs off one small idea: a recorded fact.** Get clear on what an event is and is not, and the rest of event-driven design follows.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-event" trim />
</box>

**An event is anything that happens within the business system, and it is both data and a means of asynchronous communication.** %%("Message" is avoided here on purpose: Week 10 defines a *message* as a related but distinct construct — a request to be executed — and separates the two by intent.)%% Receiving an invoice, booking a room, creating an employee record, pushing a commit — each is a fact that other components may want to know about; events are how the software passes that information along (slide 6).

**The deck organizes the uses of events into four views.** The same event artifact plays different roles depending on which question you are asking of it (slide 5, from Fowler's *Event-driven* article).

<mermaid>
flowchart TB
    EV["One event artifact"] --> V1["Discovery view:<br/>event storming — use events to<br/>discover microservices"]
    EV --> V2["Storage view:<br/>event sourcing — reconstruct state<br/>by replaying events"]
    EV --> V3["Structure view:<br/>CQRS — separate models<br/>for writes and reads"]
    EV --> V4["Content view:<br/>notification vs event-carried<br/>state transfer — how much data it carries"]
</mermaid>

%%Notation: the central box is the single event concept; each branch is one *view* — a role the event plays in design, not a different kind of object.%%

How to read it: the first three branches recycle Week 8's material — event storming discovered your service candidates ([W8.1]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c1)), and event sourcing and CQRS restructured your storage ([W8.3]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c3)). The last branch is this week's new question: *how much data should one event carry?* The two content-side answers get their own definitions below.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-event-notification" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-event-carried-state-transfer" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-event-sourcing" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-cqrs" trim />
</box>

<box type="info" seamless>

**Telling apart — event notification vs event-carried state transfer.** One distinguishing question: **how much data rides on the event — just enough to know you must ask, or enough to act without asking?**

| | Event notification | Event-carried state transfer |
|---|---|---|
| Payload | Small: an ID and the fact that something happened (Fowler: "often just some id information and a link back to the sender that can be queried for more information") | The data consumers need, so they "don't need to contact the source system" (Fowler) |
| Consumers | Must call the producer back for details | Work from the event itself |
| Cost | Every consumer adds a callback (and a dependency on the source being up) | Bigger events, more copies of data in flight |
| Course example | The thin `EquipmentCheckedOut` of Quiz 4 Q3 — checkout ID only; when the laboratory API is down, consumers *receive* the event but *cannot process it* | The fat `DeliveryConfirmed` of slide 11, if it carried requestor, courier, credit amount, names, and zone — all four consumers served without a callback |

The FoC table in this unit shows why no single event is perfect: Credit, Notification, Rating, and Analytics need different fields, so payload size is a per-event design decision, not a global style.

</box>

#### Initiating and derived events

**Every business process starts with one event and cascades into many.** Distinguishing the two kinds keeps the cascade readable (slides 7–8).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-initiating-event" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-derived-event" trim />
</box>

<box type="info" seamless>

**Telling apart — initiating vs derived event.** One distinguishing question: **did this fact originate from an end user's action, or from a service reacting inside that process?** The producer's identity is irrelevant — a derived event can come from any service, as long as it was generated *in response to* an initiating event, within the scope of that one process.

| | Initiating event | Derived event |
|---|---|---|
| Origin | An end user's action | A component's reaction to a previous event |
| Role | Kicks off the business process | Cascades the process onward |
| Course example | `RequestSubmitted` (student submits the equipment request, Quiz 4 Q2); FoC's `ErrandPosted` (L8 slide 4) | `EligibilityConfirmed`, `EquipmentReserved` (Quiz 4 Q2); FoC's `CreditReserved` (L8 slide 4) |

Quiz 4 Q2's trap is exactly here: `EligibilityConfirmed` is produced by a *different service* (Eligibility), but because it answers the user's `RequestSubmitted`, it is derived — "the trigger, not the producer", decides.

</box>

The diagram below draws the cascade slide 7 annotates: one initiating event from an end user kicks everything off, and every event after it is derived — triggered by the event before it. The chain, not the single event, is the structural heart of EDA.

<mermaid>
flowchart TB
    U(["Customer places<br/>an order (end user)"]) -->|"places order"| E1("Order Submitted<br/>initiating event")
    E1 -.-> OPS["Order Placement<br/>Service"]
    OPS -.->|"derived"| E2("Order Placed")
    E2 -.-> PS["Payment Service"]
    PS -.->|"derived"| E3("Credit Card Expired")
    E3 -.-> NS["Email Notification<br/>Service"]
    PS -.->|"derived"| E4("Payment Applied")
    E4 -.-> FS["Order Fulfillment<br/>Service"]
</mermaid>

%%Notation: rounded boxes are events, rectangles are services, and the stadium is the end user; the solid arrow is the end-user action that originates the initiating event; every dashed arrow is an asynchronous event — dashed out of a service emits a derived event, dashed into a service is that event being consumed.%%

How to read it: slide 7's annotations say it directly — "this is the initiating event that kicks everything off" (Order Submitted, from the customer's action) and "these are derived events triggered by the Order Submitted initiating event". Walk the chain: the Order Placement service reacts to Order Submitted by emitting Order Placed; Payment reacts and emits the things "that can possibly happen in the Payment service" — Credit Card Expired (routed to the Email Notification service) or Payment Applied (routed to Order Fulfillment). The slide's third annotation is the architecture lesson: "services can respond to an event and in turn trigger more events". Read against the course example: FoC's `ErrandPosted` is the initiating event and `CreditReserved` a derived one (L8 slide 4) — and the Quiz 4 Q2 workflow below is the same shape, one initiating event followed by derived ones.

{% call example("Quiz 4 Q2 — an equipment-request workflow") %}
A student submits an equipment request: the Request Intake service records it and publishes `RequestSubmitted`. The Eligibility service consumes that event, checks the student's training record, and publishes `EligibilityConfirmed`. Reservation then allocates equipment and publishes `EquipmentReserved`. Here `RequestSubmitted` is the **initiating event** (it comes from the end user and kicks off the process), while `EligibilityConfirmed` and `EquipmentReserved` are **derived events** — each service reacted within the scope of that one initiating event. (Source: Quiz 4, Question 2.)
{% endcall %}

#### Event, command, or query?

**Three kinds of communication travel between services, and confusing them is a design bug.** The difference is *intent* (slide 9).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-command" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-query" trim />
</box>

| | Command | Event | Query |
|---|---|---|---|
| What it is | Intent, imperative | Fact, past tense | Asks for current state |
| Example | `ChargeCard` | `CardCharged` | `GetBalance` |
| Addressing | Sent to a specific receiver | Broadcast by its owner — the service that produced the fact and owns that event stream (W9.4); others can only react to it | Needs a reply |
| State change | Changes state, returns no data | Records a state change that already happened | Changes nothing |
| Reply expected? | No data comes back — the sender wants *action*, not a value | None — others can only react to it | Yes — the reply is the whole point |

{% call example("Quiz 4 Q1 — redesigning the EquipmentReserved message") %}
A university equipment platform sends a message named `EquipmentReserved` to the Reservation service, which is expected to check availability and either reserve the equipment or reject the request. That is a command wearing an event's name: the sender wants an *action*, not announcing a *fact*. The correct redesign: use a `ReserveEquipment` **command** for the request, and let Reservation publish `EquipmentReserved` only **after** a reservation succeeds — a past-tense fact broadcast by its owner. (Source: Quiz 4, Question 1.)
{% endcall %}

#### Inside an event: keys and payloads

**An event is a key–value pair: the key identifies and routes, the value carries the details.** The key supports identification, routing, and aggregation on the unique ID %%aggregation: grouping or counting all events that carry the same ID, e.g. "how many times was this book opened?"%%; the value holds the complete details of the event (slide 10).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-event-key" trim />
</box>

**Events come in three structural types.** (Source: L9 slide 10.)

* **Unkeyed** — a singular statement of fact with no key. E.g., "user opened a book" on a digital book platform (key `NA`; value: ISBN — the book's International Standard Book Number — plus a timestamp). Aggregate these click events per item and sort, and you have "today's top products" on an e-commerce site or "number one in Singapore this week" on a streaming service — no user login required (L9 recording, ~[27:00]).
* **Entity** — describes the properties and state of an entity, keyed on that entity's unique ID; it provides a continual history of the entity's state and can materialize it — materialize: reconstruct the entity's current state by replaying its events, giving you a working "current" copy without ever storing one. E.g., key `ISBN=372719`, value: author and other properties.
* **Keyed** — carries a key but does not represent an entity; it partitions the stream to guarantee data locality within a partition %%data locality: every event with the same key lands in the same partition, so a consumer working on that key reads all its events together, in order%%. E.g., key `ISBN=372719`, value: `UserID=AE2341G` (a borrowing activity event).

{% call example("L9 recording ~[30:00] — the key decides which question the stream can answer") %}
The same ride-hailing platform (Quiz 2's Grab-like app) can key its car events two ways, and each choice enables a different capability. Keyed by **trip ID**, all events of one journey land together: when a taxi breaks down mid-trip, the platform knows the trip's last recorded location and can fire a compensation action — send a replacement car to those coordinates and continue the ride to the destination. Keyed by **locality** instead ("car entered Clementi"), all events about one area land together: counting arrivals reveals how crowded each zone is, feeding demand sensing and dynamic pricing. Either way the key guarantees data locality within a partition — which key you choose decides what the locality is *about*. (Source: L9 recording, ~[29:00]–[31:00]; ride-hailing context from Quiz 2.)
{% endcall %}

**How much data an event should carry is a design decision with four consumers in mind.** The deck's FoC scenario: a courier delivers an errand, the requestor confirms it, and the Order Service publishes `DeliveryConfirmed`, keyed by `errandId` — then four services consume it, each needing different fields (slide 11):

| Consumer | What it needs |
|---|---|
| Credit Service | Requestor, courier, credit amount — to transfer reserved credits |
| Notification Service | Both users' names and devices — to send "Delivered" pushes |
| Rating Service | Errand ID and the two users — to prompt a rating |
| Analytics | Vendor, pickup zone, timestamps — for delivery-time dashboards |

**One event cannot be perfectly shaped for all four.** A notification-style event (IDs only) forces consumers back to the source for details; event-carried state transfer bloats every event but removes the callback. Choose per event, guided by what consumers must do with it.

**The lecture workshop-tested the shapes against exactly this event.** Walking the FoC scenario in class (L9 recording, ~[38:00]–[41:00]):

* **A thin event re-couples consumers at runtime.** Holding only `errandId`, the Credit service must call the Order service to learn who requested, then the User service for who that is — a chain of runtime queries just to act.
* **A fat event couples every consumer to the producer's format — and leaks data.** Change the payload and all four consumers break at once; worse, courier and requestor details now travel to services that never needed them — a security and privacy exposure.
* **The middle shape — IDs of the relevant entities — is usually the sweet spot.** Carrying `errandId`, requester ID, courier ID, vendor ID, and the reserved credit amount, each consumer queries only the one service that owns what it still needs (the User service) instead of walking the Order-to-User chain.

<box type="warning" seamless>

**Pitfall — a too-thin event turns async communication back into sync.** Quiz 4 Q3: a laboratory publishes `EquipmentCheckedOut` containing only the checkout ID; every consumer must immediately call the laboratory API for details and wait for the data. During a laboratory API outage, consumers *receive* the events but *cannot process them* — the durable broker (persistent storage, per the gloss in W9.2) does not help, because the missing dependency is the callback, not the transport. (Source: Quiz 4, Question 3.)
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Name the four views of an event and the design question each answers.
<panel type="seamless" minimized header="%%Answer%%">Event storming — which services should exist? Event sourcing — where does state live? CQRS — how do writes and reads stay separate? Event notification vs event-carried state transfer — how much data does one event carry? (L9 slide 5.)</panel>

**Q2.** In Quiz 4 Q2's workflow, why is `EligibilityConfirmed` not an initiating event even though a *different service* produced it?
<panel type="seamless" minimized header="%%Answer%%">Initiating vs derived is about the trigger, not the producer: `EligibilityConfirmed` was generated in response to the user's `RequestSubmitted` event, within the scope of that initiating event — so it is derived (Quiz 4 Q2; L9 slides 7–8).</panel>

**Q3.** `ReserveEquipment` vs `EquipmentReserved` — which is the command, and why does the distinction matter?
<panel type="seamless" minimized header="%%Answer%%">`ReserveEquipment` is the command: imperative intent, sent to a specific receiver, demanding an action. `EquipmentReserved` is an event: a past-tense fact broadcast only after the action succeeded. Sending an event named like a done deal but *expecting* the receiver to act conflates the two — Quiz 4 Q1's bug.</panel>

**Q4.** In the lecture's three-minute task, which `DeliveryConfirmed` shape did the class settle on, and what was the reasoning?
<panel type="seamless" minimized header="%%Answer%%">The middle shape: `errandId` plus the IDs of the relevant entities (requester, courier, vendor) and the reserved credit amount. Reasoning in coupling terms: it avoids the thin event's chain of runtime callbacks while escaping the fat event's format coupling and personal-data exposure, and any remaining detail comes from the single service that owns it. (asked in lecture; L9 recording, ~[38:00])</panel>

</panel>

<span id="W9-c2"></span>

### W9.2 Fire-and-forget asynchronous communication ★

**The moment a producer waits for its consumers, it inherits every one of their failures.** Fire-and-forget is the communication style that makes the event cascade of W9.1 possible.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-fire-and-forget" trim />
</box>

**Two communication styles cover every inter-component exchange.** In *synchronous* communication, a component that sends information must wait for a response from the receiver before doing anything else. In *fire-and-forget* communication, the event is sent — the fire part — and the service moves on to other things — the forget part (slide 13).

**The payoff is responsiveness and availability — and the recording put numbers on both.** Order placement takes ~600 ms and payment ~1200 ms: wired synchronously the user waits ~1800 ms, while an event-wired system acknowledges as soon as the request is logged (L9 recording, ~[45:00]). **The response that gets faster is the one *about* the request — the time to *complete* the whole workflow is unchanged.** The mechanism behind the gain is thread release: a sender that does not wait frees its thread — in a traditional web app, capacity for another request (L9 recording, ~[44:00]). And availability improves because the sender does not care whether the other components are up: consumers that are temporarily down simply process later (slide 15) — whereas in a synchronous chain a dead payment service leaves the caller blocked and availability collapses (L9 recording, ~[46:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-temporal-decoupling" trim />
</box>

{% call example("Quiz 4 Q4 — uploads during a transcoding outage") %}
A media platform durably records uploaded files %%durable: written to persistent storage that survives a crash or restart, unlike data held only in memory%% and publishes `UploadAccepted` to an available broker that retains events for seven days. The Transcoding service goes down for 20 minutes; upload acceptance does not require transcoding to finish. Because communication is fire-and-forget and the broker retains events, the platform **continues accepting uploads**, and Transcoding processes the retained events after recovery — temporal decoupling doing its job. (Source: Quiz 4, Question 4.)
{% endcall %}

**The price is error handling.** In a synchronous call, the caller learns of failure immediately and can react; with fire-and-forget, error handling becomes more complex and fragmented than in sync communication — failures surface later, in different places, per consumer (slide 16).

**The user still expects to hear the outcome, and that is extra machinery.** With fire-and-forget, someone must still tell the user the card was charged and the order went through — which can take extra monitoring, or even a dedicated service that collates each user's status (L9 recording, ~[48:00]).

**The "forget" half has a failure mode of its own: both sides forget.** If the payment service is down when the event fires, the producer has already moved on and nothing catches the event — the information is simply lost (L9 recording, ~[45:00]). ==This gap is exactly what the event broker exists to close==: an intermediary that holds events until consumers return restores the reliability that pure fire-and-forget gives up (W9.3, W9.4).

{% call example("L9 recording ~[52:00] — out of stock after payment: compensation as events") %}
One item left; you order it, pay, and only at fulfillment does the system discover another customer's order consumed the stock — the Lazada-style scenario the lecturer walked through. A synchronous design would have caught this at the inventory check, but the event-driven design has already moved on — so the recovery also travels as events: either a refund event reverses the payment, or a back-order event holds the charge and completes when stock arrives, with the customer kept notified throughout. The lecturer's point: these alternative paths are baked into the events themselves, and choreography (W8.4) runs them — a saga (W8.2) executing over an event cascade, ending in a reasonably compensated state: money refunded, or product delivered a little late. (Source: L9 recording, ~[50:00]–[55:00].)
{% endcall %}

**Know exactly what events decouple — and what they do not.** (Source: L9 slide 17.)

* **Removed: temporal coupling.** Producer and consumer don't need to be up at the same time. (This is the distributed-systems sense — *not* Week 4's temporal-coupling code smell, where unrelated actions are bundled because they run at the same time.)
* **Removed: coupling on identity/location.** The producer doesn't know who listens or where they are — less reliance on service discovery.
* **Added: coupling on the event format.** Every consumer depends on the event's field names and meaning — change the event schema and you must consider every subscriber.
* **Added: coupling on the intermediary.** The broker that holds producer and consumer together is itself a shared dependency — both sides now depend on its availability and behavior (L9 recording, ~[50:00]).

**The net effect is not the elimination of coupling but its relocation.** Coupling spread across every call site is traded for coupling concentrated in two reviewable places — the event format and the intermediary (L9 recording, ~[50:00]).

%%Qualification flagged (L9 recording, ~[50:00]): the lecturer corrected his own wording from "removed" to "reduced" — temporal coupling is gone only while an intermediary holds the events. Slide 17 says "removed"; read it as *removed, given a broker*.%%

The diagram contrasts the two styles on the FoC errand flow — the async half is slide 11's `DeliveryConfirmed` publish; the sync half is the reserve-credits exchange of W8.2's errand workflow (Tutorial 7 Q1).

<mermaid>
sequenceDiagram
    participant U as Requestor
    participant O as Order service
    participant C as Credit service
    participant N as Notification service
    Note over U,N: Synchronous — sender must wait
    U->>O: Create errand
    O->>C: Reserve credits (wait)
    C-->>O: Credits reserved
    O-->>U: Errand created
    Note over U,N: Fire-and-forget — sender moves on
    O--)N: DeliveryConfirmed (event)
    Note over O,N: no reply is sent — none is expected (the "forget" part)
</mermaid>

%%Notation: in sequence diagrams a solid arrow (`->>`) is a synchronous call and its dashed counterpart (`-->>`) the awaited reply; `--)` is an asynchronous event sent without expecting a reply; the two notes spanning all four participants mark where each style begins.%%

How to read it: above the first note — the Order service cannot create the errand until Credit answers, so a Credit outage stalls the requestor. Below the second — Order publishes `DeliveryConfirmed` and immediately moves on; Notification processes it whenever it can, exactly the fire-and-forget contract of slide 13.

<box type="warning" seamless>

**Trade-off — responsiveness and availability are bought with complexity.** You accept fragmented error handling (slide 16) and event-format coupling (slide 17) in exchange for temporal and location decoupling. Quiz 4's Q10 adds the boundary: persistence protects pending work, but a *deadline* also needs enough availability and processing capacity — async is not a throughput guarantee. (Sources: L9 slides 14–17; Quiz 4 Q10.)
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** A producer's events reach consumers through a durable broker. The producer is torn down and restarted between events. Which coupling is this architecture free of?
<panel type="seamless" minimized header="%%Answer%%">Temporal coupling — producer and consumer don't need to be up at the same time (L9 slide 17).</panel>

**Q2.** You rename a field in a widely consumed event. Which coupling does this violate, and why didn't it exist in a synchronous design?
<panel type="seamless" minimized header="%%Answer%%">Event-format coupling: every consumer depends on the field names and meaning. In a request–reply design the *contract* also exists (API schema), but the deck's point is that with events the coupling is to the published format while identity/location coupling disappears (L9 slide 17).</panel>

**Q3.** True or false: fire-and-forget improves availability because the broker guarantees every consumer processes every event quickly.
<panel type="seamless" minimized header="%%Answer%%">False. Fire-and-forget improves *sender-side* availability — the sender doesn't wait and doesn't care if receivers are up (slide 15). It makes no timeliness promise for consumers; Quiz 4 Q10 shows a deadline can still be missed without capacity.</panel>

**Q4.** In slide 12's synchronous chain, the email notification service goes down after payment succeeded. Should the order die? What does the answer reveal about synchronous wiring?
<panel type="seamless" minimized header="%%Answer%%">No — the payment is real, and the customer must not be left in limbo because a notification service failed. Yet a synchronous chain makes that the default outcome: every downstream step sits on the caller's response path, so any late-stage failure either cancels completed work or blocks the caller. The lecturer used exactly this scenario to motivate moving the cascade onto events. (asked in lecture; L9 recording, ~[10:00])</panel>

</panel>

<span id="W9-c3"></span>

### W9.3 Event-driven architecture ★

**EDA is what you get when every conversation in the system becomes an event.** One definition, three component roles, and a comparison against the microservice architecture you already know.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-event-driven-architecture" trim />
</box>

**How it works:**

* **An action triggers producer components to deliver event data to something listening for it.** Event data is made available as soon as the action happens (slide 20).
* **A consumer subscribes to events of interest and takes an appropriate action on receiving one.** (Slide 20.)
* **EDA relies on asynchronous communication for sending and receiving events.** (Slide 20.)
* **Remember the deck's three-part characterization of events (slide 20):**
  * Events are data that describe some action or fact.
  * Events are notifications of some change in state or data.
  * Events are recordings of what happened.

**If the shape feels familiar, that is because it is the observer pattern at system scale.** A change in the observable generates a notification, and interested observers react — here the "observables" are loosely coupled services publishing through a broker across a network, instead of objects notifying each other in memory (L9 recorded videos, ~[04:00]). One consequence carries over unchanged: **publishing an event does not mean the resulting work is finished** — the producer does not wait for every consumer to process it.

**Three component roles make up an EDA.** (Source: L9 slide 21.)

* **Event producers** (event generators) publish data onto streams %%an *event stream* is the producer-owned, append-only event feed defined in W9.4%% or {{ term("queues", "broker channels that buffer messages for a single receiver, first-in-first-out — defined in W10.3") }}.
* **The event broker** implements the transport between them.
* **Event consumers** (event listeners) listen to and consume the event data.
* **Producers and consumers are decoupled from each other:** producers do not know which consumers are listening; consumers are decoupled from each other too — location and identity transparency. **Neither side needs the other's identity or network location, so services can be added, removed, or relocated without touching the opposite side** (L9 recorded videos, ~[04:00]).

%%Connection (L9 recording, ~[05:00]): choreography (W8.4) needed exactly this mechanism — services that each know their own job, coordinating through events rather than a central brain.%%

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-event-broker" trim />
</box>

<panel type="seamless" minimized header="%%What is loose coupling?%%">

<include src="../../se-book-adapted/common/defs-week-07.md#def-loose-coupling" trim />

</panel>

**The broker's job is to receive, publish on {{ term("topics", "broker channels enabling one-to-many communication: every subscriber of the topic receives the message — defined in W10.3") }}, and enable subscriptions.** It receives source data, publishes it on source-specific topics, and enables listeners to subscribe to topics of interest — and note what the deck points at: the *database-per-service pattern* reappears here, since each producer owns the data it publishes (slide 22).

{% call example("L9 recorded videos ~[05:00] — the event respects the data-ownership boundary") %}
The catalog receives an `UpdatePrice` command, updates **its own** database, and publishes `PriceUpdated`; the basket service consumes the event and updates the prices it holds **in its own store**. The basket learns of the change through the event — it never reads or writes the catalog's database — which is what keeps each service the sole owner of its data while they still exchange information through the broker rather than calling each other. (Source: L9 recorded videos, ~[05:00]; the database-per-service pattern from W8.2.)
{% endcall %}

<panel type="seamless" minimized header="%%What is the database-per-service pattern?%%">

<include src="../../se-book-adapted/common/defs-week-08.md#def-database-per-service" trim />

</panel>

**Pub/sub is the standard realization of EDA structure.** Event producers are publishers, event consumers are subscribers — e.g., {{ term("Kafka", "a distributed event-streaming platform: an immutable, partitioned, replayable log behind topics, treated fully in W10.3") }} pub/sub (slide 24).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-pub-sub" trim />
</box>

The diagram assembles the roles around the FoC `DeliveryConfirmed` event from slide 11.

<mermaid>
flowchart LR
    O["Order service<br/>(producer)"] -.->|"publishes<br/>DeliveryConfirmed"| B(("Event broker"))
    B -.->|"DeliveryConfirmed"| C["Credit service<br/>(consumer)"]
    B -.->|"DeliveryConfirmed"| N["Notification service<br/>(consumer)"]
    B -.->|"DeliveryConfirmed"| R["Rating service<br/>(consumer)"]
    B -.->|"DeliveryConfirmed"| A["Analytics<br/>(consumer)"]
</mermaid>

%%Notation: a rectangle is a service, the circle is the event broker, and every dashed arrow carries the same event — publish once, deliver to each subscriber.%%

How to read it: the Order service neither knows nor cares that four consumers exist; each consumer subscribed to the topic and reacts in its own way — transfer credits, push notifications, prompt a rating, update dashboards. Adding a fifth consumer means one new subscription, zero changes to the producer (L9 slides 11, 21).

#### EDA vs microservice architecture

**The two are different axes, and the deck compares them on three.** (Source: L9 slides 25–27.)

* **Communication and performance.** EDA relies on asynchronous communication — fast response to senders; microservices often communicate synchronously (occasionally asynchronously), and synchronous communication creates latency that slows the system (slide 25).
* **Bounded contexts and data ownership.** Foundational for microservices; nice-to-have for EDA (slide 26).
* **Event vs request processing.** EDA is built on event processing — responding to something that *has happened*, in turn triggering more events; microservices are built on request processing — responding to something that *needs to happen*, like a command or request (slide 27). **The recorded videos give the design test behind the axis: when designing an interaction, ask whether you are announcing a fact or asking for work to be done — the answer decides event vs command** (L9 recorded videos, ~[07:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-latency" trim />
</box>

The same three axes, side by side:

| Axis | EDA | Microservice architecture |
|---|---|---|
| Communication & performance | Asynchronous — fast response to senders (slide 25) | Often synchronous, occasionally asynchronous — sync calls create latency that slows the system (slide 25) |
| Bounded contexts & data ownership | Nice-to-have (slide 26) | Foundational (slide 26) |
| What is processed | Events — something that *has happened*, triggering more events (slide 27) | Requests — something that *needs to happen*, like a command or request (slide 27) |

%%Dimmed aside (se-book): the price of the event cascade is traceability — to answer "what happens when an invoice is deleted?" you may have to find several handlers, with no single place in the code telling you.%%

Two qualifications from the recorded videos sharpen the deck's comparison:

* **"Fast response" belongs to the sender — total workflow time is unchanged.** Asynchronous communication lets the sender continue sooner, but the full workflow still takes the work it takes — the deck's latency row is about the caller's path, not end-to-end completion (L9 recorded videos, ~[05:00]).
* **Event-driven does not outlaw synchronous calls.** Request–reply interactions coexist with event-driven ones — slide 25 contrasts the two styles' *defaults*, it does not prohibit synchronous calls where they fit (L9 recorded videos, ~[10:00]).

<box type="warning" seamless>

**Pitfall — "async" is not a substitute for boundaries.** Because bounded contexts are only a nice-to-have in EDA, an event-driven system designed without them can drift into services that publish whatever anyone might need. Keep the Week 8 discipline even when the wiring is events (L9 slide 26).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** A teammate claims your system is microservices *and* EDA because services communicate by events. Which comparison tells you to check further?
<panel type="seamless" minimized header="%%Answer%%">Bounded contexts and data ownership — foundational for microservices, nice-to-have for EDA (slide 26). Verify each service owns a bounded context and its data; otherwise you have async wiring without microservice boundaries.</panel>

**Q2.** In EDA, what does a consumer need to know about a producer? And the reverse?
<panel type="seamless" minimized header="%%Answer%%">Neither knows the other: producers don't know which consumers listen; consumers know only the topics they subscribe to — location and identity transparency via the broker (slide 21).</panel>

**Q3.** "Microservices respond to requests; EDA responds to facts." Unpack that against slide 27.
<panel type="seamless" minimized header="%%Answer%%">Microservice architecture is built on request processing — a command/request arrives and the service processes what *needs to happen*. EDA is built on event processing — a service reacts to what *has happened* and may trigger further events (slide 27).</panel>

**Q4.** Your team goes event-driven, and a teammate proposes deleting the services' REST endpoints because "EDA is asynchronous". What does the recorded lecture say?
<panel type="seamless" minimized header="%%Answer%%">Don't. Event-driven communication coexists with synchronous request–reply — synchronous calls remain appropriate where they fit (L9 recorded videos, ~[10:00]). EDA changes the default wiring for event flows; it does not ban request–reply, and W9.4 shows the same hybrid — a consumer microservice that also exposes a REST API.</panel>

</panel>

<span id="W9-c4"></span>

### W9.4 Event-driven microservices ★★

**Microservices give the boundaries; events give the wiring — the hybrid is the event-driven microservice.** The deck asks straight out: "Is this a hybrid: EDA + 𝜇service?" (slide 29 — "𝜇service" is the slide's shorthand for *microservice*: µ is the micro prefix).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-event-driven-microservice" trim />
</box>

**Applying both principle sets produces the hybrid — and shows where they clash.** Combine EDA's asynchronous communication with microservices' cohesive services and data ownership (slides 30–31).

* **One service, several responsibilities — acceptable in EDA, not in microservices.** The deck's example: an Order Submission service that has to accept an order, validate it, apply the payment, and adjust the inventory. EDA tolerates it; microservice architecture rejects it — no {{ term("single responsibility", "a service should have exactly one cohesive responsibility — one reason to change") }} (slide 30).
* **The recorded videos run the full design review on that example.** The event wiring is present — order submission publishes `OrderSubmitted`, fulfillment reacts and ships, email notifies — yet two checks still fail: payment and inventory have their own rules and reasons to change, so hiding them inside order submission makes those responsibilities harder to change independently, and the email service reading the order-submission database directly crosses the data-ownership boundary. ==So it is *not* an event-driven microservices design — event wiring alone is not enough== (L9 recorded videos, ~[07:00]–[08:00]).
* **"Is this event-driven microservices?" is a three-check question.** Event wiring alone does not settle it (L9 recorded videos, ~[07:00]):
  * **Event-driven interactions** — are the workflows wired by events?
  * **Cohesion** — does each service hold one business responsibility?
  * **Data ownership** — does each service own its data, with no direct reads of another's store?
* **Split it into microservices that each own their data, wiring them with events, and you get an event-driven microservice system.** Splitting order submission into order-placement, payment, and inventory services lets each publish events about changes within its responsibility, with the others reacting to complete the workflow — the single responsibility principle applied at the level of business capabilities, where a service may still perform several *related* operations and remain cohesive (slide 31; L9 recorded videos, ~[08:30]). Extending the same retail example with per-service data stores yields the event-driven microservice architecture for the online retail store (slide 31).

**Streams are owned by exactly one producer.** Consumer microservices consume and process events from one or more input event streams, applying their business logic (e.g., a Dashboard service consuming user data); producer microservices produce events to streams for others to consume (e.g., a User service owning user-related information) — and **each event stream has only one producing microservice, the owner of each event produced to that stream** (slide 32).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-event-stream" trim />
</box>

#### The event broker as a store

%%Terminology (L9 recorded videos, ~[10:30]): an *event store* is the related idea of keeping events around so they can be read later — and event brokers often help achieve the reliability quality attribute, because a broker with a persistent log makes the same event data support communication and storage at once.%%

**In event-driven microservices, event data is both the storage and the communication.** The broker receives events, holds them in a queue or partitions, and provides them for consumption — e.g., `UpdateProduct(pID, {"name": "SuperWidget"})` landing in an event log that Catalog, Inventory, and OrderArchive consumers read (slide 34). %%The slide's mental model: events are published to different partitioned streams according to their underlying logical meaning — much as a database keeps many tables, each holding one type of data — so UpdateProduct events land in the product stream, not in one undifferentiated log.%%

**Broker semantics — the properties you may rely on.** (Source: L9 slides 35–38.)

* **Immutable, append-only log.**
  * Events get an auto-incrementing index-ID; writes are append-only
  * All event data is immutable once published — there is no mechanism to modify it
  * You alter previous data only by publishing a new event
* **Ordering.** Data in an event stream *partition* is strictly ordered and served in exactly the published order.
* **Indexing (offsets).** A consumer seeking events seeks to the index-ID of the last message read (its offset), scans sequentially, and periodically records its new offset in the partition.
* **Partitioning.** Streams can be partitioned into substreams, the number varying with producer and consumer needs.
* **Infinite retention.** Streams retain events indefinitely if so configured — foundational for maintaining state in an event stream.
* **Replayability.** Any consumer can read whatever data it requires from the beginning — the basis for the single source of truth and for communicating state between services.

**A retained log is not a work queue — the difference is what reading does.** In a log, reading an event does not remove it: the event remains available according to the retention policy. In a conventional work queue, a message is normally removed once its processing is acknowledged — so a queue cannot offer replay or several independent readers (L9 recorded videos, ~[12:00]; queues return properly in W10.3).

**Offsets double as crash-tolerant progress markers.** A consumer that stops resumes from the offset of the last event it processed, and a consumer joining fresh chooses between that offset and the beginning of the partition (L9 recorded videos, ~[13:00]). **The offset is maintained at the consumer-group level.** Within a group, that shared bookkeeping is what prevents two members from processing the same event, while across groups one group racing ahead never blocks another from reading the same events later (L9 recorded videos, ~[13:00]).

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-immutability" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-offset" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-partition" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-consumer-group" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-infinite-retention" trim />
</box>

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-09.md#def-replayability" trim />
</box>

**Scaling falls out of the log model.**

* Producers write over many partitions on many machines.
* Load-balanced consumers share the partitions.
* Rate limits (throughput caps per producer, consumer, and group) apply to producers, consumers, and groups — Kafka ties the logs together, routing reliably, replicating for fault tolerance %%replication: Kafka keeps extra copies of each partition on other machines, so one machine failing loses no events%% (slides 39–40).

Reading and writing proceed in parallel across partitions, and scaling is straightforward: add machines and rebalance — redistributing the partitions across the enlarged set of machines (slide 40). The recorded videos give the mechanism: each partition maintains its own event order, so there is no global sequence to coordinate across the cluster, and producers and consumers scale independently because neither waits for the other to be active at the same moment (L9 recorded videos, ~[14:00]).

**The broker also buffers traffic spikes.** Producers keep publishing into the log even while consumers are temporarily slow or unavailable — the property Quiz 4 Q4's upload platform leaned on during the transcoding outage (L9 recorded videos, ~[14:30]).

The diagram shows one topic's partitions and the consumer groups reading them — the machinery behind the ordering and replay claims above.

<mermaid>
flowchart LR
    P["User service<br/>(sole producer/owner)"] -->|"append"| T["Topic 'user-activity'"]
    subgraph PART["Partitions — each an append-only log"]
        direction LR
        P0["P0: Ev0 → Ev1 → Ev2 → …"]
        P1["P1: Ev0 → Ev1 → …"]
        P2["P2: Ev0 → Ev1 → …"]
    end
    T --> PART
    PART --> C1["Consumer group:<br/>Dashboard svc reads P0+P1"]
    PART --> C2["Consumer group:<br/>Analytics reads P0–P2"]
</mermaid>

%%Notation: a rectangle is a service; each partition is an append-only log whose events carry increasing index-IDs (offsets); solid arrows are appends, and each consumer group tracks its own offset per partition.%%

How to read it: the User service is the only writer to this topic (single-owner rule, slide 32); events land in partitions by key; each consumer group reads partitions sequentially from its own offset — which is why Quiz 4 Q9's fix is to publish an order's events with `orderId` as the key, so they land on one partition and keep publication order, and why Quiz 4 Q8's reviewer is wrong: E1 on P1 and E2 on P2 advancing at different speeds is not an ordering violation, because per-partition ordering says nothing about processing order across partitions.

<box type="important" seamless>

**Events wear two hats.** The notification hat triggers services into action — the event-notification view of W9.1. The replication hat copies data from one service to another — event-carried state transfer (W9.1) applied at stream scale. Slide 42 adds a related fact: it is common for one event-driven microservice to be a consumer of some input streams and the producer of others. The recorded videos' worked example: the payment service consumes `OrderPlaced`, processes the payment, and publishes `PaymentSucceeded` or `PaymentFailed` for other services to react to (L9 recorded videos, ~[16:00]). All event brokers provide the same platform: append events to persistent logs, deliver them to consumers, and manage partitions and replication for scalability and availability — Kafka being a distributed persistent log store (slide 43).
</box>

<box type="warning" seamless>

**Trade-off — the deck's own balance sheet for event-driven microservices (slide 41).** On the plus side: performance (async, multitasking, very fast), scalability (services scale independently thanks to async processing and decoupling), maintainability (fairly independent services), evolvability (new functionality attaches to derived events), fault tolerance (one service going down doesn't bring down others in the workflow). On the minus side: complexity (async communication and varied database topologies) and testability (few dependencies and easy mocking, but high effort to test async processing across independent services).
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1.** Two microservices both write events to the `orders` stream. Which W9.4 rule is broken, and what is the fix?
<panel type="seamless" minimized header="%%Answer%%">Each event stream has exactly one producing microservice — its owner (slide 32). Split into two streams (one per owner) or funnel writes through the owning service.</panel>

**Q2.** A consumer needs to correct a published event's payload. What can it do, per broker semantics?
<panel type="seamless" minimized header="%%Answer%%">Nothing in place: event data is immutable once published; the only way to alter previous data is to publish a new event with the updated data (slide 37).</panel>

**Q3.** Quiz 4 Q8: E1 goes to partition P1 and is stuck behind a backlog; E2 goes to P2 and is processed immediately. A reviewer calls this an ordering-guarantee violation. Assess.
<panel type="seamless" minimized header="%%Answer%%">The reviewer is incorrect: per-partition ordering does not guarantee the processing order of events in *different* partitions — ordering holds strictly only within a partition (slide 37; Quiz 4 Q8).</panel>

**Q4.** A consumer-group member crashes mid-partition. What happens to its unprocessed events, and why does a *different* group still see them all?
<panel type="seamless" minimized header="%%Answer%%">Nothing is lost: the offset is maintained at the consumer-group level, so after the crash — or once a new member joins — consumption resumes from the offset of the last processed event (or from the beginning, if chosen). And because reading never removes an event from the partition, a separate group can still read the very same events from its own offset. (L9 recorded videos, ~[13:00])</panel>

</panel>

<box type="info" seamless>

**Section summary**

* **An event is a recorded fact** that is both data and an async communication means; its four views span discovery (storming), storage (sourcing), structure (CQRS), and content (notification vs event-carried state transfer).
* **Classify before you publish:** initiating vs derived events describe *where a fact came from*; event vs command vs query describes *what it wants* — and a command must never masquerade as a past-tense event.
* **Fire-and-forget buys responsiveness and availability** by removing temporal and identity/location coupling, at the price of fragmented error handling and event-format coupling.
* **EDA routes facts through a broker to subscribers**; event-driven microservices add bounded contexts, single-owner streams, and log semantics (immutability, ordering, offsets, partitions, replay) on top.
</box>

## Key terms

<span id="W9-key-terms"></span>

| Term | Definition | Unit |
|---|---|---|
| Event | A recording of something that happened; data + async communication means | [W9.1](#W9-c1) |
| Initiating event | End-user-originated event that kicks off a business process | [W9.1](#W9-c1) |
| Derived event | Internal event generated in response to an initiating event | [W9.1](#W9-c1) |
| Command | Imperative request to a specific receiver; changes state, returns no data | [W9.1](#W9-c1) |
| Query | Request for current state; needs a reply, changes nothing | [W9.1](#W9-c1) |
| Event notification | "Something happened" event carrying little data | [W9.1](#W9-c1) |
| Event-carried state transfer | Event carrying the data consumers need, avoiding callbacks | [W9.1](#W9-c1) |
| Event key | Key half of a key–value event: identification, routing, aggregation, partition placement | [W9.1](#W9-c1) |
| Fire-and-forget | Send and move on; no wait, no availability check | [W9.2](#W9-c2) |
| Temporal coupling | Producer and consumer must be up at the same time — removed by async communication | [W9.2](#W9-c2) |
| Event-driven architecture | Decoupled apps communicating asynchronously via events through a broker | [W9.3](#W9-c3) |
| Event broker | Intermediary that receives, holds, and provides events by subscription | [W9.3](#W9-c3) |
| Publish–subscribe | Publishers publish to topics; all subscribers receive | [W9.3](#W9-c3) |
| Latency | Delay between sending a request and receiving its response; sync calls create it | [W9.3](#W9-c3) |
| Event stream | Partitioned append-only sequence owned by one producing service | [W9.4](#W9-c4) |
| Event-driven microservice | Small service fulfilling a bounded context, wired by input/output event streams | [W9.4](#W9-c4) |
| Immutability | Published event data cannot be modified — corrections are new events | [W9.4](#W9-c4) |
| Offset | Index-ID of the last event read in a partition; consumers scan sequentially from it | [W9.4](#W9-c4) |
| Partition | Append-only substream of a stream; strictly ordered within; unit of parallelism | [W9.4](#W9-c4) |
| Consumer group | Load-balanced consumers sharing a stream's partitions between them | [W9.4](#W9-c4) |
| Infinite retention | Stream keeps events indefinitely if configured; foundation for state in the stream | [W9.4](#W9-c4) |
| Replayability | Any consumer can read from the beginning; basis for the single source of truth | [W9.4](#W9-c4) |
| Event sourcing | Events as source of truth; state reconstructed by replay | [W9.1](#W9-c1) |
| CQRS | Separate models for writes (commands) and reads (queries) | [W9.1](#W9-c1) |

## Connections

| Concept | Lecture | Tutorial | Other weeks / quizzes |
|---|---|---|---|
| Four views of an event | L9 slide 5 | — | W8 (storming, sourcing, CQRS) |
| Initiating vs derived events | L9 slides 7–8 | Tutorial 6 Q2 (event chains) | Quiz 4 Q2 |
| Event vs command vs query | L9 slide 9 | — | Quiz 4 Q1; W10 (events vs messages) |
| Event keys and payloads | L9 slides 10–11 | — | Quiz 4 Q3, Q9 |
| Fire-and-forget | L9 slides 13–18; L9 recording ~[44:00]–[52:00] (numbers, broker gap, compensation saga) | — | Quiz 4 Q4, Q10; W8.2/W8.4 (saga via choreography); W10 (sync vs async) |
| EDA, broker, pub/sub | L9 slides 20–27; L9 recorded videos ~[04:00]–[07:00] (observer analogy, data ownership) | — | W8.2 (database-per-service on slide 22); se-book event-driven page |
| Event-driven microservices, event broker as a store | L9 slides 29–43; L9 recorded videos ~[07:00]–[16:00] (three-check design review, log vs queue, offsets, buffering) | Tutorial 6 Q2 (bounded contexts → services) | Quiz 4 Q8, Q9; W10 (topic vs queue) |

## Further reading

* Martin Fowler, [What do you mean by Event-Driven?](https://martinfowler.com/articles/201701-event-driven.html) — the source of the four views (L9 slide 5).
* Microsoft Learn, [Implementing event-based communication between microservices](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/multi-container-microservice-net-applications/integration-event-based-microservice-communications) — source of the broker slide (L9 slide 22).
* Unkeyed / entity / keyed event classification (L9 slide 10). The deck gives no external attribution for the taxonomy.
* The se-book's [event-driven architecture page](https://se-edu.github.io/se-book/architecture/architecturalStyles/eventDriven/) — coupling vs traceability framing.

## Summary

**Key takeaways** (one per outcome):

* **An event is a recorded fact with four design views** — storming, sourcing, CQRS, and notification vs state-transfer — and it differs from a command (imperative, addressed, state-changing) and a query (state-asking, reply-needing); every cascade has exactly one initiating event and many derived ones.
* **Fire-and-forget communication decouples time and place** — producer and consumer need not coexist, and the producer need not know its consumers — while adding event-format coupling and fragmenting error handling.
* **Event-driven architecture is producers, a broker, and consumers** wired by pub/sub, trading bounded contexts (nice-to-have) for asynchronous speed, in contrast to microservices' request processing with foundational ownership.
* **Event-driven microservices are the principled hybrid** — one owner per stream, immutable ordered partitioned logs with offsets and replay — buying performance, scalability, evolvability, and fault tolerance at the price of complexity and test effort.

Key terms: see the [Key terms table](#W9-key-terms) above, each linked to its unit.

%%Next: Week 10 — Asynchronous communication. Events become one half of a bigger question — events vs messages by intent, one receiver vs many, and whether the communication persists when nobody is listening.%%

</div>
