from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-ambient-adjoint66')
def pin(p):
    b=p.read_bytes()
    return dict(path=p.as_posix(),bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest())
labels=['focused-both-v7','focused-both-v8','focused-both-typed-v9']
for label in labels:
    receipt=json.loads((r/label/'receipt.json').read_bytes())
    assert receipt['terminal_closed'] and receipt['exit_code']==1
log=(r/labels[-1]/'stdout.log').read_text(encoding='utf-8')
assert 'TRACE66 residual identity' in log and 'TRACE66 actual global witnesses' not in log
out=r/'consumer-reconstruction66.diagnosis.json'
assert not out.exists()
out.write_text(json.dumps(dict(status='TEST_OUTER_RECONSTRUCTION_RESIDUAL_LOCALIZED',receipts=[pin(r/x/'receipt.json') for x in labels],diagnosis=['v7 failed only on a redundant dsimp after extracting the named literal proposition; removed.','v8 reached deterministic 2M whnf timeout with no Test proof credit.','v9 explicitly typed operators,ambient identity and global implication; traces confirm all those steps and residual identity completed. Timeout precedes the first actual-global-witness trace,at outer nested witness reconstruction or its immediately following extraction.','Production main66 independently of this Test compiled at focused-main-private-v6; failed Test axiom print is error recovery and receives no proof credit.'],changed_route='Replace one deeply nested tuple elaboration by one constructor per existing existential/conjunction; preserve sealed private proposition and public caller header byte-for-byte.',source_mathematical_statement_changed=False,heartbeat_budget_increased=False,next_build='focused-both-staged-v10',mathematical_progress_claim=False),indent=2)+'\n',encoding='utf-8',newline='\n')
adv.checkpoint_advance('ASTIS-SA-20261009-PBPSAmbientAdjointCorrector',worker_id='companion_root_20261005',route_fingerprint='same-actual-global-consumer/staged-existing-witness-constructors',progress_signature='production-compiled-Test-outer-constructor-timeout-localized',mathematical_delta='Actual ambient adjoint main compiled; no Test closure credit. Operator/global-input typing and residual identity passed before outer reconstruction.',exact_residual='Compile the genuine global corrector consumer by changing reconstruction elaboration; independent math/source and publication remain pending.')
print('Retained three exact negative checks and strict localized residual; staged constructor route, unchanged mathematical statement.')
