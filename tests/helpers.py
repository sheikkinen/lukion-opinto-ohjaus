"""Builders for fixtures: a small topic, a fake ePerusteet answer and a fake site root."""

from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path

import yaml

from pipeline.fetch_curriculum import SUBJECT_ID, parse_curriculum
from pipeline.loaders import load_document
from pipeline.models import Topic

REPO = Path(__file__).resolve().parent.parent
TODAY = date(2026, 11, 21)

PLAN_75 = """| Vaihe | Min | Toiminta |
|---|---|---|
| Virittäytyminen | 5 | Alku |
| Työskentely | 60 | Tehtävä |
| Päätös | 10 | Exit |
"""
PLAN_60 = PLAN_75.replace("| 60 |", "| 45 |")
PLAN_45 = PLAN_75.replace("| 60 |", "| 30 |")

SECTIONS = {
    "Opiskelijalle": "Osaan suunnitella.",
    "Tehtävät": "### Tehtävä 1\n1. Tee jotain.",
    "Pohdinta": "Mitä mietit?",
    "Itseopiskelun askel": "Lue ja tee.",
    "Tuntisuunnitelma (75 min)": PLAN_75 + "\n### 60 min\n" + PLAN_60 + "\n### 45 min\n" + PLAN_45,
    "Eriyttäminen": "Helpompi ja syvempi polku.",
    "Milloin opinto-ohjaajalle": "Kun on kiire.",
}


def topic_text(sections: dict[str, str] | None = None, **meta_overrides: object) -> str:
    meta = {
        "id": "op1-01-testi",
        "module": "OP1",
        "order": 1,
        "title": "Testiaihe",
        "summary": "Yksi lause.",
        "curriculum": ["OP1.t1"],
        "suggested_timing": {"year": 1, "term": "syksy"},
        "role": "core",
        "duration_options": [45, 60, 75],
        "self_study_minutes": 20,
        "prerequisites": [],
        "official_links": [
            {"title": "Sivu", "url": "https://example.org/a", "publisher": "Testaaja", "read": "2026-11-21"},
        ],
        "yearly_facts": [],
        "school_adapts": ["Aikataulu"],
        "materials": ["Paperi"],
        "accessibility": "Toimii ilman laitetta",
        "last_reviewed": "2026-11-21",
    }
    meta.update(meta_overrides)
    body = sections or SECTIONS
    parts = ["---", yaml.safe_dump(meta, allow_unicode=True, sort_keys=False).rstrip(), "---", ""]
    for title, text in body.items():
        parts += [f"## {title}", "", text, ""]
    return "\n".join(parts)


def write_topic(root: Path, name: str = "01-testi", **kwargs: object) -> Topic:
    path = root / "content" / "topics" / f"{name}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(topic_text(**kwargs), encoding="utf-8")
    return load_document(path, root, Topic)


def fake_api_answer() -> dict:
    """An ePerusteet answer with the code counts the contract fixes (9/8, 10/8, 11)."""

    def text(value: str) -> dict:
        return {"fi": f"<p>{value}</p>"}

    def module(module_id: int, name: str, objectives: int, contents: int) -> dict:
        return {
            "id": module_id,
            "nimi": text(name + " "),
            "pakollinen": True,
            "laajuus": 2,
            "tavoitteet": {
                "kohde": text("Moduulin tavoitteena on, että opiskelija"),
                "tavoitteet": [text(f"{name} tavoite {n}") for n in range(1, objectives + 1)],
            },
            "sisallot": [{"kohde": None, "sisallot": [text(f"{name} sisältö {n}") for n in range(1, contents + 1)]}],
        }

    subject = {
        "id": SUBJECT_ID,
        "nimi": text("Opinto-ohjaus"),
        "arviointi": {"kuvaus": text("Ei arvosanaa.") | {"fi": "<p>Ei arvosanaa.</p>\n<p> </p>"}},
        "tavoitteet": {
            "tavoitealueet": [
                {
                    "nimi": text("Tavoitteena on, että"),
                    "kohde": text("opiskelija"),
                    "tavoitteet": [text(f"yleinen {n}") for n in range(1, 12)],
                }
            ]
        },
        "moduulit": [module(6835293, "Yksi", 9, 8), module(6835294, "Kaksi", 10, 8)],
    }
    return {
        "diaarinumero": "OPH-TEST",
        "nimi": text("Testiperusteet"),
        "voimassaoloAlkaa": 1627765200000,
        "viimeisinJulkaisuAika": 1779433019269,
        "lops2019": {"oppiaineet": [subject]},
    }


def make_root(tmp_path: Path, with_pages: bool = True, with_facts: bool = True) -> Path:
    """A site root with curriculum, the real templates, assets and static pages."""
    root = tmp_path / "site-root"
    (root / "data").mkdir(parents=True)
    curriculum = parse_curriculum(fake_api_answer(), TODAY)
    (root / "data" / "curriculum.yaml").write_text(yaml.safe_dump(curriculum, allow_unicode=True), encoding="utf-8")
    shutil.copytree(REPO / "templates", root / "templates")
    shutil.copytree(REPO / "site-src", root / "site-src")
    if with_facts:
        fact = {"key": "ytl_exam_dates", "rule": "Koepäivät", "url": "https://example.org/yo", "publisher": "YTL", "read": "2026-11-21"}
        (root / "data" / "yearly-facts.yaml").write_text(yaml.safe_dump([fact], allow_unicode=True), encoding="utf-8")
    if with_pages:
        shutil.copytree(REPO / "content" / "pages", root / "content" / "pages")
    return root


def all_codes_topic(root: Path) -> Topic:
    """One topic that serves every code, so that the coverage check passes."""
    codes = list(yaml.safe_load((root / "data" / "curriculum.yaml").read_text(encoding="utf-8"))["codes"])
    return write_topic(root, curriculum=codes)
