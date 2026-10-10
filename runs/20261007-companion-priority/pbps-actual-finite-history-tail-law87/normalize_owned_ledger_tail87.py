from pathlib import Path
import subprocess,json,hashlib
R=Path('E:/Samplinglib');r=Path(__file__).parent;p=R/'runs/substantive_advances.jsonl'
prefix=subprocess.check_output(['git','show','HEAD:runs/substantive_advances.jsonl'],cwd=R)
b=p.read_bytes();assert b.startswith(prefix);tail=b[len(prefix):]
events=[json.loads(x) for x in tail.splitlines() if x.strip()]
assert events and all(x['advance_id']=='ASTIS-SA-20261011-PBPSActualFiniteHistoryTailLaw' for x in events)
snap=r/'ledger87.original-own-tail.exactraw.snapshot';assert not snap.exists();snap.write_bytes(tail)
clean=tail.replace(b'\r\n',b'\n');assert [json.loads(x) for x in clean.splitlines() if x.strip()]==events
p.write_bytes(prefix+clean)
(r/'ledger87.line-ending-receipt.json').write_text(json.dumps({'scope':'Only three own87 appended JSONL events CRLF→LF; exact committed prefix and JSON payloads preserved. No review/source/statement bytes changed.','original_tail_sha256':hashlib.sha256(tail).hexdigest(),'clean_tail_sha256':hashlib.sha256(clean).hexdigest(),'event_count':len(events)},indent=2)+'\n',encoding='utf-8',newline='\n')
print('Own new ledger tail normalized; committed prefix/payloads preserved.')
