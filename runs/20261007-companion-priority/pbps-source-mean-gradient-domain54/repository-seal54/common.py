import os, sys, json, hashlib, pathlib, datetime, subprocess, re, gzip
R=pathlib.Path('E:/Samplinglib')
B=R/'runs/20261007-companion-priority/pbps-source-mean-gradient-domain54'
O=B/'repository-seal54'
SCI='16797326f3e06a853e2d047f67fde924ac8c1647'
HEAD='d6341c498a5a2f6e3f73f540896b0d1b7dbe4bd6'
ADV='ASTIS-SA-20261008-PBPSSourceMeanGradientDomain'
TARGET='AutoSamplingTheory.ExampleCases.ProximalBPS.SourceMeanGradientDomain.literal_source_mean_in_closed_gradient'
CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-source-mean-gradient-domain.json'
AUDIT='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSSourceMeanGradientDomain.json'
PUBSHA='d3a360b37b967ace97266b63ea9fab2aaea2fd1ce4a68e6255be1065ea42b8d3'
guard_denied=[]
def future_guard(event,args):
 if event not in {'open','os.listdir','os.scandir'} or not args or not isinstance(args[0],(str,bytes,os.PathLike)): return
 try:
  p=pathlib.Path(os.fsdecode(args[0])).resolve(); rel=p.relative_to(R)
 except (ValueError,OSError): return
 parts=rel.parts if event!='open' else rel.parts[:-1]
 if 'private.future55' in str(rel).lower() or (parts and parts[0]=='runs' and any(x.endswith('55') for x in parts)):
  guard_denied.append(str(rel)); raise PermissionError('Explicit future55 directory read guard: '+str(rel))
sys.dont_write_bytecode=True
sys.addaudithook(future_guard)
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def path(p):
 p=pathlib.Path(str(p).replace('\\','/')); return p if p.is_absolute() else R/p
def load(p): return json.loads(path(p).read_text(encoding='utf-8'))
def sha(b): return hashlib.sha256(b).hexdigest()
def logical(v): return sha(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8'))
def dump(n,v): (O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(p):
 p=path(p); b=p.read_bytes(); return dict(path=p.relative_to(R).as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def equal(e,p=None):
 a=pin(p or e['path']); return a['raw_sha256']==e['raw_sha256'] and a['lf_sha256']==e['lf_sha256'] and a['bytes']==e.get('bytes',e.get('raw_bytes',a['bytes']))
def git(*a): return subprocess.check_output(['git',*a],cwd=R,text=True,encoding='utf-8').strip()
def selfcheck(p,field='run_sha256'):
 d=load(p); h=logical({k:v for k,v in d.items() if k!=field}); assert h==d[field],str(p)
 return dict(input=pin(p),self_field=field,logical_sha256=h,recipe='SHA256 complete object minus named self field; sorted compact UTF8 ensure_ascii=False allow_nan=False; no newline')
def strict():
 maps={AUDIT:B/'source-admission-before.0.raw.snapshot.audit.json',CELL:B/'source-admission-before.0.raw.snapshot.cell.json'}; out=[]
 for label,rows,count in [('math552',load(B/'math-freeze.json')['inputs'],552),('source566',load(B/'reviewer.source.input-bindings.json')['original566_current_pins'],566)]:
  assert len(rows)==count
  for e in rows:
   same=equal(e); mapped=None
   if not same:
    p=e['path'].replace('\\','/'); assert p in maps,(label,p); assert equal(e,maps[p]); mapped=pin(maps[p])
   out.append(dict(set=label,original=e,current=pin(e['path']),current_equal=same,explicit_original_BEFORE_snapshot=mapped,ok=True))
 return out
if __name__=='__main__':
 assert not (O/'lease.json').exists()
 dump('lease.json',dict(status='OPEN',reviewer='whole_math52',stage='readonly scoped repository ProofSeal54',opened_utc=utc(),actual_opening_python_pid=os.getpid(),read='OPEN',write='OPEN',Python='OPEN',compiler='NOT_STARTED_CLOSED',scope='Only repository-seal54 outputs. No compiler, canonical edits, status transition, commit/push, future55 source/proof, or ExpositionSeal.'))
 dump('opening.json',dict(checked_science=SCI,checked_integration=HEAD,actual_python_pid=os.getpid(),python=sys.executable,PythonUTF8=os.environ.get('PYTHONUTF8'),opening_lease=pin(O/'lease.json')))
 print('Own readonly repository-seal54 lease OPEN; compiler NOT_STARTED_CLOSED.')
