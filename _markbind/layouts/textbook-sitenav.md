{% import "se-book-adapted/config.njk" as config with context %}
{% from "schedule/macros-fragment.md" import icon_print with context %}
<site-nav>
* [**Home** :glyphicon-home:, printable version {{ icon_print }}]({{baseUrl}}/se-book-adapted/index.html)
{% for section in config.topics %}
* **{{ section.heading }}**
{% for chapter in section.chapters %}
  * [{{ chapter.heading }}]({{baseUrl}}/se-book-adapted/chapters/{{ chapter.name }}.html)
{% endfor %}
{% endfor %}
* Supplementary
  * [Full book (printable)]({{baseUrl}}/se-book-adapted/print.html)
  * [List of definitions (glossary)]({{baseUrl}}/se-book-adapted/glossary.html)
  * [Past quizzes]({{baseUrl}}/se-book-adapted/index.html#quizzes)
</site-nav>
