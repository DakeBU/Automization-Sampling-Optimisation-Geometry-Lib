from pathlib import Path
import subprocess,json,hashlib
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81');rows=[]
for file,key,identity in [('runs/substantive_advances.jsonl','advance_id','ASTIS-SA-20261010-PBPSIdealHalfTurnKernel'),('runs/substantive_discoveries.jsonl','discovery_id','ASTIS-DISC-20261010-ActualWaitCompositionElaboration')]:
 p=Path(file);base=subprocess.check_output(['git','show','HEAD:'+file]);raw=p.read_bytes();assert raw.startswith(base)
 tail=raw[len(base):];events=[json.loads(x) for x in tail.splitlines() if x]
 assert all(e.get(key)==identity for e in events),(file,[(e.get(key),e.keys()) for e in events])
 fixed=tail.replace(b'\r\n',b'\n');assert [json.loads(x) for x in fixed.splitlines() if x]==events
 p.write_bytes(base+fixed);rows.append(dict(file=file,prefix_RAW_sha256=hashlib.sha256(base).hexdigest(),owned_events=len(events),semantic_events_unchanged=True))
(r/'owned-tail-normalization81.json').write_text(json.dumps(dict(reason='Normalize only owned Windows append tails; HEAD prefix byte-for-byte preserved.',files=rows),indent=2)+'\n',encoding='utf8',newline='\n')
print(rows)
