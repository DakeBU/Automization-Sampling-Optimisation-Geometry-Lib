"""Commit the exact normal PL append and bounded original evidence, no new API call."""
from pathlib import Path
import hashlib, json, subprocess, sys
sys.path.insert(0, 'tools')
import astis_advance as advance
W = Path(__file__).resolve().parent.relative_to(Path.cwd())
E = Path('research-wiki/technical-lemmas/matrix-bernstein-exponential-semantic-evidence')
C = Path('research-wiki/frontier-cells/ASTIS-SHARED-MATRIX-BERNSTEIN-EXPONENTIAL-QUADRATIC.json')
L = Path('runs/substantive_advances.jsonl')
N = Path('.astis/semantic-neutral-20261114/bernstein_exp_native_72c4')
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda o: (json.dumps(o, ensure_ascii=False, indent=2) + '\n').encode()
git = lambda *a: subprocess.check_output(['git', *a])
def create(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b)
head = git('rev-parse', 'HEAD').decode().strip()
cfg = json.loads((W / 'normal-PL-inputs.json').read_bytes())
assert head == cfg['metadata_commit']
assert not git('diff', '--cached', '--name-only')
assert set(git('diff', 'HEAD', '--name-only').decode().splitlines()) == {str(C), str(L)}
events = [json.loads(x) for x in L.read_bytes().splitlines()]
state = advance._replay_advances(events)['ASTIS-SA-20261114-MatrixBernsteinExponentialQuadratic']
assert state['state'] == 'PROVED_LOCAL' and state['owner_id'] == 'huanjian_20261114_matrix_bernstein_exponential'
owned = [e for e in events if e['advance_id'] == 'ASTIS-SA-20261114-MatrixBernsteinExponentialQuadratic']
assert len(owned) == 4 and owned[-1]['to_state'] == 'PROVED_LOCAL'
for x in cfg['frozen_inputs']:
    assert sha(Path(x['path']).read_bytes()) == x['sha256']
dest = E / 'normal-PL-root-originals'
for name in ['record_bernstein_proved_local.py', 'record_bernstein_proved_local.static-preflight-v1.original.py',
             'record_bernstein_proved_local.static-preflight-v2.original.py',
             'normal-PL-inputs.static-preflight-v2.original.json',
             'normalPL-static-preflight.v1.original.json', 'normalPL-static-preflight-v1.diagnosis.json',
             'normalPL-final-preflight.v2.json.original', 'normalPL-final-preflight.v3.READY.json.original',
             'normalPL-static-preflight-v2.diagnosis.json',
             'normal-PL-inputs.json', 'normal-PROVED_LOCAL-attempted.once.json',
             'browser-v2-original.exec-tool-result.json', 'ROOT-v3-actual-PNG-observations.json',
             'carry_bernstein_proved_local.py']:
    create(dest / name, (W / name).read_bytes())
helper = Path('.astis/semantic-neutral-20261114/bernstein_pl_input_refs_45be/assemble_normal_pl_inputs.py')
assert sha(helper.read_bytes()) == 'b3e9e8186828191f018f1cf6a6cd4d159e7e339727931fcbd4dc5495b2ba20fb'
create(dest / 'assemble_normal_pl_inputs.original.py', helper.read_bytes())
R = Path('.astis/huanjian-resume-20261103')
actual = []
for rp in sorted(R.glob('*matrix-bernstein-normal-PROVED_LOCAL-*.receipt.json')):
    r = json.loads(rp.read_bytes())
    assert r['exit_code'] == 0 and sha(Path(r['log']).read_bytes()) == r['log_sha256']
    for p in [rp, Path(r['log'])]:
        create(dest / 'actual-runs' / p.name, p.read_bytes())
    actual.append(str(rp))
assert len(actual) == 1
for name in ['native-mathematics-report.v1.json', 'actual-canonical-parent-supplement.v1.json']:
    create(E / 'native-prePL' / name, (N / name).read_bytes())
reader = cfg['reader']
for section in ['original', 'isolated_candidate', 'graph_zoom_supplement']:
    refs = reader[section]
    for key in ['actual_checks', 'process_receipt', 'contract', 'wrapper']:
        p = Path(refs[key]['path'])
        assert sha(p.read_bytes()) == refs[key]['sha256']
        target = E / 'native-prePL' / p.relative_to(N)
        if target.exists():
            assert target.read_bytes() == p.read_bytes()
        else:
            create(target, p.read_bytes())
    receipt = json.loads(Path(refs['process_receipt']['path']).read_bytes())
    for stream in ['stdout', 'stderr']:
        x = receipt[stream]
        p = N / x['path']
        assert sha(p.read_bytes()) == x['sha256']
        create(E / 'native-prePL' / p.relative_to(N), p.read_bytes())
review = Path(reader['independent_runtime_review']['artifact']['path'])
carried_review = E / 'source-review/bernstein_exp_fresh_61a9/runtime/independent-runtime-review.final.json'
assert carried_review.read_bytes() == review.read_bytes()
memory = {'scope': 'One locally proved shared real matrix exponential packet with an actual private original-Gaussian MGF consumer; whole Goal unfinished.',
          'mathematical_candidate': '0ff1e2227b8e5a45a6a73906582ef042bd0d73ff',
          'reader_candidate': '9a8b163f4753a1329dbc0435c1e7f810f729c349',
          'current_state': 'PROVED_LOCAL; independent normalV and serialized integration pending',
          'actual_public_delta': 'A<=I, Hermitian real A and s>0 imply exp(sA)<=I+sA+(exp(s)-s-1)A²; negative eigenvalues unrestricted.',
          'actual_private_delta': 'Literal original product-Gaussian truncated/actually centered summand normalized by source rho; individual actual MGF comparison, sole hq and all s>0; q0 retained.',
          'proof_digestion': {'existing_substrate': 'Mathlib scalar integration/CFC/exp; existing canonical actual radius/centered structure and PSD integral.',
              'bookkeeping': 'Internal rho positivity, actual normalization and all measurability/integrability/PSD expectation adapters.',
              'new_reusable': 'One public canonical deterministic matrix exponential P.',
              'new_topology': 'Private authored actual-Gaussian single-summand MGF use; not a full Bernstein theorem or new public T node.'},
          'reader': 'Actual C2 responsive desktop/mobile, formula/source/download/table checks plus real existing-UI graph zoom/pan supplement independently accepted. Initial graph fit-scale remains small; shared reader overlay is unapplied.',
          'failures_preserved': 'All Lean/API iterations, native harness/inverse-codec errors, locator correction, v2 browser ENV/no page, original v3 actual reader FAIL, v3 candidate font FAIL, v4 unexecuted preparation, v5 pre-zoom visual HOLD and graph supplement.',
          'purification': 'pending; no main/publication/full-site/purified or whole-Goal completion claim',
          'next_mathematical_boundary': 'Source-required weighted individual MGF and actual Bernstein master/sum-tail background remain unimplemented; Lieb/master-tail and full C6/Lemma4.4/main lowerbounds/oracle/TV/precision/query-cap/cost are separate.',
          'integration': 'HOLD original shared stabilization owner; no takeover/reset/shared CSS/renderer/Registry/global graph/source-index/site writes.'}
create(E / 'local-cycle-memory.json', dump(memory))
tracked = set(git('ls-files', '-z').split(b'\0'))
paths = [C, L, *[p for p in sorted(E.rglob('*')) if p.is_file() and str(p).encode() not in tracked]]
spec = W / 'PROVED_LOCAL-carrier-paths.private.nul'
create(spec, b'\0'.join(str(p).encode() for p in paths) + b'\0')
subprocess.run(['git', 'add', '-f', '--pathspec-from-file=' + str(spec), '--pathspec-file-nul'], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == set(map(str, paths))
subprocess.run(['git', 'diff', '--cached', '--check', '--', str(C), str(L)], check=True)
subprocess.run(['git', 'commit', '--quiet', '-m', 'Record locally proved matrix exponential packet with independent source native and reader evidence'], check=True)
out = {'PROVED_LOCAL_carrier_commit': git('rev-parse', 'HEAD').decode().strip(),
       'normal_API_calls_in_this_carrier': 0, 'ROOT_VERIFIED_calls': 0,
       'metadata_gate_base': '19eaadc52297606595ee5095de95742d4e6394f0',
       'exact_owned_files': len(paths)}
create(W / 'actual-PROVED_LOCAL-carrier-commit.json', dump(out))
print(json.dumps(out))
