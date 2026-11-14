from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, subprocess, sys
sys.dont_write_bytecode = True
sys.path.insert(0, 'tools')
import astis_advance as adv
rows = []
for ref in ['origin/main', 'origin/codex/slc-lsi-weighted-radial-mgf-release']:
    head = subprocess.check_output(['git', 'rev-parse', ref], text=True).strip()
    raw = subprocess.check_output(['git', 'show', head+':runs/substantive_advances.jsonl'])
    states = adv._replay_advances([json.loads(z) for z in raw.splitlines()])
    rows.append({'ref': ref, 'commit': head, 'ledger_sha256': hashlib.sha256(raw).hexdigest(),
                 'stabilizing': [{'advance_id': a, 'owner_id': x.get('owner_id'), 'state': x['state']} for a, x in states.items() if x['state'] == 'STABILIZING']})
x = {'observed_utc': datetime.now(timezone.utc).isoformat(),
     'after_real_git_fetch_origin': True, 'local_complete_sourceV_carry': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
     'refs': rows, 'scope': 'Read-only observation at a completed mathematical packet. Merged PR is not a normal ledger release; no takeover or shared integration.'}
p = Path(__file__).parent/'latest-owner-after-complete-cosine-gram-sourceV-carry.json'
with p.open('x') as f:
    json.dump(x, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(json.dumps(x))
