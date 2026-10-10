from pathlib import Path
import subprocess,json,hashlib
r=Path(__file__).parent;p=Path('runs/substantive_advances.jsonl')
prefix=subprocess.check_output(['git','show','HEAD:runs/substantive_advances.jsonl'])
raw=p.read_bytes();assert raw.startswith(prefix);tail=raw[len(prefix):]
events=[json.loads(x) for x in tail.splitlines() if x.strip()]
assert len(events)==1 and events[0]['advance_id']=='ASTIS-SA-20261011-PBPSActualFiniteHistoryTailLaw'
assert events[0]['to_state']=='VERIFIED'
snap=r/'integration87/verified-tail.original.exactraw.snapshot';assert not snap.exists();snap.write_bytes(tail)
clean=tail.replace(b'\r\n',b'\n');assert json.loads(clean)==events[0]
p.write_bytes(prefix+clean)
out=r/'integration87/verified-tail-normalization.json';assert not out.exists()
out.write_text(json.dumps(dict(scope='Only own87 independent VERIFIED appended ledger event line endings. Payload and entire committed prefix unchanged.',before_RAW_sha256=hashlib.sha256(tail).hexdigest(),after_RAW_sha256=hashlib.sha256(clean).hexdigest()),indent=2)+'\n',encoding='utf8',newline='\n')
print('Own VERIFIED ledger tail normalized without payload or committed-prefix changes.')
