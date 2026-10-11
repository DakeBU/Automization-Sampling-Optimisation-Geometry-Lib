from pathlib import Path
import copy, hashlib, json, sys

root = Path.cwd()
r = Path(__file__).resolve().parent.relative_to(root.resolve())
pre = r.parent / 'pbps-phase-normalization-preread103'
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
receipt = r / 'focused103/production1/receipt.json'
check = load(receipt)
assert check['exit_code'] == 0 and check['input_raw_sha256'] == sha(raw)
literal = s.split('private def actual_phase_normalization_statement', 1)[1].split('/-- Positive finite', 1)[0].strip()
seal = load(pre / 'root.statement-seal103.json')
assert literal == seal['expanded_literal_Prop'].strip()
binders, body = literal.split(' : Prop :=', 1)
body = body.removeprefix(' by\n  classical\n  exact\n')
statement_lean = binders + ' :\n' + body
restatement = '''Let E be a finite-dimensional real inner-product space equipped with its Borel sigma algebra and canonical Lebesgue measure, including dimension d=0. Let V:E->R be C2. Let alpha,beta>=0 with alpha>0 and alpha<=beta, and assume alpha||v||^2 <= D2 V(x)[v,v] <= beta||v||^2 for every x,v in E, where D2 is the genuine second Frechet derivative. Let eta>0 and beta*eta<=1.
For each y in E define Vy(x)=V(x)+||x-y||^2/(2 eta), U_y(x,p)=Vy(x)+||p||^2/2, w_y=exp(-U_y), and ell=volume_E times volume_E in position-momentum order. Define the real position partition Zx(y)=integral exp(-Vy(x)) dx, C_E=(sqrt(2 pi))^d using the natural-number power, and the extended nonnegative phase partition Zphase(y)=integral ofReal(w_y(z)) d ell(z). Let pi_y=volume_E.tilted(-Vy), meaning volume_E.withDensity(x -> ofReal(exp(-Vy(x))/Zx(y))). Let nu_y=ell.withDensity(z -> Zphase(y)^(-1)*ofReal(w_y(z))) and let gamma be the centered Gaussian on E with identity covariance.
Then for every y, all seven assertions hold: exp(-Vy) is integrable; Zx(y)>0; Zphase(y)=ofReal(Zx(y)*C_E); Zphase(y)>0; Zphase(y)<infinity; nu_y is a probability measure; and nu_y=pi_y times gamma exactly as measures on E times E. The real and extended-real integrals are therefore finite before normalization is justified. This identifies the actual phase law rather than a supplied density or normalizer. In dimension zero C_E=1 and the normalized measure is the unit atom on the singleton phase space. No minimizer, critical point, Gaussian envelope, measurability, integrability or finite-mass premise is added. Upper curvature, alpha<=beta and beta*eta<=1 remain as original source assumptions even though this analytic normalization proof needs only the lower curvature, C2 and eta>0. This result does not assert a process law, stationary averaging, countable sector assembly, invariance, a Markov property, hypocoercivity, simulation error, expected oracle cost or whole-paper/composition completion.'''
attribution = 'Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1, conditional potential and Eq. (3.1). Complete attributed mathematical restatement of the phase-law identification. Explicit positive finite partition and exact representative proof are ASTIS completion of source proportionality notation, not a verbatim quotation or a new claimed theorem of the authors.'
context = ['Finite-dimensional real inner-product space with its Borel sigma algebra and canonical volume; dimension zero is included.', 'The second Frechet derivative is evaluated twice on the direction v. NNReal parameters are coerced to real numbers in inequalities.', 'ENNReal is the extended nonnegative real line; ofReal embeds the positive part. Real division by zero is totalized, but no convention by itself establishes normalization.', 'Measure.tilted mu h means mu.withDensity(x -> ofReal(exp(h(x))/integral exp(h) dmu)). stdGaussian E is the centered Gaussian with identity covariance. Product measures place the first coordinate first.']
aid = 'ASTIS-RT-20261012-PBPSActualPhaseNormalization'
slug = 'pbps-actual-phase-normalization'
title = 'Actual PBPS phase Gibbs normalization'
audit = dict(id=aid, state='draft', source=dict(source_id='companion-domain:' + slug, anchor=claim['source_anchor'], url='https://arxiv.org/html/2609.06905v1#S3.E1', original_text=restatement, text_sha256=sha(restatement.encode())), lean=dict(statement=statement_lean.strip(), statement_sha256=sha(statement_lean.strip().encode()), compiled=True, decoder_context=context, declaration=decl, file=file, formalizer='companion_root_20261005', compiler_evidence=receipt.as_posix()), source_review=dict(state='pending'), repairs=[])
ap = Path('research-wiki/semantic-roundtrip/audits') / (aid + '.json')
fresh(ap, audit)
packet = rt.decoder_packet(audit)
out = Path('runs/semantic-roundtrip/anonymous103/input.json')
fresh(out, packet)
fresh(r / 'authored-statement103.json', dict(statement=restatement, attribution=attribution))
cp = Path('research-wiki/frontier-cells') / (cid + '.json')
cell = load(cp)
parents = cell['parents']
fresh(r / 'cell-before-compiled103.json', cell)
cell['evidence']['whole_target_compiled'] = pin(module)
cell['evidence']['focused_checks'] = [receipt.as_posix()]
cell['blocked']['reason'] = 'Full sealed target compiles; independent whole mathematics, blind decoding and source/exposition reviews pending.'
cell['purification']['dead_code_audit'] = 'One public actual normalization theorem and one literal private proposition; canonical public analytic leaves reused, no private dependency calls.'
save(cp, cell)

def step(title, text, formula, start, end):
    a, b = s.index(start), s.index(end, s.index(start))
    code = s[a:b]
    return dict(title=title, text=text, formula=formula, lean=code, detail='ASTIS completion of the phase-law proportionality. Exact compiled region; every analytic ingredient is derived from the original assumptions.', lean_source_region=dict(path=file, source_raw_sha256=sha(raw), start_line=s[:a].count('\n') + 1, end_line=s[:b].count('\n'), exact_code_raw_sha256=sha(code.encode())))

steps = [
    step('Obtain the integrable Gibbs tail', 'The genuine Hessian lower bound and C2 regularity imply alpha-strong convexity. The existing positive-modulus Gibbs integrability theorem uses a quadratic envelope and requires no supplied minimizing or critical point.', r'D^2V\succeq\alpha I,\quad\alpha>0\quad\Longrightarrow\quad e^{-V}\in L^1(dx).', '  have hsc', '  have hVy'),
    step('Control every conditional position partition', 'For each y, eta>0 makes the proximal quadratic nonnegative, hence 0<exp(-Vy)<=exp(-V). Continuity yields measurability; domination proves integrability. Strict positivity of the exponential and nonzero canonical volume then give Zx>0, including dimension zero.', r'V_y\ge V,\qquad 0<e^{-V_y}\le e^{-V},\qquad 0<Z_x(y)=\int e^{-V_y(x)}\,dx<\infty.', '  have hVy', '  have hC'),
    step('Evaluate the Gaussian momentum factor', 'Apply the canonical Gaussian integral with coefficient 1/2. Convert its real power to the natural-number power of sqrt(2 pi). The resulting positive factor is C_E; no variance eta appears in momentum.', r'\int e^{-\|p\|^2/2}\,dp=(2\pi)^{d/2}=(\sqrt{2\pi})^d=C_E>0.', '  have hC', '  have hw'),
    step('Factor the actual phase partition', 'The target energy is additive in position and momentum. Exponentiation factors its weight, and nonnegative product integration separates the two factors in position-first order. Integrability of the position factor permits the real-to-ENNReal integral conversion.', r'e^{-U_y(x,p)}=e^{-V_y(x)}e^{-\|p\|^2/2},\qquad Z_{\rm phase}(y)=\operatorname{ofReal}(Z_x(y)C_E).', '  have hw', '  have hpos'),
    step('Normalize only after positivity and finiteness', 'Both real factors are positive, and ofReal of a real number is finite. The existing Gibbs withDensity theorem now proves that the reciprocal-partition density has total mass one. No finite-mass premise was supplied.', r'0<Z_{\rm phase}(y)<\infty,\qquad \nu_y=\ell\mathbin{.}\mathrm{withDensity}(Z_{\rm phase}(y)^{-1}e^{-U_y}),\quad\nu_y(E\times E)=1.', '  have hpos', '  have hgamma'),
    step('Identify standard Gaussian momentum', 'Specialize the existing isotropic Gaussian density theorem to variance one. Scaling by sqrt(1) is the identity map, so the Gaussian density is C_E inverse times exp(-||p||^2/2). This also covers d=0.', r'\gamma=dp\mathbin{.}\mathrm{withDensity}\bigl(\operatorname{ofReal}(C_E^{-1}e^{-\|p\|^2/2})\bigr).', '  have hgamma', '  rw [hgamma'),
    step('Match the normalized product density', 'Expand the tilted position measure and use product-withDensity for the two measurable densities. Substitute the exact phase partition and factorized energy. Positivity and finite ofReal factors justify division and inversion; commutativity then identifies the densities pointwise and hence the measures.', r'\frac{e^{-U_y(x,p)}}{Z_x(y)C_E}=\frac{e^{-V_y(x)}}{Z_x(y)}\frac{e^{-\|p\|^2/2}}{C_E},\qquad\nu_y=\pi_y\otimes\gamma.', '  rw [hgamma', '\n#print axioms'),
]
assumptions = ['Finite-dimensional real inner-product Borel E with canonical volume, including dimension zero.', 'alpha,beta>=0; alpha>0; alpha<=beta; V is C2; alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2 for every x,v.', 'eta>0 and beta*eta<=1. All conclusions hold for every y in E.', 'Literal conditional and phase energies, real Zx, ENNReal Zphase, C_E=(sqrt(2 pi))^d, tilted position law and standard Gaussian momentum. No extra integrability, normalizer, minimizing point or regularity premise.']
source = dict(url=audit['source']['url'], edition='arXiv2609.06905v1', anchor=claim['source_anchor'], wording_status='faithful paraphrase', attribution=attribution)
deltas = [dict(source='Eq3.1 defines a proportional phase density and product probability law.', lean='Proves the actual partitions positive finite and the exact equality of canonical measures.', classification='same', reason='ASTIS expands source-implicit normalization; no new source hypothesis.'), dict(source='Euclidean finite-dimensional phase.', lean='Finite real Hilbert Borel formulation including rank zero.', classification='generalization', reason='Coordinate-free canonical volume and Gaussian representation preserve the formula, including natural zeroth power.'), dict(source='Original sampler assumptions.', lean='All six retained, including unused upper/step-size bounds.', classification='same', reason='No stronger assumption added.'), dict(source='Stationary averaging and process invariance.', lean='Only phase normalization and product-law identification.', classification='unresolved', reason=claim['truth_boundary'])]
item = dict(id=slug, library='pbps', chapter='pbps-01', chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html', title=title, source=source, statement=restatement, assumptions=assumptions, formulae=[dict(label='Actual phase partition', tex=steps[3]['formula']), dict(label='Exact phase probability law', tex=steps[-1]['formula'])], obligations=[dict(id='phase-gibbs-normalization', label='Positive finite actual phase partition and product-law identification'), dict(id='weighted-invariance', label='Normalized averaging and invariant process law')], bindings=[dict(declaration=decl, cell=cid, role='proof-edge', supports=['phase-gibbs-normalization'], audit_id=aid, boundary=claim['truth_boundary'], assumption_deltas=deltas)])
for key in ['declaration_level', 'statement_seal', 'source_proof_coverage', 'proof_digestion', 'purification']:
    item[key] = copy.deepcopy(cell[key])
unit = dict(kind='theorem', declaration=decl, title=title, sources=[dict(url=source['url'], label=source['anchor'], scope=claim['truth_boundary'])], tests=claim['focused_checks'], assumptions=assumptions, statement=restatement, formula=steps[-1]['formula'], boundary=claim['truth_boundary'], steps=steps, lean_statement=restatement, lean_proof='; '.join(x['title'] for x in steps), helpers=[decl.rsplit('.', 1)[0] + '.actual_phase_normalization_statement'], astis_dependencies=parents, mathlib_dependencies=['Integrable.mono\u0027', 'integral_exp_pos', 'lintegral_prod_mul', 'ofReal_integral_eq_lintegral_ofReal', 'Real.rpow_mul_natCast', 'Measure.tilted', 'prod_withDensity', 'withDensity_congr_ae', 'ENNReal.mul_inv'])
pp = Path('website/content/publications') / (slug + '.json')
lp = Path('website/content/declaration_lessons') / (slug + '.json')
fresh(pp, dict(schema_version=1, items=[item]))
fresh(lp, dict(schema_version=1, units=[unit]))
pub.inputs.cache_clear()
pub.load.cache_clear()
audit['publication_binding_sha256'] = pub.binding_digest(item, item['bindings'][0], pub.inputs())
audit['publication_context'] = pub.review_context(item, item['bindings'][0], pub.inputs())
start = s.index('theorem actual_phase_gibbs_normalization')
stop = s.index(':= by\n', start)
audit['lean']['statement_representation'] = dict(kind='exact-literal-Prop-expansion', actual_header=s[start:stop], private_definition='def actual_phase_normalization_statement' + literal, expanded_header='theorem actual_phase_gibbs_normalization' + statement_lean, source_approved_overlay=(pre / 'root.statement-seal103.json').as_posix(), kernel_header_and_literal_expansion_checked=False)
assert rt.decoder_packet(audit) == packet
save(ap, audit)
fresh(r / 'publication-freeze103.json', dict(status='DRAFT_PENDING_INDEPENDENT_MATH_DECODER_SOURCE_EXPOSITION', module=pin(module), inputs=[pin(p) for p in [pp, lp, ap]], packet=pin(out), canonical_packet_sha256=packet['packet_sha256'], steps=len(steps), conceptual_mirror_audit=cell['conceptual_mirror_audit'], PROVED_LOCAL=False, VERIFIED=False))
pub.check_advance([decl], reviewed=False)
print(json.dumps(dict(packet=pin(out), steps=len(steps), publication_binding_sha256=audit['publication_binding_sha256'])))
