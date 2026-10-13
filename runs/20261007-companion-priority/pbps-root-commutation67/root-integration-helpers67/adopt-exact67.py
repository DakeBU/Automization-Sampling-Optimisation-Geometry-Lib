from pathlib import Path
import hashlib, json, os, subprocess, sys

root=Path.cwd(); r=root/'runs/20261007-companion-priority/pbps-root-commutation67'; d=r/'exact-science-verification67'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
C='3da29415011a971a65f749502a625e416213f487'; P='eb3d5ffbb6853f2a0aa4a8c66aefce19d8050176'
lease, run, verdict=[load(d/n) for n in ['lease.final.json','run.json','verification-verdict.json']]
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==C==lease['exact_commit']==run['exact_commit']==verdict['verified_commit']
assert run['parent']==verdict['parent']==P
assert lease['status']=='CLOSED_LAST' and lease['final_owned_write'] and lease['owned_file_count_including_lease']==102
assert sha((d/'lease.final.json').read_bytes())=='5e47aaf073ae41fe152e10ef02c7366655edaa5f8f6f961e7fd671ec032dea37'
logical=sha(json.dumps({k:v for k,v in run.items() if k!='run_sha256'},ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
assert logical==run['run_sha256']==lease['whole_logical_run_sha256']=='9ebdf209a81eccba654b457aaa4cbb211b54971f862c6039550302d137b01e06'

def pin(x):
    b=Path(x['path']).read_bytes()
    assert len(b)==x['raw_bytes'] and sha(b)==x['raw_sha256'],x['path']
    lf=b.replace(b'\r\n',b'\n')
    assert len(lf)==x['lf_bytes'] and sha(lf)==x['lf_sha256'],x['path']
    return b

assert sha(pin(run['complete_named_RAW']))=='17f843e1a5fe6611895d24ba457a554d495f1aa6d2c8e2904a6e75be375ecaa6'
listed={Path(x['path']).resolve() for x in lease['all_owned_except_final_lease']}|{(d/'lease.final.json').resolve()}
assert listed=={p.resolve() for p in d.rglob('*') if p.is_file()} and len(listed)==102
last=(d/'lease.final.json').stat().st_mtime_ns
for x in lease['all_owned_except_final_lease']:
    pin(x); assert Path(x['path']).stat().st_mtime_ns<=last
manifest=load(d/'inputs.manifest.json'); assert len(manifest['reference_pins'])==55
for row in manifest['reference_pins']:pin(row)
git=load(d/'Git.blobs.manifest.json'); assert git['exact_commit']==C and git['actual_parent']==P
for row in git['files']:
    assert sha(subprocess.check_output(['git','show',C+':'+row['relative_path']]))==row['Git_RAW_sha256']
    pin(row['workspace_pin'])
    if 'owned_exact_Git_RAW_snapshot' in row:pin(row['owned_exact_Git_RAW_snapshot'])
assert sum('owned_exact_Git_RAW_snapshot' in row for row in git['files'])==14
focus=load(d/'focused.result.json'); assert focus['status']=='PASS'
for row in focus['results']:
    assert row['exit_code']==0 and row['terminal_closed']
    assert all(set(x['exact_axioms'])=={'propext','Classical.choice','Quot.sound'} for x in row['standard3'])
assert verdict['status']=='ACCEPTED_EXACT_SCI67' and verdict['actor']=='/root/exact_science63' and verdict['no_root_self_verification']
source=load(d/'source-bindings.result.json')
assert source['status']=='PASS' and source['adapter_preserved_every_delta_and_same_slot_evidence'] and source['native_unchanged']
assert source['finite_original_freeze_rows']==42 and len(source['finite_resolutions'])==106
assert len(source['source_audits'])==2 and all(x['verdict']=='equivalent-after-elaboration' for x in source['source_audits'])
assert load(d/'fake-closure-scan.json')['hits']==[]
t=load(d/'transition.receipt.json'); assert t['status']=='VERIFIED_BY_NONOWNER' and t['one_append'] and t['historical_prefix_unchanged']
assert t['actor']=='/root/exact_science63' and t['actor']!=verdict['PROVED_LOCAL_owner']
ledger=(root/'runs/substantive_advances.jsonl').read_bytes(); before=t['before'];after=t['after']; suffix=pin(t['append_RAW'])
assert len(ledger)==after['raw_bytes'] and sha(ledger)==after['raw_sha256']
assert sha(ledger[:before['raw_bytes']])==before['raw_sha256'] and ledger[before['raw_bytes']:]==suffix
event=json.loads(suffix); assert event['to_state']=='VERIFIED' and event['worker_id']==t['actor']
assert load(r/'verified.json')['verified_commit']==C
before_files={p.as_posix():(sha(p.read_bytes()),p.stat().st_mtime_ns) for p in d.rglob('*') if p.is_file()}
subprocess.run([sys.executable,'-B','-X','utf8',str(d/'verify67.py'),'postclose'],check=True)
assert before_files=={p.as_posix():(sha(p.read_bytes()),p.stat().st_mtime_ns) for p in d.rglob('*') if p.is_file()}
out=r/'root.exact-verification67.adoption.json'; assert not out.exists()
out.write_text(json.dumps(dict(native_verified=True,verified_commit=C,actual_parent=P,native_verifier=t['actor'],actual_root_pid=os.getpid(),
    native_whole_logical_run_sha256=logical,native_complete_RAW_payload_sha256=run['complete_named_RAW']['raw_sha256'],
    native_lease_RAW_sha256=sha((d/'lease.final.json').read_bytes()),native_owned_files=102,finite_reference_inputs=55,
    finite_source_rows=42,finite_resolutions=106,compiler_jobs=3948,proper_non_owner_transition=t,
    remaining_boundary=verdict['remaining'],postclose_owned_writes=0,aggregate_integration=False,
    full_paper_PURIFIED_ExpositionSeal_Goal=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS exact SCI67 CLOSED102 adoption:55 references/42finite rows/106finite resolutions,3948jobs,proper nonowner VERIFIED. Serialized aggregate pending.')
