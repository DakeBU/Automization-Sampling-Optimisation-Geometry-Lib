"""Reader-first subject/resource directory over one pinned external intake.

All intake items stay gray external references. Existing source/proof lessons
are linked, not copied, and keep their own compiler and review evidence.
"""
from __future__ import annotations

from collections import defaultdict
from html import escape
import json
from pathlib import Path
import re
import shutil
from urllib.parse import quote

import astis_site
import declaration_lessons
import research_resources as intake
import source_lineage

ROOT = Path(__file__).resolve().parents[2]
GUIDES = ROOT / 'website/content/resource_guides.json'
MARKER = 'data-resource-library="true"'


def guides() -> dict:
    data = json.loads(GUIDES.read_text(encoding='utf-8'))
    if data['schema_version'] != 1 or len(data['libraries']) != 7:
        raise ValueError('Resource guides must cover the seven existing libraries')
    if set(data['optlib_areas']) != {'Differential', 'Convex', 'Function', 'Optimality', 'Algorithm'}:
        raise ValueError('Incomplete Optlib topic map')
    for subject in data['subjects']:
        if not set(subject['libraries']) <= set(data['libraries']):
            raise ValueError('Unknown library route')
    return data


def a(url: str, title: str, **attrs) -> str:
    extra = ''.join(f' {key}="{escape(value, quote=True)}"' for key, value in attrs.items())
    return f'<a href="{escape(url, quote=True)}"{extra}>{escape(title)}</a>'


def title_math(text: str) -> str:
    # Literal typesetting only: no interpretation or mathematical rewriting.
    return re.sub(r'\$([^$]+)\$', lambda m: '\\(' + m[1] + '\\)', escape(text))


def render_entries(rows: list[dict]) -> str:
    items = []
    for row in rows:
        date = f'<time datetime="{row["listed_date"]}">{row["listed_date"]}</time>' if row.get('listed_date') else ''
        note = '<small>' + escape(row['link_note']) + '</small>' if row.get('link_note') else ''
        identity = f' id="{row["id"]}"' if row.get('id') else ''
        items.append(f'<li{identity} data-resource-entry data-search="{escape(row["title"].casefold(), quote=True)}">'
                     f'<a href="{escape(row["url"], quote=True)}" rel="noopener noreferrer">{title_math(row["title"])}</a>'
                     f'<small>{date} <span class="resource-external">external reference</span></small>{note}</li>')
    return '<ol class="resource-list">' + ''.join(items) + '</ol>'


def library_cards(ids: list[str], data: dict, prefix: str = '../') -> str:
    return '<div class="resource-grid">' + ''.join(
        '<article><h2>' + a(prefix + data['libraries'][key]['path'], data['libraries'][key]['title'])
        + '</h2><p>' + escape(data['libraries'][key]['role']) + '</p></article>' for key in ids) + '</div>'


def masthead(title: str, lede: str) -> str:
    return ('<header><p class="eyebrow">Samplinglib · research resources</p><h1>' + escape(title)
            + '</h1><p class="lede">' + escape(lede) + '</p></header>')


def filter_box() -> str:
    return '<div class="resource-filter"><label for="resource-query">Find a title</label><input id="resource-query" type="search" placeholder="e.g. acceleration, Sinkhorn, lower bound" autocomplete="off"><p data-resource-count role="status" aria-live="polite"></p></div>'


def hub(data: dict, catalog: dict) -> str:
    count = sum(len(s['items']) for s in catalog['forum']['sections'])
    cards = '<div class="resource-grid">' + ''.join(
        '<article><h2>' + a(s['id'] + '.html', s['title']) + '</h2><p>' + escape(s['intro']) + '</p></article>'
        for s in data['subjects']) + '</div>'
    categories = '<ul class="resource-category-list">' + ''.join(
        '<li>' + a('forum/' + s['id'] + '.html', s['title']) + f' <small>{len(s["items"])} links</small></li>'
        for s in catalog['forum']['sections']) + '</ul>'
    return (masthead('Research resources', 'Find the right mathematics, then follow it to a readable proof, its assumptions and optional Lean.')
        + '<section><h2>Start with a subject</h2>' + cards + '</section>'
        + '<section><h2>What do you need?</h2><div class="resource-grid">'
        '<article><h3>Learn the foundations</h3><p>Source-ordered textbook chapters and shared prerequisites.</p>' + a('../libraries/index.html', 'Browse seven libraries') + '</article>'
        '<article><h3>Reuse formal mathematics</h3><p>Browse Optlib by mathematical purpose, compare exact assumptions and inspect existing local proof readers.</p>' + a('optlib.html', 'Open the Optlib map') + '</article>'
        '<article><h3>Digest a new argument</h3><p>Separate the source proof, actual Lean dependencies and conceptual mirrors.</p>' + a('../example-cases/samplewiki.html', 'Explore SampleWiki') + ' · ' + a('../live/index.html', 'Open a research workspace') + '</article></div></section>'
        + f'<section><h2>Optimization × AI Forum collection</h2><p>{count} source-listed resources, across six categories. These are discovery links, not verified mathematical claims.</p>'
        + categories + '</section><details><summary>Sources, coverage and reuse boundaries</summary>' + provenance(catalog) + '</details>')


def provenance(catalog: dict) -> str:
    forum, opt = catalog['forum'], catalog['optlib']
    return ('<p>Organization informed by ' + a(intake.REPO, 'Optlib') + ' and the '
        + a(intake.FORUM, 'Optimization × AI Forum resource collection') + '. No affiliation or endorsement is implied.</p>'
        f'<p>Forum last updated {escape(forum["upstream_updated"])}; retrieved {escape(catalog["retrieved"])}. The complete six-section title/link/date inventory is retained. Linked papers, AI-assistance claims and their proofs have not been independently audited here.</p>'
        '<p>No explicit Forum reuse license was established. We do not copy its prose, styling, site code, abstracts or proofs. Paper titles and bibliographic links point to their respective owners.</p>'
        f'<p>Optlib: Apache-2.0, commit <code>{opt["commit"]}</code>; {len(opt["modules"])} modules inventoried, not blanket-audited. Copyright {escape(opt["copyright"])} '
        + a(f'{intake.REPO}/blob/{opt["commit"]}/LICENSE', 'Upstream license') + '.</p>'
        '<p><strong>Reference intake is not formal assimilation.</strong> No new declaration, chapter coverage, solid proof edge or validated conceptual transport is claimed. Existing publication metadata remains authoritative.</p>'
        '<p>' + a('data/resource-intake.json', 'Download pinned bibliography and fingerprints', download='resource-intake.json') + ' · '
        + a('data/resource-guides.json', 'Download original subject guide metadata', download='resource-guides.json') + '</p>')


def discover_geometry(catalog: dict) -> list[dict]:
    # Explicitly a title-search aid, not a semantic classifier or source binding.
    terms = ('geodesic', 'hyperbolic', 'curvature', 'manifold', 'stiefel', 'wasserstein', 'sinkhorn', 'optimal transport', 'bregman', 'mirror')
    return [r for s in catalog['forum']['sections'] for r in s['items'] if any(t in r['title'].casefold() for t in terms)]


def subject_page(subject: dict, data: dict, catalog: dict) -> str:
    route = '<ol class="resource-route">' + ''.join('<li><h3>' + escape(s['title']) + '</h3><p>' + escape(s['text']) + '</p></li>' for s in subject['route']) + '</ol>'
    body = (masthead(subject['title'], subject['intro']) + '<section><h2>Choose a reading route</h2>'
            + library_cards(subject['libraries'], data) + '</section><section><h2>Keep the argument inspectable</h2>'
            + route + '<p class="resource-boundary">' + escape(subject['boundary']) + '</p></section>')
    if subject['id'] == 'optimisation':
        body += ('<section><h2>Formal libraries and reusable techniques</h2><p>' + a('optlib.html', 'Optlib: five areas, complete module index and existing local matches')
                 + ' · ' + a('../libraries/optimisation/index.html', 'Current source-aligned chapter progress') + '</p></section>'
                 '<section><h2>Research, tools and counterexamples</h2><ul>' + ''.join('<li>' + a('forum/' + s['id'] + '.html', s['title']) + '</li>' for s in catalog['forum']['sections']) + '</ul></section>')
    elif subject['id'] == 'sampling':
        cases = json.loads((ROOT / 'website/content/samplewiki_companion_frontiers.json').read_text(encoding='utf-8'))['cases']
        body += ('<section><h2>Research projects</h2><p>Sampling regimes remain the primary SampleWiki entrance; these paper readers are a further drill-down, not a competing library.</p><ul>'
                 + ''.join('<li>' + a('../example-cases/samplewiki/companions/' + c['slug'] + '.html', c.get('reader_label', c['title'])) + '</li>' for c in cases)
                 + '</ul></section><details><summary>Where optimization foundations can help</summary><p>Convexity, smoothness, proximal energy and scalar contraction estimates can be shared when their definitions and hypotheses actually agree. '
                 'A Markov kernel, stationarity, an invariant law and an expected-cost bound still need separate proofs.</p><p>'
                 + a('optlib.html', 'Compare the upstream primitives and their strict boundaries') + ' · '
                 + a('../textbook/research-extensions.html', 'Existing research-to-textbook placements') + '</p></details>')
    else:
        body += ('<section><h2>Related research to inspect</h2><p>Title-based suggestions from the pinned Forum bibliography. Placement is a discovery aid only; no claim is made that these papers were read, formalized or assigned to a source chapter.</p>'
                 + filter_box() + render_entries(discover_geometry(catalog)) + '</section><p>'
                 + a('../lean-foundations.html?view=functor', 'Inspect the conceptual layer, keeping adapters visible') + '</p>')
    return body


def existing_optlib_matches() -> list[dict]:
    # These are source citations, NOT evidence of an Optlib import or theorem completion.
    matches = []
    for file in sorted((ROOT / 'website/content/declaration_lessons').glob('*.json')):
        for unit in json.loads(file.read_text(encoding='utf-8')).get('units', []):
            sources = [s for s in unit.get('sources', []) if s.get('url', '').startswith(intake.REPO + '/blob/' + intake.PIN + '/')]
            if sources:
                matches.append({'declaration': unit['declaration'], 'title': unit['title'],
                                'page': declaration_lessons.lesson_path(unit['declaration']), 'sources': sources})
    return matches


def optlib_page(data: dict, catalog: dict) -> str:
    opt = catalog['optlib']
    body = masthead('Optlib: mathematical reuse map', 'Browse an external library by purpose; inspect source-backed local mathematics without confusing provenance with a compiled dependency.')
    body += (f'<p class="resource-boundary">Optlib uses {escape(opt["toolchain"])}. Samplinglib stays on Lean 4.33.0 and its fixed Mathlib. No new Optlib dependency or bulk port was added.</p>'
             '<section><h2>Five mathematical areas</h2>')
    for key, area in data['optlib_areas'].items():
        rows = [m for m in opt['modules'] if m['area'] == key]
        body += ('<article class="resource-area"><h3>' + escape(area['title']) + '</h3><p>' + escape(area['purpose']) + '</p><p>'
                 + a('../' + area['chapter'], 'Related source chapter (reading context only)') + '</p><p>' + escape(area['consumer'])
                 + f'</p><details><summary>Browse {len(rows)} upstream modules</summary><ul>'
                 + ''.join('<li>' + a(m['url'], m['path']) + ' <small class="resource-external">external reference</small></li>' for m in rows) + '</ul></details></article>')
    body += '</section><section><h2>Existing local proof readers citing Optlib</h2><p>Generated from canonical authored lessons, not a second port-status table. A citation is not necessarily a code port or imported dependency. Each linked reader shows its actual statement, proof, folded Lean and review boundary.</p><ul>'
    for unit in existing_optlib_matches():
        body += ('<li>' + a('../' + unit['page'], unit['title']) + '<details><summary>Declaration and graph location</summary><code>'
                 + escape(unit['declaration']) + '</code><p>' + a('../lean-foundations.html?view=lean&focus=' + quote('decl:' + unit['declaration'], safe=''), 'Locate the actual local declaration') + '</p></details></li>')
    body += '</ul></section><details><summary>Tools, publications and textbooks indexed by Optlib</summary>'
    grouped = defaultdict(list)
    for row in opt['readme_resources']:
        row = dict(row)
        # Resolve historically floating Mathlib pointers against our fixed manifest.
        row['url'] = row['url'].replace('/mathlib4/blob/master/', '/mathlib4/blob/' + declaration_lessons.mathlib_pin() + '/')
        grouped[row['section']].append(row)
    for group, rows in grouped.items():
        body += '<h3>' + escape(group) + '</h3>' + render_entries(rows)
    body += ('</details><details><summary>Reuse checklist and upstream link caveats</summary><ol>'
             '<li>Search our declaration catalog, fixed Mathlib, active shared cells, then this pinned upstream.</li>'
             '<li>Read the exact definition, quantifiers, positivity and regularity assumptions; inspect placeholders and axioms before any port.</li>'
             '<li>Choose reuse, an explicit adapter, a genuine missing shared leaf, or out of scope. Record real consumers.</li>'
             '<li>Compile an owned declaration, test it, complete independent source review and publish the readable formula proof through the existing protocol.</li></ol>'
             '<p>The upstream README contains stale Function/BanachSubgradient and Function/FiniteDimensionalConvexFunctionsLocallyLipschitz paths and a doubled slash in an acceleration link. The complete module list above uses the pinned Git tree, not those broken paths. Mathlib pointers below the upstream migration notes are resolved against our fixed Mathlib revision, not treated as new local leaves.</p></details>')
    return body


def wrap(body: str, depth: int = 1) -> str:
    p = '../' * depth
    return (f'<article class="resource-reader" {MARKER}><nav class="resource-breadcrumb" aria-label="Resource navigation">'
            + a(p + 'resources/index.html', 'Resources') + ' / ' + a(p + 'resources/optimisation.html', 'Optimisation') + ' / '
            + a(p + 'resources/sampling.html', 'Sampling') + ' / ' + a(p + 'resources/geometry.html', 'Geometry') + '</nav>' + body + '</article>')


def enrich_site(output: Path) -> None:
    data, catalog = guides(), intake.load()
    pages = {'resources/index.html': ('Research resources', hub(data, catalog)),
             'resources/optlib.html': ('Optlib reuse map', optlib_page(data, catalog))}
    for subject in data['subjects']:
        pages['resources/' + subject['id'] + '.html'] = (subject['title'] + ' resources', subject_page(subject, data, catalog))
    for section in catalog['forum']['sections']:
        body = (masthead(section['title'], 'A complete source-listed bibliography; choose a title, then inspect the primary source before using its mathematical claims.')
                + f'<p>{len(section["items"])} references. Dates are supplied by the Forum, not independently verified publication dates.</p>'
                + filter_box() + render_entries(section['items'])
                + '<p>' + a(intake.FORUM + '#' + section['id'], 'Original category and attribution') + '</p>')
        pages['resources/forum/' + section['id'] + '.html'] = (section['title'], body)
    for rel, (title, body) in pages.items():
        text = source_lineage.canonical_shell(astis_site.page(title, rel, wrap(body, len(Path(rel).parent.parts))), rel, output)
        p = astis_site.relative_prefix(rel)
        text = text.replace('</head>', f'<link rel="stylesheet" href="{p}assets/resource-library.css"><script defer src="{p}assets/resource-library.js"></script></head>', 1)
        astis_site.write_page(output, rel, text)
    assets = output / 'assets'
    for name in ('resource-library.css', 'resource-library.js'):
        shutil.copyfile(ROOT / 'website/static' / name, assets / name)
    target = output / 'resources/data'
    target.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(intake.CATALOG, target / 'resource-intake.json')
    shutil.copyfile(GUIDES, target / 'resource-guides.json')
    # Keep subject pages discoverable inside the existing seven-library IA.
    # Do not rewrite or reorder SampleWiki's regime/paper directory.
    subject_for = {data['libraries'][key]['path']: subject['id'] for subject in data['subjects'] for key in subject['libraries']}
    subject_for.update({'index.html': 'index', 'libraries/index.html': 'index'})
    for rel, subject in subject_for.items():
        path = output / rel
        text = path.read_text(encoding='utf-8')
        marker = 'data-resource-entrypoint="true"'
        if marker not in text:
            link = a(astis_site.relative_prefix(rel) + 'resources/' + subject + '.html', 'Research resources: guides, formal libraries and papers')
            main = re.search(r'<main\b[^>]*>', text)
            stop = text.index('</section>', main.end()) + len('</section>')
            text = text[:stop] + f'<p class="resource-entrypoint" {marker}>{link}</p>' + text[stop:]
            path.write_text(text, encoding='utf-8', newline='\n')
    # Add one permanent navigation entry throughout the site, without a new library.
    for path in output.rglob('*.html'):
        text = path.read_text(encoding='utf-8')
        if 'data-resource-nav="true"' in text or 'sidebar-libraries' not in text:
            continue
        rel = path.relative_to(output).as_posix()
        start = text.index('sidebar-libraries')
        stop = text.index('</nav>', start)
        link = '<a data-resource-nav="true" href="' + astis_site.relative_prefix(rel) + 'resources/index.html">Research resources</a>'
        text = text[:stop] + link + text[stop:]
        path.write_text(text, encoding='utf-8', newline='\n')
    for rel in ('attribution/index.html', 'attribution.html'):
        path = output / rel
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        marker = 'data-resource-attribution="true"'
        if marker not in text:
            block = (f'<section {marker}><h2>Research-resource organization</h2><p>'
                     + a(intake.REPO, 'Optlib') + ' informs the mathematical topic hierarchy; '
                     + a(intake.FORUM, 'Optimization × AI Forum') + ' informs the categorized resource directory. '
                     'Only bibliographic facts are indexed from the Forum; no site code, prose or styling is copied. '
                     'Optlib retains its Apache-2.0 license and author notices. No affiliation or endorsement is implied.</p><p>'
                     + a(astis_site.relative_prefix(rel) + 'resources/index.html', 'Open the pinned resource directory and coverage boundaries') + '</p></section>')
            path.write_text(text.replace('</main>', block + '</main>', 1), encoding='utf-8', newline='\n')


def validate_site(output: Path) -> list[str]:
    errors = []
    data, catalog = guides(), intake.load()
    expected = {'resources/index.html', 'resources/optlib.html'} | {'resources/' + s['id'] + '.html' for s in data['subjects']}
    expected |= {'resources/forum/' + s['id'] + '.html' for s in catalog['forum']['sections']}
    for rel in expected:
        if not (output / rel).exists() or MARKER not in (output / rel).read_text(encoding='utf-8'):
            errors.append('Missing generated resource page: ' + rel)
    for section in catalog['forum']['sections']:
        path = output / ('resources/forum/' + section['id'] + '.html')
        if not path.exists():
            continue
        text = path.read_text(encoding='utf-8')
        actual = re.findall(r'<li id="(forum-[a-f0-9]+)"', text)
        if actual != [r['id'] for r in section['items']]:
            errors.append('Truncated/stale external bibliography: ' + section['id'])
        if 'status-blue' in text:
            errors.append('External bibliography acquired a blue proof badge')
    for source, name in ((intake.CATALOG, 'resource-intake.json'), (GUIDES, 'resource-guides.json')):
        path = output / 'resources/data' / name
        if not path.exists() or source.read_bytes() != path.read_bytes():
            errors.append('Resource metadata export is stale: ' + name)
    optlib_path = output / 'resources/optlib.html'
    if optlib_path.exists():
        text = optlib_path.read_text(encoding='utf-8')
        for module in catalog['optlib']['modules']:
            if f'href="{escape(module["url"], quote=True)}"' not in text:
                errors.append('Missing pinned Optlib module: ' + module['path'])
    for unit in existing_optlib_matches():
        if not (output / unit['page']).exists():
            errors.append('Missing actual local lesson: ' + unit['declaration'])
    for library in data['libraries'].values():
        path = output / library['path']
        if not path.exists() or 'data-resource-entrypoint="true"' not in path.read_text(encoding='utf-8'):
            errors.append('Missing existing-library resource connection: ' + library['path'])
    return errors
