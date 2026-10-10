import os,sys,pathlib,json,hashlib,subprocess,datetime,re
ROOT=pathlib.Path('E:/Samplinglib');os.chdir(ROOT)
R=ROOT/'runs/20261007-companion-priority/pbps-centered-defect-preproof59';D=R/'independent-statement59';ACTOR='whole_math52_statement_topology59'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(q):return json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def load(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,q):pathlib.Path(p).write_bytes((json.dumps(q,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode())
def path(p):return pathlib.Path(p) if pathlib.Path(p).is_absolute() else ROOT/p
def pin(p):
 p=path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def check(row):
 a=pin(row['path']);assert a['bytes']==row.get('bytes',row.get('raw_bytes')) and a['raw_sha256']==row['raw_sha256'] and a['lf_sha256']==row['lf_sha256'] and ('lf_bytes'not in row or a['lf_bytes']==row['lf_bytes']);return a
def selfcheck(q,k):assert sha(canon({a:b for a,b in q.items() if a!=k}))==q[k]
