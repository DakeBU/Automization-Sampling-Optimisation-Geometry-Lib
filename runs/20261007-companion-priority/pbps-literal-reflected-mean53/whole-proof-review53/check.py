import os, sys, json, hashlib, subprocess, datetime, pathlib, re
ROOT=pathlib.Path('E:/Samplinglib')
OUT=ROOT/'runs/20261007-companion-priority/pbps-literal-reflected-mean53/whole-proof-review53'
BASE=OUT.parent
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(name,obj): (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(path):
 p=pathlib.Path(path); p=p if p.is_absolute() else ROOT/p
 b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest(),lf_sha256=hashlib.sha256(b.replace(b'\r\n',b'\n')).hexdigest())
def strict(name):
 f=json.loads((BASE/'math-freeze.json').read_text(encoding='utf-8')); checks=[]
 for expected in f['inputs']:
  actual=pin(expected['path']);ok=all(actual[k]==expected[k] for k in ('bytes','raw_sha256','lf_sha256'))
  checks.append(dict(expected=expected,actual=actual,ok=ok))
 result=dict(utc=utc(),count=len(checks),all_pass=all(c['ok'] for c in checks),checks=checks)
 dump(name,result);assert result['count']==492 and result['all_pass'];return result
if __name__=='__main__':
 dump('lease.json',dict(status='OPEN',owner='whole_math52',review='whole-proof-review53',opened_utc=utc(),pid=os.getpid(),compiler_required=True,allowed_write_root=OUT.as_posix()))
 strict('inputs.pre.json')
 env=dict(os.environ);inherited=env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1'
 cmd=['lake','build','Tests.ProximalBPSReflectedMeanRegularity']
 def query(args):
  p=subprocess.run(args,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8');assert p.returncode==0,(args,p.stdout,p.stderr);return p.stdout.strip()
 manifest=json.loads((ROOT/'lake-manifest.json').read_text());mathlib=next(p for p in manifest['packages'] if p['name']=='mathlib')
 toolchain=(ROOT/'lean-toolchain').read_text().strip();lean=query(['lean','--version']);head=query(['git','rev-parse','HEAD']);mathhead=query(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'])
 assert toolchain=='leanprover/lean4:v4.33.0' and '4.33.0' in lean and mathhead==mathlib['rev']
 dump('environment.json',dict(utc=utc(),python=sys.executable,python_version=sys.version,inherited_ELAN_TOOLCHAIN=inherited,ELAN_TOOLCHAIN_unset=True,LEAN_NUM_THREADS=2,PYTHONUTF8=1,lean=lean,toolchain=toolchain,mathlib=mathlib,mathlib_checkout=mathhead,git_head=head,command=cmd))
 opening=utc()
 with (OUT/'focused.log').open('wb') as log:
  p=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
  dump('compiler.lease.json',dict(status='OPEN',owner='whole_math52',compiler_pid=p.pid,opened_utc=opening,command=cmd,cwd=ROOT.as_posix()))
  print(json.dumps(dict(compiler_pid=p.pid,status='RUNNING')),flush=True)
  code=p.wait()
 status=dict(command=cmd,compiler_pid=p.pid,exit_code=code,opened_utc=opening,closed_utc=utc(),log=pin(OUT/'focused.log'),production=pin('AutoSamplingTheory/ExampleCases/ProximalBPS/LiteralReflectedMean.lean'),test=pin('Tests/ProximalBPSReflectedMeanRegularity.lean'))
 dump('focused.status.json',status)
 dump('compiler.lease.json',dict(status='CLOSED',owner='whole_math52',compiler_pid=p.pid,exit_code=code,opened_utc=opening,closed_utc=utc(),command=cmd,log=status['log']))
 strict('inputs.post-build.json')
 print(json.dumps(status),flush=True)
 assert code==0
