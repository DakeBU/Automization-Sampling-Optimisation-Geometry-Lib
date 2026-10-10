from pathlib import Path
import subprocess,json,hashlib,datetime,sys
r=Path(__file__).parent/'integration-final-prefetch88';r.mkdir(exist_ok=False);sha=lambda b:hashlib.sha256(b).hexdigest()
def run(cmd):q=subprocess.run(cmd,capture_output=True);assert q.returncode==0,q.stderr.decode(errors='replace');return q.stdout
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
status=run(['git','status','--porcelain=v1','-z','--untracked-files=no']);(r/'status.exactraw.log').write_bytes(status)
mods={}
for entry in status.split(b'\0'):
 if entry:
  assert entry[:2] in [b' M',b'M '],entry;name=entry[3:].decode();mods[name]=sha(Path(name).read_bytes())
assert not run(['git','diff','--cached','--name-only']).strip()
cap=run([sys.executable,'-X','utf8','tools/astis_advance.py','capsule','--max-advances','3','--max-discoveries','1','--max-cells','1']);(r/'capsule.exactraw.log').write_bytes(cap)
cells=[dict(path=p.as_posix(),raw_sha256=sha(p.read_bytes())) for p in sorted(Path('research-wiki/frontier-cells').glob('*.json'))]
snap=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),branch=run(['git','branch','--show-current']).decode().strip(),HEAD=run(['git','rev-parse','HEAD']).decode().strip(),origin_main_before=run(['git','rev-parse','origin/main']).decode().strip(),tracked_modified=mods,frontier_cells=cells,capsule_raw_sha256=sha(cap),single_lane=json.loads(cap)['single_stabilization_lane'])
save(r/'before-fetch.json',snap)
q=subprocess.run(['git','fetch','origin'],capture_output=True);(r/'fetch.stdout.log').write_bytes(q.stdout);(r/'fetch.stderr.log').write_bytes(q.stderr);assert q.returncode==0
for p,h in mods.items():assert sha(Path(p).read_bytes())==h,p
main=run(['git','rev-parse','origin/main']).decode().strip();ancestor=subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
save(r/'receipt.json',dict(exit_code=0,terminal_closed=True,origin_main_after=main,current_main_is_ancestor=ancestor,branch_updated=False,all_recorded_worktree_RAWs_preserved=True,reason='Fetch only; preserve all local edits. Integration guard separately requires current origin/main ancestry.'))
print(json.dumps(dict(origin_main=main,main_is_ancestor=ancestor,preserved_tracked=len(mods),single_lane=snap['single_lane'])))
