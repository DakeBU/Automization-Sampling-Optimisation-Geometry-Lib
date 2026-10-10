import os,sys,pathlib,json,hashlib,datetime,subprocess,re
sys.dont_write_bytecode=True
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-macroscopic-centered-range58';O=B/'whole-math58';BASE='d6ce167820c2d897fe06b4ba9417e858dbaa008f';ACTOR='whole_math52_whole58'
def path(p):
 p=pathlib.Path(str(p).replace('\\','/'));return p if p.is_absolute() else R/p
def load(p):return json.loads(path(p).read_text(encoding='utf8'))
def sha(b):return hashlib.sha256(b).hexdigest()
def logical(d):return sha(json.dumps(d,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf8'))
def dump(n,d):(O/n).write_bytes((json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
def pin(p):
 p=path(p);b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(lf),raw_sha256=sha(b),lf_sha256=sha(lf))
def same(e,a):return all(e[k]==a[k] for k in ['bytes','raw_sha256','lf_sha256']) and ('lf_bytes' not in e or e['lf_bytes']==a['lf_bytes'])
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def guard(event,args):
 if event=='open' and args and isinstance(args[0],(str,bytes,os.PathLike)):
  s=os.fsdecode(args[0]).replace('\\','/').lower()
  if ('/runs/' in s or '/.astis/' in s) and any(('59' in x or '60' in x) and any(k in x for k in ['pbps','preproof','sourcegraph','preread','future']) for x in s.split('/')):raise PermissionError('Whole-math58 excludes future59/60')
  if '/pbps-macroscopic-centered-range58/' in s and any(k in s for k in ['/source-review58/','/anonymous-decoder/','/decoder58/']):raise PermissionError('Independent math58 excludes postproof decoder/source verdict')
sys.addaudithook(guard)
