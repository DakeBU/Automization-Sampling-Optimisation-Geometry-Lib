from common import *
assert not (O/'lease.json').exists()
dump('lease.json',dict(status='OPEN',reviewer=ACTOR,stage='precommit independent COMPLETE mathematics56',opened_utc=utc(),actual_python_PID=os.getpid(),read='OPEN',write='OPEN',Python='OPEN',compiler='NOT_STARTED',checked_base_commit=BASE,scope='Only whole-math56 outputs; freeze checked before mathematical reading. No proof/canonical/VERIFIED/decoder/source-review mutation or exposure; no future57/58.'))
assert git('rev-parse','HEAD')==BASE
strict('inputs.pre.json')
assert path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
assert next(x for x in load('lake-manifest.json')['packages'] if x['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
env=dict(os.environ);override=env.pop('ELAN_TOOLCHAIN',None);env.update(LEAN_NUM_THREADS='2',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1');lake=shutil.which('lake');assert lake
processes=subprocess.check_output(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process | Where-Object { $_.Name -in @('lean.exe','lake.exe') } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"],encoding='utf-8').strip();assert not processes,processes
v=subprocess.run([lake,'env','lean','--version'],cwd=R,env=env,capture_output=True);(O/'lean.pin.log').write_bytes(v.stdout+v.stderr);assert v.returncode==0 and b'4.33.0' in v.stdout
dump('environment.json',dict(actual_python_PID=os.getpid(),python=sys.executable,lake=lake,toolchain=pin('lean-toolchain'),manifest=pin('lake-manifest.json'),Mathlib_rev='db584cd6d46c92f209a44c0f1c829460d327499d',ELAN_TOOLCHAIN_inherited_present=override is not None,ELAN_TOOLCHAIN_removed=True,LEAN_NUM_THREADS='2',PYTHONUTF8='1',precompiler_processes=processes,version_log=pin(O/'lean.pin.log')))
command=[lake,'build','Tests.ProximalBPSRoughMeanGradient'];started=utc()
with (O/'focused.log').open('wb') as log:
 p=subprocess.Popen(command,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT);lease=dict(status='OPEN',compiler='OPEN',Python='OPEN',process_id=p.pid,opened_utc=started,command=command,forced_rebuild=False);dump('compiler.lease.json',lease);code=p.wait()
finished=utc();lp=pin(O/'focused.log');dump('focused.status.json',dict(command=command,process_id=p.pid,actual_python_PID=os.getpid(),exit_code=code,started_utc=started,finished_utc=finished,log=lp,production=pin('AutoSamplingTheory/ExampleCases/ProximalBPS/RoughMeanGradient.lean'),Tests=pin('Tests/ProximalBPSRoughMeanGradient.lean'),forced_rebuild=False,checked_base_commit=BASE))
lease.update(status='CLOSED',compiler='CLOSED',Python='CLOSED',closed_utc=finished,exit_code=code,log=lp);dump('compiler.lease.json',lease);strict('inputs.post-build.json');assert code==0
print(json.dumps(dict(status='focusedPASS',checked_base_commit=BASE,frozen418='PASS',actual_compiler_PID=p.pid,exit_code=code,compiler_lease='CLOSED',forced_rebuild=False,log=lp)))
