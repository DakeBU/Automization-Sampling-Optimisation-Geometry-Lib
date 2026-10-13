"""Prospective source/header review only; never accesses any implementation85 or math verdict."""
from pathlib import Path
from html.parser import HTMLParser
import ast,copy,datetime,hashlib,json
ROOT=Path('E:/Samplinglib'); PRE=ROOT/'runs/20261007-companion-priority/pbps-transition-kernel-preread85'; OUT=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    p=Path(p); p=p if p.is_absolute() else ROOT/p; b=p.read_bytes()
    return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)}
def read(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def put(n,v):
    p=OUT/n; assert not p.exists(),n; p.write_bytes((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode());return pin(p)
primary=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
assert pin(primary)['raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
parser_path=PRE/'freeze_preread85.py'
cls=next(n for n in ast.parse(parser_path.read_text(encoding='utf-8')).body if isinstance(n,ast.ClassDef) and n.name=='SourceHTML')
ns={'HTMLParser':HTMLParser};exec(compile(ast.Module(body=[cls],type_ignores=[]),str(parser_path),'exec'),ns)
h=ns['SourceHTML']();h.feed(primary.read_text(encoding='utf-8'))
notes=PRE/'source-first-notes85.json';assert pin(notes)['raw_sha256']=='9e9e3737db6cc73e351ffe7daa8ad7dbb124e546f1378a25372ae0dab36fa1c1'
for a in read(notes)['anchors']: assert sha(h.normalized(a['source_id']).encode())==a['normalized_anchor_sha256']
assert 'perpetual non-exclusive' in h.normalized('license-tr')
original_graph=PRE/'source-proof-graph85.json';original_inventory=PRE/'source-inventory85.json'
assert pin(original_graph)['raw_sha256']=='cff28b7b0581c3b5b0219063e422d7b3b70e738ded0e673b035dd73ac32a81be'
assert pin(original_inventory)['raw_sha256']=='b22c1c1cb9c6f2ff86d7182b6821f003058ca101684507ad97873c3a63d50730'
overlay=PRE/'independent-topology85/proposed-minimal-topology-overlay85.json'
assert pin(overlay)['raw_sha256']=='0d4911d3f7f495bc7b1a8f9c944eaaf64032a0ddc3c62b57266440a13e8441d9'
copies={'source-proof-graph85.json':read(original_graph),'source-inventory85.json':read(original_inventory)}
for op in read(overlay)['operations']:
    d=copies[op['file']];s=op['selector']
    if 'field' in s:
        assert d[s['field']]==op['before']; d[s['field']]=copy.deepcopy(op['after'])
    else:
        key='id' if 'id' in s else 'target'; c=d[s['collection']]; ids=[i for i,v in enumerate(c) if v.get(key)==s[key]]
        assert len(ids)==1 and c[ids[0]]==op['before'];c[ids[0]]=copy.deepcopy(op['after'])
effective_graph=PRE/'source-proof-graph85.reviewed-effective.json';effective_inventory=PRE/'source-inventory85.reviewed-effective.json'
assert pin(effective_graph)['raw_sha256']=='2e075d018bd310a9ecb0068e5d98bdaf01d5cf8e623e986a9b071e82b59f1f04'
assert pin(effective_inventory)['raw_sha256']=='bfb2c488d895ef1b3ff488d2f9e51e06e47ea5df9fcf3d4124ab225ffc0e52ee'
graph=read(effective_graph); inv=read(effective_inventory)
assert graph==copies['source-proof-graph85.json'] and inv==copies['source-inventory85.json']
for a in inv['anchors']+inv['additional_anchor_pins']: assert sha(h.normalized(a['source_id']).encode())==a['normalized_anchor_sha256']
for n in graph['nodes']:
    for i in n['source_ids']: assert i in h.text
header=OUT.parent/'header85.proposed.lean';hp=pin(header)
assert hp['raw_sha256']=='b2e1c43e0f7d3877096546181f06e10177486cf126bc98df16d201d5b040bb04' and hp['bytes']==6285
ht=header.read_text(encoding='utf-8');lines=ht.splitlines();assert len(lines)==100
parent=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeMeasurability.lean';pt=parent.read_text(encoding='utf-8')
pp=pt[pt.index('    {E : Type*}'):pt.index('\n\nset_option',pt.index('private def'))]
cp=ht[ht.index('    {E : Type*}'):ht.index('\n      ∧ (∃ K')]
assert pp.strip()==cp.strip()
assert ht.count('    let ')==11 and ht.count('∃ Z :')==1 and ht.count('∃ K :')==1
assert 'Kernel (((E × E) × (E × E)) × ℝ≥0) (E × E)' in ht
for token in ['∀ᵐ sample ∂P','Z y xRef z₀ 0 sample = z₀','Measure.map (Z y xRef z₀ t) P','MeasurableSet B','Measure.dirac z₀','Measurable g','0 ≤ M','Integrable g','Integrable (fun sample => g (Z y xRef z₀ t sample)) P']:
    assert token in ht

item_notes=[
 ('HEADER_OBLIGATION',[20,27],'All six source analytic binders retained exactly: alpha>0,alpha<=beta,C2,both Hessian bounds,eta>0,beta*eta<=1; finite real Borel E includes rank0.'),
 ('HEADER_OBLIGATION',[28,81],'All eleven literal definitions and complete actual80 interpolation/stop contract retained exactly, including index0 initialization and source E_(n+1) adapter.'),
 ('HEADER_OBLIGATION',[62,81],'Joint measurability is concluded; for each fixed deterministic tuple one P-AE event covers every finite time and initialization. No uniform-parameter AE or correlated-clock input.'),
 ('HEADER_OBLIGATION',[82,88],'Full-phase K on joint (y,reference,z,t) has literal actual-P map law and measurable-event law for every finite NNReal t.'),
 ('HEADER_OBLIGATION',[61,88],'Actual Z and K are existential outputs; Kernel type supplies measurable dependence on entire joint parameter/time index. No arbitrary supplied phase/measurability/probability premise.'),
 ('HEADER_OBLIGATION',[82,83],'IsMarkovKernel supplies probability fibers only. Documentation explicitly excludes process Markov/restart/Chapman-Kolmogorov.'),
 ('HEADER_OBLIGATION',[73,90],'Fixed-tuple AE initialization feeds zero-time Dirac law. No raw-sample equality asserted; rank0 and exceptional zero clocks remain covered by inherited total-version convention.'),
 ('HEADER_OBLIGATION',[91,97],'Every real measurable bounded Borel g, every global M>=0 bound, yields kernel and clock integrability and exact expectation transfer for the SAME Z.'),
 ('FUTURE_CONTEXT_NOT_REEXPORTED',[],'Exact q_y and normalized nu_y remain future invariance context. K law needs actual probability P, not supplied nu or stationarity/normalizer premise; no q/nu target is claimed.'),
 ('FUTURE_OPEN_EXCLUDED',[],'Source A.7/A.8 trajectory expansion, Borel reversal and survival identity remain OPEN. K is optional representation for their eventual invariance target, not a mathematical invariance ingredient.'),
 ('FUTURE_OPEN_EXCLUDED',[],'AE quotient operator and Jensen L2 contraction require genuine invariance; no such claim or premise occurs in header.'),
 ('FUTURE_OPEN_EXCLUDED',[],'Independent C_c density and contraction plus bounded-test convergence are separate AND ingredients for fullL2. None is credited by kernel probability or this header.'),
 ('DISTINCT_LAW_INTERFACE',[82,97],'Full phase K at arbitrary finite time and deterministic reference is distinct from ideal81 random-reference/Gaussian returned-position kernel at pi; no implemented exact-reference sampler is claimed.'),
 ('SOURCE_TEST_CLASS_DISTINCTION',[91,97],'Here tests are bounded Borel real g, as in source transition reversal identity. No continuity assumption and no C_b/C_c/allL2 identification. Existing83/84 C_b elaboration is not reproved or replaced.'),
 ('EXCLUDED_OPEN_BOUNDARY',[5,12],'Markov/restart/semigroup/true invariance/pathreversal/fullL2/hypocoercivity/main/cost remain outside target; source memorylessness obligation is not discharged.'),
 ('REUSED_BOUNDED_DUPLICATE_AUDIT',[],'Own source-first85/API audit found no actual full-phase finite-time K; no need broader historical/state review. This header meets the non-wrapper requirement via literal actual contract, initialization law and test integration.')]
ic=[{'id':i['id'],'coverage':v[0],'header_lines':v[1],'evidence':v[2],'graph_nodes':i['graph_nodes']} for i,v in zip(inv['items'],item_notes)]
node_notes=[
 ('EXPLICIT_SOURCE_BINDERS',[20,27],'Original six analytic binders and E domain retained.'),('LITERAL_ACTUAL_ALGORITHM_AND_CONTRACT',[28,81],'Exact complete actual80 Prop prefix.'),('ACTUAL_CLOCK_DEFINITION_DERIVED_PROBABILITY',[28,29],'P is the actual iidExp1 product; probability is derived background, no additional premise or arbitrary-law substitution.'),('RETAINED_PARENT_CONTRACT',[61,81],'Same actual Z, joint measurability, every live arc, uncovered fallback, fixed-tuple common AE allfinite/init.'),('ACTUAL_JOINT_INDEX_OUTPUT',[62,63],'Joint source-implicit parameter/time measurability explicitly retained.'),('SELECTED_SUFFICIENT_PROOF_ROUTE_NOT_PREMISE',[],'id×const clock kernel is one generic sufficient realization, not a public binder or logical necessity; implementation has not been read or written.'),('NEW_PROSPECTIVE_ACTUAL_INTERFACE',[82,83],'Jointly indexed full-phase probability kernel K.'),('NEW_PROSPECTIVE_ACTUAL_INTERFACE',[84,88],'Literal fiber and measurable event laws.'),('NEW_PROSPECTIVE_ACTUAL_INTERFACE',[83,83],'Every index has probability fiber.'),('RETAINED_PARENT_CONTRACT',[73,81],'For fixed tuple, on one common actual-P AE event, Z0=z and every finite time lies on live arc.'),('NEW_PROSPECTIVE_ACTUAL_INTERFACE',[89,90],'Derived zero-time Dirac output.'),('EXPLICIT_TEST_BINDERS',[91,93],'All bounded Borel real g and all nonnegative global bounds M; not additional dynamics/source hypotheses.'),('NEW_PROSPECTIVE_ACTUAL_INTERFACE',[94,97],'Both integrabilities and exact clock expectation transfer.'),('EXISTING_CONTEXT_NOT_REEXPORTED',[],'Exact q/nu normalization is not this interface output and is not added as premise.'),('FUTURE_OPEN_EXCLUDED',[],'Expanded A.7/A.8/p4.4/p5.1 bundle remains future source path-reversal work.'),('FUTURE_OPEN_EXCLUDED',[],'Actual nu invariance unproved by this interface; no supplied invariant-law premise.'),('FUTURE_OPEN_EXCLUDED',[],'AE-safe Jensen L2 contraction not concluded.'),('FUTURE_OPEN_EXCLUDED',[],'Independent compact-continuous L2 density not concluded.'),('EXISTING_CONTEXT_NOT_REEXPORTED',[],'Bounded actual84 outer limit is an existing separate interface; optional K-transfer compatibility was omitted as permitted, not required source repair.'),('FUTURE_OPEN_EXCLUDED',[],'All-L2 strong continuity stays outside header.'),('EXCLUDED_OPEN_BOUNDARY',[],'Process Markov/restart/CK, global invariance/cost/main are not inferred from kernel probability.')]
nc=[{'id':n['id'],'source_ids':n['source_ids'],'coverage':v[0],'header_lines':v[1],'evidence':v[2]} for n,v in zip(graph['nodes'],node_notes)]
edge_notes={
 1:'Source binders support the actual construction retained verbatim.',2:'Actual record/flow definition remains the basis of the retained full phase contract.',3:'Actual iid clocks remain the measure for fixed-parameter AE nonaccumulation/initialization.',4:'Joint phase yields the parameter/clock map, with no measurable-phase assumption.',5:'Selected id×const/map route uses actual P probability; this is a proof realization only.',6:'Selected map route requires joint F; header concludes that from same actual Z.',7:'Selected map route uses identity×constant clock; no generic kernel premise is introduced.',8:'Prospective K output is tied to its literal map law.',9:'Joint actual Z ensures measurable fiber/event identities; source-implicit adapter is explicit.',10:'Probability fibers are an explicit K output, not process Markov.',11:'Actual P probability is the measure-theoretic ingredient for probability fibers.',12:'Retained fixed-parameter common AE group contains Z0=z.',13:'Map law is needed to transfer initial AE equality to law equality.',14:'Actual AE init is retained and Dirac0 is explicitly concluded.',15:'Actual clock probability makes the initial constant pushforward Dirac.',16:'Exact map law is tied to bounded-test expectation transfer.',17:'Actual phase/test composition is measurable; no hidden measurable-clock premise.',18:'Real Borel test and global nonnegative bound M are explicit binders.',19:'Actual P probability supports bounded test integrability, not a supplied law premise.',20:'Exact q/nu normalization remains separate existing context, not reexported or needed as extra K premise.',21:'Path reversal to invariance remains FUTURE_OPEN.',22:'Normalized nu in future invariance is context only, no invariant-law assumption.',23:'Invariance to AE-safe/Jensen contraction remains FUTURE_OPEN.',24:'Contractivity prerequisite for all-L2 extension remains FUTURE_OPEN.',25:'Independent density prerequisite for all-L2 extension remains FUTURE_OPEN.',26:'Bounded outer convergence prerequisite for all-L2 extension remains separate existing84 result.',27:'Excluded optional law-target association: K representation is not logically necessary for source invariance proof.',28:'Excluded optional operator-interface association: test identity names pointwise operator but does not prove AE-safe L2 contractivity.',29:'Excluded no-implication association: probability fibers do not establish Markov/restart/CK.'}
ec=[]
for e in graph['edges']:
    k=int(e['id'].split('-')[1]); status='EXCLUDED_ASSOCIATION' if not e['dependency_edge'] else ('FUTURE_OPEN_NO_CREDIT' if e['classification']=='FUTURE_OPEN' else ('SELECTED_SUFFICIENT_ROUTE_NOT_HEADER_PREMISE' if e['route']=='SELECTED_ID_CONST_MAP' else ('EXISTING_CONTEXT_NOT_REEXPORTED' if k==20 else 'RETAINED_OR_PROSPECTIVE_HEADER_INGREDIENT')))
    ec.append({'id':e['id'],'from':e['from'],'to':e['to'],'dependency_edge':e['dependency_edge'],'route':e['route'],'coverage':status,'evidence':edge_notes[k]})
assert len(ic)==16 and len(nc)==21 and len(ec)==29 and sum(e['dependency_edge'] for e in ec)==26
assert set(r['id'] for r in ic)==set(i['id'] for i in inv['items'])
assert set(r['id'] for r in nc)==set(n['id'] for n in graph['nodes'])
assert set(r['id'] for r in ec)==set(e['id'] for e in graph['edges'])
scope={
 'objects':'Same literal actual iidExp1 P, threshold adapter, initialized stopped recursion and full phase Z. K is full-phase kernel, not returned-position H_y or arbitrary supplied process.',
 'domains':'Finite-dimensional real inner-product Borel E, including rank0; joint deterministic (y,xRef,z0,t) with finite NNReal t. No random-parameter or infinite-time target.',
 'quantifiers':'Exist SAME Z then K; all deterministic indices, all measurable events; for fixed parameter tuple one P-AE event for all finite t and initialization. All Borel real g and M>=0 with global |g|<=M; no uniform-parameter AE or correlated-clock substitution.',
 'assumptions':'Six original analytic binders exactly retained. Eleven literal definitions are lets, not externally supplied hypotheses. Measurable test/global bound are explicit test-class binders. No invariant law, arbitrary probability, phase/measurability, semigroup or density premise.',
 'conclusion':'Retain complete80 joint actual phase contract; add jointly indexed probability K with exact actual-P pushforward/event laws, Dirac0, bounded-Borel integrability on kernel and clock spaces and exact expectation equality.',
 'scopes':'All-finite joint kernel packaging is ASTIS measure-theoretic elaboration. Source terminal-pi failed-limit0 and actual total uncovered-z0 fallback are distinct versions; fixed-tuple AE laws agree. IsMarkovKernel is fiber normalization only. Path-law reversal/invariance/allL2/restart/cost/main remain OPEN.',
 'constant_dependencies':'K has no error/cost/uniform-state/time constants. Eta appears literally in source flow/rate. M>=0 is the test global bound, not added dynamics regularity. No extra normalizer or higher derivative conditions.'}
inputs=[pin(primary),pin(parser_path),pin(notes),pin(original_graph),pin(original_inventory),pin(overlay),pin(effective_graph),pin(effective_inventory),pin(PRE/'candidate-recommendation85.json'),pin(PRE/'api-retrieval85.json'),pin(PRE/'root.topology-adoption85.json'),pin(header),pin(parent)]
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
evidence={'schema':'astis.prospective-header-source85.evidence.v1','status':'closed','created_utc':now,'raw_inputs':inputs,'header':hp,'whole_header_reviewed_lines':[1,100],'actual80_private_Prop_prefix_exact':True,'six_original_analytic_binders':True,'eleven_literal_definitions_count':11,'same_Z_all_outputs':True,'source_inventory_coverage':ic,'source_graph_coverage':{'nodes':nc,'relations':ec,'inventory_items':16,'nodes_count':21,'relations_count':29,'dependency_edges':26,'excluded_associations':3,'gaps':[],'all_junctions':'G7 AND only within selected sufficient id×const/map route. G11/G13 AND ingredients correspond to stated outputs. G16/G20 future AND junctions remain OPEN; invariance, contraction and independent density are not completed.'},'source_anchor_hashes_verified':True,'effective_topology_equals_exact_seven_reviewed_overlay_operations':True,'complete_source_vs_header_scope_review':scope,'source_first_chronology':'Pinned primary related anchors independently reread before inspecting the exact100-line header; preproof source-only notes/topology unchanged. No mathematical reviewer verdict, new85 BODY, StatementSeal or claim read or constructed.','independence':{'source_extractor':True,'exact_overlay_proposer':False,'header_author':False,'proof_writer':False,'final_semantic_review':False,'original_graph_selfapproval':False,'other_math_verdicts_read':False},'compiler_result':'not claimed or used as source evidence','no_shared_writes':True}
ep=put('run-evidence85.json',evidence)
decision={'schema':'astis.prospective-header-source85.decision.v1','status':'closed','verdict':'ACCEPT_PROSPECTIVE_SOURCE_SCOPE','header_raw_sha256':hp['raw_sha256'],'review_run_sha256':ep['raw_sha256'],'reviewer':'/root/fresh_source78','review_kind':'independent primary/source versus complete exact prospective header; not final blind semantic or BODY audit','verdict_reason':'Exact actual80 Prop prefix is retained; SAME actual Z and actual iidExp1 P feed full-phase joint finite-time probability kernel, exact law/events, derived Dirac0 and bounded-Borel integrability/expectation transfer. Source-implicit measure-theoretic packaging is explicit without extra source hypotheses or global process claims. Every16 inventory item,21 graph node and29 relation is mapped, retained or explicitly future/excluded.','blocking_deltas':[],'required_mathematical_repairs':[],'proposed_repairs':[],'coverage_counts':{'inventory':16,'nodes':21,'relations':29,'dependencies':26,'excluded_associations':3,'header_lines':100,'literal_definitions':11,'gaps':0},'truth_boundary':['Prospective statement source acceptance only. No85 BODY/compiler/proof/StatementSeal/SAU/VERIFIED credit.','Source failed-terminal-limit0 versus total uncovered-initial-phase fallback remains a version distinction; only fixed-parameter AE law compatibility follows. Zero waits/raw invalid thresholds and infinite last-live waits inherit the exact80 contract.','Kernel probability does not establish process Markov/restart/Chapman-Kolmogorov. Kernel representation is optional for eventual source invariance proof.','A.7 path-law expansion, reverse Borel change of variables, survival identity, actual invariance, AE-safe Jensen contraction AND independent density/fullL2, hypocoercivity/cost/main/composition remain OPEN.','Original source extractor role disclosed; this is review of a distinct header author, not selfapproval of the original extraction.'], 'run_evidence':ep}
dp=put('decision85.json',decision)
outputs=[pin(Path(__file__)),ep,dp]
mp=put('run-manifest85.json',{'schema':'astis.prospective-header-source85.manifest.v1','status':'closed','m':{'status':'closed'},'raw_inputs':inputs,'raw_outputs':outputs,'selfhash':'omitted; evidence excludes decision and manifest, decision binds evidence exact RAW','owned_scope':OUT.relative_to(ROOT).as_posix(),'source_originals_unchanged':True,'no_header_production_state_ledger_cell_or_shared_edits':True})
for p in inputs+outputs: assert pin(p['path'])==p
print(json.dumps({'verdict':decision['verdict'],'decision':dp,'evidence':ep,'manifest':mp,'coverage':decision['coverage_counts']},indent=2))
