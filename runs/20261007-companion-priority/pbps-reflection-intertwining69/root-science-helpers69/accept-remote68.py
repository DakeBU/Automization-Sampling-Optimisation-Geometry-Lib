from pathlib import Path
from collections import Counter
import json,hashlib,datetime,sys
r=Path('runs/20261007-companion-priority/pbps-sharp-energy68');d=r/'integration68'/sys.argv[1]
receipt=json.loads((d/'receipt.json').read_bytes());assert receipt['terminal_closed'] and receipt['exit_code']==0
b=(d/'stdout.log').read_bytes();rows=json.loads(b);head=receipt['checked_science_parent']
assert len({x['databaseId'] for x in rows})==len(rows)
assert all(x['headSha']==head for x in rows)
expected=Counter({'Contributor contract':2,'Samplinglib site':1,'ASTIS formalization gate':1})
if Counter(x['workflowName'] for x in rows)!=expected or not all(x['status']=='completed' and x['conclusion']=='success' for x in rows):
 print('PENDING: no remote acceptance written.');sys.exit(0)
dest=r/'remote-ci68.accepted.json';assert not dest.exists()
x=dict(status='EXACT_INT68_REMOTE_ALL_SUCCESS',checked_INT_commit=head,observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_foreground_PID=receipt['actual_foreground_pid'],exit_code=0,authoritative_snapshot=(d/'receipt.json').as_posix(),complete_RAW_stdout_sha256=hashlib.sha256(b).hexdigest(),runs=rows,current_local_generated_graph_admission_separate=True,historical_INT66_freshness_withholding_unchanged=True,full_Exposition=False,PURIFIED=False,main_live=False,whole_paper_complete=False,Goal_complete=False)
dest.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
source=r/'integration68/pr315-body68.md';s=source.read_text(encoding='utf-8');old="This integration commit's remote CI is pending; main/live delivery";assert s.count(old)==1
s=s.replace(old,'All four authoritative GitHub Actions runs for this exact integration commit completed successfully (formalization, site and both contributor checks); main/live delivery')
s=s.replace('root.repository68.adoption.json.','root.repository68.adoption.json and remote-ci68.accepted.json.')
p=r/'integration68/pr315-body68-remote-accepted.md';assert not p.exists();p.write_text(s,encoding='utf-8',newline='\n')
print('PASS exact INT68 all four authoritative remote runs SUCCESS; concrete updated PR body prepared; main/live/full paper remain open.')
