"""Commit only post-main gate and immutable storage-review receipts."""
from pathlib import Path
import datetime,gzip,hashlib,json,subprocess
r=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());out=r/'integration98/current-main'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a])
head=git('rev-parse','HEAD').decode().strip()
assert head=='170e1bad1f0887512b79c4b5711ce316ade5f511'
assert not git('diff','--cached','--name-only').strip()
labels=['canonical','publication','contributor','site-regressions','site-build','site-check','graph','diff-check']
receipts=[]
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=sha(b),bytes=len(b))
for label in labels:
 p=r/'checks98'/('current-main-'+label)/'receipt.json';d=load(p)
 assert d['exit_code']==0 and d['terminal_closed'],label
 receipts.append(pin(p))
gate=load('.astis/site-lean-gate.json');assert gate['passed'] and gate['commit']==head
review=r/'integration-storage-review98/storage-review98.native.json'
assert review.exists()
saved=load(r/'exact-commit-verification98/closed-RAW-manifest98.json')['preserved_collaborator_inputs']
for d in saved:assert sha(Path(d['path']).read_bytes())==d['raw_sha256'],d['path']
reader=out/'offline-reader98.json';assert load(reader)['status']=='PASS_GENERATED_CONTENT_ONLY'
note=dict(status='PASS_POST_CURRENT_MAIN_GATES',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checked_commit=head,science_commit='530a58f7c036a67787956b20d2d390890ec2fec7',integration_commit='1f42ab322465acf7a62e4d0e28cc045b4c22e4e4',upstream_main='f4f8d3a8ef0d4918cb30c333540a303b501ffc63',receipts=receipts,source_digest=gate['source_digest'],storage_transfer=pin(review),reader=pin(reader),reused_unchanged_audits='Original exact science, mathematical/source/decoder/exposition reviews, frontier/semantic/process-memory/harness/Python gates and static SVG evidence. Current-main diff has only three presentation files; no mathematical changes.',preserved_collaborator_RAWs=21,stabilized=False,main_merged=False,purified=False,actual_page_or_fine_branch_viewed=False,full_papers_complete=0,Goal_complete=False)
np=out/'revalidation98.json'
if np.exists():
 assert load(np)['checked_commit']==head and load(np)['status']=='PASS_POST_CURRENT_MAIN_GATES'
else:np.write_text(json.dumps(note,indent=2)+'\n',encoding='utf8',newline='\n')
files={r/'close_current_main98.py',r/'push98.py'}
for folder in [out,r/'integration-storage-review98',*[r/'checks98'/('current-main-'+x) for x in labels]]:
 files.update(p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
archives=[];staged=[]
for p in sorted(files):
 b=p.read_bytes();assert sha(b)!='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
 assert p.as_posix() not in {d['path'] for d in saved}
 if p.suffix in {'.pyc','.olean','.ilean'}:continue
 opaque=p.suffix in {'.log','.snapshot','.lean','.exactraw'}
 normalized=b'\n'.join(x.rstrip(b' \t') for x in b.replace(b'\r\n',b'\n').split(b'\n')).rstrip(b'\n')+b'\n'
 if opaque or normalized!=b:
  z=Path(str(p)+'.current-main98.raw.gz');assert not z.exists();z.write_bytes(gzip.compress(b,mtime=0))
  git('-c','core.autocrlf=false','add','-f','--',z.as_posix());staged.append(z.as_posix())
  archives.append(dict(original=p.as_posix(),raw_sha256=sha(b),archive=z.as_posix(),archive_raw_sha256=sha(z.read_bytes())))
 if not opaque:
  blob=subprocess.check_output(['git','hash-object','-w','--stdin'],input=normalized).decode().strip()
  git('update-index','--add','--cacheinfo','100644',blob,p.as_posix());staged.append(p.as_posix())
ap=out/'lossless-archive-manifest98.json';assert not ap.exists();ap.write_text(json.dumps(dict(archives=archives,scope=sorted(staged)),indent=2)+'\n',encoding='utf8',newline='\n')
git('-c','core.autocrlf=false','add','--',ap.as_posix());staged.append(ap.as_posix())
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(staged)
for d in archives:assert sha(gzip.decompress(git('show',':'+d['archive'])))==d['raw_sha256']
for a in [('diff','--cached','--check'),('diff','--check')]:subprocess.run(['git',*a],check=True,capture_output=True)
git('commit','-q','-m','Record PBPS Gibbs balance validation after current-main integration')
print('POST_MAIN98_COMMIT',git('rev-parse','HEAD').decode().strip())
