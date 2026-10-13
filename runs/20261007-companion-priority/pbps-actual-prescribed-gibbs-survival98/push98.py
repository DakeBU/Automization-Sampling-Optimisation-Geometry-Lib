"""Nonforce delivery of reviewed98 through the existing PR315 branch."""
from pathlib import Path
import datetime,hashlib,json,subprocess
r=Path(__file__).parent;out=r/'integration98'
def run(argv):
 q=subprocess.run(argv,capture_output=True);assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace');return q.stdout
head=run(['git','rev-parse','HEAD']).decode().strip()
assert not run(['git','diff','--cached','--name-only']).strip()
assert (out/'current-main/revalidation98.json').exists()
assert run(['git','merge-base','170e1bad1f0887512b79c4b5711ce316ade5f511',head]).decode().strip()=='170e1bad1f0887512b79c4b5711ce316ade5f511'
branch='refs/heads/codex/sphmc-standardized-rgo'
before=run(['git','ls-remote','origin',branch]).decode().split()[0]
assert before=='49fdfd309151b30f6371767dd74d698d440a8974',before
q=subprocess.run(['git','push','origin','HEAD:'+branch],capture_output=True)
(out/'push98.stdout.log').write_bytes(q.stdout);(out/'push98.stderr.log').write_bytes(q.stderr)
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')
remote=run(['git','ls-remote','origin',branch]).decode().split()[0]
pr=json.loads(run(['gh','pr','view','315','--json','headRefName,headRefOid,state,url']))
assert head==remote==pr['headRefOid'] and pr['state']=='OPEN'
assert pr['headRefName']=='codex/sphmc-standardized-rgo'
run(['gh','pr','edit','315','--title','Construct actual PBPS paths and finite Gibbs-survival balance','--body-file',str(out/'current-main/pr-body98.md')])
d=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),local_head=head,remote_head=remote,previous_remote_head=before,pr=pr,science_commit='530a58f7c036a67787956b20d2d390890ec2fec7',independently_verified=True,stabilized=False,main_merged=False,purified=False,actual_browser_visual_acceptance=False,full_papers_completed=0)
p=out/'postpush-binding98.json';assert not p.exists();p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(d))
