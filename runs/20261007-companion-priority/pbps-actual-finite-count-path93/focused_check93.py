import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
run = Path(__file__).resolve().parent
name, label = sys.argv[1:3]
source = run / name
out = run / 'focused93' / label
out.mkdir(parents=True, exist_ok=False)
raw = source.read_bytes()
(out / 'input.exactraw.snapshot.lean').write_bytes(raw)
env = os.environ.copy()
env.pop('ELAN_TOOLCHAIN', None)
binpath = root / '.astis/toolchain/lean-4.33.0-windows/bin'
env['PATH'] = str(binpath) + os.pathsep + env['PATH']
argv = [str(binpath / 'lake.exe'), 'env', 'lean', str(source.relative_to(root))]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
with (out / 'stdout.log').open('wb') as stdout, (out / 'stderr.log').open('wb') as stderr:
    result = subprocess.run(argv, cwd=root, env=env, stdout=stdout, stderr=stderr)
receipt = dict(started_utc=start, ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               argv=argv, exit_code=result.returncode, terminal_closed=True,
               source_raw_sha256=hashlib.sha256(raw).hexdigest(),
               source_unchanged=source.read_bytes() == raw,
               scope='Private proof ingredients only; no completed source-facing SAU.')
(out / 'receipt.json').write_text(json.dumps(receipt, indent=2), encoding='utf-8')
print(json.dumps(receipt))
for stream in ('stdout.log', 'stderr.log'):
    output = (out / stream).read_text(encoding='utf-8')
    if len(output) > 6500:
        print(output[:3500])
        print('Full output retained at', out / stream)
        print('\n'.join(line for line in output.splitlines() if ': error' in line))
        print(output[-1500:])
    else:
        print(output)
sys.exit(result.returncode)
