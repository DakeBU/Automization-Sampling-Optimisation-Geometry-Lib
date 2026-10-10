from pathlib import Path
import hashlib,json,datetime
r=Path(__file__).parent;s=r/'independent-source-first88';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
expected={'source-first88.freeze.native.json':'9b3dc106bb0bd83bf846af82aef051c7af5c6c0e2142b33d6834bc89777011da','source-proof-slice88.native.json':'7fe781cc3ab8092faf0c9970787c459f662a2e52585c4d637e57c0a328895726','source-coverage88.native.json':'6e88954e891eac264d81416f5661e3726c6db3a39c4e38915c38d2f8617b2e92','closed-raw-manifest.source-first88.native.json':'fedbc429c2e3cc01aa92a2b5dd94a0f5c4c431f005564bcb50631822681432f5','terminal-completion88.native.json':'924bc5a3d80b8911dc2b3aba75851c043851a8a5f0b48ed55b32e9eed00f031a','chronology.native.jsonl':'0f256f9d216ec1b5e8ae625374e62915434c58b3f3e15930e4675406b7bfbc3a'}
for name,h in expected.items():assert sha((s/name).read_bytes())==h,name
m=load(s/'closed-raw-manifest.source-first88.native.json')
for group in ['inputs','outputs']:
 for x in m[group]:
  p=Path(x['path']);assert p.stat().st_size==x['bytes'] and sha(p.read_bytes())==x['raw_sha256'],p
primary=load(s/'primary-source88.raw-manifest.native.json');raw=Path(primary['source']['path']).read_bytes()
for x in primary['anchors']:
 assert sha(raw[x['byte_start_zero_based']:x['byte_end_exclusive']])==x['raw_span_sha256'],x['id']
terminal=load(s/'terminal-completion88.native.json');assert terminal['status']=='SOURCE_FIRST_IMMUTABLE_FREEZE_CLOSED' and not terminal['candidate88_exposure']
header=r/'header88.proposed.lean';assert header.stat().st_mtime>datetime.datetime.fromisoformat(terminal['completed_utc']).timestamp()
out=r/'root.source-first88.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='ACCEPTED_PRIMARY_FIRST_INPUT_FREEZE_ONLY',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),independent_source_author='/root/fresh_source87',rechecked_manifest_inputs=len(m['inputs']),rechecked_manifest_outputs=len(m['outputs']),rechecked_primary_byte_spans=len(primary['anchors']),closed_manifest_RAW_sha256=expected['closed-raw-manifest.source-first88.native.json'],exact_header_RAW_sha256=sha(header.read_bytes()),header_created_after_closed_freeze=True,distinct_graph_review='PENDING /root/exact_verify77; creator header correspondence is not independent approval of own source graph.',statement_sealed=False,new_proof=False,VERIFIED=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Adopted immutable independent primary-first88 inputs after full RAW/span checks; graph/header/Seal admission separate.')
