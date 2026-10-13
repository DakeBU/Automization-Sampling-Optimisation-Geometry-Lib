import pathlib,json,hashlib,sys,os,subprocess,time,ctypes,re
from ctypes import wintypes
ROOT=pathlib.Path('E:/Samplinglib');os.chdir(ROOT);R=ROOT/'runs/20261007-companion-priority/pbps-centered-defect59';D=R/'independent-math-review';D.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
freeze=load(R/'math-freeze.json');assert len(freeze['inputs'])==27
opening=[]
for row in freeze['inputs']:
 a=pin(row['path']);assert a['bytes']==row['raw_bytes'] and a['raw_sha256']==row['raw_sha256'] and a['lf_sha256']==row['lf_sha256'];opening.append(a)
write(D/'inputs.open.json',dict(freeze=pin(R/'math-freeze.json'),inputs=opening,count=len(opening)))
env=os.environ.copy();override=env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1';env['PYTHONDONTWRITEBYTECODE']='1'
assert (ROOT/'lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
assert next(x for x in load(ROOT/'lake-manifest.json')['packages'] if x['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
head=subprocess.run(['git','rev-parse','HEAD'],capture_output=True,check=True,text=True).stdout.strip();assert head==freeze['checked_base_commit']
write(D/'lease.open.json',dict(status='OPEN',actor='/root/whole_math52',actual_Python_pid=os.getpid(),scope='Independent COMPLETE mathematics/proof review59 and one nonforced focused build',checked_base=head,inherited_ELAN_TOOLCHAIN_removed=override))
version=subprocess.run(['lake','env','lean','--version'],env=env,capture_output=True);assert version.returncode==0 and b'4.33.0' in version.stdout;(D/'Lean.version.log').write_bytes(version.stdout+version.stderr)
codepaths=[ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredDefectOperator.lean',ROOT/'Tests/ProximalBPSCenteredDefect.lean']
headers=[];scans=[]
for i,p in enumerate(codepaths):
 b=p.read_bytes();s=b.decode('utf8');h=s[s.index('theorem '):s.index(' := by\n')].rstrip()+'\n'
 expected=ROOT/f'runs/20261007-companion-priority/pbps-centered-defect-preproof59/independent-elab-type-second/header{i}.inline-kernel-proposed.lean'
 assert h.encode()==expected.read_bytes();headers.append(dict(index=i,declaration=freeze['mathematical_declarations'][i],source=pin(p),accepted_header=pin(expected),signature_raw_LF_sha256=sha(h.encode()),signature_bytes=len(h.encode())))
 assert len(re.findall(r'^theorem ',s,re.M))==1 and not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',s) and 'trace "' not in s
 scans.append(dict(source=pin(p),theorems=1,private_providers=0,authored_placeholders=0,traces=0))
 (D/f'{i}.{sha(p.as_posix().encode())[:16]}.qualified.raw.snapshot').write_bytes(b)
write(D/'signature-and-fake-scan.json',dict(exact_headers=headers,authored_scans=scans))
extra=[ROOT/'.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Positive.lean',ROOT/'.lake/packages/mathlib/Mathlib/Topology/Algebra/Module/ContinuousLinearMap/Basic.lean']
write(D/'API.inputs.json',dict(inputs=[pin(x) for x in extra]))
class Entry(ctypes.Structure):
 _fields_=[('dwSize',wintypes.DWORD),('cntUsage',wintypes.DWORD),('th32ProcessID',wintypes.DWORD),('th32DefaultHeapID',ctypes.c_size_t),('th32ModuleID',wintypes.DWORD),('cntThreads',wintypes.DWORD),('th32ParentProcessID',wintypes.DWORD),('pcPriClassBase',ctypes.c_long),('dwFlags',wintypes.DWORD),('szExeFile',wintypes.WCHAR*260)]
k=ctypes.WinDLL('kernel32',use_last_error=True);k.CreateToolhelp32Snapshot.restype=wintypes.HANDLE;k.Process32FirstW.argtypes=[wintypes.HANDLE,ctypes.POINTER(Entry)];k.Process32NextW.argtypes=[wintypes.HANDLE,ctypes.POINTER(Entry)];k.CloseHandle.argtypes=[wintypes.HANDLE]
def tree(pid):
 h=k.CreateToolhelp32Snapshot(2,0);e=Entry();e.dwSize=ctypes.sizeof(e);rows=[]
 if k.Process32FirstW(h,ctypes.byref(e)):
  while True:
   rows.append(dict(pid=e.th32ProcessID,parent_pid=e.th32ParentProcessID,exe=e.szExeFile))
   if not k.Process32NextW(h,ctypes.byref(e)):break
 k.CloseHandle(h);ids={pid};changed=True
 while changed:
  changed=False
  for r in rows:
   if r['parent_pid'] in ids and r['pid'] not in ids:ids.add(r['pid']);changed=True
 return [r for r in rows if r['pid'] in ids]
cmd=['lake','build','Tests.ProximalBPSCenteredDefect']
with (D/'focused.stdout.log').open('wb') as out,(D/'focused.stderr.log').open('wb') as err:
 p=subprocess.Popen(cmd,env=env,stdout=out,stderr=err);observed={}
 while p.poll() is None:
  for row in tree(p.pid):observed[row['pid']]=row
  time.sleep(.05)
 exit_code=p.wait()
result=dict(actual_command=cmd,lake_pid=p.pid,observed_processes=list(observed.values()),actual_exit_code=exit_code,compiler='CLOSED',Python_pid=os.getpid(),nonforced=True,stdout=pin(D/'focused.stdout.log'),stderr=pin(D/'focused.stderr.log'))
write(D/'focused.status.json',result)
assert exit_code==0
out=(D/'focused.stdout.log').read_text(encoding='utf8');assert 'Build completed successfully' in out and 'sorryAx' not in out
closures=[]
for name in freeze['mathematical_declarations']:
 m=re.search(re.escape(name)+r"' depends on axioms: \[([^]]*)\]",out,re.S);assert m,name
 ax=[x.strip() for x in m.group(1).replace('\n',' ').split(',')];assert set(ax)=={'propext','Classical.choice','Quot.sound'};closures.append(dict(declaration=name,axioms=ax))
write(D/'axiom-closures.json',dict(closures=closures,actual_stdout=pin(D/'focused.stdout.log'),compile_mode='Nonforced actual lake build, compiler/replayed logs distinguished by actual stdout'))
for row in opening:assert pin(row['path'])==row
write(D/'input-postcheck.json',dict(inputs=opening,count=27,all_unchanged=True))
print(json.dumps(dict(status='INDEPENDENT_FOCUSED_PASS',actual_exit_code=exit_code,lake_pid=p.pid,Lean_pids=[x['pid'] for x in observed.values() if x['exe'].lower()=='lean.exe'],strict_frozen_inputs=27,closures=closures,Python_pid=os.getpid())),flush=True)
