from pathlib import Path
import json,hashlib,subprocess,datetime
r=Path(__file__).parent
def git(*a):return subprocess.check_output(['git','-c','core.autocrlf=false',*a]).decode().strip()
def ref(p):
 p=Path(p);return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
head=git('rev-parse','HEAD');assert head=='0ccd3eb9609e544cf4db85bbbb6438ae20966fd5'
assert not git('diff','--cached','--name-only')
dirty=git('diff','--name-only').splitlines()
before=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),head=head,branch=git('branch','--show-current'),workspace_porcelain=git('status','--porcelain=v1','--untracked-files=all'),dirty_tracked_RAW=[ref(p) for p in dirty],frontier_RAW=[ref(p) for p in Path('research-wiki/frontier-cells').glob('*.json')])
p=r/'premerge105-v2.json';assert not p.exists();p.write_text(json.dumps(before,indent=2)+'\n',encoding='utf8',newline='\n')
q=subprocess.run(['git','fetch','origin'],capture_output=True);(r/'fetch-v2.stdout.log').write_bytes(q.stdout);(r/'fetch-v2.stderr.log').write_bytes(q.stderr);assert q.returncode==0
incoming=git('diff','--name-only','HEAD...origin/main').splitlines()
assert not set(dirty)&set(incoming),('Tracked dirty overlap',set(dirty)&set(incoming))
q=subprocess.run(['git','merge','--no-commit','--no-ff','origin/main'],capture_output=True)
(r/'merge.stdout.log').write_bytes(q.stdout);(r/'merge.stderr.log').write_bytes(q.stderr)
d=dict(exit_code=q.returncode,head_before=head,head_after=git('rev-parse','HEAD'),main=git('rev-parse','origin/main'),incoming=incoming,conflicts=git('diff','--name-only','--diff-filter=U').splitlines())
(r/'merge-result105.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf8',newline='\n')
for row in before['dirty_tracked_RAW']:assert ref(row['path'])['raw_sha256']==row['raw_sha256'],row
print(json.dumps(d,indent=2));print(q.stdout.decode(errors='replace')[-2500:])
