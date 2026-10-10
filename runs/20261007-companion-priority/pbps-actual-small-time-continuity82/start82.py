from pathlib import Path
import hashlib,json,subprocess,datetime,sys
r=Path(__file__).parent
def run(args):return subprocess.run(args,capture_output=True,check=True).stdout
def write(name,data):p=r/name;assert not p.exists();p.write_bytes(data)
def save(name,x):write(name,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
sha=lambda b:hashlib.sha256(b).hexdigest()
branch=run(['git','branch','--show-current']).decode().strip();head=run(['git','rev-parse','HEAD']).decode().strip()
status=run(['git','status','--porcelain=v1','--untracked-files=all']);write('pre-fetch82.status.snapshot',status)
write('pre-fetch82.branch.snapshot',(branch+'\n').encode());write('pre-fetch82.head.snapshot',(head+'\n').encode())
capsule=run([sys.executable,'-X','utf8','tools/astis_advance.py','capsule']);write('pre-fetch82.capsule.snapshot.json',capsule)
tracked=run(['git','ls-files','-m','-z']).decode().split('\0');before={p:sha(Path(p).read_bytes()) for p in tracked if p and Path(p).is_file()}
cells={p.as_posix():sha(p.read_bytes()) for p in Path('research-wiki/frontier-cells').glob('*.json')}
save('pre-fetch82.workspace-RAW.json',dict(tracked_modified=before,frontier_cells=cells,previous_turn='PROGRESS: SAU81 independently VERIFIED and integrated normal-pushed4502b48d; Goal remains active'))
p=subprocess.run(['git','fetch','origin'],capture_output=True);write('fetch82.stdout.log',p.stdout);write('fetch82.stderr.log',p.stderr)
assert p.returncode==0
assert run(['git','rev-parse','HEAD']).decode().strip()==head
assert all(sha(Path(p).read_bytes())==h for p,h in before.items())
assert all(sha(Path(p).read_bytes())==h for p,h in cells.items())
main=run(['git','rev-parse','origin/main']).decode().strip()
save('safe-fetch82.json',dict(branch=branch,HEAD_unchanged=head,origin_main=main,tracked_workspace_RAW_unchanged=True,frontier_cells_RAW_unchanged=True,work_branch_updated=False,reason='Preserve existing local work and reviewed serial integration branch; fetch updates remote refs only',utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
data=run(['gh','pr','view','315','--repo','DakeBU/Automization-Sampling-Optimisation-Geometry-Lib','--json','url,state,headRefOid,statusCheckRollup']);write('remote81.observed.json',data)
execution=json.loads(Path('website/content/samplewiki_companion_frontiers.json').read_bytes())['execution'];save('execution82.snapshot.json',execution)
c=json.loads(capsule)
print(json.dumps(dict(branch=branch,head=head,origin_main=main,tracked_modified_count=len(before),frontier_count=len(cells),sole_stabilization_lane=c['single_stabilization_lane'],remote81=json.loads(data),execution=execution),ensure_ascii=False,indent=2))
