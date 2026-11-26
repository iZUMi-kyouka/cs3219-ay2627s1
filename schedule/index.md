{% from "schedule/macros-fragment.md" import weeks, icon_summary, icon_lecture, icon_tutorial, recess, exam with context %}
<frontmatter>
title: "Timeline"
layout: schedule-layout.md
pageNav: 3
</frontmatter>

<div class="website-content">

# Course Timeline

<box type="info" seamless>

Chapters follow the same order as the [Schedule](week1/index.html) — the [Textbook](../se-book-adapted/index.html) groups them into sections. Each week has tabs (Summary · Lecture · Tutorial) and a chapter in the Textbook.
</box>

{% for n in range(1, 14) %}
{% set w = weeks[n | string] %}

### <a href="week{{ n }}/index.html" class="badge rounded-pill bg-dark"><small>**Week {{ n }}** <small>— {{ w.label }}</small></small></a> <a href="week{{ n }}/index.html" class="badge bg-body-tertiary text-body-emphasis me-1"><small>%%{{ icon_summary }} Summary%%</small></a> <a href="week{{ n }}/lecture.html" class="badge bg-body-tertiary text-body-emphasis me-1"><small>%%{{ icon_lecture }} Lecture%%</small></a>{% if w.tutorial %} <a href="week{{ n }}/tutorial.html" class="badge bg-body-tertiary text-body-emphasis me-1"><small>%%{{ icon_tutorial }} Tutorial {{ w.tutorial }}%%</small></a>{% endif %}

<div class="indented-level2">

<include src="week{{ n }}/index.md#summary" optional />

</div>

<hr />

{% endfor %}

<div class="indented-level2"><md>%%{{ recess.label }} — {{ recess.topic }} (no class)%%</md></div>
<hr />
<div class="indented-level2"><md>%%{{ exam.label }} — {{ exam.topic }}%%</md></div>

</div>
