"""Execute after89 sole-lane integration is committed and pushed."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-next-history-extension-preread90');r.mkdir(exist_ok=True)
assert not (r/'pre-fetch90.workspace-RAW.json').exists()
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(cmd):
 q=subprocess.run(cmd,capture_output=True);assert q.returncode==0,q.stderr.decode(errors='replace');return q.stdout
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
HEAD=run(['git','rev-parse','HEAD']).decode().strip()
assert run(['git','show','-s','--format=%s']).decode().strip()=='Integrate verified actual PBPS conditional finite next-wait density'
assert run(['git','ls-remote','origin','refs/heads/codex/sphmc-standardized-rgo']).decode().split()[0]==HEAD
status=run(['git','status','--porcelain=v1','-z','--untracked-files=no']);(r/'status.exactraw.log').write_bytes(status)
mods={}
for entry in status.split(b'\0'):
 if entry:
  assert entry[:2]==b' M',entry;name=entry[3:].decode();mods[name]=sha(Path(name).read_bytes())
assert len(mods)==21 and not run(['git','diff','--cached','--name-only']).strip()
cap=run([sys.executable,'-X','utf8','tools/astis_advance.py','capsule','--max-advances','3','--max-discoveries','1','--max-cells','1']);(r/'capsule.exactraw.log').write_bytes(cap)
cells=[dict(path=p.as_posix(),raw_sha256=sha(p.read_bytes())) for p in sorted(Path('research-wiki/frontier-cells').glob('*.json'))]
execution=json.loads(Path('website/content/samplewiki_companion_frontiers.json').read_bytes())['execution']
snap=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),branch=run(['git','branch','--show-current']).decode().strip(),HEAD=HEAD,origin_main_before=run(['git','rev-parse','origin/main']).decode().strip(),tracked_modified=mods,frontier_cells=cells,capsule_raw_sha256=sha(cap),single_lane=json.loads(cap)['single_stabilization_lane'],execution=execution)
save(r/'pre-fetch90.workspace-RAW.json',snap)
q=subprocess.run(['git','fetch','origin'],capture_output=True);(r/'fetch.stdout.log').write_bytes(q.stdout);(r/'fetch.stderr.log').write_bytes(q.stderr);assert q.returncode==0
for p,h in mods.items():assert sha(Path(p).read_bytes())==h,p
main=run(['git','rev-parse','origin/main']).decode().strip();ancestor=subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
assert run(['git','rev-parse','HEAD']).decode().strip()==HEAD
save(r/'fetch.receipt.json',dict(exit_code=0,terminal_closed=True,origin_main_after=main,current_main_is_ancestor=ancestor,branch_updated=False,all_recorded_worktree_RAWs_preserved=True,reason='Fetch only; current branch contains main and no update is required.' if ancestor else 'Main divergence requires safe integration analysis; no automatic branch update.'))
assert ancestor
save(r/'scheduling90.json',dict(current_checkpoint=execution['current_checkpoint'],candidate_source_node='Remaining S87-I5/G86-11: actual next-history extension and restricted joint law',source_graph='independent-source-first90/source-proof-graph90.native.json',reason='Fresh capsule/updated handoff plus independently reconstructed source identify the missing actual append/recursion transport consumer of89 conditional density. Derive constructor Borelness and actual H_(n+1) equality internally; old88 survival and a noatom lemma are not AND parents.',scope='Preread/retrieval only. No header, Seal, claim or closure yet.',preserved_goal=True))
print(json.dumps(dict(HEAD=HEAD,origin_main=main,main_is_ancestor=ancestor,preserved_tracked=len(mods),single_lane=snap['single_lane'],next_source_node='Actual next-history extension')))
