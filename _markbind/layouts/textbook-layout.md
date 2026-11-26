{% from "schedule/macros-fragment.md" import course_code, course_name with context %}
<head-bottom>
<link rel="stylesheet" href="{{baseUrl}}/css/main.css">
</head-bottom>

{% include '_markbind/layouts/header.md' %}
{% set file = "textbook" %}
{% set sitenav_title = "CS3219 Textbook" %}
{% include '_markbind/layouts/body.md' %}
{% include '_markbind/layouts/footer.md' %}
