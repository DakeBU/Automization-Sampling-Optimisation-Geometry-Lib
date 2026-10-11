"""Merge the inspected, disjoint current-main presentation change without touching local RAWs."""
from pathlib import Path
import datetime, hashlib, json, subprocess
r=Path(__file__).parent
out=r/'integration98/current-main'
out.mkdir(exist_ok=False)
def git(*a):return subprocess.check_output(['git',*a]).decode().strip()
old='708d260b6d51369e4f2c1551d33af40d74c1e547'
new='f4f8d3a8ef0d4918cb30c333540a303b501ffc63'
assert git('rev-parse','origin/main')==new
assert not git('diff','--cached','--name-only')
paths=git('diff','--name-only',old,new).splitlines()
assert set(paths)=={'README.md','docs/math-2-0-positioning.md','website/scripts/math_2_0.py'}
assert not git('diff','--name-only','--',*paths)
saved=json.loads((r/'exact-commit-verification98/closed-RAW-manifest98.json').read_bytes())['preserved_collaborator_inputs']
def preserved():
 for d in saved:assert hashlib.sha256(Path(d['path']).read_bytes()).hexdigest()==d['raw_sha256'],d['path']
preserved()
before=git('rev-parse','HEAD')
q=subprocess.run(['git','merge','--no-edit','origin/main'],capture_output=True)
(out/'merge.stdout.log').write_bytes(q.stdout)
(out/'merge.stderr.log').write_bytes(q.stderr)
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')
preserved()
after=git('rev-parse','HEAD')
assert git('diff','--name-only',before,after).splitlines()==paths
d=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),integration_commit=before,
 merge_commit=after,upstream_main=new,changed_paths=paths,preserved_collaborator_RAWs=len(saved),
 science_commit='530a58f7c036a67787956b20d2d390890ec2fec7',science_unchanged=True,
 publication_and_site_revalidation='pending',Goal_complete=False)
(out/'merge-receipt98.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(d))
