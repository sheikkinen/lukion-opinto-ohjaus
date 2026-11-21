"""Read the content, the curriculum data and the yearly facts from disk."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from pipeline.models import Document, Problem, Section, Topic

_FENCE = re.compile(r"^\s*(```|~~~)")
_H2 = re.compile(r"^##\s+(.+?)\s*#*\s*$")


def split_front_matter(text: str) -> tuple[dict, list[str], list[str], int]:
    """Split a file into (meta, front matter lines, body lines, first body line number).

    Raises ValueError with a message when the front matter is missing or is not YAML.
    """
    lines = text.lstrip("﻿").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("the file must start with --- front matter")
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise ValueError("front matter is not closed with ---")
    front = lines[1:end]
    try:
        meta = yaml.safe_load("\n".join(front)) or {}
    except yaml.YAMLError as error:
        raise ValueError(f"front matter is not valid YAML: {error}") from error
    if not isinstance(meta, dict):
        raise ValueError("front matter must be a mapping")
    return meta, front, lines[end + 1 :], end + 2


def split_sections(body_lines: list[str], body_start: int) -> list[Section]:
    """Cut a body into H2 sections; headings inside code fences do not count."""
    sections: list[Section] = []
    in_fence = False
    for offset, line in enumerate(body_lines):
        if _FENCE.match(line):
            in_fence = not in_fence
        match = None if in_fence else _H2.match(line)
        if match:
            sections.append(Section(match.group(1).strip(), body_start + offset, []))
        elif sections:
            sections[-1].lines.append(line)
    return sections


def load_document(path: Path, root: Path, cls: type[Document] = Document) -> Document:
    shown = path.relative_to(root).as_posix() if path.is_relative_to(root) else path.as_posix()
    meta, front, body, start = split_front_matter(path.read_text(encoding="utf-8"))
    document = cls(shown, meta, body, start, front)
    document.sections = split_sections(body, start)
    return document


def load_directory(directory: Path, root: Path, cls: type[Document]) -> tuple[list, list[Problem]]:
    """Load every .md file of a directory; unreadable files become problems, not crashes."""
    documents, problems = [], []
    if not directory.is_dir():
        return documents, problems
    for path in sorted(directory.glob("*.md")):
        try:
            documents.append(load_document(path, root, cls))
        except ValueError as error:
            shown = path.relative_to(root).as_posix() if path.is_relative_to(root) else path.as_posix()
            problems.append(Problem(shown, 1, str(error), "front-matter"))
    return documents, problems


def load_topics(root: Path) -> tuple[list[Topic], list[Problem]]:
    topics, problems = load_directory(root / "content" / "topics", root, Topic)
    return sorted(topics, key=lambda t: (t.order, t.path)), problems


def load_pages(root: Path) -> tuple[dict[str, Document], list[Problem]]:
    pages, problems = load_directory(root / "content" / "pages", root, Document)
    return {page.slug: page for page in pages}, problems


def load_curriculum(root: Path) -> dict:
    path = root / "data" / "curriculum.yaml"
    if not path.is_file():
        raise FileNotFoundError("data/curriculum.yaml is missing: run python -m pipeline.fetch_curriculum")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def normalise_facts(raw: object) -> dict[str, dict]:
    """Yearly facts keyed by `key`, whether the file is a list, {facts: [...]} or a mapping."""
    if isinstance(raw, dict):
        inner = raw.get("facts") or raw.get("yearly_facts")
        if inner is None:
            return {str(k): {**v, "key": str(k)} for k, v in raw.items() if isinstance(v, dict)}
        raw = inner
    facts: dict[str, dict] = {}
    for entry in raw if isinstance(raw, list) else []:
        if isinstance(entry, dict) and "key" in entry:
            facts[str(entry["key"])] = entry
    return facts


def load_yearly_facts(root: Path) -> dict[str, dict] | None:
    """The yearly facts, or None when data/yearly-facts.yaml does not exist yet."""
    path = root / "data" / "yearly-facts.yaml"
    if not path.is_file():
        return None
    return normalise_facts(yaml.safe_load(path.read_text(encoding="utf-8")))
