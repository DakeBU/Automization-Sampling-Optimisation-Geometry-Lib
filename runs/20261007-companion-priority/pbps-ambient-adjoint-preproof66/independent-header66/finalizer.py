import json,hashlib,os,datetime
from pathlib import Path
O=Path(__file__).parent
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def load(n):return json.loads((O/n).read_bytes())
def put(n,d):(O/n).write_bytes(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')+b'\n')
def pin(p):
 b=p.read_bytes();return dict(name=p.name,RAW_bytes=len(b),RAW_sha256=H(b),LF_bytes=len(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')),LF_sha256=H(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')))
assert not (O/'lease.final.json').exists()
rows=[]
for mp in ['candidate-first-inputs.json','type-negative-input-map.json','supplemental-finite-input-map.json']:
 for x in load(mp)['inputs']:
  p=O/x['RAW_snapshot'];assert H(p.read_bytes())==x['RAW_sha256'];rows.append(dict(pin(p),source_path=x.get('path',x.get('source_path')),RAW_snapshot=p.name,LF_snapshot=x['LF_snapshot'],utf8=p.read_bytes().decode('utf-8')))
for x in load('primary-first-seal.json')['source_inputs']:
 p=O/x['snapshot'];assert H(p.read_bytes())==x['RAW_sha256'];rows.append(dict(pin(p),source_path=x['path'],RAW_snapshot=p.name,LF_snapshot=p.name,utf8=p.read_bytes().decode('utf-8')))
put('finite-input-map.json',dict(schema='header66-complete-finite-RAW-LF-input-map-v1',inputs=[{k:v for k,v in x.items() if k!='utf8'} for x in rows],source_only_parent_reuse=True,current_initial_candidate_bytes_frozen=True))
put('RAW-input-payload.json',dict(schema='header66-complete-named-RAW-input-v1',complete_finite_inputs=rows,source_primary_whole_pin=load('primary-first.source-input-regions.json'),candidate_math_proof_inputs_absent=True,semantic_decisions_included=False))
decisions=[load('decision0.core.json'),load('decision1.core.json')];assert all(len(d['semantic_slots'])==7 for d in decisions)
audits=['primary-first-seal.json','candidate-first-inputs.json','TYPE-evidence-audit.json','binder-definition-audit.json','source-ingredient-DAG-audit.json','consumer-audit.json','negative-boundary-and-process.json','process-only-overlay.json','finite-input-map.json']
pre=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in ['review-run.json','decision0.json','decision1.json','complete-RAW-decisions.json','closure-index.json','owned-manifest.json','lease.final.json']]
r=dict(schema='header66-complete-independent-header-review-run-v1',complete_semantic_decisions=decisions,seven_slots_each=True,audits={n:load(n) for n in audits},RAW_input=pin(O/'RAW-input-payload.json'),pre_finalization_artifact_pins=pre,actual_finalizer_pid=os.getpid(),hash_contract=dict(logical='SHA256 canonical UTF8 JSON ensure_ascii=false sort_keys=true separators comma/colon;delete ONLY top-level run_sha256',complete_RAW_REVIEW='Exact full review-run.json including both complete seven-slot decisions and reviewed process overlay;no deletion',complete_RAW_DECISIONS='Exact complete-RAW-decisions.json containing both full decisions plus external review_run_sha256 link',separate_RAW_INPUT='Exact RAW-input-payload.json containing all finite original input bytes,no semantic decisions',noncircularity='Run contains complete semantic decision cores;separate native decisions add external digest after sealing. Closure manifest binds those bytes and all terminal/self artifacts.'),source_mathematical_repair=False,proof_acceptance=False,header_type_elaboration_known=True,full_Exposition=False,PURIFIED=False)
r['run_sha256']=H(C(r));put('review-run.json',r);final=[dict(d,review_run_sha256=r['run_sha256']) for d in decisions]
for i,d in enumerate(final):put('decision'+str(i)+'.json',d)
put('complete-RAW-decisions.json',dict(schema='header66-complete-named-RAW-decisions-v1',decisions=final,complete_both_seven_slot_decisions=True))
c=dict(schema='header66-named-complete-payload-bindings-v1',whole_logical_run_sha256=r['run_sha256'],whole_logical_hash_deletes_only=['run_sha256'],COMPLETE_RAW_DECISIONS=pin(O/'complete-RAW-decisions.json'),COMPLETE_RAW_REVIEW=pin(O/'review-run.json'),SEPARATE_COMPLETE_RAW_INPUT=pin(O/'RAW-input-payload.json'),decisions=[pin(O/'decision0.json'),pin(O/'decision1.json')],review_schema=r['schema'],decision_schema=decisions[0]['schema'],RAW_decisions_schema=load('complete-RAW-decisions.json')['schema'],RAW_input_schema=load('RAW-input-payload.json')['schema'],process_overlay=pin(O/'process-only-overlay.json'),actual_finalizer_pid=os.getpid())
put('closure-index.json',c);print(json.dumps(dict(status='FINALIZER_PASS',actual_pid=os.getpid(),bindings=c),sort_keys=True))
