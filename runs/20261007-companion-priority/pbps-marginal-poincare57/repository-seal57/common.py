import os,sys,pathlib,json,hashlib,datetime,subprocess,re,gzip
sys.dont_write_bytecode=True
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-marginal-poincare57';O=B/'repository-seal57'
SCIENCE='e8a9044ba5a945eaa4b4aecd110b63494fe6c68e';BASE='f311e4296fb5295a2e56e3214d3bd2585f849dcf';ACTOR='whole_math52_repository57'
TARGET='AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare.actual_gaussian_marginal_centered_poincare'
def path(p):
 p=pathlib.Path(str(p).replace('\\','/'));return p if p.is_absolute() else R/p
def load(p):return json.loads(path(p).read_text(encoding='utf8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def logical(d):return sha(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf8'))
def dump(n,d):(O/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def pin(p):
 p=path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n')
 try:s=p.relative_to(R).as_posix()
 except ValueError:s=p.as_posix()
 return dict(path=s,bytes=len(b),lf_bytes=len(lf),raw_sha256=sha(b),lf_sha256=sha(lf))
def matches(a,b):return all(a[k]==b[k] for k in ('bytes','raw_sha256','lf_sha256')) and ('lf_bytes' not in a or a['lf_bytes']==b.get('lf_bytes',a['lf_bytes']))
def git(*a):return subprocess.check_output(['git',*a],cwd=R,text=True,encoding='utf8').strip()
def guard(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
  s=os.fsdecode(args[0]).replace('\\','/').lower()
  if ('/runs/' in s or '/.astis/' in s) and any(re.search(r'(?:pbps|preread|preproof|sourcegraph|future).*?(?:58|59)(?:$|\.)',x) for x in s.split('/')):raise PermissionError('Repository57 excludes future58/59')
sys.addaudithook(guard)
