import os,sys,json,hashlib,pathlib,subprocess,datetime,re,gzip
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-literal-reflected-mean53';O=B/'exact-verification53'
COMMIT='9f0305db380966529eb3b0fc17a62aa9bcd47a85';PARENT='241e01d0d1917a6400a0f43ea48697b72cee88df'
TARGET='AutoSamplingTheory.ExampleCases.ProximalBPS.LiteralReflectedMean.reflected_gibbs_mean_c1';ADV='ASTIS-SA-20261008-PBPSLiteralReflectedMean';CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-literal-reflected-mean.json';AUDIT='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSLiteralReflectedMean.json'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(path(p).read_text(encoding='utf-8'))
def path(p):
 p=pathlib.Path(p);return p if p.is_absolute() else R/p
def dump(n,v):path(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def logical(v):return sha(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
def pin(p):
 p=path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def equal(e,p=None):
 a=pin(p or e['path']);return all(a[k]==e[k] for k in ('raw_sha256','lf_sha256')) and a['bytes']==e.get('bytes',e.get('raw_bytes',a['bytes']))
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True,encoding='utf-8').strip()
def strict(n):
 math=load(B/'math-freeze.json')['inputs'];src=load(B/'source.0.review.json')['input_artifacts'];checks=[]
 mapping={AUDIT:B/'source-admission-before.0.raw.snapshot.audit.json',CELL:B/'source-admission-before.0.raw.snapshot.cell.json'}
 for label,rows in [('math492',math),('source506',src)]:
  for e in rows:
   actual=pin(e['path']);same=equal(e);snapshot=None
   if not same:
    assert label=='source506' and e['path'] in mapping,(label,e['path'])
    snapshot=pin(mapping[e['path']]);assert equal(e,mapping[e['path']])
   checks.append(dict(set=label,expected=e,current=actual,current_equal=same,admitted_original_snapshot=snapshot,ok=same or snapshot is not None))
 inv=load(B/'reviewer.source.inventory.json');assert len(inv['rows'])==506
 for row in inv['rows']:assert equal(row['snapshot']) and row['original'] in src and equal(row['original'],row['snapshot']['path'])
 assert len(math)==492 and len(src)==506
 result=dict(utc=utc(),count_math=492,count_source=506,all_strict_pins_or_exact_admitted_original_snapshots_pass=True,source_opening_snapshot_rows=506,checks=checks)
 dump(n,result);return result
if __name__=='__main__':
 dump('lease.json',dict(status='OPEN',reviewer='whole_math52',opened_utc=utc(),pid=os.getpid(),read_lease='OPEN',write_lease='OPEN',Python_lease='OPEN',compiler_lease='NOT_STARTED',checked_commit=COMMIT))
 assert git('rev-parse','HEAD')==COMMIT and git('rev-parse',COMMIT+'^')==PARENT
 assert not git('diff','--name-only','HEAD')
 strict('inputs.pre.json')
 for p in [AUDIT,CELL]: (O/('before.'+pathlib.Path(p).name)).write_bytes(path(p).read_bytes())
 changed=git('diff','--name-only',PARENT,COMMIT).splitlines();assert len(changed)==1152 and not any(re.search(r'54(?:/|\.|-)',p) for p in changed)
 dump('commit-ownedpaths.json',dict(commit=COMMIT,parent=PARENT,count=len(changed),paths=changed,no_future54_integrated=True))
 env=dict(os.environ);inherited=env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1'
 def query(args):
  p=subprocess.run(args,cwd=R,env=env,capture_output=True,text=True,encoding='utf-8');assert p.returncode==0;(O/(args[0]+'.pin.log')).write_text(p.stdout+p.stderr,encoding='utf-8');return p.stdout.strip()
 lean=query(['lean','--version']);tc=path('lean-toolchain').read_text().strip();manifest=load('lake-manifest.json');mp=next(p for p in manifest['packages'] if p['name']=='mathlib');mh=git('-C','.lake/packages/mathlib','rev-parse','HEAD')
 assert tc=='leanprover/lean4:v4.33.0' and '4.33.0' in lean and mh==mp['rev']
 dump('environment.json',dict(python=sys.executable,version=sys.version,ELAN_TOOLCHAIN_unset=True,inherited_ELAN_TOOLCHAIN=inherited,LEAN_NUM_THREADS=2,PYTHONUTF8=1,lean=lean,toolchain=tc,mathlib=mp,mathlib_checkout=mh,checked_commit=COMMIT))
 cmd=['lake','build','Tests.ProximalBPSReflectedMeanRegularity'];opened=utc()
 with (O/'focused.log').open('wb') as log:
  p=subprocess.Popen(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT)
  dump('compiler.lease.json',dict(status='OPEN',compiler_pid=p.pid,command=cmd,opened_utc=opened,owner='whole_math52'));print(json.dumps(dict(compiler_pid=p.pid,status='RUNNING')),flush=True);code=p.wait()
 st=dict(command=cmd,compiler_pid=p.pid,exit_code=code,opened_utc=opened,closed_utc=utc(),log=pin(O/'focused.log'),checked_commit=COMMIT,production=pin('AutoSamplingTheory/ExampleCases/ProximalBPS/LiteralReflectedMean.lean'),test=pin('Tests/ProximalBPSReflectedMeanRegularity.lean'))
 dump('focused.status.json',st);dump('compiler.lease.json',dict(status='CLOSED',compiler_pid=p.pid,exit_code=code,command=cmd,opened_utc=opened,closed_utc=utc(),log=st['log'],owner='whole_math52'))
 strict('inputs.post-build.json');assert code==0;print(json.dumps(st),flush=True)
