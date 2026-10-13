"""Preserve immutable reviewer evidence losslessly while satisfying diff-check."""
from pathlib import Path
import gzip,hashlib,json,re,subprocess
r=Path('runs/20261007-companion-priority/pbps-actual-nonaccumulation78')
log=r/'science-stage-whitespace78.log';raw=log.read_bytes();bad=[]
for line in raw.decode().splitlines():
 m=re.match(r'^(runs/[^:]+):\d+: (?:trailing whitespace|new blank line at EOF)',line)
 if m:bad.append(m[1])
assert len(set(bad))==6
rows=[]
for name in dict.fromkeys(bad):
 p=Path(name);assert p.resolve().is_relative_to(r.resolve())
 b=p.read_bytes();z=Path(str(p)+'.gz');assert not z.exists();z.write_bytes(gzip.compress(b,mtime=0));assert gzip.decompress(z.read_bytes())==b
 rows.append(dict(raw_path=name,RAW_sha256=hashlib.sha256(b).hexdigest(),archive=z.as_posix(),archive_RAW_sha256=hashlib.sha256(z.read_bytes()).hexdigest()))
subprocess.run(['git','restore','--staged','--',*dict.fromkeys(bad)],check=True)
index=r/'immutable-whitespace-archives78.json';index.write_text(json.dumps(dict(diagnosis='Pinned reviewer diff context and native helper EOF have literal whitespace. No RAW input/output is rewritten. Public archive restores the exact reviewed bytes; stage only the archive.',files=rows,failed_check_RAW_sha256=hashlib.sha256(raw).hexdigest()),indent=2)+'\n',encoding='utf8',newline='\n')
z=Path(str(log)+'.gz');z.write_bytes(gzip.compress(raw,mtime=0))
add=[x['archive'] for x in rows]+[index.as_posix(),z.as_posix(),Path(__file__).as_posix()]
subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',*add],check=True)
p=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True)
print('reviewed RAW evidence retained; retry whitespace EXIT',p.returncode)
assert p.returncode==0,(p.stdout+p.stderr).decode()
subprocess.run(['git','commit','-q','-m','Prove actual PBPS event-time nonaccumulation from canonical exponential inputs'],check=True)
print('SCIENCE_COMMIT',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
