from pathlib import Path
import json
out = Path('runs/20261007-companion-priority/pbps-unit-exponential-product77/integration77')
p = Path('website/content/samplewiki_companion_frontiers.json')
before = (out / '4.before.exactraw.snapshot').read_bytes()
desired = json.loads(before)
desired['execution']['updated'] = '2026-10-10'
desired['execution']['current_checkpoint'] = 'docs/companion-papers-handoff.md#actual-countable-exponential-inputs-2026-10-10'
assert json.loads(p.read_bytes()) == desired
raw = before.replace(b'"updated": "2026-10-08"', b'"updated": "2026-10-10"', 1)
raw = raw.replace(b'docs/companion-papers-handoff.md#exact-finite-pbps-jump-recursion-2026-10-10',
                  b'docs/companion-papers-handoff.md#actual-countable-exponential-inputs-2026-10-10', 1)
assert json.loads(raw) == desired
temp = p.with_suffix('.sau77.tmp')
assert not temp.exists()
temp.write_bytes(raw)
temp.replace(p)
print('Preserved original execution JSON bytes except the two intended field values.')
