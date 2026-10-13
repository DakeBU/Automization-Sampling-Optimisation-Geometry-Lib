import json,re
from pathlib import Path
P=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-sharp-energy68/focused-build68-v1');x=json.loads((P/'receipt.json').read_text(encoding='utf-8'));print(json.dumps({k:v for k,v in x.items() if not isinstance(v,(dict,list))},ensure_ascii=False));t=(P/'stdout.log').read_text(encoding='utf-8');print(t[-2400:]);print('keys',list(x))
