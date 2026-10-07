from pathlib import Path
import json,hashlib,subprocess,sys,datetime
R=Path('runs/20261007-companion-priority/gaussian-product-entropy');C='1eb2e29307d59fab662db842c3a6264c65245fe3';V='picard_commit_verifier_20261005';REPO='DakeBU/Automization-Sampling-Optimisation-Geometry-Lib'
def sha(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=Path(p).read_bytes();return dict(path=Path(p).as_posix(),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),bytes=len(b))
def put(p,x):
 assert not p.exists(),p
 p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return d(p)
label=sys.argv[1]
if label=='initial':put(R/'remote-ci.1eb2e293.lease.json',dict(status='OPEN',reviewer=V,checked_commit=C,read='OPEN exact head GitHub CI only',write='OPEN owned remote-ci.1eb2e293 artifacts only',compiler='NOT_STARTED_CLOSED',Python='OPEN',canonical_mutations=False,detached_background_started=False))
def api(label,args):
 p=R/f'remote-ci.1eb2e293.{sys.argv[1]}.{label}.raw.json';log=R/f'remote-ci.1eb2e293.{sys.argv[1]}.{label}.stderr.log'
 assert not p.exists() and not log.exists()
 with p.open('wb') as out,log.open('wb') as err:code=subprocess.run(['gh',*args],stdout=out,stderr=err).returncode
 assert code==0,(label,code)
 return json.loads(p.read_text(encoding='utf-8')),d(p)
runs,rd=api('runs',['api',f'repos/{REPO}/actions/runs?head_sha={C}&per_page=100'])
pr,pd=api('pr',['pr','view','313','--repo',REPO,'--json','state,isDraft,headRefOid,url,statusCheckRollup'])
assert pr['headRefOid']==C
items=[x for x in runs['workflow_runs'] if x['head_sha']==C];assert len(items)==runs['total_count']
rows=[{k:x.get(k) for k in ['id','name','workflow_id','event','head_branch','head_sha','status','conclusion','run_attempt','created_at','run_started_at','updated_at','html_url']} for x in items]
terminal=bool(rows) and all(x['status']=='completed' for x in rows)
jobs=[]
if terminal:
 for x in rows:
  raw,p=api('jobs'+str(x['id']),['api',f'repos/{REPO}/actions/runs/{x["id"]}/attempts/{x["run_attempt"]}/jobs?per_page=100'])
  jobs.append(dict(run_id=x['id'],raw=p,jobs=raw['jobs']))
snap=put(R/f'remote-ci.1eb2e293.{label}.snapshot.json',dict(reviewer=V,checked_commit=C,observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),runs_response=rd,pr_response=pd,exact_runs=rows,run_count=len(rows),all_runs_terminal=terminal,all_runs_success=terminal and all(x['conclusion']=='success' for x in rows),jobs=jobs,PR=dict(state=pr['state'],isDraft=pr['isDraft'],headRefOid=pr['headRefOid'],url=pr['url']),scope='Actual exact-head GitHub REST workflow runs/attempts. PR check rollup supplementary; no current main/deployed/live credit.'))
print(json.dumps(dict(snapshot=snap,terminal=terminal,runs=rows),indent=2))
