"""Replay one recorded public-dev Lean pilot without model or Lean execution."""
from __future__ import annotations

import argparse
import io
from pathlib import Path
import stat
import sys
import tempfile
import zipfile

import sog_bench_lean_local as local

bench, bridge, runtime, workspace = local.bench, local.bridge, local.runtime, local.workspace
ARCHIVE = runtime.ROOT / 'runs/20261110-bench-local-lean-first/live-v031-evidence.zip'
ARCHIVE_SHA256 = '51bfb9bce9ca3edb2c99ebd9f750aae1a149a79a78ff805add159a53d783a6c6'
EVIDENCE = 'lean-local-evidence/'
AGENT = ('prompt.json', 'Solution.lean.txt')
ACTIONS = ('check', 'submit')
MAX_ARCHIVE_BYTES = 128 * 1024
MAX_MEMBER_BYTES = 64 * 1024
MAX_EXPANDED_BYTES = 256 * 1024
FILES = {
    EVIDENCE + name for name in (
        '01-model.json', '02-model.json', 'pilot-selection.json', 'pilot-result.json',
        'bridge/prompt.jsonl', 'bridge/selection.json', 'bridge/termination.json',
        'bridge/trajectory.json', 'workspace/session.json', 'workspace/completion.json',
        'workspace/external-run.json', 'workspace/external-end.json', 'workspace/external-evidence.json',
        *('workspace/agent/' + name for name in (*AGENT, 'LICENSE', 'LICENSE_SCOPE.md', 'NOTICE')),
        *(f'bridge/{i:04d}-{name}' for i in (1, 2) for name in ('request.bin', 'feedback.json')),
        *(f'workspace/actions/{i:04d}/{name}' for i in (1, 2) for name in (
            'event.json', 'observation.json', 'source.txt', 'verification/result.json',
            'verification/submission.txt', 'verification/compiler-diagnostic.bin',
            'verification/runtime-output.bin')),
    )
} | {'lean-local-host/docker-version.txt', 'lean-local-host/pip-freeze.txt',
     'lean-local-runtime/preparation.json'}


def require(ok: bool, detail: str) -> None:
    if not ok:
        raise ValueError(detail)


def archive_members(raw: bytes) -> dict[str, bytes]:
    """Only fixed regular members of this recorded format; never use extractall."""
    require(0 < len(raw) <= MAX_ARCHIVE_BYTES, 'Unexpected pilot archive size')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        entries = archive.infolist()
        require(len(entries) == len(FILES) and {entry.filename for entry in entries} == FILES,
                'Unexpected, duplicate or missing pilot archive member')
        require(sum(entry.file_size for entry in entries) <= MAX_EXPANDED_BYTES,
                'Pilot archive expansion exceeds the bound')
        result = {}
        for entry in entries:
            require(not entry.is_dir() and stat.S_IFMT(entry.external_attr >> 16) in (0, stat.S_IFREG)
                    and 0 <= entry.file_size <= MAX_MEMBER_BYTES,
                    'Pilot archive member is not a bounded regular file')
            with archive.open(entry) as file:
                data = file.read(MAX_MEMBER_BYTES + 1)
            require(len(data) == entry.file_size, 'Pilot archive member size mismatch')
            result[entry.filename] = data
        return result


def verify_verifier_record(directory: Path, event: dict, session: dict, preparation: dict) -> None:
    record = event['result']
    require(isinstance(record, dict) and event['input_rejection'] is None
            and record['id'] == session['id'] and record['binding_sha256'] == session['binding_sha256']
            and all(record[key] == session[key] for key in (
                'runtime_receipt_sha256', 'task_packet_sha256', 'verifier_source_sha256_lf'))
            and record['image_id'] == preparation['image_id']
            and record['policy_sha256'] == bench.sha(bench.encoded(preparation['policy'])),
            'Native verifier/task/runtime binding drift')
    verifier = directory / 'verification'
    source = (verifier / 'submission.txt').read_bytes()
    require(source == (directory / 'source.txt').read_bytes()
            and bench.sha(source) == record['submission_sha256'] == event['source_sha256'],
            'Native submitted source differs from the recorded action')
    chunks = []
    native, phase = runtime.parse_control((verifier / 'runtime-output.bin').read_bytes(),
                                          diagnostic_chunks=chunks)
    diagnostic = (verifier / 'compiler-diagnostic.bin').read_bytes()
    require(native is not None and native == record['native'] and phase == record['runtime_phase']
            and b''.join(chunks)[:preparation['policy']['limits']['diagnostic_bytes']] == diagnostic
            and bench.sha(diagnostic) == record['compiler_diagnostic_sha256'],
            'Native framed output or compiler diagnostic drift')
    state = record['container_state']
    kind = runtime.classify(state['ExitCode'], native, state, record['interruption'], phase)
    require(kind == record['kind'] and kind in {'accepted', 'proof-rejected', 'resource-limit'},
            'Recorded native result does not replay as a scored attempt')


def replay_records(root: Path, *, check_current_task: bool = False) -> dict:
    """Replay bound records from the already checked, privately unpacked archive."""
    evidence = root / EVIDENCE
    directory = evidence / 'workspace'
    transport = evidence / 'bridge'

    def raw(path: str) -> bytes:
        return (evidence / path).read_bytes()

    def record(path: str) -> dict:
        return bridge.decode(raw(path))

    session, events = workspace.history(directory)
    bridge.validate_provenance(session)
    require(tuple(event['action'] for event in events) == ACTIONS
            and session['id'] == local.TASK and session['max_checks'] == session['denominator'] == 1,
            'The archive must contain the selected check and immutable first final')
    pin = local.asset_pin()
    selection = record('pilot-selection.json')
    provenance = session['provenance']
    require(selection['id'] == session['id'] and selection['binding_sha256'] == session['binding_sha256']
            and selection['split'] == 'public-dev' and selection['selected'] == 1
            and tuple(selection['actions']) == ACTIONS and selection['system'] == local.SYSTEM
            and selection['seed'] == provenance['seed'] and provenance['provider'] == 'local-safetensors'
            and selection['model'] == provenance['model'] == pin['model']
            and selection['revision'] == provenance['model_version'] == pin['revision']
            and selection['asset_sha256'] == pin['asset_sha256']
            and selection['package_versions'] == pin['environment'],
            'Archived pilot model/selection drift')
    hashes = {name: bench.sha(raw('workspace/agent/' + name)) for name in AGENT}
    template = raw('workspace/agent/Solution.lean.txt')
    require(template.endswith(local.MARKER), 'Archived fixed proof template lost its placeholder')
    prefix = template.removesuffix(local.MARKER).decode('utf-8', errors='strict')
    visible_raw = raw('bridge/prompt.jsonl')
    visible = bridge.decode(visible_raw)
    choice_raw = raw('bridge/selection.json')
    choice = bridge.decode(choice_raw)
    session_sha = bench.sha(raw('workspace/session.json'))
    choice_sha = bench.sha(choice_raw)
    require(choice['session_sha256'] == session_sha and choice['id'] == visible['id'] == session['id']
            and choice['profile'] == visible['profile'] == bridge.PROFILE
            and choice['provenance'] == provenance and choice['automatic_retries'] == 0
            and choice['max_checks'] == visible['max_checks'] == session['max_checks']
            and choice['agent_input_hashes'] == hashes and choice['prompt_sha256'] == bench.sha(visible_raw)
            and visible['content'] == ('Prompt-only task JSON:\n' + raw('workspace/agent/prompt.json').decode('utf-8')
                                       + '\nFixed Solution.lean template:\n' + template.decode('utf-8')),
            'Archived prompt-only inputs do not match the transport selection')
    if check_current_task:
        core = next(c for c in bench.materialize() if c['id'] == session['id'])
        packet = runtime.packet(core)
        require(core['binding_sha256'] == session['binding_sha256']
                and session['task_packet_sha256'] == bench.sha(packet['operator.json'])
                and all(packet['agent/' + name] == raw('workspace/agent/' + name) for name in AGENT),
                'The current fixed task differs from the archived one')
    preparation_raw = (root / 'lean-local-runtime/preparation.json').read_bytes()
    preparation = bridge.decode(preparation_raw)
    require(bench.sha(preparation_raw) == session['runtime_receipt_sha256']
            and preparation['policy'] == runtime.policy(), 'Archived preparation or pinned runtime policy drift')
    for i, event in enumerate(events, 1):
        verify_verifier_record(directory / 'actions' / f'{i:04d}', event, session, preparation)
    raw_records = local.verify_live_records(evidence, prefix, events)
    model = [record(f'{i:02d}-model.json') for i in (1, 2)]
    for turn in model:
        for key, bound in (('input_ids', selection['max_input_tokens']),
                           ('output_ids', selection['max_new_tokens'])):
            ids = turn[key]
            require(isinstance(ids, list) and 0 < len(ids) <= bound
                    and all(type(token) is int and token >= 0 for token in ids),
                    'Archived token record violates the selected budget')
    termination = record('bridge/termination.json')
    archived_names = {f'{i:04d}-{name}' for i in (1, 2) for name in ('request.bin', 'feedback.json')}
    require(raw('bridge/termination.json') == raw('workspace/external-evidence.json')
            and termination['selection_sha256'] == choice_sha
            and termination['client_stop'] == 'first-final-submitted'
            and termination['facts']['tool_calls_returned'] == 2
            and termination['facts']['archived_files_sha256'] ==
            {name: bench.sha((transport / name).read_bytes()) for name in archived_names},
            'Archived transport termination or request/feedback bytes drift')
    outcome, interrupted, external = workspace._outcome(directory, events)
    completion = record('workspace/completion.json')
    trajectory = record('bridge/trajectory.json')
    summary = record('pilot-result.json')
    score = int(outcome == 'accepted')
    require(not interrupted and completion['session_sha256'] == session_sha
            and completion['final_submissions'] == completion['check_calls'] == completion['denominator'] == 1
            and all(completion[k] == v for k, v in external.items())
            and completion['final_outcome'] == trajectory['final_outcome'] == summary['final_outcome'] == outcome
            and completion['final_accepted'] is trajectory['final_accepted'] is (score == 1)
            and trajectory['selection_sha256'] == choice_sha
            and trajectory['completion_sha256'] == bench.sha(raw('workspace/completion.json'))
            and summary['selection_sha256'] == bench.sha(raw('pilot-selection.json'))
            and summary['trajectory_sha256'] == bench.sha(raw('bridge/trajectory.json'))
            and summary['model_feedback_evidence_sha256'] == raw_records
            and summary['model_turns'] == 2 and summary['selected'] == 1
            and summary['native_check_kind'] == events[0]['result']['kind']
            and summary['live_model_feedback_observed'] is True and summary['operator_scheduled_calls'] is True
            and summary['provider_calls'] == 0 and summary['provenance_authenticated'] is False
            and type(summary['score']) is int and summary['score'] == score,
            'Archived completion, trajectory or recorded pilot score does not replay')
    return {
        'kind': 'offline-archived-live-lean-pilot-replay', 'id': session['id'], 'split': 'public-dev',
        'model': pin['model'], 'model_revision': pin['revision'], 'selected': 1,
        'recorded_check': events[0]['result']['kind'], 'recorded_final': outcome, 'recorded_score': score,
        'recorded_output_token_counts': [len(turn['output_ids']) for turn in model],
        'recorded_output_token_ids_equal': model[0]['output_ids'] == model[1]['output_ids'],
        'recorded_proof_body_equal': model[0]['raw_text'] == model[1]['raw_text'],
        'current_task_checked': check_current_task, 'model_rerun': False, 'lean_rerun': False,
        'provenance_authenticated': False,
        'scope': 'Recorded operator-scheduled feedback diagnostic; not a new run, matched comparison or calibration.',
    }


def replay(archive: Path = ARCHIVE, *, check_current_task: bool = False) -> dict:
    with archive.open('rb') as file:
        data = file.read(MAX_ARCHIVE_BYTES + 1)
    require(bench.sha(data) == ARCHIVE_SHA256, 'Archived live-v031 pilot SHA-256 mismatch')
    members = archive_members(data)
    with tempfile.TemporaryDirectory(prefix='sog-archived-pilot-') as tmp:
        root = Path(tmp)
        for name, contents in members.items():
            dest = root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(contents)
        return {**replay_records(root, check_current_task=check_current_task),
                'archive_sha256': ARCHIVE_SHA256}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, default=ARCHIVE, help='Exact byte copy of the recorded live-v031 ZIP')
    parser.add_argument('--check-current-task', action='store_true',
                        help='Also require the current task and its agent-only files to be byte-identical')
    args = parser.parse_args()
    sys.stdout.buffer.write(bench.encoded(replay(args.archive, check_current_task=args.check_current_task)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
