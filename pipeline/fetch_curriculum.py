"""Fetch the national core curriculum for guidance (OP) from the ePerusteet API.

Writes data/curriculum.yaml with the exact Finnish wording keyed by code:
OP1.t1-t9, OP1.s1-s8, OP2.t1-t10, OP2.s1-s8 and OP.yt1-yt11, in ePerusteet order.
HTML is stripped here, at the boundary; nothing downstream sees markup.

Usage: python -m pipeline.fetch_curriculum [--input saved.json] [--output data/curriculum.yaml]
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import yaml

PERUSTE_ID = 6828810
API_URL = f"https://eperusteet.opintopolku.fi/eperusteet-service/api/perusteet/{PERUSTE_ID}/kaikki"
SUBJECT_ID = 6835370
MODULE_IDS = {"OP1": 6835293, "OP2": 6835294}
EXPECTED_COUNTS = {"OP1.t": 9, "OP1.s": 8, "OP2.t": 10, "OP2.s": 8, "OP.yt": 11}
MAX_TRIES = 2

_BLOCK_END = re.compile(r"</(p|div|li|h[1-6])>|<br\s*/?>", re.IGNORECASE)
_TAG = re.compile(r"<[^>]+>")


class CurriculumError(Exception):
    """The API answer does not have the shape the contract expects."""


def clean_paragraphs(raw: str | None) -> list[str]:
    """Strip HTML; return the non-empty paragraphs with whitespace collapsed."""
    if not raw:
        return []
    text = _BLOCK_END.sub("\n", re.sub(r"\s+", " ", raw))
    text = html.unescape(_TAG.sub("", text)).replace("\xa0", " ")
    paragraphs = (re.sub(r"\s+", " ", line).strip() for line in text.split("\n"))
    return [p for p in paragraphs if p]


def clean_text(raw: str | None) -> str:
    return "\n\n".join(clean_paragraphs(raw))


def finnish(node: dict | None) -> str:
    """The Finnish text of an ePerusteet localised string."""
    if not node:
        return ""
    return clean_text(node.get("fi"))


def _last_sunday_utc(year: int, month: int) -> datetime:
    """01:00 UTC on the last Sunday of the month, when EU summer time changes."""
    day = datetime(year, month + 1, 1, 1, tzinfo=UTC) if month < 12 else datetime(year + 1, 1, 1, 1, tzinfo=UTC)
    day -= timedelta(days=1)
    return day - timedelta(days=(day.weekday() + 1) % 7)


def millis_to_date(millis: int) -> date:
    """The calendar date in Finland. Computed by hand so that no tz database is needed."""
    moment = datetime.fromtimestamp(millis / 1000, tz=UTC)
    summer = _last_sunday_utc(moment.year, 3) <= moment < _last_sunday_utc(moment.year, 10)
    return (moment + timedelta(hours=3 if summer else 2)).date()


def _find_by_id(items: list[dict], wanted: int, what: str) -> dict:
    for item in items:
        if item.get("id") == wanted:
            return item
    raise CurriculumError(f"{what} {wanted} not found in the API answer")


def _module_codes(prefix: str, module: dict) -> dict[str, dict]:
    codes: dict[str, dict] = {}
    objectives = [finnish(o) for o in module["tavoitteet"]["tavoitteet"]]
    contents = [finnish(c) for group in module["sisallot"] for c in group["sisallot"]]
    for number, text in enumerate(objectives, 1):
        codes[f"{prefix}.t{number}"] = {"kind": "tavoite", "module": prefix, "text": text}
    for number, text in enumerate(contents, 1):
        codes[f"{prefix}.s{number}"] = {"kind": "sisalto", "module": prefix, "text": text}
    return codes


def _sort_key(code: str) -> tuple:
    group = {"OP1": 1, "OP2": 2, "OP": 0}[code.split(".")[0]]
    kind = re.sub(r"\d+$", "", code.split(".")[1])
    number = int(re.search(r"\d+$", code).group())
    return (group, {"yt": 0, "t": 1, "s": 2}[kind], number)


def _check_counts(codes: dict[str, dict]) -> None:
    for prefix, expected in EXPECTED_COUNTS.items():
        found = sum(1 for c in codes if re.fullmatch(re.escape(prefix) + r"\d+", c))
        if found != expected:
            raise CurriculumError(f"{prefix}: expected {expected} codes, found {found}. The curriculum changed: update docs/content-contract.md first.")


def parse_curriculum(data: dict, checked: date) -> dict:
    """Turn the raw ePerusteet record into the structure of data/curriculum.yaml."""
    subject = _find_by_id(data["lops2019"]["oppiaineet"], SUBJECT_ID, "oppiaine")
    codes: dict[str, dict] = {}
    aims_lead = ""
    number = 0
    for area in subject["tavoitteet"]["tavoitealueet"]:
        if not aims_lead:
            aims_lead = f"{finnish(area.get('nimi'))} {finnish(area.get('kohde'))}".strip()
        for aim in area["tavoitteet"]:
            number += 1
            codes[f"OP.yt{number}"] = {"kind": "yleinen_tavoite", "module": "OP", "text": finnish(aim)}
    assessment = clean_paragraphs(((subject.get("arviointi") or {}).get("kuvaus") or {}).get("fi"))
    modules: dict[str, dict] = {}
    for prefix, module_id in MODULE_IDS.items():
        module = _find_by_id(subject["moduulit"], module_id, "module")
        codes.update(_module_codes(prefix, module))
        modules[prefix] = {
            "id": module_id,
            "name": finnish(module["nimi"]),
            "credits": module["laajuus"],
            "mandatory": bool(module["pakollinen"]),
            "objectives_lead": finnish(module["tavoitteet"].get("kohde")),
        }
    _check_counts(codes)
    ordered = dict(sorted(codes.items(), key=lambda item: _sort_key(item[0])))
    return {
        "source": {
            "peruste_id": PERUSTE_ID,
            "diaarinumero": data["diaarinumero"],
            "name": finnish(data.get("nimi")),
            "in_force_from": millis_to_date(data["voimassaoloAlkaa"]).isoformat(),
            "last_published": millis_to_date(data["viimeisinJulkaisuAika"]).isoformat(),
            "checked": checked.isoformat(),
            "api_url": API_URL,
        },
        "subject": {
            "id": SUBJECT_ID,
            "code": "OP",
            "name": finnish(subject["nimi"]),
            "aims_lead": aims_lead,
            "assessment": assessment,
        },
        "modules": modules,
        "codes": ordered,
    }


def download(url: str = API_URL) -> dict:
    """Download the record. At most two tries; no further retries."""
    last_error: Exception | None = None
    for _ in range(MAX_TRIES):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "lukion-opinto-ohjaus-build"})
            with urllib.request.urlopen(request, timeout=90) as response:
                return json.load(response)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
            last_error = error
    raise CurriculumError(f"Could not read {url} in {MAX_TRIES} tries: {last_error}")


def write_curriculum(curriculum: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    header = "# Generated by pipeline/fetch_curriculum.py from the ePerusteet API. Do not edit by hand.\n"
    body = yaml.safe_dump(curriculum, allow_unicode=True, sort_keys=False, width=100000)
    output.write_text(header + body, encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="parse a saved API answer instead of downloading")
    parser.add_argument("--output", type=Path, default=Path("data/curriculum.yaml"))
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.input.read_text(encoding="utf-8")) if args.input else download()
        curriculum = parse_curriculum(data, date.today())
    except (CurriculumError, KeyError) as error:
        print(f"fetch_curriculum: {error}", file=sys.stderr)
        return 1
    write_curriculum(curriculum, args.output)
    print(f"wrote {args.output} ({len(curriculum['codes'])} codes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
