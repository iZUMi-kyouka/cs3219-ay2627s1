{% import "se-book-adapted/config.njk" as config with context %}
{% from "schedule/macros-fragment.md" import edition_badge, icon_print, icon_quiz with context %}
<frontmatter>
title: "Textbook"
layout: textbook-layout.md
</frontmatter>

<div class="website-content" id="main">

## CS3219 Textbook {{ edition_badge() }}

<a href="{{baseUrl}}/se-book-adapted/print.html"><md>All chapters as one **printer-friendly page** {{ icon_print }}</md></a>

{% for section in config.topics %}

++**{{ section.heading }}**++

{% for chapter in section.chapters %}
* [{{ chapter.heading }}]({{baseUrl}}/se-book-adapted/chapters/{{ chapter.name }}.html)
{% endfor %}
{% endfor %}

++**Supplementary**++

* [Full book — all chapters in one continuous page]({{baseUrl}}/se-book-adapted/print.html)
* [List of definitions (glossary)]({{baseUrl}}/se-book-adapted/glossary.html)
* [Past quizzes (self-test)]({{baseUrl}}/se-book-adapted/index.html#quizzes)

<span id="quizzes">

## Past quizzes

{{ icon_quiz }} Use the four past quizzes as **closed-book self-tests** after finishing the corresponding chapters. Each is 30 minutes, 10 points.

* %%Quiz 1 (PDF kept offline)%% — **Weeks 1–5** (mainly 1, 2, 3, 5): AI in software engineering (pattern detection for a third-party-library vulnerability, AI-assisted development risks, push/pull factors), deployment mechanisms, backlog iteration, measurable NFRs and quality-attribute trade-offs, agile backlog iteration, serverless suitability. Revise [W1]({{ baseUrl }}/se-book-adapted/chapters/week-01-software-development-processes.html), [W2]({{ baseUrl }}/se-book-adapted/chapters/week-02-modern-software-engineering.html), [W3]({{ baseUrl }}/se-book-adapted/chapters/week-03-requirements.html), [W5]({{ baseUrl }}/se-book-adapted/chapters/week-05-cloud-native-paradigm.html).
* %%Quiz 2 (PDF kept offline)%% — **Weeks 4–7 and 9–10**: the Grab-like app's synchronous Booking→Matching call vs a BookingRequested event during a Matching outage; layered styles, the model–code gap, the modular monolith (Smart Kitchen), MVC vs pipe-and-filter, REST caching and statelessness. Revise [W4]({{ baseUrl }}/se-book-adapted/chapters/week-04-architecture-i.html), [W6]({{ baseUrl }}/se-book-adapted/chapters/week-06-architecture-ii-and-rest.html), [W7]({{ baseUrl }}/se-book-adapted/chapters/week-07-microservices-i.html), [W9]({{ baseUrl }}/se-book-adapted/chapters/week-09-event-driven-architecture.html), [W10]({{ baseUrl }}/se-book-adapted/chapters/week-10-asynchronous-communication.html).
* %%Quiz 3 (PDF kept offline)%% — **Weeks 7–10 and 12**: the room-booking modular monolith — extract search (80% of resources) and scale its instances on demand; when *not* to split (atomicity); DDD subdomains/bounded contexts, event storming policies, sagas, CQRS; sync/async/one-way classification. Revise [W7]({{ baseUrl }}/se-book-adapted/chapters/week-07-microservices-i.html), [W8]({{ baseUrl }}/se-book-adapted/chapters/week-08-microservices-ii.html), [W9]({{ baseUrl }}/se-book-adapted/chapters/week-09-event-driven-architecture.html), [W10]({{ baseUrl }}/se-book-adapted/chapters/week-10-asynchronous-communication.html), [W12]({{ baseUrl }}/se-book-adapted/chapters/week-12-scalability.html).
* %%Quiz 4 (PDF kept offline)%% — **Weeks 9–11**: EquipmentReserved redesign (command vs event), initiating vs derived events, temporal decoupling, choreographed compensation, aggregating facts by booking ID, async request-reply with a request identifier, per-partition ordering. Revise [W9]({{ baseUrl }}/se-book-adapted/chapters/week-09-event-driven-architecture.html), [W10]({{ baseUrl }}/se-book-adapted/chapters/week-10-asynchronous-communication.html), [W11]({{ baseUrl }}/se-book-adapted/chapters/week-11-messaging.html).

</span>

</div>
