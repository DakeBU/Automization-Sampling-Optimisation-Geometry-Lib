from pathlib import Path
import subprocess,json,hashlib,os,datetime
r=Path('runs/20261007-companion-priority/pbps-root-commutation67');d=r/'integration67/safe-fetch-final67';d.mkdir(exist_ok=False)
def run(args):
 p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE);o,e=p.communicate();return dict(command=args,pid=p.pid,exit_code=p.returncode),o,e
before,bo,be=run(['git','status','--porcelain=v1','--untracked-files=no']);(d/'before.tracked-status.RAW').write_bytes(bo);assert before['exit_code']==0
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip();refs0=subprocess.check_output(['git','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/origin']);(d/'before.refs.RAW').write_bytes(refs0)
rec,o,e=run(['git','-c','http.sslBackend=openssl','-c','credential.helper=','-c','credential.helper=!gh auth git-credential','fetch','origin']);(d/'fetch.stdout.RAW').write_bytes(o);(d/'fetch.stderr.RAW').write_bytes(e);assert rec['exit_code']==0
refs1=subprocess.check_output(['git','for-each-ref','--format=%(refname) %(objectname)','refs/remotes/origin']);(d/'after.refs.RAW').write_bytes(refs1);assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()==head
post=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=no']);(d/'after.tracked-status.RAW').write_bytes(post);assert bo==post
main=subprocess.check_output(['git','rev-parse','origin/main'],text=True).strip();anc=subprocess.run(['git','merge-base','--is-ancestor',main,head]).returncode
x=dict(status='SAFE_FETCH_NO_CHECKOUT_OR_WORKTREE_MUTATION',actual_root_pid=os.getpid(),checked_head=head,origin_main=main,origin_main_contained_in_HEAD=anc==0,fetch=rec,tracked_status_before_sha256=hashlib.sha256(bo).hexdigest(),tracked_status_after_sha256=hashlib.sha256(post).hexdigest(),observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),destructive_Git=False,automatic_merge=False)
(d/'receipt.json').write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n');print('PASS safe fetch',main,'contained',anc==0,'no tracked overwrite')
