import sys,os,json,subprocess
from pathlib import Path
import review68 as R
O=R.O;pin=R.pin;sha=R.sha;save=R.save;get=R.get;now=R.now
assert not (O/'lease.final.json').exists()
helper=O/'close68.executed-helper.RAW.py';helper.write_bytes(Path(__file__).read_bytes())
cmd=[sys.executable,'-B','-X','utf8',str(O/'readonly-validator68.py'),'preclose']
with (O/'close.validator.stdout.log').open('wb') as out,(O/'close.validator.stderr.log').open('wb') as err:
 start=now();p=subprocess.Popen(cmd,cwd=R.ROOT,stdout=out,stderr=err);code=p.wait()
receipt=dict(stage='close-foreground-readonly-probe',actual_close_writer_PID=os.getpid(),actual_foreground_probe_PID=p.pid,started_utc=start,finished_utc=now(),exit_code=code,terminal_closed=True,stdout=pin(O/'close.validator.stdout.log'),stderr=pin(O/'close.validator.stderr.log'),executed_close_helper=pin(helper))
save('close.validator.terminal.json',receipt);assert code==0
rows=[pin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name!='lease.final.json']
lease=dict(schema_version=1,status='CLOSED_LAST',actor=R.ACTOR,actual_last_writer_PID=os.getpid(),utc=now(),owned_scope=O.as_posix(),owned_file_count_including_self=len(rows)+1,all_owned_outputs_except_only_self=rows,whole_logical_run_sha256=get('run.json')['run_sha256'],named_complete_RAW_payload=pin(O/'named-mathematical-review.payload.json'),last_owned_write='lease.final.json',self_RAW_digest='Externally measured by read-only postclose validator; no circular self digest.',actual_close_foreground_probe=receipt,close_writer_terminal_exit='Must be observed by caller and then independent read-only postclose; this file does not fabricate its own future process exit.',no_owned_writes_after_this_lease=True,canonical_Git_ledger_writes=False,VERIFIED=False)
save('lease.final.json',lease)
print(json.dumps(dict(status='CLOSED_LAST',actual_last_writer_PID=os.getpid(),owned_file_count=len(rows)+1,whole_logical_run_sha256=lease['whole_logical_run_sha256'],named_complete_RAW_payload=lease['named_complete_RAW_payload'],lease_RAW=pin(O/'lease.final.json'))))
