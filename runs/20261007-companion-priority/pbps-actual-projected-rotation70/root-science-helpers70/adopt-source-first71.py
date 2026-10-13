from pathlib import Path
import hashlib,json,os
pre=Path('runs/20261007-companion-priority/pbps-corrector-change-preproof71')
o=pre/'independent-source-first71'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()
def check(z):
 b=Path(z['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert len(b)==z['raw_bytes'] and sha(b)==z['raw_sha256']
 assert len(lf)==z['lf_bytes'] and sha(lf)==z['lf_sha256']
l=load(o/'lease.final.json');assert sha((o/'lease.final.json').read_bytes())=='6feb5f619afc7d32cd196f2748165eaed9862da3a682bf782916e456fe423082'
assert l['status']=='CLOSED_LAST' and l['last_owned_write'] and l['actor']=='/root/exact_science63'
rows=l['manifest'];assert len(rows)==115 and sha(canonical(rows))==l['manifest_logical_sha256']
actual={p.relative_to(o).as_posix() for p in o.rglob('*') if p.is_file()}
assert actual=={z['relative_path'] for z in rows}|{'lease.final.json'} and len(actual)==116
last=(o/'lease.final.json').stat().st_mtime_ns
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=last
run=load(o/'run.json');h=run.pop('run_sha256');assert sha(canonical(run))==h==l['whole_logical_run_sha256']
check(l['named_complete_RAW_payload'])
for name in ['inputs.manifest.json','interface.inputs.manifest.json']:
 for row in load(o/name)['inputs']:check(row['original'])
d=load(o/'decision.json');assert d['status']=='ACCEPTED_BOUNDED_SOURCE_EXTRACTION_AND_PROSPECTIVE_INTERFACE_MATCH'
assert d['no_70_BODY_read'] and d['no_canonical_Git_ledger_writes']
p=pre/'root.source-first71.adoption.json';assert not p.exists()
p.write_text(json.dumps(dict(status='SOURCE_FIRST71_AND_PROSPECTIVE_INTERFACE_ADOPTED_ONLY',
 actual_root_PID=os.getpid(),native_files=116,current_inputs=5,whole_logical_run_sha256=h,
 native_named_RAW_sha256=l['named_complete_RAW_payload']['raw_sha256'],
 native_lease_RAW_sha256=sha((o/'lease.final.json').read_bytes()),
 source_first_before_current_interface=True,prior70_header_visibility_disclosed=True,
 exact_formula='C(u,v)=(norm(u)^2-norm(v)^2)/2-inner(A0 Inv u,v); actual ideal difference=-norm(fP)^2+norm(fV)^2.',
 consumer='B4 B28 first two terms; SAME actual witnesses required.',
 no_sharp_bound68_public_premise=True,no_70_BODY_read=True,native_files_mutated=False,
 seventy_proof_or_VERIFIED_credit=False,SAU71_claimed=False,Goal_complete=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS source-first71 CLOSED116/current5 adopted; actual B21/P16 source delta only; no70/71 proof credit.')
