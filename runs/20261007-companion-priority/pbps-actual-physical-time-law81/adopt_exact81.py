from pathlib import Path
import hashlib,json
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81');d=r/'exact-commit-verification81'
sha=lambda b:hashlib.sha256(b).hexdigest()
m=json.loads((d/'closed-manifest81.json').read_bytes())
assert sha((d/'closed-manifest81.json').read_bytes())=='c10d63e4ca9903a1a95b925fc68567070ab67338f7bcb169bbde1c05ede4a900'
assert sha((d/'verified.json').read_bytes())=='d193e172fc6504bcae94696e97237a794dcbd2abbddfb9e23e7732912de56ee8'
for x in [m['verified'],m['admission'],m['post_admission_frontier'],m['cell'],*m['artifacts']]:
 assert sha(Path(x['path']).read_bytes())==x['RAW_sha256'],x['path']
ack=r/'fresh-source81/schema-adapter-acknowledgment81.json'
assert sha(ack.read_bytes())=='986c324506ba0a6cc15f4a367a54d7cfc6eb80ee38770b376003cb0b0937222e'
(r/'root.exact81.adoption.json').write_text(json.dumps(dict(status='ADOPTED_INDEPENDENT_VERIFIED_SCIENCE',checked_commit=m['verified_commit'],verifier=m['verifier_id'],native_manifest_RAW_sha256=sha((d/'closed-manifest81.json').read_bytes()),schema_adapter_ack_RAW_sha256=sha(ack.read_bytes()),all_native_artifacts_RAW_rechecked=True,local_aggregate='pending',Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Native independent exact-commit evidence checked; no self-verification.')
