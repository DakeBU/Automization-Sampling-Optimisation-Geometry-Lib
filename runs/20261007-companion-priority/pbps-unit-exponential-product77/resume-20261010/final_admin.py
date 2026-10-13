"""Record passed aggregate evidence before freezing current site inputs."""
from pathlib import Path
import hashlib
import json
import re
run = Path('runs/20261007-companion-priority/pbps-unit-exponential-product77')
out = run / 'integration77'
receipt = json.loads((out / 'canonical-lean-gate/receipt.json').read_bytes())
assert receipt['exit_code'] == 0 and receipt['terminal_closed']
jobs = [int(s) for s in re.findall(r'Build completed successfully \((\d+) jobs\)',
    (out / 'canonical-lean-gate/stdout.log').read_text(encoding='utf8'))]
assert len(jobs) == 2
cp = Path('research-wiki/frontier-cells/ASTIS-SHARED-unit-exponential-product.json')
before = cp.read_bytes()
assert not (out / 'cell.before-final-admin.snapshot.json').exists()
(out / 'cell.before-final-admin.snapshot.json').write_bytes(before)
cell = json.loads(before)
assert cell['status'] == 'independently_verified'
cell['evidence']['serialized_shared_gate'] = {
    'evidence': (out / 'canonical-lean-gate/receipt.json').as_posix(),
    'root_jobs': jobs[0], 'test_jobs': jobs[1], 'registry_count': 526,
    'status': 'PASS', 'proof_commit': '4f88383540a865aea304c63c40de5a699ea61611',
    'scope': 'Current local aggregate with exact independently verified science; pending main/live/purification and browser visual acceptance remain distinct.',
}
cell['graph_contribution']['visual_review'] = (
    'Static module SVG rasterized with bundled sharp and actually viewed by /root; readable shared-root labels/directions/legend. '
    'This coarse diagram does not display the new leaf individually. Exact declaration branch generated/checked separately. '
    'Browser runtime discovered only an empty MCP Apps surface; no inspectable page/graph tab, so actual page and interactive branch visual acceptance remain pending.')
cell['blocked'] = {'status': False, 'reason':
    'Input-law leaf independently verified and full local aggregate passed. Site/graph checks and actual page visual acceptance remain separate; actual clock nonaccumulation/process/invariance/main/cost/composition remain open.'}
cp.write_text(json.dumps(cell, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
p = Path('docs/companion-papers-handoff.md')
raw = p.read_bytes()
old = b'Serialized aggregate/publication/site/graph/visual checks are pending for this\nintegration candidate.'
nl = b'\r\n' if b'\r\n' in raw else b'\n'
old = old.replace(b'\n', nl)
assert raw.count(old) == 1
new = (f'Current local aggregate77 passed: root{jobs[0]}, Tests{jobs[1]}, Registry526,\n'
       'ATLAS check and fake-closure scan; tools/astis.py py_compile also passed.\n'
       'Publication/site/graph checks are recorded in77 integration.notes.json.\n'
       'Static module SVG was viewed; browser page/interactive branch visual\n'
       'acceptance is pending because no inspectable browser tab is available.').encode().replace(b'\n', nl)
p.write_bytes(raw.replace(old, new, 1))
(out / 'final-admin.json').write_text(json.dumps({
    'root_jobs': jobs[0], 'test_jobs': jobs[1], 'registry_count': 526,
    'cell_sha256': hashlib.sha256(cp.read_bytes()).hexdigest(),
    'static_svg_viewed_by_root': True, 'browser_page_visual_pending': True,
    'source_statement_proof_and_lesson_unchanged': True, 'Goal_complete': False,
}, indent=2) + '\n', encoding='utf8')
print(f'Local aggregate passed root{jobs[0]}/Tests{jobs[1]}; final site inputs ready, browser visual pending.')
