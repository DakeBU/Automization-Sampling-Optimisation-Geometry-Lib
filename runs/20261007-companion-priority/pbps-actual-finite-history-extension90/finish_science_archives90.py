"""Finish exact staged archive-only repair after absolute/relative set diagnosis."""
from pathlib import Path
import hashlib,json,subprocess,gzip
r=Path(__file__).parent;sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='8f70c088b7c06f4a3048ff5966f4dda7903f0aa0'
receipt=r/'science-archive-repair90.json';x=load(receipt)
paths={Path(p).resolve().relative_to(Path.cwd()).as_posix() for p in x['missing_archives']+[receipt.as_posix()]}
assert len(paths)==4 and set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==paths
diag=r/'science-archive-repair90.stage-path-diagnosis.json';assert not diag.exists()
diag.write_text(json.dumps(dict(classification='PATH_REPRESENTATION_ONLY',original_helper='repair_science_archives90.py',failure='Staged paths were relative while two expected archive descriptors were absolute; exact set equality rejected before commit.',resolution='Normalize only expected set to repository-relative paths; confirm precisely three missing archives plus receipt already staged.',no_mathematical_change=True),indent=2)+'\n',encoding='utf8',newline='\n')
subprocess.run(['git','diff','--cached','--check'],check=True)
subprocess.run(['git','commit','-q','-m','Restore exact lossless PBPS history review archives'],check=True)
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
for item in load(r/'immutable-RAW-archives90.json')['files']:
 p=Path(item['archive']);name=p.resolve().relative_to(Path.cwd()).as_posix()
 b=subprocess.check_output(['git','show',head+':'+name]);assert b==p.read_bytes() and sha(gzip.decompress(b))==item['raw_sha256'],name
saved=load(r.parent/'pbps-next-history-extension-preread90/pre-fetch90.workspace-RAW.json')['tracked_modified']
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
print('ARCHIVE_COMPLETE_SCIENCE_SUCCESSOR',head)
