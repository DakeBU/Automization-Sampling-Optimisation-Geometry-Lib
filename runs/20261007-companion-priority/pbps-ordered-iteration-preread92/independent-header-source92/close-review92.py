import json, hashlib, pathlib, re, datetime

ROOT = pathlib.Path('E:/Samplinglib')
BASE = ROOT/'runs/20261007-companion-priority/pbps-ordered-iteration-preread92'
OUT = BASE/'independent-header-source92'
def sha(b): return hashlib.sha256(b).hexdigest()
def binding(p):
    p = pathlib.Path(p)
    b = p.read_bytes()
    return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)}
def write(name,obj):
    p=OUT/name
    with p.open('x',encoding='utf8',newline='\n') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
    return binding(p)

packetpath=BASE/'prospective-header/review-packet92.v2.json'
packet=json.loads(packetpath.read_text(encoding='utf8'))
headerpath=ROOT/packet['header']['path']; raw=headerpath.read_bytes()
assert sha(raw)=='9ad92c3ba89af78f3096342f7663bc547e6c03b6ce8173645cc13030d24bcd1f'
assert len(raw)==6445
sourcepath=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
source=sourcepath.read_bytes()
assert sha(source)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
for k in ['header','source_recommendation','source_graph','source_coverage']:
    assert binding(ROOT/packet[k]['path'])==packet[k]
graph=json.loads((ROOT/packet['source_graph']['path']).read_text(encoding='utf8'))
coverage=json.loads((ROOT/packet['source_coverage']['path']).read_text(encoding='utf8'))
for r in graph['source_regions'].values():
    assert sha(source[r['byte_start']:r['byte_end_exclusive']])==r['raw_sha256']
receiptpath=ROOT/packet['compiler_receipt']
receipt=json.loads(receiptpath.read_text(encoding='utf8'))
assert receipt['exit_code']==0 and receipt['terminal_closed']
assert receipt['header_raw_sha256']==sha(raw)
assert (receiptpath.parent/'Header92.snapshot.lean').read_bytes()==raw

# Byte regions are exact slices of the reviewed prospective header, not reconstructed text.
matches=list(re.finditer(rb'(?m)^\s*let ([^\s:]+)',raw))
assert len(matches)==25
definition_reviews={
'c':('LITERAL_SOURCE','O92','Center y minus eta gradient at fixed reference; no reference draw.'),
'Φ':('LITERAL_SOURCE','O92','Harmonic flow has source sine/cosine signs and sqrt(eta) scaling in both coordinates.'),
'S':('LITERAL_SOURCE_WITH_TOTALIZED_ZERO_NORMAL','O92','Lean real division by zero is zero; when residual normal is zero, subtraction term is zero, giving R_0=identity exactly. Does not assume bounce continuity.'),
'rate':('LITERAL_SOURCE','O92','sqrt(eta) times positive part of momentum-residual inner product; max 0 a=max a 0. Zero normal implies zero rate.'),
'Λ':('LITERAL_SOURCE','I92','Interval integral from 0 to nonnegative elapsed t of actual rate along actual flow.'),
'τ':('LITERAL_SOURCE_VIA_BACKGROUND_DEFINITION','I92','hittingAfter at 0 of Lambda-e in Ici 0 uses closed threshold Lambda>=e; nonempty crossing infimum and empty crossing top are correct. Source clock zero yields wait zero.'),
'next':('LITERAL_SOURCE_PLUS_STOPPED_TOTALIZATION','T92','Absorbing stopped Sum tag; infinite hit produces stopped; finite branch adds elapsed wait and applies S after Phi. untopD zero is used only after top guard.'),
'record':('LITERAL_SOURCE_PLUS_TOTAL_RECURSION','I92','Nat.rec starts live(0,z0); step k consumes clock k and appends actual cumulative time/state.'),
'P':('CANONICAL_REALIZATION_OF_SOURCE_IID_LAW','I92','Literal countable product of unit exponential measures; no arbitrary law or independence provider binder.'),
'ε':('ASTIS_NULL_INPUT_TOTALIZATION','I92','Real.toNNReal clips negative raw coordinates to zero. Coordinates are strictly positive P-a.e.; positivity must be derived, not assumed.'),
'history':('ASTIS_COMPLETE_RECORD_ENCODING','T92','Finite tuple reads every actual record from index 0 through n, preserving all prior times and poststates.'),
'Rec':('ASTIS_CARRIER_ENCODING','T92','Borel disjoint sum (NNReal x phase) + Unit; stopped is no finite event.'),
'Hist':('ASTIS_CARRIER_ENCODING','T92','Borel product Fin(n+1)->Rec, including unrealizable ambient histories for testing.'),
'readTime':('ASTIS_AUXILIARY_TOTAL_OBSERVER','E92','Live cumulative time; stopped zero fallback cannot count as live because A explicitly requires every record live.'),
'Δ':('LITERAL_SOURCE_SIMPLEX','D92','StrictMono of 0 prepended to n real times enforces all strict inequalities; every coordinate less than T. For n=0 vacuous strict comparisons yield singleton even T=0.'),
'Prefix':('ASTIS_DOMAIN_ENCODING','D92','Simplex subtype; no off-simplex prescribed-path extension.'),
'm':('ASTIS_EXACT_REFERENCE_MEASURE_ENCODING','SEC92','Comap of finite product real Lebesgue by simplex inclusion. Measurability of Delta makes inclusion a measurable embedding; map_comap_subtype_coe gives restricted volume, not normalized measure. Empty product volume is Dirac mass one.'),
'zAt':('ASTIS_EXPANSION_OF_PRESCRIBED_SOURCE_PATH','K92','Fin.induction starts at z0 and at i.succ flows by t_i-(0::t)_i.castSucc from preceding zAt i.castSucc, then reflects. Both indices match consecutive records.'),
'K':('ASTIS_COMPLETE_PRESCRIBED_HISTORY','K92','Live record at all indices, initial time zero; later toNNReal times equal source times because strict simplex implies positive values. Retains every poststate.'),
'qReal':('ASTIS_PREFIX_DENSITY_EXPANSION','Q92','Product over each prescribed gap of pre-bounce rate times exp(-segment hazard). Each factor uses preceding poststate, not reflected endpoint rate. Strict gap makes toNNReal exact.'),
'q':('ASTIS_EXTENDED_NONNEGATIVE_ENCODING','Q92','ofReal of entire finite nonnegative product; nonnegativity is an explicit conclusion. Empty product gives one. No terminal survival factor.'),
'A':('ASTIS_AUXILIARY_AMBIENT_HISTORY_GUARD','E92','All live, strictly increasing stored times and every successor time<T. A on arbitrary Hist does not fix first time zero. Its actual pullback does, from record zero. Thus actual B is precisely strict first-n prefix.'),
'H':('ASTIS_LOCAL_ALIAS_OF_LITERAL_HISTORY','T92','Specializes literal history at fixed y,reference,z0,n; no supplied history function.'),
'B':('ASTIS_LITERAL_STRICT_PREFIX_EVENT','E92','Pullback H inverse A. Initial live time0 makes B the strict first-n event; B0=univ. No condition on next wait, no exactly-n event and no pointwise raw-input count gloss.'),
'obs':('ASTIS_AUXILIARY_EVENT_COORDINATE','A92','Reads times of actual records 1..n. Under B these form the strict simplex and reconstruct all records pointwise.')}
audits=[]
for i,m in enumerate(matches):
    name=m.group(1).decode('utf8')
    a=m.start();b=matches[i+1].start() if i+1<len(matches) else len(raw)
    kind,node,reason=definition_reviews[name]
    audits.append({'name':name,'classification':kind,'source_graph_node':node,'verdict':'MATCH','reason':reason,
       'header_region':{'byte_start':a,'byte_end_exclusive':b,'raw_sha256':sha(raw[a:b]),'line_start':raw[:a].count(b'\n')+1,'line_end':raw[:b].count(b'\n')+1},
       'region_note':'Slice begins at literal let and ends at next let; intervening binder/conclusion text is included where present.'})
assert set(definition_reviews)==set(a['name'] for a in audits)

binders=[
('hα','0 < (alpha : Real)','Positive strong-convexity constant.','S1.p1'),
('hαβ','alpha <= beta','Original ordered curvature constants, encoded in NNReal without loss because source values are positive.','S1.p1'),
('hV','ContDiff Real 2 V','Original globally C2 potential.','S1.p1'),
('hH','forall x v, alpha*norm(v)^2 <= D2V(x)[v,v] and D2V(x)[v,v] <= beta*norm(v)^2','Both global Hessian quadratic-form bounds, not a provider for an intended conclusion.','S1.p1'),
('hη','0 < eta','Original positive scale.','S2.SS2.p1'),
('hβη','(beta : Real)*eta <= 1','Equivalent to eta<=1/beta since hα and hαβ imply beta>0; no assumption weakened.','S2.SS2.p1')]

inputs=[sourcepath,packetpath,headerpath,receiptpath,receiptpath.parent/'Header92.snapshot.lean',receiptpath.parent/'stdout.log',receiptpath.parent/'stderr.log',
 ROOT/packet['source_recommendation']['path'],ROOT/packet['source_graph']['path'],ROOT/packet['source_coverage']['path'],
 ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Comap.lean',ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Restrict.lean',
 ROOT/'.lake/packages/mathlib/Mathlib/Probability/Process/HittingTime.lean',ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/Pi.lean',
 ROOT/'.astis/toolchain/lean-4.33.0-windows/src/lean/Init/Data/Fin/Lemmas.lean',
 ROOT/'docs/proof-digestion-protocol.md',ROOT/'docs/theorem-publication-protocol.md',ROOT/'.agents/skills/astis-semantic-roundtrip/SKILL.md']
run=write('review-run92.native.json',{'record_kind':'independent-prospective-header-source-review-run','reviewer':'/root/primary_source91',
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'primary_first_checkpoint':binding(OUT/'primary-first-header92.native.json'),
 'inputs':[binding(p) for p in inputs],'scope':'Source review of prospective proposition and definition semantics before proof search. No production proof read to determine topology; no proof body provided. Source candidate previously authored by this reviewer; independently reviewed v2 topology is context, not evidence replacing direct source inspection.',
 'source_target_acceptance_not_used_as_mathematical_authority':True,'compiler_receipt_scope':'Existing compile2 receipt and exact matching snapshot inspected; no independent compiler rerun. Exit0 is elaboration of Prop definition only.',
 'mathlib_read_scope':'Definitions needed to interpret comap, hittingAfter, finite product volume and Fin.induction; not implementation-driven proof topology.'})

decision={
 'schema_version':1,'record_kind':'independent-prospective-header-source-decision','reviewer':'/root/primary_source91',
 'verdict':'SOURCE_HEADER_ACCEPTABLE_FOR_STATEMENT_SEAL','meaning':'Exact prospective proposition matches source-derived bounded strict-prefix target with the explicitly listed ASTIS encodings and extensions. This approves source semantics of the header only; it is neither a seal operation nor proof/theorem verification.',
 'header':binding(headerpath),'packet':binding(packetpath),'reviewer_run':run,
 'source':binding(sourcepath),'source_regions':graph['source_regions'],
 'source_version_license':{'version':'arXiv:2609.06905v1','license':'arXiv non-exclusive distribution license','verification':'Previously checked official fixed-version page/license and local banner; fixed private primary hash reverified here. No full raw source copied.'},
 'analytic_binder_audit':[{'name':n,'classification':'ORIGINAL_SOURCE_ASSUMPTION','meaning':s,'reason':r,'source_region':a,'verdict':'MATCH'} for n,s,r,a in binders],
 'typing_and_quantifier_audit':[
 {'item':'E, NormedAddCommGroup, InnerProductSpace Real, FiniteDimensional','classification':'EXPLICIT_ASTIS_EXTENSION','result':'Coordinate-free finite-dimensional real Hilbert presentation includes rank zero. Source states Euclidean R^d; do not attribute rank-zero/general carrier wording to authors.'},
 {'item':'MeasurableSpace E, BorelSpace E','classification':'STANDARD_SOURCE_MEASURABLE_STRUCTURE','result':'Borel structure fixed by topology; not an additional analytical regularity premise.'},
 {'item':'V, alpha beta : NNReal, eta : Real','classification':'SOURCE_DATA_WITH_EQUIVALENT_ENCODING','result':'NNReal curvature constants plus positivity/order recover source real constants; eta remains real with original bounds.'},
 {'item':'n : Nat, T : NNReal','classification':'TARGET_INDEX_AND_HORIZON','result':'Arbitrary finite deterministic depth and nonnegative finite horizon; no random index or infinity horizon.'},
 {'item':'y, xRef, z0','classification':'ARBITRARY_FIXED_SOURCE_PARAMETERS','result':'No initial equilibrium, reference sampling, warm start or moment premise.'},
 {'item':'F : Hist n -> ENNReal, Measurable F','classification':'EXPLICIT_ASTIS_TEST_EXTENSION_AND_DOMAIN','result':'Every nonnegative extended measurable whole-history test, not only bounded path tests printed at A7. Measurable F specifies test class; no integrability assumption or density-provider premise.'}],
 'literal_definition_audit':audits,
 'conclusion_audit':[
 {'item':'MeasurableSet Delta and A; Measurable H,B,obs','nodes':['D92','M92','E92'],'result':'Required structural consequences retained as conclusions. A is auxiliary ambient guard; B is the actual event.'},
 {'item':'joint Measurable K and q','nodes':['M92','K92','Q92'],'result':'Product argument ((y,xRef),z0),t is correct. Fixed V,eta,n,T; no joint regularity in V or eta claimed.'},
 {'item':'qReal nonnegative','nodes':['Q92'],'result':'Conclusion supplied for every simplex point, consistent with sqrt(eta) positive and positive-part rate.'},
 {'item':'forall w in B, exists t with t.val=obs w and H w=K t','nodes':['A92','K92','I92'],'result':'Correct pointwise full-history identification on literal strict-prefix guard. Initial record zero plus cumulative update supplies positive gaps even on arbitrary clipped raw inputs. This is not pointwise event-count equivalence.'},
 {'item':'pushforward equality','nodes':['PREFIX92'],'result':'Actual H pushforward of unnormalized P restricted B equals prescribed K pushforward of q-density on simplex comap measure.'},
 {'item':'all nonnegative extended history-test identity','nodes':['PREFIX92'],'result':'Equivalent law form; correct product F(K)*q and ENNReal 0*infinity convention. No conditioning by P(B).'},
 {'item':'integral q=P(B), P(B)<=1','nodes':['PREFIX92','B92'],'result':'Mass consequence of law and canonical probability. No strictly positive event probability required.'}],
 'edge_case_audit':[
 'n=0: A requires one live record, StrictMono is vacuous; actual H0 is live(0,z0), so B=univ. Delta0 singleton and m0 Dirac mass1; K0 equals H0 and q0=1, including T=0.',
 'n>0,T=0: simplex empty, actual strict-positive-time event empty; no positive event mass assumption.',
 'Zero hazard/rank zero: positive clocks have infinite wait, stopped records excluded; zero raw clock may give wait0 but cannot create strict prefix, and source-count gloss is only a.e.',
 'Finite raw positive or zero clocks with strict actual prefix reconstruct pointwise; no nonaccumulation needed at deterministic finite depth.',
 'Zero residual: S fixes momentum and rate zero; bounce Borel suffices, continuity is not imported.',
 'Simplex comap is not silently zero: inclusion is injective and images of Borel subtype sets are Borel because Delta is Borel. Required identification is a proof dependency, not supplied binder.' ],
 'source_proof_graph_mapping':{'graph_binding':binding(ROOT/packet['source_graph']['path']),
   'target':'PREFIX92','direct_object_nodes':['H92','O92','I92','T92','D92','K92','Q92','E92'],
   'must_be_proved_or_reused_not_assumed':['M92','W92','B92','A92','J92','FUB92','SEC92','PREFIX92'],
   'and_or_preserved':'Preferred absolute-coordinate induction uses base and successor with genuine one-step law, complete append, Tonelli and simplex sections. Relative-vector plus triangular transport remains an alternative, not a simultaneous requirement. Header commits to a statement, not implementation route.',
   'genuine_consumer':'Full-history law can feed terminal survival at T-last_time and prescribed path tests; PREFIX92 -> TERM92 -> A7 still requires SURV92, ALG92, PATH92, COUNT92 and a signed-series assembly route.',
   'open_future_nodes':['SURV92','ALG92','END92 when endpoint conventions require','PATH92','COUNT92','TERM92','CAP92 or MASS92','A7'],
   'existing_actual_input_results':'Nonaccumulation78 and coverage79 are preserved; future path/count identification must consume them accurately. They are not conflated with the still-open full A7 identity.',
   'not_a_Lean_dependency_graph':True},
 'source_coverage_audit':{'binding':binding(ROOT/packet['source_coverage']['path']),'rows_checked':len(coverage['coverage']),
   'all_region_hashes_reverified':True,'dispositions_preserved':True,
   'source_gaps':'C92-10 total stopped representation; C92-21 omitted iteration; C92-22 simplex section product measure; C92-24 n0 and history tests are explicitly supplied as header targets/definitions, still unproved. C92-25 final survival, C92-26 full path/count/endpoint, C92-41 alternative summation remain outside this header.',
   'specific_v2_dispositions':'Residual Lipschitz belongs to ENERGY92 source consequence, not extra binder. Full-force recombination and bounce involution remain excluded prefix dependencies; zero-normal zero-rate retained in O92 literal definition.',
   'excluded_claims':'Generator/invariance/reversal/Markov/averaged-kernel/global uniqueness/operator/cost results are not asserted by this header.'},
 'assumption_delta':[],
 'explicit_ASTIS_extensions':['Arbitrary finite-dimensional real inner-product carrier, including rank zero','Nonnegative possibly infinite measurable whole-history tests','Canonical product-clock realization and clipping on P-null raw negative inputs','Absorbing Sum stopped totalization and finite history/observer encodings','Finite-prefix proposition unpacking omitted source iteration, including Borel and pointwise structural conclusions'],
 'repair_proposals':[],
 'proof_obligations_not_discharged':['Every mathematical conjunct of the prospective Prop still needs proof or exact compiled reuse.','Simplex Borel/comap reference and n0 mass must be proved/instantiated.','Joint measurable finite recursion and q; actual/prescribed pointwise identification.','Whole-history induction using actual one-step law, correct simplex sections and Tonelli.','Canonical P probability and elementary mass corollaries.'],
 'limitations':['No proof BODY exists. compile2 confirms proposition elaboration only.','No decoder reconstruction was supplied for this prospective stage; this is direct header/source review, not a completed compiled-theorem semantic round trip.','Unused source premise warnings reflect that this is a Prop-valued definition. Preserve all six parameters in the future proved source-facing theorem.','No terminal survival, exact-count law, full-path A7, physical-time restart, invariance, main theorem, composition or whole-paper completion is claimed.'],
 'canonical_state_changed':False,'actual_theorem_verified':False,'creator_topology_self_approval':False}
dec=write('source-decision92.native.json',decision)
manifest=write('closed-RAW92.native.json',{'record_kind':'closed-raw-prospective-header-source-review-manifest','reviewer':'/root/primary_source91',
 'inputs':[binding(p) for p in inputs],
 'outputs':[binding(OUT/'primary-first-header92.native.json'),run,dec,binding(OUT/'close-review92.py')],
 'closure':'Every listed RAW byte digest checked at closure; manifest excludes itself to avoid circular binding. All outputs newly appended in owned independent-header-source92 directory. No existing evidence/canonical/Lean file changed.',
 'decision':'SOURCE_HEADER_ACCEPTABLE_FOR_STATEMENT_SEAL','proof_claim':False})
for p in inputs: assert binding(p) in json.loads((OUT/'review-run92.native.json').read_text(encoding='utf8'))['inputs']
print(json.dumps({'decision':dec,'run':run,'manifest':manifest},indent=2))
