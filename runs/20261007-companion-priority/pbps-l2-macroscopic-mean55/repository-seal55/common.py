import os,sys,pathlib,json,hashlib,datetime,subprocess,re,gzip,struct
sys.dont_write_bytecode=True
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-l2-macroscopic-mean55';O=B/'repository-seal55';SCI='4f71a36d56500fda7f86e8080f695a514913950a';HEAD='aa34b6a4ff0f9b24c497472d25ce072ecb8d091a';ACTOR='whole_math52';TARGET='AutoSamplingTheory.ExampleCases.ProximalBPS.L2MacroscopicMean.actual_macroscopic_l2_mean';ADV='ASTIS-SA-20261008-PBPSL2MacroscopicMean';CELL='research-wiki/frontier-cells/ASTIS-SW-PBPS-l2-macroscopic-mean.json';AUDIT='research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261008-PBPSL2MacroscopicMean.json'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def logical(d):return sha(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode())
def path(p):p=pathlib.Path(str(p).replace('\\','/'));return p if p.is_absolute() else R/p
def load(p):return json.loads(path(p).read_text(encoding='utf-8'))
def dump(p,d):(O/p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(p):
 p=path(p);b=p.read_bytes()
 try:s=p.relative_to(R).as_posix()
 except ValueError:s=p.as_posix()
 return dict(path=s,bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def equal(e,p=None):
 p=p or e['path'];a=pin(p);return a['raw_sha256']==e['raw_sha256'] and a['lf_sha256']==e['lf_sha256'] and a['bytes']==e.get('bytes',e.get('raw_bytes',a['bytes'])) and ('lf_bytes' not in e or len(path(p).read_bytes().replace(b'\r\n',b'\n'))==e['lf_bytes'])
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True,encoding='utf-8').strip()
def selfcheck(p,field='run_sha256'):
 d=load(p);h=logical({k:v for k,v in d.items() if k!=field});assert h==d[field],(p,field);return dict(input=pin(p),self_field=field,logical_sha256=h,recipe='Complete object minus ONLY named self field sorted compact UTF8 ensure_ascii=False allow_nan=False no newline')
reads=set()
def guard(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
  s=os.fsdecode(args[0]).replace('\\','/').lower()
  if '/runs/' in s and any(re.search(r'(?:pbps|preread|sourcegraph|future).*?(?:56|57)$',c) for c in s.split('/')):raise PermissionError('ProofSeal55 excludes future packet56/57')
sys.addaudithook(guard)
