from pathlib import Path
import json,hashlib
r=Path(__file__).parent;p=Path('runs/20261007-companion-priority/pbps-bounded-test-preread83/source_freeze83.closed-raw-manifest.json')
raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()=='6f0e838a8c3ada6dec3d3e842be55252885f0ba49f861256309963d5e8b6201d'
m=json.loads(raw);checked=[]
for x in m['raw_inputs']+m['raw_outputs']:
    b=Path(x['path']).read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['raw_sha256'];checked.append(x['path'])
z=dict(source_manifest=p.as_posix(),source_manifest_raw_sha256=hashlib.sha256(raw).hexdigest(),verified_raw_files=checked,effective_source_counts=m['effective_source_counts'],status='source-only-preread-mechanically-adopted',candidate='Actual fixed-reference bounded continuous real test integrability and expectation continuity, consuming actual82 internally.',truth_boundary='No83 Lean statement, proof, claim, source-topology approval or theorem admission. Distinct independent topology/header review required before seal. Full outer L2/Markov/restart/semigroup/invariance/cost/composition remain open.',Goal_complete=False)
(r/'next-source83.readiness.json').write_text(json.dumps(z,indent=2)+'\n',encoding='utf8',newline='\n')
print('Source-only83 RAW manifest adopted; no83 proof or independent topology admission')
