"""Prepare and syntax-check new Geometry helpers without importing/running them."""
from pathlib import Path
import ast, difflib, gzip, hashlib, json
R = Path('/Users/zhouhuanjian/ASTIS-GC')
S = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader'
OLD = R / '.astis/huanjian-gc-fixed-spectrum-first-order-integration-20261108/independent-reader'
O = S / 'conditional-browser-preparation-v1'
assert not O.exists() and not (S / 'check_final_reader_v1.py').exists()
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
old_path = OLD / 'check_final_reader_v4.py'; old = old_path.read_bytes()
old_common = (OLD / 'first_order_browser_common_v4.py').read_bytes()
assert sha(old) == 'de762a4107ce9bf844fa6ecf7f7d388928f0f15b391b9e63209ddeee22a9614f'
assert sha(old_common) == '523eefc6eba165093e51cdcb9fd67377ba6a66b95b1721e34d62b337d9a10e26'
s = old.decode()
def replace(a, b, count=1):
    global s
    assert s.count(a) == count, (a, s.count(a), count)
    s = s.replace(a, b)
replace('CONDITIONAL new FirstOrder browser helper: no actual run until fresh sourceV/soleSTAB/exact gates and separate root+OS authorization.', 'CONDITIONAL new Geometry browser helper: unexecuted; real current sourceV/soleSTAB/core gates and separate new root+OS authorization required.')
replace('from first_order_browser_common_v4 import', 'from geometry_browser_common_v1 import')
replace("CANDIDATE='9d306d837fbddf1518b0035494baaf5c21c24488'", "CANDIDATE='ab8b47caed9f781191f8408154cd355c7e7c104c'")
replace("NAME=PREFIX+'FixedSpectrumFirstOrder.actual_first_order_query'", "NAME=PREFIX+'FixedSpectrumGeometry.actual_potential_geometry'")
replace("MODULE=PREFIX+'FixedSpectrumFirstOrder'", "MODULE=PREFIX+'FixedSpectrumGeometry'")
replace("ITEM='huanjian-fixed-spectrum-first-order'", "ITEM='huanjian-fixed-spectrum-geometry'")
replace("BINDING='51d5a5e9390a0d66c2d5b72d042a042eec8d3d60433043ea3909bf9320ccb31e'", "BINDING='69c4f115a417c0aea6a8ebc9384cfc66ff07e6fae92de806831b79075a4760fa'")
replace("AFFINE=PREFIX+'FixedSpectrumAffine.actual_affine_precision_query'\nPRODUCER_ASTIS_PARENTS=[ADMISSIBILITY]\nCONSUMER_ASTIS_PARENTS=[NAME,AFFINE]", "FIRST=PREFIX+'FixedSpectrumFirstOrder.actual_first_order_query'\nCONVERSE='AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGradientConverse.strongConvexOn_of_gradient_inner_lower_bound'\nPRODUCER_ASTIS_PARENTS=[ADMISSIBILITY,FIRST,CONVERSE]\nCONSUMER_ASTIS_PARENTS=[NAME,FIRST]")
report = json.loads((S / 'conditional-proposal-v1/proposal-report.json').read_bytes())
pins = {p: h for p, h in report['source_Test_lesson_publication_pins'].items()
        if p not in ['runs/substantive_advances.jsonl', 'runs/substantive_discoveries.jsonl',
                     'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-geometry.json']}
for p in ['website/static/underlying-lean-graph.js', 'website/static/information-architecture.css',
          'website/content/graph_memory_index.json', 'website/content/functor_hypergraph.json']:
    pins[p] = sha((R / p).read_bytes())
pins['website/content/samplewiki_companion_frontiers.json'] = next(x['planned_after_sha256'] for x in report['shared_paths'] if x['path'] == 'website/content/samplewiki_companion_frontiers.json')
line = next(x for x in s.splitlines() if x.startswith('PINS='))
replace(line, 'PINS=' + repr(pins))
# Exact path substitutions affect only the current target; old conceptual
# FirstOrder substrate is retained explicitly below as a regression.
for a, b in [
    ('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumFirstOrder.lean', 'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumGeometry.lean'),
    ('Tests/GaussianComplexityFixedSpectrumFirstOrder.lean', 'Tests/GaussianComplexityFixedSpectrumGeometry.lean'),
    ('website/content/declaration_lessons/huanjian-fixed-spectrum-first-order.json', 'website/content/declaration_lessons/huanjian-fixed-spectrum-geometry.json'),
    ('fixed-spectrum-first-order-semantic-evidence/local-proof-capsule.json', 'fixed-spectrum-geometry-semantic-evidence/local-proof-capsule.json'),
    ('actual_reference_precision_first_order_consumer', 'actual_first_order_oracle_measurable'),
    ("'Tests.GaussianComplexityFixedSpectrumFirstOrder'", "'Tests.GaussianComplexityFixedSpectrumGeometry'")]:
    # PINS already contains current Geometry paths and the actual old parent
    # FirstOrder path, which must not be replaced by a duplicate Geometry key.
    pin_start = s.index('PINS='); pin_end = s.index('\n', pin_start)
    prefix, pin_line, suffix = s[:pin_start], s[pin_start:pin_end], s[pin_end:]
    assert a in prefix + suffix, a
    s = prefix.replace(a, b) + pin_line + suffix.replace(a, b)
replace("len(unit['steps'])==6", "len(unit['steps'])==7")
replace("parent_ids=['decl:'+ADMISSIBILITY]", "parent_ids=['decl:'+parent for parent in PRODUCER_ASTIS_PARENTS]")
replace("assert sum(x['node']==MODULE for x in family['compiled_substrate_bindings'])==1\nassert nodes[bridge]['hyperedge']==edge and module_id in nodes[bridge]['candidate_substrates']\nincidence=[e for e in graph['edges'] if e['source']==module_id and e['target']==bridge]", "concept_module=PREFIX+'FixedSpectrumFirstOrder';concept_module_id='module:'+concept_module\nassert sum(x['node']==concept_module for x in family['compiled_substrate_bindings'])==1\nassert not any(x['node']==MODULE for x in family['compiled_substrate_bindings'])\nassert nodes[bridge]['hyperedge']==edge and concept_module_id in nodes[bridge]['candidate_substrates']\nassert module_id not in nodes[bridge]['candidate_substrates']\nincidence=[e for e in graph['edges'] if e['source']==concept_module_id and e['target']==bridge]")
replace(".astis/huanjian-gc-fixed-spectrum-first-order-integration-20261108/independent-reader/browser", ".astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader/browser")
replace('Private Test only; exactly new producer and actual SAME-O affine provider. No Registry consumer or operational cost theorem.', 'Private Test only; exactly new Geometry and canonical FirstOrder. Actual fixed-input Borel pair, with no joint/adaptive/query-cap/cost theorem or public Registry consumer.')
replace("('either determinant sign', 'zero additive constant', 'Fréchet derivative existence', 'same hidden', 'Reference', 'Random seeds')", "('either determinant sign', 'no additive shift', 'All spatial points and pairs', 'Fréchet derivative', 'Strong convexity', 'Haar randomness', 'query budgets')")
replace('assert steps.count() == 6\n            for i in range(6):', 'assert steps.count() == 7\n            for i in range(7):')
replace('every one of the six steps', 'every one of the seven steps')
replace('assert parent_list.count() == 1', 'assert parent_list.count() == 3')
replace("'six_formula_steps_opened': True", "'seven_formula_steps_opened': True")
replace("'consumer_uses_same_O_forward_affine': True", "'consumer_fixed_input_actual_Borel': True")
replace("'C4 calculus/minimizer'", "'actual fixed-spectrum C4 geometry'")
needle = "            determinant_text = page.locator('#gaussian-complexity-determinant').text_content()"
replace(needle, "            for phrase in ('genuine gradient derivative', '1-strongly convex', 'value zero uniquely at the origin', 'three direct kernel ASTIS parents', 'Borel measurable for each fixed hidden input', 'strict angle/cosine prefix', 'generic Hessian-criterion route', 'deterministic worst-query caps', 'explicit expected-cost reductions'):\n                assert phrase in boundary, phrase\n" + needle)
replace("'native_one_canonical_parent_click': True", "'native_three_canonical_parent_clicks': True")
replace('ONE separately kernel-confirmed admissibility producer parent and TWO private Test parents: new producer plus same-O affine provider. Scanner references are dashed/incomplete, not complete kernel export. No old GPD source/audit change is part of this packet.', 'THREE separately kernel-confirmed producer parents: actual admissibility, actual FirstOrder and the same canonical gradient converse. TWO private Borel Test parents: Geometry plus FirstOrder. Scanner references remain dashed/incomplete, never complete kernel export. No old GPD/source/audit/model history changes.')
start = s.index("            bridge_focus = focused_entry(page, bridge,")
end = s.index('            context.close()', start)
section = s[start:end]
section = section.replace('module_id', 'concept_module_id')
section = section.replace("'same_existing_bridge_typed_supplement': True", "'existing_FirstOrder_typed_supplement_regression': True")
section = "            # Unchanged existing FirstOrder conceptual supplement regression only.\n            # Geometry gains no candidate incidence or conceptual transport credit.\n" + section
s = s[:start] + section + s[end:]
replace("assert len(report['screenshots']) == 38", "assert len(report['screenshots']) == 44")
replace("assert len(report['native_selection_geometry']) == 8", "assert len(report['native_selection_geometry']) == 12")
compile(s, str(S / 'check_final_reader_v1.py'), 'exec')
common = (S / 'geometry_browser_common_v1.py').read_bytes()
compile(common, str(S / 'geometry_browser_common_v1.py'), 'exec')
O.mkdir()
(S / 'check_final_reader_v1.py').write_bytes(s.encode())
for name, raw in [('FirstOrder-v4-checker.before.raw.gz', old), ('FirstOrder-v4-common.before.raw.gz', old_common),
                  ('Geometry-v1-checker.after.raw.gz', s.encode()), ('Geometry-v1-common.after.raw.gz', common)]:
    (O / name).write_bytes(gzip.compress(raw, mtime=0))
(O / 'FirstOrder-v4-to-Geometry-v1-checker.exact.diff').write_bytes(''.join(difflib.unified_diff(old.decode().splitlines(keepends=True), s.splitlines(keepends=True), fromfile='historical/check_final_reader_v4.py', tofile='conditional/check_final_reader_v1.py')).encode())
(O / 'FirstOrder-v4-to-Geometry-v1-common.exact.diff').write_bytes(''.join(difflib.unified_diff(old_common.decode().splitlines(keepends=True), common.decode().splitlines(keepends=True), fromfile='historical/first_order_browser_common_v4.py', tofile='conditional/geometry_browser_common_v1.py')).encode())
# Assertions retained exactly in the inherited browser body where semantic
# current-target substitutions are not necessary. No Playwright import/run.
critical_functions = ['ordinary_prose_bounds', 'native_selection_geometry', 'focused_entry']
def functions(text):
    return {n.name: ast.get_source_segment(text, n) for n in ast.parse(text).body if isinstance(n, ast.FunctionDef)}
old_functions = functions(old.decode()); new_functions = functions(s)
assert all(old_functions[n] == new_functions[n] for n in critical_functions)
assert old.decode().split('NATIVE_GEOMETRY_JS = ', 1)[1].split('\n\n\ndef native_selection_geometry', 1)[0] == s.split('NATIVE_GEOMETRY_JS = ', 1)[1].split('\n\n\ndef native_selection_geometry', 1)[0]
old_regression = old.decode().split('            # One existing generic long-Lean card regression;', 1)[1].split('            bridge_focus = ', 1)[0]
new_regression = s.split('            # One existing generic long-Lean card regression;', 1)[1].split('            # Unchanged existing FirstOrder conceptual', 1)[0]
assert old_regression == new_regression
assert 'f45ba48f' not in s + common.decode() and 'source_reader_4e8f6a' not in s + common.decode()
assert old_path.read_bytes() == old and (OLD / 'first_order_browser_common_v4.py').read_bytes() == old_common
info = {'state': 'CONDITIONAL_NEW_GEOMETRY_BROWSER_HELPERS_PREPARED_UNEXECUTED',
    'sourceV_browser_OS_network_authorized_by_this_preparation': False,
    'checker_sha256': sha(s.encode()), 'common_sha256': sha(common),
    'prior_FirstOrder_checker_sha256': sha(old), 'prior_FirstOrder_common_sha256': sha(old_common),
    'candidate_commit': report['candidate_commit'], 'proposal_report_sha256': sha((S / 'conditional-proposal-v1/proposal-report.json').read_bytes()),
    'future_actual_commit_digest_gate_audit_sourceV_values': 'No values invented. Actual references are mandatory in a future root-pinned authorization record.',
    'authorization_kind': 'fixed-spectrum-geometry-final-browser-v1',
    'new_command_entry': '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader/check_final_reader_v1.py',
    'old_approved_FirstOrder_or_Normalizer_prefix_reused': False,
    'desktop_mobile': [1440, 390], 'planned_actual_original_PNGs': 44, 'planned_native_geometry_rows': 12,
    'planned_old_DensityAffinity_DOM_regressions': 2, 'planned_formula_steps_per_width': 7,
    'native_geometry_JS_and_functions_exact_inherited': critical_functions,
    'old_DensityAffinity_DOM_regression_block_exact_inherited': True,
    'existing_FirstOrder_conceptual_supplement': 'Unchanged regression only; Geometry absent from model candidate incidence. No model edit/transport inferred.',
    'private_Test': 'Actual Borel consumer; exact candidate/current Git, DOM and download bytes; not a public/Registry node.',
    'pixel_acceptance': 'A later actual script PASS is DOM/UI evidence. All actual original PNGs still require separate independent original-image inspection and acceptance.',
    'syntax_only_checks': 'compile() without import/execution, no Playwright/HTTP/Chrome run',
    'remaining': ['Root exact helper/static review', 'Real sourceV/soleSTAB/core/gate/site/graph records',
                  'New scoped OS/browser approval', 'Actual browser originals and separate independent pixels']}
(O / 'preparation-report.json').write_bytes(dump(info))
(O / 'preparation-driver.py.raw.gz').write_bytes(gzip.compress(Path(__file__).read_bytes(), mtime=0))
freeze = {'state': info['state'], 'report_sha256': sha((O / 'preparation-report.json').read_bytes()),
    'files': [{'path': str(p.relative_to(R)), 'sha256': sha(p.read_bytes())} for p in sorted(O.iterdir()) if p.is_file()], 'executed': False}
(O / 'freeze.json').write_bytes(dump(freeze))
print(json.dumps({'report_sha256': freeze['report_sha256'], 'freeze_sha256': sha((O / 'freeze.json').read_bytes()),
    'checker_sha256': sha(s.encode()), 'common_sha256': sha(common), 'browser_executed': False}, indent=2))
