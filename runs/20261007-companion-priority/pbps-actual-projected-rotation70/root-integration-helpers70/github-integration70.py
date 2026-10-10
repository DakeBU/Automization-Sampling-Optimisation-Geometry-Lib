from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70')
mode=sys.argv[1]; dest=r/'integration70'/('github-'+mode+'-record'); dest.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(name,args):
 with (dest/(name+'.stdout.log')).open('wb') as out,(dest/(name+'.stderr.log')).open('wb') as err:
  p=subprocess.Popen(args,stdout=out,stderr=err); code=p.wait()
 row=dict(command=args,actual_PID=p.pid,exit_code=code,terminal_closed=True)
 for k in ['stdout','stderr']:
  q=dest/(name+'.'+k+'.log'); b=q.read_bytes(); row[k]=dict(path=q.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b))
 (dest/(name+'.receipt.json')).write_text(json.dumps(row,indent=2)+'\n',encoding='utf8')
 assert code==0,(name,code)
 return (dest/(name+'.stdout.log')).read_bytes()
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip()=='c46af8a55e89419109f654c4553cf527993cbeed'
assert json.loads((r/'root.repository70.adoption.json').read_bytes())['accepted_scoped_aggregate']
git=['git','-c','http.sslBackend=openssl','-c','credential.helper=','-c','credential.helper=!gh auth git-credential']
branch='refs/heads/codex/sphmc-standardized-rgo'
if mode=='push':
 before=run('remote-before',git+['ls-remote','origin',branch]).decode().split()[0]
 assert before=='aa9dd2cf691489535aa8039850c2ee0bcdacdfb4',before
 run('ancestry',['git','merge-base','--is-ancestor',before,head])
 run('push',git+['push','origin','HEAD:'+branch])
 after=run('remote-after',git+['ls-remote','origin',branch]).decode().split()[0]
 assert after==head
elif mode=='pr':
 run('update-pr',['gh','pr','edit','315','--title','Prove actual PBPS projected rotation and preserve reader proof folds','--body-file',str(r/'integration70/pr315-body70.md')])
 q=json.loads(run('current-pr',['gh','pr','view','315','--json','url,title,headRefName,headRefOid,baseRefName,state']))
 assert q['headRefOid']==head and q['headRefName']=='codex/sphmc-standardized-rgo' and q['state']=='OPEN'
else: raise ValueError(mode)
(dest/'summary.json').write_text(json.dumps(dict(status='SUCCESS',actual_root_PID=os.getpid(),head=head,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),mode=mode,main_merged=False,live=False,Goal_complete=False),indent=2)+'\n',encoding='utf8')
print('PASS',mode,'exact integration commit',head,'main/live/Goal remain open.')
