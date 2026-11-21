from datetime import date

from pipeline import checks
from tests.helpers import PLAN_75, SECTIONS, TODAY, topic_text, write_topic

KNOWN = {"OP1.t1", "OP1.t2", "OP1.s1", "OP2.t1", "OP.yt1"}


def errors(problems):
    return [p for p in problems if not p.warning]


def messages(problems):
    return [p.message for p in problems]


def test_valid_topic_has_no_errors(tmp_path):
    topic = write_topic(tmp_path)
    assert errors(checks.check_topic(topic, KNOWN, {}, TODAY)) == []


def test_unknown_code_is_reported_with_its_line(tmp_path):
    topic = write_topic(tmp_path, curriculum=["OP1.t1", "OP1.t99"])
    problems = checks.check_codes(topic, KNOWN)
    assert len(problems) == 1
    assert "OP1.t99" in problems[0].message
    assert problems[0].line > 1
    assert problems[0].path.endswith("01-testi.md")


def test_malformed_code_is_reported(tmp_path):
    topic = write_topic(tmp_path, curriculum=["foo"])
    assert "malformed" in checks.check_codes(topic, KNOWN)[0].message


def test_codes_may_be_written_as_mappings(tmp_path):
    topic = write_topic(tmp_path, curriculum=[{"code": "OP1.t1", "kind": "tavoite"}])
    assert topic.codes == ["OP1.t1"]


def test_uncovered_codes_are_listed(tmp_path):
    topic = write_topic(tmp_path)
    problems = checks.check_coverage([topic], KNOWN, "data/curriculum.yaml")
    assert sorted(p.message.split()[0] for p in problems) == ["OP.yt1", "OP1.s1", "OP1.t2", "OP2.t1"]


def test_missing_section_is_reported(tmp_path):
    sections = {k: v for k, v in SECTIONS.items() if k != "Pohdinta"}
    topic = write_topic(tmp_path, sections=sections)
    assert any("missing section '## Pohdinta'" in m for m in messages(checks.check_sections(topic)))


def test_out_of_order_section_is_reported(tmp_path):
    keys = list(SECTIONS)
    keys[1], keys[2] = keys[2], keys[1]
    topic = write_topic(tmp_path, sections={k: SECTIONS[k] for k in keys})
    assert any("out of order" in m for m in messages(checks.check_sections(topic)))


def test_generated_sources_section_is_allowed_only_last(tmp_path):
    topic = write_topic(tmp_path, sections={**SECTIONS, "Lähteet": "x"})
    assert checks.check_sections(topic) == []
    topic = write_topic(tmp_path, sections={"Lähteet": "x", **SECTIONS})
    assert any("must be the last" in m for m in messages(checks.check_sections(topic)))


def test_unknown_section_is_reported(tmp_path):
    topic = write_topic(tmp_path, sections={**SECTIONS, "Muuta": "x"})
    assert any("unknown section" in m for m in messages(checks.check_sections(topic)))


def test_lesson_minutes_must_add_up(tmp_path):
    bad = SECTIONS["Tuntisuunnitelma (75 min)"].replace("| 60 | Tehtävä |", "| 55 | Tehtävä |", 1)
    topic = write_topic(tmp_path, sections={**SECTIONS, "Tuntisuunnitelma (75 min)": bad})
    found = checks.check_lesson_minutes(topic)
    assert [p.message for p in found] == ["the 75 min plan adds up to 70 minutes"]


def test_missing_variant_plan_is_reported(tmp_path):
    only_master = PLAN_75
    topic = write_topic(tmp_path, sections={**SECTIONS, "Tuntisuunnitelma (75 min)": only_master})
    found = messages(checks.check_lesson_minutes(topic))
    assert "duration_options lists 45 but there is no 45 min plan" in found


def test_minutes_range_is_rejected(tmp_path):
    bad = PLAN_75.replace("| 10 |", "| 5-10 |")
    sections = {**SECTIONS, "Tuntisuunnitelma (75 min)": bad}
    topic = write_topic(tmp_path, sections=sections, duration_options=[75])
    assert any("one number" in m for m in messages(checks.check_lesson_minutes(topic)))


def test_total_row_is_not_counted(tmp_path):
    plan = PLAN_75 + "| Yhteensä | 75 | |\n"
    topic = write_topic(tmp_path, sections={**SECTIONS, "Tuntisuunnitelma (75 min)": plan}, duration_options=[75])
    assert checks.check_lesson_minutes(topic) == []


def test_link_without_read_date_fails(tmp_path):
    link = {"title": "A", "url": "https://example.org/a", "publisher": "B"}
    topic = write_topic(tmp_path, official_links=[link])
    assert any("no read date" in m for m in messages(checks.check_official_links(topic, TODAY)))


def test_old_link_fails_and_recent_link_passes(tmp_path):
    old = {"title": "A", "url": "https://example.org/a", "publisher": "B", "read": "2025-11-20"}
    topic = write_topic(tmp_path, official_links=[old])
    assert any("12 months" in m for m in messages(checks.check_official_links(topic, TODAY)))
    old["read"] = "2025-11-21"
    topic = write_topic(tmp_path, official_links=[old])
    assert checks.check_official_links(topic, TODAY) == []


def test_future_read_date_fails():
    problems = checks.check_read_date("f.md", 1, "2027-01-01", TODAY, "link")
    assert "future" in problems[0].message


def test_leap_day_today_does_not_crash():
    assert checks.check_read_date("f.md", 1, "2023-03-01", date(2024, 2, 29), "link") == []
    assert checks.check_read_date("f.md", 1, "2023-02-01", date(2024, 2, 29), "link")


def test_body_link_must_be_listed_with_read_date(tmp_path):
    sections = {**SECTIONS, "Opiskelijalle": "Katso [sivu](https://example.org/b) ja [toinen](https://example.org/a/)."}
    topic = write_topic(tmp_path, sections=sections)
    found = checks.check_body_links(topic, {})
    assert len(found) == 1
    assert "example.org/b" in found[0].message


FACTS = {"ytl_exam_dates": {"key": "ytl_exam_dates", "url": "https://example.org/yo", "stable_figures": ["1.12."]}}


def test_figure_outside_link_fails_when_yearly_facts_apply(tmp_path):
    sections = {**SECTIONS, "Opiskelijalle": "Koe on 15.3.2027 ja maksaa 25 euroa. Läpäisee 40 % hakijoista. Vuonna 2027 se muuttuu."}
    topic = write_topic(tmp_path, sections=sections, yearly_facts=["ytl_exam_dates"])
    found = checks.check_yearly_figures(topic, FACTS)
    assert {m.split("'")[0].strip() for m in messages(found)} == {"date", "euro amount", "percentage", "year"}
    assert all(not p.warning for p in found)


def test_figure_inside_link_text_is_allowed(tmp_path):
    text = "Katso [koepäivät 15.3.2027, hinta 25 €](https://example.org/yo)."
    topic = write_topic(tmp_path, sections={**SECTIONS, "Opiskelijalle": text}, yearly_facts=["ytl_exam_dates"])
    assert checks.check_yearly_figures(topic, FACTS) == []


def test_stable_figure_is_exempt(tmp_path):
    text = "Ilmoittaudu viimeistään 1.12. mennessä."
    topic = write_topic(tmp_path, sections={**SECTIONS, "Opiskelijalle": text}, yearly_facts=["ytl_exam_dates"])
    assert checks.check_yearly_figures(topic, FACTS) == []


def test_figure_without_yearly_facts_is_only_a_warning(tmp_path):
    topic = write_topic(tmp_path, sections={**SECTIONS, "Opiskelijalle": "Hinta on 25 euroa."})
    found = checks.check_yearly_figures(topic, {})
    assert found
    assert all(p.warning for p in found)


def test_minutes_and_curriculum_codes_are_not_figures(tmp_path):
    text = "Tehtävä kestää 20 min. Koodi OP1.t6 ja 3. vaihe ja 2019 perusteet."
    topic = write_topic(tmp_path, sections={**SECTIONS, "Opiskelijalle": text}, yearly_facts=["ytl_exam_dates"])
    assert checks.check_yearly_figures(topic, FACTS) == []


def test_figures_in_generated_sources_section_are_ignored(tmp_path):
    sections = {**SECTIONS, "Lähteet": "Luettu 21.11.2026"}
    topic = write_topic(tmp_path, sections=sections, yearly_facts=["ytl_exam_dates"])
    assert checks.check_yearly_figures(topic, FACTS) == []


def test_unknown_yearly_fact_key_is_reported(tmp_path):
    topic = write_topic(tmp_path, yearly_facts=["nope"])
    assert len(checks.check_yearly_fact_keys(topic, FACTS)) == 1
    assert checks.check_yearly_fact_keys(topic, None) == []


def test_missing_front_matter_key_stops_other_checks(tmp_path):
    text = topic_text().replace("summary: Yksi lause.\n", "")
    path = tmp_path / "content" / "topics" / "01-testi.md"
    path.parent.mkdir(parents=True)
    path.write_text(text, encoding="utf-8")
    from pipeline.loaders import load_document
    from pipeline.models import Topic

    topic = load_document(path, tmp_path, Topic)
    found = checks.check_topic(topic, KNOWN, {}, TODAY)
    assert messages(found) == ["front matter key 'summary' is missing"]


def test_id_must_match_file_name(tmp_path):
    topic = write_topic(tmp_path, id="op1-99-muu")
    assert any(p.message.startswith("id:") for p in checks.check_front_matter(topic))


def test_duplicate_order_and_id_are_reported(tmp_path):
    first = write_topic(tmp_path, "01-testi")
    second = write_topic(tmp_path, "02-testi", id="op1-02-testi")
    found = messages(checks.check_unique([first, second]))
    assert len(found) == 1
    assert "order 1" in found[0]


def test_facts_file_needs_dates_and_fields():
    facts = {"a": {"key": "a", "rule": "r", "url": "https://x.fi", "publisher": "p", "read": "2020-01-01"}}
    assert any("12 months" in m for m in messages(checks.check_facts_file(facts, TODAY)))
    facts = {"a": {"key": "a", "rule": "r"}}
    assert len(checks.check_facts_file(facts, TODAY)) == 3
