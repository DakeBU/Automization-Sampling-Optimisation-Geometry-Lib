from datetime import datetime,timezone
from pathlib import Path
import json,subprocess,hashlib,sys
sys.dont_write_bytecode=True
sys.path.insert(0,'tools')
import astis_advance as advance
refs=[]
for ref in ['origin/main','origin/codex/slc-lsi-weighted-radial-mgf-release']:
    commit=subprocess.check_output(['git','rev-parse',ref]).decode().strip()
    raw=subprocess.check_output(['git','show',f'{commit}:runs/substantive_advances.jsonl'])
    states=advance._replay_advances([json.loads(x) for x in raw.splitlines()])
    own=states['ASTIS-SA-20261110-SlcLsiWeightedRadialMGF']
    refs.append({'ref':ref,'commit':commit,'ledger_sha256':hashlib.sha256(raw).hexdigest(),'original_owner_state':own['state'],'original_owner_id':own.get('worker_id',own.get('owner_id')),'active_stabilizing':[k for k,v in states.items() if v['state']=='STABILIZING']})
record={'checked_utc':datetime.now(timezone.utc).isoformat(),'actual_foreground_fetch':{'command':['git','fetch','origin'],'tool_chunk':'8f8601','exit_code':0},'refs':refs,'decision':'Original owner remains unreleased. Preserve user-selected finish-and-release route; no shared integration, CSS edit or takeover authorized by this observation.'}
p=Path(__file__).resolve().parent/'original-owner-at-resume.json'
with p.open('x') as f:f.write(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(record))
