<span id="summary">

**How do you carve a business into microservices — and which patterns keep the pieces decoupled?** The lecture first finishes the DDD toolkit from Week 7 (domain → subdomains → bounded contexts, then event storming to find service candidates) and then walks the microservice *patterns*: data ownership and its exceptions, sagas, event sourcing, CQRS, and the wiring patterns (API gateway, orchestration vs choreography, service discovery).

</span>

<span id="toc">

* [W8.1 Domain-driven design: from domain to bounded context]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c1)
* [W8.2 Data patterns: owning, querying, and reconciling data]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c2)
* [W8.3 Event sourcing and CQRS]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c3)
* [W8.4 Communication, gateway, and discovery patterns]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c4)

</span>

<span id="lecture">

### Lecture

**The lecture opens by finishing last week's DDD story: the problem space is named first, the solution space second.**

- A *domain* is the problem space a business occupies (for FoC, peer-to-peer campus errands)
- *Subdomains* are its responsibility-focused components: errand fulfillment, the closed credit economy, campus vendors, and identity
- *Bounded contexts* are the solution-space boundaries you design for them — with a ubiquitous language per context, so *Student* can mean "account holder" in Identity and "requestor or courier" in Order

Slides 2–3 → [W8.1]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c1).

**Event storming is the lightweight practice that turns that vocabulary into microservice candidates.** Identify domain events (`ErrandPosted`, `CreditReserved`, `ErrandCompleted`), the commands that cause them (`PostErrand`, `SettleCredits`), the aggregates commands act on (`Errand`, `Wallet`), and the policies that react ("when `ErrandCompleted` then `SettleCredits`"). Slides 4 → [W8.1]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c1).

**The core guideline of the patterns half: microservices must own their data — that is what makes independent deployment possible.** The lecture gets there by elimination: agreed interfaces are a prerequisite, communication mechanisms merely carry data — the real threat is *co-ownership of data* (data written by one service and updated by another). Database-server-per-service is the strongest form; data independence also admits weaker forms (RBAC database users, private tables, private schemas), and the shared database is named as an antipattern for the coupling it creates at development time and runtime. Slides 6–10 → [W8.2]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c2).

**Cross-service needs get purpose-built patterns.** Queries that must join several services' data are served by a *data lake* — a read-only, queryable sink fed by data-change events from the owners, buffered by a message broker because the lake is read-optimized while the data changes fast (slide 11). Business processes that must modify several services' data become a *saga*: local transactions with registered compensating actions — each step's undo entry recorded on a routing slip, the running list that travels with the transaction — so if a later step fails, the compensations on the slip run, bringing the system to a reasonably compensated state, not the original one. Compensations must be *initiated* even when a service dies: the lecture works through a separate compensation worker, and a task queue whose time-to-live fires the compensation route when a step's acknowledgment never arrives. Slides 12–15 → [W8.2]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c2).

**Event sourcing replaces stored state with stored facts.** Events are immutable, timestamped, and appended in order; the current state is derived by replaying them (chess moves; `OrderPlaced` → `PaymentReceived` → `OrderShipped`). Slides 17–21 → [W8.3]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c3).

**CQRS separates the write path from the read path, each with its own model.** Commands change state and return nothing; queries return data and change nothing. One write model can feed many materialized views (e.g., via Kafka + KSQL), each scaled and stored independently — and, as the next lecture clarifies, CQRS doesn't *always* need events or event sourcing; they are just mostly used together. Slides 22–28 → [W8.3]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c3).

**The closing set wires services together.**

* Three interprocess styles — request/sync response, notification (send and don't care what the recipient does), request/async response (the TripManagement / PassengerManagement / Dispatcher examples, plus the lecture's taxi-booking story).
* The API gateway as the single, client-tailored entry point — with modern gateways adding authentication, monitoring, load balancing, and caching, and Kubernetes providing one automatically.
* Orchestration (central brain) vs choreography (each part reacts to events) — worked in the lecture on a loyalty-program enrollment, and connected back to the saga: the compensation worker is an orchestrator, TTL-fired compensation actions from an event store are choreography.
* Service discovery — client-side or server-side — against a service registry ("nothing but a database" of instances and ip:port locations) with self- or third-party registration.

Slides 30–37 → [W8.4]({{baseUrl}}/se-book-adapted/chapters/week-08-microservices-ii.html#W8-c4).

%%The deck ends by listing what it deliberately left out: backend-for-frontend, circuit breaker, retry, timeout, service mesh, observability (slide 39) — know the names, not the details.%%

</span>

<span id="tutorial-summary">

**Tutorial 5 consolidates your architecture toolkit before decomposition:** drawing an architecture for a CRUD single-page application (supplier repository), identifying Model/Controller/View parts of a Sudoku app, and designing a REST API — resources, URIs, representations, and HTTP verb mappings — for a library system.

</span>

<span id="tutorial">

### Tutorial 5

**What it practises:** architecture diagramming for a client–server application (Q1), the MVC pattern in a concrete app (Q2), and RESTful API design end-to-end — resource types, model URIs, JSON representations, and HTTP verb mappings (Q3). Q2 and Q3 apply Weeks 4 and 6; Q1 is the shape you will decompose into microservices in Weeks 8–9.

**Q1 — Architecture for the supplier repository.** The FoC project needs a single-page application performing CRUD operations on campus suppliers/vendors/landmarks. Develop the architecture and draw the diagram. *Hint: be able to show the different ways a user interacts with the system.* (Many valid answers; the solution stresses including the **supplier service** and the **CRUD** operations.)
<panel type="seamless" minimized header="%%Answer sketch%%">One valid shape: the SPA (browser client) talks to an API layer, which fronts the supplier service backed by its database — user interactions (browse, create, update, delete suppliers/vendors/landmarks) map to CRUD operations on the supplier service. Compare with the model solution's diagram in the PDF.</panel>

**Q2 — Sudoku as MVC.** (Rules as per sudokuonline.io; pre-loaded games plus player-built games that can be saved and reloaded.)
**a.** What constitutes the *Model*?
<panel type="seamless" minimized header="%%Answer%%">The Model manages the data, database interactions, and business rules: the core Sudoku grid (blocks/nonets — "nonet" is another name for a 3×3 block, cells, rows, columns), grid logic (rules, validation, completion checking, optional hint generation), user-created puzzles, saved games — plus other data such as player data and statistics.</panel>

**b.** What actions does the *Controller* provide?
<panel type="seamless" minimized header="%%Answer%%">The Controller is the middleman: it receives user input (note-taking, selecting a cell), updates the Model, and chooses the view — input handling plus game state management (creating, pausing, saving, loading, playing, resetting, finishing a game).</panel>

**c.** What *views* can the application provide?
<panel type="seamless" minimized header="%%Answer%%">The View displays the Model's data through views such as: puzzle editor, game board, game over/win, statistics, and player page (student solutions add main menu, puzzle library, saved games, puzzle builder, completion, settings, and rules views).</panel>

**Q3 — REST for a library management system.** Resources: Books; Book Status (borrowed/not); Book Author; Users; Books Borrowed.

**a.** What resource *types* (object types) do these fall under?

%%Resource types (the taxonomy the tutorial's solution uses): a **document** is one resource's full state at a single URI; a **collection** is a server-managed directory of documents (its items are sometimes called **singletons** — one item addressed inside the collection); a **store** is a repository where *clients* create and manage their own resources under chosen ids.%%
<panel type="seamless" minimized header="%%Answer%%">Books — a **collection** (a single book by id is a **document**/singleton). Book Status — a **document** (an attribute of each book). Book Author — a **document** (likewise an attribute). Users — a **collection** (a single user is a document). Books Borrowed — depends on management: a **collection** if the server manages borrowing records, or a **store** if clients manage their own records (less ideal).</panel>

**b.** Model URIs for these resources.
<panel type="seamless" minimized header="%%Answer%%">`http://api.library.restapi.org/books` and `/books/{book-id}`; `/books/{book-id}/status`; `/books/{book-id}/author`; `/users` and `/users/{user-id}`; `/users/{user-id}/books-borrowed`.</panel>

**c.** Design JSON representations for Users and Book Status (small but sufficient payloads).
<panel type="seamless" minimized header="%%Answer%%">Users: a well-formed array of `{ id, name, email, role }` objects. Status: `{ "book_id": "12345", "status": "available", "due_date": null }`.</panel>

**d.** Map the application's operations to HTTP requests (examples: *browse all books* → `GET /books`).
<panel type="seamless" minimized header="%%Answer%%">Full mapping in the solution PDF; highlights: get one book `GET /books/{book-id}`; search `GET /books/search?q={query}`; add book `POST /books`; update book `PUT /books/{book-id}`; delete book `DELETE /books/{book-id}`; add user `POST /users`; browse a user's borrowed books `GET /users/{user-id}/borrowedbooks`; borrow `POST /users/{user-id}/borrowedbooks`; return `PUT` or `DELETE /users/{user-id}/borrowedbooks/{book-id}`.</panel>

**Materials:**

* %%Tutorial sheet (PDF kept offline)%%
* %%Model solution (PDF kept offline)%%

</span>
