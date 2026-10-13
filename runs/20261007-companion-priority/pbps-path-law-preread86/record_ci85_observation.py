from pathlib import Path
import json,subprocess,datetime,hashlib
R=Path('E:/Samplinglib');D=R/'runs/20261007-companion-priority/pbps-path-law-preread86'
cmd=['gh','run','view','38074998616','--json','headSha,status,conclusion,jobs']
p=subprocess.run(cmd,cwd=R,capture_output=True);assert p.returncode==0,p.stderr
x=json.loads(p.stdout);assert x['headSha']=='8280ef700ea01a1e94c9e7a3cba05a26b4156b56'
for name,data in [('remote-ci85.native.json',p.stdout),('remote-ci85.stderr.txt',p.stderr)]:
 f=D/name;assert not f.exists();f.write_bytes(data)
z={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'exit_code':p.returncode,'head':x['headSha'],'status':x['status'],'conclusion':x['conclusion'],'native_raw_sha256':hashlib.sha256(p.stdout).hexdigest(),'local_aggregate_pass_separate':True,'merged':False,'purified':False,'live':False,'Goal_complete':False}
f=D/'remote-ci85.observation.json';assert not f.exists();f.write_text(json.dumps(z,indent=2)+'\n',encoding='utf-8')
print(json.dumps(z))
