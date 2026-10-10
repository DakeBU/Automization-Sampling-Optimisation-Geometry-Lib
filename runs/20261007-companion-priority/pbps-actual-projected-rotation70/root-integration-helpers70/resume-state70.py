from pathlib import Path
import hashlib, json, os, subprocess, sys
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70/resume-state70')
r.mkdir(exist_ok=False)
def git(*a): return subprocess.check_output(['git',*a])
before={k:git(*a) for k,a in {'head':['rev-parse','HEAD'],'branch':['branch','--show-current'],'tracked':['status','--porcelain=v1','--untracked-files=no'],'main':['rev-parse','origin/main']}.items()}
capsule=subprocess.check_output([sys.executable,'-X','utf8','tools/astis_advance.py','capsule'])
(r/'capsule.exactraw.json').write_bytes(capsule)
x=json.loads(capsule)
compact={k:v for k,v in x.items() if k!='advances'}
compact['advances']=[{k:a.get(k) for k in ['advance_id','state','owner_id','frontier_cell','updated_at']} for a in x.get('advances',[])]
(r/'capsule.compact.json').write_text(json.dumps(compact,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
with (r/'fetch.stdout.log').open('wb') as out,(r/'fetch.stderr.log').open('wb') as err:
 p=subprocess.Popen(['git','-c','http.sslBackend=openssl','-c','credential.helper=','-c','credential.helper=!gh auth git-credential','fetch','origin'],stdout=out,stderr=err)
 code=p.wait()
assert code==0,code
assert git('rev-parse','HEAD')==before['head'] and git('status','--porcelain=v1','--untracked-files=no')==before['tracked']
ancestor=subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode==0
receipt=dict(status='SAFE_FETCH_NO_CHECKOUT_MERGE_RESET',root_PID=os.getpid(),actual_git_PID=p.pid,exit_code=code,head=before['head'].decode().strip(),branch=before['branch'].decode().strip(),tracked_status=before['tracked'].decode(),origin_main_before=before['main'].decode().strip(),origin_main_after=git('rev-parse','origin/main').decode().strip(),main_is_ancestor=ancestor,capsule_RAW_sha256=hashlib.sha256(capsule).hexdigest(),user_explicit_resume=True)
(r/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8')
print(json.dumps(receipt));assert ancestor,'Updated main requires non-destructive reconciliation before integration'
