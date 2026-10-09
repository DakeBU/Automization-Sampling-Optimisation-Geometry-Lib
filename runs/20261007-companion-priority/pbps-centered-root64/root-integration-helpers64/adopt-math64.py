from pathlib import Path
import hashlib,json,os
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-centered-root64';d=r/'independent-math64'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
run,lease,receipt,verdict=[load(d/n) for n in ['run.json','lease.json','native.receipt.json','verdict.json']]
assert lease['status']=='CLOSED_LAST' and not lease['VERIFIED_transition']
assert sha(can({k:v for k,v in run.items() if k!='run_sha256'}))==run['run_sha256']==lease['whole_logical_run_sha256']==receipt['whole_logical_run_sha256']=='16d9117a32c0ba6f01a1d60b382da4d7e500a38c12ff94188984fc37a2b87773'
named=sha((d/'named-mathematics.payload.json').read_bytes())
assert named==run['distinct_complete_named_RAW_payload_sha256']==lease['distinct_complete_named_RAW_payload_sha256']==receipt['distinct_complete_named_RAW_payload_sha256']=='a1154b20b2b47ca74aa3edc9db01e9b38e149c6824985b22cc6a816b0867c258'
assert verdict['mathematics']=='ACCEPTED' and verdict['publication']=='BLOCKED_EXCERPT_BODY_BINDING_STEP6'
assert verdict['candidate_uncommitted'] and not verdict['VERIFIED_transition'] and len(verdict['blocker'])==1
history={};seen=set();used=[]
def qualify(original,snapshot):
 p=Path(original['path']).resolve();sp=Path(snapshot);b=sp.read_bytes()
 assert sha(b)==original['raw_sha256'],sp
 if 'lf_sha256' in original:assert sha(b.replace(b'\r\n',b'\n'))==original['lf_sha256'],sp
 history[(str(p),original['raw_sha256'])]=sp
for row in load(d/'input.manifest.json')['inputs']:qualify(row,row['exact_RAW_snapshot'])
for row in load(d/'input.supplement.json')['qualified_maps']:
 mp=row['map'];qualify(mp['original'],mp['explicit_exact_raw_snapshot']['path'])
def walk(x):
 if isinstance(x,dict):
  if {'path','raw_sha256'}<=x.keys():
   p=Path(x['path']);p=p if p.is_absolute() else root/p;k=(str(p.resolve()),x['raw_sha256'],x.get('lf_sha256'))
   if k not in seen:
    effective=history.get((str(p.resolve()),x['raw_sha256']),p);b=effective.read_bytes()
    assert sha(b)==x['raw_sha256'],(p,effective)
    if 'lf_sha256' in x:assert sha(b.replace(b'\r\n',b'\n'))==x['lf_sha256'],p
    for f in ['bytes','raw_bytes']:
     if f in x:assert len(b)==x[f],p
    if effective!=p:used.append(dict(original=x,explicit_exact_raw_snapshot=effective.as_posix()))
    seen.add(k)
  for v in x.values():walk(v)
 elif isinstance(x,list):
  for v in x:walk(v)
for p in d.rglob('*.json'):walk(load(p))
owned={Path(x['path']).resolve() for x in lease['complete_owned_output_manifest_after_readback']}|{(d/'lease.json').resolve()}
actual={p.resolve() for p in d.rglob('*') if p.is_file()};assert owned==actual and len(owned)==168
focus=load(d/'focused/receipt.json');assert focus['terminal_closed'] and focus['exit_code']==0 and focus['actual_foreground_pid']==12600
assert focus['pre_post_equal'] and focus['pre']==focus['post'] and len(focus['pre'])==130
payload=load(d/'named-mathematics.payload.json');assert payload['full_native_verdict']==verdict and payload['full_mathematical_review']==load(d/'mathematical-review.json')
for n,pid in [('finalizer',47920),('readback',45180)]:
 x=load(d/n/'receipt.json');assert x['exit_code']==0 and x['actual_foreground_pid']==pid and x['terminal_closed']
out=r/'root.math64.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='INDEPENDENT_PRECOMMIT_MATHEMATICS64_ACCEPTED_WITH_STEP6_PUBLICATION_BLOCKER',actual_adopter_pid=os.getpid(),native_run_sha256=run['run_sha256'],native_named_RAW_payload_sha256=named,native_lease_RAW_sha256=sha((d/'lease.json').read_bytes()),qualified_readbacks=len(seen),finite_historical_maps=used,native_owned_files=len(owned),compiler_pid=12600,compiler_exit_code=0,checked_BASE=run['checked_BASE'],publication_blocker=verdict['blocker'],remaining_boundary=verdict['remaining_boundary'],source_review_separate=True,VERIFIED_transition=False),ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS CLOSED_LAST math64:',len(owned),'owned files;',len(seen),'qualified RAW/LF pins; mathematics accepted, step6 publication blocker retained.')
