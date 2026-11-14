#!/usr/bin/env python3
"""Narrow foreground browser QA runner for this fixed independent review only."""
from pathlib import Path
import hashlib, json, sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from runner import ROOT, OUT, run
assert HERE==OUT.resolve()
VERSIONS={
 'v3':('browser-proposal-v3','check_browser_proposal_v3.py','513ec00bbd2cece81ee65124d69f88f6472a030561f9bbe92c12f5cdb50b9757'),
 'v2':('browser-1d0-v2','check_browser_1d0_v2.py','7a29754dc25d2008be8b8136594fb707d922f0e572c59b768560f349ee2b5764'),
}
if len(sys.argv)!=2 or sys.argv[1] not in VERSIONS:
 raise SystemExit('usage: run_browser_check.py v2|v3')
label,filename,expected=VERSIONS[sys.argv[1]]
checker=HERE/filename
actual=hashlib.sha256(checker.read_bytes()).hexdigest()
if actual!=expected:raise SystemExit('checker hash mismatch')
runner_hash=hashlib.sha256((HERE/'runner.py').read_bytes()).hexdigest()
if runner_hash!='1352f9bb2a89fd32820114e72af13eaf6bff54b3d4326b946cb0cf00fbb21081':
 raise SystemExit('runner hash mismatch')
python=ROOT/'.astis/huanjian-gc-integration-20261105/browser-venv/bin/python'
print(json.dumps({'version':sys.argv[1],'label':label,'checker':str(checker),'checker_sha256':actual,'wrapper_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'operator_role':'ROOT runs exact independent checker; assessment remains variance_native_61d0'},indent=2),flush=True)
run(label,[python,checker],check=False)
result=json.loads((HERE/'commands'/label/'result.json').read_text())
print('ACTUAL_BROWSER_EXIT',result['exit'],flush=True)
sys.exit(result['exit'])
