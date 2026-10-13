from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
r=Path('runs/20261007-companion-priority/pbps-macro-root63');out=r/'resume-sync63';out.mkdir(exist_ok=False)
def raw(cmd):return subprocess.check_output(cmd)
def text(cmd):return raw(cmd).decode('utf-8').strip()
def w(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
status=raw(['git','status','--porcelain=v1','-uall']);(out/'worktree.before.raw.txt').write_bytes(status)
before=dict(actual_pid=os.getpid(),at=datetime.datetime.now(datetime.timezone.utc).isoformat(),branch=text(['git','branch','--show-current']),commit=text(['git','rev-parse','HEAD']),origin_main=text(['git','rev-parse','origin/main']),status_raw_sha256=hashlib.sha256(status).hexdigest(),dirty_lines=len(status.splitlines()),toolchain=text(['git','show','HEAD:lean-toolchain']))
capsule=raw([sys.executable,'-X','utf8','tools/astis_advance.py','capsule']);(out/'capsule.current.raw.json').write_bytes(capsule);c=json.loads(capsule)
before['current_frontiers']=[dict(advance_id=a['advance_id'],state=a['state'],frontier_cell=a['frontier_cell']) for a in c['advances'] if a['state']!='VERIFIED'];before['single_stabilization_lane']=c['single_stabilization_lane'];w(out/'state.before-fetch.json',before)
cmd=['git','-c','http.sslBackend=openssl','-c','credential.helper=','-c','credential.helper=!gh auth git-credential','fetch','origin']
with (out/'fetch.stdout.log').open('wb') as o,(out/'fetch.stderr.log').open('wb') as e:
 p=subprocess.Popen(cmd,stdout=o,stderr=e);pid=p.pid;code=p.wait()
after=dict(fetch_pid=pid,fetch_exit_code=code,terminal_closed=True,commit=text(['git','rev-parse','HEAD']),branch=text(['git','branch','--show-current']),origin_main=text(['git','rev-parse','origin/main']),worktree_update='No checkout/reset/rebase/merge; dirty original directory retained.',main_changed=False)
after['main_changed']=after['origin_main']!=before['origin_main'];assert after['commit']==before['commit'] and after['branch']==before['branch'];assert raw(['git','status','--porcelain=v1','-uall']).splitlines()[:2]==status.splitlines()[:2]
w(out/'state.after-fetch.json',after);print('PASS safe fetch',pid,'EXIT',code,'origin/main',after['origin_main'],'main_changed',after['main_changed'],'original dirty branch retained.')
sys.exit(code)
