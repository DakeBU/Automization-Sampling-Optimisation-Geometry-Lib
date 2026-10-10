"""Refresh existing module graph views and the one admitted module card."""
from pathlib import Path
import hashlib
import json
import sys

sys.path.insert(0, str(Path.cwd() / 'tools'))
import astis as a
import astis_advance as advance

run = Path('runs/20261007-companion-priority/pbps-actual-small-time-continuity82')
claim = json.loads((run / 'claim.json').read_bytes())
assert advance.current_advances()[claim['advance_id']]['state'] == 'VERIFIED'
assert [s['advance_id'] for s in advance.current_advances().values() if s['state'] == 'STABILIZING'] == ['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
out = run / 'integration82/affected-graph'
out.mkdir(exist_ok=False)
records = a.lean_module_records()
name = 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualSmallTimeContinuity'
selected = [x for x in records if x['module'] == name]
assert len(selected) == 1
graph = a.arsenal_module_graph_svg(records)
payload = {'generated': a.now_stamp(), 'module_graph_svg': 'docs/module-graph.svg',
           'ledger': a.rel(a.SAMPLING_LIBRARY_DIR / 'lean-leaf-module-graph.md'), 'modules': records}
targets = {
    Path('docs/module-graph.svg'): graph,
    Path('docs/assets/astis_lean_arsenal_module_graph.svg'): graph,
    a.SAMPLING_LIBRARY_DIR / 'lean-leaf-module-graph.md': a.arsenal_module_graph_markdown(records),
    a.RETRIEVAL_INDEX_DIR / 'astis-lean-arsenal-module-graph.json': json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + '\n',
    a.SAMPLING_LIBRARY_DIR / 'cards' / f'{a.slugify(name)}.md': a.arsenal_module_card_text(selected[0]),
}
rows = []
for i, (p, text) in enumerate(targets.items()):
    if p.exists():
        (out / f'{i}.before.exactraw.snapshot').write_bytes(p.read_bytes())
    text = '\n'.join(line.rstrip(' \t\r') for line in text.split('\n'))
    p.write_text(text, encoding='utf8', newline='\n')
    raw = p.read_bytes()
    rows.append({'path': p.as_posix(), 'RAW_sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)})
(out / 'receipt.json').write_text(json.dumps({
    'status': 'generated-visual-pending', 'outputs': rows,
    'existing_pure_generators': True, 'canonical_tool_source_changed': False,
    'unrelated_cards_changed': False, 'Goal_complete': False,
}, indent=2) + '\n', encoding='utf8')
print('Generated existing module graph views and one ActualSmallTimeContinuity card; visual review pending.')
