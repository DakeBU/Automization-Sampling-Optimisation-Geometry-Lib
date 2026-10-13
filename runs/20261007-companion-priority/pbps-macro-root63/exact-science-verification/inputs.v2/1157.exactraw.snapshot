import json,subprocess,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
p=subprocess.run([sys.executable,'-X','utf8',str(OUT/'check_closed63.py')],capture_output=True)
assert p.returncode==0 and not p.stderr,p.stderr
print(p.stdout.decode('utf-8'),end='')
b=(OUT/'proposed-lease.closed.json').read_bytes()
assert json.loads(b.decode('utf-8'))['status']=='CLOSED_LAST'
# FINAL OWNED WRITE of the review run. stdout is terminal only.
(OUT/'lease.json').write_bytes(b)
print('CLOSED_LAST final lease write committed; no owned writes follow.')
