from pathlib import Path
import datetime,hashlib,json,subprocess,sys
R=Path.cwd();r=Path(__file__).parent
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):assert not p.exists();p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
prior=load(r.parent/'pbps-bounded-test-preread83/post-fetch83.workspace-RAW.corrected.json')['tracked_modified']
for p,h in prior.items():assert sha(p)==h,p
status=subprocess.check_output(['git','-c','core.quotePath=false','status','--porcelain=v1','--untracked-files=no'],text=True)
modified={}
for line in status.splitlines():
 p=Path(line[3:]);assert p.is_file(),line;modified[p.as_posix()]=sha(p)
assert modified==prior,(set(modified),set(prior))
snapshot=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),branch=subprocess.check_output(['git','branch','--show-current'],text=True).strip(),commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),status=status,tracked_modified=modified,source_manifest=dict(path=(r/'source_freeze84.raw-manifest.json').as_posix(),RAW_sha256=sha(r/'source_freeze84.raw-manifest.json')),prior83='independently VERIFIED, full local aggregate/gates, normalpushed integration5f29b2a3; actual browser/main/PURIFIED/live separate',frontier_cells=[dict(path=p.as_posix(),RAW_sha256=sha(p)) for p in sorted(Path('research-wiki/frontier-cells').glob('*.json'))])
write(r/'pre-fetch84.workspace-RAW.json',snapshot)
cmd=[sys.executable,'-X','utf8','tools/astis_advance.py','capsule'];q=subprocess.run(cmd,capture_output=True);assert q.returncode==0
(r/'capsule.before-fetch84.json').write_bytes(q.stdout)
write(r/'capsule.before-fetch84.receipt.json',dict(command=cmd,exit_code=q.returncode,terminal_closed=True,RAW_sha256=sha(r/'capsule.before-fetch84.json')))
q=subprocess.run(['git','fetch','origin'],capture_output=True);assert q.returncode==0,q.stderr.decode(errors='replace')
for p,h in modified.items():assert sha(p)==h,p
write(r/'post-fetch84.json',dict(exit_code=q.returncode,stdout=q.stdout.decode(errors='replace'),stderr=q.stderr.decode(errors='replace'),origin_main=subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip(),HEAD=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),all21_RAW_preserved=True,working_branch_updated=False,reason='Own local branch is ahead of main; preserve collaborator RAW modifications and current reviewed integration. No reset/rebase/checkout/pull.'))
print('Recorded branch/commit/all21RAW/frontier/capsule, then safe fetch; branch preserved')
