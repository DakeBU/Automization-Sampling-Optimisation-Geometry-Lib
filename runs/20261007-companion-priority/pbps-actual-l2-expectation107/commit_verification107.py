from pathlib import Path
import gzip,hashlib,json,subprocess
r=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git','-c','core.autocrlf=false','-c','core.fscache=false',*a])
science=load(r/'science-commit107.receipt.json')['commit']
assert git('rev-parse','HEAD').decode().strip()==science
assert not git('diff','--cached','--name-only').strip()
folder=r/'exact-commit-verification107'
v=load(folder/'verified.json')
# Verify native independent admission and the exact committed theorem.
assert science in json.dumps(v)
sys_path=Path.cwd()/'tools'
import sys
sys.path.insert(0,str(sys_path))
import astis_advance as adv
c=load(r/'claim.json');state=adv.current_advances()[c['advance_id']]
assert state['state']=='VERIFIED' and state['latest_evidence']['verified_commit']==science
saved=load(folder/'closed-RAW-manifest107.json')['preserved_collaborator_inputs']
for row in saved:assert sha(Path(row['path']).read_bytes())==row['raw_sha256']
# Only normalize this independently written owned tail; retain exact original bytes.
ledger=Path('runs/substantive_advances.jsonl');raw_ledger=ledger.read_bytes();prefix=git('show','HEAD:runs/substantive_advances.jsonl')
assert raw_ledger.startswith(prefix)
tail=raw_ledger[len(prefix):]
assert all(json.loads(x)['advance_id']==c['advance_id'] for x in tail.splitlines())
newtail=tail.replace(b'\r\n',b'\n')
assert tail.splitlines()==newtail.splitlines()
if newtail!=tail:
 z=r/'ledger-before-verification-tail-EOL107.exactraw.gz';assert not z.exists();z.write_bytes(gzip.compress(raw_ledger,mtime=0))
 ledger.write_bytes(prefix+newtail)
 (r/'verification-tail-EOL107.json').write_text(json.dumps(dict(original_raw_sha256=sha(raw_ledger),normalized_raw_sha256=sha(ledger.read_bytes()),committed_prefix_unchanged=True,record_payloads_unchanged=True,owned_advance=c['advance_id'],events=len(tail.splitlines()),original_archive=z.as_posix()),indent=2)+'\n',encoding='utf8',newline='\n')
paths=[p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
paths += [Path('research-wiki/frontier-cells')/(c['frontier_cell']+'.json'),Path('runs/substantive_advances.jsonl'),r/'science-commit107.receipt.json',r/'ledger-before-verification-tail-EOL107.exactraw.gz',r/'verification-tail-EOL107.json',Path(__file__).resolve().relative_to(Path.cwd().resolve())]
staged=[];archives=[]
for p in sorted(set(paths)):
 if not p.exists():continue
 raw=p.read_bytes();name=p.as_posix()
 if name == 'runs/substantive_advances.jsonl':
  prior=git('show','HEAD:'+name)
  assert raw.startswith(prior), 'Canonical ledger prefix must remain byte-identical'
  assert all(json.loads(line)['advance_id']==c['advance_id'] for line in raw[len(prior):].splitlines()), 'Only owned107 events may append'
 if p.suffix.lower() in {'.gz','.png','.jpg','.pdf'}:
  git('-c','core.autocrlf=false','add','-f','--',name);staged.append(name);continue
 normalized=b'\n'.join(x.rstrip(b' \t') for x in raw.replace(b'\r\n',b'\n').split(b'\n')).rstrip(b'\n')+b'\n'
 opaque=name != 'runs/substantive_advances.jsonl' and name.startswith('runs/') and (p.suffix in {'.log','.lean','.html','.snapshot','.exactraw'} or len(raw)>200000)
 if opaque or normalized!=raw:
  z=Path(str(p)+'.verification107.raw.gz')
  assert not z.exists() or gzip.decompress(z.read_bytes())==raw
  if not z.exists():z.write_bytes(gzip.compress(raw,mtime=0))
  git('-c','core.autocrlf=false','add','-f','--',z.as_posix());staged.append(z.as_posix())
  archives.append(dict(raw_path=name,raw_sha256=sha(raw),archive=z.as_posix(),archive_sha256=sha(z.read_bytes()),archive_only=opaque))
 if not opaque:
  blob=subprocess.check_output(['git','hash-object','-w','--stdin'],input=normalized).decode().strip()
  subprocess.run(['git','update-index','--add','--cacheinfo','100644',blob,name],check=True);staged.append(name)
m=r/'verification-storage107.json';assert not m.exists()
m.write_text(json.dumps(dict(science_commit=science,archives=archives,preserved_collaborator_inputs=saved,scope='Independent VERIFIED checkpoint only; aggregate integration pending.'),indent=2)+'\n',encoding='utf8',newline='\n')
git('-c','core.autocrlf=false','add','--',m.as_posix());staged.append(m.as_posix())
assert set(git('diff','--cached','--name-only').decode().splitlines())<=set(staged)
subprocess.run(['git','diff','--cached','--check'],check=True)
git('commit','-q','-m','Record independent verification of actual PBPS L2 expectation contraction')
print(git('rev-parse','HEAD').decode().strip())
