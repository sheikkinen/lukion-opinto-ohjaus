from pipeline import checks


def page(body: str, head: str = "") -> str:
    return f'<!doctype html><html lang="fi"><head><meta charset="utf-8"><title>t</title>{head}</head><body>{body}</body></html>'


def write(site, name, text):
    path = site / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_plain_external_link_is_allowed(tmp_path):
    write(tmp_path, "index.html", page('<h1>A</h1><a href="https://example.org/">x</a>'))
    assert checks.check_external_resources(tmp_path) == []


def test_external_script_font_image_and_iframe_fail(tmp_path):
    head = '<script src="https://cdn.example.org/a.js"></script><link rel="stylesheet" href="//fonts.example.org/f.css">'
    body = '<h1>A</h1><img src="https://example.org/i.png" alt=""><iframe src="https://example.org/"></iframe>'
    write(tmp_path, "index.html", page(body, head))
    found = checks.check_external_resources(tmp_path)
    assert len(found) == 4
    assert all(p.path == "_site/index.html" and p.line >= 1 for p in found)


def test_external_url_in_css_and_js_files_fails(tmp_path):
    write(tmp_path, "a.css", "body { background: url(https://example.org/a.png); }\n")
    write(tmp_path, "b.css", '@import "x.css";\n')
    write(tmp_path, "c.js", "fetch('https://example.org');\n")
    write(tmp_path, "ok.css", "a { color: red; }\n")
    assert len(checks.check_external_resources(tmp_path)) == 3


def test_internal_links_and_anchors_are_checked(tmp_path):
    write(tmp_path, "index.html", page('<h1>A</h1><a href="op1/">a</a><a href="op1/#x">b</a><a href="op1/#nope">c</a><a href="gone/">d</a>'))
    write(tmp_path, "op1/index.html", page('<h1>B</h1><h2 id="x">X</h2><a href="../">home</a><a href="#x">self</a>'))
    found = checks.check_internal_links_and_headings(tmp_path)
    assert sorted(p.message for p in found) == ["broken internal link gone/", "link op1/#nope points to a missing anchor"]


def test_heading_order_and_single_h1(tmp_path):
    write(tmp_path, "index.html", page("<h1>A</h1><h3>skipped</h3>"))
    write(tmp_path, "two/index.html", page("<h1>A</h1><h1>B</h1>"))
    messages = [p.message for p in checks.check_internal_links_and_headings(tmp_path)]
    assert "heading order jumps from h1 to h3" in messages
    assert "page has 2 h1 headings, expected 1" in messages


def test_image_without_alt_and_link_without_text(tmp_path):
    write(tmp_path, "index.html", page('<h1>A</h1><img src="a.png"><a href="#"></a>'))
    messages = [p.message for p in checks.check_internal_links_and_headings(tmp_path)]
    assert "image without alt text" in messages
    assert "link without text" in messages
