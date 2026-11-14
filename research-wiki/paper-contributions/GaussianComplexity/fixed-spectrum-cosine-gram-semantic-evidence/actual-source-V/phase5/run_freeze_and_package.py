#!/opt/anaconda3/bin/python
import datetime,hashlib,json,pathlib,subprocess,sys
BASE=pathlib.Path(__file__).resolve().parent;ROLE=BASE.parent
argv=['/opt/anaconda3/bin/python',str(BASE/'freeze_phase5.py')]
started=datetime.datetime.now(datetime.timezone.utc).isoformat()
proc=subprocess.run(argv,cwd='/Users/zhouhuanjian/ASTIS-GC',capture_output=True)
out=ROLE/'phase5_freeze_execution.stdout';err=ROLE/'phase5_freeze_execution.stderr'
out.write_bytes(proc.stdout);err.write_bytes(proc.stderr)
record={'argv':argv,'cwd':'/Users/zhouhuanjian/ASTIS-GC','started_utc':started,'returncode':proc.returncode,
        'stdout_file':out.name,'stderr_file':err.name,'stdout_bytes':len(proc.stdout),'stderr_bytes':len(proc.stderr),
        'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(proc.stderr).hexdigest()}
if proc.returncode==0:
    record['observed_freeze_result']=json.loads(proc.stdout)
    record['receipt_sha256_observed']=hashlib.sha256((BASE/'freeze_receipt.json').read_bytes()).hexdigest()
    assert record['receipt_sha256_observed']==record['observed_freeze_result']['receipt_sha256']
path=ROLE/'phase5_freeze_execution.json';path.write_text(json.dumps(record,indent=2)+'\n')
for p in [out,err,path]:p.chmod(0o444)
print(json.dumps(record,indent=2));sys.stdout.write(proc.stdout.decode(errors='replace'));sys.stderr.write(proc.stderr.decode(errors='replace'))
if proc.returncode:raise SystemExit(proc.returncode)
package_argv=['/opt/anaconda3/bin/python',str(BASE/'package_portable_phase5.py')]
pack=subprocess.run(package_argv,cwd='/Users/zhouhuanjian/ASTIS-GC',capture_output=True)
po=ROLE/'phase5_package_execution.stdout';pe=ROLE/'phase5_package_execution.stderr'
po.write_bytes(pack.stdout);pe.write_bytes(pack.stderr)
pr={'argv':package_argv,'returncode':pack.returncode,'stdout_file':po.name,'stderr_file':pe.name,
    'stdout_sha256':hashlib.sha256(pack.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(pack.stderr).hexdigest()}
pj=ROLE/'phase5_package_execution.json';pj.write_text(json.dumps(pr,indent=2)+'\n')
for p in [po,pe,pj]:p.chmod(0o444)
print('PACKAGE_EXECUTION',json.dumps(pr));sys.stdout.write(pack.stdout.decode(errors='replace'));sys.stderr.write(pack.stderr.decode(errors='replace'))
raise SystemExit(pack.returncode)
