"""Exact subprocess argv, stdout/stderr and receipt preservation; no shell."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import os
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
label = sys.argv[1]
argv = sys.argv[2:]
log = ROOT / (label + '.raw.log')
receipt = ROOT / (label + '.receipt.json')
assert argv and not log.exists() and not receipt.exists()
head = lambda: subprocess.run(['git','rev-parse','HEAD'],capture_output=True,check=True).stdout.decode().strip()
before = head()
started = datetime.now(timezone.utc).isoformat()
clock = time.monotonic()
env = dict(os.environ)
env['PYTHONDONTWRITEBYTECODE'] = '1'
with log.open('xb') as out:
    result = subprocess.run(argv,stdout=out,stderr=subprocess.STDOUT,env=env)
record = {'label':label,'argv':argv,'cwd':str(Path.cwd()),'started_utc':started,
          'elapsed_seconds':time.monotonic()-clock,'exit_code':result.returncode,
          'head_before':before,'head_after':head(),'log':log.name,
          'log_bytes':log.stat().st_size,'log_sha256':sha256(log.read_bytes()).hexdigest(),
          'script_sha256':sha256(Path(argv[1]).read_bytes()).hexdigest() if len(argv)>1 and Path(argv[1]).is_file() else None}
receipt.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(log.read_text(),end='')
print(json.dumps({'receipt':receipt.name,'exit_code':result.returncode,'log_sha256':record['log_sha256']},indent=2))
raise SystemExit(result.returncode)
