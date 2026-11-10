"""Freeze, record and replay paired public-dev graph access conditions (JSONL)."""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import io
from pathlib import Path
import re
import sys

import sog_bench_graph_search as graph
from sog_bench_graph_model_replay import Archive, directory_members, plain

bench = graph.bench
SNAPSHOT = 'given-snapshot'
PROFILES = (SNAPSHOT, graph.PROFILE)
TASK_ID = re.compile(r'sogb-g[0-9]{3}')
MAX_TASKS = 16


def visible_prompt(item: dict, profile: str, max_lookups: int) -> bytes:
    prompt = graph.prompt(item, max_lookups)
    if profile == SNAPSHOT:
        prompt.update(profile=SNAPSHOT, max_lookups=0,
                      tools={'submit': prompt['tools']['submit']},
                      instruction='Use the supplied graph snapshot. No lookup is available. Submit once.',
                      snapshot={key: item['context'][key] for key in
                                ('nodes', 'node_labels', 'edges', 'statement_profiles')})
    elif profile != graph.PROFILE:
        raise ValueError('Unknown graph access condition')
    return graph.line(prompt)


def admitted_tasks(ids: list[str]) -> list[dict]:
    if (not isinstance(ids, list) or not 1 <= len(ids) <= MAX_TASKS
            or not all(isinstance(i, str) and TASK_ID.fullmatch(i) for i in ids)
            or len(set(ids)) != len(ids)):
        raise ValueError('Select 1–16 distinct graph task IDs')
    items = bench.curriculum.graph_items()
    decisions = graph.review.summary(items)['items']
    eligible = {x['id']: x for x in items if x['split'] == 'public-dev'
                and x['context']['kind'] == graph.KIND
                and decisions[x['id']]['editorial'] in {'accepted', 'accepted-after-repair'}}
    if not set(ids) <= eligible.keys():
        raise ValueError('Only currently admitted public-dev compiled-body tasks are eligible')
    return [eligible[i] for i in ids]


def selection(items: list[dict], max_lookups: int, provenance: dict, created_at: str) -> dict:
    if type(max_lookups) is not int or not 1 <= max_lookups <= 16:
        raise ValueError('Declare 1–16 lookups per bounded condition')
    if len({x['family'] for x in items}) != len(items):
        raise ValueError('Select at most one item per family in a paired suite')
    if (not isinstance(provenance, dict) or set(provenance) != {'kind', 'agent', 'revision', 'settings'}
            or provenance['kind'] not in ('declared-agent', 'controlled-software-fixture')
            or not all(isinstance(provenance[k], str) and 0 < len(provenance[k].strip()) <= 240
                       for k in ('agent', 'revision'))
            or not isinstance(provenance['settings'], dict) or len(bench.encoded(provenance)) > 8192):
        raise ValueError('Declare the agent, exact revision and bounded settings before any run')
    if datetime.fromisoformat(created_at).tzinfo is None:
        raise ValueError('Selection timestamp requires a timezone')
    return {'schema_version': 1, 'kind': 'public-dev-paired-graph-jsonl',
            'created_at': created_at, 'split': 'public-dev', 'provenance': provenance,
            'attempt_policy': 'first-final-no-retries', 'max_lookups': max_lookups,
            'suite_source_sha256_lf': bench.text_hash(Path(__file__)),
            'engine_sha256_lf': bench.text_hash(Path(graph.__file__)),
            'scorer_sha256_lf': bench.text_hash(Path(bench.curriculum.__file__)),
            'selected': [
                {'id': x['id'], 'family': x['family'], 'level': x['level'],
                 'operator_task_sha256': bench.sha(bench.encoded(x)),
                 'prompts': {p: bench.sha(visible_prompt(x, p, max_lookups)) for p in PROFILES}}
                for x in items]}


def plan(root: Path, ids: list[str], max_lookups: int, provenance: dict) -> str:
    items = admitted_tasks(ids)
    frozen = selection(items, max_lookups, provenance, datetime.now(timezone.utc).isoformat())
    raw = bench.encoded(frozen)
    root.mkdir(parents=True, exist_ok=False)
    graph.write_new(root / 'selection.json', raw)
    (root / 'prompts').mkdir()
    (root / 'runs').mkdir()
    for item in items:
        folder = root / 'prompts' / item['id']
        folder.mkdir()
        for p in PROFILES:
            graph.write_new(folder / (p + '.json'), visible_prompt(item, p, max_lookups))
    return bench.sha(raw)


def load(root: Path, expected: str) -> tuple[dict, dict[str, dict]]:
    directory_members(root, {'selection.json', 'prompts', 'runs'})
    archive = Archive(root)
    raw = archive.raw(root / 'selection.json')
    if bench.sha(raw) != expected:
        raise ValueError('Selection digest mismatch; supply the digest saved at planning')
    data = graph.request(raw)
    try:
        items = admitted_tasks([x['id'] for x in data['selected']])
        exact = selection(items, data['max_lookups'], data['provenance'], data['created_at'])
    except (TypeError, KeyError, AttributeError) as error:
        raise ValueError('Malformed graph suite plan') from error
    if bench.encoded(exact) != raw:
        raise ValueError('Graph suite plan, task, or executable binding drift')
    directory_members(root / 'prompts', {x['id'] for x in items})
    for item in items:
        folder = root / 'prompts' / item['id']
        directory_members(folder, {p + '.json' for p in PROFILES})
        for p in PROFILES:
            archive.equal(folder / (p + '.json'), visible_prompt(item, p, data['max_lookups']))
    plain(root / 'runs', directory=True)
    return exact, {x['id']: x for x in items}


def evaluate(item: dict, profile: str, max_lookups: int, source, emit, observe) -> dict:
    # The engine's first emission is its native lookup prompt. Substitute the
    # frozen access projection; never forward the operator item or score.
    first = True
    def forward(row):
        nonlocal first
        emit(visible_prompt(item, profile, max_lookups) if first else graph.line(row))
        first = False
    budget = 0 if profile == SNAPSHOT else max_lookups
    return graph.run_trial(item, budget, source, forward, observe)


def reserve_bytes(digest: str, identity: str, profile: str) -> bytes:
    return bench.encoded({'selection_sha256': digest, 'id': identity, 'profile': profile})


def record(root: Path, digest: str, identity: str, profile: str, source, emit) -> dict:
    frozen, items = load(root, digest)
    if identity not in items or profile not in PROFILES:
        raise ValueError('Select a predeclared task and access condition')
    folder = root / 'runs' / identity
    folder.mkdir(exist_ok=True)
    plain(folder, directory=True)
    case = folder / profile
    case.mkdir(exist_ok=False)  # reserve before reading even one action
    graph.write_new(case / 'started.json', reserve_bytes(digest, identity, profile))
    with (case / 'actions.jsonl').open('xb') as output:
        def observe(event):
            output.write(graph.line(event))
            output.flush()
        result = evaluate(items[identity], profile, frozen['max_lookups'], source, emit, observe)
    return persist_result(case, result)


def persist_result(case: Path, result: dict) -> dict:
    report = {'schema_version': 1, **result,
              'actions_sha256': bench.sha((case / 'actions.jsonl').read_bytes()),
              'reservation_sha256': bench.sha((case / 'started.json').read_bytes())}
    graph.write_new(case / 'result.json', bench.encoded(report))
    return report


def replay_case(root: Path, item: dict, profile: str, max_lookups: int, digest: str) -> dict:
    identity = item['id']
    case = root / 'runs' / identity / profile
    row = {'id': identity, 'family': item['family'], 'points': None, 'termination': 'not-started',
           'valid_final': None, 'lookups_used': None, 'result_sha256': None}
    if not case.exists() and not case.is_symlink():
        return row
    plain(case, directory=True)
    members = {p.name for p in case.iterdir()}
    if members not in (set(), {'started.json'}, {'started.json', 'actions.jsonl'},
                       {'started.json', 'actions.jsonl', 'result.json'}):
        raise ValueError('Unexpected case archive entries')
    archive = Archive(root)
    if 'started.json' in members:
        archive.equal(case / 'started.json', reserve_bytes(digest, identity, profile))
    if 'result.json' not in members:
        if 'actions.jsonl' in members:
            archive.raw(case / 'actions.jsonl')
        return {**row, 'termination': 'unfinished-archive'}
    actions = archive.raw(case / 'actions.jsonl')
    records = actions.splitlines(keepends=True)
    max_events = 1 if profile == SNAPSHOT else max_lookups + 1
    if len(records) > max_events:
        raise ValueError('Action count exceeds declared access budget')
    requests = []
    for line in records:
        obj = graph.request(line)
        try:
            raw = base64.b64decode(obj['request_base64'], validate=True)
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError('Malformed raw action in transcript') from error
        if not 0 < len(raw) <= graph.MAX_REQUEST + 1:
            raise ValueError('Archived action exceeds wire bounds')
        requests.append(raw)
    events = []
    result = evaluate(item, profile, max_lookups, io.BytesIO(b''.join(requests)), lambda _: None, events.append)
    if actions != b''.join(map(graph.line, events)):
        raise ValueError('Raw graph actions or observations differ from replay')
    report = {'schema_version': 1, **result, 'actions_sha256': bench.sha(actions),
              'reservation_sha256': bench.sha(reserve_bytes(digest, identity, profile))}
    raw = bench.encoded(report)
    archive.equal(case / 'result.json', raw)
    return {**row, 'termination': result['termination'], 'points': result['score']['points'],
            'valid_final': any(r['valid_schema'] for r in result['score']['results']),
            'lookups_used': result['lookups_used'], 'result_sha256': bench.sha(raw)}


def account(root: Path, digest: str) -> dict:
    frozen, items = load(root, digest)
    for folder in (root / 'runs').iterdir():
        if folder.name not in items:
            raise ValueError('Unexpected task in suite run directory')
        plain(folder, directory=True)
        if not {p.name for p in folder.iterdir()} <= set(PROFILES):
            raise ValueError('Unexpected profile in suite run directory')
    rows = {p: [replay_case(root, item, p, frozen['max_lookups'], digest) for item in items.values()]
            for p in PROFILES}
    pairs = [identity for j, identity in enumerate(items)
             if all(rows[p][j]['points'] is not None for p in PROFILES)]
    return {'schema_version': 1, 'kind': 'paired-graph-suite-accounting', 'selection_sha256': digest,
            'split': 'public-dev', 'selected_per_condition': len(items), 'paired_replayed_ids': pairs,
            'conditions': {p: {'replayed': sum(r['points'] is not None for r in rows[p]),
                               'observed_points': sum(r['points'] or 0 for r in rows[p]),
                               'rows': rows[p]} for p in PROFILES},
            'provenance_authenticated': False, 'model_measurement_certified': False,
            'scope': 'All selected rows kept; unfinished/unstarted are null, not proof failures. '
                     'Observed points are sums over replayed rows, not a calibrated or unseen model score.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    setup = commands.add_parser('plan')
    setup.add_argument('--task-id', required=True, action='append')
    setup.add_argument('--max-lookups', type=int, default=8)
    setup.add_argument('--provenance', required=True, type=Path)
    for command in ('record', 'account'):
        child = commands.add_parser(command)
        child.add_argument('--plan-sha256', required=True)
        if command == 'record':
            child.add_argument('--task-id', required=True)
            child.add_argument('--profile', required=True, choices=PROFILES)
    for child in commands.choices.values():
        child.add_argument('--suite', required=True, type=Path)
    args = parser.parse_args()
    if args.command == 'plan':
        raw = Archive(args.provenance.parent).raw(args.provenance)
        print(plan(args.suite, args.task_id, args.max_lookups, graph.request(raw)))
    elif args.command == 'record':
        def emit(raw):
            sys.stdout.buffer.write(raw)
            sys.stdout.buffer.flush()
        record(args.suite, args.plan_sha256, args.task_id, args.profile, sys.stdin.buffer, emit)
    else:
        sys.stdout.buffer.write(bench.encoded(account(args.suite, args.plan_sha256)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
