"""Seventh peer source library and ASTIS-owned extended reading paths.

All mathematical entries are source-backed outlines, not fresh Lean certificates.
"""
from __future__ import annotations
import hashlib
import json
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT/'Libraries/MCMC/source-map.json'
BASE = 'libraries/mcmc/'


def load():
    return json.loads(PATH.read_text(encoding='utf-8'))


def validate_data(data=None):
    d=load() if data is None else data
    def req(b,m):
        if not b: raise ValueError('MCMC: '+m)
    req(d['library_id']=='mcmc','stable library identity required')
    req(d['primary']['version']=='2407.12751v1','primary version drift')
    req(d['pdf_pages']==244 and d['pdf_page_offset']==6,'primary pagination drift')
    req(len(d['primary']['sha256'])==64 and all(c in '0123456789abcdef' for c in d['primary']['sha256']),'primary fingerprint missing')
    req([c['id'] for c in d['chapters']]==['01','02','03','04','05','06'],'six primary chapters required')
    req(sum(len(c['sections']) for c in d['chapters'])==85,'primary subsection inventory drift')
    seen=set()
    for c in d['chapters']:
        req(c['status']=='scaffold','primary source environment is not a theorem certificate')
        for s in [c,*c['sections']]:
            req(s['pdf_page']==s['printed_page']+6 and 1<=s['pdf_page']<=244,'bad primary anchor')
            req(s['id'] not in seen,'repeated source id');seen.add(s['id'])
    req('mcmc-rr' in d['sources'] and d['sources']['mcmc-rr']['version']=='math/0404033v4','required Roberts–Rosenthal source absent')
    extids=set();paths=set()
    for e in d['extensions']:
        req(e['id'] not in extids and e['path'] not in paths,'duplicate extension');extids.add(e['id']);paths.add(e['path'])
        req(e['parent_chapter'] in {c['id'] for c in d['chapters']},'extension has no parent chapter')
        req(e['status']=='source-backed-outline' and e['truth_boundary'],'extension cannot assert proof completion')
        req(set(e['source_ids'])<=set(d['sources']) and e['source_ids'],'extension source unresolved')
    return d


def refs_html(d,ids):
    rows = []
    for key in ids:
        source = d["sources"][key]
        authors = ", ".join(source.get("authors", []))
        version = source.get("version", "author manuscript")
        pin_status = source.get("pin_status", "")
        rows.append(
            f'<p><a href="{esc(source["url"])}">{esc(source["title"])} ↗</a><br>'
            f'{esc(authors)} · {esc(version)}<br><small>{esc(source["anchor"])}<br>'
            f'{esc(pin_status)}</small></p>'
        )
    return "".join(rows)


def extension_cards(d,chapter=None):
    return ''.join(f'''<article class="library-chapter-card"><div class="library-chapter-number">{e['id']}</div><div><div class="card-meta"><span class="status status-gray">extended · outline</span></div><h2><a href="{e['path']}">{esc(e['title'])}</a></h2><p>Attached to primary Chapter {int(e['parent_chapter'])}. {esc(e['motivation'])}</p></div></article>''' for e in d['extensions'] if chapter is None or e['parent_chapter']==chapter)


def write_pages(output,shelves):
    import astis_site
    d=validate_data();commit=astis_site.git_context().commit
    body=shelves.index_body(eyebrow='MCMC Library · seventh peer source',title=d['title'],lede='A method-family view of sampling: general-state kernels, reversible and nonreversible algorithms, scalable computation and dependent-sample estimation.',source=d['primary']['url'],chapters=tuple(c['title'] for c in d['chapters']),contract='Source-facing statements follow Fearnhead–Nemeth–Oates–Sherlock. Reuse the shared kernel/measure/geometry floor; supplementary theorems keep their own sources and explicit convention adapters.')
    body+=f'''<section class="library-integration-note" id="primary-source"><h2>Controlling textbook</h2><p><strong>{esc(d['primary']['title'])}</strong><br>{esc(', '.join(d['primary']['authors']))}. The pinned reader is arXiv:2407.12751v1 (2024), 244 PDF pages; it is not a claim of identical pagination to the published edition.</p><p>Six primary chapters · 85 subordinate source anchors · PDF page = printed page + 6.</p><p>SHA-256: <code class="source-fingerprint">{d['primary']['sha256']}</code></p><p>The primary preface explicitly leaves some measure-theoretic details to references. Recover exact hypotheses; do not silently strengthen a target.</p></section>
<section class="library-integration-note" id="method-perspective"><h2>Methods overlap target classes</h2><p>MCMC is a major method family, not the set of all sampling methods. Log-concavity describes a target; discreteness describes its state; geometry describes the analysis. ULA/MALA, Hit-and-Run and Glauber therefore connect several library views without nesting whole textbooks.</p><p><a href="../../lean-foundations.html?view=perspectives&amp;color=library">Explore Methods × targets</a> · <a href="../../lean-foundations.html?view=functor&amp;focus=concept:mcmc">Functor Hypergraph</a> · <a href="../../progress/index.html#mcmc">MCMC Route</a></p><p>Fixed-step ULA/SGLD are approximate samplers: target-invariance bias is separate from mixing. Hit-and-Run is continuous-state MCMC; finite-state Glauber may run in discrete or continuous time.</p></section>
<section class="library-integration-note" id="extended-chapters"><h2>Extended subchapters · auxiliary sources</h2><p>These ASTIS reading paths are attached to the primary chapters below. They are not Chapters 7–16 of the original book and are not automatically formalized.</p><div class="library-chapter-list">{extension_cards(d)}</div></section>
<section class="library-integration-note" id="contributor-contract"><h2>One shared graph, multiple reader views</h2><p>Start at §1.3 and §2.1 for kernels and invariance; add RR §§3–4 for drift/coupling. The SDE branch (§1.4), RKHS branch (§1.5) and CLT/Poisson branch have separate prerequisites. Finite Gibbs updates do not wait for these branches.</p><p><a href="https://github.com/DakeBU/Auto-Sampling-Theory-In-Sleep/blob/{commit}/docs/mcmc-library-protocol.md">Source, reuse, overlap-colour and conceptual-review protocol ↗</a></p><p>All new chapter/extension pages are outlines; there is no new Lean theorem or certified transport in this integration.</p><h3>Required rigorous companion</h3>{refs_html(d,['mcmc-rr'])}</section>'''
    astis_site.write_page(output,BASE+'index.html',astis_site.page(d['title'],BASE+'index.html',body,active='Libraries'))
    for c in d['chapters']:
        rel=BASE+c['path'];url=d['primary']['url']+'#page='+str(c['pdf_page'])
        body=shelves.chapter_body(d['title'],'Primary Chapter '+str(int(c['id'])),c['title'],url,'Search shared kernel/measure, finite-state, calculus, covariance and geometry APIs; source overlap does not certify direct Lean compatibility.',source_label=f"Primary v1 · printed p.{c['printed_page']} / PDF p.{c['pdf_page']}")
        sections=''.join(f'<li id="section-{s["id"].replace(".","-")}"><a href="{d["primary"]["url"]}#page={s["pdf_page"]}">§{s["id"]} · {esc(s["title"])}</a> <small>printed {s["printed_page"]} / PDF {s["pdf_page"]}</small></li>' for s in c['sections'])
        body+=rf'''<section class="library-integration-note"><h2>{esc(c['motivation'])}</h2><div class="math-display">\[{esc(c['formula'])}\]</div><p>{esc(c['boundary'])}</p><p>ASTIS orientation, not a verbatim source theorem or Lean closure.</p><h2>Primary source anchors</h2><ol>{sections}</ol><h2>Attached extended material</h2><div class="library-chapter-list">{extension_cards(d,c['id']) or '<p>Use the related Chapters 4–5 extensions through the index.</p>'}</div><p><a href="index.html">All chapters and extensions</a> · <a href="../../lean-foundations.html?view=perspectives&amp;color=library">Method and target intersections</a></p></section>'''
        astis_site.write_page(output,rel,astis_site.page(c['title'],rel,body,active='Libraries'))
    for e in d['extensions']:
        rel=BASE+e['path'];steps=''.join('<li>'+esc(s)+'</li>' for s in e['proof_route'])
        body=shelves.chapter_body(d['title'],'Extended '+e['id']+' · attached to Chapter '+str(int(e['parent_chapter'])),e['title'],d['sources'][e['source_ids'][0]]['url'],'Use one canonical shared node where types match. Formal/source audit is still required.')
        body+=rf'''<section class="library-integration-note"><p><strong>{esc(e['attribution'])}</strong></p><h2>Why this extension?</h2><p>{esc(e['motivation'])}</p><p>{esc(e['primary_connection'])}</p><div class="math-display">\[{esc(e['formula'])}\]</div><h2>Proposed proof / reuse route</h2><ol>{steps}</ol><h2>Truth boundary</h2><p>{esc(e['truth_boundary'])}</p><p>Planned consumers: {esc(', '.join(e['consumers']))}. Planned sharing is not a compiled dependency or a priority claim.</p><h2>Sources and exact scope</h2>{refs_html(d,e['source_ids'])}<p><a href="chapter-{e['parent_chapter']}.html">← Primary chapter</a> · <a href="index.html#extended-chapters">All extended subchapters</a></p></section>'''
        astis_site.write_page(output,rel,astis_site.page(e['title'],rel,body,active='Libraries'))


def route_panel(grouped,panel):
    return panel(route_id='mcmc',anchor='mcmc',title='Markov Chain Monte Carlo Route',eyebrow='Fearnhead · Nemeth · Oates · Sherlock',status='scaffold',source_label='Open library',source_url='../libraries/mcmc/index.html',lede='General-state kernel construction, scalable MCMC and estimation. Shared with continuous and discrete sampling without identifying a method family with a target class.',items=[('planned','Kernel → invariance → convergence','§§1.3,2.1 and Roberts–Rosenthal §§2–4; no SDE/RKHS bottleneck for finite MH or Gibbs.'),('planned','Diffusions / geometry / estimation branch separately','ULA and MALA reuse shared analysis with exact clock/bias adapters; HMC and PDMP need augmented-state contracts.'),('scaffold','Six primary chapters and ten extensions','Every extension has a parent chapter and its own pinned source. No theorem-completion credit.'),('candidate','Conceptual bridges with independent review','Metropolis correction, weak limits, lifting, perturbation and block conditionals. Candidate labels never certify formal transport.')],cells=grouped['mcmc'],actions='<p><a class="button" href="../lean-foundations.html?view=perspectives&amp;color=library">Methods × targets</a></p>')


def add_to_graph(b):
    d=validate_data();b.add('library:mcmc','library',d['title'],status='planned',subtitle='peer method-family source library · scaffold',url=BASE+'index.html');b.edge('library:samplinglib','library:mcmc','formalization route')
    for c in d['chapters']:
        nid='library-chapter:mcmc:'+c['id'];b.add(nid,'library-chapter',c['id']+'. '+c['title'],status='planned',subtitle='source scaffold · not a Lean closure',url=BASE+c['path'],source_url=d['primary']['url']+'#page='+str(c['pdf_page']));b.edge('library:mcmc',nid,'chapter scaffold')
    for e in d['extensions']:
        nid='library-extension:mcmc:'+e['id'];b.add(nid,'library-extension',e['id']+'. '+e['title'],status='planned',subtitle='ASTIS extended subchapter · source-backed outline',url=BASE+e['path'],summary=e['truth_boundary'],source_url=d['sources'][e['source_ids'][0]]['url']);b.edge('library-chapter:mcmc:'+e['parent_chapter'],nid,'extended reading; not a proof dependency')


def validate_site(output):
    import library_shelves
    d=validate_data(); canonical=set(library_shelves.canonical_theme_styles(output))
    for rel in [BASE+'index.html',*[BASE+c['path'] for c in d['chapters']],*[BASE+e['path'] for e in d['extensions']]]:
        text=(output/rel).read_text(encoding='utf-8')
        if not canonical<=set(library_shelves.stylesheet_names(text)):raise ValueError('MCMC theme drift: '+rel)
        if 'Markov Chain Monte Carlo Route' not in text:raise ValueError('MCMC route missing: '+rel)
    if 'math/0404033v4' not in (output/BASE/'index.html').read_text():raise ValueError('Required RR citation missing')
