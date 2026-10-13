from pathlib import Path
import json,hashlib,gzip,subprocess
r=Path(__file__).parent;p=Path('runs/substantive_advances.jsonl')
a=subprocess.check_output(['git','show','HEAD:'+p.as_posix()]);b=p.read_bytes();al=a.splitlines();bl=b.splitlines()
assert b.replace(b'\r\n',b'\n').startswith(a)
assert len(bl)==len(al)+1 and bl[:len(al)]==al
new=json.loads(bl[-1]);assert new['advance_id']=='ASTIS-SA-20261012-PBPSActualBoundedGibbsDuality' and new['to_state']=='VERIFIED'
original=r/'ledger-before-EOL-repair106.exactraw.gz';assert not original.exists();original.write_bytes(gzip.compress(b,mtime=0))
normalized=b.replace(b'\r\n',b'\n');p.write_bytes(normalized)
assert normalized.startswith(a) and normalized.splitlines()==bl
(r/'ledger-EOL-repair106.json').write_text(json.dumps(dict(original_RAW_sha256=hashlib.sha256(b).hexdigest(),exact_archive=original.as_posix(),corrected_RAW_sha256=hashlib.sha256(normalized).hexdigest(),committed_prefix_sha256=hashlib.sha256(a).hexdigest(),historical_events_unchanged=True,verified_tail_unchanged=True,transformation='CRLF to LF only; five line endings; no JSON payload change'),indent=2)+'\n',encoding='utf8',newline='\n')
print('Exact committed prefix plus unchanged independent VERIFIED event restored; original RAW retained.')
