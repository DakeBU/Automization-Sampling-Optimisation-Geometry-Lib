"""Small subject doors; canonical proofs, source maps and evidence stay where they are.

This module authors navigation/orientation, never theorem status. It projects
the existing finite-state proof readers and preserves complete textbook lists.
"""
from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re
import shutil

import astis_site
import information_architecture
import lower_bounds
import proof_readers
import source_lineage
from samplewiki_reader_contract import formula_html

ROOT = Path(__file__).resolve().parents[2]
SAMPLING = 'sampling/index.html'
OPT = 'libraries/optimisation/index.html'
DISCRETE = 'libraries/discrete-sampling/index.html'
SUBJECTS = ((SAMPLING, 'Sampling'), (OPT, 'Optimisation'),
            (lower_bounds.PAGE, 'Lower Bounds'), (DISCRETE, 'Discrete Sampling'))
MARKER = 'data-subject-reader="true"'
DISCRETE_READERS = ('random-scan-law', 'random-scan-reversibility')


def a(rel: str, target: str, label: str) -> str:
    return lower_bounds.link(target, label, page=rel)


def subject_nav(rel: str) -> str:
    return ('<nav class="subject-switcher" aria-label="Subjects">'
            + ''.join(a(rel, p, label) for p, label in SUBJECTS) + '</nav>')


def card(rel: str, target: str, title: str, description: str) -> str:
    return f'<article><h3>{a(rel, target, title)}</h3><p>{escape(description)}</p></article>'


def evidence_rows(data: dict) -> list[dict]:
    """Do not infer that 'scaffold' in a book inventory erases existing shared Lean."""
    items = {i['id']: i for i in proof_readers.load_items()}
    return [{**items[key], 'evidence': proof_readers.evidence(items[key], data)}
            for key in DISCRETE_READERS]


def discrete_proofs(rows: list[dict]) -> str:
    result = []
    for row in rows:
        ev = row['evidence']
        label = 'Compiled' if ev['compiled'] else 'Compilation not certified by this build'
        # Display raw canonical audit/Cell states instead of deriving a new badge.
        label += f' · Cell: {ev["cell_status"]} · source review: {ev["source_review"]}'
        result.append('<li>' + a(DISCRETE, 'proofs/' + row['id'] + '.html', row['title'])
                      + f'<p>{escape(row["purpose"])}</p><small>{escape(label)}</small></li>')
    return '<ol class="subject-path">' + ''.join(result) + '</ol>'


def sampling_body() -> str:
    rel = SAMPLING
    return (f'<article class="resource-reader subject-reader" {MARKER}>' + subject_nav(rel)
            + '<header><p class="eyebrow">Samplinglib · subject guide</p><h1>Sampling</h1>'
            '<p class="lede">Choose a target class, learn the proof tools, then follow a research result.</p></header>'
            '<section><h2>Where would you like to start?</h2><div class="resource-grid sampling-doors">'
            + card(rel, 'example-cases/samplewiki.html', 'Research problems and new results',
                   'Browse sampling regimes first; open a paper for its statement, proof route and verified pieces.')
            + card(rel, 'textbook/index.html', 'Log-Concave Sampling',
                   'Chewi’s continuous-state textbook: dynamics, functional inequalities and quantitative algorithms.')
            + card(rel, DISCRETE, 'Discrete Sampling',
                   'Finite configurations, conditional updates, reversibility and the route to fast mixing.')
            + card(rel, 'libraries/mcmc/index.html', 'MCMC methods',
                   'Markov kernels and Monte Carlo algorithms across target classes; invariance is not convergence.')
            + '</div></section><section><h2>A short reading path</h2><ol class="subject-path">'
            '<li><strong>Specify the problem.</strong> State space, oracle, target assumptions, initialization, discrepancy and cost.</li>'
            '<li><strong>Read the argument.</strong> A theorem statement comes before its formula proof. Open Lean beside an individual step when needed.</li>'
            '<li><strong>Check what is established.</strong> A compiled helper, a reviewed source theorem and a complete paper are different milestones.</li></ol>'
            '<p>' + a(rel, lower_bounds.PAGE, 'What can no algorithm do? Read Lower Bounds →') + '</p></section>'
            '<details><summary>Shared tools, research extensions and current work</summary><ul>'
            '<li>' + a(rel, 'textbook/research-extensions.html', 'Research results next to textbook prerequisites') + '</li>'
            '<li>' + a(rel, 'proofs/index.html', 'Readable shared proofs with adjacent Lean') + '</li>'
            '<li>' + a(rel, 'progress/index.html#samplewiki', 'Current cells and remaining proof obligations') + '</li>'
            '<li>' + a(rel, 'lean-foundations.html?view=lean', 'Inspect exact Lean nodes') + '</li></ul>'
            '<p>Reading-context links are not theorem implications. The source route and conceptual mirrors '
            'remain separate from compiler-backed Lean structure.</p></details></article>')


def discrete_body(rows: list[dict], original: str) -> str:
    rel = DISCRETE
    return (f'<article class="resource-reader subject-reader" {MARKER}>' + subject_nav(rel)
            + '<header><p class="eyebrow">Finite-state probability · Chen–Štefankovič–Vigoda</p>'
            '<h1>Discrete Sampling</h1><p class="lede">From a conditional update to an invariant law — '
            'then, separately, to a quantitative mixing theorem.</p></header>'
            '<section id="start-here"><h2>Start with one random-coordinate update</h2>'
            '<p>For a finite nonempty configuration space, nonnegative weights with positive total mass define</p>'
            + formula_html(r'Z=\sum_{x\in\Omega}w(x)>0,\qquad\pi(x)=w(x)/Z.')
            + '<p>Keep every other coordinate fixed and resample the selected coordinate from its conditional law. '
            'For a supported binary configuration, averaging those coordinate kernels gives one Glauber update:</p>'
            + formula_html(r'P=\frac1n\sum_{i=1}^{n}P_i,\qquad n\ge1.')
            + '<p>Null conditioning fibers need an explicit kernel convention. The existing Lean treatment handles '
            'zero target atoms; it does not assume full support. Read these two proofs in order:</p>'
            + discrete_proofs(rows) + '</section>'
            '<section id="beyond-invariance"><h2>What is still needed for fast mixing?</h2><div class="resource-grid">'
            + card(rel, 'libraries/discrete-sampling/chapter-03.html', 'Kernel → quantitative contraction',
                   'Reversibility alone leaves ergodicity, the right spectral gap and its quantitative bound open. Pull §3 forward.')
            + card(rel, 'libraries/discrete-sampling/chapter-04.html', 'Conditioning → local-to-global',
                   'Bound influences uniformly under every feasible pinning, then supply the stated factorization theorem.')
            + card(rel, 'libraries/discrete-sampling/chapter-12.html', 'Choose a model',
                   'Ising and colourings: retain graph, fields, temperature and boundary assumptions; §12 cites external proofs.')
            + '</div><details><summary>Clock, metric and entropy conventions</summary>'
            + formula_html(r'L=P-I\quad\text{(total rate 1)},\qquad L=n(P-I)\quad\text{(rate 1 per site)}.')
            + '<p>Updates and sweeps differ by n. Discrete-time mixing needs an absolute-gap, laziness or '
            'aperiodicity argument; a positive ordinary gap is not enough. Jump-chain modified LSI uses '
            'its own entropy dissipation, not the diffusion Fisher chain rule. Totalized log at zero is not a justification.</p>'
            '<p>' + a(rel, 'progress/index.html#discrete-sampling', 'See exact shared cells and open adapters')
            + '</p></details></section>'
            '<section><h2>Continue through the subject</h2><p>Start with §§1.1–1.3 and §3; then choose '
            'conditional influences (§2), local-to-global and entropy (§§4–6), or matroids (§§7–8). '
            'Hard-core is the running model in §1.2. No SDE prerequisite is imposed on finite kernels.</p>'
            '<p>' + a(rel, 'libraries/discrete-sampling/chapter-01.html', 'Open the source-aligned starting chapter')
            + ' · ' + a(rel, 'lean-foundations.html?view=functor&focus=concept:discrete-sampling', 'Compare conceptual mechanisms')
            + '</p></section><details class="subject-contents"><summary>All 12 source sections, references and source caveats</summary>'
            + original + '</details></article>')


def main_inner(text: str) -> str:
    match = re.search(r'<main\b[^>]*>(.*?)</main>', text, re.S)
    if not match:
        raise ValueError('Subject reader missing main')
    return match.group(1)


def enrich_site(output: Path) -> None:
    shutil.copyfile(ROOT / 'website/static/subject-readers.css', output / 'assets/subject-readers.css')
    text = astis_site.page('Sampling', SAMPLING, sampling_body(),
                          extra_head='<link rel="stylesheet" href="../assets/resource-library.css">')
    astis_site.write_page(output, SAMPLING, source_lineage.canonical_shell(text, SAMPLING, output))
    path = output / DISCRETE
    text = path.read_text(encoding='utf-8')
    original = main_inner(text)
    # Keep the full source inventory, without a second competing h1 or stale blanket claim.
    original = re.sub(r'<h1\b[^>]*>.*?</h1>', '', original, flags=re.S)
    original = original.replace('All twelve pages are scaffolds.',
        'The twelve-section inventory is a source map, not exhaustive theorem coverage; shared proofs are linked above.')
    text = information_architecture.replace_main(text, discrete_body(
        evidence_rows(json.loads((output / 'data/site-data.json').read_text(encoding='utf-8'))), original), DISCRETE)
    path.write_text(text, encoding='utf-8', newline='\n')
    path = output / OPT
    text = path.read_text(encoding='utf-8')
    orientation = (f'<section class="resource-reader subject-reader" {MARKER}>' + subject_nav(OPT)
        + '<h2>Choose your reading route</h2><div class="resource-grid">'
        + card(OPT, 'libraries/optimisation/chapter-01.html', 'Foundations → algorithms',
               'Convexity (§1), gradient flow (§2), smooth gradient descent (§3), then acceleration (§5).')
        + card(OPT, lower_bounds.PAGE, 'Lower bounds and oracle models',
               'Read §4 next to sampling hard instances. A shared mechanism is not yet a certified reduction.')
        + card(OPT, 'libraries/riemannian-optimization/index.html', 'Beyond Euclidean space',
               'Keep geometry, gradients, retractions and curvature assumptions explicit when comparing methods.')
        + '</div><p>' + a(OPT, 'progress/index.html#optimisation', 'Proof progress and open interfaces →')
        + '</p><p>Chapter labels below come from publication evidence. A proved exercise or sharpness example '
        'is not a complete chapter or an oracle-complexity lower bound.</p></section>')
    # Place route choices after the title, not between a contents heading and its list.
    marker = '<section class="library-integration-note">'
    pos = text.find(marker)
    if pos < 0:
        pos = text.find('<section><div class="section-heading"><span>Lecture-note contents')
    if pos < 0:
        raise ValueError('Optimisation chapter inventory missing')
    text = text[:pos] + orientation + text[pos:]
    text = re.sub(r'(<section><div class="section-heading"><span>Lecture-note contents.*?</section>)',
                  r'<details class="subject-contents"><summary>All 13 chapters and Appendix A</summary>\1</details>',
                  text, count=1, flags=re.S)
    text = re.sub(r'(<section class="library-integration-note">.*?</section>)',
                  r'<details class="subject-contents"><summary>Primary source and reuse boundaries</summary>\1</details>',
                  text, count=1, flags=re.S)
    path.write_text(text, encoding='utf-8', newline='\n')
    path = output / lower_bounds.PAGE
    text = path.read_text(encoding='utf-8').replace('<header>', subject_nav(lower_bounds.PAGE) + '<header>', 1)
    path.write_text(text, encoding='utf-8', newline='\n')
    for rel, _ in SUBJECTS:
        path = output / rel
        text = path.read_text(encoding='utf-8')
        p = astis_site.relative_prefix(rel)
        for name in ('resource-library.css', 'subject-readers.css'):
            if f'assets/{name}' not in text:
                text = text.replace('</head>', f'<link rel="stylesheet" href="{p}assets/{name}"></head>', 1)
        path.write_text(text, encoding='utf-8', newline='\n')


def validate_site(output: Path) -> list[str]:
    errors = []
    for rel, _ in SUBJECTS:
        text = (output / rel).read_text(encoding='utf-8')
        if 'aria-label="Subjects"' not in text:
            errors.append('Missing subject navigation: ' + rel)
        if text.count('<h1') != 1:
            errors.append('Subject reader needs one title: ' + rel)
    text = (output / DISCRETE).read_text(encoding='utf-8')
    for ident in DISCRETE_READERS:
        if f'proofs/{ident}.html' not in text:
            errors.append('Missing existing discrete proof reader: ' + ident)
    if 'All twelve pages are scaffolds.' in text:
        errors.append('Stale blanket discrete progress message')
    return errors
