"""Extract bounded native CI evidence as DATA only, never execute submissions."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--zip',type=Path,required=True)
p.add_argument('--sha256',required=True)
p.add_argument('--destination',type=Path,required=True)
p.add_argument('--run',type=int,required=True)
p.add_argument('--artifact',type=int,required=True)
p.add_argument('--head',required=True)
args=p.parse_args()
raw=args.zip.read_bytes()
assert len(raw)<=20*1024*1024 and hashlib.sha256(raw).hexdigest()==args.sha256
dest=args.destination.resolve()
assert dest.parent==Path(__file__).resolve().parent and not dest.exists()
members={}
with zipfile.ZipFile(args.zip) as archive:
    files=[i for i in archive.infolist() if not i.is_dir()]
    assert len({i.filename for i in files})==len(files)
    assert sum(i.file_size for i in files)<=20*1024*1024
    for info in files:
        path=PurePosixPath(info.filename)
        assert not path.is_absolute() and '..' not in path.parts and '\\' not in info.filename
        assert ':' not in info.filename and info.file_size<=2*1024*1024
    dest.mkdir()
    for info in files:
        target=dest/info.filename
        assert target.resolve().is_relative_to(dest)
        target.parent.mkdir(parents=True,exist_ok=True)
        data=archive.read(info)
        target.write_bytes(data)
        members[info.filename]=hashlib.sha256(data).hexdigest()
manifest={'schema_version':1,'scope':'Unmodified CI evidence DATA; never host-execute submitted/hostile Lean',
          'run':args.run,'artifact':args.artifact,'head':args.head,
          'zip_sha256':args.sha256,'members':members}
(dest/'archive-binding.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'run':args.run,'head':args.head,'files':len(files),'zip_sha256':args.sha256}))
