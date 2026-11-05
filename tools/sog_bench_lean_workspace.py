"""Finite fixed-target compiler tool. No provider calls, shell tool or host Lean.

The operator owns this directory and passes ONLY agent/ plus returned feedback
to an agent. The agent sends bounded JSON {action, source}; it cannot choose a
task, command, mount, verifier or output path. This is not a public web service,
authenticated model provenance, suite score or security certification.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
import sog_bench_lean as runtime

REQUEST_BYTES=524288
FEEDBACK_BYTES=8192


def now():
    return datetime.now(timezone.utc).isoformat()


def write_new(path: Path, value: dict):
    with path.open('xb') as stream:stream.write(runtime.bench.encoded(value))


def json_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('Duplicate JSON key')
        result[key]=value
    return result


def read_request(path: Path) -> dict:
    raw,reason=runtime.read_submission(path,REQUEST_BYTES)
    if reason is not None:raise ValueError('Rejected request envelope: '+reason)
    result=json.loads(raw,object_pairs_hook=json_object)
    if not isinstance(result,dict):raise ValueError('Request must be a JSON object')
    return result


@contextmanager
def exclusive(directory: Path):
    # O_EXCL: concurrent calls cannot both reserve the first final submission.
    # An interrupted operator leaves the lock for manual evidence inspection;
    # there is deliberately no automatic retry or stale-lock deletion command.
    lock=directory/'operation.lock'
    with lock.open('xb') as stream:stream.write(b'operator operation in progress\n')
    try:yield
    finally:lock.unlink()


def start(*, task: Path, stage: Path, prepared: Path, output: Path,
          provenance: dict, max_checks: int=4) -> dict:
    if sys.platform!='linux' or shutil.which('docker') is None:
        raise RuntimeError('An actual Linux Docker runtime is required; no host fallback')
    if output.exists():raise ValueError('Workspace requires a fresh operator directory')
    if type(max_checks) is not int or not 0<=max_checks<=8:raise ValueError('Declare between0 and8 check calls')
    if not isinstance(provenance,dict) or provenance.get('kind') not in {
            'controlled-software-fixture','declared-model-run'}:
        raise ValueError('Explicitly distinguish a fixture from operator-declared model provenance')
    if provenance['kind']=='declared-model-run':
        for key in ('provider','model','model_version','retrieval_profile'):
            if not isinstance(provenance.get(key),str) or not provenance[key].strip():
                raise ValueError('Record actual provider/model/version/retrieval profile')
        if (not isinstance(provenance.get('tools'),list)
                or not all(isinstance(t,str) for t in provenance['tools'])
                or not isinstance(provenance.get('decoding'),dict)):
            raise ValueError('Record available tools and decoding settings')
        if 'seed' not in provenance or not (provenance['seed'] is None or type(provenance['seed']) is int):
            raise ValueError('Record seed or null')
    core=runtime.checked_packet(task);runtime.check_runtime(prepared)
    desc=json.loads((stage/'stage.json').read_text())
    if desc['id']!=core['id'] or desc['binding_sha256']!=core['binding_sha256']:
        raise ValueError('Stage/task binding mismatch')
    manifest={'schema_version':1,'kind':'fixed-target-compiler-workspace','created_at':now(),
        'id':core['id'],'binding_sha256':core['binding_sha256'],'denominator':1,
        'attempt_policy':'first-final-after-bounded-checks','max_checks':max_checks,
        'paths':{'task':str(task.resolve()),'stage':str(stage.resolve()),'prepared':str(prepared.resolve())},
        'task_packet_sha256':runtime.bench.sha((task/'operator.json').read_bytes()),
        'runtime_receipt_sha256':runtime.bench.sha((prepared/'preparation.json').read_bytes()),
        'workspace_source_sha256_lf':runtime.bench.text_hash(Path(__file__)),
        'verifier_source_sha256_lf':runtime.bench.text_hash(Path(runtime.__file__)),
        'provenance':provenance,'provenance_authenticated':False,'model_measurement':False,
        'scope':'Single selected public-dev target; check calls are tools, not additional final attempts. Operator provenance is not authenticated.'}
    output.mkdir(parents=True)
    (output/'actions').mkdir()
    # Never expose the operator packet, source oracle, receipts or private paths
    # as agent context. The same canonical agent view is reused without gold.
    shutil.copytree(task/'agent',output/'agent')
    write_new(output/'session.json',manifest)
    return manifest


def history(directory: Path) -> tuple[dict,list[dict]]:
    raw=(directory/'session.json').read_bytes();manifest=json.loads(raw)
    if manifest.get('kind')!='fixed-target-compiler-workspace' or manifest.get('schema_version')!=1:
        raise ValueError('Unsupported workspace manifest')
    events=[]
    for index,path in enumerate(sorted((directory/'actions').iterdir()),1):
        if not path.is_dir() or path.name!=f'{index:04d}':raise ValueError('Nonsequential action evidence')
        event=json.loads((path/'event.json').read_bytes())
        if event['session_sha256']!=runtime.bench.sha(raw) or event['sequence']!=index:
            raise ValueError('Action/session drift')
        source=path/'source.txt'
        if event['source_sha256'] is not None and runtime.bench.sha(source.read_bytes())!=event['source_sha256']:
            raise ValueError('Submitted source drift')
        observation=path/'observation.json'
        if observation.exists():
            observation=json.loads(observation.read_bytes())
            report=(path/'verification/result.json').read_bytes()
            if (observation['event_sha256']!=runtime.bench.sha((path/'event.json').read_bytes())
                    or observation['result_sha256']!=runtime.bench.sha(report)):
                raise ValueError('Observation/result drift')
            result=json.loads(report)
            if result['kind']!=observation['kind']:raise ValueError('Observation/result mismatch')
            event={**event,'result':result}
        else:event={**event,'result':None}
        events.append(event)
    actions=[event['action'] for event in events]
    if (any(a not in {'check','submit'} for a in actions) or actions.count('check')>manifest['max_checks']
            or actions.count('submit')>1 or ('submit' in actions and actions[-1]!='submit')):
        raise ValueError('Invalid action history')
    return manifest,events


def act(directory: Path, request: dict) -> dict:
    if (not isinstance(request,dict) or set(request)-{'action','source'}
            or request.get('action') not in {'check','submit'}):
        raise ValueError('Only {action: check|submit, source: UTF8 Lean text} is supported')
    with exclusive(directory):
        manifest,events=history(directory)
        if (directory/'completion.json').exists() or any(e['action']=='submit' for e in events):
            raise ValueError('The first final submission has already sealed this workspace')
        if any(e['result'] is None for e in events):raise ValueError('Inspect interrupted evidence; never silently retry')
        if request['action']=='check' and len(events)>=manifest['max_checks']:
            raise ValueError('Declared check-call budget exhausted')
        if (runtime.bench.text_hash(Path(__file__))!=manifest['workspace_source_sha256_lf']
                or runtime.bench.text_hash(Path(runtime.__file__))!=manifest['verifier_source_sha256_lf']):
            raise ValueError('Workspace implementation drift; keep old evidence and start a new declared run')
        paths={k:Path(v) for k,v in manifest['paths'].items()}
        if (runtime.bench.sha((paths['task']/'operator.json').read_bytes())!=manifest['task_packet_sha256']
                or runtime.bench.sha((paths['prepared']/'preparation.json').read_bytes())!=manifest['runtime_receipt_sha256']):
            raise ValueError('Selected packet/runtime drift')
        sequence=len(events)+1;action_dir=directory/'actions'/f'{sequence:04d}';action_dir.mkdir()
        source=request.get('source');reason=None;raw=None
        if not isinstance(source,str):reason='missing-or-nontext-source'
        elif len(source)>runtime.policy()['limits']['submission_bytes']:reason='too-large'
        else:
            try:raw=source.encode('utf-8',errors='strict')
            except UnicodeEncodeError:reason='invalid-utf8'
        if raw is not None and len(raw)>runtime.policy()['limits']['submission_bytes']:
            reason='too-large';raw=None
        event={'sequence':sequence,'action':request['action'],'received_at':now(),
            'session_sha256':runtime.bench.sha((directory/'session.json').read_bytes()),
            'source_sha256':runtime.bench.sha(raw) if raw is not None else None,
            'input_rejection':reason}
        if raw is not None:(action_dir/'source.txt').write_bytes(raw)
        # Reserve BEFORE execution: a timeout, crash or invalid final cannot be
        # replaced with a more favorable "first" final submission.
        write_new(action_dir/'event.json',event)
        if reason is not None:
            (action_dir/'verification').mkdir()
            report={'kind':'invalid-submission','reason':reason,'id':manifest['id'],
                'binding_sha256':manifest['binding_sha256'],'container_started':False,'model_measurement':False}
            write_new(action_dir/'verification/result.json',report)
        else:
            report=runtime.run_submission(task=paths['task'],stage_dir=paths['stage'],
                runtime=paths['prepared'],submission=action_dir/'source.txt',output=action_dir/'verification')
        observation={'kind':report['kind'],'completed_at':now(),
            'event_sha256':runtime.bench.sha((action_dir/'event.json').read_bytes()),
            'result_sha256':runtime.bench.sha((action_dir/'verification/result.json').read_bytes())}
        write_new(action_dir/'observation.json',observation)
        diagnostic=action_dir/'verification/compiler-diagnostic.bin'
        feedback=diagnostic.read_bytes() if diagnostic.exists() else b''
        return {'sequence':sequence,'action':request['action'],'kind':report['kind'],
            'reason':report.get('reason'),'diagnostic':feedback[:FEEDBACK_BYTES].decode('utf-8',errors='replace'),
            'diagnostic_truncated':len(feedback)>FEEDBACK_BYTES,'final':request['action']=='submit',
            'runtime_phase':report.get('runtime_phase'),'interruption':report.get('interruption'),
            'model_measurement':False}


def close(directory: Path) -> dict:
    with exclusive(directory):
        manifest,events=history(directory)
        final=next((e for e in events if e['action']=='submit'),None)
        interrupted=any(e['result'] is None for e in events)
        outcome=('infrastructure-error' if interrupted else final['result']['kind'] if final else 'no-final-submission')
        result={'schema_version':1,'kind':'fixed-target-workspace-completion','closed_at':now(),
            'session_sha256':runtime.bench.sha((directory/'session.json').read_bytes()),
            'id':manifest['id'],'denominator':1,'check_calls':sum(e['action']=='check' for e in events),
            'final_submissions':int(final is not None),'final_outcome':outcome,
            'final_accepted':outcome=='accepted','interrupted':interrupted,
            'provenance_authenticated':False,'model_measurement':False,
            'scope':'One operator-recorded trajectory, not a suite/model score. Invalid/missing finals remain selected; infrastructure errors are distinct.'}
        write_new(directory/'completion.json',result)
        return result


def start_suite(*, tasks: Path, stages: Path, prepared: Path, output: Path,
                task_ids: list[str], provenance: dict, max_checks: int=4) -> dict:
    """Freeze ALL selected targets before the first tool call, not survivors."""
    if output.exists():raise ValueError('Suite requires a fresh operator directory')
    if not task_ids or len(set(task_ids))!=len(task_ids):raise ValueError('Select distinct admitted task identities')
    # Resolve identities through the canonical admitted packets, never use an
    # unchecked agent-provided identity as a filesystem path.
    admitted={p.name:p for p in tasks.iterdir() if p.is_dir()}
    if set(task_ids)-set(admitted):raise ValueError('Unknown task selection')
    selected=[]
    for identity in task_ids:
        core=runtime.checked_packet(admitted[identity])
        if core['id']!=identity:raise ValueError('Packet directory/identity mismatch')
        selected.append({k:core[k] for k in ('id','family','split','binding_sha256')})
    runtime.check_runtime(prepared)
    manifest={'schema_version':1,'kind':'fixed-target-workspace-suite','created_at':now(),
        'selected':selected,'denominator':len(selected),'provenance':provenance,
        'max_checks_per_target':max_checks,'attempt_policy':'first-final-after-bounded-checks',
        'model_measurement':False,'provenance_authenticated':False,
        'scope':'Frozen selected public-dev targets, including missing/invalid/unstarted/infra outcomes. No model score.'}
    output.mkdir(parents=True);(output/'tasks').mkdir()
    # If later initialization fails, this immutable denominator already exists.
    # Do not delete the partial suite or quietly create a survivors-only run.
    write_new(output/'suite.json',manifest)
    for row in selected:
        identity=row['id']
        start(task=admitted[identity],stage=stages/identity,prepared=prepared,
            output=output/'tasks'/identity,provenance=provenance,max_checks=max_checks)
    return manifest


def suite_status(directory: Path, *, finish: bool=False) -> dict:
    def collect():
        raw=(directory/'suite.json').read_bytes();manifest=json.loads(raw)
        if manifest.get('kind')!='fixed-target-workspace-suite' or manifest.get('schema_version')!=1:
            raise ValueError('Unsupported suite manifest')
        selected=manifest['selected'];identities=[row['id'] for row in selected]
        if len(set(identities))!=len(selected) or manifest['denominator']!=len(selected):
            raise ValueError('Invalid frozen suite selection')
        rows=[]
        for selected_row in selected:
            identity=selected_row['id'];task_dir=directory/'tasks'/identity
            # Recheck trusted frozen identities before following any paths.
            if not isinstance(identity,str) or not identity.startswith('sogb-') or not identity[5:].isdigit():
                raise ValueError('Unsafe suite identity')
            if not (task_dir/'session.json').is_file():
                rows.append({'id':identity,'outcome':'initialization-error','completion_sha256':None})
                continue
            session,events=history(task_dir)
            if (session['id']!=identity or session['binding_sha256']!=selected_row['binding_sha256']
                    or session['provenance']!=manifest['provenance']
                    or session['max_checks']!=manifest['max_checks_per_target']):
                raise ValueError('Suite/child binding or declared policy drift')
            completion=task_dir/'completion.json'
            if finish and not completion.exists():
                close(task_dir)
                session,events=history(task_dir)
            if completion.exists():
                value=json.loads(completion.read_bytes())
                if (value['session_sha256']!=runtime.bench.sha((task_dir/'session.json').read_bytes())
                        or value['denominator']!=1):
                    raise ValueError('Child completion/session drift')
                final=next((e for e in events if e['action']=='submit'),None)
                expected=('infrastructure-error' if any(e['result'] is None for e in events)
                    else final['result']['kind'] if final else 'no-final-submission')
                if value['final_outcome']!=expected or value['final_accepted']!=(expected=='accepted'):
                    raise ValueError('Child completion/history drift')
                rows.append({'id':identity,'outcome':expected,'completion_sha256':runtime.bench.sha(completion.read_bytes())})
            else:rows.append({'id':identity,'outcome':'unfinished','completion_sha256':None})
        counts={kind:sum(row['outcome']==kind for row in rows) for kind in sorted({row['outcome'] for row in rows})}
        result={'schema_version':1,'kind':'fixed-target-suite-accounting',
            'suite_sha256':runtime.bench.sha(raw),'denominator':len(selected),'results':rows,'outcome_counts':counts,
            'closed':finish or (directory/'accounting.json').exists(),
            'model_measurement':False,'provenance_authenticated':False,
            'scope':'Every preselected target retained; infrastructure errors remain distinct/unscored. Not a model score or authenticated trajectory.'}
        accounting=directory/'accounting.json'
        if accounting.exists() and json.loads(accounting.read_bytes())!=result:
            raise ValueError('Closed suite accounting/evidence drift')
        return result
    if finish:
        with exclusive(directory):
            if (directory/'accounting.json').exists():raise ValueError('Never overwrite closed suite accounting')
            result=collect();write_new(directory/'accounting.json',result);return result
    return collect()


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='cmd',required=True)
    p=sub.add_parser('start');p.add_argument('--task',type=Path,required=True);p.add_argument('--stage',type=Path,required=True)
    p.add_argument('--runtime',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--provenance',type=Path,required=True);p.add_argument('--max-checks',type=int,default=4)
    p=sub.add_parser('act');p.add_argument('--workspace',type=Path,required=True);p.add_argument('--request',type=Path,required=True)
    for command in ('close','status'):
        p=sub.add_parser(command);p.add_argument('--workspace',type=Path,required=True)
    p=sub.add_parser('suite-start');p.add_argument('--tasks',type=Path,required=True);p.add_argument('--stages',type=Path,required=True)
    p.add_argument('--runtime',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--task-id',action='append',required=True);p.add_argument('--provenance',type=Path,required=True)
    p.add_argument('--max-checks',type=int,default=4)
    for command in ('suite-close','suite-status'):
        p=sub.add_parser(command);p.add_argument('--suite',type=Path,required=True)
    args=parser.parse_args()
    if args.cmd=='suite-start':
        start_suite(tasks=args.tasks,stages=args.stages,prepared=args.runtime,output=args.output,
            task_ids=args.task_id,provenance=read_request(args.provenance),max_checks=args.max_checks)
        result={'kind':'suite-created','selected_task_ids':args.task_id,'model_measurement':False}
    elif args.cmd in {'suite-close','suite-status'}:result=suite_status(args.suite,finish=args.cmd=='suite-close')
    elif args.cmd=='start':
        start(task=args.task,stage=args.stage,prepared=args.runtime,output=args.output,
            provenance=read_request(args.provenance),max_checks=args.max_checks)
        result={'kind':'workspace-created','agent_view':str(args.output/'agent'),'model_measurement':False}
    elif args.cmd=='act':result=act(args.workspace,read_request(args.request))
    elif args.cmd=='close':result=close(args.workspace)
    else:
        manifest,events=history(args.workspace)
        result={'id':manifest['id'],'max_checks':manifest['max_checks'],'events':events,
            'closed':(args.workspace/'completion.json').exists(),'model_measurement':False}
    print(json.dumps(result,ensure_ascii=False))


if __name__=='__main__':main()
