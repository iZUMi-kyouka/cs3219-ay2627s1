{% from "schedule/macros-fragment.md" import week_pagetop with context %}

{{ week_pagetop(6, "summary") }}

<div class="website-content">

<span id="summary">
<div class="container">
  <div class="row">
  <div class="col-sm border-end">

**Lecture topics:**

<include src="content-fragment.md#summary" />

<box type="info" seamless>

**Lecture decks:**

* %%L6-Architecture (PDF kept offline)%%
* %%L6-REST (PDF kept offline)%%
</box>

<panel type="seamless" header="%%Full ToC%%">
  <include src="content-fragment.md#toc" optional />
</panel>

  </div>
  <div class="col-sm">

**Tutorial:**

<include src="content-fragment.md#tutorial-summary" optional />

* %%Tutorial sheet (PDF kept offline)%%
* %%Model solution (PDF kept offline)%%

  </div>
  </div>
</div>
</span>

</div>
