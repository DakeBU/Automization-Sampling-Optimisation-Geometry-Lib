from pathlib import Path
import json,hashlib,sys
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-measurability80');d=r/'independent-math80'
raw=(d/'closed-manifest80.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='a855ab9e046a5b8176f4b8eae525ef81db1555b1b004bc97f2724af6897e0b87';m=json.loads(raw)
for x in m['artifacts']+[m['module'],m['decision'],m['additional_consulted_API']]:
 b=Path(x['path']).read_bytes();assert len(b)==x['RAW_bytes'] and hashlib.sha256(b).hexdigest()==x['RAW_sha256'],x['path']
a=json.loads((d/'decision80.json').read_bytes());assert a['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS' and not a['repair_required'];assert set(a['axioms'])=={'propext','Classical.choice','Quot.sound'}
q=json.loads(Path(a['fresh_whole_source_receipt']['path']).read_bytes());assert q['exit_code']==0 and q['terminal_closed'] and q['actual_foreground_PID']>0
out=r/'root.math80.adoption.json';assert not out.exists()
out.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_MATH_ONLY',reviewer=a['reviewer'],module=a['module'],native_decision_RAW_sha256=m['decision']['RAW_sha256'],native_closed_manifest_RAW_sha256=hashlib.sha256(raw).hexdigest(),fresh_compiler_receipt=a['fresh_whole_source_receipt'],kernel_dependency_receipt=a['kernel_closure'],axioms=a['axioms'],source_verdict=False,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n')
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
claim=json.loads((r/'claim.json').read_bytes());adv.checkpoint_advance(claim['advance_id'],worker_id=claim['created_by'],route_fingerprint='actual-clock/countable-measurable-gluing/exceptional-initial-phase/common-AE-arc-and-origin',progress_signature='3119jobs-EXIT0-standard3-independent-math-nine-formulaBODY-regions',mathematical_delta=claim['theorem_delta'],exact_residual='Source-blind reconstruction, fresh independently frozen source coverage and exact-commit admission pending; aggregate/reader/main/purification/global process laws remain separate.')
print('Independent math80 native artifacts adopted; no source/VERIFIED credit')
