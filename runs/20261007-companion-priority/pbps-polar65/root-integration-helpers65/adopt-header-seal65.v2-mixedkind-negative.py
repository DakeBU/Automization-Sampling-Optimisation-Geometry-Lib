from pathlib import Path
import json,hashlib,os,subprocess
r=Path('runs/20261007-companion-priority/pbps-polar-preproof65');d=r/'independent-header65'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
lease,manifest,run,inputs=[load(d/n) for n in ['lease.final.json','owned-manifest.json','review-run.json','inputs.manifest.json']]
assert lease['status']=='CLOSED_LAST' and lease['final_owned_file_count']==89
assert sha((d/'lease.final.json').read_bytes())=='f6831fef0fe01e678f94b0f1816692f885790acb0af43181035925dc7b26a68b'
assert sha((d/'owned-manifest.json').read_bytes())==lease['owned_manifest_RAW_sha256']=='6319ea0d5c78d5a9fe918ff02b88395b975e41f8e5e6e971e0c45444976ef2db'
owned=manifest['all_preclosure_owned_files']
for q in owned:
 b=(d/q['filename']).read_bytes();assert sha(b)==q['raw_sha256'] and len(b)==q['raw_bytes']
 assert sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))==q['lf_sha256']
assert {q['filename'] for q in owned}|{'owned-manifest.json','lease.final.json'}=={p.name for p in d.iterdir() if p.is_file()}
logical=sha(json.dumps({k:v for k,v in run.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
assert logical==run['run_sha256']==lease['run_sha256']=='1321beab60f85cb5b846f0860a22f959cf03fcb23501cb07afd20904930d1775'
assert sha((d/'review-run.json').read_bytes())==lease['complete_RAW_REVIEW_sha256']=='c54f74887ccaba9f79d76bf3e9b64cae6b24d80e9153c36a1c499840457d6bf2'
payload=(d/'complete-inputs.named.raw.payload').read_bytes();assert sha(payload)=='d36123c1109c28213a6ef354a1cf0e448b3d154f11025e65581cf3acc80f081f'
assert len(inputs['inputs'])==32
for q in inputs['inputs']:
 full=Path(q['original_path']).read_bytes()
 if 'source_full_raw_sha256' in q:
  assert sha(full)==q['source_full_raw_sha256']
  if q['source_raw_byte_range'] is not None:
   a,z=q['source_raw_byte_range'];b=full[a:z]
  else:
   assert q['name']=='evidence/baseline64.actual.header'
   a=full.index(b'theorem actual_centered_root_order_inverse');z=full.index(b':= by',a);b=full[a:z]
 else:b=full
 assert b==(d/q['raw_snapshot']).read_bytes() and sha(b)==q['raw_sha256'] and len(b)==q['raw_bytes']
 assert sha(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n'))==q['lf_sha256']
 assert b==payload[q['payload_body_byte_start']:q['payload_body_byte_end_exclusive']]
headers=[]
for i in range(2):
 q=load(d/f'decision.{i}.json');b=(r/f'header{i}.lean').read_bytes()
 assert q['header_admission']=='ACCEPT_HEADER_ONLY' and q['verdict']=='equivalent-after-elaboration'
 assert q['verdict_scope']=='SOURCE_FIRST_HEADER_ONLY_NOT_A_PROVED_THEOREM'
 assert not q['deltas'] and not q['repairs'] and not q['source_mathematical_repair_needed']
 assert sha(b)==q['header_RAW_sha256']==q['header_LF_sha256']
 assert len(q['semantic_slots'])==7
 headers.append(dict(path=(r/f'header{i}.lean').as_posix(),raw_sha256=sha(b),lf_sha256=sha(b),independent_decision=(d/f'decision.{i}.json').as_posix(),decision_RAW_sha256=sha((d/f'decision.{i}.json').read_bytes())))
assert load(r/'root.primary65.adoption.json')['source_only']
assert not load(r/'root.type-only65.adoption.json')['compiler_success']
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head=='0aef19ca2711159eeaec86d42c9be142a94fa402'
def write(p,x):
 assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
adopt=dict(status='CLOSED_INDEPENDENT_SOURCE_FIRST_HEADER65_ACCEPTED_ONLY',actual_reader_pid=os.getpid(),native_owned_files=89,finite_RAW_LF_input_maps=32,native_whole_logical_run_sha256=logical,native_complete_RAW_review_sha256=sha((d/'review-run.json').read_bytes()),native_lease_RAW_sha256=sha((d/'lease.final.json').read_bytes()),headers=headers,mathematical_statement_repair=False,proof_search=False,theorem_compiler_PASS=False)
write(r/'root.header65.adoption.json',adopt)
write(r/'root.statement-seal65.json',dict(status='STATEMENT65_SEALED_NOT_PROVED_NOT_CLAIMED',actual_sealer_pid=os.getpid(),checked_parent_integration=head,headers=headers,whole_logical_run_sha256=logical,primary_source_graph=(r/'independent-primary65/source-proof-graph.json').as_posix(),binder_audit=(d/'binder-definition-audit.json').as_posix(),source_ingredient_DAG=(d/'source-ingredient-DAG-audit.json').as_posix(),consumer_audit=(d/'consumer-audit.json').as_posix(),header_adoption=(r/'root.header65.adoption.json').as_posix(),proof_search_started=False,formal_credit=False))
print('PASS CLOSED_HEADER65 adoption:89 files,32 named RAW/LF inputs,full7slots each; exact2headers SEALED, no proof or SAU yet.')
