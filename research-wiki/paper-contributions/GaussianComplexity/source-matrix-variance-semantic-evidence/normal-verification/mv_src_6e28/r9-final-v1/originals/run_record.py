from pathlib import Path
import subprocess,sys,os,json,hashlib,traceback
from datetime import datetime,timezone
R=Path('/Users/zhouhuanjian/ASTIS-GC');B=Path(__file__).resolve().parent
label=sys.argv[1];argv=sys.argv[2:];d=B/'commands'/label;d.mkdir(exist_ok=False)
env=dict(os.environ);env['GIT_OPTIONAL_LOCKS']='0';env['PYTHONDONTWRITEBYTECODE']='1'
rec={'label':label,'argv':argv,'cwd':str(R),'started_utc':datetime.now(timezone.utc).isoformat(),'effective_environment':env}
try:
 with (d/'stdout').open('wb') as out,(d/'stderr').open('wb') as err:
  p=subprocess.run(argv,cwd=R,env=env,stdout=out,stderr=err)
 rec['exit']=p.returncode
except BaseException:
 rec['exception']=traceback.format_exc();rec['exit']=255
finally:
 rec['finished_utc']=datetime.now(timezone.utc).isoformat()
 for n in ['stdout','stderr']:
  f=d/n
  if f.exists():rec[n]={'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
 (d/'receipt.json').write_text(json.dumps(rec,indent=2)+'\n')
 print(json.dumps({k:rec[k] for k in ['label','argv','exit','stdout','stderr'] if k in rec}))
sys.exit(rec['exit'])
