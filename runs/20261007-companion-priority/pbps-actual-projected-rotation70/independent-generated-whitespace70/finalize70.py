import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,os,base64
O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
manifest=json.loads((O/'input-manifest.json').read_bytes())
for q in manifest['inputs']:
 b=pathlib.Path(q['path']).read_bytes();assert len(b)==q['RAW_bytes'] and sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
for q in manifest['other137_original_packet_inputs_checked_in_place_not_duplicated']:
 b=pathlib.Path(q['path']).read_bytes();assert sha(b)==q['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==q['LF_sha256']
receipt=json.loads((O/'audit-overlay.terminal-receipt.json').read_bytes());assert receipt['exit_code']==0
layers=[]
for n in ['overlay.full-review.RAW.md','overlay.decision.json','input-manifest.json','audit-overlay.terminal-receipt.json']:
 b=(O/n).read_bytes();layers.append({'name':n,'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n')),'raw_base64':base64.b64encode(b).decode()})
payload={'schema':'bounded-complete-generated-whitespace70-named-payload-v1','finite_input_manifest_RAW_sha256':sha((O/'input-manifest.json').read_bytes()),'named_RAW_layers':layers,'no_recursive_old_history_payload':True,'paired_RAW_and_CRLF_only_LF_snapshots':'Six small paired snapshots retained separately and bound by final owned manifest.'};write('complete-named-review-decision-input-payload.json',payload)
run={'schema':'independent-generated-whitespace70-run-v1','conclusion':'accept_exact_generated_whitespace_overlay','original_CLOSED213_whole_logical':'19365ca83c536e7f2e117d7148363201bf2049c604a7959a9df3499a398e090b','original_packet_RAW_sha256':'4b98a34d129fcd9c0d8aa5352eb25b5b198a480585a6f37edfba2726e8cf5740','decision_RAW_sha256':sha((O/'overlay.decision.json').read_bytes()),'input_manifest_RAW_sha256':sha((O/'input-manifest.json').read_bytes()),'complete_named_payload_RAW_sha256':sha((O/'complete-named-review-decision-input-payload.json').read_bytes()),'actual_audit_PID':receipt['actual_pid'],'actual_audit_EXIT':receipt['exit_code'],'logical_hash_recipe':'Delete ONLY top-level run_sha256; compact sorted ensure_ascii=False UTF8 JSON; no nested fields removed.','no_math_source_VERIFIED_new_credit':True};run['run_sha256']=sha(canon(run));write('review.run.json',run)
print('actual_PID',os.getpid(),'PASS finite inputs',manifest['count'],'plus other137 unchanged; named payload bytes',(O/'complete-named-review-decision-input-payload.json').stat().st_size,'wholelogical',run['run_sha256'])
