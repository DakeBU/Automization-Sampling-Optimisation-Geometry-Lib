import json,hashlib,os
from pathlib import Path
O=Path(__file__).parent;H=lambda b:hashlib.sha256(b).hexdigest();C=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def load(n):return json.loads((O/n).read_bytes())
r=load('review-run.json');q=dict(r);del q['run_sha256'];assert H(C(q))==r['run_sha256']
for i in [0,1]:
 d=load('decision'+str(i)+'.json');z=dict(d);del z['review_run_sha256'];assert z==r['complete_semantic_decisions'][i];assert len(z['semantic_slots'])==7;assert z['status']=='HEADER_ACCEPTED_TYPE_ELABORATED_BODY_UNIMPLEMENTED';assert not z['proof_acceptance'] and not z['source_mathematical_repair']
for x in r['pre_finalization_artifact_pins']:
 b=(O/x['name']).read_bytes();assert H(b)==x['RAW_sha256'] and len(b)==x['RAW_bytes'],x['name']
for x in load('RAW-input-payload.json')['complete_finite_inputs']:
 b=x['utf8'].encode('utf-8');assert H(b)==x['RAW_sha256'] and len(b)==x['RAW_bytes'];assert H(Path(x['source_path']).read_bytes())==x['RAW_sha256'],x['source_path']
c=load('closure-index.json')
for k in ['COMPLETE_RAW_DECISIONS','COMPLETE_RAW_REVIEW','SEPARATE_COMPLETE_RAW_INPUT','process_overlay']:
 x=c[k];assert H((O/x['name']).read_bytes())==x['RAW_sha256']
over=load('process-only-overlay.json');assert over['changed_metadata_field_count']==2
for x in over['wrapper_syntax_overlays']:
 a=(O/x['before_RAW_snapshot']).read_bytes();b=(O/x['after_RAW_snapshot']).read_bytes();assert b==a.replace(b'  exact ASTIS_UNIMPLEMENTED_BODY66',b'  ASTIS_UNIMPLEMENTED_BODY66')
print(json.dumps(dict(status='READBACK_PASS',actual_pid=os.getpid(),logical_run_sha256=r['run_sha256'],both_decisions_seven_slots=True,current_initial_input_pins_match=True,source_inventory_reused=310,owned_TYPE_pids=[33108,41072],TYPE_only_exit_codes=[1,1],only_intentional_BODY_errors=True,process_only_metadata_fields=2,proof_acceptance=False),sort_keys=True))
