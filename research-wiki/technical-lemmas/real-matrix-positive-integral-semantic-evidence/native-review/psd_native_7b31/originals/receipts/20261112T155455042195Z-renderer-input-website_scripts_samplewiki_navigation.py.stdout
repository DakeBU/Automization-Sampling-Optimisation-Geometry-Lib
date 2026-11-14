"""One SampleWiki research directory, projected from the existing source model.

The execution phase order selects the priority papers. This module owns no
theorem, completion status, proof graph or alternative source registry.
"""
from __future__ import annotations

import json
import posixpath
import re
from html import escape
from pathlib import Path

MODEL = Path(__file__).resolve().parents[1] / 'content/samplewiki_companion_frontiers.json'
REGIMES = Path(__file__).resolve().parents[2] / 'research-wiki/source-index/SampleWiki_cases.json'
PAPER_HOME = 'example-cases/samplewiki.html'
PAPER_BASE = 'example-cases/samplewiki/companions/'
STYLE_NAME = 'samplewiki-paper-navigation.css'
SCRIPT_NAME = 'samplewiki-paper-navigation.js'


def install_style(output: Path) -> None:
    assets = output / 'assets'
    assets.mkdir(parents=True, exist_ok=True)
    (assets / STYLE_NAME).write_text(
        (Path(__file__).resolve().parents[1] / 'static' / STYLE_NAME).read_text(encoding='utf-8'),
        encoding='utf-8', newline='\n')
    (assets / SCRIPT_NAME).write_text(
        (Path(__file__).resolve().parents[1] / 'static' / SCRIPT_NAME).read_text(encoding='utf-8'),
        encoding='utf-8', newline='\n')


def load_model() -> dict:
    return json.loads(MODEL.read_text(encoding='utf-8'))


def regime_pages() -> list[dict]:
    return json.loads(REGIMES.read_text(encoding='utf-8'))['pages']


def relative(rel: str, target: str) -> str:
    return posixpath.relpath(target, posixpath.dirname(rel) or '.')


def priority_cases(model: dict | None = None) -> list[dict]:
    model = load_model() if model is None else model
    by_version = {model['sources'][sid]['version']: row
                  for row in model['cases'] for sid in row['source_ids']}
    rows, seen = [], set()
    for phase in model['execution']['phase_order']:
        for version in phase['source_versions']:
            row = by_version[version]
            if row['id'] not in seen:
                rows.append(row)
                seen.add(row['id'])
    return rows


def research_cases(model: dict | None = None) -> list[dict]:
    """Scheduling order does not exclude other SampleWiki research projects."""
    model = load_model() if model is None else model
    rows = priority_cases(model)
    selected = {row['id'] for row in rows}
    return rows + [row for row in model['cases'] if row['id'] not in selected]


def paper_cards(rel: str, model: dict | None = None) -> str:
    model = load_model() if model is None else model
    cards = []
    for index, row in enumerate(research_cases(model), 1):
        href = relative(rel, PAPER_BASE + row['slug'] + '.html')
        versions = ', '.join(model['sources'][sid]['version'] for sid in row['source_ids'])
        reading_links = ''.join(
            f'<a href="{escape(relative(rel, link["path"]))}">{escape(link["label"])}</a>'
            for link in row.get('reader_links', []))
        cards.append(
            f'<article class="sw-paper-card" data-paper-id="{escape(row["id"])}">'
            f'<span class="sw-paper-number">{index:02d}</span>'
            f'<h3><a href="{escape(href)}">{escape(row.get("reader_label", row["title"]))}</a></h3>'
            f'<p>{escape(row.get("reader_summary", row["role"]))}</p>'
            f'<small>arXiv:{escape(versions)}</small>'
            f'<a class="sw-paper-action" href="{escape(href)}">Statement and proof →</a>'
            + (f'<nav class="sw-case-reading-links" aria-label="Related verified work">{reading_links}</nav>' if reading_links else '')
            + '</article>'
        )
    return ('<section class="sw-priority-papers" id="research-cases" data-companion-frontiers="true">'
            '<h2>Selected research projects</h2><p>Read a paper or case study, its proof route and the pieces verified so far.</p>'
            '<div class="sw-paper-grid">' + ''.join(cards) + '</div>'
            '<p class="sw-reader-boundary">Verified building blocks are not completed paper proofs.</p></section>')


def paper_directory(rel: str, model: dict | None = None) -> str:
    rows = research_cases(model)
    regimes = ''.join(
        f'<a href="{escape(relative(rel, "example-cases/samplewiki/settings/" + r["setting_slug"] + ".html"))}">{escape(r["setting_title"])}</a>'
        for r in regime_pages())
    links = ''.join(
        f'<a href="{escape(relative(rel, PAPER_BASE + r["slug"] + ".html"))}"'
        + (' aria-current="page"' if rel == PAPER_BASE + r['slug'] + '.html' else '')
        + f'>{escape(r.get("reader_label", r["title"]))}</a>' for r in rows
    )
    return ('<section class="sidebar-group sw-paper-directory" data-paper-directory="true">'
            f'<h2>SampleWiki</h2><nav><a href="{escape(relative(rel, PAPER_HOME))}">All research problems</a>'
            + regimes + '</nav><details class="sw-project-directory"'
            + (' open' if rel.startswith(PAPER_BASE) else '')
            + '><summary>Research projects</summary><nav>' + links + '</nav></details></section>')


def inject_paper_directory(text: str, rel: str, model: dict | None = None) -> str:
    if 'data-paper-directory="true"' in text:
        return text
    marker = '<details class="book-nav"'
    position = text.find(marker)
    if position < 0:
        # Late companion pages use the canonical shelf fallback, without a
        # chapter-specific book directory. Keep their paper links first too.
        position = text.find('<section class="sidebar-group sidebar-libraries"')
    if position < 0:
        raise ValueError(f'{rel}: canonical sidebar marker missing')
    return text[:position] + paper_directory(rel, model) + text[position:]


def attach_research_context(output: Path, model: dict | None = None) -> None:
    """Link an existing mathematical lesson to its research context, not new proof credit."""
    for row in research_cases(model):
        for link in row.get('reader_links', []):
            rel = link['path']
            path = (output / rel).resolve()
            if not path.is_relative_to(output.resolve()):
                raise ValueError(f'{rel}: research lesson must stay inside generated site')
            text = path.read_text(encoding='utf-8')
            if 'data-samplewiki-research-context="true"' in text:
                continue
            context = (
                '<nav class="reader-breadcrumb" data-samplewiki-research-context="true" aria-label="Research context">'
                f'<a href="{escape(relative(rel, PAPER_HOME))}">SampleWiki</a> / '
                f'<a href="{escape(relative(rel, PAPER_BASE + row["slug"] + ".html"))}">'
                f'{escape(row.get("reader_label", row["title"]))}</a></nav>')
            text, count = re.subn(r'(<main\b[^>]*>)', lambda m: m.group(1) + context, text, count=1)
            if count != 1:
                raise ValueError(f'{rel}: missing main for SampleWiki research context')
            path.write_text(text, encoding='utf-8', newline='\n')
