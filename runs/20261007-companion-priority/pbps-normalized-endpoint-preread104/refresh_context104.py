from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys
R=Path.cwd();pre=Path(__file__).parent;prev=pre.parent/'pbps-actual-phase-normalization103';source=prev/'next-primary104'
load=lambda p:json.loads(Path(p).read_bytes())
def ref(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def write(p,d):
 assert not p.exists(),p;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def git(*a):return subprocess.check_output(['git',*a]).decode('utf8').strip()
delivered=load(prev/'integration103/postpush-binding103.json');head=git('rev-parse','HEAD');assert head==delivered['local_head']==delivered['remote_head']==delivered['pr']['headRefOid']
write(pre/'context-before-fetch104.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),branch=git('branch','--show-current'),commit=head,workspace_porcelain=git('status','--porcelain=v1','--untracked-files=all'),frontier_files=[ref(p) for p in sorted(Path('research-wiki/frontier-cells').glob('*.json'))],execution=load('website/content/samplewiki_companion_frontiers.json')['execution']))
env=os.environ.copy();env['PYTHONUTF8']='1'
q=subprocess.run([sys.executable,'-X','utf8','tools/astis_advance.py','capsule'],capture_output=True,env=env)
(pre/'capsule104.json').write_bytes(q.stdout);(pre/'capsule104.stderr.log').write_bytes(q.stderr);assert q.returncode==0
q=subprocess.run(['git','fetch','origin'],capture_output=True)
(pre/'fetch104.stdout.log').write_bytes(q.stdout);(pre/'fetch104.stderr.log').write_bytes(q.stderr)
write(pre/'fetch-status104.json',dict(exit_code=q.returncode,head_after=git('rev-parse','HEAD'),origin_main=git('rev-parse','origin/main'),work_branch_updated=False,reason='Preserved existing dirty collaborator workspace; fetch only.'))
assert q.returncode==0 and git('rev-parse','HEAD')==head
print('104 before-fetch snapshot, live capsule and safe fetch recorded. No seal or claim yet.')
