from pathlib import Path
import copy, datetime, hashlib, json, os

OUT=Path(__file__).resolve().parent
REVIEWER='/root/fresh_source76'
MODULE='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean'
def sha(b): return hashlib.sha256(b).hexdigest()
def get(name): return json.loads((OUT/name).read_text(encoding='utf-8'))
def put(name,obj):
    data=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    assert not (OUT/name).exists()
    (OUT/name).write_bytes(data)
    return sha(data)
packet=get('candidate-input01.raw')
checks=get('candidate-checks76.json')
source=get('source-coverage76.json')
source_graph=get('source-proof-graph76.json')
intake=get('candidate-intake76.json')
direct=get('direct-review76.foreground-exit.json')
packet_hash=packet['packet_sha256']
binding=packet['publication_binding_sha256']
module_hash=checks['whole_module_RAW_sha256']
assert packet_hash=='1a72e794cd4e22dd03762b4a58d82419d1c49372cd8252f8611ba8335b37580d'
assert binding=='ef7ddf32173166e15704713b04a186c1ae19f324f9d555083a416ed5af930c11'
assert module_hash=='1f1ebc187676e0481247bc2f58ec0bf94b2fc6f02a563b87009a0fe7bfb4910c'

slots={
 'objects':{'original':'Appendix A.1 fixes y and xRef; its actual harmonic flow Φ, residual-rate λ, zero-safe specular bounce S, integrated hazard and initial phase generate (A.1)/(A.2). Ex4–8 use the energy of the original initial phase.','reconstructed':'The decoder reconstructs exactly c,Φ,S,rate,H,C,Λ,τ,next,record,eventTime; active records contain finite time/phase and stopped records contain no phase. These are literal definitions, not caller certificates.','relation':'explicit-elaboration','evidence':'Primary A1.SS1.p1–p3 L2859–2974; S3.E4/(3.4), S2.E4/(2.4). Current module L25–60 and L114–149; BODY L225–237,284–305,325–373. The scalar reflection agrees with R_h p and total division at h=0 gives R_0=I. The guarded Sum representation refines the source stop convention without adding Φ∞.'},
 'domains':{'original':'R^d×R^d with Euclidean norm/inner product; V∈C² and the standing Hessian bounds; nonnegative finite hazard times and an extended waiting time with empty infimum ∞.','reconstructed':'A finite-dimensional real inner-product Borel space E, with no Nontrivial/rank-positive assumption; phase E×E; finite times NNReal; extended times WithTop NNReal; native product and disjoint-union measurable structures and product measurable threshold sequences.','relation':'equivalent','evidence':'Source S1.p1 L350–363, S2.SS2.p1 L613–662. Module L17–24,104–112 and L47–60. Finite-dimensional coordinate-free notation preserves the Euclidean argument, including dimension zero. Energy uses the two component norms separately, not the product max norm. η>0 and βη≤1 are equivalent to the source η∈(0,1/β] because β≥α>0.'},
 'quantifiers':{'original':'Proposition 3.1 quantifies over every fixed y,xRef and every initial phase. A.1 uses E_(n+1), n≥0. The selected ingredient is the concrete finite recurrence, while iid Exp clocks belong to the later stochastic composition.','reconstructed':'For all fixed y,xRef,z₀ and arbitrary e:Nat→NNReal, for every finite n (and n,k where stopped absorption is used). e(n) is consumed in the n→n+1 transition. Joint Borel assertions fix n and vary y,xRef,z₀ and the entire product-measurable threshold sequence.','relation':'explicit-elaboration','evidence':'Source A1.SS1.p2 L2889–2912, Alg1 L1559–1638 and Prop3.1 L1639–1649. Module L55–101 and L144–191; recurrence proof L225–237, measurable finite induction L271–283. The source E_(n+1) is reindexed e(n), not E_n. Arbitrary zeros are explicitly labelled deterministic completion; no law or iid realization is claimed.'},
 'assumptions':{'original':'Source standing assumptions: V∈C², 0<α≤β, αI≤Hess V≤βI everywhere, and η∈(0,1/β]. Fixed inputs y,xRef,z₀ are arbitrary.','reconstructed':'Five typing instances and exactly six analytic callers hα,hαβ,hV,hH,hη,hβη. hH is the quadratic-form expression of the Hessian inequalities. All eleven definitions are expanded and all ten conclusion groups are produced.','relation':'equivalent','evidence':'Current L17–24,104–113; independent fresh literal remap of every 6+11+10 inventory item in candidate-checks76.json. BODY L193–222 calls actual_harmonic_flow_laws, actual_bounce_rate_energy_laws and actual_integrated_hazard_clock_laws with these same six callers. Energy, cap, hitting attainment, Borel next/record and increment are dependency conclusions, never extra theorem premises. No global bounce continuity, finite clock, moment, iid, SLLN, Markov, stationarity or cost premise is smuggled in.'},
 'conclusion':{'original':'The selected A.2 finite update and stop convention, original-energy propagation and Ex4–8 cap/waiting ingredients, with explicit ASTIS measurable stopped representation. The source complete process proposition and Ex9 limit are outside this bounded target.','reconstructed':'Ten groups: initial record; exact active/infinite successor; jointly Borel next, finite record and event time; initial/monotone time; absorbing stop; original-energy and before-clock arc bound; original-cap all-index extended waiting increment and positive-threshold zero-cap stop; zero-threshold bounce and positive finite strict growth.','relation':'equivalent','evidence':'Main statement L61–101, changed goal L151–191 and all BODY L193–409. Ex5 norm bounds are real consumed parent results (ActualBounceRate L170–187); Ex7 and first-hit attainment are proved in ActualHazardClock L151–189,269–341,369–390, then consumed at current L195,209–222. The optional finite-sum corollary in the source-only inventory is not separately exported or credited in this packet.'},
 'scopes':{'original':'The source updates a phase only for a finite wait, stops when the hit set is empty and follows Φ for 0≤t<S. Strictly positive exponential thresholds are the a.s. source situation; infinite processes/Markov/invariance are later claims.','reconstructed':'A stopped record has event time∞ and no phase. The finite value untopD0 is used in the successor only after testing τ≠∞. Active arcs keep t<τ; e=0 yields the indexed state (T,Sz), while positive e plus finite active successor gives T<T′.','relation':'same','evidence':'Definition/guard L136–149; active branches L229–237; Borel branch split L238–270; energy/arcs L284–305,325–335; stopped/all-index increment L338–366; cap-zero L367–373; zero/positive branches L374–401. Arbitrary zeros can yield different indexed phases at the same timestamp, as independently found before candidate access; neither decoder nor authored statement asserts a single physical-time phase for those inputs.'},
 'constant_dependencies':{'original':'Ex6 uses B=√η β √(2E)(√(2ηE)+||c−xRef||), E=H(z₀), at fixed y,xRef; this same finite constant bounds the whole recursively preserved energy shell. Ex8 divides only when B>0.','reconstructed':'C₀=C(y,xRef,z₀) has exactly that formula. henergy transports H(z)=H(z₀); hcap_eq transports C(z)=C₀. The extended increment uses C₀, never a fresh arbitrary C_n. Cap zero is a distinct positive-threshold implication.','relation':'same','evidence':'Source A1.Ex4–Ex8 L2915–2958. Current C formula L126–128; henergy L284–305; hcap_eq L336–337; hincrement L338–366; hzerocap L367–373. Real.toNNReal(e/C₀) is max(e/C₀,0), which equals e/C₀ for e≥0,C₀>0. No cost/truncation/warm-start/accuracy constant appears.'}
}
deltas=[
 {'slot':'objects','kind':'explicit-elaboration','classification':'phase-free-finite-stopped-representation','blocking':False,'source':'Stop the source recursion at an empty hit set and do not define a phase at∞.','lean':'A Sum.inr Unit stopped tag is absorbing and its event time is∞; the finite successor is guarded before untopD0/Φ/S.','evidence':'L47–60,136–149,229–237,319–324. This is a faithful finite representation plus inert post-stop indexing, not an invented phase fallback.'},
 {'slot':'quantifiers','kind':'explicit-elaboration','classification':'declared-deterministic-zero-threshold-extension','blocking':False,'source':'E_(n+1) are independent Exp(1), strictly positive a.s. in the future stochastic construction.','lean':'Arbitrary e(n)≥0 is supplied as deterministic data; zero gives a same-time indexed bounce.','evidence':'The attribution explicitly names the ASTIS extension and reserves iid/nonaccumulation. L99–101,374–401 preserve the independently frozen zero-time limitation. No source repair is being accepted.'},
 {'slot':'domains','kind':'explicit-elaboration','classification':'coordinate-free-Euclidean-Borel-formulation','blocking':False,'source':'Finite-dimensional Euclidean R^d, with no source-added higher regularity or rank-positive condition.','lean':'Finite-dimensional real inner-product Borel E, including rank zero.','evidence':'L17–18,104–106 and the five typing instances. The argument is coordinate invariant and all zero-dimensional cases remain defined.'},
 {'slot':'conclusion','kind':'explicit-elaboration','classification':'Borel-recursion-and-extended-wait-bookkeeping','blocking':False,'source':'Source A.2 is stated by recursion and Ex8 is stated for finite waits.','lean':'The actual successor/record/time maps are jointly Borel, and the increment extends to stopped∞ indices in the standard extended order.','evidence':'L238–283 and338–366; finite hit measurability is derived by the consumed concrete clock theorem. Extended∞ inequalities add no finite-wait or process premise.'}
]
provenance_notes=[{'type':'auxiliary-coordinate-mismatch','blocking_for_semantics':False,'artifact':'candidate-input06.raw neutral-expanded-binders76.json','finding':'All supplied neutral header_RAW_range offsets are stale for the current 5425-byte expanded header. All six caller, eleven definition and ten conclusion literals match current content exactly.','resolution':'No supplied offset is used as evidence. candidate-checks76.json records independently recomputed exact current byte intervals, and all source/property claims below point to the reviewed current module BODY lines.','source_or_publication_mathematical_repair_required':False},
 {'type':'non-normative-comment','blocking_for_semantics':False,'artifact':'Current module L5–9 and consumed clock module L8–9','finding':'Prospective/header-only wording remains in comments although theorem proofs now exist. The actual declarations and reviewed proof, not that stale prose, determine the checked proposition.','resolution':'Recorded as editorial debt only; no frozen code/source change or source repair is proposed in this review.'}]

step_reviews=[
 ('The three concrete producer laws are invoked with the same six analytic callers. Continuity/Borel, H-preservation, zero/positive threshold and waiting claims match the consumed propositions, including their finite/top scope. No certificate is assumed.', ['ActualHarmonicFlow L98–173','ActualBounceRate L107–208','ActualHazardClock L151–189,269–341,369–390']),
 ('Nat.rec gives the exact base and e(n) successor; the top test is equivalent to stopped and otherwise yields exactly the finite flowed/reflected record. Fixed y,xRef are retained.', ['A1.E1–A1.E2; A1.SS1.p2']),
 ('The concrete clock is composed with correct projections ((y,xRef),z,e). Its finite-value extension is Borel; equality to top is Borel. The infinite branch returns the phase-free tag and the finite branch composes actual Φ then S. Product-over-sum is a measurable representation change.', ['ActualHazardClock L327–341','A1.E2 finite/top rule']),
 ('The finite record induction uses measurable e(n) from the product sequence sigma algebra. Event time is finite projection/coercion on the active summand and constant∞ on the stopped summand. n is fixed in each map.', ['A1.E2 finite indexed recursion']),
 ('Induction generalizes the active record. A stopped or top predecessor cannot yield an active successor; the finite case applies H(SΦqz)=H(Φqz)=H(z)=H(z₀). This discharges the concrete induction rather than requiring energy as a caller.', ['A1.SS1.p3 energy preservation paragraph']),
 ('Finite waits are nonnegative; transition to top and absorbing top preserve the extended order. Separate k induction proves stopped absorption. T₀=0 also uses the base definition and final assembly L405, so it is not falsely assigned solely to this step slice.', ['A1.SS1.p2; current L147–149,225–228,405']),
 ('The outgoing harmonic arc remains on the initial energy shell. The same-shell producer cap gives the original C(z₀); its symbolic dependence only on H yields C(z)=C(z₀). The public arc guard t<τ is retained even though the energy formula holds for all finite t.', ['A1.Ex4–Ex7','ActualBounceRate L170–208']),
 ('For C₀>0 the one-clock bound uses the current phase, then hcap_eq replaces its cap with the original one. Finite clocks add the same wait; infinite clocks and already stopped records give the extended inequality to∞. max is harmless because e/C₀≥0.', ['A1.Ex8; current hcap_eq L336–337']),
 ('Under C₀=0 at an active record, hcap_eq supplies zero cap to the concrete one-clock law. Positive e gives τ=∞, then exact branch equivalence stops. No finite-clock premise is inserted.', ['A1.SS1.p3 L2949–2951','ActualHazardClock L386–390']),
 ('e=0 uses τ0=0 and Φ0=id, yielding (T,Sz). For positive e and an active successor, branch equivalence excludes top and one-clock positivity supplies a positive finite wait, hence T<T′. Final assembly contains exactly all ten groups; zero-time indexed states are not identified with a physical process.', ['A1.E1–A1.E2 deterministic extension; source positive-clock case'])
]
steps=[]
for i,(s,(reason,anchors)) in enumerate(zip(packet['candidate_publication_context']['lesson']['steps'],step_reviews),1):
    steps.append({'step':i,'state':'accepted','title':s['title'],'text':s['text'],'formula':s['formula'],'BODY_region':s['lean_source_region'],'reason':reason,'source_or_consumed_dependency_anchors':anchors,'exact_contiguous_BODY_match':True})
whole_module=[
 {'start_line':1,'end_line':15,'status':'reviewed','content':'Imports, namespace/options and explicit finite-only scope; no extra scoped premise.'},
 {'start_line':16,'end_line':101,'status':'reviewed','content':'Only private meaning-carrying statement alias; five typing classes, six analytic callers, eleven literal definitions and ten conclusion groups expanded and checked.'},
 {'start_line':103,'end_line':113,'status':'reviewed','content':'Public theorem repeats exactly the six source analytic callers and five typing classes; no extra provider.'},
 {'start_line':114,'end_line':149,'status':'reviewed','content':'Actual body definitions match the private statement and blind reconstruction; guard prevents phase∞.'},
 {'start_line':150,'end_line':191,'status':'reviewed','content':'change expands the exact conjunction; no weaker target or altered assumption.'},
 {'start_line':193,'end_line':409,'status':'reviewed','content':'All substantive BODY is covered by ten exact contiguous authored steps, with individual semantic reasoning.'},
 {'start_line':410,'end_line':412,'status':'reviewed','content':'Only whitespace and namespace/section closure.'}
]

maps={}
def add(ids,status,lines,reason,parents=None):
    for sid in ids: maps[sid]={'status':status,'current_BODY_or_definition_lines':lines,'compiled_parent_regions':parents or [],'reason':reason}
add(['S1.p1','S1.E1','S2.SS2.p1'],'source-standing-input',[17,24,104,112],'Exact original analytic inputs; η range equivalent because β≥α>0.')
add(['S2.SS1.p1','S2.E4'],'compiled-parent-and-literal-definition',[119,121,194,201,203],'Zero-safe reflection/Borel/orthogonality/energy background; vanilla process context is excluded.',['ActualBounceRate L112–143'])
add(['S2.SS3.SSS0.Px1','S2.SS3.SSS0.Px1.p1'],'notation-context',[122,128],'Positive part and separate Euclidean component norms match; other notation/table has no finite-proof credit.')
add(['S3.SS2.p1','S3.Ex5','S3.E1'],'explicit-context-OPEN',[],'Conditional/stationary target laws are identity context only; no distribution or invariance is proved by this finite target.')
add(['S3.SS2.p4','S3.Ex6','S3.E4'],'literal-fixed-reference-context',[114,123],'Fixed center and gradient residual are literal; source random reference and expected bounce cost remain OPEN.')
add(['S3.Ex7'],'covered-by-compiled-parent',[194,206,208],'The residual Lipschitz bound is proved from the original C²/Hessian callers, then used in the actual energy-shell cap.',['ActualBounceRate L107–110,194–198'])
add(['S3.SS2.p5','S3.E6','S4.E5'],'literal-flow-and-compiled-parent',[115,118,193,198,200],'Actual source harmonic arc formula and energy law.',['ActualHarmonicFlow L69–75,128–173'])
add(['S3.E7'],'contextual-parent-only-no-terminal-credit',[193],'Pure no-bounce half-turn identity exists in the parent; current76 does not construct the terminal stochastic return/kernel.',['ActualHarmonicFlow L166–173'])
add(['S3.SS2.p6','alg1'],'partially-selected-finite-mechanics',[114,149,225,409],'Finite Algorithm1 mechanics are selected; random draws and the full π-horizon return remain OPEN.')
add(['alg1.l1','alg1.l3','alg1.l4'],'covered-fixed-input-initialization',[114,123,144,146,225,228],'Fixed inputs/reference gradient and exact initial record; no query count claim.')
add(['alg1.l5','S3.E8'],'covered-finite-arc-only',[115,118,193,198,200,325,335],'The explicit flow solves the source harmonic ODE in the parent; a complete run until π is still outside current scope.',['ActualHarmonicFlow L128–145'])
add(['alg1.l6','S3.E9','alg1.l7'],'covered-concrete-rate-and-bounce',[119,123,194,201,208,229,237],'Actual residual rate and post-flow reflection; no arbitrary transition witness.')
add(['S3.Thmtheorem1','S3.Thmtheorem1.p1','S3.SS2.p7'],'partial-context-full-Proposition3.1-OPEN',[225,409],'The source quantifiers are preserved for its finite ingredient. Nonexplosive global Markov/stationary process and a.s. terminal return are not admitted.')
add(['A1.SS1.p1','A1.Ex1','A1.EGx1'],'covered-concrete-background',[114,135,193,222],'Source flow/rate/bounce including R0=I, possible discontinuity and Borel alternative; no global bounce continuity caller.',['ActualHarmonicFlow L69–173','ActualBounceRate L112–161'])
add(['A1.SS1.p2','A1.EGx2','A1.E1','A1.E2'],'covered-selected-finite-recursion',[129,149,225,283,306,324,374,401],'Exact source indexing e(n)=E_(n+1), actual first hit, finite/top split, no phase∞, initial record and finite indexed evolution. iid/physical-global reading is excluded.',['ActualHazardClock L269–341'])
add(['A1.SS1.p3'],'covered-finite-estimates-future-OPEN',[193,222,284,373],'Energy propagation/cap/wait pieces mapped below. Ex9 a.s. limit, all-time construction, memorylessness and Davis theorem remain OPEN.')
add(['A1.Ex4'],'literal-energy-and-induction',[124,125,284,305,325,335],'Exact initial H and recursively conserved original energy.',['ActualHarmonicFlow L149–165','ActualBounceRate L141–143'])
add(['A1.Ex5'],'covered-by-consumed-parent',[194,206,208],'Both source norm estimates are proved in the actual bounce/energy parent and feed its cap, not added as current callers.',['ActualBounceRate L170–187'])
add(['A1.Ex6'],'covered-original-cap',[126,128,206,208,325,337],'Exact initial-energy cap; equality of cap at active states is proved, not presumed.',['ActualBounceRate L188–208'])
add(['A1.Ex7'],'covered-by-consumed-clock-parent',[195,218,222],'Concrete integrated bound for every finite u is proved by actual continuous rate/flow integration and feeds the wait theorem.',['ActualHazardClock L151–189'])
add(['A1.Ex8'],'covered-extended-increment',[218,222,336,366],'Concrete finite-clock lower bound transports to original C0 and all-index extended event-time increment; B>0 guard preserved.',['ActualHazardClock L369–385'])
inventory=[]
for original in source['inventory']:
    item=copy.deepcopy(original)
    sid=item['id']
    item['compiled76_projection']=maps.get(sid,{'status':'EXCLUDED_OPEN_OR_CONTEXT','current_BODY_or_definition_lines':[],'compiled_parent_regions':[],'reason':original['reason']})
    inventory.append(item)
assert len(inventory)==131
assert all(x['id'] in maps for x in source['inventory'] if x['disposition']=='NODE')
subclaims=[]
for x in source['subclaim_inventory']:
    y=copy.deepcopy(x)
    sid=y['id']
    if sid=='src76:finite-init': m={'status':'covered-current76','lines':[225,228]}
    elif sid=='src76:finite-stop-and-arcs': m={'status':'covered-current76','lines':[229,237,319,335]}
    elif sid=='src76:finite-energy-induction': m={'status':'covered-current76','lines':[284,305]}
    elif sid=='src76:cap-zero-positive-clock': m={'status':'covered-current76','lines':[367,373]}
    elif sid=='src76:finite-sum-bound': m={'status':'OPEN_OPTIONAL_NOT_CLAIMED','lines':[],'reason':'Source-only optional finite corollary is not separately exported; current target proves increments only. No source/whole-result credit is inferred.'}
    else: m={'status':'OPEN_EXCLUDED','lines':[],'reason':y['reason']}
    y['compiled76_projection']=m
    subclaims.append(y)
bridges=[
 {'id':'src76:hitting-bridge','state':'discharged-by-actual-consumed-dependency','source_anchor':'A1.E1; Ex7–8 implicit','current_lines':[195,209,222],'parent':'ActualHazardClock L151–189,269–341,369–390','evidence':'Joint continuity/integrability, monotone primitive, exact sublevel and top iff, finite hit attainment/equality, positive/zero clocks and extended wait bound are proved for the concrete source rate. No new public premise.'},
 {'id':'src76:borel-bridge','state':'discharged-by-actual-dependency-and-current-proof','source_anchor':'A1.E1–A1.E2 implicit','current_lines':[196,215,238,283],'parent':'ActualBounceRate L131–133; ActualHazardClock L327–341','evidence':'Actual Borel bounce and hitting time compose into guarded product/sum next; primitive-recursive record and time maps follow. No physical path-space/kernel measurability is inferred.'}
]
topology=copy.deepcopy(source_graph)
topology['status']='INDEPENDENT_SOURCE_TO_CURRENT_COMPILED76_TOPOLOGY_ACCEPTED_FOR_BOUNDED_TARGET'
topology['source_first_freeze_sha256']='b543f6543f3d6c8e22bea1986427c41e9b10a45e0f732f143c59c4d75a3f771f'
topology['packet_sha256']=packet_hash
topology['current_module_sha256']=module_hash
topology['comparison_to_other_prospective_maps']={'other_prospective_graph_read':False,'other_prospective_counts_used':False,'independent_basis':'My primary-only source graph and complete 131-block inventory were frozen before this candidate. I mapped its finite mathematical moves to actual BODY and consumed declarations; I did not attempt to reproduce another graph count.','changes_from_my_source_only_graph':['The hitting and Borel gaps are now concretely discharged by the pinned parent/current declarations.','The actual Sum finite/stopped representation, measurable product-over-sum step and finite record/time induction are explicit implementation elaborations.','Original-energy transfer to the cap is explicit at current hcap_eq; waiting increments include stopped∞.','The optional finite sum remains unexported; all future stochastic/global/operator/cost nodes remain OPEN.']}
topology['actual_compiled_consumption']=[{'declaration':x,'BODY_line':193+i,'kind':'actual theorem invocation, not import/source resemblance'} for i,x in enumerate(packet['candidate_publication_context']['lesson']['astis_dependencies'])]
topology['bridge_discharge']=bridges
topology['finite_projection_nodes']=[{'id':'src76:next-Borel-representation','lines':[238,270],'source_role':'Explicit measurable elaboration of A.2 finite/top update'}, {'id':'src76:record-time-finite-induction','lines':[271,283],'source_role':'Finite indexed measurability extension, not all-time path law'}, {'id':'src76:original-cap-transfer','lines':[336,337],'source_role':'C depends on phase only through conserved H; current source estimate composition'}, {'id':'src76:positive-finite-growth','lines':[381,401],'source_role':'Source-positive-clock finite branch; no nonaccumulation conclusion'}]
topology['independent_topology_approval']='This reviewer independently reconstructed the source topology before code access and now reviews the current implementation correspondence. No whole-source root-closure or independent second review of my source-only extraction is claimed.'
topology['coverage_inventory_file']='compiled-source-coverage76.json'
put('compiled-source-topology76.json',topology)
coverage={'schema_version':1,'reviewer':REVIEWER,'state':'accepted-for-selected-finite-target','packet_sha256':packet_hash,'publication_binding_sha256':binding,'source_only_inventory_sha256':sha((OUT/'source-coverage76.json').read_bytes()),'inventory':inventory,'subclaim_inventory':subclaims,'external_citation_inventory':source['external_citation_inventory'],'source_gaps':bridges,'open_optional_subclaims':[x for x in subclaims if x['id']=='src76:finite-sum-bound'],'counts':source['counts'],'no_silent_coverage_omission':True,'scope':'All original 131 blocks and nine subclaims retain their identities and explicit disposition. A represented contextual node is not automatically a proved paper obligation. Twelve external citation occurrences remain context/excluded; Davis theorem was not read or admitted.'}
put('compiled-source-coverage76.json',coverage)
canonical_coverage={'inventory':inventory,'reviewed_nodes':[x['id'] for x in inventory if x['disposition']=='NODE'],'excluded_with_reason':[{'id':x['id'],'reason':x['reason']} for x in inventory if x['disposition']=='EXCLUDED'],'source_gaps':bridges,'alternative_routes':[],'subclaim_inventory':subclaims,'external_citation_inventory':source['external_citation_inventory'],'source_topology':'compiled-source-topology76.json','source_first_freeze_sha256':'b543f6543f3d6c8e22bea1986427c41e9b10a45e0f732f143c59c4d75a3f771f','packet_sha256':packet_hash,'publication_binding_sha256':binding,'reviewer':REVIEWER,'selected_scope_status':'accepted finite deterministic recursion only','future_scope_status':'OPEN','no_whole_Proposition3_1_credit':True,'no_whole_paper_or_Goal_credit':True,'other_prospective_graph_seen':False,'counts_are_coverage_not_progress_metrics':True}
for target in ['cell','publication']:
    put('canonical-'+target+'-source-proof-coverage76.json',{'projection_target':target,'source_proof_coverage':canonical_coverage,'canonical_write_performed':False,'adoption_rule':'Root may adopt these native source-only-derived projections into the existing canonical record without reinterpreting excluded/open context as completed proof.'})

truth_boundary=['iid Exp sequence realization/composition','a.s. positive exponential clock event for literal process reading','SLLN and nonaccumulation','unique all-time physical path/cadlag/path-space law','memorylessness and time-homogeneous Markov law','stationarity/reversal/invariance and semigroup','Algorithm1 terminal xπ sampler and position kernel','main theorem/hypocoercivity/errors/caps and unbounded/expected costs','full actual-input paper composition','aggregate build/tests/publication admission/reader website checks','Exposition Seal/PURIFIED/main/live/whole-paper/Goal credit']
logical={'schema_version':1,'task':'Independent anti-anchored compiled PBPS finite recursion source review76','reviewer':REVIEWER,'formalizer':packet['roles']['formalizer'],'decoder':packet['roles']['blind_decoder'],'source_first_freeze_sha256':'b543f6543f3d6c8e22bea1986427c41e9b10a45e0f732f143c59c4d75a3f771f','candidate_access_authorized_after_source_freeze':True,'prior_verdicts_or_other_reviewer_outcomes_seen':False,'canonical_audit_cell_publication_contents_seen':False,'hash_only_pins_used_as_content':False,'packet_sha256':packet_hash,'packet_RAW_sha256':sha((OUT/'candidate-input01.raw').read_bytes()),'publication_binding_sha256':binding,'primary_RAW_sha256':'d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760','current_whole_module_RAW_sha256':module_hash,'current_module_lines':412,'readable_input_manifest':intake['readable_inputs'],'hash_only_manifest':intake['hash_only_inputs'],'semantic_slots':slots,'typed_semantic_deltas':deltas,'blocking_deltas':[],'repairs':[],'provenance_notes':provenance_notes,'whole_module_coverage':whole_module,'ten_BODY_and_formula_step_reviews':steps,'bridge_discharge':bridges,'source_coverage_artifact_sha256':sha((OUT/'compiled-source-coverage76.json').read_bytes()),'source_topology_artifact_sha256':sha((OUT/'compiled-source-topology76.json').read_bytes()),'source_topology_independence':topology['comparison_to_other_prospective_maps'],'direct_focused_Lean_and_axiom_evidence':direct,'axioms':['propext','Classical.choice','Quot.sound'],'fake_closure_scan':checks['fake_closure_scan'],'verdict':'equivalent-after-elaboration','state':'accepted','accepted_scope':'Actual fixed-reference finite indexed stopped recursion and its ten listed conclusions, including explicit deterministic zero-threshold/Borel/stopped elaborations.','open_truth_boundary':truth_boundary,'no_PROVED_LOCAL_VERIFIED_Goal_transition':True,'canonical_or_ledger_writes':False,'review_basis':'Raw primary mathematics, independent pre-candidate extraction, complete current Lean/consumed parent bodies, decoder reconstruction and current authored formula proof are compared. Compilation/hash equality alone is not semantic evidence.'}
logical_hash=put('review-logical-run76.json',logical)
assert not (OUT/'review-logical-run76.raw.json').exists()
(OUT/'review-logical-run76.raw.json').write_bytes((OUT/'review-logical-run76.json').read_bytes())
evidence='Fresh source-only freeze preceded candidate access; complete current module, all consumed concrete interfaces, seven slots, 131-source-block projection and ten contiguous BODY/formula steps audited. Current exact-module+#print axioms foreground PID '+str(direct['actual_foreground_PID'])+' exited '+str(direct['exit_code'])+' with only propext/Classical.choice/Quot.sound. See named native logical run, source coverage/topology and process receipts; all future stochastic/global/cost/publication gates remain OPEN.'
audit_fields={"state":"accepted",'semantic_slots':slots,'deltas':deltas,'verdict':'equivalent-after-elaboration','repairs':[],'reviewer':REVIEWER,'independent_from_formalizer':True,'independent_from_decoder':True,'review_evidence':evidence,'review_run_sha256':logical_hash,'reviewer_packet_sha256':packet_hash,'publication_binding_sha256':binding}
source_review={'state':'accepted','reviewer':REVIEWER,'independent_from_formalizer':True,'independent_from_decoder':True,'reviewer_packet_sha256':packet_hash,'packet_sha256':packet_hash,'review_run_sha256':logical_hash,'publication_binding_sha256':binding,'verdict':'equivalent-after-elaboration','semantic_slots':slots,'deltas':deltas,'blocking_deltas':[],'no_blocking_delta':True,'repairs':[],'whole_module_reviewed':True,'whole_module_RAW_sha256':module_hash,'whole_module_lines':412,'ten_steps_reviewed':10,'exact_BODY_coverage':[193,409],'source_first_freeze_sha256':logical['source_first_freeze_sha256'],'source_coverage':'compiled-source-coverage76.json','independent_topology':'compiled-source-topology76.json','scope':logical['accepted_scope'],'open_truth_boundary':truth_boundary,'evidence':evidence,'no_PROVED_LOCAL_VERIFIED_Goal_transition':True}
report={'schema_version':1,'state':'accepted','verdict':'equivalent-after-elaboration','packet_sha256':packet_hash,'reviewer_packet_sha256':packet_hash,'packet_RAW_sha256':logical['packet_RAW_sha256'],'publication_binding_sha256':binding,'reviewer':REVIEWER,'review_run_sha256':logical_hash,'logical_run_file':'review-logical-run76.json','named_RAW_payload':'review-logical-run76.raw.json','logical_and_RAW_payload_identical':True,'audit_fields':audit_fields,'source_review':source_review,'typed_provenance_notes':provenance_notes,'whole_module_coverage':whole_module,'ten_BODY_and_formula_step_reviews':steps,'canonical_cell_projection':'canonical-cell-source-proof-coverage76.json','canonical_publication_projection':'canonical-publication-source-proof-coverage76.json','source_or_publication_mathematical_repair_required':False,'writer_pid':os.getpid(),'writer_actual_exit_evidence':'write_compiled_review76.attempt2.foreground-exit.json is recorded by the foreground runner after this process terminates; no exit is self-asserted.','closing_policy':'This report precedes one immutable CLOSED_LAST marker. No writes occur after that marker; external validation is read-only.'}
report_hash=put('compiled-source-review76.json',report)
summary='''# Independent compiled source review76

Accepted for the bounded actual finite indexed stopped recursion, with verdict
`equivalent-after-elaboration`. This accepts neither the complete Proposition
3.1 nor the full paper. No mathematical/source repair is required.

The source-first freeze remains unchanged. The present review independently
compares its primary mathematics and 131-block coverage with the exact current
412-line module, consumed concrete dependency bodies, blind reconstruction and
all ten authored formula/BODY steps. The BODY steps exactly and continuously
cover lines 193–409; setup/meaning-carrying definitions/change/final closures
are additionally reviewed. The canonical current publication binding and
packet hash are recorded in the native JSON fields.

The proof uses the same six original analytic callers and five typing classes.
It derives actual transitions, measurable maps, energy, cap and waiting facts
inside the proof. The stopped tag has no phase. e(n)=E_(n+1), the reference is
fixed, the original energy and cap persist, and the positive-cap increment is
valid even at stopped infinity. Zero cap requires a positive threshold to stop;
zero threshold instead yields the indexed same-time bounce. Positive threshold
and a finite active successor give strict time growth. This preserves the
source-only warning that arbitrary zero thresholds do not define a single
physical-time phase.

Both source-only analytical/Borel bridges are discharged by the actual pinned
clock/bounce producers and current product/sum recursion. Ex5/Ex7 remain real
consumed parent proof steps, not extra premises. The optional finite sum from
Ex9 is not separately exported or credited. iid/SLLN/nonaccumulation, all-time
path, Markov/invariance, terminal output, main/error/cost and whole composition
remain OPEN. Davis was bibliographic context only, never an admitted theorem.

The auxiliary neutral inventory has stale header byte coordinates; its literal
six callers/eleven definitions/ten groups are correct. This review independently
recomputed current coordinates and never used stale offsets as evidence.
Prospective-only comments in compiled files are editorial debt, not a changed
proposition. Neither note requires a mathematical repair overlay.

A fresh foreground check compiled the complete frozen module followed only by
`#print axioms`. It exited zero and reported only propext, Classical.choice and
Quot.sound. The complete native output, exact probe and actual Popen.wait
receipts are preserved. No aggregate/root build, canonical/ledger write or
PROVED_LOCAL/VERIFIED/Goal transition was performed. No Exposition Seal,
PURIFIED, main, live or whole-paper credit is conferred by this review.
'''
assert not (OUT/'compiled-source-review76.md').exists()
(OUT/'compiled-source-review76.md').write_text(summary,encoding='utf-8',newline='\n')
print(json.dumps({'state':'accepted','verdict':'equivalent-after-elaboration','writer_pid':os.getpid(),'packet_sha256':packet_hash,'publication_binding_sha256':binding,'review_run_sha256':logical_hash,'report_RAW_sha256':report_hash,'source_inventory_count':len(inventory),'ten_steps':len(steps),'direct_Lean_PID':direct['actual_foreground_PID'],'direct_Lean_exit':direct['exit_code'],'repairs':[],'blocking_deltas':[],'canonical_writes':False,'close_pending':True},ensure_ascii=False,indent=2))
