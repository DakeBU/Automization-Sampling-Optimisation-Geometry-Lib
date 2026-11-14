"""Milestone ownership observation after an actual foreground fetch; no takeover."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import subprocess
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
refs=[]
for ref in ['origin/main','origin/codex/slc-lsi-weighted-radial-mgf-release']:
    commit=subprocess.check_output(['git','rev-parse',ref]).decode().strip()
    raw=subprocess.check_output(['git','show',f'{commit}:runs/substantive_advances.jsonl'])
    states=advance._replay_advances([json.loads(x) for x in raw.splitlines()])
    own=states['ASTIS-SA-20261110-SlcLsiWeightedRadialMGF']
    refs.append({'ref':ref,'commit':commit,'ledger_sha256':hashlib.sha256(raw).hexdigest(),
        'original_owner_state':own['state'],'original_owner_id':own.get('worker_id',own.get('owner_id')),
        'active_stabilizing':[k for k,v in states.items() if v['state']=='STABILIZING']})
record={'checked_utc':datetime.now(timezone.utc).isoformat(),
    'actual_fetch':{'command':['git','fetch','origin'],'start_tool_chunk':'d0e9d4','completion_tool_chunk':'4cb50e','exit_code':0},
    'refs':refs,'decision':'Preserve user choice: original owner must finish and release. Observation alone grants no takeover/shared integration or original-reader acceptance.'}
p=Path(__file__).resolve().parent/'original-owner-after-R9-VERIFIED.json'
with p.open('x') as f:f.write(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record))
