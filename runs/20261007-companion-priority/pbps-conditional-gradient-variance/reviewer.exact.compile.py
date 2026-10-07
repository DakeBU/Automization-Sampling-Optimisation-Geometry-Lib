from pathlib import Path
import json,subprocess,datetime,hashlib
r=Path('E:/Samplinglib');p=r/'runs/20261007-companion-priority/pbps-conditional-gradient-variance';f=p/'reviewer.exact.lease.json'
lease=json.loads(f.read_text());assert lease['status']=='OPEN' and lease['compiler']=='NOT_STARTED_CLOSED'
assert json.loads((p/'reviewer.exact.precompiler.json').read_text())['status']=='PASS_COMPILER_INPUTS_BOUND'
started=datetime.datetime.now(datetime.timezone.utc).isoformat();lease.update(compiler='OPEN',compiler_started=True,compiler_opened_utc=started,compiler_command=['lake','build','Tests.ProximalBPSConditionalGradientVariance']);f.write_text(json.dumps(lease,indent=2)+'\n',encoding='utf-8');(p/'reviewer.exact.compiler.open.raw.snapshot.json').write_bytes(f.read_bytes())
cmd=[r'C:/Users/admin/.elan/bin/lake.EXE','build','Tests.ProximalBPSConditionalGradientVariance']
with (p/'reviewer.exact.focused.log').open('wb') as log:
 proc=subprocess.Popen(cmd,cwd=r,stdout=log,stderr=subprocess.STDOUT);pid=proc.pid;exitcode=proc.wait()
finished=datetime.datetime.now(datetime.timezone.utc).isoformat();raw=(p/'reviewer.exact.focused.log').read_bytes();status={'checked_commit':'53f65a50263c13823aef5da7d9a3279de3514243','command':cmd,'process_id':pid,'foreground_process':True,'started_utc':started,'finished_utc':finished,'exit_code':exitcode,'log_raw_sha256':hashlib.sha256(raw).hexdigest(),'log_LF_sha256':hashlib.sha256(raw.replace(b'\r\n',b'\n').replace(b'\r',b'\n')).hexdigest(),'compiler_runs_by_this_verifier':1}
(p/'reviewer.exact.focused.status.json').write_text(json.dumps(status,indent=2)+'\n',encoding='utf-8')
lease.update(compiler='CLOSED',compiler_closed_utc=finished,compiler_exit_code=exitcode,compiler_pid=pid);f.write_text(json.dumps(lease,indent=2)+'\n',encoding='utf-8');(p/'reviewer.exact.compiler.closed.raw.snapshot.json').write_bytes(f.read_bytes())
print(json.dumps(status));print(raw.decode('utf-8',errors='replace')[-2200:]);assert exitcode==0
