"""Commit only independently admitted92 scientific work; preserve collaborator RAW."""
from pathlib import Path
import datetime,gzip,hashlib,json,subprocess
R=Path('E:/Samplinglib');r=Path(__file__).parent
pre=r.parent/'pbps-ordered-iteration-preread92'
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def fresh(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def cmd(args):return subprocess.check_output(args,cwd=R)
claim=load(r/'claim.json')
assert load(r/'root.source92.visibility-adoption.json')['status']=='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY'
assert load(r/'root.math92.visibility-adoption.json')['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
assert (r/'proved-local92.v3.json').exists()
for label in ['publication-final','contributor-final','semantic-final','frontier-final','contributor-regressions','python-compile']:
    v=load(r/'checks92'/label/'receipt.json')
    assert v['terminal_closed'] and v['exit_code']==0,label
    if label not in {'contributor-regressions','python-compile'}:
        assert v['module_raw_sha256']=='4737e98180ad69da03ad8b68f72f996ebe265b1eda1fafaa0521f591b7644ead'
assert not cmd(['git','diff','--cached','--name-only']).strip()
assert cmd(['git','rev-parse','HEAD']).decode().strip()=='57ffbfed9ecde5d49c9dae4f9d2cb5aa593f26fe'
saved={str(R/x['path']):x['raw_sha256'] for x in load(pre/'resume-before-seal92/preserved-collaborator92.json')};assert len(saved)==21
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
ledger=R/'runs/substantive_advances.jsonl'
prefix=cmd(['git','show','HEAD:runs/substantive_advances.jsonl']);raw=ledger.read_bytes();assert raw.startswith(prefix)
tail=raw[len(prefix):];events=[json.loads(s) for s in tail.splitlines() if s.strip()]
assert events and all(x['advance_id']==claim['advance_id'] for x in events)
(r/'science-ledger-tail92.exactraw.snapshot').write_bytes(tail)
ledger.write_bytes(prefix+tail.replace(b'\r\n',b'\n'))
q=subprocess.run(['git','diff','--check'],cwd=R,capture_output=True)
(r/'science-plain-diff-check.stdout.log').write_bytes(q.stdout)
(r/'science-plain-diff-check.stderr.log').write_bytes(q.stderr)
fresh(r/'science-plain-diff-check.receipt.json',dict(command=['git','diff','--check'],exit_code=q.returncode,terminal_closed=True,new_tail_only_normalized=True,original_tail_sha256=sha(tail)))
assert q.returncode==0
folders=[r,pre,R/'runs/semantic-roundtrip/anonymous92']
def allowed(p):
    name=p.name.lower()
    return (not name.startswith('.private') and not name.endswith('.private.json') and name != 'primary-source-slices92.native.json' and '__pycache__' not in p.parts and
        p.suffix not in {'.pyc','.olean','.ilean','.c','.o','.ir'} and
        not name.endswith('.text.txt') and not ('primary' in name and p.suffix=='.html') and
        sha(p.read_bytes())!='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760')
def archive_raw(p):
    return p.suffix!='.gz' and (p.suffix in {'.log','.diff','.html','.lean','.snapshot'} or '.snapshot.' in p.name)
native=[p for folder in folders for p in folder.rglob('*') if p.is_file()]
fresh(r/'public-source-exclusions92.json',dict(reason='Primary source and private extracts stay local; public materials use attributed restatements.',
    paths=sorted(p.relative_to(R).as_posix() for p in native if not allowed(p))))
rows=[];raw_excluded=set()
for p in sorted(native):
    if not allowed(p) or not archive_raw(p):continue
    b=p.read_bytes();z=Path(str(p)+'.gz')
    if not z.exists():z.write_bytes(gzip.compress(b,mtime=0))
    assert gzip.decompress(z.read_bytes())==b
    raw_excluded.add(p)
    rows.append(dict(raw_path=p.relative_to(R).as_posix(),raw_bytes=len(b),raw_sha256=sha(b),
        archive=z.relative_to(R).as_posix(),archive_raw_sha256=sha(z.read_bytes())))
fresh(r/'immutable-RAW-archives92.json',dict(status='NATIVE_RETAINED_LOSSLESS_ARCHIVES',files=rows))
paths=set(claim['proposed_files']+[
 'research-wiki/frontier-cells/'+claim['frontier_cell']+'.json',
 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualOrderedPrefix.json',
 'website/content/declaration_lessons/pbps-actual-ordered-prefix.json',
 'website/content/publications/pbps-actual-ordered-prefix.json','runs/substantive_advances.jsonl'])
for folder in folders:
    for p in folder.rglob('*'):
        if p.is_file() and allowed(p) and p not in raw_excluded and not archive_raw(p):paths.add(p.relative_to(R).as_posix())
assert all(row['archive'] in paths for row in rows)
protected={Path(p).resolve().relative_to(R).as_posix() for p in saved}
assert not paths.intersection(protected)
inventory=[dict(path=p,raw_sha256=sha((R/p).read_bytes()),bytes=(R/p).stat().st_size) for p in sorted(paths)]
staging=r/'science-staging92.json'
fresh(staging,dict(files=inventory,archive_count=len(rows),preserved_collaborator_files=21,source_review='accepted',
    exact_commit_verification='pending',aggregate='pending',Goal_complete=False))
paths.add(staging.relative_to(R).as_posix());paths=sorted(paths)
for i in range(0,len(paths),25):
    subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',*paths[i:i+25]],cwd=R,check=True,capture_output=True)
assert set(cmd(['git','diff','--cached','--name-only']).decode().splitlines())==set(paths)
for row in rows:
    b=cmd(['git','show',':'+row['archive']]);assert sha(b)==row['archive_raw_sha256'] and sha(gzip.decompress(b))==row['raw_sha256']
subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],cwd=R,check=True,capture_output=True)
subprocess.run(['git','commit','-q','-m','Prove actual PBPS ordered finite-prefix law'],cwd=R,check=True,capture_output=True)
head=cmd(['git','rev-parse','HEAD']).decode().strip()
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
fresh(r/'science-commit92.receipt.json',dict(commit=head,files=len(paths),archives=len(rows),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    source_review='accepted',exact_commit_verification='pending',full_integration='pending',all21_collaborator_files_preserved=True))
print('SCIENCE_COMMIT',head,'files',len(paths),'archives',len(rows))
