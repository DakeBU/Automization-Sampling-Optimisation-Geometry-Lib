"""Export admitted graph tasks to Harbor; never execute submitted Lean."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import sog_bench as bench
import sog_bench_graph_review as review

HARBOR_VERSION = '0.25.0'
HARBOR_WHEEL_SHA256 = '51923ac567fc57b03279e93468b105f689628bcac2cd3d541d4e44aa5c0ec309'
BASE_IMAGE = 'python:3.12-slim-bookworm@sha256:e697c81897302a4c4333bade000d98038fbb21eb064f8ee1fd42d02ebcd9d337'
TEMPLATES = ROOT / 'benchmarks/samplingoptimisationgeometrybench/harbor'
FIXTURES = ('oversize', 'symlink', 'fifo', 'missing', 'hook-failure')


def task_files(item: dict, fixture: str | None = None) -> dict[str, bytes]:
    """Project one exact reviewed task; the existing scorer is copied verbatim."""
    identity = item['id']
    if not re.fullmatch(r'sogb-g\d{3}', identity):
        raise ValueError('Only existing structural graph identities are supported')
    prompt = bench.curriculum.graph_prompts([item])[0]
    answer = {'id': identity, 'prompt_sha256': prompt['prompt_sha256'], 'attempt': 1,
              'answer': item['answer']}
    config = f'''schema_version = "1.4"
artifacts = ["/handoff/answer.bin", "/handoff/collection.json"]

[task]
name = "samplinglib/{identity}"
version = "3"
description = "Public-dev structural QA; not mathematical proof or Lean submission grading"

[metadata]
family = {json.dumps(item['family'])}
split = "public-dev"
track = "graph-json"
prompt_sha256 = "{prompt['prompt_sha256']}"
provisional_level = "{item['level']}"
measured_model_result = false
network_contract = "Docker compose network_mode:none; Harbor public means no additional egress controller"

[agent]
timeout_sec = 120
user = "bench"

[environment]
network_mode = "public"
cpus = 1
memory_mb = 256
build_timeout_sec = 180

[verifier]
environment_mode = "separate"
user = "root"
timeout_sec = 30
network_mode = "public"

[[verifier.collect]]
command = "python -I /app/collect_answer.py"
service = "main"
user = "root"
timeout_sec = 5
'''
    dockerfile = f'''FROM {BASE_IMAGE}
RUN useradd --create-home --uid 1000 bench && mkdir -p /app /output /handoff && chmod 0700 /handoff && touch /output/answer.json && chown -R bench:bench /output
COPY prompt.json isolation_check.py bench_bounded_io.py collect_answer.py /app/
WORKDIR /app
USER bench
'''
    instruction = ('# ' + item['title'] + '\n\n'
        'Read `/app/prompt.json`. Solve the given structural snapshot question, not a theorem-necessity question. '
        'Write one UTF-8 JSON object to `/output/answer.json` (at most 65536 bytes):\n\n```json\n'
        + json.dumps({**answer, 'answer': {'nodes': [], 'entails_mathematical_necessity': False}}, indent=2)
        + '\n```\n\nThe empty node list above is a response-format example, not an answer. '
        'Keep the exact identity, public prompt fingerprint and attempt=1. No other files are accepted as answers. '
        'Do not execute Lean. The task is public-dev, and its published solution is not a held-out test.\n')
    files = {
        'instruction.md': instruction.encode(), 'task.toml': config.encode(),
        'environment/Dockerfile': dockerfile.encode(),
        # Disable all container networking intrinsically. Harbor 0.25's
        # no-network controller instead retains DNS/ICMP via an egress sidecar.
        # The public phase policy adds no controller; it cannot give this
        # network_mode:none container an external interface.
        'environment/docker-compose.yaml': b'''services:
  main:
    build:
      context: ${CONTEXT_DIR}
      dockerfile: Dockerfile
    command: ["sh", "-c", "sleep infinity"]
    network_mode: none
    cpus: 1
    mem_limit: 256m
    pids_limit: 128
    security_opt:
      - no-new-privileges:true
''',
        'environment/prompt.json': bench.encoded(prompt),
        'environment/isolation_check.py': (TEMPLATES / 'isolation_check.py').read_bytes().replace(b'\r\n', b'\n'),
        'environment/bench_bounded_io.py': (TEMPLATES / 'bench_bounded_io.py').read_bytes().replace(b'\r\n', b'\n'),
        'environment/collect_answer.py': (TEMPLATES / 'collect_answer.py').read_bytes().replace(b'\r\n', b'\n'),
        'tests/verify.py': (TEMPLATES / 'verify.py').read_bytes().replace(b'\r\n', b'\n'),
        'tests/bench_bounded_io.py': (TEMPLATES / 'bench_bounded_io.py').read_bytes().replace(b'\r\n', b'\n'),
        'tests/collect_answer.py': (TEMPLATES / 'collect_answer.py').read_bytes().replace(b'\r\n', b'\n'),
        'tests/sog_bench_curriculum.py': (ROOT / 'tools/sog_bench_curriculum.py').read_bytes().replace(b'\r\n', b'\n'),
        'tests/question.json': bench.encoded(item),
        'tests/test.sh': b'#!/bin/sh\nset -eu\npython -I /app/isolation_check.py --uid 0\ntest ! -e /output/agent-marker\npython -I /tests/verify.py\n',
        'solution/answer.json': bench.encoded(answer),
        'solution/solve.sh': b'#!/bin/sh\nset -eu\npython -I /app/isolation_check.py --uid 1000\ntest ! -w /handoff\ntest ! -e /tests/question.json\ntouch /output/agent-marker\ncp /solution/answer.json /output/answer.json\n',
    }
    if fixture is not None:
        if fixture not in FIXTURES:
            raise ValueError('Unknown controlled transport fixture')
        files['task.toml'] = files['task.toml'].replace(b'measured_model_result = false',
            b'measured_model_result = false\nsoftware_fixture = "' + fixture.encode() + b'"')
        if fixture == 'hook-failure':
            files['task.toml'] = files['task.toml'].replace(b'command = "python -I /app/collect_answer.py"', b'command = "false"')
        else:
            script = "from pathlib import Path; import os; p=Path('/output/answer.json'); "
            if fixture == 'oversize':
                script += "p.write_bytes(b'x'*65537)"
            else:
                script += 'p.unlink(); '
                script += {'symlink': "p.symlink_to('/app/prompt.json')", 'fifo': 'os.mkfifo(p)', 'missing': 'pass'}[fixture]
            files['solution/solve.sh'] = files['solution/solve.sh'].replace(
                b'cp /solution/answer.json /output/answer.json', b'python -I -c "' + script.encode() + b'"')
    return files


def package_files(selected: list[dict], statuses: dict, fixture: str | None = None) -> tuple[dict[str, bytes], dict]:
    """Build the same full operator package for CLI exports and website downloads."""
    if any(statuses[i['id']]['editorial'] not in {'accepted', 'accepted-after-repair'} for i in selected):
        raise ValueError('Only currently independently admitted graph tasks can be exported')
    files = {i['id'] + '/' + name: data for i in selected for name, data in task_files(i, fixture).items()}
    for name in ('LICENSE', 'NOTICE', 'LICENSE_SCOPE.md'):
        files[name] = (ROOT / name).read_bytes().replace(b'\r\n', b'\n')
    manifest = {'schema_version': 1, 'name': 'SamplingOptimisationGeometryBench Harbor graph adapter',
                'harbor_version': HARBOR_VERSION, 'harbor_wheel_sha256': HARBOR_WHEEL_SHA256,
                'base_image': BASE_IMAGE, 'split': 'public-dev', 'track': 'graph-json',
                'producer_lean_toolchain': (ROOT / 'lean-toolchain').read_text().strip(),
                'producer_mathlib_manifest_sha256_lf': bench.text_hash(ROOT / 'lake-manifest.json'),
                'task_ids': [i['id'] for i in selected], 'measured_model_result': False,
                'lean_submission_execution': False, 'native_runtime_evidence': 'separate CI run required',
                'collection_policy': 'bounded-answer-before-transfer-v1',
                'software_fixture': fixture,
                'collection_bounds': {'answer_bytes': 65536, 'receipt_bytes': 1024,
                                      'scope': 'declared answer channel, not automatic logs or total storage'},
                'editorial_evidence': {i['id']: statuses[i['id']] for i in selected},
                'scorer_source_sha256_lf': bench.text_hash(ROOT / 'tools/sog_bench_curriculum.py'),
                'files': {n: hashlib.sha256(data).hexdigest() for n, data in sorted(files.items())}}
    files['adapter-manifest.json'] = bench.encoded(manifest)
    return files, manifest


def archive(selected: list[dict]) -> bytes:
    current = bench.curriculum.graph_items()
    known = {i['id']: i for i in current}
    if any(i != known.get(i['id']) for i in selected) or len({i['id'] for i in selected}) != len(selected):
        raise ValueError('Archive must retain exact current graph tasks without duplicates')
    files, _ = package_files(selected, review.summary(current)['items'])
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, content in sorted(files.items()):
            member = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            member.create_system = 3
            member.external_attr = 0o100644 << 16
            member.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(member, content)
    return payload.getvalue()


def export(output: Path, task_ids: list[str] | None = None, fixture: str | None = None) -> dict:
    items = bench.curriculum.graph_items()
    statuses = review.summary(items)['items']
    selected = bench.selected_graph_tasks(items, {'task_ids': task_ids}) if task_ids is not None else items
    # Render/validate everything before touching the requested destination.
    files, manifest = package_files(selected, statuses, fixture)
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


def check_job(job: Path, expected_ids: list[str], reward: int, rejection: str | None = None) -> dict:
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
        # Verify actual host-transferred payload sizes, not only a declared cap.
        handoff = path.parent / 'artifacts/handoff'
        raw_path, receipt_path = handoff / 'answer.bin', handoff / 'collection.json'
        if raw_path.stat().st_size > 65536 or receipt_path.stat().st_size > 1024:
            raise ValueError('Host-transferred answer artifacts exceed the fixed bounds')
        raw = raw_path.read_bytes()
        receipt = json.loads(receipt_path.read_text(encoding='utf-8'))
        if (receipt.get('policy') != 'bounded-answer-before-transfer-v1'
                or receipt.get('raw_bytes') != len(raw)
                or receipt.get('raw_sha256') != hashlib.sha256(raw).hexdigest()
                or receipt.get('status') != ('rejected' if rejection else 'captured')
                or receipt.get('reason') != rejection):
            raise ValueError('Unexpected native collection receipt')
    if len(results) != len(expected_ids) or {r['task_name'] for r in results} != {'samplinglib/' + i for i in expected_ids}:
        raise ValueError('Missing, repeated or extra native trials; never drop a failed task')
    for row in results:
        rewards = (row.get('verifier_result') or {}).get('rewards')
        if (rewards != {'reward': reward} or type(rewards['reward']) not in (int, float)):
            raise ValueError('Unexpected native verifier result: ' + str(row.get('task_name')))
    return {'scope': 'native Harbor software-fixture smoke; not a model score',
            'tasks': len(results), 'expected_reward': reward, 'complete': True}


def check_failed_collection(job: Path, expected_ids: list[str]) -> dict:
    """Controlled failed-hook test only; never reinterpret this as model zeroes."""
    if not expected_ids or len(set(expected_ids)) != len(expected_ids):
        raise ValueError('Expected unique fixture identities')
    results = [(p, json.loads(p.read_text(encoding='utf-8'))) for p in job.glob('*/result.json')]
    if len(results) != len(expected_ids) or {r['task_name'] for _, r in results} != {'samplinglib/' + i for i in expected_ids}:
        raise ValueError('Missing or duplicate failed-hook fixture trials')
    for path, row in results:
        if ((row.get('exception_info') or {}).get('exception_type') != 'RewardFileNotFoundError'
                or (row.get('verifier_result') or {}).get('rewards') is not None
                or (path.parent / 'artifacts/handoff/collection.json').exists()):
            raise ValueError('Failed hook was not rejected as an unscored infrastructure failure')
    return {'scope': 'controlled failed-hook software fixture; no model score',
            'tasks': len(results), 'unscored_infrastructure_failure': True}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['export', 'check-job', 'check-failed-collection'])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--task-id', action='append')
    parser.add_argument('--job', type=Path)
    parser.add_argument('--expect-reward', type=int, choices=[0, 1])
    parser.add_argument('--fixture', choices=FIXTURES, help='Controlled software test only, never new benchmark questions')
    parser.add_argument('--expect-rejection', choices=['too-large', 'symlink', 'not-regular', 'missing'])
    args = parser.parse_args()
    if args.command == 'export':
        if args.output is None:
            parser.error('export requires --output (fresh directory)')
        report = export(args.output, args.task_id, args.fixture)
        print(json.dumps({'exported_tasks': report['task_ids'], 'harbor': HARBOR_VERSION}))
    elif args.command == 'check-failed-collection':
        if args.job is None or not args.task_id:
            parser.error('check-failed-collection requires --job and --task-id')
        print(json.dumps(check_failed_collection(args.job, args.task_id)))
    else:
        if args.job is None or not args.task_id or args.expect_reward is None:
            parser.error('check-job requires --job, --task-id and --expect-reward')
        print(json.dumps(check_job(args.job, args.task_id, args.expect_reward, args.expect_rejection)))


if __name__ == '__main__':
    main()
