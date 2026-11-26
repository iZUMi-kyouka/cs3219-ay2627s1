<span id="summary">

**How does it all fit together — and what should you revise, in what order?** L13 recaps the course along its four through-lines: requirements & quality attributes → architecture (monolith → modular monolith → microservices) → communication (sync → async, events, messages, EIPs — enterprise integration patterns, W11's pattern catalogue) → scaling (the scale cube), then closes with the exam-prep map: the four past quizzes, what each examines, and the study guide of slides to focus on.

</span>

<span id="toc">

* [W13.1 The course in one line: architecture serves requirements]({{baseUrl}}/se-book-adapted/chapters/week-13-course-recap.html#W13-c1)
* [W13.2 Through-line 1 — architecture: monolith → modular monolith → microservices]({{baseUrl}}/se-book-adapted/chapters/week-13-course-recap.html#W13-c2)
* [W13.3 Through-line 2 — communication: sync → async → events → messages]({{baseUrl}}/se-book-adapted/chapters/week-13-course-recap.html#W13-c3)
* [W13.4 Through-line 3 — scaling: the scale cube]({{baseUrl}}/se-book-adapted/chapters/week-13-course-recap.html#W13-c4)
* [W13.5 The whole course in one picture]({{baseUrl}}/se-book-adapted/chapters/week-13-course-recap.html#W13-c5)
* [W13.6 Exam preparation: the four quizzes and what each examines]({{baseUrl}}/se-book-adapted/chapters/week-13-course-recap.html#W13-c6)

</span>

<span id="lecture">

### Lecture

**The recap restarts from the beginning — requirements and quality attributes — because every later choice answers them.** What is software architecture, modularity/coupling/cohesion, the styles (layered, pipes-and-filters, MV* — the model–view family, e.g. MVC), web architecture and REST, and the modular monolith; the deck's partitioning picture sorts it along two dimensions: code *partitioning* — technical (layered) vs domain (modular monolith) — crossed with code *deployment* — monolith vs distributed (e.g. microservices, event-driven) (slide 2). → Chapter unit [W13.2]({{baseUrl}}/se-book-adapted/chapters/week-13-course-recap.html#W13-c2).

**Microservices are identified with DDD and event storming** — subdomains, bounded contexts, events, commands and policies (slide 3) — the Week 7–8 toolkit. → [W13.2]({{baseUrl}}/se-book-adapted/chapters/week-13-course-recap.html#W13-c2).

**Event-driven architecture is retold in one contrast: fire-and-forget vs synchronous communication**, with initiating and derived events (slide 4) — Week 9. → [W13.3]({{baseUrl}}/se-book-adapted/chapters/week-13-course-recap.html#W13-c3).

**Asynchronous communication condenses to its exam-ready rules** (slide 5) — Weeks 10–11:

- Message vs event — *intent matters*
- Pub-sub
- Messaging
- Asynchronicity in the request-reply pattern
- Architect based on business needs

→ [W13.3]({{baseUrl}}/se-book-adapted/chapters/week-13-course-recap.html#W13-c3).

**Messaging's premise is one line: components need to communicate to exchange information — the EIP catalogue is how** (slides 6–7). → [W13.3]({{baseUrl}}/se-book-adapted/chapters/week-13-course-recap.html#W13-c3).

**The scalability lens replays Week 12: the scale cube, scaling databases, scale out, multi-tier scaling** (slide 8). → [W13.4]({{baseUrl}}/se-book-adapted/chapters/week-13-course-recap.html#W13-c4).

**The deck closes with exam matters and a study guide** — the format (closed-book, one A4 cheat sheet, MCQ/short answers/drawing) and a per-deck list of slides to focus on (slides 10–11) — plus the course's core skills and practical tips: sane boundaries, the right level of coupling, document decisions and evolution (slides 12–13). → [W13.6]({{baseUrl}}/se-book-adapted/chapters/week-13-course-recap.html#W13-c6).

<box type="tip" seamless>

**How to use this lecture:** it has no new material — its value is the *sequence*. If any slide-2-through-slide-8 recap feels unfamiliar, that through-line is your revision queue; the chapter maps each one to its defining week.
</box>

</span>
