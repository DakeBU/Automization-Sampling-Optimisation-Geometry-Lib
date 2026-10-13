from pathlib import Path
import gzip,hashlib,json,subprocess
r=Path(__file__).parent
files=[r/'header-review82/local-check-only.diff',r/'independent-math82/documentation-only-successor82.diff'];rows=[]
for p in files:
 raw=p.read_bytes();z=Path(str(p)+'.gz');assert not z.exists();z.write_bytes(gzip.compress(raw,mtime=0));assert gzip.decompress(z.read_bytes())==raw
 subprocess.run(['git','restore','--staged','--',p.as_posix()],check=True)
 subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',z.as_posix()],check=True)
 rows.append(dict(raw_path=p.as_posix(),RAW_bytes=len(raw),RAW_sha256=hashlib.sha256(raw).hexdigest(),archive=z.as_posix(),archive_RAW_sha256=hashlib.sha256(z.read_bytes()).hexdigest()))
record=r/'immutable-whitespace-archives82.json';record.write_text(json.dumps(dict(reason='Native audit diff context whitespace retained byte-exact locally and losslessly archived publicly; no source/proof/native verdict changes.',files=rows),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',record.as_posix(),Path(__file__).as_posix()],check=True)
q=subprocess.run(['git','-c','core.whitespace=cr-at-eol','diff','--cached','--check'],capture_output=True);assert q.returncode==0,(q.stdout+q.stderr).decode()
subprocess.run(['git','commit','-q','-m','Prove actual PBPS first-event defect and zero-time stochastic continuity'],check=True)
print('SCIENCE_COMMIT',subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip())
