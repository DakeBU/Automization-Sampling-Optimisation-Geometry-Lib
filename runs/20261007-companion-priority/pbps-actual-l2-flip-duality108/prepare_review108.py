from pathlib import Path
import copy, hashlib, json, sys

root = Path.cwd()
r = Path(__file__).resolve().parent.relative_to(root.resolve())
pre = r.parent / 'pbps-actual-l2-flip-preread108'
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
receipt = r / 'focused108/full2/receipt.json'
check = load(receipt)
assert check['exit_code'] == 0 and check['input_RAW_sha256'] == sha(raw)
literal = s.split('private def actual_l2_flip_statement', 1)[1].split('set_option maxHeartbeats', 1)[0].strip()
seal = load(pre / 'root.statement-seal108.json')
assert literal == seal['expanded_literal_Prop'].strip()
binders, body = literal.split(' : Prop :=', 1)
body = body.removeprefix(' by\n  classical\n  exact\n')
statement_lean = binders + ' :\n' + body
old = load(r.parent / 'pbps-actual-l2-expectation107/authored-statement107.json')['statement']
restatement = old.split('There is no joint measurability or continuity claim')[0] + """
In addition, for each y,r the same operator family A has the following property. The literal phase reflection R(x,p)=(x,-p) preserves nu_y. Its canonical pullback J_y on real L2(nu_y) is the linear isometry defined by composition with R; for every L2 class f, (J_y f)(z)=f(R(z)) for nu_y-almost every z, and J_y(J_y f)=f. For every finite nonnegative T, the Hilbert adjoint of that same A_T satisfies A_T*=J_y A_T J_y as an equality of continuous real linear operators. Equivalently its pairing obeys <f,A_T g>=<J_y g,A_T(J_y f)> for all real L2 classes f,g. The pullback and its preservation/involution are proved conclusions; no supplied symmetry, operator relation, integrability or density hypothesis is added.
The flip depends only on the displayed R and nu_y; the proof witness hR under y,r does not introduce reference or time dependence into J_y. The identity includes T=0 and rank zero. All representative equalities retain their stated almost-everywhere sense, with no common null set over all parameters or representatives. This is the full fixed-time real-L2 identity of Appendix A.3, together with the exact inherited process and expectation contract. Strong continuity, restart/Markov/semigroup, complex-L2 extension, a separately existential kernel identification, actual momentum-averaged position operator, hypocoercivity, implementation errors, actual expected costs, actual-input composition and complete papers remain outside this result.
"""
attribution = 'Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1, Appendix A.1 Eq A.3 and final density extension, with Eq3.1 phase law. Complete attributed mathematical restatement; ASTIS makes the canonical L2 flip and dense-subspace extension explicit. This is not a verbatim standalone theorem quotation.'

context = ['Finite-dimensional real inner-product Borel space with canonical volume, including rank zero; genuine second Frechet derivative and real Hilbert gradient.', 'Fin n is zero-based; Fin.cons prepends; Fin.induction constructs a finite sequence; Fin.foldl visits ascending indices. Sum.inl represents a live time/state record; Unit represents a stopped record.', 'Real division by zero is zero; Real.toNNReal is positive part; nonnegative subtraction is truncated. ENNReal.ofReal embeds the positive part in extended nonnegative reals. Interval integrals use real Lebesgue measure.', 'Measure.tilted mu h is mu.withDensity(x -> ofReal(exp(h(x))/integral exp(h) dmu)). stdGaussian E is the centered identity-covariance Gaussian. Measure.comap along a measurable subtype inclusion is the induced subtype measure. Products use the displayed coordinate order.', 'MeasurePreserving f mu nu states Measurable f and Measure.map f mu = nu. withDensity multiplies the base measure by the given extended-nonnegative density. Measure.sum is the countable sum of the displayed measures. IsProbabilityMeasure means total mass one. All literal let bindings are definitions, not hypotheses.', 'hittingAfter f D 0 a is the infimum of nonnegative times t at which f t a lies in D, in WithTop nonnegative reals; the empty infimum is top. untopD 0 returns the finite value when not top and zero otherwise.', 'Measure.infinitePi constructs the displayed countable product law; expMeasure 1 is the unit-rate exponential probability measure on real numbers. The function space carries the coordinate-product measurable structure. A measurable global process and its almost-everywhere initialization are conclusions.']

context += ['Lp R 2 mu is the real Hilbert space of square-integrable strongly measurable functions modulo almost-everywhere equality; MemLp is the corresponding property of a raw function and hG.toLp G is its equivalence class.', 'The notation X ->L[R] Y means a continuous real linear map with operator norm. ContinuousLinearMap.id is the identity; an indexed family of such maps alone imposes no continuity in the index.']

context += ['The notation X ->li[R] Y denotes a real linear norm-preserving map. Lp.compMeasurePreserving_li R hR is the canonical pullback on Lp classes by a measure-preserving map R. The adjoint A.adjoint is the real Hilbert adjoint characterized by <A* f,g>=<f,A g>; comp composes continuous linear maps.']

aid = 'ASTIS-RT-20261012-PBPSActualL2FlipDuality'
slug = 'pbps-actual-l2-flip-duality'
title = 'Actual PBPS full real-L2 momentum-flip adjoint identity'
audit = dict(id=aid, state='draft', source=dict(source_id='companion-domain:' + slug, anchor=claim['source_anchor'], url='https://arxiv.org/html/2609.06905v1#A1.E3', original_text=restatement, text_sha256=sha(restatement.encode())), lean=dict(statement=statement_lean.strip(), statement_sha256=sha(statement_lean.strip().encode()), compiled=True, decoder_context=context, declaration=decl, file=file, formalizer='companion_root_20261005', compiler_evidence=receipt.as_posix()), source_review=dict(state='pending'), repairs=[])
ap = Path('research-wiki/semantic-roundtrip/audits') / (aid + '.json')
fresh(ap, audit)
packet = rt.decoder_packet(audit)
out = Path('runs/semantic-roundtrip/anonymous108/input.json')
fresh(out, packet)
fresh(r / 'authored-statement108.json', dict(statement=restatement, attribution=attribution))
cp = Path('research-wiki/frontier-cells') / (cid + '.json')
cell = load(cp)
parents = cell['parents']
fresh(r / 'cell-before-compiled108.json', cell)
cell['evidence']['whole_target_compiled'] = pin(module)
cell['evidence']['focused_checks'] = [receipt.as_posix()]
cell['blocked']['reason'] = 'Full sealed target compiles; independent whole mathematics, blind decoding and source/exposition reviews pending.'
cell['purification']['dead_code_audit'] = 'One public actual full real-L2 flip theorem and one literal private proposition. Same-process public107 is the only direct actual producer. Canonical flip, simple representative pairings, two-variable density and adjoint uniqueness are local blocks using pinned Mathlib. No private producer calls or semigroup assertion.'
save(cp, cell)

def step(title, text, formula, start, end):
    a, b = s.index(start), s.index(end, s.index(start))
    code = s[a:b]
    return dict(title=title, text=text, formula=formula, lean=code, detail='ASTIS expansion of the source dense-subspace extension for full real-L2 flip duality. Exact compiled region; original six analytic assumptions and same global process are unchanged.', lean_source_region=dict(path=file, source_raw_sha256=sha(raw), start_line=s[:a].count('\n') + 1, end_line=s[:b].count('\n'), exact_code_raw_sha256=sha(code.encode())))

steps = [
    step('Retain one actual process and the same expectation family', 'Invoke the previous actual expectation theorem once. Carry its global process, live arcs, fallback, initialization, invariant phase law, bounded duality, Borel expectation and every L2 contraction conclusion. Fix y,r and use precisely its family A; the proof never chooses another path or operator.', r'Z\text{ fixed};\quad A_T[G]=[\operatorname{op}_TG],\quad A_0=I,\quad\|A_T\|\le1.', '  obtain ⟨Z', '  have hRm'),
    step('Preserve the actual phase law under momentum reflection', 'The centered Gaussian is invariant under the linear isometry p↦−p. The position coordinate is unchanged. Apply the product-map identity to the actual tilted position measure and Gaussian. Mathlib supplies finite-factor instances for tilted and Gaussian measures, so no extra probability or integrability assumption enters this argument.', r'R(x,p)=(x,-p),\qquad R_*\bigl(\pi_y\otimes\gamma\bigr)=\pi_y\otimes\gamma=\nu_y.', '  have hRm', '  refine ⟨hR'),
    step('Construct the canonical involutive L2 isometry', 'Use the measure-preserving pullback J on L2 classes. Its canonical representative equals f∘R almost everywhere. Transport that equality through R and use R(Rz)=z; Lp extensionality proves J²=I. The linear-isometry type itself certifies norm preservation.', r'Jf=f\circ R\quad\nu_y\text{-a.e.},\qquad\|Jf\|_2=\|f\|_2,\qquad J^2=I.', '  refine ⟨hR', '  have hrep'),
    step('Expose the inherited actual expectation representative', 'For a MemLp raw function G, take the existing quotient identity for A_T[G]. Its output toLp representative equals the literal clock expectation almost everywhere. This uses the existing same-Z identity and does not assume a new integral formula.', r'A_T[G](z)=\int G(Z(y,r,z,T,w))\,dP(w)\quad\nu_y\text{-a.e.}', '  have hrep', '  have hsimple'),
    step('Choose simple representatives and match every pullback class', 'Each L2 simple class has a measurable finite-range representative F with its own MemLp witness. Identify [F] with f. Measure preservation transports MemLp to F∘R and transports representative equalities. Consequently Jf=[F∘R], Jg agrees with G∘R, and both operator representatives match their actual expectations.', r'[F]=f,\quad[G]=g,\quad[F\circ R]=Jf,\quad Jg=G\circ R\ \nu_y\text{-a.e.}', '  have hsimple', '    obtain ⟨CF'),
    step('Apply the bounded signed duality to these representatives', 'Finite range supplies finite norm bounds C_F and C_G; replace them by max(C,0) for the inherited nonnegative-bound contract. Apply the actual bounded signed identity to F,G. Substitute the proved representative equalities into the L2 inner-product integrals, obtaining the pairing identity for the two simple classes.', r'\langle f,A_Tg\rangle=\int F\operatorname{op}_TG\,d\nu_y=\int(G\circ R)\operatorname{op}_T(F\circ R)\,d\nu_y=\langle Jg,A_TJf\rangle.', '    obtain ⟨CF', '  have hpair'),
    step('Extend both arguments by L2 density', 'L2 simple classes form a dense subset. Both pairings are continuous jointly in (f,g), since the inner product, A_T and J are continuous. Their equality set is closed and contains every pair of simple classes; the two-variable dense-range induction therefore proves equality for all real L2 classes.', r'\forall f,g\in L^2(\nu_y;\mathbb R),\qquad\langle f,A_Tg\rangle=\langle Jg,A_TJf\rangle.', '  have hpair', '  apply ContinuousLinearMap.ext'),
    step('Identify the Hilbert adjoint', 'By the adjoint defining relation and the full pairing identity, <A_T* f,g>=<Jg,A_TJf>. The isometry and involution move J across the inner product; real symmetry turns this into <JA_TJf,g>. Inner-product extensionality for each f, followed by operator extensionality, gives the claimed equality of the same operators.', r'A_T^*=J A_T J.', '  apply ContinuousLinearMap.ext', '\n#print axioms'),
]

assumptions = ['Finite-dimensional real inner-product Borel E with canonical volume, including rank zero.', 'alpha,beta>=0; alpha>0; alpha<=beta; V is C2; alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2 for every x,v; eta>0; beta*eta<=1.', 'A single global actual process is constructed in the conclusion, with the literal joint measurability, arc/fallback and parameterwise almost-sure initialization contracts; every y,r and finite nonnegative T is included.', 'The universal bounded-observable conclusion ranges over measurable real F,G and finite nonnegative C_F,C_G with pointwise absolute-value bounds. These are test domains, not extra assumptions on the sampler.', 'For the L2 conclusion G is any real function with MemLp G 2 nu_y. For joint Borel dependence G is Borel; every-section L1 additionally uses a finite nonnegative pointwise bound. Operator existence, integrability, output membership and bound1 are conclusions.', 'All actual algorithm, clock and Gibbs phase objects are literal. No supplied Z/kernel/operator, integrability, normalizer, momentum symmetry, restart or Markov premise.']

source = dict(url=audit['source']['url'], edition='arXiv2609.06905v1', anchor=claim['source_anchor'], wording_status='faithful paraphrase', attribution=attribution)
deltas = [dict(source='Appendix A.1 Eq A.3 and its dense-subspace extension.', lean='Full same-process real-L2 adjoint equals canonical momentum-flip conjugation, retaining all107 conclusions.', classification='same', reason='Canonical flip, simple representatives, continuous density and adjoint uniqueness are internal dependencies.'), dict(source='Finite-dimensional Euclidean phase.', lean='Finite real inner-product Borel space including rank zero.', classification='generalization', reason='Canonical volume/Gaussian formulation preserves the source formulas.'), dict(source='Later process and sampler properties.', lean='Fixed-time real-L2 Eq A.3 is closed; semigroup, strong continuity and later sampler results remain open.', classification='unresolved', reason=claim['truth_boundary'])]
item = dict(id=slug, library='pbps', chapter='pbps-01', chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html', title=title, source=source, statement=restatement, assumptions=assumptions, formulae=[dict(label='Actual full real-L2 flip adjoint identity', tex=steps[-1]['formula']), dict(label='All L2 pairings', tex=steps[-2]['formula'])], obligations=[dict(id='l2-flip-duality', label='Full actual real-L2 momentum-flip identity')], bindings=[dict(declaration=decl, cell=cid, role='proof-edge', supports=['l2-flip-duality'], audit_id=aid, boundary=claim['truth_boundary'], assumption_deltas=deltas)])

for key in ['declaration_level', 'statement_seal', 'source_proof_coverage', 'proof_digestion', 'purification']:
    item[key] = copy.deepcopy(cell[key])
unit = dict(kind='theorem', declaration=decl, title=title, sources=[dict(url=source['url'], label=source['anchor'], scope=claim['truth_boundary'])], tests=claim['focused_checks'], assumptions=assumptions, statement=restatement, formula=steps[-1]['formula'], boundary=claim['truth_boundary'], steps=steps, lean_statement=restatement, lean_proof='; '.join(x['title'] for x in steps), helpers=[decl.rsplit('.', 1)[0] + '.actual_l2_flip_statement'], astis_dependencies=parents, mathlib_dependencies=['stdGaussian_map', 'Measure.map_prod_map', 'Lp.compMeasurePreservingₗᵢ', 'Lp.coeFn_compMeasurePreserving', 'Measure.QuasiMeasurePreserving.ae_eq_comp', 'Lp.simpleFunc.toSimpleFunc', 'Lp.simpleFunc.memLp', 'SimpleFunc.exists_forall_norm_le', 'Lp.simpleFunc.denseRange', 'DenseRange.induction_on₂', 'L2.inner_def', 'isClosed_eq', 'LinearIsometry.inner_map_map', 'ContinuousLinearMap.adjoint_inner_left', 'ext_inner_right', 'Lp.ext'])

pp = Path('website/content/publications') / (slug + '.json')
lp = Path('website/content/declaration_lessons') / (slug + '.json')
fresh(pp, dict(schema_version=1, items=[item]))
fresh(lp, dict(schema_version=1, units=[unit]))
pub.inputs.cache_clear()
pub.load.cache_clear()
audit['publication_binding_sha256'] = pub.binding_digest(item, item['bindings'][0], pub.inputs())
audit['publication_context'] = pub.review_context(item, item['bindings'][0], pub.inputs())
start = s.index('theorem actual_l2_flip_duality')
stop = s.index(':= by\n', start)
audit['lean']['statement_representation'] = dict(kind='exact-literal-Prop-expansion', actual_header=s[start:stop], private_definition='def actual_l2_flip_statement' + literal, expanded_header='theorem actual_l2_flip_duality' + statement_lean, source_approved_overlay=(pre / 'root.statement-seal108.json').as_posix(), kernel_header_and_literal_expansion_checked=False)
assert rt.decoder_packet(audit) == packet
save(ap, audit)
fresh(r / 'publication-freeze108.json', dict(status='DRAFT_PENDING_INDEPENDENT_MATH_DECODER_SOURCE_EXPOSITION', module=pin(module), inputs=[pin(p) for p in [pp, lp, ap]], packet=pin(out), canonical_packet_sha256=packet['packet_sha256'], steps=len(steps), conceptual_mirror_audit=cell['conceptual_mirror_audit'], PROVED_LOCAL=False, VERIFIED=False))
pub.check_advance([decl], reviewed=False)
print(json.dumps(dict(packet=pin(out), steps=len(steps), publication_binding_sha256=audit['publication_binding_sha256'])))
