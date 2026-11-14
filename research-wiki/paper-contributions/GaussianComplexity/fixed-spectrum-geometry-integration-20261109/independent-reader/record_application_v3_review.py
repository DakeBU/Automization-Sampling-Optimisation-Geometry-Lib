"""Exact static V3 acceptance recorder. Never imports or executes application helper."""
from pathlib import Path
import ast, datetime, difflib, gzip, hashlib, json, subprocess
R = Path('/Users/zhouhuanjian/ASTIS-GC')
S = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader'
P = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109'
O = S / 'application-helper-review-v3'
assert not O.exists()
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
v1 = (P / 'apply_reviewed_shared.py').read_bytes()
v2 = (P / 'apply_reviewed_shared_v2.py').read_bytes()
v3 = (P / 'apply_reviewed_shared_v3.py').read_bytes()
assert sha(v1) == '4fc3f6e5ce97512f2b742428dc6ff1225f5e56e8a545fb9acda83feb49d482a2'
assert sha(v2) == '6589347d7588d7932c8f6330c1a3809afe41864f6b9a1dc7a8d60265da31e9f9'
assert sha(v3) == '33d3be0ef4cf9c9bc7ed756b8509e39f2b323ff5881a2adf5e8ae8909030b702'
expected = v2
for old, new in [
    (b'import datetime,gzip,hashlib,json,os,subprocess,sys\n', b'import datetime,gzip,hashlib,json,os,subprocess,sys\nsys.dont_write_bytecode=True\n'),
    (b"authpath=P/'root-sole-STAB-application-authorization-v2.json'", b"authpath=P/'root-sole-STAB-application-authorization-v3.json'"),
    (b'CP.write_bytes(cell_after)\n', b'CP.write_bytes(cell_after)\nassert CP.read_bytes()==cell_after\n')]:
    assert expected.count(old) == 1
    expected = expected.replace(old, new, 1)
assert v3 == expected
compile(v3, '<static-v3-no-execution>', 'exec')
tree = ast.parse(v3)
functions = lambda raw: {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(raw).body if isinstance(n, ast.FunctionDef)}
assert functions(v2) == functions(v3)
for folder, digest in [('application-helper-review-v1', '77a43899689d2b2dda7b2fba1eadb7b96cb71acd91a06041deee5aeda0cc21ca'),
                       ('application-helper-review-v2', '399f1b387412d783a6f668bbfb3d1106a8db965409a70545a2684ba140e4a07c')]:
    path = S / folder / 'freeze.json'
    assert sha(path.read_bytes()) == digest
    freeze = json.loads(path.read_bytes())
    for row in freeze['files']: assert sha((R / row['path']).read_bytes()) == row['sha256']
fixture = S / 'application-helper-review-v2/pure-helper-fixture-report.json'
assert sha(fixture.read_bytes()) == '8dc12fa073d17d3480f756413a409743871b8979aef6e550ad944372e5bad3c4'
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R).decode().strip() == 'ab8b47caed9f781191f8408154cd355c7e7c104c'
assert not subprocess.check_output(['git', 'diff', 'HEAD', '--name-only'], cwd=R)
O.mkdir()
(O / 'helper-v3.exact.raw.py.gz').write_bytes(gzip.compress(v3, mtime=0))
diff = ''.join(difflib.unified_diff(v2.decode().splitlines(keepends=True), v3.decode().splitlines(keepends=True),
                                 fromfile='reviewed-HOLD/apply_reviewed_shared_v2.py', tofile='accepted-unapplied/apply_reviewed_shared_v3.py')).encode()
(O / 'v2-to-v3.exact.diff').write_bytes(diff)
record = {'reviewer': '/root/geometry_integration_reader', 'verdict': 'ACCEPT_EXACT_UNAPPLIED_SUCCESSOR',
 'helper_sha256': sha(v3), 'helper': str((P / 'apply_reviewed_shared_v3.py').relative_to(R)),
 'candidate_commit': 'ab8b47caed9f781191f8408154cd355c7e7c104c',
 'scope': 'Independent exact static review of the unapplied V3 shared application helper only. This is an accepted-helper review token; actual separate root authorization and real sourceV evidence are still mandatory.',
 'exact_v2_to_v3_delta': ['Set sys.dont_write_bytecode=True before local imports',
    'Use distinct v3 root application authorization filename', 'Read back CP.read_bytes()==cell_after immediately after own-frontier write'],
 'other_byte_changes': False, 'exact_delta_sha256': sha(diff),
 'R1_R4_resolution': 'All substantive V1 findings closed by independently inspected V2 guards, retained byte-exact except the three listed V3 changes. V3 closes both frozen V2 hardening findings.',
 'guard_summary': ['Full frozen candidate raw baseline and exact foreign frontier inventory checked before/after; exact own audit/ledger/reviewed-frontier exceptions only.',
    'Real one-call sourceV execution manifest, original accepted current-binding audit/review run and exact append hashes; known source verifier/decoder and all six roles distinct.',
    'Complete raw candidate prefix plus sole actual own V validated before pure replay; proofowner preserved; one normal VERIFIED→STABILIZING append parsed and sole lane checked.',
    'Six exact reviewed byte payloads plus explicitly authorized one-object own metadata projection; no old canonical result overwrite, exact inverse restoration and actual raw own-cell readback.',
    'Expected source digest and all foreign source/audit/model/discovery/README/frontier/state preservation enforced; no browser/remote/Goal completion inferred.'],
 'fixture_reuse': {'path': str(fixture.relative_to(R)), 'sha256': sha(fixture.read_bytes()),
    'pure_function_ASTs_V2_V3_identical': True, 'five_lossless_cases_and_refusal_checks': 'PASS, explicitly fixture-only',
    'actual_sourceV_or_STAB_fixture_used_as_real': False},
 'prior_reviews_retained': [
    {'path': str((S / 'application-helper-review-v1/static-review-HOLD.json').relative_to(R)), 'sha256': '9ad7b55da7cea7625aeba3a997205a77e7643f58c30e58f4d4d372ef12a4710f'},
    {'path': str((S / 'application-helper-review-v2/static-review-HOLD.json').relative_to(R)), 'sha256': 'a00ed3c92930f4a1ece314eb74a1567934eb1521f283b2625974843a543e88ea'}],
 'no_full_helper_execution_or_API_or_shared_mutation': True,
 'sourceV_application_runtime_pixel_or_remote_acceptance_granted': False,
 'remaining_before_actual_application': ['Real separately issued distinct current-binding sourceV and its exact execution/append/audit/source-review-run evidence',
    'Separately accepted exact sourceV own-frontier metadata projection if any', 'Concrete root exact V3 application authorization with this review hash and actual immutable references'],
 'later_acceptance': 'Actual immutable core official8 gates/site/graph; new scoped Chrome/OS authorization;44 actual original PNGs/12 native geometry rows; separate independent original-image acceptance. No script PASS substitutes for pixels.',
 'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
(O / 'static-review-ACCEPT.json').write_bytes(dump(record))
(O / 'review-recorder.raw.py.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(), mtime=0))
freeze = {'state': record['verdict'], 'report_sha256': sha((O / 'static-review-ACCEPT.json').read_bytes()),
 'files': [{'path': str(q.relative_to(R)), 'sha256': sha(q.read_bytes())} for q in sorted(O.iterdir()) if q.is_file()],
 'actual_sourceV_or_STAB_or_application_executed': False}
(O / 'freeze.json').write_bytes(dump(freeze))
assert (P / 'apply_reviewed_shared_v3.py').read_bytes() == v3
print(json.dumps({'report': str((O / 'static-review-ACCEPT.json').relative_to(R)), 'report_sha256': freeze['report_sha256'],
 'freeze_sha256': sha((O / 'freeze.json').read_bytes()), 'helper_sha256': sha(v3), 'verdict': record['verdict'],
 'application_executed': False}, indent=2))
