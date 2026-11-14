"""Stage exact actor-selected reader originals; no discovery, Git or API mutation."""
from pathlib import Path
import json
import hashlib

R = Path('/Users/zhouhuanjian/ASTIS-GC')
E = R / 'research-wiki/technical-lemmas/matrix-bernstein-mgf-semantic-evidence'
OUT = E / 'reader-runtime-originals'
N = R / '.astis/semantic-neutral-20261114/weighted_mgf_native_8c2d/runtime'
S = R / '.astis/semantic-neutral-20261114/mgf_fresh_source_5b7e'
sha = lambda b: hashlib.sha256(b).hexdigest()
def emit(p, x):
    assert not p.exists(), p
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n')
def exact_copy(src, dst, expected):
    data = src.read_bytes()
    assert sha(data) == expected, src
    assert not dst.exists(), dst
    dst.write_bytes(data)
    return json.loads(data)
OUT.mkdir(exist_ok=False)
nm = exact_copy(N / 'runtime-selected-originals.manifest.v4.json', OUT / 'native-runtime-selected.manifest.v4.json', '14b588b9e458c4392c6c75b5ab166f53c5c561e50b3720d44ac9dd8887b1a93e')
rm = exact_copy(N / 'reader-replay-selected.manifest.v1.json', OUT / 'reader-replay-selected.original-manifest.v1.json', '87344012c377b92ff9795ca7a95890f3b0a5376e32bbda7180ad02bbe12ebea8')
sm = exact_copy(S / 'public-chosen-originals.manifest.phase5-through-final.json', OUT / 'fresh-reader-selected.manifest.phase5-through-final.json', 'fd5b9d90b028333f4f11e1247b53d47df3ea8689fec055fea03c9d1e30f513a1')
native = exact_copy(N / 'runtime-bounded-acceptance-report.v1.json', OUT / 'native-runtime-bounded-acceptance-report.v1.json', '11d5eb4ee723d00f80cf3bb86495ce2981337ee5f3f3bbff2520c455ebe1bf96')
verdict_path = 'phase12_final_native_visual/current-reader-independent-verdict.json'
verdict = exact_copy(S / verdict_path, OUT / 'fresh-current-reader-independent-verdict.json', '34b2134fe658637b075ce07632d17ec660458553d3c3263d489ad6b57b9e7aca')
assert verdict['verdict'] == 'ACCEPTED_SCOPED_EXACT_ISOLATED_READER_V2_ACTUAL_V4'
assert verdict['blocking_defects_within_tested_scope'] == []
assert str(N) == nm['root'] and str(S) == sm['source_base']
# Normalize only the actor-selected multi-root rows. Never enumerate a directory.
replay = []
for row in rm['files']:
    base = Path(rm['roots'][row['root']]['original_local_root'])
    logical = Path(row['path'])
    assert not logical.is_absolute() and '..' not in logical.parts
    p = base / logical
    rel = p.relative_to(R).as_posix()
    data = p.read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256']
    replay.append({'path': rel, 'bytes': len(data), 'sha256': sha(data),
        'actor_root': row['root'], 'actor_path': row['path']})
assert len({x['path'] for x in replay}) == len(replay) == 737
emit(OUT / 'reader-replay-normalized.manifest.v1.json', {
    'kind': 'ROOT normalization of exact independent multi-root leaf locators only',
    'source_base': str(R), 'original_manifest_sha256': '87344012c377b92ff9795ca7a95890f3b0a5376e32bbda7180ad02bbe12ebea8',
    'file_count': len(replay), 'files': replay,
    'no_directory_selection_or_original_bytes_changed': True})
actual = json.loads((N / 'browser-output-v4/candidate/actual-checks.json').read_text())
receipt = json.loads((N / 'browser-process-v4/candidate/process-receipt.json').read_text())
assert actual['status'] == 'PASS' and receipt['exit_code'] == 0 and receipt['exception'] is None
assert len(actual['checks']) == 343 and all(x['pass'] for x in actual['checks'])
assert sha((N / 'browser-output-v4/candidate/actual-checks.json').read_bytes()) == verdict['actual_raw_checks']['sha256']
assert sha((N / 'browser-process-v4/candidate/process-receipt.json').read_bytes()) == verdict['process_receipt_sha256']
emit(E / 'reader-current-acceptance.v1.json', {
    'status': 'ACCEPTED_ISOLATED_READER_ONLY',
    'mathematical_candidate': '4869db55d340cee39f0ba4d49fb0a7a4309ba2d6',
    'mathematical_and_authored_v2_metadata_bytes_changed_by_runtime_repairs': False,
    'reader_preview_manifest_sha256': 'c93f60d6b51a0da491bd748d54bdbc68fbdbc2f86653de5914539afb2aaee7d1',
    'actual_v4': {'exit_code': 0, 'failures': 0, 'checks': 343, 'screenshots': 86,
        'actual_checks_sha256': verdict['actual_raw_checks']['sha256'],
        'process_receipt_sha256': verdict['process_receipt_sha256'],
        'native_runtime_archive': 'reader-runtime-originals/native-runtime.selected.v1.tar.gz',
        'checks_member': 'browser-output-v4/candidate/actual-checks.json',
        'process_member': 'browser-process-v4/candidate/process-receipt.json',
        'actual_invoker': 'ROOT; actual exec session10914 completion chunk22d418',
        'script_and_contract_author_and_interpreter': 'Independent native actor gaussian_push_audit_c7b1 / weighted_mgf_native_8c2d'},
    'independent_visual_review': {'accepted': True, 'actor': 'mgf_fresh_source_5b7e',
        'personally_viewed_PNGs': verdict['personally_viewed_PNGs'],
        'archive': 'reader-runtime-originals/fresh-reader-review.selected.v1.tar.gz',
        'report_member': 'phase12_final_native_visual/final-reader-v4-independent-review.md',
        'report_sha256': verdict['report_sha256'],
        'verdict_member': verdict_path, 'verdict_sha256': '34b2134fe658637b075ce07632d17ec660458553d3c3263d489ad6b57b9e7aca'},
    'tested_scope': 'Exact responsive Chrome desktop1440x1000/mobile390x844 fixture; main/formula rendering, initially folded proofs/code, six P/P/P/T/T/T source/copy/full-download actions, full280 source lines, anchors, actual last-glyph scroll/header geometry, source-index and bounded graph/parent navigation.',
    'graph_boundary': verdict['qualified_graph_route'],
    'preserved_failures': ['v1 real Chrome reporter KeyError with original24 PNGs and no reconstructed flags',
        'v2 original renderer162checks/15failures and candidate228checks/12anchor failures',
        'v3 actual343checks/8LF measurement failures/86PNG; all original flags remain unchanged'],
    'excluded_claims': ['production/shared renderer, CSS, global graph or website acceptance',
        'default-fit or complete SVG-label readability', 'physical phone/touch testing',
        'runtime rendering of all step_source attribution metadata', 'post-V status pixels',
        'a build at metadata/public export identities', 'full Bernstein/C6/main bounds, purification or whole-Goal completion'],
    'normal_proof_V_at_this_snapshot': 0,
    'portable_custody': 'Actor-selected originals are later ROOT lossless containers with explicit manifests; no new review is created by packaging.'})
print(json.dumps({'prepared_exact_native_leaves': len(nm['files']), 'prepared_reader_replay_leaves': len(replay),
    'prepared_fresh_source_leaves': len(sm['files']), 'normal_API_calls': 0, 'Git_calls': 0}, ensure_ascii=False))
