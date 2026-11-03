"""Independent structural-QA editorial evidence, never theorem entailment."""
from __future__ import annotations

import argparse
import inspect
import json
from pathlib import Path

import sog_bench as bench
import sog_bench_review as review

ROUND = bench.DATA.parent/'reviews/graph-1'
SCOPE = 'independent AI structural QA editorial review; not mathematical necessity or calibration'
REPAIR_ROUND = ROUND.parent/'graph-3'
REPAIR_SCOPE = 'independent AI graph-difficulty repair review; not empirical calibration'
CURRENT_ROUND = ROUND.parent/'graph-7'
CURRENT_REPAIR_ROUND = ROUND.parent/'graph-8'
SUPERSEDES = ['graph-1','graph-2','graph-3','graph-4','graph-5','graph-6']


def payload(items: list[dict]) -> dict:
    frozen = [{k:v for k,v in item.items() if k not in {'review_status','reference_status'}} for item in items]
    return {'schema_version': 1, 'scope': SCOPE, 'author_identity': review.AUTHOR, 'items': frozen,
            'spec_sha256_lf': bench.text_hash(bench.curriculum.BASE/'graph_tasks.json'),
            'policy_sha256_lf': bench.text_hash(bench.curriculum.BASE/'curriculum.json'),
            'scorer_source': inspect.getsource(bench.curriculum.grade_graph).replace('\r\n','\n'),
            'supersedes_rounds':SUPERSEDES,
            'instruction': 'Independently inspect every current question, original source and evidence kind, including both compiler slices and fresh trusted replay. Audit core/family links, source eligibility, body-edge direction, omitted-constant/private/full-closure boundaries, unexpanded-statement constant profiles, typed/path operations, scoring and provisional reasoning levels from scratch. Statement occurrences are not a binder-role analysis, inferred hypothesis list or necessity certificate; absence is not absence after definition unfolding. Neither positive nor absent induced paths certify mathematical necessity or full independence. Earlier verdicts and preferred repairs are omitted. Compiler replay is not editorial acceptance; reference self-tests are not model measurements. Return accept, repair-required or reject with precise evidence for every item. This full-scope round explicitly supersedes earlier graph rounds for current admission without rewriting reports; do not edit corpus or publish canonical theorem status.'}


def prepare(output: Path) -> None:
    if output.exists():
        raise ValueError('Never overwrite an independent graph-review input')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(bench.encoded(payload(bench.curriculum.graph_items())))


def statuses(items: list[dict], directory: Path = ROUND) -> dict:
    result = {item['id']: {'editorial':'pending'} for item in items}
    report_path = directory/'source-review.json'
    if not report_path.is_file():
        return result
    input_path = directory/'input.json'
    packet = json.loads(input_path.read_text(encoding='utf-8'))
    report = json.loads(report_path.read_text(encoding='utf-8'))
    if (packet['schema_version'] != 1 or report['schema_version'] != 1
            or packet['scope'] != SCOPE or report['scope'] != SCOPE
            or packet['author_identity'] != review.AUTHOR
            or not isinstance(report['actor_identity'], str) or not report['actor_identity'].strip()
            or report['actor_identity'] == review.AUTHOR
            or report['input_packet_sha256'] != bench.sha(input_path.read_bytes())):
        raise ValueError('Structural review needs a distinct actual actor and exact input bytes/scope')
    frozen = {item['id']:item for item in packet['items']}
    if len(frozen) != len(packet['items']) or set(report['items']) != set(frozen):
        raise ValueError('Review every frozen graph question exactly once')
    current = payload(items)
    # Each frozen row already binds its full graph, question, label and answer.
    # Editing another task in the specification must not stale this task.
    global_current = all(packet[key] == current[key] for key in ('policy_sha256_lf','scorer_source'))
    for item in items:
        identity = item['id']
        row = report['items'].get(identity)
        if row is None:
            continue
        if (row['binding_sha256'] != frozen[identity]['binding_sha256']
                or row['mathematical_necessity_certified'] is not False):
            raise ValueError('A graph review cannot certify mathematical necessity')
        for key in ('graph_checks','scoring_checks','difficulty_checks','remaining_limits'):
            if not isinstance(row[key], list) or not row[key] or not all(isinstance(s,str) and s.strip() for s in row[key]):
                raise ValueError('Structural editorial decisions need explicit graph/scoring/level/boundary evidence')
        if row['verdict'] not in {'accept','repair-required','reject'} or not isinstance(row['repair_requests'],list):
            raise ValueError('Invalid structural editorial decision')
        if row['verdict']=='accept' and row['repair_requests']:
            raise ValueError('Unresolved structural/rubric repairs cannot be accepted')
        clean_item = {k:v for k,v in item.items() if k not in {'review_status','reference_status'}}
        stale = not global_current or clean_item != frozen[identity]
        result[identity] = {'editorial': 'stale' if stale else ('accepted' if row['verdict']=='accept' else row['verdict']),
                            'issues': row['repair_requests'], 'remaining_limits': row['remaining_limits'],
                            'reviewer':report['actor_identity'], 'report_sha256':bench.sha(report_path.read_bytes()),
                            'mathematical_necessity_certified':False}
    return result


def prepare_repair(output: Path, identity: str, base: Path = ROUND) -> None:
    original = json.loads((base/'input.json').read_text(encoding='utf-8'))
    before = next((row for row in original['items'] if row['id']==identity),None)
    if before is None:
        raise ValueError('Repair target must occur in the selected frozen base round')
    current = payload(bench.curriculum.graph_items())
    after = next(row for row in current['items'] if row['id']==identity)
    if set(before)!=set(after) or {k for k in before if before[k]!=after[k]} != {'level','binding_sha256'}:
        raise ValueError('This repair changes only a provisional level and its binding')
    packet = {'schema_version':1, 'scope':REPAIR_SCOPE, 'author_identity':review.AUTHOR, 'base_round':base.name,
              'before':before, 'proposed_after':after, 'policy_sha256_lf':current['policy_sha256_lf'],
              'scorer_source':current['scorer_source'],
              'instruction':'Independently evaluate this exact provisional-level proposal and its minimality from the graph, question, source and scoring policy. Earlier reviewer verdicts and preferred delta classifications are omitted. No source graph, question, answer, score rule or empirical calibration changes. Accept, reject or request a narrower repair with evidence; do not edit earlier records.'}
    if output.exists():
        raise ValueError('Never overwrite an exact-proposal review input')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(bench.encoded(packet))


def apply_repair(items: list[dict], rows: dict, directory: Path = REPAIR_ROUND, base: Path = ROUND) -> dict:
    report_path = directory/'source-review.json'
    if not report_path.is_file():
        return rows
    packet_path = directory/'input.json'
    proposal = json.loads(packet_path.read_text(encoding='utf-8'))
    report = json.loads(report_path.read_text(encoding='utf-8'))
    original_path=base/'input.json'
    original = json.loads(original_path.read_text(encoding='utf-8'))
    prior = json.loads((base/'source-review.json').read_text(encoding='utf-8'))
    before, after = proposal['before'],proposal['proposed_after']
    identity = after['id']
    if (proposal['schema_version']!=1 or report['schema_version']!=1
            or proposal['scope']!=REPAIR_SCOPE or report['scope']!=REPAIR_SCOPE
            or proposal['author_identity']!=review.AUTHOR
            or proposal.get('base_round','graph-1')!=base.name
            or report.get('base_round','graph-1')!=base.name
            or prior['input_packet_sha256']!=bench.sha(original_path.read_bytes())
            or not isinstance(report['actor_identity'],str) or not report['actor_identity'].strip()
            or report['actor_identity'] in {review.AUTHOR,prior['actor_identity']}
            or report['input_packet_sha256']!=bench.sha(packet_path.read_bytes())
            or before!=next(row for row in original['items'] if row['id']==identity)
            or prior['items'][identity]['verdict']!='repair-required'
            or set(before)!=set(after)
            or {k for k in before if before[k]!=after[k]}!={'level','binding_sha256'}
            or report['proposed_binding_sha256']!=after['binding_sha256']
            or report['mathematical_necessity_certified'] is not False):
        raise ValueError('Difficulty repair must preserve the exact source/question/answer and independent evidence')
    for key in ('difficulty_checks','minimality_checks','remaining_limits'):
        if not isinstance(report[key],list) or not report[key] or not all(isinstance(s,str) and s.strip() for s in report[key]):
            raise ValueError('Exact repair review needs explicit level/minimality/boundary evidence')
    if report['verdict'] not in {'accept','repair-required','reject'} or not isinstance(report['repair_requests'],list):
        raise ValueError('Invalid difficulty-repair decision')
    if report['verdict']=='accept' and report['repair_requests']:
        raise ValueError('An unresolved repair cannot be accepted, even if its content is stale')
    current = payload(items)
    present = next((row for row in current['items'] if row['id']==identity),None)
    if (present!=after or current['policy_sha256_lf']!=proposal['policy_sha256_lf']
            or current['scorer_source']!=proposal['scorer_source']):
        rows[identity]={'editorial':'stale'}
    elif report['verdict']=='accept':
        rows[identity]={'editorial':'accepted-after-repair','issues':[],
                        'reviewer':report['actor_identity'],'report_sha256':bench.sha(report_path.read_bytes()),
                        'remaining_limits':report['remaining_limits'],'mathematical_necessity_certified':False}
    else:
        rows[identity]={'editorial':report['verdict'],'issues':report['repair_requests']}
    return rows


def summary(items: list[dict]) -> dict:
    if (CURRENT_ROUND/'source-review.json').is_file():
        packet=json.loads((CURRENT_ROUND/'input.json').read_text(encoding='utf-8'))
        report=json.loads((CURRENT_ROUND/'source-review.json').read_text(encoding='utf-8'))
        if packet.get('supersedes_rounds')!=SUPERSEDES or report.get('supersedes_rounds')!=SUPERSEDES:
            raise ValueError('Current whole-scope graph review needs explicit historical supersession')
        rows=apply_repair(items,statuses(items,CURRENT_ROUND),CURRENT_REPAIR_ROUND,CURRENT_ROUND)
        admission_round=CURRENT_ROUND.name
    else:
        rows=apply_repair(items,statuses(items))
        admission_round='historical-only; new policy/content requires fresh review'
    accepted = sum(row['editorial'] in {'accepted','accepted-after-repair'} for row in rows.values())
    return {'scope':SCOPE, 'accepted_tasks':accepted, 'total_tasks':len(items),
            'editorial_status':'complete-for-current-tasks' if items and accepted==len(items) else ('partial' if accepted else 'pending'),
            'difficulty_calibrated':False, 'model_performance_measured':False,
            'admission_round':admission_round,
            'repair_round':CURRENT_REPAIR_ROUND.name if (CURRENT_REPAIR_ROUND/'source-review.json').is_file() else None,
            'items':rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--repair-id')
    parser.add_argument('--base-round',choices=('graph-1','graph-4','graph-6','graph-7'),default='graph-1')
    args = parser.parse_args()
    if args.repair_id:
        prepare_repair(args.output,args.repair_id,ROUND.parent/args.base_round)
    else:
        prepare(args.output)
    print('Prepared structural review input; no independent verdict was created.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
