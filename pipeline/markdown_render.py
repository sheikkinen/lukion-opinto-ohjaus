"""Markdown to HTML, plus the small HTML clean-ups the site needs."""

from __future__ import annotations

import html
import re
from collections.abc import Callable

import markdown

BLOCK_TOKEN = re.compile(r"^\{\{\s*([a-z_0-9]+(?::[A-Za-z0-9]+)?)\s*\}\}\s*$", re.MULTILINE)


def render_markdown(text: str) -> str:
    """Render Markdown (tables and lists as in the contract) to HTML, ready for the page."""
    engine = markdown.Markdown(extensions=["tables", "sane_lists"], output_format="html")
    return mark_external_links(label_tables(engine.convert(text)))


def mark_external_links(rendered: str) -> str:
    """External links open in the same tab and send no referrer."""
    return re.sub(r'<a href="(https?://[^"]*)"', r'<a href="\1" rel="noopener noreferrer"', rendered)


def label_tables(rendered: str) -> str:
    """Give every table cell a data-label from its column header, so the CSS can stack rows."""

    def process(table: re.Match) -> str:
        block = table.group(0)
        labels = [re.sub(r"<[^>]+>", "", cell).strip() for cell in re.findall(r"<th[^>]*>(.*?)</th>", block, re.DOTALL)]
        block = re.sub(r"<th(?=[\s>])", '<th scope="col"', block)

        def label_row(row: re.Match) -> str:
            cells = iter(range(len(labels)))

            def label_cell(cell: re.Match) -> str:
                index = next(cells, None)
                label = html.escape(labels[index], quote=True) if index is not None else ""
                return f'<td data-label="{label}"{cell.group(1)}>'

            return re.sub(r"<td([^>]*)>", label_cell, row.group(0))

        body = re.sub(r"<tr>.*?</tr>", label_row, block, flags=re.DOTALL)
        caption = re.search(r"<caption[^>]*>(.*?)</caption>", block, re.DOTALL)
        name = re.sub(r"<[^>]+>", "", caption.group(1)).strip() if caption else ""
        name = html.escape(name, quote=True) or "Taulukko"
        return f'<div class="table-wrap" role="region" aria-label="{name}" tabindex="0">{body}</div>'

    return re.sub(r"<table>.*?</table>", process, rendered, flags=re.DOTALL)


def shift_headings(rendered: str, by: int) -> str:
    """Move every heading `by` levels down (h2 to h3), never past h6."""

    def shift(match: re.Match) -> str:
        level = min(6, int(match.group(2)) + by)
        return f"<{match.group(1)}h{level}"

    return re.sub(r"<(/?)h([1-6])(?=[\s>])", shift, rendered)


def replace_tokens(text: str, values: dict[str, str]) -> str:
    """Replace inline {{name}} tokens (not block tokens, which sit alone on a line)."""
    for name, value in values.items():
        text = text.replace("{{" + name + "}}", value)
    return text


def render_with_blocks(text: str, blocks: dict[str, Callable[[], str]]) -> str:
    """Render Markdown in which a line `{{name}}` is replaced by generated HTML."""
    parts = BLOCK_TOKEN.split(text)
    out = []
    for index, part in enumerate(parts):
        if index % 2 == 0:
            out.append(render_markdown(part) if part.strip() else "")
        elif part in blocks:
            out.append(blocks[part]())
        else:
            raise KeyError(f"unknown block token {{{{{part}}}}}")
    return "\n".join(out)


def strip_tags(rendered: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", rendered))
