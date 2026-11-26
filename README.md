# CS3219 Website (self-learning)

A [MarkBind](https://markbind.org/) site that distils **CS3219 — Software Design
and Architecture (AY2026/27 S1)** course materials — lecture slides, tutorials
and past quizzes — into:

- **Weekly pages** (`schedule/weekN/`) — only that week's material, as tabs
  (Summary · Lecture · Tutorial).
- **Textbook** (`se-book-adapted/`) — the continuous textbook, structured like
  the CS2103T `se-book-adapted`: a `config.njk` groups the week chapters into
  sections, `index.md` is the generated ToC, and `print.md` is the full book
  (all chapters, one page, with page breaks between chapters).

Styling follows the [CS2103(T) course website](https://github.com/NUS-CS2103-AY2627-S1/website)
(dark navbar, site/page nav columns, textbook layout), stripped of everything
not relevant to self-learning: there are **no admin, tP/iP, project or grading
pages**.

## Build & preview

```bash
npm install
npx markbind serve   # live preview at http://localhost:8080
npx markbind build   # static build into _site/
```

## Deploy (GitHub Pages)

The repo ships a ready-made workflow at `.github/workflows/deploy.yml`
(Node 22 → `npm ci` → `markbind build` → Pages artifact). To go live:

1. Push this folder as a repo (its root must be the site root, so the
   workflow paths match) to `github.com/iZUMi-kyouka/cs3219-ay2627s1`.
2. In the repo: **Settings → Pages → Build and deployment → Source =
   GitHub Actions**.
3. The project-page base URL is already set: `site.json` →
   `"baseUrl": "/cs3219-ay2627s1"`.
4. Push to `main` (or run the workflow manually) — the site appears at
   `https://izumi-kyouka.github.io/cs3219-ay2627s1/`.

> **Copyright note:** copyrighted NUS course PDFs (slides, tutorials,
> quizzes) are intentionally **not published** — `assets/**/*.pdf` is
> git-ignored and asset links are rendered as "kept offline" notes. Keep the
> PDFs in your local `assets/` folder for offline study.

## Layout of this repo

```
site.json, _markbind/layouts/     site chrome (adapted from the CS2103T site)
schedule/macros-fragment.md       course data (weeks/topics/dates) + macros
schedule/weekN/                   weekly pages (Summary/Lecture/Tutorial) + fragments
se-book-adapted/                  continuous textbook (config.njk, ToC, print.md, chapters)
assets/week-NN/                   slides, tutorial sheets & solutions
assets/quizzes/                   the four past quiz papers
AGENTS.md                         guide for filling in the content
```

Content is not populated yet — every page carries `TODO` markers. See
`AGENTS.md` for the population workflow.
