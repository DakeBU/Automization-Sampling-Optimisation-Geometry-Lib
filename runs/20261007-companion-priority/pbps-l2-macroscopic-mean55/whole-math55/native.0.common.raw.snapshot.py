import os,sys,pathlib,json,hashlib,datetime,subprocess,re,shutil
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-l2-macroscopic-mean55';O=B/'whole-math55'
BASE='aa62b6f194cd93d69bec8b3979fb8e65cadb0220';ADV='ASTIS-SA-20261008-PBPSL2MacroscopicMean';TARGET='AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean.actual_macroscopic_l2_mean'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def path(p):p=pathlib.Path(str(p).replace('\\','/'));return p if p.is_absolute() else R/p
def load(p):return json.loads(path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def logical(v):return sha(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8'))
def dump(n,v):(O/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(p):
 p=path(p);b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def equal(e,p=None):
 a=pin(p or e['path']);same=a['raw_sha256']==e['raw_sha256'] and a['lf_sha256']==e['lf_sha256'] and a['bytes']==e.get('bytes',e.get('raw_bytes',a['bytes']))
 if 'lf_bytes' in e:same=same and len(path(p or e['path']).read_bytes().replace(b'\r\n',b'\n'))==e['lf_bytes']
 return same
def strict(n):
 rows=load(B/'math-freeze.json')['inputs'];assert len(rows)==282
 checks=[]
 for e in rows:
  assert equal(e),e['path'];checks.append(dict(original=e,actual=pin(e['path']),ok=True))
 dump(n,dict(status='PASS',all_original_inputs=282,checks=checks));return rows
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True,encoding='utf-8').strip()
def selfcheck(p,field='run_sha256'):
 d=load(p);h=logical({k:v for k,v in d.items() if k!=field});assert h==d[field];return dict(input=pin(p),full_self_field=field,logical_sha256=h,recipe='Complete object minus named self field, sorted compact UTF8 ensure_ascii=False allow_nan=False JSON, no newline')
def exposure_guard(event,args):
 if event!='open' or not args or not isinstance(args[0],(str,bytes,os.PathLike)):return
 s=os.fsdecode(args[0]).replace('\\','/').lower()
 if ('decoder' in s and ('decoder-55' in s or 'decoder55' in s or ('mean55/' in s and '/anonymous' in s))) or s.endswith('/pbps-l2-macroscopic-mean55/source.0.review.json'):
  raise PermissionError('Whole-math55 forbids decoder55 or final source55 verdict exposure')
sys.dont_write_bytecode=True;sys.addaudithook(exposure_guard)
