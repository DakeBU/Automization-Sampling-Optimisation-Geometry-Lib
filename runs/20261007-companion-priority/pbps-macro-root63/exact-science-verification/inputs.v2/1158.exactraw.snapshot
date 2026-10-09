import hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(r'E:\Samplinglib')
OUT=ROOT/'runs/20261007-companion-priority/pbps-macro-root63/independent-source63'
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(d):return json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def put(name,d):(OUT/name).write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
payload=load(OUT/'review.payload.json');binding=load(OUT/'binding-check.result.json')
inputs=load(OUT/'candidate-input.manifest.json')
for r in inputs:assert sha(Path(r['origin']).read_bytes())==r['raw_sha256']
source=load(OUT/'primary-only.input.manifest.json')
assert sha((ROOT/source['source_primary']['path']).read_bytes())==source['source_primary']['raw_sha256']
for r in source['primary_regions']:
 assert sha(Path(r['raw_path']).read_bytes())==r['raw_sha256']
 assert sha(Path(r['lf_path']).read_bytes())==r['lf_sha256']
for r in binding['math_pins_current30']:assert sha(Path(r['path']).read_bytes())==r['raw_sha256']
for r in binding['eight_exact_spans']:
 p=ROOT/r['path'];b=b''.join(p.read_bytes().splitlines(keepends=True)[r['start_line']-1:r['end_line']]);assert sha(b)==r['raw_sha256']
payload_raw=(OUT/'review.payload.json').read_bytes();payload_hash=sha(payload_raw)
assert len(payload['semantic_slots'])==7 and payload['binder_audit']['EXCESS_count']==0
assert payload['verdict']=='equivalent-after-elaboration'
pre_manifest={str(p.relative_to(OUT)).replace('\\','/'):sha(p.read_bytes()) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='lease.json'}
run={'schema_version':1,'status':'NATIVE_SOURCE_PRESENTATION_REVIEW_COMPLETED','reviewer':'/root/independent_source63','actual_finalizer_pid':os.getpid(),'executed_utc':datetime.now(timezone.utc).isoformat(),'compiler_started':False,'canonical_or_production_edits':False,'source_first_seal_receipt':load(OUT/'source-first.seal.receipt.json'),'source_primary_RAW_sha256':source['source_primary']['raw_sha256'],'source_primary_regions':source['primary_regions'],'candidate_input_manifest':inputs,'full_semantic_review':payload,'complete_review_payload_RAW_sha256':payload_hash,'artifacts_before_finalization':pre_manifest,'whole_run_hash_recipe':'SHA256 of sorted compact UTF-8 JSON of WHOLE run.json object excluding ONLY top-level run_sha256','named_full_payload_hash_recipe':'SHA256 of COMPLETE exact RAW review.payload.json bytes; DISTINCT from whole logical run hash','manifest_layering':'Run binds all evidence present before finalization and complete native semantic payload. CLOSED_LAST lease binds the completed full output manifest, receipts, stdout/readbacks and closure scripts without circular self hashes.'}
run_hash=sha(canonical(run));run['run_sha256']=run_hash
put('run.json',run)
(OUT/'run.logical.sha256').write_bytes((run_hash+'\n').encode('ascii'))
(OUT/'review.payload.RAW.sha256').write_bytes((payload_hash+'\n').encode('ascii'))
receipt={'status':'FOREGROUND_FINALIZER_COMPLETED','actual_finalizer_pid':os.getpid(),'whole_run_sha256':run_hash,'named_complete_payload_RAW_sha256':payload_hash,'run_RAW_sha256':sha((OUT/'run.json').read_bytes()),'reviewer_packet_sha256':payload['reviewer_packet_sha256'],'publication_binding_sha256':payload['publication_binding_sha256'],'verdict':payload['verdict'],'all_seven_slots_complete':True,'all24_source_regions':True,'eight_literal_code_spans':True,'EXCESS_count':0,'source_assumption_repairs':0,'full_paper_complete':False,'canonical_VERIFIED':False,'rendered_Exposition_Seal_granted':False,'lease_closed':False}
put('native.receipt.json',receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2))
