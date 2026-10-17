"""Small paper-first navigation, projected from the existing companion model.

The execution phase order selects the priority papers. This module owns no
theorem, completion status, proof graph or alternative source registry.
"""
from __future__ import annotations

import json
import posixpath
from html import escape
from pathlib import Path

MODEL = Path(__file__).resolve().parents[1] / 'content/samplewiki_companion_frontiers.json'
PAPER_HOME = 'example-cases/samplewiki/companions/index.html'
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


def paper_cards(rel: str, model: dict | None = None) -> str:
    model = load_model() if model is None else model
    cards = []
    for index, row in enumerate(priority_cases(model), 1):
        href = relative(rel, PAPER_BASE + row['slug'] + '.html')
        versions = ', '.join(model['sources'][sid]['version'] for sid in row['source_ids'])
        cards.append(
            f'<a class="sw-paper-card" href="{escape(href)}" data-paper-id="{escape(row["id"])}">'
            f'<span class="sw-paper-number">{index:02d}</span>'
            f'<h3>{escape(row.get("reader_label", row["title"]))}</h3>'
            f'<p>{escape(row.get("reader_summary", row["role"]))}</p>'
            f'<small>arXiv:{escape(versions)}</small><span class="sw-paper-action">Read paper →</span></a>'
        )
    heading = 'Four sampling papers' if len(cards) == 4 else f'{len(cards)} sampling papers'
    return ('<section class="sw-priority-papers" id="sampling-papers" data-companion-frontiers="true">'
            f'<h2>{heading}</h2><p>Choose a paper, then follow its statements, proof route and checked Lean.</p>'
            '<div class="sw-paper-grid">' + ''.join(cards) + '</div>'
            '<p class="sw-reader-boundary">Verified building blocks are not completed paper proofs.</p></section>')


def paper_directory(rel: str, model: dict | None = None) -> str:
    rows = priority_cases(model)
    links = ''.join(
        f'<a href="{escape(relative(rel, PAPER_BASE + r["slug"] + ".html"))}"'
        + (' aria-current="page"' if rel == PAPER_BASE + r['slug'] + '.html' else '')
        + f'>{escape(r.get("reader_label", r["title"]))}</a>' for r in rows
    )
    return ('<section class="sidebar-group sw-paper-directory" data-paper-directory="true">'
            f'<h2>Sampling papers</h2><nav><a href="{escape(relative(rel, PAPER_HOME))}">Paper reading guide</a>'
            + links + '</nav></section>')


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
