"""Page shell, relative links and the data every view reads."""

from __future__ import annotations

import html
import posixpath
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from string import Template

from pipeline.images import ImageSet
from pipeline.models import Document, Topic, fi_date

SITE_NAME = "Lukion opinto-ohjaus"
NAV = (
    ("", "Etusivu"),
    ("op1", "OP1"),
    ("op2", "OP2"),
    ("polku", "Itseopiskelupolku"),
    ("opetussuunnitelma", "Opetussuunnitelma"),
    ("lahteet", "Lähteet"),
)


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def code_id(code: str) -> str:
    """The HTML id of a curriculum code: OP1.t3 becomes op1-t3."""
    return code.lower().replace(".", "-")


@dataclass
class SiteData:
    """Everything the views read: the curriculum, the topics, the static pages and the facts."""

    curriculum: dict
    topics: list[Topic]
    pages: dict[str, Document]
    facts: dict[str, dict]
    today: date
    templates_dir: Path
    images: ImageSet = field(default_factory=ImageSet)
    topics_by_id: dict[str, Topic] = field(init=False)

    def __post_init__(self) -> None:
        self.topics_by_id = {t.id: t for t in self.topics}

    @property
    def checked(self) -> str:
        return fi_date(self.curriculum["source"]["checked"])

    @property
    def codes(self) -> dict[str, dict]:
        return self.curriculum["codes"]

    def module_topics(self, module: str) -> list[Topic]:
        return [t for t in self.topics if t.module == module]

    def serving(self, code: str) -> list[Topic]:
        return [t for t in self.topics if code in t.codes]


class Ctx:
    """Where a page lives, so that every link can be written relative to it."""

    def __init__(self, directory: str = "") -> None:
        self.directory = directory.strip("/")

    def link(self, target: str = "", fragment: str = "") -> str:
        """Relative link to a page directory (a trailing slash) with an optional #fragment."""
        path = posixpath.relpath(target.strip("/") or ".", self.directory or ".")
        href = "./" if path == "." else path + "/"
        return f"{href}#{fragment}" if fragment else href

    def asset(self, path: str) -> str:
        return posixpath.relpath("assets/" + path, self.directory or ".")


def topic_label(topic: Topic) -> str:
    return f"{topic.order:02d}"


def render_page(
    data: SiteData,
    ctx: Ctx,
    title: str,
    main: str,
    description: str,
    current: str | None = None,
    scripts: bool = False,
    body_class: str = "",
) -> str:
    """Wrap the main content in templates/base.html."""
    template = Template((data.templates_dir / "base.html").read_text(encoding="utf-8"))
    nav = []
    for target, label in NAV:
        mark = ' aria-current="page"' if current == target else ""
        nav.append(f'<li><a href="{ctx.link(target)}"{mark}>{esc(label)}</a></li>')
    script_tag = f'<script src="{ctx.asset("js/polku.js")}" defer></script>' if scripts else ""
    page_title = SITE_NAME if title == SITE_NAME else f"{title} – {SITE_NAME}"
    return template.safe_substitute(
        title=esc(page_title),
        description=esc(description),
        css=ctx.asset("css/site.css"),
        print_css=ctx.asset("css/print.css"),
        body_class=esc(body_class),
        home=ctx.link(""),
        nav="\n".join(nav),
        main=main,
        checked=esc(data.checked),
        privacy=ctx.link("tietosuoja"),
        accessibility=ctx.link("saavutettavuus"),
        sources=ctx.link("lahteet"),
        scripts=script_tag,
    )
