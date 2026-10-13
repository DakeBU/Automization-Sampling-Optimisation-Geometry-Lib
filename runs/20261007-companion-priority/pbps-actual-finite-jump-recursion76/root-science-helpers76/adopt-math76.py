from pathlib import Path
import hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76');o=r/'independent-math76'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(z):
 b=Path(z['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(lf)==z['LF_sha256'],z['path']
 if 'LF_bytes' in z:assert len(lf)==z['LF_bytes']
 return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
expected_run='f6c4234dc480c07e4e0e24f93e4f8edd8a5a4da8b81de897f0eb2e43bcb63049'
expected_lease='9104b0faedfd55116e0bfa04a7dc7c9d22631a2aa378cd18659f39805248e24b'
expected_payload='be081891fef6297d33f28cef80420b6167c6fbb55763a789e94c7add525aee16'
lp=o/'lease.final.json';lease=load(lp);assert sha(lp.read_bytes())==expected_lease
assert lease['status']=='CLOSED_LAST' and lease['actor']=='/root/exact_science63' and not lease['VERIFIED']
assert lease['all_sessions_closed'] and lease['final_owned_write'] and not lease['postclose_owned_writes']
rows=lease['all_owned_outputs_except_only_self'];assert len(rows)+1==lease['owned_count']==82
assert sha(can(rows))==lease['closure_logical_sha256']
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve()}
for z in rows:check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert h==run['run_sha256']==lease['whole_logical_run_sha256']==expected_run
assert run['checked_parent']==subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert run['accepted_whole_mathematics'] and not run['source_fidelity_verdict'] and not run['VERIFIED']
payload=load(run['complete_named_RAW_payload']['path']);assert sha(check(run['complete_named_RAW_payload']))==expected_payload
decision=load(run['decision']['path']);assert decision==payload['decision']
assert decision['accepted_whole_mathematics'] and not decision['mathematical_repair_required'] and not decision['blockers'] and decision['fake_closure_hits']==0
assert (decision['callers'],decision['literal_definitions'],decision['conclusion_groups'])==(6,11,10)
assert check(run['module'])==check(decision['module'])
inputs=load(run['inputs_manifest']['path']);assert inputs==payload['inputs']
assert inputs['dispatch_input_count']==12 and inputs['supplemental_input_count']==2 and inputs['total_input_rows']==14
for z in inputs['inputs']+inputs['supplemental_inputs']:
 b=check(z['original'])
 if 'snapshot' in z:assert b==check(z['snapshot'])
api=load(run['analysis_inputs_manifest']['path']);assert api==payload['analysis_inputs']
for z in api['API_inputs']:check(z['original'])
check(api['expanded_header_input'])
c=payload['fresh_compiler'];assert c==load(decision['fresh_compiler']['path'])
assert c['fresh_source_elaboration'] and not c['Lake_build_cache_replay'] and c['terminal_EXIT']==0
assert set(c['standard_axioms'])=={'propext','Classical.choice','Quot.sound'}
for key in ['compiler_receipt','axiom_receipt']:
 q=json.loads(check(c[key]));assert q['exit_code']==0 and q['terminal_closed']
check(c['output_olean'])
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
with (out/'native-readonly.stdout.log').open('wb') as s,(out/'native-readonly.stderr.log').open('wb') as e:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(o/'close_probe.executed-helper.RAW.py'),'postclose'],stdout=s,stderr=e);code=p.wait()
assert code==0
readonly=json.loads((out/'native-readonly.stdout.log').read_text(encoding='utf8').splitlines()[-1]);assert readonly['status']=='READONLY_POSTCLOSE_PASS' and not readonly['owned_writes']
dest=r/'root.math76.adoption.json';assert not dest.exists()
dest.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_WHOLE_MATHEMATICS76_ONLY',actual_root_PID=os.getpid(),native_files=82,finite_current_inputs=14,native_whole_logical_run_sha256=h,native_lease=pin(lp),native_complete_named=run['complete_named_RAW_payload'],fresh_compiler=c,checked_parent=run['checked_parent'],readonly_PID=p.pid,readonly_EXIT=code,readonly=readonly,mathematical_repairs=[],documentation_debt=decision['documentation_debt'],source_review=False,VERIFIED=False,full_paper=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS76 independent whole-body mathematics, CLOSED82, fresh direct Lean/standard3; source/exact-SCI/reader pending.')
