"""A small hierarchical reader over the paired benchmark's canonical cores."""
from __future__ import annotations

from html import escape
import json
from pathlib import Path
import re
import shutil

import astis_site
import source_lineage
import sog_bench as bench
import sog_bench_graph_review as graph_review

ROOT = Path(__file__).resolve().parents[2]
HUB = 'benchmarks/samplingoptimisationgeometrybench/'
MARKER = 'data-sog-bench="true"'


def prose(text: str) -> str:
    # Stack independent comma-separated display identities, without changing
    # the audited source strings or shrinking their mobile math fonts.
    def stack(match):
        body = match.group(1)
        if r'\begin{' in body:
            return match.group(0)
        depth, start, parts = 0, 0, []
        for index, char in enumerate(body):
            if char in '{}' and (index == 0 or body[index-1] != '\\'):
                depth += 1 if char == '{' else -1
            if depth == 0 and body.startswith(r',\qquad', index):
                parts.append(body[start:index+1])
                start = index + len(r',\qquad')
        if not parts:
            return match.group(0)
        parts.append(body[start:])
        return r'\[\begin{gathered}' + r'\\'.join(parts) + r'\end{gathered}\]'
    rendered = re.sub(r'\\\[(.*?)\\\]', stack, text, flags=re.S)
    return '<p>' + escape(rendered) + '</p>'


def fold(title: str, content: str) -> str:
    return '<details class="sog-fold"><summary>' + escape(title) + '</summary>' + content + '</details>'


def domain_names(core: dict) -> str:
    labels = bench.curriculum.curriculum()['domains']
    return ' / '.join(labels[d] for d in core['library_domains'])


def review_panel(core: dict) -> str:
    row = bench.editorial_review([core])['items'][core['id']]
    label = {'accepted': 'AI editorial review accepted', 'accepted-after-repair': 'AI editorial review accepted after a separately reviewed correction',
             'pending': 'Independent QA review pending', 'stale': 'Previous review is stale for this content',
             'repair-required': 'Editorial repair required', 'reject': 'Editorial review rejected'}[row['editorial']]
    detail = prose(label + '. This is not canonical theorem publication, full Lean coverage or empirical difficulty calibration.')
    if row.get('remaining_unformalized'):
        detail += '<ul>' + ''.join('<li>' + escape(s) + '</li>' for s in row['remaining_unformalized']) + '</ul>'
    if row.get('issues'):
        detail += '<ul>' + ''.join('<li>' + escape(str(s)) + '</li>' for s in row['issues']) + '</ul>'
    detail += '<p><a href="downloads/editorial-review.json">Content-bound review status and evidence hashes</a> · <a href="https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/tree/main/benchmarks/samplingoptimisationgeometrybench/reviews">Independent reports and frozen inputs</a>. Historical rejected wording is audit material, not training gold.</p>'
    return fold('Editorial review and exact formal-coverage boundary', detail)


def home(cores: list[dict]) -> str:
    graphs = bench.curriculum.graph_items()
    review = bench.editorial_review(cores)
    structural = graph_review.summary(graphs)
    return (f'<article class="sog-reader" {MARKER}><div class="eyebrow">Public development curriculum · {escape(bench.load()["version"])}</div>'
        '<h1>SamplingOptimisationGeometryBench</h1><p class="lede">Can an AI explain the mathematics—and reconstruct a precise Lean proof?</p>'
        f'<p>{len(cores)} mathematical cores · {len(bench.prompts(cores))} mathematical QA views · {len(graphs)} structural graph tasks. {review["accepted_cores"]} mathematical cores and {structural["accepted_tasks"]} graph tasks have content-bound AI editorial acceptance. Review never supplies missing Lean coverage or empirical calibration.</p>'
        '<p><a class="button" href="curriculum/index.html">Browse seven domains and L1–L5 coverage</a></p>'
        '<section class="sog-grid"><article><h2>Natural-language QA</h2><p>Explain a proof, track its constants and identify what the assumptions do not imply. No Lean knowledge required.</p><a class="button primary" href="natural-language/index.html">Try natural-language questions</a></article>'
        '<article><h2>Lean-assisted QA</h2><p>Reconstruct a fixed theorem from its allowed imports and explicit context. Read the mathematical reasoning beside optional exact Lean.</p><a class="button" href="lean/index.html">Try Lean questions</a></article>'
        '<article><h2>Structured graph QA</h2><p>Distinguish module imports from selected constants in actual compiled proof bodies. Compare shared ingredients and proof branches without claiming mathematical necessity.</p><a class="button" href="graph-json/index.html">Try graph questions</a></article></section>'
        '<section><h2>Use the pilot</h2><p><a class="button" href="evaluation/index.html">Run and assess answers</a></p><p><a href="downloads/questions.jsonl" download>Prompt-only JSONL</a> · '
        '<a href="downloads/reference.jsonl" download>References and rubrics</a> · '
        '<a href="downloads/manifest.json" download>Version and hashes</a> · '
        '<a href="pilot.zip" download>Download the full pilot</a></p>'
        '<p>Prefer the separate <a href="downloads/reviewed-questions.jsonl" download>editorially reviewed prompts</a> and <a href="downloads/reviewed-reference.jsonl" download>reviewed references</a> for the reviewed subset. Review is AI editorial checking, not full Lean verification.</p>'
        '<p>Public questions and answers may already occur in training data. This is not an unseen test set, a model ranking, or evidence that a paper is fully formalized.</p></section>'
        + fold('Evaluation policy and contribution guide',
            '<p>Each pair shares one core, family and public-dev split. Score the two tracks separately. Human-assessed natural-language rubrics have four one-point criteria; no automated semantic grader is claimed.</p>'
            '<p>Lean compiler acceptance certifies the fixed proposition only. Arbitrary model output requires target-preservation checks and an isolated, resource-limited sandbox. No submission execution service or AI API is connected here.</p>'
            '<p>Only original or permission-cleared material may enter ML training/evaluation. Restricted external indexes and their derivatives are excluded. Each question discloses its current editorial status and remaining formal boundary; compilation is not that review. Future drafts require their own review.</p>'
            '<p><a href="downloads/README.md">Commands, grading protocol and how to add a core</a> · <a href="downloads/LICENSE_SCOPE.md">License boundaries</a></p>') + '</article>')


def track_page(cores: list[dict], track: str) -> str:
    title = 'Natural-language QA' if track == 'natural-language' else 'Lean-assisted QA'
    cores = [c for c in cores if track in c['track_levels']]
    cards = ''.join('<article><small>' + escape(domain_names(c)) + ' · ' + escape(c['track_levels'][track]) + ' (provisional)</small><h2>'
        + escape(c['title']) + '</h2><p>' + escape(c['id']) + ' · 4 rubric points · public-dev</p>'
        '<a class="button" href="../' + c['id'] + '.html?track=' + track + '#' + track + '">Open question</a></article>' for c in cores)
    return (f'<article class="sog-reader" {MARKER}><p><a href="../index.html">Bench overview</a></p><h1>{title}</h1>'
        f'<p>{len(cores)} available views. Missing equivalent Lean tasks remain gaps, not borrowed proof credit. Reference answers stay closed until you choose to read them.</p>'
        '<div class="sog-grid">' + cards + '</div></article>')


def core_page(core: dict, checked: bool, graph_ids: set[str] | None = None, known: dict | None = None, structural: list[dict] | None = None) -> str:
    from urllib.parse import quote
    rel = HUB + core['id'] + '.html'
    known = known or astis_site._SOURCE_BY_NAME or {d.full_name: d for d in astis_site.scan_project_sources()[1]}
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
    if not bench.has_lean(core):
        lean = prose(core['lean_explanation'])
        if core.get('support_source_view'):
            lean += (fold('Supporting library Lean (not an aligned QA task)',
                '<div data-lean-code-panel><button type="button" data-lean-copy>Copy supporting module</button>'
                '<span data-lean-copy-status role="status" aria-live="polite"></span>'
                + astis_site.code_html(core['support_lean_source']) + '</div>'
                '<p><a href="downloads/lean/' + core['id'] + '-support.lean" download>Download exact supporting module</a>'
                ' · Uses the project toolchain and its listed imports; not a standalone replacement QA proof.</p>'))
    formal_view = ('<section id="lean"><h2>Lean question</h2><p>Keep the target and context fixed; replace the comment slot with your proof. Ancestor libraries are allowed, but the target module is not imported directly.</p>'
        + fold('Show fixed Lean task', astis_site.code_html(core['lean_task'])
               + '<p><a href="downloads/lean/' + core['id'] + '-task.lean.txt" download>Download task template</a></p>')
        + fold('Reference Lean and explanation', lean) + prose(status) + '</section>') if bench.has_lean(core) else (
        '<section id="lean"><h2>Lean view: not yet aligned</h2>' + lean + '<p>This support theorem does not certify the complete QA or its explanatory counterexamples.</p></section>')
    dependencies = ''.join('<h3>' + label + '</h3><ul>' + ''.join('<li><code>' + escape(n) + '</code></li>' for n in core['dependencies'][key]) + '</ul>'
                           for key, label in (('astis', 'ASTIS definitions / proof calls' if bench.has_lean(core) else 'ASTIS formal support (not an equivalent QA)'), ('mathlib', 'Mathlib facts / definitions')))
    related=[g for g in (bench.curriculum.graph_items() if structural is None else structural) if g.get('core_id')==core['id']]
    graph_links=('<p>Structural questions about this proof context (not equivalent mathematical tasks): '+
                 ' · '.join('<a href="'+g['id']+'.html">'+escape(g['title'])+'</a>' for g in related)+'</p>') if related else ''
    return (f'<article class="sog-reader" {MARKER}><p><a href="index.html">Bench</a> / ' + escape(core['domain']) + '</p>'
        '<div class="eyebrow">' + escape(core['id']) + ' · public-dev · editorial and formal status separate</div><h1>' + escape(core['title']) + '</h1>'
        + '<p>' + escape(domain_names(core)) + ' · ' + escape(' / '.join(t + ': ' + l for t, l in core['track_levels'].items())) + ' (author-assigned; calibration pending)</p>'
        + fold('Why this difficulty?', prose(core['difficulty_reason']))
        + review_panel(core)
        + '<section><h2>Assumptions and conventions</h2>' + assumptions + '</section>'
        '<section id="natural-language"><h2>Natural-language question</h2>' + prose(core['question'])
        + fold('Reference mathematical proof', proof + fold('How the Lean proof follows these steps' if bench.has_lean(core) else 'Formal support and missing Lean alignment', lean))
        + fold('Assessment rubric · 4 points', rubric) + '</section>'
        + formal_view
        + graph_links + '<section><h2>What this does—and does not—verify</h2>' + prose(core['boundary'])
        + '<p>Existing library mathematics reused; no new mathematical leaf or paper-completion credit. The editorial panel records the exact current review scope and remaining unformalized explanation.</p></section>'
        + fold('Sources, graph location and dependencies', prose(core['source_note'])
            + '<p><a href="' + escape(href) + '">Exact local source and full context</a> · <a href="../../underlying-lean-graph/index.html?focus='
            + quote(graph_id, safe='') + '">' + graph_label + '</a></p><p><code>' + escape(core['declaration']) + '</code></p>'
            + dependencies + '<p>Binding SHA-256: <code>' + core['binding_sha256'] + '</code></p>')
        + '</article>')


def curriculum_page(cores: list[dict]) -> str:
    policy = bench.curriculum.curriculum()
    cover = bench.coverage(cores, bench.curriculum.graph_items())
    editorial = bench.editorial_review(cores)
    rows = []
    for domain, name in policy['domains'].items():
        cells = [c for c in cover['cells'] if c['domain'] == domain]
        values = ''.join('<td>' + ('gap' if c['gap'] else ' / '.join(str(c['draft_views'][t]) for t in ('natural-language', 'lean', 'graph-json'))) + '</td>' for c in cells)
        rows.append('<tr><th><a href="../domains/' + domain + '.html">' + escape(name) + '</a></th>' + values + '</tr>')
    levels = ''.join('<li><a href="../levels/' + key + '.html"><strong>' + key + ' · ' + escape(row['label']) + '</strong></a>' + prose(row['criterion']) + '</li>' for key, row in policy['levels'].items())
    return (f'<article class="sog-reader" {MARKER}><p><a href="../index.html">Bench</a></p><h1>Domains and reasoning levels</h1>'
        '<p>Each cell shows available public-dev views as Natural language / Lean / Graph JSON. On small screens, scroll the table horizontally for L3–L5. A gap is not a proof-completion percentage. Shared questions can occur in several domain indexes but count once globally.</p>'
        '<div class="sog-table"><table><thead><tr><th>Domain</th>' + ''.join('<th>' + l + '</th>' for l in policy['levels']) + '</tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'
        '<h2>What the levels mean</h2><ol>' + levels + '</ol>' + prose(policy['difficulty_policy']) + prose(policy['graph_policy'])
        + f'<p>{editorial["accepted_cores"]} of {len(cores)} mathematical cores currently have AI editorial acceptance. Structural editorial status: {escape(cover["graph_editorial_status"])}. Empirical calibration remains open. L5 is a planned research-audit tier, not a claim of solved open problems.</p></article>')


def browse_page(cores: list[dict], key: str, *, domain: bool) -> str:
    policy = bench.curriculum.curriculum()
    title = policy['domains'][key] if domain else key + ' · ' + policy['levels'][key]['label']
    selected = [c for c in cores if key in c['library_domains']] if domain else [c for c in cores if key in c['track_levels'].values()]
    rows = ''.join('<li><a href="../' + c['id'] + '.html">' + escape(c['title']) + '</a> · '
        + escape(' / '.join(t + ': ' + l for t, l in c['track_levels'].items())) + '</li>' for c in selected)
    graphs = [g for g in bench.curriculum.graph_items() if (key in g['library_domains'] if domain else g['level'] == key)]
    graph_rows = ''.join('<li><a href="../' + g['id'] + '.html">' + escape(g['title']) + '</a> · ' + g['level'] + '</li>' for g in graphs)
    return (f'<article class="sog-reader" {MARKER}><p><a href="../curriculum/index.html">Curriculum</a></p><h1>' + escape(title)
        + '</h1><h2>Mathematical QA</h2>' + ('<ul>' + rows + '</ul>' if rows else '<p>No authored question at this tier yet. This is an explicit coverage gap.</p>')
        + '<h2>Structural graph QA</h2>' + ('<ul>' + graph_rows + '</ul>' if graphs else '<p>No structural question in this slice yet.</p>')
        + '<p>Difficulty is provisional. Each question discloses its own current editorial status; empirical calibration remains pending.</p></article>')


def graph_page(item: dict) -> str:
    prompt = bench.curriculum.graph_prompts([item])[0]
    evidence = graph_review.summary(bench.curriculum.graph_items())['items'][item['id']]
    status = '<p>Current editorial status: <strong>' + escape(evidence['editorial']) + '</strong>. This is AI review of structural QA, not a theorem or calibrated difficulty.</p>'
    status += '<ul>' + ''.join('<li>' + escape(s) + '</li>' for s in evidence.get('issues', []) + evidence.get('remaining_limits', [])) + '</ul>'
    status += '<p><a href="downloads/graph-editorial-review.json">Exact review bindings and report hashes</a> · <a href="https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/tree/main/benchmarks/samplingoptimisationgeometrybench/reviews/graph-4">Current independent review and explicit historical supersession</a></p>'
    compiled=item['context']['kind']=='compiled-proof-body-constant-occurrences'
    provenance=('<p>This is a recorded source-bound compiler snapshot. CI separately replays the trusted extractor. It is not a fresh Lean run in this browser, a full proof closure or a minimal-premise certificate. Unique proof constants do not count runtime invocations, recursive calls or oracle queries.</p><p><a href="downloads/compiled-transport-graph.json">Recorded compiler slice and provenance</a></p>') if compiled else '<p>This graph scans source import declarations, not theorem proof bodies.</p>'
    related=[c for c in bench.materialize() if c['id']!=item['core_id'] and c['declaration'] in item['context']['nodes']]
    background=('<p>Related exercises about selected statements: '+ ' · '.join(
        '<a href="'+c['id']+'.html">'+escape(c['title'])+'</a>' for c in related)+'.</p>') if related else ''
    return (f'<article class="sog-reader" {MARKER}><p><a href="graph-json/index.html">Graph QA</a></p><h1>' + escape(item['title']) + '</h1>'
        + '<p>' + item['level'] + ' · public-dev · structural QA, not a theorem proof</p>'
        + '<p><a href="'+item['core_id']+'.html">Read the source mathematical proof and optional Lean</a>. This is context linkage, not an equivalent mathematical question.</p>' + prose(item['question'])
        + '<p>Targets: ' + escape(', '.join(item['context'].get('node_labels',{}).get(n,n) for n in item['targets'])) + '</p>'
        + (prose(('Queried interface: ' if compiled else 'Removed module: ') + item['context'].get('node_labels',{}).get(item['remove'],item['remove'])) if 'remove' in item else '')
        + import_figure(item['context'])
        + background
        + fold('Independent structural review and limits', status)
        + fold('Evidence kind and source scope', provenance+prose(item['context']['truth_boundary']))
        + fold('Exact JSON snapshot and response schema', '<pre><code class="language-json">' + escape(json.dumps(prompt, indent=2)) + '</code></pre>')
        + fold('Reference structural answer · 2 checks, 1 point', '<pre><code>' + escape(json.dumps(item['answer'], indent=2)) + '</code></pre>'
            '<p>One point requires both the exact structural node set and a false mathematical-necessity certification. The constant boundary answer earns no standalone credit. Edges have only the stated evidence kind. Neither a positive path nor an absent induced path proves mathematical necessity or full-closure independence.</p>')
        + '<p>No model score, theorem-equivalence certificate or calibrated difficulty is asserted.</p></article>')


def evaluation_page() -> str:
    prepare = 'python tools/sog_bench_prose.py prepare --submissions responses.jsonl --run-metadata run.json --output .astis/sog-bench/runs/my-run'
    score = 'python tools/sog_bench_prose.py score --packet .astis/sog-bench/runs/my-run --adjudication completed.json --output .astis/sog-bench/runs/my-run-score.json'
    return (f'<article class="sog-reader" {MARKER}><p><a href="../index.html">Bench</a></p><h1>Run and assess answers</h1>'
        '<p class="lede">Keep the question, first answer and judgment traceable.</p>'
        '<p>Offline human-attested prose scoring is available. No model performance has been measured; no AI API or untrusted-Lean executor is connected.</p>'
        '<ol><li><strong>Choose first.</strong> Select core IDs, model/version, retrieval policy and tools before collecting answers. Give the model only the prompt-only records.</li>'
        '<li><strong>Freeze the run.</strong> Save raw first responses and metadata. The recorder binds prompts, references, rubric and answers by SHA-256; missing answers stay in the denominator.</li>'
        '<li><strong>Have a human assess it.</strong> Fill each frozen rubric criterion with 0/1 and a reason. The report records those judgments, not automatically verified mathematics or authenticated grader identity.</li></ol>'
        + fold('Commands and input formats',
            '<p>From the repository root, Python 3.11+:</p><pre><code>' + escape(prepare) + '</code></pre>'
            '<p>Copy the generated adjudication-template.json to completed.json. An actual human supplies grader identity, timestamp and all four criterion judgments per nonempty answer.</p>'
            '<pre><code>' + escape(score) + '</code></pre>'
            '<p><a href="../downloads/examples/prose-run.json" download>Run-metadata template</a> · <a href="../downloads/EVALUATION.md">Complete recording and scoring instructions</a></p>')
        + fold('Other tracks and scientific limits',
            '<p>Graph JSON has deterministic exact-snapshot scoring; it certifies no mathematical necessity. Lean reference compilation checks trusted references only, not arbitrary submissions.</p>'
            '<p>Human assessments require actual mathematical checking. No keyword grader or unvalidated AI grader is supplied. Run execution, retrieval compliance and human identity are not authenticated by this recorder.</p>'
            '<p>All current tasks are public-dev. These records cannot demonstrate unseen generalization, difficulty calibration or private-family evaluation. A paired core is not two independent samples.</p>')
        + '<p><a href="../downloads/reviewed-questions.jsonl" download>Reviewed prompt-only tasks</a> · <a href="../downloads/EVALUATION.md">Full protocol</a> · <a href="../graph-json/index.html">Structural graph QA</a></p></article>')


def graph_index_page(graphs: list[dict]) -> str:
    groups=(('source-scanned-module-imports','Source imports','Arrows record imported modules, not proof-term use.'),
            ('compiled-proof-body-constant-occurrences','Compiled proof bodies','Arrows record selected theorem constants in compiled proof bodies, not necessity or a full closure.'))
    sections=''
    for kind,title,note in groups:
        selected=[g for g in graphs if g['context']['kind']==kind]
        sections+='<section><h2>'+title+'</h2><p>'+note+'</p><ul>'+''.join(
            '<li><a href="../'+g['id']+'.html">'+escape(g['title'])+'</a> · '+g['level']+
            ' · <a href="../'+g['core_id']+'.html">mathematical source context</a></li>' for g in selected)+'</ul></section>'
    return (f'<article class="sog-reader" {MARKER}><p><a href="../index.html">Bench</a></p><h1>Structured graph QA</h1>'
        '<p>Choose the evidence kind before interpreting an arrow. These public-dev structural questions link to mathematical source cores but are not equivalent mathematics tasks or independent held-out samples.</p>'
        +sections+'<p><a href="../downloads/graph-questions.jsonl" download>Prompt-only graph JSONL</a> · <a href="../downloads/graph-reference.jsonl" download>Structural references</a></p>'
        '<p>Prefer the current admitted subset: <a href="../downloads/reviewed-graph-questions.jsonl" download>Reviewed graph prompts</a> · <a href="../downloads/reviewed-graph-reference.jsonl" download>Reviewed graph references</a> · <a href="../downloads/graph-editorial-review.json">Current review evidence</a>.</p></article>')


def import_figure(graph: dict) -> str:
    """Layout a bounded DAG from its real edges; no graph-theoretic proof credit."""
    nodes, edges = graph['nodes'], graph['edges']
    compiled=graph['kind']=='compiled-proof-body-constant-occurrences'
    ranks = {}
    def rank(node, active):
        if node in active:
            raise ValueError('Graph illustration requires an acyclic slice')
        if node not in ranks:
            ranks[node] = max([rank(b, active | {node}) + 1 for a, b in edges if a == node] or [0])
        return ranks[node]
    for node in nodes:
        rank(node, set())
    highest = max(ranks.values(), default=0)
    groups = {r: sorted(n for n in nodes if ranks[n] == r) for r in set(ranks.values())}
    width = max(660, 280 * (max(map(len, groups.values()), default=1) + 1))
    height = 100 + highest * 130
    positions = {n: ((i + 1) * width / (len(group) + 1), 45 + (highest - r) * 130)
                 for r, group in groups.items() for i, n in enumerate(group)}
    box_width=250
    if compiled:
        box_width=220
        width=max(660,250*max(map(len,groups.values()),default=1)+40)
        positions={n:((width-(len(group)*box_width+(len(group)-1)*30))/2+box_width/2+i*250,
                      45+(highest-r)*130) for r,group in groups.items() for i,n in enumerate(group)}
    style='' if compiled else 'stroke-dasharray="5 4"'
    paths = ''.join(f'<path d="M {positions[a][0]} {positions[a][1]+22} L {positions[b][0]} {positions[b][1]-22}" stroke="#657080" {style} fill="none" marker-end="url(#sog-arrow)"/>' for a, b in edges)
    boxes = ''.join(f'<g><title>{escape(n)}</title><rect x="{x-box_width/2}" y="{y-22}" width="{box_width}" height="44" rx="6" fill="#f5f6f8" stroke="#657080"/><text x="{x}" y="{y+4}" text-anchor="middle" font-size="14" fill="#17212f">{escape(graph.get("node_labels",{}).get(n,n.rsplit(".",1)[-1]))}</text></g>' for n, (x, y) in positions.items())
    label='Selected compiled proof-body occurrences; not full closure or mathematical necessity' if compiled else 'Source-scanned import graph; arrows point to imported modules, not theorem implication'
    caption='Solid arrows: selected theorem constants occur in the compiled proof bodies, including proof-term annotations. Other constants and private auxiliaries are omitted; a missing path is not full-closure independence.' if compiled else 'Dashed arrows: source-scanned imports in the supplied slice. The shared module occurs once.'
    return (f'<figure class="sog-graph"><svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" role="img" aria-label="{label}" viewBox="0 0 {width} {height}">'
        '<defs><marker id="sog-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#657080"/></marker></defs>'
        + paths + boxes + '</svg><figcaption>Scroll horizontally on a small screen. '+caption+' Neutral colours make no proof-status claim.</figcaption></figure>')


def enrich_site(output: Path) -> None:
    cores = bench.materialize()
    known = astis_site._SOURCE_BY_NAME or {d.full_name: d for d in astis_site.scan_project_sources()[1]}
    astis_site._SOURCE_BY_NAME=known
    checked = bench.receipt_current(cores)
    graph_ids = {n['id'] for n in json.loads((output / 'data/underlying-lean-graph.json').read_text(encoding='utf-8'))['nodes']}
    target = output / HUB
    target.mkdir(parents=True, exist_ok=True)
    bench.export(target / 'downloads', cores)
    bench.archive_bytes(target / 'downloads', target / 'pilot.zip')
    shutil.copyfile(ROOT / 'website/static/sog-bench.css', output / 'assets/sog-bench.css')
    pages = [('index.html', 'SamplingOptimisationGeometryBench', home(cores))]
    graphs = bench.curriculum.graph_items()
    pages += [(track + '/index.html', track.replace('-', ' ').title(), track_page(cores, track)) for track in bench.TRACKS]
    pages += [(c['id'] + '.html', c['title'], core_page(c, checked, graph_ids, known,graphs)) for c in cores]
    policy = bench.curriculum.curriculum()
    graphs = bench.curriculum.graph_items()
    pages.append(('curriculum/index.html', 'Bench curriculum', curriculum_page(cores)))
    pages.append(('evaluation/index.html', 'Run and assess answers', evaluation_page()))
    pages += [('domains/' + key + '.html', title, browse_page(cores, key, domain=True)) for key, title in policy['domains'].items()]
    pages += [('levels/' + key + '.html', key, browse_page(cores, key, domain=False)) for key in policy['levels']]
    pages += [(g['id'] + '.html', g['title'], graph_page(g)) for g in graphs]
    graph_index=graph_index_page(graphs)
    pages.append(('graph-json/index.html', 'Structured graph QA', graph_index))
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
    known = astis_site._SOURCE_BY_NAME or {d.full_name: d for d in astis_site.scan_project_sources()[1]}
    astis_site._SOURCE_BY_NAME=known
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
    policy = bench.curriculum.curriculum()
    graphs = bench.curriculum.graph_items()
    extra = ['curriculum/index.html', 'graph-json/index.html', 'evaluation/index.html',
             *('domains/' + d + '.html' for d in policy['domains']),
             *('levels/' + l + '.html' for l in policy['levels']), *(g['id'] + '.html' for g in graphs)]
    for rel in ['index.html', *(t + '/index.html' for t in bench.TRACKS), *(c['id'] + '.html' for c in cores), *extra]:
        path = output / HUB / rel
        if not path.is_file() or MARKER not in path.read_text(encoding='utf-8'):
            errors.append('Missing Bench reader: ' + rel)
    current_pages = {'index.html': home(cores), 'evaluation/index.html': evaluation_page(),
                     'graph-json/index.html':graph_index_page(graphs),
                     'curriculum/index.html': curriculum_page(cores),
                     **{'domains/' + d + '.html': browse_page(cores, d, domain=True) for d in policy['domains']},
                     **{'levels/' + l + '.html': browse_page(cores, l, domain=False) for l in policy['levels']},
                     **{g['id'] + '.html': graph_page(g) for g in graphs}}
    for rel, body in current_pages.items():
        path = output / HUB / rel
        if path.exists() and body not in path.read_text(encoding='utf-8'):
            errors.append('Stale Bench curriculum or structural graph: ' + rel)
    for core in cores:
        path = output / HUB / (core['id'] + '.html')
        if path.is_file() and core_page(core, checked, ids, known,graphs) not in path.read_text(encoding='utf-8'):
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
