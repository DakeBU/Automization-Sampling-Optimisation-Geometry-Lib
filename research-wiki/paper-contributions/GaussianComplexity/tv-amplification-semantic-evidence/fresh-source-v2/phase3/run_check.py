#!/usr/bin/env python3
"""Run one actual review command, archiving exact merged stdout/stderr bytes."""
from pathlib import Path
import datetime
import gzip
import hashlib
import json
import subprocess
import sys
import time

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
OUT = Path(__file__).resolve().parent
key, *command = sys.argv[1:]
assert key and command and '/' not in key
paths = ['lean-toolchain','lake-manifest.json',
 'AutoSamplingTheory/ExampleCases/GaussianComplexity/TVAmplification.lean',
 'Tests/GaussianComplexityTVAmplification.lean']
paths += [arg for arg in command if arg.endswith('.lean') and (ROOT/arg).is_file() and arg not in paths]
def sha(b): return hashlib.sha256(b).hexdigest()
def state():
 return {'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip(),
 'file_sha256':{p:sha((ROOT/p).read_bytes()) for p in paths}}
before=state();started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
print(json.dumps({'check':key,'command':command,'started_utc':started,'before':before}),flush=True)
process=subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
elapsed=time.monotonic()-t;data=process.stdout
(OUT/(key+'.log.gz')).write_bytes(gzip.compress(data,mtime=0))
receipt={'check':key,'command':command,'cwd':str(ROOT),'started_utc':started,
 'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'wall_seconds':elapsed,
 'exit_code':process.returncode,'before':before,'after':state(),
 'raw_log_bytes':len(data),'raw_log_sha256':sha(data),'raw_log_gzip':key+'.log.gz',
 'compressed_log_sha256':sha((OUT/(key+'.log.gz')).read_bytes()),'raw_whitespace_preserved':True}
(OUT/(key+'.receipt.json')).write_text(json.dumps(receipt,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
print(data.decode('utf-8',errors='replace'),end='')
print(json.dumps({'check':key,'exit_code':process.returncode,'wall_seconds':elapsed,'raw_log_sha256':sha(data)}),flush=True)
sys.exit(process.returncode)
