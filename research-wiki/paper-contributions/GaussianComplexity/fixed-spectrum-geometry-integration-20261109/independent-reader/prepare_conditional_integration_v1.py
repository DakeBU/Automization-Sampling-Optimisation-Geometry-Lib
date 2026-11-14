"""Freeze an unapplied Geometry integration proposal. No lifecycle or build calls."""
from pathlib import Path
import ast, copy, datetime, difflib, gzip, hashlib, json, os, re, subprocess

R = Path('/Users/zhouhuanjian/ASTIS-GC')
S = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader'
O = S / 'conditional-proposal-v1'
E = R / 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-geometry-semantic-evidence'
HEAD = 'ab8b47caed9f781191f8408154cd355c7e7c104c'
ADV = 'ASTIS-SA-20261109-GaussianComplexityFixedSpectrumGeometry'
CELL = 'ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-geometry'
P = 'AutoSamplingTheory.ExampleCases.GaussianComplexity.'
MODULE = P + 'FixedSpectrumGeometry'
DECL = MODULE + '.actual_potential_geometry'
ADMISS = P + 'FixedSpectrumAdmissibility.actual_precision_admissible'
FIRST = P + 'FixedSpectrumFirstOrder.actual_first_order_query'
CONVERSE = 'AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGradientConverse.strongConvexOn_of_gradient_inner_lower_bound'
PARENTS = [ADMISS, FIRST, CONVERSE]
BINDING = '69c4f115a417c0aea6a8ebc9384cfc66ff07e6fae92de806831b79075a4760fa'
sha = lambda b: hashlib.sha256(b).hexdigest()
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode()
canon = lambda x: json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
def cmd(*args):
    return subprocess.check_output(args, cwd=R)
def archive(name, raw):
    q = O / name
    assert not q.exists()
    q.write_bytes(gzip.compress(raw, mtime=0))
    assert gzip.decompress(q.read_bytes()) == raw
    return {'path': str(q.relative_to(R)), 'raw_sha256': sha(raw),
            'gzip_sha256': sha(q.read_bytes()), 'raw_bytes': len(raw)}
def once(raw, old, new):
    a = old.encode() if isinstance(old, str) else old
    b = new.encode() if isinstance(new, str) else new
    assert raw.count(a) == 1, old
    return raw.replace(a, b, 1)
def source_digest(overrides):
    d = hashlib.sha256()
    paths = [R / 'AutoSamplingTheory.lean', *sorted((R / 'AutoSamplingTheory').rglob('*.lean')),
             R / 'Tests.lean', *sorted((R / 'Tests').rglob('*.lean')),
             R / 'lakefile.lean', R / 'lean-toolchain', R / 'lake-manifest.json']
    for q in paths:
        if q.exists():
            p = q.relative_to(R).as_posix()
            d.update(p.encode()); d.update(b'\0')
            d.update(overrides.get(p, q.read_bytes())); d.update(b'\0')
    return d.hexdigest()
def pure_replays():
    # Compile only the two official pure replay functions. Never call the public
    # load/recovery/control-plane APIs: some of those can rewrite interrupted tails.
    source = (R / 'tools/astis_advance.py').read_text()
    tree = ast.parse(source)
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name in {'_replay_advances', '_replay_discoveries'}]
    assert len(nodes) == 2
    ns = {'Iterable': list, 'Any': object, 'NO_PROGRESS_FREEZE_AT': 3}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), '<official-pure-replay-only>', 'exec'), ns)
    ledger = (R / 'runs/substantive_advances.jsonl').read_bytes()
    discoveries = (R / 'runs/substantive_discoveries.jsonl').read_bytes()
    return (ns['_replay_advances']([json.loads(x) for x in ledger.splitlines() if x.strip()]),
            ns['_replay_discoveries']([json.loads(x) for x in discoveries.splitlines() if x.strip()]))

assert cmd('git', 'rev-parse', 'HEAD').decode().strip() == HEAD
assert not cmd('git', 'diff', '--name-only') and not cmd('git', 'diff', '--cached', '--name-only')
assert not O.exists()
pins_path = E / 'full-review-input-pins.json'
pins = json.loads(pins_path.read_bytes())
assert pins['checked_candidate_commit'] == HEAD and pins['publication_binding_sha256'] == BINDING
for p, h in pins['exact_inputs'].items():
    assert sha((R / p).read_bytes()) == h, p
    assert cmd('git', 'show', HEAD + ':' + p) == (R / p).read_bytes(), p
capsule = json.loads((E / 'local-proof-capsule.json').read_bytes())
assert capsule['actual_direct_ASTIS_producer_parents'] == PARENTS
assert capsule['actual_direct_ASTIS_private_consumer_parents'] == [DECL, FIRST]
assert json.loads((E / 'postproof-conceptual-mirror-audit.json').read_bytes())['status'] == 'none-found'
audit_path = 'research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-geometry.json'
audit = json.loads((R / audit_path).read_bytes())
assert audit['state'] == 'blind-reconstructed' and audit['verdict'] == 'pending'
assert audit['publication_binding_sha256'] == BINDING
lesson_path = 'website/content/declaration_lessons/huanjian-fixed-spectrum-geometry.json'
publication_path = 'website/content/publications/huanjian-fixed-spectrum-geometry.json'
lesson = json.loads((R / lesson_path).read_bytes())['units'][0]
item = json.loads((R / publication_path).read_bytes())['items'][0]
assert lesson['declaration'] == DECL and lesson['astis_dependencies'] == PARENTS and len(lesson['steps']) == 7
binding = item['bindings'][0]
assert binding['declaration'] == DECL and binding['cell'] == CELL
code_path = 'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumGeometry.lean'
payload = {'file': sha((R / code_path).read_text().encode()),
           'current_lean_module': (R / code_path).read_text(),
           'toolchain': sha((R / 'lean-toolchain').read_text().encode()),
           'dependencies': sha((R / 'lake-manifest.json').read_text().encode()),
           **{k: item[k] for k in ['source', 'statement', 'formulae', 'assumptions', 'obligations']},
           'lesson': lesson, 'binding': {k: v for k, v in binding.items() if k not in {'audit_id', 'legacy_audit_debt'}}}
assert sha(canon(payload)) == BINDING

# Inspect successful historical raw receipts and their actual logs; these are
# focused local proof evidence, never a current same-head aggregate gate.
receipts = []
for k in ['focused_success_receipt', 'kernel_and_exact_statement_success_receipt']:
    c = capsule[k]; q = R / c['receipt']; raw = q.read_bytes(); rec = json.loads(raw)
    log = Path(rec['log']).read_bytes()
    assert sha(raw) == c['receipt_sha256'] and rec['exit_code'] == 0
    assert sha(log) == c['raw_log_sha256'] == rec['log_sha256']
    receipts.append({'receipt': str(q.relative_to(R)), 'receipt_sha256': sha(raw),
                     'raw_log': str(Path(rec['log']).relative_to(R)), 'raw_log_sha256': sha(log),
                     'actual_command': rec['command'], 'historical_head': rec['head_before'],
                     'same_head_aggregate_gate': False})
kernel = (R / receipts[1]['raw_log']).read_text()
parts = kernel.split('ACTUAL_TARGET ')
assert len(parts) == 3
got = [[line.removeprefix('ACTUAL_ASTIS_PARENT ') for line in p.splitlines()
        if line.startswith('ACTUAL_ASTIS_PARENT ')] for p in parts[1:]]
assert got == [PARENTS, [DECL, FIRST]]
assert 'Exact sealed full-forall producer application and literal private-consumer type application checked.' in kernel
assert 'Actual proof-term ASTIS parents producer3/consumer2' in kernel
focused = (R / receipts[0]['raw_log']).read_text()
assert 'Build completed successfully (2694 jobs).' in focused
assert focused.count('depends on axioms: [propext,\n Classical.choice,\n Quot.sound]') == 2

paths = ['AutoSamplingTheory.lean', 'Tests.lean', 'Tests/Basic.lean',
         'AutoSamplingTheory/TechnicalLemmas/Registry.lean',
         'website/content/samplewiki_companion_frontiers.json',
         'research-wiki/sampling-sde-library/cards/' + MODULE + '.md']
before = {p: (R / p).read_bytes() if (R / p).exists() else None for p in paths}
assert before[paths[5]] is None
plans = {}
for p, anchor, added in [
    (paths[0], 'import ' + P + 'FixedSpectrumFirstOrder\n', 'import ' + MODULE + '\n'),
    (paths[1], 'import Tests.GaussianComplexityFixedSpectrumFirstOrder\n', 'import Tests.GaussianComplexityFixedSpectrumGeometry\n'),
    (paths[3], 'import ' + P + 'FixedSpectrumFirstOrder\n', 'import ' + MODULE + '\n')]:
    plans[p] = once(before[p], anchor, anchor + added)
assert before[paths[3]].count(b'status := LemmaMemoryStatus.formalizedLocal') == 623
for parent in PARENTS:
    assert before[paths[3]].count(('localDecl := "' + parent + '"').encode()) == 1
assert DECL.encode() not in before[paths[3]] and b'actual_first_order_oracle_measurable' not in before[paths[3]]
plans[paths[2]] = once(before[paths[2]], 'formalizedTechnicalLemmaCount = 623', 'formalizedTechnicalLemmaCount = 624')
entry = '''  {
    key := "gaussian-complexity.fixed-spectrum-geometry",
    localDecl := "AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry.actual_potential_geometry",
    upstreamDecl := "arXiv2610.20492v1 Eq11 and AppendixC.4 actual potential geometry",
    upstreamFile := "S4.SS1/E11 literal family; AppendixC.4 smoothness/Hessian/convexity/minimizer; S2.E1 fixed-input Borel reply background",
    status := LemmaMemoryStatus.formalizedLocal,
    tags := ["GaussianComplexity", "fixed-spectrum", "actual-potential", "strong-convexity", "Borel-consumer", "canonical-reuse"],
    saldUse := "The real private fixed-input Borel Test consumes this producer's scalar smoothness and genuine gradient derivative, then the identical canonical FirstOrder identity to identify the actual value/precision reply",
    note := "Mathematical candidate ab8b47caed9f781191f8408154cd355c7e7c104c and publication binding 69c4f115a417c0aea6a8ebc9384cfc66ff07e6fae92de806831b79075a4760fa pin exact code, Test and authored mathematics. Genuine current-binding independent source/whole-module review, normal source V and sole STAB are prerequisites to applying this conditional payload. Exactly d>=2, kappa>=2 and every full real orthogonal O, including either determinant sign: the literal centered cosine-grid potential is globally C-infinity; its actual Euclidean gradient has Frechet derivative A at every point; it is 1-strongly convex with the r-squared/2 modulus and kappa-Lipschitz gradient; f(0)=0 and a point is a global minimizer iff it is zero. Actual admissibility, actual FirstOrder and the identical StrongConvexGradientConverse.strongConvexOn_of_gradient_inner_lower_bound are the THREE direct kernel ASTIS producer parents, already canonical Registry nodes. Symmetry, closed quadratic bounds, regularity, operator norm and minimizer facts are derived internally, never caller certificate premises. The private Test genuinely consumes Geometry and canonical FirstOrder as its TWO direct kernel ASTIS parents to prove the literal same-A ordered value/reply pair Borel for each fixed O. It creates no public or Registry consumer node. The strict source angle/cosine prefix and author's generic Hessian-criterion route remain distinct source obligations; this implementation uses closed canonical admissibility and the same gradient-monotonicity converse. No new conceptual transport is proposed; GraphMemory, Functor and discovery ledger stay unchanged. Joint hidden-input/adaptive/private-seed/history/transcript/output-law, actual Gaussian target/TV and finite precision, deterministic worst-query caps and explicit expected-cost reductions, moments/Krylov and both complete main lower bounds, remote publication and postmerge purification/Exposition Seal remain separate."
  },
'''
plans[paths[3]] = once(plans[paths[3]], '  {\n    key := "gaussian-complexity.single-block-separation",', entry + '  {\n    key := "gaussian-complexity.single-block-separation",')
assert plans[paths[3]].count(b'status := LemmaMemoryStatus.formalizedLocal') == 624
assert plans[paths[3]].replace(entry.encode(), b'', 1).replace(('import ' + MODULE + '\n').encode(), b'', 1) == before[paths[3]]

model = json.loads(before[paths[4]])
case = model['cases'][4]
assert case['id'] == 'ASTIS-SW-GAUSSIAN-COMPLEXITY-2026'
guide = case['reader_guide'][3]; boundary = case['theorems'][1]['boundary']
suffix = boundary[boundary.index(' Section 4.4 limits'):]
# These future after-bytes say independently reviewed ONLY conditionally. They
# must not be copied before the separately issued current-binding source V.
paragraph = r"The actual fixed-spectrum C4 geometry is also compiled and independently source-reviewed: for exactly \(d\ge2,\ \kappa\ge2\) and every full real \(O\), the same literal centered potential is globally \(C^\infty\), has genuine gradient derivative \(D(\nabla f_A)(x)=A\), is 1-strongly convex and \(\kappa\)-smooth, and has value zero uniquely at the origin. Its three direct kernel ASTIS parents are canonical actual admissibility, actual FirstOrder and the identical gradient-monotonicity strong-convexity converse; regularity, matrix/norm bounds and minimizer facts are outputs. A real private Test consumes the new geometry and canonical FirstOrder to prove the literal same-A ordered value/reply pair Borel measurable for each fixed hidden input. Fixed-input Borel measurability does not close joint-in-O or adaptive seed/history/transcript/output laws. The author's strict angle/cosine prefix and generic Hessian-criterion route remain separate source obligations; the implementation uses closed canonical admissibility and the canonical quantitative-gradient route. "
newguide = guide.replace('Remaining C4 calculus/minimizer, the strict historical angle/cosine route, moments/Krylov and all full lower-bound transports remain separate.', paragraph + 'Moments/Krylov and all full lower-bound transports remain separate.', 1)
newboundary = boundary.replace('Remaining C4 calculus/minimizer, strict historical angle/cosine route, Gaussian target-law/TV parameter transport, operational adaptive/seed/transcript/output simulation, deterministic/expected costs, finite-precision adapters and Krylov/moment/main-bound composition remain separate.', paragraph + 'Gaussian target-law/TV parameter transport, operational adaptive/seed/transcript/output simulation, deterministic worst-query caps and explicit expected-cost reductions, finite-precision adapters and Krylov/moment/main-bound composition remain separate.', 1)
assert newguide != guide and newboundary != boundary and newboundary.endswith(suffix)
raw = before[paths[4]]
for old, new in [(guide, newguide), (boundary, newboundary)]:
    raw = once(raw, json.dumps(old, ensure_ascii=False), json.dumps(new, ensure_ascii=False))
aftermodel = json.loads(raw)
maskedbefore = copy.deepcopy(model); maskedafter = copy.deepcopy(aftermodel)
for obj in [maskedbefore, maskedafter]:
    obj['cases'][4]['reader_guide'][3] = '<OWN>'
    obj['cases'][4]['theorems'][1]['boundary'] = '<OWN>'
assert maskedbefore == maskedafter
plans[paths[4]] = raw
plans[paths[5]] = f'''# {MODULE}

- This is a conditional integration payload for candidate `{HEAD}` and publication binding `{BINDING}`. Applying it requires a separately issued genuine current-binding source V, sole stabilization ownership and exact patch review. Preparation grants no source verdict or runtime reader acceptance.
- Sole public declaration: `actual_potential_geometry`, with exactly `d >= 2`, real `kappa >= 2`, and every full real orthogonal `O`, including either determinant sign. The literal half-node cosine-grid precision is `A = O diagonal(lambda) O^T`; the centered potential is `f(x) = x^T A x / 2` on all Euclidean space.
- Outputs: ordinary global C-infinity; the genuine real Frechet derivative of the Euclidean gradient equals the exact matrix continuous linear map A at every point; 1-strong convexity with modulus r-squared/2; kappa-Lipschitz gradient; f(0)=0; and global `IsMinOn` iff the point is zero, supplying existence and uniqueness.
- THREE direct kernel ASTIS producer parents, reused with their same canonical identities: `FixedSpectrumAdmissibility.actual_precision_admissible`, `FixedSpectrumFirstOrder.actual_first_order_query`, and `StrongConvexGradientConverse.strongConvexOn_of_gradient_inner_lower_bound`. Symmetry, spectral/quadratic bounds, derivative existence, induced Euclidean operator-norm control and minimizer facts are internal proof ingredients, not public premises.
- Genuine private Test `actual_first_order_oracle_measurable`: the new scalar smoothness and gradient-derivative outputs give continuity, canonical FirstOrder identifies the same actual precision reply, and the ordered pair `(f(x), A x)` is Borel measurable for each fixed O. Its TWO direct kernel ASTIS parents are Geometry and FirstOrder. The private Test is not a public or Registry node and does not prove joint-in-O or adaptive measurability.
- Seven authored formula steps, exact adjacent initially folded Lean and source correspondence remain in `website/content/declaration_lessons/huanjian-fixed-spectrum-geometry.json` and `website/content/publications/huanjian-fixed-spectrum-geometry.json`. Attribution: Zhou--Suzuki, arXiv2610.20492v1 Eq11, AppendixC.4 and Section2 exact-oracle/Borel context. The fixed-input Borel bridge is source-model background, not a numbered C4 assertion.
- The strict source angle/cosine prefix and author's generic Hessian-criterion route remain separate source obligations. The sufficient implementation route uses the already canonical closed admissibility envelope and quantitative-gradient converse, while producing the actual Hessian independently. No new conceptual transport is proposed; GraphMemory, Functor and the discovery ledger remain unchanged.
- Remaining: joint hidden-input/adaptive/private-seed/history/transcript/output-law lifting, actual Gaussian target/TV and finite-precision/arithmetic adapters, deterministic worst-query caps and explicit expected-cost reductions, moments/Krylov, both full main lower bounds, remote publication and postmerge purification/Exposition Seal. Main d/kappa/epsilon/delta ranges and Section4.4 limitations remain explicit in the unchanged source statements. A TV bound alone does not transfer an unbounded expected query cost.
'''.encode()
assert set(plans) == set(paths) and len(plans) == 6

states, discoveries = pure_replays()
assert states[ADV]['state'] == 'PROVED_LOCAL'
foreign = {k: v for k, v in states.items() if k != ADV}
frontiers = {str(q.relative_to(R)): sha(q.read_bytes()) for q in sorted((R / 'research-wiki/frontier-cells').glob('*.json'))}
models = ['website/content/graph_memory_index.json', 'website/content/functor_hypergraph.json',
          'Libraries/frontloaded-shared-spine.json', 'Libraries/conceptual-mirror-protocol.json',
          'website/content/source_correspondence.json']
protected = {}; tracked = {}
for row in cmd('git', 'ls-files', '--stage', '-z').split(b'\0'):
    if not row: continue
    meta, bpath = row.split(b'\t', 1); mode, blob, stage = meta.decode().split(); p = os.fsdecode(bpath)
    assert stage == '0'
    q = R / p
    raw = os.fsencode(os.readlink(q)) if q.is_symlink() else q.read_bytes()
    tracked[p] = {'sha256': sha(raw), 'git_index_blob': blob, 'mode': mode, 'raw_bytes': len(raw), 'symlink': q.is_symlink()}
    if p not in paths: protected[p] = tracked[p]
candidate_digest = source_digest({}); predicted_digest = source_digest(plans)
O.mkdir(parents=True)
rows = []; diff = b''
for i, p in enumerate(paths, 1):
    old = before[p]; new = plans[p]
    diff += ''.join(difflib.unified_diff((old or b'').decode().splitlines(keepends=True), new.decode().splitlines(keepends=True), fromfile='a/' + p, tofile='b/' + p)).encode()
    rows.append({'path': p, 'before_exists': old is not None,
                 'before_sha256': sha(old) if old is not None else None, 'planned_after_sha256': sha(new),
                 'before_archive': archive(f'path-{i}.before.raw.gz', old) if old is not None else None,
                 'planned_after_archive': archive(f'path-{i}.planned-after.raw.gz', new),
                 'before_CRLF': old.count(b'\r\n') if old else 0, 'after_CRLF': new.count(b'\r\n'),
                 'before_lone_LF': old.count(b'\n') - old.count(b'\r\n') if old else 0,
                 'after_lone_LF': new.count(b'\n') - new.count(b'\r\n')})
(O / 'exact-shared-proposal.diff').write_bytes(diff)
baseline = {'candidate': HEAD, 'all_tracked': tracked, 'protected_tracked': protected,
            'own_SAU_state': states[ADV], 'foreign_SAU_states': foreign, 'all_discovery_states': discoveries,
            'all_frontier_raw_hashes': frontiers, 'source_audit': {'path': audit_path, 'sha256': sha((R / audit_path).read_bytes()), 'state': audit['state'], 'verdict': audit['verdict']},
            'all_models_before': {p: sha((R / p).read_bytes()) for p in models},
            'preservation_rule': 'This proposal changes no shared bytes at all. A later actual independent source review/audit and normal sourceV/STAB must be separately authorized/pinned; they are not exceptions silently granted here. Every raw tracked baseline, own/foreign frontier, foreign SAU and discovery state is frozen.'}
baseline_ref = archive('protected-baseline.json.raw.gz', dump(baseline))
critical = []
critical_paths = list(pins['exact_inputs']) + [str((E / 'local-proof-capsule.json').relative_to(R)),
    str((E / 'full-review-input-pins.json').relative_to(R)), str((E / 'postproof-conceptual-mirror-audit.json').relative_to(R)),
    'research-wiki/frontier-cells/' + CELL + '.json', 'AGENTS.md', 'docs/theorem-publication-protocol.md',
    'docs/proof-digestion-protocol.md', 'docs/evidence-routed-memory-protocol.md', 'docs/samplewiki-reader-navigation.md',
    'tools/astis_site.py', 'tools/astis_advance.py', 'tools/astis_publication.py',
    'website/scripts/publication_reader.py', 'website/scripts/declaration_lessons.py', 'website/scripts/samplewiki_placements.py',
    '.astis/huanjian-gc-fixed-spectrum-geometry-20261109/KernelAndExactMeaning-v2.lean', *models]
for rec in receipts: critical_paths.extend([rec['receipt'], rec['raw_log']])
for i, p in enumerate(dict.fromkeys(critical_paths), 1):
    critical.append({'source': p, 'archive': archive(f'input-{i:02d}.raw.gz', (R / p).read_bytes())})
report = {'reviewer': '/root/geometry_integration_reader', 'state': 'CONDITIONAL_INTEGRATION_PREPARED_NOT_APPLIED_NOT_ACCEPTED',
          'candidate_commit': HEAD, 'candidate_source_digest': candidate_digest,
          'predicted_source_digest_after_exact_proposed_Lean_payloads': predicted_digest,
          'publication_binding_sha256': BINDING, 'sourceV_status': 'PENDING, separate actor; no source-fidelity verdict granted',
          'shared_paths': rows, 'shared_path_count': 6, 'formal_ASTIS_producer_parents': PARENTS,
          'private_Test_ASTIS_parents': [DECL, FIRST], 'no_private_Test_public_or_Registry_node': True,
          'administrative_count': '623 -> 624: exactly one genuinely new public Registry node; all three parents already exist once',
          'source_correspondence': 'Existing current-binding publication plus single authored lesson automatically project focused source reader, compact case index, source/proof and reviewed-placement links. source_correspondence.json has no Geometry row and needs no duplicate manually authored row.',
          'conditional_source_case_claim': 'Planned after-bytes say independently source-reviewed only under the unmet prerequisite of genuine same-binding source V. They are unapplied conditional text, not a current review verdict.',
          'source_case_edit_scope': ['cases[4].reader_guide[3]', 'cases[4].theorems[1].boundary'],
          'all_other_case_values_and_raw_prefix_suffix_preserved': True,
          'Section4_4_suffix_raw_sha256': sha(suffix.encode()), 'source_Test_lesson_publication_pins': pins['exact_inputs'],
          'historical_focused_receipts_actually_read': receipts,
          'historical_receipt_boundary': 'Successful focused build and proof-term inspector ran at preproof HEAD64497b46 with the now-pinned production/Test bytes. They are not current ab8 same-head aggregate/publication/site/graph/browser receipts.',
          'critical_raw_inputs': critical, 'protected_baseline': baseline_ref,
          'tracked_count': len(tracked), 'protected_tracked_count': len(protected), 'foreign_SAU_count': len(foreign), 'frontier_count': len(frontiers),
          'GraphMemory_Functor_discovery_ledger_unchanged': True, 'new_conceptual_transport': False,
          'diff_sha256': sha(diff), 'no_apply_build_browser_OS_network_model_sourceV_STAB_commit_API': True,
          'later_gates': ['Independent current-binding full-module/source review and normal source V by separate actor',
              'Sole root stabilization ownership and exact payload review/application',
              'Immutable actual integration core with official Lean/rootTests/fakeclosure and publication/contributor/semantic/frontier gates',
              'Actual same-head sitebuild/sitecheck/graphcheck and correct typed branch inspection',
              'New scoped Chrome/OS approval, actual desktop/mobile originals, old DensityAffinity DOM regressions and separate independent original-pixel acceptance',
              'Postmerge purification/Exposition Seal, remote acceptance and whole-Goal completion remain distinct'],
          'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
# Full final raw preservation readback. No shared write occurs in this script.
for p, x in tracked.items():
    q = R / p; raw = os.fsencode(os.readlink(q)) if q.is_symlink() else q.read_bytes()
    assert sha(raw) == x['sha256'], p
for p, raw in before.items(): assert ((R / p).read_bytes() if (R / p).exists() else None) == raw
assert cmd('git', 'rev-parse', 'HEAD').decode().strip() == HEAD
assert pure_replays() == (states, discoveries)
(O / 'proposal-report.json').write_bytes(dump(report))
archive('preparation-driver.py.raw.gz', Path(__file__).read_bytes())
freeze = {'state': report['state'], 'report_sha256': sha((O / 'proposal-report.json').read_bytes()),
          'files': [{'path': str(q.relative_to(R)), 'sha256': sha(q.read_bytes())} for q in sorted(O.iterdir()) if q.is_file()],
          'applied': False, 'sourceV_STAB_API_build_browser_acceptance': False}
(O / 'freeze.json').write_bytes(dump(freeze))
print(json.dumps({'report': str((O / 'proposal-report.json').relative_to(R)), 'report_sha256': sha((O / 'proposal-report.json').read_bytes()),
                  'freeze_sha256': sha((O / 'freeze.json').read_bytes()), 'diff_sha256': sha(diff),
                  'candidate_source_digest': candidate_digest, 'predicted_source_digest': predicted_digest,
                  'shared_paths': 6, 'tracked_protected': len(protected), 'applied': False}, indent=2))
