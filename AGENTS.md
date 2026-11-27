# AGENTS.md — Populating the CS3219 Course Website

You are an AI agent **populating content** in a MarkBind course website for
**CS3219 — Software Design and Architecture** (AY2026/27 S1). The goal is
**learning that is easy, comprehensive and smooth**: a student working alone,
with no lecturer and no tutor, should be able to learn each week from this
site alone.

Fill the `TODO` markers with pedagogically excellent content. **Do not
restructure the site, do not edit `site.json`, layouts,
`schedule/macros-fragment.md`, or any file outside your assigned ownership
(unless you are the sole agent working).** Pages are thin renderers; all
content lives in fragments.

This site is **for self-learning only**. There are deliberately **no admin,
tP/iP, project, grading or logistics pages**. Never add them.

Structure and styling follow the CS2103(T) website
(`NUS-CS2103-AY2627-S1/website`) and its textbook (`se-edu/se-book`) **as
closely as possible** — in phrasing, organisation and flow, not just markup.
When in doubt about how to phrase or structure something, open the closest
se-book source file (see the audit table below) and imitate it.

## 1. Where things live

```
site.json, _markbind/layouts/     site chrome — DO NOT TOUCH
schedule/macros-fragment.md       course data + shared macros (term, example) — DO NOT TOUCH
index.md                          landing page
schedule/index.md                 full-semester timeline (generated)
schedule/weekN/                   ← weekly workspace
  index.md / lecture.md / tutorial.md   thin tab pages — do not edit
  content-fragment.md             ← EDIT: weekly content (anchored spans)
  chapter-fragment.md             ← EDIT: the week's textbook chapter
se-book-adapted/config.njk        textbook sections + chapter list — DO NOT TOUCH
se-book-adapted/common/defs-week-NN.md   ← EDIT: your week's key-term definitions
se-book-adapted/glossary.md       GENERATED — do not hand-edit; run scripts/build-glossary.py
se-book-adapted/chapters/*.md     thin renderers of chapter fragments — do not edit
se-book-adapted/index.md          textbook ToC (+ quizzes section)
se-book-adapted/print.md          full book — auto-assembles from chapter fragments
assets/week-NN/                   slides, tutorial sheets & solutions
assets/quizzes/                   the four past quiz papers
```

**Golden rule:** to populate week N you edit exactly two course files —
`schedule/weekN/content-fragment.md` and `schedule/weekN/chapter-fragment.md`
— plus your week's `se-book-adapted/common/defs-week-NN.md`. The week Summary
page, the Timeline and `se-book-adapted/print.md` pick up the fragments
automatically. Never copy fragment content into thin pages.

## 2. Source material (ground truth — never invent facts)

Sources are in `/home/iz/Documents/cs3219/`, mirrored into `assets/week-NN/`:

| Source | Where | Use |
|---|---|---|
| Lecture slides | `assets/week-NN/slides/*.pdf` | primary structure for Lecture tab and chapter units |
| Tutorial sheets | `assets/week-NN/tutorial/` | Tutorial tab tasks |
| Tutorial solutions | `assets/week-NN/tutorial/*Solutions*` | model answers (Tutorial 2 has none) |
| Past quizzes | `assets/quizzes/` | self-check material |

> **Publication note:** the course PDFs are copyrighted ("not to be
> distributed") and are **not part of the published site** — `assets/**/*.pdf`
> is git-ignored. Never add new links to PDFs under `assets/`; refer to
> materials as dimmed text (e.g. `%%L9 slides, kept offline%%`).

Extract slide text with `pdftotext <pdf> -`. Every claim must be traceable to
a slide, tutorial or quiz item; cite slide ranges ("Source: L9 slides 4–12").
Week 5 is a **guest lecture (Dell, cloud-native paradigm)** — attribute it.
If an example is needed that the course doesn't provide, use a deliberately
plain one and mark it `%%external example%%`.

## 3. Content conventions — se-book fidelity (STRICT)

Import the shared macros in every fragment that uses them:

```
{% from "schedule/macros-fragment.md" import term, example with context %}
```

### 3.1 Unit anatomy and flow

Every concept unit `W<N>.k` flows **Motivation → What → How → Example →
Pitfalls/trade-offs** — the se-book order. Never open a unit with a definition;
open with one bold sentence saying *why the reader should care*. Then:

```
<span id="W4-c1"></span>

### W4.1 <concept title> ★

**Motivation — one bold, self-contained sentence.** One or two supporting
sentences.

<box type="definition" seamless>
<include src="../../se-book-adapted/common/defs-week-04.md#def-software-architecture" trim />
</box>

**How it works:** ... (bold-TLDR prose, 2–5 bold claims with unbolded support)

{{ example("L4 slides 14–17 — modular monolith") }}
... concrete course scenario ...
{{ endexample() }}   ← not needed; see note below

<box type="warning" seamless>
**Pitfall / trade-off:** ...
</box>

<panel type="seamless" header=":glyphicon-question-sign: **Self-check**">

**Q1. ...?**
<panel type="seamless" minimized header="%%Answer%%"> ... </panel>

</panel>
```

(For `example`, use `{% call example("label") %} ... {% endcall %}` — the macro
renders the panel; do not close it manually.)

### 3.2 Definitions

- Every key term is defined **once**, in your week's
  `se-book-adapted/common/defs-week-NN.md`, in an anchored span `def-<term>`
  (skeletons already exist — fill them, don't rename anchors).
- In the chapter, render it with `<box type="definition" seamless><include
  src="../../se-book-adapted/common/defs-week-NN.md#def-<term>" trim /></box>`
  (adjust the relative path: `chapters/` pages include the fragment from
  `schedule/weekN/`, so the fragment's own relative path is what matters).
- Definition phrasing = se-book cadence: short, testable, no filler
  ("A **microservice** is an independently deployable service modelled around
  a business domain." — compare `se-edu/se-book` definitions).
- In running prose, wrap the **first use per page** with
  `{{ term("term", "one-line definition for the popover") }}`. Later mentions
  are plain text.

### 3.3 Examples

- `{% call example("concrete label") %} ... {% endcall %}` — every example is a
  single concrete scenario, placed **immediately after** the claim it
  illustrates, never in a separate dump.
- Prefer course examples: the errand/pickup platform (L4-backlog, Tutorial 2),
  the Grab-like app (Quiz 2), the room-booking monolith (Quiz 3),
  `EquipmentReserved` (Quiz 4), and each deck's own examples.
- State provenance (slides/tutorial/quiz) and, for extracted requirements or
  scenarios, quote them faithfully.

### 3.4 Diagrams (mermaid)

- Renderer: the **`<mermaid>` custom tag** (MarkBind's mermaid plugin is
  enabled in site.json). Syntax:
  ```
  <mermaid>
  flowchart LR
    A[Client] -->|sync call| B[API]
  </mermaid>
  ```
  Do NOT use ```mermaid fenced code blocks — they are NOT rendered.
- Only **strategic** diagrams — those showing structure, flow or comparison
  that prose alone can't convey. No decoration.
- Every diagram is explained in three parts: (a) one sentence before it saying
  what it shows and why it matters, (b) the diagram, (c) after it:
  `%%Notation: ...%%` + a short "how to read it" walkthrough tied to a course
  example. This is non-negotiable.
- Keep notation consistent across chapters (box = component/service, solid
  arrow = synchronous call, dashed arrow = async message/event, cylinder = data
  store).
- **Never start an arrow with `<`** (`<-->`, `<-.->`): MarkBind's HTML
  conversion of `<mermaid>` blocks eats these as tags, corrupting the shipped
  source — the diagram parses in the source file but **fails in the browser**.
  Use `---`/`-.-` (optionally with a two-headed arrowhead via the node-end
  syntax, e.g. `A --- B` with an explicit arrowhead statement) and say in the
  %%Notation%% that the relation is bidirectional.
- Diagram size: keep ≤ ~8–10 nodes and labels ≤ ~30 characters — the content
  column is ~944 px, and oversized diagrams render with unreadably small text.
  Prefer splitting a crowded diagram into two over squeezing it.

### 3.5 Summaries

- **Every `##` section that spans two or more units ends with a short
  "Section summary" box** (`<box type="info" seamless>` with 2–4 bold-TLDR
  takeaway bullets).
- **Every chapter ends with `## Summary`**: (1) **Key takeaways** — one bold
  bullet per unit, mapping 1:1 to the unit outcomes; (2) **Key terms** table
  (term | one-line definition | link back to the unit anchor); (3) a final
  `%%Next: ...%%` pointer to what the next chapter builds on it.

### 3.6 Voice and markup

- **Bold-TLDR prose**: every claim is a bold, self-contained sentence; the bold
  text alone must read as a coherent skim-outline of the chapter.
- `#outcomes` items are always "**Can** …" phrases, verifiable by the reader.
- Priority stars on every unit: ★ core · ★★ supporting · ★★★ extension ·
  ★★★★ optional.
- `<box>` semantics: `info` = explanation/example; `tip` = advice;
  `important` = must-read; `warning` = pitfalls; `seamless` when nesting.
- `<panel type="seamless">` for multi-part material (two lecture decks in one
  week): `expanded` primary, `minimized` secondary, headers
  `## %%[W<N>.<k>]%% **Title**`.
- `%%dimmed%%` for asides, `==highlight==` for critical points, `:fas-...:`/
  `:glyphicon-...:` shortcodes inside `<md>` when needed.
- American English, plain language, direct address, no filler ("interesting",
  "important" without saying why).
- **Restructure, don't mirror, the slides.** CS3219 slide bulleting is often
  flat; when transcribing slide content into fragments, rebuild it to the
  CS2103 standard: one bold-TLDR claim per idea, sub-points as proper nested
  bullets, related bullets grouped under a claim, enumeration logic made
  explicit. A reader should get a *better-organized* version of the deck, not
  a slide dump.

## 4. Per-file specs

### `content-fragment.md` (weekly tabs)
- `#summary` — 2–3 sentences: the week's organising question and what the
  lecture(s) cover.
- `#toc` — the week's topics in reading order, one entry per chapter unit,
  each linking to its anchor (`...chapters/<slug>.html#w<n>-c<k>`).
- `#lecture` — bold-TLDR walkthrough, one claim per key move of the lecture,
  each with slide references; one `<panel type="seamless">` per deck for
  two-deck weeks.
- `#tutorial-summary` — 1–2 lines (what the tutorial practises).
- `#tutorial` — tasks in order; questions visible, answers revealed
  progressively (minimized panels); solution link after the tasks.

### `chapter-fragment.md` (the textbook chapter — core deliverable)
Follow the existing skeleton (`h2 #title`, `#prereqs`, `#outcomes`,
`<div id="body">`) exactly. **Units are dropdownified**: each `W<N>.k` unit is
wrapped as `<panel type="seamless" minimized header="**W<N>.k Title ★**">`
with the unit's `<span id="W<n>-c<k>">` anchor OUTSIDE (before) the panel, a
blank line after the panel open and before `</panel>`, and a generated unit-ToC
bulleted list under `## Core concepts`. When adding a new unit, write it as a
plain `### W<N>.k Title ★` heading + body and then re-run
`python3 scripts/dropdownify_units.py --apply all` (idempotent) to convert and
refresh the ToC — do not hand-write the panel wrapper. Concepts come from that
week's slides and tutorial only. End with `## Key terms` (if not folded into
`## Summary`) and `## Summary` per §3.5.

## 5. Build & verification

```
cd /home/iz/Documents/cs3219/website
flock /tmp/opencode/cs3219-build.lock npx markbind build
```

The build must finish **warning-free** (no "invalid intra-link" warnings).
Do not run `markbind serve`. Do not edit `site.json`. Never `git commit`.

## 6. Per-chapter audit — mandatory before a chapter counts as done

Audit against the closest se-book exemplar (fetch the raw source, e.g.
`https://raw.githubusercontent.com/se-edu/se-book/master/<path>/what/text.md`,
read it, compare):

| Chapter | se-book exemplar |
|---|---|
| W3 Requirements & quality attributes | `requirements/requirements/what/`, `requirements/nonFunctionalRequirements/` |
| W4–W6 Architecture, styles, REST | `architecture/architecturalStyles/` (each style), `architecture/introduction/` |
| W7–W8 Microservices, DDD | `architecture/architecturalStyles/` + `designPatterns/introduction/` phrasing |
| W9–W11 EDA, async, messaging | `architecture/architecturalStyles/eventDriven/what/` |
| W12 Scalability | quality-attribute phrasing from `requirements/nonFunctionalRequirements/` |

**Checklist (all must pass; fix in the same pass):**
1. Every unit opens with motivation before any definition.
2. All definitions are `def-*` includes in `<box type="definition">`, phrased
   in se-book cadence.
3. Reading only the bold text yields a coherent skim-outline of the chapter.
4. Every example is concrete, single-scenario, provenance-labelled, and placed
   immediately after its claim.
5. Every diagram has the three explanation parts (§3.4).
6. Outcomes are "Can …"; Summary takeaways map 1:1 to outcomes.
7. Self-checks reveal answers progressively; stars are consistent.
8. Flow read-through: no term used before it is defined (across weeks too —
   check the earlier def fragments for anchors you reuse).
9. Voice matches se-book: direct, plain, no filler; `%%dimmed%%` asides.
10. `flock` build is warning-free; Full Book (`print.html`) renders the chapter
    correctly.

Record the audit outcome (per-checklist-item pass + anything you deliberately
diverged on and why) in your final report — not on the site.
