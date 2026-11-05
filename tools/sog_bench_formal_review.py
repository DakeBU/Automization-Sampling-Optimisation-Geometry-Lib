"""Reusable paired-QA review rounds; input preparation never creates verdicts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sog_bench as bench
import sog_bench_review as review

SCOPE = 'independent AI paired QA editorial review; not canonical theorem publication'
REVIEWS = bench.DATA.parent / 'reviews'


def decoder_payload(cores: list[dict]) -> tuple[dict, dict]:
    if not cores or len({c['id'] for c in cores}) != len(cores) or not all(bench.has_lean(c) for c in cores):
        raise ValueError('Select distinct aligned Lean cores')
    cases, mapping = [], {}
    for index, core in enumerate(cores):
        definitions = core.get('decoder_definitions')
        if not isinstance(definitions, list) or not definitions or not all(isinstance(s, str) and s.strip() for s in definitions):
            raise ValueError('Supply plain minimal definition context, not source identity or a gold proof')
        context = bench.astis_site.sanitize_lean(core['context'])
        context = '\n'.join(line for line in context.splitlines()
                            if not line.strip().startswith(('namespace AutoSamplingTheory', 'end AutoSamplingTheory', 'open AutoSamplingTheory')))
        target = 'example' + core['lean_task'].split('\nexample', 1)[1].rsplit(':= by', 1)[0]
        alias = f'case-{index + 1}'
        cases.append({'case': alias, 'context': context, 'statement': target, 'definition_context': definitions})
        mapping[alias] = {'core_id': core['id'], 'binding_sha256': core['binding_sha256']}
    packet = {'schema_version': 1, 'compiler_version': 'Lean 4.33.0', 'cases': cases,
              'requested_slots': list(review.SLOTS),
              'instruction': 'From these anonymous Lean signatures and definition context only, reconstruct the precise mathematical propositions in all seven slots. Do not inspect project files, sources, filenames, question/answer text, prior audits or repair proposals. Report implicit quantification, typeclass assumptions and what the conclusions do not say. No source-fidelity verdict is requested.'}
    serialized = json.dumps(packet, ensure_ascii=False)
    secrets = [c[key] for c in cores for key in ('id', 'title', 'family', 'source_file', 'declaration')]
    if any(secret in serialized for secret in secrets) or 'AutoSamplingTheory' in serialized or 'arXiv' in serialized:
        raise ValueError('Source identity leaked into the anonymous packet')
    return packet, {'schema_version': 1, 'author_identity': review.AUTHOR, 'cases': mapping,
                    'decoder_packet_sha256': bench.sha(bench.encoded(packet))}


def prepare_decoder(cores: list[dict], output: Path) -> None:
    packet, mapping = decoder_payload(cores)
    if output.exists() and any(output.iterdir()):
        raise ValueError('Use a fresh packet directory; never overwrite audit evidence')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'anonymous-input.json').write_bytes(bench.encoded(packet))
    (output / 'coordinator-map.json').write_bytes(bench.encoded(mapping))


def decoder_evidence(directory: Path, frozen: list[dict]) -> tuple[dict, dict]:
    packets = directory / 'packets'
    input_path = packets / 'anonymous-input.json'
    map_path = packets / 'coordinator-map.json'
    decoded_path = directory / 'decoder.json'
    packet, mapping = decoder_payload(frozen)
    if input_path.read_bytes() != bench.encoded(packet) or map_path.read_bytes() != bench.encoded(mapping):
        raise ValueError('Anonymous input/mapping no longer matches the frozen formal target')
    decoded = json.loads(decoded_path.read_text(encoding='utf-8'))
    if (decoded['schema_version'] != 1 or decoded['source_text_visible'] is not False
            or not isinstance(decoded['actor_identity'], str) or not decoded['actor_identity'].strip()
            or decoded['actor_identity'] == review.AUTHOR
            or decoded['input_packet_sha256'] != bench.sha(input_path.read_bytes())
            or set(decoded['cases']) != set(mapping['cases'])):
        raise ValueError('Decoder must be independent, source-blind and bound to every exact case')
    if any(set(row) != set(review.SLOTS) or not all(isinstance(s, str) and s.strip() for s in row.values())
           for row in decoded['cases'].values()):
        raise ValueError('Every blind reconstruction needs all seven semantic slots')
    return mapping, decoded


def prepare_reviewer(cores: list[dict], directory: Path) -> None:
    mapping = json.loads((directory / 'packets/coordinator-map.json').read_text(encoding='utf-8'))
    by_id = {c['id']: c for c in cores}
    aliases = sorted(mapping['cases'], key=lambda alias: int(alias.rsplit('-', 1)[1]))
    frozen = [by_id[mapping['cases'][alias]['core_id']] for alias in aliases]
    mapping, decoded = decoder_evidence(directory, frozen)
    packet = {'schema_version': 1, 'scope': SCOPE, 'author_identity': review.AUTHOR,
              'decoder_identity': decoded['actor_identity'],
              'decoder_input_sha256': mapping['decoder_packet_sha256'],
              'decoder_output_sha256': bench.sha((directory / 'decoder.json').read_bytes()),
              'cases': mapping['cases'], 'reconstructions': decoded['cases'], 'mathematical_cores': frozen,
              'context_bindings': {c['id']: review.context_binding(c) for c in frozen},
              'instruction': 'Independently audit each authored question, formula proof, rubric and actual local declaration. Compare all seven slots to the blind reconstruction. The authored support, status and formal-coverage language are claims to audit, not preferred verdicts. No previous source verdict or repair proposal is supplied. Record precise conclusion-only formal coverage and remaining unformalized explanation; accept, request repair or reject with mathematical and scoring evidence. This is Bench editorial review, not canonical theorem publication or model measurement.'}
    destination = directory / 'packets/reviewer-input.json'
    if destination.exists():
        raise ValueError('Never overwrite a source-review packet')
    destination.write_bytes(bench.encoded(packet))


def round_statuses(cores: list[dict], directory: Path) -> dict:
    report_path = directory / 'source-review.json'
    if not report_path.is_file():
        return {}
    packet_path = directory / 'packets/reviewer-input.json'
    packet = json.loads(packet_path.read_text(encoding='utf-8'))
    report = json.loads(report_path.read_text(encoding='utf-8'))
    frozen = packet['mathematical_cores']
    mapping, decoded = decoder_evidence(directory, frozen)
    actors = {review.AUTHOR, decoded['actor_identity'], report['actor_identity']}
    if (packet['schema_version'] != 1 or report['schema_version'] != 1
            or packet['scope'] != SCOPE or report['scope'] != SCOPE
            or packet['author_identity'] != review.AUTHOR or len(actors) != 3
            or not isinstance(report['actor_identity'], str) or not report['actor_identity'].strip()
            or packet['decoder_identity'] != decoded['actor_identity']
            or packet['decoder_input_sha256'] != mapping['decoder_packet_sha256']
            or packet['decoder_output_sha256'] != bench.sha((directory / 'decoder.json').read_bytes())
            or packet['cases'] != mapping['cases'] or packet['reconstructions'] != decoded['cases']
            or report['input_packet_sha256'] != bench.sha(packet_path.read_bytes())):
        raise ValueError('Paired review needs three distinct actual actors and exact frozen inputs')
    originals = {c['id']: c for c in frozen}
    if len(originals) != len(frozen) or set(report['items']) != set(originals) or set(packet['context_bindings']) != set(originals):
        raise ValueError('Review every frozen paired core exactly once')
    current = {c['id']: c for c in cores}
    result = {}
    for identity, row in report['items'].items():
        original = originals[identity]
        if (row['binding_sha256'] != original['binding_sha256']
                or row['context_sha256'] != packet['context_bindings'][identity]
                or row['formal_scope'] != 'conclusion-only'):
            raise ValueError('Formal review must preserve the frozen question and its conclusion-only boundary')
        if (set(row['semantic_slots']) != set(review.SLOTS)
                or not all(isinstance(s, str) and s.strip() for s in row['semantic_slots'].values())):
            raise ValueError('Source comparison requires all seven semantic slots')
        for key in ('mathematics_checks', 'scoring_checks', 'remaining_unformalized'):
            if not isinstance(row[key], list) or not row[key] or not all(isinstance(s, str) and s.strip() for s in row[key]):
                raise ValueError('Paired acceptance needs mathematical/rubric evidence and explicit formal limits')
        if row['verdict'] not in {'accept', 'repair-required', 'reject'} or not isinstance(row['repair_requests'], list):
            raise ValueError('Invalid paired-QA editorial decision')
        if row['verdict'] == 'accept' and row['repair_requests']:
            raise ValueError('Open repairs cannot be accepted')
        core = current.get(identity)
        if core is None:
            continue
        stale = core['binding_sha256'] != original['binding_sha256'] or review.context_binding(core) != row['context_sha256']
        result[identity] = {'editorial': 'stale' if stale else ('accepted' if row['verdict'] == 'accept' else row['verdict']),
            'formal_alignment': 'not-reviewed' if stale else 'conclusion-only', 'issues': row['repair_requests'],
            'reviewer': report['actor_identity'], 'report_sha256': bench.sha(report_path.read_bytes()),
            'remaining_unformalized': row['remaining_unformalized']}
    review.apply_scoped_repair(cores, directory, packet, report, result, formal=True)
    return result


def statuses(cores: list[dict], root: Path = REVIEWS) -> dict:
    result = {}
    for directory in sorted(root.glob('formal-*')):
        rows = round_statuses(cores, directory)
        if result.keys() & rows.keys():
            raise ValueError('Overlapping paired rounds require an explicit supersession policy')
        result.update(rows)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('decoder-packet', 'reviewer-packet'))
    parser.add_argument('--round', type=Path, required=True)
    parser.add_argument('--ids', nargs='+')
    args = parser.parse_args()
    cores = bench.materialize()
    if args.command == 'decoder-packet':
        by_id = {c['id']: c for c in cores}
        if not args.ids or any(identity not in by_id for identity in args.ids):
            parser.error('Select existing aligned --ids')
        prepare_decoder([by_id[identity] for identity in args.ids], args.round / 'packets')
    else:
        prepare_reviewer(cores, args.round)
    print('Prepared input only; independent actors must write their own reports.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
