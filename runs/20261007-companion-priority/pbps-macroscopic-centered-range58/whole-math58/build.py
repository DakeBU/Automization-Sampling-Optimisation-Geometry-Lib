from common import *
sys.stdout.reconfigure(encoding='utf8')
rows=load(B/'math-freeze.json')['inputs'];assert len(rows)==72
for e in rows:assert same(e,pin(e['path'])),e['path']
env=dict(os.environ);old=env.pop('ELAN_TOOLCHAIN',None);env.update(LEAN_NUM_THREADS='2',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1')
assert (R/'lean-toolchain').read_text(encoding='utf8').strip()=='leanprover/lean4:v4.33.0'
ml=load(R/'lake-manifest.json');mathlib=next(x for x in ml['packages'] if x['name']=='mathlib');assert mathlib['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
lean=pathlib.Path('C:/Users/admin/.elan/bin/lean.exe');lake=lean.with_name('lake.exe')
v=subprocess.Popen([str(lean),'--version'],cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);vb,_=v.communicate();assert v.returncode==0 and b'version 4.33.0' in vb;dump('toolchain.json',dict(status='PASS',inherited_ELAN_TOOLCHAIN_unset=old is not None,Lean_version_stdout=vb.decode('utf8'),actual_version_PID=v.pid,version_exit_code=0,version_resource='CLOSED',Lean_toolchain=pin(R/'lean-toolchain'),Mathlib_manifest=pin(R/'lake-manifest.json'),Mathlib_rev=mathlib['rev'],environment=dict(LEAN_NUM_THREADS='2',PYTHONUTF8='1',ELAN_TOOLCHAIN='ABSENT')))
opened=dict(status='OPEN',compiler='OPEN',Python='OPEN',actual_wrapper_PID=os.getpid(),command=[str(lake),'build','Tests.ProximalBPSMacroscopicRange'],opened_utc=utc(),forced_rebuild=False)
dump('compiler.lease.json',opened)
p=subprocess.Popen(opened['command'],cwd=R,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);out,_=p.communicate();(O/'focused.log').write_bytes(out)
d=dict(status='PASS' if p.returncode==0 else 'FAILED',actual_compiler_PID=p.pid,actual_wrapper_Python_PID=os.getpid(),command=opened['command'],actual_exit_code=p.returncode,finished_utc=utc(),log=pin(O/'focused.log'),source_pins=[pin(R/x) for x in ['AutoSamplingTheory/TechnicalLemmas/Measure/L2PullbackRange.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/MacroscopicRange.lean','Tests/ProximalBPSMacroscopicRange.lean']],forced_rebuild=False,cache_behavior='Actual compiler output preserves replay/cache markers; no forced rebuild or source edits')
dump('focused.status.json',d)
for e in rows:assert same(e,pin(e['path'])),e['path']
dump('compiler.lease.json',dict(status='CLOSED',compiler='CLOSED',Python='CLOSED_AT_FOREGROUND_EXIT',actual_compiler_PID=p.pid,actual_compiler_exit_code=p.returncode,actual_wrapper_Python_PID=os.getpid(),opened=opened,finished_utc=utc(),actual_log=pin(O/'focused.log'),actual_status=pin(O/'focused.status.json'),scope='One independent smallest focused build, not source-fidelity or exact-science VERIFIED'))
print(json.dumps(d));raise SystemExit(p.returncode)
