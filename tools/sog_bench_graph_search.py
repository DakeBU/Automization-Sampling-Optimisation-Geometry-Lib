"""Operator-side JSONL tools for an admitted, bounded compiled-graph QA slice."""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import io
import json
from pathlib import Path
import re
import sys

import sog_bench as bench
import sog_bench_graph_review as review


PROFILE = 'bounded-compiled-graph-lookup-v1'
KIND = 'compiled-proof-body-constant-occurrences'
MAX_REQUEST = 8192
MAX_RESULTS = 8
PROMPT_FIELDS = ('id', 'core_id', 'family', 'split', 'title', 'question', 'targets',
                 'remove', 'required_statement_constants', 'answer_schema')


def line(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(',', ':')) + '\n').encode('ascii')


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate key')
        result[key] = value
    return result


def no_nonfinite(_):
    raise ValueError('Nonfinite JSON value')


def request(raw: bytes) -> dict:
    try:
        value = json.loads(raw.decode('utf-8'), object_pairs_hook=no_duplicates,
                           parse_constant=no_nonfinite)
    except (ValueError, RecursionError):
        return {}
    return value if isinstance(value, dict) else {}


def admitted(identity: str) -> dict:
    items = bench.curriculum.graph_items()
    item = next((item for item in items if item['id'] == identity), None)
    if (item is None or item['context']['kind'] != KIND or item['split'] != 'public-dev'
            or review.summary(items)['items'][identity]['editorial'] not in {'accepted', 'accepted-after-repair'}):
        raise ValueError('Select a currently admitted public-dev compiled-body graph task')
    return item


def prompt(item: dict, max_lookups: int) -> dict:
    graph = item['context']
    return {'kind': 'prompt', 'profile': PROFILE,
            **{key: item[key] for key in PROMPT_FIELDS if key in item},
            'evidence': {key: graph[key] for key in ('kind', 'direction', 'scope', 'truth_boundary',
                                                   'statement_profile_scope')},
            'max_lookups': max_lookups,
            'tools': {'find': {'action': 'find', 'query': '3–96 ASCII letters/digits/space/._-'},
                      'inspect': {'action': 'inspect', 'id': 'exact node identifier'},
                      'submit': {'action': 'submit', 'answer': {'nodes': 'array of distinct node IDs',
                                                               'entails_mathematical_necessity': 'boolean'}}},
            'instruction': 'Use find or inspect to read the selected graph. Queries consume budget even if invalid. '
                           'Submit your answer once. Only the exact node set and boundary judgment count.'}


def lookup(item: dict, call: dict) -> dict:
    graph = item['context']
    if call.get('action') == 'find' and set(call) == {'action', 'query'}:
        query = call['query']
        if isinstance(query, str) and re.fullmatch(r'[A-Za-z0-9 ._\-]{3,96}', query.strip()):
            needle = query.strip().casefold()
            matches = [node for node in sorted(graph['nodes']) if
                       needle in node.casefold() or needle in graph['node_labels'][node].casefold()]
            return {'kind': 'matches', 'matches': [{'id': node, 'label': graph['node_labels'][node]}
                                                  for node in matches[:MAX_RESULTS]],
                    'truncated': len(matches) > MAX_RESULTS}
    if call.get('action') == 'inspect' and set(call) == {'action', 'id'} and isinstance(call['id'], str):
        node = call['id']
        if node not in graph['node_labels']:
            return {'kind': 'unknown-node'}
        return {'kind': 'node', 'id': node, 'label': graph['node_labels'][node],
                'parents': sorted(parent for child, parent in graph['edges'] if child == node),
                'statement_constants': graph['statement_profiles'][node]}
    return {'kind': 'invalid-lookup'}


def run_trial(item: dict, max_lookups: int, source, emit, record) -> dict:
    used = 0
    terminal = 'eof-no-final'
    submission = []
    emit(prompt(item, max_lookups))
    while raw := source.readline(MAX_REQUEST + 1):
        stop = True
        if len(raw) > MAX_REQUEST:
            terminal = 'oversized-request-no-final'
            observation = {'kind': terminal}
        else:
            call = request(raw)
            if call.get('action') == 'submit':
                terminal = 'first-final'
                answer = call.get('answer') if set(call) == {'action', 'answer'} else None
                submission = [{'id': item['id'], 'binding_sha256': item['binding_sha256'],
                               'attempt': 1, 'answer': answer}]
                observation = {'kind': 'final-recorded'}
            elif used == max_lookups:
                terminal = 'lookup-budget-exhausted-no-final'
                observation = {'kind': terminal}
            else:
                stop = False
                used += 1
                observation = {**lookup(item, call), 'remaining_lookups': max_lookups - used}
        record({'request_base64': base64.b64encode(raw).decode('ascii'),
                'request_is_oversize_prefix': len(raw) > MAX_REQUEST, 'observation': observation})
        emit(observation)
        if stop:
            break
    return {'termination': terminal, 'lookups_used': used,
            'score': bench.curriculum.grade_graph([item], submission), 'model_measurement': False}


def session_binding(item: dict, max_lookups: int) -> dict:
    if type(max_lookups) is not int or not 1 <= max_lookups <= 16:
        raise ValueError('Declare between 1 and 16 lookup calls')
    return {'schema_version': 1, 'profile': PROFILE, 'id': item['id'], 'family': item['family'],
            'binding_sha256': item['binding_sha256'], 'graph_sha256': item['graph_sha256'],
            'operator_task_sha256': bench.sha(bench.encoded(item)), 'max_lookups': max_lookups,
            'prompt_sha256': bench.sha(line(prompt(item, max_lookups))),
            'runner_sha256_lf': bench.text_hash(Path(__file__)),
            'scorer_sha256_lf': bench.text_hash(Path(bench.curriculum.__file__)),
            'split': 'public-dev', 'selected_denominator': 1, 'provenance_authenticated': False}


def write_new(path: Path, payload: bytes) -> None:
    with path.open('xb') as stream:
        stream.write(payload)


def archive(item: dict, max_lookups: int, output: Path, source, emit) -> dict:
    session = {**session_binding(item, max_lookups), 'created_at': datetime.now(timezone.utc).isoformat()}
    output.mkdir(parents=True, exist_ok=False)
    write_new(output / 'session.json', bench.encoded(session))
    write_new(output / 'operator-task.json', bench.encoded(item))
    write_new(output / 'agent-prompt.json', line(prompt(item, max_lookups)))
    log = output / 'actions.jsonl'
    with log.open('xb') as trace:
        def record(event):
            trace.write(line(event))
            trace.flush()
        result = run_trial(item, max_lookups, source, emit, record)
    report = {**result, 'session_sha256': bench.sha((output / 'session.json').read_bytes()),
              'actions_sha256': bench.sha(log.read_bytes())}
    write_new(output / 'report.json', bench.encoded(report))
    return report


def replay(directory: Path, item: dict) -> dict:
    session_raw = (directory / 'session.json').read_bytes()
    session = json.loads(session_raw)
    max_lookups = session['max_lookups']
    if (session_binding(item, max_lookups) != {k: v for k, v in session.items() if k != 'created_at'}
            or (directory / 'operator-task.json').read_bytes() != bench.encoded(item)
            or (directory / 'agent-prompt.json').read_bytes() != line(prompt(item, max_lookups))):
        raise ValueError('Task, prompt, or executable binding drift')
    raw = (directory / 'actions.jsonl').read_bytes()
    events = [json.loads(row) for row in raw.splitlines()]
    requests = b''.join(base64.b64decode(event['request_base64'], validate=True) for event in events)
    observations = []
    result = run_trial(item, max_lookups, io.BytesIO(requests), lambda _: None, observations.append)
    report = {**result, 'session_sha256': bench.sha(session_raw), 'actions_sha256': bench.sha(raw)}
    if (events != observations or raw != b''.join(map(line, observations))
            or (directory / 'report.json').read_bytes() != bench.encoded(report)):
        raise ValueError('Recorded transcript or result differs from exact replay')
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest='command', required=True)
    run = actions.add_parser('run')
    run.add_argument('--task-id', required=True)
    run.add_argument('--max-lookups', type=int, default=8)
    run.add_argument('--output', required=True, type=Path)
    check = actions.add_parser('replay')
    check.add_argument('--run', required=True, type=Path)
    args = parser.parse_args()
    if args.command == 'run':
        def emit(row):
            sys.stdout.buffer.write(line(row))
            sys.stdout.buffer.flush()
        archive(admitted(args.task_id), args.max_lookups, args.output, sys.stdin.buffer, emit)
    else:
        session = json.loads((args.run / 'session.json').read_bytes())
        sys.stdout.buffer.write(bench.encoded(replay(args.run, admitted(session['id']))))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
