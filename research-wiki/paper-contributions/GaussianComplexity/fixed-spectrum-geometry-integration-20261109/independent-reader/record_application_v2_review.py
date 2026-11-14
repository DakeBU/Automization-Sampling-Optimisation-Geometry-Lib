"""Record exact static V2 review; no application/sourceV/lifecycle execution."""
from pathlib import Path
import datetime, gzip, hashlib, json, subprocess
R = Path('/Users/zhouhuanjian/ASTIS-GC')
S = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader'
O = S / 'application-helper-review-v2'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
p = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/apply_reviewed_shared_v2.py'
raw = p.read_bytes(); expected = '6589347d7588d7932c8f6330c1a3809afe41864f6b9a1dc7a8d60265da31e9f9'
assert sha(raw) == expected
fixture = O / 'pure-helper-fixture-report.json'
assert sha(fixture.read_bytes()) == '8dc12fa073d17d3480f756413a409743871b8979aef6e550ad944372e5bad3c4'
assert not (O / 'static-review-HOLD.json').exists() and not (O / 'freeze.json').exists()
record = {'reviewer': '/root/geometry_integration_reader', 'verdict': 'HOLD_EXACT_UNAPPLIED_SUCCESSOR',
 'helper_sha256': expected, 'helper': str(p.relative_to(R)),
 'previous_defect_report_sha256': '9ad7b55da7cea7625aeba3a997205a77e7643f58c30e58f4d4d372ef12a4710f',
 'corrected_R1_R4': {
  'R1': 'Frozen all_tracked raw baseline verified before and after; AP/LP/CP each has exact separately bound own successor semantics. Exact foreign frontier inventory/raw hashes, foreign states and all discovery state/bytes protected; new tracked paths restricted to own source evidence/application bundle plus reviewed shared card.',
  'R2': 'Known actual source reviewer9a6d2f and decoder80a1c2 fixed; all six role IDs distinct; actual accepted audit/source run/current binding and one-call actual sourceV execution manifest actor/append/candidate/binding/audit/run hashes required. No fabricated future values or sourceV issuance.',
  'R3': 'Explicit root own-frontier one-object authorization; separately reviewed actual sourceV metadata successor required if candidate own-cell changes. New canonical key must be absent. Raw insertion preserves old bytes and reverses exactly; exact own metadata delta/actual STAB/sourceV references archived honestly alongside six payloads.',
  'R4': 'Complete raw candidate-prefix+soleV JSONL pinned before local imports; pure official replay without recovery. One normal STAB API call, returned append parsed as VERIFIED→STABILIZING by INTEGRATOR with exact original verifier/candidate/declaration set, proofowner and sole-STAB/foreign state checks.'},
 'remaining_items': [
  {'id': 'V2-H1', 'severity': 'REQUIRED_FOR_NO_MUTATION_PREFLIGHT',
   'finding': 'Local imports adv/pub/site occur before the --preflight exit and Python bytecode is not disabled in this helper. Ordinary Python can create tools/website __pycache__ files despite the no-mutation preflight claim.',
   'required_successor_change': 'Set sys.dont_write_bytecode=True before any local import. This avoids relying on a separate invocation environment constraint.'},
  {'id': 'V2-H2', 'severity': 'REQUIRED_OWN_FRONTIER_RAW_READBACK',
   'finding': 'CP.write_bytes(cell_after) is followed by baseline checks that explicitly exempt CP. The later projection hashes/archives use in-memory cell_after, so actual written own-cell bytes have no explicit equality readback.',
   'required_successor_change': 'Immediately after CP.write_bytes(cell_after), require CP.read_bytes()==cell_after before recording the actual projection/application receipt.'}],
 'pure_helper_fixture_results': {'path': str(fixture.relative_to(R)), 'sha256': sha(fixture.read_bytes()),
   'cases': 5, 'scope': 'Only AST-extracted rows/differences/spans/append_integration functions executed. Actual-candidate raw copy and synthetic CRLF/mixed/minified/nested cases all restore original bytes exactly. Existing canonical overwrite/empty evidence and invalid JSONL cases refuse. No original application module imported or executed; fixture metadata explicitly not actual sourceV/STAB.'},
 'acceptance_boundary': 'V2 closes the substantive R1–R4 defects but remains HOLD for the two explicit hardening changes. A separately pinned V3 requires independent exact delta re-review. This record is not an accepted-review token consumed by the application helper.',
 'root_original_V1_lossless_preserved': True, 'V2_full_script_unexecuted': True,
 'sourceV_or_STAB_or_application_or_runtime_or_pixel_acceptance_granted': False,
 'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
(O / 'static-review-HOLD.json').write_bytes(dump(record))
(O / 'review-recorder.raw.py.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(), mtime=0))
freeze = {'state': record['verdict'], 'report_sha256': sha((O / 'static-review-HOLD.json').read_bytes()),
 'files': [{'path': str(q.relative_to(R)), 'sha256': sha(q.read_bytes())} for q in sorted(O.iterdir()) if q.is_file()],
 'application_execution_or_sourceV_authorized': False}
(O / 'freeze.json').write_bytes(dump(freeze))
assert p.read_bytes() == raw
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R).decode().strip() == 'ab8b47caed9f781191f8408154cd355c7e7c104c'
assert not subprocess.check_output(['git', 'diff', 'HEAD', '--name-only'], cwd=R)
print(json.dumps({'report_sha256': freeze['report_sha256'], 'freeze_sha256': sha((O / 'freeze.json').read_bytes()),
 'helper_sha256': expected, 'verdict': record['verdict'], 'application_executed': False}, indent=2))
