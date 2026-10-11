from pathlib import Path
import subprocess,json,hashlib,datetime
r=Path(__file__).parent;out=r/'preintegration-fetch90';out.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();assert head=='e8d38b3002f4562ef254205135c0d213f9efe410'
saved=load(r.parent/'pbps-next-history-extension-preread90/pre-fetch90.workspace-RAW.json')['tracked_modified']
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
cells={p.as_posix():sha(p.read_bytes()) for p in Path('research-wiki/frontier-cells').glob('*.json')}
snap=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),HEAD=head,branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip(),status=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=no'],text=True),collaborator_RAWs=saved,frontier_RAWs=cells,origin_main_before=subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip())
(out/'before.json').write_text(json.dumps(snap,indent=2)+'\n',encoding='utf8',newline='\n')
q=subprocess.run(['git','fetch','origin'],capture_output=True)
(out/'stdout.log').write_bytes(q.stdout);(out/'stderr.log').write_bytes(q.stderr)
assert q.returncode==0,q.stderr.decode(errors='replace')
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==head
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
main=subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip()
ancestor=subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
(out/'receipt.json').write_text(json.dumps(dict(exit_code=0,terminal_closed=True,origin_main_after=main,main_is_ancestor=ancestor,branch_updated=False,all21_RAW_preserved=True,scope='Safe fetch only before sole-lane aggregation; no working-tree update.'),indent=2)+'\n',encoding='utf8',newline='\n')
assert ancestor,'New main requires safe integration diagnosis.'
print('Current main ancestor',main,';21RAW preserved; no branch update.')
