import re

import pytest

from pipeline import build
from pipeline.build import build_site
from tests.helpers import SECTIONS, TODAY, all_codes_topic, make_root, write_topic


def errors(problems):
    return [p for p in problems if not p.warning]


def test_build_writes_every_page_and_passes(tmp_path):
    root = make_root(tmp_path)
    all_codes_topic(root)
    out = root / "_site"
    problems = build_site(root, out, today=TODAY)
    assert errors(problems) == []
    for page in (
        "index.html",
        "op1/index.html",
        "op2/index.html",
        "op1/01-testi/index.html",
        "op1/01-testi/tunti/index.html",
        "polku/index.html",
        "tulosta/op1/index.html",
        "tulosta/op2/index.html",
        "opetussuunnitelma/index.html",
        "lahteet/index.html",
        "tietosuoja/index.html",
        "saavutettavuus/index.html",
        "assets/js/polku.js",
        "assets/css/site.css",
        "assets/css/print.css",
    ):
        assert (out / page).is_file(), page


def test_links_are_relative_only(tmp_path):
    root = make_root(tmp_path)
    all_codes_topic(root)
    build_site(root, root / "_site", today=TODAY)
    for path in (root / "_site").rglob("*.html"):
        for href in re.findall(r'(?:href|src)="([^"]*)"', path.read_text(encoding="utf-8")):
            assert not href.startswith("/"), (path, href)


def test_student_view_has_tick_hidden_without_script_and_lesson_view_has_plan(tmp_path):
    root = make_root(tmp_path)
    all_codes_topic(root)
    build_site(root, root / "_site", today=TODAY)
    student = (root / "_site/op1/01-testi/index.html").read_text(encoding="utf-8")
    lesson = (root / "_site/op1/01-testi/tunti/index.html").read_text(encoding="utf-8")
    assert "data-step-toggle" in student
    assert re.search(r"<p class=\"tick\" data-js-only hidden>", student)
    assert "Tuntisuunnitelma (75 min)" in lesson
    assert "Tuntisuunnitelma (75 min)" not in student
    assert "Opiskelijalle" in student
    assert "<h2>Opiskelijalle</h2>" in student
    assert "<h2>Opiskelijalle</h2>" not in lesson


def test_unknown_code_fails_the_build(tmp_path):
    root = make_root(tmp_path)
    write_topic(root, curriculum=["OP1.t77"])
    found = errors(build_site(root, root / "_site", today=TODAY))
    assert any("unknown curriculum code OP1.t77" in p.message and p.line > 1 for p in found)
    assert any(p.kind == "coverage" for p in found)


def test_partial_mode_makes_coverage_a_warning(tmp_path):
    root = make_root(tmp_path)
    write_topic(root)
    assert any(p.kind == "coverage" for p in errors(build_site(root, root / "_site", today=TODAY)))
    partial = build_site(root, root / "_site", partial=True, today=TODAY)
    assert not any(p.kind == "coverage" for p in errors(partial))


def test_build_copes_with_no_topics(tmp_path):
    root = make_root(tmp_path)
    problems = build_site(root, root / "_site", partial=True, today=TODAY)
    assert errors(problems) == []
    assert "Aiheita ei ole vielä julkaistu" in (root / "_site/op1/index.html").read_text(encoding="utf-8")


def test_broken_topic_is_reported_and_skipped(tmp_path):
    root = make_root(tmp_path)
    all_codes_topic(root)
    write_topic(root, "02-rikki", id="op1-02-rikki", order=2, role="nonsense")
    problems = build_site(root, root / "_site", today=TODAY)
    assert any("role" in p.message for p in errors(problems))
    assert not (root / "_site/op1/02-rikki").exists()
    assert (root / "_site/op1/01-testi").exists()


def test_missing_section_fails_with_file_name(tmp_path):
    root = make_root(tmp_path)
    all_codes_topic(root)
    sections = {k: v for k, v in SECTIONS.items() if k != "Eriyttäminen"}
    write_topic(root, "02-vajaa", id="op1-02-vajaa", order=2, sections=sections)
    found = errors(build_site(root, root / "_site", today=TODAY))
    assert any(p.path.endswith("02-vajaa.md") and "Eriyttäminen" in p.message for p in found)


def test_cli_exit_codes_and_output_listing(tmp_path, capsys):
    root = make_root(tmp_path, with_facts=False)
    all_codes_topic(root)
    assert build.main(["--root", str(root)]) == 1  # no yearly-facts file yet
    assert "yearly-facts.yaml" in capsys.readouterr().err
    assert build.main(["--root", str(root), "--partial"]) == 0


def test_refuses_to_clear_the_project_itself(tmp_path):
    root = make_root(tmp_path)
    with pytest.raises(ValueError):
        build.prepare_output(root, root)
