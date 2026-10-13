"""Run only after this verifier's single native VERIFIED append, before closure."""
from context108 import *
import gzip
assert sys.argv[1:] == ['--after-native-VERIFIED']
assert head() == C
v=load(O/'verified.json')
assert v['verified_commit']==C and v['verifier_id']=='/root/exact_verifier96'
path=R/'runs/substantive_advances.jsonl'
prefix=git('show',C+':runs/substantive_advances.jsonl')
raw=path.read_bytes()
assert raw.startswith(prefix)
tail=raw[len(prefix):]
assert len(tail.splitlines())==1
event=json.loads(tail)
assert event['advance_id']==ID and event['to_state']=='VERIFIED'
assert event['worker_id']=='/root/exact_verifier96'
assert event['evidence']['verified_commit']==C
canonical_tail=tail.replace(b'\r\n',b'\n')
assert canonical_tail.splitlines()==tail.splitlines()
canonical=prefix+canonical_tail
archive=O/'ledger-before-owned-VERIFIED-tail-EOL108.exactraw.gz'
assert not archive.exists()
archive.write_bytes(gzip.compress(raw,mtime=0))
assert gzip.decompress(archive.read_bytes())==raw
for name,data in [('verified-ledger-tail108.original.exactraw.snapshot',tail),('verified-ledger-tail108.canonical.exactraw.snapshot',canonical_tail)]:
 p=O/name;assert not p.exists();p.write_bytes(data)
assert head()==C and path.read_bytes()==raw
if canonical!=raw:path.write_bytes(canonical)
assert path.read_bytes().startswith(prefix)
assert path.read_bytes().splitlines()==raw.splitlines()
save('owned-VERIFIED-tail-EOL108.native.json',dict(status='PASS',verified_commit=C,prefix_raw_sha256=sha(prefix),prefix_bytes=len(prefix),original_ledger_raw_sha256=sha(raw),canonical_ledger=info(path),original_archive=info(archive),native_event_payload_unchanged=True,only_one_owned_tail_event=True,existing_prefix_byte_identical=True,changed_CRLF_endings=tail.count(b'\r\n'),trailing_whitespace_changes=0,transformation='Only newly appended independent VERIFIED108 event terminal CRLF to LF; all prior committed bytes remain identical.'))
