from pathlib import Path
import gzip, hashlib, json, os

r = Path('runs/20261007-companion-priority/pbps-reflection-intertwining69')
o = r/'independent-repository-reader69'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
assert load(r/'root.repository69.adoption.json')['accepted_scoped_aggregate']
lease_before = (o/'lease.final.json').read_bytes()
row = load(o/'lease.final.json')['COMPLETE_NAMED_REVIEW_DECISION_INPUT']
native = o/row['name']; raw = native.read_bytes()
assert len(raw) == row['RAW_bytes'] == 167233478
assert sha(raw) == row['RAW_sha256'] == '87b24e44b44993928d6ce9c511036e98d53ecbbbd5da126408362cb9af873605'
d = r/'integration69/native-transport69'; d.mkdir(exist_ok=False)
packed = gzip.compress(raw, compresslevel=6, mtime=0)
assert gzip.decompress(packed) == raw and len(packed) < 95*1024*1024
p = d/'complete-named-review-decision-input-payload.exactraw.json.gz'; p.write_bytes(packed)
manifest = dict(schema='exact-native69-Git-transport-v1', actual_root_PID=os.getpid(),
    original_path=native.as_posix(), original_RAW_bytes=len(raw), original_RAW_sha256=sha(raw),
    transport_path=p.as_posix(), transport_bytes=len(packed), transport_RAW_sha256=sha(packed),
    encoding='gzip level6, mtime0, decompress to exact original RAW bytes; no JSON reserialization',
    native_CLOSED_lease_RAW_sha256=sha(lease_before), native_local_files_unchanged=True,
    Git_RAW_object_identity_for_oversized_file=False,
    Git_transport_representation_only=True, mathematical_or_source_change=False,
    original_postclose_chronology_not_replayed_by_materialization=True)
(d/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
restore = '''from pathlib import Path
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
'''
(d/'materialize-outside-native-tree.py').write_text(restore,encoding='utf-8',newline='\n')
(d/'README.md').write_text('''The independently closed reader69 bundle has 335 original local files. One 167233478-byte complete named payload exceeds the Git hosting single-file limit. Its original local RAW file and CLOSED lease remain unchanged.

Git retains every other native file and this deterministic gzip representation. The manifest binds both compressed and original RAW bytes. This is an explicit transport representation, not a claim that the oversized original is a Git RAW object. No JSON content is reserialized or removed.

Run `materialize-outside-native-tree.py FRESH_OUTPUT_FILE` to recover the exact original outside the closed native directory, then use that RAW artifact for the manifest entry named in manifest.json. Original close receipts establish the original chronology; a new checkout/materialization does not replay timestamps or the original postclose event. Never overwrite or rewrite the original CLOSED bundle.
''',encoding='utf-8',newline='\n')
assert native.read_bytes() == raw and (o/'lease.final.json').read_bytes() == lease_before
print(json.dumps(dict(status='EXACT_NATIVE69_COMPRESSED_TRANSPORT_PREPARED',original_bytes=len(raw),transport_bytes=len(packed),native_unchanged=True)))
