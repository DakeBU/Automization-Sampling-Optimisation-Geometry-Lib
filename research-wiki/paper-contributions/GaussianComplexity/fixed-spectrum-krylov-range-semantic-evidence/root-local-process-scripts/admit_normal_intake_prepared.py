"""Prepared prospective control only; no execution before exact independent grant."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys

if sys.flags.optimize != 0 or os.environ.get('PYTHONOPTIMIZE') != '0':
    raise RuntimeError('Explicit PYTHONOPTIMIZE=0 and active assertions are required')
sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as adv

W = Path(__file__).parent
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-krylov-range.json')
L = Path('runs/substantive_advances.jsonl')
ADV = 'ASTIS-SA-20261110-GaussianComplexityFixedSpectrumKrylovRange'
OWNER = 'huanjian_gc_20261110_fixed_spectrum_krylov_range'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
def put(path, data):
    assert not path.exists(), path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
def ref(path):
    path = Path(path)
    data = path.read_bytes()
    return {'path':str(path),'bytes':len(data),'sha256':sha(data)}
def controls():
    import stat
    regular = lambda p: p.exists() and stat.S_ISREG(p.lstat().st_mode)
    names = {str(p) for p in Path('research-wiki/frontier-cells').rglob('*') if regular(p)}
    names |= {str(p) for p in Path('runs').iterdir() if regular(p)}
    names.add('website/content/samplewiki_companion_frontiers.json')
    for p in Path('.astis').iterdir():
        if regular(p) and any(t in p.name.lower() for t in ['queue','control','global','goal','steer','execution']):
            names.add(str(p))
    for n in ['control','queues','runtime','harness','state','locks']:
        d = Path('.astis')/n
        if d.is_dir() and not d.is_symlink():
            names |= {str(p) for p in d.rglob('*') if regular(p)}
    # Reuse only exact known older control PATHS. Never export their private values.
    known = json.loads(Path('.astis/huanjian-gc-fixed-spectrum-cosine-gram-20261110/intake-baseline.private.json').read_bytes())
    names |= set(known['foreign_control_hashes'])
    # Latest original sourceV portable paths only; never glob its PRIVATE sibling.
    root = Path('.astis/semantic-neutral-20261110/cg_src_7e41d9')
    manifest = root/'phase5-normal-sourceV-archive-manifest.json'
    m = json.loads(manifest.read_bytes())
    assert m['full_private_foreign_snapshots_included'] is False
    for x in m['files']:
        n = x['original_repo_path']
        assert 'private-phase5-preservation' not in n
        names.add(n)
    names |= {str(root/n) for n in ['phase5_package_execution.json','phase5_package_execution.stdout','phase5_package_execution.stderr','phase5-normal-sourceV-archive-manifest.json','phase5-normal-sourceV-all-portable-original-files.lossless-file-bytes.tar.gz']}
    own_roots = ['research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-semantic-evidence/']
    own_exact = {
        'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-statement-seal.json',
        'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumKrylovRange.lean',
        'Tests/GaussianComplexityFixedSpectrumKrylovRange.lean',
        'website/content/declaration_lessons/huanjian-fixed-spectrum-krylov-range.json',
        'website/content/publications/huanjian-fixed-spectrum-krylov-range.json',
        'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-krylov-range.json'}
    for raw in subprocess.check_output(['git','ls-files','--others','--exclude-standard','-z']).split(b'\0'):
        if not raw:
            continue
        n = raw.decode()
        if n not in own_exact and not any(n.startswith(p) for p in own_roots) and regular(Path(n)):
            names.add(n)
    # Nested repositories/directories/symlinks are not followed or hashed.
    return sorted(n for n in names if regular(Path(n)))

assert len(sys.argv) == 4, 'grant path, exact raw grant SHA256, exact private intake-baseline raw SHA256'
grantpath = Path(sys.argv[1])
assert sha(grantpath.read_bytes()) == sys.argv[2]
grant = json.loads(grantpath.read_bytes())
assert grant['prospective_target_Lean_proof_API_allowed_after_this_grant'] is True
assert grant['root_sole_mathematical_worker'] is True
assert grant['prepared_intake_script_sha256'] == sha(Path(__file__).read_bytes())
assert grant['private_baseline_sha256'] == sys.argv[3]
for row in grant['independent_inputs']:
    assert sha(Path(row['path']).read_bytes()) == row['sha256'], row['path']
baselinepath = W / 'intake-baseline.private.json'
assert sha(baselinepath.read_bytes()) == sys.argv[3]
b = json.loads(baselinepath.read_bytes())
prepath = Path(b['preproof_snapshot']['path'])
assert sha(prepath.read_bytes()) == b['preproof_snapshot']['sha256']
pre = json.loads(prepath.read_bytes())
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip() == pre['head']
sp = W / 'statement-seal-v1.json'
assert sha(sp.read_bytes()) == 'f47e23a601d1a8e0ff4760224676313e0f1999877a97156841a65c01847e5d82'
s = json.loads(sp.read_bytes())
prod = s['producer']['planned_file']
test = s['actual_private_consumer']['planned_file']
name = s['producer']['name']
assert not Path(prod).exists() and not Path(test).exists()
assert not (W/'StatementFormation.lean').exists()
publicseal = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-krylov-range-statement-seal.json')
assert publicseal.read_bytes() == sp.read_bytes()
assert sha(C.read_bytes()) == b['own_frontier']['sha256']
assert set(b['control_paths']) <= set(controls())
for path, h in b['foreign_control_hashes'].items():
    assert sha(Path(path).read_bytes()) == h, path
before = L.read_bytes()
assert sha(before) == pre['ledger_sha256'] and len(before) == pre['ledger_bytes']
states = adv._replay_advances([json.loads(z) for z in before.splitlines()])
assert states == pre['all_foreign_states'] and ADV not in states
assert states['ASTIS-SA-20261110-GaussianComplexityFixedSpectrumTargetLaw']['state'] == 'VERIFIED'
assert states['ASTIS-SA-20261110-GaussianComplexityZeroQuerySeparation']['state'] == 'VERIFIED'
assert states['ASTIS-SA-20261110-GaussianComplexityFixedSpectrumCosineGram']['state'] == 'VERIFIED'
tracked = [p.decode() for p in subprocess.check_output(['git','ls-files','-z']).split(b'\0') if p]
assert set(tracked) == set(pre['all_tracked_regular_file_hashes'])
for path, h in pre['all_tracked_regular_file_hashes'].items():
    assert sha(Path(path).read_bytes()) == h, path
for path, h in pre['all_existing_frontier_hashes'].items():
    assert sha(Path(path).read_bytes()) == h, path
assert json.loads(C.read_bytes())['owner_id'] == OWNER
put(E/'preproof-source-admission.json', grantpath.read_bytes())
put(W/'intake-tracked-private-preservation.json', dump({
    'all_tracked_hashes_except_own_ledger_and_frontier':{
        p:h for p,h in pre['all_tracked_regular_file_hashes'].items() if p not in {str(L),str(C)}},
    'all_foreign_states':states, 'raw_private_not_for_public_copy':True}))
cell = json.loads(C.read_bytes())
boundary = ('Prove the actual pointwise cosine-feature image=Krylov equality at source kappa>=2 '
    'and natural d,q with2q+1<d includingq0, materially consumed by actual Euclidean norm and '
    'signed weighted-inner coefficient identities for every actual Krylov vector. Unscaled source g; '
    'B alone has d^-1/2. No supplied polynomial/invertibility/normalization/rank/span/Gram/moment '
    'certificate. No concentration/absoluteC/C6/full Lemma4.4, Haar/joint/adaptive/measurable-choice/'
    'oracle/exact-matvec/precision/TV/dimension-condition-number/deterministic worst-query-cap/'
    'explicit expected-cost adapter, either full main bound, sourceV/global/site/browser/publication/'
    'purification/ExpositionSeal or Goal completion. All twelve prior original sourceV values and '
    'all other states/frontiers/queues/other ASTIS chat and current reader HOLDs are preserved; '
    'the original foreign global lease is not transferred.')
proposal = adv.AdvanceProposal(
    advance_id=ADV, task_id='ASTIS-SW-GAUSSIAN-COMPLEXITY-2026',
    goal='Prove the actual hard-family cosine-feature Krylov range, materially consumed by actual Euclidean energy coordinates.',
    source_anchor=cell['source_anchor'], theorem_delta=s['producer']['signature'],
    truth_boundary=boundary, created_by=OWNER,
    dag_inputs=('source:arXiv2610.20492v1 S4.SS1.p1; S4.SS2.SSS0.Px1.p2; A3.Thmtheorem5/A3.SS2.2 range and A3.SS2.p19 exact pointwise energy equalities',
        'Literal canonical finite-matrix/span/Euclidean definitions. General proof-API retrieval only after exact independent qualified admission; actual compiled parents remain unknown.'),
    proposed_files=(prod,test,str(C),str(publicseal),
        'website/content/declaration_lessons/huanjian-fixed-spectrum-krylov-range.json',
        'website/content/publications/huanjian-fixed-spectrum-krylov-range.json',
        'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-krylov-range.json'),
    focused_checks=('lake env lean '+prod,'lake build Tests.GaussianComplexityFixedSpectrumKrylovRange'),
    modes=('source-reading','proof-design','compiler-diagnosis'),priority=50,
    frontier_cell=C.stem,target_declarations=(name,))
proposal.validate()
fd = os.open(W/'normal-intake-attempted.once.json', os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
with os.fdopen(fd,'wb') as f:
    f.write(dump({'advance':ADV,'permanent_no_replay_marker':True,'proof_API_not_allowed_until_all3_events_and_postguards_pass':True}))
try:
    adv.propose_advance(proposal)
    adv.transition_advance(ADV,'CLAIMED',worker_id=OWNER,evidence={
        'exact_statement_seal':ref(sp),'preproof_admission':ref(E/'preproof-source-admission.json'),'truth_boundary':boundary})
    adv.transition_advance(ADV,'EXPLORING',worker_id=OWNER,evidence={
        'preproof_admission':ref(E/'preproof-source-admission.json'),
        'target_proof_API_search_starts_only_after_all_postguards':True,
        'preseal_planning_and_old_related_implementation_exposure_retained':True,
        'no_pristine_history_or_self_sourceV_claim':True,'no_own_STAB_authority':True,'truth_boundary':boundary})
except BaseException:
    observed = L.read_bytes()
    put(W/'normal-intake-failed-observed-ledger.PRIVATE.raw.jsonl', observed)
    put(W/'normal-intake-failed-no-replay.json',dump({'ledger_starts_with_original_prefix':observed.startswith(before),'normal_intake_attempted_once':True,'proof_API_authority':False,'next':'Readonly determine exact completed events and legal remaining recovery; never re-propose/reset/rewrite history.'}))
    raise
after = L.read_bytes()
assert after.startswith(before)
app = after[len(before):]
assert len(app.splitlines()) == 3
rows = [json.loads(z) for z in app.splitlines()]
assert all(z['advance_id']==ADV for z in rows)
new = adv._replay_advances([json.loads(z) for z in after.splitlines()])
assert new[ADV]['state']=='EXPLORING' and new[ADV]['owner_id']==OWNER
assert {k:v for k,v in new.items() if k!=ADV} == states
for path, h in pre['all_tracked_regular_file_hashes'].items():
    if path not in {str(L),str(C)}:
        assert sha(Path(path).read_bytes()) == h, path
for path, h in pre['all_existing_frontier_hashes'].items():
    assert sha(Path(path).read_bytes()) == h, path
assert set(b['control_paths']) <= set(controls())
for path, h in b['foreign_control_hashes'].items():
    assert sha(Path(path).read_bytes()) == h, path
assert sha(C.read_bytes())==b['own_frontier']['sha256']
cell['evidence']['preproof_source_admission'] = ref(E/'preproof-source-admission.json')
cell['evidence']['execution_boundary'] = 'EXPLORING only after exact qualified intake3events and preservation postguards. No proof or sourceV yet. '+boundary
cell['truth_boundary'] = boundary
C.write_bytes(dump(cell))
assert json.loads(C.read_bytes())['owner_id']==OWNER
put(E/'normal-EXPLORING-append.exact.jsonl',app)
put(E/'normal-intake-preservation.json',dump({'actual_normal_API_calls':3,'state':'EXPLORING',
    'advance_id':ADV,'owner':OWNER,'append_sha256':sha(app),'foreign_states_preserved':len(states),
    'foreign_frontiers_preserved':len(pre['all_existing_frontier_hashes']),
    'protected_tracked_files_preserved':len(pre['all_tracked_regular_file_hashes'])-1,
    'foreign_raw_private':True,'no_proof_or_sourceV_STAB_or_global_credit':True}))
print(json.dumps({'state':'EXPLORING','actual_normal_API_calls':3,'append_sha256':sha(app),
    'foreign_states_preserved':len(states),'foreign_frontiers_preserved':len(pre['all_existing_frontier_hashes']),
    'proof_or_sourceV_credit':False}))
