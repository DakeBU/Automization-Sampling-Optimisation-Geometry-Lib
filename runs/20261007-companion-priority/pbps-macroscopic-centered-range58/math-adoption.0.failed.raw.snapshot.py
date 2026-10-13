from pathlib import Path
import json,hashlib,copy
r=Path('runs/20261007-companion-priority/pbps-macroscopic-centered-range58');s=r/'whole-math58'
j=lambda p:json.loads(Path(p).read_text(encoding='utf-8'));H=lambda b:hashlib.sha256(b).hexdigest();canon=lambda d:json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(row):
 b=Path(row['path']).read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==row['bytes'] and H(b)==row['raw_sha256'] and H(lf)==row['lf_sha256'],row['path']
 if 'lf_bytes' in row:assert len(lf)==row['lf_bytes']
def selfcheck(d,k):assert H(canon({a:b for a,b in d.items() if a!=k}))==d[k],k
n=j(s/'run.json');l=j(s/'lease.json');q=j(s/'receipt.json');ck=j(s/'checks.json');out=j(s/'outputs.final.json')
for d,k in [(n,'run_sha256'),(l,'lease_sha256'),(q,'receipt_sha256'),(out,'content_self_sha256')]:selfcheck(d,k)
assert n['status']==l['status']==q['status']=='CLOSED';assert q['verdict']=='ACCEPT_SCOPED_NO_MATHEMATICAL_BLOCKER';assert l['actual_compiler_exit_code']==l['actual_check_exit_code']==l['actual_foreground_exit_code']==0;assert n['focused_invocations']==1
assert all(l[k]=='CLOSED' for k in ['read','write','Python','compiler']);assert len(n['inputs'])==l['input_count']==q['actual_distinct_input_count']==80;assert len(l['outputs'])==l['output_count']==20;assert len(out['outputs'])==out['count']==18;assert l['original_pin_count']==q['strict_original_count']==72
assert H(canon(n['review_binding_payload']))==n['review_binding_payload_sha256']==q['review_binding_payload_sha256']==l['review_binding_payload_sha256'];assert l['complete_run_minus_run_sha256']==n['run_sha256']=='ac1ea3448ce99e749c09463d2a2d374a1b75d78b2abe68a4e489a3b3750b30e3'
rows=n['inputs']+l['outputs']+out['outputs']+[l['run'],l['receipt'],l['readback'],q['inputs']]
for row in rows:check(row)
for row in j(r/'math-freeze.json')['inputs']:check(row)
assert ck['all_three_new_bodies_reviewed'] and ck['original_proof_and_statement_unchanged'] and ck['no_source_fidelity_verdict'] and ck['no_VERIFIED_transition']
p=r/'root.math58.adoption.json';assert not p.exists();p.write_text(json.dumps(dict(status='INDEPENDENT_WHOLE_MATHEMATICS58_ACCEPTED_SCOPED_NOT_VERIFIED',actual_pin_checks=len(rows)+72,distinct_native_inputs=80,outputs=20,run_complete_sha256=n['run_sha256'],distinct_review_payload_sha256=n['review_binding_payload_sha256'],native_receipt=q['verdict'],checked_base_commit=n['checked_base_commit'],compiler_PID=l['actual_compiler_PID'],actual_focused_build_exit=0,scope=q['remaining_truth_boundary']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(len(rows)+72,'actual raw/LF checks; scoped independent math58 adopted; exact-science and source admission pending.')
