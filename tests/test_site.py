"""This site's content builds cleanly with the installed engine: fast, no network."""

from __future__ import annotations

from pathlib import Path

from lukio_runko.build import build_site
from lukio_runko.subject import load_subject

ROOT = Path(__file__).resolve().parent.parent


def test_subject_yaml_loads():
    subject = load_subject(ROOT)
    assert [m.code for m in subject.modules] == ["OP1", "OP2"]
    assert subject.assessment == "sh"


def test_site_builds_without_problems(tmp_path):
    problems = build_site(ROOT, tmp_path / "_site")
    assert [str(p) for p in problems] == []
    site = tmp_path / "_site"
    for page in ("index.html", "op1/index.html", "op2/index.html", "polku/index.html", "sitemap.xml"):
        assert (site / page).is_file(), page
    assert (site / "assets" / "css" / "site.css").is_file() and (site / "assets" / "img" / "il-front.webp").is_file()
