from pathlib import Path
import datetime,hashlib,json,subprocess,sys
R=Path('E:/Samplinglib');r=Path(__file__).parent;out=r/'preintegration-fetch89';out.mkdir(exist_ok=False)
sys.path.insert(0,str(R/'tools'));import astis_advance as adv
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
preserved=json.loads((r.parent/'pbps-conditional-next-wait-density-preread89/pre-fetch89.workspace-RAW.json').read_bytes())['tracked_modified']
for p,h in preserved.items():assert sha((R/p).read_bytes())==h
capsule=adv.coordinator_capsule();save(out/'capsule.before-fetch.json',capsule)
status=git('status','--porcelain=v1','-z');(out/'status.before-fetch.exactraw.snapshot').write_bytes(status)
save(out/'before.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),branch=git('branch','--show-current').decode().strip(),HEAD=git('rev-parse','HEAD').decode().strip(),origin_main=git('rev-parse','origin/main').decode().strip(),preserved_collaborator_modified_RAWs=preserved,all_current_tracked_modified={p:sha((R/p).read_bytes()) for p in git('diff','--name-only').decode().splitlines()},single_stabilization_lane=capsule['single_stabilization_lane']))
q=subprocess.run(['git','fetch','origin'],cwd=R,capture_output=True);(out/'fetch.stdout.log').write_bytes(q.stdout);(out/'fetch.stderr.log').write_bytes(q.stderr);assert q.returncode==0
before=json.loads((out/'before.json').read_bytes());assert before['HEAD']==git('rev-parse','HEAD').decode().strip()
for p,h in before['all_current_tracked_modified'].items():assert sha((R/p).read_bytes())==h
ancestor=subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD'],cwd=R).returncode==0
save(out/'after.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),fetch_exit_code=0,origin_main=git('rev-parse','origin/main').decode().strip(),main_is_ancestor=ancestor,HEAD_unchanged=True,all_recorded_local_RAWs_unchanged=True,branch_updated=False,reason='Working branch already contains fetched main; no branch update needed.' if ancestor else 'Inspect integration without overwriting local changes; no automatic checkout/merge.'))
assert ancestor,'Fetched main diverged; clean integration analysis required.'
print('Safe fetch complete; main ancestor; HEAD/local RAWs unchanged.')
