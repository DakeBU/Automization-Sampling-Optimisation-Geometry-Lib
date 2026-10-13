from pathlib import Path
import subprocess,json,hashlib
r=Path(__file__).parent
load=lambda p:json.loads(Path(p).read_bytes())
def git(*a):return subprocess.check_output(['git','-c','core.autocrlf=false','-c','core.fscache=false',*a])
assert git('rev-parse','HEAD').decode().strip()=='8b25d43e477db682be0227f14ce8140859567fc1'
assert git('rev-parse','MERGE_HEAD').decode().strip()=='26dce3a7442577b8bdfbfb20e8b77f681c052528'
assert load(r/'independent-merge-review106/decision106.native.json')['status']=='ACCEPT_BOUNDED_MERGE_RESOLUTION'
run=r.parent.parent/'pbps-actual-bounded-gibbs-duality106'
assert load(run/'checks106/upstream-merge-tests/receipt.json')['exit_code']==0
assert not git('diff','--name-only','--diff-filter=U').strip()
for row in load(r/'premerge106.json')['dirty_tracked_RAW']:assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['raw_sha256'],row['path']
subprocess.run(['git','diff','--cached','--check'],check=True)
git('commit','-q','-m','Merge reviewed sphere Rayleigh results into PBPS integration')
commit=git('rev-parse','HEAD').decode().strip()
(r/'merge-commit106.json').write_text(json.dumps(dict(commit=commit,upstream='26dce3a7442577b8bdfbfb20e8b77f681c052528',independent_review=True,Tests_pass=True),indent=2)+'\n',encoding='utf8',newline='\n')
print(commit)
