from pathlib import Path
import subprocess,json,hashlib
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81');p=Path('runs/substantive_advances.jsonl')
base=subprocess.run(['git','show','HEAD:runs/substantive_advances.jsonl'],capture_output=True,check=True).stdout
raw=p.read_bytes();assert raw.startswith(base)
tail=raw[len(base):];events=[json.loads(x) for x in tail.splitlines() if x]
assert all(e['advance_id']=='ASTIS-SA-20261010-PBPSIdealHalfTurnKernel' for e in events)
fixed=tail.replace(b'\r\n',b'\n');assert [json.loads(x) for x in fixed.splitlines() if x]==events
p.write_bytes(base+fixed)
(r/'owned-ledger-newline-receipt81.json').write_text(json.dumps(dict(reason='durable append on Windows produced CRLF; normalize only this SAU owned suffix, preserve HEAD historical prefix byte-for-byte',prefix_sha256=hashlib.sha256(base).hexdigest(),owned_events=len(events),semantic_events_unchanged=True),indent=2)+'\n')
p2=subprocess.run(['git','diff','--check'],capture_output=True)
(r/'diff-check81.stdout.log').write_bytes(p2.stdout);(r/'diff-check81.stderr.log').write_bytes(p2.stderr)
print('owned events',len(events),'diff-check',p2.returncode)
assert p2.returncode==0,p2.stdout.decode()
