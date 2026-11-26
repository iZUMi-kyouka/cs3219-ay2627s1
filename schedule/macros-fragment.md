{#
Central data + macro library for the CS3219 course site.

This file is a *fragment*: it is never built as a page (site.json
pagesExclude `**/*-fragment.md`). Pages and layouts import from it:

    {% from "schedule/macros-fragment.md" import week_pagetop with context %}

Edit the `weeks` map to re-date or re-title the whole site.

This site is for self-learning only: lecture material, tutorial material
and the textbook. There are deliberately no admin, project (tP/iP) or
grading pages.

Week-page structure follows the CS2103(T) website (NUS-CS2103-AY2627-S1/website):
each week has separate pages (Summary / Lecture / Tutorial) sharing one
`week_pagetop` (frontmatter + pagination tab nav + week heading), and the
textbook lives in `se-book-adapted/` driven by `config.njk`.
#}

{% set course_code = "CS3219" %}
{% set course_pair = "CS3219" %}
{% set course_name = "Software Design and Architecture" %}
{% set semester = "AY2026/27 Semester 1" %}
{% set period = "AY2627S1" %}

{% set icon_summary = ":glyphicon-book:" %}
{% set icon_lecture = ":glyphicon-facetime-video:" %}
{% set icon_tutorial = ":fas-chalkboard-user:" %}
{% set icon_slides = ":far-images:" %}
{% set icon_chapter = ":fas-sitemap:" %}
{% set icon_prereq = ":glyphicon-education:" %}
{% set icon_outcome = ":fas-trophy:" %}
{% set icon_example = ":fas-cube:" %}
{% set icon_Q = ":glyphicon-question-sign:" %}
{% set icon_quiz = ":fas-clipboard-question:" %}
{% set icon_embedding = ":glyphicon-log-in:" %}
{% set icon_info = ":glyphicon-info-sign:" %}
{% set icon_tip = ":glyphicon-lightbulb:" %}
{% set icon_warning = ":glyphicon-exclamation-sign:" %}
{% set icon_print = ":fas-print:" %}

{# Week-page categories, in CS2103(T) style: each weekly tab's name, file and
   pageNav depth. Keys are the `category` argument of `week_pagetop`. #}
{% set week_categories = {
    summary:  { name: "Summary",  file: "index",    icon: icon_summary,  pagenav: 4 },
    lecture:  { name: "Lecture",  file: "lecture",  icon: icon_lecture,  pagenav: 3 },
    tutorial: { name: "Tutorial", file: "tutorial", icon: icon_tutorial, pagenav: 4 }
} %}

{# One entry per teaching week.
   `lecture`: lecture decks (assets/week-NN/slides/); `tutorial`: tutorial
   number (assets/week-NN/tutorial/), "" when the week has no tutorial;
   `chapter`: Textbook chapter page name under se-book-adapted/chapters/. #}
{% set weeks = {
  "1":  { label: "Aug 10–14",    topic: "Software Development Processes",        lecture: ["L1-SoftwareDevProcesses.pdf"],                          tutorial: "",  chapter: "week-01-software-development-processes" },
  "2":  { label: "Aug 17–21",    topic: "Modern Software Engineering",           lecture: ["L2-ModernSoftwareEngineering.pdf"],                     tutorial: "",  chapter: "week-02-modern-software-engineering" },
  "3":  { label: "Aug 24–28",    topic: "Requirements",                          lecture: ["L3-Requirements.pdf"],                                  tutorial: 1,   chapter: "week-03-requirements" },
  "4":  { label: "Aug 31–Sep 4", topic: "Architecture (I) & Product Backlog",    lecture: ["L4-Architecture.pdf", "L4-AlternativeExamplesForProductBacklog.pdf"], tutorial: 2, chapter: "week-04-architecture-i" },
  "5":  { label: "Sep 7–11",     topic: "Cloud-Native Paradigm (Guest Lecture)", lecture: ["L5-CloudNativeParadigm-GuestLectureByDell.pdf"],        tutorial: 3,   chapter: "week-05-cloud-native-paradigm" },
  "6":  { label: "Sep 14–18",    topic: "Architecture (II) & REST",              lecture: ["L6-Architecture.pdf", "L6-REST.pdf"],                   tutorial: 4,   chapter: "week-06-architecture-ii-and-rest" },
  "7":  { label: "Sep 28–Oct 2", topic: "Microservices (I)",                     lecture: ["L7-Microservices.pdf"],                                 tutorial: "",  chapter: "week-07-microservices-i" },
  "8":  { label: "Oct 5–9",      topic: "Microservices (II)",                    lecture: ["L8-Microservices.pdf"],                                 tutorial: 5,   chapter: "week-08-microservices-ii" },
  "9":  { label: "Oct 12–16",    topic: "Event-Driven Architecture",             lecture: ["L9-EDA.pdf"],                                           tutorial: 6,   chapter: "week-09-event-driven-architecture" },
  "10": { label: "Oct 19–23",    topic: "Asynchronous Communication",            lecture: ["L10-AsyncCommunication.pdf"],                           tutorial: 7,   chapter: "week-10-asynchronous-communication" },
  "11": { label: "Oct 26–30",    topic: "Messaging",                             lecture: ["L11-Messaging.pdf"],                                    tutorial: 8,   chapter: "week-11-messaging" },
  "12": { label: "Nov 2–6",      topic: "Scalability",                           lecture: ["L12-Scalability.pdf"],                                  tutorial: 9,   chapter: "week-12-scalability" },
  "13": { label: "Nov 9–13",     topic: "Course Recap",                          lecture: ["L13-Recap.pdf"],                                        tutorial: "",  chapter: "week-13-course-recap" }
} %}

{% set recess = { label: "Sep 21–25", topic: "Recess Week" } %}
{% set exam = { label: "Nov 21–Dec 5", topic: "Examination Week" } %}

{% macro edition_badge() %}<span class="badge rounded-pill bg-success">{{ course_pair }} edition - {{ period }}</span>{% endmacro %}

{# === se-book-style content macros ======================================
   Usage (import with context):
     {% from "schedule/macros-fragment.md" import term, example with context %}

   term(name, definition)  — key term on first use: highlighted badge with a
     popover carrying the definition. Use ONLY on first use per page; later
     mentions are plain text.
       {{ term("REST", "An architectural style for distributed hypermedia systems.") }}

   example(label)          — se-book-style example callout; wrap the body in
     {% call %}. The label names the concrete scenario.
       {% call example("Errand platform — pickup points") %} ... {% endcall %}
   ======================================================================== #}
{% macro term(name, definition) %}<span class="badge bg-term-highlight text-body-emphasis"><popover content="{{ definition }}">++{{ name }}++</popover></span>{% endmacro %}
{% macro example(label) %}<panel type="seamless" header=":fas-cube: **Example: {{ label }}**">

{{ caller() }}

</panel>{% endmacro %}

{% macro week_pagetop(week_num, category) %}
{% set c = week_categories[category] %}
<frontmatter>
title: "Week {{ week_num }} - {{ c.name }}"
layout: schedule-layout.md
pageNav: {{ c.pagenav }}
</frontmatter>

<nav>
<ul class="pagination mt-2">
{%- set previous_status = " disabled" if week_num == 1 else "" -%}
{%- set next_status = " disabled" if week_num == 13 else "" -%}
<li class="page-item{{ previous_status }}"><a class="page-link" href="../week{{ 1 if week_num == 1 else (week_num - 1) }}/index.html"><md>:glyphicon-chevron-left: **Prev. Week**</md></a></li>
<li class="page-item">&nbsp;&nbsp;&nbsp;</li>
{% for key, v in week_categories %}
  {%- if key != "tutorial" or weeks[week_num | string].tutorial -%}
  {%- set is_active = " active" if category == key else "" -%}
  <li class="page-item{{ is_active }}"><a class="page-link" href="{{ v.file }}.html"><md>{{ v.icon }} {{ v.name }}</md></a></li>
  {%- endif -%}
{% endfor %}
<li class="page-item">&nbsp;&nbsp;&nbsp;</li><li class="page-item{{ next_status }}"><a class="page-link" href="../week{{ 13 if week_num == 13 else (week_num + 1) }}/index.html"><md>**Next Week** :glyphicon-chevron-right:</md></a></li>
</ul>
</nav>

<p/>

# Week {{ week_num }} <small><small>%%[{{ weeks[week_num | string].label }}]%% - {{ c.name }}</small></small>
{% endmacro %}

{% macro chapter_head(n) %}
<frontmatter>
title: "Textbook — Week {{ n }}: {{ weeks[n | string].topic }}"
layout: textbook-layout.md
pageNav: 3
</frontmatter>

<nav>
<ul class="pagination mt-2">
<li class="page-item"><a class="page-link" href="{{ baseUrl }}/se-book-adapted/index.html"><md>{{ icon_chapter }} **All chapters**</md></a></li>
<li class="page-item"><a class="page-link" href="{{ baseUrl }}/se-book-adapted/print.html"><md>{{ icon_print }} **Full book**</md></a></li>
{% set prev_w = weeks[(n - 1) | string] %}{% if prev_w and prev_w.chapter %}<li class="page-item"><a class="page-link" href="{{ baseUrl }}/se-book-adapted/chapters/{{ prev_w.chapter }}.html"><md>:glyphicon-chevron-left: **Prev. Chapter**</md></a></li>{% endif %}
{% set next_w = weeks[(n + 1) | string] %}{% if next_w and next_w.chapter %}<li class="page-item"><a class="page-link" href="{{ baseUrl }}/se-book-adapted/chapters/{{ next_w.chapter }}.html"><md>**Next Chapter** :glyphicon-chevron-right:</md></a></li>{% endif %}
</ul>
</nav>

# Week {{ n }}: {{ weeks[n | string].topic }} <small><small>%%[{{ weeks[n | string].label }}]%% — Textbook Chapter</small></small>

<box type="info" seamless>

This is the **textbook chapter** for Week {{ n }}. For the week's overview, lecture and tutorial material, see the [Week {{ n }} page]({{ baseUrl }}/schedule/week{{ n }}/index.html).
</box>
{% endmacro %}
