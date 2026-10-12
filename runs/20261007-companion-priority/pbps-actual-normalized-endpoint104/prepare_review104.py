from pathlib import Path
import copy, hashlib, json, sys

root = Path.cwd()
r = Path(__file__).resolve().parent.relative_to(root.resolve())
pre = r.parent / 'pbps-normalized-endpoint-preread104'
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
receipt = r / 'focused104/production1/receipt.json'
check = load(receipt)
assert check['exit_code'] == 0 and check['input_raw_sha256'] == sha(raw)
literal = s.split('private def actual_normalized_endpoint_sector_statement', 1)[1].split('set_option maxHeartbeats', 1)[0].strip()
seal = load(pre / 'root.statement-seal104.json')
assert literal == seal['expanded_literal_Prop'].strip()
binders, body = literal.split(' : Prop :=', 1)
body = body.removeprefix(' by\n  classical\n  exact\n')
statement_lean = binders + ' :\n' + body
old = load(r.parent / 'pbps-actual-weighted-sector102/authored-statement102.json')['statement']
restatement = old.split('Define R(x,p)')[0].replace(' Extend this particular prescribed path to all real times by gamma(s)=Gamma_n(t)(min(max(s,0),T)). This extension agrees with Gamma on[0,T]; no topology on an entire function space is asserted.', '') + """Define R(x,p)=(x,-p), Vy(x)=V(x)+||x-y||^2/(2 eta), and pi_y=volume_E.tilted(-Vy), that is, the measure with density ofReal(exp(-Vy(x))/integral exp(-Vy) dx). Let gamma=stdGaussian(E), the centered identity-covariance Gaussian. Let m_n,T be the comap of Lebesgue measure on R^n by the inclusion of the strict simplex Prefix_n(T), without a factorial factor or an extra normalization.
For every y,r in E, n>=0 and T>=0, let X_n,T=(E times E) times Prefix_n(T), with phase coordinate first. Define the actual terminal phase A(z,t)=Gamma_(y,r,z,n,T,t)(T), endpoint-pair map B(z,t)=(z,A(z,t)), and the density-weighted sector measure sigma_(y,r,n,T)=((pi_y times gamma) times m_n,T).withDensity((z,t) -> rho_(y,r,z,n,T)(t)). This uses precisely the actual product of event rates, intervening survivals and terminal survival defined above. Define its pushforward L_(y,r,n,T)=map B sigma_(y,r,n,T), a measure on (E times E) times (E times E). Define J(z0,zT)=(R(zT),R(z0)).
Then J is measurable and map J L_(y,r,n,T)=L_(y,r,n,T) for every y,r,n,T. Equivalently J is measure preserving from this actual endpoint-pair measure to itself. Phase normalization, joint measurability, simplex sigma-finiteness and the density conversion are established internally; none is a supplied premise. The word normalized describes the initial phase probability pi_y times gamma; it does not assert that each fixed-count sector has total mass one. The statement does not supply a finite-mass or subprobability bound for sigma or L. The result includes n=0, T=0, dimension-zero E, zero reflection normals and zero rates. For n>0,T=0 the strict simplex is empty. Countable sector assembly, signed bilinear identities, process invariance, restart/Markovness, hypocoercivity, implementation error, expected costs and whole-paper/composition conclusions remain separate."""
attribution = 'Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1, Eq. (3.1) and Appendix A.1 fixed-count reversal and Gibbs averaging. Complete attributed mathematical restatement. Explicit normalized sector and endpoint-pair pushforward identities, witness alignment and measurability bookkeeping are ASTIS completion of the source calculation, not a verbatim theorem quotation.'
context = ['Finite-dimensional real inner-product Borel space with canonical volume, including rank zero; genuine second Frechet derivative and real Hilbert gradient.', 'Fin n is zero-based; Fin.cons prepends; Fin.induction constructs a finite sequence; Fin.foldl visits ascending indices. Sum.inl represents a live time/state record; Unit represents a stopped record.', 'Real division by zero is zero; Real.toNNReal is positive part; nonnegative subtraction is truncated. ENNReal.ofReal embeds the positive part in extended nonnegative reals. Interval integrals use real Lebesgue measure.', 'Measure.tilted mu h is mu.withDensity(x -> ofReal(exp(h(x))/integral exp(h) dmu)). stdGaussian E is the centered identity-covariance Gaussian. Measure.comap along a measurable subtype inclusion is the induced subtype measure. Products use the displayed coordinate order.', 'MeasurePreserving f mu nu states Measurable f and Measure.map f mu = nu. withDensity multiplies the base measure by the given extended-nonnegative density. All literal let bindings are definitions, not hypotheses.']

aid = 'ASTIS-RT-20261012-PBPSActualNormalizedEndpointSector'
slug = 'pbps-actual-normalized-endpoint-sector'
title = 'Actual normalized PBPS endpoint-pair sector reversal'
audit = dict(id=aid, state='draft', source=dict(source_id='companion-domain:' + slug, anchor=claim['source_anchor'], url='https://arxiv.org/html/2609.06905v1#A1.E8', original_text=restatement, text_sha256=sha(restatement.encode())), lean=dict(statement=statement_lean.strip(), statement_sha256=sha(statement_lean.strip().encode()), compiled=True, decoder_context=context, declaration=decl, file=file, formalizer='companion_root_20261005', compiler_evidence=receipt.as_posix()), source_review=dict(state='pending'), repairs=[])
ap = Path('research-wiki/semantic-roundtrip/audits') / (aid + '.json')
fresh(ap, audit)
packet = rt.decoder_packet(audit)
out = Path('runs/semantic-roundtrip/anonymous104/input.json')
fresh(out, packet)
fresh(r / 'authored-statement104.json', dict(statement=restatement, attribution=attribution))
cp = Path('research-wiki/frontier-cells') / (cid + '.json')
cell = load(cp)
parents = cell['parents']
fresh(r / 'cell-before-compiled104.json', cell)
cell['evidence']['whole_target_compiled'] = pin(module)
cell['evidence']['focused_checks'] = [receipt.as_posix()]
cell['blocked']['reason'] = 'Full sealed target compiles; independent whole mathematics, blind decoding and source/exposition reviews pending.'
cell['purification']['dead_code_audit'] = 'One public endpoint-pair sector theorem and one literal private proposition; four actual public parents reused, no private dependency calls or duplicate analytic helpers.'
save(cp, cell)

def step(title, text, formula, start, end):
    a, b = s.index(start), s.index(end, s.index(start))
    code = s[a:b]
    return dict(title=title, text=text, formula=formula, lean=code, detail='ASTIS completion of the phase-law proportionality. Exact compiled region; every analytic ingredient is derived from the original assumptions.', lean_source_region=dict(path=file, source_raw_sha256=sha(raw), start_line=s[:a].count('\n') + 1, end_line=s[:b].count('\n'), exact_code_raw_sha256=sha(code.encode())))

steps = [
    step('Align the two event-time reversal witnesses', 'The endpoint reversal and nonnegative weighted substitution each provide a time reversal with the same coordinate formula. Subtype and coordinate extensionality identify them, so one map serves both parents.', r'\vartheta(t)_i=T-t_{n-1-i},\qquad \vartheta_{102}=\vartheta_{97}.', '  obtain ⟨rhoTime', '  rcases h97'),
    step('Construct the measurable endpoint diagram', 'Fix y,r using a measurable embedding into the joint parameter domain. The actual terminal map is measurable. Pair it with the initial phase to obtain B; momentum reversal gives measurable J and Theta. The parent endpoint reversal proves B after Theta equals J after B, including the final flow arc.', r'B(z,t)=(z,A(z,t)),\quad \Theta(z,t)=(R A(z,t),\vartheta t),\quad B\circ\Theta=J\circ B.', '  rcases h97', '  obtain ⟨Z'),
    step('Recover joint measurability of the actual density', 'Apply the finite-count path theorem at the same original analytic assumptions and compose its joint density map with the fixed-parameter embedding. This is the actual rho, including terminal survival.', r'(z,t)\longmapsto \rho_{y,r,z,n,T}(t)\quad\text{is measurable}.', '  obtain ⟨Z', '  have hcons'),
    step('Justify the simplex measure product', 'Each coordinate inequality is measurable. Express the strict time ordering and terminal bound as finite, hence countable, intersections. Mapping the subtype measure back to Euclidean time space gives restricted Lebesgue measure; sigma-finiteness pulls back along the measurable inclusion.', r'\Delta_n(T)=\{0<t_1<\cdots<t_n<T\},\quad \iota_*m_{n,T}=dt|_{\Delta_n(T)},\quad m_{n,T}\text{ is sigma-finite}.', '  have hcons', '  let U'),
    step('Identify the normalized phase density', 'C2 regularity makes the phase Gibbs weight measurable. The existing phase normalization theorem proves that its reciprocal-partition density on phase volume is exactly pi_y times the standard Gaussian. Its positivity and finiteness are supplied by that theorem, not by extra binders here.', r'U_y(x,p)=V_y(x)+\|p\|^2/2,\quad w_y=e^{-U_y},\quad Z_y=\int w_y\,d\ell,\quad \pi_y\otimes\gamma=\ell.\mathrm{withDensity}(Z_y^{-1}w_y).', '  let U', '  have hsigma'),
    step('Rewrite the actual normalized sector measure', 'Use the product-with-density identity, justified by simplex sigma-finiteness. Combine the measurable initial phase density with the actual event density; associativity leaves one constant normalizer multiplying the previous unnormalized weight.', r'W(z,t)=w_y(z)\rho_{y,r,z,n,T}(t),\qquad \sigma=(\ell\otimes m).\mathrm{withDensity}(Z_y^{-1}W).', '  have hsigma', '  have hsector'),
    step('Prove preservation of the full normalized sector', 'Test the pushed-forward measure against every measurable extended-nonnegative F. Rewrite the two density integrals, factor out the constant normalizer and apply the actual unnormalized weighted-sector substitution. Equality of all these integrals proves the full measure identity; no finite integral or cancellation is needed.', r'\int F\circ\Theta\,d\sigma=Z_y^{-1}\int W(F\circ\Theta)\,d(\ell\otimes m)=Z_y^{-1}\int WF\,d(\ell\otimes m)=\int F\,d\sigma,\quad\Theta_*\sigma=\sigma.', '  have hsector', '  refine ⟨hJ'),
    step('Push the reversal to endpoint pairs', 'Apply composition of measurable pushforwards and the endpoint intertwining. This transports the full normalized-sector identity through B to precisely the declared endpoint-pair measure L.', r'J_*L=(J\circ B)_*\sigma=(B\circ\Theta)_*\sigma=B_*(\Theta_*\sigma)=B_*\sigma=L.', '  refine ⟨hJ', '\n#print axioms'),
]
assumptions = ['Finite-dimensional real inner-product Borel E with canonical volume, including dimension zero.', 'alpha,beta>=0; alpha>0; alpha<=beta; V is C2; alpha||v||^2<=D2V(x)[v,v]<=beta||v||^2 for every x,v; eta>0; beta*eta<=1.', 'Every y,r in E, n>=0 and finite nonnegative T. Literal harmonic flow, totalized reflection, nonnegative event rate, strict time simplex, actual recursively reflected states and interpolated endpoint.', 'The actual density is the product of event rates and interval survivals times terminal survival. Initial phase measure is tilted conditional position law times standard Gaussian momentum; no extra normalizer, integrability, measurability, sigma-finiteness or finite-sector-mass hypothesis.']

source = dict(url=audit['source']['url'], edition='arXiv2609.06905v1', anchor=claim['source_anchor'], wording_status='faithful paraphrase', attribution=attribution)
deltas = [dict(source='Fixed-count change of variables followed by initial Gibbs averaging.', lean='Exact measure-preserving flipped swap for the actual normalized endpoint-pair sector.', classification='same', reason='ASTIS states the measure identity underlying the source calculation and derives all measurability and normalization ingredients.'), dict(source='Finite-dimensional Euclidean phase.', lean='Finite real Hilbert Borel space including rank zero.', classification='generalization', reason='Coordinate-free canonical volume and standard Gaussian retain the formulas.'), dict(source='Original six analytic assumptions.', lean='The same six assumptions; no proof ingredient is a supplied premise.', classification='same', reason='The exact presealed proposition is unchanged.'), dict(source='Full stationary averaging and invariant process.', lean='Only a fixed-count normalized endpoint-pair measure identity.', classification='unresolved', reason=claim['truth_boundary'])]

item = dict(id=slug, library='pbps', chapter='pbps-01', chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html', title=title, source=source, statement=restatement, assumptions=assumptions, formulae=[dict(label='Actual normalized sector', tex=steps[5]['formula']), dict(label='Endpoint-pair reversal', tex=steps[-1]['formula'])], obligations=[dict(id='normalized-endpoint-sector', label='Actual normalized endpoint-pair sector reversal'), dict(id='weighted-invariance', label='Normalized averaging and invariant process law')], bindings=[dict(declaration=decl, cell=cid, role='proof-edge', supports=['normalized-endpoint-sector'], audit_id=aid, boundary=claim['truth_boundary'], assumption_deltas=deltas)])
for key in ['declaration_level', 'statement_seal', 'source_proof_coverage', 'proof_digestion', 'purification']:
    item[key] = copy.deepcopy(cell[key])
unit = dict(kind='theorem', declaration=decl, title=title, sources=[dict(url=source['url'], label=source['anchor'], scope=claim['truth_boundary'])], tests=claim['focused_checks'], assumptions=assumptions, statement=restatement, formula=steps[-1]['formula'], boundary=claim['truth_boundary'], steps=steps, lean_statement=restatement, lean_proof='; '.join(x['title'] for x in steps), helpers=[decl.rsplit('.', 1)[0] + '.actual_normalized_endpoint_sector_statement'], astis_dependencies=parents, mathlib_dependencies=['MeasurableSet.iInter', 'Set.ofPred_forall', 'Set.ofPred_and', 'map_comap_subtype_coe', 'SigmaFinite.of_map', 'prod_withDensity_left', 'withDensity_mul', 'Measure.ext_of_lintegral', 'lintegral_map', 'lintegral_withDensity_eq_lintegral_mul', 'lintegral_const_mul', 'Measure.map_map'])
pp = Path('website/content/publications') / (slug + '.json')
lp = Path('website/content/declaration_lessons') / (slug + '.json')
fresh(pp, dict(schema_version=1, items=[item]))
fresh(lp, dict(schema_version=1, units=[unit]))
pub.inputs.cache_clear()
pub.load.cache_clear()
audit['publication_binding_sha256'] = pub.binding_digest(item, item['bindings'][0], pub.inputs())
audit['publication_context'] = pub.review_context(item, item['bindings'][0], pub.inputs())
start = s.index('theorem actual_normalized_endpoint_sector_reversal')
stop = s.index(':= by\n', start)
audit['lean']['statement_representation'] = dict(kind='exact-literal-Prop-expansion', actual_header=s[start:stop], private_definition='def actual_normalized_endpoint_sector_statement' + literal, expanded_header='theorem actual_normalized_endpoint_sector_reversal' + statement_lean, source_approved_overlay=(pre / 'root.statement-seal104.json').as_posix(), kernel_header_and_literal_expansion_checked=False)
assert rt.decoder_packet(audit) == packet
save(ap, audit)
fresh(r / 'publication-freeze104.json', dict(status='DRAFT_PENDING_INDEPENDENT_MATH_DECODER_SOURCE_EXPOSITION', module=pin(module), inputs=[pin(p) for p in [pp, lp, ap]], packet=pin(out), canonical_packet_sha256=packet['packet_sha256'], steps=len(steps), conceptual_mirror_audit=cell['conceptual_mirror_audit'], PROVED_LOCAL=False, VERIFIED=False))
pub.check_advance([decl], reviewed=False)
print(json.dumps(dict(packet=pin(out), steps=len(steps), publication_binding_sha256=audit['publication_binding_sha256'])))
