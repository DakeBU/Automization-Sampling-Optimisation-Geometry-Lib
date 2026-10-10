from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-nonaccumulation78');d=r/'independent-math78'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
manifest=load(d/'closed-manifest78.json')
for p in manifest['files']:
 b=Path(p['path']).read_bytes();assert len(b)==p['RAW_bytes'] and sha(b)==p['RAW_sha256']
decision=load(d/'decision78.json');assert sha((d/'decision78.json').read_bytes())=='9e2d5529437717aab24950a4b09d9105faaba82364807d7a09beceab7df66eb5'
assert decision['status']=='ACCEPTED_INDEPENDENT_WHOLE_MATHEMATICS78_ONLY' and decision['no_mathematical_repair_required']
assert sha(Path(decision['module']['path']).read_bytes())==decision['module']['RAW_sha256']
assert set(decision['axioms'])=={'propext','Classical.choice','Quot.sound'} and decision['full_fresh_source_elaboration']
receipt=load(decision['terminal_receipt']['path']);assert receipt['exit_code']==0 and receipt['terminal_closed']
def new(p,x):
 assert not Path(p).exists();Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
new(r/'root.math78.adoption.json',dict(status='ACCEPTED_INDEPENDENT_MATH_ONLY',reviewer=decision['reviewer'],module=decision['module'],native_decision_RAW_sha256=sha((d/'decision78.json').read_bytes()),native_run_manifest_RAW_sha256=sha((d/'closed-manifest78.json').read_bytes()),fresh_compiler_receipt=decision['terminal_receipt'],axioms=decision['axioms'],source_verdict=False,VERIFIED=False))
new(r/'proof-route-diagnosis78.json',dict(failure_class='IMPLEMENTATION_FAILED',mathematical_statement_unchanged=True,retained_failed_run='focused78-attempt1',diagnosis='The elaborated add_le_add_right API placed the fixed summand on the opposite side from the displayed comparison. Replace with the general add_le_add ih le_rfl; no theorem, route, assumption or definition change.',salvage='Complete source recurrence, probability good event, C0 stop, prefix induction, escape and finite-set proof retained.',retired_route='Ambiguous sided-add helper at the positive-cap induction step.',final_run='focused78-attempt2',final_exit=0,purification_debt=['Inherited prospective-only module comment is stale prose; private complete statement and compiled BODY are the reviewed mathematics.','Unused local hcapPos is nonblocking private proof debris; remove only with refreshed whole-module review during purification.']))
claim=load(r/'claim.json')
adv.checkpoint_advance(claim['advance_id'],worker_id=claim['created_by'],route_fingerprint='actual-clock/zero-cap-stop-or-positive-cap/Exp1-good-event/scaled-partial-sum/finite-horizon',progress_signature='3117jobs-EXIT0-standard3-independent-math-seven-formulaBODY-regions-blind-decoded',mathematical_delta=claim['theorem_delta'],exact_residual='Fresh source review and exact-commit independent verification; aggregate/reader/main/purification and downstream global process remain separate.')
print('Independent mathematics adopted; source and exact-commit verification remain pending.')
