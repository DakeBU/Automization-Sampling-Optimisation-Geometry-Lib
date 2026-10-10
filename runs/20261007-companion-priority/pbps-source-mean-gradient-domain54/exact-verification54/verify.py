import os,sys,pathlib,json,hashlib,datetime,subprocess,shutil,re,gzip
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-source-mean-gradient-domain54';O=B/'exact-verification54';COMMIT='16797326f3e06a853e2d047f67fde924ac8c1647';ADV='ASTIS-SA-20261008-PBPSSourceMeanGradientDomain';TARGET='AutoSamplingTheory.ExampleCases.ProximalBPS.SourceMeanGradientDomain.literal_source_mean_in_closed_gradient';CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-source-mean-gradient-domain.json';AUDIT='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSSourceMeanGradientDomain.json';PUBSHA='d3a360b37b967ace97266b63ea9fab2aaea2fd1ce4a68e6255be1065ea42b8d3'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def path(p):p=pathlib.Path(p);return p if p.is_absolute() else R/p
def load(p):return json.loads(path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def logical(v):return sha(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode())
def dump(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(p):
 p=path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def equal(e,p=None):
 a=pin(p or e['path']);return a['raw_sha256']==e['raw_sha256'] and a['lf_sha256']==e['lf_sha256'] and a['bytes']==e.get('bytes',e.get('raw_bytes',a['bytes']))
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True,encoding='utf-8').strip()
def strict(n):
 maps={AUDIT:B/'source-admission-before.0.raw.snapshot.audit.json',CELL:B/'source-admission-before.0.raw.snapshot.cell.json'};results=[]
 for label,rows,count in [('math552',load(B/'math-freeze.json')['inputs'],552),('source566',load(B/'reviewer.source.input-bindings.json')['original566_current_pins'],566)]:
  assert len(rows)==count
  for e in rows:
   same=equal(e);snap=None
   if not same:
    p=e['path'].replace('\\','/');assert p in maps,(label,p);assert equal(e,maps[p]);snap=pin(maps[p])
   results.append(dict(set=label,original=e,current=pin(e['path']),current_equal=same,exact_admission_BEFORE_snapshot=snap,ok=same or snap is not None))
 assert len(results)==1118 and all(x['ok'] for x in results);dump(n,dict(status='PASS',count=1118,math=552,source=566,checks=results));return results
def selfcheck(p,field='run_sha256'):
 d=load(p);h=logical({k:v for k,v in d.items() if k!=field});assert h==d[field];return dict(input=pin(p),self_field=field,logical_sha256=h,recipe='SHA256 complete object minus named self field; sorted compact UTF8 ensure_ascii=False allow_nan=False; no newline')
if __name__=='__main__':
 assert not (O/'lease.json').exists(),'Do not repeat focused compiler'
 dump('lease.json',dict(status='OPEN',reviewer='whole_math52',opened_utc=utc(),actual_python_pid=os.getpid(),read='OPEN',write='OPEN',Python='OPEN',compiler='NOT_STARTED',scope='Independent exact science54 verification; own outputs plus authorized54 VERIFIED/cell transition only. No proof/shared-import/Registry/site edits, commits, pushes or future55 reads.'))
 assert git('rev-parse','HEAD')==COMMIT and not git('diff','--name-only','HEAD')
 parent=git('rev-parse','HEAD^');assert parent=='cfcc67b5dd956b3d4fc1fb7e578ad241bd2618b3'
 strict('inputs.pre.json')
 for p,n in [(CELL,'before.cell.raw.snapshot.json'),(AUDIT,'before.audit.raw.snapshot.json')]: (O/n).write_bytes(path(p).read_bytes())
 paths=git('diff','--name-only',parent,COMMIT).splitlines();assert len(paths)==810
 assert not any(re.search(r'(?i)(?:^|/)[^/]*55(?:/|$)',p) for p in paths)
 bindings=[]
 for p in paths:
  blob=subprocess.check_output(['git','show',COMMIT+':'+p],cwd=R);cur=path(p).read_bytes();assert blob.replace(b'\r\n',b'\n')==cur.replace(b'\r\n',b'\n'),p
  bindings.append(dict(current=pin(p),Git_blob_raw_sha256=sha(blob),Git_blob_LF_sha256=sha(blob.replace(b'\r\n',b'\n')),current_LF_equal=True))
 dump('git-owned-file-bindings.json',dict(status='PASS',checked_commit=COMMIT,parent=parent,count=810,bindings=bindings))
 env=dict(os.environ);original=env.pop('ELAN_TOOLCHAIN',None);env.update(PYTHONUTF8='1',LEAN_NUM_THREADS='2');lake=shutil.which('lake');assert lake
 assert path('lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0';manifest=load('lake-manifest.json');assert next(x for x in manifest['packages'] if x['name']=='mathlib')['rev']=='db584cd6d46c92f209a44c0f1c829460d327499d'
 processes=subprocess.check_output(['powershell','-NoProfile','-Command',"Get-CimInstance Win32_Process | Where-Object { $_.Name -in @('lean.exe','lake.exe') } | Select-Object ProcessId,Name,CommandLine | ConvertTo-Json -Compress"],encoding='utf-8').strip();assert not processes,processes
 version=subprocess.run([lake,'env','lean','--version'],cwd=R,env=env,capture_output=True);(O/'lean.pin.log').write_bytes(version.stdout+version.stderr);assert version.returncode==0 and b'4.33.0' in version.stdout
 dump('environment.json',dict(python=sys.executable,actual_python_pid=os.getpid(),lake=lake,Lean_pin=pin('lean-toolchain'),Mathlib_manifest=pin('lake-manifest.json'),ELAN_TOOLCHAIN_inherited_present=original is not None,ELAN_TOOLCHAIN_removed=True,LEAN_NUM_THREADS='2',PYTHONUTF8='1',precompiler_processes=processes,lean_version_exit=0,lean_version_log=pin(O/'lean.pin.log')))
 command=[lake,'build','Tests.ProximalBPSSourceMeanGradientDomain'];start=utc()
 with (O/'focused.log').open('wb') as log:
  proc=subprocess.Popen(command,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT);lease=dict(status='OPEN',compiler='OPEN',Python='OPEN',process_id=proc.pid,opened_utc=start,command=command,force_rebuild=False);dump('compiler.lease.json',lease);code=proc.wait()
 end=utc();logpin=pin(O/'focused.log');dump('focused.status.json',dict(command=command,process_id=proc.pid,actual_python_pid=os.getpid(),exit_code=code,started_utc=start,finished_utc=end,log=logpin,source=pin('Tests/ProximalBPSSourceMeanGradientDomain.lean'),forced_rebuild=False,checked_commit=COMMIT));lease.update(status='CLOSED',compiler='CLOSED',Python='CLOSED',closed_utc=end,exit_code=code,log=logpin);dump('compiler.lease.json',lease);strict('inputs.post-build.json');assert code==0
 print(json.dumps(dict(status='focusedPASS',checked_commit=COMMIT,actual_compiler_PID=proc.pid,exit_code=code,ownedGitfiles=810,all1118_original_inputs='PASS',log=logpin,compiler_lease='CLOSED',forced_rebuild=False)))
