import json,hashlib,os
from pathlib import Path
O=Path(__file__).parent
H=lambda b:hashlib.sha256(b).hexdigest()
C=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def load(n):return json.loads((O/n).read_bytes())
r=load('review-run.json');logical=dict(r);del logical['run_sha256'];assert H(C(logical))==r['run_sha256']
c=load('closure-index.json');d=load('semantic-decision.json');core=dict(d);del core['review_run_sha256'];assert core==r['decision'];assert len(core['semantic_slots'])==7
assert core['verdict']=='equivalent-after-elaboration' and not core['deltas'] and not core['repairs']
for k in ['COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_COMPLETE_RAW_INPUT']:
 p=O/c[k]['name'];b=p.read_bytes();assert H(b)==c[k]['RAW_sha256'] and len(b)==c[k]['RAW_bytes']
for x in r['pre_finalization_artifact_pins']:
 b=(O/x['name']).read_bytes();assert H(b)==x['RAW_sha256'] and len(b)==x['RAW_bytes'],x['name']
for x in load('RAW-input-payload.json')['finite_exact_RAW_inputs']:
 b=x['utf8'].encode('utf-8');assert H(b)==x['RAW_sha256'] and len(b)==x['RAW_bytes']
assert len(load('literal-BODY-excerpts-audit.json')['spans'])==5
assert load('source-coverage-audit.json')['classified']==280
for x in load('finite-candidate-input-map.json')['inputs']:
 assert H(Path(x['source_path']).read_bytes())==x['RAW_sha256'],x['source_path']
print(json.dumps(dict(actual_pid=os.getpid(),status='READBACK_PASS',whole_logical_run_sha256=r['run_sha256'],complete_seven_slots=True,distinct_complete_RAW_review_decision_input=True,artifacts_checked=len(r['pre_finalization_artifact_pins']),source_items=280,literal_BODY_spans=5,canonical_candidate_pins_current=True),sort_keys=True))
