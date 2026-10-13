from pathlib import Path
import subprocess,json,hashlib,datetime,sys
r=Path(__file__).parent
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(cmd):
 q=subprocess.run(cmd,capture_output=True);assert q.returncode==0,(cmd,q.stderr.decode(errors='replace'));return q.stdout
def save(p,x):assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
save(r/'start87.attempt1.diagnosis.json',dict(status='NEWLINE_WORKTREE_INVENTORY_API_CORRECTED',observed_exception='KeyError: agent-briefs/mathlib_ready_leaf_packet.md',cause='git diff --name-only omits working-tree newline-only status modifications under configured Git conversion; cannot use it as RAW inventory.',correction='Use NUL-delimited tracked git status entries to preserve exact modified paths; original full status log retained.',fetch_started=False,mathematical_progress=False))
tracked=run(['git','status','--porcelain=v1','-z','--untracked-files=no'])
mods={}
for entry in tracked.split(b'\0'):
 if not entry:continue
 assert entry[:2] in [b' M',b'M ',b'AM',b' A'],entry[:2]
 name=entry[3:].decode('utf8');p=Path(name);assert p.is_file();mods[name]=sha(p.read_bytes())
old=load('runs/20261007-companion-priority/pbps-path-law-preread86/pre-fetch86.workspace-RAW.json')['tracked_modified'];assert len(old)==len(mods)==21
assert old==mods
assert not run(['git','diff','--cached','--name-only']).strip()
cells=[dict(path=p.as_posix(),RAW_sha256=sha(p.read_bytes()),id=load(p).get('cell_id',p.stem),status=load(p).get('status')) for p in sorted(Path('research-wiki/frontier-cells').glob('*.json'))]
capcmd=[sys.executable,'-X','utf8','tools/astis_advance.py','capsule','--max-advances','3','--max-discoveries','1','--max-cells','1'];cap=run(capcmd)
(r/'capsule87.stdout.log').write_bytes(cap)
front=load('website/content/samplewiki_companion_frontiers.json')['execution']
snap=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),branch=run(['git','branch','--show-current']).decode().strip(),HEAD=run(['git','rev-parse','HEAD']).decode().strip(),origin_main_before=run(['git','rev-parse','origin/main']).decode().strip(),tracked_modified=mods,original_full_worktree_status_RAW_sha256=sha((r/'pre-fetch87.git-status.exactraw.log').read_bytes()),frontier_cells=cells,execution=front,capsule_command=capcmd,capsule_RAW_sha256=sha(cap),capsule_exit_code=0,single_lane=json.loads(cap)['single_stabilization_lane'],Goal='existing active unbudgeted four-paper Goal; no reset',science86='0bb3cd64ba1235114feaeed99ba22e675b23db76',pushed_integration86='f62dca7500b1fa035ef7b377ac55e182ea3fd057')
save(r/'pre-fetch87.workspace-RAW.json',snap)
fetch=subprocess.run(['git','fetch','origin'],capture_output=True);(r/'fetch87.stdout.log').write_bytes(fetch.stdout);(r/'fetch87.stderr.log').write_bytes(fetch.stderr);assert fetch.returncode==0
for name,h in mods.items():assert sha(Path(name).read_bytes())==h,name
main=run(['git','rev-parse','origin/main']).decode().strip()
save(r/'fetch87.receipt.json',dict(exit_code=0,terminal_closed=True,origin_main_after=main,local_branch_updated=False,reason='Current working branch has isolated proof commits and preserved collaborator modifications; fetch only, no merge/reset.',all_recorded_worktree_bytes_preserved=True,Goal_complete=False))
print(json.dumps(dict(HEAD=snap['HEAD'],origin_main=main,preserved_tracked=len(mods),frontier_cells=len(cells),single_lane=snap['single_lane'])))
