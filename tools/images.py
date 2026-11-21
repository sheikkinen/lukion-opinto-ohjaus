"""Make the site's pictures from data/images*.yaml with game-engine's pimage modules (read-only, imported by path).

    python tools/images.py [--kind diagram|illustration] [--only ID ...] [--redo ID ...] [--max-dollars 10]
                           [--dry-run] [--per-run] [--host hosts/NAME.yaml]

nano-banana pictures go through Replicate (pimage's ReplicateClient; the key is read by pimage's read_token and is
never printed). klein pictures go through pimage's clients.make_api, which takes game-engine's GPU lock and starts
ComfyUI itself. The planned calls and dollars are printed first; a wave that would pass --max-dollars is not started.
By default the cap counts what data/images.run.yaml already records (the whole brief's cap); --per-run counts this
run only. A picture already made is kept unless it is named in --redo. Output: site-src/img/<id>.webp (under 200 KB)
and one appended entry per picture in data/images.run.yaml (id, model, prompt, seed, sha256, dollars, date).
"""

from __future__ import annotations

import argparse
import hashlib
import io
import os
import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline.images import IMG_DIR, RUN_LOG, Entry, Manifest, load_manifest  # noqa: E402

GAME_ENGINE = Path(os.environ.get("GAME_ENGINE_DIR", "game-engine-not-set"))  # the game-engine checkout
MAX_BYTES = 195_000  # the brief says under 200 KB; stay clear of the line
LOSSY_QUALITIES = (92, 85, 78, 70, 62, 54, 46, 38)
NO_SEED = ("nano-banana",)  # models that take no seed; the run log records null
WAVE_SIZE = 8  # calls per budget wave


@dataclass
class Engine:
    """What the tool takes from game-engine, so tests can pass fakes."""

    adapters: dict  # {(model name, "create"): Adapter(name, model_id, price_usd, build, ...)}
    budget_cls: type  # budget.Budget: plan(label, calls, dollars) and wave(name, calls, dollars)
    make_router: Callable[[str | None], object]  # host file path or None -> a router with run_many and close
    refused: type  # the Refused class of replicate_client


@dataclass
class Job:
    entry: Entry
    adapter: object
    prompt: str
    seed: int
    model_input: dict

    @property
    def dollars(self) -> float:
        return float(self.adapter.price_usd)


def load_engine() -> Engine:
    """Import pimage by path (appended last so this project's own names win) and wire its router."""
    pimage = GAME_ENGINE / "tools" / "pimage"
    if not pimage.is_dir():
        raise SystemExit("stop: game-engine's tools/pimage was not found (set GAME_ENGINE_DIR)")
    if str(pimage) not in sys.path:
        sys.path.append(str(pimage))
    import budget
    import clients
    import models
    import replicate_client

    def replicate() -> object:
        token = replicate_client.read_token()
        if not token:
            raise SystemExit("stop: no Replicate token (pimage's read_token found none in the environment or game-engine's .env)")
        return replicate_client.ReplicateClient(token)

    def make_router(host: str | None) -> object:
        return clients.make_api(host, GAME_ENGINE, replicate)

    return Engine(models.ADAPTERS, budget.Budget, make_router, replicate_client.Refused)


def base_seed(entry_id: str) -> int:
    return int(hashlib.sha256(entry_id.encode()).hexdigest()[:8], 16) % 2**31


def read_log(root: Path) -> list[dict]:
    path = root / RUN_LOG
    if not path.exists():
        return []
    return yaml.safe_load(path.read_text(encoding="utf-8")) or []


def final_prompt(entry: Entry, style: str) -> str:
    """Illustrations carry the style line; a diagram's prompt is already exact."""
    return f"{entry.prompt} {style}".strip() if entry.kind == "illustration" else entry.prompt


def select(manifest: Manifest, root: Path, kind: str | None, only: list[str], redo: list[str]) -> tuple[list[Entry], list[str]]:
    """The entries to make, and the ids kept as they are. Unknown ids stop the run."""
    known = manifest.by_id()
    unknown = [i for i in only + redo if i not in known]
    if unknown:
        raise SystemExit(f"stop: no such picture id in data/images*.yaml: {', '.join(unknown)}")
    named = only + redo  # --redo alone names the whole run; it never widens to every missing picture
    wanted = [e for e in manifest.entries if (not named or e.id in named) and (kind is None or e.kind == kind)]
    wanted += [known[i] for i in redo if known[i] not in wanted and (kind is None or known[i].kind == kind)]
    make, kept = [], []
    for entry in wanted:
        made = (root / IMG_DIR / f"{entry.id}.webp").exists() and entry.id not in redo
        if entry.fallback == "svg" or made:
            kept.append(entry.id)
        else:
            make.append(entry)
    return make, kept


def make_jobs(entries: list[Entry], style: str, log: list[dict], engine: Engine) -> list[Job]:
    jobs = []
    for entry in entries:
        adapter = engine.adapters[(entry.model, "create")]
        tries = sum(1 for row in log if row.get("id") == entry.id)
        seed = (entry.seed if entry.seed is not None else base_seed(entry.id)) + tries  # a redo draws a new picture
        prompt = final_prompt(entry, style)
        jobs.append(Job(entry, adapter, prompt, seed, adapter.build(prompt, seed, entry.aspect, None)))
    return jobs


def to_webp(png: bytes, limit: int = MAX_BYTES) -> bytes:
    """WebP under `limit` bytes: lossless first (crisp text in diagrams), then lossy, then smaller."""
    from PIL import Image

    image = Image.open(io.BytesIO(png))
    image.load()
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGBA" if "transparency" in image.info else "RGB")
    while True:
        for lossless, qualities in ((True, (100,)), (False, LOSSY_QUALITIES)):
            for quality in qualities:
                buffer = io.BytesIO()
                image.save(buffer, "WEBP", lossless=lossless, quality=quality, method=6)
                if buffer.tell() <= limit:
                    return buffer.getvalue()
        if image.width < 480:
            raise ValueError(f"cannot get a {image.width}x{image.height} picture under {limit} bytes")
        image = image.resize((round(image.width * 0.85), round(image.height * 0.85)), Image.Resampling.LANCZOS)


def print_plan(jobs: list[Job], kept: list[str], budget: object, total: float) -> None:
    for job in jobs:
        e = job.entry
        print(f"  make {e.id}: {e.kind}, {job.adapter.name} {e.aspect}, ${job.dollars:.4f}")
    if kept:
        print(f"  kept as they are ({len(kept)}): {', '.join(kept)}")
    budget.plan("images", len(jobs), total)


def waves(jobs: list[Job]) -> list[tuple[str, list[Job]]]:
    """Diagrams (paid, remote) first, then the local illustrations; remote waves hold at most WAVE_SIZE calls."""
    ordered = sorted(jobs, key=lambda j: (j.adapter.price_usd == 0, j.entry.kind != "diagram"))
    result: list[tuple[str, list[Job]]] = []
    for job in ordered:
        if not result or result[-1][1][0].adapter.name != job.adapter.name or len(result[-1][1]) >= WAVE_SIZE:
            result.append((f"{job.adapter.name} {len(result) + 1}", []))
        result[-1][1].append(job)
    return result


def record(root: Path, job: Job, data: bytes, today: date) -> None:
    row = {
        "id": job.entry.id,
        "model": job.adapter.model_id,
        "prompt": job.prompt,
        "seed": None if job.adapter.name in NO_SEED else job.seed,
        "sha256": hashlib.sha256(data).hexdigest(),
        "dollars": job.dollars,
        "date": today.isoformat(),
    }
    path = root / RUN_LOG
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(yaml.safe_dump([row], allow_unicode=True, sort_keys=False, width=1000))


def run_wave(root: Path, router: object, batch: list[Job], today: date) -> list[str]:
    """Run one wave; returns the failures. Each picture is written and logged as soon as it is back."""
    results = router.run_many([(job.entry.id, job.adapter.model_id, job.model_input) for job in batch])
    failures = []
    for job in batch:
        result = results.get(job.entry.id)
        if not isinstance(result, bytes | bytearray):
            reason = str(result)[:200] if result is not None else "no answer"
            print(f"  failed {job.entry.id}: {reason}")
            failures.append(job.entry.id)
            continue
        try:
            data = to_webp(bytes(result))
        except (ValueError, OSError) as error:
            print(f"  failed {job.entry.id}: cannot convert: {error}")
            failures.append(job.entry.id)
            continue
        target = root / IMG_DIR / f"{job.entry.id}.webp"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        record(root, job, data, today)
        print(f"  made {job.entry.id}: {len(data) // 1024} KB, ${job.dollars:.4f}")
    return failures


def run(root: Path, args: argparse.Namespace, engine: Engine, today: date | None = None) -> int:
    today = today or date.today()
    manifest, errors = load_manifest(root)
    if errors:
        print("\n".join(f"data/images*.yaml: {e}" for e in errors), file=sys.stderr)
        return 2
    if not manifest.entries:
        print("data/images*.yaml does not exist or has no pictures yet")
        return 2
    entries, kept = select(manifest, root, args.kind, args.only or [], args.redo or [])
    log = read_log(root)
    jobs = make_jobs(entries, manifest.style, log, engine)
    total = sum(j.dollars for j in jobs)
    budget = engine.budget_cls(args.max_dollars)
    if not args.per_run:
        budget.spent = sum(float(row.get("dollars") or 0) for row in log)
        print(f"already spent according to {RUN_LOG}: ${budget.spent:.4f}")
    print_plan(jobs, kept, budget, total)
    if args.dry_run or not jobs:
        return 0
    router = engine.make_router(args.host)
    failures: list[str] = []
    try:
        for name, batch in waves(jobs):
            budget.wave(name, len(batch), sum(j.dollars for j in batch))
            failures += run_wave(root, router, batch, today)
    finally:
        router.close()
    print(f"done: {len(jobs) - len(failures)} made, {len(failures)} failed, about ${budget.spent:.4f} counted")
    return 1 if failures else 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--kind", choices=("diagram", "illustration"))
    parser.add_argument("--only", nargs="+", metavar="ID", help="make only these ids")
    parser.add_argument("--redo", nargs="+", metavar="ID", help="make these ids again even if their file exists")
    parser.add_argument("--max-dollars", type=float, default=10.0, metavar="USD", help="cap, default 10")
    parser.add_argument("--per-run", action="store_true", help="count only this run against the cap, not the run log")
    parser.add_argument("--dry-run", action="store_true", help="print the plan and stop")
    parser.add_argument("--host", help="game-engine host file (default hosts/<machine>.yaml there)")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return run(args.root, args, load_engine())


if __name__ == "__main__":
    sys.exit(main())
