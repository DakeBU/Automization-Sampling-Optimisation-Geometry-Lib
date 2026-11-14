"""First-class finite-state library using the existing Samplinglib page factory.

Metadata/route acceptance never certifies a theorem or a conceptual functor.
"""
from __future__ import annotations
import hashlib
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE_MAP = ROOT / 'Libraries/DiscreteSampling/source-map.json'
BASE = 'libraries/discrete-sampling/'
BRIDGES = ('discrete-pi', 'discrete-mlsi', 'discrete-transport', 'discrete-influence')


def load() -> dict:
    return json.loads(SOURCE_MAP.read_text(encoding='utf-8'))


def validate_data(data=None, model=None, source_pdf: Path | None = None) -> None:
    data = load() if data is None else data
    def require(ok, message):
        if not ok:
            raise ValueError('Discrete Sampling: ' + message)
    require(data['library_id'] == 'discrete-sampling', 'wrong library identity')
    require(data['arxiv_id'] == '2307.13826v4', 'edition drift')
    require(data['authors'] == ['Zongchen Chen', 'Daniel Štefankovič', 'Eric Vigoda'], 'source authors drift (not project authors)')
    digest = data.get('sha256', '')
    require(len(digest) == 64 and all(c in '0123456789abcdef' for c in digest), 'source needs a byte fingerprint')
    require(data['pdf_pages'] == 100, 'source pagination drift')
    rows = data['chapters']; ids = {r['id'] for r in rows}
    require([r['id'] for r in rows] == [f'{i:02d}' for i in range(1, 13)], 'twelve source sections required')
    require(sum(len(r['sections']) for r in rows) == 72, 'source subsection inventory drift')
    seen = set()
    for r in rows:
        require(r['status'] == 'scaffold', 'source scaffold cannot assert a Lean closure')
        require(r['path'] == f"chapter-{r['id']}.html", 'unstable chapter path')
        for entry in [r, *r['sections']]:
            require(1 <= entry['pdf_page'] <= 100 and entry['printed_page'] == entry['pdf_page'], 'bad page anchor')
        for s in r['sections']:
            require(s['id'] not in seen and s['id'].split('.')[0] == str(int(r['id'])), 'duplicate or misplaced section')
            seen.add(s['id'])
    require(rows[-1]['source_detail_status'] == 'cites_external', 'Section 12 proofs must remain external')
    edges = data['planned_prerequisites']
    require(all(a in ids and b in ids for a,b in edges), 'dangling planned prerequisite')
    visited=set()
    while visited != ids:
        ready={n for n in ids-visited if all(a in visited for a,b in edges if b==n)}
        require(bool(ready), 'planned prerequisite cycle')
        visited |= ready
    require({x['id'] for x in data['source_issues']} >= {'discrete-glauber-copy-index','discrete-ising-proof-gap'}, 'known source issues lost')
    if source_pdf is not None:
        require(hashlib.sha256(source_pdf.read_bytes()).hexdigest() == digest, 'downloaded PDF differs from audited bytes')
    if model is None:
        model = json.loads((ROOT/'website/content/functor_hypergraph.json').read_text())
    lookup={e['id']:e for e in model['hyperedges']}
    for slug in BRIDGES:
        e=lookup['transport:'+slug]
        require('concept:discrete-sampling' in e['heads'], 'bridge lacks discrete target')
        require(e['status']=='not-Lean-certified' and not e['formal_refs'], 'conceptual mirror is not a certified transport')
        review=e.get('review', {})
        require(review.get('status') in {'candidate','independently-reviewed'}, 'review state required')
        require(bool(review.get('proposed_by')), 'proposer required')
        if review['status']=='independently-reviewed':
            require(bool(review.get('independent_reviewer')) and review['independent_reviewer'] != review['proposed_by'], 'no self-validation')
            require(isinstance(review.get('evidence'),list) and bool(review['evidence']), 'independent source review evidence required')


def write_pages(output: Path, shelves) -> None:
    import astis_site
    data=load();validate_data(data)
    commit = astis_site.git_context().commit
    body=shelves.index_body(eyebrow='Discrete Sampling Library', title='Discrete Sampling', lede='Ising / Glauber dynamics, hard-core models, colourings and matroids. Finite state spaces—not Euler discretization of continuous sampling.', source=data['source_url'], chapters=(), contract='Search Samplinglib, Mathlib and compatible upstreams before defining anything. Reuse one shared probability/Dirichlet/entropy floor, keep finite-state adapters explicit, and publish conceptual mirrors through the independent-review protocol.')
    cards=''.join(f'''<article class="library-chapter-card"><div class="library-chapter-number">{r['id']}</div><div><div class="card-meta">{shelves.badge('scaffold')}</div><h2><a href="{r['path']}">{escape(r['title'])}</a></h2><p>Source section {int(r['id'])} · printed/PDF p. {r['pdf_page']}. Source map, not Lean completion.</p></div></article>''' for r in data['chapters'])
    body=body.replace('<div class="library-chapter-list"></div>',f'<div class="library-chapter-list">{cards}</div>')
    refs=''.join(f'''<article><h3>{escape(s['title'])}</h3><p><strong>{escape(s['role'])}</strong> · {escape(s['use'])}</p><a href="{escape(s['url'])}">Source ↗</a></article>''' for s in data['supporting_sources'])
    body += f'''<section class="library-integration-note" id="primary-source"><h2>Primary source and supplementary roles</h2><p><strong>{escape(data['primary_title'])}</strong> — {escape(', '.join(data['authors']))}. arXiv:2307.13826v4; 100 pages. This is a modern spectral-independence monograph, not an exhaustive book on every discrete sampler.</p><p>{escape(data['edition_note'])}</p><p>PDF SHA-256: <code class="source-fingerprint">{data['sha256']}</code></p><div class="upstream-library-grid">{refs}</div></section>
<section class="library-integration-note" id="entry-route"><h2>Start with the shared floor, not page order</h2><p>Read §§1.1–1.3 and pull §3 forward for kernels, reversibility, Dirichlet forms and gap. Read §12.1 model definitions early for Ising; advanced mixing waits for exact proof prerequisites. Then branch through §2/§4.1 pinnings, §§4–6 local-to-global and entropy, or §§7–8 matroids.</p><p>Finite kernels do not wait for SDEs, spatial derivatives or manifold calculus. Shared scalar decay and probability algebra are reusable; a chain-dependent metric or finite-jump dissipation identity needs its own adapter.</p><p><a href="../../progress/index.html#discrete-sampling">Discrete Sampling Route</a> · <a href="../../lean-foundations.html?view=functor&amp;focus=concept:discrete-sampling">Functor Hypergraph</a> · <a href="../../lean-foundations.html?view=lean">Lean Branches</a></p></section>
<section class="library-integration-note" id="source-boundaries"><h2>Known source boundaries</h2><p>Section 12 states Ising/colouring extensions without their proofs. Follow each cited original paper and keep model/temperature/field/degree assumptions. The general update at §1.3 p.5 also has a copy-index discrepancy between its formula and prose: a correction is a recorded repair candidate, not a silent rewrite.</p><p><a href="https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/blob/{commit}/docs/discrete-sampling-protocol.md">Contributor protocol and clock contract ↗</a></p><p>All twelve pages are scaffolds. New conceptual bridges are explicitly candidate, awaiting independent review; none is a Lean-certified functor.</p></section>'''
    astis_site.write_page(output,BASE+'index.html',astis_site.page('Discrete Sampling',BASE+'index.html',body,active='Libraries'))
    for i,row in enumerate(data['chapters']):
        rel=BASE+row['path'];url=f"{data['source_url']}#page={row['pdf_page']}"
        body=shelves.chapter_body('Discrete Sampling',f"Source section {int(row['id'])}",row['title'],url,'Search PMF/measure/kernel, finite matrix, conditional probability, variance and entropy APIs before adding route-local definitions.',source_label=f"arXiv:2307.13826v4 · printed/PDF p. {row['pdf_page']}")
        anchors=''.join(f'''<li id="section-{s['id'].replace('.','-')}"><a href="{data['source_url']}#page={s['pdf_page']}">§{s['id']} · {escape(s['title'])}</a> <small>printed/PDF p. {s['pdf_page']}</small></li>''' for s in row['sections'])
        prev=f'<a href="{data["chapters"][i-1]["path"]}">← Previous</a> · ' if i else ''
        nxt=f' · <a href="{data["chapters"][i+1]["path"]}">Next →</a>' if i+1<len(data['chapters']) else ''
        body+=rf'''<section class="library-integration-note"><h2>Mathematical orientation</h2><div class="math-display">\[{escape(row['formula'])}\]</div><p>{escape(row['guide'])}</p><p>This is ASTIS orientation, not a verbatim theorem or completed Lean proof. Pin each source theorem, hypotheses and clock before claiming a Frontier Cell.</p><h2>Section source map</h2><ol>{anchors}</ol><p>{prev}<a href="index.html">Book contents</a>{nxt}</p><p><a href="../../progress/index.html#discrete-sampling">Shared route</a> · <a href="../../lean-foundations.html?view=functor&amp;focus=concept:discrete-sampling">Conceptual bridges</a></p></section>'''
        astis_site.write_page(output,rel,astis_site.page(f"Discrete Sampling {int(row['id'])}: {row['title']}",rel,body,active='Libraries'))


def route_panel(grouped, panel) -> str:
    return panel(route_id='discrete-sampling',anchor='discrete-sampling',title='Discrete Sampling Route',eyebrow='Chen · Štefankovič · Vigoda',status='scaffold',source_label='Open library',source_url='../libraries/discrete-sampling/index.html',lede='Finite-state Ising/Glauber, hard-core and matroid sampling. Same shared graph and source/mirror gates; not continuous-sampling time discretization.',items=[('scaffold','Pinned source and Ising entry','12 sections, 72 anchors; read Ising definitions early. Section 12 mixing proofs must be recovered from cited original papers.'),('planned','Shared finite probability and kernel floor','Reuse PMF, measures, kernels and finite linear algebra; fix support, feasible pinnings, reversibility and clock before mixing.'),('planned','Dirichlet / entropy / local-to-global','Pull §3 forward; prove finite dissipation adapters, uniform conditional-influence bounds and factorization with the exact normalization.'),('candidate','Cross-domain conceptual mirrors','PI/chi-square, modified LSI/KL, finite transport geometry and conditional covariance. Independent source review never substitutes for a Lean transport certificate.')],cells=grouped['discrete-sampling'],actions='<p><a class="button" href="#shared-order">Shared prerequisite order</a></p>')


def add_to_graph(builder) -> None:
    data=load()
    builder.add('library:discrete-sampling','library','Discrete Sampling',status='planned',subtitle='peer finite-state source library · scaffold, not a Lean closure',url=BASE+'index.html')
    builder.edge('library:samplinglib','library:discrete-sampling','formalization route')
    for row in data['chapters']:
        nid=builder.add('library-chapter:discrete-sampling:'+row['id'],'library-chapter',row['id']+'. '+row['title'],status='planned',subtitle='source section scaffold · printed/PDF p. '+str(row['pdf_page']),url=BASE+row['path'],source_url=data['source_url']+'#page='+str(row['pdf_page']))
        builder.edge('library:discrete-sampling',nid,'chapter scaffold')
    for a,b in data['planned_prerequisites']:
        builder.edge('library-chapter:discrete-sampling:'+a,'library-chapter:discrete-sampling:'+b,'planned prerequisite; not a proof dependency')


def validate_site(output: Path) -> None:
    import library_shelves
    validate_data()
    canonical=set(library_shelves.canonical_theme_styles(output))
    for rel in [BASE+'index.html',*[BASE+r['path'] for r in load()['chapters']]]:
        path=output/rel
        if not path.exists():raise ValueError('Missing Discrete Sampling page: '+rel)
        text=path.read_text(encoding='utf-8')
        if not canonical <= set(library_shelves.stylesheet_names(text)):raise ValueError('Discrete Sampling theme drift: '+rel)
        if 'Discrete Sampling Route' not in text:raise ValueError('Discrete Sampling route absent: '+rel)
    graph=json.loads((output/'data/underlying-lean-graph.json').read_text())
    nodes={n['id']:n for n in graph['nodes']}
    for ident in ['library:discrete-sampling','concept:discrete-sampling',*['library-chapter:discrete-sampling:'+r['id'] for r in load()['chapters']]]:
        if ident not in nodes:raise ValueError('Discrete graph node missing: '+ident)
    for slug in BRIDGES:
        node=nodes['transport:'+slug]
        if not any(d['label']=='Review status' and d['value']=='candidate' for d in node['details']):
            # Independently reviewed candidates have a different label value, but
            # must still satisfy validate_data's distinct-reviewer/evidence gate.
            if node['hyperedge']['review']['status']!='independently-reviewed':raise ValueError('Mirror review boundary hidden')
