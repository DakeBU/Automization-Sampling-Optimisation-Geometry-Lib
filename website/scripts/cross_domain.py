"""Shared source/route/semantic-transport metadata; no mathematical status upgrades.

The hypergraph is an incidence overlay, not the compiler's proof dependency DAG.
All renderers use Samplinglib's existing page factory, CSS and MathJax stack.
"""
from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
OT_PATH = ROOT / 'Libraries/StatisticalOptimalTransport/source-map.json'
PLAN_PATH = ROOT / 'Libraries/cross-domain-program.json'
MIRROR_POLICY_PATH = ROOT / 'Libraries/conceptual-mirror-protocol.json'
FUNCTOR_PATH = ROOT / 'website/content/functor_hypergraph.json'
GRAPH_MEMORY_PATH = ROOT / 'website/content/graph_memory_index.json'
OT_BASE = 'libraries/statistical-optimal-transport/'
RESEARCH_PAGE = 'progress/higher-order-sampling-detail.html'

# These are bridge-local search locations that do not belong to a reusable
# conceptual family. Family-wide search locations and stabilized compiled
# examples live only in graph_memory_index.json so Codex and the renderer read
# the same memory source.
EDGE_SPECIFIC_SUBSTRATES = {
    'transport:duality': [
        'AutoSamplingTheory.TechnicalLemmas.Analysis.ConvexSubgradient',
    ],
    'transport:wasserstein-flow': [
        'AutoSamplingTheory.TechnicalLemmas.Measure.DisplacementInterpolationCoupling',
    ],
    'transport:high-order': [
        'AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.Taylor',
        'AutoSamplingTheory.TechnicalLemmas.Taylor',
    ],
    'transport:statistical-loss': [
        'AutoSamplingTheory.TechnicalLemmas.Measure.CouplingQuadraticIntegrability',
    ],
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def candidate_substrate_ids(
    edge: dict[str, Any],
    memory: dict[str, Any],
    present_node_ids: set[str],
) -> list[str]:
    """Resolve dashed Lean search substrates from one canonical family memory.

    `formal_search_nodes` are family-wide search regions. A
    `compiled_substrate_binding` is narrower: its node is attached only to the
    explicitly listed bridge ids. Neither kind of link is a transport theorem or
    a compiler dependency; the returned ids are rendered as dashed evidence
    overlays.
    """
    family_lookup = {row['id']: row for row in memory.get('families', [])}
    names: list[str] = []
    for family_id in edge.get('family_ids', []):
        family = family_lookup.get(family_id, {})
        names.extend(family.get('formal_search_nodes', []))
        for binding in family.get('compiled_substrate_bindings', []):
            if edge.get('id') in binding.get('edges', []):
                names.append(str(binding.get('node', '')))
    names.extend(EDGE_SPECIFIC_SUBSTRATES.get(str(edge.get('id', '')), []))

    result: list[str] = []
    seen: set[str] = set()
    for name in names:
        if not name:
            continue
        node_id = name if name.startswith('module:') else 'module:' + name
        if node_id in present_node_ids and node_id not in seen:
            seen.add(node_id)
            result.append(node_id)
    return result


def validate_data(ot=None, plan=None, model=None, memory=None, mirror_policy=None) -> None:
    ot = load(OT_PATH) if ot is None else ot
    plan = load(PLAN_PATH) if plan is None else plan
    model = load(FUNCTOR_PATH) if model is None else model
    memory = load(GRAPH_MEMORY_PATH) if memory is None else memory
    mirror_policy = load(MIRROR_POLICY_PATH) if mirror_policy is None else mirror_policy
    require(isinstance(ot.get('sha256'), str) and len(ot['sha256']) == 64 and all(c in '0123456789abcdef' for c in ot['sha256']), 'OT source must be byte-pinned')
    rows = ot['chapters']
    require([r['id'] for r in rows] == ['01', '02', '03', '04', '05', '06', '07', '08', 'A', 'B'], 'OT contents drift')
    require(len(ot['authors']) == 3 and ot['pdf_pages'] == 290, 'Cross-domain contract invariant failed')
    for row in rows:
        require(row['status'] == 'scaffold', 'A source scaffold cannot assert Lean completion')
        for entry in [row, *row['sections']]:
            require(entry['pdf_page'] == entry['printed_page'] + 6, 'Cross-domain contract invariant failed')
            require(1 <= entry['pdf_page'] <= ot['pdf_pages'], 'Cross-domain contract invariant failed')
    stages = plan['stages']
    seen = set()
    for row in stages:
        require(row['id'] not in seen, 'Duplicate shared-stage identity')
        require(set(row['parents']) <= seen, 'Shared plan must be dependency ordered and acyclic')
        seen.add(row['id'])
    require('lower' not in next(s for s in stages if s['id'] == 'upper')['parents'], 'Cross-domain contract invariant failed')
    require('upper' not in next(s for s in stages if s['id'] == 'lower')['parents'], 'Cross-domain contract invariant failed')

    require(mirror_policy.get('policy_id') == 'ASTIS-CONCEPTUAL-MIRROR-v1', 'Conceptual mirror policy drift')
    require(mirror_policy.get('mandatory_sau_audit', {}).get('applies_from_advance_schema') == 3, 'Conceptual mirror SAU gate drift')
    require(set(mirror_policy.get('graph_view_contracts', {})) == {'overview', 'lean', 'functor'}, 'Graph view truth contracts drift')
    family_rows = memory.get('families', [])
    family_ids = {row['id'] for row in family_rows}
    require(len(family_ids) == len(family_rows) and family_ids, 'Graph memory family identities must be unique and nonempty')
    require(all(fid.startswith('family:') for fid in family_ids), 'Graph memory family ids must be stable family:<slug> identities')
    seed_ids = {row['id'] for row in mirror_policy.get('seed_families', [])}
    require(seed_ids <= family_ids, 'Every seed conceptual family must exist in graph memory')
    require(set(memory.get('views', {})) == {'overview', 'lean', 'functor'}, 'Graph memory must document exactly the three main graph truth views')

    ids = {o['id'] for o in model['objects']}
    require(len(ids) == len(model['objects']) and len(ids) >= 7, 'Unique peer conceptual domains required')
    require('concept:discrete-sampling' in ids, 'Discrete Sampling conceptual domain missing')
    require(model['center'] in ids, 'Cross-domain contract invariant failed')
    edge_ids = set()
    for edge in model['hyperedges']:
        require(edge['id'] not in ids | edge_ids, 'Cross-domain contract invariant failed')
        edge_ids.add(edge['id'])
        require(edge['tails'] and edge['heads'], 'Cross-domain contract invariant failed')
        require(set(edge['tails'] + edge['heads']) <= ids, 'Cross-domain contract invariant failed')
        require(len(set(edge['tails'])) == len(edge['tails']), 'Cross-domain contract invariant failed')
        require(len(set(edge['heads'])) == len(edge['heads']), 'Cross-domain contract invariant failed')
        require(set(edge['shared_stages']) <= seen, 'Cross-domain contract invariant failed')
        require(edge['source_ids'] and set(edge['source_ids']) <= set(model['sources']), 'Cross-domain contract invariant failed')
        require(isinstance(edge.get('family_ids'), list) and set(edge['family_ids']) <= family_ids, 'Functor edge has an unknown conceptual family')
        for slot in ('mechanism', 'hypothesis_map', 'conclusion_map', 'failure_boundary', 'relation_kind'):
            require(edge[slot].strip(), f'Missing transport slot: {slot}')
        require(set(edge['category_contract']) == {'objects', 'morphisms', 'identity', 'composition'}, 'Cross-domain contract invariant failed')
        # This schema has no certificate verifier yet. Fail closed, rather than
        # accepting a status string as evidence of a Lean-certified functor.
        require(edge['status'] == 'not-Lean-certified', 'Certification needs a real independent certificate gate')
        require(edge['formal_refs'] == [], 'Do not fabricate formal transport witnesses')
        if edge['id'].startswith('transport:mcmc-'):
            review=edge.get('review',{})
            require(review.get('status') in {'candidate','independently-reviewed'}, 'MCMC mirror review status required')
            require(bool(review.get('proposed_by')), 'MCMC mirror proposer required')
            if review['status']=='independently-reviewed':
                require(bool(review.get('independent_reviewer')) and review['independent_reviewer']!=review['proposed_by'], 'MCMC mirror cannot self-validate')
                require(isinstance(review.get('evidence'),list) and bool(review['evidence']), 'MCMC source review evidence required')
    for family in family_rows:
        require(set(family.get('domains', [])) <= ids, f"Graph memory family {family['id']} has an unknown domain")
        require(set(family.get('functor_edges', [])) <= edge_ids, f"Graph memory family {family['id']} has an unknown Functor edge")
        search_nodes = family.get('formal_search_nodes')
        require(isinstance(search_nodes, list) and search_nodes, f"Graph memory family {family['id']} needs formal search nodes")
        require(len(search_nodes) == len(set(search_nodes)), f"Graph memory family {family['id']} repeats a formal search node")
        require(all(isinstance(name, str) and name.startswith('AutoSamplingTheory.') for name in search_nodes), f"Graph memory family {family['id']} has a malformed formal search node")
        bindings = family.get('compiled_substrate_bindings', [])
        require(isinstance(bindings, list), f"Graph memory family {family['id']} compiled bindings must be a list")
        binding_nodes: set[str] = set()
        for binding in bindings:
            require(isinstance(binding, dict), f"Graph memory family {family['id']} has a malformed compiled binding")
            node = binding.get('node')
            require(isinstance(node, str) and node.startswith('AutoSamplingTheory.'), f"Graph memory family {family['id']} compiled binding has a malformed node")
            require(node not in binding_nodes, f"Graph memory family {family['id']} repeats a compiled binding node")
            binding_nodes.add(node)
            binding_edges = binding.get('edges')
            require(isinstance(binding_edges, list) and binding_edges and set(binding_edges) <= set(family.get('functor_edges', [])), f"Graph memory family {family['id']} compiled binding targets an unrelated bridge")
            require(isinstance(binding.get('role'), str) and binding['role'].strip(), f"Graph memory family {family['id']} compiled binding lacks role")
            require(isinstance(binding.get('truth_boundary'), str) and binding['truth_boundary'].strip(), f"Graph memory family {family['id']} compiled binding lacks truth boundary")
        for slot in ('plain_language', 'reading_order', 'do_not_conflate'):
            require(family.get(slot), f"Graph memory family {family['id']} lacks {slot}")
    import discrete_sampling
    discrete_sampling.validate_data(model=model)


def write_ot_pages(output: Path, shelves) -> None:
    import astis_site
    ot = load(OT_PATH)
    validate_data()
    body = shelves.index_body(
        eyebrow='Statistical Optimal Transport Library', title=ot['title'],
        lede='Sinho Chewi · Jonathan Niles-Weed · Philippe Rigollet. Eight chapters and two appendices in the shared Samplinglib reader.',
        source=ot['source_url'], chapters=(),
        contract='Search Samplinglib, Mathlib and compatible formal upstreams first. Recover omitted details from Villani, Santambrogio and Ambrosio–Gigli–Savaré without silently changing the source theorem.')
    cards = []
    for row in ot['chapters']:
        cards.append(f'''<article class="library-chapter-card"><div class="library-chapter-number">{row['id']}</div><div><div class="card-meta">{shelves.badge('scaffold')}</div><h2><a href="{row['path']}">{escape(row['title'])}</a></h2><p>Printed p. {row['printed_page']} · PDF p. {row['pdf_page']} · source map and reuse audit; not a Lean closure.</p></div></article>''')
    body = body.replace('<div class="library-chapter-list"></div>', '<div class="library-chapter-list">' + ''.join(cards) + '</div>')
    body += '''<section class="library-integration-note"><h2>Dependency-first, not cover-to-cover.</h2><p>Chapter 1 unlocks Chapters 2, 3, 4, 5 and 7; then 5 → 6 and 7 → 8. The book separates prerequisites from cross-references in Figure 0.1. Appendices A/B are shared-entry material, not a second convex/probability library.</p><p><a href="../../progress/index.html#optimal-transport">Statistical Optimal Transport Route</a> · <a href="../../lean-foundations.html?view=functor&amp;focus=concept:transport">Functor Hypergraph</a></p><p>Pagination audited on 5 September 2026. The public PDF is mutable; every claimed theorem must pin its edition and exact statement independently.</p></section>'''
    astis_site.write_page(output, OT_BASE + 'index.html', astis_site.page(ot['title'], OT_BASE + 'index.html', body, active='Libraries'))
    for row in ot['chapters']:
        rel = OT_BASE + row['path']
        label = f"Chapter {int(row['id'])}" if row['id'].isdigit() else f"Appendix {row['id']}"
        source = f"{ot['source_url']}#page={row['pdf_page']}"
        body = shelves.chapter_body(ot['title'], label, row['title'], source,
            'Reuse the canonical convex, coupling, entropy and calculus interfaces. Local source availability is not yet a compatible Lean theorem.',
            source_label=f"Source: printed p. {row['printed_page']} / PDF p. {row['pdf_page']}")
        section_links = ''.join(f'''<li id="section-{s['id'].replace('.', '-')}"><a href="{ot['source_url']}#page={s['pdf_page']}">§{s['id']} · {escape(s['title'])}</a> <small>printed p. {s['printed_page']} / PDF p. {s['pdf_page']}</small></li>''' for s in row['sections'])
        body += rf'''<section class="library-integration-note"><h2>Mathematical orientation</h2><div class="math-display">\[{escape(row['formula'])}\]</div><p>{escape(row['guide'])}</p><p>This is ASTIS orientation, not a verbatim source theorem or a completed formalization. Each theorem needs its own assumptions and source-to-Lean audit.</p><h2>Section source map</h2><ol>{section_links}</ol><p><a href="index.html">← Book contents</a> · <a href="../../progress/index.html#optimal-transport">Shared route</a> · <a href="../../lean-foundations.html?view=functor&amp;focus=concept:transport">Conceptual transports</a></p></section>'''
        astis_site.write_page(output, rel, astis_site.page(f"Statistical Optimal Transport {label}: {row['title']}", rel, body, active='Libraries'))


def shared_plan_html() -> str:
    plan = load(PLAN_PATH)
    cards = ''.join(f'''<article id="shared-{s['id']}"><span>{escape(s['status'])}</span><h3>{escape(s['title'])}</h3><p><strong>Parents:</strong> {escape(', '.join(s['parents']) or 'none — start here')}</p><p>{escape(s['target'])}</p><p><strong>Reuse search:</strong> {escape(s['search'])}</p><small>Consumers: {escape(', '.join(s['consumers']))}</small></article>''' for s in plan['stages'])
    return f'''<section class="progress-intersections" id="shared-order" data-shared-partial-order="true"><div class="section-heading"><span>All routes · shared prerequisite partial order</span><h2>Share mathematical cores; keep transports explicit.</h2></div><p>{escape(plan['priority_rule'])}</p><p>Convexity, measure theory and calculus start in parallel after contract alignment. Their consumers branch, rather than waiting for every textbook chapter. These are planned reuse audits, not compiler-certified dependency edges.</p><div class="progress-overlap-grid">{cards}</div><p><a href="../lean-foundations.html?view=functor">Explore the Functor Hypergraph</a> · <a href="higher-order-sampling-detail.html">Higher-order sampling research contract</a></p></section>'''


def extra_route_panels(grouped, panel) -> str:
    ot = panel(route_id='statistical-optimal-transport', anchor='optimal-transport', title='Statistical Optimal Transport Route', eyebrow='Chewi · Niles-Weed · Rigollet', status='scaffold', source_label='Open library', source_url='../libraries/statistical-optimal-transport/index.html', lede='Eight chapters and two appendices share the same reader, source-fidelity protocol and canonical Lean floor as the existing libraries.', items=[
        ('scaffold', 'Source map and shared entry points', '8 chapters + A/B; exact page anchors. Audit convexity, probability and existing coupling code before introducing anything new.'),
        ('planned', 'Chapter 1: transport foundation', 'Couplings, Wasserstein distance, Brenier and duality. Reuse shared convex/marginal/compactness ingredients.'),
        ('planned', 'Parallel branches after Chapter 1', '2–3 statistical estimation; 4 entropic transport; 5→6 flows and sampling; 7→8 metric geometry and barycenters.'),
        ('planned', 'Source omissions and transport review', 'Use Villani / Santambrogio / AGS for missing analytic details. Separate conceptual correspondence from certified Lean reuse.')], cells=grouped['statistical-optimal-transport'], actions='<p><a class="button" href="#shared-order">Shared prerequisite order</a></p>')
    high = panel(route_id='higher-order-sampling', anchor='higher-order-sampling', title='Higher-Order Smoothness × Sampling', eyebrow='Optimisation × Sampling research route', status='research plan', source_label='Research contract and literature', source_url='higher-order-sampling-detail.html', lede='Determine when additional potential smoothness yields a real sampling advantage at a fixed oracle and total computational cost. Existing high-order sampling literature is the starting point, not a novelty claim.', items=[
        ('planned', 'Regime and oracle matrix', 'Separate potential smoothness p, derivative access q, dynamical order k and discretization order r; fix metric, starts and dimension-dependent constants.'),
        ('planned', 'Shared Taylor and stochastic local error', 'Search existing Taylor, moment and coupling APIs; prove one useful local-error/invariant-target interface before a full rate.'),
        ('planned', 'Mixing plus discretization', 'Couple an audited local error with a compatible contraction theorem; count derivative evaluations and matrix/tensor work, not iterations alone.'),
        ('parallel', 'Lower bounds remain an independent lane', 'SampleWiki studies hard instances and information transcripts. Compare the two lanes only after oracle, class, metric and costs match.')], cells=grouped['higher-order-sampling'], actions='<p><a class="button" href="higher-order-sampling-detail.html">Read research targets</a></p>')
    return ot + high


def write_research_page(output: Path) -> None:
    import astis_site
    model = load(FUNCTOR_PATH)
    sources = ''.join(f'<li><a href="{escape(model["sources"][key]["url"])}">{escape(model["sources"][key]["title"])}</a>: {escape(model["sources"][key]["anchor"])}</li>' for key in ['mou','midpoint','dang','prox','mfld','lower'])
    body = r'''
<section class="page-hero compact progress-hero"><div class="eyebrow">Research route · Optimisation × Sampling</div><h1>What does higher-order smoothness buy for sampling?</h1><p class="lede">A contract-driven research program, not a claim that this literature is empty and not a completed Lean theorem.</p><p><a href="index.html#higher-order-sampling">← Current Progress</a> · <a href="../lean-foundations.html?view=functor&amp;focus=transport:high-order">Inspect the conceptual bridge</a></p></section>
<section class="library-integration-note"><h2>Four orders, four different questions.</h2><p>Let V be a potential on Euclidean space, with target π proportional to exp(−V). A first controlled class has αI ≼ ∇²V ≼ βI and a Lipschitz p-th derivative, measured in operator norm. Here α &gt; 0 is the strong-convexity constant and β bounds the Hessian.</p><div class="math-display">\[\|D^p V(x)-D^p V(y)\|_{\mathrm{op}}\leq L_p\|x-y\|.\]</div><div class="library-contract-grid"><article><h3>p · Potential smoothness</h3><p>The available regularity and constants Lp. A smaller local remainder need not change the diffusion's mixing geometry.</p></article><article><h3>q · Oracle information</h3><p>The highest derivative the algorithm may query: gradients, Hessians or higher tensors. Extra regularity does not grant extra oracle access.</p></article><article><h3>k · Dynamical order</h3><p>The chosen extended-state Langevin system. Auxiliary variables are not derivative queries; preserve the intended positional marginal.</p></article><article><h3>r · Approximation accuracy</h3><p>The local error exponent and its metric; weak error, strong error and invariant-measure bias are different contracts.</p></article></div></section>
<section class="library-integration-note"><h2>What is already known—and what we will audit.</h2><p>Mou et al. analyze a high-order Langevin construction, including smoothness-dependent regimes. Shen–Lee improve discretization with randomized midpoint under strong convexity and Lipschitz gradients. Dang et al. study higher-order Langevin dynamics. These are different mechanisms; source-by-source theorem audits must precede any rate table or claim of novelty.</p><p>Our first question holds the oracle fixed and changes regularity. The second allows richer oracles and charges their full cost. The third keeps regularity fixed and changes the stochastic integrator. Only then should we explore weaker curvature, manifolds or non-log-concave targets.</p></section>
<section class="library-integration-note"><h2>First reusable target: local error → global sampling error.</h2><p>Let P_h be an exact Markov evolution with invariant π and W₂ contraction factor a = exp(−αh), where h &gt; 0 and α &gt; 0. Let K_h be the numerical kernel and μ_j = μ_0 K_h^j. Suppose all laws have finite second moments and, along this orbit, W₂(μ_j K_h, μ_j P_h) ≤ C h^(r+1), with a uniform C. The triangle inequality gives the following proposed reusable interface:</p><div class="math-display">\[e_{j+1}\leq a e_j+C h^{r+1},\qquad e_N\leq a^N e_0+C h^{r+1}\frac{1-a^N}{1-a},\quad e_j=W_2(\mu_j,\pi).\]</div><p>This elementary implication is a target for reuse/audit, not new research or a Lean closure. The difficult task is proving the local bound with controlled moments and the right invariant target, then determining its dependence on p, q, k, dimension d and the requested error ε. Moment-dependent local constants must be bounded along the whole numerical orbit.</p><p>The exact-flow contract and the numerical-analysis contract remain separate. Do not infer a usable r directly from p. Charge N oracle calls multiplied by per-step derivative, tensor, linear-algebra and auxiliary-variable costs; parallel rounds are a separate budget.</p></section>
<section class="library-integration-note"><h2>Upper and lower bounds: complementary, not one forced proof route.</h2><p><strong>Upper-bound lane:</strong> Taylor remainders → stochastic integration/moments → stable kernel and invariant target → contraction/mixing → cost-aware accuracy.</p><p><strong>SampleWiki lower-bound lane:</strong> admissible hard distributions → oracle transcripts → indistinguishability or testing → reduction and query lower bound. Its proof need not use the high-order integrator.</p><p>Compare only matched contracts: potential class and regularity constants; q-th derivative versus stochastic oracle; warm/cold starts; KL/TV/W₂ normalization; adaptive randomized access; success probability; total work versus parallel depth. A statistical OT sample size is not automatically a sampling query budget.</p><p>Shared probability, data-processing and discrepancy lemmas may be reused. A hardness transfer between fields requires an explicit simulation and error/cost transformation. No current plan presumes the unknown lower bound matches the upper bound.</p></section>
<section class="library-integration-note"><h2>Acceptance and stopping boundaries</h2><p>A publishable advance must either reuse an exact existing theorem, add a genuinely missing compiled lemma with consumers, prove a cost-aware improvement under a fixed comparison contract, or expose a typed obstruction/counterexample. An alternative proof, new diagram or additional assumption alone is not a new sampling complexity result.</p><p><a href="index.html#shared-order">Dependency-ready shared work queue</a> · <a href="../workflow/index.html">ASTIS Harness and independent verification</a></p><h2>Primary starting sources</h2><ul>''' + sources + '</ul><p>Literature entry points checked 5 September 2026; this is not an exhaustive novelty search.</p></section>'
    astis_site.write_page(output, RESEARCH_PAGE, astis_site.page('Higher-Order Smoothness × Sampling', RESEARCH_PAGE, body, active='Progress'))


def add_to_graph(builder) -> dict[str, Any]:
    import library_shelves
    validate_data()
    model, ot, memory = load(FUNCTOR_PATH), load(OT_PATH), load(GRAPH_MEMORY_PATH)
    for ident, label, url in [('riemannian','Riemannian Optimization','libraries/riemannian-optimization/index.html'),('optimisation','Optimisation','libraries/optimisation/index.html'),('optimal-transport','Statistical Optimal Transport',OT_BASE+'index.html')]:
        progress = library_shelves.publication_reader.publication.chapter_progress(ident)
        builder.add('library:'+ident, 'library', label, status='partial' if progress['status'] == 'partial' else 'planned', subtitle=progress['label']+' · not a source closure', url=url)
        builder.edge('library:samplinglib', 'library:'+ident, 'formalization route')
    for ident, rows in [('riemannian', [(f'{i:02d}', t, f'libraries/riemannian-optimization/chapter-{i:02d}.html') for i,t in enumerate(library_shelves.BOUMAL,1)]), ('optimisation', [(i,t,'libraries/optimisation/'+('appendix-a.html' if i=='A' else f'chapter-{i}.html')) for i,t,_,_ in library_shelves.OPTIMISATION]), ('optimal-transport',[(r['id'],r['title'],OT_BASE+r['path']) for r in ot['chapters']])]:
        for cid,title,url in rows:
            progress = library_shelves.publication_reader.publication.chapter_progress(ident, cid)
            node = builder.add(f'library-chapter:{ident}:{cid}', 'library-chapter', f'{cid}. {title}', status='partial' if progress['status'] == 'partial' else 'planned', subtitle=progress['label']+' · source fidelity separate', url=url)
            builder.edge('library:'+ident,node,'chapter scaffold')
    for a,b in ot['chapter_prerequisites']:
        builder.edge('library-chapter:optimal-transport:'+a,'library-chapter:optimal-transport:'+b,'source prerequisite')
    for a,b in ot['chapter_reference_edges']:
        builder.edge('library-chapter:optimal-transport:'+a,'library-chapter:optimal-transport:'+b,'source cross-reference')
    import discrete_sampling
    discrete_sampling.add_to_graph(builder)
    import mcmc_library
    mcmc_library.add_to_graph(builder)
    for obj in model['objects']:
        builder.add(obj['id'],'concept-domain',obj['label'],status='shared',subtitle=obj['space'],url=obj['url'],details=[{'label':k.title(),'value':obj[k]} for k in ['space','energy','assumptions']])

    # Candidate substrates are resolved from compact family memory plus a very
    # small set of bridge-local search nodes. All such incidence edges stay
    # dashed and never become compiler dependencies or transport certificates.
    for edge in model['hyperedges']:
        details = [{'label':'Evidence boundary','value':'Literature/structural correspondence; no Lean-certified functor or theorem transfer.'}]
        if edge.get('review'):
            review_boundary = ('Independent source review is recorded. Source review does not certify a Lean transport.'
                               if edge['review']['status'] == 'independently-reviewed'
                               else 'A candidate awaits independent source review. Source review does not certify a Lean transport.')
            details += [{'label':'Review status','value':edge['review']['status']}, {'label':'Review boundary','value':review_boundary}]
        if edge.get('family_ids'):
            details += [{'label':'Conceptual families','value':', '.join(edge['family_ids'])}]
        details += [{'label':k.replace('_',' ').title(),'value':edge[k]} for k in ['mechanism','hypothesis_map','conclusion_map','failure_boundary']]
        details += [{'label':'Category '+k,'value':v} for k,v in edge['category_contract'].items()]
        details += [{'label':'Shared planned checkpoints','value':', '.join(edge['shared_stages'])}]
        refs = candidate_substrate_ids(edge, memory, set(builder.nodes))
        builder.add(edge['id'],'concept-bridge',edge['label'],status='proposal',subtitle=edge['relation_kind'],summary=edge['mechanism'],formula=edge['formula'],details=details,url=edge.get('url','progress/index.html#shared-order'),source_url=model['sources'][edge['source_ids'][0]]['url'],hyperedge=edge,sources=[model['sources'][key] for key in edge['source_ids']],candidate_substrates=refs)
        for src in edge['tails']:
            builder.edge(src,edge['id'],'joint conceptual input')
        for dst in edge['heads']:
            builder.edge(edge['id'],dst,'conditional conceptual output')
        for mid in refs:
            builder.edge(mid,edge['id'],'reuse search candidate; not a proof dependency')
    return model


def graph_guide_html() -> str:
    model = load(FUNCTOR_PATH)
    memory = load(GRAPH_MEMORY_PATH)
    view_cards = ''.join(
        f'''<article><b>{escape(view_id.upper())}</b><h3>{escape(view['label'])}</h3><p>{escape(view['question'])}</p><small>{escape(view['status_semantics'])}</small></article>'''
        for view_id, view in memory['views'].items()
    )
    family_cards = []
    for family in memory['families']:
        jumps = ''.join(
            f'<button type="button" data-functor-jump="{escape(edge_id)}">{escape(edge_id.replace("transport:", ""))}</button>'
            for edge_id in family['functor_edges']
        )
        bindings = ''.join(
            f'''<li><code>{escape(binding['node'])}</code><br><small>{escape(binding['role'])} Bound only to {escape(', '.join(binding['edges']))}. {escape(binding['truth_boundary'])}</small></li>'''
            for binding in family.get('compiled_substrate_bindings', [])
        )
        compiled = f'<p><strong>Compiled substrates</strong></p><ul>{bindings}</ul>' if bindings else ''
        family_cards.append(
            f'''<article id="{escape(family['id'].replace(':','-'))}"><b>{escape(family['id'])}</b><h3>{escape(family['label'])}</h3><p>{escape(family['plain_language'])}</p>{compiled}<p><strong>Do not conflate:</strong> {escape(family['do_not_conflate'])}</p><nav class="ulg-functor-links" aria-label="{escape(family['label'])}">{jumps}</nav></article>'''
        )
    links = ''.join(f'<button type="button" data-functor-jump="{escape(e["id"])}">{escape(e["label"])}</button>' for e in model['hyperedges'])
    return r'''<section class="ulg-semantics" id="graph-truth-contract"><div class="section-heading"><span>One data model · three truth views</span><h2>Overview, Lean Branches, and Functor Hypergraph answer different questions.</h2></div><p>Agents should read stable family and bridge ids before expanding the full declaration graph. Readers can use the same order: orient by source/project topology, understand the recurring mathematical mechanism, then inspect the exact compiled Lean substrate. A conceptual bridge never upgrades the Lean view.</p><div>''' + view_cards + r'''</div></section>
<section class="ulg-semantics" id="functor-contract"><div class="section-heading"><span>Functor Hypergraph · conceptual layer</span><h2>Transport the idea, not just the lemma.</h2></div><p>Optimization is the organizing center, not a claim that every other field is merely optimization on another space. In particular, lower bounds add an information/oracle model. Domain cards are coarse presentations; bridge cards record the actual mathematical mechanism.</p><p>Each hyperedge has a joint input set, output set, hypothesis and conclusion maps, source evidence, conceptual-family ids and a failure boundary. All inputs are read together (AND); pairwise lines do not each assert an implication. Cycles in this conceptual atlas are not cyclic Lean proofs.</p><div class="math-display">\[e:(P_1,\ldots,P_m;H_e)\rightsquigarrow(Q_1,\ldots,Q_n),\qquad F(\mathrm{id})=\mathrm{id},\quad F(g\circ f)=F(g)\circ F(f).\]</div><p>The first notation describes a conditional transport record. The latter two equations are obligations for an actual functor, not laws established by this diagram. Shared-energy spans, PL/LSI mirrors, curvature patterns, conditional reductions and functor candidates have different types. None of the current bridges is Lean-certified.</p><p>A safe graph compression must preserve source/assumption provenance, primitive dependencies and an expandable certificate. Conceptual similarity alone never merges Lean declarations. The inspector exposes object/morphism assignments, identity/composition gaps and candidate Lean substrates separately.</p><div class="section-heading"><span>Conceptual memory families</span><h2>Read the mother mechanism first; expand bridges second.</h2></div><div>''' + ''.join(family_cards) + r'''</div><div class="section-heading"><span>All typed bridges</span><h2>Direct bridge inspector</h2></div><nav class="ulg-functor-links" aria-label="Conceptual bridge inspector">''' + links + '''</nav><p><a href="progress/index.html#shared-order">Shared prerequisite order</a> · <a href="progress/higher-order-sampling-detail.html">Higher-order smoothness research route</a></p></section>'''


def validate_site(output: Path) -> None:
    validate_data()
    import library_shelves
    import discrete_sampling
    discrete_sampling.validate_site(output)
    import mcmc_library
    mcmc_library.validate_site(output)
    ot = load(OT_PATH)
    memory = load(GRAPH_MEMORY_PATH)
    canonical = set(library_shelves.canonical_theme_styles(output))
    for rel in [OT_BASE+'index.html', *[OT_BASE+r['path'] for r in ot['chapters']], RESEARCH_PAGE]:
        path = output/rel
        require(path.exists(), f'Missing peer page {rel}')
        text = path.read_text(encoding='utf-8')
        require(canonical <= set(library_shelves.stylesheet_names(text)), f'Theme mismatch {rel}')
        require('Statistical Optimal Transport' in text and 'Higher-Order Smoothness' in text, f'Navigation mismatch {rel}')
    graph = load(output/'data/underlying-lean-graph.json')
    require(len(graph['hyperedges']) == len(load(FUNCTOR_PATH)['hyperedges']), 'Cross-domain contract invariant failed')
    require(graph['counts']['conceptual_domains'] == len(load(FUNCTOR_PATH)['objects']), 'Conceptual domain count drift')
    lookup = {n['id']: n for n in graph['nodes']}
    present = set(lookup)
    for edge in graph['hyperedges']:
        node = lookup[edge['id']]
        require(node['kind'] == 'concept-bridge' and node['hyperedge'] == edge, 'Cross-domain contract invariant failed')
        for tail in edge['tails']:
            require(any(e['source']==tail and e['target']==edge['id'] and e['relation']=='joint conceptual input' for e in graph['edges']), 'Cross-domain contract invariant failed')
        for head in edge['heads']:
            require(any(e['target']==head and e['source']==edge['id'] and e['relation']=='conditional conceptual output' for e in graph['edges']), 'Cross-domain contract invariant failed')
        expected_refs = candidate_substrate_ids(edge, memory, present)
        require(set(node.get('candidate_substrates', [])) == set(expected_refs), f"Functor substrate drift: {edge['id']}")
        for mid in expected_refs:
            require(any(e['source']==mid and e['target']==edge['id'] and e['relation']=='reuse search candidate; not a proof dependency' for e in graph['edges']), f"Functor substrate edge missing: {mid} -> {edge['id']}")
    for family in memory['families']:
        for binding in family.get('compiled_substrate_bindings', []):
            mid = 'module:' + binding['node']
            require(mid in lookup, f"Compiled family substrate missing from Lean graph: {binding['node']}")
            for edge_id in binding['edges']:
                require(mid in lookup[edge_id].get('candidate_substrates', []), f"Compiled family substrate is not attached to {edge_id}: {binding['node']}")
    page = (output/'lean-foundations.html').read_text(encoding='utf-8')
    require('data-view="functor"' in page and 'id="functor-contract"' in page, 'Cross-domain contract invariant failed')
    require('id="graph-truth-contract"' in page, 'Three-view graph truth contract missing')
    for family in memory['families']:
        require(family['label'] in page, f"Conceptual family missing from reader guide: {family['id']}")
        for binding in family.get('compiled_substrate_bindings', []):
            require(binding['node'] in page, f"Compiled family substrate missing from reader guide: {binding['node']}")
