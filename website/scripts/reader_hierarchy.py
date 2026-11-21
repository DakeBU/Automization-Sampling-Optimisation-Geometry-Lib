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
        ('Research libraries',
         'Explore seven connected textbook and research routes, including SampleWiki.',
         'libraries/index.html', 'libraries'),
        ('Lean proof graph',
         'Trace locally checked statements, hypotheses, and actual proof dependencies.',
         'lean-foundations.html?view=lean', 'lean'),
        ('Functor Hypergraph',
         'Compare mathematical techniques across fields, with explicit assumption and failure maps.',
         'lean-foundations.html?view=functor', 'functor'),
        ('Domain QA Bench',
         'Train and evaluate specialist reasoning with non-agentic QA and agentic Lean-assisted tasks.',
         bench_portals.HUB+'index.html', 'bench'),
    ]
    cards_html = ''.join(bench_portals.card(*row) for row in cards)
    subject_links = ' · '.join(
        lower_bounds.link(p, label, page="index.html")
        for p, label in subject_readers.SUBJECTS
    )
    bench = bench_portals.HUB
    return f'''<section class="reader-home" data-reader-home>
      <p class="eyebrow">Samplinglib · research platform</p>
      <h1>Sampling, Optimisation &amp; Geometry</h1>
      <p class="lede">Understand new mathematical techniques through their proofs, assumptions, and connections.</p>
      <p class="reader-home-purpose">Samplinglib connects textbook foundations and frontier papers to source-aligned explanations, Lean-checked results where available, and navigable proof graphs. Researchers can inspect what a new method actually contributes, identify reusable ingredients, and see where hypotheses or verification still limit an argument.</p>
      <div class="reader-home-grid" data-sog-bench-entry>{cards_html}</div>
      <section class="reader-home-bench" aria-labelledby="reader-home-bench-title">
        <p class="eyebrow">Sampling-Optimisation-Geometry-Bench</p>
        <h2 id="reader-home-bench-title">QA Bench for training and evaluating domain-specific models</h2>
        <p>One source-grounded curriculum spans sampling, optimisation, geometry and their connected subjects. It distinguishes two different kinds of mathematical QA:</p>
        <div class="reader-home-qa-grid">
          <a href="{bench}natural-language/index.html">
            <strong>Non-agentic mathematical QA</strong>
            <span>Answer questions, derive formulas, and explain proofs without interactive tools. Reviewed solutions and rubrics support specialist-model development and mathematical assessment.</span>
            <small>Explore natural-language QA →</small>
          </a>
          <a href="{bench}lean/index.html">
            <strong>Agentic Lean-assisted QA</strong>
            <span>Work toward fixed formal proof targets using Lean and compiler feedback. This tests tool-assisted proof construction rather than text-only answers; the isolated Lean environment remains experimental.</span>
            <small>Explore Lean-assisted QA →</small>
          </a>
        </div>
        <p class="reader-home-bench-note"><a href="{bench}training/index.html">Training resources</a> · <a href="{bench}evaluation/index.html">Evaluation protocols</a> · <a href="{bench}graph-json/index.html">Separate graph QA</a>. This is a public-development curriculum, not an unseen test set or a measured model leaderboard.</p>
      </section>
      <p class="reader-home-note">Read by subject: {subject_links}</p>
      <p class="reader-home-note">Formalisation is ongoing; only locally verified results receive formal proof edges. <a href="progress/index.html">Current progress →</a></p>
      <p class="sog-caption">Navigation sketches are illustrative; the graph views distinguish formal dependencies from conceptual connections.</p>
    </section>'''

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
    homepage = output / 'index.html'
    if homepage.is_file():
        main = homepage.read_text(encoding='utf-8')
        for marker in (
            '<h1>Sampling, Optimisation &amp; Geometry</h1>',
            'what a new method actually contributes',
            'Non-agentic mathematical QA',
            'Agentic Lean-assisted QA',
            'natural-language/index.html',
            'lean/index.html',
            'training/index.html',
            'evaluation/index.html',
            'not an unseen test set or a measured model leaderboard',
        ):
            if marker not in main:
                errors.append('Homepage research/QA purpose missing: ' + marker)
        if 'Learn the mathematics.<br>Explore the proofs.' in main:
            errors.append('Obsolete generic homepage headline was restored')
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
