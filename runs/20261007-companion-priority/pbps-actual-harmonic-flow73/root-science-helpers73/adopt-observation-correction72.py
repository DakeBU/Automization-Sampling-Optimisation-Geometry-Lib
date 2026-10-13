from pathlib import Path
import hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-b4-corrector-perturbation72');o=r/'reader-observation-correction72'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def check(z):
 p=Path(z['path']);b=p.read_bytes();assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['LF_sha256'],p
 return b
lp=o/'lease.final.json';assert sha(lp.read_bytes())=='5b59dd714cc4b019b4f15576cc7fe768042e203f52ba5f8c368d5abe41195d1c'
l=load(lp);rows=l['all_owned_outputs_except_only_self'];assert l['status']=='CLOSED_LAST' and l['owned_count']==27 and len(rows)==26
assert not l['postclose_owned_writes'] and l['all_sessions_closed']
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve()}
for z in rows:
 check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
assert sha(can(rows))==l['closure_logical_sha256']
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert h==run['run_sha256']==l['whole_logical_run_sha256']=='38e999c0e37883e5cbc36c392df792e66c40b8e72d86a419bc75b4ae14699d72'
payload=load(l['complete_named_RAW_payload']['path']);check(l['complete_named_RAW_payload'])
decision=load(run['decision']['path']);check(run['decision']);assert payload['decision']==decision
assert decision['correction_confirmed'] and decision['reviewer_transcription_error'] and not decision['canonical_or_Lean_repair_needed'] and not decision['new_math_or_source_or_repository_acceptance']
inputs=load(run['inputs']['path']);check(run['inputs']);assert len(inputs['inputs'])==inputs['input_count']==14
for z in inputs['inputs']:check(z)
dest=r/'root.reader-observation-correction72.adoption.json';assert not dest.exists()
dest.write_text(json.dumps(dict(status='ACCEPTED_REVIEWER_TRANSCRIPTION_CORRECTION_ONLY',actual_root_PID=os.getpid(),native_whole_logical_run_sha256=h,native_lease=dict(path=lp.as_posix(),RAW_sha256=sha(lp.read_bytes())),decision=decision,canonical_or_Lean_changes=False,original_CLOSED91_preserved=True,new_acceptance=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS CLOSED27/14inputs: reader transcription corrected; no canonical repair or acceptance badge.')
