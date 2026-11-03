"""A small hierarchical reader over the paired benchmark's canonical cores."""
from __future__ import annotations

from html import escape
import json
from pathlib import Path
import shutil

import astis_site
import source_lineage
import sog_bench as bench

ROOT = Path(__file__).resolve().parents[2]
HUB = 'benchmarks/samplingoptimisationgeometrybench/'
MARKER = 'data-sog-bench="true"'


def prose(text: str) -> str:
    return '<p>' + escape(text) + '</p>'


def fold(title: str, content: str) -> str:
    return '<details class="sog-fold"><summary>' + escape(title) + '</summary>' + content + '</details>'


def home(cores: list[dict]) -> str:
    return (f'<article class="sog-reader" {MARKER}><div class="eyebrow">Public development pilot · v0.1</div>'
        '<h1>SamplingOptimisationGeometryBench</h1><p class="lede">Can an AI explain the mathematics—and reconstruct a precise Lean proof?</p>'
        f'<p>{len(cores)} mathematical cores · {2*len(cores)} paired QA views · independent semantic review pending.</p>'
        '<section class="sog-grid"><article><h2>Natural-language QA</h2><p>Explain a proof, track its constants and identify what the assumptions do not imply. No Lean knowledge required.</p><a class="button primary" href="natural-language/index.html">Try natural-language questions</a></article>'
        '<article><h2>Lean-assisted QA</h2><p>Reconstruct a fixed theorem from its allowed imports and explicit context. Read the mathematical reasoning beside optional exact Lean.</p><a class="button" href="lean/index.html">Try Lean questions</a></article></section>'
        '<section><h2>Use the pilot</h2><p><a href="downloads/questions.jsonl" download>Prompt-only JSONL</a> · '
        '<a href="downloads/reference.jsonl" download>References and rubrics</a> · '
        '<a href="downloads/manifest.json" download>Version and hashes</a> · '
        '<a href="pilot.zip" download>Download the full pilot</a></p>'
        '<p>Public questions and answers may already occur in training data. This is not an unseen test set, a model ranking, or evidence that a paper is fully formalized.</p></section>'
        + fold('Evaluation policy and contribution guide',
            '<p>Each pair shares one core, family and public-dev split. Score the two tracks separately. Human-assessed natural-language rubrics have four one-point criteria; no automated semantic grader is claimed.</p>'
            '<p>Lean compiler acceptance certifies the fixed proposition only. Arbitrary model output requires target-preservation checks and an isolated, resource-limited sandbox. No submission execution service or AI API is connected here.</p>'
            '<p>Only original or permission-cleared material may enter ML training/evaluation. Restricted external indexes and their derivatives are excluded. Independent source-blind QA review remains pending; compilation is not that review.</p>'
            '<p><a href="downloads/README.md">Commands, grading protocol and how to add a core</a> · <a href="downloads/LICENSE_SCOPE.md">License boundaries</a></p>') + '</article>')


def track_page(cores: list[dict], track: str) -> str:
    title = 'Natural-language QA' if track == 'natural-language' else 'Lean-assisted QA'
    cards = ''.join('<article><small>' + escape(c['domain']) + ' · ' + escape(c['difficulty']) + '</small><h2>'
        + escape(c['title']) + '</h2><p>' + escape(c['id']) + ' · 4 rubric points · public-dev</p>'
        '<a class="button" href="../' + c['id'] + '.html?track=' + track + '#' + track + '">Open question</a></article>' for c in cores)
    return (f'<article class="sog-reader" {MARKER}><p><a href="../index.html">Bench overview</a></p><h1>{title}</h1>'
        '<p>Three views of the same shared cores. Reference answers stay closed until you choose to read them.</p>'
        '<div class="sog-grid">' + cards + '</div></article>')


def core_page(core: dict, checked: bool, graph_ids: set[str] | None = None) -> str:
    from urllib.parse import quote
    rel = HUB + core['id'] + '.html'
    known = astis_site._SOURCE_BY_NAME or {d.full_name: d for d in astis_site.scan_project_sources()[1]}
    declaration = known[core['declaration']]
    href, _ = astis_site.source_href(declaration, from_path=rel)
    graph_id = 'decl:' + core['declaration']
    if graph_id in (graph_ids or set()):
        graph_label = 'Locate the existing Lean declaration'
    else:
        graph_id = 'module:' + declaration.module
        graph_label = 'Locate the owning module (declaration not yet indexed in this graph)'
    status = 'Trusted reference compilation recorded for this source state.' if checked else 'No current trusted-reference compiler receipt recorded in this build.'
    assumptions = '<ul>' + ''.join('<li>' + escape(s) + '</li>' for s in core['assumptions']) + '</ul>'
    proof = '<ol>' + ''.join('<li>' + prose(s) + '</li>' for s in core['steps']) + '</ol>'
    rubric = '<ol>' + ''.join('<li>' + escape(r['criterion']) + ' (1 point)</li>' for r in core['rubric']) + '</ol>'
    lean = (prose(core['lean_explanation']) + '<div data-lean-code-panel><button type="button" data-lean-copy>Copy Lean reference</button><span data-lean-copy-status role="status" aria-live="polite"></span>'
            + astis_site.code_html(core['lean_reference']) + '</div>'
            '<p><a href="downloads/lean/' + core['id'] + '-reference.lean" download>Download runnable reference</a></p>')
    dependencies = ''.join('<h3>' + label + '</h3><ul>' + ''.join('<li><code>' + escape(n) + '</code></li>' for n in core['dependencies'][key]) + '</ul>'
                           for key, label in (('astis', 'ASTIS proof calls'), ('mathlib', 'Mathlib facts / definitions')))
    return (f'<article class="sog-reader" {MARKER}><p><a href="index.html">Bench</a> / ' + escape(core['domain']) + '</p>'
        '<div class="eyebrow">' + escape(core['id']) + ' · public-dev · independent QA review pending</div><h1>' + escape(core['title']) + '</h1>'
        '<section><h2>Assumptions and conventions</h2>' + assumptions + '</section>'
        '<section id="natural-language"><h2>Natural-language question</h2>' + prose(core['question'])
        + fold('Reference mathematical proof', proof + fold('How the Lean proof follows these steps', lean))
        + fold('Assessment rubric · 4 points', rubric) + '</section>'
        '<section id="lean"><h2>Lean question</h2><p>Keep the target and context fixed; replace the comment slot with your proof. Ancestor libraries are allowed, but the target module is not imported directly.</p>'
        + fold('Show fixed Lean task', astis_site.code_html(core['lean_task'])
               + '<p><a href="downloads/lean/' + core['id'] + '-task.lean.txt" download>Download task template</a></p>')
        + fold('Reference Lean and explanation', lean) + prose(status) + '</section>'
        '<section><h2>What this does—and does not—verify</h2>' + prose(core['boundary'])
        + '<p>Existing library theorem reused; no new mathematical leaf or paper-completion credit. The new QA pair has not yet passed an independent semantic review.</p></section>'
        + fold('Sources, graph location and dependencies', prose(core['source_note'])
            + '<p><a href="' + escape(href) + '">Exact local source and full context</a> · <a href="../../underlying-lean-graph/index.html?focus='
            + quote(graph_id, safe='') + '">' + graph_label + '</a></p><p><code>' + escape(core['declaration']) + '</code></p>'
            + dependencies + '<p>Binding SHA-256: <code>' + core['binding_sha256'] + '</code></p>')
        + '</article>')


def enrich_site(output: Path) -> None:
    cores = bench.materialize()
    checked = bench.receipt_current(cores)
    graph_ids = {n['id'] for n in json.loads((output / 'data/underlying-lean-graph.json').read_text(encoding='utf-8'))['nodes']}
    target = output / HUB
    target.mkdir(parents=True, exist_ok=True)
    bench.export(target / 'downloads', cores)
    bench.archive_bytes(target / 'downloads', target / 'pilot.zip')
    shutil.copyfile(ROOT / 'website/static/sog-bench.css', output / 'assets/sog-bench.css')
    pages = [('index.html', 'SamplingOptimisationGeometryBench', home(cores))]
    pages += [(track + '/index.html', track.replace('-', ' ').title(), track_page(cores, track)) for track in bench.TRACKS]
    pages += [(c['id'] + '.html', c['title'], core_page(c, checked, graph_ids)) for c in cores]
    for tail, title, body in pages:
        rel = HUB + tail
        text = astis_site.page(title, rel, body)
        text = source_lineage.canonical_shell(text, rel, output)
        text = text.replace('</head>', '<link rel="stylesheet" href="' + astis_site.relative_prefix(rel) + 'assets/sog-bench.css"></head>')
        astis_site.write_page(output, rel, text)
    # A quiet, independent entry point: no links to unrelated libraries/projects.
    for path in output.rglob('*.html'):
        text = path.read_text(encoding='utf-8')
        if 'data-sog-bench-nav' not in text and '<div class="sidebar-utility">' in text:
            link = astis_site.relative_prefix(path.relative_to(output).as_posix()) + HUB + 'index.html'
            text = text.replace('<div class="sidebar-utility">', '<div class="sidebar-utility"><a data-sog-bench-nav href="' + link + '">QA Bench</a>', 1)
            path.write_text(text, encoding='utf-8', newline='\n')
    source_lineage.append_main(output, 'index.html',
        f'<section data-sog-bench-entry><h2>SamplingOptimisationGeometryBench</h2><p>Explore paired natural-language and Lean QA for sampling, optimisation and geometry. <a href="{HUB}index.html">Open the public development pilot</a>.</p></section>',
        'data-sog-bench-entry')


def validate_site(output: Path) -> list[str]:
    errors = []
    cores = bench.materialize()
    checked = bench.receipt_current(cores)
    graph_path = output / 'data/underlying-lean-graph.json'
    ids = set()
    if graph_path.is_file():
        ids = {n['id'] for n in json.loads(graph_path.read_text(encoding='utf-8'))['nodes']}
        for core in cores:
            module = core['source_file'].removesuffix('.lean').replace('/', '.')
            if 'decl:' + core['declaration'] not in ids and 'module:' + module not in ids:
                errors.append('Missing Bench graph target: ' + core['id'])
    else:
        errors.append('Bench requires the canonical Lean graph')
    for rel in ['index.html', *(t + '/index.html' for t in bench.TRACKS), *(c['id'] + '.html' for c in bench.load()['cores'])]:
        path = output / HUB / rel
        if not path.is_file() or MARKER not in path.read_text(encoding='utf-8'):
            errors.append('Missing Bench reader: ' + rel)
    for core in cores:
        path = output / HUB / (core['id'] + '.html')
        if path.is_file() and core_page(core, checked, ids) not in path.read_text(encoding='utf-8'):
            errors.append('Stale Bench mathematics or compiler label: ' + core['id'])
    # Recreate the deterministic export and compare bytes, not manually copied counts.
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        export = Path(tmp) / 'export'
        bench.export(export, cores)
        for source in export.rglob('*'):
            if source.is_file():
                target = output / HUB / 'downloads' / source.relative_to(export)
                if not target.is_file() or target.read_bytes() != source.read_bytes():
                    errors.append('Stale Bench export: ' + source.relative_to(export).as_posix())
        archive = Path(tmp) / 'pilot.zip'
        bench.archive_bytes(export, archive)
        published = output / HUB / 'pilot.zip'
        if not published.is_file() or published.read_bytes() != archive.read_bytes():
            errors.append('Missing or stale Bench archive')
    return errors
