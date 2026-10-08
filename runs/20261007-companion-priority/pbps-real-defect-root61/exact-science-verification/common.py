import hashlib,json,pathlib,os,subprocess,sys
ROOT=pathlib.Path('E:/Samplinglib'); R=ROOT/'runs/20261007-companion-priority/pbps-real-defect-root61'; P=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/'tools'))
SCI='bcd245d90b21b899acb9937fc54dffcea20e86ee'; BASE='63c74351566095343985d36dfcb13dca32a666b7'; SAU='ASTIS-SA-20261009-PBPSPositiveRealDefectRoot'; ACTOR='independent_whole_math52_exact61'
def H(b): return hashlib.sha256(b).hexdigest()
def C(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def J(p): return json.loads(pathlib.Path(p).read_text(encoding='utf8'))
def W(p,x): pathlib.Path(p).write_bytes(json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False).encode()+b'\n')
def path(p):
 x=pathlib.Path(p); return x if x.is_absolute() else ROOT/x
def pin(p):
 x=path(p); b=x.read_bytes(); l=b.replace(b'\r\n',b'\n')
 return dict(path=x.as_posix(),raw_bytes=len(b),lf_bytes=len(l),raw_sha256=H(b),lf_sha256=H(l))
def matches(row,p=None):
 a=pin(p or row['path']); fields={'raw_bytes':row.get('raw_bytes',row.get('bytes')),'lf_bytes':row.get('lf_bytes'),'raw_sha256':row.get('raw_sha256'),'lf_sha256':row.get('lf_sha256')}
 assert all(a[k]==v for k,v in fields.items() if v is not None),(row,a)
 return a
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT)
def head(): return git('rev-parse','HEAD').decode().strip()
def snapshot(p,label):
 original=pin(p); b=path(p).read_bytes(); ident=H(original['path'].encode())[:18]; dest=P/(label+'-'+ident+'.raw.snapshot'); dest.write_bytes(b)
 return dict(original=original,raw_snapshot=pin(dest))
def invoke(name,cmd,env=None):
 with (P/(name+'.stdout.log')).open('wb') as out,(P/(name+'.stderr.log')).open('wb') as err:
  proc=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=out,stderr=err); rc=proc.wait()
 obj=dict(name=name,command=cmd,actual_wrapper_PID=os.getpid(),actual_PID=proc.pid,exit_code=rc,terminal_closed=True,stdout=pin(P/(name+'.stdout.log')),stderr=pin(P/(name+'.stderr.log')))
 W(P/(name+'.status.json'),obj); return obj
