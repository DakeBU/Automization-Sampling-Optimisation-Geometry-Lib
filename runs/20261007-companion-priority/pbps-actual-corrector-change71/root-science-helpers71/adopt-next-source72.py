from pathlib import Path
import hashlib,json,os
pre=Path('runs/20261007-companion-priority/pbps-b4-perturbation-preproof72');o=pre/'independent-source-first72'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
lease=load(o/'lease.final72.json');assert sha((o/'lease.final72.json').read_bytes())=='f9fdad44c9aa9e980d68cf2fce6f2535ce080e2a42db63c9797a8866763a0b2f'
assert lease['status']=='CLOSED_LAST' and lease['last_owned_write'] and not lease['blind_decode72_eligible']
files={p.name for p in o.iterdir() if p.is_file()};assert len(files)==lease['owned_file_count_including_lease']==9 and files=={z['name'] for z in lease['covered_files']}|{'lease.final72.json'}
for z in lease['covered_files']:
 p=o/z['name'];b=p.read_bytes();assert len(b)==z['raw_byte_count'] and sha(b)==z['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['lf_only_sha256'];assert p.stat().st_mtime_ns<=(o/'lease.final72.json').stat().st_mtime_ns
assert sha((o/'manifest72.json').read_bytes())==lease['manifest_raw_sha256']
manifest=load(o/'manifest72.json');assert len(manifest['files'])==7 and {z['name'] for z in manifest['files']}==files-{'manifest72.json','lease.final72.json'}
pins=load(o/'input-finite-pins72.json')['pins']
for z in pins:
 b=Path(z['path']).read_bytes();assert len(b)==z['raw_bytes'] and sha(b)==z['raw_sha256'] and sha(b.replace(b'\r\n',b'\n'))==z['lf_only_sha256']
payload=load(o/'preproof72.payload.json');assert payload['task_kind']=='READ_ONLY_SOURCE_FIRST_PREPROOF_PLANNING_ONLY' and not payload['full_B4_claimed'] and not payload['new_canonical_or_ledger_edits']
assert sha((o/'preproof72.payload.json').read_bytes())=='85107ef2fee08c580f2badc85a6482f4dd4066bd965a5ea76ddb163e49b14b3c'
q=dict(status='ACCEPTED_SOURCE_FIRST72_PLAN_ONLY_NO_PROOF_NO_CLAIM',actual_root_PID=os.getpid(),native_owned_count=9,current_finite_inputs=len(pins),native_lease_RAW_sha256=sha((o/'lease.final72.json').read_bytes()),native_named_payload_RAW_sha256=sha((o/'preproof72.payload.json').read_bytes()),target=payload['target'],counts=payload['counts'],dependency_distinction=payload['B21_dependency_distinction'],no_canonical_Lean_or_ledger_writes=True,proof=False,SAU_claim=False,VERIFIED=False,full_B4=False,Goal_complete=False)
p=pre/'root.source-first72.adoption.json';assert not p.exists();p.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS source-first72 CLOSED9 and all finite pins adopted as planning only; B21 is NOT a logical dependency of perturbation algebra; no proof/SAU claim.')
