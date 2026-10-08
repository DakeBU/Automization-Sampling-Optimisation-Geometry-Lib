import os,sys,json,pathlib,hashlib,datetime,subprocess,shutil,re
R=pathlib.Path('E:/Samplinglib'); B=R/'runs/20261007-companion-priority/pbps-source-mean-gradient-domain54';O=B/'whole-proof-review54'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def path(p):p=pathlib.Path(p);return p if p.is_absolute() else R/p
def load(p):return json.loads(path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def logical(d):return sha(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode())
def dump(p,d):path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(p):
 p=path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def equal(e):
 a=pin(e['path']);return all(a[k]==e[k] for k in ('raw_sha256','lf_sha256')) and a['bytes']==e.get('bytes',e.get('raw_bytes',a['bytes']))
def strict(name):
 rows=load(B/'math-freeze.json')['inputs'];assert len(rows)==552
 results=[dict(expected=e,actual=pin(e['path']),ok=equal(e)) for e in rows];assert all(x['ok'] for x in results)
 dump(O/name,dict(status='PASS',count=552,checks=results));return results
if __name__=='__main__':
 assert not (O/'lease.json').exists(),'Do not repeat compiler invocation'
 dump(O/'lease.json',dict(status='OPEN',reviewer='whole_math52',actual_python_pid=os.getpid(),opened_utc=utc(),read='OPEN',write='OPEN',Python='OPEN',compiler='NOT_STARTED',scope='Precommit independent whole mathematical proof54; no source/decoder verdict read, proof/canonical edit or state transition; own outputs only.'))
 strict('inputs.pre.json')
 env=dict(os.environ);original=env.pop('ELAN_TOOLCHAIN',None);env.update(PYTHONUTF8='1',LEAN_NUM_THREADS='2')
 assert path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
 manifest=load('lake-manifest.json');mathlib=next(x for x in manifest['packages'] if x['name']=='mathlib');assert mathlib['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
 processes=subprocess.check_output(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process | Where-Object { $_.Name -in @('lean.exe','lake.exe') } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"],encoding='utf-8').strip();assert not processes,processes
 lake=shutil.which('lake');assert lake
 version=subprocess.run([lake,'env','lean','--version'],cwd=R,env=env,capture_output=True);(O/'lean.pin.log').write_bytes(version.stdout+version.stderr);assert version.returncode==0 and b'4.33.0' in version.stdout
 dump(O/'environment.json',dict(actual_python_pid=os.getpid(),python=sys.executable,python_version=sys.version,lake=lake,ELAN_TOOLCHAIN_inherited_present=original is not None,ELAN_TOOLCHAIN_removed=True,LEAN_NUM_THREADS='2',PYTHONUTF8='1',Lean_pin=pin('lean-toolchain'),Mathlib_manifest=pin('lake-manifest.json'),Mathlib_rev=mathlib['rev'],precompiler_processes=processes,lean_version_exit=version.returncode,lean_version_log=pin(O/'lean.pin.log'),HEAD=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()))
 for p,n in [('AutoSamplingTheory/ExampleCases/ProximalBPS/SourceMeanGradientDomain.lean','production.actual.raw.snapshot.lean'),('Tests/ProximalBPSSourceMeanGradientDomain.lean','Tests.actual.raw.snapshot.lean')]: (O/n).write_bytes(path(p).read_bytes())
 command=[lake,'build','Tests.ProximalBPSSourceMeanGradientDomain'];start=utc()
 with (O/'focused.log').open('wb') as log:
  proc=subprocess.Popen(command,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
  lease=dict(status='OPEN',compiler='OPEN',Python='OPEN',opened_utc=start,process_id=proc.pid,command=command,source=pin('Tests/ProximalBPSSourceMeanGradientDomain.lean'),force_rebuild=False)
  dump(O/'compiler.lease.json',lease);code=proc.wait()
 finish=utc();log=pin(O/'focused.log');dump(O/'focused.status.json',dict(command=command,process_id=proc.pid,actual_python_pid=os.getpid(),exit_code=code,started_utc=start,finished_utc=finish,log=log,source=pin('Tests/ProximalBPSSourceMeanGradientDomain.lean'),forced_rebuild=False))
 lease.update(status='CLOSED',compiler='CLOSED',Python='CLOSED',closed_utc=finish,exit_code=code,log=log);dump(O/'compiler.lease.json',lease)
 strict('inputs.post-build.json');assert code==0
 print(json.dumps(dict(focused_exit=code,actual_compiler_PID=proc.pid,actual_python_PID=os.getpid(),log=log,all552_post_inputs='PASS',compiler_lease='CLOSED',replay_not_forced=True)))
