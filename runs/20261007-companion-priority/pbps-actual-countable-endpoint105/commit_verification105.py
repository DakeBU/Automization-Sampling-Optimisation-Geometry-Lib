from pathlib import Path
import gzip,hashlib,json,subprocess
r=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a])
science=load(r/'science-commit105.receipt.json')['commit']
assert git('rev-parse','HEAD').decode().strip()==science
assert not git('diff','--cached','--name-only').strip()
folder=r/'exact-commit-verification105'
v=load(folder/'verified.json')
# Verify native independent admission and the exact committed theorem.
assert science in json.dumps(v)
sys_path=Path.cwd()/'tools'
import sys
sys.path.insert(0,str(sys_path))
import astis_advance as adv
c=load(r/'claim.json');state=adv.current_advances()[c['advance_id']]
assert state['state']=='VERIFIED' and state['latest_evidence']['verified_commit']==science
saved=load(folder/'closed-RAW-manifest105.json')['preserved_collaborator_inputs']
for row in saved:assert sha(Path(row['path']).read_bytes())==row['raw_sha256']
paths=[p for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
paths += [Path('research-wiki/frontier-cells')/(c['frontier_cell']+'.json'),Path('runs/substantive_advances.jsonl'),r/'science-commit105.receipt.json',Path(__file__).resolve().relative_to(Path.cwd().resolve())]
staged=[];archives=[]
for p in sorted(set(paths)):
 raw=p.read_bytes();name=p.as_posix()
 if p.suffix.lower() in {'.gz','.png','.jpg','.pdf'}:
  git('-c','core.autocrlf=false','add','-f','--',name);staged.append(name);continue
 normalized=b'\n'.join(x.rstrip(b' \t') for x in raw.replace(b'\r\n',b'\n').split(b'\n')).rstrip(b'\n')+b'\n'
 opaque=name.startswith('runs/') and (p.suffix in {'.log','.lean','.html','.snapshot','.exactraw'} or len(raw)>200000)
 if opaque or normalized!=raw:
  z=Path(str(p)+'.verification105.raw.gz')
  assert not z.exists() or gzip.decompress(z.read_bytes())==raw
  if not z.exists():z.write_bytes(gzip.compress(raw,mtime=0))
  git('-c','core.autocrlf=false','add','-f','--',z.as_posix());staged.append(z.as_posix())
  archives.append(dict(raw_path=name,raw_sha256=sha(raw),archive=z.as_posix(),archive_sha256=sha(z.read_bytes()),archive_only=opaque))
 if not opaque:
  blob=subprocess.check_output(['git','hash-object','-w','--stdin'],input=normalized).decode().strip()
  subprocess.run(['git','update-index','--add','--cacheinfo','100644',blob,name],check=True);staged.append(name)
m=r/'verification-storage105.json';assert not m.exists()
m.write_text(json.dumps(dict(science_commit=science,archives=archives,preserved_collaborator_inputs=saved,scope='Independent VERIFIED checkpoint only; aggregate integration and sphere-gradient reconciliation pending.'),indent=2)+'\n',encoding='utf8',newline='\n')
git('-c','core.autocrlf=false','add','--',m.as_posix());staged.append(m.as_posix())
assert set(git('diff','--cached','--name-only').decode().splitlines())<=set(staged)
subprocess.run(['git','diff','--cached','--check'],check=True)
git('commit','-q','-m','Record independent verification of actual PBPS endpoint law')
print(git('rev-parse','HEAD').decode().strip())
