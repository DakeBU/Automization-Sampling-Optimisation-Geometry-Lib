import json,hashlib,os,datetime
from pathlib import Path
O=Path(__file__).parent
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def put(n,d):(O/n).write_bytes(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')+b'\n')
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');return dict(name=p.name,RAW_bytes=len(b),RAW_sha256=H(b),LF_sha256=H(l))
def load(n):return json.loads((O/n).read_bytes())
assert not (O/'lease.final.json').exists()
core=load('semantic-decision.json');assert 'review_run_sha256' not in core
put('semantic-decision.core.json',core)
# Exact finite inputs, named complete RAW INPUT independently of all reviewer conclusions.
first=load('candidate-first-inputs.json')['inputs'];candidate=load('finite-candidate-input-map.json')['inputs'];maps=[]
for row in first+candidate:
 p=O/row['RAW_snapshot'];maps.append(dict(pin(p),source_path=row['source_path'],utf8=p.read_bytes().decode('utf-8')))
for n in ['primary-first.source-proof-graph.json','primary-first.source-coverage-inventory.json','primary-first.source-inputs.json','primary-first.residual-next-header.json','primary-first.lease.final.json']+[r['name']+'.raw.html' for r in load('primary-first.source-coverage-inventory.json')['regions']]+['input.canonical-audit.before-decoder.raw']:
 p=O/n;maps.append(dict(pin(p),source_path='closed-primary65 reuse or exact finite source slice or explicit pre-decoder audit',utf8=p.read_bytes().decode('utf-8')))
put('RAW-input-payload.json',dict(schema='source65-complete-named-RAW-input-v1',semantic_review_decisions_included=False,complete_finite_input_set=True,primary_full_file_pin=dict(path='E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html',RAW_bytes=1482128,RAW_sha256='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'),finite_exact_RAW_inputs=maps,RAW_LF_maps=[load('candidate-first-inputs.json'),load('finite-candidate-input-map.json')],selected_primary_regions=load('primary-first.source-coverage-inventory.json')['regions']))
audit_names=['primary-first-seal.json','candidate-first-inputs.json','math-freeze-pin-check.json','audit-decoder-bookkeeping-drift.json','publication-binding-audit.json','literal-BODY-excerpts-audit.json','focused-evidence-audit.json','sealed-header-pin-audit.json','source-coverage-audit.json','binder-definition-audit.json','source-ingredient-DAG-audit.json','consumer-audit.json','endpoint-and-negative-boundary-audit.json','anti-anchoring-and-process.json']
negative_names=sorted(p.name for p in O.glob('negative.*') if p.suffix=='.json')
excluded={'semantic-decision.json','review-run.json','closure-index.json','owned-manifest.json','lease.final.json'}
pre=[pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name not in excluded]
run=dict(schema='source65-complete-independent-review-run-v1',reviewer='/root/independent_source64',packet_id=core['packet_id'],reviewer_packet_sha256=core['reviewer_packet_sha256'],publication_binding_sha256=core['publication_binding_sha256'],decision=core,complete_seven_slot_decision=True,RAW_input=pin(O/'RAW-input-payload.json'),audits={n:load(n) for n in audit_names},negative_observer_evidence={n:load(n) for n in negative_names},pre_finalization_artifact_pins=pre,hash_contract=dict(whole_logical_run='SHA256 canonical UTF8 JSON ensure_ascii=false sort_keys=true separators comma/colon, deleting ONLY top-level run_sha256',complete_named_RAW_REVIEW='Exact full review-run.json bytes including full seven-slot source decision, all verdict/deltas/repairs and audits; no byte deletion',complete_named_RAW_DECISION='Exact semantic-decision.json bytes, with the whole run digest added after sealing the complete semantic decision in this run',separate_named_RAW_INPUT='Exact RAW-input-payload.json bytes; no semantic decisions',noncircularity='The review-run embeds the complete semantic decision core. Only the separate decision file adds the external review_run_sha256 link after sealing. Closure manifest binds both complete native files and later terminal/closure artifacts. No other field is deleted from run hashing.'),actual_finalizer_pid=os.getpid(),finalizer_started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_mathematical_repair=False,full_Exposition=False,PURIFIED=False)
run['run_sha256']=H(C(run));put('review-run.json',run)
final=dict(core,review_run_sha256=run['run_sha256']);put('semantic-decision.json',final)
raw_review=pin(O/'review-run.json');raw_decision=pin(O/'semantic-decision.json');raw_input=pin(O/'RAW-input-payload.json')
closure=dict(schema='source65-named-complete-payload-bindings-v1',whole_logical_run_sha256=run['run_sha256'],whole_logical_hash_deletes_only=['run_sha256'],COMPLETE_RAW_REVIEW=raw_review,COMPLETE_RAW_DECISION=raw_decision,SEPARATE_COMPLETE_RAW_INPUT=raw_input,decision_schema=core['schema'],review_schema=run['schema'],input_schema=load('RAW-input-payload.json')['schema'],decision_embedded_in_review_core_is_complete_seven_slots=True,finalizer_pid=os.getpid(),later_terminal_and_self_artifacts_bound_by='owned-manifest.json and lease.final.json plus external read-only postclose tool pins')
put('closure-index.json',closure)
print(json.dumps(dict(actual_pid=os.getpid(),status='FINALIZER_COMPLETED',whole_logical_run_sha256=run['run_sha256'],COMPLETE_RAW_REVIEW=raw_review,COMPLETE_RAW_DECISION=raw_decision,SEPARATE_COMPLETE_RAW_INPUT=raw_input),sort_keys=True))
