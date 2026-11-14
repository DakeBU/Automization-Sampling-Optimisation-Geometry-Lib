"""One normal R9 local proof transition; public P and real private T kept distinct."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode = True
sys.path.insert(0,'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers
import astis_publication as publication
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
A = Path('research-wiki/semantic-roundtrip/audits/huanjian-gaussian-source-matrix-variance.json')
LEDGER = Path('runs/substantive_advances.jsonl')
ADV = 'ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance'
OWNER = 'huanjian_gc_20261112_source_matrix_variance'
MATH = 'e654e98642350a615c473bc8190fbc1d47fe52bd'
P = Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixVariance.lean')
T = Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean')
sha = lambda raw: hashlib.sha256(raw).hexdigest()
dump = lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git = lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    with p.open('xb') as out: out.write(raw)
head = git('rev-parse','HEAD').decode().strip()
b = json.loads((W/'continuation-after-S-schema-correction.private.json').read_bytes())
assert head == b['head']
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
before = LEDGER.read_bytes()
assert sha(before) == b['ledger_sha256']
states = advance._replay_advances([json.loads(x) for x in before.splitlines()])
assert states[ADV]['state'] == 'EXPLORING' and states[ADV]['owner_id'] == OWNER
assert {k:v for k,v in states.items() if k != ADV} == b['all_foreign_states']
for p,h in b['all_existing_frontier_hashes'].items(): assert sha(Path(p).read_bytes()) == h,p
discovery = Path('runs/substantive_discoveries.jsonl').read_bytes()
assert sha(discovery) == json.loads((W/'continuation-discoveries.private.json').read_bytes())['ledger_sha256']
assert git('show',f'{MATH}:{P}') == P.read_bytes()
assert git('show',f'{MATH}:{T}') == T.read_bytes()
assert sha(P.read_bytes()) == 'd9db32e38f18f1f92a94c82886063181375a9e214f7d44ce1bca2a240586ace6'
assert sha(T.read_bytes()) == 'c72d3573c6047b75983a958ad8b98de9c399e13277daa852a66c3e5a0820e73b'
sealpath = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-statement-seal.json')
assert sha(sealpath.read_bytes()) == '5f905cafe6035238cebdedd4f841e87b703e741b4c8aa204471d89e4c07e8a14'
seal = json.loads(sealpath.read_bytes())
math = json.loads((E/'full-variance-local-mathematical-result.json').read_bytes())
checks = [math['actual_final_build'],math['actual_final_proof_value_kernel']]
for x in checks:
    raw = Path(x['path']).read_bytes(); r = json.loads(raw)
    assert sha(raw) == x['sha256'] and r['exit_code'] == 0
    assert sha(Path(r['log']).read_bytes()) == x['log_sha256'] == r['log_sha256']
audit = json.loads(A.read_bytes())
assert audit['state'] == 'source-reviewed' and audit['source_review']['state'] == 'accepted'
assert audit['actual_math_commit'] == MATH and audit['reader_commit'] == '1d0dedf3aac3c2ff72ee96566461e29e38a2eeae'
name = audit['lean']['declaration']
publication.check_advance([name],reviewed=True)
assert not frontiers.validate_cells(frontiers.load_cells())
cell = json.loads(C.read_bytes())
assert cell['status'] == 'claimed' and cell['conceptual_mirror_audit']['status'] == 'none-found'
boundary = 'Actual original independent-column Gaussian experiment only; sole source condition2q+1<d and q0 retained. Public P is actual uncentered square-integrability/PSD bound. Private Test T materially consumes P and the actual mean provider to prove actual centered and cosine-weighted square integrability plus both true real L2 operator norm variance bounds. T is not a public API/main consumer. No bounded-summand radius, matrix Bernstein/concentration, full Lemma4.4, either main lower bound, oracle/TV/precision/cap/cost adaptation, serialized integration/publication, purification or wholeGoal credit.'
result = {
    'result_kind':'theorem-edge',
    'theorem_delta':seal['producer']['signature'],
    'lean_files':[str(P),str(T)],
    'lean_declarations':[name],'publication_declarations':[name],
    'focused_checks':checks,'truth_boundary':boundary,
    'mathematical_candidate':MATH,'source_review_metadata_commit':head,
    'reader_metadata_commit':audit['reader_commit'],
    'publication_binding_sha256':audit['publication_binding_sha256'],
    'actual_compiled_parent_edges':cell['reuse_plan']['reused_declarations'],
    'actual_material_consumer':{
        **math['actual_private_consumer'],
        'name':'_private.Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance.0.AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance.actual_source_centered_variance_bounds',
        'sealed_signature':seal['actual_private_consumer']['signature'],
        'actual_compiled_parent_edges':cell['reuse_plan']['actual_private_consumer_parents'],
        'private_implementation_only':True,'public_API_registry_credit':False,
        'source_decision':cell['evidence']['independent_source_review']['private_T_decision'],
        'anonymous_decoder_original_run_sha256':'12b1d9e3e5eac97c57ae70f0dee529d9b3eac68db7f90f1172b616f442ed463a',
    },
    'independent_source_review':cell['evidence']['independent_source_review'],
    'conceptual_mirror_audit':cell['conceptual_mirror_audit'],
    'owned_theorems':math['owned_math'],
    'kernel_type_check':'Actual final P/T proof bodies (not opaque constants) applied by the kernel to both unchanged complete sealed literal Props; both raw Expr equalities false but kernel conversion succeeds. All7 new owned declarations closed/reachable with standard three axioms; real q0 P/T applications compile.',
    'proof_iteration':{
        'failed_draft_versions_retained':True,
        'diagnosis':'Earlier draft sum-simp orientation and Bochner integral rewrite typing failed; typed local integrand equalities and actual probReal_univ provider close the same exact seal. No target premise or definition changed. Final actual206-line Test builds; final actual proof-value kernel probe passes.',
        'reader_v3a_blocker_retained':'Independent stale unimplemented scope text corrected, v3b original accepted; v3c stable mathematical/API scope increment accepted, unchanged whole code/decoders.',
        'source_transfer_failures_retained':'ROOT initially demanded zero deltas despite two informational independent elaborations; then encountered pre-existing S record string/object schema mismatch. Original failed scripts/receipts preserved; original S verifier metadata-only repair preserves normal V exactly. Neither is mathematical negative evidence.',
    },
    'formalizer_preseal_API_pristine':False,'preseal_exposure':seal['preseal_exposure'],
    'reader_boundary':cell['reader_contract']['status'],
}
create(W/'local-proof-transition-attempted.once.json',dump({'advance_id':ADV,'from_state':'EXPLORING','to_state':'PROVED_LOCAL','head':head,'actual_math_commit':MATH,'before_ledger_sha256':sha(before)}))
advance.transition_advance(ADV,'PROVED_LOCAL',worker_id=OWNER,evidence=result)
after = LEDGER.read_bytes()
assert after.startswith(before)
append = after[len(before):]
assert len(append.splitlines()) == 1
event = json.loads(append)
assert event['advance_id'] == ADV and event['worker_id'] == OWNER and event['to_state'] == 'PROVED_LOCAL'
assert event['evidence'] == result
now = advance._replay_advances([json.loads(x) for x in after.splitlines()])
assert now[ADV]['state'] == 'PROVED_LOCAL'
assert {k:v for k,v in now.items() if k != ADV} == b['all_foreign_states']
cell['status'] = 'proved_locally'
cell.pop('reservation_only',None)
cell['truth_boundary'] = boundary
cell['evidence']['focused_checks'] = checks
cell['evidence']['actual_PROVED_LOCAL_append_sha256'] = sha(append)
cell['evidence']['normal_API_calls'] = len([json.loads(x) for x in after.splitlines() if json.loads(x).get('advance_id') == ADV])
cell['statement_seal']['status'] = 'EXACT_UNCHANGED_P_T_TYPES_COMPILED;INDEPENDENT_SOURCE_ACCEPTED;NATIVE_READER_VERIFICATION_SEPARATE'
cell['learning_contract']['failure_class'] = 'IMPLEMENTATION_FAILED'
cell['learning_contract']['salvage'] = {'required':True,'status':'completed','reason':'All failed proof and metadata versions retained; no statement retired and no theorem fragment discarded. Final exact P/T full proofs and source reviews survive; schema correction changes evidence presentation only.','promoted_fragments':[name],'discarded_fragments':[]}
cell['learning_contract']['reader_backpressure']['assumptions_preserved'] = True
cell['reuse_plan']['known_consumers'] = ['Private actual206-line centered/weighted Test theorem; no public API/main-result credit.']
cell['reuse_plan']['searched_existing'][-1] = 'Completed actual API search: canonical real PSD expectation from shared S, real MatrixOrder/L2Operator CFC for true operator norm, both fixed-matrix Bochner integral rules and probability real mass. No caller-supplied norm/PSD/integrability certificate.'
C.write_bytes(dump(cell))
assert not frontiers.validate_cells(frontiers.load_cells())
create(E/'actual-PROVED_LOCAL-append.exact.jsonl',append)
create(E/'actual-PROVED_LOCAL-evidence.full.json',dump(result))
for p,h in b['all_existing_frontier_hashes'].items(): assert sha(Path(p).read_bytes()) == h,p
assert Path('runs/substantive_discoveries.jsonl').read_bytes() == discovery
assert set(git('diff','HEAD','--name-only').decode().splitlines()) == {str(C),str(LEDGER)}
print(json.dumps({'state':'PROVED_LOCAL','actual_math_commit':MATH,'source_metadata_commit':head,'append_sha256':sha(append),'full_original_payload_sha256':sha(dump(result)),'foreign_full_states_preserved':len(states)-1,'foreign_frontiers_preserved':len(b['all_existing_frontier_hashes']),'root_VERIFIED_calls':0}))
