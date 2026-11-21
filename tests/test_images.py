"""Image tool and placement tests: fake clients, no network, no GPU."""

from __future__ import annotations

import argparse
import io
from collections import namedtuple
from pathlib import Path

import pytest
import yaml
from PIL import Image

from pipeline import images
from pipeline.build import build_site
from pipeline.layout import Ctx
from tests.helpers import TODAY, all_codes_topic, make_root
from tools import images as tool

Adapter = namedtuple("Adapter", "name kind model_id price_usd build")


def fake_adapters():
    def build(prompt, seed, aspect, image):
        return {"prompt": prompt, "seed": seed, "aspect": aspect}

    return {
        ("nano-banana", "create"): Adapter("nano-banana", "create", "google/nano-banana-2.1", 0.0336, build),
        ("klein", "create"): Adapter("klein", "create", "local/flux2-klein-4b", 0.0, build),
    }


class FakeBudget:
    def __init__(self, cap):
        self.cap, self.spent, self.planned = float(cap), 0.0, None

    def plan(self, label, calls, dollars):
        self.planned = (calls, dollars)

    def wave(self, name, calls, dollars):
        if self.spent + dollars > self.cap + 1e-9:
            raise SystemExit("stop: over the cap")
        self.spent += dollars


class Refused(Exception):
    pass


class FakeRouter:
    def __init__(self, refuse=()):
        self.calls, self.refuse, self.closed = [], set(refuse), False

    def run_many(self, jobs, max_parallel=12):
        self.calls.append([job[0] for job in jobs])
        return {key: (Refused("nsfw") if key in self.refuse else png(key)) for key, _, _ in jobs}

    def close(self):
        self.closed = True


def png(seed_text="x", size=(320, 180)):
    shade = sum(map(ord, seed_text)) % 200
    buffer = io.BytesIO()
    Image.new("RGB", size, (shade, 120, 200)).save(buffer, "PNG")
    return buffer.getvalue()


def entry(id_, kind="illustration", model="klein", page="op1-01-testi", placement="header", **extra):
    base = {"id": id_, "kind": kind, "model": model, "aspect": "16:9", "prompt": f"prompt {id_}", "page": page,
            "placement": placement, "alt": f"alt {id_}"}
    if kind == "diagram":
        base["expected_labels"] = ["Yksi", "Kaksi"]
    return base | extra


def write_manifest(root: Path, *entries, style="Calm style."):
    (root / "data").mkdir(exist_ok=True)
    (root / "data" / "images.yaml").write_text(yaml.safe_dump({"style": style, "images": list(entries)}, allow_unicode=True), encoding="utf-8")


def args(**kw):
    base = {"kind": None, "only": None, "redo": None, "max_dollars": 10.0, "per_run": False, "dry_run": False, "host": None}
    return argparse.Namespace(**(base | kw))


def engine(router):
    return tool.Engine(fake_adapters(), FakeBudget, lambda host: router, Refused)


def run_tool(root, router, **kw):
    return tool.run(root, args(**kw), engine(router), today=TODAY)


def log_rows(root):
    return yaml.safe_load((root / "data" / "images.run.yaml").read_text(encoding="utf-8"))


@pytest.fixture
def root(tmp_path):
    (tmp_path / "data").mkdir()
    return tmp_path


def test_makes_webp_and_logs_without_key_or_path(root):
    write_manifest(root, entry("a-diagram", "diagram", "nano-banana"), entry("b-ill"))
    router = FakeRouter()
    assert run_tool(root, router) == 0
    assert router.closed
    for name in ("a-diagram", "b-ill"):
        data = (root / "site-src" / "img" / f"{name}.webp").read_bytes()
        assert data[:4] == b"RIFF" and len(data) < 200_000
    rows = log_rows(root)
    assert [r["id"] for r in rows] == ["a-diagram", "b-ill"]
    assert rows[0]["model"] == "google/nano-banana-2.1" and rows[0]["seed"] is None and rows[0]["dollars"] == 0.0336
    assert rows[1]["seed"] is not None and rows[1]["dollars"] == 0.0 and rows[1]["prompt"].endswith("Calm style.")
    assert rows[0]["prompt"] == "prompt a-diagram"  # a diagram prompt is not given the illustration style
    assert len(rows[0]["sha256"]) == 64 and rows[0]["date"] == "2026-11-21"
    text = (root / "data" / "images.run.yaml").read_text(encoding="utf-8")
    assert str(root) not in text and "r8_" not in text and "Users" not in text


def test_diagrams_go_first_and_kept_pictures_are_not_remade(root):
    write_manifest(root, entry("ill"), entry("dia", "diagram", "nano-banana"))
    router = FakeRouter()
    run_tool(root, router)
    assert router.calls == [["dia"], ["ill"]]
    again = FakeRouter()
    assert run_tool(root, again) == 0
    assert again.calls == []
    assert len(log_rows(root)) == 2


def test_redo_remakes_with_a_new_seed(root):
    write_manifest(root, entry("ill"))
    run_tool(root, FakeRouter())
    router = FakeRouter()
    run_tool(root, router, redo=["ill"])
    first, second = log_rows(root)
    assert router.calls == [["ill"]] and second["seed"] == first["seed"] + 1


def test_only_and_kind_select(root):
    write_manifest(root, entry("a"), entry("b"), entry("c", "diagram", "nano-banana"))
    router = FakeRouter()
    run_tool(root, router, only=["b"])
    assert router.calls == [["b"]]
    router = FakeRouter()
    run_tool(root, router, kind="diagram")
    assert router.calls == [["c"]]
    with pytest.raises(SystemExit):
        run_tool(root, FakeRouter(), only=["nope"])


def test_dry_run_prints_plan_and_calls_nothing(root, capsys):
    write_manifest(root, entry("a", "diagram", "nano-banana"))
    router = FakeRouter()
    assert run_tool(root, router, dry_run=True) == 0
    out = capsys.readouterr().out
    assert "make a" in out and "$0.0336" in out and router.calls == []
    assert not (root / "site-src").exists()


def test_cap_stops_before_the_wave_and_counts_the_log(root):
    write_manifest(root, entry("a", "diagram", "nano-banana"))
    router = FakeRouter()
    with pytest.raises(SystemExit):
        run_tool(root, router, max_dollars=0.01)
    assert router.calls == [] and router.closed
    # the cap counts what the log already holds, unless --per-run
    (root / "data" / "images.run.yaml").write_text(yaml.safe_dump([{"id": "old", "dollars": 9.99}]), encoding="utf-8")
    with pytest.raises(SystemExit):
        run_tool(root, FakeRouter())
    assert run_tool(root, FakeRouter(), per_run=True) == 0


def test_refused_picture_is_reported_and_others_go_on(root, capsys):
    write_manifest(root, entry("bad"), entry("good"))
    assert run_tool(root, FakeRouter(refuse=["bad"])) == 1
    assert "failed bad" in capsys.readouterr().out
    assert [r["id"] for r in log_rows(root)] == ["good"]
    assert not (root / "site-src" / "img" / "bad.webp").exists()


def test_svg_fallback_is_skipped(root):
    write_manifest(root, entry("d", "diagram", "nano-banana", fallback="svg"))
    router = FakeRouter()
    assert run_tool(root, router) == 0 and router.calls == []


def test_invalid_manifest_is_refused(root, capsys):
    write_manifest(root, entry("a", model="sdxl"), {"id": "b"})
    assert run_tool(root, FakeRouter()) == 2
    assert "model must be" in capsys.readouterr().err


def test_to_webp_gets_noisy_pictures_under_the_limit():
    import random

    random.seed(1)
    noise = Image.frombytes("RGB", (900, 500), random.randbytes(900 * 500 * 3))
    buffer = io.BytesIO()
    noise.save(buffer, "PNG")
    data = tool.to_webp(buffer.getvalue())
    assert len(data) <= tool.MAX_BYTES
    assert images.webp_size(data)[0] <= 900


def test_webp_size_reads_lossy_and_lossless():
    for lossless in (True, False):
        buffer = io.BytesIO()
        Image.new("RGB", (123, 45), (9, 9, 9)).save(buffer, "WEBP", lossless=lossless)
        assert images.webp_size(buffer.getvalue()) == (123, 45)
    assert images.svg_size('<svg viewBox="0 0 800 450" xmlns="x"></svg>') == (800, 450)


def test_manifest_rules():
    manifest, errors = images.parse_manifest({"images": [entry("a", "diagram", "nano-banana", expected_labels=[]), entry("a")]})
    assert any("expected_labels" in e for e in errors) and len(manifest.entries) == 1
    _, errors = images.parse_manifest({"images": [entry("x", alt="", decorative=False), entry("y", aspect="4:3")]})
    assert any("alt" in e for e in errors) and any("klein draws" in e for e in errors)
    deco, errors = images.parse_manifest({"images": [entry("z", alt="", decorative=True)]})
    assert not errors and deco.entries[0].alt == ""


def build_with(tmp_path, *entries, make=()):
    root = make_root(tmp_path)
    all_codes_topic(root)
    write_manifest(root, *entries)
    for name in make:
        (root / "site-src" / "img").mkdir(parents=True, exist_ok=True)
        (root / "site-src" / "img" / f"{name}.webp").write_bytes(tool.to_webp(png(name, (640, 360))))
    problems = build_site(root, root / "_site", today=TODAY)
    return root, problems


def test_build_places_header_diagram_front_and_module_pictures(tmp_path):
    root, problems = build_with(
        tmp_path,
        entry("head", alt="Otsikkokuva"),
        entry("dia", "diagram", "nano-banana", placement="Opiskelijalle", alt="Kaavio, jossa Yksi ja Kaksi"),
        entry("front", page="front", alt="", decorative=True),
        entry("mod", page="op1", alt="Moduulin kuva"),
        make=("head", "dia", "front", "mod"),
    )
    assert not [p for p in problems if not p.warning], problems
    site = root / "_site"
    student = (site / "op1" / "01-testi" / "index.html").read_text(encoding="utf-8")
    assert 'alt="Otsikkokuva" width="640" height="360" loading="lazy"' in student
    assert student.index("Otsikkokuva") < student.index('id="opiskelijalle"')
    section = student[student.index('id="opiskelijalle"'):student.index("</section>", student.index('id="opiskelijalle"'))]
    assert 'alt="Kaavio, jossa Yksi ja Kaksi"' in section and "picture-diagram" in section
    assert 'src="../../assets/img/dia.webp"' in student and (site / "assets" / "img" / "dia.webp").exists()
    front = (site / "index.html").read_text(encoding="utf-8")
    assert 'alt="" width="640" height="360" loading="lazy"' in front and 'src="assets/img/front.webp"' in front
    assert 'alt="Moduulin kuva"' in (site / "op1" / "index.html").read_text(encoding="utf-8")
    assert "Otsikkokuva" in (site / "op1" / "01-testi" / "tunti" / "index.html").read_text(encoding="utf-8")


def test_build_warns_for_missing_file_and_fails_for_bad_page(tmp_path):
    _, problems = build_with(tmp_path, entry("nofile"), entry("lost", page="op1-99-ei"), make=("lost",))
    assert any(p.warning and "nofile" in p.message for p in problems)
    assert any(not p.warning and "op1-99-ei" in p.message for p in problems)


def test_build_without_manifest_is_unchanged(tmp_path):
    root = make_root(tmp_path)
    all_codes_topic(root)
    assert not [p for p in build_site(root, root / "_site", today=TODAY) if not p.warning]
    assert "<figure" not in (root / "_site" / "index.html").read_text(encoding="utf-8")


def test_figure_escapes_alt():
    entry_ = images.parse_entry(entry("e", alt='Kuva "x" <b>'), 1)[0]
    html = images.figure(Ctx(""), images.Picture(entry_, "e.webp", 10, 5))
    assert "&quot;x&quot; &lt;b&gt;" in html and "<b>" not in html


def test_manifest_is_read_from_both_files(tmp_path):
    from pipeline.images import load_manifest

    (tmp_path / "data").mkdir()
    write_manifest(tmp_path, entry("a-diagram", "diagram", "nano-banana"))
    (tmp_path / "data" / "images-illustrations.yaml").write_text(yaml.safe_dump({"images": [entry("b-ill")]}), encoding="utf-8")
    manifest, errors = load_manifest(tmp_path)
    assert errors == []
    assert [e.id for e in manifest.entries] == ["a-diagram", "b-ill"]
    assert manifest.style == "Calm style."


def test_diagram_figure_links_to_the_full_image():
    from pipeline.images import Entry, Picture, figure

    class Ctx:
        def asset(self, path):
            return "/" + path

    diagram = Entry("dg-x", "diagram", "nano-banana", "16:9", "p", "op1", "header", alt="Kuvaus", expected_labels=("A",))
    html_ = figure(Ctx(), Picture(diagram, "dg-x.webp", 1200, 675))
    assert 'href="/img/dg-x.webp"' in html_ and "Avaa kuva suurempana" in html_
    ill = Entry("il-x", "illustration", "klein", "16:9", "p", "op1", "header", decorative=True)
    assert "<a " not in figure(Ctx(), Picture(ill, "il-x.webp", 800, 450))


def test_redo_alone_makes_only_the_named_ids(root):
    write_manifest(root, entry("a"), entry("b"), entry("c"))
    router = FakeRouter()
    run_tool(root, router, redo=["b"])
    assert router.calls == [["b"]]


def test_diagram_caps_and_lesson_placement():
    from pipeline.images import Entry, ImageSet, Picture, figure

    class Ctx:
        def asset(self, path):
            return "/" + path

    def diagram(name, w, h, placement="header"):
        return Picture(Entry(name, "diagram", "nano-banana", "1:1", "p", "t1", placement, alt="K", expected_labels=("A",)), name + ".webp", w, h)

    assert "picture-square" in figure(Ctx(), diagram("sq", 1024, 1024))
    assert "picture-compact" in figure(Ctx(), diagram("sm", 1200, 896))
    assert "picture-square" not in figure(Ctx(), diagram("wide", 1376, 768))
    images = ImageSet([diagram("h", 1376, 768), diagram("s", 1376, 768, "lesson-body")])
    html_ = images.diagrams(Ctx(), "t1")
    assert "s.webp" in html_ and "h.webp" not in html_
    assert images.sections(Ctx(), "t1", {}, diagrams=False) == {}
