"""Content-bound editorial review packets for Bench QA, not theorem publication."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import sog_bench as bench

ROOT = bench.ROOT
BASE = bench.DATA.parent
ROUND = BASE / 'reviews/round-1'
PROSE_ROUND = BASE / 'reviews/round-2'
PROSE_SCOPE = 'independent AI natural-language QA editorial review; no aligned Lean certification'
PROSE_REPAIR_SCOPE = 'independent exact prose/difficulty repair; no aligned Lean certification'
PAIRED_REPAIR_SCOPE = 'independent exact scoring repair; paired Lean conclusions unchanged'
SLOTS = ('objects', 'domains', 'quantifiers', 'assumptions', 'conclusion', 'senses', 'constants')
AUTHOR = 'agent-task:root'


def context_binding(core: dict) -> str:
    """Invalidate only the item's actual local import closure, plus pinned APIs."""
    seen = {}
    def visit(rel):
        if rel in seen:
            return
        path = ROOT / rel
        text = path.read_text(encoding='utf-8')
        seen[rel] = bench.text_hash(path)
        for name in re.findall(r'^import ([\w.]+)\s*$', bench.astis_site.sanitize_lean(text), re.M):
            if name.startswith('AutoSamplingTheory.'):
                visit(name.replace('.', '/') + '.lean')
    visit(core['source_file'])
    return bench.sha(bench.encoded({'binding_sha256': core['binding_sha256'], 'local_context': seen,
        'toolchain': bench.text_hash(ROOT / 'lean-toolchain'),
        'mathlib': bench.text_hash(ROOT / 'lake-manifest.json')}))


def decoder_packet(cores: list[dict]) -> tuple[dict, dict]:
    """No question, answer, original id, filename, theorem identity or proof."""
    contexts = [
        ['Kernel α α is a measurable transition kernel with nonnegative extended measure values.',
         'Kernel.IsReversible κ μ means equality of the two nonnegative set integrals for every pair of measurable sets: ∫⁻ x in A, κ x B ∂μ = ∫⁻ x in B, κ x A ∂μ.'],
        ['IsMinOn f Set.univ z means f z ≤ f x for every x.',
         'gradient f x is the real Hilbert-space vector representing fderiv ℝ f x; fderiv and hence this vector are zero when the function is not differentiable at x.',
         'T^[N] x₀ denotes N-fold function iteration, including the identity at N=0.'],
        ['StrongConvexOn Set.univ k V uses the convention V(a • x + b • y) ≤ a*V(x)+b*V(y)−(k/2)*a*b*‖x−y‖² for a,b≥0 and a+b=1.',
         'IsMinOn V Set.univ x₀ means V x₀ ≤ V x for every x.']
    ]
    cases, mapping = [], {}
    by_id = {c['id']: c for c in cores}
    formal = [by_id[f'sogb-{i:03d}'] for i in range(1,4)]
    if not all(bench.has_lean(c) for c in formal):
        raise ValueError('The frozen round requires its original three formal cases')
    for index, core in enumerate(formal):
        alias = chr(ord('A') + index)
        target = core['lean_task'].split('\nexample', 1)[1].rsplit(':= by', 1)[0]
        context = '\n'.join(line for line in core['context'].splitlines() if not line.startswith('open AutoSamplingTheory'))
        cases.append({'case': alias, 'context': context, 'statement': 'example' + target,
                      'definition_context': contexts[index]})
        mapping[alias] = {'core_id': core['id'], 'binding_sha256': core['binding_sha256']}
    packet = {'schema_version': 1, 'compiler_version': 'Lean 4.33.0', 'cases': cases,
              'requested_slots': list(SLOTS),
              'instruction': 'Reconstruct the precise mathematical proposition from these anonymous statements only. Do not inspect other project/source files, questions, solutions or prior audits. Record all assumptions and semantic limits; do not propose a preferred source theorem.'}
    text = json.dumps(packet, ensure_ascii=False)
    secrets = [c[k] for c in cores for k in ('id', 'declaration', 'source_file', 'title')]
    if any(secret in text for secret in secrets) or 'AutoSamplingTheory' in text or 'arXiv' in text:
        raise ValueError('Source identity leaked into anonymous decoder packet')
    return packet, {'schema_version': 1, 'author_identity': AUTHOR, 'cases': mapping,
                    'decoder_packet_sha256': bench.sha(bench.encoded(packet))}


def prepare_decoder(cores: list[dict], output: Path) -> None:
    packet, mapping = decoder_packet(cores)
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError('Use a fresh review-packet directory; no evidence will be overwritten')
    (output / 'anonymous-input.json').write_bytes(bench.encoded(packet))
    (output / 'coordinator-map.json').write_bytes(bench.encoded(mapping))


def prepare_reviewer(cores: list[dict], decoder_input: Path, mapping_path: Path, decoder_output: Path, destination: Path) -> None:
    mapping = json.loads(mapping_path.read_text(encoding='utf-8'))
    decoded = json.loads(decoder_output.read_text(encoding='utf-8'))
    input_sha = bench.sha(decoder_input.read_bytes())
    if mapping['decoder_packet_sha256'] != input_sha or decoded['input_packet_sha256'] != input_sha:
        raise ValueError('Decoder evidence does not bind the exact anonymous packet')
    if decoded['source_text_visible'] is not False or decoded['actor_identity'] == AUTHOR:
        raise ValueError('Decoder must be independent and source-blind')
    expected = set(mapping['cases'])
    if set(decoded['cases']) != expected or any(set(row) != set(SLOTS) or not all(isinstance(v,str) and v.strip() for v in row.values()) for row in decoded['cases'].values()):
        raise ValueError('Decoder must reconstruct every semantic slot of every case')
    by_id = {c['id']: c for c in cores}
    for row in mapping['cases'].values():
        if by_id[row['core_id']]['binding_sha256'] != row['binding_sha256']:
            raise ValueError('QA changed since the anonymous packet was prepared')
    # Authored question/explanation is the review object, not a prior verdict.
    packet = {'schema_version': 1, 'author_identity': AUTHOR, 'decoder_identity': decoded['actor_identity'],
              'decoder_input_sha256': input_sha, 'decoder_output_sha256': bench.sha(decoder_output.read_bytes()),
              'cases': mapping['cases'], 'reconstructions': decoded['cases'],
              'mathematical_cores': cores,
              'context_bindings': {c['id']: context_binding(c) for c in cores},
              'instruction': 'Independently check each question, solution, rubric and cited local support. For the three formal views compare all seven slots against the blind reconstruction. Treat authored scope/alignment claims as claims to audit, not evidence. No earlier reviewer verdicts are supplied. Accept only with precise formal coverage and explicit unformalized explanation. Propose repairs instead of silently altering questions. This is Bench editorial review, not canonical paper-source publication or model evaluation.'}
    if destination.exists():
        raise ValueError('Never overwrite a reviewer packet')
    destination.write_bytes(bench.encoded(packet))


def prepare_repair(cores: list[dict], directory: Path) -> None:
    """Exact-proposal input, deliberately omitting previous verdict/delta text."""
    before_packet = json.loads((directory / 'packets/reviewer-input.json').read_text(encoding='utf-8'))
    before = next(c for c in before_packet['mathematical_cores'] if c['id'] == 'sogb-003')
    after = next(c for c in cores if c['id'] == 'sogb-003')
    old_formal = before['lean_task']
    if after['lean_task'] != old_formal or after['lean_reference'] != before['lean_reference']:
        raise ValueError('This repair route is restricted to unchanged formal code')
    old_authored = {k:v for k,v in before.items() if k not in {'binding_sha256'}}
    new_authored = {k:v for k,v in after.items() if k not in {'binding_sha256'}}
    changed = [k for k in new_authored if old_authored.get(k) != new_authored[k]]
    if changed != ['steps']:
        raise ValueError('The exact explanation-only proposal has an unexpected delta')
    packet = {'schema_version': 1, 'author_identity': AUTHOR, 'core_id': after['id'],
              'before': before, 'proposed_after': after, 'changed_fields': changed,
              'context_sha256': context_binding(after),
              'anonymous_statement_reconstruction': before_packet['reconstructions']['C'],
              'instruction': 'Evaluate this exact explanation-only proposal independently. Earlier reviewer verdicts/delta classifications are intentionally absent. Check mathematical correctness, necessity versus sufficiency, minimality of the edit, unchanged formal coverage and the stated counterexample. This repairs project-authored exposition, not a source textbook or the Lean theorem. Accept, reject or request a narrower repair; do not edit source or prior reports.'}
    destination = directory / 'packets/repair-input.json'
    if destination.exists():
        raise ValueError('Do not overwrite a repair proposal')
    destination.write_bytes(bench.encoded(packet))


def statuses(cores: list[dict], directory: Path = ROUND) -> dict:
    """Editorial evidence only; never a VERIFIED paper/theorem transition."""
    result = {c['id']: {'editorial': 'pending', 'formal_alignment': 'not-reviewed', 'issues': []} for c in cores}
    report_path = directory / 'source-review.json'
    if not report_path.is_file():
        return result
    report = json.loads(report_path.read_text(encoding='utf-8'))
    if report['scope'] != 'independent AI Bench editorial review; not canonical theorem publication':
        raise ValueError('Bench editorial checking must not impersonate theorem publication')
    packet_path = directory / 'packets/reviewer-input.json'
    decoded_path = directory / 'decoder.json'
    input_path = directory / 'packets/anonymous-input.json'
    packet = json.loads(packet_path.read_text(encoding='utf-8'))
    decoded = json.loads(decoded_path.read_text(encoding='utf-8'))
    actors = {AUTHOR, decoded['actor_identity'], report['actor_identity']}
    if len(actors) != 3 or packet['author_identity'] != AUTHOR or packet['decoder_identity'] != decoded['actor_identity']:
        raise ValueError('Author, blind decoder and reviewer must be distinct actual actors')
    if (decoded['source_text_visible'] is not False or decoded['input_packet_sha256'] != bench.sha(input_path.read_bytes())
            or packet['decoder_input_sha256'] != decoded['input_packet_sha256']
            or packet['decoder_output_sha256'] != bench.sha(decoded_path.read_bytes())
            or report['input_packet_sha256'] != bench.sha(packet_path.read_bytes())):
        raise ValueError('Review evidence does not bind the exact input/reconstruction packets')
    for core in cores:
        identity = core['id']
        row = report['items'].get(identity)
        if row is None:
            continue
        if row['binding_sha256'] != core['binding_sha256'] or row['context_sha256'] != context_binding(core):
            result[identity]['editorial'] = 'stale'
            continue
        if row['verdict'] not in {'accept', 'repair-required', 'reject'}:
            raise ValueError('Invalid editorial verdict')
        if not row['mathematics_checks'] or not row['scoring_checks']:
            raise ValueError('An editorial decision needs mathematical and rubric evidence')
        if bench.has_lean(core):
            if set(row['semantic_slots']) != set(SLOTS) or not all(isinstance(v, str) and v.strip() for v in row['semantic_slots'].values()):
                raise ValueError('Aligned-view review needs every semantic slot')
            if row['formal_scope'] != 'conclusion-only' or not row['remaining_unformalized']:
                raise ValueError('This round must disclose the original questions\' unformalized explanatory parts')
        elif row['formal_scope'] != 'no-aligned-view':
            raise ValueError('A supporting theorem cannot create an aligned QA')
        if row['verdict'] == 'accept' and row['repair_requests']:
            raise ValueError('An unresolved mathematical/rubric repair cannot be accepted')
        result[identity] = {'editorial': 'accepted' if row['verdict'] == 'accept' else row['verdict'],
            'formal_alignment': row['formal_scope'], 'issues': row['repair_requests'],
            'reviewer': report['actor_identity'], 'report_sha256': bench.sha(report_path.read_bytes()),
            'remaining_unformalized': row['remaining_unformalized']}
    repair_path = directory / 'repair-review.json'
    if repair_path.is_file():
        repair = json.loads(repair_path.read_text(encoding='utf-8'))
        proposal_path = directory / 'packets/repair-input.json'
        proposal = json.loads(proposal_path.read_text(encoding='utf-8'))
        identity = proposal['core_id']
        current = next((c for c in cores if c['id'] == identity), None)
        if current is None:
            return result
        before, after = proposal['before'], proposal['proposed_after']
        old = next(c for c in packet['mathematical_cores'] if c['id'] == identity)
        if (before != old or report['items'][identity]['verdict'] != 'repair-required'
                or before['lean_task'] != after['lean_task'] or before['lean_reference'] != after['lean_reference']):
            raise ValueError('Repair must preserve the exact original review and formal code')
        if [k for k in after if k != 'binding_sha256' and before.get(k) != after[k]] != ['steps']:
            raise ValueError('An explanation-only repair cannot change other authored fields')
        if (len(before['steps']) != len(after['steps'])
                or [i for i,(a,b) in enumerate(zip(before['steps'], after['steps'])) if a != b] != [3]):
            raise ValueError('This bounded repair changes exactly the fourth explanation step')
        if repair['actor_identity'] in actors or repair['input_packet_sha256'] != bench.sha(proposal_path.read_bytes()):
            raise ValueError('Exact-proposal reviewer must be distinct and bound to the proposal')
        if (current['binding_sha256'] != after['binding_sha256'] or repair['proposed_binding_sha256'] != current['binding_sha256']
                or proposal['context_sha256'] != context_binding(current) or repair['context_sha256'] != context_binding(current)):
            if result[identity]['editorial'] not in {'repair-required', 'reject'}:
                result[identity]['editorial'] = 'stale'
        elif repair['verdict'] == 'accept':
            if repair['repair_requests'] or not repair['mathematics_checks'] or not repair['minimality_checks']:
                raise ValueError('Accepted repair requires mathematics/minimality evidence and no open repair')
            if repair['formal_coverage'] != 'conclusion-only; unchanged' or not repair['remaining_unformalized']:
                raise ValueError('Explanation repair cannot upgrade formal coverage')
            result[identity] = {'editorial': 'accepted-after-repair', 'formal_alignment': 'conclusion-only',
                'issues': [], 'reviewer': repair['actor_identity'], 'report_sha256': bench.sha(repair_path.read_bytes()),
                'prior_review_report_sha256': bench.sha(report_path.read_bytes()),
                'remaining_unformalized': repair['remaining_unformalized']}
        else:
            result[identity] = {'editorial': 'repair-required', 'formal_alignment': 'conclusion-only',
                                'issues': repair['repair_requests']}
    return result


def accepted(row: dict) -> bool:
    return row['editorial'] in {'accepted', 'accepted-after-repair'}


def prepare_prose(cores: list[dict], identities: list[str], destination: Path) -> None:
    """NL-only review: do not invent a blind Lean alignment for an absent task."""
    by_id = {c['id']: c for c in cores}
    if not identities or len(set(identities)) != len(identities) or set(identities) - by_id.keys():
        raise ValueError('Select distinct existing natural-language cores')
    selected = [by_id[identity] for identity in identities]
    if any(bench.has_lean(c) for c in selected):
        raise ValueError('Aligned Lean views require the independent decoder route')
    packet = {'schema_version': 1, 'scope': PROSE_SCOPE, 'author_identity': AUTHOR,
              'mathematical_cores': selected,
              'context_bindings': {c['id']: context_binding(c) for c in selected},
              'instruction': 'Independently check each original natural-language question, formula solution, rubric and cited local support. Inspect the exact local declaration and its hypotheses. Treat authored support/boundary claims as claims to audit. Explain which parts the cited Lean does not prove. No earlier reviewer verdict is supplied. There is no equivalent Lean task and no anonymous Lean reconstruction to certify; do not create one. Return accept, repair-required or reject with mathematical, support and scoring evidence, explicit source-assumption differences and unresolved repair requests. Do not edit the catalog or prior reports. This is editorial review, not theorem publication or a measured benchmark run.'}
    if destination.exists():
        raise ValueError('Never overwrite an independent-review input')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(bench.encoded(packet))


def prepare_scoped_repair(cores: list[dict], directory: Path, identities: list[str], destination: Path, *, formal: bool = False) -> None:
    input_path = directory / ('packets/reviewer-input.json' if formal else 'packets/prose-input.json')
    original = json.loads(input_path.read_text(encoding='utf-8'))
    report_path = directory / 'source-review.json'
    report = json.loads(report_path.read_text(encoding='utf-8'))
    if not identities or len(set(identities)) != len(identities):
        raise ValueError('Select distinct requested repairs')
    cases = {}
    for identity in identities:
        if report['items'][identity]['verdict'] != 'repair-required':
            raise ValueError('Only an explicitly requested repair may enter this route')
        before = next(c for c in original['mathematical_cores'] if c['id'] == identity)
        after = next(c for c in cores if c['id'] == identity)
        cases[identity] = {'before': before, 'proposed_after': after,
                          'context_sha256': context_binding(after),
                          'repair_requests': report['items'][identity]['repair_requests']}
    proposal = {'schema_version': 1, 'scope': PAIRED_REPAIR_SCOPE if formal else PROSE_REPAIR_SCOPE, 'author_identity': AUTHOR,
                'base_input_sha256': bench.sha(input_path.read_bytes()),
                'base_report_sha256': bench.sha(report_path.read_bytes()),
                'cases': cases,
                'instruction': 'Independently audit these exact proposed repairs, source/target invariants, rubric and minimality. Paired repairs may change only rubric fields; NL-only repairs only proof prose and difficulty fields. Never change source, assumptions, question, formal coverage or family. Keep earlier reports immutable; return actual per-item decisions with exact digests and no accepted open repairs.'}
    if destination.exists():
        raise ValueError('Never overwrite a frozen repair proposal')
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(bench.encoded(proposal))


def apply_scoped_repair(cores: list[dict], directory: Path, packet: dict, report: dict, result: dict, *, formal: bool = False) -> None:
    path = directory / 'repair-review.json'
    if not path.is_file():
        return
    proposal_path = directory / 'packets/repair-input.json'
    proposal = json.loads(proposal_path.read_text(encoding='utf-8'))
    repair = json.loads(path.read_text(encoding='utf-8'))
    input_path = directory / ('packets/reviewer-input.json' if formal else 'packets/prose-input.json')
    scope = PAIRED_REPAIR_SCOPE if formal else PROSE_REPAIR_SCOPE
    if (proposal['schema_version'] != 1 or repair['schema_version'] != 1
            or proposal['scope'] != scope or repair['scope'] != scope
            or proposal['author_identity'] != AUTHOR
            or proposal['base_input_sha256'] != bench.sha(input_path.read_bytes())
            or proposal['base_report_sha256'] != bench.sha((directory / 'source-review.json').read_bytes())
            or not proposal['cases'] or set(repair['items']) != set(proposal['cases'])
            or not isinstance(repair['actor_identity'], str) or not repair['actor_identity'].strip()
            or repair['actor_identity'] in {AUTHOR, report['actor_identity'], packet.get('decoder_identity')}
            or repair['input_packet_sha256'] != bench.sha(proposal_path.read_bytes())
            ):
        raise ValueError('Scoped repair needs a fresh independent actor and exact frozen inputs')
    for identity, case in proposal['cases'].items():
        before, after, row = case['before'], case['proposed_after'], repair['items'][identity]
        allowed = {'rubric', 'binding_sha256'} if formal else {'steps', 'difficulty', 'difficulty_reason', 'track_levels', 'binding_sha256'}
        changed = {k for k in before.keys() | after.keys() if before.get(k) != after.get(k)}
        coverage = 'conclusion-only' if formal else 'no-aligned-view'
        if (before != next(c for c in packet['mathematical_cores'] if c['id'] == identity)
                or report['items'][identity]['verdict'] != 'repair-required'
                or case['repair_requests'] != report['items'][identity]['repair_requests']
                or not changed or not changed <= allowed or bench.has_lean(after) != formal
                or (not formal and set(after['track_levels']) != {'natural-language'})
                # Context digests include the QA binding: a prose/rubric repair
                # legitimately changes that digest without changing imports.
                # Rebind today's context to the frozen BEFORE QA to compare.
                # A later changed source is handled as stale below, not used
                # to invalidate the historical report's immutable bytes.
                or (context_binding(after) == case['context_sha256']
                    and context_binding(before) != packet['context_bindings'][identity])
                or after['binding_sha256'] != bench.sha(bench.encoded({k:v for k,v in after.items() if k != 'binding_sha256'}))
                or row['proposed_binding_sha256'] != after['binding_sha256']
                or row['context_sha256'] != case['context_sha256']
                or row['formal_coverage'] != coverage + '; unchanged'
                or row['verdict'] not in {'accept', 'repair-required', 'reject'}
                or not isinstance(row['repair_requests'], list)):
            raise ValueError('Scoped repair must preserve source, target and identity outside its allowed fields')
        for key in ('mathematics_checks', 'minimality_checks', 'remaining_unformalized'):
            if not isinstance(row[key], list) or not row[key] or not all(isinstance(s,str) and s.strip() for s in row[key]):
                raise ValueError('Scoped repair needs mathematics, minimality and formal-boundary evidence')
        if row['verdict'] == 'accept' and row['repair_requests']:
            raise ValueError('Open repairs cannot be accepted')
        current = next((c for c in cores if c['id'] == identity), None)
        if current is None:
            continue
        stale = current['binding_sha256'] != after['binding_sha256'] or context_binding(current) != case['context_sha256']
        result[identity] = {'editorial': 'stale' if stale else ('accepted-after-repair' if row['verdict'] == 'accept' else row['verdict']),
            'formal_alignment': coverage, 'issues': row['repair_requests'],
            'reviewer': repair['actor_identity'], 'report_sha256': bench.sha(path.read_bytes()),
            'prior_review_report_sha256': bench.sha((directory / 'source-review.json').read_bytes()),
            'remaining_unformalized': row['remaining_unformalized']}


def prose_statuses(cores: list[dict], directory: Path = PROSE_ROUND) -> dict:
    report_path = directory / 'source-review.json'
    if not report_path.is_file():
        return {}
    input_path = directory / 'packets/prose-input.json'
    packet = json.loads(input_path.read_text(encoding='utf-8'))
    report = json.loads(report_path.read_text(encoding='utf-8'))
    if (packet['schema_version'] != 1 or report['schema_version'] != 1
            or packet['scope'] != PROSE_SCOPE or report['scope'] != PROSE_SCOPE
            or packet['author_identity'] != AUTHOR
            or not isinstance(report['actor_identity'], str) or not report['actor_identity'].strip()
            or report['actor_identity'] == AUTHOR
            or report['input_packet_sha256'] != bench.sha(input_path.read_bytes())):
        raise ValueError('NL review needs independent authorship, correct scope and exact input bytes')
    frozen = {c['id']: c for c in packet['mathematical_cores']}
    if (len(frozen) != len(packet['mathematical_cores']) or set(report['items']) != set(frozen)
            or set(packet['context_bindings']) != set(frozen)):
        raise ValueError('Review every frozen NL core exactly once')
    result = {}
    for identity, row in report['items'].items():
        original = frozen[identity]
        if (bench.has_lean(original) or row['binding_sha256'] != original['binding_sha256']
                or row['context_sha256'] != packet['context_bindings'][identity]
                or row['formal_scope'] != 'no-aligned-view'):
            raise ValueError('A supporting declaration cannot certify an equivalent Lean QA')
        for key in ('mathematics_checks', 'support_checks', 'scoring_checks', 'source_assumption_differences', 'remaining_unformalized'):
            if not isinstance(row[key], list) or not row[key] or not all(isinstance(s, str) and s.strip() for s in row[key]):
                raise ValueError('NL editorial review needs explicit mathematics, support, rubric and scope evidence')
        if row['verdict'] not in {'accept', 'repair-required', 'reject'} or not isinstance(row['repair_requests'], list):
            raise ValueError('Invalid NL editorial verdict or repair requests')
        if row['verdict'] == 'accept' and row['repair_requests']:
            raise ValueError('Open mathematical/rubric repairs cannot be accepted')
        current = next((c for c in cores if c['id'] == identity), None)
        if current is None:
            continue
        if (bench.has_lean(current) or current['binding_sha256'] != original['binding_sha256']
                or context_binding(current) != packet['context_bindings'][identity]):
            result[identity] = {'editorial': 'stale', 'formal_alignment': 'not-reviewed', 'issues': []}
        else:
            result[identity] = {'editorial': 'accepted' if row['verdict'] == 'accept' else row['verdict'],
                'formal_alignment': 'no-aligned-view', 'issues': row['repair_requests'],
                'reviewer': report['actor_identity'], 'report_sha256': bench.sha(report_path.read_bytes()),
                'remaining_unformalized': row['remaining_unformalized']}
    apply_scoped_repair(cores, directory, packet, report, result)
    return result


def summary(cores: list[dict]) -> dict:
    import sog_bench_formal_review
    rows = statuses(cores)
    prose_rounds = [PROSE_ROUND, *sorted((BASE / 'reviews').glob('prose-*'))]
    for additional in [*(prose_statuses(cores, directory) for directory in prose_rounds),
                       sog_bench_formal_review.statuses(cores)]:
        for identity, row in additional.items():
            if rows[identity]['editorial'] != 'pending':
                raise ValueError('Overlapping review rounds require an explicit supersession policy')
            rows[identity] = row
    return {'kind': 'independent AI editorial review; not canonical theorem publication',
            'accepted_cores': sum(accepted(r) for r in rows.values()), 'total_cores': len(cores),
            'difficulty_calibrated': False, 'model_performance_measured': False, 'items': rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=('decoder-packet', 'reviewer-packet', 'repair-packet', 'prose-packet', 'prose-repair-packet', 'paired-repair-packet'))
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--decoder-input', type=Path)
    parser.add_argument('--mapping', type=Path)
    parser.add_argument('--decoder-output', type=Path)
    parser.add_argument('--ids', nargs='+', help='Distinct NL-only core IDs for prose-packet')
    parser.add_argument('--review-round', type=Path, help='Original NL-only round for an exact prose repair')
    args = parser.parse_args()
    cores = bench.materialize()
    if args.command in {'prose-repair-packet', 'paired-repair-packet'}:
        if not args.review_round or not args.ids:
            parser.error('Supply --review-round and --ids')
        prepare_scoped_repair(cores, args.review_round, args.ids, args.output, formal=args.command == 'paired-repair-packet')
    elif args.command == 'prose-packet':
        prepare_prose(cores, args.ids or [], args.output)
    elif args.command == 'decoder-packet':
        prepare_decoder(cores, args.output)
    elif args.command == 'repair-packet':
        prepare_repair(cores, args.output)
    else:
        if not args.decoder_input or not args.mapping or not args.decoder_output:
            parser.error('Supply --decoder-input, --mapping and --decoder-output')
        prepare_reviewer(cores, args.decoder_input, args.mapping, args.decoder_output, args.output)
    print('Prepared Bench review input; no verdict or admission was created.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
