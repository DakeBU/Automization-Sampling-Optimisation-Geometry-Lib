import os,sys,json,subprocess
from pathlib import Path
import review69 as R
O=R.O;pin=R.pin;save=R.save;get=R.get
assert not(O/'lease.final.json').exists();(O/'close.executed-helper.RAW.py').write_bytes(Path(__file__).read_bytes())
with (O/'close.validator.stdout.log').open('wb') as out,(O/'close.validator.stderr.log').open('wb') as err:
 start=R.now();p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(O/'readonly69.py'),'preclose'],cwd=R.ROOT,stdout=out,stderr=err);code=p.wait()
receipt=dict(actual_close_writer_PID=os.getpid(),actual_readonly_probe_PID=p.pid,started_utc=start,finished_utc=R.now(),exit_code=code,terminal_closed=True,stdout=pin(O/'close.validator.stdout.log'),stderr=pin(O/'close.validator.stderr.log'));save('close.validator.terminal.json',receipt);assert code==0
rows=[pin(p) for p in sorted(O.rglob('*')) if p.is_file() and p.name!='lease.final.json'];lease=dict(status='CLOSED_LAST',actor=R.ACTOR,actual_last_writer_PID=os.getpid(),utc=R.now(),checked_base_commit=R.BASE,owned_scope=O.as_posix(),owned_file_count_including_self=len(rows)+1,all_owned_outputs_except_only_self=rows,whole_logical_run_sha256=get('run.json')['run_sha256'],named_complete_RAW_review=pin(O/'named-mathematical-review.payload.json'),last_owned_write='lease.final.json',actual_foreground_close_probe=receipt,close_writer_exit='Externally observed after final write; no invented future exit.',own_lease_RAW='Independently measured by read-only postclose, not circular self digest.',no_more_owned_writes=True,canonical_Git_ledger_writes=False,VERIFIED=False)
save('lease.final.json',lease);print(json.dumps(dict(status='CLOSED_LAST',actual_last_writer_PID=os.getpid(),owned_file_count=len(rows)+1,whole_logical_run_sha256=lease['whole_logical_run_sha256'],complete_named_RAW=lease['named_complete_RAW_review'],lease_RAW=pin(O/'lease.final.json'))))
