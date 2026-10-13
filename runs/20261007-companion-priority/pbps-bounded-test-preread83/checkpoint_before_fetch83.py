from pathlib import Path
import datetime,hashlib,json,subprocess,sys
r=Path(__file__).parent
def git(*a):return subprocess.check_output(['git',*a],text=True).strip()
modified=git('diff','--name-only').splitlines()
snapshot=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),previous_goal_turn='progress: independently verified actual82, full local gates, commit481d8f1b and normal push/PR315 head verified',branch=git('branch','--show-current'),commit=git('rev-parse','HEAD'),status=git('status','--porcelain=v1'),tracked_modified={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in modified},frontier_cells={p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path('research-wiki/frontier-cells').glob('*.json'))},existing_Goal_preserved=True)
p=r/'pre-fetch83.workspace-RAW.json';assert not p.exists();p.write_text(json.dumps(snapshot,indent=2)+'\n',encoding='utf8',newline='\n')
q=subprocess.run([sys.executable,'-X','utf8','tools/astis_advance.py','capsule'],capture_output=True);assert q.returncode==0
(r/'current-capsule83.json').write_bytes(q.stdout)
x=json.loads(q.stdout);print('Recorded branch/commit/workspace/frontier before fetch;',len(snapshot['tracked_modified']),'modified files; sole lane',x['single_stabilization_lane'])
