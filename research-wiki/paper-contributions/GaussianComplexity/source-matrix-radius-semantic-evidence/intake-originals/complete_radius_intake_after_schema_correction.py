"""Resume the prepared, source-admitted reservation after a project-label schema correction."""
from pathlib import Path
import hashlib
import json
import os
import stat
import subprocess
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
import astis_frontier_cells as frontiers
W=Path(__file__).resolve().parent.relative_to(Path.cwd())
E=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-semantic-evidence')
SP=Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-radius-statement-seal.json')
C=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-source-matrix-radius.json')
L=Path('runs/substantive_advances.jsonl')
ADV='ASTIS-SA-20261113-GaussianComplexitySourceMatrixRadius'
OWNER='huanjian_gc_20261113_source_matrix_radius'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
dump=lambda obj:(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode()
git=lambda *args:subprocess.check_output(['git',*args])
def create(p,raw):
    with p.open('xb') as f:f.write(raw)
def fingerprint(p):
    info=p.lstat()
    if stat.S_ISLNK(info.st_mode):return {'mode':stat.S_IMODE(info.st_mode),'kind':'symlink','target':os.readlink(p)}
    assert stat.S_ISREG(info.st_mode),str(p)
    return {'mode':stat.S_IMODE(info.st_mode),'kind':'regular','bytes':info.st_size,'sha256':sha(p.read_bytes())}
b=json.loads((W/'preproof-baseline.private.json').read_bytes())
assert git('rev-parse','HEAD').decode().strip()==b['head']=='505879e768e94f446bddd790d9330bf43ca2ea76'
assert not git('diff','HEAD','--name-only') and not git('diff','--cached','--name-only')
assert not (W/'normal-intake-attempted.once.json').exists()
before=L.read_bytes();assert sha(before)==b['ledger_sha256']
states=advance._replay_advances([json.loads(x) for x in before.splitlines()])
assert states==b['all_foreign_states'] and ADV not in states
assert git('ls-files','--stage','-z').decode()==b['tracked_git_index']
for name,h in b['all_existing_frontier_hashes'].items():assert sha(Path(name).read_bytes())==h,name
for name,fp in b['all_existing_tracked_fingerprints'].items():assert fingerprint(Path(name))==fp,name
for name,fp in b['actual_control_fingerprints'].items():assert fingerprint(Path(name))==fp,name
discovery=Path('runs/substantive_discoveries.jsonl').read_bytes()
assert sha(discovery)==json.loads((W/'preproof-discoveries.private.json').read_bytes())['ledger_sha256']
sealraw=SP.read_bytes();assert sha(sealraw)=='49d5fa00c9ae90d65878d955fab59d6a4bc03e942501677719881f3d26bf1a72'
seal=json.loads(sealraw);P,T=[seal[k]['planned_file'] for k in ['producer','actual_private_consumer']]
assert not Path(P).exists() and not Path(T).exists()
reviewraw=(E/'preproof-source-admission.json').read_bytes()
assert sha(reviewraw)=='1401d188fb352a3d2a768d11a2d79f484261195d658fff2d9f17b1fff2f9b514'
cell=json.loads(C.read_bytes());assert cell['status']=='claimed' and cell['evidence']['normal_API_calls']==0
errors=frontiers.validate_cells(frontiers.load_cells());assert not errors,errors
proposal=advance.AdvanceProposal(advance_id=ADV,task_id='ASTIS-SW-GAUSSIAN-COMPLEXITY-2026',
    goal='Prove actualpointwise truncatedYi norm<=2rL/d andactualmean norm<=2r/d; materiallyconsume both in literalcentered andcosineweighted radius<=2r(L+1)/d on the originalexperiment withonlyhq.',
    source_anchor=cell['source_anchor'],theorem_delta=seal['producer']['signature'],truth_boundary=seal['scope_boundary'],created_by=OWNER,
    dag_inputs=(cell['source_anchor'],'Actualpublicmean/frame/standardGaussiansecondmoment andrealMathliboperatornorm applicability; allnorm/mean/regularity/sign/cutoff/triangle/scalar estimates remaininternal, never sourcecertificatebinders.'),
    proposed_files=tuple(p for p in cell['owned_files'] if not p.endswith('/')),
    focused_checks=('lake env lean '+P,'lake build Tests.GaussianComplexityFixedSpectrumSourceMatrixRadius'),
    modes=('source-reading','proof-design','compiler-diagnosis'),priority=50,frontier_cell=C.stem,target_declarations=(seal['producer']['name'],))
proposal.validate()
create(W/'normal-intake-attempted.once.json',dump({'advance_id':ADV,'before_ledger_sha256':sha(before),'source_admission_sha256':sha(reviewraw),'no_replay':True}))
ev={'independent_topology':cell['evidence']['preproof_source_admission'],'statement_seal_sha256':sha(sealraw),'truth_boundary':seal['scope_boundary'],'formalizer_API_pristine':False}
advance.propose_advance(proposal)
advance.transition_advance(ADV,'CLAIMED',worker_id=OWNER,evidence=ev)
advance.transition_advance(ADV,'EXPLORING',worker_id=OWNER,evidence=ev)
after=L.read_bytes();assert after.startswith(before)
append=after[len(before):];events=[json.loads(x) for x in append.splitlines()]
assert len(events)==3 and all(x['advance_id']==ADV for x in events)
assert [x.get('state',x.get('to_state')) for x in events]==['PROPOSED','CLAIMED','EXPLORING']
now=advance._replay_advances([json.loads(x) for x in after.splitlines()])
assert now.pop(ADV)['state']=='EXPLORING' and now==states
assert git('ls-files','--stage','-z').decode()==b['tracked_git_index']
for name,fp in b['all_existing_tracked_fingerprints'].items():
    if name!=str(L):assert fingerprint(Path(name))==fp,name
for name,fp in b['actual_control_fingerprints'].items():
    if name!=str(L):assert fingerprint(Path(name))==fp,name
for name,h in b['all_existing_frontier_hashes'].items():assert sha(Path(name).read_bytes())==h,name
assert Path('runs/substantive_discoveries.jsonl').read_bytes()==discovery
cell['reservation_only']='Normalledger EXPLORING under namedowner; no targetproof yet.'
cell['evidence']['normal_API_calls']=3
C.write_bytes(dump(cell))
assert not frontiers.validate_cells(frontiers.load_cells())
create(E/'normal-EXPLORING-append.exact.jsonl',append)
summary={'state':'EXPLORING','actual_normal_API_calls':3,'append_sha256':sha(append),'baseline_commit':b['head'],
    'foreign_full_advances_preserved':len(states),'foreign_discoveries_preserved':43,
    'all_existing_regular_frontier_files_preserved':len(b['all_existing_frontier_hashes']),
    'all_existing_tracked_bytes_modes_index_preserved_except_exact_ledger_append':len(b['all_existing_tracked_fingerprints']),
    'actual_control_files_preserved':len(b['actual_control_fingerprints']),'target_formal_proof_calls':0,'root_VERIFIED_calls':0,
    'preproof_archive_sha256':sha((E/'independent-preproof-source.original-files.tar.gz').read_bytes()),'statement_seal_sha256':sha(sealraw),
    'prior_schema_failure_before_any_API_preserved':True}
create(E/'normal-intake-preservation.json',dump(summary))
assert set(git('diff','HEAD','--name-only').decode().splitlines())=={str(L)}
print(json.dumps(summary))
