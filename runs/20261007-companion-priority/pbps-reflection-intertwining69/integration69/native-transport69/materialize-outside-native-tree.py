from pathlib import Path
import gzip,hashlib,json,sys
d=Path(__file__).resolve().parent;m=json.loads((d/'manifest.json').read_bytes())
p=d/Path(m['transport_path']).name;b=p.read_bytes()
assert hashlib.sha256(b).hexdigest()==m['transport_RAW_sha256']
raw=gzip.decompress(b)
assert len(raw)==m['original_RAW_bytes'] and hashlib.sha256(raw).hexdigest()==m['original_RAW_sha256']
dst=Path(sys.argv[1]).resolve()
assert not dst.exists(), 'Use a fresh output file; never overwrite the original CLOSED tree.'
assert not dst.is_relative_to(d.parents[1]/'independent-repository-reader69')
dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
print(json.dumps(dict(materialized_RAW_path=dst.as_posix(),RAW_bytes=len(raw),RAW_sha256=m['original_RAW_sha256'],original_native_tree_mutated=False,original_closure_chronology_replayed=False)))
