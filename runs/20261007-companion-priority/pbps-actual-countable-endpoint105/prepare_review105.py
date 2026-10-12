from pathlib import Path
import copy, hashlib, json, sys

root = Path.cwd()
r = Path(__file__).resolve().parent.relative_to(root.resolve())
pre = r.parent / 'pbps-countable-endpoint-preread105'
sys.path.insert(0, str(root / 'tools'))
import astis_semantic_roundtrip as rt
import astis_publication as pub

load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
def save(p, value):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
def fresh(p, value):
    assert not p.exists(), p
    save(p, value)
def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.as_posix(), raw_sha256=sha(b), bytes=len(b))

claim = load(r / 'claim.json')
decl, file, cid = claim['target_declarations'][0], claim['proposed_files'][0], claim['frontier_cell']
module = Path(file)
s, raw = module.read_text(encoding='utf8'), module.read_bytes()
receipt = r / 'focused105/production1/receipt.json'
check = load(receipt)
assert check['exit_code'] == 0 and check['input_raw_sha256'] == sha(raw)
literal = s.split('private def actual_countable_endpoint_statement', 1)[1].split('set_option maxHeartbeats', 1)[0].strip()
seal = load(pre / 'root.statement-seal105.json')
assert literal == seal['expanded_literal_Prop'].strip()
binders, body = literal.split(' : Prop :=', 1)
body = body.removeprefix(' by\n  classical\n  exact\n')
statement_lean = binders + ' :\n' + body
old = load(r.parent / 'pbps-actual-finite-count-path93/authored-statement93.json')['statement']
restatement = old.split('For every n≥0 and finite T≥0, Ψ_n')[0].replace('Fix any deterministic y,r∈E and initial phase z₀∈E×E.', 'The following literal constructions are made for all y,r∈E and initial phases z₀∈E×E; the existential process witness below is global in these parameters.').replace('\\n', '\n') + """
Put R(x,p)=(x,-p), V_y(x)=V(x)+||x-y||^2/(2 eta), and nu_y=(volume_E.tilted(-V_y)) times stdGaussian(E), in position/momentum order. Here tilted(-V_y) has density ofReal(exp(-V_y(x))/integral exp(-V_y) dx), and stdGaussian is the centered identity-covariance Gaussian. Normalizability is a consequence, not a premise.
For the same single actual Z described above, every y,r in E and every finite T>=0, define for each n in Nat the map B_n(z,t)=(z,Gamma_(y,r,z,n,T,t)(T)), the measure sigma_n=(nu_y times m_n,T).withDensity((z,t)->rho_(y,r,z,n,T)(t)), and L_n=map B_n sigma_n on (E times E) times (E times E). Define M_Z(z,w)=(z,Z(y,r,z,T,w)), Q=map M_Z (nu_y times P), and J(z0,zT)=(R(zT),R(z0)). Every product uses initial phase first, and Q is the actual endpoint-pair law of the specified clock process.
Then simultaneously Q=Measure.sum(n in Nat -> L_n), Q is a probability measure, and J is measurable with map J Q=Q. The sum includes every nonnegative integer without a cap. There is no assumption that a fixed-count sector has mass one. Joint measurability, simplex sigma-finiteness, measurable initial-phase sector integrals, countable exchange, and probability of the input measures are internal dependencies, not supplied hypotheses. In particular no joint-in-initial-state measurability of N is assumed: the count partition is taken at each fixed initial state before nonnegative integration against nu_y.
The conclusion includes n=0 in the sum, T=0, dimension zero, zero rates and infinite waits with the explicit raw exceptional fallback above. At T=0 the actual initialization is almost sure; no pointwise all-clock initialization or jumpwise reversed-path equality is added. Arbitrary nonnegative measurable test functions may have infinite integrals during assembly. Signed bilinear duality, marginal phase invariance, restart/Markovness, hypocoercivity, implementation error, unbounded expected oracle cost and complete paper/composition results remain separate obligations.
"""
attribution = 'Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1, Appendix A.1 A7 and Gibbs averaging before A8, with Eq3.1 normalization. Complete attributed mathematical restatement of the selected measure-assembly step. Joint measurable representatives and explicit measure identities are ASTIS completion; this is not a verbatim standalone theorem quotation.'
context = ['Finite-dimensional real inner-product Borel space with canonical volume, including rank zero; genuine second Frechet derivative and real Hilbert gradient.', 'Fin n is zero-based; Fin.cons prepends; Fin.induction constructs a finite sequence; Fin.foldl visits ascending indices. Sum.inl represents a live time/state record; Unit represents a stopped record.', 'Real division by zero is zero; Real.toNNReal is positive part; nonnegative subtraction is truncated. ENNReal.ofReal embeds the positive part in extended nonnegative reals. Interval integrals use real Lebesgue measure.', 'Measure.tilted mu h is mu.withDensity(x -> ofReal(exp(h(x))/integral exp(h) dmu)). stdGaussian E is the centered identity-covariance Gaussian. Measure.comap along a measurable subtype inclusion is the induced subtype measure. Products use the displayed coordinate order.', 'MeasurePreserving f mu nu states Measurable f and Measure.map f mu = nu. withDensity multiplies the base measure by the given extended-nonnegative density. Measure.sum is the countable sum of the displayed measures. IsProbabilityMeasure means total mass one. All literal let bindings are definitions, not hypotheses.', 'hittingAfter f D 0 a is the infimum of nonnegative times t at which f t a lies in D, in WithTop nonnegative reals; the empty infimum is top. untopD 0 returns the finite value when not top and zero otherwise.', 'Measure.infinitePi constructs the displayed countable product law; expMeasure 1 is the unit-rate exponential probability measure on real numbers. The function space carries the coordinate-product measurable structure. A measurable global process and its almost-everywhere initialization are conclusions.']

aid = 'ASTIS-RT-20261012-PBPSActualCountableEndpointLaw'
slug = 'pbps-actual-countable-endpoint-law'
title = 'Actual normalized PBPS countable endpoint law'
audit = dict(id=aid, state='draft', source=dict(source_id='companion-domain:' + slug, anchor=claim['source_anchor'], url='https://arxiv.org/html/2609.06905v1#A1.E8', original_text=restatement, text_sha256=sha(restatement.encode())), lean=dict(statement=statement_lean.strip(), statement_sha256=sha(statement_lean.strip().encode()), compiled=True, decoder_context=context, declaration=decl, file=file, formalizer='companion_root_20261005', compiler_evidence=receipt.as_posix()), source_review=dict(state='pending'), repairs=[])
ap = Path('research-wiki/semantic-roundtrip/audits') / (aid + '.json')
fresh(ap, audit)
packet = rt.decoder_packet(audit)
out = Path('runs/semantic-roundtrip/anonymous105/input.json')
fresh(out, packet)
fresh(r / 'authored-statement105.json', dict(statement=restatement, attribution=attribution))
cp = Path('research-wiki/frontier-cells') / (cid + '.json')
cell = load(cp)
parents = cell['parents']
fresh(r / 'cell-before-compiled105.json', cell)
cell['evidence']['whole_target_compiled'] = pin(module)
cell['evidence']['focused_checks'] = [receipt.as_posix()]
cell['blocked']['reason'] = 'Full sealed target compiles; independent whole mathematics, blind decoding and source/exposition reviews pending.'
cell['purification']['dead_code_audit'] = 'One public countable endpoint theorem and one literal private proposition; four actual public parents reused, no private dependency calls or duplicate analytic helpers.'
save(cp, cell)

def step(title, text, formula, start, end):
    a, b = s.index(start), s.index(end, s.index(start))
    code = s[a:b]
    return dict(title=title, text=text, formula=formula, lean=code, detail='ASTIS completion of the countable initial-phase averaging step. Exact compiled region; the original six analytic assumptions are unchanged.', lean_source_region=dict(path=file, source_raw_sha256=sha(raw), start_line=s[:a].count('\n') + 1, end_line=s[:b].count('\n'), exact_code_raw_sha256=sha(code.encode())))

steps = [
    step('Select the same actual global process', 'Use the existing actual finite-count path law once. Retain its single jointly measurable Z and its arc, fallback and almost-sure zero-time formulas for the entire theorem. No fresh abstract process replaces it.', r'Z(y,r,z,s,w)=\Phi_{s-a}(b)\quad\text{on each live covering arc }(a,b);\qquad Z(y,r,z,0,w)=z\ \ P\text{-a.e.}', '  obtain ⟨Z', '  have h103'),
    step('Establish the actual endpoint probability', 'The phase normalization theorem identifies the initial product law and proves it is probability. The unit-exponential product theorem supplies probability, hence sigma-finiteness, of P. Joint measurability of Z makes the actual endpoint map M measurable; its pushforward Q has mass one.', r'\nu_y=\pi_y\otimes\gamma,\quad M(z,w)=(z,Z(y,r,z,T,w)),\quad Q=M_*(\nu_y\otimes P),\quad Q(H\times H)=1.', '  have h103', '  have hB'),
    step('Retain joint endpoint and density measurability', 'Fix y,r with a measurable embedding and evaluate the jointly measurable prescribed path at T. Pairing with z yields B_n. The same actual finite-count theorem supplies the actual density rho, including terminal survival.', r'(z,t)\mapsto B_n(z,t),\qquad (z,t)\mapsto\rho_{y,r,z,n,T}(t)\quad\text{are measurable}.', '  have hB', '  have hm'),
    step('Justify integration over each time simplex', 'Express strict ordering and the terminal bound through measurable coordinate inequalities. The subtype measure maps to Lebesgue measure restricted to the simplex, so it is sigma-finite for every n, including n=0.', r'\Delta_n(T)=\{0<t_1<\cdots<t_n<T\},\quad\iota_*m_{n,T}=dt|_{\Delta_n(T)},\quad m_{n,T}\text{ sigma-finite}.', '  have hm', '  have hsum'),
    step('Make the sector integrals measurable in the initial phase', 'To identify measures, fix any measurable extended-nonnegative F. Joint measurability of B_n and rho and sigma-finiteness of m give measurable parameter integrals D_n(z). No finite-integral or signed domination premise is used.', r'D_n(z)=\int_{\Delta_n(T)}F(B_n(z,t))\rho_{y,r,z,n,T}(t)\,m_{n,T}(dt).', '  have hsum', '    have hz'),
    step('Partition the actual clock input by its finite count', 'For each fixed initial z, the Nat-valued total count has measurable disjoint fibers whose union is all clock inputs. Apply the actual finite-count test identity on each fiber using the terminal evaluation test. This gives a nonnegative countable expansion for the same Z. No joint-in-z count measurability is needed.', r'\int F(z,Z_T(w))\,P(dw)=\sum_{n\ge0}\int_{\{N(T)=n\}}F(z,Z_T(w))\,P(dw)=\sum_{n\ge0}D_n(z).', '    have hz', '    calc\n      (∫⁻ x'),
    step('Average and identify the full countable measure', 'Integrate the fixed-initial identity against nu_y. Nonnegative Tonelli on nu_y times P and on nu_y times m_n,T, together with measurable D_n and countable monotone summation, turns each term into the integral against L_n. Equality on every measurable extended-nonnegative F proves Q=sum L_n; infinite test integrals are allowed.', r'\int F\,dQ=\int\sum_nD_n\,d\nu_y=\sum_n\int D_n\,d\nu_y=\sum_n\int F\,dL_n=\int F\,d\!\left(\sum_nL_n\right).', '    calc\n      (∫⁻ x', '  have hsector'),
    step('Assemble the common endpoint reversal', 'Apply the reviewed normalized endpoint reversal to each n using the same literal J. Global measurability permits pushforward to commute with the countable sum. Combine with the actual-law equality and its already established probability.', r'J_*Q=J_*\!\left(\sum_n L_n\right)=\sum_nJ_*L_n=\sum_nL_n=Q.', '  have hsector', '\n#print axioms'),
]
assumptions = ['Finite-dimensional real inner-product Borel E with canonical volume, including rank zero.', 'alpha,beta>=0; alpha>0; alpha<=beta; V is C2; alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2 for every x,v; eta>0; beta*eta<=1.', 'The actual global process is existentially constructed, with joint measurability, literal arc/fallback characterization and almost-sure initialization. Every y,r and finite nonnegative T is included, and all n in Nat are summed.', 'All harmonic flow, totalized reflection, exponential clocks, strict simplex, actual event density, conditional Gibbs initial phase and endpoint measures are the displayed definitions. No supplied process, normalizer, integrability, joint count-measurability, cap or finite-sector-probability premise.']

source = dict(url=audit['source']['url'], edition='arXiv2609.06905v1', anchor=claim['source_anchor'], wording_status='faithful paraphrase', attribution=attribution)
deltas = [dict(source='A7 finite-count expansion followed by initial Gibbs averaging and nonnegative Tonelli.', lean='Actual endpoint probability Q equals the all-Nat sector sum and is preserved by J.', classification='same', reason='ASTIS exposes the measure identity of the source averaging step with all ingredients derived.'), dict(source='Finite-dimensional Euclidean phase.', lean='Finite real Hilbert Borel space including rank zero.', classification='generalization', reason='Coordinate-free canonical volume and Gaussian preserve the formulas.'), dict(source='Original six analytic assumptions.', lean='Same six assumptions, with one actual global process in the conclusion.', classification='same', reason='Unchanged presealed literal proposition.'), dict(source='Signed duality and invariant process arguments.', lean='Countable endpoint-law assembly and reversal only.', classification='unresolved', reason=claim['truth_boundary'])]

item = dict(id=slug, library='pbps', chapter='pbps-01', chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html', title=title, source=source, statement=restatement, assumptions=assumptions, formulae=[dict(label='Actual countable law', tex=steps[6]['formula']), dict(label='Endpoint-pair reversal', tex=steps[-1]['formula'])], obligations=[dict(id='countable-endpoint-law', label='Actual normalized countable endpoint law'), dict(id='weighted-invariance', label='Normalized averaging and invariant process law')], bindings=[dict(declaration=decl, cell=cid, role='proof-edge', supports=['countable-endpoint-law'], audit_id=aid, boundary=claim['truth_boundary'], assumption_deltas=deltas)])
for key in ['declaration_level', 'statement_seal', 'source_proof_coverage', 'proof_digestion', 'purification']:
    item[key] = copy.deepcopy(cell[key])
unit = dict(kind='theorem', declaration=decl, title=title, sources=[dict(url=source['url'], label=source['anchor'], scope=claim['truth_boundary'])], tests=claim['focused_checks'], assumptions=assumptions, statement=restatement, formula=steps[-1]['formula'], boundary=claim['truth_boundary'], steps=steps, lean_statement=restatement, lean_proof='; '.join(x['title'] for x in steps), helpers=[decl.rsplit('.', 1)[0] + '.actual_countable_endpoint_statement'], astis_dependencies=parents, mathlib_dependencies=["Measurable.lintegral_prod_right'", 'Measure.isProbabilityMeasure_map', 'map_comap_subtype_coe', 'SigmaFinite.of_map', 'Measure.ext_of_lintegral', 'lintegral_iUnion', 'lintegral_tsum', 'lintegral_prod', 'lintegral_map', 'lintegral_withDensity_eq_lintegral_mul', 'lintegral_sum_measure', 'Measure.map_sum' ])
pp = Path('website/content/publications') / (slug + '.json')
lp = Path('website/content/declaration_lessons') / (slug + '.json')
fresh(pp, dict(schema_version=1, items=[item]))
fresh(lp, dict(schema_version=1, units=[unit]))
pub.inputs.cache_clear()
pub.load.cache_clear()
audit['publication_binding_sha256'] = pub.binding_digest(item, item['bindings'][0], pub.inputs())
audit['publication_context'] = pub.review_context(item, item['bindings'][0], pub.inputs())
start = s.index('theorem actual_countable_endpoint_law')
stop = s.index(':= by\n', start)
audit['lean']['statement_representation'] = dict(kind='exact-literal-Prop-expansion', actual_header=s[start:stop], private_definition='def actual_countable_endpoint_statement' + literal, expanded_header='theorem actual_countable_endpoint_law' + statement_lean, source_approved_overlay=(pre / 'root.statement-seal105.json').as_posix(), kernel_header_and_literal_expansion_checked=False)
assert rt.decoder_packet(audit) == packet
save(ap, audit)
fresh(r / 'publication-freeze105.json', dict(status='DRAFT_PENDING_INDEPENDENT_MATH_DECODER_SOURCE_EXPOSITION', module=pin(module), inputs=[pin(p) for p in [pp, lp, ap]], packet=pin(out), canonical_packet_sha256=packet['packet_sha256'], steps=len(steps), conceptual_mirror_audit=cell['conceptual_mirror_audit'], PROVED_LOCAL=False, VERIFIED=False))
pub.check_advance([decl], reviewed=False)
print(json.dumps(dict(packet=pin(out), steps=len(steps), publication_binding_sha256=audit['publication_binding_sha256'])))
