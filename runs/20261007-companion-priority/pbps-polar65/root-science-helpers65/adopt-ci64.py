from pathlib import Path
import hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-centered-root64');d=r/'integration64/remote-int64-snapshot-v4'
receipt=json.loads((d/'receipt.json').read_bytes());rows=json.loads((d/'stdout.log').read_bytes());head='0aef19ca2711159eeaec86d42c9be142a94fa402'
assert receipt['exit_code']==0 and receipt['terminal_closed'] and receipt['actual_foreground_pid']==35364
expected={37889381650:'ASTIS formalization gate',37889381654:'Samplinglib site',37889381651:'Contributor contract',37889368928:'Contributor contract'}
assert {x['databaseId'] for x in rows}==set(expected)
for x in rows:assert x['headSha']==head and x['status']=='completed' and x['conclusion']=='success' and x['name']==expected[x['databaseId']]
assert json.loads((r/'root.repository-exposition64.adoption.json').read_bytes())['checked_commit']==head
out=r/'remote-ci64.accepted.json';assert not out.exists()
out.write_text(json.dumps(dict(status='EXACT_INT64_REMOTE_ALL_SUCCESS',checked_commit=head,actual_root_adopter_pid=os.getpid(),authoritative_gh_run_snapshot=(d/'stdout.log').as_posix(),snapshot_RAW_sha256=hashlib.sha256((d/'stdout.log').read_bytes()).hexdigest(),actual_foreground_receipt=(d/'receipt.json').as_posix(),actual_gh_pid=35364,workflows=rows,independent_repository_reader='Accepted bounded with reader and stale metadata debt; separately reviewed two-field overlay not yet applied.',merged_main_live_full_Exposition_PURIFIED_paper_Goal=False),indent=2)+'\n',encoding='utf-8',newline='\n')
print('PASS exact INT64 remote: formal/site/contributor + push contributor all terminal SUCCESS; no merge/live/Goal claim.')
