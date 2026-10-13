from common import *
assert load(O/'lease.json')['status']=='OPEN'
assert git('rev-parse','HEAD')==BASE
strict('inputs.pre.json')
assert path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
assert next(x for x in load('lake-manifest.json')['packages'] if x['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
env=dict(os.environ);override=env.pop('ELAN_TOOLCHAIN',None);env.update(LEAN_NUM_THREADS='2',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1');lake=shutil.which('lake');assert lake
processes=subprocess.check_output(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process | Where-Object { $_.Name -in @('lean.exe','lake.exe') } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"],encoding='utf-8').strip()
process_rows=json.loads(processes) if processes else [];process_rows=process_rows if isinstance(process_rows,list) else [process_rows]
active_repo=[p for p in process_rows if 'samplinglib' in (p.get('CommandLine') or '').lower()];assert not active_repo,active_repo
dump('compiler.preflight.json',{'status':'NO_SAMPLINGLIB_COMPILER','observed_other_repository_processes':process_rows,'scope':'Only actual Samplinglib compiler conflicts; unrelated ABRL4.29 processes are not touched','Samplinglib_compilers':active_repo})
v=subprocess.run([lake,'env','lean','--version'],cwd=R,env=env,capture_output=True);(O/'lean.pin.log').write_bytes(v.stdout+v.stderr);assert v.returncode==0 and b'4.33.0' in v.stdout
dump('environment.json',dict(actual_python_PID=os.getpid(),python=sys.executable,lake=lake,toolchain=pin('lean-toolchain'),manifest=pin('lake-manifest.json'),Mathlib_rev='db584cd6d46c92f209a44c0f1c829460d327499d',ELAN_TOOLCHAIN_inherited_present=override is not None,ELAN_TOOLCHAIN_removed=True,LEAN_NUM_THREADS='2',PYTHONUTF8='1',precompiler_processes=processes,version_log=pin(O/'lean.pin.log')))
command=[lake,'build','Tests.GaussianMarginalPoincare'];started=utc()
with (O/'focused.log').open('wb') as log:
 p=subprocess.Popen(command,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT);lease=dict(status='OPEN',compiler='OPEN',Python='OPEN',process_id=p.pid,opened_utc=started,command=command,forced_rebuild=False);dump('compiler.lease.json',lease);code=p.wait()
finished=utc();lp=pin(O/'focused.log');dump('focused.status.json',dict(command=command,process_id=p.pid,actual_python_PID=os.getpid(),exit_code=code,started_utc=started,finished_utc=finished,log=lp,production=pin('AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalPoincare.lean'),Tests=pin('Tests/GaussianMarginalPoincare.lean'),forced_rebuild=False,checked_base_commit=BASE))
lease.update(status='CLOSED',compiler='CLOSED',Python='CLOSED',closed_utc=finished,exit_code=code,log=lp);dump('compiler.lease.json',lease);strict('inputs.post-build.json');assert code==0
print(json.dumps(dict(status='focusedPASS',checked_base_commit=BASE,frozen602='PASS',actual_compiler_PID=p.pid,exit_code=code,compiler_lease='CLOSED',forced_rebuild=False,log=lp)))
