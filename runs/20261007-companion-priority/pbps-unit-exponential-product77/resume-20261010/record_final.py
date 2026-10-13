"""Record exact local acceptance and the remaining reader boundary."""
from pathlib import Path
import datetime
import hashlib
import json
import sys
root = Path.cwd()
run = Path('runs/20261007-companion-priority/pbps-unit-exponential-product77')
out = run / 'integration77'
def pin(p):
    p = Path(p)
    raw = p.read_bytes()
    return {'path': p.as_posix(), 'RAW_bytes': len(raw), 'RAW_sha256': hashlib.sha256(raw).hexdigest()}
labels = ['canonical-lean-gate', 'python-compile', 'contributor', 'publication', 'semantic',
          'frontier', 'site-build', 'underlying-graph', 'graph-check', 'site-check', 'diff-check']
checks = []
for label in labels:
    p = out / label / 'receipt.json'
    receipt = json.loads(p.read_bytes())
    assert receipt['terminal_closed'] and receipt['exit_code'] == 0, label
    checks.append({'label': label, 'receipt': pin(p), 'stdout': receipt['stdout'], 'stderr': receipt['stderr']})
sys.path.insert(0, str(root / 'tools'))
sys.path.insert(0, str(root / 'website/scripts'))
import astis_site
import astis_advance as advance
import publication_reader
import underlying_lean_graph
gate = json.loads(Path('.astis/site-lean-gate.json').read_bytes())
assert gate['passed'] and gate['source_digest'] == astis_site.source_digest()
graph = json.loads(Path('_site/data/underlying-lean-graph.json').read_bytes())
assert graph['publication_inputs_sha256'] == publication_reader.graph_input_digest()
underlying_lean_graph.validate(Path('_site'), graph)
decl = 'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws'
assert any(n.get('id') == 'decl:' + decl for n in graph['nodes'])
assert advance.current_advances()['ASTIS-SA-20261010-UnitExponentialProduct']['state'] == 'VERIFIED'
lanes = [s['advance_id'] for s in advance.current_advances().values() if s['state'] == 'STABILIZING']
assert lanes == ['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
admin = json.loads((out / 'final-admin.json').read_bytes())
note = {
    'status': 'LOCAL_SHARED_AGGREGATE_AND_GENERATED_READER_GATES_PASS_VISUAL_PENDING',
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'science_commit': '4f88383540a865aea304c63c40de5a699ea61611',
    'independent_verifier': '/root/exact_verify77',
    'verification': pin(run / 'exact-commit-verification77/verified.json'),
    'root_jobs': admin['root_jobs'], 'test_jobs': admin['test_jobs'], 'registry_count': 526,
    'publication_units': 247, 'checks': checks,
    'lean_source_digest': gate['source_digest'],
    'publication_inputs_sha256': graph['publication_inputs_sha256'],
    'current_graph': pin('_site/data/underlying-lean-graph.json'),
    'graph_delta': 'One canonical actual unit-Exp infinite-product declaration with actual Mathlib product/distribution/independence/SLLN dependencies. Future PBPS clock consumer is not presented as an existing formal edge. No conceptual mirror.',
    'actual_visual_inspection': {
        'static_svg': pin('docs/module-graph.svg'),
        'static_raster': pin(out / 'static-svg/module-graph.png'),
        'static_svg_viewed_by_root': True,
        'observation': 'Shared-root hierarchy, source layers, labels and legend readable. Coarse SVG omits individual new leaf; generated exact branch is a separate view.',
        'browser_page_and_interactive_branch': 'pending; discovered browser surface has no inspectable tab; open_in_codex queued but no page inspection occurred',
        'full_Exposition_Seal': False,
    },
    'sole_stabilization_owner': lanes[0],
    'state_distinctions': {'proved_locally': True, 'independently_verified': True,
        'local_aggregate_and_generated_site_gates': True, 'stabilized': False,
        'merged': False, 'purified': False, 'live_verified': False, 'main_theorem_complete': False},
    'remaining': ['Actual event-time nonaccumulation composition is next; source-only preread/header review separate.',
        'Global physical-time process, Markov/invariance/kernel/hypocoercivity/main/errors/cost/composition remain open.',
        'Author direct Exp integrability/mean-one SLLN route remains an OPEN alternative.',
        'Actual page/interactive branch visual acceptance, full Exposition Seal, main merge/live and postmerge purification remain open.'],
    'Goal_complete': False,
}
p = run / 'integration.notes.json'
assert not p.exists()
p.write_text(json.dumps(note, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
print('Recorded source-bound local aggregate and current generated graph/site acceptance; visual and canonical stabilization remain pending.')
