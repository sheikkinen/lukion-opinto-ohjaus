"""Build the site: python -m pipeline.build [--partial] [--out _site]

Reads content/topics/*.md, content/pages/*.md, data/curriculum.yaml and data/yearly-facts.yaml,
writes _site/, runs every check and exits non-zero when any check fails. `--partial` is for
development while topics or facts are still being written: coverage and missing-facts problems
become warnings.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from datetime import date
from pathlib import Path

from pipeline import checks, views_site, views_topic
from pipeline.layout import SiteData
from pipeline.loaders import load_curriculum, load_pages, load_topics, load_yearly_facts
from pipeline.models import Problem

REQUIRED_PAGES = ("etusivu", "opetussuunnitelma", "lahteet", "polku", "tietosuoja", "saavutettavuus")
PARTIAL_KINDS = {"coverage", "facts-file", "prerequisite"}
STATIC_PAGES = {
    # page file: (output directory, current nav item, needs the progress script)
    "etusivu": ("", "", False),
    "opetussuunnitelma": ("opetussuunnitelma", "opetussuunnitelma", False),
    "lahteet": ("lahteet", "lahteet", False),
    "polku": ("polku", "polku", True),
    "tietosuoja": ("tietosuoja", None, False),
    "saavutettavuus": ("saavutettavuus", None, False),
}


def today_date() -> date:
    """Today, or the date in LOO_TODAY (YYYY-MM-DD) so the link age check can be repeated."""
    override = os.environ.get("LOO_TODAY")
    return date.fromisoformat(override) if override else date.today()


def write_page(out: Path, directory: str, html_text: str) -> None:
    target = out / directory / "index.html" if directory else out / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html_text, encoding="utf-8", newline="\n")


def prepare_output(root: Path, out: Path) -> None:
    resolved = out.resolve()
    if resolved == root.resolve() or resolved in root.resolve().parents:
        raise ValueError(f"refusing to clear {resolved}")
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    assets = root / "site-src"
    if assets.is_dir():
        shutil.copytree(assets, out / "assets")
    (out / ".nojekyll").write_text("", encoding="utf-8")


def collect_content_problems(data: SiteData, all_topics: list, facts: dict | None, root: Path) -> list[Problem]:
    known = set(data.codes)
    problems = checks.check_unique(all_topics)
    ids = {t.id for t in all_topics}
    for topic in all_topics:
        problems += checks.check_topic(topic, known, facts, data.today)
        problems += checks.check_prerequisites(topic, ids)
    problems += checks.check_coverage(all_topics, known, "data/curriculum.yaml")
    for page in data.pages.values():
        problems += checks.check_official_links(page, data.today)
        problems += checks.check_body_links(page, facts)
    if facts is None:
        problems.append(Problem("data/yearly-facts.yaml", 1, "the file does not exist yet", "facts-file"))
    else:
        problems += checks.check_facts_file(facts, data.today)
    return problems


def write_site(data: SiteData, out: Path) -> None:
    for slug, (directory, current, scripts) in STATIC_PAGES.items():
        write_page(out, directory, views_site.static_page(data, slug, directory, current, scripts))
    for module in ("OP1", "OP2"):
        write_page(out, module.lower(), views_site.module_page(data, module))
        write_page(out, f"tulosta/{module.lower()}", views_site.print_page(data, module))
    write_page(out, "tulosta", views_site.print_index(data))
    for topic in data.topics:
        write_page(out, topic.url_dir, views_topic.student_page(data, topic))
        write_page(out, topic.url_dir + "/tunti", views_topic.lesson_page(data, topic))


def build_site(root: Path, out: Path, partial: bool = False, today: date | None = None) -> list[Problem]:
    """Build the site and return every problem found (errors and warnings)."""
    today = today or today_date()
    curriculum = load_curriculum(root)
    all_topics, problems = load_topics(root)
    pages, page_problems = load_pages(root)
    problems += page_problems
    for slug in REQUIRED_PAGES:
        if slug not in pages:
            problems.append(Problem(f"content/pages/{slug}.md", 1, "required static page is missing", "pages"))
    facts = load_yearly_facts(root)
    data = SiteData(curriculum, [], pages, facts or {}, today, root / "templates")
    problems += collect_content_problems(data, all_topics, facts, root)
    renderable = [t for t in all_topics if not any(p.kind == "front-matter" and p.path == t.path for p in problems)]
    data = SiteData(curriculum, renderable, pages, facts or {}, today, root / "templates")
    if all(slug in pages for slug in REQUIRED_PAGES):
        prepare_output(root, out)
        write_site(data, out)
        problems += checks.check_external_resources(out)
        problems += checks.check_internal_links_and_headings(out)
    if partial:
        problems = [p.as_warning() if p.kind in PARTIAL_KINDS else p for p in problems]
    return problems


def report(problems: list[Problem]) -> int:
    ordered = sorted(problems, key=lambda p: (p.warning, p.path, p.line))
    for problem in ordered:
        print(problem, file=sys.stderr if not problem.warning else sys.stdout)
    errors = sum(1 for p in problems if not p.warning)
    print(f"build: {errors} errors, {len(problems) - errors} warnings")
    return 1 if errors else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, default=None, help="output directory, default <root>/_site")
    parser.add_argument("--partial", action="store_true", help="development: coverage and missing facts are warnings")
    args = parser.parse_args(argv)
    out = args.out or args.root / "_site"
    try:
        problems = build_site(args.root, out, args.partial)
    except (FileNotFoundError, ValueError) as error:
        print(f"build: {error}", file=sys.stderr)
        return 1
    return report(problems)


if __name__ == "__main__":
    sys.exit(main())
