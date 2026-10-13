from pathlib import Path
import json,hashlib,sys,copy,datetime
root=Path(__file__).resolve().parents[3]; run=Path(__file__).resolve().parent
sys.path.insert(0,str(root/'tools'))
import astis_semantic_roundtrip as rt
import astis_publication as pub
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def fresh(p,x):
    assert not p.exists(),p
    save(p,x)
def pin(p):return dict(path=p.relative_to(root).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
claim=load(run/'claim.json');decl=claim['target_declarations'][0];file=claim['proposed_files'][0];cid=claim['frontier_cell']
module=root/file;s=module.read_text(encoding='utf8');raw=module.read_bytes()
receipt=run/'focused93/production1-sealed-law/receipt.json';r=load(receipt)
assert r['exit_code']==0 and r['source_raw_sha256']==sha(raw)
seal=load(run/'root.statement-seal93.json')
literal=s.split('private def actual_finite_count_path_statement',1)[1].split('/-- Exact sealed',1)[0].strip()
assert literal==seal['expanded_literal_Prop'].strip()
statement_lean=literal.replace(' : Prop :=',' :',1)
standing=load(root/'website/content/publications/pbps-actual-ordered-prefix.json')['items'][0]['statement'].split('For every deterministic finite n')[0]
restatement=standing+'''
Write T_j(w)=a for a live record R_j(ε(w))=live(a,z), and T_j(w)=∞ for a stopped record. Define I_n(T)={T_n≤T<T_(n+1)}, and the total selector N(T,w)=min{n:w∈I_n(T)} when such an n exists, and 0 otherwise. For n≥0 let Hist_n=D^(Fin(n+1)) and H_n(w)_j=R_j(ε(w)). Write readTime(live(a,z))=a and readTime(stopped)=0. The abstract guard A_n(T) consists of histories all of whose records are live, whose read times are strictly increasing and whose positive-index read times are strictly below T; it does not constrain record0 itself. Actual H_n starts at live(0,z₀). For h∈Hist_n set d_n(T,h)=max{T−readTime(h_n),0}. Define survival(live(a,z),u,e) to mean u<τ_z(max{e,0}); on stopped it is false. Define W(live(a,z),u)=exp(−Λ_z(u)); on stopped W=0. Put C_n(T)={w:H_n(w)∈A_n(T), survival(R_n(ε(w)),d_n(T,H_n(w)),w_n)}.
For a fixed finite T≥0 let Path_T be all functions from [0,T] into E×E, with its coordinate-product sigma algebra. On every history, including unrealizable ones, define Ψ_n(T,h)(s) by starting at z₀ and visiting j=0,…,n in increasing order: a live record (a,z) with a≤s replaces the current value by Φ_(s−a)(z), and an ineligible live or stopped record leaves it unchanged. All elapsed times in this total definition use nonnegative subtraction.
Define Δ_n(T)={t∈ℝ^n:0<t₁<⋯<t_n<T}, and let m_n be the comap of product Lebesgue measure to this subtype, without normalization. For t∈Δ_n(T), put s₀=0,s_i=t_i, z₀ equal to the prescribed initial phase and z_i=S_rΦ_(s_i−s_(i−1))(z_(i−1)). Set K_n(t)_j=live(s_j,z_j), Γ_n(T,t)=Ψ_n(T,K_n(t)), q_n(t)=ofReal(∏_(i=1)^n λ_r(Φ_(s_i−s_(i−1))(z_(i−1)))exp[−Λ_(z_(i−1))(s_i−s_(i−1))]), and ρ_n(T,t)=q_n(t)W(K_n(t)_n,d_n(T,K_n(t))). The literal toNNReal conversions agree with these nonnegative simplex times.
There exists one actual phase representative Z(y,r,z₀,t,w), jointly Borel in all deterministic parameters, finite time and raw input, with the following properties. On every raw covering interval T_n(w)≤s<T_(n+1)(w), if R_n(ε(w))=live(a,z), then Z(s,w)=Φ_(s−a)(z). If no interval covers s, Z(s,w)=z₀. For each fixed parameter tuple, Z(0,w)=z₀ almost surely.
For every n≥0 and finite T≥0, Ψ_n, Γ_n and ρ_n are jointly Borel in their deterministic parameters and history or simplex input. For each fixed parameter tuple, H_n, Z_T:w↦(s↦Z(s,w)), N(T,·) and C_n(T) are measurable. For every prescribed t and s∈[0,T], if s_j≤s and every later s_k>s, then Γ_n(T,t)(s)=Φ_(s−s_j)(z_j). For every raw w∈C_n(T), Ψ_n(T,H_n(w))=Z_T(w) as entire functions on [0,T].
For each fixed parameter tuple and T, on one P-full event simultaneously for every j>0 and every k≥0: T_j(w)≠T, N(T,w)=k if and only if w∈C_k(T), both sets {j>0:T_j(w)<T} and {j>0:T_j(w)≤T} are finite, and both cardinalities equal N(T,w). This is not a single no-jump event valid for all T. The raw sets C_k(T) are pairwise disjoint, and P(⋃_(k≥0)C_k(T))=1.
The exact unnormalized joint history/path law is (H_n,Z_T)_*(P restricted to {N(T)=n})=(K_n,Γ_n)_*(ρ_n m_n). Equivalently, for every Borel F:Hist_n×Path_T→[0,∞], ∫_{N(T)=n}F(H_n(w),Z_T(w))P(dw)=∫_{Δ_n(T)}F(K_n(t),Γ_n(t))ρ_n(T,t)m_n(dt). Moreover ∫ρ_n dm_n=P{N(T)=n}≤1. No test boundedness, integrability, positive event probability, provider of densities, independence, finite waits or process measurability is assumed. The result includes n=0,T=0, rank0, infinite waits and explicit raw exceptional fallbacks; at n=0 the terminal survival factor remains, so the mass is not generally one for T>0.
This is an attributed ASTIS completion of the finite-count complete-path ingredient implicit in Appendix A.1(A.7), using Appendix A.2. It is a faithful mathematical restatement with disclosed rank-zero, extended-test and coordinate-product-path choices, not a quoted standalone theorem. Hazard stitching along the path, pre-jump left limits, Skorokhod compatibility, the infinite full A.7 expansion, restart/Markovness, invariance, hypocoercivity, implementation errors, expected query costs, full paper results and actual-input composition are separate remaining obligations.
'''
attribution='Chen, Chewi, Lu and Zhang, arXiv:2609.06905v1, Appendix A.1 and A.2; attributed ASTIS completion of a source-implicit finite-count path ingredient, not verbatim source text.'
fresh(run/'authored-statement93.json',dict(statement=restatement,attribution=attribution))
context=load(root/'runs/semantic-roundtrip/anonymous92/input.json').get('definition_context')
if context is None:
    context=load(root/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualOrderedPrefix.json')['lean']['decoder_context']
context=list(context)+[
 'Nat.find returns the least natural satisfying a decidable predicate, given existence; the displayed default is part of the total definition.',
 'Fin.foldl visits increasing finite indices, updating the accumulator at each step. A function-valued measurable space here is the product of its coordinate measurable spaces; no topology or diagonal measurability of an uncountable function space is implicit.',
 'Set.ncard is the natural cardinality; explicit Finite conclusions precede its use. A WithTop nonnegative real can be infinity, and nonnegative subtraction is truncated at zero.'
]
aid='ASTIS-RT-20261011-PBPSActualFiniteCountPath';slug='pbps-actual-finite-count-path';title='Actual PBPS finite-count complete-path law'
audit=dict(id=aid,state='draft',source=dict(source_id='companion-domain:'+slug,anchor=claim['source_anchor'],
 url='https://arxiv.org/html/2609.06905v1#A1.E7',original_text=restatement,text_sha256=sha(restatement.encode())),
 lean=dict(statement=statement_lean,statement_sha256=sha(statement_lean.encode()),compiled=True,decoder_context=context,
 declaration=decl,file=file,formalizer='companion_root_20261005',compiler_evidence=receipt.relative_to(root).as_posix()),source_review=dict(state='pending'),repairs=[])
ap=root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json';fresh(ap,audit)
packet=rt.decoder_packet(audit);out=root/'runs/semantic-roundtrip/anonymous93/input.json';fresh(out,packet)
fresh(run/'decoder-freeze93.json',dict(module=pin(module),seal=pin(run/'root.statement-seal93.json'),compile=pin(receipt),packet=pin(out),canonical_packet_sha256=packet['packet_sha256'],source_visible=False,publication_binding_pending=True))

cp=root/'research-wiki/frontier-cells'/f'{cid}.json';cell=load(cp)
parents=sorted(set(re.findall(r'AutoSamplingTheory\.(?:ExampleCases|TechnicalLemmas)\.[A-Za-z0-9_.]+',s))) if False else []
import re
parents=sorted(set(re.findall(r'(?:AutoSamplingTheory\.(?:ExampleCases|TechnicalLemmas)\.[A-Za-z0-9_.]+)',s)))
parents=[p for p in parents if p!=decl.rsplit('.',1)[0]]
cell['parents']=parents;cell['reuse_plan']['reused_declarations']=parents;cell['proof_digestion']['existing_substrate']=parents
cell['blocked']['reason']='The whole sealed production proposition compiles; independent whole mathematics, anonymous decoder, primary-first source/exposition and publication admission remain pending.'
cell['evidence']['focused_checks']=[receipt.relative_to(root).as_posix()]
cell['evidence']['whole_target_compiled']=pin(module)
save(cp,cell)
assumptions=[
 'Finite-dimensional real inner-product Borel space E, including the disclosed rank-zero extension.',
 'Exactly six analytic assumptions: α>0, α≤β, V∈C², α‖v‖²≤D²V(x)[v,v]≤β‖v‖² for all x,v, η>0, βη≤1; α,β are nonnegative.',
 'All finite n,T≥0 and deterministic y,r,z₀ are universal. The actual iid Exp(1) input, stopped recursion, count, history/path maps and density are literal definitions, not supplied certificates.',
 'Path_T carries the coordinate-product sigma algebra. Each test F is arbitrary Borel Hist_n×Path_T→[0,∞].',
 'Joint measurability, existence, initialization, endpoint nullity, finite counts, all laws and mass bounds are derived; no additional boundedness, integrability, positive mass, finite waiting time or independence premise.'
]
formulae=[
 r'C_n(T)=\{H_n\in A_n(T),\ T-T_n<\tau_{z_n}(\epsilon_n)\},\quad \rho_n=q_n\exp[-\Lambda_{z_n}(T-s_n)].',
 r'\Psi_n(h)(s)=\Phi_{s-a_j}(z_j),\quad j=\max\{i\le n:h_i=\operatorname{live}(a_i,z_i),\ a_i\le s\},',
 r'\forall T\ge0,\quad P\{\exists j>0:T_j=T\}=0.',
 r'N(T)=n\ \Longleftrightarrow\ C_n(T)\quad P\text{-a.s.},\qquad N(T)=\#\{j>0:T_j<T\}=\#\{j>0:T_j\le T\}.',
 r'(H_n,Z_T)_*(P|_{\{N(T)=n\}})=(K_n,\Gamma_n)_*(\rho_nm_n).',
 r'\int_{N(T)=n}F(H_n,Z_T)\,dP=\int_{\Delta_n(T)}F(K_n,\Gamma_n)\rho_n\,dm_n,\quad \int\rho_n\,dm_n=P\{N(T)=n\}\le1.'
]
def step(title,text,formula,start,end):
    a=s.index(start);b=s.index(end,a);code=s[a:b]
    return dict(title=title,text=text,formula=formula,lean=code,detail='Exact compiled proof region; internal helper premises are discharged by the actual producers inside the final proof.',
      lean_source_region=dict(path=file,source_raw_sha256=sha(raw),start_line=s[:a].count('\n')+1,end_line=s[:b].count('\n'),exact_code_raw_sha256=sha(code.encode())))
steps=[
 step('Construct a total measurable finite-history interpolation',
 'Fix one coordinate s of the path. Each tagged record either retains the accumulator or replaces it by the harmonic flow at s−a; the live/stopped tag and a≤s are Borel. Finite induction proves the fold measurable. The product sigma algebra then makes the entire function-valued map measurable by its coordinates. The last eligible record controls the fold, including when no record is eligible and z₀ remains. Reuse the actual harmonic-flow joint measurability to obtain Ψ for every parameter and arbitrary history.',
 formulae[1], 'private theorem measurable_finite_fold','private theorem localized_survival_history_measure'),
 step('Convert conditional next-wait survival into a weighted history measure',
 'The actual conditional survival theorem applies at the history-dependent residual d=max(T−lastTime,0). For every Borel history event A, its probability with survival is the history integral of W over A. Apply this to B∩A for an arbitrary Borel test set B; measure extensionality identifies H_*(P|_{H∈A,survival})=(H_*P|_A).withDensity(W). Measurability is inherited from actual history, the tagged time observer and the actual hazard. No positive conditioning probability or finite wait is required, and W vanishes on the stopped tag.',
 r'H_*(P|_{\{H\in A,\,survival\}})=(H_*P|_A)W.',
 'private theorem localized_survival_history_measure','private theorem actual_terminal_weighted_prefix_tests'),
 step('Attach the terminal factor to the ordered-prefix law',
 'Apply the weighted history identity to F(h,Ψ(h)). The actual ordered-prefix law applies to this nonnegative Borel function times W, giving the simplex integral of F(K,Ψ(K))qW. This is precisely F(K,Γ)ρ. Joint Borel K, Ψ, q and the tagged terminal weight imply joint Borel Γ and ρ. Equality of all nonnegative tests gives the joint history/interpolation pushforward, and F=1 gives its unnormalized mass P(C_n)≤1. This step does not yet identify C_n with a count event.',
 r'\int_{C_n}F(H_n,\Psi_n(H_n))dP=\int_{\Delta_n}F(K_n,\Gamma_n)q_nW(K_n)dm_n.',
 'private theorem actual_terminal_weighted_prefix_tests','private theorem finite_history_fold_eq_process'),
 step('Identify interpolation with one actual process on the raw event',
 'Take the existing jointly measurable physical-time representative Z, with its exact covered-arc and uncovered-fallback behavior. On C_n all records through n are live, and strict terminal survival gives T<T_(n+1), also when the wait is infinite. At any s≤T choose the greatest index j≤n whose record time is at most s; initialization supplies index0. Every later index is ineligible and the next event lies after s. The finite fold therefore equals the harmonic arc selected by the actual Z. Function extensionality gives whole-path equality on every raw C_n sample, without assuming a measurable diagonal in the uncountable path space.',
 r'w\in C_n(T)\Longrightarrow\Psi_n(H_n(w))=Z_T(w).',
 'private theorem finite_history_fold_eq_process','private theorem find_decidable_eq'),
 step('Make the total count measurable and relate interval indices to cardinalities',
 'Each half-open interval membership predicate is Borel because actual event times are jointly measurable. Their countable union is Borel. On that union the least successful index is measurable; use0 off it. Distinct half-open intervals cannot overlap for a monotone event-time sequence. If N selects the covering interval, monotonicity gives T_j≤T iff j≤N. In the absence of positive-index events exactly at T the strict and non-strict positive-index sets both equal {1,…,N}, hence are finite with cardinality N. The no-atom condition is an internal dependency supplied below.',
 formulae[3], 'private theorem find_decidable_eq','private theorem actual_prescribed_path_interpolation'),
 step('Read the prescribed path at its last eligible event',
 'Every ordered simplex time is nonnegative. The real time and nonnegative-time coercions therefore agree, and the last-eligible fold identity yields Γ(t)(s)=Φ_(s−s_j)(z_j). The condition requires s_j≤s and all later s_k>s; at an event time the selected state is the post-bounce z_j. It also covers n=0 and T=0.',
 r's_j\le s< s_k\ (k>j)\Longrightarrow\Gamma_n(t)(s)=\Phi_{s-s_j}(z_j).',
 'private theorem actual_prescribed_path_interpolation','private theorem subtype_coordinate_null'),
 step('Exclude fixed-horizon endpoint atoms from the actual input',
 'A coordinate hyperplane {t_i=T} has zero finite-product Lebesgue measure. Comap to the simplex and multiplication by any nonnegative density preserve that null set. The prefix pushforward law transfers this to the actual history observer on the strict guard. Actual exponential inputs are simultaneously positive almost surely, and the actual finite recurrence then gives strict increases between live records. If the nth event equals T, the entire finite history belongs to the strict guard at T+1. Applying the guarded nullity there avoids excluding the endpoint by definition. A countable intersection over positive n proves no event exactly at this fixed T. No intersection over all real T is taken.',
 formulae[2], 'private theorem subtype_coordinate_null','private theorem actual_count_event_identification'),
 step('Close count interpretation, disjointness and full probability',
 'On every raw C_n, the last time is at most T (initial time0 handles n=0), and survival makes the next time strictly greater than T: thus C_n⊆I_n. Conversely, on the common full event of positive clocks, fixed-T no-atoms and physical-time coverage, any covering interval has a strict live prefix below T, and its residual wait survives to T. Hence I_n=C_n on that event for all n. The least covering index is unique, so N=n iff C_n and the preceding cardinality lemma applies. Raw C disjointness follows from C_n⊆I_n and monotonicity. Almost-sure coverage then makes their countable union have mass1.',
 formulae[3]+r'\qquad C_i\cap C_j=\varnothing\ (i\ne j),\quad P(\bigcup_n C_n)=1.',
 'private theorem actual_count_event_identification','private def actual_finite_count_path_statement'),
 step('Assemble the sealed actual history/path law',
 'Keep the one actual Z and all original six assumptions. Its joint measurability gives each coordinate-measurable Z_T; combine this with H_n,N,Ψ,Γ,ρ measurability and prescribed path evaluation. The sets {N=n} and C_n agree almost surely, so their restricted measures agree. On C_n the whole paths Ψ(H_n) and Z_T agree pointwise. Substitution into the weighted joint pushforward and every nonnegative test identity gives the claimed actual law. The same almost-sure set equality transfers the mass formula ∫ρ=P(C_n) to P{N=n}. In particular the zero-event term retains terminal survival; it is not normalized to one for positive T.',
 formulae[4]+formulae[5], 'theorem actual_finite_count_path_law','\nend\n')
]
source=dict(url=audit['source']['url'],edition='arXiv2609.06905v1',anchor=claim['source_anchor'],wording_status='faithful paraphrase',attribution=attribution)
deltas=[dict(source='Actual exponential-clock construction and finite-count path ingredient around A.7.',lean='Same six conditions with fully derived literal recursion, measurable total representative, terminal survival and count/path law.',classification='source-implicit',reason='ASTIS supplies omitted measurable/count/endpoint adapters as proofs, not public premises.'),
 dict(source='Source path-functionals and positive-dimensional setting.',lean='Coordinate-product path sigma algebra, rank-zero and arbitrary nonnegative extended Borel tests are explicit.',classification='generalization',reason='No Skorokhod measurability or bounded signed-test summation is inferred.'),
 dict(source='Full A.7 combines finite-count terms, path hazard and all counts.',lean='One exact finite-count joint law for every n,T; hazard stitching, left limits and infinite assembly remain open.',classification='unresolved',reason='The finite-count ingredient is not the whole A.7 or the main sampling theorem.')]
item=dict(id=slug,library='pbps',chapter='pbps-01',chapter_path='example-cases/samplewiki/companions/proximal-bouncy-particle.html',title=title,source=source,statement=restatement,assumptions=assumptions,
 formulae=[dict(label='Finite-count path formula '+str(i+1),tex=f) for i,f in enumerate(formulae)],
 obligations=[dict(id='actual-finite-count-path',label='Terminally survived actual finite-count history/path law'),dict(id='full-path-a7',label='Hazard stitching, left limits and infinite full A7 assembly')],
 bindings=[dict(declaration=decl,cell=cid,role='proof-edge',supports=['actual-finite-count-path'],audit_id=aid,boundary=claim['truth_boundary'],assumption_deltas=deltas)])
for key in ['declaration_level','statement_seal','source_proof_coverage','proof_digestion','purification']:item[key]=copy.deepcopy(cell[key])
unit=dict(kind='theorem',declaration=decl,title=title,sources=[dict(url=source['url'],label=source['anchor'],scope=claim['truth_boundary'])],tests=claim['focused_checks'],assumptions=assumptions,statement=restatement,formula=formulae[4],boundary=claim['truth_boundary'],steps=steps,lean_statement=restatement,lean_proof='; '.join(x['title'] for x in steps),helpers=[decl.rsplit('.',1)[0]+'.actual_finite_count_path_statement'],astis_dependencies=parents,
 mathlib_dependencies=['Measure.pi_hyperplane','Measure.comap_apply_le','withDensity_absolutelyContinuous','measurable_find','Measurable.dite','Fin.foldl_succ_last','Nat.findGreatest_spec','Measure.restrict_congr_set','ae_restrict_of_forall_mem','Measure.map_congr','lintegral_congr_ae'])
pp=root/'website/content/publications'/f'{slug}.json';lp=root/'website/content/declaration_lessons'/f'{slug}.json'
fresh(pp,dict(schema_version=1,items=[item]));fresh(lp,dict(schema_version=1,units=[unit]))
pub.inputs.cache_clear();pub.load.cache_clear()
audit['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs())
audit['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs())
start=s.index('theorem actual_finite_count_path_law');stop=s.index(':= by\n',start)
audit['lean']['statement_representation']=dict(kind='exact-literal-Prop-expansion',actual_header=s[start:stop],private_definition='def actual_finite_count_path_statement'+literal,expanded_header='theorem actual_finite_count_path_law'+statement_lean,source_approved_overlay=(run/'root.statement-seal93.json').relative_to(root).as_posix(),kernel_header_and_literal_expansion_checked=False)
assert rt.decoder_packet(audit)==packet
save(ap,audit)
fresh(run/'publication-freeze93.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='DRAFT_PENDING_WHOLE_MATH_SOURCE_EXPOSITION',module=pin(module),inputs=[pin(p) for p in [pp,lp,ap]],steps=len(steps),conceptual_mirror_audit=dict(status='none-found',reason='This is an actual consumer join of the existing survival/disintegration/finite-prefix mechanism; no new cross-domain transport is claimed.'),PROVED_LOCAL=False,VERIFIED=False))
pub.check_advance([decl],reviewed=False)
print(json.dumps(dict(packet=pin(out),steps=len(steps),publication_binding_sha256=audit['publication_binding_sha256'])))
