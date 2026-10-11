"""Resume explicit staging; retain native RAW, publish LF text and lossless archives."""
from pathlib import Path
import hashlib,json,subprocess,gzip,re,datetime
R=Path(__file__).resolve().parents[3];r=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
assert git('rev-parse','HEAD').decode().strip()=='a50632d37112aa59b7368079a917add0c69d0852'
v=load(r/'science-staging93.json');expected={x['path'] for x in v['files']}|{(r/'science-staging93.json').relative_to(R).as_posix()}
actual=set(git('diff','--cached','--name-only').decode().splitlines());assert actual<=expected|{x+'.gz' for x in expected}
unchanged=[]
for p in sorted(expected-actual):
    assert git('show','HEAD:'+p)==(R/p).read_bytes(),p
    unchanged.append(p)
check=subprocess.run(['git','diff','--cached','--check'],cwd=R,capture_output=True)
bad=sorted(set(re.findall(r'^(.+?):\d+: (?:trailing whitespace|new blank line at EOF|space before tab)',(r/'science-staged-diff-check-first.log').read_text(encoding='utf8'),re.M)))
assert bad and all(p in actual and p.startswith('runs/') for p in bad)
archives=[]
for name in bad:
    p=R/name;raw=p.read_bytes();z=Path(str(p)+'.gz');zrel=z.relative_to(R).as_posix()
    if not z.exists():z.write_bytes(gzip.compress(raw,mtime=0))
    assert gzip.decompress(z.read_bytes())==raw
    subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',zrel],cwd=R,check=True,capture_output=True)
    normalized=raw.replace(b'\r\n',b'\n')
    # These are immutable evidence, so only the public index copy is normalized.
    normalized=b'\n'.join(x.rstrip(b' \t') for x in normalized.split(b'\n')).rstrip(b'\n')+b'\n'
    blob=subprocess.check_output(['git','hash-object','-w','--stdin'],input=normalized,cwd=R).decode().strip()
    subprocess.run(['git','update-index','--cacheinfo','100644',blob,name],cwd=R,check=True)
    archives.append(dict(raw_path=name,raw_bytes=len(raw),raw_sha256=sha(raw),archive=zrel,archive_raw_sha256=sha(z.read_bytes()),public_text_raw_sha256=sha(normalized),native_unchanged=True))
report=r/'science-text-RAW-archives93.json';assert not report.exists()
report.write_bytes((json.dumps(dict(status='EXACT_NATIVE_ARCHIVED_PUBLIC_TEXT_NORMALIZED',files=archives,unchanged_already_committed=unchanged),indent=2)+'\n').encode())
for p in [report,Path(__file__)]:subprocess.run(['git','-c','core.autocrlf=false','add','--',str(p)],cwd=R,check=True,capture_output=True)
for row in archives:
    assert sha((R/row['raw_path']).read_bytes())==row['raw_sha256']
    assert sha(git('show',':'+row['raw_path']))==row['public_text_raw_sha256']
    assert sha(gzip.decompress(git('show',':'+row['archive'])))==row['raw_sha256']
q=subprocess.run(['git','diff','--cached','--check'],cwd=R,capture_output=True)
(r/'science-staged-diff-check-final.log').write_bytes(q.stdout+q.stderr)
assert q.returncode==0,q.stdout.decode(errors='replace')[-5000:]
saved=load(r.parent/'pbps-actual-ordered-prefix92/exact-commit-verification92/closed-RAW-manifest92.json')['preserved_collaborator_inputs']
staged=set(git('diff','--cached','--name-only').decode().splitlines());assert not staged.intersection(x['path'] for x in saved)
for x in saved:assert sha((R/x['path']).read_bytes())==x['raw_sha256']
subprocess.run(['git','commit','-q','-m','Prove actual PBPS finite-count complete-path law'],cwd=R,check=True,capture_output=True)
commit=git('rev-parse','HEAD').decode().strip()
(r/'science-commit93.receipt.json').write_bytes((json.dumps(dict(commit=commit,files=len(staged),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_review='accepted',exact_commit_verification='pending',full_integration='pending',all21_collaborator_files_preserved=True),indent=2)+'\n').encode())
print(commit,len(staged),'files; independent exact-commit verification pending')
