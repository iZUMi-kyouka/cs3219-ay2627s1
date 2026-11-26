{% import "se-book-adapted/config.njk" as config with context %}
{% from "schedule/macros-fragment.md" import edition_badge, icon_print with context %}
<frontmatter>
title: "CS3219 Textbook [Printable Version]"
</frontmatter>

<div class="website-content">

# ++**CS3219 Textbook**++ {{ edition_badge() }}

<span id="printable-version-description"><small>%%{{ icon_print }} This is a **printer-friendly** version: all chapters as one continuous document, grouped by section.%%</small></span>

{% set is_first_section = true %}
{% for section in config.topics %}
  {% if is_first_section %}
    {% set is_first_section = false %}
  {% else %}
{{ pagebreak }}
  {% endif %}

# **SECTION: {{ section.heading | upper }}**

{% set is_first_chapter = true %}
{% for chapter in section.chapters %}
  {% if is_first_chapter %}
    {% set is_first_chapter = false %}
  {% else %}
{{ pagebreak }}
  {% endif %}
<include src="../schedule/week{{ chapter.week }}/chapter-fragment.md" />
{% endfor %}
{% endfor %}

</div>
