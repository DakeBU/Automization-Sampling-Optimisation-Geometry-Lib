"""Continue the same R9 SAU after its shared dependency's real independent V.

No new intake, no statement change, no ledger transition and no shared reset.
"""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
T=Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean')
P=Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixVariance.lean')
sha=lambda raw:hashlib.sha256(raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    with p.open('xb') as f:f.write(raw)
head=git('rev-parse','HEAD').decode().strip()
assert head=='6819e686116e6f18df3ef0e638c6ca24bde7dd8d'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
raw=Path('runs/substantive_advances.jsonl').read_bytes()
states=advance._replay_advances([json.loads(x) for x in raw.splitlines()])
target='ASTIS-SA-20261112-GaussianComplexitySourceMatrixVariance'
assert states[target]['state']=='EXPLORING'
assert states['ASTIS-SA-20261112-RealMatrixPositiveIntegral']['state']=='VERIFIED'
events=[json.loads(x) for x in raw.splitlines() if json.loads(x).get('advance_id')==target]
assert len(events)==3 and [e.get('state',e.get('to_state')) for e in events]==['PROPOSED','CLAIMED','EXPLORING']
seal_path=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-statement-seal.json')
seal_raw=seal_path.read_bytes()
assert sha(seal_raw)=='5f905cafe6035238cebdedd4f841e87b703e741b4c8aa204471d89e4c07e8a14'
assert sha(P.read_bytes())=='d9db32e38f18f1f92a94c82886063181375a9e214f7d44ce1bca2a240586ace6'
assert not T.exists()
cell_raw=C.read_bytes(); cell=json.loads(cell_raw)
assert cell['status']=='claimed' and cell['owner_id']=='huanjian_gc_20261112_source_matrix_variance'
assert sha((W/'consumer-signature.original.txt').read_bytes())=='95e81a02e5302de9a42e3b60038ffad6195315ac2eca99a4e6abb39978609f7e'
baseline={
    'kind':'Versioned continuation guard after actual independent shared V; not a replacement preproof baseline',
    'head':head,'ledger_bytes':len(raw),'ledger_sha256':sha(raw),
    'original_R9_preproof_baseline_sha256':sha((W/'preproof-baseline.private.json').read_bytes()),
    'original_source_statement_seal_sha256':sha(seal_raw),
    'all_foreign_states':{k:v for k,v in states.items() if k!=target},
    'all_existing_frontier_hashes':{str(p):sha(p.read_bytes()) for p in sorted(C.parent.iterdir()) if p.is_file() and not p.is_symlink() and p!=C},
    'tracked_git_index':git('ls-files','--stage').decode(),
    'own_active_cell_before_final_consumer_sha256':sha(cell_raw),
    'authorized_history':'Original R9 intake remains exactly3; its public P became a real compiled/source/native-reviewed consumer during the distinct S shared cycle. S has one actual independent V, all original failed metadata phases and source/native limits preserved. Now continue the already sealed private T only.',
    'source_and_actual_math_signatures_unchanged':True,
    'private_data_not_for_export':True}
create(W/'continuation-after-shared-VERIFIED.private.json',dump(baseline))
disc=Path('runs/substantive_discoveries.jsonl').read_bytes()
create(W/'continuation-discoveries.private.json',dump({'ledger_sha256':sha(disc),'full_states':advance._replay_discoveries([json.loads(x) for x in disc.splitlines()])}))
create(W/'active-cell-before-final-consumer.original.json',cell_raw)
source=(W/'CenteredVarianceDraft.lean').read_text()
assert source.count('convert h using 1 <;> abel')==2
source=source.replace('convert h using 1 <;> abel','convert h using 1; abel')
note='''/-! Actual original-experiment centered and deterministic cosine-weighted
matrix variance bounds, arXiv2610.20492v1 C.2 Ex118/120. This private consumer
materially uses the canonical public uncentered producer, actual first moments
and shared real PSD-integral node. Both product integrals are justified without
matrix commutativity; real CFC yields the actual L2 operator norms. No matrix
concentration, oracle reduction or main lower bound is claimed here. -/

'''
source=source.replace('noncomputable section\n',note+'noncomputable section\n',1)
signature=source.split('private theorem actual_source_centered_variance_bounds\n',1)[1].split(' := by\n',1)[0]
assert signature==(W/'consumer-signature.original.txt').read_text()
create(T,source.encode())
assert Path('runs/substantive_advances.jsonl').read_bytes()==raw
record={'continuation_HEAD':head,'same_existing_advance':target,'new_intake_calls':0,
    'new_ledger_transitions':0,'final_private_consumer':str(T),'final_file_sha256':sha(T.read_bytes()),
    'lines':len(source.splitlines()),'unchanged_signature_sha256':sha(signature.encode()),
    'draft_proof_change':'Only two unnecessary sequence-focus lint forms normalized; added precise module boundary comment. No theorem statement, assumption, source object or mathematical route change.',
    'foreign_full_states_preserved':len(baseline['all_foreign_states']),
    'prior_regular_frontiers_including_verified_S':len(baseline['all_existing_frontier_hashes']),
    'public_P_unchanged':True,'root_VERIFIED_calls':0}
create(W/'final-consumer-transfer-record.json',dump(record))
print(json.dumps(record))
