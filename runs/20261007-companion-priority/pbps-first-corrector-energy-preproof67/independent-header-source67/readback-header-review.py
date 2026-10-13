from pathlib import Path
import json,hashlib,base64,os,sys
O=Path(__file__).parent;H=lambda b:hashlib.sha256(b).hexdigest();C=lambda d:H(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
def read(n):return json.loads((O/n).read_bytes())
run=read('review-run.json');c=dict(run);del c['run_sha256'];assert C(c)==run['run_sha256'];d=read('header-decisions.json');core=dict(d);del core['review_run_sha256'];assert core==run['complete_three_header_decisions'];assert d['review_run_sha256']==run['run_sha256'];assert len(d['decisions'])==3
for decision in d['decisions']:
 assert len(decision['semantic_slots'])==7 and not decision['compiler_or_type_elaboration_claim'] and not decision['proof_credit'];assert decision['repairs']==[] and not decision['source_mathematical_repair'];assert decision['final_source_review_after_implementation_required']
 for s in decision['semantic_slots'].values():assert s['original'] and s['reconstructed'] and s['evidence']
for r in run['owned_pre_finalization_RAW_LF_bindings']:
 b=(O/r['name']).read_bytes();assert H(b)==r['RAW_sha256'];assert H(b.replace(b'\r\n',b'\n'))==r['LF_sha256']
for r in read('review-payload-pins.json').values():
 if isinstance(r,dict) and 'RAW_sha256' in r:assert H((O/r['name']).read_bytes())==r['RAW_sha256']
inp=read('RAW-input-payload.json');assert inp==run['complete_named_RAW_INPUT_payload']
for r in inp['inputs']:assert base64.b64decode(r['complete_RAW_bytes_base64'])==(O/r['pin']['name']).read_bytes()
for r in read('source-first-adoption.json')['parents']:assert H(Path(r['path']).read_bytes())==r['RAW_sha256']
for r in read('candidate-inputs.json')['inputs']:assert H(Path(r['path']).read_bytes())==r['RAW_sha256']
r=read('supplemental-whole-primary-binding.json');assert H(Path(r['source_map_path']).read_bytes())==r['RAW_sha256'];whole=r['whole_primary'];assert H(Path(whole['path']).read_bytes())==whole['RAW_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
assert read('source-inventory-header-disposition.json')['classified']==344
if '--close' in sys.argv:
 for label in ['finalize','readback']:
  r=read('foreground-'+label+'.receipt.json');assert r['actual_exit']==0
  for k in ['stdout','stderr']:assert H((O/r[k]['name']).read_bytes())==r[k]['RAW_sha256']
print(json.dumps(dict(schema='header-source67-actual-foreground-readback-v1',actual_pid=os.getpid(),mode='close-validator' if '--close' in sys.argv else 'readback',whole_logical_run_sha256=run['run_sha256'],whole_object_deleting_ONLY_top_level_run_sha256=True,complete_RAW_REVIEW_and_DECISION_all21slots=True,complete_RAW_INPUT_bytes_checked=True,source_inventory=344,missing=0,all_pre_finalization_owned_bytes_checked=True,closed_parents_unchanged=True,unsealed_draft_bytes_stable=True,no_type_or_proof_credit=True),sort_keys=True))
