"""Repair evidence carriage only; keep science mathematics and native reviews unchanged."""
from pathlib import Path
import hashlib,json,gzip,subprocess,datetime
r=Path(__file__).parent;sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert head=='8f70c088b7c06f4a3048ff5966f4dda7903f0aa0'
assert not subprocess.check_output(['git','diff','--cached','--name-only'],text=True).strip()
saved=load(r.parent/'pbps-next-history-extension-preread90/pre-fetch90.workspace-RAW.json')['tracked_modified']
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
index=load(r/'immutable-RAW-archives90.json');missing=[];checked=[]
tree=set(subprocess.check_output(['git','ls-tree','-r','--name-only',head],text=True).splitlines())
for x in index['files']:
 archive=Path(x['archive']);name=archive.resolve().relative_to(Path.cwd()).as_posix()
 assert '.private.' not in name and not name.endswith('.text.txt.gz')
 b=archive.read_bytes();raw=gzip.decompress(b)
 assert sha(b)==x['archive_raw_sha256'] and sha(raw)==x['raw_sha256'] and len(raw)==x['raw_bytes']
 assert raw==Path(x['raw_path']).read_bytes()
 assert sha(raw)!='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
 checked.append(name)
 if name not in tree:missing.append(name)
assert missing and all('.snapshot.' in p for p in missing)
receipt=r/'science-archive-repair90.json';assert not receipt.exists()
receipt.write_text(json.dumps(dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),classification='PUBLICATION_EVIDENCE_CARRIAGE',original_science_commit=head,diagnosis="The '.snapshot.' original exclusion also excluded corresponding .gz archives.",native_index=r.joinpath('immutable-RAW-archives90.json').as_posix(),all_declared_archives_checked=len(checked),missing_archives=missing,repair='Add only missing byteexact lossless public archives. Native index, originals, Lean, Seal, source/blind review and canonical semantic audit unchanged.',VERIFIED=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
paths=missing+[receipt.as_posix()]
assert not set(paths).intersection(saved)
for offset in range(0,len(paths),25):subprocess.run(['git','-c','core.autocrlf=false','add','-f','--',*paths[offset:offset+25]],check=True)
assert set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())==set(paths)
subprocess.run(['git','diff','--cached','--check'],check=True)
subprocess.run(['git','commit','-q','-m','Restore exact lossless PBPS history review archives'],check=True)
newhead=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
for name in checked:
 assert subprocess.check_output(['git','show',newhead+':'+name])==Path(name).read_bytes(),name
for p,h in saved.items():assert sha(Path(p).read_bytes())==h,p
print(json.dumps(dict(repaired_commit=newhead,archives_restored=len(missing),all_named_archives_in_tree=len(checked))))
