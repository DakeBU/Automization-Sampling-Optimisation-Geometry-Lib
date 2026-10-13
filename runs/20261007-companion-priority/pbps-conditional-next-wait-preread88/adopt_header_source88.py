from pathlib import Path
import hashlib,json,datetime
r=Path(__file__).parent;s=r/'header-source88';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
expected={'header88.source-decision.native.json':'38a95c5cd4c34d1861fdce32ec3c506afd41a58abef7430fe3815b10e30dc228','header88.source-review.run.native.json':'950d7ce2df3151ae0280725f717ce9b580c36f4de3070edafe0ec901c03d8038','closed-raw-manifest.header-source88.native.json':'2f2c49e16104d098e24fb99c5ff45db849245cf26e0008407bd8193a7d1b80fa','chronology.header-source88.native.jsonl':'b4baaf4d3fff0e84d6c72223236c6b8aa8873707434e65aacd1242a0f2fae07e'}
for name,h in expected.items():assert sha((s/name).read_bytes())==h,name
m=load(s/'closed-raw-manifest.header-source88.native.json')
for group in ['inputs','outputs']:
 for x in m[group]:
  p=Path(x['path']);assert p.stat().st_size==x['bytes'] and sha(p.read_bytes())==x['raw_sha256'],p
decision=load(s/'header88.source-decision.native.json');assert decision['verdict']=='ACCEPT_EXACT_HEADER_SOURCE_EQUIVALENT_AFTER_ELABORATION'
assert len(decision['semantic_slots'])==7
assert not any(x.get('blocking') for x in decision['deltas'])
assert sha((r/'header88.proposed.lean').read_bytes())=='89890948b0716e9e8a0a4e4d5c634aa166361b7fb1575f57e751d49e024aeed3'
out=r/'root.header-source88.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_PROSPECTIVE_HEADER_SOURCE_ONLY',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),reviewer='/root/fresh_source87',native_decision_RAW_sha256=expected['header88.source-decision.native.json'],native_manifest_RAW_sha256=expected['closed-raw-manifest.header-source88.native.json'],rechecked_inputs=len(m['inputs']),rechecked_outputs=len(m['outputs']),exact_header_RAW_sha256='89890948b0716e9e8a0a4e4d5c634aa166361b7fb1575f57e751d49e024aeed3',separate_distinct_source_graph_review='PENDING /root/exact_verify77',BODY_source_review=False,statement_sealed=False,VERIFIED=False,Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Adopted complete native independent source-header88 acceptance after exact RAW checks; not BODY/graph/VERIFIED credit.')
