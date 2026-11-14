"""Observe current remote ledger ownership after the actual foreground fetch."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as advance

observations = []
for ref in ['origin/main', 'origin/codex/slc-lsi-weighted-radial-mgf-release']:
    commit = subprocess.check_output(['git', 'rev-parse', ref]).decode().strip()
    raw = subprocess.check_output(['git', 'show', f'{commit}:runs/substantive_advances.jsonl'])
    states = advance._replay_advances([json.loads(line) for line in raw.splitlines()])
    original = states['ASTIS-SA-20261110-SlcLsiWeightedRadialMGF']
    observations.append({
        'ref': ref, 'commit': commit, 'ledger_sha256': hashlib.sha256(raw).hexdigest(),
        'original_owner_state': original['state'],
        'original_owner_id': original.get('worker_id', original.get('owner_id')),
        'active_stabilizing': [key for key, value in states.items() if value['state'] == 'STABILIZING'],
    })
record = {
    'checked_utc': datetime.now(timezone.utc).isoformat(),
    'actual_fetch': {'command': ['git', 'fetch', 'origin'], 'tool_chunk': 'fc26f0', 'exit_code': 0},
    'refs': observations,
    'interpretation': 'Wait for the original owner to complete and release. No takeover or shared integration from this observation.',
}
path = Path(__file__).resolve().parent / 'latest-original-owner-after-math-candidate.json'
with path.open('x') as out:
    out.write(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(record))
