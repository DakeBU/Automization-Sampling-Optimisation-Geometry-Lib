from pathlib import Path
import copy, hashlib, json, sys

root = Path.cwd()
r = Path(__file__).resolve().parent.relative_to(root.resolve())
pre = r.parent / 'pbps-bounded-gibbs-duality-preread106'
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
receipt = r / 'focused106/production1/receipt.json'
check = load(receipt)
assert check['exit_code'] == 0 and check['module_raw_sha256'] == sha(raw)
literal = s.split('private def actual_bounded_gibbs_duality_statement', 1)[1].split('set_option maxHeartbeats', 1)[0].strip()
seal = load(pre / 'root.statement-seal106.json')
assert literal == seal['expanded_literal_Prop'].strip()
binders, body = literal.split(' : Prop :=', 1)
body = body.removeprefix(' by\n  classical\n  exact\n')
statement_lean = binders + ' :\n' + body
old = load(r.parent / 'pbps-actual-countable-endpoint105/authored-statement105.json')['statement']
restatement = old.split('For the same single actual Z described above, every y,r')[0] + """
Write H=E times E, pi_y=volume_E.tilted(-V_y), gamma=stdGaussian(E), so nu_y=pi_y times gamma. For the same single global actual Z described above, every y,r in E and every finite T>=0, define op_T G(z)=integral G(Z(y,r,z,T,w)) dP(w), a real Bochner integral, and endpoint_T(z,w)=Z(y,r,z,T,w). Then endpoint_T is measurable and its pushforward of nu_y times P is exactly nu_y.
For every pair F,G:H->R of Borel measurable functions and finite real bounds C_F,C_G>=0 with |F(z)|<=C_F and |G(z)|<=C_G for all z, both z->F(z)*op_T G(z) and z->G(R(z))*op_T(F composed R)(z) are integrable against nu_y, and their real integrals are equal. Thus integral F(z)*op_T G(z) dnu_y(z) = integral G(R(z))*op_T(F composed R)(z) dnu_y(z).
All these conclusions use the same Z, existentially chosen before all centers, references, horizons and observables. Products are phase first, clock input second. No process, kernel, finite mass, signed integrability, momentum symmetry or normalizability is a supplied premise. Dimension zero, T=0, vanishing test bounds, zero bounce rates, infinite waits and raw exceptional fallback remain included. Almost-sure initialization stays parameterwise; no uniform all-parameter null set or pointwise reversed path at jumps is asserted.
The phase-invariance conclusion is fixed-time stationarity of the actual output under Gibbs initialization. It does not assert Markov/restart, Chapman-Kolmogorov, an L2 operator/domain identity, identification with a different existential kernel witness, hypocoercivity, implementation accuracy or actual expected oracle costs. Full paper results and actual-input composition remain open.
"""

attribution = 'Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1, Appendix A.1 final bounded bilinear identity and fixed-time stationarity, with Eq3.1 normalization. Complete attributed mathematical restatement. Signed integrability and the explicit same-process pushforward are ASTIS completion; this is not a verbatim standalone theorem quotation.'
context = ['Finite-dimensional real inner-product Borel space with canonical volume, including rank zero; genuine second Frechet derivative and real Hilbert gradient.', 'Fin n is zero-based; Fin.cons prepends; Fin.induction constructs a finite sequence; Fin.foldl visits ascending indices. Sum.inl represents a live time/state record; Unit represents a stopped record.', 'Real division by zero is zero; Real.toNNReal is positive part; nonnegative subtraction is truncated. ENNReal.ofReal embeds the positive part in extended nonnegative reals. Interval integrals use real Lebesgue measure.', 'Measure.tilted mu h is mu.withDensity(x -> ofReal(exp(h(x))/integral exp(h) dmu)). stdGaussian E is the centered identity-covariance Gaussian. Measure.comap along a measurable subtype inclusion is the induced subtype measure. Products use the displayed coordinate order.', 'MeasurePreserving f mu nu states Measurable f and Measure.map f mu = nu. withDensity multiplies the base measure by the given extended-nonnegative density. Measure.sum is the countable sum of the displayed measures. IsProbabilityMeasure means total mass one. All literal let bindings are definitions, not hypotheses.', 'hittingAfter f D 0 a is the infimum of nonnegative times t at which f t a lies in D, in WithTop nonnegative reals; the empty infimum is top. untopD 0 returns the finite value when not top and zero otherwise.', 'Measure.infinitePi constructs the displayed countable product law; expMeasure 1 is the unit-rate exponential probability measure on real numbers. The function space carries the coordinate-product measurable structure. A measurable global process and its almost-everywhere initialization are conclusions.']

aid = 'ASTIS-RT-20261012-PBPSActualBoundedGibbsDuality'
slug = 'pbps-actual-bounded-gibbs-duality'
title = 'Actual PBPS bounded Gibbs duality and fixed-time invariance'
audit = dict(id=aid, state='draft', source=dict(source_id='companion-domain:' + slug, anchor=claim['source_anchor'], url='https://arxiv.org/html/2609.06905v1#A1.E8', original_text=restatement, text_sha256=sha(restatement.encode())), lean=dict(statement=statement_lean.strip(), statement_sha256=sha(statement_lean.strip().encode()), compiled=True, decoder_context=context, declaration=decl, file=file, formalizer='companion_root_20261005', compiler_evidence=receipt.as_posix()), source_review=dict(state='pending'), repairs=[])
ap = Path('research-wiki/semantic-roundtrip/audits') / (aid + '.json')
fresh(ap, audit)
packet = rt.decoder_packet(audit)
out = Path('runs/semantic-roundtrip/anonymous106/input.json')
fresh(out, packet)
fresh(r / 'authored-statement106.json', dict(statement=restatement, attribution=attribution))
cp = Path('research-wiki/frontier-cells') / (cid + '.json')
cell = load(cp)
parents = cell['parents']
fresh(r / 'cell-before-compiled106.json', cell)
cell['evidence']['whole_target_compiled'] = pin(module)
cell['evidence']['focused_checks'] = [receipt.as_posix()]
cell['blocked']['reason'] = 'Full sealed target compiles; independent whole mathematics, blind decoding and source/exposition reviews pending.'
cell['purification']['dead_code_audit'] = 'One public bounded duality/invariance theorem and one literal private proposition; three actual public parents reused. Direct marginal implementation of fixed-time invariance is recorded separately from the printed F=1 route; no private dependency calls.'
save(cp, cell)

def step(title, text, formula, start, end):
    a, b = s.index(start), s.index(end, s.index(start))
    code = s[a:b]
    return dict(title=title, text=text, formula=formula, lean=code, detail='ASTIS completion of bounded signed averaging and fixed-time stationarity. Exact compiled region; the original six analytic assumptions are unchanged.', lean_source_region=dict(path=file, source_raw_sha256=sha(raw), start_line=s[:a].count('\n') + 1, end_line=s[:b].count('\n'), exact_code_raw_sha256=sha(code.encode())))

steps = [
    step('Keep the same global actual process', 'Consume the actual countable endpoint-law producer once. Retain the exact joint measurability, live-arc, raw fallback and parameterwise almost-sure initialization of its single global Z. All subsequent maps and test integrals use this witness.', r'Z(y,r,z,s,w)=\Phi_{s-a}(b)\text{ on a live arc};\qquad Z(y,r,z,0,w)=z\quad P\text{-a.e.}', '  obtain ⟨Z', '  have h103'),
    step('Recover the actual probability laws and endpoint reversal', 'Write H=E×E, pi_y=volume_E.tilted(-V_y), gamma=stdGaussian(E), and nu_y=pi_y times gamma. The normalization and clock producers prove that nu_y and P are probability measures. Joint Z makes endpoint and M measurable. The countable-law producer gives probability of Q and J-preservation; these are internal dependencies.', r'M(z,w)=(z,Z_T(z,w)),\quad Q=M_*(\nu_y\otimes P),\quad J(a,b)=(Rb,Ra),\quad J_*Q=Q.', '  have h103', '  have hRm'),
    step('Prove momentum-flip symmetry of the actual phase law', 'Negation is a linear isometry of E, so it preserves the standard Gaussian, including dimension zero. Product pushforward leaves the tilted position factor unchanged and negates only the momentum factor. Thus the literal R is measurable and preserves nu_y.', r'(-\mathrm{id})_*\gamma=\gamma,\qquad R_*(\pi_y\otimes\gamma)=\pi_y\otimes\gamma=\nu_y.', '  have hRm', '  have hMP'),
    step('Identify the actual fixed-time Gibbs marginal', 'The initial marginal of Q is nu_y because P has mass one. Compose the preserving maps M, J, first projection and R. Since R is an involution, R composed fst composed J is the second projection; the resulting map is the actual endpoint. This is the explicitly recorded direct-marginal implementation of the source stationarity consequence. The printed F=1 argument follows from the bounded identity proved below.', r'\mathrm{fst}_*Q=\nu_y,\quad R\circ\mathrm{fst}\circ J=\mathrm{snd},\quad (\mathrm{endpoint}_T)_*(\nu_y\otimes P)=\nu_y.', '  have hMP', '  have htest'),
    step('Derive product integrability from the observable bounds', 'Fix arbitrary measurable real F,G with finite nonnegative bounds C_F,C_G. Their actual-input product H_FG(z,w)=F(z)G(Z_T(z,w)) is measurable and bounded by C_F C_G. The input product is probability, so this bound proves honest real Bochner integrability without any integrability premise.', r'|F(z)G(Z_T(z,w))|\le C_FC_G,\qquad H_{F,G}\in L^1(\nu_y\otimes P).', '  have htest', '    have houter'),
    step('Use signed Fubini and pushforward for the test identity', 'Product integrability yields integrability of the inner integral. Pull F(z) through the clock integral, then apply signed Fubini. The measurable pushforward M identifies the resulting integral with the endpoint-pair test under Q. This proves both the outer L1 conclusion and its exact integral representation.', r'\int F(z)\,\operatorname{op}_TG(z)\,\nu_y(dz)=\int F(z)G(Z_T(z,w))\,d(\nu_y\otimes P)=\int F(a)G(b)\,Q(d(a,b)).', '    have houter', '  intro F G'),
    step('Apply the same integrability argument to the flipped tests', 'Apply the already proved test identity first to F,G and then to G composed R,F composed R. Measurability of R and the original pointwise bounds give all required hypotheses. Both displayed outer integrals are therefore integrable, including when either bound vanishes.', r'(F,G)\quad\text{and}\quad(G\circ R,F\circ R)\quad\Longrightarrow\quad\text{both outer tests belong to }L^1(\nu_y).', '  intro F G', '  calc\n    (∫ a'),
    step('Transfer endpoint reversal to bounded signed duality', 'Use the measurable map J and J_*Q=Q in the real integral-map identity for F(a)G(b). After the flipped swap the integrand is F(Rb)G(Ra); commute the real factors and combine the two test representations. No unbounded observable or L2 extension is inferred.', r'\int F(a)G(b)\,dQ=\int F(Rb)G(Ra)\,dQ=\int G(Rz)\,\operatorname{op}_T(F\circ R)(z)\,\nu_y(dz).', '  calc\n    (∫ a', '\n#print axioms'),
]
assumptions = ['Finite-dimensional real inner-product Borel E with canonical volume, including rank zero.', 'alpha,beta>=0; alpha>0; alpha<=beta; V is C2; alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2 for every x,v; eta>0; beta*eta<=1.', 'A single global actual process is constructed in the conclusion, with the literal joint measurability, arc/fallback and parameterwise almost-sure initialization contracts; every y,r and finite nonnegative T is included.', 'The universal bounded-observable conclusion ranges over measurable real F,G and finite nonnegative C_F,C_G with pointwise absolute-value bounds. These are test domains, not extra assumptions on the sampler.', 'All actual algorithm, clock and Gibbs phase objects are defined literally; no supplied Z/kernel, integrability, normalizer, momentum symmetry, restart or Markov premise.']

source = dict(url=audit['source']['url'], edition='arXiv2609.06905v1', anchor=claim['source_anchor'], wording_status='faithful paraphrase', attribution=attribution)
deltas = [dict(source='Bounded signed bilinear identity and Gibbs stationarity in Appendix A.1.', lean='Both real outer integrals are integrable, have the stated flipped equality, and the same actual endpoint preserves nu_y.', classification='same', reason='Signed Fubini and momentum symmetry are proved internally.'), dict(source='Finite-dimensional Euclidean phase.', lean='Finite real inner-product Borel space including rank zero.', classification='generalization', reason='Coordinate-free canonical volume and Gaussian preserve the formulas.'), dict(source='Printed F=1 marginal consequence.', lean='Equivalent direct first/second marginal argument through actual endpoint reversal, with full bounded duality also proved.', classification='same', reason='Selected route explicitly allowed in the independently reviewed source graph; exact implementation selection is recorded.'), dict(source='L2 operator and later sampler results.', lean='Fixed-time stationarity and bounded real-test duality only.', classification='unresolved', reason=claim['truth_boundary'])]
item = dict(id=slug, library='pbps', chapter='pbps-01', chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html', title=title, source=source, statement=restatement, assumptions=assumptions, formulae=[dict(label='Actual fixed-time stationarity', tex=steps[3]['formula']), dict(label='Bounded signed Gibbs duality', tex=steps[-1]['formula'])], obligations=[dict(id='bounded-gibbs-duality', label='Actual bounded Gibbs duality and fixed-time phase invariance'), dict(id='process-semigroup', label='Actual restart and semigroup law')], bindings=[dict(declaration=decl, cell=cid, role='proof-edge', supports=['bounded-gibbs-duality'], audit_id=aid, boundary=claim['truth_boundary'], assumption_deltas=deltas)])

for key in ['declaration_level', 'statement_seal', 'source_proof_coverage', 'proof_digestion', 'purification']:
    item[key] = copy.deepcopy(cell[key])
unit = dict(kind='theorem', declaration=decl, title=title, sources=[dict(url=source['url'], label=source['anchor'], scope=claim['truth_boundary'])], tests=claim['focused_checks'], assumptions=assumptions, statement=restatement, formula=steps[-1]['formula'], boundary=claim['truth_boundary'], steps=steps, lean_statement=restatement, lean_proof='; '.join(x['title'] for x in steps), helpers=[decl.rsplit('.', 1)[0] + '.actual_bounded_gibbs_duality_statement'], astis_dependencies=parents, mathlib_dependencies=['stdGaussian_map', 'Measure.map_prod_map', 'Measure.map_map', 'Measure.map_fst_prod', 'MeasurePreserving.comp', 'Integrable.of_bound', 'Integrable.integral_prod_left', 'integral_const_mul', 'integral_prod', 'integral_map'])

pp = Path('website/content/publications') / (slug + '.json')
lp = Path('website/content/declaration_lessons') / (slug + '.json')
fresh(pp, dict(schema_version=1, items=[item]))
fresh(lp, dict(schema_version=1, units=[unit]))
pub.inputs.cache_clear()
pub.load.cache_clear()
audit['publication_binding_sha256'] = pub.binding_digest(item, item['bindings'][0], pub.inputs())
audit['publication_context'] = pub.review_context(item, item['bindings'][0], pub.inputs())
start = s.index('theorem actual_bounded_gibbs_duality')
stop = s.index(':= by\n', start)
audit['lean']['statement_representation'] = dict(kind='exact-literal-Prop-expansion', actual_header=s[start:stop], private_definition='def actual_bounded_gibbs_duality_statement' + literal, expanded_header='theorem actual_bounded_gibbs_duality' + statement_lean, source_approved_overlay=(pre / 'root.statement-seal106.json').as_posix(), kernel_header_and_literal_expansion_checked=False)
assert rt.decoder_packet(audit) == packet
save(ap, audit)
fresh(r / 'publication-freeze106.json', dict(status='DRAFT_PENDING_INDEPENDENT_MATH_DECODER_SOURCE_EXPOSITION', module=pin(module), inputs=[pin(p) for p in [pp, lp, ap]], packet=pin(out), canonical_packet_sha256=packet['packet_sha256'], steps=len(steps), conceptual_mirror_audit=cell['conceptual_mirror_audit'], PROVED_LOCAL=False, VERIFIED=False))
pub.check_advance([decl], reviewed=False)
print(json.dumps(dict(packet=pin(out), steps=len(steps), publication_binding_sha256=audit['publication_binding_sha256'])))
