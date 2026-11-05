"""Capture observed local checks; never substitute for clean CI or public QA."""
import hashlib
import json
from pathlib import Path
import subprocess

from tools import astis_contributor_contract as contract
from tools import astis_publication as publication
from tools import sog_bench as bench
from tools import sog_bench_review as review

RUN = Path('runs/20261105-compact-gradient-sqrt-test')
CACHE = Path('.astis/sog-bench')
NAME = ('AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.'
        'CompactGradientSqrtPerturbation.'
        'eventually_contDiff_and_integrable_sqrt_perturbation')
CELL = 'ASTIS-SHARED-compact-gradient-sqrt-test-data'

publication.check_advance([NAME], reviewed=True)
errors = contract.validate_targets({NAME}, publication.load(),
                                  publication.inputs(), {CELL})
assert not errors, errors
preserved = json.loads((RUN/'qa-binding-preservation.json').read_text())
current = {c['id']: {'binding': c['binding_sha256'],
                     'context': review.context_binding(c)}
           for c in bench.materialize()}
assert current == preserved['before'] == preserved['after']
reader = json.loads(Path('_browser-evidence/compact-gradient-sqrt/report.json').read_text())
assert reader['steps'] == 6 and reader['actual_math_rendered']
assert reader['initially_folded_lean_highlight_copy']
assert reader['actual_graph_focus'] and not reader['runtime_errors']

logs = {}
for name, expected in [
    ('compact-gradient-sqrt-root-tests-retry.log', 'Build completed successfully (9613 jobs).'),
    ('compact-gradient-sqrt-astis.log', 'Build completed successfully (9271 jobs).'),
    ('compact-gradient-sqrt-site-build.log', '597 compiled local leaves'),
    ('compact-gradient-sqrt-site-check.log', 'ASTIS site check passed'),
]:
    raw = (CACHE/name).read_bytes()
    assert expected in raw.decode('utf-8-sig', errors='strict'), name
    logs[name] = {'sha256': hashlib.sha256(raw).hexdigest(),
                  'observed_success_marker': expected}

protected = {}
for path, expected in [
    ('AutoSamplingTheory/TechnicalLemmas/Probability/KernelReversibilityTransport.lean',
     'bf79413b618fbcf5315b058f605e22e58f211f783bcee51127cd1f9bcbb0a54d'),
    ('Tests/KernelReversibilityTransport.lean',
     '72480ff8b269a31eec74d7606f223d10149480dc35375d28c36f7e5f3c60a67d'),
]:
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    assert digest == expected, path
    protected[path] = digest

result = {
    'scope': 'Local serial integration, not fresh clean CI, merge, deployment, QA admission or purification',
    'verified_code_commit': 'eead411ec020bb34ad18208d3453067e8905c0a6',
    'registry_candidate': 597,
    'scoped_publication_reviewed': True, 'scoped_contributor': True,
    'preserved_qa_cores': len(current), 'changed_qa_or_recursive_context': [],
    'browser': reader, 'log_bindings': logs,
    'protected_untracked_files_unchanged': protected,
    'full_local_publication_and_contributor': 'FAIL solely on protected untracked KernelReversibilityTransport missing publication; never hide or stage it',
    'initial_root_failure': 'RCLike Basic.olean read failed; file existed, cache get downloaded nothing. Serial direct calculus/root retry pass; cause unestablished.',
    'visual_inspection': 'Root opened statement, formula/mobile, exact highlighted/copyable Lean and actual selected graph SVG PNGs, desktop and mobile. Neighboring graph nodes use pan/zoom; long formulas/code scroll, not page overflow.',
    'remaining': 'Clean exact-head CI, actual merge/Pages readback and independent helper-only purification/Exposition Seal. Full Exercise1.7 and Agentic Lean native acceptance remain open.',
}
(RUN/'integration-evidence.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'scoped_checks': 'PASS', 'preserved_cores': len(current),
                  'registry_candidate': 597, 'protected_files': len(protected)}))
