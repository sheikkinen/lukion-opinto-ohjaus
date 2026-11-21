from datetime import date

import pytest

from pipeline import loaders, markdown_render
from pipeline.fetch_curriculum import (
    CurriculumError,
    clean_paragraphs,
    clean_text,
    millis_to_date,
    parse_curriculum,
)
from pipeline.layout import Ctx
from pipeline.models import as_date, fi_date
from tests.helpers import TODAY, fake_api_answer


def test_front_matter_split_gives_line_numbers():
    meta, front, body, start = loaders.split_front_matter("---\na: 1\nb: 2\n---\nteksti\n")
    assert meta == {"a": 1, "b": 2}
    assert front == ["a: 1", "b: 2"]
    assert body == ["teksti"]
    assert start == 5


@pytest.mark.parametrize("text", ["ei front matteria", "---\na: 1\n", "---\n- a\n---\n", "---\na: [\n---\n"])
def test_front_matter_errors(text):
    with pytest.raises(ValueError):
        loaders.split_front_matter(text)


def test_sections_ignore_headings_inside_code_fences():
    lines = ["intro", "## Yksi", "a", "```", "## ei otsikko", "```", "## Kaksi", "b"]
    sections = loaders.split_sections(lines, 10)
    assert [(s.title, s.line) for s in sections] == [("Yksi", 11), ("Kaksi", 16)]
    assert "## ei otsikko" in sections[0].text


def test_yearly_facts_accept_three_shapes():
    entry = {"key": "a", "rule": "r"}
    assert loaders.normalise_facts([entry]) == {"a": entry}
    assert loaders.normalise_facts({"facts": [entry]}) == {"a": entry}
    assert loaders.normalise_facts({"a": {"rule": "r"}}) == {"a": {"rule": "r", "key": "a"}}


def test_missing_facts_file_is_none(tmp_path):
    assert loaders.load_yearly_facts(tmp_path) is None


def test_bad_topic_file_becomes_a_problem(tmp_path):
    directory = tmp_path / "content" / "topics"
    directory.mkdir(parents=True)
    (directory / "01-x.md").write_text("ei front matteria", encoding="utf-8")
    topics, problems = loaders.load_topics(tmp_path)
    assert topics == []
    assert problems[0].path == "content/topics/01-x.md"


def test_dates():
    assert as_date("2026-11-21") == date(2026, 11, 21)
    assert as_date("21.11.2026") is None
    assert fi_date("2026-11-21") == "21.11.2026"
    assert fi_date(date(2026, 1, 5)) == "5.1.2026"


def test_relative_links_work_from_any_depth():
    assert Ctx("").link("op1") == "op1/"
    assert Ctx("").link("") == "./"
    assert Ctx("op1/07-x").link("op1") == "../"
    assert Ctx("op1/07-x/tunti").link("op1/07-x") == "../"
    assert Ctx("op1/07-x/tunti").link("polku", "alku") == "../../../polku/#alku"
    assert Ctx("op1").asset("css/site.css") == "../assets/css/site.css"
    assert Ctx("").asset("css/site.css") == "assets/css/site.css"


def test_table_cells_get_labels_and_headers_scope():
    out = markdown_render.render_markdown("| A | B |\n|---|---|\n| 1 | 2 |\n")
    assert '<td data-label="A">1</td>' in out
    assert '<th scope="col">B</th>' in out
    assert out.startswith('<div class="table-wrap" role="region" aria-label="Taulukko" tabindex="0">')


def test_headings_shift_down_but_stop_at_h6():
    assert markdown_render.shift_headings("<h2>a</h2><h5 id='x'>b</h5>", 1) == "<h3>a</h3><h6 id='x'>b</h6>"
    assert markdown_render.shift_headings("<h6>a</h6>", 2) == "<h6>a</h6>"


def test_external_links_get_rel():
    out = markdown_render.render_markdown("[a](https://example.org) [b](../x/)")
    assert 'rel="noopener noreferrer"' in out
    assert out.count("rel=") == 1


def test_block_tokens_are_replaced_by_generated_html():
    out = markdown_render.render_with_blocks("Alku\n\n{{box}}\n\nLoppu\n", {"box": lambda: "<p>BOX</p>"})
    assert out.index("Alku") < out.index("BOX") < out.index("Loppu")
    with pytest.raises(KeyError):
        markdown_render.render_with_blocks("{{missing}}\n", {})


def test_clean_text_strips_html_and_entities():
    assert clean_text("<p>Tuntee&nbsp;<b>lukion</b>\n  käytänteet &amp; rakenteen</p>") == "Tuntee lukion käytänteet & rakenteen"
    assert clean_paragraphs("<p>Yksi</p>\n\n<p> </p><p>Kaksi</p>") == ["Yksi", "Kaksi"]
    assert clean_text(None) == ""


def test_publication_date_uses_finnish_calendar_day():
    assert millis_to_date(1627765200000) == date(2021, 8, 1)  # 21:00 UTC is already 1 August in Finland
    assert millis_to_date(1779433019269) == date(2026, 5, 22)
    assert millis_to_date(1767218400000) == date(2026, 1, 1)  # 22:00 UTC on 31 Dec, winter time


def test_parse_curriculum_keys_codes_in_order():
    data = parse_curriculum(fake_api_answer(), TODAY)
    codes = list(data["codes"])
    assert len(codes) == 46
    assert codes[0] == "OP.yt1"
    assert codes[10] == "OP.yt11"
    assert codes.index("OP1.t9") < codes.index("OP1.s1") < codes.index("OP2.t1")
    assert data["codes"]["OP1.t1"]["text"] == "Yksi tavoite 1"
    assert data["modules"]["OP1"]["name"] == "Yksi"
    assert data["modules"]["OP2"]["credits"] == 2
    assert data["subject"]["assessment"] == ["Ei arvosanaa."]
    assert data["source"]["last_published"] == "2026-05-22"
    assert data["source"]["checked"] == "2026-11-21"


def test_parse_curriculum_fails_when_counts_change():
    answer = fake_api_answer()
    answer["lops2019"]["oppiaineet"][0]["moduulit"][0]["tavoitteet"]["tavoitteet"].pop()
    with pytest.raises(CurriculumError, match=r"OP1\.t"):
        parse_curriculum(answer, TODAY)
