"""Read-only independent execution of exact CI test repair snapshots."""
from __future__ import annotations
import ast
import contextlib
import datetime
import hashlib
import importlib.util
import io
import json
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[5]
BASE = ROOT / 'runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/ci-reader-order-repair86'
OUT = BASE / 'independent-review'
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'website/scripts'))

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def dump(name, value):
    path = OUT / name
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

variant = sys.argv[1]
assert variant in ('before', 'proposed')
source = BASE / f'test.{variant}.exactraw.snapshot'
raw = source.read_bytes()
copy_path = OUT / f'test_{variant}_isolated86.py'
assert not copy_path.exists(), 'Do not replace a frozen isolated input'
copy_path.write_bytes(raw)
assert copy_path.read_bytes() == raw
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
spec = importlib.util.spec_from_file_location(f'independent_ci86_{variant}', copy_path)
module = importlib.util.module_from_spec(spec)
capture = io.StringIO()
with contextlib.redirect_stdout(capture), contextlib.redirect_stderr(capture):
    spec.loader.exec_module(module)
    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    result = unittest.TextTestRunner(stream=capture, verbosity=2).run(suite)
log = capture.getvalue()
(OUT / f'{variant}.isolated.log').write_text(log, encoding='utf-8')
record = {
    'variant': variant, 'started_utc': start,
    'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'python': sys.version, 'source': source.relative_to(ROOT).as_posix(),
    'source_raw_sha256': sha(raw), 'isolated_copy': copy_path.relative_to(ROOT).as_posix(),
    'tests_run': result.testsRun, 'success': result.wasSuccessful(),
    'failures': [{'test': str(t), 'traceback': v} for t,v in result.failures],
    'errors': [{'test': str(t), 'traceback': v} for t,v in result.errors],
    'skipped': [{'test': str(t), 'reason': v} for t,v in result.skipped],
    'expected_failures': len(result.expectedFailures),
    'unexpected_successes': len(result.unexpectedSuccesses),
    'log_raw_sha256': sha((OUT / f'{variant}.isolated.log').read_bytes()),
    'execution': 'importlib exact isolated copy; no production test or renderer edits; bytecode disabled'
}
dump(f'{variant}.isolated.result.json', record)
print(json.dumps({k:record[k] for k in ('variant','tests_run','success','source_raw_sha256')}))
print(json.dumps({'failures':[v['test'] for v in record['failures']], 'errors':[v['test'] for v in record['errors']], 'skipped':record['skipped']}))
