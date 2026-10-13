from pathlib import Path
import hashlib,json,subprocess
r=Path(__file__).parent;p=Path('runs/substantive_advances.jsonl');base=subprocess.check_output(['git','show','HEAD:runs/substantive_advances.jsonl']);raw=p.read_bytes();assert raw.startswith(base)
tail=raw[len(base):];events=[json.loads(x) for x in tail.splitlines() if x]
assert events and all(x.get('advance_id')=='ASTIS-SA-20261010-PBPSActualBoundedTestContinuity' for x in events)
fixed=tail.replace(b'\r\n',b'\n');assert [json.loads(x) for x in fixed.splitlines() if x]==events;p.write_bytes(base+fixed)
(r/'owned-tail-normalization83.json').write_text(json.dumps(dict(file=p.as_posix(),prefix_RAW_sha256=hashlib.sha256(base).hexdigest(),owned_events=len(events),semantic_events_unchanged=True,scope='Only owned Windows append tail; HEAD prefix preserved byte for byte.'),indent=2)+'\n',encoding='utf8',newline='\n')
