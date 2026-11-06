"""Claim the sole integration lane for the independently VERIFIED node."""
import hashlib
import json
from pathlib import Path
from tools.astis_advance import current_advances, transition_advance

advance='ASTIS-SA-20261105-CompactGradientSqrtTest'
ledger=Path('runs/substantive_advances.jsonl');before=ledger.read_bytes()
state=current_advances()[advance]
assert state['state']=='VERIFIED'
assert state['latest_evidence']['verified_commit']=='eead411ec020bb34ad18208d3453067e8905c0a6'
transition_advance(advance,'STABILIZING',worker_id='agent-task:/root',evidence={
    'canonical_branch':'codex/sog-bench-source-test-energy','integration_owner':'agent-task:/root',
    'publication_declarations':state['publication_declarations'],
    'checkpoint':'Serialized public calculus/Registry/root-Test and reader/graph integration only. Verified module, test, source statement and corrected lesson remain unchanged; no whole exercise/Bench QA/model credit.'})
after=ledger.read_bytes();assert after.startswith(before)
assert b'\r\n' not in after[len(before):]
print(json.dumps({'state':current_advances()[advance]['state'],
    'preserved_prefix_bytes':len(before),'preserved_prefix_sha256':hashlib.sha256(before).hexdigest()}))
