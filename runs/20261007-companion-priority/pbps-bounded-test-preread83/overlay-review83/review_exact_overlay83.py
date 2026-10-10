"""Independent review of distinct proposer's exact source-topology overlay only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,copy
R=Path('E:/Samplinglib')
B=R/'runs/20261007-companion-priority/pbps-bounded-test-preread83'
O=B/'overlay-review83'
P=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
X=B/'independent-topology83/proposed-minimal-topology-overlay83.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text('utf8'))
def raw(p):return {'path':p.as_posix(),'raw_sha256':sha(p),'bytes':p.stat().st_size}
def save(n,x):
 p=O/n;assert not p.exists(),n;p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'));return p
assert sha(P)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert sha(X)=='6a8870abda762b76523c2bc9fef7dac87cef1b7dd64c1c034865745abbb702a6'
x=load(X);canonical=hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
assert canonical=='658ac15013e06953943e0be38406784d60c4ad301df65adf2a4ed12297af4fde'
assert x['proposer']=='/root/exact_verify77' and len(x['patches'])==3
frozen=load(B/'source_freeze83.closed-raw-manifest.json')
for a in frozen['raw_inputs']+frozen['raw_outputs']:assert sha(Path(a['path']))==a['raw_sha256']
g=load(B/'source_proof_graph83.json');s=load(B/'optional-route-topology-supplement83.json')
assert sha(B/'source_proof_graph83.json')==x['original_graph']['RAW_sha256']
assert sha(B/'optional-route-topology-supplement83.json')==x['original_supplement']['RAW_sha256']
effective=copy.deepcopy(g['edges']+s['added_edges']);byid={e['id']:e for e in effective}
for edgeid,patch in zip(['E83-29','E83-30','E83-28'],x['patches']):
 e=byid[edgeid]
 if edgeid!='E83-28':
  assert e['status']==patch['before']=='OPTIONAL_OR'
  assert patch['after']=='OPTIONAL_ROUTE_AND_INGREDIENT';e['status']=patch['after']
 else:
  assert e==patch['before']
  assert patch['after']['dependency_edge'] is False
  e.clear();e.update(patch['after'])
assert byid['E83-24']['status']=='OPTIONAL_OR'
assert byid['E83-28']['status']=='EXCLUDED_BOUNDARY_ASSOCIATION'
nodeids={a['id']for a in g['nodes']}
deps=[e for e in effective if e.get('dependency_edge',True)]
assert len(nodeids)==17 and len(effective)==30 and len(deps)==29
assert all(e['ingredient']in nodeids and e['consumer']in nodeids for e in effective)
incoming={n:0 for n in nodeids};outgoing={n:[]for n in nodeids}
for e in deps:incoming[e['consumer']]+=1;outgoing[e['ingredient']].append(e['consumer'])
queue=[n for n in nodeids if incoming[n]==0];visited=[]
while queue:
 n=queue.pop();visited.append(n)
 for k in outgoing[n]:
  incoming[k]-=1
  if incoming[k]==0:queue.append(k)
assert len(visited)==17
j={a['id']:a for a in x['junctions']}
assert j['J83-main-expectation']['AND_edges']==['E83-18','E83-19','E83-20']
assert j['J83-optional-tail']['AND_edges']==['E83-21','E83-22','E83-23','E83-29','E83-30']
assert j['J83-expectation-alternatives']['OR_routes']==[{'junction':'J83-main-expectation'},{'edge':'E83-24','producer':'G83-13'}]
assert all(byid[k]['consumer']=='G83-12'for k in j['J83-main-expectation']['AND_edges'])
assert all(byid[k]['consumer']=='G83-13'for k in j['J83-optional-tail']['AND_edges'])
inputs=[P,X,B/'source_inventory83.json',B/'source_proof_graph83.json',B/'optional-route-topology-supplement83.json',B/'bounded_candidate83.json',B/'source_freeze83.closed-raw-manifest.json']
now=datetime.now(timezone.utc).isoformat()
evidence=save('overlay-review83.run-evidence.json',{'schema':'exact-topology-overlay-review-evidence-v1','created_utc':now,'status':'closed','reviewer':'/root/fresh_source78','proposer':x['proposer'],
 'raw_inputs':[raw(p)for p in inputs],'overlay_canonical_sha256':canonical,
 'primary_first_chronology':'Primary RAW and source Ex22/p6.1-p6.2/PropA.1/p3.7/measurability reread and parsed before opening exact overlay; then original frozen graph/supplement and bounded source-only candidate checked. No proposed83 Lean/header/proof or proposer verdict opened.',
 'checks':{'exact_before_values_match':True,'patches_applied_in_memory_only':True,'original_frozen_bytes_unchanged':True,'junction_edges_match':True,'dependency_graph_acyclic':True,'relation_rows':30,'dependency_rows':29,'boundary_associations':1},
 'noncircular_rule':'Evidence omits own/result/manifest hashes; decision binds exact evidence RAW and final manifest binds both without selfhash.'})
decision=save('overlay-review83.decision.json',{'schema':'independent-exact-source-topology-overlay-decision-v1','created_utc':now,'status':'closed','reviewer':'/root/fresh_source78','proposer':x['proposer'],
 'verdict':'ACCEPT_EXACT_TOPOLOGY_CLARIFICATION_ONLY','reviewed_overlay':raw(X),'overlay_canonical_sha256':canonical,'review_run_sha256':sha(evidence),
 'scope':'Review of distinct exact proposal only; original extraction authorship disclosed, no self-approval of original graph and no83 theorem/StatementSeal/proof/completion or source repair credit.',
 'patch_decisions':[
  {'id':'PATCH83-E29','selector':x['patches'][0]['selector'],'decision':'accept','blocking':False,'reason':'Freeflow continuity is jointly required inside the optional derivation of positive-threshold phase tails; it is not an independently sufficient OR alternative to vanishing hazard. Exact new status removes that ambiguity.'},
  {'id':'PATCH83-E30','selector':x['patches'][1]['selector'],'decision':'accept','blocking':False,'reason':'Vanishing q_t from hazard0 continuity combines with phase-flow defect bound and freeflow convergence. AND within this optional branch, not OR against freeflow convergence.'},
  {'id':'PATCH83-E28','selector':x['patches'][2]['selector'],'decision':'accept','blocking':False,'reason':'EXCLUDED_BOUNDARY_ASSOCIATION and dependency_edge=false correctly prevent an L2-to-Markov/restart/invariance implication. Source p3.7 constructs Markov via memorylessness first; PropA.1 assumes those transition operators. No dependency or conclusion follows from scope adjacency.'}],
 'junction_decisions':{'preferred_route':'E18 AND E19 AND E20: hazard smalltime, actual integrated test defect estimate and deterministic test-flow limit are sufficient together.',
 'optional_route':'E21 AND E22 AND E23 AND E29 AND E30: actual probability/measurability, continuous bounded test, phase-flow defect bound, freeflow continuity and vanishing hazard are jointly present; bounded integrability also follows through G09.',
 'between_routes':'Preferred complete branch OR optional complete epsilon/delta branch. E24 stays OPTIONAL_OR; optional branch never becomes an extra mandatory premise of preferred branch.'},
 'source_reasoning':{'anchors':['A1.Ex22','A1.SS1.SSS0.Px1.p6.1','A1.SS1.SSS0.Px1.p6.2','A1.SS1.p3.7','A1.Thmtheorem1','A1.SS2.p3.1'],
 'C_c_vs_C_b':'Literal source uses compactly supported continuous phase tests. Bounded continuous real tests C_b are an explicit ASTIS elaboration of the pointwise ingredient. Overlay changes no test class and does not silently attribute C_b wording to source.',
 'nonnegative_M':'Test bound is exists M>=0, forall z,abs(f(z))<=M; this defines bounded test, not a seventh dynamical hypothesis. It yields integrability on actual probability input and nonnegative2M domination, including M0.',
 'no_AS_DCT_shortcut':'Convergence in probability alone does not provide samplewise almost-sure convergence. Optional route uses local continuity and bounded epsilon/delta integration. Source later DCT is outer initial-phase L2 integration, requiring its own measurable probability/integrable domination; not licensed by a naive clock-sample DCT.',
 'limits':'Fixed deterministic y,r,z0 and finite NNReal time approach0 only. No arbitrary correlated random parameter substitution, uniform parameter/state/time consequence, full L2 semigroup, Markov, invariance or cost claim.'},
 'topology_counts':{'inventory_unchanged':30,'nodes_unchanged':17,'relation_rows_unchanged':30,'dependency_rows':29,'excluded_boundary_associations':1,'dependency_acyclic':True},
 'independence':{'authored_original_extraction':True,'authored_exact_reviewed_overlay':False,'distinct_overlay_proposer':'/root/exact_verify77','no_proposer_decision_or_other_review_verdict_read':True,'no83_Lean_header_proof_seen':True,'primary_read_first':True,'owned_review_outputs_only':True,'no_original_graph_or_supplement_mutation':True,'no_shared_state_or_proof_credit':True},
 'blocking_deltas':[],'required_overlay_repairs':[],'source_theorem_repairs':[],'StatementSeal':False,'VERIFIED':False})
manifest=save('overlay-review83.closed-raw-manifest.json',{'schema':'acyclic-closed-raw-review-manifest-v1','created_utc':now,'status':'closed','raw_inputs':[raw(p)for p in inputs],
 'raw_outputs':[raw(Path(__file__).resolve()),raw(evidence),raw(decision)],'self_hash_omitted':True,
 'acyclic_hash_binding':'Inputs -> run evidence -> decision; manifest lists exact input/evidence/decision/script RAWs, omits its own selfhash. No backward reference from evidence to decision/manifest.'})
for a in load(manifest)['raw_inputs']+load(manifest)['raw_outputs']:assert sha(Path(a['path']))==a['raw_sha256']
for a in frozen['raw_inputs']+frozen['raw_outputs']:assert sha(Path(a['path']))==a['raw_sha256']
assert load(decision)['review_run_sha256']==sha(evidence)
print(json.dumps({'status':'closed','verdict':load(decision)['verdict'],'outputs':[raw(p)for p in [decision,evidence,manifest]]},indent=2))
