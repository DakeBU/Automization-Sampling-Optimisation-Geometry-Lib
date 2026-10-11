"""Normalize only owned integration text after preserving original bytes."""
from pathlib import Path
import hashlib,json,subprocess,re
R=Path(__file__).resolve().parents[3];r=Path(__file__).resolve().parent;o=r/'integration93/line-ending-repair';o.mkdir(exist_ok=False)
q=subprocess.run(['git','diff','--check'],cwd=R,capture_output=True)
(o/'before.log').write_bytes(q.stdout+q.stderr)
names=sorted(set(re.findall(r'^(.+?):\d+: (?:trailing whitespace|new blank line at EOF)',q.stdout.decode(),re.M)))
owned=set(json.loads((r/'integration93/integration-scope.json').read_bytes())['owned'])
assert set(names)<=owned,names
rows=[]
for i,name in enumerate(names):
    p=R/name;b=p.read_bytes();(o/f'{i}.before.exactraw.snapshot').write_bytes(b)
    a=b.replace(b'\r\n',b'\n');assert a.replace(b'\r',b'')==b.replace(b'\r\n',b'\n').replace(b'\r',b'')
    p.write_bytes(a);rows.append(dict(path=name,before_raw_sha256=hashlib.sha256(b).hexdigest(),after_raw_sha256=hashlib.sha256(a).hexdigest(),change='CRLF to LF only'))
q=subprocess.run(['git','diff','--check'],cwd=R,capture_output=True);(o/'after.log').write_bytes(q.stdout+q.stderr);assert q.returncode==0
(o/'receipt.json').write_bytes((json.dumps(dict(status='PASS_PLAIN_DIFF_CHECK',changed=rows,collaborator_files_untouched=True),indent=2)+'\n').encode())
print('Owned integration line endings normalized; plain git diff --check passed.',names)
