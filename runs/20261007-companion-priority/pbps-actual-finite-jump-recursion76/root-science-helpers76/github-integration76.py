from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-actual-finite-jump-recursion76');mode=sys.argv[1]
out=r/'integration76'/('github-'+mode+'-record');out.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(name,args):
 with (out/(name+'.stdout.log')).open('wb') as s,(out/(name+'.stderr.log')).open('wb') as e:
  p=subprocess.Popen(args,stdout=s,stderr=e);code=p.wait()
 row=dict(command=args,actual_PID=p.pid,exit_code=code,terminal_closed=True)
 for k in ['stdout','stderr']:
  q=out/(name+'.'+k+'.log');b=q.read_bytes();row[k]=dict(path=q.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b))
 (out/(name+'.receipt.json')).write_text(json.dumps(row,indent=2)+'\n',encoding='utf8',newline='\n')
 assert code==0,(name,code)
 return (out/(name+'.stdout.log')).read_bytes()
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert subprocess.check_output(['git','rev-parse','HEAD^'],text=True).strip()==json.loads((r/'root.exact-verification76.adoption.json').read_bytes())['verified_commit']
assert json.loads((r/'root.repository76.adoption.json').read_bytes())['accepted_scoped_aggregate']
git=['git','-c','http.sslBackend=openssl','-c','http.version=HTTP/1.1','-c','credential.helper=','-c','credential.helper=!gh auth git-credential'];branch='refs/heads/codex/sphmc-standardized-rgo'
if mode=='push':
 before=run('remote-before',git+['ls-remote','origin',branch]).decode().split()[0]
 assert before=='54620175c56e7db191bcebe7bb010edda1744894',before
 run('ancestry',['git','merge-base','--is-ancestor',before,head])
 run('push',git+['push','origin','HEAD:'+branch]);after=run('remote-after',git+['ls-remote','origin',branch]).decode().split()[0];assert after==head
elif mode=='pr':
 run('update-pr',['gh','pr','edit','315','--title','Prove actual finite PBPS jump recursion and uniform spacing','--body-file',str(r/'integration76/pr315-body76.md')])
 q=json.loads(run('current-pr',['gh','pr','view','315','--json','url,title,headRefName,headRefOid,baseRefName,state']))
 assert q['headRefOid']==head and q['headRefName']=='codex/sphmc-standardized-rgo' and q['state']=='OPEN'
else:raise ValueError(mode)
(out/'summary.json').write_text(json.dumps(dict(status='SUCCESS',actual_root_PID=os.getpid(),head=head,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),mode=mode,normal_fast_forward_only=True,main_merged=False,live=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS',mode,'exact integration commit',head,'main/live/Goal remain open.')
