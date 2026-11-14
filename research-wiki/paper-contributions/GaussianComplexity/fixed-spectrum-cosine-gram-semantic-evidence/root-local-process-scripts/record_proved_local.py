"""One normal local-proof checkpoint; no source verification or stabilization."""
from pathlib import Path
import gzip, hashlib, json, os, subprocess, sys

if sys.flags.optimize != 0 or os.environ.get('PYTHONOPTIMIZE') != '0':
    raise RuntimeError('Explicit PYTHONOPTIMIZE=0 and active assertions required')
sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as adv
import astis_publication as pub

W = Path(__file__).parent
E = Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-cosine-gram.json')
L = Path('runs/substantive_advances.jsonl')
ADV = 'ASTIS-SA-20261110-GaussianComplexityFixedSpectrumCosineGram'
OWNER = 'huanjian_gc_20261110_fixed_spectrum_cosine_gram'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()

def put(p, data):
    with p.open('xb') as f:
        f.write(data)

assert not (W/'PROVED_LOCAL-attempted.once.json').exists(), 'Never replay an uncertain normal transition'
base = json.loads((W/'preproof-baseline.private.json').read_bytes())
protected = json.loads((W/'intake-tracked-private-preservation.json').read_bytes())
controls = json.loads((W/'intake-baseline.private.json').read_bytes())
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == base['head']

def preserve():
    for p, h in protected['all_tracked_hashes_except_own_ledger_and_frontier'].items():
        assert sha(Path(p).read_bytes()) == h, p
    for p, h in base['all_existing_frontier_hashes'].items():
        assert sha(Path(p).read_bytes()) == h, p
    for p, h in controls['foreign_control_hashes'].items():
        assert sha(Path(p).read_bytes()) == h, p

preserve()
seal_raw = (W/'statement-seal-v1.json').read_bytes()
assert sha(seal_raw) == 'a5e464a34ee276e62267d21f0965c1a0b1ef905bed27e679a85ecee3cd7fd45c'
assert Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-cosine-gram-statement-seal.json').read_bytes() == seal_raw
s = json.loads(seal_raw)
k = json.loads((E/'actual-kernel-owned-inventory.json').read_bytes())
p = Path(s['producer']['planned_file'])
t = Path(s['actual_private_consumer']['planned_file'])
name = s['producer']['name']
assert sha(p.read_bytes()) == k['actual_producer_sha256'] == '88f29461fcac1825675e417a1bc3f3952404f1cd08183d6e484162aefe9f5d54'
assert sha(t.read_bytes()) == k['actual_Test_sha256'] == '90b43f488d3fe9b6c95d4c039d0f771ee5bfecdd699b72dfa52465643f0b0dee'
assert k['both_exact_sealed_types_kernel_applied'] and k['all_owned_reachable']
assert (k['actual_owned_declarations'], k['handwritten'], k['generated_auxiliaries']) == (26, 2, 24)
parents = k['actual_first_public_ASTIS_parents']
consumer_name = next(n for n in parents if n != name)
assert parents[name] == ['AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGridAlias.actual_midpoint_grid_cosine_alias']
assert consumer_name.startswith('_private.Tests.GaussianComplexityFixedSpectrumCosineGram.')
assert consumer_name.endswith('.actual_gaussian_gram_means') and parents[consumer_name] == [name]
checks = []
for stem in [
    '20261110T153832124572Z-cosine-gram-producer-v4-native',
    '20261110T155836447467Z-cosine-gram-complete-producer-consumer-native',
    '20261110T155942501800Z-cosine-gram-actual-kernel-exact-types-all-owned',
]:
    rp = Path('.astis/huanjian-resume-20261103')/(stem+'.receipt.json')
    x = json.loads(rp.read_bytes())
    assert x['exit_code'] == 0 and sha(Path(x['log']).read_bytes()) == x['log_sha256']
    checks.append({'receipt': str(rp), 'receipt_sha256': sha(rp.read_bytes()),
                   'actual_log_sha256': x['log_sha256'], 'actual_HEAD': x['head_before'],
                   'scope': 'Actual current mathematical working bytes. Independent fresh compile at an immutable candidate remains separate.'})
for n in ['independent-preproof-source-topology-archive.json', 'actual-local-checks-lossless-archive.json', 'non-authoritative-source-attempt-c63b08.archive-manifest.json']:
    x = json.loads((E/n).read_bytes())
    assert sha(Path(x['archive']).read_bytes()) == x['sha256']
mirror = json.loads((E/'postproof-conceptual-mirror-audit.json').read_bytes())
assert mirror['status'] == 'none-found' and mirror['discovery_ids'] == []
ma = {'status': 'none-found', 'discovery_ids': [], 'evidence': str(E/'postproof-conceptual-mirror-audit.json')}
pub.check_advance([name], reviewed=False)
record = json.loads((E/'publication-draft-record.json').read_bytes())
boundary = json.loads(Path('website/content/declaration_lessons/huanjian-fixed-spectrum-cosine-gram.json').read_bytes())['units'][0]['boundary']
before = L.read_bytes()
states = adv._replay_advances([json.loads(z) for z in before.splitlines()])
assert states[ADV]['state'] == 'EXPLORING' and states[ADV]['owner_id'] == OWNER
assert {a: x for a, x in states.items() if a != ADV} == protected['all_foreign_states']
cellraw = C.read_bytes()
assert json.loads(cellraw)['owner_id'] == OWNER
evidence = {
    'result_kind': 'theorem-edge', 'theorem_delta': s['producer']['signature'],
    'lean_files': [str(p), str(t)], 'lean_declarations': [name],
    'publication_declarations': [name], 'focused_checks': checks,
    'truth_boundary': boundary, 'conceptual_mirror_audit': ma,
    'actual_consumer': 'The actual private identity-covariance Gaussian on EuclideanSpace (Fin d × Fin (q+1)) has internally derived coordinate-product L1, and computes both actual Gram-entry means using the producer. This is feature randomness, not the inverse-precision target law. No Gram, moment, independence, integrability or normalization certificate is a binder.',
    'actual_ASTIS_parents': parents, 'source_VERIFIED_or_global': False,
}
fd = os.open(W/'PROVED_LOCAL-attempted.once.json', os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, 'wb') as f:
    f.write(dump({'advance_id': ADV, 'ledger_prefix_sha256': sha(before), 'action': 'Exactly one normal PROVED_LOCAL invocation. Inspect actual ledger after interruption; never replay.'}))
adv.transition_advance(ADV, 'PROVED_LOCAL', worker_id=OWNER, evidence=evidence)
after = L.read_bytes()
assert after.startswith(before)
app = after[len(before):]
assert len(app.splitlines()) == 1
put(E/'actual-PROVED_LOCAL-append.exact.jsonl', app)
put(E/'frontier-before-PROVED_LOCAL.raw.json.gz', gzip.compress(cellraw, mtime=0))
new = adv._replay_advances([json.loads(z) for z in after.splitlines()])
assert new[ADV]['state'] == 'PROVED_LOCAL'
assert {a: x for a, x in new.items() if a != ADV} == protected['all_foreign_states']
preserve()
capsule = {
    'state': 'PROVED_LOCAL_NOT_SOURCE_VERIFIED', 'advance_id': ADV, 'owner': OWNER,
    'normal_PROVED_LOCAL_API_calls': 1, 'append_sha256': sha(app),
    'foreign_states_preserved': len(protected['all_foreign_states']),
    'foreign_frontiers_preserved': len(base['all_existing_frontier_hashes']),
    'protected_tracked_files_preserved': len(protected['all_tracked_hashes_except_own_ledger_and_frontier']),
    'foreign_control_files_preserved': len(controls['foreign_control_hashes']),
    'producer': {'file': str(p), 'sha256': sha(p.read_bytes()), 'declaration': name, 'actual_ASTIS_parents': parents[name]},
    'private_consumer': {'file': str(t), 'sha256': sha(t.read_bytes()), 'declaration': consumer_name, 'actual_ASTIS_parents': parents[consumer_name], 'source_Anchor': False, 'Registry_node': False},
    'actual_checks': checks, 'both_exact_sealed_types_kernel_applied': True,
    'actual_owned_declarations': 26, 'handwritten_roots': 2, 'generated_certificates': 24,
    'generated_certificates_are_not_new_mathematical_results': True,
    'all_reachable': True, 'recursive_axioms': 'standard3 only',
    'binding_sha256': record['publication_binding_sha256'],
    'source_to_lean_map': str(E/'source-to-lean-map-v1.json'),
    'conceptual_mirror_audit': ma, 'truth_boundary': boundary,
    'independent_source_native_reader_V_global_purification_Goal_pending': True,
}
put(E/'local-proof-capsule.json', dump(capsule))
c = json.loads(cellraw)
c['status'] = 'proved_locally'
c['conceptual_mirror_audit'] = ma
c['evidence'].update({
    'focused_checks': [z['receipt'] for z in checks],
    'local_proof_capsule': str(E/'local-proof-capsule.json'),
    'publication_binding_sha256': record['publication_binding_sha256'],
    'actual_compiled_ASTIS_parents': parents,
    'source_to_lean_map': str(E/'source-to-lean-map-v1.json'),
    'source_review': 'Fresh source role raw-first freeze complete; selective type/definition review in progress. Previous scope-breached attempt retained as non-authoritative, no SourceV.',
    'execution_boundary': boundary,
})
c['statement_seal']['status'] = 'EXACT_UNCHANGED_SEALED_TYPES_COMPILED;QUALIFIED_PROSPECTIVE_SOURCE_TOPOLOGY_ADMISSION_RETAINED;INDEPENDENT_POSTPROOF_REVIEW_PENDING'
c['learning_contract']['reader_backpressure']['assumptions_preserved'] = True
c['learning_contract']['reader_backpressure']['boundary_preserved'] = True
c['learning_contract']['failure_class'] = 'IMPLEMENTATION_FAILED'
c['learning_contract']['salvage'] = {
    'required': True, 'status': 'completed',
    'reason': 'Actual import, coercion, finite-sum orientation, transpose-entry and vector-mean diagnoses retained with all failed raw attempts and unchanged sealed statements. Both roots compile and all26 owned declarations are reachable;24 generated tactic certificates grant no extra mathematical credit. Exact process failures and retired source-review attempt are preserved without sourceV, mathematical-refutation or postmerge PURIFIED claims.',
    'promoted_fragments': [], 'discarded_fragments': [],
}
C.write_bytes(dump(c))
print(json.dumps({'state': 'PROVED_LOCAL', 'append_sha256': sha(app), 'sourceV': False, 'global': False,
                  'foreign_states': len(protected['all_foreign_states']),
                  'foreign_frontiers': len(base['all_existing_frontier_hashes']),
                  'tracked_files': len(protected['all_tracked_hashes_except_own_ledger_and_frontier']),
                  'foreign_control_files': len(controls['foreign_control_hashes'])}))
