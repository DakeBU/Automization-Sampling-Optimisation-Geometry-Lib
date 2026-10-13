from pathlib import Path
import hashlib,json,os,subprocess
out=Path(os.environ['ASTIS_FOREGROUND_OBSERVER_DIR'])
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args])
head=git('rev-parse','HEAD');tracked=git('status','--porcelain=v1','--untracked-files=no');main=git('rev-parse','origin/main')
(out/'before.tracked.RAW.log').write_bytes(tracked)
cmd=['git','-c','http.sslBackend=openssl','-c','http.version=HTTP/1.1','-c','credential.helper=','-c','credential.helper=!gh auth git-credential','fetch','origin']
with (out/'fetch.stdout.RAW.log').open('wb') as s,(out/'fetch.stderr.RAW.log').open('wb') as e:
 p=subprocess.Popen(cmd,stdout=s,stderr=e);code=p.wait()
assert code==0,code
after_head=git('rev-parse','HEAD');after_tracked=git('status','--porcelain=v1','--untracked-files=no');after_main=git('rev-parse','origin/main')
(out/'after.tracked.RAW.log').write_bytes(after_tracked)
assert head==after_head and tracked==after_tracked
ancestor=subprocess.run(['git','merge-base','--is-ancestor','origin/main','HEAD']).returncode
q=dict(status='SAFE_FETCH_NO_CHECKOUT_NO_MERGE_NO_RESET',actual_root_PID=os.getpid(),actual_PID=p.pid,exit_code=code,terminal_closed=True,head=head.decode().strip(),origin_main_before=main.decode().strip(),origin_main_after=after_main.decode().strip(),tracked_status_unchanged=True,tracked_RAW_sha256=sha(tracked),main_is_ancestor_of_head=ancestor==0,working_tree_retained=True,HTTP11_reason='Prior74 normal push encountered SSL unexpected EOF under default HTTP; separately diagnosed HTTP1.1 normal TLS succeeded. This fetch uses the already demonstrated transport.',TLS_validation_preserved=True)
(out/'safe-fetch.receipt.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf8',newline='\n');print(json.dumps(q))
