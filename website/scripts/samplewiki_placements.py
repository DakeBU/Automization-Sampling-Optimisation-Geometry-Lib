"""Research extensions reuse reviewed lessons and canonical Lean graph identities.

Chapter associations are reading-context overlays, not formal dependencies or
source-book completion. No theorem/status/proof is authored in this projection.
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path
from urllib.parse import urlencode

import astis_publication as publication
import astis_site
import publication_reader
import samplewiki_navigation as navigation
import source_lineage

PAGE = 'textbook/research-extensions.html'
MARKER = 'data-samplewiki-extensions="true"'


def reviewed_rows(row: dict, items: list[dict], data: dict) -> list[dict]:
    path = navigation.PAPER_BASE + row['slug'] + '.html'
    result = {}
    for item in sorted(items, key=lambda i: i.get('source_order', float('inf'))):
        if item['chapter_path'] != path:
            continue
        for binding in item['bindings']:
            if not publication.verified_binding(binding, data):
                continue
            name = binding['declaration']
            result.setdefault(name, {'name': name, 'title': data['lessons'][name]['title'],
                                    'source_reader': publication_reader.source_proof_path(item),
                                    'module': data['declarations'][name].module})
    return list(result.values())


def graph_link(name: str) -> str:
    return 'lean-foundations.html?' + urlencode({'view': 'lean', 'focus': 'decl:' + name})


def links(row: dict, chapters: dict[int, dict], rel: str) -> str:
    targets = [(PAGE + '#' + row['slug'], 'Textbook research extension')]
    targets += [(f'textbook/chapter-{n:02d}.html', f'Ch. {n}: {chapters[n]["title"]}')
                for n in row['reader_chapters']]
    return ' · '.join(f'<a href="{escape(navigation.relative(rel, path))}">{escape(label)}</a>'
                      for path, label in targets)


def enrich_site(output: Path) -> None:
    model = navigation.load_model()
    chapters = {c['number']: c for c in json.loads(
        (navigation.MODEL.parent / 'chapters.json').read_text(encoding='utf-8'))}
    data, items = publication.inputs(), publication.load()
    graph = json.loads((output / 'data/underlying-lean-graph.json').read_text(encoding='utf-8'))
    nodes = {n['id'] for n in graph['nodes']}
    groups, chapter_projects = [], {}
    for row in navigation.research_cases(model):
        for n in row['reader_chapters']:
            if n not in chapters:
                raise ValueError(f'{row["id"]}: unknown reading-context chapter {n}')
            chapter_projects.setdefault(n, []).append(row)
        reviewed = reviewed_rows(row, items, data)
        entries = []
        for entry in reviewed:
            if 'decl:' + entry['name'] not in nodes:
                raise ValueError(f'{entry["name"]}: reviewed placement missing canonical Lean graph node')
            href = navigation.relative(PAGE, entry['source_reader'])
            graph_href = navigation.relative(PAGE, graph_link(entry['name']))
            shared = entry['module'].startswith('AutoSamplingTheory.TechnicalLemmas.')
            owner = 'Canonical shared module' if shared else 'Paper-specific owning module'
            module_href = navigation.relative(PAGE, 'modules/' + astis_site.slugify(entry['module']) + '.html')
            entries.append(f'<li data-reviewed-placement="{escape(entry["name"])}">'
                f'<a href="{escape(href)}">{escape(entry["title"])}</a> · '
                f'<a href="{escape(graph_href)}">Lean graph</a>'
                f'<small>{owner}: <a href="{escape(module_href)}">{escape(entry["module"])}</a></small></li>')
        label = row.get('reader_label', row['title'])
        paper = navigation.PAPER_BASE + row['slug'] + '.html'
        groups.append(f'<section id="{escape(row["slug"])}"><h2>{escape(label)}</h2>'
            f'<p><a href="{escape(navigation.relative(PAGE, paper))}">Research page</a> · '
            + links(row, chapters, PAGE) + '</p>'
            + (f'<details><summary>{len(reviewed)} independently reviewed declarations: statements, proofs and graph locations</summary><ul class="sw-extension-proofs">'
               + ''.join(entries) + '</ul></details>' if entries else
               '<p>No independently reviewed declaration is projected here yet. The source route remains open.</p>')
            + '</section>')
        note = f'<nav {MARKER} aria-label="Textbook and shared foundations"><p>' + links(row, chapters, paper) + '</p><small>Reading context only; not chapter-completion credit. Verified proofs below link to their canonical shared or paper-specific Lean nodes.</small></nav>'
        source_lineage.append_main(output, paper, note, MARKER)
    body = ('<nav class="reader-breadcrumb"><a href="index.html">Log-Concave Sampling</a> / Research extensions</nav>'
        '<h1>Research extensions</h1><p>Read the textbook background, then follow a research result into its verified mathematical proofs and exact Lean graph locations.</p>'
        '<p>These are Samplinglib extensions, not chapters or numbered results of Chewi’s book. Chapter links are reading context, not certified theorem dependencies. Counts are reviewed declarations, not paper-completion percentages. The same canonical proof is reused, never copied into a second theorem.</p>'
        + ''.join(groups))
    text = astis_site.page('Sampling research extensions', PAGE, body, active='Textbook',
        extra_head='<link rel="stylesheet" href="../assets/samplewiki-paper-navigation.css">')
    astis_site.write_page(output, PAGE, source_lineage.canonical_shell(text, PAGE, output))
    for n, rows in chapter_projects.items():
        rel = f'textbook/chapter-{n:02d}.html'
        entries = ''.join(f'<li><a href="research-extensions.html#{escape(r["slug"])}">{escape(r.get("reader_label", r["title"]))}</a></li>' for r in rows)
        source_lineage.append_main(output, rel, f'<details {MARKER}><summary>Research extensions using this background</summary><p>Reading-context links, not additional source-book results or proof dependencies.</p><ul>{entries}</ul></details>', MARKER)
    source_lineage.append_main(output, 'textbook/index.html',
        f'<section {MARKER}><h2>Research extensions</h2><p><a href="research-extensions.html">From textbook background to current Sampling research</a>: reviewed proofs, canonical shared modules and exact Lean graph locations. Source-text chapter progress is unchanged.</p></section>', MARKER)
