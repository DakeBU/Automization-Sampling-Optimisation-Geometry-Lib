from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
HERE=Path(__file__).resolve().parent
E=ROOT/'research-wiki/paper-contributions/GaussianComplexity/truncated-row-second-moment-semantic-evidence'
script=HERE/'actual_normal_verification.py'
started=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
head_before=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
verification_env=os.environ.copy();verification_env['LEAN_NUM_THREADS']='2';verification_env['ASTIS_ATLAS_ROOT']=str(ROOT/'.atlas-upstream/v1')
command=[sys.executable,'-B',str(script)]
r=subprocess.run(command,cwd=ROOT,env=verification_env,capture_output=True)
ended=datetime.datetime.now(datetime.timezone.utc).isoformat()
head_after=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
def sha(b):return hashlib.sha256(b).hexdigest()
def create(path,data):
    with path.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
create(E/'actual-VERIFIED-run.stdout.log',r.stdout)
create(E/'actual-VERIFIED-run.stderr.log',r.stderr)
create(E/'actual-VERIFIED-runner.original.py',Path(__file__).read_bytes())
receipt={'kind':'Actual single normal verification subprocess receipt','started_utc':started,'ended_utc':ended,'command':command,'cwd':str(ROOT),'head_before':head_before,'head_after':head_after,'exit_code':r.returncode,'elapsed_seconds':time.monotonic()-t,'python':sys.executable,'LEAN_NUM_THREADS':'2','ASTIS_ATLAS_ROOT':verification_env['ASTIS_ATLAS_ROOT'],'script_sha256':sha(script.read_bytes()),'stdout_path':str((E/'actual-VERIFIED-run.stdout.log').relative_to(ROOT)),'stdout_sha256':sha(r.stdout),'stderr_path':str((E/'actual-VERIFIED-run.stderr.log').relative_to(ROOT)),'stderr_sha256':sha(r.stderr),'normal_API':'tools.astis_advance.transition_advance','advance_id':'ASTIS-SA-20261111-GaussianComplexityTruncatedRowMoment'}
create(E/'actual-VERIFIED-run.receipt.json',(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode())
sys.stdout.buffer.write(r.stdout);sys.stderr.buffer.write(r.stderr)
raise SystemExit(r.returncode)
