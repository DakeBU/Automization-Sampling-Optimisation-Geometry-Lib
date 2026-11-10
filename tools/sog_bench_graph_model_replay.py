"""Offline verification of an archived paired graph-model trajectory."""
from __future__ import annotations

import argparse
from datetime import datetime
import io
from pathlib import Path
import stat
import tempfile

import sog_bench_graph_model as model

bench = model.bench
graph = model.graph


def plain(path: Path, *, directory: bool) -> None:
    try:
        info = path.lstat()
    except FileNotFoundError as exc:
        raise ValueError(f'Missing archived {path.name}; bounded raw evidence is required') from exc
    kind = stat.S_ISDIR if directory else stat.S_ISREG
    if not kind(info.st_mode) or getattr(info, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
        raise ValueError(f'Archive entry is not a plain {"directory" if directory else "file"}: {path.name}')


def directory_members(path: Path, expected: set[str]) -> None:
    plain(path, directory=True)
    remaining = set(expected)
    for child in path.iterdir():
        if child.name not in remaining:
            raise ValueError(f'Unexpected archive entry: {child.name}')
        remaining.remove(child.name)
    if remaining:
        raise ValueError('Archive is missing expected entries: ' + ', '.join(sorted(remaining)))


class Archive:
    """Read only exact caller-constructed paths, never manifest-provided paths."""
    def __init__(self, root: Path):
        self.root = root
        self.hashes: dict[str, str] = {}

    def raw(self, path: Path, *, record=True) -> bytes:
        plain(path, directory=False)
        with path.open('rb') as stream:
            raw = stream.read(model.WIRE_BYTES + 1)
        if len(raw) > model.WIRE_BYTES:
            raise ValueError(f'Archive entry exceeds byte cap: {path.name}')
        if record:
            self.hashes[path.relative_to(self.root).as_posix()] = bench.sha(raw)
        return raw

    def equal(self, path: Path, expected: bytes) -> None:
        if self.raw(path) != expected:
            raise ValueError(f'Archived {path.name} differs from exact replay')


class RecordedTransport:
    """Feed one archived response only after the regenerated request matches."""
    def __init__(self, archive: Archive, profile: Path):
        self.archive, self.profile = archive, profile
        self.steps: set[str] = set()

    def __call__(self, request: bytes) -> tuple[bytes, dict]:
        name = f'{len(self.steps) + 1:04d}'
        step = self.profile / name
        directory_members(step, {'request.json', 'response.json', 'transport.json'})
        self.archive.equal(step / 'request.json', request)
        response = self.archive.raw(step / 'response.json')
        transport_raw = self.archive.raw(step / 'transport.json')
        transport = model.decode(transport_raw)
        if (not isinstance(transport, dict) or set(transport) - {'http_status', 'request_id', 'response_date'}
                or type(transport.get('http_status')) is not int
                or any(not isinstance(transport.get(k), (str, type(None))) for k in ('request_id', 'response_date'))
                or bench.encoded(transport) != transport_raw):
            raise ValueError('Invalid archived transport receipt')
        self.steps.add(name)
        return response, transport


class ReplayMismatch(Exception):
    """Replay errors must not be swallowed as provider-protocol failures."""


def check_selection(raw: bytes, item: dict) -> tuple[dict, list]:
    choice = model.decode(raw)
    if not isinstance(choice, dict):
        raise ValueError('Comparison selection must be a JSON object')
    model_name, expected = choice.get('model'), choice.get('expected_returned_model')
    tokens, max_lookups = choice.get('max_output_tokens_per_call'), choice.get('max_lookups')
    timestamp, transport = choice.get('created_at'), choice.get('provider_transport')
    if (any(not isinstance(s, str) or not s.strip() for s in (model_name, expected, timestamp, transport))
            or type(tokens) is not int or not 128 <= tokens <= 32768
            or datetime.fromisoformat(timestamp).tzinfo is None):
        raise ValueError('Invalid archived comparison selection')
    binding = graph.session_binding(item, max_lookups)
    del binding['profile'], binding['prompt_sha256']
    order = [(name, *model.condition(item, name, max_lookups)) for name in model.PROFILES]
    exact = {**binding, 'kind': 'graph-responses-comparison', 'created_at': timestamp,
             'model': model_name, 'expected_returned_model': expected, 'max_output_tokens_per_call': tokens,
             'provider_transport': transport,
             'endpoint': model.ENDPOINT if transport == model.OpenAIResponses.kind else None,
             'profiles': [{'profile': name, 'prompt_sha256': bench.sha(graph.line(prompt)),
                           'max_api_calls': 1 if name == model.PROFILES[0] else max_lookups + 1}
                          for name, prompt, _ in order],
             'model_bridge_sha256_lf': bench.text_hash(Path(model.__file__)),
             'automatic_retries': 0, 'model_measurement': False}
    if bench.encoded(exact) != raw:
        raise ValueError('Task, profile, policy or executable binding drift')
    return exact, order


def replay(directory: Path, item: dict) -> dict:
    directory_members(directory, {'selection.json', 'operator-task.json', 'comparison.json', *model.PROFILES})
    archive = Archive(directory)
    selection, order = check_selection(archive.raw(directory / 'selection.json'), item)
    archive.equal(directory / 'operator-task.json', bench.encoded(item))
    results, abort = [], False
    for name, prompt, tools in order:
        root = directory / name
        plain(root, directory=True)
        archive.equal(root / 'prompt.json', graph.line(prompt))
        members = {'prompt.json', 'result.json'}
        if abort:
            result = {'profile': name, 'score': None, 'selected_denominator': 1,
                      'termination': 'not-run-after-infrastructure-error', 'api_turns': 0}
        else:
            transport = RecordedTransport(archive, root)
            def offline(request):
                try:
                    return transport(request)
                except (ValueError, OSError, RecursionError) as error:
                    raise ReplayMismatch(str(error)) from error
            events = io.BytesIO()
            # Only the normal request builder uses this temporary directory.
            # The original archive is never written, and no network client exists.
            with tempfile.TemporaryDirectory(prefix='sog-graph-replay-') as temporary:
                adapter = model.ResponsesInput(Path(temporary), offline, prompt, tools, selection['model'],
                                               selection['expected_returned_model'], selection['max_output_tokens_per_call'])
                limit = 0 if name == model.PROFILES[0] else selection['max_lookups']
                try:
                    result = graph.run_trial(item, limit, adapter, adapter.emit, lambda event: events.write(graph.line(event)))
                except ReplayMismatch as error:
                    raise ValueError(str(error)) from error
            if adapter.turns != len(transport.steps):
                raise ValueError('Missing bounded raw round trip; cannot replay the archived outcome')
            archive.equal(root / 'actions.jsonl', events.getvalue())
            members.update({'actions.jsonl', *transport.steps})
            result.update(profile=name, api_turns=adapter.turns, selected_denominator=1)
            if adapter.infrastructure:
                result.update(score=None, termination=adapter.infrastructure)
                abort = True
            elif adapter.stop:
                result['termination'] = adapter.stop
        directory_members(root, members)
        archive.equal(root / 'result.json', bench.encoded(result))
        results.append(result)
    report = {'schema_version': 1, 'kind': 'recorded-graph-interface-comparison', 'id': item['id'],
              'family': item['family'], 'split': 'public-dev', 'results': results,
              'model_measurement': False, 'provenance_authenticated': False, 'files_sha256': archive.hashes}
    if archive.raw(directory / 'comparison.json', record=False) != bench.encoded(report):
        raise ValueError('Archived comparison or file manifest differs from exact replay')
    return {'schema_version': 1, 'kind': 'offline-graph-comparison-replay',
            'id': item['id'], 'comparison_sha256': bench.sha(bench.encoded(report)),
            'profiles': [r['profile'] for r in results], 'results': results,
            'model_measurement': False, 'provenance_authenticated': False, 'network_calls': 0}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True, type=Path)
    parser.add_argument('--task-id', required=True)
    args = parser.parse_args()
    print(bench.encoded(replay(args.run, graph.admitted(args.task_id))).decode('utf-8'), end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
