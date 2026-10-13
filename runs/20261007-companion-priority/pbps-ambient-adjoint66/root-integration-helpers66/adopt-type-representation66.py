from pathlib import Path
import hashlib,json,os
pre=Path('runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66');d=pre/'independent-type-diagnosis66';r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66')
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
lease=load(d/'lease.final.json');run=load(d/'review-run.json');manifest=load(d/'owned-manifest.json')
assert lease['status']=='CLOSED_LAST' and lease['owned_file_count']==147 and lease['last_owned_write']
assert sha((d/'lease.final.json').read_bytes())=='5e9ef411d55713273752c3167c8a07abe2846bb91c306d977dcddd2ec27378a5'
logical=sha(json.dumps({k:v for k,v in run.items() if k!='run_sha256'},sort_keys=True,separators=(',',':'),ensure_ascii=False).encode())
assert logical==run['run_sha256']==lease['whole_logical_run_sha256']=='3196f08c7b46e925134e32f6cfdac920388cc35f1eae82739f50c75f5638f800'
def check(x):
 b=(d/x['name']).read_bytes();assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256']
 lf=b.replace(b'\r\n',b'\n');assert len(lf)==x['LF_bytes'] and sha(lf)==x['LF_sha256']
for x in manifest['file_entries']:check(x)
for k in ['COMPLETE_RAW_REVIEW','COMPLETE_RAW_DECISION','SEPARATE_RAW_INPUT','owned_manifest']:check(lease[k])
assert lease['COMPLETE_RAW_REVIEW']['RAW_sha256']=='6e9dc30ebc9abecba9f65665af6852e1296d9e2ce031645b9a4388c1e9a119a0'
assert lease['COMPLETE_RAW_DECISION']['RAW_sha256']=='d25f567037a79f37c3f753c23a2a4f03ea4413d963ace17db83d868d0243a88b'
assert lease['SEPARATE_RAW_INPUT']['RAW_sha256']=='31ff27027f7bd0e65428162408f646291622c4e86d45e0d8cbdcbd16d2e04879'
expected={x['name'] for x in manifest['file_entries']}|{'owned-manifest.json','lease.final.json'}
assert expected=={p.relative_to(d).as_posix() for p in d.rglob('*') if p.is_file()} and len(expected)==147
last=(d/'lease.final.json').stat().st_mtime_ns;assert all(p.stat().st_mtime_ns<=last for p in d.rglob('*') if p.is_file())
assert all(lease[k]==0 for k in ['actual_finalizer_exit','actual_readback_exit','actual_close_validator_exit'])
hashes=[('935603044de2011a02c06d62078b6f5c66cafbece245ac1585529c8fd9f60e09','7cc17f626dc04f5a963a535a6d7ec4495584b2b67f30e5b8cfd9b04e5b1869d6'),('e96784695df38fe4d65917dfc591446786ff3e61c5c92a8fa26b7f0ada2678ac','ed84c6d31a861aff1e8e2c0258574268bdcb1ca67d10081611995cfd7543ff69')]
claim=load(r/'claim.json');rows=[]
for i,(path,(dh,hh)) in enumerate(zip(claim['proposed_files'],hashes)):
 df=(d/f'proposed.statement{i}.lean').read_bytes();hf=(d/f'proposed.header{i}.lean').read_bytes();assert sha(df)==dh and sha(hf)==hh
 s=Path(path).read_text(encoding='utf-8');a=s.index('private def ');b=s.index('\ntheorem ',a);actual_def=s[a:b].rstrip()+'\n'
 a=s.index('theorem ',b);b=s.index(':= by',a);actual_header=s[a:b].rstrip()+'\n'
 assert actual_def==df.decode().replace('\r\n','\n') and actual_header==hf.decode().replace('\r\n','\n'),path
 old=(pre/f'header{i}.lean').read_text(encoding='utf-8')
 short=actual_header.splitlines()[0].split('theorem ',1)[1]
 expanded=actual_def.replace(actual_def.splitlines()[0],'theorem '+short,1).replace(' : Prop :=\n',' :\n',1)
 assert expanded.rstrip()+'\n'==old.rstrip()+'\n'
 rows.append(dict(path=path,private_literal_definition_RAW_sha256=dh,actual_public_header_RAW_sha256=hh,expanded_original_header_RAW_sha256=sha((pre/f'header{i}.lean').read_bytes()),exact_literal_expansion=True,extra_public_premises=[]))
out=pre/'root.type-representation66.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='INDEPENDENT_REPRESENTATION_OVERLAY_ACCEPTED',actual_adopter_pid=os.getpid(),whole_logical_run_sha256=logical,complete_RAW_review_sha256=lease['COMPLETE_RAW_REVIEW']['RAW_sha256'],complete_RAW_decision_sha256=lease['COMPLETE_RAW_DECISION']['RAW_sha256'],separate_RAW_input_sha256=lease['SEPARATE_RAW_INPUT']['RAW_sha256'],owned_files=147,final_lease_RAW_sha256=sha((d/'lease.final.json').read_bytes()),no_postclose_writes=True,exact_statement_mappings=rows,prior_bare_unknown_tactic_type_credit_withdrawn=True,original_source_statement_unchanged=True,source_mathematical_repair=False,kernel_proof_credit=False,full_Exposition_PURIFIED=False),indent=2)+'\n',encoding='utf-8',newline='\n')
seal=pre/'root.statement-representation-seal66.json';assert not seal.exists()
seal.write_text(json.dumps(dict(status='STATEMENT66_LITERAL_PRIVATE_EXPANSION_SEALED',independent_overlay=out.as_posix(),original_statement_seal=(pre/'root.statement-seal66.json').as_posix(),rows=rows,private_mathematical_providers=[],new_mathematical_assumptions=[],scope='Private Prop definition stores exactly the old full statement; no result is assumed or proved by the definition. Full whole-module independent source review covers it before publication admission.'),indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS CLOSED147 exact representation adoption; both literal expansions/caller binders match original seals; no private mathematical provider or new premise.')
