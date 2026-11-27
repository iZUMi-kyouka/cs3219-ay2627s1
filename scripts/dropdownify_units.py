#!/usr/bin/env python3
"""Dropdownify all WX.Y unit headings in the CS3219 chapter fragments.

Each `### W<N>.k Title` unit becomes:
    <panel type="seamless" minimized header="**W<N>.k Title ★**">
    <unit body>
    </panel>
with the preceding `<span id="W<n>-c<k>">` anchor kept OUTSIDE the panel
(so cross-reference jumps land on the collapsed header), and a compact
unit-ToC inserted after each `## Core concepts` heading.

Idempotent: skips files already containing the panel form for their units.
Usage: python3 scripts/dropdownify_units.py [--apply week4]   (default: dry-run all)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEEKS = sorted(ROOT.glob("schedule/week*/chapter-fragment.md"),
               key=lambda p: int(re.search(r"week(\d+)", p.parent.name).group(1)))

UNIT = re.compile(r"^### (W\d+\.\d+\s+.*)$")
SECTION = re.compile(r"^## ")
SPAN = re.compile(r'<span id="(W\d+-c\d+)"></span>')


def transform(text):
    lines = text.split("\n")
    out, units, i = [], [], 0
    pending_span = None
    changed = False
    while i < len(lines):
        line = lines[i]
        m = UNIT.match(line)
        if not m:
            sm = SPAN.match(line)
            if sm:
                pending_span = sm.group(1)
            out.append(line)
            i += 1
            continue
        header = m.group(1).strip()
        # collect body until next unit heading / section heading / next unit anchor / EOF
        j = i + 1
        body = []
        while j < len(lines) and not UNIT.match(lines[j]) and not SECTION.match(lines[j]) \
                and not SPAN.match(lines[j]):
            body.append(lines[j])
            j += 1
        # trim trailing blanks
        while body and not body[-1].strip():
            body.pop()
        anchor = pending_span or ""
        units.append((header, anchor))
        # CS2103(T) se-book unit panel: seamless + expanded, card-title header
        out.append("")
        out.append('<panel type="seamless" expanded>')
        out.append(f'  <span slot="header" class="card-title"><markdown>### {header}</markdown></span>')
        out.append("")
        out.extend(body)
        out.append("")
        out.append("</panel>")
        out.append("")
        pending_span = None
        changed = True
        i = j
    # insert unit ToC after each `## Core concepts`
    if units and changed:
        final, k = [], 0
        toc_needed = False
        while k < len(out):
            final.append(out[k])
            if re.match(r"^## Core concepts\s*$", out[k]):
                toc_needed = True
                # peek ahead: skip blank lines; if the next non-blank is our first
                # panel, insert the ToC before it
                m2 = k + 1
                while m2 < len(out) and not out[m2].strip():
                    m2 += 1
                if m2 < len(out) and out[m2].startswith('<panel type="seamless" expanded>'):
                    final.append("")
                    for header, anchor in units:
                        title = re.sub(r"\*\*", "", header)
                        if anchor:
                            final.append(f"- [{title}](#{anchor})")
                        else:
                            final.append(f"- {title}")
                    final.append("")
                    k = m2 - 1  # resume so the blank line before the panel stays
            k += 1
        out = final
    return "\n".join(out), changed, units


def main():
    apply_to = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--apply" else None
    for path in WEEKS:
        week = re.search(r"week(\d+)", path.parent.name).group(1)
        if apply_to and apply_to != "all" and week != apply_to:
            continue
        text = path.read_text()
        if 'slot="header" class="card-title"><markdown>### W' in text:
            print(f"week{week}: already dropdownified — skipped")
            continue
        new, changed, units = transform(text)
        if not changed:
            print(f"week{week}: no WX.Y units found — skipped")
            continue
        if apply_to:
            path.write_text(new)
        print(f"week{week}: {len(units)} units dropdownified"
              + ("" if apply_to else "  (dry-run)"))
        for header, anchor in units:
            print(f"   - {header}  [{anchor or 'NO ANCHOR'}]")


if __name__ == "__main__":
    main()
