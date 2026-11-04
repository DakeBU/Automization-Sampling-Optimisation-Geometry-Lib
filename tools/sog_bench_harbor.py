"""Export admitted graph tasks to Harbor; never execute submitted Lean."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import sog_bench as bench
import sog_bench_graph_review as review

HARBOR_VERSION = '0.25.0'
HARBOR_WHEEL_SHA256 = '51923ac567fc57b03279e93468b105f689628bcac2cd3d541d4e44aa5c0ec309'
BASE_IMAGE = 'python:3.12-slim-bookworm@sha256:e697c81897302a4c4333bade000d98038fbb21eb064f8ee1fd42d02ebcd9d337'
TEMPLATES = ROOT / 'benchmarks/samplingoptimisationgeometrybench/harbor'


def task_files(item: dict) -> dict[str, bytes]:
    """Project one exact reviewed task; the existing scorer is copied verbatim."""
    identity = item['id']
    if not re.fullmatch(r'sogb-g\d{3}', identity):
        raise ValueError('Only existing structural graph identities are supported')
    prompt = bench.curriculum.graph_prompts([item])[0]
    answer = {'id': identity, 'binding_sha256': item['binding_sha256'], 'attempt': 1,
              'answer': item['answer']}
    config = f'''schema_version = "1.4"
artifacts = ["/output/answer.json"]

[task]
name = "samplinglib/{identity}"
version = "1"
description = "Public-dev structural QA; not mathematical proof or Lean submission grading"

[metadata]
family = {json.dumps(item['family'])}
split = "public-dev"
track = "graph-json"
binding_sha256 = "{item['binding_sha256']}"
provisional_level = "{item['level']}"
measured_model_result = false

[agent]
timeout_sec = 120
user = "bench"

[environment]
network_mode = "no-network"
cpus = 1
memory_mb = 256
build_timeout_sec = 180

[verifier]
environment_mode = "separate"
user = "root"
timeout_sec = 30
network_mode = "no-network"
'''
    dockerfile = f'''FROM {BASE_IMAGE}
RUN useradd --create-home --uid 1000 bench && mkdir -p /app /output && touch /output/answer.json && chown -R bench:bench /output
COPY prompt.json isolation_check.py /app/
WORKDIR /app
USER bench
'''
    instruction = ('# ' + item['title'] + '\n\n'
        'Read `/app/prompt.json`. Solve the given structural snapshot question, not a theorem-necessity question. '
        'Write one UTF-8 JSON object to `/output/answer.json` (at most 65536 bytes):\n\n```json\n'
        + json.dumps({**answer, 'answer': {'nodes': [], 'entails_mathematical_necessity': False}}, indent=2)
        + '\n```\n\nThe empty node list above is a response-format example, not an answer. '
        'Keep the exact identity, binding and attempt=1. No other files are accepted as answers. '
        'Do not execute Lean. The task is public-dev, and its published solution is not a held-out test.\n')
    files = {
        'instruction.md': instruction.encode(), 'task.toml': config.encode(),
        'environment/Dockerfile': dockerfile.encode(),
        'environment/prompt.json': bench.encoded(prompt),
        'environment/isolation_check.py': (TEMPLATES / 'isolation_check.py').read_bytes().replace(b'\r\n', b'\n'),
        'tests/verify.py': (TEMPLATES / 'verify.py').read_bytes().replace(b'\r\n', b'\n'),
        'tests/sog_bench_curriculum.py': (ROOT / 'tools/sog_bench_curriculum.py').read_bytes().replace(b'\r\n', b'\n'),
        'tests/question.json': bench.encoded(item),
        'tests/test.sh': b'#!/bin/sh\nset -eu\npython -I /app/isolation_check.py --uid 0\ntest ! -e /output/agent-marker\npython -I /tests/verify.py\n',
        'solution/answer.json': bench.encoded(answer),
        'solution/solve.sh': b'#!/bin/sh\nset -eu\npython -I /app/isolation_check.py --uid 1000\ntest ! -e /tests/question.json\ntouch /output/agent-marker\ncp /solution/answer.json /output/answer.json\n',
    }
    return files


def export(output: Path, task_ids: list[str] | None = None) -> dict:
    items = bench.curriculum.graph_items()
    statuses = review.summary(items)['items']
    selected = bench.selected_graph_tasks(items, {'task_ids': task_ids}) if task_ids is not None else items
    if any(statuses[i['id']]['editorial'] not in {'accepted', 'accepted-after-repair'} for i in selected):
        raise ValueError('Only currently independently admitted graph tasks can be exported')
    # Render/validate everything before touching the requested destination.
    files = {i['id'] + '/' + name: data for i in selected for name, data in task_files(i).items()}
    for name in ('LICENSE', 'NOTICE', 'LICENSE_SCOPE.md'):
        files[name] = (ROOT / name).read_bytes().replace(b'\r\n', b'\n')
    manifest = {'schema_version': 1, 'name': 'SamplingOptimisationGeometryBench Harbor graph adapter',
                'harbor_version': HARBOR_VERSION, 'harbor_wheel_sha256': HARBOR_WHEEL_SHA256,
                'base_image': BASE_IMAGE, 'split': 'public-dev', 'track': 'graph-json',
                'task_ids': [i['id'] for i in selected], 'measured_model_result': False,
                'lean_submission_execution': False, 'native_runtime_evidence': 'separate CI run required',
                'scorer_source_sha256_lf': bench.text_hash(ROOT / 'tools/sog_bench_curriculum.py'),
                'files': {n: hashlib.sha256(data).hexdigest() for n, data in sorted(files.items())}}
    files['adapter-manifest.json'] = bench.encoded(manifest)
    output = output.resolve()
    if output.exists():
        raise ValueError('Use a fresh export directory; existing evidence is never overwritten')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='sog-harbor-', dir=output.parent) as temporary:
        stage = Path(temporary) / 'export'
        stage.mkdir()
        for name, data in files.items():
            target = stage / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        stage.rename(output)
    return manifest


def check_job(job: Path, expected_ids: list[str], reward: int) -> dict:
    """Accept only complete native software-fixture runs, including zero rewards."""
    if (not expected_ids or len(set(expected_ids)) != len(expected_ids)
            or any(not re.fullmatch(r'sogb-g\d{3}', identity) for identity in expected_ids)):
        raise ValueError('Expected nonempty unique canonical task identities')
    results = []
    for path in sorted(job.glob('*/result.json')):
        row = json.loads(path.read_text(encoding='utf-8'))
        if row.get('exception_info') is not None:
            raise ValueError('Native trial has an infrastructure/agent exception: ' + str(path))
        results.append(row)
    if len(results) != len(expected_ids) or {r['task_name'] for r in results} != {'samplinglib/' + i for i in expected_ids}:
        raise ValueError('Missing, repeated or extra native trials; never drop a failed task')
    for row in results:
        rewards = (row.get('verifier_result') or {}).get('rewards')
        if (rewards != {'reward': reward} or type(rewards['reward']) not in (int, float)):
            raise ValueError('Unexpected native verifier result: ' + str(row.get('task_name')))
    return {'scope': 'native Harbor software-fixture smoke; not a model score',
            'tasks': len(results), 'expected_reward': reward, 'complete': True}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['export', 'check-job'])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--task-id', action='append')
    parser.add_argument('--job', type=Path)
    parser.add_argument('--expect-reward', type=int, choices=[0, 1])
    args = parser.parse_args()
    if args.command == 'export':
        if args.output is None:
            parser.error('export requires --output (fresh directory)')
        report = export(args.output, args.task_id)
        print(json.dumps({'exported_tasks': report['task_ids'], 'harbor': HARBOR_VERSION}))
    else:
        if args.job is None or not args.task_id or args.expect_reward is None:
            parser.error('check-job requires --job, --task-id and --expect-reward')
        print(json.dumps(check_job(args.job, args.task_id, args.expect_reward)))


if __name__ == '__main__':
    main()
