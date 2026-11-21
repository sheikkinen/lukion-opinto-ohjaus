"""Tests for pipeline/sitemap.py: fast, no network."""

from datetime import date
from xml.etree import ElementTree

from pipeline import sitemap

NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def make_site(out):
    for directory in ("", "op1", "op1/01-lukio-alkaa", "op1/01-lukio-alkaa/tunti", "tulosta", "tulosta/op1", "polku"):
        target = out / directory / "index.html" if directory else out / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("<html></html>", encoding="utf-8")
    (out / "assets").mkdir()
    (out / "assets" / "index.html").write_text("x", encoding="utf-8")


def test_sitemap_lists_pages_and_leaves_out_print_and_assets(tmp_path):
    make_site(tmp_path)
    count = sitemap.write_sitemap(tmp_path, date(2026, 11, 21), "https://example.test/site")
    root = ElementTree.parse(tmp_path / "sitemap.xml").getroot()
    locs = [e.text for e in root.findall("s:url/s:loc", NS)]
    assert count == len(locs) == 5
    assert locs[0] == "https://example.test/site/"
    assert "https://example.test/site/op1/01-lukio-alkaa/tunti/" in locs
    assert not any("tulosta" in loc or "assets" in loc for loc in locs)
    assert {e.text for e in root.findall("s:url/s:lastmod", NS)} == {"2026-11-21"}


def test_site_url_override_and_trailing_slash(monkeypatch):
    monkeypatch.delenv("LOO_SITE_URL", raising=False)
    assert sitemap.site_url() == sitemap.SITE_URL
    monkeypatch.setenv("LOO_SITE_URL", "https://example.test/x")
    assert sitemap.site_url() == "https://example.test/x/"
    assert sitemap.site_url("https://other.test/") == "https://other.test/"


def test_addresses_are_escaped():
    xml = sitemap.sitemap_xml("https://example.test/", ["a&b/"], date(2026, 1, 1))
    assert "a&amp;b/" in xml
