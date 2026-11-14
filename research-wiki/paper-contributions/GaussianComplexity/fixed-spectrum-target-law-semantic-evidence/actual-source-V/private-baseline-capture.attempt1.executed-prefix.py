from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json,subprocess,sys,base64,os,stat
sys.dont_write_bytecode=True
from tools import astis_advance as adv
root=Path('.astis/semantic-neutral-20261110/tl_src_e028af').resolve();pub=root/'normal-sourceV';priv=root/'PRIVATE-normal-sourceV-baseline';priv.mkdir(exist_ok=False)
aid='ASTIS-SA-20261110-GaussianComplexityFixedSpectrumTargetLaw'
cp='research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-target-law.json'
ledger=Path('runs/substantive_advances.jsonl');raw=ledger.read_bytes();assert raw.endswith(b'\n')
records=[json.loads(x) for x in raw.splitlines() if x.strip()]
states=adv._replay_advances(records);own=states[aid];foreign={k:v for k,v in states.items() if k!=aid}
assert len(foreign)==296 and own['state']=='PROVED_LOCAL' and own['owner_id']=='huanjian_gc_20261110_fixed_spectrum_target_law'
priorV=[x for x in records if x.get('event')=='transition' and x.get('to_state')=='VERIFIED']
assert len(priorV)==9
