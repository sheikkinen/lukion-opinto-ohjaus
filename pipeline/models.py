"""Plain data classes and small helpers shared by the build and the checks."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date

MODULES = ("OP1", "OP2")
CODE_PATTERN = re.compile(r"^(OP1|OP2)\.(t|s)\d+$|^OP\.yt\d+$")


@dataclass(frozen=True)
class Problem:
    """One thing the build found wrong, with the file and line it is in."""

    path: str
    line: int
    message: str
    kind: str = "content"
    warning: bool = False

    def __str__(self) -> str:
        label = "warning" if self.warning else "error"
        return f"{self.path}:{self.line}: {label}: {self.message}"

    def as_warning(self) -> Problem:
        return Problem(self.path, self.line, self.message, self.kind, True)


@dataclass
class Section:
    """An H2 section of a topic body. `line` is the absolute line of the heading."""

    title: str
    line: int
    lines: list[str]

    @property
    def text(self) -> str:
        return "\n".join(self.lines).strip("\n")


@dataclass
class Document:
    """A Markdown file with front matter (a topic or a static page)."""

    path: str
    meta: dict
    body_lines: list[str]
    body_start: int
    front_lines: list[str] = field(default_factory=list)
    sections: list[Section] = field(default_factory=list)

    @property
    def slug(self) -> str:
        return self.path.rsplit("/", 1)[-1].removesuffix(".md")

    @property
    def title(self) -> str:
        return str(self.meta.get("title", self.slug))

    def line_of(self, needle: str, default: int = 1) -> int:
        """The absolute line in the front matter where `needle` first appears."""
        for offset, text in enumerate(self.front_lines):
            if needle in text:
                return offset + 2
        return default

    def section(self, prefix: str) -> Section | None:
        for section in self.sections:
            if section.title.startswith(prefix):
                return section
        return None


@dataclass
class Topic(Document):
    """A topic file, content/topics/NN-slug.md."""

    @property
    def id(self) -> str:
        return str(self.meta.get("id", ""))

    @property
    def module(self) -> str:
        return str(self.meta.get("module", ""))

    @property
    def order(self) -> int:
        value = self.meta.get("order")
        return value if isinstance(value, int) else 0

    @property
    def codes(self) -> list[str]:
        """Curriculum codes, whether written as plain codes or as {code: ...} mappings."""
        found = []
        for item in self.meta.get("curriculum") or []:
            code = item.get("code") if isinstance(item, dict) else item
            if isinstance(code, str):
                found.append(code)
        return found

    @property
    def official_links(self) -> list[dict]:
        return [link for link in self.meta.get("official_links") or [] if isinstance(link, dict)]

    @property
    def yearly_fact_keys(self) -> list[str]:
        return [str(key) for key in self.meta.get("yearly_facts") or []]

    @property
    def durations(self) -> list[int]:
        return [d for d in self.meta.get("duration_options") or [] if isinstance(d, int)]

    @property
    def url_dir(self) -> str:
        return f"{self.module.lower()}/{self.slug}"


def as_date(value: object) -> date | None:
    """A date from YAML (already a date) or from a YYYY-MM-DD string; None if neither."""
    if isinstance(value, date):
        return value
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value.strip()):
        try:
            return date.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


def fi_date(value: object) -> str:
    """A date as Finnish d.m.yyyy text; the original text if it is not a date."""
    parsed = as_date(value)
    return f"{parsed.day}.{parsed.month}.{parsed.year}" if parsed else str(value)
