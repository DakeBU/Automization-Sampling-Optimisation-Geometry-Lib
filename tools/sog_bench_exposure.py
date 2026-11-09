"""Public exposure snapshots and offline private holdout integrity checks."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


PUBLIC_FILE = 'public-exposure.json'
PUBLIC_DRAFT_FILE = 'published-draft-exposure.json'
PUBLIC_DRAFT_SOURCE_FILE = 'published-draft-exposure-sources.json'
PUBLIC_DRAFTS = (Path(__file__).resolve().parents[1] /
                 'benchmarks/samplingoptimisationgeometrybench' / PUBLIC_DRAFT_FILE)
PUBLIC_DRAFT_SOURCES = PUBLIC_DRAFTS.with_name(PUBLIC_DRAFT_SOURCE_FILE)
PUBLIC_KIND = 'sog-bench-public-exposure'
PRIVATE_KIND = 'sog-bench-private-inventory'
PROMPT_KIND = 'sog-bench-private-prompts'
REFERENCE_KIND = 'sog-bench-private-references'
REVIEW_KIND = 'sog-bench-private-review'
SOURCE_SCOPE = 'project-owned-original-only'
TRACKS = frozenset({'natural-language', 'lean', 'graph-json'})
GRAPH_FIELDS = frozenset({'question', 'context', 'targets', 'remove',
                          'required_statement_constants', 'answer_schema'})
LEAN_PROMPT_PREFIX = ('Complete the fixed Lean target below. Keep its imports, context and proposition unchanged. '
                      'Use the repository-pinned Lean/Mathlib. This is open-library reconstruction; '
                      'the target module is not imported directly.\n\n')
PROMPT_COMMON = frozenset({'id', 'family', 'library_domains', 'skills', 'title',
                           'split', 'binding_sha256', 'track', 'level'})
MAX_METADATA_BYTES = 2 * 1024 * 1024
LABEL = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*')
SHA = re.compile(r'[a-f0-9]{64}')
ANCHOR = re.compile(r'(?:(?:exercise|original):[a-z0-9]+(?:-[a-z0-9]+)*|'
                    r'lean:AutoSamplingTheory(?:\.[\w]+)+)')
REVIEW_CHECKS = frozenset({'source-and-rights', 'family-independence',
                           'solution-and-rubric', 'tool-and-graph-scope'})


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
    return public_bytes(list(records.values()))


def public_bytes(records: list[dict]) -> bytes:
    check_rows(records)
    return encoded({'schema_version': 1, 'kind': PUBLIC_KIND,
                    'records': sorted(records, key=lambda row: row['id'])})


def build_published_drafts(prompts: list[dict], anchors: dict[str, list[str]]) -> bytes:
    """Fingerprints only, from selected public prompt exports and audited primary anchors.

    This does not discover exposures or prove that the inputs were public.
    Record exact public commits and the prompt-export digests separately.
    """
    records = {}
    for prompt in prompts:
        if (not isinstance(prompt, dict) or not PROMPT_COMMON <= prompt.keys()
                or prompt['split'] != 'public-dev'
                or not matches(prompt['id'], LABEL, 120)
                or not matches(prompt['family'], LABEL, 160)
                or not matches(prompt['binding_sha256'], SHA, 64)
                or not isinstance(prompt['track'], str) or prompt['track'] not in TRACKS):
            raise ValueError('Expected a bound public prompt-only row')
        identity, family, track = (prompt[k] for k in ('id', 'family', 'track'))
        if identity not in anchors:
            raise ValueError('Each published draft needs an audited primary source anchor')
        if track == 'graph-json':
            if not set(prompt) <= PROMPT_COMMON | GRAPH_FIELDS | {'core_id', 'graph_sha256'}:
                raise ValueError('Graph draft input is not prompt-only')
            payload = {k: prompt[k] for k in GRAPH_FIELDS if k in prompt}
        else:
            if (not {'assumptions', 'question'} <= prompt.keys()
                    or not set(prompt) <= PROMPT_COMMON | {'domain', 'assumptions', 'question', 'exercise_source'}):
                raise ValueError('Mathematical draft input is not prompt-only')
            payload = {k: prompt[k] for k in ('assumptions', 'question')}
            if track == 'lean':
                text = payload['question']
                if (not isinstance(text, str) or not text.startswith(LEAN_PROMPT_PREFIX)
                        or not text.endswith(' := by\n  -- Replace this comment with your proof.\n')):
                    raise ValueError('Lean draft input is not the canonical fixed proof slot')
                payload = text.removeprefix(LEAN_PROMPT_PREFIX)
        row = records.setdefault(identity, {'id': identity, 'family': family,
                                  'anchors': anchors[identity], 'views': {}})
        if row['family'] != family or track in row['views']:
            raise ValueError('A published draft cannot repeat a track or split its family')
        row['views'][track] = prompt_sha256(track, payload)
    if records.keys() != anchors.keys():
        raise ValueError('Draft prompt rows and audited anchor identities must match exactly')
    return public_bytes(list(records.values()))


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


def public_records(raw: bytes) -> list[dict]:
    snapshot = strict_json(raw)
    if set(snapshot) != {'schema_version', 'kind', 'records'} or snapshot['kind'] != PUBLIC_KIND:
        raise ValueError('Expected a public exposure snapshot')
    check_rows(snapshot['records'])
    return snapshot['records']


def draft_sources(raw: bytes) -> dict:
    source = strict_json(raw)
    if (set(source) != {'schema_version', 'snapshot_sha256', 'inputs'}
            or not matches(source['snapshot_sha256'], SHA, 64)
            or not isinstance(source['inputs'], dict) or not source['inputs']):
        raise ValueError('Invalid published draft exposure provenance')
    identities = set()
    for label, item in source['inputs'].items():
        if (not matches(label, LABEL, 80) or not isinstance(item, dict)
                or set(item) != {'ref', 'commit', 'format', 'sha256', 'anchors'}
                or not matches(item['ref'], re.compile(r'refs/heads/codex/[a-z0-9-]+'), 180)
                or not matches(item['commit'], re.compile(r'[a-f0-9]{40}'), 40)
                or item['format'] not in ('json', 'jsonl')
                or not matches(item['sha256'], SHA, 64)
                or not isinstance(item['anchors'], dict) or not item['anchors']
                or identities.intersection(item['anchors'])):
            raise ValueError('Invalid or duplicated published draft source')
        for identity, anchors in item['anchors'].items():
            if (not matches(identity, LABEL, 120) or not isinstance(anchors, list) or not anchors
                    or not all(matches(a, ANCHOR, 360) for a in anchors) or len(anchors) != len(set(anchors))):
                raise ValueError('A published source needs distinct, eligible typed anchors')
        identities.update(item['anchors'])
    return source


def known_published_drafts() -> tuple[bytes, bytes]:
    raw, provenance = read_metadata(PUBLIC_DRAFTS), read_metadata(PUBLIC_DRAFT_SOURCES)
    source = draft_sources(provenance)
    anchors = {identity: names for item in source['inputs'].values()
               for identity, names in item['anchors'].items()}
    if digest(raw) != source['snapshot_sha256'] or {
            row['id']: row['anchors'] for row in public_records(raw)} != anchors:
        raise ValueError('Published draft fingerprints no longer match their recorded provenance')
    return raw, provenance


def replay_published_drafts(files: dict[str, Path], snapshot: bytes, provenance: bytes) -> None:
    source = draft_sources(provenance)
    if files.keys() != source['inputs'].keys():
        raise ValueError('Supply each exact recorded public prompt export once')
    anchors, prompts = {}, []
    for label, item in source['inputs'].items():
        raw = read_metadata(files[label])
        if digest(raw) != item['sha256']:
            raise ValueError('Public prompt export digest changed: ' + label)
        rows = ([json.loads(line) for line in raw.splitlines() if line.strip()]
                if item['format'] == 'jsonl' else [json.loads(raw)])
        if not all(isinstance(row, dict) and isinstance(row.get('id'), str) for row in rows):
            raise ValueError('Expected exported public prompt rows')
        anchors.update(item['anchors'])
        prompts.extend(r for r in rows if r['id'] in item['anchors'])
    if digest(snapshot) != source['snapshot_sha256'] or build_published_drafts(prompts, anchors) != snapshot:
        raise ValueError('Replayed published draft fingerprints do not match the snapshot')


def audit_private(current: bytes, historical: list[bytes], private: bytes) -> dict:
    """Check only declared exact overlaps; does not certify novelty, rights or admission."""
    public = {'id': set(), 'family': set(), 'anchor': set(), 'prompt': set()}
    snapshots = set()
    for raw in (current, *historical):
        records = public_records(raw)
        sha = digest(raw)
        if sha in snapshots:
            raise ValueError('Duplicate public exposure snapshot')
        snapshots.add(sha)
        for row in records:
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


def bundle_views(raw: bytes, kind: str, expected: dict) -> dict:
    pack = strict_json(raw)
    if (set(pack) != {'schema_version', 'kind', 'records'} or pack['kind'] != kind
            or not isinstance(pack['records'], list)):
        raise ValueError('Invalid private task pack')
    indexed = {}
    for row in pack['records']:
        if (not isinstance(row, dict) or set(row) != {'id', 'views'}
                or not matches(row['id'], LABEL, 120) or row['id'] not in expected
                or row['id'] in indexed or not isinstance(row['views'], dict)
                or row['views'].keys() != expected[row['id']].keys()):
            raise ValueError('Private task pack differs from the inventory IDs or tracks')
        indexed[row['id']] = row['views']
    if indexed.keys() != expected.keys():
        raise ValueError('Private task pack does not cover the inventory')
    return indexed


def audit_private_seal(current: bytes, historical: list[bytes], private: bytes,
                       prompts: bytes, references: bytes, review: bytes,
                       expected_review_sha256: str) -> dict:
    """Check externally pinned receipt bytes; no identity, proof or score assertion."""
    result = audit_private(current, historical, private)
    if not matches(expected_review_sha256, SHA, 64) or digest(review) != expected_review_sha256:
        raise ValueError('Private review does not match the separately pinned SHA-256')
    receipt = strict_json(review)
    if (set(receipt) != {'schema_version', 'kind', 'inventory_sha256', 'prompts_sha256',
                         'references_sha256', 'author', 'reviewer', 'families'}
            or receipt['kind'] != REVIEW_KIND or receipt['inventory_sha256'] != digest(private)
            or receipt['prompts_sha256'] != digest(prompts)
            or receipt['references_sha256'] != digest(references)
            or not matches(receipt['author'], LABEL, 120)
            or not matches(receipt['reviewer'], LABEL, 120)
            or receipt['author'] == receipt['reviewer'] or not isinstance(receipt['families'], list)):
        raise ValueError('Private review does not bind these files and separate author/reviewer labels')

    rows = strict_json(private)['records']
    expected_families = {row['family'] for row in rows}
    reviewed = set()
    for family in receipt['families']:
        if (not isinstance(family, dict) or set(family) != {'id', 'decision', 'checks'}
                or not matches(family['id'], LABEL, 160) or family['id'] not in expected_families
                or family['id'] in reviewed or family['decision'] != 'accept'
                or not isinstance(family['checks'], list)
                or not all(isinstance(c, str) for c in family['checks'])
                or len(family['checks']) != len(REVIEW_CHECKS)
                or set(family['checks']) != REVIEW_CHECKS):
            raise ValueError('Private review has a rejected, duplicate or incomplete family record')
        reviewed.add(family['id'])
    if reviewed != expected_families:
        raise ValueError('Private review does not cover every held-out family')

    expected = {r['id']: r['views'] for r in rows}
    prompt_index = bundle_views(prompts, PROMPT_KIND, expected)
    reference_index = bundle_views(references, REFERENCE_KIND, expected)
    for identity, views in expected.items():
        for track, sha in views.items():
            if prompt_sha256(track, prompt_index[identity][track]) != sha:
                raise ValueError('Private prompt does not match the screened inventory')
            ref = reference_index[identity][track]
            if (not isinstance(ref, dict) or set(ref) != {'solution', 'rubric'}
                    or not all(isinstance(v, str) and v.strip() for v in ref.values())):
                raise ValueError('Private reference needs a nonempty solution and rubric for each track')
    return {**result, 'status': 'matches-pinned-private-review', 'receipt_identity_authenticated': False,
            'review_bound_families': len(reviewed), 'private_views': sum(map(len, expected.values()))}


def read_metadata(path: Path, *, outside: Path | None = None) -> bytes:
    try:
        target = path.resolve(strict=True)
        if outside is not None and target.is_relative_to(outside.resolve()):
            raise ValueError('Keep the private input file outside the repository')
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
    parser.add_argument('--inventory', type=Path,
                        help='External private-test inventory metadata, not prompts or answers')
    parser.add_argument('--historical-public', type=Path, action='append', default=[],
                        help='Other retained public snapshots; the shipped published-draft snapshot is included automatically')
    parser.add_argument('--prompts', type=Path, help='External prompt-only pack (offline only)')
    parser.add_argument('--references', type=Path, help='External grader-only reference pack (offline only)')
    parser.add_argument('--review', type=Path, help='External reviewer receipt for these exact files')
    parser.add_argument('--expected-review-sha256', help='SHA-256 received from a trusted reviewer channel')
    parser.add_argument('--replay-published-drafts', nargs=2, metavar=('LABEL', 'PUBLIC_PROMPT_EXPORT'),
                        action='append', help='Recompute shipped fingerprints from exact public prompt inputs')
    args = parser.parse_args()
    options = (args.prompts, args.references, args.review, args.expected_review_sha256)
    if args.replay_published_drafts:
        if args.inventory or args.historical_public or any(x is not None for x in options):
            parser.error('Public replay does not accept any private input or other historical snapshots')
        files = {label: Path(path) for label, path in args.replay_published_drafts}
        if len(files) != len(args.replay_published_drafts):
            parser.error('Do not repeat a public input label')
        try:
            snapshot, source = known_published_drafts()
            replay_published_drafts(files, snapshot, source)
        except ValueError as exc:
            parser.exit(1, f'Published draft replay refused: {exc}\n')
        print(json.dumps({'status': 'published-draft-exposure-replayed',
                          'records': len(public_records(snapshot)), 'snapshot_sha256': digest(snapshot)}))
        return 0
    if not args.inventory:
        parser.error('Provide an external --inventory for offline private checks')
    if any(x is not None for x in options) and any(x is None for x in options):
        parser.error('Provide --prompts, --references, --review and --expected-review-sha256 together')
    import sog_bench as bench
    try:
        private = read_metadata(args.inventory, outside=bench.ROOT)
        historical = [known_published_drafts()[0], *(read_metadata(path) for path in args.historical_public)]
        current = build_public(bench.materialize(), bench.curriculum.graph_items())
        if args.prompts is None:
            result = audit_private(current, historical, private)
        else:
            prompts, references, review = (read_metadata(p, outside=bench.ROOT) for p in options[:3])
            result = audit_private_seal(current, historical, private, prompts, references,
                                        review, args.expected_review_sha256)
    except ValueError as exc:
        parser.exit(1, f'Exposure preflight refused: {exc}\n')
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
