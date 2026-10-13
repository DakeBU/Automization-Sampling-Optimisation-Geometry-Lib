from pathlib import Path
import subprocess,json,hashlib,datetime
r=Path(__file__).parent;out=r/'postpush87';out.mkdir(exist_ok=False)
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert commit=='24210c17b36c608fec3c259f811430cc9fc148cf'
q=subprocess.run(['git','diff','--check'],capture_output=True)
(out/'diff.stdout.log').write_bytes(q.stdout);(out/'diff.stderr.log').write_bytes(q.stderr);assert q.returncode==0
saved=load(r/'pre-fetch88.workspace-RAW.json')['tracked_modified'];assert len(saved)==21
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
q=subprocess.run(['gh','run','list','--commit',commit,'--limit','8','--json','databaseId,name,status,conclusion,headSha,url'],capture_output=True)
(out/'CI.stdout.log').write_bytes(q.stdout);(out/'CI.stderr.log').write_bytes(q.stderr);assert q.returncode==0
rows=json.loads(q.stdout);assert all(x['headSha']==commit for x in rows)
(out/'receipt.json').write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),commit=commit,plain_git_diff_check_exit_code=0,preserved_original_collaborator_files=21,remote_CI=rows,scope='Remote integration87 observations only; queued/in-progress/cancelled are not PASS. No main/merge/PURIFIED/Goal credit.'),indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(dict(commit=commit,plain_git_diff_check='PASS',remote_CI=rows)))
