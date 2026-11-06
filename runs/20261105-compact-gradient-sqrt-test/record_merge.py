"""Record the actual accepted merge, not fresh main CI or purification."""
import hashlib
import json
from pathlib import Path
import subprocess
from tools.astis_advance import current_advances, transition_advance

advance='ASTIS-SA-20261105-CompactGradientSqrtTest'
actor='agent-task:/root'
merge='c843e133d42b8b904db3e78c0572c644908b7a59'
head='d7df928e3f6425811b5e7f4162f7647b08ca91b4'
state=current_advances()[advance]
assert state['state']=='STABILIZING' and state['latest_evidence']['integration_owner']==actor
subprocess.run(['git','merge-base','--is-ancestor',merge,'HEAD'],check=True)
trees=subprocess.check_output(['git','rev-parse',head+'^{tree}',merge+'^{tree}']).decode().splitlines()
assert len(set(trees))==1
ledger=Path('runs/substantive_advances.jsonl');prefix=ledger.read_bytes()
assert hashlib.sha256(prefix).hexdigest()=='1847e0164eaf3a6498ac9de42d75f3c44f386c8c9a5b0d2019297e95986352f2'
transition_advance(advance,'MERGED',worker_id=actor,evidence={
    'pr':'https://github.com/DakeBU/Automization-Sampling-Optimisation-Geometry-Lib/pull/381',
    'commit':merge,'exact_head':head,'source_tree':trees[0],
    'accepted_checks':[42058868210,42058867735,42058867863,42058867764,42058867747,42058858610],
    'gate':'All six current exact-head checks actually succeeded before merge. Accepted head and merge trees agree; not relabelled as fresh main compilation.',
    'local':'Root Tests9632 with temporary LEAN_NUM_THREADS=1, ASTIS check, site608/12/1100/5260, fresh graph check and actual desktop/mobile formula/folded-Lean/copy/graph PNG inspection pass.29 QA/recursive contexts unchanged. Parallel Windows read failures retained; cause not proved.',
    'remaining':'Main CI/Pages, actual public readback, independent helper-only purification/Exposition Seal. Full Exercise1.7 and real Agentic Lean/model acceptance remain OPEN.',
})
after=ledger.read_bytes();assert after.startswith(prefix)
suffix=after[len(prefix):]
assert b'\r\n' not in suffix and len(suffix.splitlines())==1
print(json.dumps({'state':'MERGED','commit':merge,'tree':trees[0],
    'preserved_prefix_bytes':len(prefix),'preserved_prefix_sha256':hashlib.sha256(prefix).hexdigest(),
    'event_sha256_raw':hashlib.sha256(suffix).hexdigest()}))
