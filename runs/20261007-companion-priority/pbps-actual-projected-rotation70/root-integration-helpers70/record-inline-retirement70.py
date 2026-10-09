from pathlib import Path
import hashlib,json,sys

r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70')
names=['focused-v1','scope-diagnostic-v1','type-ascription-diagnostic-v1']
rows=[]
for name in names:
 p=r/name/'receipt.json'; b=p.read_bytes(); q=json.loads(b)
 assert q['terminal_closed'] and q['exit_code']==1
 rows.append(dict(path=p.as_posix(),RAW_sha256=hashlib.sha256(b).hexdigest(),PID=q['actual_foreground_PID'],exit_code=1))
p=r/'compiler-diagnosis70/inline-route-retired70.json';assert not p.exists()
p.write_text(json.dumps(dict(status='INLINE_DEPENDENT_TYPE_ROUTE_RETIRED_WITH_PRIOR66_REUSE',
 negative_receipts=rows,first_tactic_never_executed=True,
 exact_residual='Pinned Lean4.33.0 reports declaration-level unknown free variable before BODY on the complete inline dependent result.',
 strict_reduction='Separate representation/type-elaboration failure from the unchanged mathematical proof; reuse independently diagnosed66 literal Prop route already accepted in69.',
 not_a_mathematical_obstruction=True,source_hypotheses_unchanged=True,
 no_theorem_compile_credit=True,no_fourth_unchanged_inline_retry=True,
 smaller_next_delta='Compile exact literal statement representation, then resolve BODY-local APIs without changing the sealed mathematical statement.'),indent=2)+'\n',encoding='utf-8',newline='\n')
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_advance as adv
adv.checkpoint_advance('ASTIS-SA-20261009-PBPSActualProjectedRotation',worker_id='companion_root_20261005',
 route_fingerprint='actual-projected-rotation/inline-dependent-type-route-retired',
 progress_signature='three-negative-type-only-receipts-prior66-diagnosis-reused-literal-prop-candidate',
 mathematical_delta='Exact70 statement and proof route preserved; header failures isolated before BODY, no theorem credit.',
 exact_residual='Admit reviewed exact literal representation and compile actual reflected-input mean/rotation/energy theorem BODY.')
print('Inline route retired with three terminal negatives and prior66 diagnosis; no mathematical obstruction or proof credit.')
