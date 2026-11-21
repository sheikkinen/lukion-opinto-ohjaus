"""The picture manifest (data/images.yaml) and where the build places each picture.

The manifest (split over the files in MANIFEST_PARTS) is read by tools/images.py (to make the pictures) and by the build (to place them). A picture is
placed only when its file site-src/img/<id>.webp (or .svg) exists, so a partly made set still builds.

Schema: a top-level `style` line (added to every illustration prompt) and `images`, a list of entries with
id, kind (diagram | illustration), model (nano-banana | klein | p-image), aspect, prompt, page (a topic id, or front, op1,
op2), placement (header, or the H2 section the picture belongs to, by name or by id), alt (Finnish) or
`decorative: true` (then alt=""), and for diagrams expected_labels and facts_from. Optional: seed, fallback: svg.
"""

from __future__ import annotations

import html
import re
import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

from pipeline.models import Problem

if TYPE_CHECKING:
    from pipeline.layout import Ctx

KINDS = ("diagram", "illustration")
MODELS = ("nano-banana", "klein", "p-image")  # p-image: D-009, E: full so klein cannot run
KLEIN_ASPECTS = ("9:16", "3:4", "16:9", "1:1")  # the sizes game-engine's klein.py can draw
PAGE_KEYS = ("front", "op1", "op2")
MANIFEST = "data/images.yaml"
MANIFEST_PARTS = (MANIFEST, "data/images-illustrations.yaml")  # the style line and diagrams, then the illustrations
IMG_DIR = "site-src/img"
RUN_LOG = "data/images.run.yaml"
REQUIRED = ("id", "kind", "model", "aspect", "prompt", "page", "placement")


@dataclass(frozen=True)
class Entry:
    id: str
    kind: str
    model: str
    aspect: str
    prompt: str
    page: str
    placement: str
    alt: str = ""
    decorative: bool = False
    expected_labels: tuple[str, ...] = ()
    facts_from: str = ""
    fallback: str = ""
    seed: int | None = None


@dataclass
class Manifest:
    style: str = ""
    entries: list[Entry] = field(default_factory=list)

    def by_id(self) -> dict[str, Entry]:
        return {e.id: e for e in self.entries}


def parse_entry(raw: object, position: int) -> tuple[Entry | None, list[str]]:
    """One manifest entry, or the reasons it is not valid."""
    if not isinstance(raw, dict):
        return None, [f"entry {position} is not a mapping"]
    name = raw.get("id") or f"entry {position}"
    errors = [f"{name}: missing {key}" for key in REQUIRED if not raw.get(key)]
    if raw.get("kind") and raw["kind"] not in KINDS:
        errors.append(f"{name}: kind must be one of {', '.join(KINDS)}")
    if raw.get("model") and raw["model"] not in MODELS:
        errors.append(f"{name}: model must be one of {', '.join(MODELS)}")
    if raw.get("model") == "klein" and raw.get("aspect") and str(raw["aspect"]) not in KLEIN_ASPECTS:
        errors.append(f"{name}: klein draws only {', '.join(KLEIN_ASPECTS)}")
    decorative = bool(raw.get("decorative"))
    if not decorative and not str(raw.get("alt") or "").strip():
        errors.append(f"{name}: needs an alt text, or decorative: true")
    labels = tuple(str(x) for x in raw.get("expected_labels") or [])
    if raw.get("kind") == "diagram" and not labels:
        errors.append(f"{name}: a diagram needs expected_labels")
    if errors:
        return None, errors
    seed = raw.get("seed")
    entry = Entry(
        id=str(raw["id"]), kind=raw["kind"], model=raw["model"], aspect=str(raw["aspect"]), prompt=str(raw["prompt"]).strip(),
        page=str(raw["page"]), placement=str(raw["placement"]), alt="" if decorative else str(raw["alt"]).strip(),
        decorative=decorative, expected_labels=labels, facts_from=str(raw.get("facts_from") or ""),
        fallback=str(raw.get("fallback") or ""), seed=seed if isinstance(seed, int) else None,
    )
    return entry, []


def parse_manifest(data: object) -> tuple[Manifest, list[str]]:
    if not isinstance(data, dict) or not isinstance(data.get("images"), list):
        return Manifest(), ["the manifest needs a top-level `images` list"]
    manifest, errors, seen = Manifest(style=str(data.get("style") or "").strip()), [], set()
    for position, raw in enumerate(data["images"], 1):
        entry, problems = parse_entry(raw, position)
        errors += problems
        if entry is None:
            continue
        if entry.id in seen:
            errors.append(f"{entry.id}: id used twice")
        seen.add(entry.id)
        manifest.entries.append(entry)
    return manifest, errors


def load_manifest(root: Path) -> tuple[Manifest, list[str]]:
    """The manifest from all its files (each stays under the 500-line limit); the first `style` line wins."""
    merged: dict = {"images": []}
    found = False
    for name in MANIFEST_PARTS:
        path = root / name
        if not path.exists():
            continue
        found = True
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or not isinstance(data.get("images"), list):
            return Manifest(), [f"{name}: needs a top-level `images` list"]
        merged["style"] = merged.get("style") or data.get("style")
        merged["images"] += data["images"]
    return parse_manifest(merged) if found else (Manifest(), [])


def webp_size(data: bytes) -> tuple[int, int]:
    """Width and height from a WebP header (lossy, lossless or extended)."""
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        raise ValueError("not a WebP file")
    kind = data[12:16]
    if kind == b"VP8 ":
        width, height = struct.unpack("<HH", data[26:30])
        return width & 0x3FFF, height & 0x3FFF
    if kind == b"VP8L":
        bits = int.from_bytes(data[21:25], "little")
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if kind == b"VP8X":
        return int.from_bytes(data[24:27], "little") + 1, int.from_bytes(data[27:30], "little") + 1
    raise ValueError("unknown WebP chunk")


def svg_size(text: str) -> tuple[int, int]:
    box = re.search(r'viewBox="\s*[-\d.]+[ ,]+[-\d.]+[ ,]+([\d.]+)[ ,]+([\d.]+)', text)
    if box:
        return round(float(box.group(1))), round(float(box.group(2)))
    sizes = [re.search(rf'<svg[^>]*\s{name}="([\d.]+)', text) for name in ("width", "height")]
    if all(sizes):
        return round(float(sizes[0].group(1))), round(float(sizes[1].group(1)))
    raise ValueError("svg without viewBox or size")


def image_file(root: Path, image_id: str) -> Path | None:
    for suffix in (".webp", ".svg"):
        path = root / IMG_DIR / f"{image_id}{suffix}"
        if path.exists():
            return path
    return None


def file_size(path: Path) -> tuple[int, int]:
    if path.suffix == ".svg":
        return svg_size(path.read_text(encoding="utf-8"))
    return webp_size(path.read_bytes())


@dataclass(frozen=True)
class Picture:
    entry: Entry
    filename: str
    width: int
    height: int

    @property
    def placement(self) -> str:
        return self.entry.placement


class ImageSet:
    """The pictures that have a file, ready to place."""

    def __init__(self, pictures: list[Picture] | None = None) -> None:
        self.pictures = pictures or []

    def on_page(self, page: str) -> list[Picture]:
        return [p for p in self.pictures if p.entry.page == page]

    def header(self, ctx: Ctx, page: str) -> str:
        return "".join(figure(ctx, p) for p in self.on_page(page) if p.placement == "header")

    def diagrams(self, ctx: Ctx, page: str) -> str:
        """The page's diagrams that are not in the header, as figures (the lesson view shows them after the curriculum box)."""
        return "".join(figure(ctx, p) for p in self.on_page(page) if p.entry.kind == "diagram" and p.placement != "header")

    def sections(self, ctx: Ctx, page: str, idents: dict[str, str], diagrams: bool = True) -> dict[str, str]:
        """{section id: figures}; `idents` maps a section name to its id so a placement may use either.
        With diagrams=False the diagrams are left out (the lesson view shows them in one place, see `diagrams`)."""
        found: dict[str, str] = {}
        for pic in self.on_page(page):
            if pic.placement != "header" and (diagrams or pic.entry.kind != "diagram"):
                ident = idents.get(pic.placement, pic.placement)
                found[ident] = found.get(ident, "") + figure(ctx, pic)
        return found


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def figure(ctx: Ctx, pic: Picture) -> str:
    """A picture. A diagram links to its full-size file, so a phone user can open and zoom it (WCAG 1.4.4, 1.4.10)."""
    entry = pic.entry
    href = esc(ctx.asset("img/" + pic.filename))
    img = f'<img src="{href}" alt="{esc(entry.alt)}" width="{pic.width}" height="{pic.height}" loading="lazy">'
    if entry.kind != "diagram":
        return f'<figure class="picture picture-{entry.kind}">{img}</figure>'
    caption = f'<figcaption><a href="{href}">Avaa kuva suurempana</a> (kuva avautuu omalle sivulleen, ja sitä voi lähentää)</figcaption>'
    ratio = pic.width / pic.height
    shape = " picture-square" if ratio <= 1.1 else " picture-compact" if ratio < 1.5 else ""  # CSS caps the displayed width
    return f'<figure class="picture picture-diagram{shape}">{img}{caption}</figure>'


def load_images(root: Path) -> tuple[ImageSet, list[Problem]]:
    """The picture set for a build, and the problems found in the manifest and its files."""
    manifest, errors = load_manifest(root)
    problems = [Problem(MANIFEST, 1, message, "images") for message in errors]
    pictures = []
    for entry in manifest.entries:
        path = image_file(root, entry.id)
        if path is None:
            if not entry.fallback:
                problems.append(Problem(MANIFEST, 1, f"{entry.id}: no picture file yet", "images", warning=True))
            continue
        try:
            width, height = file_size(path)
        except (ValueError, OSError, struct.error) as error:
            problems.append(Problem(f"{IMG_DIR}/{path.name}", 1, f"cannot read the picture size: {error}", "images"))
            continue
        pictures.append(Picture(entry, path.name, width, height))
    return ImageSet(pictures), problems


def check_pages(images: ImageSet, topic_ids: set[str], section_names: dict[str, set[str]]) -> list[Problem]:
    """Every picture goes to a page and section that exist. `section_names` is {topic id: names and ids}."""
    problems = []
    for pic in images.pictures:
        entry = pic.entry
        if entry.page not in PAGE_KEYS and entry.page not in topic_ids:
            problems.append(Problem(MANIFEST, 1, f"{entry.id}: page {entry.page!r} is not front, op1, op2 or a topic id", "images"))
        elif entry.placement != "header" and entry.page in topic_ids and entry.placement not in section_names.get(entry.page, set()):
            problems.append(Problem(MANIFEST, 1, f"{entry.id}: section {entry.placement!r} not found in {entry.page}", "images"))
        elif entry.placement != "header" and entry.page in PAGE_KEYS:
            problems.append(Problem(MANIFEST, 1, f"{entry.id}: only a topic can place a picture at a section", "images"))
    return problems
