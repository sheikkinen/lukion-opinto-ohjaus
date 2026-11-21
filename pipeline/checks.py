"""Build checks from docs/content-contract.md. Every function returns a list of Problem.

Content checks live here; checks of the written HTML output live in site_checks.py and are
re-exported below, so `pipeline.checks` is the one place that lists every check.
"""

from __future__ import annotations

import re
from datetime import date, timedelta

from pipeline.models import CODE_PATTERN, MODULES, Document, Problem, Topic, as_date
from pipeline.plan import length_heading
from pipeline.site_checks import (  # noqa: F401  (re-exported)
    check_external_resources,
    check_internal_links_and_headings,
)

SECTION_ORDER = (
    "Opiskelijalle",
    "Tehtävät",
    "Pohdinta",
    "Itseopiskelun askel",
    "Tuntisuunnitelma",
    "Eriyttäminen",
    "Milloin opinto-ohjaajalle",
)
GENERATED_SECTION = "Lähteet"
REQUIRED_KEYS = (
    "id", "module", "order", "title", "summary", "curriculum", "suggested_timing", "role",
    "duration_options", "self_study_minutes", "prerequisites", "official_links", "yearly_facts",
    "school_adapts", "materials", "accessibility", "last_reviewed",
)  # fmt: skip
LINK_KEYS = ("title", "url", "publisher", "read")
ALLOWED_DURATIONS = (45, 60, 75, 90)
MAX_LINK_AGE_DAYS = 366

_LINK = re.compile(r"\[([^\]]*)\]\(([^)\s]*)[^)]*\)")
_AUTOLINK = re.compile(r"<https?://[^>]+>")
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_CODE_SPAN = re.compile(r"`[^`]*`")
_MONTHS = "tammi|helmi|maalis|huhti|touko|kesä|heinä|elo|syys|loka|marras|joulu"
FIGURE_PATTERNS = {
    "date": re.compile(rf"(?<![\w.,])\d{{1,2}}\.\d{{1,2}}\.?(?:\d{{4}})?(?!\w)|\b\d{{1,2}}\.\s?(?:{_MONTHS})\w*"),
    "euro amount": re.compile(r"\d[\d\s.,]*\s?(?:€|euroa\b|eur\b)|€\s?\d"),
    "percentage": re.compile(r"\d+(?:[.,]\d+)?\s?(?:%|prosentti\w*)"),
    "year": re.compile(r"(?<![\w.])20(?:2[5-9]|[3-9]\d)(?!\w)"),
}


def _twelve_months_before(today: date) -> date:
    try:
        return today.replace(year=today.year - 1)
    except ValueError:  # 29 February
        return today - timedelta(days=MAX_LINK_AGE_DAYS)


def check_read_date(path: str, line: int, value: object, today: date, what: str) -> list[Problem]:
    parsed = as_date(value)
    if parsed is None:
        return [Problem(path, line, f"{what} has no read date (read: YYYY-MM-DD)", "link-date")]
    if parsed > today:
        return [Problem(path, line, f"{what} has a read date in the future ({parsed})", "link-date")]
    if parsed < _twelve_months_before(today):
        return [Problem(path, line, f"{what} was read {parsed}, more than 12 months ago", "link-date")]
    return []


def check_front_matter(topic: Topic) -> list[Problem]:
    problems = []
    for key in REQUIRED_KEYS:
        if key not in topic.meta:
            problems.append(Problem(topic.path, 1, f"front matter key '{key}' is missing", "front-matter"))
    if problems:
        return problems
    meta = topic.meta
    here = topic.path

    def bad(key: str, message: str) -> None:
        problems.append(Problem(here, topic.line_of(f"{key}:"), f"{key}: {message}", "front-matter"))

    if meta["module"] not in MODULES:
        bad("module", "must be OP1 or OP2")
    if not isinstance(meta["order"], int) or not 1 <= meta["order"] <= 18:
        bad("order", "must be a whole number from 1 to 18")
    if topic.id != f"{topic.module.lower()}-{topic.slug}":
        bad("id", f"must be '{topic.module.lower()}-{topic.slug}' (module and file name)")
    if meta["role"] not in ("core", "extension"):
        bad("role", "must be core or extension")
    if not topic.durations or any(d not in ALLOWED_DURATIONS for d in topic.durations):
        bad("duration_options", "must list some of 45, 60, 75, 90")
    elif 75 not in topic.durations:
        bad("duration_options", "must include 75, the master plan")
    if not isinstance(meta["self_study_minutes"], int):
        bad("self_study_minutes", "must be a whole number of minutes")
    timing = meta["suggested_timing"]
    if not isinstance(timing, dict) or "year" not in timing or "term" not in timing:
        bad("suggested_timing", "must have year and term")
    if not isinstance(meta["curriculum"], list) or not topic.codes:
        bad("curriculum", "must list at least one curriculum code")
    for key in ("prerequisites", "official_links", "yearly_facts", "school_adapts", "materials"):
        if not isinstance(meta[key], list):
            bad(key, "must be a list (it may be empty)")
    hops = meta.get("hops_part")
    parts = ("opiskelusuunnitelma", "ylioppilastutkintosuunnitelma", "jatko-opinto- ja urasuunnitelma")
    if hops is not None and hops not in parts:
        bad("hops_part", "must be one of " + ", ".join(parts))
    return problems


def check_unique(topics: list[Topic]) -> list[Problem]:
    problems = []
    seen_ids: dict[str, str] = {}
    seen_orders: dict[int, str] = {}
    for topic in topics:
        if topic.id in seen_ids:
            problems.append(Problem(topic.path, 1, f"id '{topic.id}' is also used in {seen_ids[topic.id]}"))
        seen_ids.setdefault(topic.id, topic.path)
        if topic.order in seen_orders:
            problems.append(Problem(topic.path, 1, f"order {topic.order} is also used in {seen_orders[topic.order]}"))
        seen_orders.setdefault(topic.order, topic.path)
    return problems


def check_prerequisites(topic: Topic, known_ids: set[str]) -> list[Problem]:
    return [
        Problem(topic.path, topic.line_of(str(item)), f"prerequisite '{item}' is not a topic id", "prerequisite")
        for item in topic.meta.get("prerequisites") or []
        if item not in known_ids
    ]


def check_codes(topic: Topic, known_codes: set[str]) -> list[Problem]:
    problems = []
    for code in topic.codes:
        if code not in known_codes:
            kind = "unknown curriculum code" if CODE_PATTERN.match(code) else "malformed curriculum code"
            problems.append(Problem(topic.path, topic.line_of(code), f"{kind} {code}", "unknown-code"))
    return problems


def check_coverage(topics: list[Topic], known_codes: set[str], curriculum_path: str) -> list[Problem]:
    covered = {code for topic in topics for code in topic.codes}
    return [Problem(curriculum_path, 1, f"{code} is not served by any topic", "coverage") for code in sorted(known_codes - covered, key=_code_sort_key)]


def _code_sort_key(code: str) -> tuple:
    head, tail = code.split(".")
    return (head, tail[0] if tail[0] != "y" else "0", int(re.search(r"\d+$", tail).group()))


def check_sections(topic: Topic) -> list[Problem]:
    titles = [s.title for s in topic.sections]
    problems = []
    cursor = 0
    for expected in SECTION_ORDER:
        found = next((i for i in range(len(titles)) if _same_section(titles[i], expected)), None)
        if found is None:
            problems.append(Problem(topic.path, topic.body_start, f"missing section '## {expected}'", "sections"))
        elif found < cursor:
            line = topic.sections[found].line
            problems.append(Problem(topic.path, line, f"section '{titles[found]}' is out of order", "sections"))
        else:
            cursor = found
    known = [*SECTION_ORDER, GENERATED_SECTION]
    for index, section in enumerate(topic.sections):
        if not any(_same_section(section.title, name) for name in known):
            problems.append(Problem(topic.path, section.line, f"unknown section '## {section.title}'", "sections"))
        if _same_section(section.title, GENERATED_SECTION) and index != len(topic.sections) - 1:
            problems.append(Problem(topic.path, section.line, "'## Lähteet' must be the last section", "sections"))
    return problems


def _same_section(title: str, expected: str) -> bool:
    if expected == "Tuntisuunnitelma":
        return title.startswith("Tuntisuunnitelma")
    return title == expected


def word_count(text: str) -> int:
    return len(re.findall(r"[\wäöåÄÖÅ-]+", re.sub(r"[#|*_>`\[\]()]", " ", text)))


def check_lengths(topic: Topic) -> list[Problem]:
    """Soft limits from the contract, reported as warnings."""
    problems = []
    student = topic.section("Opiskelijalle")
    if student is not None and not 300 <= word_count(student.text) <= 600:
        count = word_count(student.text)
        problems.append(Problem(topic.path, student.line, f"'Opiskelijalle' has {count} words, expected 300-600", "length", True))
    tasks = topic.section("Tehtävät")
    if tasks is not None:
        count = len(re.findall(r"^###\s", tasks.text, re.MULTILINE))
        if not 1 <= count <= 3:
            problems.append(Problem(topic.path, tasks.line, f"'Tehtävät' has {count} tasks (### headings), expected 1-3", "length", True))
    return problems


def _table_rows(lines: list[str]) -> list[tuple[int, list[str]]]:
    """Rows of every Markdown table in `lines` as (index, cells), the separator rows left out."""
    rows = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c) and any(cells):
            continue
        rows.append((index, cells))
    return rows


def sum_plan_minutes(lines: list[str], start: int, path: str) -> tuple[int, list[Problem]]:
    """Add up the minutes column of the plan tables in `lines`; `start` is the first line number."""
    problems: list[Problem] = []
    rows = _table_rows(lines)
    column = 0
    total = 0
    header_seen = False
    for index, cells in rows:
        if not header_seen:
            header_seen = True
            column = next((i for i, c in enumerate(cells) if re.search(r"\bmin", c, re.I)), 0)
            continue
        cell = cells[column] if column < len(cells) else ""
        if "yhteensä" in " ".join(cells).lower():
            continue
        line = start + index
        if re.search(r"\d+\s*[–—-]\s*\d+", cell):
            problems.append(Problem(path, line, f"minutes must be one number, found '{cell}'", "minutes"))
            continue
        number = re.search(r"\d+", cell)
        if number is None:
            problems.append(Problem(path, line, f"table row has no minutes in column {column + 1}", "minutes"))
            continue
        total += int(number.group())
    return total, problems


def check_lesson_minutes(topic: Topic) -> list[Problem]:
    plan = topic.section("Tuntisuunnitelma")
    if plan is None:
        return []
    problems: list[Problem] = []
    start = plan.line + 1
    parts: dict[int, tuple[int, list[str]]] = {}
    stated = re.search(r"\((\d+)\s*min\)", plan.title)
    current = int(stated.group(1)) if stated else None
    if current is None:
        problems.append(Problem(topic.path, plan.line, "heading must state the length: 'Tuntisuunnitelma (75 min)'", "minutes"))
    else:
        parts[current] = (start, [])
    for offset, line in enumerate(plan.lines):
        heading = length_heading(line)
        if heading is not None:
            current = heading
            parts[current] = (start + offset, [])
        elif current is not None:
            parts[current][1].append(line)
    for length, (first_line, lines) in parts.items():
        if not _table_rows(lines):
            problems.append(Problem(topic.path, first_line, f"the {length} min plan has no table", "minutes"))
            continue
        total, found = sum_plan_minutes(lines, first_line + 1, topic.path)
        problems += found
        if total != length:
            problems.append(Problem(topic.path, first_line, f"the {length} min plan adds up to {total} minutes", "minutes"))
    for length in topic.durations:
        if length not in parts:
            problems.append(
                Problem(
                    topic.path,
                    plan.line,
                    f"duration_options lists {length} but there is no {length} min plan",
                    "minutes",
                )
            )
    for length in parts:
        if topic.durations and length not in topic.durations:
            problems.append(Problem(topic.path, plan.line, f"a {length} min plan exists but is not in duration_options", "minutes", True))
    return problems


def check_official_links(doc: Document, today: date) -> list[Problem]:
    problems = []
    links = doc.meta.get("official_links") or []
    for item in links:
        if not isinstance(item, dict):
            problems.append(Problem(doc.path, doc.line_of("official_links"), "official_links entries must be mappings", "front-matter"))
            continue
        line = doc.line_of(str(item.get("url", "")), doc.line_of("official_links"))
        for key in LINK_KEYS:
            if key != "read" and not item.get(key):
                problems.append(Problem(doc.path, line, f"official link has no {key}", "front-matter"))
        if not str(item.get("url", "")).startswith(("http://", "https://")):
            problems.append(Problem(doc.path, line, f"link url '{item.get('url')}' is not an http(s) address", "front-matter"))
        problems += check_read_date(doc.path, line, item.get("read"), today, f"link '{item.get('title', item.get('url'))}'")
    return problems


def check_yearly_fact_keys(topic: Topic, facts: dict[str, dict] | None) -> list[Problem]:
    if facts is None:
        return []
    return [
        Problem(topic.path, topic.line_of(key), f"yearly fact '{key}' is not in data/yearly-facts.yaml", "yearly-fact")
        for key in topic.yearly_fact_keys
        if key not in facts
    ]


def check_facts_file(facts: dict[str, dict], today: date, path: str = "data/yearly-facts.yaml") -> list[Problem]:
    problems = []
    for key, entry in facts.items():
        for field_name in ("rule", "url", "publisher"):
            if not entry.get(field_name):
                problems.append(Problem(path, 1, f"fact '{key}' has no {field_name}", "yearly-fact"))
        problems += check_read_date(path, 1, entry.get("read"), today, f"fact '{key}'")
    return problems


def _mask_links(line: str) -> str:
    """Blank out links, so that figures inside link text and urls are not counted."""
    for pattern in (_LINK, _AUTOLINK, _CODE_SPAN):
        line = pattern.sub(lambda m: " " * len(m.group()), line)
    return line


def body_lines_without_markup(topic: Topic) -> list[tuple[int, str]]:
    """(absolute line, masked text) for the body, minus comments, code, and the Lähteet section."""
    text = "\n".join(topic.body_lines)
    text = _COMMENT.sub(lambda m: re.sub(r"[^\n]", " ", m.group()), text)
    result = []
    in_fence = False
    generated = False
    for offset, line in enumerate(text.splitlines()):
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            continue
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading and not in_fence:
            generated = heading.group(1) == GENERATED_SECTION
        if not in_fence and not generated:
            result.append((topic.body_start + offset, _mask_links(line)))
    return result


def check_yearly_figures(topic: Topic, facts: dict[str, dict] | None) -> list[Problem]:
    """A date, euro amount, percentage or year in the text, outside a link, where yearly facts apply."""
    stable: list[str] = []
    for key in topic.yearly_fact_keys:
        stable += [str(s) for s in ((facts or {}).get(key, {}).get("stable_figures") or [])]
    problems = []
    for line_number, text in body_lines_without_markup(topic):
        for label, pattern in FIGURE_PATTERNS.items():
            for match in pattern.finditer(text):
                if match.group().strip() in stable:
                    continue
                message = f"{label} '{match.group().strip()}' in text: link to the official page instead of copying it"
                problem = Problem(topic.path, line_number, message, "yearly-figure")
                problems.append(problem if topic.yearly_fact_keys else problem.as_warning())
    return problems


def check_body_links(topic: Document, facts: dict[str, dict] | None) -> list[Problem]:
    """External links in the body must be listed in official_links (which carry read dates)."""
    allowed = {_normal_url(link.get("url", "")) for link in topic.meta.get("official_links") or [] if isinstance(link, dict)}
    for key in topic.meta.get("yearly_facts") or []:
        allowed.add(_normal_url((facts or {}).get(str(key), {}).get("url", "")))
    problems = []
    for offset, line in enumerate(topic.body_lines):
        for match in _LINK.finditer(line):
            url = match.group(2)
            if url.startswith(("http://", "https://")) and _normal_url(url) not in allowed:
                problems.append(
                    Problem(
                        topic.path,
                        topic.body_start + offset,
                        f"link {url} has no read date: add it to official_links",
                        "link-date",
                    )
                )
    return problems


def _normal_url(url: str) -> str:
    return str(url).strip().rstrip("/").lower()


def check_topic(topic: Topic, known_codes: set[str], facts: dict[str, dict] | None, today: date) -> list[Problem]:
    """All checks that look at one topic file on its own."""
    problems = check_front_matter(topic)
    if any(p.kind == "front-matter" and p.line == 1 for p in problems):
        return problems  # the later checks need the required keys
    problems += check_codes(topic, known_codes)
    problems += check_sections(topic)
    problems += check_lesson_minutes(topic)
    problems += check_official_links(topic, today)
    problems += check_yearly_fact_keys(topic, facts)
    problems += check_yearly_figures(topic, facts)
    problems += check_body_links(topic, facts)
    problems += check_lengths(topic)
    return problems
