#!/usr/bin/env python3
"""Generate se-book-adapted/glossary.md from the def-* spans in
se-book-adapted/common/defs-week-*.md.

The glossary is GENERATED — edit the defs-week-NN.md files (the single source
of truth) and re-run this script; never hand-edit glossary.md.

    python3 scripts/build-glossary.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMON = ROOT / "se-book-adapted" / "common"

CHAPTERS = {
    1: "week-01-software-development-processes",
    2: "week-02-modern-software-engineering",
    3: "week-03-requirements",
    4: "week-04-architecture-i",
    5: "week-05-cloud-native-paradigm",
    6: "week-06-architecture-ii-and-rest",
    7: "week-07-microservices-i",
    8: "week-08-microservices-ii",
    9: "week-09-event-driven-architecture",
    10: "week-10-asynchronous-communication",
    11: "week-11-messaging",
    12: "week-12-scalability",
}

WEEK_TOPICS = {
    1: "Software Development Processes",
    2: "Modern Software Engineering",
    3: "Requirements",
    4: "Architecture (I) & Product Backlog",
    5: "Cloud-Native Paradigm (Guest Lecture)",
    6: "Architecture (II) & REST",
    7: "Microservices (I)",
    8: "Microservices (II) & DDD",
    9: "Event-Driven Architecture",
    10: "Asynchronous Communication",
    11: "Messaging",
    12: "Scalability",
}

SECTIONS = [
    ("Foundations", [1, 2, 3]),
    ("Architecture", [4, 5, 6]),
    ("Distributed Systems & Microservices", [7, 8, 9, 10, 11, 12]),
]

# Terms defined in more than one week: keep the HOME week's row (richest
# phrasing), note the revisit, and skip the later duplicate.
DUPLICATES = {  # anchor -> (home_week, revisit_note)
    "def-subdomain": (7, "revisited with the FoC example in Week 8"),
    "def-bounded-context": (7, "revisited with the FoC example in Week 8"),
    "def-ubiquitous-language": (7, "revisited with the FoC example in Week 8"),
    "def-event-sourcing": (8, "revisited as the storage view of an event in Week 9"),
    "def-cqrs": (8, "revisited in Week 9's four views of an event"),
}


def parse_spans(path):
    text = path.read_text()
    spans = re.findall(r'<span id="(def-[^"]+)">(.*?)</span>', text, re.S)
    out = []
    for anchor, body in spans:
        body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
        # normalise the three citation styles into a Source column
        src = ""
        m = re.search(r"<sub>\s*--\s*(.*?)</sub>", body, re.S)
        if not m:
            m = re.search(r"%%\s*Source:\s*(.*?)%%", body, re.S)
        if not m:
            m = re.search(r"\(Sources?:\s*(.*?)\)\s*$", body, re.S)
        if m:
            src = re.sub(r"\s+", " ", m.group(1)).strip(" .%()")
            body = body[: m.start()]
        body = re.sub(r"\s+", " ", body).strip()
        # term = first bold phrase in the body (strip leading articles);
        # definition = the full body, left intact and grammatical
        m = re.search(r"\*\*(.+?)\*\*", body)
        if m:
            term = re.sub(r"^(A|An|The)\s+", "", m.group(1)).strip()
            term = term.split("(")[0].strip() or m.group(1)
        else:
            term = anchor[4:].replace("-", " ").capitalize()
        out.append((anchor, term, body, src))
    return out


def main():
    by_week = {w: parse_spans(COMMON / f"defs-week-{w:02d}.md") for w in CHAPTERS}

    lines = [
        "{% from \"schedule/macros-fragment.md\" import edition_badge with context %}",
        "<frontmatter>",
        'title: "Glossary — Definitions & Key Terms"',
        "layout: textbook-layout.md",
        "pageNav: 2",
        "</frontmatter>",
        "",
        "<div class=\"website-content\">",
        "",
        "## Definitions & Key Terms {{ edition_badge() }}",
        "",
        "Every key term of the course, **collated by topic and week**. Each row links to the week that teaches the term — follow it for the full treatment (diagram, example, self-check). Generated from the week definition files; terms defined in more than one week appear once, under their home week.",
        "",
    ]

    count = 0
    seen = set()
    for section, weeks in SECTIONS:
        lines += [f"### {section}", ""]
        for w in weeks:
            rows = []
            for anchor, term, definition, src in by_week[w]:
                if anchor in DUPLICATES and DUPLICATES[anchor][0] != w:
                    continue  # later duplicate: show once, at its home week
                if anchor in DUPLICATES:
                    definition += f" %%({DUPLICATES[anchor][1]})%%"
                term_cell = f"[**{term}**](chapters/{CHAPTERS[w]}.html)"
                rows.append(f"| {term_cell} | {definition} | {src} |")
                seen.add(anchor)
                count += 1
            if not rows:
                continue
            lines += [f"#### Week {w} — {WEEK_TOPICS[w]}", "",
                      "| Term | Definition | Source |",
                      "|---|---|---|"] + rows + [""]
    lines += ["</div>", ""]

    out = ROOT / "se-book-adapted" / "glossary.md"
    out.write_text("\n".join(lines))
    print(f"glossary.md written: {count} terms ({len(seen)} unique anchors)")


if __name__ == "__main__":
    main()
