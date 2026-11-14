from pathlib import Path
from datetime import datetime, timezone
from contextlib import redirect_stdout, redirect_stderr
import hashlib
import json
import sys
import time
import traceback

sys.dont_write_bytecode = True
ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
PRIVATE = ROOT / '.astis/huanjian-gc-fixed-spectrum-first-order-20261108/topology-challenge/mirror-review'
PUBLIC = ROOT / 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-first-order-semantic-evidence/conceptual-oracle-factorization/independent-review'
TARGET = 'ASTIS-DISC-20261108-GaussianQuadraticOracleFactorization-FixedSpectrumGradient'
ACTOR = '/root/fixed_foq_topology_challenge'
REVIEW_REL = 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-first-order-semantic-evidence/conceptual-oracle-factorization/independent-review/review-v1.json'
REVIEW_SHA = 'd26df0070bed3549b90087003af5e26884d58788e6f23586db3f0476bcb23597'
PROPOSAL_REL = 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-first-order-semantic-evidence/conceptual-oracle-factorization/existing-bridge-substrate-supplement-v1.json'
PROPOSAL_SHA = '52c7027af4de67a4ab99b3141daa9d900fad878b7c016bd0cea86ea8d487585a'
sha = lambda b: hashlib.sha256(b).hexdigest()
canon = lambda obj: json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()

def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def protected_bytes():
    paths = {
        ROOT / 'runs/substantive_advances.jsonl',
        ROOT / 'website/content/functor_hypergraph.json',
        ROOT / 'website/content/graph_memory_index.json',
        ROOT / '.astis/huanjian-resume-20261103/2610.20492v1.html',
    }
    paths.update(p for p in (ROOT / 'research-wiki/frontier-cells').rglob('*') if p.is_file())
    for folder in ['AutoSamplingTheory', 'Tests']:
        paths.update((ROOT / folder).rglob('*.lean'))
    return {str(p.relative_to(ROOT)): {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes())} for p in sorted(paths)}

assert not (PRIVATE / 'validation-transition.receipt.json').exists(), 'Validation receipt already exists; never repeat the API call.'
started = datetime.now(timezone.utc)
stamp = started.strftime('%Y%m%dT%H%M%S%fZ')
logname = stamp + '-normal-discovery-validation.log'
logpath = PRIVATE / logname
receiptpath = PRIVATE / 'validation-transition.receipt.json'
normal_api_calls = 0
exit_code = 1
checks = {}
start_clock = time.monotonic()
with logpath.open('x') as logfile, redirect_stdout(logfile), redirect_stderr(logfile):
    try:
        print('STARTED_UTC', started.isoformat())
        print('COMMAND', json.dumps([sys.executable, *sys.argv]))
        assert sha((ROOT / REVIEW_REL).read_bytes()) == REVIEW_SHA
        review = json.loads((ROOT / REVIEW_REL).read_text())
        assert review['verdict'] == 'ACCEPT' and not review['blocking_findings']
        assert sha((ROOT / PROPOSAL_REL).read_bytes()) == PROPOSAL_SHA
        proposal = json.loads((ROOT / PROPOSAL_REL).read_text())
        sys.path.insert(0, str(ROOT / 'tools'))
        import astis_advance
        ledger = astis_advance.DEFAULT_DISCOVERY_LEDGER
        before = ledger.read_bytes()
        assert before.endswith(b'\n')
        for line in before.splitlines():
            json.loads(line)
        states_before = astis_advance.current_discoveries()
        target_before = states_before[TARGET]
        assert len(states_before) == 39
        assert target_before['status'] == 'raw'
        assert target_before['kind'] == 'conceptual-mirror'
        assert target_before['created_by'] != ACTOR
        assert target_before['metadata'] == proposal['metadata']
        old_states = {key: value for key, value in states_before.items() if key != TARGET}
        assert len(old_states) == 38
        protected_before = protected_bytes()
        for path, digest in proposal['baseline_models'].items():
            assert protected_before[path]['sha256'] == digest
        (PRIVATE / 'discovery-ledger-before.raw.jsonl').write_bytes(before)
        write_json(PRIVATE / 'discovery-states-before.private.json', states_before)
        write_json(PRIVATE / 'protected-baseline.private.json', protected_before)
        note = (
            'Independent source-level ACCEPT of the exact existing conceptual bridge pointwise-substrate supplement; '
            'review=' + REVIEW_REL + '; review_sha256=' + REVIEW_SHA + '; proposal_sha256=' + PROPOSAL_SHA + '. '
            'Scope: same canonical transport:gaussian-quadratic-oracle-factorization and family:gaussian-oracle-hardness; '
            'genuine pointwise precision-to-value/gradient plus same-O forward consumer only. '
            'No current theorem source-V, Lean cross-route implication, operational/adaptive/target-law/TV/precision/expected-cost transport, '
            'functor certification or shared-model application. Later current-binding source V and serialized independent model patch acceptance remain mandatory; '
            'old critical_estimates/review remain history.'
        )
        api_called_at = datetime.now(timezone.utc).isoformat()
        print('ACTUAL_NORMAL_API_CALL', 'astis_advance.transition_discovery', TARGET, 'validated', ACTOR)
        print('API_CALLED_AT_UTC', api_called_at)
        print('REVIEW_SHA256', REVIEW_SHA)
        normal_api_calls += 1
        astis_advance.transition_discovery(TARGET, 'validated', actor=ACTOR, note=note)
        after = ledger.read_bytes()
        assert after.startswith(before), 'Old Discovery bytes changed.'
        appended = after[len(before):]
        new_records = [json.loads(line) for line in appended.splitlines() if line.strip()]
        assert len(new_records) == 1
        event = new_records[0]
        assert event['event'] == 'discovery_transition'
        assert event['discovery_id'] == TARGET and event['from_status'] == 'raw'
        assert event['to_status'] == 'validated' and event['actor'] == ACTOR and event['note'] == note
        states_after = astis_advance.current_discoveries()
        assert len(states_after) == len(states_before)
        assert {key: value for key, value in states_after.items() if key != TARGET} == old_states
        assert states_after[TARGET]['metadata'] == target_before['metadata']
        assert states_after[TARGET]['created_by'] == target_before['created_by']
        assert states_after[TARGET]['status'] == 'validated'
        protected_after = protected_bytes()
        assert protected_after == protected_before, 'A protected non-Discovery byte or path changed.'
        write_json(PRIVATE / 'discovery-states-after.private.json', states_after)
        write_json(PRIVATE / 'protected-after.private.json', protected_after)
        checks = {
            'old_ledger_prefix_bytes': len(before),
            'old_ledger_prefix_sha256': sha(before),
            'old_ledger_prefix_preserved': True,
            'ledger_after_bytes': len(after),
            'ledger_after_sha256': sha(after),
            'appended_records': 1,
            'appended_event': event,
            'old_other_discovery_states': 38,
            'old_other_states_sha256': sha(canon(old_states)),
            'all38otherstates_identical': True,
            'target_metadata_and_creator_unchanged': True,
            'target_from_status': 'raw',
            'target_to_status': 'validated',
            'protected_file_count': len(protected_before),
            'protected_manifest_sha256': sha(canon(protected_before)),
            'all_SAU_frontier_model_source_and_proof_files_unchanged': True,
            'shared_models_applied': False,
            'current_theorem_sourceV_granted': False,
            'normal_API_called_at_utc': api_called_at,
        }
        print('PRESERVATION_CHECKS', json.dumps(checks, ensure_ascii=False, sort_keys=True))
        print('NORMAL_API_TRANSITIONS', normal_api_calls)
        print('RESULT', 'Discovery validated for typed conceptual supplement only.')
        exit_code = 0
    except BaseException:
        traceback.print_exc()
        print('NORMAL_API_TRANSITIONS_ATTEMPTED', normal_api_calls)
        exit_code = 1
elapsed = time.monotonic() - start_clock
receipt = {
    'started_utc': started.isoformat(),
    'ended_utc': datetime.now(timezone.utc).isoformat(),
    'command': [sys.executable, *sys.argv],
    'cwd': str(ROOT),
    'function': 'astis_advance.transition_discovery',
    'discovery_id': TARGET,
    'actor': ACTOR,
    'normal_API_call_count': normal_api_calls,
    'exit_code': exit_code,
    'elapsed_seconds': elapsed,
    'review_path': REVIEW_REL,
    'review_sha256': REVIEW_SHA,
    'proposal_sha256': PROPOSAL_SHA,
    'script_sha256': sha(Path(__file__).read_bytes()),
    'private_raw_log': str(logpath.relative_to(ROOT)),
    'public_raw_log': str((PUBLIC / logname).relative_to(ROOT)),
    'raw_log_sha256': sha(logpath.read_bytes()),
    'preservation': checks,
}
write_json(receiptpath, receipt)
(PUBLIC / logname).write_bytes(logpath.read_bytes())
write_json(PUBLIC / receiptpath.name, receipt)
print(json.dumps({'exit_code': exit_code, 'normal_API_call_count': normal_api_calls, 'receipt': str(receiptpath.relative_to(ROOT)), 'receipt_sha256': sha(receiptpath.read_bytes()), 'raw_log_sha256': receipt['raw_log_sha256'], 'target_status': checks.get('target_to_status')}))
raise SystemExit(exit_code)
