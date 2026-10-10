"""Exact distinct-proposer overlay audit, owned-only outputs, no Lean inputs."""
from pathlib import Path
import ast,copy,datetime,hashlib,json
from html.parser import HTMLParser
import re
R=Path('E:/Samplinglib'); O=Path(__file__).resolve().parent; B=O.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(b),bytes=len(b))
def read(p):return json.loads(p.read_bytes())
def put(n,j):
 p=O/n;assert not p.exists(),n;p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode());return pin(p)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
primary=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
freeze=O/'fresh-primary-topology86.json'; assert pin(freeze)['raw_sha256']=='a50b617c244a513777a10b5db9766e47a1bddbd4deb061c1c065fef935d7fee6'
proposal=B/'independent-topology86/proposed-topology-overlay86.json';assert pin(proposal)['raw_sha256']=='a8bff963452d39a1b971a90a4c68c5737ef519d9b7266294483ebf6694d3370d'
p=read(proposal);g0=read(B/'source-proof-graph86.json');i0=read(B/'source-inventory86.json')
assert pin(B/'source-proof-graph86.json')['raw_sha256']==p['original_graph']['raw_sha256']
assert pin(B/'source-inventory86.json')['raw_sha256']==p['original_inventory']['raw_sha256']
g=copy.deepcopy(g0);i=copy.deepcopy(i0); operation_results=[]
reasons={
 'G86-02':'Primary A1.SS2.p3.1 explicitly supplies joint Borel flow/rate/reflection including zero normal. Actual Ex1-3 supply continuous rate and literal map. No S continuity claim.',
 'G86-10':'Fresh P04/P05/P25/P26 identifies Borel time/post-bounce marking as an AND ingredient common to either sufficient density route. The two routes remain OR; no requirement to prove both.',
 'E86-67':'Fresh P05→P09 supports the measurable marked integral; unmarked density alone cannot define/transfer arbitrary Borel marked tests.',
 'E86-68':'Fresh P06→P07 and A1.E7 last-arc survival require unused next-clock conditional independence at the past-dependent current poststate. This is future A7 consumption, not an extra premise for fixed-state first-event density.',
 'E86-69':'Fresh P02→P15: literal total S fixes position and preserves momentum norm, including R0=I.',
 'E86-70':'Fresh P14→P15: exact phase density depends on position and squared momentum norm, so the bounce fixes its value.',
 'E86-71':'Fresh P15→P17 and primary p5.1: rho(Sz)=rho(z) supplies telescoping through jumps. Lebesgue preservation does not substitute for this.',
 'G86-37':'Fresh P15 explicitly separated pointwise bounce density preservation from A4 arc derivative, volume preservation and process invariance. New source ingredient remains OPEN.',
 'I86-31':'Existing density-value item now directly maps its separate source ingredient G37; no statement or assumption change.',
 'I86-09':'Primary p3.1-4 narrates energy conservation, gradient Lipschitz cap and integrated cap immediately around Ex4-7.',
 'I86-10':'Primary p3.5-6 distinguishes zero cap/no jumps, positive cap finite wait bound, and continuing recursion before SLLN.',
 'I86-26':'Primary p3.1 introduces the actual arc used in A4.',
 'I86-25':'Primary p3.2 introduces R-flow and R-S identities displayed in Ex18.',
 'I86-33':'Primary p3.3 introduces the nontrivial forward/pre versus reverse/post jump calculation A5; zero-factor/trivial cases need no new positive-rate binder.',
 'I86-18':'Primary p4.1 introduces the strict ordered time simplex Ex19.',
 'I86-40':'A3 is the full L2 adjoint conclusion and belongs only to excluded global boundary. Adding its source pin grants no credit.',
 'I86-37':'Ex22 is the bounded-test small-time ingredient for the allL2 discussion, not a proof of contraction/density/allL2.'}
for k,op in enumerate(p['operations'],1):
 obj=g if op['file']=='graph' else i
 if op['action']=='append':
  array=obj['nodes'] if op['id'].startswith('G') else obj['edges']
  assert all(q['id']!=op['id'] for q in array);assert op['before'] is None
  array.append(copy.deepcopy(op['after']))
 else:
  if op['field'].startswith('junction.routes['):
   route=op['field'].split('[',1)[1].split(']',1)[0]
   target=next(q for q in obj['junctions'] if q['target']==op['id'])
   record=next(q for q in target['routes'] if q['route']==route);field='ingredients'
  else:
   array=obj['nodes'] if op['id'].startswith('G') else obj['items'];record=next(q for q in array if q['id']==op['id']);field=op['field']
  assert record[field]==op['before'],(k,op['id'],field)
  record[field]=copy.deepcopy(op['after'])
 operation_results.append({'operation':k,'id':op['id'],'field':op['field'],'action':op['action'],'exact_before_match':True,'exact_after_reviewed':True,'decision':'ACCEPT_EXACT_OPERATION','source_reason':reasons[op['id']]})
assert len(i['items'])==40 and len(g['nodes'])==37 and len(g['edges'])==71
assert sum(e['dependency_edge'] for e in g['edges'])==68
assert sum(not e['dependency_edge'] for e in g['edges'])==3
nodes={n['id']:n for n in g['nodes']};edges={e['id']:e for e in g['edges']}
assert len(nodes)==37 and len(edges)==71 and all(e['from'] in nodes and e['to'] in nodes for e in g['edges'])
indegree={n:0 for n in nodes};out={n:[] for n in nodes}
for e in g['edges']:
 if e['dependency_edge']:out[e['from']].append(e['to']);indegree[e['to']]+=1
queue=[n for n in nodes if indegree[n]==0];order=[]
while queue:
 a=queue.pop();order.append(a)
 for b in out[a]:
  indegree[b]-=1
  if indegree[b]==0:queue.append(b)
assert len(order)==37,'dependency cycle'
for old in g0['nodes']:
 assert nodes[old['id']]['classification']==old['classification']
for old in i0['items']:
 assert next(q for q in i['items'] if q['id']==old['id'])['content']==old['content']
j=next(q for q in g['junctions'] if q['target']=='G86-10')
assert j['kind']=='OR_OF_SUFFICIENT_BACKGROUND_ROUTES' and len(j['routes'])==2
for route in j['routes']:
 assert route['kind']=='AND' and 'G86-02' in route['ingredients']
 assert all(any(e['dependency_edge'] and e['from']==ingredient and e['to']=='G86-10' for e in g['edges']) for ingredient in route['ingredients'])
fp=O/'freeze_primary_review86.py';ns={'HTMLParser':HTMLParser,'re':re};tree=ast.parse(fp.read_text(encoding='utf8'))
exec(compile(ast.Module(body=[next(n for n in tree.body if isinstance(n,ast.ClassDef))],type_ignores=[]),str(fp),'exec'),ns)
x=ns['X']();x.feed(primary.read_text(encoding='utf8'))
for a in i0['anchors']:assert sha(x.norm(a['source_id']).encode())==a['normalized_anchor_sha256']
anchor_additions=[]
for old in i0['items']:
 new=next(q for q in i['items'] if q['id']==old['id'])
 for sid in new['source_ids']:
  if sid not in old['source_ids']:anchor_additions.append({'inventory_id':old['id'],'source_id':sid,'normalized_sha256':sha(x.norm(sid).encode()),'decision':'SOURCE_MAPPING_ACCEPTED_NO_PROOF_CREDIT'})
assert len(anchor_additions)==12
group={
 1:'P01',2:'P02/P05',3:'P03',4:'P03',5:'P03/P10',6:'P10',7:'P10',8:'P23 (optional measurable-law context, no process conclusion)',9:'P02/P25/P26',10:'P04/P05/P25/P26',11:'P06',12:'P08',13:'P09',14:'P07',15:'P11',16:'P12',17:'P13',18:'P18',19:'P19',20:'P20',21:'P16',22:'P17',23:'P18',24:'P21',25:'P21',26:'P22 OPEN',27:'P22 OPEN',28:'P24 source context',29:'P22 OPEN',30:'P22 OPEN',31:'P23 separate OPEN',32:'P23 excluded heuristic',33:'P14',34:'P08/P20 convention gap',35:'P25 sufficient route',36:'P26 alternative route',37:'P15 OPEN'}
node_coverage=[{'id':n['id'],'fresh_primary_mapping':group[int(n['id'][-2:])],'classification_retained':n['classification'],'decision':'SOURCE_TOPOLOGY_SUPPORTED_NOT_PROVED'} for n in g['nodes']]
inventory_coverage=[{'id':a['id'],'nodes':a['nodes'],'source_ids':a['source_ids'],'classification':a['classification'],'content_byte_identical_to_original':True,'decision':'SOURCE_SCOPE_SUPPORTED_OR_EXPLICIT_EXCLUSION'} for a in i['items']]
edge_coverage=[]
for e in g['edges']:
 if not e['dependency_edge']: assessment='EXCLUDED_ASSOCIATION_ONLY_NO_IMPLICATION'
 elif e['id']=='E86-63':assessment='OPTIONAL_FIXED_STATE_SUMMABILITY_ROUTE_NOT_UNIFORM_OUTER_ENVELOPE'
 elif e['route'] in ['CDF_ROUTE','HAZARD_TRANSPORT_OR_ALTERNATIVE','REQUIRED_MARKING']:assessment='REQUIRED_AND_INGREDIENT_WITHIN_SELECTED_SUFFICIENT_ROUTE_OR_COMMON_MARK'
 elif e['id'] in ['E86-68','E86-69','E86-70','E86-71']:assessment=reasons[e['id']]
 else:assessment='SUPPORTED_SOURCE_INGREDIENT; FUTURE_CONSUMERS_REMAIN_OPEN; NO_ADDED_THEOREM_BINDER'
 edge_coverage.append({'id':e['id'],'from':e['from'],'to':e['to'],'dependency_edge':e['dependency_edge'],'route':e['route'],'fresh_source_endpoints':[group[int(e['from'][-2:])],group[int(e['to'][-2:])]],'assessment':assessment})
evidence=put('overlay-review.run-evidence86.json',{
 'schema':'astis.distinct-exact-overlay-run86.v1','status':'closed','created_utc':now,'reviewer':'/root/fresh_source78',
 'primary':pin(primary),'fresh_preproposal_freeze':pin(freeze),'exact_overlay':pin(proposal),'original_graph':pin(B/'source-proof-graph86.json'),'original_inventory':pin(B/'source-inventory86.json'),
 'observed_checks':{'exact_operations':len(operation_results),'all_before_after_matches':True,'effective_counts':{'inventory':40,'nodes':37,'relations':71,'dependencies':68,'excluded_associations':3},'DAG_acyclic':True,'all_56_original_primary_anchor_hashes_rechecked':True,'12_inventory_anchor_remappings_exact':True,'no_classification_or_inventory_content_change':True},
 'chronology':['Fresh primary E1/E2/E7/E8/Ex1-23 and exact context reread before proposed overlay.','Fresh independent primary topology frozen; original86 graph not used as validation during reconstruction.','Exact overlay opened, then original before records and additional primary narrative anchors checked.','All exact operations and complete effective topology audited without Lean input or theorem proof work.'],
 'independence':{'original_extraction_author':True,'overlay_creator':False,'root_formalizer':False,'fresh_primary_reconstruction_precedes_overlay':True,'no_Lean_BODY_or_final_verdict_read':True,'no_proposer_decision_text_read':True,'proposer_contamination_disclosure':'Parent disclosed that exact_verify77 displayed parent BODY outside its scope. This audit does not treat proposer run as fully BODY-blind. Its decisions/diagnostics are not a basis. Own primary-first freeze and exact patch semantics are the source basis.','no_self_approval_of_original_extraction':True},
 'command_observations':['Python stdlib HTMLParser re-extracted pinned primary with math alttext, zero source edits.','Native extraction printed exact E1/E2/E7/E8, Ex1-23 and relevant narrative; no implementation files opened.','Exact proposal RAW asserted before JSON inspection.','Own close script asserts every before value, applies operations in memory only, checks graph IDs/counts/DAG/junction branches and source anchor hashes.'],
 'no_header_proof_compiler_shared_state_or_source_completion':True})
decision=put('overlay-review.decision86.json',{
 'schema':'astis.distinct-exact-source-overlay-decision86.v1','status':'closed','created_utc':now,'verdict':'ACCEPT_EXACT_OVERLAY_SOURCE_TOPOLOGY_ONLY','review_run_sha256':evidence['raw_sha256'],
 'exact_proposal_sha256':pin(proposal)['raw_sha256'],'fresh_primary_freeze_sha256':pin(freeze)['raw_sha256'],
 'operation_results':operation_results,'inventory_coverage':inventory_coverage,'node_coverage':node_coverage,'relation_coverage':edge_coverage,'anchor_remapping_coverage':anchor_additions,
 'effective_counts':p['prospective_counts'],'all_before_after_operations_accepted':True,'gaps':[],'required_additional_repairs':[],
 'selected_candidate_audit':{'verdict':'GENUINE_STRICT_NEXT_SOURCE_IMPLICIT_EDGE','content':'Actual finite first-wait density plus post-bounce marked integral, using literal independent Exp product and actual tau/Phi/S under the original six analytic binders.','new_mathematics':'Derived C1-hazard density and finite measure equality, then measurable marking and bounded-test integration. Existing CDF/tail and joint measurability alone do not establish it.','duplicate_check_limit':'Uses earlier own statement-only API receipt as a bounded duplicate check after fresh primary freeze; not a comprehensive negative library theorem or proof of candidate.','no_new_public_binders':True,'bounded_test_M':'M>=0 and Borel bounded-test hypotheses are test-class binders, not extra dynamics/law/invariance/normalizer assumptions.','source_vs_ASTIS':'A1.E7 source density factor is implicit in authors iterating actual clocks. Explicit finite subprobability/marked-law packaging and CDF/FTC justification are ASTIS elaboration, not a full source A7 theorem.'},
 'boundary_preserved':['Future conditional-tail survival is not demanded as a premise for fixed-state first-event density; it remains a later A7 producer.','Both background branches are AND internally and OR with each other; Borel mark is common.','Pointwise rho(Sz)=rho(z) is neither Lebesgue-preservation nor process invariance.','All futureOPEN/excluded node classifications unchanged; G37 explicitly SOURCE_REQUIRED_OPEN.','Source failed terminal limit0 versus actual uncovered initial-phase fallback remains only fixed-parameter AE compatible, not uniform parameters/correlated initialization.','Infinite first wait leaves last live arc; no finite bounce or phase-at-infinity evaluation. Threshold0 is null under actual Exp1; T0/rank0/zero cap retained.','Full path A7, jump-value reversal/path sigma, outer Tonelli, A8, actual invariance, allL2, Markov/restart/semigroup, main/cost/composition remain OPEN.','A3/Ex23/full L2 adjoint/compression are source global boundaries, not new proof credit.'],
 'truth_boundary':'This accepts only a distinct exact source-topology overlay and prospective candidate scope. It is not approval of original graph by its author, a header/StatementSeal, a mathematical proof, or a state transition.'})
opaque=[]
for name,expected in [('decision86.json','74a784150e377d7887806092acf714808f317ed8920dc7ec0ee91c35b0e0af88'),('closed-RAW-manifest86.authoritative.json','7970ce0bde03f67e6ac472f74644d71a8beddb1023768069bebff327e862854e')]:
 q=B/'independent-topology86'/name;assert pin(q)['raw_sha256']==expected;opaque.append(dict(**pin(q),usage='Opaque SHA/size only; content not parsed or used as source verdict.'))
manifest=put('overlay-review.run-manifest86.json',{
 'schema':'astis.raw-exact-overlay-manifest86.v1','status':'closed','created_utc':now,
 'raw_inputs':[pin(q) for q in [primary,proposal,B/'source-proof-graph86.json',B/'source-inventory86.json',B/'statement-api-retrieval86.json']]+opaque,
 'raw_outputs':[pin(q) for q in sorted(O.iterdir()) if q.is_file() and q.name!='overlay-review.run-manifest86.json'],
 'manifest_self_hash_omitted':True,'noncircular':'Evidence binds prior source freeze/inputs; decision binds evidence RAW; manifest binds all exact outputs including decision and scripts, omitting itself.','originals_unchanged':True,'no_shared_or_production_writes':True})
for q in [O/'overlay-review.decision86.json',O/'overlay-review.run-evidence86.json',O/'overlay-review.run-manifest86.json']:print(json.dumps(pin(q)))
