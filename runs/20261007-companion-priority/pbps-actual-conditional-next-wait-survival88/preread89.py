"""Snapshot current truth before a safe fetch and the next bounded source edge."""
from pathlib import Path
import subprocess,json,hashlib,datetime,sys
r=Path('runs/20261007-companion-priority/pbps-conditional-next-wait-density-preread89');r.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(cmd):
 q=subprocess.run(cmd,capture_output=True);assert q.returncode==0,q.stderr.decode(errors='replace');return q.stdout
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
status=run(['git','status','--porcelain=v1','-z','--untracked-files=no']);(r/'status.exactraw.log').write_bytes(status)
mods={}
for entry in status.split(b'\0'):
 if entry:
  assert entry[:2]==b' M',entry;name=entry[3:].decode();mods[name]=sha(Path(name).read_bytes())
assert len(mods)==21 and not run(['git','diff','--cached','--name-only']).strip()
cap=run([sys.executable,'-X','utf8','tools/astis_advance.py','capsule','--max-advances','3','--max-discoveries','1','--max-cells','1']);(r/'capsule.exactraw.log').write_bytes(cap)
cells=[dict(path=p.as_posix(),raw_sha256=sha(p.read_bytes())) for p in sorted(Path('research-wiki/frontier-cells').glob('*.json'))]
snap=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),branch=run(['git','branch','--show-current']).decode().strip(),HEAD=run(['git','rev-parse','HEAD']).decode().strip(),origin_main_before=run(['git','rev-parse','origin/main']).decode().strip(),tracked_modified=mods,frontier_cells=cells,capsule_raw_sha256=sha(cap),single_lane=json.loads(cap)['single_stabilization_lane'])
save(r/'pre-fetch89.workspace-RAW.json',snap)
q=subprocess.run(['git','fetch','origin'],capture_output=True);(r/'fetch.stdout.log').write_bytes(q.stdout);(r/'fetch.stderr.log').write_bytes(q.stderr);assert q.returncode==0
for p,h in mods.items():assert sha(Path(p).read_bytes())==h,p
main=run(['git','rev-parse','origin/main']).decode().strip();ancestor=subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
save(r/'fetch.receipt.json',dict(exit_code=0,terminal_closed=True,origin_main_after=main,current_main_is_ancestor=ancestor,branch_updated=False,all_recorded_worktree_RAWs_preserved=True,reason='Fetch only; existing main ancestor checked, no update needed and all original local changes preserved.'))
save(r/'scheduling89.json',dict(current_checkpoint='docs/companion-papers-handoff.md#actual-pbps-history-dependent-next-wait-survival-2026-10-11',source_slice='runs/20261007-companion-priority/pbps-clock-tail-preread87/source-slice87.v2.json',candidate_source_node='S87-I5: conditional finite next-wait density',reason='actual87 supplies the entire-tail/history product law, actual86 the deterministic finite first-event density, and independently verified actual88 closes S87-I4 history-dependent survival. The smaller density component of S87-I5 is a candidate for the ordered-time/fullA7 consumer; select it only after current capsule/source/reuse review, without credit to remaining iteration/final factor.',scope='Preread/retrieval only. No new theorem, Seal, claim or closure yet.',preserved_goal=True))
print(json.dumps(dict(HEAD=snap['HEAD'],origin_main=main,main_is_ancestor=ancestor,preserved_tracked=len(mods),single_lane=snap['single_lane'],next_source_node='S87-I5: conditional finite next-wait density')))
