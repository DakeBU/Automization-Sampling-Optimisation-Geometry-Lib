"""Preserve a failed diagnostic script byte-for-byte in a lossless archive."""
from pathlib import Path
import gzip,hashlib,json,subprocess
r=Path(__file__).parent;load=lambda p:json.loads(p.read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
rel=lambda p:Path(p).resolve().relative_to(Path.cwd()).as_posix()
stage=load(r/'science-staging89.json');expected={x['path'] for x in stage['files']}|{rel(r/'science-staging89.json')}
current=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())
assert current==expected
bad=r/'prepare_publication89.escape-error.exactraw.snapshot.py';raw=bad.read_bytes();z=Path(str(bad)+'.gz')
assert not z.exists();z.write_bytes(gzip.compress(raw,mtime=0));assert gzip.decompress(z.read_bytes())==raw
receipt=r/'science-whitespace89.recovery.json';assert not receipt.exists()
receipt.write_text(json.dumps(dict(failure_class='API_BLOCKED',negative_terminal='8870ab',staged_check_exit_code=2,native_snapshot=bad.as_posix(),native_RAW_sha256=sha(raw),native_bytes=len(raw),lossless_archive=z.as_posix(),archive_RAW_sha256=sha(z.read_bytes()),resolution='Remove only this newly staged diagnostic snapshot from index; publish lossless archive instead. Original remains byte-exact on disk. No production/source/Lean/state or collaborator change.',mathematics_changed=False),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','rm','--cached','--',bad.as_posix()],check=True)
add=[z.as_posix(),receipt.as_posix(),Path(__file__).as_posix()]
subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',*add],check=True)
current=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())
normalized={Path(p).resolve().relative_to(Path.cwd()).as_posix() for p in add}
assert current==(expected-{rel(bad)})|normalized
saved=load(r.parent/'pbps-conditional-next-wait-density-preread89/pre-fetch89.workspace-RAW.json')['tracked_modified']
assert len(saved)==21 and not current.intersection(saved)
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
assert load(r/'root.source89.adoption.json')['status']=='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY'
assert load(r/'root.math89.adoption.json')['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True)
(r/'science-staged-whitespace89.successor.log').write_bytes(q.stdout+q.stderr)
assert q.returncode==0,(q.stdout+q.stderr).decode(errors='replace')[-2000:]
subprocess.run(['git','commit','-q','-m','Prove actual PBPS conditional finite next-wait density'],check=True)
assert bad.read_bytes()==raw
print('SCIENCE_COMMIT',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
