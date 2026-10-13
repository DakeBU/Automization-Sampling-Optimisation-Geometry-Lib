from pathlib import Path
import hashlib,json,subprocess,os,sys
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-sharp-energy68';d=r/'exact-science-verification68-corrected'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
C='3ad3b127b5a645be9cf71b3d14520b2d8fea3122';P='a3191d97ccf78d58c301d024fc86b2a3289fc0a6'
def pin(q):
 b=Path(q['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert len(b)==q['raw_bytes'] and sha(b)==q['raw_sha256'],q['path']
 assert len(lf)==q['lf_bytes'] and sha(lf)==q['lf_sha256'],q['path']
 return b
lease,run,v=[load(d/n) for n in ['lease.final.json','run.json','verification-verdict.json']]
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C==lease['verified_commit']==run['verified_commit']==v['verified_commit']
assert subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip()==P==v['parent']
assert lease['status']=='CLOSED_LAST' and lease['VERIFIED'] and lease['owned_file_count_including_self']==74
assert sha((d/'lease.final.json').read_bytes())=='f04ba4e71ce32647a5a67d022e46693a39cae9718a5249eb3d24a4e05f6120b4'
logical=sha(json.dumps({k:x for k,x in run.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
assert logical==run['run_sha256']==lease['whole_logical_run_sha256']=='3d5354384181d0d17fd622ce39800208c6421397728efb2897039c4b6b6ab2e4'
assert sha(pin(run['named_complete_RAW_review']))=='94ff3f710ae6239c66beca927b94fe3105020f6077279ba302ed7d8b0e6b0b44'
listed={Path(q['path']).resolve() for q in lease['all_owned_outputs_except_only_self']}|{(d/'lease.final.json').resolve()}
assert listed=={p.resolve() for p in d.rglob('*') if p.is_file()}
last=(d/'lease.final.json').stat().st_mtime_ns
for q in lease['all_owned_outputs_except_only_self']:
 pin(q);assert Path(q['path']).stat().st_mtime_ns<=last
t=load(d/'transition.receipt.json');assert t['status']=='VERIFIED_BY_NONOWNER' and t['one_append'] and t['historical_prefix_unchanged']
assert t['actor']=='/root/exact_science63' and t['actor']!=v['owner_id'] and t['actual_transition_PID']==27872
ledger=(root/'runs/substantive_advances.jsonl').read_bytes();a=t['after'];b=t['before'];suffix=pin(t['append_RAW'])
assert len(ledger)==a['raw_bytes'] and sha(ledger)==a['raw_sha256']
assert sha(ledger[:b['raw_bytes']])==b['raw_sha256'] and ledger[b['raw_bytes']:]==suffix
event=json.loads(suffix);assert event['to_state']=='VERIFIED' and event['worker_id']==t['actor']
assert v['status']=='ACCEPTED_EXACT_SCI68B' and run['strict_BODY_spans']==11 and run['source_slots']==21 and run['retained_nonblocking_deltas']==15
assert run['exact_five_process_fields_only'] and run['old_CLOSED131_unchanged'] and run['old_required_frontier_negative_preserved']
assert run['private_mathematical_providers']==run['fakeclosures']==0
assert load(r/'verified.json')['verified_commit']==C
manifest=load(d/'inputs.manifest.json');assert manifest['input_count']==len(manifest['reference_pins'])==115
for q in manifest['reference_pins']:
 if Path(q['path']).resolve()==(root/'runs/substantive_advances.jsonl').resolve():
  assert sha(ledger[:q['raw_bytes']])==q['raw_sha256']
 else:pin(q)
git=load(d/'Git.blobs.manifest.json');assert git['exact_commit']==C and git['parent']==P and len(git['files'])==99
for q in git['files']:
 assert sha(subprocess.check_output(['git','show',C+':'+q['relative_path']]))==q['Git_RAW_sha256']
for name in load(r/'claim.json')['proposed_files']:
 assert subprocess.check_output(['git','show',C+':'+name])==subprocess.check_output(['git','show',P+':'+name])==(root/name).read_bytes()
for q in v['gate']['results']:
 assert q['exit_code']==0 and q['terminal_closed']
before={p.as_posix():(sha(p.read_bytes()),p.stat().st_mtime_ns) for p in d.rglob('*') if p.is_file()}
subprocess.run([sys.executable,'-B','-X','utf8',str(d/'readonly68b.py'),'postclose'],check=True)
assert before=={p.as_posix():(sha(p.read_bytes()),p.stat().st_mtime_ns) for p in d.rglob('*') if p.is_file()}
out=r/'root.exact-verification68.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(native_verified=True,verified_commit=C,actual_parent=P,native_verifier=t['actor'],actual_root_pid=os.getpid(),native_whole_logical_run_sha256=logical,native_complete_RAW_payload_sha256=run['named_complete_RAW_review']['raw_sha256'],native_lease_RAW_sha256=sha((d/'lease.final.json').read_bytes()),native_owned_files=74,finite_reference_inputs=115,exact_git_inputs=99,source_slots=21,literal_BODY=11,reused_focused_jobs=3950,reused_focused_PID=5528,proper_non_owner_transition_receipt=(d/'transition.receipt.json').relative_to(root).as_posix(),old_obstruction_CLOSED131_unchanged=True,old_required_frontier_EXIT1_retained=True,remaining_boundary=v['remaining'],postclose_owned_writes=0,aggregate_integration=False,full_paper_PURIFIED_ExpositionSeal_Goal=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS corrected exact SCI68B CLOSED74 adopted;115 references/99 exact Git inputs; proper nonowner VERIFIED; old CLOSED131 negative preserved.')
