from pathlib import Path
import json,hashlib,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-cover79');d=r/'independent-math79'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
m=load(d/'closed-manifest79.json')
for x in m['artifacts']:
 b=Path(x['path']).read_bytes();assert len(b)==x['RAW_bytes'] and sha(b)==x['RAW_sha256']
a=load(d/'decision79.json');assert sha((d/'decision79.json').read_bytes())=='0a278d51e6459e0260d3ff6d1dc6dbb2d59d7a50b4fedc853a99825ebe731694'
assert a['status']=='ACCEPTED_INDEPENDENT_WHOLE_MATHEMATICS79_ONLY' and a['no_repair_required']
assert sha(Path(a['module']['path']).read_bytes())==a['module']['RAW_sha256']
assert set(a['axioms'])=={'propext','Classical.choice','Quot.sound'}
q=load(a['fresh_complete_source_receipt']['path']);assert q['exit_code']==0 and q['terminal_closed']
x=dict(status='ACCEPTED_INDEPENDENT_MATH_ONLY',reviewer=a['reviewer'],module=a['module'],native_decision_RAW_sha256=sha((d/'decision79.json').read_bytes()),native_run_manifest_RAW_sha256=sha((d/'closed-manifest79.json').read_bytes()),fresh_compiler_receipt=a['fresh_complete_source_receipt'],axioms=a['axioms'],direct_ASTIS_dependencies=a['direct_ASTIS_dependencies'],source_verdict=False,VERIFIED=False)
p=r/'root.math79.adoption.json';assert not p.exists();p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf8',newline='\n')
claim=load(r/'claim.json');adv.checkpoint_advance(claim['advance_id'],worker_id=claim['created_by'],route_fingerprint='actual-clock/least-first-crossing/monotone-half-open/live-record/finite-or-top-next-wait',progress_signature='3118jobs-EXIT0-standard3-independent-math-nine-formulaBODY-regions-blind-decoded',mathematical_delta=claim['theorem_delta'],exact_residual='Fresh independent source review and exact-commit verification; aggregate/reader/main/purification and global measurable process remain separate.')
print('Math79 accepted/adopted only; source and exact-commit verification pending.')
