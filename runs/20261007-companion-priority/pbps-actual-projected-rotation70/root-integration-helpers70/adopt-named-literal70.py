from pathlib import Path
import base64,hashlib,json,os
root=Path.cwd();r=root/'runs/20261007-companion-priority/pbps-actual-projected-rotation70'
sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
load=lambda p:json.loads(Path(p).read_bytes())
def check(b,z,lower=False):
 prefix='raw' if lower else 'RAW';lp='lf' if lower else 'LF'
 assert len(b)==z[prefix+'_bytes'] and sha(b)==z[prefix+'_sha256'],z
 lf=b.replace(b'\r\n',b'\n');assert sha(lf)==z[lp+'_sha256'],z
 if lp+'_bytes' in z:assert len(lf)==z[lp+'_bytes']
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(root).as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b))
math=r/'independent-named-literal-math70';source=r/'independent-named-literal-source70'
ml=load(math/'lease.final.json');sl=load(source/'lease.final.json')
assert sha((math/'lease.final.json').read_bytes())=='eb8e5dfce6b2d1347540e97dc7ebeb51700a2b0a6e058e3274d25918e99f13f8'
assert sha((source/'lease.final.json').read_bytes())=='f467f5a53dcb7c1ab8a79fd87511c7feab021ad3039e10339f72c9e11360bc83'
assert ml['status']==sl['status']=='CLOSED_LAST'
assert ml['last_owned_write'] and not ml['postclose_writes_allowed'] and not sl['postclose_writes_permitted']
assert ml['actor']=='/root/exact_science63' and sl['owner']=='/root/independent_primary69'
rows=ml['manifest'];assert sha(can(rows))==ml['manifest_logical_sha256']
files={x.resolve() for x in math.rglob('*') if x.is_file()}
assert len(files)==ml['owned_file_count']==69
assert files=={Path(x['path']).resolve() for x in rows}|{(math/'lease.final.json').resolve()}
for z in rows:
 p=Path(z['path']);check(p.read_bytes(),z,True);assert p.stat().st_mtime_ns<=(math/'lease.final.json').stat().st_mtime_ns
mr=load(math/'run.json');mh=sha(can({k:v for k,v in mr.items() if k!='run_sha256'}))
assert mh==mr['run_sha256']==ml['whole_logical_run_sha256']=='4de5de3f3457211df5db9b3a1ed0d8daef1d3893fcd798ea9229b12b4ea56589'
assert mr['status']=='ACCEPTED_LITERAL_REPRESENTATION_EQUIVALENCE_ONLY_NOT_PROVED'
assert all(t['terminal_closed'] and t['exit_code']==0 for t in mr['stage_terminals'].values())
mi=load(math/'inputs.manifest.json');assert mi['input_count']==len(mi['inputs'])==17
pin_only=[]
for row in mi['inputs']:
 check(Path(row['original']['path']).read_bytes(),row['original'],True)
 if 'RAW_snapshot' not in row:
  assert row['storage'].startswith('Exact RAW/LF pin only; retained authority at original locator, not copied.')
  pin_only.append(row['original']['path']);continue
 for key in ['RAW_snapshot','LF_snapshot']:check(Path(row[key]['path']).read_bytes(),row[key],True)
 b=Path(row['original']['path']).read_bytes()
 assert b==Path(row['RAW_snapshot']['path']).read_bytes()
 assert b.replace(b'\r\n',b'\n')==Path(row['LF_snapshot']['path']).read_bytes()
assert len(pin_only)==2 and pin_only[0].endswith('/named-literal-diagnostic-v1/stdout.log') and pin_only[1].endswith('/named-literal-reuse-origin3.exactraw.snapshot')
sm=load(source/'manifest.final.json');assert sha((source/'manifest.final.json').read_bytes())==sl['manifest_RAW_sha256']=='a70c378ba2f5dcdcb3c7ea46619a56b22505f7611cef123d21fdad586ea3dfff'
assert sha(can(sm['entries']))==sm['finite_owned_closure_sha256']==sl['finite_owned_closure_sha256']
files={x.relative_to(source).as_posix():x for x in source.rglob('*') if x.is_file()}
assert len(files)==sl['owned_file_count']==63
assert set(files)=={z['name'] for z in sm['entries']}|{'manifest.final.json','lease.final.json'}
for z in sm['entries']:
 p=files[z['name']];check(p.read_bytes(),z);assert p.stat().st_mtime_ns<=(source/'lease.final.json').stat().st_mtime_ns
sr=load(source/'review-run.json');sh=sha(can({k:v for k,v in sr.items() if k!='run_sha256'}))
assert sh==sr['run_sha256']==sl['whole_logical_run_sha256']=='6e5709b599fc855ccc40e21cc5d14dc636039b0d75ffbd0660c37a3bc77d2910'
assert all(sl[k]==0 for k in ['actual_freeze_exit','actual_review_exit','actual_readback_exit']) and sl['actual_writer_exit_observed_externally']
payload=load(source/'RAW-LF-input-payload.json');assert payload['count']==len(payload['inputs'])==18
for z in payload['inputs']:
 a=z['attribution'];b=base64.b64decode(z['RAW_base64'],validate=True);lf=base64.b64decode(z['LF_base64'],validate=True)
 check(b,a);assert lf==b.replace(b'\r\n',b'\n')
 assert b==(source/a['name']).read_bytes()==Path(a['original_path']).read_bytes()
for z in load(source/'complete-named-review-decision-input.json')['named']:
 b=base64.b64decode(z['RAW_base64'],validate=True);check(b,z)
 assert b==(source/z['name']).read_bytes()
 assert base64.b64decode(z['LF_base64'],validate=True)==b.replace(b'\r\n',b'\n')
sd=load(source/'decision.json');assert sha((source/'decision.json').read_bytes())=='1fbc093e3564a5addc2a78dfc61fc986d8d46e2eefab6eca44a86b7a491e1f24'
assert not sd['mathematical_source_statement_repairs_required'] and not sd['missing_or_extra_public_premises']
assert sl['source_repairs']==0 and sl['exact_literal_value_lines']==107
q=root/'.astis/pbps-actual-rotation70/diagnostic-named-literal70-v2.lean';s=q.read_text(encoding='utf-8')
h=r/'compiler-diagnosis70/header-named-literal70.proposed.lean'
assert sha(h.read_bytes())=='5014d6e596a33ac58479cb19c6adad075ce4a0ed45e54d9ceec38214a144c2f2'
start=s.index('private def actual_projected_rotation_statement')
end=s.index(' := by\n',s.index('theorem actual_projected_rotation',start))
assert s[start:end]+'\n'==h.read_text(encoding='utf-8')
compiled=load(r/'named-literal-diagnostic-v2/receipt.json');assert compiled['terminal_closed'] and compiled['exit_code']==0
assert compiled['command'][-1]==q.relative_to(root).as_posix()
assert 'depends on axioms: [propext,' in (r/'named-literal-diagnostic-v2/stdout.log').read_text(encoding='utf-8')
dest=r/'root.named-literal70.adoption.json';assert not dest.exists()
prod=root/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualProjectedRotation.lean'
before=r/'compiler-diagnosis70/canonical-before-adoption.exactraw.snapshot.lean';assert not before.exists()
before.write_bytes(prod.read_bytes())
dest.write_text(json.dumps(dict(status='INDEPENDENT_LITERAL_REPRESENTATION70_ADMITTED_ONLY',actual_root_PID=os.getpid(),
 original_statement_seal_unchanged=True,representation_overlay=pin(h),math_lease=pin(math/'lease.final.json'),source_lease=pin(source/'lease.final.json'),
 math_logical=mh,source_logical=sh,math_current_inputs=17,source_current_inputs=18,native_owned_files=[69,63],
 exact107_return_lines_preserved=True,original6_callers_and12_witnesses_preserved=True,
 original_inline_syntax_requirement_amended_by_independently_reviewed_equivalent_representation=True,
 prior66_retired_routes_reused=True,reader_requires_complete_adjacent_literal_fold=True,
 mathematical_provider=False,extra_public_premise=False,mathematical_repair=False,
 scratch_compiled=pin(r/'named-literal-diagnostic-v2/receipt.json'),canonical_compilation_pending=True,
 full_theorem_mathematics_review=False,full_source_review=False,VERIFIED=False,Goal_complete=False),indent=2)+'\n',encoding='utf-8',newline='\n')
prod.write_bytes(q.read_bytes())
(r/'implementation70.v2.json').write_text(json.dumps(dict(status='CANONICAL70_IMPLEMENTED_FOCUSED_COMPILE_PENDING',actual_root_PID=os.getpid(),
 before=pin(before),after=pin(prod),representation_admission=pin(dest),
 source_of_exact_bytes=pin(q),BODY_api_repairs=pin(r/'compiler-diagnosis70/body-api-v2.json'),
 full_theorem_review=False,VERIFIED=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS math CLOSED69/17 and source CLOSED63/18 native RAW/LF closures; exact literal overlay admitted; compiled scratch exact bytes applied canonically, canonical focused compile pending.')
