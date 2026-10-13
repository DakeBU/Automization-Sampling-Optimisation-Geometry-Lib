from pathlib import Path
import json,sys,hashlib
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66')
pre=Path('runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66')
load=lambda p:json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return dict(path=p.as_posix(),bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest())
receipts=[r/n/'receipt.json' for n in ['focused-main-v1','diagnose-main-v2','diagnose-main-v3']]
assert all(load(p)['terminal_closed'] and load(p)['exit_code']==1 for p in receipts)
out=r/'elaboration-boundary66.diagnosis.json';assert not out.exists()
out.write_text(json.dumps(dict(kind='DEPENDENT_TYPE_ELABORATION_BOUNDARY',status='UNCHANGED_FREE_VARIABLE_ROUTE_FROZEN_FOR_DIAGNOSIS',receipts=[pin(p) for p in receipts],diagnosis=['v1 and v3 report declaration-level unknown free variable _fvar.8860. No BODY trace or mathematical fragment has compiler credit.','The v2 trace-insertion diagnostic inadvertently touched header let hp; that parser-negative is retained. The v3 header was restored from the immutable candidate exactly.','A bare unknown TACTIC in earlier type probes does not establish full elaboration; independently checking the sealed expression as a Prop-valued definition and a valid failing tactic.'],source_mathematical_statement_changed=False,full_type_elaboration_credit_suspended=True,prior_closed_header97_preserved=True,next_route='Minimal dependent-type elaboration diagnosis; no fourth identical body retry.',mathematical_progress_claim=False),indent=2)+'\n',encoding='utf-8',newline='\n')
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_advance as adv
adv.checkpoint_advance('ASTIS-SA-20261009-PBPSAmbientAdjointCorrector',worker_id='companion_root_20261005',route_fingerprint='same-actual-adjoint/typed-header-minimal-elaboration-diagnosis',progress_signature='declaration-free-variable-route-frozen-independent-header-diagnosis-pending',mathematical_delta='No compiled66 theorem credit; exact negative inputs and mathematical route retained, source statement unchanged.',exact_residual='Demonstrate full elaboration of the sealed dependent expression before further proof checking; independently distinguish header versus proof-body failure.')
print('Typed elaboration boundary retained; unchanged route frozen; no theorem/type acceptance inferred from unknown tactic.')
