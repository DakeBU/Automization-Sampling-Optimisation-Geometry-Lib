import pathlib,json,hashlib,os,sys,subprocess
ROOT=pathlib.Path('E:/Samplinglib');P=pathlib.Path(__file__).resolve().parent;ACTOR='independent_whole_math52_primary_first_source_API63'
def H(b):return hashlib.sha256(b).hexdigest()
def C(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def J(p):return json.loads(pathlib.Path(p).read_text(encoding='utf8'))
def W(p,x):pathlib.Path(p).write_bytes(json.dumps(x,ensure_ascii=False,indent=2).encode()+b'\n')
def path(p):
 p=pathlib.Path(p);return p if p.is_absolute() else ROOT/p
def pin(p):
 p=path(p);b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),raw_bytes=len(b),lf_bytes=len(l),raw_sha256=H(b),lf_sha256=H(l))
def matches(q,p=None):
 a=pin(p or q['path']);assert all(a[k]==v for k,v in {'raw_bytes':q.get('raw_bytes',q.get('bytes')),'lf_bytes':q.get('lf_bytes'),'raw_sha256':q.get('raw_sha256'),'lf_sha256':q.get('lf_sha256')}.items() if v is not None),(q,a);return a
