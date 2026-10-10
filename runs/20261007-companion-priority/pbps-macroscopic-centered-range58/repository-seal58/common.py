import pathlib,os,sys,json,hashlib,datetime,subprocess,re
ROOT=pathlib.Path('E:/Samplinglib');os.chdir(ROOT)
R=ROOT/'runs/20261007-companion-priority/pbps-macroscopic-centered-range58';D=R/'repository-seal58'
SCI='8c8847715c1d4c3033224b069d8dd694f2a4bd30';HEAD='a7cafde7957a8562bcd697d89c56b14768914c66';ACTOR='whole_math52_repository58'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def path(p):return pathlib.Path(p) if pathlib.Path(p).is_absolute() else ROOT/p
def pin(p):
 p=path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def check(row):
 a=pin(row['path']);assert a['bytes']==row.get('bytes',row.get('raw_bytes')) and a['raw_sha256']==row['raw_sha256'] and a['lf_sha256']==row['lf_sha256'] and ('lf_bytes' not in row or a['lf_bytes']==row['lf_bytes']),row;return a
def rows(q):
 if isinstance(q,dict):
  if 'path' in q and 'raw_sha256' in q and 'lf_sha256' in q and ('bytes'in q or 'raw_bytes'in q):yield q
  for v in q.values():yield from rows(v)
 elif isinstance(q,list):
  for v in q:yield from rows(v)
def selfcheck(q,k):assert sha(canon({a:b for a,b in q.items() if a!=k}))==q[k]
def diff(a,b,p=''):
 if type(a)!=type(b):return[p]
 if isinstance(a,dict):return sum([diff(a.get(k),b.get(k),p+'/'+k) for k in sorted(set(a)|set(b))],[])
 if isinstance(a,list):return[p] if len(a)!=len(b) else sum([diff(x,y,p+'/'+str(i)) for i,(x,y) in enumerate(zip(a,b))],[])
 return[] if a==b else[p]
