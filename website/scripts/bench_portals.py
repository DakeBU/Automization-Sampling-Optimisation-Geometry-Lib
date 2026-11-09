"""Small visual doors into the unchanged, source-reviewed benchmark catalog.

Collections are navigation, not new tasks, mathematical evidence or data splits.
SVGs are original schematic illustrations, never invented proof graphs.
"""
from __future__ import annotations

from html import escape
import hashlib
import json
from pathlib import Path

import astis_site
import sog_bench as bench

ROOT = Path(__file__).resolve().parents[2]
HUB = 'benchmarks/samplingoptimisationgeometrybench/'
MARKER = 'data-sog-bench="true"'


def configuration() -> dict:
    data = json.loads((ROOT / 'website/content/bench_navigation.json').read_text(encoding='utf-8'))
    domains = set(bench.curriculum.curriculum()['domains'])
    if data['schema_version'] != 1 or [c['id'] for c in data['collections']] != ['sampling', 'optimisation', 'geometry']:
        raise ValueError('Bench navigation requires the three canonical collections')
    if set().union(*(set(c['domains']) for c in data['collections'])) != domains:
        raise ValueError('Bench navigation must cover precisely the canonical seven domains')
    return data


def members(cores: list[dict], collection: dict) -> list[dict]:
    return [c for c in cores if set(c['library_domains']) & set(collection['domains'])]


def sketch(kind: str) -> str:
    drawings = {
        'sampling': '<path d="M20 118C60 118 64 25 124 25S190 118 238 118"/><path class="secondary" d="M20 132C76 132 90 65 137 65S204 132 238 132"/><circle cx="58" cy="88" r="5"/><circle cx="108" cy="29" r="5"/><circle cx="167" cy="50" r="5"/><circle cx="212" cy="105" r="5"/>',
        'optimisation': '<path d="M25 30Q125 224 235 30"/><path class="secondary" d="M54 52L83 91L110 119L129 126"/><circle cx="54" cy="52" r="5"/><circle cx="83" cy="91" r="5"/><circle cx="110" cy="119" r="5"/><circle cx="129" cy="126" r="5"/>',
        'geometry': '<ellipse cx="131" cy="83" rx="77" ry="66"/><ellipse class="secondary" cx="131" cy="83" rx="77" ry="23"/><path class="secondary" d="M131 17C83 43 83 124 131 149M131 17C179 43 179 124 131 149"/><path d="M169 48L225 24M169 48L215 80"/><circle cx="169" cy="48" r="5"/>',
        'lean': '<path d="M54 82L125 38M54 82L125 125M125 38L210 82M125 125L210 82"/><rect x="31" y="62" width="46" height="40" rx="9"/><rect x="103" y="18" width="46" height="40" rx="9"/><rect x="103" y="105" width="46" height="40" rx="9"/><rect x="188" y="62" width="46" height="40" rx="9"/>',
        'functor': '<circle cx="53" cy="38" r="17"/><circle cx="53" cy="126" r="17"/><circle cx="209" cy="82" r="22"/><path class="secondary" d="M71 38Q142 38 147 82Q142 126 71 126M147 82H186"/>',
        'libraries': '<rect x="38" y="32" width="54" height="104" rx="7"/><rect x="102" y="19" width="54" height="117" rx="7"/><path d="M170 36L211 27L235 128L194 138Z"/><path class="secondary" d="M52 49H78M116 38H142M54 116H76M119 116H141"/>',
        'bench': '<path d="M26 118L78 48L130 92L180 31L235 73"/><circle cx="78" cy="48" r="14"/><circle cx="130" cy="92" r="14"/><circle cx="180" cy="31" r="14"/><path class="secondary" d="M25 145H237"/>',
    }
    return ('<svg class="sog-sketch" viewBox="0 0 260 165" aria-hidden="true" focusable="false">'
            + drawings[kind] + '</svg>')


def card(title: str, caption: str, href: str, kind: str, *, extra: str = '', download: bool = False) -> str:
    return ('<a class="sog-portal-card"' + (' download' if download else '') + ' href="' + escape(href, quote=True) + '">'
            + sketch(kind) + '<div><h2>' + escape(title) + ' <span aria-hidden="true">↗</span></h2>'
            + '<p>' + escape(caption) + '</p>' + extra + '</div></a>')


def fold(title: str, content: str) -> str:
    return '<details class="sog-fold"><summary>' + escape(title) + '</summary>' + content + '</details>'


def home(cores: list[dict], graphs: list[dict]) -> str:
    portals = ''.join(card(c['name'], c['caption'], c['id'] + '/index.html', c['illustration'],
        extra='<small>' + str(len(members(cores, c))) + ' task cores</small>') for c in configuration()['collections'])
    return (f'<article class="sog-reader sog-hub" {MARKER}><p class="eyebrow">Mathematics &amp; agentic proof</p>'
        '<h1 class="sog-name">Sampling-<wbr>Optimisation-<wbr>Geometry-Bench</h1>'
        '<p class="lede">Choose a field to begin.</p>'
        '<section class="sog-portal-grid" aria-label="Three benchmark collections">' + portals + '</section>'
        '<nav class="sog-launches" aria-label="Use the benchmark"><a href="evaluation/index.html">Evaluate a model →</a>'
        '<a href="training/index.html">Get training data →</a><a href="experts/index.html">Inspect proof evidence →</a></nav>'
        '<p class="sog-caption">Public-dev collections overlap. No held-out test or measured leaderboard is claimed.</p>'
        + fold('Coverage, downloads and readiness',
            f'<p>{len(cores)} mathematical cores · {len(bench.prompts(cores))} mathematical QA views · {len(graphs)} structural tasks.</p>'
            '<p><a href="curriculum/index.html">Seven-domain L1–L5 coverage</a> · <a href="natural-language/index.html">Natural-language QA</a> · <a href="lean/index.html">Lean QA</a> · <a href="graph-json/index.html">Graph QA</a></p>'
            '<p><a href="downloads/questions.jsonl" download>Prompt-only JSONL</a> · <a href="downloads/reviewed-questions.jsonl" download>editorially reviewed prompts</a> · <a href="downloads/manifest.json">Version and hashes</a> · <a href="pilot.zip" download>Download the full pilot</a></p>'
            '<p>Reviewed subsets use content-bound AI editorial acceptance, not empirical difficulty calibration or a certificate for arbitrary submitted proofs.</p>'
            '<p>Natural-language scoring needs mathematical assessment. Graph JSON and the experimental fixed-target Linux Lean CLI have different contracts; neither supplies a measured model score. Hosted Lean execution, empirical calibration and private families remain open.</p>')
        + fold('Numbered textbook exercises and our reference solutions',
            '<p><a href="textbook-exercises/index.html">Textbook exercises &amp; answers</a></p>'
            '<p>Complete original answers, exact source numbers and separately checked Lean scope.</p>'
            '<p>Intake itself is not admission: a source exercise needs a complete answer, exact formal-coverage boundaries and current independent review before entering the reviewed subset.</p>'
            '<p><a href="downloads/TEXTBOOK_EXERCISES.md">Verified source intake and admission checklist</a> · <a href="../../libraries/optimisation/chapter-03.html#chewi-opt-v1-exercise-3-2">Existing Chewi Optimization Exercise 3.2 source/solution window</a></p>')
        + '<p class="sog-caption">Illustrations are navigation sketches, not proof-dependency evidence.</p></article>')


def collection_page(cores: list[dict], collection: dict) -> str:
    selected = members(cores, collection)
    rows = []
    for core in selected:
        tracks = ' · '.join(('NL' if t == 'natural-language' else 'Lean') + ' ' + level for t, level in core['track_levels'].items())
        rows.append('<a class="sog-task-row" href="../' + core['id'] + '.html"><span>'
                    + escape(core['title']) + '</span><small>' + escape(core['id'] + ' · ' + tracks) + '</small><b aria-hidden="true">→</b></a>')
    return (f'<article class="sog-reader sog-hub" {MARKER} data-sog-collection="{collection["id"]}"><header class="sog-collection-heading">'
        + sketch(collection['illustration']) + '<div><p class="eyebrow">Sampling-Optimisation-Geometry-Bench</p><h1>'
        + escape(collection['name']) + '</h1><p>' + escape(collection['caption']) + '</p></div></header>'
        '<nav class="sog-launches"><a href="questions.jsonl" download>Download prompt-only questions →</a><a href="../evaluation/index.html">Evaluate →</a><a href="../training/index.html">Train →</a></nav>'
        '<p class="sog-caption">Public-dev · shared task identities · <a href="manifest.json">Dataset manifest</a></p>'
        '<section aria-label="Task list" data-sog-task-list><h2>Choose a task</h2>'
        '<label class="sog-task-search">Find a task<input type="search" placeholder="Topic, task ID or level"></label>'
        + ''.join(rows) + '<p class="sog-caption" data-sog-list-status role="status"></p>'
        '<button class="sog-show-more" type="button" data-sog-show-more hidden>Show more tasks</button></section>'
        + fold('Scope and difficulty', '<p>These are views of the same catalog, not new datasets. A cross-listed core keeps its identity, family, split and source binding. NL/Lean levels are provisional, not empirically calibrated.</p>'
            '<p>Topics: ' + ', '.join(escape(bench.curriculum.curriculum()['domains'][d]) for d in collection['domains']) + '.</p>') + '</article>')


def collection_assets(downloads: Path, cores: list[dict], collection: dict) -> dict[str, bytes]:
    """Project only already-admitted prompts, preserving each original row byte."""
    source = (downloads / 'reviewed-questions.jsonl').read_bytes()
    identities = {c['id'] for c in members(cores, collection)}
    rows = [line for line in source.splitlines(keepends=True) if json.loads(line)['id'] in identities]
    records = [json.loads(line) for line in rows]
    if any({'lean_reference','steps','rubric','answer','solution'} & set(row) for row in records):
        raise ValueError('Collection prompts must not contain reference or grading material')
    questions = b''.join(rows)
    manifest = {
        'schema_version':1, 'display_name':configuration()['display_name'],
        'collection':collection, 'usage':'Public-dev projection, not an unseen or independent test split.',
        'identity_policy':'Original core/family/split/binding preserved; overlapping collections are not independent samples.',
        'core_ids':sorted({r['id'] for r in records}), 'qa_views':len(records),
        'source_reviewed_prompts_sha256':hashlib.sha256(source).hexdigest(),
        'source_manifest_sha256':hashlib.sha256((downloads/'manifest.json').read_bytes()).hexdigest(),
        'files':{'questions.jsonl':hashlib.sha256(questions).hexdigest()},
        'includes_reference_answers':False,
        'license_scope':'../downloads/LICENSE_SCOPE.md',
    }
    return {'questions.jsonl':questions, 'manifest.json':(json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()}


def evaluation_page() -> str:
    git=astis_site.git_context()
    repository=git.web_root or 'https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib'
    source_root=escape(f'{repository}/blob/{git.commit}',quote=True)
    return (f'<article class="sog-reader sog-hub" {MARKER}><h1>Evaluate a model</h1><p class="lede">Choose what you want to measure.</p>'
        '<div class="sog-portal-grid">'
        + card('Mathematical reasoning', 'Natural-language answers, checked against a mathematical rubric.', 'guide.html', 'optimisation', extra='<small>Human-assessed · available</small>')
        + card('Agentic Lean', 'Fixed proof targets. General hosted execution is not ready.', '../lean/index.html', 'lean', extra='<small>Experimental Linux CLI · hosted executor pending</small>')
        + card('Graph reasoning', 'Exact structural answers in the tested isolated Graph JSON runner.', '../graph-json/index.html', 'functor', extra='<small>Native Harbor adapter · available</small>')
        + '</div><p><a href="../downloads/EVALUATION.md">Run metadata, scoring and reproducibility</a> · <a href="../downloads/HARBOR.md">Native runtime guide</a></p>'
        + fold('Use the experimental Lean compiler workspace',
            '<p>For Linux operators: bounded proof checks, compiler feedback and one reserved final submission. This is not a hosted service or a model result.</p>'
            f'<p><a href="{source_root}/benchmarks/samplingoptimisationgeometrybench/lean-runtime/WORKSPACE.md">Setup and check/submit commands</a> · '
            f'<a href="{source_root}/runs/20261105-bench-lean-runtime/native08-independent-review.json">Exact native evidence and independent scope review</a></p>')
        + fold('Before reporting a score', '<p>Freeze prompts, family split, model/version, retrieval/tools, attempts and raw outputs. Keep answers out of evaluation prompts. Current data is public-dev; no unseen-generalization or measured model-ranking claim is supported.</p><p>Exact exposure checks: <a href="../downloads/public-exposure.json" download>Catalog snapshot</a> · <a href="../downloads/published-draft-exposure.json" download>Known public drafts</a> · <a href="../downloads/published-draft-exposure-sources.json">Draft provenance</a>. These do not certify novelty.</p><p>Recorded human rubric judgments are not automatically verified mathematics.</p>') + '</article>')


def training_page() -> str:
    return (f'<article class="sog-reader sog-hub" {MARKER}><h1>Train or develop a model</h1>'
        '<p class="lede">Choose inputs without mixing questions and answers.</p><div class="reader-home-grid">'
        + card('Prompt-only tasks', 'Instructions, questions and response templates. No gold answers.', '../downloads/agent-tasks.zip','bench',download=True)
        + card('Reviewed training pairs', 'Mathematical answers and aligned Lean references. Contains answers.', '../downloads/training-pairs.jsonl','lean',download=True)
        + '</div><p class="sog-caption">All current families are public-dev. Keep training answers out of evaluation prompts.</p>'
        + fold('Native graph runner details', '<p>Graph JSON only; not an arbitrary Lean executor.</p>'
            '<p><a href="../downloads/harbor-graph-tasks.zip" download>Download Harbor operator package</a></p>'
            '<p>Includes oracle answers and verifier material: never give this full ZIP to a closed-book agent.</p>'
            '<p><a href="../downloads/HARBOR.md">Runtime requirements and commands</a></p>')
        + '<p><a href="guide.html">Complete training and environment guide →</a> · <a href="../downloads/task-index.json">Task API →</a></p></article>')
