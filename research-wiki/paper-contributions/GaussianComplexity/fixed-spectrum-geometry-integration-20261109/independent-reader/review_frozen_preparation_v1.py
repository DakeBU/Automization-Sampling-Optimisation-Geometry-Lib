"""Independent post-freeze byte readback. No application, gate or browser execution."""
from pathlib import Path
import ast, copy, datetime, gzip, hashlib, json, os, subprocess
R = Path('/Users/zhouhuanjian/ASTIS-GC')
S = R / '.astis/huanjian-gc-fixed-spectrum-geometry-integration-20261109/independent-reader'
P = S / 'conditional-proposal-v1'
B = S / 'conditional-browser-preparation-v1'
OUT = S / 'conditional-static-readback-v1.json'
assert not OUT.exists()
sha = lambda b: hashlib.sha256(b).hexdigest()
def raw_archive(ref):
    compressed = (R / ref['path']).read_bytes()
    assert sha(compressed) == ref['gzip_sha256']
    raw = gzip.decompress(compressed); assert sha(raw) == ref['raw_sha256']
    return raw
report_raw = (P / 'proposal-report.json').read_bytes()
assert sha(report_raw) == '6f9045472dc9f11da494942d065b093efab12c2cf385f6d83a379ad771a5e904'
report = json.loads(report_raw)
freezes = []
for folder in [P, B]:
    frozen = json.loads((folder / 'freeze.json').read_bytes())
    for row in frozen['files']: assert sha((R / row['path']).read_bytes()) == row['sha256'], row['path']
    freezes.append({'path': str((folder / 'freeze.json').relative_to(R)), 'sha256': sha((folder / 'freeze.json').read_bytes())})
before = {}; after = {}
for row in report['shared_paths']:
    p = row['path']
    before[p] = raw_archive(row['before_archive']) if row['before_exists'] else None
    after[p] = raw_archive(row['planned_after_archive'])
    assert (sha(before[p]) if before[p] is not None else None) == row['before_sha256']
    assert sha(after[p]) == row['planned_after_sha256']
    assert ((R / p).read_bytes() if (R / p).exists() else None) == before[p]
    if before[p] is not None: assert before[p].count(b'\r\n') == after[p].count(b'\r\n')
assert len(after) == 6
for path, added in [('AutoSamplingTheory.lean', b'import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry\n'),
                    ('Tests.lean', b'import Tests.GaussianComplexityFixedSpectrumGeometry\n')]:
    assert after[path].count(added) == 1 and after[path].replace(added, b'', 1) == before[path]
basic = 'Tests/Basic.lean'
assert after[basic].replace(b'formalizedTechnicalLemmaCount = 624', b'formalizedTechnicalLemmaCount = 623', 1) == before[basic]
registry = 'AutoSamplingTheory/TechnicalLemmas/Registry.lean'
entry_start = after[registry].index(b'  {\n    key := "gaussian-complexity.fixed-spectrum-geometry",')
entry_end = after[registry].index(b'  {\n    key := "gaussian-complexity.single-block-separation",', entry_start)
entry = after[registry][entry_start:entry_end]
assert entry.count(b'localDecl :=') == 1 and b'actual_first_order_oracle_measurable' not in entry
assert after[registry].replace(entry, b'', 1).replace(b'import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumGeometry\n', b'', 1) == before[registry]
assert after[registry].count(b'status := LemmaMemoryStatus.formalizedLocal') == 624
casefile = 'website/content/samplewiki_companion_frontiers.json'
old = json.loads(before[casefile]); new = json.loads(after[casefile]); reverse = after[casefile]
changes = []
for key in ['reader_guide', 'boundary']:
    a = old['cases'][4]['reader_guide'][3] if key == 'reader_guide' else old['cases'][4]['theorems'][1]['boundary']
    b = new['cases'][4]['reader_guide'][3] if key == 'reader_guide' else new['cases'][4]['theorems'][1]['boundary']
    assert a != b
    before_token = json.dumps(a, ensure_ascii=False).encode(); after_token = json.dumps(b, ensure_ascii=False).encode()
    assert reverse.count(after_token) == 1; reverse = reverse.replace(after_token, before_token, 1)
    for phrase in ['strict angle/cosine prefix', 'generic Hessian-criterion route', 'Borel measurable for each fixed hidden input', 'joint-in-O']:
        assert phrase in b
    changes.append(key)
assert reverse == before[casefile]
case = new['cases'][4]
assert case['theorems'][0] == old['cases'][4]['theorems'][0]
for n in [0, 1]:
    for key in ['assumptions', 'formula', 'steps', 'statement']:
        assert case['theorems'][n][key] == old['cases'][4]['theorems'][n][key]
assert 'd >= 1, kappa >= 4, and 0 < epsilon <= 1/16' in ' '.join(case['theorems'][0]['assumptions'])
assert 'delta in (0,1)' in ' '.join(case['theorems'][1]['assumptions'])
assert '2 <= kappa <= d^(1-delta), and 0 < epsilon <= 1/10' in ' '.join(case['theorems'][1]['assumptions'])
for theorem in case['theorems']:
    assumptions = ' '.join(theorem['assumptions'])
    for phrase in ['Exact matrix-vector access', 'input-independent random seed', 'deterministic cap', 'TV with normalization']:
        assert phrase in assumptions
assert new['execution'] == old['execution']
assert case['theorems'][1]['boundary'].split(' Section 4.4 limits', 1)[1] == old['cases'][4]['theorems'][1]['boundary'].split(' Section 4.4 limits', 1)[1]
baseline = json.loads(raw_archive(report['protected_baseline']))
assert len(baseline['all_tracked']) == 125851 and len(baseline['protected_tracked']) == 125846
for p, row in baseline['all_tracked'].items():
    q = R / p; raw = os.fsencode(os.readlink(q)) if q.is_symlink() else q.read_bytes()
    assert sha(raw) == row['sha256'], p
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R).decode().strip() == report['candidate_commit']
assert not subprocess.check_output(['git', 'diff', '--name-only'], cwd=R)
assert not subprocess.check_output(['git', 'diff', '--cached', '--name-only'], cwd=R)
source_audit = json.loads((R / baseline['source_audit']['path']).read_bytes())
assert source_audit['state'] == 'blind-reconstructed' and source_audit['verdict'] == 'pending'
lesson = json.loads((R / 'website/content/declaration_lessons/huanjian-fixed-spectrum-geometry.json').read_bytes())['units'][0]
assert len(lesson['steps']) == 7 and lesson['reading_layout'] == 'progressive'
assert lesson['astis_dependencies'] == report['formal_ASTIS_producer_parents']
browser_report = json.loads((B / 'preparation-report.json').read_bytes())
checker = (S / 'check_final_reader_v1.py').read_bytes(); common = (S / 'geometry_browser_common_v1.py').read_bytes()
assert sha(checker) == browser_report['checker_sha256'] and sha(common) == browser_report['common_sha256']
compile(checker, '<unexecuted-new-Geometry-checker>', 'exec'); compile(common, '<unexecuted-new-Geometry-common>', 'exec')
out = {'state': 'ACCEPTED_SCOPED_CONDITIONAL_PREPARATION_ONLY', 'reviewer': '/root/geometry_integration_reader',
    'candidate_commit': report['candidate_commit'], 'proposal_report_sha256': sha(report_raw), 'frozen_proposals': freezes,
    'sourceV_status': 'PENDING distinct source reviewer; no fidelity/VERIFIED transition granted here',
    'exact_payload_scope': 'Six paths, one public new node, existing623->624 count, no private Test node; all three canonical parents already present.',
    'source_correspondence': 'One existing authored lesson/publication binding; generated source reader/index/placement already derives from these inputs. No source_correspondence.json duplicate.',
    'static_reader_review': {'seven_steps': ['same quadratic and global smoothness', 'genuine gradient derivative', 'closed quadratic bounds from canonical admissibility', 'same quantitative-gradient strong-convexity converse', 'Euclidean Rayleigh/operator norm and gradient Lipschitz bound', 'zero value and unique global minimizer', 'genuine fixed-input actual Borel reply consumer'],
        'assumptions_preserved': 'Exactly local d>=2,kappa>=2/full real O of either determinant sign; literal source f/A and all points/pairs; geometric certificates are outputs.',
        'source_vs_implementation': 'Strict source angle/cosine prefix and author generic Hessian-criterion route remain separate source obligations. Current implementation route uses actual canonical closed admissibility and quantitative-gradient converse.',
        'navigation_plan': 'Single SampleWiki case -> compact source-mapped index -> source-huanjian-fixed-spectrum-geometry.html and canonical lesson; adjacent closed exact statement/proof Lean; exact owning module/download/current Git; canonical declaration/module/three parent native graph clicks.',
        'main_contracts_preserved': 'Both full lower bounds open; determinant d>=1,kappa>=4,0<epsilon<=1/16; eigenbasis fixed delta in(0,1), d>=d0(delta),2<=kappa<=d^(1-delta),0<epsilon<=1/10. Exact matvec/value-gradient model, Borel seed/history and every-input/every-seed deterministic cap, uniform normalized TV retained. Expected-cost reduction remains separate.',
        'actual_visual_or_runtime_acceptance': False},
    'lossless_preservation': {'tracked_raw_files_checked': len(baseline['all_tracked']), 'all_protected_and_proposed_current_shared_bytes_unchanged': True,
        'case_only_two_scalar_tokens_change_in_proposal': changes, 'old_completed_theorem0_all_bytes_values': 'preserved',
        'all_other_case_values_execution_frontier_queue': 'preserved', 'Section4_4_suffix': 'exact',
        'GraphMemory_Functor_source_correspondence_discovery_ledger': 'unchanged exact baseline', 'raw_CRLF_bytes_normalized': False},
    'browser_helper_review': {'syntax_only': True, 'unexecuted_checker_sha256': sha(checker), 'unexecuted_common_sha256': sha(common),
        'future_real_records_required': True, 'planned_original_PNGs': 44, 'planned_native_geometry_rows': 12,
        'old_DensityAffinity_DOM_regressions': 2, 'old_native_geometry_and_DensityAffinity_blocks_retained_exactly': True,
        'old_FirstOrder_conceptual_view': 'Unchanged regression only; no Geometry model incidence or new transport',
        'script_PASS_does_not_accept_pixels': True, 'old_OS_command_prefix_reused': False},
    'pending': ['Root exact patch/helper inspection', 'Distinct genuine current-binding sourceV', 'Sole stabilization and actual immutable core official Lean/publication/site/graph gates',
        'New scoped Chrome/OS approval', 'Actual desktop/mobile originals and separate independent image acceptance', 'Postmerge purification/Exposition Seal and remote acceptance'],
    'no_shared_edits_API_sourceV_STAB_build_browser_OS_network_model_commit': True,
    'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
OUT.write_bytes((json.dumps(out, ensure_ascii=False, indent=2) + '\n').encode())
print(json.dumps({'report': str(OUT.relative_to(R)), 'sha256': sha(OUT.read_bytes()), 'status': out['state'],
    'proposal_applied': False, 'sourceV_issued': False, 'browser_executed': False}, indent=2))
