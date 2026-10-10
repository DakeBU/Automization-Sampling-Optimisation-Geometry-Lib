from pathlib import Path
import hashlib, json, gzip, os, datetime
r=Path('runs/20261007-companion-priority/pbps-macro-root63')
p=r/'exact-science-verification/inputs/0446.exactraw.snapshot'
out=r/'integration63/oversize-native-archive';out.mkdir(exist_ok=False)
def file_sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
expected='83aac919eb340fc489b6e6b1f9cc6adbcffb6f4208a1d422034082f531e12845'
assert p.stat().st_size==613225589 and file_sha(p)==expected
archive=out/'0446.exactraw.snapshot.gz'
with p.open('rb') as source,archive.open('wb') as dest,gzip.GzipFile(fileobj=dest,mode='wb',mtime=0,compresslevel=6) as packed:
 for block in iter(lambda:source.read(1024*1024),b''):packed.write(block)
h=hashlib.sha256();size=0
with gzip.open(archive,'rb') as f:
 for block in iter(lambda:f.read(1024*1024),b''):h.update(block);size+=len(block)
assert h.hexdigest()==expected and size==613225589
assert file_sha(p)==expected
record=dict(schema=1,event='LOSSLESS_NATIVE_HISTORICAL_RAW_PACKAGING_ONLY',actual_root_pid=os.getpid(),utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=p.as_posix(),source_RAW_sha256=expected,source_bytes=size,archive=archive.as_posix(),archive_RAW_sha256=file_sha(archive),archive_bytes=archive.stat().st_size,streaming_decompression_SHA_and_byte_count_verified=True,original_native_file_retained_unchanged=True,native_manifest_not_rewritten=True,staging_exclusion=[p.as_posix()],mathematical_admission=False,reason='GitHub standard blob limit; native superseded first-input snapshot preserved exactly in compressed form. Current corrected input.v2/0446 is2926bytes and staged normally.')
(out/'manifest.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(status='PASS',raw_bytes=size,archive_bytes=archive.stat().st_size,RAW_SHA_preserved=expected,original_retained=True)))
