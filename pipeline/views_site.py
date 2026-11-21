"""Module pages, print pages and the generated blocks of the static pages."""

from __future__ import annotations

from pipeline.layout import Ctx, SiteData, code_id, esc, render_page, topic_label
from pipeline.markdown_render import label_tables, render_with_blocks, replace_tokens
from pipeline.models import Document, Topic
from pipeline.views_topic import ROLE_LABELS, print_article, time_tag, timing_text

MODULE_TITLE = "{code} {name}"


def module_title(data: SiteData, module: str) -> str:
    return MODULE_TITLE.format(code=module, name=data.curriculum["modules"][module]["name"])


def topic_link(ctx: Ctx, topic: Topic, suffix: str = "", text: str | None = None) -> str:
    label = text if text is not None else f"{topic_label(topic)} {topic.title}"
    return f'<a href="{ctx.link(topic.url_dir + suffix)}">{esc(label)}</a>'


def codes_list(ctx: Ctx, data: SiteData, module: str, kind: str) -> str:
    """The exact objectives or contents of a module, each with the topics that serve it."""
    items = []
    for code, entry in data.codes.items():
        if entry["module"] != module or entry["kind"] != kind:
            continue
        serving = data.serving(code)
        if serving:
            served = ", ".join(topic_link(ctx, t, text=topic_label(t)) for t in serving)
            note = f'<span class="served">Aiheet: {served}</span>'
        else:
            note = '<span class="served">Ei vielä aihetta</span>'
        items.append(f'<li id="{code_id(code)}"><span class="code">{esc(code)}</span> <span class="wording">{esc(entry["text"])}</span> {note}</li>')
    return f'<ul class="codelist">\n{chr(10).join(items)}\n</ul>'


def coverage_matrix(ctx: Ctx, data: SiteData, module: str) -> str:
    topics = data.module_topics(module)
    head = "".join(
        f'<th scope="col"><a href="{ctx.link(t.url_dir)}"><span aria-hidden="true">{t.order}</span>'
        f'<span class="sr-only">Aihe {topic_label(t)}: {esc(t.title)}</span></a></th>'
        for t in topics
    )
    rows = []
    for code, entry in data.codes.items():
        if entry["module"] != module:
            continue
        serving = data.serving(code)
        cells = "".join(
            '<td class="yes"><span aria-hidden="true">●</span><span class="sr-only">kattaa</span></td>'
            if t in serving
            else '<td class="no"><span aria-hidden="true">·</span><span class="sr-only">ei kata</span></td>'
            for t in topics
        )
        others = ", ".join(topic_link(ctx, t, text=f"{t.module} {topic_label(t)}") for t in serving if t.module != module)
        rows.append(f'<tr><th scope="row"><a href="#{code_id(code)}">{esc(code)}</a></th>{cells}<td>{others}</td></tr>')
    caption = f"Opetussuunnitelman koodit ({module}) ja aiheet, jotka niitä palvelevat"
    return (
        '<div class="matrix-wrap" role="region" aria-label="Kattavuustaulukko" tabindex="0">\n'
        f'<table class="matrix"><caption>{esc(caption)}</caption>\n'
        f'<thead><tr><th scope="col">Koodi</th>{head}<th scope="col">Muu moduuli</th></tr></thead>\n'
        f"<tbody>\n{chr(10).join(rows)}\n</tbody></table>\n</div>"
    )


def topic_cards(ctx: Ctx, data: SiteData, module: str) -> str:
    topics = data.module_topics(module)
    if not topics:
        return "<p>Aiheita ei ole vielä julkaistu.</p>"
    items = []
    for topic in topics:
        durations = ", ".join(str(d) for d in sorted(topic.durations))
        items.append(
            f'<li class="topic-card"><h3>{topic_link(ctx, topic)}</h3>\n'
            f"<p>{esc(topic.meta.get('summary', ''))}</p>\n"
            f'<p class="small">{esc(timing_text(topic))} · {esc(ROLE_LABELS.get(topic.meta.get("role"), ""))} · '
            f"tunti {esc(durations)} min · itseopiskelu noin {esc(topic.meta.get('self_study_minutes'))} min</p>\n"
            f'<p class="links">{topic_link(ctx, topic, text="Opiskelijan näkymä")} '
            f"{topic_link(ctx, topic, '/tunti', 'Tuntisuunnitelma')}</p></li>"
        )
    return f'<ol class="topic-list">\n{chr(10).join(items)}\n</ol>'


def module_page(data: SiteData, module: str) -> str:
    ctx = Ctx(module.lower())
    info = data.curriculum["modules"][module]
    subject = data.curriculum["subject"]
    status = "pakollinen" if info["mandatory"] else "valinnainen"
    assessment = "".join(f"<p>{esc(p)}</p>" for p in subject["assessment"])
    main = f"""<article class="module">
<p class="kicker">Moduuli</p>
<h1>{esc(module_title(data, module))}</h1>
{data.images.header(ctx, module.lower())}<dl class="meta">
<div><dt>Laajuus</dt><dd>{esc(info["credits"])} opintopistettä, {status}</dd></div>
<div><dt>Arviointi</dt><dd>suoritusmerkintä (S tai H), ei arvosanaa</dd></div>
<div><dt>Aiheita</dt><dd>{len(data.module_topics(module))}</dd></div>
</dl>
<section id="aiheet"><h2>Aiheet</h2>
<p>Jokainen aihe on yksi oppitunti ja yksi itseopiskelun askel. Ajoitukset ovat esimerkkejä: koulu päättää.</p>
{topic_cards(ctx, data, module)}
</section>
<section id="tavoitteet"><h2>Tavoitteet</h2>
<p>{esc(info["objectives_lead"])}</p>
{codes_list(ctx, data, module, "tavoite")}
</section>
<section id="sisallot"><h2>Keskeiset sisällöt</h2>
{codes_list(ctx, data, module, "sisalto")}
</section>
<section id="kattavuus"><h2>Kattavuus</h2>
<p>Taulukko näyttää, mikä aihe palvelee mitäkin tavoitetta ja sisältöä. Sanamuoto on opetussuunnitelman perusteista sellaisenaan.</p>
{coverage_matrix(ctx, data, module)}
</section>
<section id="arviointi"><h2>Arviointi</h2>
{assessment}
<p>Lähde: <a href="{ctx.link("lahteet")}">Lukion opetussuunnitelman perusteet 2019, tarkistettu {esc(data.checked)}</a>.</p>
</section>
</article>"""
    description = f"{module_title(data, module)}: aiheet, tavoitteet, sisällöt ja kattavuus."
    return render_page(data, ctx, module_title(data, module), main, description, current=module.lower())


def print_page(data: SiteData, module: str) -> str:
    ctx = Ctx(f"tulosta/{module.lower()}")
    topics = data.module_topics(module)
    toc = "".join(f'<li><a href="#{esc(t.slug)}">{topic_label(t)} {esc(t.title)}</a></li>' for t in topics)
    articles = "\n".join(print_article(ctx, data, t) for t in topics) or "<p>Aiheita ei ole vielä julkaistu.</p>"
    main = f"""<article class="print-module">
<h1>Tuntisuunnitelmat: {esc(module_title(data, module))}</h1>
<p class="no-print">Tulosta sivu selaimen tulostustoiminnolla. Jokainen aihe alkaa uudelta sivulta.
Aikataulut ovat esimerkkejä: koulu päättää.</p>
<nav aria-label="Sisällys" class="no-print"><ol class="toc">{toc}</ol></nav>
{articles}
</article>"""
    return render_page(
        data,
        ctx,
        f"Tulosta: {module_title(data, module)}",
        main,
        "Kaikki moduulin tuntisuunnitelmat tulostettavana.",
        body_class="print-view",
    )


def print_index(data: SiteData) -> str:
    ctx = Ctx("tulosta")
    items = "".join(f'<li><a href="{ctx.link("tulosta/" + m.lower())}">{esc(module_title(data, m))}: kaikki tuntisuunnitelmat</a></li>' for m in ("OP1", "OP2"))
    main = f"<article>\n<h1>Tulosta tuntisuunnitelmat</h1>\n<ul>{items}</ul>\n</article>"
    return render_page(data, ctx, "Tulosta tuntisuunnitelmat", main, "Tulostettavat tuntisuunnitelmat.")


def doors(ctx: Ctx, data: SiteData) -> str:
    modules = " ".join(f'<a class="button" href="{ctx.link(m.lower())}">{esc(module_title(data, m))}</a>' for m in ("OP1", "OP2"))
    return f"""<div class="doors">
<section class="door" aria-labelledby="ovi-ohjaaja"><h2 id="ovi-ohjaaja">Opinto-ohjaajalle</h2>
<p>Valmiita tuntisuunnitelmia 75, 60 ja 45 minuutille. Jokaisessa on opetussuunnitelman kohta, tehtävät ja eriyttämisen tuki.</p>
<p class="actions">{modules} <a class="button secondary" href="{ctx.link("tulosta")}">Tulosta tuntisuunnitelmat</a></p></section>
<section class="door" aria-labelledby="ovi-opiskelija"><h2 id="ovi-opiskelija">Opiskelijalle</h2>
<p>Voit edetä itseopiskelupolulla omaan tahtiisi. Merkinnät ja muistiinpanot jäävät vain omalle laitteellesi.</p>
<p class="actions"><a class="button" href="{ctx.link("polku")}">Aloita itseopiskelupolku</a></p></section>
</div>"""


def module_cards(ctx: Ctx, data: SiteData) -> str:
    cards = []
    for module in ("OP1", "OP2"):
        info = data.curriculum["modules"][module]
        count = len(data.module_topics(module))
        cards.append(
            f'<li class="card"><h3><a href="{ctx.link(module.lower())}">{esc(module_title(data, module))}</a></h3>\n'
            f"<p>{esc(info['credits'])} opintopistettä, pakollinen. {count} aihetta.</p></li>"
        )
    return f'<ul class="cards">\n{chr(10).join(cards)}\n</ul>'


def path_controls(data: SiteData) -> str:
    return f"""<div class="path-controls" data-js-only hidden>
<p data-progress data-total="{len(data.topics)}" aria-live="polite"></p>
<p><button type="button" class="button secondary" data-print-notes>Tulosta omat muistiinpanot</button>
<button type="button" class="button danger" data-clear-data>Tyhjennä tietoni</button></p>
<p class="status" data-storage-status role="status"></p>
</div>"""


def path_list(ctx: Ctx, data: SiteData) -> str:
    if not data.topics:
        return "<p>Aiheita ei ole vielä julkaistu.</p>"
    items = []
    for topic in data.topics:
        ident = esc(topic.id)
        items.append(
            f'<li class="path-step" data-step="{ident}">\n'
            f'<h3><span class="num">{topic_label(topic)}</span> {topic_link(ctx, topic, text=topic.title)}</h3>\n'
            f"<p>{esc(topic.meta.get('summary', ''))}</p>\n"
            f'<p class="small">{esc(topic.module)} · {esc(timing_text(topic))} · noin {esc(topic.meta.get("self_study_minutes"))} min</p>\n'
            f'<p data-js-only hidden><button type="button" class="button" data-step-toggle="{ident}" aria-pressed="false">Merkitse tehdyksi</button></p>\n'
            f"<details data-js-only hidden><summary>Oma muistiinpano</summary>\n"
            f'<label for="note-{ident}">Muistiinpano (jää vain tälle laitteelle)</label>\n'
            f'<textarea id="note-{ident}" rows="4" data-note-for="{ident}"></textarea>\n'
            f'<p><button type="button" class="button secondary" data-note-save="{ident}">Tallenna muistiinpano</button></p>\n'
            "</details>\n</li>"
        )
    return f'<ol class="path-list">\n{chr(10).join(items)}\n</ol>'


def _links_list(links: list[dict]) -> str:
    items = "".join(
        f'<li><a href="{esc(link["url"])}" rel="noopener noreferrer">{esc(link["title"])}</a>, '
        f"{esc(link['publisher'])}. Luettu {time_tag(link.get('read'))}.</li>"
        for link in links
    )
    return f"<ul>{items}</ul>"


def sources_site(data: SiteData) -> str:
    source = data.curriculum["source"]
    parts = [
        f'<h3>Opetussuunnitelman perusteet</h3>\n<ul><li><a href="{esc(source["api_url"])}" rel="noopener noreferrer">'
        f"ePerusteet: {esc(source['name'])}, {esc(source['diaarinumero'])}</a> (rajapinta), Opetushallitus. "
        f"Viimeksi julkaistu {time_tag(source['last_published'])}, luettu {time_tag(source['checked'])}.</li></ul>"
    ]
    for page in data.pages.values():
        if page.meta.get("official_links"):
            parts.append(f"<h3>{esc(page.title)}</h3>\n{_links_list(page.meta['official_links'])}")
    return "\n".join(parts)


def sources_topics(data: SiteData) -> str:
    parts = []
    for topic in data.topics:
        if topic.official_links:
            parts.append(f"<h3>{topic_label(topic)} {esc(topic.title)}</h3>\n{_links_list(topic.official_links)}")
    return "\n".join(parts) or "<p>Aiheiden lähteet näkyvät tässä, kun aiheet on julkaistu.</p>"


def facts_table(data: SiteData) -> str:
    if not data.facts:
        return "<p>Muuttuvien tietojen taulukko ei ole vielä saatavilla.</p>"
    rows = []
    for key, fact in data.facts.items():
        rule = esc(fact.get("rule", key))
        link = f'<a href="{esc(fact.get("url", ""))}" rel="noopener noreferrer">Tarkista ajantasainen tieto<span class="sr-only">: {rule}</span></a>'
        rows.append(f"<tr><td>{rule}</td><td>{esc(fact.get('publisher', ''))}</td><td>{time_tag(fact.get('read'))}</td><td>{link}</td></tr>")
    table = (
        "<table><caption>Tiedot, jotka muuttuvat vuosittain</caption>\n<thead><tr><th>Tieto</th><th>Julkaisija</th>"
        f"<th>Luettu</th><th>Linkki</th></tr></thead>\n<tbody>\n{chr(10).join(rows)}\n</tbody></table>"
    )
    return label_tables(table)


def general_aims(ctx: Ctx, data: SiteData) -> str:
    lead = data.curriculum["subject"]["aims_lead"]
    items = []
    for code, entry in data.codes.items():
        if entry["kind"] != "yleinen_tavoite":
            continue
        served = ", ".join(topic_link(ctx, t, text=f"{t.module} {topic_label(t)}") for t in data.serving(code))
        note = f'<span class="served">Aiheet: {served or "ei vielä aihetta"}</span>'
        items.append(f'<li id="{code_id(code)}"><span class="code">{esc(code)}</span> <span class="wording">{esc(entry["text"])}</span> {note}</li>')
    return f'<p>{esc(lead)}</p>\n<ul class="codelist">\n{chr(10).join(items)}\n</ul>'


def module_codes(ctx: Ctx, data: SiteData, module: str) -> str:
    lead = data.curriculum["modules"][module]["objectives_lead"]
    return (
        f"<h3>Tavoitteet</h3>\n<p>{esc(lead)}</p>\n{codes_list(ctx, data, module, 'tavoite')}\n"
        f"<h3>Keskeiset sisällöt</h3>\n{codes_list(ctx, data, module, 'sisalto')}"
    )


def static_page(data: SiteData, slug: str, directory: str, current: str | None = None, scripts: bool = False) -> str:
    """Render content/pages/<slug>.md with its generated blocks."""
    page: Document = data.pages[slug]
    ctx = Ctx(directory)
    source = data.curriculum["source"]
    text = replace_tokens(
        "\n".join(page.body_lines),
        {
            "curriculum_checked": esc(data.checked),
            "curriculum_published": esc(source["last_published"]),
            "topic_count": str(len(data.topics)),
        },
    )
    blocks = {
        "doors": lambda: doors(ctx, data),
        "module_cards": lambda: module_cards(ctx, data),
        "path_controls": lambda: path_controls(data),
        "path_list": lambda: path_list(ctx, data),
        "sources_site": lambda: sources_site(data),
        "sources_topics": lambda: sources_topics(data),
        "facts_table": lambda: facts_table(data),
        "general_aims": lambda: general_aims(ctx, data),
        "module_codes:OP1": lambda: module_codes(ctx, data, "OP1"),
        "module_codes:OP2": lambda: module_codes(ctx, data, "OP2"),
    }
    body = render_with_blocks(text, blocks)
    header = data.images.header(ctx, "front") if slug == "etusivu" else ""
    main = f'<article class="page">\n<h1>{esc(page.title)}</h1>\n{header}{body}\n</article>'
    description = str(page.meta.get("description", page.title))
    return render_page(data, ctx, page.title, main, description, current=current, scripts=scripts)
