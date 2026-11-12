"""One explicit index for versioned Bench compiler slices and their replay."""
from __future__ import annotations

import argparse
from collections import deque
import json
from pathlib import Path
import re

DIRECTORY = Path(__file__).resolve().parents[1] / 'benchmarks/samplingoptimisationgeometrybench'
INDEX = 'compiled_graph_slices.json'
LEGACY_LABELS = ('transport', 'flow')
LABEL = re.compile(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*')


def labels(index: dict) -> tuple[str, ...]:
    if (type(index) is not dict or set(index) != {'schema_version', 'slices'}
            or type(index['schema_version']) is not int or index['schema_version'] != 1
            or type(index['slices']) is not list or not 0 < len(index['slices']) <= 16
            or any(type(s) is not str or len(s) > 40 or not LABEL.fullmatch(s)
                   for s in index['slices']) or len(set(index['slices'])) != len(index['slices'])):
        raise ValueError('Invalid explicit compiled graph slice index')
    return tuple(index['slices'])


def spec_name(label: str) -> str:
    if not LABEL.fullmatch(label):
        raise ValueError('Invalid compiled graph slice label')
    return ('compiled_graph_tasks.json' if label == 'transport'
            else 'compiled_' + label.replace('-', '_') + '_graph_tasks.json')


def configured(directory: Path = DIRECTORY) -> list[tuple[str, Path, Path]]:
    index = directory / INDEX
    if index.is_symlink():
        raise ValueError('Compiled graph slice index must be a repository file')
    specs = []
    for label in labels(json.loads(index.read_text(encoding='utf-8'))):
        spec, snapshot = directory / spec_name(label), directory / f'compiled-{label}-graph.json'
        if not spec.is_file() or not snapshot.is_file() or spec.is_symlink() or snapshot.is_symlink():
            raise ValueError('Registered compiler slice needs a regular selection and snapshot')
        specs.append((label, spec, snapshot))
    return specs


def items() -> list[dict]:
    import sog_bench_compiled_graph as compiler
    return [item for _, spec, snapshot in configured() for item in compiler.items(spec, snapshot)]


def snapshots() -> dict[str, dict]:
    import sog_bench_compiled_graph as compiler
    return {snapshot.name: compiler.recorded(spec, snapshot)[2] for _, spec, snapshot in configured()}


def artifact_for(task_id: str) -> str:
    # Use membership, not a special case on the anchor core: one core can
    # have multiple structural questions with different selected slices.
    matches = [snapshot.name for _, spec, snapshot in configured()
               if any(row['id'] == task_id for row in json.loads(spec.read_text(encoding='utf-8'))['tasks'])]
    if len(matches) != 1:
        raise ValueError('Each compiled graph task must resolve to exactly one registered snapshot')
    return matches[0]


def reference_paths(item: dict) -> tuple[list[list[str]], list[str]]:
    """Explain positive selected paths without altering prompts or scoring."""
    adjacency = {n: set() for n in item['context']['nodes']}
    for source, target in item['context']['edges']:
        adjacency[source].add(target)
    shared = sorted(set.intersection(*(adjacency[n] for n in item['targets'])))
    paths = []
    for start in item['answer']['nodes']:
        queue, seen = deque([[start]]), {start}
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node == item['remove']:
                paths.append(path)
                break
            for child in sorted(adjacency[node] - seen):
                queue.append([*path, child])
                seen.add(child)
        else:
            raise ValueError('Positive structural answer has no path in its selected slice')
    return paths, shared


def main() -> int:
    import sog_bench_compiled_graph as compiler
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('check',))
    args = parser.parse_args()
    for label, spec, snapshot in configured():
        if compiler.replay(spec) != compiler.recorded(spec, snapshot)[2]:
            raise ValueError(label + ': graph differs from fresh compiled replay')
        print(label + ': fresh compiler replay matches; not a full closure or necessity certificate.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
