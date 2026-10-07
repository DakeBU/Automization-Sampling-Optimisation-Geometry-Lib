from pathlib import Path
import json,hashlib,subprocess,datetime
R=Path('runs/20261007-companion-priority/gaussian-compact-hilbert-lsi');C='7e29e520bc57416a24a4609366c4d0f49cc97e22';V='picard_commit_verifier_20261005';REPO='DakeBU/Automization-Sampling-Optimisation-Geometry-Lib';PREFIX='remote-ci.7e29e520.retry1'
def sha(b):return hashlib.sha256(b).hexdigest()
def d(p):
 b=Path(p).read_bytes();return dict(path=Path(p).as_posix(),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')),bytes=len(b))
def put(p,x):
 assert not p.exists(),p;p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return d(p)
put(R/f'{PREFIX}.lease.json',dict(status='OPEN',reviewer=V,checked_commit=C,read='OPEN exact own-head GitHub REST states only',write='OPEN owned remote-ci.7e29e520.retry1 artifacts only',compiler='NOT_STARTED_CLOSED',Python='OPEN',canonical_mutations=False,detached_background_started=False))
def api(label,args):
 p=R/f'{PREFIX}.{label}.raw.json';err=R/f'{PREFIX}.{label}.stderr.log';assert not p.exists() and not err.exists()
 with p.open('wb') as out,err.open('wb') as log:code=subprocess.run(['gh',*args],stdout=out,stderr=log).returncode
 assert code==0,(label,code);return json.loads(p.read_text(encoding='utf-8')),d(p)
branch,bd=api('branch',['api',f'repos/{REPO}/git/ref/heads/codex/sphmc-standardized-rgo'])
pr,pd=api('pr',['pr','view','313','--repo',REPO,'--json','state,isDraft,headRefOid,url'])
assert branch['object']['sha']==pr['headRefOid']=='5e808dacffd1c97d8d0dcc01c8e92052bf180426'
runs,rd=api('runs',['api',f'repos/{REPO}/actions/runs?head_sha={C}&per_page=30'])
items=[x for x in runs['workflow_runs'] if x['head_sha']==C];assert len(items)==runs['total_count'] and len(items)<=4
rows=[{k:x.get(k) for k in ['id','name','workflow_id','event','head_branch','head_sha','status','conclusion','run_attempt','created_at','run_started_at','updated_at','html_url']} for x in items]
assert all(z['head_sha']==C and z['head_branch']=='codex/sphmc-standardized-rgo' for z in rows)
site=[x for x in rows if 'site' in x['name'].lower()];jobs=[];jobsraw=None
if site:
 assert len(site)==1
 raw,jobsraw=api('site-jobs',['api',f'repos/{REPO}/actions/runs/{site[0]["id"]}/attempts/{site[0]["run_attempt"]}/jobs?per_page=30'])
 jobs=[{k:z.get(k) for k in ['id','name','head_sha','status','conclusion','started_at','completed_at','html_url']} for z in raw['jobs']];assert all(z['head_sha']==C for z in jobs)
deploy=[z for z in jobs if 'deploy' in z['name'].lower()]
terminal=len(rows)==4 and all(z['status']=='completed' for z in rows)
success=terminal and all(z['conclusion']=='success' for z in rows)
state='terminal-four-run-success' if success else 'terminal-with-nonsuccess' if terminal else 'pending'
snapshot=put(R/f'{PREFIX}.snapshot.json',dict(reviewer=V,checked_commit=C,observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),branch_response=bd,pr_response=pd,runs_response=rd,site_jobs_response=jobsraw,exact_runs=rows,actual_branch_sha=branch['object']['sha'],PR=pr,site_jobs=jobs,all_four_observed=len(rows)==4,all_terminal=terminal))
receipt=dict(schema_version=1,reviewer=V,checked_commit=C,status=state,snapshot=snapshot,exact_runs=rows,success_count=sum(z['status']=='completed' and z['conclusion']=='success' for z in rows),pending_count=sum(z['status']!='completed' for z in rows),failure_count=sum(z['status']=='completed' and z['conclusion'] not in ['success','skipped'] for z in rows),not_yet_observed_count=4-len(rows),site_jobs=jobs,deployment_jobs=deploy,deployment_skipped_confirmed=bool(deploy) and all(z['status']=='completed' and z['conclusion']=='skipped' for z in deploy),actual_branch_sha=branch['object']['sha'],PR=pr,historical_checked_head=(C!=branch['object']['sha']),bounded_polling='Exactly one workflow run snapshot and one site-job snapshot; no backoff loop or background watcher.',boundary='Only actual exact7e29e520 head workflow/attempt states. Earlier39 and related heads excluded. Success requires all four completed/success; deployment skipped only from actual site job status. No main merge/deployed/live/future mathematical credit.',leases=dict(read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED'),canonical_mutations=False)
saved=put(R/f'{PREFIX}.audit.json',receipt);basis=dict(reviewer=V,checked_commit=C,audit=saved,snapshot=snapshot,status='CLOSED');run=put(R/f'{PREFIX}.run.json',dict(basis,deterministic_run_sha256=sha(json.dumps(basis,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()),hash_recipe='sha256 sorted compact UTF8 JSON basis'))
lp=R/f'{PREFIX}.lease.json';opening=R/f'{PREFIX}.lease.open.raw.snapshot.json';assert not opening.exists();opening.write_bytes(lp.read_bytes());lp.write_bytes((json.dumps(dict(status='CLOSED',reviewer=V,checked_commit=C,read='CLOSED',write='CLOSED',Python='CLOSED',compiler='NOT_STARTED_CLOSED',initial_manifest=d(opening),receipt=saved,run=run,canonical_mutations=False,detached_background_started=False),indent=2)+'\n').encode())
print(json.dumps(dict(status=state,receipt=saved,runs=rows,deployment_jobs=deploy,all_leases='CLOSED'),indent=2))
