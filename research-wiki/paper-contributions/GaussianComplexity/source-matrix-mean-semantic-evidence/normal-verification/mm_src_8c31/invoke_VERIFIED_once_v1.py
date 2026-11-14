#!/usr/bin/env python3
"""Exactly one normal API call; outcome must subsequently be read from ledger."""
from pathlib import Path
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
sys.path.insert(0, str(ROOT))
from tools.astis_advance import transition_advance

OUT = Path(__file__).resolve().parent
pre = json.loads((OUT / 'precheck-v1.json').read_text())
assert pre['status'] == 'PASS' and pre['normal_API_calls_so_far'] == 0
payload = json.loads((OUT / 'actual-VERIFIED-evidence.full.json').read_text())
marker = OUT / 'api-once-v1.started.json'
with marker.open('x') as f:
    json.dump({'normal_transition_advance_call_limit': 1, 'advance_id': 'ASTIS-SA-20261112-GaussianComplexitySourceMatrixMean',
               'worker_id': '/root/mm_fresh_source_8c31', 'payload_sha256': hashlib.sha256((OUT / 'actual-VERIFIED-evidence.full.json').read_bytes()).hexdigest()}, f)
transition_advance('ASTIS-SA-20261112-GaussianComplexitySourceMatrixMean', 'VERIFIED',
                   worker_id='/root/mm_fresh_source_8c31',
                   modes=['independent-source-review', 'native-verification', 'preservation-readback'],
                   evidence=payload)
print(json.dumps({'normal_API_returned': True, 'normal_transition_advance_calls': 1,
                  'actual_ledger_readback_required_before_any_further_action': True}))
