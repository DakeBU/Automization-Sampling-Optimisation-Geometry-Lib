import os,sys,pathlib,json,hashlib,datetime,subprocess,re,shutil
sys.dont_write_bytecode=True
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-marginal-poincare57';O=B/'exact-verification57';BASE='e8a9044ba5a945eaa4b4aecd110b63494fe6c68e';ACTOR='whole_math52_exact57';TARGET='AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare.actual_gaussian_marginal_centered_poincare'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def path(p):p=pathlib.Path(str(p).replace('\\','/'));return p if p.is_absolute() else R/p
def load(p):return json.loads(path(p).read_text(encoding='utf-8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def logical(d):return sha(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8'))
def dump(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(p):
 p=path(p);b=p.read_bytes()
 try:s=p.relative_to(R).as_posix()
 except ValueError:s=p.as_posix()
 return dict(path=s,bytes=len(b),lf_bytes=len(b.replace(b'\r\n',b'\n')),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def equal(e,p=None):
 p=p or e['path'];a=pin(p);return a['raw_sha256']==e['raw_sha256'] and a['lf_sha256']==e['lf_sha256'] and a['bytes']==e.get('bytes',e.get('raw_bytes',a['bytes'])) and ('lf_bytes' not in e or len(path(p).read_bytes().replace(b'\r\n',b'\n'))==e['lf_bytes'])
def git(*args):return subprocess.check_output(['git',*args],cwd=R,text=True,encoding='utf-8').strip()
def selfcheck(p,field='run_sha256'):
 d=load(p);h=logical({k:v for k,v in d.items() if k!=field});assert h==d[field],(p,field);return dict(input=pin(p),self_field=field,logical_sha256=h,recipe='Complete object minus ONLY named self field; sorted compact UTF8 ensure_ascii=False allow_nan=False no newline')
def strict(name):
 rows=load(B/'math-freeze.json')['inputs'];assert len(rows)==602
 checks=[]
 for e in rows:assert equal(e),e['path'];checks.append(dict(original=e,actual=pin(e['path']),ok=True))
 dump(name,dict(status='PASS',original_count=602,checks=checks));return rows
def guard(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
  s=os.fsdecode(args[0]).replace('\\','/').lower()
  if '/runs/' in s and any(re.search(r'(?:pbps|preread|sourcegraph|future).*?(?:58|59)$',c) for c in s.split('/')):raise PermissionError('Whole-math57 excludes future58/59')

sys.addaudithook(guard)
