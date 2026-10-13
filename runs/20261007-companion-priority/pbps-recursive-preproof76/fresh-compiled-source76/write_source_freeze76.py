from pathlib import Path
import datetime, hashlib, html, json, os, re

OUT=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def put(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
raw=(OUT/'primary-pbps.exactraw.snapshot.html').read_bytes()
assert len(raw)==1482128 and sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
manifest=json.loads((OUT/'raw-manifest76.json').read_text(encoding='utf-8'))
blocks=json.loads((OUT/'source-dom-index76.json').read_text(encoding='utf-8'))
byid={x['id']:x for x in blocks}
assert all(x in byid for x in ['A1.E1','A1.E2','A1.Ex4','A1.Ex5','A1.Ex6','A1.Ex7','A1.Ex8'])

slots={
 'objects':{'source':'A fixed-reference phase-space motion with y,r in R^d, z=(x,p), residual h(x)=∇V(x)-∇V(r), center c=y-η∇V(r), rate λ, harmonic flow Φ, reflection S, clocks E_j, indexed waits S_j and accumulated times T_j.','finite_selection':'Concrete indexed active finite prefixes starting at z_0=(x_0,p_0), T_0=0, together with their deterministic arcs and energy/rate/hazard estimates.','must_not_substitute':'An arbitrary certified trace, arbitrary hazard satisfying pre-assumed bounds, or a resampled reference at each bounce.'},
 'domains':{'source':'Finite-dimensional Euclidean R^d×R^d with Euclidean norm/inner product and its Borel sigma algebra; Φ_t for real t; hazard integration over [0,u] for u≥0; extended nonnegative waiting time, with ∞ for the empty hit set. η in (0,1/β].','finite_selection':'Finite n or prefix length N in N, only reached finite recursion indices; real finite waits when updating a state. Never evaluate Φ at ∞.','zero_normal':'R_0=I, explicitly from (2.4) and A.1.'},
 'quantifiers':{'source':'Every fixed y,r and every initial phase-space point, under standing paper assumptions. The clock sequence is independent Exp(1), indexed j≥1.','finite_selection':'For every finite indexed prefix and every reached index. A deterministic version may quantify over e_j≥0, with an explicit generalization label.','restrictions':'A finite next wait is not universally guaranteed; the update formula applies conditionally on the actual recursion producing a finite wait. Fixed y,r remain the same for all steps.'},
 'assumptions':{'standing_source':['V∈C²(R^d)','0<α≤β','αI≤Hess V(x)≤βI for all x','η∈(0,1/β]'], 'selected_minimal_analytic_inputs':['η>0','β≥0 and β-Lipschitz g; specialize to g=∇V using source standing assumptions'], 'not_extra_public_premises':['energy preservation','energy-shell norm bounds','rate cap','hazard integrability/continuity','first-hit attainment','waiting-time lower bound','Borel reflection/hitting/recursion','iid/SLLN/nonaccumulation','Markov property or stationarity'], 'source_probability':'iid Exp(1) is the full-process source input, not needed as a new premise for the deterministic finite ingredient.'},
 'conclusion':{'finite_selection':['Exact initialization and finite update T_(n+1)=T_n+s_(n+1), z_(n+1)=S(Φ_s(z_n))','Termination with both next wait and time ∞ when the hit set is empty; no post-termination state claim','H(z_n)=H(z_0), and H(Φ_u z_n)=H(z_0)','The Ex5 norm bounds and exact Ex6 source cap on active states/arcs','0≤A_z(u)≤Bu for u≥0','For B>0 and a finite wait, s≥e/B','For a positive threshold and B=0, empty hit set/termination','Borel finite-input recursion only after concrete measurability bridges are proved'], 'optional_finite_corollary':'T_n≥(sum_{j=1}^n e_j)/B on an active finite prefix, B>0; the finite part of Ex9.', 'explicitly_not_concluded':['Almost-sure nonaccumulation','global unique process','time-homogeneous Markov property','stationarity','half-turn kernel/reversibility','bounce or query cost','whole Proposition 3.1 or whole paper']},
 'scopes_senses':{'selected':'Deterministic finite-index recursion/finite arcs, not an a.s. global path theorem. Source s=inf of the actual integrated concrete rate with ≥ threshold; stopped branches have no chosen fake state.','positive_exponential':'The original source clocks are positive a.s.; the source no-jump cap-zero branch uses this fact.','zero_extension':'e=0 forces s=0. Indexed states may share a timestamp and differ. This is admissible deterministic completion of the finite recurrence only; it is not literal trajectory evaluation ζ_(T_n) for arbitrary zero clocks.','measurability':'Borel on the finite active domain; no global path-space/kernel/conditional-law measurability is silently certified.'},
 'constant_dependencies':{'cap':'B=√η β √(2E)(√(2ηE)+||c-r||), E=H(z_0). Depends on η,β,y,r,g(r),initial state. Same cap for all finite steps/arcs at these fixed inputs.','no_random_cost':'No K_id, c_evt, truncation cap, warm-start Δ, TV ε, or query bound belongs to this finite claim.','zero_branch':'B=0 must be handled separately; division/lower bound e/B is restricted to B>0.'}
}
put('source-seven-slots76.json',{'phase':'SOURCE_ONLY','candidate_seen':False,'slots':slots})

node_reasons={
 'S1.p1':'Standing potential/carrier assumptions; source main theorem after this paragraph is not selected.',
 'S1.E1':'Standing C²/Hessian convention; upper Hessian control yields the Lipschitz background used here.',
 'S2.SS1.p1':'Only Euclidean phase space, specular reflection and norm preservation are selected; vanilla BPS dynamics/laws/citation remain context.',
 'S2.E4':'Exact nonzero reflection and explicit R_0=I convention.',
 'S2.SS2.p1':'Only η∈(0,1/β] and conditional-target notation are background; Gibbs sampling and its cost are excluded.',
 'S2.SS3.SSS0.Px1':'Only positive-part/Euclidean norm conventions in the notation paragraph are selected; table and probability/operator notation are context.',
 'S2.SS3.SSS0.Px1.p1':'Positive-part and Euclidean norm/inner-product conventions; the other notation is context.',
 'S3.SS2.p1':'Conditional target and phase-space measure are contextual identity only; invariance and random-law construction remain OPEN.',
 'S3.Ex5':'Conditional potential background; not a finite-recursion premise requiring a random draw.',
 'S3.E1':'Definition of source stationary target only; no stationarity admitted.',
 'S3.SS2.p4':'Fixed center/residual and Lipschitz estimate are selected; reference sampling and cost conclusion are explicitly excluded.',
 'S3.Ex6':'Exact force decomposition underlying fixed-reference center and residual.',
 'S3.E4':'Exact center and residual definitions reused at A.1.',
 'S3.Ex7':'Residual bound from the source smoothness constant.',
 'S3.SS2.p5':'Explicit harmonic motion is background; half-turn return/kernel is outside the selected finite prefix.',
 'S3.E6':'Position component of the harmonic flow.',
 'S3.E7':'Half-turn identity is contextual only; source process output is not admitted.',
 'S3.SS2.p6':'Algorithm linkage; no whole algorithm correctness claim.',
 'alg1':'Finite mechanics use lines 1,3–7 at fixed reference; line 2 sampling and line 8 returned law remain OPEN.',
 'alg1.l1':'Input position and fixed auxiliary point.',
 'alg1.l3':'One fixed-reference gradient fixes c and h; query cost is not selected.',
 'alg1.l4':'Exact initial position x_0=x.',
 'alg1.l5':'Concrete harmonic ODE is background; full run until π requires later global construction.',
 'S3.E8':'ODE solved by the concrete Φ formula.',
 'alg1.l6':'Concrete residual positive-part bounce rate.',
 'S3.E9':'Concrete residual positive-part bounce rate.',
 'alg1.l7':'Post-flow momentum reflection at each finite bounce.',
 'S3.Thmtheorem1':'Target context only: every fixed y,r and initial point; full nonexplosive Markov/stationary/a.s.-return conclusion remains OPEN.',
 'S3.Thmtheorem1.p1':'Target context only; finite-recursion fragment is not the complete proposition.',
 'S3.SS2.p7':'Exact pointer to A.1 for well-posedness and stationarity.',
 'S4.E5':'Explicit full phase-space harmonic flow reused in A.1.',
 'A1.SS1.p1':'Exact fixed-reference λ, Φ, S, involution, zero-normal convention and possible discontinuity.',
 'A1.Ex1':'Exact bounce rate.',
 'A1.EGx1':'Exact harmonic flow and reflection map.',
 'A1.SS1.p2':'Finite recursion is selected; iid Exp law remains a full-process source input not claimed here. Includes finite/∞ split and arcs.',
 'A1.EGx2':'Full combined A.1/A.2 equation region, including inequalities and indices.',
 'A1.E1':'Integrated-hazard first-hit waiting-time definition.',
 'A1.E2':'Finite waiting-time accumulated-time and post-bounce-state update.',
 'A1.SS1.p3':'Energy/envelope/waiting finite estimates selected; SLLN/divergence/global process/Markov/Davis theorem are OPEN and separately inventoried.',
 'A1.Ex4':'Exact shifted energy definition.',
 'A1.Ex5':'Energy-shell momentum and shifted-position norm bounds.',
 'A1.Ex6':'Exact source cap B on the whole energy shell.',
 'A1.Ex7':'Integrated hazard upper bound.',
 'A1.Ex8':'Finite waiting lower bound when the cap is positive.'
}
def exclude_reason(x):
    sid=x['id']
    if sid=='bib.bib16': return 'Bibliographic context only. Davis Section 2 theorem text was not read; not an admitted external theorem.'
    if sid=='A1.Ex9': return 'Future nonaccumulation/SLLN limit is OPEN. Its deterministic finite-sum part is recorded separately as an optional finite corollary.'
    if sid.startswith('A1.'):
        return 'Later A.1 stationarity/reversal/trajectory-law/semigroup argument, outside the selected finite-recursion delta; retained RAW, no admission.'
    if sid=='alg1.l2': return 'Conditional reference and independent Gaussian momentum sampling; full randomized actual-input composition remains OPEN.'
    if sid=='alg1.l8': return 'Returned x_π requires the global process and half-turn kernel, both OPEN.'
    if sid.startswith('S3.Thmtheorem2') or sid in ['S3.SS2.p8','S3.SS2.p9']:
        return 'Half-turn kernel reversibility is outside this finite-recursion delta and remains OPEN.'
    if sid.startswith('S3.Thmtheorem3') or sid in ['S3.SS2.p10','S3.SS2.p11','S3.E10']:
        return 'Stationary bounce count/expected cost is outside this finite-recursion delta and remains OPEN.'
    if sid in ['S3.SS2.p2','S3.E2','S3.SS2.p3','S3.E3','S3.E5']:
        return 'Generator/vanilla/boomerang motivational context; not needed to prove the concrete finite recurrence or its estimates.'
    if sid.startswith('S2.'):
        return 'Retained §2 context outside the selected reflection/scale/notation background: vanilla process, refresh/thinning, Gibbs/geometric/oracle/divergence results are not admitted.'
    return 'Context outside the explicitly selected fixed-reference finite-recursion and its required background.'
inventory=[]
for x in blocks:
    sid=x['id']; disp='NODE' if sid in node_reasons else 'EXCLUDED'
    inventory.append({**x,'disposition':disp,'classification':'selected-source-node' if disp=='NODE' else 'excluded-with-reason','reason':node_reasons.get(sid,exclude_reason(x)),'overlap_policy':'Nested paragraph/theorem/display records overlap intentionally; coverage is by source region, not a theorem-count metric.'})
synthetic=[
 {'id':'src76:clock-law','source_anchor':'A1.SS1.p2 L2889–2892','disposition':'EXCLUDED','classification':'future-probability-input','reason':'Independent Exp(1) law is source context for later stochastic composition; no iid theorem proved in this finite review.'},
 {'id':'src76:finite-init','source_anchor':'A1.SS1.p2 L2890–2892','disposition':'NODE','classification':'selected-finite-recursion','reason':'z_0=(x_0,p_0), T_0=0.'},
 {'id':'src76:finite-stop-and-arcs','source_anchor':'A1.SS1.p2 L2908–2912','disposition':'NODE','classification':'selected-finite-recursion','reason':'Finite guard, empty-hit-set wait/time ∞ and stop, deterministic arcs for 0≤t<s.'},
 {'id':'src76:finite-energy-induction','source_anchor':'A1.SS1.p3 L2922–2924','disposition':'NODE','classification':'selected-finite-proof','reason':'Flow and every bounce preserve energy, then recurse; these must be proved dependencies.'},
 {'id':'src76:cap-zero-positive-clock','source_anchor':'A1.SS1.p3 L2949–2951','disposition':'NODE','classification':'selected-finite-zero-branch','reason':'Cap zero implies zero rate; a positive threshold yields no finite hit and stops. Zero-threshold deterministic completion is separate.'},
 {'id':'src76:finite-sum-bound','source_anchor':'A1.Ex9 L2960–2966','disposition':'NODE','classification':'optional-finite-corollary','reason':'Only T_n≥sum(e_j)/B on active finite prefixes; no limit claim.'},
 {'id':'src76:slln-nonaccumulation','source_anchor':'A1.SS1.p3 L2959–2970','disposition':'EXCLUDED','classification':'future-iid-SLLN-nonaccumulation-OPEN','reason':'The strong law, almost-sure divergent clock sum, no accumulating jump times and global unique process remain OPEN.'},
 {'id':'src76:memoryless-markov','source_anchor':'A1.SS1.p3 L2970–2973','disposition':'EXCLUDED','classification':'future-global-process-Markov-OPEN','reason':'Memorylessness and time-homogeneous Markov property require later stochastic/global work.'},
 {'id':'src76:davis-citation','source_anchor':'A1.SS1.p3 L2972–2973; bib.bib16 L6203–6214','disposition':'EXCLUDED','classification':'unread-external-theorem-OPEN','reason':'The paper cites Davis Section 2; bibliographic entry read only, theorem hypotheses/text not read.'}
]
citations=[]
for f in manifest['fragments']:
    if f['source_id']=='S1': continue
    data=(OUT/f['file']).read_text(encoding='utf-8')
    for m in re.finditer(r'<a\b[^>]*href="#(bib\.[^"]+)"[^>]*>[\s\S]*?</a>',data):
        label=html.unescape(re.sub(r'<[^>]+>','',m.group(0)))
        citations.append({'source_fragment':f['source_id'],'source_line':f['start_line']+data.count('\n',0,m.start()),'bib_id':m.group(1),'label':label,'disposition':'EXCLUDED','reason':'External citation in retained contextual source. No external theorem text inspected/admitted. Davis is separately tracked as the later integrated-hazard citation.'})
put('source-coverage76.json',{'status':'FROZEN_SOURCE_ONLY_OPEN','coverage_scope':'Every identified mathematical paragraph/theorem/display/algorithm-line block in S1.p1, S2, S3.SS2, S4.E5 and A1.SS1, plus the Davis bibliographic entry, receives NODE or EXCLUDED(reason). All combined equation regions retain their complete RAW mathematics. Mixed paragraphs additionally have explicit subclaim records.','raw_manifest':manifest,'inventory':inventory,'subclaim_inventory':synthetic,'external_citation_inventory':citations,'counts':{'blocks':len(inventory),'node':sum(x['disposition']=='NODE' for x in inventory),'excluded':sum(x['disposition']=='EXCLUDED' for x in inventory),'subclaims':len(synthetic),'external_citations':len(citations)},'exhaustiveness_limit':'This is independent source extraction, not self-approved topology certification or whole-paper coverage; a separate coverage/topology review remains pending.'})

graph_nodes=[
 ('standing','S1.p1; S2.SS2.p1','Standing potential/scale conditions','SOURCE_CONTEXT'),
 ('center-residual','S3.E4','Fixed center c and residual h','SOURCE_DEFINITION'),
 ('reflection','S2.E4; A1.EGx1','Specular R_h including R_0=I, bounce S','SOURCE_DEFINITION'),
 ('flow','S4.E5; A1.EGx1','Explicit harmonic Φ','SOURCE_DEFINITION'),
 ('rate','S3.E9; A1.Ex1','Concrete nonnegative residual rate λ','SOURCE_DEFINITION'),
 ('hazard','A1.E1','Integral A_z and extended first hit','SELECTED_FINITE_DEFINITION'),
 ('recursion','A1.E2; A1.SS1.p2','Finite guarded update, initialization, stop and arcs','SELECTED_FINITE_TARGET'),
 ('energy','A1.Ex4','Shifted H and initial E','SOURCE_DEFINITION'),
 ('energy-flow','A1.SS1.p3 L2922','H(Φ_u z)=H(z)','SELECTED_PROOF_INGREDIENT'),
 ('energy-bounce','A1.SS1.p3 L2922','H(Sz)=H(z)','SELECTED_PROOF_INGREDIENT'),
 ('energy-prefix','A1.SS1.p3 L2922–2924','Every active finite state/arc has initial energy','SELECTED_FINITE_TARGET'),
 ('norms','A1.Ex5','Momentum and shifted-position bounds','SELECTED_FINITE_TARGET'),
 ('lip','S3.Ex7; A1.SS1.p3 L2932','Residual Lipschitz bound','SELECTED_PROOF_INGREDIENT'),
 ('cap','A1.Ex6','Exact constant B bounds concrete rate','SELECTED_FINITE_TARGET'),
 ('integral-cap','A1.Ex7','A_z(u)≤Bu, u≥0','SELECTED_FINITE_TARGET'),
 ('positive-cap-wait','A1.Ex8','B>0 and finite wait imply s≥e/B','SELECTED_FINITE_TARGET'),
 ('zero-cap-wait','A1.SS1.p3 L2949–2951','B=0 and e>0: empty hit set and stop','SELECTED_FINITE_TARGET'),
 ('finite-sum','A1.Ex9 finite part','Finite accumulated lower bound, no limit','OPTIONAL_FINITE_COROLLARY'),
 ('hitting-bridge','A1.E1 implicit','Concrete continuity/integrability/closed-hit-set/attainment','SOURCE_GAP_TO_DISCHARGE'),
 ('borel-bridge','A1.E1–A1.E2 implicit','Borel S, extended first hit and finite stopped recursion','SOURCE_GAP_TO_DISCHARGE'),
 ('zero-extension','A1.E1–A1.E2 deterministic generalization','e=0 gives s=0; indexed recurrence only','REVIEWER_DERIVED_GENERALIZATION_BOUNDARY'),
 ('iid-clocks','A1.SS1.p2','Independent Exp(1) inputs and positive-clock event','OPEN_FUTURE_PROBABILITY'),
 ('slln','A1.Ex9; A1.SS1.p3','Almost-sure clock-sum divergence','OPEN_FUTURE_SLLN'),
 ('global','A1.SS1.p3','No accumulation and unique global path','OPEN_FUTURE_GLOBAL_PROCESS'),
 ('markov','A1.SS1.p3','Memorylessness and time-homogeneous Markov property','OPEN_FUTURE_MARKOV'),
 ('davis','bib.bib16; A1.SS1.p3','Davis Section 2 bibliographic reference; theorem unread','OPEN_EXTERNAL_REFERENCE'),
 ('invariance','S3.Thmtheorem1; A1.Thmtheorem1','Stationarity, reversal and semigroup results','OPEN_FUTURE_INVARIANCE'),
 ('cost','S3.Thmtheorem3','Stationary bounce count and query cost','OPEN_FUTURE_COST')
]
edges=[]
def edge(parents,child,use,condition='',status='SOURCE_DERIVED_NOT_COMPILER_EVIDENCE'):
    edges.append({'parents':['src76:'+p for p in parents],'consumer':'src76:'+child,'consumer_use_site':use,'conditional_premise':condition,'public_binder_policy':'Proof ingredients are dependency edges; do not promote their conclusions into extra source hypotheses.','status':status,'semantics':'AND of exactly these listed ingredients for this local move, not all routes flattened together.'})
edge(['standing','center-residual'],'lip','S3.Ex7 and A1.SS1.p3 L2932')
edge(['center-residual','flow','rate'],'hazard','A1.E1')
edge(['hazard','flow','reflection'],'recursion','A1.E2 / A1.SS1.p2','Only finite waits update a state; empty hit set stops.')
edge(['flow','energy'],'energy-flow','A1.SS1.p3 L2922')
edge(['reflection','energy'],'energy-bounce','A1.SS1.p3 L2922')
edge(['recursion','energy-flow','energy-bounce'],'energy-prefix','A1.SS1.p3 L2922–2924','Induction over actual active finite steps.')
edge(['energy-prefix','energy'],'norms','A1.Ex5')
edge(['norms','lip','rate','center-residual'],'cap','A1.SS1.p3 L2932–2940')
edge(['cap','hazard'],'integral-cap','A1.Ex7','Finite u≥0; actual concrete hazard integrable.')
edge(['hazard','hitting-bridge','integral-cap'],'positive-cap-wait','A1.Ex8','B>0 and the actual wait is finite.')
edge(['hazard','integral-cap'],'zero-cap-wait','A1.SS1.p3 L2949–2951','B=0 and e>0.')
edge(['positive-cap-wait','recursion'],'finite-sum','A1.Ex9 finite inequality','Active finite prefix and B>0.')
edge(['standing','rate','flow','reflection','hazard','recursion'],'borel-bridge','A1.E1–A1.E2 implicit analytical/Borel bookkeeping')
edge(['hazard','recursion'],'zero-extension','Deterministic evaluation of A.1/A.2 at e=0','Only an indexed finite recurrence; not arbitrary zero-clock global ζ_t.')
edge(['finite-sum','iid-clocks','slln'],'global','A1.SS1.p3 L2959–2970','Actual iid Exp clocks and SLLN are still OPEN.',status='OPEN_FUTURE_SOURCE_ROUTE')
edge(['global','iid-clocks'],'markov','A1.SS1.p3 L2970–2973','Memorylessness/global process work still OPEN.',status='OPEN_FUTURE_SOURCE_ROUTE')
put('source-proof-graph76.json',{'status':'INDEPENDENT_SOURCE_ONLY_GRAPH_OPEN','source_raw_sha256':sha(raw),'implementation_used':False,'nodes':[{'id':'src76:'+i,'source_anchor':a,'mathematical_content':c,'status':s} for i,a,c,s in graph_nodes],'hyperedges':edges,'excluded_bridge_warning':'Davis bibliographic context is not an admitted theorem edge. Invariance/cost are represented OPEN without inventing them as parents of the finite recursion.','independent_topology_approval':'pending; the extractor does not self-certify its graph.'})

inputs=[]
for p in [Path('E:/Samplinglib/AGENTS.md'),Path('E:/Samplinglib/.agents/skills/astis-semantic-roundtrip/SKILL.md'),Path('E:/Samplinglib/docs/theorem-publication-protocol.md'),Path('E:/Samplinglib/docs/proof-digestion-protocol.md')]:
    b=p.read_bytes(); inputs.append({'path':str(p),'bytes':len(b),'sha256':sha(b),'role':'allowed governance/protocol input only'})
own_files=[]
for name in ['source-only-analysis76.md','source-seven-slots76.json','source-coverage76.json','source-proof-graph76.json','raw-manifest76.json','source-dom-index76.json','extract_source76.py','write_source_freeze76.py','run_capture76.py']:
    b=(OUT/name).read_bytes(); own_files.append({'file':name,'bytes':len(b),'sha256':sha(b)})
freeze={
 'schema':1,'id':'fresh-compiled-source76.source-only.freeze76','phase':'SOURCE_ONLY_FROZEN','status':'OPEN_WAITING_FOR_AUTHORIZED_CANDIDATE_PACKET',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer_identity':'/root/fresh_source76','canonical_writer':'/root only; this reviewer writes its new output directory only',
 'anti_anchoring':{'candidate_lean_seen':False,'candidate_header76_seen':False,'old_source_or_math_verdicts_seen':False,'other_reviewer_transcripts_seen':False,'publication_frontier_or_adoption_records_seen':False,'private_global_session_stores_accessed':False,'source_first_extraction':True},
 'primary_source':{'title':'Accelerated High-Accuracy Sampling from a Warm Start via the Proximal Bouncy Particle Sampler','version':'arXiv:2609.06905v1','mathematical_input':'fixed exact RAW snapshot only','raw_manifest':manifest},
 'target':'A.1 (A.1)/(A.2) fixed-reference finite indexed recursion and Ex4–Ex8 deterministic energy/cap/wait ingredients; optional finite-sum corollary only.',
 'seven_slots_file':'source-seven-slots76.json','source_proof_graph_file':'source-proof-graph76.json','exhaustive_inventory_file':'source-coverage76.json','analysis_file':'source-only-analysis76.md','allowed_protocol_inputs':inputs,'own_artifacts':own_files,
 'zero_threshold_ruling':{'scope':'Deterministic generalization of indexed finite recurrence only','wait_at_zero':0,'cap_zero_positive_threshold':'empty hit set, ∞ wait/time, stop','cap_zero_zero_threshold':'wait 0 by inverse-hazard definition; no stochastic no-jumps conclusion','blocking_limit':'Distinct indexed states can share a timestamp. Cannot assert a single-valued global ζ_t for arbitrary zero clocks. Counterexample d=1,V=x²/2,α=β=η=1,y=r=0,z0=(1,1),e1=0 gives z1=(1,-1),T1=T0=0.'},
 'source_gaps_to_discharge':['Concrete hazard continuity/integrability/first-hit attainment','Borel finite-input hitting/active recursion if claimed; no extra theorem premises'],
 'open_future':['iid Exp actual-input composition','positive-clock a.s. event as needed for literal trajectory','SLLN/nonaccumulation','global process/uniqueness/path measurability','memorylessness/Markov','Davis theorem text and applicability','stationarity/reversal/semigroup','half-turn law/kernel','expected bounce/query costs','whole-paper composition/publication'],
 'admission':{'whole_source_admission':False,'verified':False,'lean_or_compiler_used_as_source_evidence':False,'candidate_comparison':'pending explicit root authorization','topology_self_approved':False},
 'foreground_writer':{'writer_pid':os.getpid(),'parent_pid':os.getppid(),'foreground':True,'exit_code':'Not guessed in the running process; run_capture76.py will append the actual Popen.wait result after termination.','receipt':'write_source_freeze76.foreground-exit.json'},
 'preserved_errors':{'extraction_attempt1':'HTMLParser offset attribute collision; original script and complete raw stdout/stderr/actual exit 1 retained.','render_v1':'Non-authoritative mathtext stripping consumed < inside math; source-dom-index76.render-v1.json retained; corrected placeholder rendering preserves inequalities. RAW source never modified.'}
}
put('source-only.freeze76.json',freeze)
print(json.dumps({'status':freeze['status'],'writer_pid':os.getpid(),'raw_sha256':sha(raw),'coverage_counts':json.loads((OUT/'source-coverage76.json').read_text(encoding='utf-8'))['counts'],'candidate_seen':False,'old_verdicts_seen':False,'wait_for_candidate':True},ensure_ascii=False,indent=2))
