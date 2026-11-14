"""Freeze actual compiled P/T and all owned proof iterations, without advancing ledger."""
from pathlib import Path
import hashlib, json, subprocess

W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SHARED-MATRIX-BERNSTEIN-EXPONENTIAL-QUADRATIC.json')
P = Path('AutoSamplingTheory/TechnicalLemmas/Probability/MatrixBernsteinExponential.lean')
T = Path('Tests/GaussianComplexityBernsteinMgf.lean')
R = Path('.astis/huanjian-resume-20261103')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda o: (json.dumps(o, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *a: subprocess.check_output(['git', *a])

def create(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)

def no_private_payload(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in {'all_foreign_states', 'all_existing_frontier_hashes',
                     'all_existing_tracked_fingerprints', 'actual_control_fingerprints', 'full_states'}:
                assert isinstance(v, (int, bool)), k
            assert k != 'tracked_git_index', k
            no_private_payload(v)
    elif isinstance(o, list):
        for v in o:
            no_private_payload(v)

head = git('rev-parse', 'HEAD').decode().strip()
assert head == 'ba438e3085775662a027d68093f5864645566de7'
assert not git('diff', 'HEAD', '--name-only') and not git('diff', '--cached', '--name-only')
expected = {P: '7fc1996495b439c1b0aa53a3e69b6b4547952a42ee5f721834b6a1092430f6cc',
            T: '66bcf7750e8a70f6d69cea4bb08513f78364c3c3583862c119ffe4ff9cc9d883'}
sealraw = (W / 'statement-seal.unclaimed.v1.json').read_bytes()
assert sha(sealraw) == 'c3103a9e8d08fea6c83f35201fce953af4dd93e88a1a3d7d647fc4deaaddeb7a'
seal = json.loads(sealraw)
for (p, h), key in zip(expected.items(), ['producer', 'actual_private_consumer']):
    assert sha(p.read_bytes()) == h
    assert ' '.join(seal[key]['signature'].split()) in ' '.join(p.read_text().split())
dest = E / 'math-originals'
assert not dest.exists()
names = {'make_bernstein_kernel_probe.py', 'FinalBernsteinKernelProbe.lean',
         'DerivativeReproducer.v1.lean', 'write_actual_consumer.v1.py',
         'freeze_bernstein_math.py', 'freeze_bernstein_math.attempt1.original.py',
         'freeze-math-attempt1.diagnosis.json'}
selected = [p for p in sorted(W.iterdir()) if p.is_file() and
            (p.name.startswith(('P.', 'T.')) or p.name in names)]
for p in selected:
    assert '.private.' not in p.name
    if p.suffix == '.json':
        no_private_payload(json.loads(p.read_bytes()))
    create(dest / 'task-files' / p.name, p.read_bytes())
for p in expected:
    create(dest / ('final-' + p.name), p.read_bytes())
receipts = []
for rp in sorted(R.glob('*matrix-bernstein-*.receipt.json')):
    if 'freeze-actual-compiled-math-candidate' in rp.name and rp.name.startswith('20261113T172039346611Z') is False:
        continue  # Do not package this still-running carrier as completed evidence.
    r = json.loads(rp.read_bytes())
    if r['head_before'] != head:
        continue
    lp = Path(r['log'])
    assert sha(lp.read_bytes()) == r['log_sha256']
    for f in [rp, lp]:
        create(dest / 'actual-runs' / f.name, f.read_bytes())
    receipts.append({'file': str(dest / 'actual-runs' / rp.name), 'sha256': sha(rp.read_bytes()),
                     'command': r['command'], 'exit_code': r['exit_code'],
                     'log_sha256': r['log_sha256'], 'executed_HEAD': r['head_before']})
build = next(x for x in receipts if 'fifth-actual-Gaussian-MGF-explicit-integral-scalar-instantiations' in x['file'])
strict = next(x for x in receipts if 'actual-universal-P-T-values-sealed-kernel-owned-inventory-q0' in x['file'])
assert build['exit_code'] == strict['exit_code'] == 0
kernel = (R / '20261113T171903121371Z-matrix-bernstein-actual-universal-P-T-values-sealed-kernel-owned-inventory-q0.log').read_text()
assert kernel.count('ACTUAL_R13_ROOT_PROOF_VALUE_SEALED_KERNEL_APPLICATION_PASS') == 2
assert kernel.count('ACTUAL_R13_OWNED_TYPE_VALUE_KERNEL_PASS') == 26
assert 'ACTUAL_R13_ALL_NAMESPACE_OWNED_KERNEL_INSPECTED 26' in kernel
assert kernel.count('reachable=false') == 8
parents = [seal['producer']['name'],
           'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixRadius.actual_source_truncated_matrix_norm_bounds',
           'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixStructure.actual_source_centered_matrix_structure',
           'AutoSamplingTheory.TechnicalLemmas.Probability.RealMatrixPositiveIntegral.integral_posSemidef']
record = {
    'scope': 'Actual local real deterministic matrix exponential P and private original-Gaussian single-summand MGF T. Independent postproof native/semantic/reader admission pending; ledger remains EXPLORING.',
    'executed_base_HEAD': head,
    'source_files': [{'path': str(p), 'sha256': h, 'lines': len(p.read_text().splitlines())} for p, h in expected.items()],
    'actual_runs': receipts, 'actual_final_build': build, 'actual_final_proof_value_kernel': strict,
    'sealed_statement_sha256': sha(sealraw), 'canonical_P_parents': [], 'private_T_parents': parents,
    'kernel': {'full_universal_root_proof_values_at_literal_sealed_types': 2,
               'raw_literal_Expr_equalities': [False, False], 'kernel_definitional_conversion': 'passed',
               'all_namespace_owned_type_value_rechecks': 26, 'handwritten_declarations': 14,
               'generated_declarations': 12, 'all_handwritten_reachable': True,
               'unreachable_generated': 8, 'nonstandard_axioms': [],
               'actual_private_name': '_private.Tests.GaussianComplexityBernsteinMgf.0.AutoSamplingTheory.Tests.GaussianComplexityBernsteinMgf.actual_source_normalized_single_summand_mgf',
               'genuine_q0_universal_and_q0_d2_applications': True,
               'scope_limit': 'ROOT namespace-owned check only; independent full raw ModuleData/emission inventory still required.'},
    'no_new_source_binders': True,
    'iteration_qualification': 'Exact failed original sources, diagnoses and actual log/receipts preserved. Scalar derivative, CFC continuity, private consumer parser/API and integral-rewrite instantiation failures were implementation/API issues, not mathematical refutations. Last scalar-integral equations explicitly instantiated s and g to avoid definitionally reducing X into its internal rho scaling. Exact sealed P/T unchanged.',
    'definition_semantics': 'Standard real Euclidean L2Operator matrix norm and topology; matrix-algebra series exponential, not entrywise; original unconditional product standard Gaussian law and inclusive own-row cutoff; actual integral means; rho=2r(L+1)/d positive internally.',
    'placement': 'One public generic real deterministic component, one private original-Gaussian consumer; future cosine-weighted MGF route remains unimplemented. No public T/Registry credit.',
    'truth_boundary': 'No Bernstein sum tail or event probability, Lieb/master-tail/full C6/Lemma4.4/main lowerbounds, oracle/TV/precision/query-cap/cost, integration/publication/purification or whole-Goal credit.',
    'build_commit_qualification': 'Actual ROOT build and kernel ran at intake HEAD with the exact listed worktree source bytes. The future immutable math commit is not retroactively claimed to have been the executed build HEAD.'}
create(E / 'local-math-candidate.json', dump(record))
cell = json.loads(C.read_bytes())
cell['evidence']['local_math_candidate'] = {'file': str(E / 'local-math-candidate.json'),
    'sha256': sha(dump(record)), 'independent_native': 'pending', 'independent_semantic': 'pending'}
cell['evidence']['new_target_proof_calls_at_intake'] = cell['evidence'].pop('new_target_proof_calls')
cell['statement_seal']['status'] = 'EXACT_UNCHANGED_LITERAL_P_T_TYPES;LOCAL_FULL_BUILD_AND_PROOF_VALUE_KERNEL_PASSED;INDEPENDENT_POSTPROOF_REVIEW_PENDING'
cell['consumer_scope']['current_exact_consumer']['state'] = 'ACTUAL_PRIVATE_COMPILED;INDEPENDENT_NATIVE_AND_SEMANTIC_PENDING'
cell['consumer_scope']['compiled_consumer_credit'] = True
cell['reuse_plan']['actual_private_consumer_parents'] = parents
cell['reuse_plan']['known_consumers'] = [seal['actual_private_consumer']['name']]
cell['reuse_plan']['planned_consumers'] = [cell['consumers'][1]]
cell['reuse_plan']['decision_reason'] = 'One generic canonical exp bound has the actual privately compiled original-Gaussian unweighted MGF consumer; the distinct source-required cosine-weighted application remains explicitly future/unimplemented. Internal radius derivation uses existing public bounds; no extra public wrapper.'
cell['learning_contract']['salvage']['reason'] = 'All failed API/implementation source snapshots, diagnoses and actual receipts retained; scalar and CFC fragments are consumed by P and Gaussian support fragments by T. No discarded proof route is treated as a mathematical refutation.'
cell['reservation_only'] = 'Normal ledger remains EXPLORING; full actual local P/T compiled and literal sealed proof values rechecked. Independent native, semantic and reader admission pending.'
C.write_bytes(dump(cell))
paths = [P, T, C, E / 'local-math-candidate.json', *[p for p in sorted(dest.rglob('*')) if p.is_file()]]
spec = W / 'math-candidate-paths.private.nul'
create(spec, b'\0'.join(str(p).encode() for p in paths) + b'\0')
subprocess.run(['git', 'add', '-f', '--pathspec-from-file=' + str(spec), '--pathspec-file-nul'], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, paths))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(P), str(T), str(C)], check=True)
subprocess.run(['git', 'commit', '--quiet', '-m', 'Prove shared real matrix exponential bound and actual Gaussian single-summand MGF'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
for p in paths:
    assert git('show', f'{commit}:{p}') == p.read_bytes()
out = {'math_candidate_commit': commit, 'executed_base_HEAD': head, 'exact_owned_files': len(paths),
       'ledger_mutations': 0, 'ROOT_V_calls': 0, 'independent_postproof_acceptance': 'pending'}
create(W / 'actual-math-candidate-commit.json', dump(out))
print(json.dumps(out))
