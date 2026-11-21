"""sitemap.xml for the built site: every page's address, from the written index.html files.

The print pages (/tulosta/) repeat the lesson plans, so they are left out. The base address is the GitHub Pages
address unless LOO_SITE_URL or --site-url names another.
"""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

SITE_URL = "https://sheikkinen.github.io/lukion-opinto-ohjaus/"
LEFT_OUT = ("tulosta",)


def site_url(override: str | None = None) -> str:
    """The site's base address, always ending in a slash."""
    url = override or os.environ.get("LOO_SITE_URL") or SITE_URL
    return url if url.endswith("/") else url + "/"


def page_paths(out: Path) -> list[str]:
    """The page directories under out that hold an index.html, as URL paths ('' for the front page), sorted."""
    paths = []
    for index in out.rglob("index.html"):
        relative = index.parent.relative_to(out).as_posix()
        path = "" if relative == "." else relative + "/"
        if path.split("/", 1)[0] in LEFT_OUT or path.startswith("assets/"):
            continue
        paths.append(path)
    return sorted(paths, key=lambda p: (p.count("/"), p))


def sitemap_xml(base: str, paths: list[str], built: date) -> str:
    """The sitemap document for these paths under base, with the build date as lastmod."""
    rows = [
        f"  <url><loc>{escape(base + path)}</loc><lastmod>{built.isoformat()}</lastmod></url>"
        for path in paths
    ]
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )


def write_sitemap(out: Path, built: date, base: str | None = None) -> int:
    """Write out/sitemap.xml and return the number of addresses in it."""
    paths = page_paths(out)
    (out / "sitemap.xml").write_text(sitemap_xml(site_url(base), paths, built), encoding="utf-8", newline="\n")
    return len(paths)
