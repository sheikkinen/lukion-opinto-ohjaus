"""The lesson plan section: split it into one part per lesson length, so that each length can be printed alone."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# "### 60 min" (older form) and "### Tuntisuunnitelma (60 min)" both start a plan for one length.
LENGTH_HEADING = re.compile(r"^###\s+(?:Tuntisuunnitelma\s*\(\s*)?(\d+)\s*min\s*\)?\s*$")
TITLE_LENGTH = re.compile(r"\(\s*(\d+)\s*min\s*\)")
_ANY_H3 = re.compile(r"^###\s")


@dataclass
class PlanParts:
    """The intro (shared), one block of lines per length, and the shared tail (preparation, rules)."""

    intro: list[str] = field(default_factory=list)
    lengths: list[tuple[int, list[str]]] = field(default_factory=list)
    tail: list[str] = field(default_factory=list)


def title_length(title: str) -> int | None:
    found = TITLE_LENGTH.search(title)
    return int(found.group(1)) if found else None


def length_heading(line: str) -> int | None:
    found = LENGTH_HEADING.match(line.strip())
    return int(found.group(1)) if found else None


def split_plan(title: str, lines: list[str]) -> PlanParts | None:
    """Split the section body by length. None if the heading does not state the master length."""
    master = title_length(title)
    if master is None:
        return None
    parts = PlanParts()
    current: list[str] = parts.intro
    in_tail = False
    for line in lines:
        length = length_heading(line)
        if length is not None:
            current = []
            parts.lengths.append((length, current))
            in_tail = False
            continue
        if current is parts.intro and line.lstrip().startswith("|") and not in_tail:
            current = []
            parts.lengths.append((master, current))
        elif _ANY_H3.match(line) and not in_tail:
            current = parts.tail
            in_tail = True
        current.append(line)
    return parts
