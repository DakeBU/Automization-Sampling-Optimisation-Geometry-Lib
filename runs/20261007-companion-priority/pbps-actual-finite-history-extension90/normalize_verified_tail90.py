from pathlib import Path
import hashlib,json,subprocess
r=Path(__file__).parent;out=r/'integration90';p=Path('runs/substantive_advances.jsonl')
prefix=subprocess.check_output(['git','show','HEAD:runs/substantive_advances.jsonl']);raw=p.read_bytes()
assert raw.startswith(prefix);tail=raw[len(prefix):];events=[json.loads(x) for x in tail.splitlines() if x.strip()]
claim=json.loads((r/'claim.json').read_bytes())
assert len(events)==1 and events[0]['advance_id']==claim['advance_id'] and events[0]['event']=='transition' and events[0]['to_state']=='VERIFIED'
snapshot=out/'verified-tail.original.exactraw.snapshot';assert not snapshot.exists();snapshot.write_bytes(tail)
normalized=tail.replace(b'\r\n',b'\n');assert [json.loads(x) for x in normalized.splitlines() if x.strip()]==events
p.write_bytes(prefix+normalized)
receipt=out/'verified-tail.newline-only.json';assert not receipt.exists()
receipt.write_text(json.dumps(dict(only_new_verified_event_tail=True,original_ledger_RAW_sha256=hashlib.sha256(raw).hexdigest(),original_tail_RAW_sha256=hashlib.sha256(tail).hexdigest(),normalized_ledger_RAW_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),snapshot=snapshot.as_posix(),historical_native_admission_resolution='Reconstruct exact original native ledger as git sciencee8d38b3002f4562ef254205135c0d213f9efe410:runs/substantive_advances.jsonl plus original tail snapshot; native admission remains immutable.',all_event_payloads_unchanged=True),indent=2)+'\n',encoding='utf8',newline='\n')
print('Only new verified90 tail newline normalized; exact native snapshot retained.')
