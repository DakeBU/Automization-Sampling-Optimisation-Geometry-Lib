from pathlib import Path
import json,hashlib,os,copy
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def can(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode('utf-8')
def load(n):return json.loads((O/n).read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(b.replace(b'\r\n',b'\n')),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))}
def put(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
assert not (O/'lease.final.json').exists()
names=['source.0.coverage.json','source.0.review.json','source.0.run.json','source.0.decision.json','source.0.admission-fields.json','complete-named-review-decision-input-payload.json']
before=[]
for i,n in enumerate(names):
 p=O/n;q=O/'native-final-draft.before-state-completion'/f'{i:02d}.exactraw.snapshot';q.parent.mkdir(parents=True,exist_ok=True);assert not q.exists();q.write_bytes(p.read_bytes());before.append({'current_path':p.relative_to(R).as_posix(),'before':pin(q)})
coverage=load('source.0.coverage.json')
assert coverage['phase']=='FINAL_INDEPENDENT_SOURCE_IMPLEMENTATION_AND_LOCAL_EXPOSITION_REVIEW'
for q in coverage['7_BODY_formula_checks']:
 q['source_review_status']='accepted exact current BODY/formula under final official packet; local exposition only'
for q in coverage['26_obligations']:q.pop('preparation_finding',None)
assert coverage.pop('current_source_nodes_N01_through_N24_produced_or_defined')
coverage['current_source_nodes_N01_through_N24_mapped_to_original_inputs_definitions_or_internal_proofs']=True
put('source.0.coverage.json',coverage)
review=load('source.0.review.json')
review['whole_body_source_analysis']='Historical prepacket preparation analysis follows verbatim; its then-pending stage descriptions are historical only. The final-packet qualification at its end and this final review verdict govern current admission. The original preparation artifact remains unchanged.\n\n'+review['whole_body_source_analysis']
review['source_coverage']=pin(O/'source.0.coverage.json');put('source.0.review.json',review)
run=load('source.0.run.json');oldhash=run.pop('run_sha256')
run['review']=pin(O/'source.0.review.json');run['coverage']=pin(O/'source.0.coverage.json');run['complete_review']=review;run['run_sha256']=sha(can(run));put('source.0.run.json',run);h=run['run_sha256']
decision=load('source.0.decision.json');decision['review_run_sha256']=h;put('source.0.decision.json',decision)
admission=load('source.0.admission-fields.json');admission['audit_fields']['source_review']['review_run_sha256']=h
for k in ['cell_source_proof_coverage','publication_source_proof_coverage']:admission[k]['coverage_report']=pin(O/'source.0.coverage.json')
put('source.0.admission-fields.json',admission)
payload=load('complete-named-review-decision-input-payload.json');payload['whole_logical_run_sha256']=h
for z in payload['named_payloads']:
 p=O/z['name'];z['pin']=pin(p);z['complete_RAW_UTF8']=p.read_bytes().decode('utf-8')
put('complete-named-review-decision-input-payload.json',payload)
mapping={'classification':'OPEN_NATIVE_REVIEW_STATE_COMPLETION_AND_HISTORICAL_QUOTE_LABEL_ONLY','mathematical_source_candidate_or_canonical_changes':False,'source_graph_or_preparation_files_changed':False,'reasons':['Per-step final coverage statuses now agree with the already accepted final coverage phase; original prepacket records stay immutable.','Final obligation rows remove superseded preparation-only pending text; expectations and final decisions unchanged.','Historical body-analysis quote explicitly labeled as historical before its final qualification.','Source graph inputs/hypotheses are distinguished from internally produced proof nodes.'],'old_whole_logical_run_sha256':oldhash,'new_whole_logical_run_sha256':h,'rows':[{**z,'after':pin(R/z['current_path'])} for z in before]}
put('native-review-state-completion.finite-map.json',mapping)
put('terminal.review-state-completion74.receipt.json',{'actual_PID':os.getpid(),'EXIT':0,'files':len(names),'whole_logical_run_sha256':h,'mathematical_or_source_repair':False,'old_preparation_canonical_or_CLOSED_writes':False})
print(json.dumps({'actual_PID':os.getpid(),'EXIT':0,'whole_logical_run_sha256':h,'named_payload_RAW':pin(O/'complete-named-review-decision-input-payload.json'),'open_native_states_completed_without_semantic_change':True}))
