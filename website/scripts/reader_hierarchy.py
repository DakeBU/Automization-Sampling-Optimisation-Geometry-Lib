"""Final navigation projection: visible graph doors and peer library/Bench shelves.

Does not rewrite mathematical statements, proofs, source maps or status data.
Secondary sidebar links are retained behind one disclosure, never deleted.
"""
from __future__ import annotations

from html import escape
from pathlib import Path
import re
import shutil

import astis_site
import bench_portals
import information_architecture
import library_shelves
import lower_bounds
import subject_readers

ROOT = Path(__file__).resolve().parents[2]
MARKER = 'data-reader-hierarchy="3"'


def sidebar(text: str, rel: str) -> str:
    if MARKER in text:
        return text
    text = re.sub(r'<a\b[^>]*data-sog-bench-nav[^>]*>.*?</a>', '', text, flags=re.S)
    start = re.search(r'<div class="sidebar-contents"[^>]*>', text)
    if not start:
        return text
    end = text.find('<div class="sidebar-utility">', start.end())
    if end < 0:
        return text
    old = text[start.end():end].rsplit('</div>', 1)[0]
    rest = re.sub(r'<section class="sidebar-group sidebar-libraries".*?</section>', '', old, count=1, flags=re.S)
    p = astis_site.relative_prefix(rel)
    graph = (f'<section class="sidebar-group sidebar-graphs" data-reader-graph-nav><h2>Proof maps</h2><nav>'
             f'<a href="{p}lean-foundations.html?view=lean">Lean Graph <span aria-hidden="true">↗</span></a>'
             f'<a href="{p}lean-foundations.html?view=functor">Functor Hypergraph <span aria-hidden="true">↗</span></a></nav></section>')
    benches = (f'<section class="sidebar-group sidebar-benches"><h2><a data-sog-bench-nav href="{p}{bench_portals.HUB}index.html" '
               'title="Sampling-Optimisation-Geometry-Bench">Benchmarks</a></h2><nav class="source-hubs bench-source-hubs">'
               + ''.join(f'<a class="source-hub" data-bench-collection="{c["id"]}" href="{p}{bench_portals.HUB}{c["id"]}/index.html"'
                         + (' aria-current="page"' if rel.startswith(bench_portals.HUB+c['id']+'/') else '')
                         + f'><span class="source-hub-title">{escape(c["name"])}</span></a>' for c in bench_portals.configuration()['collections'])
               + '</nav></section>')
    topics = ('<section class="sidebar-group sidebar-topics"><h2>Research topics</h2><nav>'
              + lower_bounds.link(subject_readers.SAMPLING, "Sampling guide", page=rel)
              + lower_bounds.link(lower_bounds.PAGE, "Lower Bounds", page=rel) + '</nav></section>')
    contents = (f'<div class="sidebar-contents" data-ia-version="3" {MARKER}>' + graph
                + library_shelves.libraries_sidebar(rel) + benches + topics
                + '<details class="sidebar-more reader-secondary-nav"><summary>Library tools &amp; project</summary>' + rest + '</details></div>\n')
    return text[:start.start()] + contents + text[end:]


def home() -> str:
    cards = [
        ('Lean Graph', 'Locate the formal results and their checked structure.', 'lean-foundations.html?view=lean', 'lean'),
        ('Functor Hypergraph', 'Compare recurring proof mechanisms and their boundaries.', 'lean-foundations.html?view=functor', 'functor'),
        ('Libraries', 'Read the mathematics across seven connected subjects.', 'libraries/index.html', 'libraries'),
        ('Benchmarks', 'Mathematical tasks, proof evidence and evaluation tools.', bench_portals.HUB+'index.html', 'bench'),
    ]
    return ('<section class="reader-home" data-reader-home><p class="eyebrow">Samplinglib</p>'
            '<h1>Learn the mathematics.<br>Explore the proofs.</h1>'
            '<p class="lede">Sampling, optimisation and geometry — connected by formal mathematics.</p>'
            '<div class="reader-home-grid" data-sog-bench-entry>'
            + ''.join(bench_portals.card(*row) for row in cards) + '</div>'
            '<p class="reader-home-note">Read by subject: '
            + ' · '.join(lower_bounds.link(p, label, page="index.html") for p, label in subject_readers.SUBJECTS) + '</p>'
            '<p class="reader-home-note">Early formalisation. Inspect the evidence for each result. <a href="progress/index.html">Current progress →</a></p>'
            '<p class="sog-caption">Navigation sketches are illustrative; graph views distinguish formal edges from conceptual overlays.</p></section>')


def enrich_site(output: Path) -> None:
    for name in ('reader-hierarchy.css', 'sog-navigation.js'):
        shutil.copyfile(ROOT / 'website/static' / name, output / 'assets' / name)
    for path in output.rglob('*.html'):
        rel = path.relative_to(output).as_posix()
        text = path.read_text(encoding='utf-8')
        if rel == 'index.html':
            text = information_architecture.replace_main(text, home(), rel)
        if 'sidebar-contents' not in text:
            continue
        text = sidebar(text, rel)
        p = astis_site.relative_prefix(rel)
        if 'assets/reader-hierarchy.css' not in text:
            text = text.replace('</head>', f'<link rel="stylesheet" href="{p}assets/reader-hierarchy.css">\n</head>', 1)
        if rel.startswith(bench_portals.HUB) and 'assets/sog-navigation.js' not in text:
            text = text.replace('</body>', f'<script defer src="{p}assets/sog-navigation.js"></script></body>', 1)
        path.write_text(text, encoding='utf-8', newline='\n')


def validate_site(output: Path) -> list[str]:
    errors = []
    for rel in ('index.html', 'lean-foundations.html', 'textbook/index.html', bench_portals.HUB+'index.html',
                *(bench_portals.HUB+c['id']+'/index.html' for c in bench_portals.configuration()['collections'])):
        path = output / rel
        if not path.is_file():
            errors.append('Missing hierarchical reader: '+rel)
            continue
        text = path.read_text(encoding='utf-8')
        if MARKER not in text or text.count('data-bench-collection=') != 3:
            errors.append('Missing peer Bench shelf: '+rel)
        if 'data-reader-graph-nav' not in text or text.index('data-reader-graph-nav') > text.index('sidebar-libraries'):
            errors.append('Graph doors are not first-level navigation: '+rel)
        if not re.search(r'</section>\s*<section class="sidebar-group sidebar-benches"', text):
            errors.append('Bench and Libraries are not peer sections: '+rel)
    return errors
