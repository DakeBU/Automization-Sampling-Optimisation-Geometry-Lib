from pathlib import Path
import datetime,hashlib,json,subprocess,sys
root=Path.cwd(); pre=root/'runs/20261007-companion-priority/pbps-actual-position-l2-preread109'
pre.mkdir(exist_ok=False)
def git(*args):
    q=subprocess.run(['git','-c','core.autocrlf=false','-c','core.fscache=false',*args],capture_output=True)
    assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')
    return q.stdout
def save(name,data):
    (pre/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf8',newline='\n')
status=git('status','--porcelain=v1','--untracked-files=all');(pre/'status-before-fetch109.exactraw.log').write_bytes(status)
paths=['docs/companion-papers-handoff.md','website/content/samplewiki_companion_frontiers.json','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-l2-flip-duality.json','lean-toolchain','lake-manifest.json']
refs=[]
for name in paths:
    data=(root/name).read_bytes();(pre/(Path(name).name+'.current.exactraw')).write_bytes(data)
    refs.append(dict(path=name,raw_sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)))
head=git('rev-parse','HEAD').decode().strip()
assert head=='7b5717252c1a7e7f813e3d5931ecb283e39ff771'
save('before-fetch109.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),branch=git('branch','--show-current').decode().strip(),commit=head,status_raw_sha256=hashlib.sha256(status).hexdigest(),current_refs=refs))
q=subprocess.run([sys.executable,'-X','utf8','tools/astis_advance.py','capsule'],capture_output=True)
(pre/'capsule109.stdout.log').write_bytes(q.stdout);(pre/'capsule109.stderr.log').write_bytes(q.stderr);assert q.returncode==0
q=subprocess.run(['git','-c','core.autocrlf=false','-c','core.fscache=false','fetch','origin'],capture_output=True)
(pre/'fetch109.log').write_bytes(q.stdout+q.stderr);assert q.returncode==0
assert git('rev-parse','HEAD').decode().strip()==head
q=subprocess.run(['git','merge-base','--is-ancestor','origin/main',head])
save('after-fetch109.json',dict(commit=head,origin_main=git('rev-parse','origin/main').decode().strip(),origin_main_ancestor=q.returncode==0,worktree_updated=False,reason='Preserve current collaborator work and unique integration branch.'))
execution=json.loads((root/paths[1]).read_bytes())['execution'];print(json.dumps(execution,ensure_ascii=False)[:6500]);print(q.returncode)
