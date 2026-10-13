from pathlib import Path
import json,subprocess,hashlib,datetime,os
r=Path('E:/Samplinglib');q=r/'runs/20261007-companion-priority/pbps-gaussian-marginal-gradient';o=q/'exact-verification51';H=lambda b:hashlib.sha256(b).hexdigest();now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=r).decode().strip()=='19f7e6bed7975fac9b7e1ea0b0b95d0c084083f6'
for p,h in [('AutoSamplingTheory/TechnicalLemmas/FunctionalInequalities/GaussianMarginalGradient.lean','a985303fc08242eb186e42e810b8fae9c9b7183c1e0f52b944f6836c9f55b2fb'),('Tests/ProximalBPSGaussianMarginalGradient.lean','c5d65500d5a645bf9d9f4ad4381c8a34b322fa227196b42eaf19110ed23f09e1')]:
 b=(r/p).read_bytes();assert H(b)==h;g=subprocess.check_output(['git','show','HEAD:'+p],cwd=r);assert g in (b,b.replace(b'\r\n',b'\n'))
lp=o/'reviewer.exact.lease.json';d=json.loads(lp.read_text('utf-8'));d['compiler']='OPEN';d['compiler_opened_utc']=now();put(lp,d)
env=os.environ.copy();env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';cmd=['lake','build','Tests.ProximalBPSGaussianMarginalGradient'];start=now()
with (o/'focused.log').open('wb') as f:
 p=subprocess.Popen(cmd,cwd=r,env=env,stdout=f,stderr=subprocess.STDOUT);d['compiler_pid']=p.pid;put(lp,d);rc=p.wait()
b=(o/'focused.log').read_bytes();s={'command':cmd,'PID':p.pid,'started_utc':start,'finished_utc':now(),'exit_code':rc,'log_raw_sha256':H(b),'log_lf_sha256':H(b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')),'log_bytes':len(b),'compiler_environment':{'ELAN_TOOLCHAIN':'unset','LEAN_NUM_THREADS':'2'}};put(o/'focused.status.json',s);d['compiler']='CLOSED';d['compiler_closed_utc']=now();d['compiler_exit_code']=rc;put(lp,d);print(json.dumps(s));print(b.decode('utf-8')[-3500:]);assert rc==0
