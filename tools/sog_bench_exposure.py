"""Public exposure snapshots and an offline, metadata-only private preflight."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


PUBLIC_FILE = 'public-exposure.json'
PUBLIC_KIND = 'sog-bench-public-exposure'
PRIVATE_KIND = 'sog-bench-private-inventory'
SOURCE_SCOPE = 'project-owned-original-only'
TRACKS = frozenset({'natural-language', 'lean', 'graph-json'})
GRAPH_FIELDS = frozenset({'question', 'context', 'targets', 'remove',
                          'required_statement_constants', 'answer_schema'})
MAX_METADATA_BYTES = 2 * 1024 * 1024
LABEL = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')
SHA = re.compile(r'[a-f0-9]{64}')
ANCHOR = re.compile(r'(?:(?:exercise|original):[a-z0-9]+(?:-[a-z0-9]+)*|'
                    r'lean:AutoSamplingTheory(?:\.[\w]+)+)')


def encoded(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def prompt_sha256(track: str, payload) -> str:
    """Hash canonical task material, excluding ID, family, title, level and answer."""
    if track == 'natural-language':
        if (not isinstance(payload, dict) or set(payload) != {'assumptions', 'question'}
                or not isinstance(payload['assumptions'], list)
                or not all(isinstance(s, str) for s in payload['assumptions'])
                or not isinstance(payload['question'], str)):
            raise ValueError('Expected natural-language assumptions and question')
    elif track == 'lean':
        if not isinstance(payload, str):
            raise ValueError('Expected the fixed Lean template text')
    elif track == 'graph-json':
        if (not isinstance(payload, dict) or not {'question', 'context', 'targets'} <= set(payload)
                or not set(payload) <= GRAPH_FIELDS):
            raise ValueError('Expected only the structural graph prompt fields')
    else:
        raise ValueError('Unknown exposure track')
    return digest(encoded({'track': track, 'payload': payload}))


def build_public(cores: list[dict], graphs: list[dict]) -> bytes:
    """Include all public catalog entries, not only admitted/exported training rows."""
    records = {}
    for core in cores:
        if core['split'] != 'public-dev' or core['id'] in records:
            raise ValueError('Expected distinct public-dev cores')
        anchors = ['lean:' + core['declaration']]
        if core.get('textbook_exercise_id'):
            anchors.append('exercise:' + core['textbook_exercise_id'])
        views = {'natural-language': prompt_sha256('natural-language',
                 {k: core[k] for k in ('assumptions', 'question')})}
        if core['lean_task']:
            views['lean'] = prompt_sha256('lean', core['lean_task'])
        records[core['id']] = {'id': core['id'], 'family': core['family'],
                               'anchors': sorted(anchors), 'views': views}
    for graph in graphs:
        core = records.get(graph['core_id'])
        if (graph['split'] != 'public-dev' or graph['id'] in records or not core
                or graph['family'] != core['family']):
            raise ValueError('Expected a distinct public graph view in its source family')
        records[graph['id']] = {'id': graph['id'], 'family': graph['family'],
            'anchors': core['anchors'], 'views': {'graph-json': prompt_sha256('graph-json',
                {k: graph[k] for k in GRAPH_FIELDS if k in graph})}}
    rows = [records[identity] for identity in sorted(records)]
    check_rows(rows)
    return encoded({'schema_version': 1, 'kind': PUBLIC_KIND, 'records': rows})


def matches(value, pattern: re.Pattern, limit: int) -> bool:
    return isinstance(value, str) and len(value) <= limit and pattern.fullmatch(value) is not None


def check_rows(rows) -> None:
    if not isinstance(rows, list) or not rows:
        raise ValueError('Inventory needs nonempty metadata records')
    seen = set()
    for row in rows:
        if (not isinstance(row, dict) or set(row) != {'id', 'family', 'anchors', 'views'}
                or not matches(row['id'], LABEL, 120) or row['id'] in seen
                or not matches(row['family'], LABEL, 160)
                or not isinstance(row['anchors'], list) or not row['anchors']
                or not all(matches(a, ANCHOR, 360) for a in row['anchors'])
                or len(set(row['anchors'])) != len(row['anchors'])
                or not isinstance(row['views'], dict) or not row['views']
                or not set(row['views']) <= TRACKS
                or not all(matches(v, SHA, 64) for v in row['views'].values())):
            raise ValueError('Invalid inventory row; only IDs, families, typed anchors and prompt hashes are allowed')
        seen.add(row['id'])


def strict_json(raw: bytes) -> dict:
    def pairs(items):
        if len({k for k, _ in items}) != len(items):
            raise ValueError('Duplicate metadata key')
        return dict(items)

    if len(raw) > MAX_METADATA_BYTES:
        raise ValueError('Exposure metadata exceeds the byte limit')
    try:
        obj = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs)
    except (UnicodeError, ValueError, RecursionError):
        raise ValueError('Invalid strict UTF-8 exposure metadata') from None
    if not isinstance(obj, dict) or type(obj.get('schema_version')) is not int or obj['schema_version'] != 1:
        raise ValueError('Unsupported exposure schema')
    return obj


def audit_private(current: bytes, historical: list[bytes], private: bytes) -> dict:
    """Check only declared exact overlaps; does not certify novelty, rights or admission."""
    public = {'id': set(), 'family': set(), 'anchor': set(), 'prompt': set()}
    snapshots = set()
    for raw in (current, *historical):
        snapshot = strict_json(raw)
        if set(snapshot) != {'schema_version', 'kind', 'records'} or snapshot['kind'] != PUBLIC_KIND:
            raise ValueError('Expected a public exposure snapshot')
        sha = digest(raw)
        if sha in snapshots:
            raise ValueError('Duplicate public exposure snapshot')
        snapshots.add(sha)
        check_rows(snapshot['records'])
        for row in snapshot['records']:
            for key in ('id', 'family'):
                public[key].add(row[key])
            public['anchor'].update(row['anchors'])
            public['prompt'].update(row['views'].items())
    inventory = strict_json(private)
    if (set(inventory) != {'schema_version', 'kind', 'split', 'source_scope', 'public_snapshots', 'records'}
            or inventory['kind'] != PRIVATE_KIND or inventory['split'] != 'private-test'
            or inventory['source_scope'] != SOURCE_SCOPE):
        raise ValueError('Expected metadata for a project-original private-test inventory')
    claimed = inventory['public_snapshots']
    if (not isinstance(claimed, list) or not all(matches(s, SHA, 64) for s in claimed)
            or sorted(claimed) != sorted(snapshots)):
        raise ValueError('Inventory is not bound to exactly the current and supplied historical public snapshots')
    rows = inventory['records']
    check_rows(rows)
    seen_anchors, seen_prompts = {}, set()
    collisions = dict.fromkeys(public, 0)
    for row in rows:
        for key in ('id', 'family'):
            collisions[key] += row[key] in public[key]
        for anchor in row['anchors']:
            collisions['anchor'] += anchor in public['anchor']
            if seen_anchors.setdefault(anchor, row['family']) != row['family']:
                raise ValueError('A declared private source anchor is split across families')
        for view in row['views'].items():
            collisions['prompt'] += view in public['prompt']
            if view in seen_prompts:
                raise ValueError('Duplicate exact prompt view in private inventory')
            seen_prompts.add(view)
    if any(collisions.values()):
        raise ValueError('Public exposure overlaps: ' + ', '.join(f'{k}={n}' for k, n in collisions.items() if n))
    return {'status': 'no-exact-overlap', 'public_snapshot_count': len(snapshots),
            'current_public_snapshot_sha256': digest(current), 'private_records': len(rows),
            'private_families': len({r['family'] for r in rows}),
            'semantic_independence_verified': False, 'admitted': False, 'model_measurement': False}


def read_metadata(path: Path, *, outside: Path | None = None) -> bytes:
    try:
        target = path.resolve(strict=True)
        if outside is not None and target.is_relative_to(outside.resolve()):
            raise ValueError('Keep the private metadata file outside the repository')
        if not target.is_file():
            raise ValueError('Metadata input must be a regular file')
        with target.open('rb') as f:
            raw = f.read(MAX_METADATA_BYTES + 1)
    except (OSError, RuntimeError):
        raise ValueError('Cannot read exposure metadata file') from None
    if len(raw) > MAX_METADATA_BYTES:
        raise ValueError('Exposure metadata exceeds the byte limit')
    return raw


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, required=True,
                        help='External private-test inventory metadata, not prompts or answers')
    parser.add_argument('--historical-public', type=Path, action='append', default=[],
                        help='A retained public exposure snapshot, repeat for each distinct release')
    args = parser.parse_args()
    import sog_bench as bench
    try:
        private = read_metadata(args.inventory, outside=bench.ROOT)
        historical = [read_metadata(path) for path in args.historical_public]
        current = build_public(bench.materialize(), bench.curriculum.graph_items())
        result = audit_private(current, historical, private)
    except ValueError as exc:
        parser.exit(1, f'Exposure preflight refused: {exc}\n')
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
