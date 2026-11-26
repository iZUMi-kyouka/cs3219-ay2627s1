{% from "schedule/macros-fragment.md" import course_code, course_name, semester, weeks, icon_chapter, icon_lecture, icon_tutorial, icon_quiz, icon_print with context %}
<frontmatter>
title: "CS3219 — Software Design and Architecture"
layout: schedule-layout.md
pageNav: 2
</frontmatter>

# {{ course_code }}: {{ course_name }} <small><small>%%{{ semester }}%%</small></small>

<box type="important">

<!-- TODO(index): course pitch — what this site is for (self-learning revision),
     where to start (Textbook → Full Book, or the week you are revising), and
     what the weekly pages contain. Keep it short; remove this comment when done. -->

**This is a self-learning site**: it distils the course's **lecture slides, tutorials and quizzes** into a weekly set of pages and a continuous textbook. It contains no course logistics — only the material.

</box>

**How to use it:** learn a concept in the [Textbook]({{ baseUrl }}/se-book-adapted/index.html) → see how the lecture presented it (each week's *Lecture* tab) → rehearse with the week's tutorial → test yourself with the past [quizzes]({{ baseUrl }}/se-book-adapted/index.html#quizzes). The [Full Book]({{ baseUrl }}/se-book-adapted/print.html) gives the whole course as one continuous, printable read.

<div class="container">
  <div class="row">
  <div class="col-sm border-end">

**Navigate the weeks** — full details on the [Schedule]({{ baseUrl }}/schedule/index.html) page:

{% for n in range(1, 14) %}
* [**Week {{ n }}**]({{ baseUrl }}/schedule/week{{ n }}/index.html) <small><small>%%[{{ weeks[n | string].label }}]%% {{ weeks[n | string].topic }}</small></small>
{% endfor %}

  </div>
  <div class="col-sm">

**This site is your one-stop resource:**

* {{ icon_chapter }} **[Textbook]({{ baseUrl }}/se-book-adapted/index.html)** — one chapter per week, readable continuously: concepts, examples and key terms.
* {{ icon_lecture }} **Lecture material** — the week's slide decks with a curated walkthrough (see each week's *Lecture* tab).
* {{ icon_tutorial }} **Tutorials** — the week's tutorial sheet and, where available, its solution.
* {{ icon_quiz }} **Past quizzes** — four 30-minute quizzes for self-testing ([Textbook → Quizzes]({{ baseUrl }}/se-book-adapted/index.html#quizzes)).
* {{ icon_print }} **[Full Book]({{ baseUrl }}/se-book-adapted/print.html)** — all chapters in one continuous page.

</div>
  </div>
</div>
