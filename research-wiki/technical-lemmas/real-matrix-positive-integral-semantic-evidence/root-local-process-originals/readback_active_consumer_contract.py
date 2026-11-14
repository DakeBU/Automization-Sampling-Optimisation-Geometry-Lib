"""Bring ROOT's own active R9 metadata up to already accepted P facts only."""
from pathlib import Path
import hashlib
import json
import subprocess
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence')
E22=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-variance.json')
sha=lambda raw:hashlib.sha256(raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    with p.open('xb') as f:f.write(raw)
head=git('rev-parse','HEAD').decode().strip()
assert head=='762ea453a3dea70136ff902a1cc1203baa8d283e'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
ledger=Path('runs/substantive_advances.jsonl').read_bytes()
b=json.loads((W/'candidate-boundary-v3.private.json').read_bytes())
for p,h in b['all_existing_frontier_hashes'].items():assert sha(Path(p).read_bytes())==h,p
before=C.read_bytes()
old_path=E22/'active-cell-before-accepted-P-contract-readback.original.json'
create(old_path,before)
cell=json.loads(before)
assert cell['status']=='claimed' and cell['owner_id']=='huanjian_gc_20261112_source_matrix_variance'
original_statement=cell['target_statement']
original_seal=cell['statement_seal'].copy()
concept_path=E/'conceptual-mirror-originals/GaussianComplexitySourceMatrixVariance.audit.json'
assert sha(concept_path.read_bytes())=='ac82492e34422b99a45c6dbc013e22f7ede04c3f800f1bcecc3dd0e884aac9e5'
concept=json.loads(concept_path.read_bytes())
assert concept['conceptual_mirror_audit']['status']=='none-found'
cell['conceptual_mirror_audit']={
    'status':'none-found','discovery_ids':[],
    'independent_reviewer':'/root/row_indep_source_graph_78c2',
    'evidence':str(concept_path),
    'boundary':'Original bounded per-SAU conceptual judgment only; existing mirror identities/status unchanged without revalidation, no compiler/source acceptance or new Lean implication.'}
cell['graph_contribution']['functor_view']='none-found'
cell['graph_contribution']['visual_review']='Public P actual four-parent edges independently kernel-extracted; public P production pages desktop/mobile accepted in bounded fixture. Globalgraph/source-index/site integration remains serialized and unaccepted. No final centered-T edge or source credit.'
cell['shared_floor_audit']['decision']='reuse_existing'
cell['shared_floor_audit']['canonical_declaration']='AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef'
cell['shared_floor_audit']['classification']='adapt'
cell['reuse_plan']['reused_declarations']=cell['evidence']['partial_public_producer_ASTIS_parents']
cell['reuse_plan']['new_shared_declarations']=[]
cell['reuse_plan']['decision_reason']+=' Current readback: the earlier requested shared node now exists in its own shared SAU and is actually called by P, so this caller reuses it. It does not claim the shared declaration as a new R9-owned node. Initial request records remain immutable.'
for key in ['source_ordered','source_statement_adjacent','natural_language_formula_proof','hidden_assumptions_visible','lean_collapsed','external_dependencies_visible']:
    cell['reader_contract'][key]=True
cell['reader_contract']['status']='For the public uncentered P binding only, independent source review and production desktop/mobile formula/fold/source/download acceptance passed. The full R9 centered/weighted final Tests consumer is not in this candidate and has no source/native/reader acceptance; source SAU remains EXPLORING.'
assert cell['target_statement']==original_statement and cell['statement_seal']==original_seal
C.write_bytes(dump(cell))
qualification={
    'kind':'Authorized current-contract readback on ROOT own active R9 cell, never another owner or a completed prior frontier',
    'path':str(C),'before_sha256':sha(before),'after_sha256':sha(C.read_bytes()),
    'exact_previous_bytes':str(old_path),'source_statement_and_seal_unchanged':True,
    'status_unchanged':'claimed','source_SAU_still_EXPLORING':True,
    'credit':'Only already source/native/reader accepted public uncentered P metadata and exact original independent per-SAU conceptual none-found. Full R9/finalT receives no credit.',
    'reason':'Initial reader/reuse/Functor pending fields must describe the actual current published P binding before final diff-aware contributor gates; do not add false contracts or shared-node ownership to make a checker pass.'}
record_path=E/'authorized-active-consumer-contract-readback.json'
create(record_path,dump(qualification))
b['all_existing_frontier_hashes'][str(C)]=sha(C.read_bytes())
b['qualification']['v3_boundary_preserved_sha256']=sha((W/'candidate-boundary-v3.private.json').read_bytes())
b['qualification']['current_active_consumer_contract_readback']=qualification
b['qualification']['only_authorized_active_consumer_cell_delta']['after_sha256']=sha(C.read_bytes())
b['qualification']['only_authorized_active_consumer_cell_delta']['changes']+=' Accepted P-only reader/reuse contracts and original per-SAU conceptual audit read back; no finalT or R9 completion credit.'
create(W/'candidate-boundary-v4.private.json',dump(b))
assert Path('runs/substantive_advances.jsonl').read_bytes()==ledger
paths=[C,old_path,record_path]
subprocess.run(['git','add','-f','--',*map(str,paths)],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(map(str,paths))
subprocess.run(['git','diff','--cached','--check'],check=True)
subprocess.run(['git','commit','--quiet','-m','Read back accepted uncentered consumer contracts without closing source variance SAU'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
assert not git('diff','HEAD','--name-only')
create(W/'actual-active-consumer-contract-readback-commit.json',dump({'commit':commit,'parent':head,**qualification}))
print(json.dumps({'commit':commit,'R9_status':'claimed/EXPLORING','T_credit':False,'ledger_changed':False,'other468_prior_frontiers_preserved':True}))
