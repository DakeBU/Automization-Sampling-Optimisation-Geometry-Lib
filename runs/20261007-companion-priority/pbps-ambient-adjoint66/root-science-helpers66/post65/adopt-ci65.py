from pathlib import Path
import hashlib,json,os
r=Path('runs/20261007-companion-priority/pbps-polar65')
d=r/'integration65/remote-ci65-terminal-v4'
receipt=json.loads((d/'receipt.json').read_bytes())
rows=json.loads((d/'stdout.log').read_bytes())
head='31ce36e7ca01b203696918672c33d29a337550c3'
assert receipt['exit_code']==0 and receipt['terminal_closed'] and receipt['actual_foreground_pid']==47904
expected={37897529640:'ASTIS formalization gate',37897529689:'Samplinglib site',37897529600:'Contributor contract',37897511973:'Contributor contract'}
assert {x['databaseId'] for x in rows}==set(expected)
for x in rows:
    assert x['headSha']==head and x['status']=='completed' and x['conclusion']=='success' and x['workflowName']==expected[x['databaseId']]
assert json.loads((r/'root.repository-exposition65.adoption.json').read_bytes())['checked_commit']==head
out=r/'remote-ci65.accepted.json'
assert not out.exists()
out.write_text(json.dumps(dict(status='EXACT_INT65_REMOTE_ALL_SUCCESS',checked_commit=head,actual_root_adopter_pid=os.getpid(),authoritative_gh_run_snapshot=(d/'stdout.log').as_posix(),snapshot_RAW_sha256=hashlib.sha256((d/'stdout.log').read_bytes()).hexdigest(),actual_foreground_receipt=(d/'receipt.json').as_posix(),actual_gh_pid=47904,workflows=rows,independent_repository_reader='Accepted bounded with explicit reader debt; full Exposition Seal and postmerge purification unclaimed.',merged_main_live_full_Exposition_PURIFIED_paper_Goal=False),indent=2)+'\n',encoding='utf-8',newline='\n')
body=r/'integration65/pr315-body65-repository-admitted.md'
text=body.read_text(encoding='utf-8')
old='Site and contributor workflows have succeeded; formalization CI awaits an authoritative terminal result.'
assert text.count(old)==1
target=r/'integration65/pr315-body65-remote-accepted.md'
assert not target.exists()
target.write_text(text.replace(old,'Formalization, site and both contributor workflows are authoritatively terminal SUCCESS on this exact integration commit.'),encoding='utf-8',newline='\n')
print('PASS exact INT65 remote: four terminal successes adopted; concrete PR body updated. No merge/live/Goal claim.')
