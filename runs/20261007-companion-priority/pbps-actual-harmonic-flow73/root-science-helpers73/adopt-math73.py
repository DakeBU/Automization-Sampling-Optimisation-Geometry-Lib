from pathlib import Path
import hashlib, json, os, subprocess, sys
r=Path('runs/20261007-companion-priority/pbps-actual-harmonic-flow73');o=r/'independent-math73'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(z):
 b=Path(z['path']).read_bytes();lf=b.replace(b'\r\n',b'\n')
 assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(lf)==z['LF_sha256'],z['path']
 if 'LF_bytes' in z:assert len(lf)==z['LF_bytes']
 return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
lease=load(o/'lease.final.json');assert sha((o/'lease.final.json').read_bytes())=='a8c5c2abc6658bec6a199a308733a3e185fa41b2e6b6f9ec866661c3b789da77'
assert lease['status']=='CLOSED_LAST' and lease['reviewer']=='/root/header_math72' and not lease['VERIFIED']
check(lease['manifest']);m=load(o/'native.manifest.json');rows=m['entries']
assert len(rows)==m['entry_count']==37 and lease['owned_files']==39
assert sha(can(rows))==m['logical_entries_sha256']
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{(o/'lease.final.json').resolve(),(o/'native.manifest.json').resolve()}
for z in rows:
 check(z);assert Path(z['path']).stat().st_mtime_ns<=(o/'lease.final.json').stat().st_mtime_ns
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}))
assert h==run['run_sha256']==lease['run_sha256']=='05edca61e3a4c6b3790bec73d2ae7b63d410c76a5b3b95217e8f7ed74d743c2c'
assert run['checked_parent']==subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert run['status']=='ACCEPTED_MATHEMATICS_ONLY' and not run['source_review'] and not run['VERIFIED']
assert sha(check(run['complete_named']))=='fe2618d61ad6308d3ba7e692687501baceecc7ba693902284edadc0a35da57c1'
payload=load(run['complete_named']['path']);assert payload['decision']==run['decision']
assert payload['full_exact_module_UTF8']==check(run['candidate_module']).decode()
assert payload['input_manifest']==run['input_manifest']
inputs=run['input_manifest'];assert len(inputs['inputs'])==inputs['input_count']==13
for z in inputs['inputs']:
 assert check(z['original'])==check(z['snapshot'])
v=run['decision'];assert v['nine_clauses_mathematically_correct'] and not v['minimum_mathematical_repair']
assert v['fake_closures']==0 and v['rank_zero_allowed'] and v['alphaeta_one_allowed'] and v['zero_energy_allowed']
c=run['fresh_compiler'];assert c['fresh_source_elaboration'] and not c['Lake_build_cache_replay']
assert c['terminal_EXIT']==0 and c['actual_foreground_Lean_PID']==39960
assert set(c['standard_axioms'])=={'propext','Classical.choice','Quot.sound'}
check(c['compiler_receipt']);q=load(c['compiler_receipt']['path']);assert q['terminal_closed'] and q['terminal_EXIT']==0
check(c['output_olean'])
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
with (out/'native-readonly.stdout.log').open('wb') as s,(out/'native-readonly.stderr.log').open('wb') as e:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(o/'math73.py'),'readonly'],stdout=s,stderr=e);code=p.wait()
assert code==0
readonly=json.loads((out/'native-readonly.stdout.log').read_text(encoding='utf8').splitlines()[-1]);assert readonly['status']=='PASS'
dest=r/'root.math73.adoption.json';assert not dest.exists()
dest.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_MATHEMATICS73_ONLY',actual_root_PID=os.getpid(),native_files=39,
 finite_current_inputs=13,native_whole_logical_run_sha256=h,native_lease=pin(o/'lease.final.json'),native_complete_named=run['complete_named'],
 fresh_compiler=c,checked_parent=run['checked_parent'],readonly_PID=p.pid,readonly_EXIT=code,readonly=readonly,
 mathematical_repairs=[],source_review=False,VERIFIED=False,full_paper=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS73 CLOSED39 independent whole178-line mathematics,13 current pins,fresh39960 EXIT0/standard3; source/VERIFIED pending.')
