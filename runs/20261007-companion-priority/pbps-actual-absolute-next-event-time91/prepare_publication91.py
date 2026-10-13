from pathlib import Path
import copy, datetime, hashlib, json, sys

ROOT=Path('E:/Samplinglib')
RUN=Path(__file__).parent
sys.path.insert(0,str(ROOT/'tools'))
import astis_publication as pub
import astis_semantic_roundtrip as rt
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def fresh(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
    return dict(path=p.relative_to(ROOT).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)

claim=load(RUN/'claim.json')
decl=claim['target_declarations'][0];file=claim['proposed_files'][0];cid=claim['frontier_cell']
module=ROOT/file;raw=module.read_bytes();s=raw.decode('utf-8')
assert sha(raw)=='8e28fb218233358a9b1c7a2b41689071ca3c410faa58a0883a0885243d588ab2'
seal=load(RUN/'root.statement-seal91.json')
literal=s.split('private def ',1)[1].split('\n\nset_option',1)[0]
assert literal.strip()==seal['expanded_literal_Prop'].strip()
receipt=RUN/'focused/production7-absolute-joint-law/receipt.json'
assert load(receipt)['exit_code']==0 and load(receipt)['module_raw_sha256']==sha(raw)
cell=load(ROOT/'research-wiki/frontier-cells'/f'{cid}.json')
standing=load(ROOT/'website/content/publications/pbps-actual-finite-history-tail-law.json')['items'][0]['statement'].split('For every deterministic n≥0 define',1)[0]
statement=standing+(
    'For every deterministic n≥0 define Rec=([0,∞)×(E×E))⊕{stopped}, Hist_n=Rec^(Fin(n+1)), '
    'H_n(w)=(R_j(ε(w)))_(0≤j≤n), H_next=H_(n+1), and μ_n=(H_n)_*P. '
    'Let readTime(live(T,z))=T and readTime(stopped)=0; a(h)=readTime(h_n), and U(w)=readTime(H_next(w)_(n+1)). '
    'Thus U reads the actual next record, rather than being defined as a shifted waiting time. '
    'Set W(live(T,z),e)=τ_z(max(e,0)), W(stopped,e)=0 and t(r,e)=real(untopD_0 W(r,e)). '
    'Set ρ(live(T,z),s)=ofReal[λ_r(Φ_s z) exp(−Λ_z(max(s,0)))] and ρ(stopped,s)=0. '
    'The relative append A_rel(h,s) preserves every old coordinate and appends live(T+max(s,0),S_rΦ_s z) '
    'when h_n=live(T,z), and stopped when h_n=stopped. Define A_abs(h,u)=A_rel(h,u−a(h)) and L_abs(h,u)=(A_abs(h,u),u). '
    'The raw harmonic flow at negative real time, clipped cumulative increment and stopped time0 are auxiliary totalizations. '
    'H_n,H_next,a,U,A_abs,L_abs are Borel; for every abstract (h,u) and every 0≤j≤n, A_abs(h,u)_j=h_j. '
    'For any fixed Borel b:Hist_n→[0,∞), finite at every history but not required uniformly bounded, put d(h)=max(b(h)−a(h),0) and '
    'D_b(h,u)=1_{a(h)<u<b(h)}ρ(h_n,u−a(h)). '
    'Define B_rel={w:0<W(R_n(ε(w)),w_n)<d(H_n(w))} and '
    'B={w:H_n(w)_n and H_next(w)_(n+1) are live, a(H_n(w))<U(w)<b(H_n(w))}. '
    'Let X(w)=(H_n(w),U(w)), Y(w)=(H_next(w),U(w)), and ν_b=D_b(μ_n⊗du), where du is real Lebesgue measure. '
    'D_b is jointly Borel and ∫_ℝD_b(h,u)du≤1 for EVERY abstract history h. B,X,Y are Borel and B_rel=B pointwise. '
    'For every w∈B, U(w)=a(H_n(w))+t(R_n(ε(w)),w_n) and H_next(w)=A_abs(X(w)). '
    'The exact restricted laws are X_*(P|B)=ν_b, Y_*(P|B)=(L_abs)_*ν_b and (H_next)_*(P|B)=(A_abs)_*ν_b, with ν_b(univ)≤1. '
    'For every jointly Borel G:Hist_n×ℝ→[0,∞], the parameter integral h↦∫G(h,u)D_b(h,u)du is Borel and, for every Borel A⊆Hist_n, '
    '∫_{B∩{H_n∈A}}G(X(w))P(dw)=∫_A[∫G(h,u)D_b(h,u)du]μ_n(dh). '
    'For every jointly Borel F:Hist_(n+1)×ℝ→[0,∞], the parameter integral h↦∫F(L_abs(h,u))D_b(h,u)du is Borel and '
    '∫_{B∩{H_n∈A}}F(Y(w))P(dw)=∫_A[∫F(L_abs(h,u))D_b(h,u)du]μ_n(dh). '
    'No boundedness or integrability of F,G, positive μ_n(A), normalized conditioning, finite wait, no-atom, probability or density provider is assumed. '
    'This includes n=0, rank zero, zero hazard, stopped records, live infinite waits, b(h)≤a(h), null A and unrealizable histories; missing mass is not normalized. '
    'This is attributed ASTIS completion of one absolute-coordinate ingredient implicit in Appendix A.1(A.7), not a standalone printed theorem. '
    'Finite ordered iteration, terminal survival/full path/count assembly, full(A.7), physical-time restart/Markovness, invariance, hypocoercivity, '
    'implementation/errors/unbounded query costs/main/composition/wholepaper/Goal remain OPEN.')
assumptions=[
    'E is a finite-dimensional real inner-product space with its Borel structure, including rank zero.',
    'Exactly six source analytic hypotheses: α>0, α≤β, V∈C², α‖v‖²≤D²V(x)[v,v]≤β‖v‖² for every x,v, η>0 and βη≤1; α,β≥0.',
    'y,xRef,z₀ and deterministic n are universally quantified; the exponential product, clipped thresholds, stopped recursion and observations are literal definitions.',
    'b is any fixed Borel finite-valued history function, possibly globally unbounded. F and G are arbitrary jointly Borel extended nonnegative tests; A is any Borel old-history event.',
    'Joint measurability, actual clock/append identities, fiber mass and all distribution/integration statements are conclusions. No independence, normalization, no-atom or finite-wait premise is supplied.'
]
formulae=[
    r"a(h)=\operatorname{time}(h_n),\quad U(w)=\operatorname{time}(H_{n+1}(w)_{n+1}),\quad A_{\rm abs}(h,u)=A_{\rm rel}(h,u-a(h)).",
    r"D_b(h,u)=\mathbf1_{\{a(h)<u<b(h)\}}\rho(h_n,u-a(h)),\quad d(h)=(b(h)-a(h))_+,\quad D_b(h,a(h)+s)=D_d^{\rm rel}(h,s).",
    r"B=B_{\rm rel},\quad w\in B\Longrightarrow U(w)=a(H_n(w))+t_n(w),\quad H_{n+1}(w)=A_{\rm abs}(H_n(w),U(w)).",
    r"X_*(P|_B)=\nu_b,\quad Y_*(P|_B)=(L_{\rm abs})_*\nu_b,\quad(H_{n+1})_*(P|_B)=(A_{\rm abs})_*\nu_b,\quad\nu_b=D_b(\mu_n\otimes du).",
    r"\int_{B\cap\{H_n\in A\}}G(H_n,U)\,dP=\int_A\int_{\mathbb R}G(h,u)D_b(h,u)\,du\,\mu_n(dh).",
    r"\int_{B\cap\{H_n\in A\}}F(H_{n+1},U)\,dP=\int_A\int_{\mathbb R}F(L_{\rm abs}(h,u))D_b(h,u)\,du\,\mu_n(dh)."
]
body=s.index(':= by\n',s.index('theorem actual_absolute_next_event_time_law'))+len(':= by\n')
def step(title,text,formula,start,end):
    a=s.index(start,body);b=s.index(end,a);code=s[a:b]
    return dict(title=title,text=text,formula=formula,lean=code,detail='Exact contiguous compiled proof region; mathematical dependencies are discharged inside the proof.',
        lean_source_region=dict(path=file,source_raw_sha256=sha(raw),start_line=s[:a].count('\n')+1,end_line=s[:b].count('\n'),exact_code_raw_sha256=sha(code.encode())))
steps=[
    step('Retain the literal model and actual next record',
        'Expand the sealed literal clock, reflection, harmonic flow, stopped recursion and complete histories. Reuse the complete-history extension and conditional-density producers with the same six source hypotheses. Define U by reading the next record itself, a by reading the old last record, and absolute append by subtracting a(h) before relative append. No clock identity is assumed.',
        formulae[0],'  classical\n','  have hnext :'),
    step('Prove Borel observers and preserve every old coordinate',
        'The complete next history is Borel by the preceding producer; each old coordinate is its projection. readTime is a Borel sum-elimination, with constant0 on stopped. Composition gives Borel a and U. The Borel map (h,u)↦(h,u−a(h)), followed by the existing relative append, gives Borel absolute append; pairing with u gives its lift. The relative prefix identity preserves all old coordinates for every real u, including auxiliary off-support inputs.',
        r"H_n,H_{n+1},a,U,A_{\rm abs},L_{\rm abs}\ \text{are Borel};\quad A_{\rm abs}(h,u)_j=h_j\ (j\le n).",
        '  have hnext :','  intro b hb\n'),
    step('Translate the strict density and its fiber mass',
        'For fixed Borel b, the positive part d=(b−a)₊ is Borel. The strict region a(h)<u<b(h) is Borel, so multiplying the shifted old density by its indicator gives jointly Borel D_b. Elementary real inequalities show a<a+s<b iff 0<s<d; the assertion remains true when b≤a, when both sides are false. Thus D_b(h,a+s)=D_rel(h,s). Lebesgue translation invariance in each fixed history fiber preserves its nonnegative integral, and the verified relative density bound gives ∫D_b≤1 for every history. This is a fiberwise change of variables, with no unproved product-shear certificate.',
        formulae[1],'  intro b hb\n','  have h90d :='),
    step('Identify the actual clock and absolute append on exactly the strict event',
        'Split the actual old record into stopped and live. Stopped remains stopped and has zero wait, so neither strict event occurs. For a live record, an infinite threshold-crossing time produces stopped next record and violates the finite relative upper bound. A finite wait v produces exactly live(T+v,SΦ_v z). Reading that record gives U=T+v; the cutoff equivalence proves B_rel=B pointwise, including v=0. This establishes Borel B and the actual clock equality. Substitute U−a=t in the preceding guarded relative-history identity to obtain H_next=A_abs(X) throughout B.',
        formulae[2],'  have h90d :=','  let oldPrefix :'),
    step('Transfer all old-history and absolute-time tests',
        'Let π drop the last record from an extended history. It is Borel, π(H_next)=H_n and π(A_rel(h,s))=h. For any jointly Borel G, use G_rel(h_next,s)=G(πh_next,a(πh_next)+s) in the existing complete-history law. The actual clock identity identifies its left integrand with G(H_n,U) on B. In each right fiber, Lebesgue translation converts G(h,a+s)D_rel(h,s) to G(h,u)D_b(h,u). Integrating over any Borel A gives the unnormalized identity, including null A. Borel parameter integration follows from joint nonnegative measurability, without boundedness or integrability assumptions.',
        formulae[4],'  let oldPrefix :','  -- Reuse the canonical actual input probability;'),
    step('Recover the weighted joint measure and its actual-history marginals',
        'Reuse only the probability-normalization component of the canonical exponential-product theorem to obtain probability P and its Borel pushforward μ_n. Apply the preceding test identity at A=univ. Equality against every Borel nonnegative test, Tonelli and the withDensity integral formula yield X_*(P|B)=D_b(μ_n⊗du). On B, Y=L_abs(X) and H_next=A_abs(X), so measurable pushforward composition gives both remaining laws. Their reference measure ν_b has total mass P(B)≤1. Missing mass is never renormalized.',
        formulae[3],'  -- Reuse the canonical actual input probability;','  refine ⟨hD, hfiber,'),
    step('Obtain every next-history test and retain the remaining boundary',
        'For jointly Borel F, apply the old-history test identity to G=F∘L_abs. Its parameter integral is Borel. The pointwise Y=L_abs(X) identity replaces the integrand throughout B∩{H_n∈A}, giving the displayed identity for every Borel A. This proves one strict next absolute-time step; iteration over ordered times, terminal survival, full path/count identification and full A.7 still require separate proofs.',
        formulae[5],'  refine ⟨hD, hfiber,','\nend\n')
]
assert ''.join(x['lean'] for x in steps)==s[body:s.index('\nend\n',body)]
slug='pbps-actual-absolute-next-event-time';aid='ASTIS-RT-20261011-PBPSActualAbsoluteNextEventTime'
title='Actual PBPS next absolute-event-time law'
source=dict(url='https://arxiv.org/html/2609.06905v1#A1.E7',edition='arXiv2609.06905v1',anchor=claim['source_anchor'],wording_status='faithful paraphrase',
    attribution='Fan Chen, Sinho Chewi, Jianfeng Lu and Matthew S. Zhang, arXiv2609.06905v1 Appendix A.1(A.1),(A.2),(A.7) and Appendix A.2. This explicit actual-history absolute-time density is attributed ASTIS completion of an implicit coordinate step; it is not a quoted standalone source theorem.')
deltas=[
    dict(source='Actual source clock recursion and original smoothness/curvature/step assumptions.',lean='Literal stopped iid exponential recursion under the same six analytic hypotheses.',classification='source-implicit',reason='Borel tagged histories, clipped null-set inputs, rank-zero extension and auxiliary totalizations are explicit.'),
    dict(source='Event times in A.7 are cumulative absolute times.',lean='U reads the actual next record; strict relative/absolute guards and U=a+t are proved internally.',classification='source-implicit',reason='Coordinate equivalence, measurability and translation are dependency conclusions, not public assumptions.'),
    dict(source='A.7 uses ordered event densities and reflected states.',lean='One strict absolute-time joint law and complete-history transport, with all ENNReal joint tests and Borel history cutoffs.',classification='source-implicit',reason='This single iteration ingredient preserves null events and missing mass without normalized conditional probabilities.'),
    dict(source='Full path-functional identity, ordered iteration and final survival.',lean='Only the next coordinate is proved; full A7 and downstream restart/main/composition remain open.',classification='unresolved',reason='No full ordered-time integral, path/count partition or terminal survival assembly is asserted.')
]
item=dict(id=slug,library='pbps',chapter='pbps-01',chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html',title=title,source=source,statement=statement,assumptions=assumptions,
    formulae=[dict(label='Absolute-time law '+str(i+1),tex=f) for i,f in enumerate(formulae)],
    obligations=[dict(id='actual-absolute-coordinate',label='Actual strict next absolute-event-time law'),dict(id='full-ordered-path',label='Ordered iteration, terminal survival and full path/count identity A7')],
    bindings=[dict(declaration=decl,cell=cid,role='proof-edge',supports=['actual-absolute-coordinate'],audit_id=aid,boundary=claim['truth_boundary'],assumption_deltas=deltas)])
for key in ['declaration_level','statement_seal','source_proof_coverage','proof_digestion','purification']:item[key]=copy.deepcopy(cell[key])
unit=dict(kind='theorem',declaration=decl,title=title,sources=[dict(url=source['url'],label=source['anchor'],scope=claim['truth_boundary'])],tests=claim['focused_checks'],
    assumptions=assumptions,statement=statement,formula=formulae[5],boundary=claim['truth_boundary'],steps=steps,lean_statement=statement,lean_proof='; '.join(x['title'] for x in steps),
    helpers=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualAbsoluteNextEventTime.actual_absolute_next_event_time_statement'],
    astis_dependencies=cell['parents'],mathlib_dependencies=['measurePreserving_add_left','MeasurePreserving.lintegral_comp','Measure.ext_of_lintegral','lintegral_prod','lintegral_withDensity_eq_lintegral_mul','Measurable.lintegral_prod_right','Measure.map_map','Measure.map_congr','setLIntegral_congr_fun'])
pp=ROOT/'website/content/publications'/f'{slug}.json';lp=ROOT/'website/content/declaration_lessons'/f'{slug}.json'
fresh(pp,dict(schema_version=1,items=[item]));fresh(lp,dict(schema_version=1,units=[unit]))
draft=load(RUN/'decoder-draft91.json')
lean=copy.deepcopy(draft['lean'])
lean.update(formalizer='companion_root_20261005',compiler_evidence=str(receipt),statement_representation=dict(
    kind='exact-literal-private-Prop-expansion',actual_header=s[s.index('theorem actual_absolute_next_event_time_law'):body-len(':= by\n')],
    private_definition='private def '+literal,expanded_header='theorem actual_absolute_next_event_time_law'+lean['statement'],
    source_approved_overlay=str(RUN/'root.statement-seal91.json'),kernel_header_and_literal_expansion_checked=False))
original=source['attribution']+'\n'+statement+'\n'+source['anchor']
pub.inputs.cache_clear();pub.load.cache_clear()
audit=dict(id=aid,state='draft',source=dict(source_id='companion-domain:'+slug,anchor=source['anchor'],url=source['url'],original_text=original,text_sha256=sha(original.encode())),
    lean=lean,source_review=dict(state='pending'),repairs=[],publication_binding_sha256=pub.binding_digest(item,item['bindings'][0],pub.inputs()),
    publication_context=pub.review_context(item,item['bindings'][0],pub.inputs()))
assert rt.decoder_packet(audit)==load(ROOT/'runs/semantic-roundtrip/anonymous91/input.json')
ap=ROOT/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json';fresh(ap,audit)
fresh(RUN/'publication-freeze91.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='DRAFT_PENDING_INDEPENDENT_MATH_SOURCE_AND_EXPOSITION',inputs=[pin(p) for p in [pp,lp,ap]],module=pin(module),steps=len(steps),exhaustive_BODY_coverage=True,PROVED_LOCAL=False,VERIFIED=False))
pub.check_advance([decl],reviewed=False)
print('Draft publication and identical anonymous packet: seven exhaustive proof regions; reviews pending.')
