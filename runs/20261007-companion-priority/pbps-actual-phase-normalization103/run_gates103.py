from pathlib import Path
import json,subprocess,sys
r=Path(__file__).parent
labels=['tests','astis','canonical','publication','contributor','semantic','frontier','process-memory','python-compile','site-build','site-check','graph','site-regressions','harness','diff-check']
for label in labels:
 suffix='graph-after-site' if label=='graph' else label
 p=subprocess.run([sys.executable,'-X','utf8',str(r/'check103.py'),label,'integration-'+suffix],capture_output=True)
 print(label,p.returncode,flush=True)
 if p.returncode:
  print(p.stdout.decode(errors='replace')[-3000:]);print(p.stderr.decode(errors='replace')[-2000:]);raise SystemExit(p.returncode)
print('All15 integration gates closed PASS.',flush=True)
