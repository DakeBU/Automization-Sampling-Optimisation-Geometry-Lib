from pathlib import Path
import datetime,gzip,hashlib,json,subprocess,sys,time
out=Path(__file__).resolve().parent
root=Path('/Users/zhouhuanjian/ASTIS-GC')
commands=[
 ('focused-build',['lake','build','AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumAffine','Tests.GaussianComplexityFixedSpectrumAffine']),
 ('direct-production',['lake','env','lean','AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumAffine.lean']),
 ('direct-consumer',['lake','env','lean','Tests/GaussianComplexityFixedSpectrumAffine.lean']),
 ('anonymous-application-critical-axioms',['lake','env','lean',str((out/'anonymous-application-and-critical-axioms.lean').relative_to(root))])]
records=[]
for label,cmd in commands:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
 p=subprocess.run(cmd,cwd=root,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log=p.stdout; gz=gzip.compress(log,mtime=0);(out/(label+'.log.gz')).write_bytes(gz)
 r={'label':label,'command':cmd,'cwd':str(root),'started_utc':start,'elapsed_seconds':time.monotonic()-t,'exit_code':p.returncode,'raw_log_bytes':len(log),'raw_log_sha256':hashlib.sha256(log).hexdigest(),'gzip_log_sha256':hashlib.sha256(gz).hexdigest(),'terminal_bytes_hex':log[-32:].hex(),'raw_log_preserved_lossless':True}
 (out/(label+'.receipt.json')).write_text(json.dumps(r,indent=2)+'\n');records.append(r)
 print(json.dumps(r),flush=True)
 print(log.decode(errors='replace')[-6000:],flush=True)
 if p.returncode: break
(out/'fresh-lean-checks.json').write_text(json.dumps(records,indent=2)+'\n')
sys.exit(0 if len(records)==len(commands) and all(r['exit_code']==0 for r in records) else 1)
