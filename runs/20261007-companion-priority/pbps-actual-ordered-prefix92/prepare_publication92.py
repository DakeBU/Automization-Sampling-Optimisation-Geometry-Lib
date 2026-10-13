from pathlib import Path
import json, hashlib, copy, sys, datetime

ROOT=Path(__file__).resolve().parents[3]
RUN=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
import astis_publication as pub
import astis_semantic_roundtrip as rt
read=lambda p:json.loads(p.read_text(encoding='utf8'))
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def fresh(p,x):
    assert not p.exists(),p
    save(p,x)
def pin(p): return dict(path=p.relative_to(ROOT).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)

claim=read(RUN/'claim.json');decl=claim['target_declarations'][0];file=claim['proposed_files'][0];cid=claim['frontier_cell']
module=ROOT/file;s=module.read_text(encoding='utf8');raw=module.read_bytes()
receipt=RUN/'focused/production1-sealed-law/receipt.json'
r=read(receipt);assert r['exit_code']==0 and r['source']['raw_sha256']==sha(raw)
assert sha(raw)=='46c637205d601786472e789bf4706a77b18ea6dad423ab33d1ac39491e71e111'
cp=ROOT/'research-wiki/frontier-cells'/f'{cid}.json';cell=read(cp)
fresh(RUN/'frontier-before-publication92.json',cell)
parents=[
 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime.actual_absolute_next_event_time_law',
 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws',
 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_laws',
 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock.actual_integrated_hazard_clock_laws',
 'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws']
cell['parents']=parents
cell['reuse_plan']['reused_declarations']=parents
cell['proof_digestion']['existing_substrate']=parents
cell['reuse_plan']['decision_reason']='The actual91 localized one-step law drives induction; actual flow/reflection-rate/hazard producers give joint Borel geometry; only probability normalization is reused from the canonical exponential product. Fixed Mathlib supplies finite-coordinate volume preservation, nonnegative Tonelli, measurable extension, comap and measure extensionality.'
cell['purification']['dead_code_audit']='Full source compiles; independent integration and postmerge dead-code/purification review remain pending.'
cell['blocked']['reason']='The exact sealed law now compiles. Whole-module independent math, anonymous decoding, source/exposition review and publication admission are pending.'
cell['evidence']['focused_checks']=[receipt.relative_to(ROOT).as_posix()]
save(cp,cell)
authored=read(RUN/'authored-statement92.json');statement=authored['statement']
assumptions=[
 'Finite-dimensional real inner-product Borel space E, including the explicitly disclosed rank-zero extension.',
 'α,β≥0; exactly six analytic assumptions: α>0, α≤β, V is C², α‖v‖²≤D²V(x)[v,v]≤β‖v‖² for all x,v, η>0, βη≤1.',
 'Every deterministic n≥0, finite T≥0 and y,r,z₀ are universally quantified. The exponential product P, clipped coordinates, stopped recursion, complete histories, simplex and reference measure are literal definitions.',
 'Tests F are arbitrary Borel Hist_n→[0,∞], with no boundedness, integrability or positive-event-mass requirement.',
 'All joint measurability, pointwise reconstruction, nonnegativity, density law and mass bounds are proved conclusions; no law, independence, normalization or density provider is an additional public premise.'
]
formulae=[
 r'\Delta_n(T)=\{0<s_1<\cdots<s_n<T\},\quad s_0=0,\quad z_i=S_r\Phi_{s_i-s_{i-1}}z_{i-1},\quad K_n(s)_i=\operatorname{live}(s_i,z_i).',
 r'q_n(s)=\prod_{i=1}^n\lambda_r(\Phi_{s_i-s_{i-1}}z_{i-1})\exp[-\Lambda_{z_{i-1}}(s_i-s_{i-1})].',
 r'B_{n+1}(T)=B_n(T)\cap\{R_n,R_{n+1}\text{ live},\ s_n<U_{n+1}<T\}.',
 r'\int_{B_{n+1}}F(H_{n+1})\,dP=\int_{B_n}J_F(H_n)\,dP,\quad J_F(h)=\int_{\mathbb R}F(A_{\rm abs}(h,u))D_T(h,u)\,du.',
 r'\int_{\Delta_{n+1}(T)}g(s,u)\,d(s,u)=\int_{\Delta_n(T)}\int_{s_n}^Tg(s,u)\,du\,ds.',
 r'\int_{B_n(T)}F(H_n)\,dP=\int_{\Delta_n(T)}F(K_n(s))q_n(s)\,dm_n(s).',
 r'(H_n)_*(P|_{B_n(T)})=(K_n)_*(q_nm_n),\qquad\int q_n\,dm_n=P(B_n(T))\le1.'
]
def step(title,text,formula,start,end):
    a=s.index(start);b=s.index(end,a);code=s[a:b]
    return dict(title=title,text=text,formula=formula,lean=code,
      detail='Exact compiled region. Private interface premises are discharged by the final proof, not added to the public theorem.',
      lean_source_region=dict(path=file,source_raw_sha256=sha(raw),start_line=s[:a].count('\n')+1,end_line=s[:b].count('\n'),exact_code_raw_sha256=sha(code.encode())))
steps=[
 step('Build the Borel geometry and a nonnegative density',
  'The simplex is a finite intersection of strict inequalities between coordinate maps. Reading a live time and returning zero on the stopped tag is Borel; the live tag is a measurable summand. Thus the complete-history guard is Borel. Reuse the actual harmonic-flow, reflection/rate and integrated-hazard theorems. Finite induction through the bounce-after-flow update makes every prescribed state jointly Borel in y,r,z₀ and time coordinates. Pair with the nonnegative time coordinates to obtain K; finite products and exp/ofReal give q. Each rate is √η times a nonnegative positive part and each exponential is positive, so every factor and the real finite product are nonnegative.',
  formulae[0]+r'\qquad K_n,q_n\text{ jointly Borel},\quad q_n^{\rm real}\ge0.',
  'private theorem measurable_cons_zero','private theorem actual_prefix_identification'),
 step('Recover the complete prescribed history from each actual strict prefix',
  'Take w in B_n and read its postinitial times into s. The actual zeroth record is live(0,z₀); the guard supplies strict increase and s_i<T, hence s lies in the simplex. Induct over records. A live successor excludes an infinite clock by the literal stopped recursion. Its time is the previous live time plus the finite wait, so that wait equals s_i−s_(i−1). The recursive state is therefore exactly S_rΦ_(s_i−s_(i−1))z_(i−1). Nonnegative clocks make the toNNReal representatives agree. Every time, state and tag is preserved, proving H_n(w)=K_n(s) pointwise, rather than merely identifying a final marginal.',
  r'w\in B_n(T)\Longrightarrow \exists s\in\Delta_n(T):\ s=\operatorname{obs}_n(w),\ H_n(w)=K_n(s).',
  'private theorem actual_prefix_identification','private theorem actual_prefix_base_integral'),
 step('Start the probability induction at zero events',
  'For n=0 the complete history is the single initial live record. The guard and zero-dimensional simplex are universal, even when T=0. The empty density product equals one. The subtype comap has mass one: push its inclusion forward to restricted zero-dimensional product volume and use the empty product of masses. The canonical exponential product is a probability measure. Both sides of the test identity are therefore F(live(0,z₀)), including F=∞. No positive horizon or finite test assumption is introduced.',
  r'B_0(T)=\Omega,\quad m_0(\Delta_0(T))=1,\quad q_0=1,\quad\int_{B_0}F(H_0)dP=\int F(K_0)q_0dm_0.',
  'private theorem actual_prefix_base_integral','private def guard'),
 step('Split exactly the next strict-prefix event',
  'A length n+2 history is the old length n+1 history followed by its last record. Strict monotonicity splits into old strict monotonicity and one final strict comparison; the cap splits into the old cap and the final time below T. All-live status splits in the same way. The old last record is live because it belongs to the old guard. Applying this finite-tuple identity to the literal record sequence gives the displayed event equality on every raw input. Stopped or zero-wait transitions cannot enter the strict next-event part; no almost-everywhere count interpretation is used.',
  formulae[2],'private def guard','private theorem actual_prefix_step_integral'),
 step('Use the actual one-step probability law inside the old guard',
  'Apply the previously verified absolute-event-time theorem at constant horizon T and its full next-history test (h_next,u)↦F(h_next). It produces the Borel inner function J_F. Localize its unnormalized law to A_n(T), the old Borel guard. The event equality just proved changes its left side to B_(n+1)(T). Pull the right integral against the old history pushforward back to canonical P. This gives the actual recurrence, using the law of the real exponential-clock recursion. No conditional density or recurrence is assumed as a new source premise.',
  formulae[3],'private theorem actual_prefix_step_integral','private theorem strictMono_snoc'),
 step('Disintegrate the ordered simplex with its actual subtype measure',
  'Appending u to s belongs to Δ_(n+1)(T) exactly when s lies in Δ_n(T) and s_n<u<T. Fixed Mathlib proves that inserting the last real coordinate preserves product Lebesgue volume. Pull back the simplex indicator and apply nonnegative Tonelli to obtain the iterated integral. For a Borel function defined only on the simplex subtype, extend it measurably to the ambient finite product using the measurable inclusion. It agrees on the subtype; all integrals are restricted there, so outside values have no effect. The comap integral formula transfers the resulting equality back to the dependent simplex and interval subtypes. The argument includes empty domains and infinite integrals.',
  formulae[4],'private theorem strictMono_snoc','private def state'),
 step('Identify the appended history and factor the density',
  'Finite induction shows that appending a last time leaves every earlier state unchanged and adds state S_rΦ_(u−s_n)z_n. Since s_n≥0 and u>s_n, toNNReal(s_n)+toNNReal(u−s_n)=toNNReal(u); therefore absolute append equals K_(n+1)(s,u) as a complete history. Split the finite product at its last index to get q_(n+1)=q_n times the next pre-bounce rate and elapsed survival. The real product is already nonnegative, so ofReal preserves this multiplication. These private algebraic inputs are instantiated by the actual flow, reflection, rate and hazard in the induction.',
  r'A_{\rm abs}(K_n(s),u)=K_{n+1}(s,u),\qquad q_{n+1}(s,u)=q_n(s)\rho(z_n,u-s_n).',
  'private def state','private theorem actual_prefix_all_integrals'),
 step('Close the all-n probability induction for every nonnegative test',
  'Assume the test identity at n. Apply it to the Borel J_F produced by the actual recurrence. The resulting integrand is J_F(K_n(s))q_n(s). At K_n(s), the next-event density is the indicator of s_n<u<T times ρ(z_n,u−s_n). Move the finite nonnegative scalar q_n(s)=ofReal(qReal_n(s)) inside the nonnegative integral, restrict to that open interval, and use the exact append and product identities. The result is F(K_(n+1)(s,u))q_(n+1)(s,u). The subtype Tonelli equality turns the two integrals into the integral over Δ_(n+1). Joint Borel K and q ensure the composed test is Borel. Together with the zero-event base this proves the formula for every n, without boundedness or integrability.',
  formulae[5],'private theorem actual_prefix_all_integrals','private theorem law_and_mass_of_all_tests'),
 step('Recover the measure equality and the exact missing mass',
  'Compare both pushforward measures against every Borel ENNReal test. The map-integral formula and the withDensity formula turn their integrals into the identity just proved; measure extensionality gives equality. Taking F=1 gives ∫q_n dm_n=P(B_n(T)), and the canonical probability normalization gives P(B_n(T))≤1. This mass is not renormalized. The private all-test input is supplied by the actual all-n induction, not by a public hypothesis.',
  formulae[6],'private theorem law_and_mass_of_all_tests','def actual_ordered_prefix_statement'),
 step('Assemble the sealed statement and retain its source boundary',
  'Keep the literal definitions and the six original analytic hypotheses. Assemble the joint Borel conclusions, derive actual H_n from the existing next-event theorem and obs_n by Borel coordinate projection, use the pointwise reconstruction, and pass the proved all-n tests to measure extensionality. The result is the complete strict-prefix statement displayed above. A final no-further-event survival term, exact-count/path identification and summing full path terms are separate remaining source steps; this theorem makes no invariance, mixing or expected-cost claim.',
  formulae[6],'theorem actual_ordered_prefix_law','\nend\n')
]
slug='pbps-actual-ordered-prefix';aid='ASTIS-RT-20261011-PBPSActualOrderedPrefix';title='Actual PBPS ordered finite-prefix law'
source=dict(url='https://arxiv.org/html/2609.06905v1#A1.E7',edition='arXiv2609.06905v1',anchor=claim['source_anchor'],wording_status='faithful paraphrase',attribution=authored['attribution'])
deltas=[
 dict(source='The source constructs actual event times from independent exponential clocks under its original analytic hypotheses.',lean='Literal stopped recursion and canonical exponential product with the same six analytic hypotheses.',classification='source-implicit',reason='Tagged Borel histories and raw-coordinate totalizations are made explicit; none are new public providers.'),
 dict(source='The ordered-time expansion around A.7 implicitly iterates finite event densities.',lean='Exact strict first-n complete-history prefix law, its subtype Lebesgue density and all nonnegative extended tests.',classification='source-implicit',reason='This is an attributed ASTIS completion of that ingredient; rank-zero space and ENNReal-test extensions are disclosed.'),
 dict(source='Full A.7 includes the remaining path/count and final-survival assembly.',lean='The prefix density contains only the n elapsed rate/survival factors; it is neither an exact-n raw count event nor full A7.',classification='unresolved',reason='Terminal survival, endpoint/count identification, whole path equality and summation remain separate dependencies.')]
item=dict(id=slug,library='pbps',chapter='pbps-01',chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html',title=title,source=source,statement=statement,assumptions=assumptions,
 formulae=[dict(label='Ordered-prefix formula '+str(i+1),tex=f) for i,f in enumerate(formulae)],
 obligations=[dict(id='actual-ordered-prefix',label='Actual strict finite-prefix history law'),dict(id='full-ordered-path',label='Terminal survival, path/count identification and full A7')],
 bindings=[dict(declaration=decl,cell=cid,role='proof-edge',supports=['actual-ordered-prefix'],audit_id=aid,boundary=claim['truth_boundary'],assumption_deltas=deltas)])
for key in ['declaration_level','statement_seal','source_proof_coverage','proof_digestion','purification']:item[key]=copy.deepcopy(cell[key])
unit=dict(kind='theorem',declaration=decl,title=title,sources=[dict(url=source['url'],label=source['anchor'],scope=claim['truth_boundary'])],tests=claim['focused_checks'],assumptions=assumptions,statement=statement,formula=formulae[5],boundary=claim['truth_boundary'],steps=steps,lean_statement=statement,lean_proof='; '.join(x['title'] for x in steps),helpers=[decl.rsplit('.',1)[0]+'.actual_ordered_prefix_statement'],astis_dependencies=parents,
 mathlib_dependencies=['volume_preserving_piFinSuccAbove','MeasurableEmbedding.exists_measurable_extend','lintegral_subtype_comap','lintegral_prod_symm','setLIntegral_map','Measure.ext_of_lintegral','lintegral_withDensity_eq_lintegral_mul','Fin.prod_univ_castSucc'])
pp=ROOT/'website/content/publications'/f'{slug}.json';lp=ROOT/'website/content/declaration_lessons'/f'{slug}.json'
fresh(pp,dict(schema_version=1,items=[item]));fresh(lp,dict(schema_version=1,units=[unit]))
ap=ROOT/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json';audit=read(ap)
pub.inputs.cache_clear();pub.load.cache_clear()
audit['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs())
audit['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs())
literal=s.split('def actual_ordered_prefix_statement',1)[1].split('\n\nset_option',1)[0]
audit['lean']['statement_representation']=dict(kind='exact-literal-Prop-expansion',actual_header=s[s.index('theorem actual_ordered_prefix_law'):s.index(':= by\n',s.index('theorem actual_ordered_prefix_law'))],private_definition='def actual_ordered_prefix_statement'+literal,expanded_header='theorem actual_ordered_prefix_law'+audit['lean']['statement'],source_approved_overlay=(RUN/'root.statement-seal92.json').relative_to(ROOT).as_posix(),kernel_header_and_literal_expansion_checked=False)
assert rt.decoder_packet(audit)==read(ROOT/'runs/semantic-roundtrip/anonymous92/input.json')
save(ap,audit)
fresh(RUN/'publication-freeze92.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='DRAFT_PENDING_WHOLE_MATH_SOURCE_EXPOSITION',module=pin(module),inputs=[pin(p) for p in [pp,lp,ap]],steps=len(steps),conceptual_mirror_audit=dict(status='none-found',reason='This proof instantiates the existing finite-history density/Tonelli mechanism; no new independently supportable cross-domain transport or conceptual mirror was identified.'),PROVED_LOCAL=False,VERIFIED=False))
pub.check_advance([decl],reviewed=False)
print('Draft publication: ten source-bound mathematical steps with exact adjacent Lean; canonical anonymous packet unchanged.')
