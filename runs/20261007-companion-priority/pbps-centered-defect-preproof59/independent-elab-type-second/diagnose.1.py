import pathlib,json,hashlib,os,sys,subprocess,time,ctypes
from ctypes import wintypes
ROOT=pathlib.Path('E:/Samplinglib');os.chdir(ROOT)
R=ROOT/'runs/20261007-companion-priority/pbps-centered-defect-preproof59';D=R/'independent-elab-type-second/phase1';P=ROOT/'.astis/pbps-centered-defect59/independent-elab-type-second/phase1'
D.mkdir(exist_ok=True);P.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode())
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
env=os.environ.copy();inherited=env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1';env['PYTHONDONTWRITEBYTECODE']='1'
assert (ROOT/'lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
assert next(x for x in json.loads((ROOT/'lake-manifest.json').read_bytes())['packages'] if x['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
write(D/'lease.open.json',dict(status='OPEN',actor='/root/whole_math52',python_pid=os.getpid(),inherited_ELAN_TOOLCHAIN_removed=inherited,scope='Independent bounded declaration/elaboration diagnostics59'))
paths=[R/'header0.lean',R/'header1.lean',ROOT/'.astis/pbps-centered-defect59/positive-fragment.lean',ROOT/'.astis/pbps-centered-defect59/positive-min-repro.lean',ROOT/'.astis/pbps-centered-defect59/centered-fragment.lean',ROOT/'.astis/pbps-centered-defect59/mean-fragment.lean',ROOT/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Positive.lean',ROOT/'lean-toolchain',ROOT/'lake-manifest.json']
inputs=[pin(x) for x in paths];write(D/'inputs.open.json',dict(inputs=inputs))
for i,x in enumerate(paths[:6]):(D/(str(i)+'.'+sha(x.as_posix().encode())[:16]+'.raw.snapshot')).write_bytes(x.read_bytes())
minimum=paths[3].read_text(encoding='utf8');positive=paths[2].read_text(encoding='utf8')
variants={name:(P/(name+'.lean')).read_text(encoding='utf8') for name in ['full-type-inline-kernel','full-type-no-centered-tail','consumer-complete-type']}
for name,content in variants.items():(P/(name+'.lean')).write_text(content,encoding='utf8',newline='\n')
# Enumerate only actual foreground process descendants to record the real Lean PID.
class Entry(ctypes.Structure):
 _fields_=[('dwSize',wintypes.DWORD),('cntUsage',wintypes.DWORD),('th32ProcessID',wintypes.DWORD),('th32DefaultHeapID',ctypes.c_size_t),('th32ModuleID',wintypes.DWORD),('cntThreads',wintypes.DWORD),('th32ParentProcessID',wintypes.DWORD),('pcPriClassBase',ctypes.c_long),('dwFlags',wintypes.DWORD),('szExeFile',wintypes.WCHAR*260)]
k=ctypes.WinDLL('kernel32',use_last_error=True);k.CreateToolhelp32Snapshot.restype=wintypes.HANDLE;k.Process32FirstW.argtypes=[wintypes.HANDLE,ctypes.POINTER(Entry)];k.Process32NextW.argtypes=[wintypes.HANDLE,ctypes.POINTER(Entry)];k.CloseHandle.argtypes=[wintypes.HANDLE]
def tree(pid):
 h=k.CreateToolhelp32Snapshot(2,0);e=Entry();e.dwSize=ctypes.sizeof(e);rows=[]
 if k.Process32FirstW(h,ctypes.byref(e)):
  while True:
   rows.append(dict(pid=e.th32ProcessID,parent_pid=e.th32ParentProcessID,exe=e.szExeFile))
   if not k.Process32NextW(h,ctypes.byref(e)):break
 k.CloseHandle(h);ids={pid};change=True
 while change:
  change=False
  for row in rows:
   if row['parent_pid'] in ids and row['pid'] not in ids:ids.add(row['pid']);change=True
 return [r for r in rows if r['pid'] in ids]
version=subprocess.run(['lake','env','lean','--version'],env=env,capture_output=True);assert version.returncode==0 and b'4.33.0' in version.stdout
(D/'toolchain.version.log').write_bytes(version.stdout+version.stderr)
results=[]
for name in variants:
 cmd=['lake','env','lean',str(P/(name+'.lean'))]
 with (D/(name+'.stdout.log')).open('wb') as out,(D/(name+'.stderr.log')).open('wb') as err:
  child=subprocess.Popen(cmd,env=env,stdout=out,stderr=err);observed={}
  while child.poll() is None:
   for row in tree(child.pid):observed[row['pid']]=row
   time.sleep(.05)
  exit_code=child.wait()
 result=dict(name=name,command=cmd,lake_pid=child.pid,observed_processes=list(observed.values()),actual_exit_code=exit_code,source=pin(P/(name+'.lean')),stdout=pin(D/(name+'.stdout.log')),stderr=pin(D/(name+'.stderr.log')),compiler_status='CLOSED')
 results.append(result);write(D/(name+'.status.json'),result);print(json.dumps(dict(name=name,actual_exit_code=exit_code,observed_processes=list(observed.values()))),flush=True)
write(D/'compiler.results.json',dict(results=results,all_compiler_leases='CLOSED',version=pin(D/'toolchain.version.log'),inputs=inputs,python_pid=os.getpid()))
assert all(pin(x['path'])==x for x in inputs)
print('DIAGNOSTICS_FOREGROUND_COMPLETE',flush=True)
