"""Nonforce delivery of independently verified100 through existing PR315."""
from pathlib import Path
import datetime,json,subprocess
r=Path(__file__).parent;out=r/'integration100'
def run(argv):
 q=subprocess.run(argv,capture_output=True);assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace');return q.stdout
head=run(['git','rev-parse','HEAD']).decode().strip()
assert not run(['git','diff','--cached','--name-only']).strip()
note=json.loads((r/'integration.notes.json').read_bytes());assert note['state_distinctions']['local_aggregate_and_generated_site_gates']
run(['git','merge-base','--is-ancestor','origin/main',head])
branch='refs/heads/codex/sphmc-standardized-rgo'
before=run(['git','ls-remote','origin',branch]).decode().split()[0]
assert before=='af9c34eb875fd0261f9c40020d7ee22ecdffebbf',before
run(['git','merge-base','--is-ancestor',before,head])
q=subprocess.run(['git','push','origin','HEAD:'+branch],capture_output=True)
(out/'push100.stdout.log').write_bytes(q.stdout);(out/'push100.stderr.log').write_bytes(q.stderr)
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')
remote=run(['git','ls-remote','origin',branch]).decode().split()[0]
pr=json.loads(run(['gh','pr','view','315','--json','headRefName,headRefOid,state,url']))
assert head==remote==pr['headRefOid'] and pr['state']=='OPEN' and pr['headRefName']=='codex/sphmc-standardized-rgo'
run(['gh','pr','edit','315','--title','Construct actual PBPS paths, Gibbs balance and finite path reversal','--body-file',str(out/'pr-body100.md')])
d=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),local_head=head,remote_head=remote,previous_remote_head=before,pr=pr,science_commit=note['science_commit'],independently_verified=True,stabilized=False,main_merged=False,purified=False,actual_browser_visual_acceptance=False,full_papers_completed=0)
p=out/'postpush-binding100.json';assert not p.exists();p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(d))
