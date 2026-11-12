"""Compare the same recorded Lean check with and without its diagnostic text."""
from __future__ import annotations

import argparse
from pathlib import Path
import platform
import sys

import sog_bench_pilot_replay as archived

bench, bridge, local = archived.bench, archived.bridge, archived.local
CONDITIONS = ('status-only', 'diagnostic')
WITHHELD = '[diagnostic text withheld]'
MAX_RECORD = 256 * 1024


def context() -> tuple[dict, bytes, bytes, dict]:
    """Freeze the verified public archive; never import its reference proof."""
    replay = archived.replay(check_current_task=True)
    with archived.ARCHIVE.open('rb') as file:
        raw = file.read(archived.MAX_ARCHIVE_BYTES + 1)
    archived.require(bench.sha(raw) == replay['archive_sha256'], 'Archived context changed')
    members = archived.archive_members(raw)

    def read(name: str) -> bytes:
        return members[archived.EVIDENCE + name]

    first = bridge.decode(read('01-model.json'))
    feedback = bridge.decode(read('bridge/0001-feedback.json'))
    template = read('workspace/agent/Solution.lean.txt')
    prefix = template.removesuffix(local.MARKER)
    final = read('workspace/actions/0002/verification/submission.txt')
    common = [*first['messages'], {'role': 'assistant', 'content': first['raw_text']}]
    views = {}
    for condition in CONDITIONS:
        observation = feedback if condition == 'diagnostic' else {**feedback, 'diagnostic': WITHHELD}
        frame = bridge.line({'kind': 'lean-workspace-feedback', 'feedback': observation})
        views[condition] = [*common, local.feedback_message(frame)]
    pin = local.asset_pin()
    plan = {
        'schema_version': 1, 'kind': 'frozen-check-diagnostic-text-ablation-v1',
        'archive_sha256': replay['archive_sha256'], 'id': replay['id'], 'split': replay['split'],
        'condition_order': list(CONDITIONS), 'messages_by_condition': views,
        'recorded_first_turn_sha256': bench.sha(read('01-model.json')),
        'recorded_check_feedback_sha256': bench.sha(read('bridge/0001-feedback.json')),
        'recorded_final_submission_sha256': bench.sha(final),
        'proof_prefix_sha256': bench.sha(prefix),
        'model': pin['model'], 'revision': pin['revision'], 'asset_sha256': pin['asset_sha256'],
        'packages': pin['environment'], 'seed': local.SEED, 'cpu_threads': local.THREADS,
        'max_input_tokens': local.INPUT_TOKENS, 'max_new_tokens': local.OUTPUT_TOKENS,
        'decoding': 'greedy-cpu-float32',
        'recorder_sha256_lf': bench.text_hash(Path(__file__)),
        'inference_source_sha256_lf': bench.text_hash(Path(local.__file__)),
        'scope': 'Two new second-turn generations with a common recorded check, not a live verifier or autonomous tool selection.',
    }
    return plan, prefix, final, replay


def candidate(prefix: bytes, turn: dict, plan: dict) -> bytes:
    archived.require(set(turn) == {'input_ids', 'output_ids', 'raw_text'}
                     and isinstance(turn['raw_text'], str), 'Unexpected model record')
    for key, limit in (('input_ids', plan['max_input_tokens']), ('output_ids', plan['max_new_tokens'])):
        ids = turn[key]
        archived.require(isinstance(ids, list) and 0 < len(ids) <= limit
                         and all(type(x) is int and x >= 0 for x in ids), 'Invalid model token record')
    return prefix + turn['raw_text'].encode('utf-8', errors='strict')


def read_bounded(path: Path) -> bytes:
    archived.require(path.is_file() and not path.is_symlink(), 'Missing or unsafe ablation record')
    with path.open('rb') as file:
        raw = file.read(MAX_RECORD + 1)
    archived.require(len(raw) <= MAX_RECORD, 'Ablation record exceeds its byte bound')
    return raw


def summarize(output: Path, fixed: tuple) -> dict:
    plan, prefix, archived_final, replay = fixed
    raw_plan = read_bounded(output / 'plan.json')
    saved = bridge.decode(raw_plan)
    host = saved.pop('operator_environment')
    archived.require(saved == plan and isinstance(host, dict) and set(host) == {'system', 'python'}
                     and all(isinstance(v, str) and v.strip() for v in host.values()),
                     'Ablation plan, host labels or frozen condition drift')
    records, rows = {}, {}
    for condition in CONDITIONS:
        raw = read_bounded(output / f'{condition}-model.json')
        row = bridge.decode(raw)
        turn = row['turn']
        expected = candidate(prefix, turn, plan)
        archived.require(row['plan_sha256'] == bench.sha(raw_plan) and row['condition'] == condition
                         and row['messages'] == plan['messages_by_condition'][condition]
                         and expected == read_bounded(output / f'{condition}-candidate.lean.txt')
                         and bench.sha(expected) == row['candidate_sha256'],
                         'Ablation candidate, prompt or plan drift')
        records[condition] = turn
        matched = expected == archived_final
        rows[condition] = {
            'model_record_sha256': bench.sha(raw), 'candidate_sha256': bench.sha(expected),
            'input_token_count': len(turn['input_ids']), 'output_token_count': len(turn['output_ids']),
            'matches_archived_native_submission': matched,
            'reused_archived_native_result': replay['recorded_final'] if matched else None,
            'reused_archived_score': replay['recorded_score'] if matched else None,
        }
    return {
        'schema_version': 1, 'kind': 'recorded-lean-diagnostic-text-ablation',
        'plan_sha256': bench.sha(raw_plan), 'id': plan['id'], 'split': 'public-dev',
        'conditions': rows,
        'output_token_ids_equal': records[CONDITIONS[0]]['output_ids'] == records[CONDITIONS[1]]['output_ids'],
        'proof_bodies_equal': records[CONDITIONS[0]]['raw_text'] == records[CONDITIONS[1]]['raw_text'],
        'fresh_native_verification': False, 'provider_calls': 0, 'provenance_authenticated': False,
        'scope': 'One paired second-turn inference diagnostic, not held-out performance, calibration, or live proof repair.',
    }


def record(model_directory: Path, output: Path) -> dict:
    fixed = context()
    plan, prefix, _, _ = fixed
    pin = local.asset_pin()
    local.check_assets(model_directory, pin)
    output.mkdir(parents=True, exist_ok=False)
    plan_file = output / 'plan.json'
    local.workspace.write_new(plan_file, {**plan, 'operator_environment': {
        'system': platform.platform(), 'python': platform.python_version()}})
    plan_hash = local.digest(plan_file)
    generate = local.CpuModel(model_directory, pin['environment'])
    for condition in CONDITIONS:
        messages = plan['messages_by_condition'][condition]
        try:
            turn = generate(messages)
        except (ImportError, OSError, RuntimeError, ValueError) as error:
            local.workspace.write_new(output / f'{condition}-infrastructure-error.json',
                                      {'condition': condition, 'plan_sha256': plan_hash, 'score': None})
            raise RuntimeError('Ablation inference did not return both selected responses') from error
        source = candidate(prefix, turn, plan)
        with (output / f'{condition}-candidate.lean.txt').open('xb') as file:
            file.write(source)
        local.workspace.write_new(output / f'{condition}-model.json', {
            'plan_sha256': plan_hash, 'condition': condition, 'messages': messages,
            'turn': turn, 'candidate_sha256': bench.sha(source)})
    result = summarize(output, fixed)
    local.workspace.write_new(output / 'comparison.json', result)
    return result


def verify(output: Path) -> dict:
    result = summarize(output, context())
    archived.require(bench.encoded(result) == read_bounded(output / 'comparison.json'),
                     'Ablation comparison does not replay from its raw records')
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    run = commands.add_parser('record')
    run.add_argument('--model-directory', required=True, type=Path)
    run.add_argument('--output', required=True, type=Path)
    audit = commands.add_parser('replay')
    audit.add_argument('--run', required=True, type=Path)
    args = parser.parse_args()
    result = record(args.model_directory, args.output) if args.command == 'record' else verify(args.run)
    sys.stdout.buffer.write(bench.encoded(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
