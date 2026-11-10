"""Freeze prose runs and record human rubric judgments; never execute answers."""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime
from fractions import Fraction
import json
from pathlib import Path
import unicodedata

import sog_bench as bench

SEALED_FILES = {'run-metadata.json', 'prompts.jsonl', 'responses.jsonl', 'rubric-packet.json'}
PLAN_FILE = 'registered-plan.json'
NAME = 'SamplingOptimisationGeometryBench prose run'
PLAN_NAME = 'SamplingOptimisationGeometryBench prose run plan'
PANEL_RESOLUTION = 'SamplingOptimisationGeometryBench prose panel resolution'


def aware_time(value: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError('Record a timezone-aware ISO timestamp')
    result = datetime.fromisoformat(value)
    if result.tzinfo is None:
        raise ValueError('Timestamp must include its timezone')
    return result


def validate_metadata(metadata: dict, cores: list[dict], *, prompt_profile: str = 'catalog-question') -> list[str]:
    if not isinstance(metadata, dict):
        raise ValueError('Run metadata must be a JSON object')
    for key in ('run_id', 'model', 'model_version'):
        if not isinstance(metadata.get(key), str) or not metadata[key].strip():
            raise ValueError('Record run identity and actual model/version')
    aware_time(metadata.get('created_at'))
    if (metadata.get('track') != 'natural-language'
            or metadata.get('prompt_profile') != prompt_profile
            or metadata.get('attempt_policy') != 'first-attempt'):
        raise ValueError('A first-attempt prose run with the expected prompt profile is required')
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


def select_admitted(cores: list[dict], metadata: dict) -> tuple[list[str], list[dict], dict]:
    identities = validate_metadata(metadata, cores)
    by_id = {c['id']: c for c in cores}
    selected = [by_id[identity] for identity in identities]
    eligibility = bench.editorial_review(selected)
    if any(row['editorial'] not in {'accepted', 'accepted-after-repair'} for row in eligibility['items'].values()):
        raise ValueError('Scored prose tasks need current editorial admission, not draft or stale references')
    return identities, selected, eligibility


def prompt_bytes(selected: list[dict]) -> bytes:
    return jsonl([row for row in bench.prompts(selected) if row['track'] == 'natural-language'])


def plan_record(version: str, metadata: dict, selected: list[dict], prompts: bytes) -> dict:
    return {'schema_version': 1, 'name': PLAN_NAME, 'split': 'public-dev', 'catalog_version': version,
            'run_metadata': metadata, 'prompt_sha256': bench.sha(prompts),
            'task_bindings': [{k: c[k] for k in ('id', 'binding_sha256')} for c in selected]}


def verify_plan(raw: bytes, expected: dict) -> str:
    if raw != bench.encoded(expected):
        raise ValueError('The plan differs from the exact catalog version, selection, prompts, or run conditions')
    return bench.sha(raw)


def register_plan(cores: list[dict], metadata: dict, output: Path) -> str:
    """Write only a plan and prompt-only inputs, without accepting any answers."""
    _, selected, _ = select_admitted(cores, metadata)
    prompts = prompt_bytes(selected)
    plan = bench.encoded(plan_record(bench.load()['version'], metadata, selected, prompts))
    try:
        output.mkdir(parents=True)
    except FileExistsError as exc:
        raise ValueError('Use a new plan directory; no existing files will be overwritten') from exc
    (output/'plan.json').write_bytes(plan)
    (output/'prompts.jsonl').write_bytes(prompts)
    return bench.sha(plan)


def judgment_template(cores: list[dict], responses: list[dict], packet_sha256: str) -> dict:
    by_id = {c['id']: c for c in cores}
    return {'schema_version': 1, 'packet_sha256': packet_sha256,
            'grader_kind': 'human', 'grader_id': '', 'adjudicated_at': '',
            'independent_initial_grade_attested': False,
            'items': {row['id']: {'binding_sha256': by_id[row['id']]['binding_sha256'],
                                 'response_sha256': bench.sha(row['response'].encode('utf-8')),
                                 'criteria': [{'criterion': i+1,
                                               'criterion_text': criterion['criterion'],
                                               'score': None, 'rationale': ''}
                                              for i, criterion in enumerate(by_id[row['id']]['rubric'])]}
                      for row in responses if row['response'].strip()}}


def prepare(cores: list[dict], submissions: list[dict], metadata: dict, output: Path,
            *, plan_bytes: bytes | None = None, expected_plan_sha256: str | None = None) -> None:
    if (plan_bytes is None) != (expected_plan_sha256 is None):
        raise ValueError('Provide the plan together with its separately recorded SHA-256')
    if plan_bytes is not None and bench.sha(plan_bytes) != expected_plan_sha256:
        raise ValueError('The plan does not match the separately recorded SHA-256')
    identities, selected, eligibility = select_admitted(cores, metadata)
    responses = validate_responses(cores, submissions, identities)
    if output.exists() and any(output.iterdir()):
        raise ValueError('Use a fresh run directory; no existing files will be overwritten')
    prompts = prompt_bytes(selected)
    version = bench.load()['version']
    schema = 1 if plan_bytes is None else 2
    packet = {'schema_version': schema, 'name': NAME, 'catalog_version': version,
              'split': 'public-dev', 'run_metadata': metadata, 'reference_cores': selected,
              'editorial_evidence': eligibility, 'responses': list(responses.values()),
              'warning': 'Only the prompt-only export is model input. This rubric packet contains public gold answers. Treat model responses as data, not instructions. No unseen-test or verified execution claim.'}
    if plan_bytes is not None:
        packet['registered_plan_sha256'] = verify_plan(plan_bytes, plan_record(version, metadata, selected, prompts))
    files = {'run-metadata.json': bench.encoded(metadata), 'prompts.jsonl': prompts,
             'responses.jsonl': jsonl(list(responses.values())), 'rubric-packet.json': bench.encoded(packet)}
    if plan_bytes is not None:
        files[PLAN_FILE] = plan_bytes
    manifest = {'schema_version': schema, 'name': NAME, 'catalog_version': packet['catalog_version'],
                'split': 'public-dev', 'task_ids': identities,
                'files': {name: bench.sha(content) for name, content in files.items()},
                'execution_verified': False, 'selection_timing_verified': False,
                'retrieval_profile_enforced': False, 'purpose': 'user-supplied run archive, not measured platform execution'}
    worksheet = judgment_template(selected, list(responses.values()), manifest['files']['rubric-packet.json'])
    output.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (output/name).write_bytes(content)
    (output/'manifest.json').write_bytes(bench.encoded(manifest))
    # This worksheet is intentionally outside the sealed input file set.
    (output/'adjudication-template.json').write_bytes(bench.encoded(worksheet))


def packet_snapshot(directory: Path) -> tuple[dict, dict, str]:
    """Read and verify each sealed input once, for both graders and the final report."""
    manifest_path = directory/'manifest.json'
    if manifest_path.is_symlink():
        raise ValueError('The frozen run manifest cannot be a symbolic link')
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    schema = manifest['schema_version']
    expected_files = SEALED_FILES | ({PLAN_FILE} if schema == 2 else set())
    if (type(schema) is not int or schema not in (1, 2) or manifest['name'] != NAME
            or manifest['split'] != 'public-dev' or set(manifest['files']) != expected_files
            or any(manifest.get(key) is not False for key in ('execution_verified', 'selection_timing_verified',
                                                               'retrieval_profile_enforced'))):
        raise ValueError('Unsupported prose run manifest or file selection')
    sealed = {}
    for name, expected in manifest['files'].items():
        path = directory/name
        if path.is_symlink():
            raise ValueError('A sealed run input changed: ' + name)
        sealed[name] = path.read_bytes()
        if bench.sha(sealed[name]) != expected:
            raise ValueError('A sealed run input changed: ' + name)
    packet = json.loads(sealed['rubric-packet.json'])
    if (type(packet['schema_version']) is not int or packet['schema_version'] != schema
            or packet['name'] != NAME or packet['split'] != 'public-dev'):
        raise ValueError('Unsupported frozen rubric packet')
    frozen = packet['reference_cores']
    identities = validate_metadata(packet['run_metadata'], frozen)
    if ([c['id'] for c in frozen] != identities or identities != manifest['task_ids']
            or packet['catalog_version'] != manifest['catalog_version']
            or json.loads(sealed['run-metadata.json']) != packet['run_metadata']
            or sealed['prompts.jsonl'] != prompt_bytes(frozen)
            or sealed['responses.jsonl'] != jsonl(packet['responses'])):
        raise ValueError('Frozen run selection, prompts, responses or provenance disagree')
    if schema == 2:
        plan_sha = verify_plan(sealed[PLAN_FILE], plan_record(packet['catalog_version'], packet['run_metadata'],
                                                             frozen, sealed['prompts.jsonl']))
        if packet.get('registered_plan_sha256') != plan_sha:
            raise ValueError('The archived plan binding differs from the rubric packet')
    elif 'registered_plan_sha256' in packet:
        raise ValueError('An unregistered archive cannot claim a registered plan')
    validate_responses(frozen, packet['responses'], identities)
    return manifest, packet, bench.sha(manifest_bytes)


def load_packet(directory: Path) -> tuple[dict, dict]:
    manifest, packet, _ = packet_snapshot(directory)
    return manifest, packet


def totals(rows: list[dict]) -> dict:
    return {'selected_cores': len(rows), 'selected_families': len({r['family'] for r in rows}),
            'missing_or_empty_count': sum(not r['nonempty'] for r in rows),
            'points': sum(r['points'] for r in rows), 'max_points': sum(r['max_points'] for r in rows)}


def breakdown(rows: list[dict]) -> dict:
    """Use the selected denominator, with exact equal-weight family averaging."""
    def groups(key):
        buckets = defaultdict(list)
        for row in rows:
            buckets[row[key]].append(row)
        return {name: totals(bucket) for name, bucket in sorted(buckets.items())}

    families = groups('family')
    rate = sum((Fraction(x['points'], x['max_points']) for x in families.values()), Fraction()) / len(families)
    return {'by_family': families, 'by_level': groups('level'),
            'family_macro_rate': {'numerator': rate.numerator, 'denominator': rate.denominator},
            'scope': 'Descriptive breakdown of selected natural-language cores only. Each represented family has equal weight in family_macro_rate. Missing answers remain in every applicable denominator. Provisional levels are not empirical calibration.'}


def grade_snapshot(snapshot: tuple[dict, dict, str], judgment: dict) -> dict:
    manifest, packet, manifest_sha = snapshot
    if not isinstance(judgment, dict):
        raise ValueError('A human adjudication must be a JSON object')


    if (type(judgment.get('schema_version')) is not int or judgment['schema_version'] != 1
            or judgment.get('grader_kind') != 'human'
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
            if (not isinstance(row, dict) or row.get('binding_sha256') != core['binding_sha256']
                    or row.get('response_sha256') != bench.sha(submitted['response'].encode('utf-8'))):
                raise ValueError('Adjudication does not bind the exact response and question')
            criteria = row.get('criteria')
            if (not isinstance(criteria, list) or len(criteria) != 4
                    or any(not isinstance(c, dict) or type(c.get('criterion')) is not int for c in criteria)
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
            'run_metadata': packet['run_metadata'], 'catalog_version': packet['catalog_version'], 'split': packet['split'],
            'results': results, **totals(results), 'breakdown': breakdown(results),
            'manifest_sha256': manifest_sha,
            'registered_plan_sha256': packet.get('registered_plan_sha256'), 'selection_timing_verified': False,
            'adjudication_sha256': bench.sha(bench.encoded(judgment)),
            'grader': {k: judgment[k] for k in ('grader_kind','grader_id','adjudicated_at')},
            'scorer_sha256_lf': bench.text_hash(Path(__file__)),
            'execution_verified': False, 'grader_identity_authenticated': False,
            'judgments_automatically_verified': False, 'unseen_generalization_claim': False,
            'scoring_policy': 'Four human rubric points per preselected core. Missing/empty answers score zero and stay in the denominator. No keyword, Lean execution or AI semantic grader is used.'}


def adjudicate(directory: Path, judgment: dict) -> dict:
    return grade_snapshot(packet_snapshot(directory), judgment)


def actor_key(name: str) -> str:
    return unicodedata.normalize('NFKC', name).strip().casefold()


def panel_inputs(directory: Path, first: dict, second: dict) -> tuple[dict, dict, dict]:
    snapshot = packet_snapshot(directory)
    a, b = (grade_snapshot(snapshot, sheet) for sheet in (first, second))
    if (any(sheet.get('independent_initial_grade_attested') is not True for sheet in (first, second))
            or actor_key(a['grader']['grader_id']) == actor_key(b['grader']['grader_id'])):
        raise ValueError('The panel requires two distinct named humans attesting independently recorded initial grades')
    disagreements = {}
    for left, right in zip(a['results'], b['results'], strict=True):
        for x, y in zip(left['criteria'], right['criteria'], strict=True):
            if x['score'] != y['score']:
                disagreements.setdefault(left['id'], {})[str(x['criterion'])] = {
                    'criterion_text': x['criterion_text'], 'initial_scores': [x['score'], y['score']],
                    'score': None, 'rationale': ''}
    template = {'schema_version': 1, 'name': PANEL_RESOLUTION,
                'packet_sha256': snapshot[0]['files']['rubric-packet.json'],
                'initial_adjudication_sha256': [a['adjudication_sha256'], b['adjudication_sha256']],
                'resolver_kind': 'human', 'resolver_id': '', 'resolved_at': '', 'items': disagreements}
    return a, b, template


def panel_template(directory: Path, first: dict, second: dict) -> dict:
    return panel_inputs(directory, first, second)[2]


def validate_resolution(a: dict, b: dict, template: dict, resolution: dict | None) -> dict:
    expected = template['items']
    if not expected:
        if resolution is not None:
            raise ValueError('No disputes exist; a resolution may not override agreed grades')
        return {}
    if (not isinstance(resolution, dict) or set(resolution) != set(template)
            or any(resolution[k] != template[k] for k in ('schema_version', 'name', 'packet_sha256',
                                                          'initial_adjudication_sha256', 'resolver_kind'))
            or type(resolution['schema_version']) is not int
            or not isinstance(resolution['resolver_id'], str) or not actor_key(resolution['resolver_id'])
            or actor_key(resolution['resolver_id']) in {actor_key(x['grader']['grader_id']) for x in (a, b)}
            or aware_time(resolution['resolved_at']) < max(aware_time(x['grader']['adjudicated_at']) for x in (a, b))
            or not isinstance(resolution['items'], dict) or set(resolution['items']) != set(expected)):
        raise ValueError('Resolve all disputes on the exact ordered initial grades with a distinct named human')
    for identity, keys in expected.items():
        provided = resolution['items'][identity]
        if not isinstance(provided, dict) or set(provided) != set(keys):
            raise ValueError('Resolve every and only disputed criterion')
        for key, old in keys.items():
            row = provided[key]
            if (not isinstance(row, dict) or set(row) != set(old)
                    or row['criterion_text'] != old['criterion_text'] or row['initial_scores'] != old['initial_scores']
                    or type(row['initial_scores']) is not list or any(type(s) is not int for s in row['initial_scores'])
                    or type(row['score']) is not int or row['score'] not in {0, 1}
                    or not isinstance(row['rationale'], str) or not row['rationale'].strip()):
                raise ValueError('Keep each dispute binding unchanged and supply a 0/1 resolution and a reason')
    return resolution['items']


def adjudicate_panel(directory: Path, first: dict, second: dict, resolution: dict | None = None) -> dict:
    a, b, template = panel_inputs(directory, first, second)
    disputed = validate_resolution(a, b, template, resolution)
    results, agreement, disagreement = [], 0, 0
    for left, right in zip(a['results'], b['results'], strict=True):
        criteria = []
        for x, y in zip(left['criteria'], right['criteria'], strict=True):
            decision = disputed.get(left['id'], {}).get(str(x['criterion']))
            agreement += decision is None
            disagreement += decision is not None
            criteria.append({'criterion': x['criterion'], 'criterion_text': x['criterion_text'],
                             'initial_grades': [{k: row[k] for k in ('score', 'rationale')} for row in (x, y)],
                             'resolution': {k: decision[k] for k in ('score', 'rationale')} if decision else None,
                             'score': decision['score'] if decision else x['score']})
        results.append({**left, 'criteria': criteria, 'points': sum(row['score'] for row in criteria)})
    return {k: a[k] for k in ('schema_version', 'run_metadata', 'catalog_version', 'split', 'manifest_sha256',
                              'registered_plan_sha256', 'selection_timing_verified',
                              'scorer_sha256_lf', 'execution_verified', 'grader_identity_authenticated',
                              'judgments_automatically_verified', 'unseen_generalization_claim')} | {
        'report_kind': 'two-human-grader-prose-panel',
        'scope': 'Human-attested panel judgments only; independent grading, identity and execution not authenticated',
        'packet_sha256': template['packet_sha256'],
        'initial_graders': [a['grader'], b['grader']],
        'initial_adjudication_sha256': template['initial_adjudication_sha256'],
        'resolution_sha256': bench.sha(bench.encoded(resolution)) if resolution is not None else None,
        'resolver': {k: resolution[k] for k in ('resolver_kind', 'resolver_id', 'resolved_at')}
                    if resolution is not None else None,
        'criterion_agreement': {'agreed': agreement, 'disputed': disagreement,
                                'compared': agreement + disagreement,
                                'scope': 'Nonempty responses only; descriptive pre-resolution counts, not statistical agreement or independent samples.'},
        'results': results, **totals(results), 'breakdown': breakdown(results),
        'scoring_policy': 'Agreeing rubric scores are kept. A third named human resolves only disputed criteria. Missing/empty answers score zero and remain in every applicable score denominator.'}


def write_new_report(output: Path, report: dict) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with output.open('xb') as stream:
            stream.write(bench.encoded(report))
    except FileExistsError as exc:
        raise ValueError('Never overwrite a recorded score or panel worksheet; choose a fresh output file') from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('plan', 'prepare', 'score', 'panel-template', 'score-panel'))
    parser.add_argument('--submissions', type=Path)
    parser.add_argument('--run-metadata', type=Path)
    parser.add_argument('--plan', type=Path)
    parser.add_argument('--plan-sha256', help='The plan digest recorded separately before the run')
    parser.add_argument('--packet', type=Path)
    parser.add_argument('--adjudication', type=Path)
    parser.add_argument('--second-adjudication', type=Path)
    parser.add_argument('--resolution', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.command != 'prepare' and (args.plan or args.plan_sha256 is not None):
        parser.error('--plan and --plan-sha256 only apply to prepare')
    if args.command == 'plan':
        if not args.run_metadata or any((args.submissions, args.packet, args.adjudication,
                                        args.second_adjudication, args.resolution)):
            parser.error('plan takes --run-metadata and a new --output directory, not answers or grades')
        metadata = json.loads(args.run_metadata.read_text(encoding='utf-8'))
        digest = register_plan(bench.materialize(), metadata, args.output)
        print('Plan SHA-256: ' + digest)
        print('Keep that digest separately; give the model prompts.jsonl only. No execution or timestamp attestation was created.')
    elif args.command == 'prepare':
        if not args.submissions or (args.run_metadata is None) == (args.plan is None):
            parser.error('prepare needs --submissions and either --run-metadata or --plan')
        if (args.plan is None) != (args.plan_sha256 is None):
            parser.error('--plan requires --plan-sha256 from the pre-response record')
        raw_plan = args.plan.read_bytes() if args.plan else None
        if raw_plan is not None:
            plan = json.loads(raw_plan)
            if not isinstance(plan, dict) or plan.get('name') != PLAN_NAME or 'run_metadata' not in plan:
                parser.error('--plan must point to an exact plan.json produced by plan')
            metadata = plan['run_metadata']
        else:
            metadata = json.loads(args.run_metadata.read_text(encoding='utf-8'))
        responses = [json.loads(line) for line in args.submissions.read_text(encoding='utf-8').splitlines() if line.strip()]
        prepare(bench.materialize(), responses, metadata, args.output, plan_bytes=raw_plan,
                expected_plan_sha256=args.plan_sha256)
        print('Prepared a frozen human-grading packet; no score or model execution was created.')
    elif args.command == 'score':
        if not args.packet or not args.adjudication:
            parser.error('score needs --packet and --adjudication')
        if args.second_adjudication or args.resolution:
            parser.error('use score-panel for two initial adjudications')
        judgment = json.loads(args.adjudication.read_text(encoding='utf-8'))
        report = adjudicate(args.packet, judgment)
        write_new_report(args.output, report)
        print('Recorded supplied human judgments; not an automated or unseen benchmark score.')
    else:
        if not args.packet or not args.adjudication or not args.second_adjudication:
            parser.error('panel commands need --packet, --adjudication and --second-adjudication')
        first, second = (json.loads(p.read_text(encoding='utf-8'))
                         for p in (args.adjudication, args.second_adjudication))
        if args.command == 'panel-template':
            if args.resolution:
                parser.error('panel-template does not accept a resolution')
            worksheet = panel_template(args.packet, first, second)
            write_new_report(args.output, worksheet)
            print('Prepared a worksheet for disputed criteria only; no score recorded.')
        else:
            resolution = json.loads(args.resolution.read_text(encoding='utf-8')) if args.resolution else None
            if args.resolution and not isinstance(resolution, dict):
                parser.error('--resolution must be a completed JSON worksheet; omit it when there are no disputes')
            report = adjudicate_panel(args.packet, first, second, resolution)
            write_new_report(args.output, report)
            print('Recorded two human attestations and any dispute resolution; not an automated or unseen benchmark score.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
