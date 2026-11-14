from pathlib import Path
import hashlib, json, subprocess, sys
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
rp = Path('.astis/huanjian-resume-20261103/20261110T193357904072Z-krylov-range-normal-intake-exact-independent-qualified-grant.receipt.json')
r = json.loads(rp.read_bytes())
assert r['exit_code'] == 0 and sha(Path(r['log']).read_bytes()) == r['log_sha256']
pre = json.loads((W/'preproof-baseline.private.json').read_bytes())
control = json.loads((W/'intake-baseline.private.json').read_bytes())
assert subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip() == pre['head']
now = L.read_bytes()
old = now[:pre['ledger_bytes']]
assert sha(old) == pre['ledger_sha256']
app = now[len(old):]
assert app == (E/'normal-EXPLORING-append.exact.jsonl').read_bytes()
assert sha(app) == 'aae0ba7001b2d78f4d3816e0a174bfccb1e930bd29cacf69a9e66ed844f90cc0'
rows = [json.loads(z) for z in app.splitlines()]
assert len(rows) == 3 and all(z['advance_id'] == ADV for z in rows)
states = adv._replay_advances([json.loads(z) for z in now.splitlines()])
assert states[ADV]['state'] == 'EXPLORING' and states[ADV]['owner_id'] == OWNER
assert {a: x for a,x in states.items() if a != ADV} == pre['all_foreign_states']
for p,h in pre['all_tracked_regular_file_hashes'].items():
    if p != str(L):
        assert sha(Path(p).read_bytes()) == h, p
for p,h in pre['all_existing_frontier_hashes'].items():
    assert sha(Path(p).read_bytes()) == h, p
for p,h in control['foreign_control_hashes'].items():
    assert sha(Path(p).read_bytes()) == h, p
c = json.loads(C.read_bytes())
assert c['owner_id'] == OWNER and c['status'] == 'claimed'
assert c['statement_seal']['sha256'] == 'f47e23a601d1a8e0ff4760224676313e0f1999877a97156841a65c01847e5d82'
assert c['truth_boundary'] == states[ADV]['truth_boundary']
assert c['evidence']['preproof_source_admission']['sha256'] == 'de404e2102d7cf74ef9462a3677bd81aa6e0398d529b9ee25f0059394743fe13'
assert sha((E/'preproof-source-admission.json').read_bytes()) == 'de404e2102d7cf74ef9462a3677bd81aa6e0398d529b9ee25f0059394743fe13'
assert not c['learning_contract']['reader_backpressure']['assumptions_preserved']
for p in ['AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumKrylovRange.lean', 'Tests/GaussianComplexityFixedSpectrumKrylovRange.lean', str(W/'StatementFormation.lean')]:
    assert not Path(p).exists(), p
out = {'actual_state': 'EXPLORING', 'root_actual_readback_after_real_intake_and_all_postguards': True,
       'normal_API_calls_completed_once': 3, 'actual_append_sha256': sha(app),
       'actual_intake_receipt_sha256': sha(rp.read_bytes()), 'actual_intake_log_sha256': r['log_sha256'],
       'all299_foreign_states_and_latest_evidence_unchanged': True,
       'all459_old_frontier_files_unchanged': True, 'all128850_other_tracked_regular_files_unchanged': True,
       'all927_foreign_control_files_unchanged': True,
       'target_formal_proof_API_may_begin_only_NOW': True,
       'target_proof_or_sourceV_or_global_credit': False,
       'same_goal_original_global_lease_and_all12_prior_sourceV_values_preserved': True}
with (W/'root-confirmed-actual-intake-success.json').open('x') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(json.dumps(out))
