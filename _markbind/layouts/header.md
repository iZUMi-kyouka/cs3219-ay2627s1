{% from "schedule/macros-fragment.md" import course_code, course_pair, period, weeks, recess with context %}
<header sticky>
<navbar placement="top" type="dark">
<a slot="brand" href="{{baseUrl}}/index.html" title="Home" class="navbar-brand"><span class="badge rounded-pill bg-success">{{ course_pair }} <small>{{ period }}</small></span></a>
  <dropdown header="**Schedule**" class="nav-link">
  <li><a href="{{baseUrl}}/schedule/index.html" class="dropdown-item"><md>**Full Timeline**</md></a></li>
  <li class="dropdown-divider"></li>
{% for n in range(1, 14) %}
  <li><a href="{{ baseUrl }}/schedule/week{{ n }}/index.html" class="dropdown-item"><md>**Week {{ n }}** <small><small>[{{ weeks[n | string].label }}] {{ weeks[n | string].topic }}</small></small></md></a></li>
  {% if n == 6 %}<li class="dropdown-divider"></li><li class="dropdown-item disabled"><md>%%{{ recess.label }} — {{ recess.topic }}%%</md></li>{% endif %}
{% endfor %}
  </dropdown>
  <li><a href="{{baseUrl}}/se-book-adapted/index.html" class="nav-link"><md>**Textbook**</md></a></li>
  <li><a href="{{baseUrl}}/se-book-adapted/print.html" class="nav-link"><md>:fas-print: **Full Book**</md></a></li>
  <li slot="right" class="nav-link">
    <form class="navbar-form">
      <searchbar :data="searchData" placeholder="Search" :on-hit="searchCallback" menu-align-right></searchbar>
    </form>
  </li>
</navbar>
</header>
