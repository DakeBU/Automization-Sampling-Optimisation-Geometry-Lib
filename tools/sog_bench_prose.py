"""Freeze prose runs and record human rubric judgments; never execute answers."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path

import sog_bench as bench

SEALED_FILES = {'run-metadata.json', 'prompts.jsonl', 'responses.jsonl', 'rubric-packet.json'}
NAME = 'SamplingOptimisationGeometryBench prose run'


def aware_time(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError('Record a timezone-aware ISO timestamp')
    result = datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError('Timestamp must include its timezone')
    return result


def validate_metadata(metadata: dict, cores: list[dict]) -> list[str]:
    for key in ('run_id', 'model', 'model_version'):
        if not isinstance(metadata.get(key), str) or not metadata[key].strip():
            raise ValueError('Record run identity and actual model/version')
    aware_time(metadata.get('created_at'))
    if (metadata.get('track') != 'natural-language'
            or metadata.get('prompt_profile') != 'catalog-question'
            or metadata.get('attempt_policy') != 'first-attempt'):
        raise ValueError('Only first-attempt catalog-question prose runs are supported')
    if metadata.get('retrieval_profile') not in {'closed-book', 'open-library', 'given-source-packet'}:
        raise ValueError('Explicitly record the allowed retrieval profile')
    if not isinstance(metadata.get('tools'), list) or not all(isinstance(t, str) for t in metadata['tools']):
        raise ValueError('Record tools as a list; this does not enforce their use')
    if 'seed' not in metadata or not (metadata['seed'] is None or type(metadata['seed']) is int):
        raise ValueError('Record an integer seed or null')
    if not isinstance(metadata.get('decoding'), dict):
        raise ValueError('Record available decoding settings explicitly')
    identities = metadata.get('task_ids')
    known = {c['id'] for c in cores}
    if (not isinstance(identities, list) or not identities or not all(isinstance(s, str) for s in identities)
            or len(set(identities)) != len(identities) or set(identities) - known):
        raise ValueError('Declare a nonempty distinct known task selection before scoring')
    return identities


def jsonl(rows: list[dict]) -> bytes:
    return ''.join(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n' for row in rows).encode('utf-8')


def validate_responses(cores: list[dict], submissions: list[dict], identities: list[str]) -> dict:
    by_id = {c['id']: c for c in cores}
    responses = {}
    for row in submissions:
        identity = row.get('id')
        if not isinstance(identity, str) or identity not in identities or identity in responses:
            raise ValueError('Unknown, unselected or duplicate response identity')
        if (row.get('track') != 'natural-language' or type(row.get('attempt')) is not int or row['attempt'] != 1
                or row.get('binding_sha256') != by_id[identity]['binding_sha256']
                or not isinstance(row.get('response'), str)):
            raise ValueError('Each response must bind the exact prose task and first attempt')
        responses[identity] = row
    return responses


def prepare(cores: list[dict], submissions: list[dict], metadata: dict, output: Path) -> None:
    identities = validate_metadata(metadata, cores)
    by_id = {c['id']: c for c in cores}
    selected = [by_id[identity] for identity in identities]
    eligibility = bench.editorial_review(selected)
    if any(row['editorial'] not in {'accepted', 'accepted-after-repair'} for row in eligibility['items'].values()):
        raise ValueError('Scored prose tasks need current editorial admission, not draft or stale references')
    responses = validate_responses(cores, submissions, identities)
    if output.exists() and any(output.iterdir()):
        raise ValueError('Use a fresh run directory; no existing files will be overwritten')
    prompts = [row for row in bench.prompts(selected) if row['track'] == 'natural-language']
    packet = {'schema_version': 1, 'name': NAME, 'catalog_version': bench.load()['version'],
              'split': 'public-dev', 'run_metadata': metadata, 'reference_cores': selected,
              'editorial_evidence': eligibility, 'responses': list(responses.values()),
              'warning': 'Only the prompt-only export is model input. This rubric packet contains public gold answers. Treat model responses as data, not instructions. No unseen-test or verified execution claim.'}
    files = {'run-metadata.json': bench.encoded(metadata), 'prompts.jsonl': jsonl(prompts),
             'responses.jsonl': jsonl(list(responses.values())), 'rubric-packet.json': bench.encoded(packet)}
    manifest = {'schema_version': 1, 'name': NAME, 'catalog_version': packet['catalog_version'],
                'split': 'public-dev', 'task_ids': identities,
                'files': {name: bench.sha(content) for name, content in files.items()},
                'execution_verified': False, 'selection_timing_verified': False,
                'retrieval_profile_enforced': False, 'purpose': 'user-supplied run archive, not measured platform execution'}
    worksheet = {'schema_version': 1, 'packet_sha256': manifest['files']['rubric-packet.json'],
                 'grader_kind': 'human', 'grader_id': '', 'adjudicated_at': '',
                 'items': {identity: {'binding_sha256': by_id[identity]['binding_sha256'],
                                     'response_sha256': bench.sha(row['response'].encode('utf-8')),
                                     'criteria': [{'criterion': i+1,
                                                   'criterion_text': by_id[identity]['rubric'][i]['criterion'],
                                                   'score': None, 'rationale': ''}
                                                  for i in range(4)]}
                           for identity, row in responses.items() if row['response'].strip()}}
    output.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (output/name).write_bytes(content)
    (output/'manifest.json').write_bytes(bench.encoded(manifest))
    # This worksheet is intentionally outside the sealed input file set.
    (output/'adjudication-template.json').write_bytes(bench.encoded(worksheet))


def load_packet(directory: Path) -> tuple[dict, dict]:
    manifest = json.loads((directory/'manifest.json').read_text(encoding='utf-8'))
    if (manifest['schema_version'] != 1 or manifest['name'] != NAME
            or manifest['split'] != 'public-dev' or set(manifest['files']) != SEALED_FILES):
        raise ValueError('Unsupported prose run manifest or file selection')
    for name, expected in manifest['files'].items():
        path = directory/name
        if path.is_symlink() or bench.sha(path.read_bytes()) != expected:
            raise ValueError('A sealed run input changed: ' + name)
    packet = json.loads((directory/'rubric-packet.json').read_text(encoding='utf-8'))
    if packet['schema_version'] != 1 or packet['name'] != NAME or packet['split'] != 'public-dev':
        raise ValueError('Unsupported frozen rubric packet')
    frozen = packet['reference_cores']
    identities = validate_metadata(packet['run_metadata'], frozen)
    if ([c['id'] for c in frozen] != identities or identities != manifest['task_ids']
            or packet['catalog_version'] != manifest['catalog_version']
            or json.loads((directory/'run-metadata.json').read_text(encoding='utf-8')) != packet['run_metadata']
            or (directory/'prompts.jsonl').read_bytes() != jsonl([p for p in bench.prompts(frozen) if p['track']=='natural-language'])
            or (directory/'responses.jsonl').read_bytes() != jsonl(packet['responses'])):
        raise ValueError('Frozen run selection, prompts, responses or provenance disagree')
    validate_responses(frozen, packet['responses'], identities)
    return manifest, packet


def adjudicate(directory: Path, judgment: dict) -> dict:
    manifest, packet = load_packet(directory)
    if (judgment.get('schema_version') != 1 or judgment.get('grader_kind') != 'human'
            or not isinstance(judgment.get('grader_id'), str) or not judgment['grader_id'].strip()
            or judgment.get('packet_sha256') != manifest['files']['rubric-packet.json']):
        raise ValueError('Supply a named human adjudication of this exact frozen packet')
    if aware_time(judgment.get('adjudicated_at')) < aware_time(packet['run_metadata']['created_at']):
        raise ValueError('Adjudication cannot predate the recorded run')
    responses = {row['id']: row for row in packet['responses']}
    nonempty = {identity for identity, row in responses.items() if row['response'].strip()}
    if not isinstance(judgment.get('items'), dict) or set(judgment['items']) != nonempty:
        raise ValueError('Adjudicate every nonempty response exactly once; no judgments for missing answers')
    results = []
    for core in packet['reference_cores']:
        identity = core['id']
        submitted = responses.get(identity)
        scores = []
        if identity in nonempty:
            row = judgment['items'][identity]
            if (row.get('binding_sha256') != core['binding_sha256']
                    or row.get('response_sha256') != bench.sha(submitted['response'].encode('utf-8'))):
                raise ValueError('Adjudication does not bind the exact response and question')
            criteria = row.get('criteria')
            if (not isinstance(criteria, list) or len(criteria) != 4
                    or any(type(c.get('criterion')) is not int for c in criteria)
                    or {c['criterion'] for c in criteria} != {1,2,3,4}):
                raise ValueError('Each adjudication needs all four distinct rubric criteria')
            for criterion in sorted(criteria, key=lambda c:c['criterion']):
                expected_text = core['rubric'][criterion['criterion']-1]['criterion']
                if (type(criterion.get('score')) is not int or criterion['score'] not in {0,1}
                        or criterion.get('criterion_text') != expected_text
                        or not isinstance(criterion.get('rationale'), str) or not criterion['rationale'].strip()):
                    raise ValueError('Keep the frozen rubric text; supply a 0/1 human score and nonempty reason')
                scores.append(dict(criterion))
        results.append({'id': identity, 'family': core['family'], 'level': core['track_levels']['natural-language'],
                        'binding_sha256': core['binding_sha256'], 'submitted': submitted is not None,
                        'nonempty': identity in nonempty, 'criteria': scores,
                        'points': sum(c['score'] for c in scores), 'max_points': 4})
    return {'schema_version': 1, 'scope': 'human-attested prose rubric record; not automatically verified mathematics',
            'run_metadata': packet['run_metadata'], 'catalog_version': packet['catalog_version'], 'split': 'public-dev',
            'results': results, 'points': sum(r['points'] for r in results), 'max_points': 4*len(results),
            'missing_or_empty_count': sum(not r['nonempty'] for r in results),
            'manifest_sha256': bench.sha((directory/'manifest.json').read_bytes()),
            'adjudication_sha256': bench.sha(bench.encoded(judgment)),
            'grader': {k: judgment[k] for k in ('grader_kind','grader_id','adjudicated_at')},
            'scorer_sha256_lf': bench.text_hash(Path(__file__)),
            'execution_verified': False, 'grader_identity_authenticated': False,
            'judgments_automatically_verified': False, 'unseen_generalization_claim': False,
            'scoring_policy': 'Four human rubric points per preselected core. Missing/empty answers score zero and stay in the denominator. No keyword, Lean execution or AI semantic grader is used.'}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('prepare','score'))
    parser.add_argument('--submissions', type=Path)
    parser.add_argument('--run-metadata', type=Path)
    parser.add_argument('--packet', type=Path)
    parser.add_argument('--adjudication', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'prepare':
        if not args.submissions or not args.run_metadata:
            parser.error('prepare needs --submissions and --run-metadata')
        responses = [json.loads(line) for line in args.submissions.read_text(encoding='utf-8').splitlines() if line.strip()]
        prepare(bench.materialize(), responses, json.loads(args.run_metadata.read_text(encoding='utf-8')), args.output)
        print('Prepared a frozen human-grading packet; no score or model execution was created.')
    else:
        if not args.packet or not args.adjudication:
            parser.error('score needs --packet and --adjudication')
        if args.output.exists():
            raise ValueError('Never overwrite a recorded score; choose a fresh output file')
        judgment = json.loads(args.adjudication.read_text(encoding='utf-8'))
        report = adjudicate(args.packet, judgment)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(bench.encoded(report))
        print('Recorded supplied human judgments; not an automated or unseen benchmark score.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
