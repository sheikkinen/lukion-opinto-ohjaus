"""Checks of the written site: external resources, internal links, headings, alt text."""

from __future__ import annotations

import posixpath
import re
from functools import cache
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from pipeline.models import Problem

URL_ATTRIBUTES = ("src", "href", "action", "data", "poster", "srcset", "formaction")
EXTERNAL = re.compile(r"^\s*(?:https?:)?//", re.IGNORECASE)
CSS_EXTERNAL = re.compile(r"url\(\s*['\"]?\s*(?:https?:)?//|@import", re.IGNORECASE)
JS_EXTERNAL = re.compile(r"https?://", re.IGNORECASE)


class PageScan(HTMLParser):
    """Collects what the checks need from one HTML page, with line numbers."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.resources: list[tuple[int, str, str]] = []  # line, tag, external url
        self.links: list[tuple[int, str]] = []
        self.ids: set[str] = set()
        self.headings: list[tuple[int, int, str]] = []  # line, level, text
        self.problems: list[tuple[int, str]] = []
        self._in_style = False
        self._anchor: list | None = None
        self._heading: list | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {name: value or "" for name, value in attrs}
        line = self.getpos()[0]
        if "id" in values:
            self.ids.add(values["id"])
        if tag == "style":
            self._in_style = True
        if "style" in values and CSS_EXTERNAL.search(values["style"]):
            self.resources.append((line, tag, "style attribute"))
        for name in URL_ATTRIBUTES:
            value = values.get(name, "")
            if tag != "a" and value and EXTERNAL.match(value):
                self.resources.append((line, tag, value))
        if tag == "a" and "href" in values:
            self.links.append((line, values["href"]))
            self._anchor = [line, values.get("aria-label", "")]
        if tag == "img" and "alt" not in values:
            self.problems.append((line, "image without alt text"))
        if re.fullmatch(r"h[1-6]", tag):
            self._heading = [line, int(tag[1]), ""]
        if tag == "meta" and values.get("http-equiv", "").lower() == "refresh":
            self.problems.append((line, "meta refresh is not allowed"))

    def handle_endtag(self, tag: str) -> None:
        if tag == "style":
            self._in_style = False
        if tag == "a" and self._anchor is not None:
            if not self._anchor[1].strip():
                self.problems.append((self._anchor[0], "link without text"))
            self._anchor = None
        if re.fullmatch(r"h[1-6]", tag) and self._heading is not None:
            self.headings.append((self._heading[0], self._heading[1], self._heading[2]))
            self._heading = None

    def handle_data(self, data: str) -> None:
        if self._in_style and CSS_EXTERNAL.search(data):
            self.resources.append((self.getpos()[0], "style", "external url in <style>"))
        if self._anchor is not None:
            self._anchor[1] += data
        if self._heading is not None:
            self._heading[2] += data


def scan_page(path: Path) -> PageScan:
    scan = PageScan()
    scan.feed(path.read_text(encoding="utf-8"))
    return scan


def _shown(path: Path, site_dir: Path) -> str:
    return "_site/" + path.relative_to(site_dir).as_posix()


def check_external_resources(site_dir: Path) -> list[Problem]:
    """Anything in the output that loads from another host. Plain <a> links are fine."""
    problems = []
    for path in sorted(site_dir.rglob("*")):
        if not path.is_file():
            continue
        shown = _shown(path, site_dir)
        if path.suffix == ".html":
            for line, tag, url in scan_page(path).resources:
                problems.append(Problem(shown, line, f"external resource <{tag}> loads {url}", "external-resource"))
        elif path.suffix in (".css", ".js"):
            pattern = CSS_EXTERNAL if path.suffix == ".css" else JS_EXTERNAL
            for number, text in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if pattern.search(text):
                    problems.append(Problem(shown, number, "external address in a style or script file", "external-resource"))
    return problems


@cache
def _ids_of(path: str) -> frozenset[str]:
    return frozenset(scan_page(Path(path)).ids)


def _target_file(site_dir: Path, page_dir: str, href: str) -> Path | None:
    parts = urlsplit(href)
    target = posixpath.normpath(posixpath.join(page_dir, unquote(parts.path))) if parts.path else page_dir
    if target.startswith(".."):
        return None
    candidate = site_dir / target
    if candidate.is_dir():
        candidate = candidate / "index.html"
    return candidate if candidate.is_file() else None


def check_internal_links_and_headings(site_dir: Path) -> list[Problem]:
    _ids_of.cache_clear()
    problems = []
    for path in sorted(site_dir.rglob("*.html")):
        shown = _shown(path, site_dir)
        scan = scan_page(path)
        page_dir = path.parent.relative_to(site_dir).as_posix()
        for line, message in scan.problems:
            problems.append(Problem(shown, line, message, "html"))
        levels = [level for _, level, _ in scan.headings]
        if levels.count(1) != 1:
            problems.append(Problem(shown, 1, f"page has {levels.count(1)} h1 headings, expected 1", "html"))
        previous = 0
        for line, level, text in scan.headings:
            if not text.strip():
                problems.append(Problem(shown, line, "empty heading", "html"))
            if level > previous + 1:
                problems.append(Problem(shown, line, f"heading order jumps from h{previous} to h{level}", "html"))
            previous = level
        for line, href in scan.links:
            if re.match(r"^(?:[a-z][a-z0-9+.-]*:|//)", href, re.IGNORECASE):
                continue  # external or mailto: not our business here
            fragment = urlsplit(href).fragment
            target = _target_file(site_dir, page_dir, href)
            if target is None:
                problems.append(Problem(shown, line, f"broken internal link {href}", "html"))
            elif fragment and fragment not in _ids_of(str(target)):
                problems.append(Problem(shown, line, f"link {href} points to a missing anchor", "html"))
    return problems
