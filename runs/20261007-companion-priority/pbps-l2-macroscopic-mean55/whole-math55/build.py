from common import *
assert not (O/'lease.json').exists()
dump('lease.json',dict(status='OPEN',reviewer='whole_math52',stage='precommit independent COMPLETE mathematics55',opened_utc=utc(),actual_python_PID=os.getpid(),read='OPEN',write='OPEN',Python='OPEN',compiler='NOT_STARTED',scope='Only whole-math55 outputs; no proof/canonical/state transition/commit/push; no decoder55 or source55 verdict exposure. Base not scientific55 commit.'))
assert git('rev-parse','HEAD')==BASE
strict('inputs.pre.json')
assert path('lean-toolchain').read_text(encoding='utf-8').strip()=='leanprover/lean4:v4.33.0'
manifest=load('lake-manifest.json');assert next(x for x in manifest['packages'] if x['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
env=dict(os.environ);override=env.pop('ELAN_TOOLCHAIN',None);env.update(LEAN_NUM_THREADS='2',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1');lake=shutil.which('lake');assert lake
processes=subprocess.check_output(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process | Where-Object { $_.Name -in @('lean.exe','lake.exe') } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"],encoding='utf-8').strip();assert not processes,processes
version=subprocess.run([lake,'env','lean','--version'],cwd=R,env=env,capture_output=True);(O/'lean.pin.log').write_bytes(version.stdout+version.stderr);assert version.returncode==0 and b'4.33.0' in version.stdout
dump('environment.json',dict(python=sys.executable,actual_python_PID=os.getpid(),lake=lake,base_commit=BASE,toolchain=pin('lean-toolchain'),manifest=pin('lake-manifest.json'),Mathlib_rev='db584cd6d46c92f209a44c0f1c829460d327499d',ELAN_TOOLCHAIN_inherited_present=override is not None,ELAN_TOOLCHAIN_removed=True,LEAN_NUM_THREADS='2',PYTHONUTF8='1',precompiler_processes=processes,version_exit=0,version_log=pin(O/'lean.pin.log')))
command=[lake,'build','Tests.ProximalBPSL2MacroscopicMean'];started=utc()
with (O/'focused.log').open('wb') as log:
 proc=subprocess.Popen(command,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
 lease=dict(status='OPEN',compiler='OPEN',Python='OPEN',process_id=proc.pid,opened_utc=started,command=command,forced_rebuild=False);dump('compiler.lease.json',lease);code=proc.wait()
finished=utc();logpin=pin(O/'focused.log')
dump('focused.status.json',dict(command=command,process_id=proc.pid,actual_python_PID=os.getpid(),exit_code=code,started_utc=started,finished_utc=finished,log=logpin,production=pin('AutoSamplingTheory/ExampleCases/ProximalBPS/L2MacroscopicMean.lean'),Tests=pin('Tests/ProximalBPSL2MacroscopicMean.lean'),forced_rebuild=False,checked_base_commit=BASE))
lease.update(status='CLOSED',compiler='CLOSED',Python='CLOSED',closed_utc=finished,exit_code=code,log=logpin);dump('compiler.lease.json',lease)
strict('inputs.post-build.json');assert code==0
print(json.dumps(dict(status='focusedPASS',checked_base_commit=BASE,actual_compiler_PID=proc.pid,exit_code=code,all282_original_inputs='PASS',compiler_lease='CLOSED',log=logpin,forced_rebuild=False)))
