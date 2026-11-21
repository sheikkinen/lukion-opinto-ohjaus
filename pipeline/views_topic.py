"""The student view and the lesson view of a topic, and the generated Lähteet block."""

from __future__ import annotations

from pipeline.layout import Ctx, SiteData, code_id, esc, render_page, topic_label
from pipeline.markdown_render import render_markdown, shift_headings
from pipeline.models import Section, Topic, as_date, fi_date

SECTION_IDS = {
    "Opiskelijalle": "opiskelijalle",
    "Tehtävät": "tehtavat",
    "Pohdinta": "pohdinta",
    "Itseopiskelun askel": "itseopiskelun-askel",
    "Tuntisuunnitelma": "tuntisuunnitelma",
    "Eriyttäminen": "eriyttaminen",
    "Milloin opinto-ohjaajalle": "milloin-opinto-ohjaajalle",
}
STUDENT_SECTIONS = ("Opiskelijalle", "Tehtävät", "Pohdinta", "Itseopiskelun askel", "Milloin opinto-ohjaajalle")
LESSON_SECTIONS = ("Tuntisuunnitelma", "Eriyttäminen")
ROLE_LABELS = {"core": "ydinaihe", "extension": "laajennus"}


def time_tag(value: object) -> str:
    parsed = as_date(value)
    iso = f' datetime="{parsed.isoformat()}"' if parsed else ""
    return f"<time{iso}>{esc(fi_date(value))}</time>"


def timing_text(topic: Topic) -> str:
    timing = topic.meta.get("suggested_timing") or {}
    return f"{timing.get('year')}. vuosi, {timing.get('term')} (esimerkki, koulu päättää)"


def render_section(section: Section, ident: str) -> str:
    body = render_markdown(section.text)
    return f'<section id="{ident}" class="topic-section">\n<h2>{esc(section.title)}</h2>\n{body}\n</section>'


def render_named_sections(topic: Topic, names: tuple[str, ...]) -> str:
    parts = []
    for name in names:
        section = topic.section(name)
        if section is not None:
            parts.append(render_section(section, SECTION_IDS[name]))
    return "\n".join(parts)


def code_href(ctx: Ctx, code: str) -> str:
    module = code.split(".")[0]
    return ctx.link("opetussuunnitelma" if module == "OP" else module.lower(), code_id(code))


def curriculum_box(ctx: Ctx, data: SiteData, topic: Topic) -> str:
    items = []
    for code in topic.codes:
        entry = data.codes.get(code)
        if entry is None:
            continue
        link = f'<a href="{code_href(ctx, code)}">{esc(code)}</a>'
        items.append(f"<dt>{link}</dt>\n<dd>{esc(entry['text'])}</dd>")
    law = "".join(f"<li>{esc(item)}</li>" for item in topic.meta.get("law") or [])
    law_html = f"<h3>Laki</h3>\n<ul>{law}</ul>" if law else ""
    return (
        '<section id="opetussuunnitelma" class="box">\n<h2>Opetussuunnitelma: tämä aihe palvelee</h2>\n'
        "<p>Sanamuoto on Lukion opetussuunnitelman perusteista 2019 sellaisenaan.</p>\n"
        f'<dl class="codes">\n{chr(10).join(items)}\n</dl>\n{law_html}\n</section>'
    )


def sources_block(ctx: Ctx, data: SiteData, topic: Topic) -> str:
    """The Lähteet section, generated from the front matter and never written by hand."""
    parts = ['<section id="lahteet" class="topic-section">', "<h2>Lähteet</h2>"]
    codes = []
    for code in topic.codes:
        entry = data.codes.get(code)
        if entry:
            codes.append(f'<dt><a href="{code_href(ctx, code)}">{esc(code)}</a></dt>\n<dd>{esc(entry["text"])}</dd>')
    source = data.curriculum["source"]
    parts.append("<h3>Opetussuunnitelman perusteet</h3>")
    parts.append(f"<p>{esc(source['name'])}, {esc(source['diaarinumero'])}. Tarkistettu {time_tag(source['checked'])}.</p>")
    parts.append(f'<dl class="codes">\n{chr(10).join(codes)}\n</dl>')
    if topic.meta.get("law"):
        items = "".join(f"<li>{esc(item)}</li>" for item in topic.meta["law"])
        parts.append(f"<h3>Laki</h3>\n<ul>{items}</ul>")
    if topic.official_links:
        parts.append("<h3>Viralliset lähteet</h3>\n<ul>")
        for link in topic.official_links:
            parts.append(
                f'<li><a href="{esc(link["url"])}" rel="noopener noreferrer">{esc(link["title"])}</a>, '
                f"{esc(link['publisher'])}. Luettu {time_tag(link.get('read'))}.</li>"
            )
        parts.append("</ul>")
    parts.append(yearly_facts_list(topic, data))
    parts.append("</section>")
    return "\n".join(p for p in parts if p)


def yearly_facts_list(topic: Topic, data: SiteData) -> str:
    if not topic.yearly_fact_keys:
        return ""
    items = []
    for key in topic.yearly_fact_keys:
        fact = data.facts.get(key)
        if fact is None:
            items.append(f"<li>{esc(key)}</li>")
            continue
        items.append(
            f"<li>{esc(fact.get('rule', key))} "
            f'<a href="{esc(fact.get("url", ""))}" rel="noopener noreferrer">'
            f"Tarkista ajantasainen tieto: {esc(fact.get('publisher', ''))}</a>. "
            f"Luettu {time_tag(fact.get('read'))}.</li>"
        )
    return f"<h3>Muuttuu vuosittain</h3>\n<p>Näitä tietoja ei kopioida tälle sivulle. Katso arvo virallisesta lähteestä.</p>\n<ul>{''.join(items)}</ul>"


def meta_list(ctx: Ctx, data: SiteData, topic: Topic, lesson: bool) -> str:
    rows = [("Moduuli", f'<a href="{ctx.link(topic.module.lower())}">{esc(topic.module)}</a>')]
    rows.append(("Ajoitus", esc(timing_text(topic))))
    rows.append(("Rooli", esc(ROLE_LABELS.get(topic.meta.get("role"), ""))))
    if lesson:
        rows.append(("Tunnin pituus", esc(", ".join(f"{d} min" for d in sorted(topic.durations)))))
        if topic.meta.get("materials"):
            rows.append(("Tarvikkeet", esc("; ".join(map(str, topic.meta["materials"])))))
    else:
        rows.append(("Itseopiskelu", esc(f"noin {topic.meta.get('self_study_minutes')} min")))
    if topic.meta.get("hops_part"):
        rows.append(("HOPS-osa", esc(topic.meta["hops_part"])))
    before = [data.topics_by_id[p] for p in topic.meta.get("prerequisites") or [] if p in data.topics_by_id]
    if before:
        links = ", ".join(f'<a href="{ctx.link(p.url_dir)}">{esc(p.title)}</a>' for p in before)
        rows.append(("Ennen tätä", links))
    cells = "\n".join(f"<div><dt>{label}</dt><dd>{value}</dd></div>" for label, value in rows)
    return f'<dl class="meta">\n{cells}\n</dl>'


def view_switch(ctx: Ctx, topic: Topic, current: str) -> str:
    student = f'<a href="{ctx.link(topic.url_dir)}"{_current(current == "student")}>Opiskelijan näkymä</a>'
    lesson = f'<a href="{ctx.link(topic.url_dir + "/tunti")}"{_current(current == "lesson")}>Tuntisuunnitelma opinto-ohjaajalle</a>'
    return f'<nav class="view-switch" aria-label="Näkymät"><ul><li>{student}</li><li>{lesson}</li></ul></nav>'


def _current(active: bool) -> str:
    return ' aria-current="page"' if active else ""


def neighbours(ctx: Ctx, data: SiteData, topic: Topic, suffix: str) -> str:
    index = data.topics.index(topic)
    items = []
    if index > 0:
        before = data.topics[index - 1]
        items.append(f'<li class="prev"><a href="{ctx.link(before.url_dir + suffix)}">Edellinen: {esc(before.title)}</a></li>')
    if index < len(data.topics) - 1:
        after = data.topics[index + 1]
        items.append(f'<li class="next"><a href="{ctx.link(after.url_dir + suffix)}">Seuraava: {esc(after.title)}</a></li>')
    return f'<nav class="pager" aria-label="Aiheiden välillä"><ul>{"".join(items)}</ul></nav>' if items else ""


def tick_block(ctx: Ctx, topic: Topic) -> str:
    return (
        '<p class="tick" data-js-only hidden>'
        f'<button type="button" class="button" data-step-toggle="{esc(topic.id)}" aria-pressed="false">Merkitse tehdyksi</button> '
        '<span class="hint">Merkintä tallentuu vain tähän selaimeen, kun painat painiketta. '
        f'<a href="{ctx.link("polku")}">Itseopiskelupolku ja omien tietojen tyhjennys</a></span></p>'
    )


def student_page(data: SiteData, topic: Topic) -> str:
    ctx = Ctx(topic.url_dir)
    parts = [
        f'<article class="topic student-view">\n<p class="kicker">Aihe {topic_label(topic)}</p>',
        f"<h1>{esc(topic.title)}</h1>",
        f'<p class="summary">{esc(topic.meta.get("summary", ""))}</p>',
        meta_list(ctx, data, topic, lesson=False),
        view_switch(ctx, topic, "student"),
    ]
    for name in STUDENT_SECTIONS:
        parts.append(render_named_sections(topic, (name,)))
        if name == "Itseopiskelun askel":
            parts.append(tick_block(ctx, topic))
    parts += [sources_block(ctx, data, topic), neighbours(ctx, data, topic, ""), "</article>"]
    return render_page(
        data,
        ctx,
        topic.title,
        "\n".join(parts),
        str(topic.meta.get("summary", "")),
        current=topic.module.lower(),
        scripts=True,
    )


def lesson_body(ctx: Ctx, data: SiteData, topic: Topic, full_sources: bool) -> str:
    """The lesson view without the page heading, used alone and in the print pages."""
    parts = [meta_list(ctx, data, topic, lesson=True)]
    adapts = topic.meta.get("school_adapts") or []
    if adapts:
        items = "".join(f"<li>{esc(item)}</li>" for item in adapts)
        parts.append(f'<section id="koulu-paattaa" class="box">\n<h2>Koulu päättää (esimerkki)</h2>\n<ul>{items}</ul>\n</section>')
    parts.append(curriculum_box(ctx, data, topic))
    parts.append(render_named_sections(topic, LESSON_SECTIONS))
    parts.append(sources_block(ctx, data, topic) if full_sources else "")
    return "\n".join(p for p in parts if p)


def lesson_page(data: SiteData, topic: Topic) -> str:
    ctx = Ctx(topic.url_dir + "/tunti")
    parts = [
        f'<article class="topic lesson-view">\n<p class="kicker">Aihe {topic_label(topic)} · opinto-ohjaajalle</p>',
        f"<h1>{esc(topic.title)}: tuntisuunnitelma</h1>",
        f'<p class="summary">{esc(topic.meta.get("summary", ""))}</p>',
        view_switch(ctx, topic, "lesson"),
        lesson_body(ctx, data, topic, full_sources=True),
        neighbours(ctx, data, topic, "/tunti"),
        "</article>",
    ]
    description = f"Tuntisuunnitelma: {topic.title}"
    return render_page(data, ctx, f"{topic.title}: tuntisuunnitelma", "\n".join(parts), description, current=topic.module.lower())


def print_article(ctx: Ctx, data: SiteData, topic: Topic) -> str:
    """One topic's lesson plan inside a combined print page (headings one level down)."""
    inner = shift_headings(lesson_body(ctx, data, topic, full_sources=False), 1)
    inner = inner.replace(' id="', f' id="{topic.slug}-')  # ids stay unique on the combined page
    codes = ", ".join(esc(c) for c in topic.codes)
    return (
        f'<article class="print-topic" id="{esc(topic.slug)}">\n<h2>{topic_label(topic)} {esc(topic.title)}</h2>\n'
        f'<p class="summary">{esc(topic.meta.get("summary", ""))}</p>\n'
        f'<p class="codes-line">Opetussuunnitelman koodit: {codes}.</p>\n{inner}\n</article>'
    )
