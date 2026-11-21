"""Lesson plan headings, one-length printing, view links, the path without JavaScript and the date format."""

import re
from datetime import date

from pipeline import checks
from pipeline.build import build_site
from pipeline.models import fi_date
from pipeline.plan import length_heading, split_plan
from tests.helpers import PLAN_45, PLAN_60, PLAN_75, TODAY, all_codes_topic, make_root, write_topic


def build(tmp_path):
    root = make_root(tmp_path)
    all_codes_topic(root)
    build_site(root, root / "_site", today=TODAY)
    return root / "_site"


def read(site, name):
    return (site / name / "index.html").read_text(encoding="utf-8")


def test_length_heading_accepts_the_full_and_the_older_form():
    assert length_heading("### Tuntisuunnitelma (60 min)") == 60
    assert length_heading("### 45 min") == 45
    assert length_heading("### Valmistelu") is None
    assert length_heading("### Tuntisuunnitelma (abc min)") is None


def test_check_reads_full_and_older_length_headings(tmp_path):
    older = PLAN_75 + "\n### 60 min\n" + PLAN_60 + "\n### 45 min\n" + PLAN_45
    from tests.helpers import SECTIONS

    topic = write_topic(tmp_path, sections={**SECTIONS, "Tuntisuunnitelma (75 min)": older})
    assert checks.check_lesson_minutes(topic) == []
    topic = write_topic(tmp_path, sections=SECTIONS)
    assert checks.check_lesson_minutes(topic) == []


def test_check_still_wants_the_length_in_the_main_heading(tmp_path):
    from tests.helpers import SECTIONS

    sections = {("Tuntisuunnitelma" if k.startswith("Tuntisuunnitelma") else k): v for k, v in SECTIONS.items()}
    topic = write_topic(tmp_path, sections=sections)
    assert any("heading must state the length" in p.message for p in checks.check_lesson_minutes(topic))


def test_split_plan_keeps_the_tail_out_of_the_last_length():
    lines = ["Johdanto", "", *PLAN_75.splitlines(), "### 60 min", *PLAN_60.splitlines(), "### Valmistelu", "- a"]
    parts = split_plan("Tuntisuunnitelma (75 min)", lines)
    assert [n for n, _ in parts.lengths] == [75, 60]
    assert "Johdanto" in parts.intro[0]
    assert "- a" in parts.tail
    assert not any("Valmistelu" in line for _, block in parts.lengths for line in block)
    assert split_plan("Tuntisuunnitelma", lines) is None


def test_lesson_view_has_one_heading_and_id_per_length_and_print_links(tmp_path):
    lesson = read(build(tmp_path), "op1/01-testi/tunti")
    for length in (75, 60, 45):
        assert f"<h3>Tuntisuunnitelma ({length} min)</h3>" in lesson
        assert f'id="tunti-{length}" class="plan-length"' in lesson
        assert f'<a href="#tunti-{length}" data-print-length>Tulosta {length} min</a>' in lesson
    assert 'href="#tuntisuunnitelma" data-print-length' in lesson
    assert "<h3>Valmistelu</h3>" in lesson
    # the shared tail is outside every length block, so it prints whichever length is chosen
    common = lesson.split('class="plan-common"')[1]
    assert "Valmistelu" in common
    assert not re.search(r">\s*60 min\s*<", lesson)


def test_print_selection_needs_no_script_and_all_lengths_print_by_default(tmp_path):
    site = build(tmp_path)
    css = (site / "assets/css/print.css").read_text(encoding="utf-8")
    assert ".plan-length:not(:target)" in css and ":has(.plan-length:target)" in css
    # the hiding rule only applies after a choice; nothing hides a length otherwise
    assert not re.search(r"^\.plan-length\s*\{[^}]*display:\s*none", css, re.MULTILINE)
    assert ".plan-print" in css
    js = (site / "assets/js/polku.js").read_text(encoding="utf-8")
    assert "a[data-print-length]" in js
    # the links are plain anchors in the HTML: they work with JavaScript off
    assert 'data-js-only' not in read(site, "op1/01-testi/tunti").split("plan-print")[1].split("</nav>")[0]


def test_module_print_page_prints_every_length_without_choice_links(tmp_path):
    page = read(build(tmp_path), "tulosta/op1")
    assert "plan-print" not in page
    assert page.count('class="plan-length"') == 3
    assert len(set(re.findall(r'id="([^"]+)"', page))) == len(re.findall(r'id="([^"]+)"', page))


def test_both_views_mark_the_current_view_in_the_same_place(tmp_path):
    site = build(tmp_path)
    student = read(site, "op1/01-testi")
    lesson = read(site, "op1/01-testi/tunti")
    for page, current in ((student, "Opiskelijan näkymä"), (lesson, "Tuntisuunnitelma opinto-ohjaajalle")):
        nav = re.search(r'<nav class="view-switch".*?</nav>', page, re.DOTALL).group(0)
        assert nav.count('aria-current="page"') == 1
        assert re.search(rf'aria-current="page">{current}</a>', nav)
        # directly after the header picture or summary, before the meta list, in both views
        assert page.index("view-switch") < page.index('<dl class="meta">')
    css = (site / "assets/css/site.css").read_text(encoding="utf-8")
    assert '.view-switch a[aria-current="page"]' in css


def test_path_controls_are_hidden_without_javascript(tmp_path):
    site = build(tmp_path)
    page = read(site, "polku")
    controls = re.search(r'<div class="path-controls"[^>]*>', page).group(0)
    assert "data-js-only" in controls and " hidden" in controls
    # every button sits inside an element that is hidden without the script
    stripped = re.sub(r"<(div|p|details)[^>]*data-js-only[^>]*hidden[^>]*>.*?</\1>", "", page, flags=re.DOTALL)
    assert "<button" not in stripped
    assert "data-progress" not in stripped
    css = (site / "assets/css/site.css").read_text(encoding="utf-8")
    assert "html:not(.js) [data-js-only]" in css


def test_fi_date_is_d_m_yyyy():
    assert fi_date(date(2026, 5, 2)) == "2.5.2026"
    assert fi_date("2026-05-22") == "22.5.2026"
    assert fi_date("ei päivä") == "ei päivä"


def test_curriculum_page_shows_no_iso_dates_in_text(tmp_path):
    site = build(tmp_path)
    for name in ("opetussuunnitelma", "lahteet", "op1/01-testi", "op1/01-testi/tunti"):
        page = read(site, name)
        text = re.sub(r'datetime="[^"]*"', "", page)
        assert not re.search(r"\b20\d\d-\d\d-\d\d\b", re.sub(r"<[^>]+>", " ", text)), name
    assert re.search(r"julkaisupäivä on \d{1,2}\.\d{1,2}\.\d{4}", read(site, "opetussuunnitelma"))
