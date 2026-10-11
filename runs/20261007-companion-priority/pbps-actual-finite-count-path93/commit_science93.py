"""Commit only independently source-admitted science, preserving collaborators."""
from pathlib import Path
import json,hashlib,gzip,subprocess,datetime,sys
R=Path(__file__).resolve().parents[3];run=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'));import astis_advance as adv
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def fresh(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
claim=load(run/'claim.json')
assert adv.current_advances()[claim['advance_id']]['state']=='PROVED_LOCAL'
assert load(run/'root.source93.scoped-adoption.json')['status']=='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY'
for label in ['publication-scoped-final','contributor-scoped-final','semantic-scoped-final','frontier-scoped-final','contributor-regressions','python-compile']:
    v=load(run/'checks93'/label/'receipt.json');assert v['exit_code']==0 and v['terminal_closed'],label
assert git('rev-parse','HEAD').decode().strip()=='a50632d37112aa59b7368079a917add0c69d0852'
assert not git('diff','--cached','--name-only').strip()
preserved=load(run.parent/'pbps-actual-ordered-prefix92/exact-commit-verification92/closed-RAW-manifest92.json')['preserved_collaborator_inputs']
for x in preserved:assert sha((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
ledger=R/'runs/substantive_advances.jsonl';head=git('show','HEAD:runs/substantive_advances.jsonl');raw=ledger.read_bytes();assert raw.startswith(head)
tail=raw[len(head):]
for row in tail.splitlines():
    if row.strip():assert json.loads(row)['advance_id']==claim['advance_id']
(run/'science-ledger-tail93.exactraw.snapshot').write_bytes(tail)
ledger.write_bytes(head+tail.replace(b'\r\n',b'\n'))
q=subprocess.run(['git','diff','--check'],cwd=R,capture_output=True)
(run/'science-plain-diff-check.stdout.log').write_bytes(q.stdout);(run/'science-plain-diff-check.stderr.log').write_bytes(q.stderr)
assert q.returncode==0
folders=[run,run.parent/'pbps-finite-count-path-preread93',R/'runs/semantic-roundtrip/anonymous93',
 run.parent/'pbps-actual-ordered-prefix92/next-source-graph93',run.parent/'pbps-actual-ordered-prefix92/next-boundary-math93',run.parent/'pbps-actual-ordered-prefix92/next-boundary-preread93']
def allowed(p):
    name=p.name.lower()
    return ('__pycache__' not in p.parts and not name.startswith('.private') and not name.endswith('.private.json')
      and p.suffix not in {'.pyc','.olean','.ilean','.c','.o','.ir'} and not name.endswith('.text.txt')
      and not ('primary' in name and p.suffix=='.html')
      and sha(p.read_bytes())!='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760')
def archive_raw(p):return p.suffix!='.gz' and (p.suffix in {'.log','.diff','.html','.lean','.snapshot','.stdout','.stderr'} or '.snapshot.' in p.name)
native=[p for d in folders if d.exists() for p in d.rglob('*') if p.is_file()]
fresh(run/'public-source-exclusions93.json',dict(reason='Full primary and private extracts stay local; public source text is attributed mathematical restatement.',paths=sorted(p.relative_to(R).as_posix() for p in native if not allowed(p))))
rows=[];excluded=set()
for p in sorted(native):
    if not allowed(p) or not archive_raw(p):continue
    b=p.read_bytes();z=Path(str(p)+'.gz')
    if not z.exists():z.write_bytes(gzip.compress(b,mtime=0))
    assert gzip.decompress(z.read_bytes())==b
    excluded.add(p);rows.append(dict(raw_path=p.relative_to(R).as_posix(),raw_bytes=len(b),raw_sha256=sha(b),archive=z.relative_to(R).as_posix(),archive_raw_sha256=sha(z.read_bytes())))
fresh(run/'immutable-RAW-archives93.json',dict(status='NATIVE_RETAINED_LOSSLESS_ARCHIVES',files=rows))
paths=set(claim['proposed_files']+['research-wiki/frontier-cells/'+claim['frontier_cell']+'.json',
 'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteCountPath.json',
 'website/content/declaration_lessons/pbps-actual-finite-count-path.json',
 'website/content/publications/pbps-actual-finite-count-path.json','runs/substantive_advances.jsonl'])
for d in folders:
    if d.exists():
        for p in d.rglob('*'):
            if p.is_file() and allowed(p) and p not in excluded and not archive_raw(p):paths.add(p.relative_to(R).as_posix())
assert not paths.intersection(x['path'] for x in preserved)
inventory=[dict(path=p,raw_sha256=sha((R/p).read_bytes()),bytes=(R/p).stat().st_size) for p in sorted(paths)]
staging=run/'science-staging93.json';fresh(staging,dict(files=inventory,archive_count=len(rows),preserved_collaborator_files=21,source_review='accepted',exact_commit_verification='pending',aggregate='pending',Goal_complete=False))
paths.add(staging.relative_to(R).as_posix());paths=sorted(paths)
for i in range(0,len(paths),25):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',*paths[i:i+25]],cwd=R,check=True,capture_output=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(paths)
for row in rows:
    b=git('show',':'+row['archive']);assert sha(b)==row['archive_raw_sha256'] and sha(gzip.decompress(b))==row['raw_sha256']
check=subprocess.run(['git','diff','--cached','--check'],cwd=R,capture_output=True)
(run/'science-staged-diff-check.log').write_bytes(check.stdout+check.stderr)
assert check.returncode==0,check.stdout.decode(errors='replace')[-4000:]
subprocess.run(['git','commit','-q','-m','Prove actual PBPS finite-count complete-path law'],cwd=R,check=True,capture_output=True)
commit=git('rev-parse','HEAD').decode().strip()
for x in preserved:assert sha((R/x['path']).read_bytes())==x['raw_sha256'],x['path']
fresh(run/'science-commit93.receipt.json',dict(commit=commit,files=len(paths),archives=len(rows),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_review='accepted',exact_commit_verification='pending',full_integration='pending',all21_collaborator_files_preserved=True))
print(json.dumps(dict(science_commit=commit,files=len(paths),archives=len(rows))))
