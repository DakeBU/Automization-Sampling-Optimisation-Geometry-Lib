from pathlib import Path
import copy, hashlib, json, sys

root = Path.cwd()
r = Path(__file__).resolve().parent.relative_to(root.resolve())
pre = r.parent / 'pbps-actual-l2-expectation-preread107'
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
receipt = r / 'focused107/production1/receipt.json'
check = load(receipt)
assert check['exit_code'] == 0 and check['module_raw_sha256'] == sha(raw)
literal = s.split('private def actual_l2_expectation_statement', 1)[1].split('set_option maxHeartbeats', 1)[0].strip()
seal = load(pre / 'root.statement-seal107.json')
assert literal == seal['expanded_literal_Prop'].strip()
binders, body = literal.split(' : Prop :=', 1)
body = body.removeprefix(' by\n  classical\n  exact\n')
statement_lean = binders + ' :\n' + body
old = load(r.parent / 'pbps-actual-bounded-gibbs-duality106/authored-statement106.json')['statement']
restatement = old.split('The phase-invariance conclusion')[0] + """
For every Borel G:H->R, the total real clock expectation (y,r,z,T)->integral G(Z(y,r,z,T,w)) dP(w) is jointly Borel. If C is a finite nonnegative real number and |G(z)|<=C for all z, then for every y,r,z,T the clock section is P-integrable and the absolute value of this expectation is at most C.
For every y,r in E there exists a family A indexed by finite nonnegative T, where A_T:L2(nu_y;R)->L2(nu_y;R) is a continuous real linear operator, A_0 is the identity and ||A_T||<=1 for every T. For every real function G with MemLp G 2 nu_y (almost-everywhere strong measurability and finite L2 seminorm), the section w->G(Z(y,r,z,T,w)) is P-integrable for nu_y-almost every z. The literal expectation op_T G belongs to L2(nu_y;R), and A_T[G]=[op_T G]. Thus integral |op_T G|^2 dnu_y <= integral |G|^2 dnu_y. Brackets denote equality classes modulo nu_y-almost-everywhere equality; no pointwise identification of arbitrary L2 representatives is asserted. The operator, section integrability and output L2 membership are conclusions, not supplied premises.
These operators use the same single global Z as all inherited path, initialization, invariance and bounded-duality conclusions. The bound1 is exact and independent of dimension, center, reference and horizon. The joint Borel assertion concerns Borel input G; arbitrary MemLp representatives receive the stated almost-everywhere conclusions. There is no joint measurability or continuity claim for the operator-valued family, no strong-continuity claim, and no assertion of full L2 momentum-flip duality Eq A.3, restart/Markov/semigroup, equality with a separately existential kernel, hypocoercivity, implementation accuracy or actual expected costs. Full papers and actual-input composition remain open.
"""
attribution = 'Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1, Appendix A.1 bounded averaging toward Eq A.3, with Eq3.1 normalization. Complete attributed mathematical restatement. Actual L2 operator construction, integrability and quotient-representative identification are ASTIS completion of the domain requirements; this is not a verbatim standalone theorem quotation.'

context = ['Finite-dimensional real inner-product Borel space with canonical volume, including rank zero; genuine second Frechet derivative and real Hilbert gradient.', 'Fin n is zero-based; Fin.cons prepends; Fin.induction constructs a finite sequence; Fin.foldl visits ascending indices. Sum.inl represents a live time/state record; Unit represents a stopped record.', 'Real division by zero is zero; Real.toNNReal is positive part; nonnegative subtraction is truncated. ENNReal.ofReal embeds the positive part in extended nonnegative reals. Interval integrals use real Lebesgue measure.', 'Measure.tilted mu h is mu.withDensity(x -> ofReal(exp(h(x))/integral exp(h) dmu)). stdGaussian E is the centered identity-covariance Gaussian. Measure.comap along a measurable subtype inclusion is the induced subtype measure. Products use the displayed coordinate order.', 'MeasurePreserving f mu nu states Measurable f and Measure.map f mu = nu. withDensity multiplies the base measure by the given extended-nonnegative density. Measure.sum is the countable sum of the displayed measures. IsProbabilityMeasure means total mass one. All literal let bindings are definitions, not hypotheses.', 'hittingAfter f D 0 a is the infimum of nonnegative times t at which f t a lies in D, in WithTop nonnegative reals; the empty infimum is top. untopD 0 returns the finite value when not top and zero otherwise.', 'Measure.infinitePi constructs the displayed countable product law; expMeasure 1 is the unit-rate exponential probability measure on real numbers. The function space carries the coordinate-product measurable structure. A measurable global process and its almost-everywhere initialization are conclusions.']

context += ['Lp R 2 mu is the real Hilbert space of square-integrable strongly measurable functions modulo almost-everywhere equality; MemLp is the corresponding property of a raw function and hG.toLp G is its equivalence class.', 'The notation X ->L[R] Y means a continuous real linear map with operator norm. ContinuousLinearMap.id is the identity; an indexed family of such maps alone imposes no continuity in the index.']

aid = 'ASTIS-RT-20261012-PBPSActualL2Expectation'
slug = 'pbps-actual-l2-expectation'
title = 'Actual PBPS fixed-time L2 expectation contraction'
audit = dict(id=aid, state='draft', source=dict(source_id='companion-domain:' + slug, anchor=claim['source_anchor'], url='https://arxiv.org/html/2609.06905v1#A1.E3', original_text=restatement, text_sha256=sha(restatement.encode())), lean=dict(statement=statement_lean.strip(), statement_sha256=sha(statement_lean.strip().encode()), compiled=True, decoder_context=context, declaration=decl, file=file, formalizer='companion_root_20261005', compiler_evidence=receipt.as_posix()), source_review=dict(state='pending'), repairs=[])
ap = Path('research-wiki/semantic-roundtrip/audits') / (aid + '.json')
fresh(ap, audit)
packet = rt.decoder_packet(audit)
out = Path('runs/semantic-roundtrip/anonymous107/input.json')
fresh(out, packet)
fresh(r / 'authored-statement107.json', dict(statement=restatement, attribution=attribution))
cp = Path('research-wiki/frontier-cells') / (cid + '.json')
cell = load(cp)
parents = cell['parents']
fresh(r / 'cell-before-compiled107.json', cell)
cell['evidence']['whole_target_compiled'] = pin(module)
cell['evidence']['focused_checks'] = [receipt.as_posix()]
cell['blocked']['reason'] = 'Full sealed target compiles; independent whole mathematics, blind decoding and source/exposition reviews pending.'
cell['purification']['dead_code_audit'] = 'One public actual L2 expectation theorem and one literal private proposition; three proof-local ingredient blocks reuse pinned Mathlib. Actual public106/103/UnitExponentialProduct are the three producers. No private dependency calls or semigroup assertion.'
save(cp, cell)

def step(title, text, formula, start, end):
    a, b = s.index(start), s.index(end, s.index(start))
    code = s[a:b]
    return dict(title=title, text=text, formula=formula, lean=code, detail='ASTIS completion of actual fixed-time L2 averaging. Exact compiled region; original six analytic assumptions and same global process are unchanged.', lean_source_region=dict(path=file, source_raw_sha256=sha(raw), start_line=s[:a].count('\n') + 1, end_line=s[:b].count('\n'), exact_code_raw_sha256=sha(code.encode())))

steps = [
    step('Retain the same actual process and all bounded results', 'Consume the actual bounded-duality producer once. Preserve its joint measurable process, exact live arcs and fallback, parameterwise clock-almost-sure initialization, fixed-time Gibbs preservation and bounded momentum-flip duality. Every new expectation below uses this same witness.', r'Z\text{ fixed globally};\quad (Z_T)_*(\nu_y\otimes P)=\nu_y;\quad Z_0(z,w)=z\quad P\text{-a.e.}', '  obtain ⟨Z', '  have hpair_core'),
    step('Construct the Hilbert-space averaging contraction', 'For a probability input mu times nu and a measure-preserving endpoint, pullback along first projection and endpoint gives L2 isometries B and C. Define the operator internally by A=B* C. Adjoint norm preservation gives ||A||<=1. The adjoint identity and the exact pullback representatives give the displayed product pairing. This proof-local lemma is later instantiated with the actual Gibbs and clock laws, not assumed about the sampler.', r'Bf(z,w)=f(z),\quad Cg(z,w)=g(Z_T(z,w)),\quad A=B^*C,\quad\|A\|\le1,\quad\langle f,Ag\rangle=\int f(z)g(Z_T(z,w))\,d(\mu\otimes\nu).', '  have hpair_core', '  have haverage_core'),
    step('Prove product and outer integrability before identification', 'For arbitrary MemLp input G, endpoint preservation transports L2 to the input product probability, hence to L1. Signed Fubini gives almost-everywhere clock-section integrability and outer L1. The constructed operator output is itself in L2 and therefore L1. These facts precede the uniqueness argument; output expectation L2 has not been assumed.', r'G\in L^2(\mu)\Rightarrow G\circ Z_T\in L^2(\mu\otimes\nu)\subset L^1;\qquad z\mapsto\int G(Z_T(z,w))\,d\nu(w)\in L^1(\mu).', '  have haverage_core', '    have heq :'),
    step('Identify the average through measurable-set indicators', 'Test the product pairing against the L2 class of 1_s for each measurable set s. Pullback preserves almost-everywhere changes of both indicator and G representatives. The indicator-weighted product is integrable; signed Fubini equates the two set integrals. L1 set-integral uniqueness then identifies the operator representative with the literal clock expectation almost everywhere.', r'\int_s A[G]\,d\mu=\langle1_s,A[G]\rangle=\int1_s(z)G(Z_T(z,w))\,d(\mu\otimes\nu)=\int_s\operatorname{op}_TG\,d\mu.', '    have heq :', '    have hOp :'),
    step('Transfer L2 membership to the actual expectation', 'The identified operator representative is L2. Transfer this membership across the proved almost-everywhere equality and use Lp extensionality to certify the exact quotient equality. Together with product Fubini this returns the section L1 and output membership conclusions for arbitrary MemLp representatives.', r'\operatorname{op}_TG=A[G]\quad\mu\text{-a.e.}\quad\Rightarrow\quad\operatorname{op}_TG\in L^2(\mu),\quad[\operatorname{op}_TG]=A[G].', '    have hOp :', '  have hsquare_core'),
    step('Relate the scalar square integral to the L2 norm', 'The canonical toLp representative agrees almost everywhere with the raw function. Substitute this equality in the real inner-product integral; the Hilbert norm identity gives the exact square integral. This converts the operator norm bound into the requested scalar inequality.', r'\int |G|^2\,d\mu=\langle[G],[G]\rangle=\|[G]\|_2^2.', '  have hsquare_core', '  refine ⟨Z, hZm'),
    step('Prove joint Borel expectation and every bounded section', 'For Borel G, compose the jointly measurable actual Z with G and integrate out the clock variable under its probability law. Product-integral measurability gives joint Borel dependence on y,r,z,T. A pointwise finite bound C proves every clock section integrable and the expectation bound, including C=0.', r'(y,r,z,T)\mapsto\int G(Z(y,r,z,T,w))\,dP(w)\text{ is Borel};\quad |G|\le C\Rightarrow |\operatorname{op}_TG|\le C.', '  refine ⟨Z, hZm', '  · intro y xRef'),
    step('Instantiate the construction at the actual probability laws', 'Recover nu_y probability from actual Gibbs normalization and P probability from the countable exponential producer. Actual fixed-time endpoint preservation, inherited from the same Z, supplies the input to the proved local averaging construction. Choose one operator for each T; no regularity of the operator-valued family is inferred.', r'\mu=\nu_y,\quad\nu=P,\quad(Z_T)_*(\nu_y\otimes P)=\nu_y\Rightarrow\exists(A_T)_{T\ge0}\text{ with }\|A_T\|\le1.', '  · intro y xRef', '    refine ⟨L, ?_, ?_⟩'),
    step('Prove the zero-time operator is the identity', 'Apply representative identification to the canonical representative of an arbitrary L2 class. The inherited parameterwise clock-almost-sure equality Z_0(z,w)=z makes its clock integral equal to that representative for each z. Lp and continuous-linear-map extensionality imply A_0=id without a uniform parameter-null-set assumption.', r'\int f(Z_0(z,w))\,dP(w)=f(z)\quad\Rightarrow\quad A_0[f]=[f],\qquad A_0=\mathrm{id}.', '    refine ⟨L, ?_, ?_⟩', '    · intro T'),
    step('Return the actual L2 representative and square contraction', 'For every T and every MemLp G, return the previously proved section integrability and exact toLp equality. Express both scalar square integrals as L2 norm squares, use the operator bound1, then square the nonnegative norm inequality. This completes the fixed-time result; full L2 momentum-flip duality remains a separate density argument.', r'\int|\operatorname{op}_TG|^2\,d\nu_y=\|A_T[G]\|_2^2\le\|[G]\|_2^2=\int|G|^2\,d\nu_y.', '    · intro T', '\n#print axioms'),
]

assumptions = ['Finite-dimensional real inner-product Borel E with canonical volume, including rank zero.', 'alpha,beta>=0; alpha>0; alpha<=beta; V is C2; alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2 for every x,v; eta>0; beta*eta<=1.', 'A single global actual process is constructed in the conclusion, with the literal joint measurability, arc/fallback and parameterwise almost-sure initialization contracts; every y,r and finite nonnegative T is included.', 'The universal bounded-observable conclusion ranges over measurable real F,G and finite nonnegative C_F,C_G with pointwise absolute-value bounds. These are test domains, not extra assumptions on the sampler.', 'For the L2 conclusion G is any real function with MemLp G 2 nu_y. For joint Borel dependence G is Borel; every-section L1 additionally uses a finite nonnegative pointwise bound. Operator existence, integrability, output membership and bound1 are conclusions.', 'All actual algorithm, clock and Gibbs phase objects are literal. No supplied Z/kernel/operator, integrability, normalizer, momentum symmetry, restart or Markov premise.']

source = dict(url=audit['source']['url'], edition='arXiv2609.06905v1', anchor=claim['source_anchor'], wording_status='faithful paraphrase', attribution=attribution)
deltas = [dict(source='Appendix A.1 actual expectation and L2 domain toward Eq A.3.', lean='Same-process Borel expectation and a norm-one-or-smaller continuous real L2 operator with exact representative and zero-time identity.', classification='same', reason='Operator construction and all integrability are discharged internally as ASTIS completion.'), dict(source='Finite-dimensional Euclidean phase.', lean='Finite real inner-product Borel space including rank zero.', classification='generalization', reason='Canonical volume/Gaussian formulation preserves the source formulas.'), dict(source='Full Eq A.3 and later process/sampler properties.', lean='The fixed-time L2 contraction domain is closed; full L2 flip identity and semigroup properties are not asserted.', classification='unresolved', reason=claim['truth_boundary'])]
item = dict(id=slug, library='pbps', chapter='pbps-01', chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html', title=title, source=source, statement=restatement, assumptions=assumptions, formulae=[dict(label='Actual L2 expectation and contraction', tex=steps[-1]['formula']), dict(label='Zero-time identity', tex=steps[-2]['formula'])], obligations=[dict(id='actual-l2-expectation', label='Actual fixed-time L2 expectation contraction'), dict(id='l2-flip-duality', label='Full L2 momentum-flip identity')], bindings=[dict(declaration=decl, cell=cid, role='proof-edge', supports=['actual-l2-expectation'], audit_id=aid, boundary=claim['truth_boundary'], assumption_deltas=deltas)])

for key in ['declaration_level', 'statement_seal', 'source_proof_coverage', 'proof_digestion', 'purification']:
    item[key] = copy.deepcopy(cell[key])
unit = dict(kind='theorem', declaration=decl, title=title, sources=[dict(url=source['url'], label=source['anchor'], scope=claim['truth_boundary'])], tests=claim['focused_checks'], assumptions=assumptions, statement=restatement, formula=steps[-1]['formula'], boundary=claim['truth_boundary'], steps=steps, lean_statement=restatement, lean_proof='; '.join(x['title'] for x in steps), helpers=[decl.rsplit('.', 1)[0] + '.actual_l2_expectation_statement'], astis_dependencies=parents, mathlib_dependencies=['StronglyMeasurable.integral_prod_right', 'Integrable.of_bound', 'norm_integral_le_of_norm_le_const', 'Lp.compMeasurePreservingₗᵢ', 'Lp.coeFn_compMeasurePreserving', 'ContinuousLinearMap.adjoint_inner_right', 'ContinuousLinearMap.opNorm_comp_le', 'LinearIsometry.norm_toContinuousLinearMap_le', 'MemLp.integrable', 'Integrable.prod_right_ae', 'Integrable.integral_prod_left', 'L2.inner_indicatorConstLp_one', 'integral_prod', 'Integrable.ae_eq_of_forall_setIntegral_eq', 'memLp_congr_ae', 'Lp.ext', 'integral_eq_const', 'Lp.toLp_coeFn'])

pp = Path('website/content/publications') / (slug + '.json')
lp = Path('website/content/declaration_lessons') / (slug + '.json')
fresh(pp, dict(schema_version=1, items=[item]))
fresh(lp, dict(schema_version=1, units=[unit]))
pub.inputs.cache_clear()
pub.load.cache_clear()
audit['publication_binding_sha256'] = pub.binding_digest(item, item['bindings'][0], pub.inputs())
audit['publication_context'] = pub.review_context(item, item['bindings'][0], pub.inputs())
start = s.index('theorem actual_l2_expectation_contraction')
stop = s.index(':= by\n', start)
audit['lean']['statement_representation'] = dict(kind='exact-literal-Prop-expansion', actual_header=s[start:stop], private_definition='def actual_l2_expectation_statement' + literal, expanded_header='theorem actual_l2_expectation_contraction' + statement_lean, source_approved_overlay=(pre / 'root.statement-seal107.json').as_posix(), kernel_header_and_literal_expansion_checked=False)
assert rt.decoder_packet(audit) == packet
save(ap, audit)
fresh(r / 'publication-freeze107.json', dict(status='DRAFT_PENDING_INDEPENDENT_MATH_DECODER_SOURCE_EXPOSITION', module=pin(module), inputs=[pin(p) for p in [pp, lp, ap]], packet=pin(out), canonical_packet_sha256=packet['packet_sha256'], steps=len(steps), conceptual_mirror_audit=cell['conceptual_mirror_audit'], PROVED_LOCAL=False, VERIFIED=False))
pub.check_advance([decl], reviewed=False)
print(json.dumps(dict(packet=pin(out), steps=len(steps), publication_binding_sha256=audit['publication_binding_sha256'])))
