from pathlib import Path
import json, hashlib, datetime

task = Path(r'E:\Samplinglib\runs\20261007-companion-priority\pbps-rough-mean-gradient-sourcegraph56')
def digest(data):
    return hashlib.sha256(data).hexdigest()
with (task / 'primary-before-signature.freeze.json').open('rb') as handle:
    freeze_raw = handle.read()
freeze = json.loads(freeze_raw.decode('utf-8'))
for name, metadata in freeze['first_stage_artifacts'].items():
    with (task / name).open('rb') as handle:
        data = handle.read()
    assert len(data) == metadata['bytes']
    assert digest(data) == metadata['raw_sha256']
receipt = {
    'schema_version': 1,
    'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'stage': 'FIRST_STAGE_READY_RESOURCE_CLOSED',
    'freeze_raw_sha256': digest(freeze_raw),
    'artifact_digest_validation': 'PASS',
    'compiler': 'NOT_STARTED_CLOSED',
    'compiler_processes_started': 0,
    'background_jobs_started': 0,
    'persistent_tool_sessions': 0,
    'prior_python_foreground_calls': [
        {'command': 'source_first_extract.py', 'exit_code': 0},
        {'command': 'extract_support.py', 'exit_code': 0},
        {'command': 'anchor_inventory.py', 'exit_code': 0},
        {'command': 'write_first_stage.py', 'exit_code': 0},
    ],
    'file_resource_closure': 'All explicit reads and writes use context managers; Path.read_text closes on return. Receipt write closes before this process returns.',
    'candidate_API_body_or_target_verdict_read': False,
    'scope': 'Exclusive run directory only; no Lean, canonical, ledger or site mutation',
    'independent_mathematical_review': 'PENDING',
    'source_graph_counts': {'inventory': 92, 'nodes': 22, 'routes': 12},
    'automatic_policy_rejection': 'One attempted combined closure script command was rejected before process creation with blocked by policy; no stated reason was supplied. This smaller closure pass leaves the freeze and source graph unchanged.'
}
with (task / 'first-stage-resource-closure.json').open('w', encoding='utf-8', newline='\n') as handle:
    json.dump(receipt, handle, indent=2)
    handle.write('\n')
print(json.dumps({'freeze_sha256': digest(freeze_raw), 'compiler': 'NOT_STARTED_CLOSED', 'artifact_digest_validation': 'PASS'}))
