"""Fixed-target Lean runtime preparation. Never run submitted Lean on the host.

Official comparator is an external tool, not an ASTIS theorem or a new rubric.
Export and static tests do not certify native runtime acceptance or model scores.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'tools'))
import sog_bench as bench
import sog_bench_review as review

RUNTIME = ROOT/'benchmarks/samplingoptimisationgeometrybench/lean-runtime'
RUNTIME_TOOLS = {'comparator','lean4export','landrun','container.py','landrun-env',
                 'policy.json','bench_bounded_io.py'}
EXIT_CODES = {'accepted':0, 'proof-rejected':10, 'infrastructure-error':20,
              'resource-limit':30, 'invalid-submission':40}
PROXY_VARIABLES = ('HTTP_PROXY','HTTPS_PROXY','FTP_PROXY','ALL_PROXY','NO_PROXY',
                   'http_proxy','https_proxy','ftp_proxy','all_proxy','no_proxy')


def policy() -> dict:
    value = json.loads((RUNTIME/'policy.json').read_text(encoding='utf-8'))
    if value['schema_version'] != 2 or value['lean_toolchain'] != (ROOT/'lean-toolchain').read_text().strip():
        raise ValueError('Runtime requires the unchanged project toolchain')
    manifest = json.loads((ROOT/'lake-manifest.json').read_text())
    mathlib = next(p for p in manifest['packages'] if p['name']=='mathlib')
    if mathlib['rev'] != value['mathlib_commit']:
        raise ValueError('Runtime Mathlib pin is stale')
    if set(value['permitted_axioms']) != {'propext','Quot.sound','Classical.choice'}:
        raise ValueError('Runtime may not silently expand permitted axioms')
    for key in ('comparator_commit','lean4export_commit','landrun_commit'):
        if not re.fullmatch('[a-f0-9]{40}', value[key]):
            raise ValueError('External tools must use full commit identities')
    return value


def packet(core: dict) -> dict[str, bytes]:
    """Use the actual fixed task, not a new theorem or changed challenge meaning."""
    if not bench.has_lean(core):
        raise ValueError('Supporting-only Lean is not an aligned runtime task')
    p = policy()
    def named(source):
        result, count = re.subn(r'(?m)^example\b', 'theorem '+p['target_name'], source)
        if count != 1:
            raise ValueError('Expected exactly one canonical anonymous task')
        return result
    task, oracle = named(core['lean_task']), named(core['lean_reference'])
    slot = 'by\n  -- Replace this comment with your proof.\n'
    if not task.endswith(slot):
        raise ValueError('Unexpected canonical proof slot')
    # This is a verifier-only statement baseline, never a submitted/accepted proof.
    # Importing it cannot solve the task: its sorryAx is not permitted in solutions.
    challenge = task[:-len(slot)] + 'by\n  sorry\n'
    prompts = [row for row in bench.prompts([core]) if row['track']=='lean']
    files = {'agent/prompt.json':bench.encoded(prompts[0]),
             'agent/Solution.lean.txt':task.encode(),
             'verifier/Challenge.lean':challenge.encode(),
             'oracle/Solution.lean.txt':oracle.encode(),
             'verifier/config.json':bench.encoded({
                 'challenge_module':'Challenge', 'solution_module':'Solution',
                 'theorem_names':[p['target_name']], 'definition_names':[],
                 'permitted_axioms':p['permitted_axioms'], 'enable_nanoda':False})}
    for name in ('LICENSE','NOTICE','LICENSE_SCOPE.md'):
        files['agent/'+name]=(ROOT/name).read_bytes()
    descriptor = {k:core[k] for k in ('id','family','split','binding_sha256','imports','source_file')}
    descriptor.update(schema_version=1,track='lean',usage='public-dev; no model measurement',
        target_name=p['target_name'], policy_sha256=bench.sha(bench.encoded(p)),
        source_environment_sha256=bench.environment_digest([core]),
        files={name:bench.sha(data) for name,data in files.items()})
    files['operator.json'] = bench.encoded(descriptor)
    return files


def export(output: Path, task_ids: list[str] | None = None) -> list[str]:
    if output.exists():
        raise ValueError('Export requires a fresh directory; no overwrite')
    cores = bench.materialize()
    current = bench.editorial_review(cores)['items']
    selected = [c for c in cores if bench.has_lean(c) and review.accepted(current[c['id']])]
    if task_ids is not None:
        if not task_ids or len(task_ids)!=len(set(task_ids)) or not set(task_ids)<={c['id'] for c in selected}:
            raise ValueError('Select distinct, currently admitted aligned tasks')
        selected = [c for c in selected if c['id'] in task_ids]
    # Validate all records before creating any output.
    records = {c['id']:packet(c) for c in selected}
    output.mkdir(parents=True)
    for identity, files in records.items():
        for name, data in files.items():
            dest = output/identity/name
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(data)
    return list(records)


def local_imports(imports: list[str]) -> list[str]:
    """Only the declared ASTIS import closure; never a union with other targets."""
    found, todo = set(), list(imports)
    while todo:
        name = todo.pop()
        if not name.startswith('AutoSamplingTheory.') or name in found:
            continue
        if not re.fullmatch(r'[A-Za-z0-9_.]+',name):
            raise ValueError('Unsupported local module name')
        path = ROOT/(name.replace('.','/')+'.lean')
        if not path.is_file():
            raise ValueError('Missing declared ASTIS ancestor: '+name)
        found.add(name)
        todo.extend(re.findall(r'^import\s+([A-Za-z0-9_.]+)\s*$',bench.astis_site.sanitize_lean(path.read_text(encoding='utf-8')),re.M))
    return sorted(found)


def offline_manifest(prefix: str = '/deps/packages') -> dict:
    """Path projection of the SAME pinned snapshots; no Git/credentials at runtime.

    Keep the original manifest separately for provenance. A readonly snapshot
    without .git cannot satisfy Lake's Git materializer, which would otherwise
    try to fetch or replace it. This changes location, not mathematical APIs.
    """
    data=json.loads((ROOT/'lake-manifest.json').read_text())
    rows=[]
    for entry in data['packages']:
        if entry['type']!='git' or entry.get('subDir') is not None:
            raise ValueError('Only the current flat pinned Git package graph is supported')
        row={k:entry[k] for k in ('name','scope','inherited','configFile','manifestFile')}
        row.update(type='path',dir=prefix.rstrip('/')+'/'+entry['name'])
        rows.append(row)
    return {**data,'packages':rows}


def offline_lakefile(prefix: str = '/deps/packages') -> str:
    source=(ROOT/'lakefile.lean').read_text()
    replacement='require mathlib from '+json.dumps(prefix.rstrip('/')+'/mathlib')
    source,count=re.subn(r'require mathlib from git\s+"https://github.com/leanprover-community/mathlib4.git" @ "v4.33.0"',replacement,source)
    if count!=1:raise ValueError('Unexpected project Lake configuration')
    return source+'\nlean_lib Challenge\nlean_lib Solution\n'


def checked_packet(task: Path) -> dict:
    desc = json.loads((task/'operator.json').read_text())
    if desc['policy_sha256'] != bench.sha(bench.encoded(policy())):
        raise ValueError('Stale runtime policy')
    for name,digest in desc['files'].items():
        path = Path(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name or bench.sha((task/path).read_bytes())!=digest:
            raise ValueError('Task artifact drift or unsafe path: '+name)
    cores = bench.materialize()
    core = next((c for c in cores if c['id']==desc['id']),None)
    if core is None or packet(core)['operator.json'] != (task/'operator.json').read_bytes():
        raise ValueError('Task/source binding drift')
    state = bench.editorial_review([core])['items'][core['id']]
    if not review.accepted(state):
        raise ValueError('Task no longer admitted')
    return core


def owned_artifacts(modules: list[str]) -> dict[str, Path]:
    """Complete Lake artifacts for exactly the allowed owned module closure.

    Lean4.33's Module.checkArtifactsExist requires C output as well as oleans.
    Dropping IR/C files silently turns cache reuse into expensive recompilation.
    """
    found={}
    for module in modules:
        rel=module.replace('.','/')
        lib=ROOT/'.lake/build/lib/lean'/rel
        ir=ROOT/'.lake/build/ir'/rel
        required=[lib.with_suffix(ext) for ext in ('.olean','.ilean','.trace')]+[ir.with_suffix('.c')]
        if not all(path.is_file() for path in required):
            raise ValueError('Build the complete trusted module artifacts first: '+module)
        for stem in (lib,ir):
            for path in stem.parent.glob(stem.name+'.*'):
                if path.is_file():found[path.relative_to(ROOT/'.lake/build').as_posix()]=path
    return found


def stage(task: Path, output: Path) -> None:
    """Small per-task owning-library snapshot; dependencies are mounted read-only."""
    if output.exists():
        raise ValueError('Stage requires a fresh directory')
    core = checked_packet(task)
    modules = local_imports(core['imports'])
    target_module = core['source_file'][:-5].replace('/','.')
    if target_module in modules:
        raise ValueError('Target owner is in its permitted ancestor closure')
    artifacts=owned_artifacts(modules)
    output.mkdir(parents=True)
    (output/'owned-build').mkdir()
    for module in modules:
        rel=module.replace('.','/')+'.lean';dest=output/'project'/rel
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/rel,dest)
        dest.chmod(dest.stat().st_mode|0o444)
    for rel,source in artifacts.items():
        dest=output/'owned-build'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
        dest.chmod(dest.stat().st_mode|0o444)
    for name in ('Challenge.lean','config.json'):
        shutil.copyfile(task/'verifier'/name,output/name)
    # Same trusted package graph via credential-free readonly offline snapshots.
    (output/'project').mkdir(exist_ok=True)
    (output/'project/lakefile.lean').write_text(offline_lakefile(),encoding='utf-8',newline='\n')
    (output/'project/lake-manifest.json').write_bytes(bench.encoded(offline_manifest()))
    shutil.copyfile(ROOT/'lake-manifest.json',output/'original-lake-manifest.json')
    shutil.copyfile(ROOT/'lean-toolchain',output/'project/lean-toolchain')
    for name in ('LICENSE','NOTICE','LICENSE_SCOPE.md'):
        shutil.copyfile(ROOT/name,output/name)
    (output/'stage.json').write_bytes(bench.encoded({'id':core['id'],'binding_sha256':core['binding_sha256'],
        'owned_ancestor_modules':modules,'target_module_absent':True,'oracle_included':False,
        'files':{path.relative_to(output).as_posix():bench.sha(path.read_bytes())
                 for path in sorted(output.rglob('*')) if path.is_file()}}))


def docker_command(*, image: str, name: str, stage_dir: Path, submission: Path,
                   packages: Path, toolchain: Path, tools_dir: Path) -> list[str]:
    """Argv only. No shell strings, Docker socket, host home, or writable bind."""
    if not re.fullmatch(r'sha256:[0-9a-f]{64}',image) or not re.fullmatch(r'sog-lean-[a-z0-9-]+',name):
        raise ValueError('Require immutable image ID and generated container name')
    p=policy();limits=p['limits']
    argv=['docker','run','--name',name,'--network=none','--read-only','--user=1000:1000',
        '--cap-drop=ALL','--security-opt=no-new-privileges:true','--pids-limit='+str(limits['pids']),
        '--memory='+str(limits['memory_mb'])+'m','--memory-swap='+str(limits['memory_mb'])+'m',
        '--cpus='+str(limits['cpus']),'--ipc=none','--log-driver=none',
        '--ulimit','nofile=256:256','--ulimit','core=0:0',
        '--tmpfs','/work:rw,nosuid,nodev,size='+str(limits['scratch_mb'])+'m,uid=1000,gid=1000',
        '--tmpfs','/tmp:rw,noexec,nosuid,nodev,size=64m,uid=1000,gid=1000']
    # Docker CLI may inject configured proxy credentials automatically. Network
    # isolation does NOT make those strings safe to expose to submitted #eval.
    for variable in PROXY_VARIABLES:argv.extend(['--env',variable+'='])
    for source,dest in ((stage_dir,'/task'),(submission,'/input/Solution.lean'),
                        (packages,'/deps/packages'),(toolchain,'/opt/lean'),(tools_dir,'/opt/judge')):
        source=source.resolve(strict=True)
        if any(c in str(source) for c in (',','\n','\r')):
            raise ValueError('Unsafe Docker mount path')
        argv.extend(['--mount','type=bind,source='+str(source)+',target='+dest+',readonly'])
    return argv+[image,'python3','-I','/opt/judge/container.py']


def parse_control(raw: bytes, *, diagnostic_chunks: list[bytes] | None = None) -> tuple[dict | None,str | None]:
    """Only supervisor-framed JSON; child stdout is escaped diagnostic data."""
    phase=None;result=None;malformed=False;diagnostic_size=0
    cap=policy()['limits']['diagnostic_bytes']
    for line in raw.splitlines():
        try: value=json.loads(line)
        except (ValueError,UnicodeError): malformed=True;continue
        if not isinstance(value,dict):malformed=True;continue
        if value.get('kind')=='runtime-phase':
            next_phase=value.get('phase')
            if result is not None or (phase,next_phase) not in ((None,'challenge-preflight'),('challenge-preflight','verifying-solution')):
                malformed=True
            phase=next_phase
        elif value.get('kind')=='runtime-diagnostic':
            try:
                if result is not None or value.get('phase')!=phase or phase not in ('challenge-preflight','verifying-solution'):
                    raise ValueError('Diagnostic outside an active phase')
                chunk=base64.b64decode(value['chunk_b64'],validate=True)
                diagnostic_size+=len(chunk)
                if diagnostic_size>cap:raise ValueError('Raw diagnostic cap exceeded')
                if diagnostic_chunks is not None:diagnostic_chunks.append(chunk)
            except (ValueError,KeyError,TypeError):malformed=True
        elif result is None:result=value
        else:malformed=True
    if result and result.get('kind')=='fixed-target-comparator' and phase!='verifying-solution':malformed=True
    return (None if malformed else result),phase


def classify(returncode: int, native, state, interruption, phase=None) -> str:
    """Malformed/missing infrastructure evidence never becomes proof rejection."""
    if not isinstance(state,dict) or not state.get('StartedAt') or str(state['StartedAt']).startswith('0001-'):
        return 'infrastructure-error'
    if state.get('OOMKilled') is True or interruption:
        return 'resource-limit' if phase=='verifying-solution' else 'infrastructure-error'
    if not isinstance(native,dict) or native.get('kind')!='fixed-target-comparator':
        return 'infrastructure-error'
    if returncode==30 and state.get('ExitCode')==30 and native.get('diagnostic_limit') is True:
        return 'resource-limit'
    comparator_exit=native.get('comparator_exit')
    if type(comparator_exit) is not int or state.get('ExitCode')!=returncode:
        return 'infrastructure-error'
    if returncode==0 and comparator_exit==0 and native.get('accepted') is True:
        return 'accepted'
    if returncode==10 and comparator_exit!=0 and native.get('accepted') is False:
        return 'proof-rejected'
    return 'infrastructure-error'


def check_runtime(directory: Path) -> dict:
    """Operator-prepared receipt, unchanged tools and source; not attestation."""
    receipt=json.loads((directory/'preparation.json').read_text())
    if receipt['policy']!=policy() or receipt['image_id']!=(directory/'image-id').read_text().strip():
        raise ValueError('Runtime policy/image drift')
    actual={path.name for path in (directory/'tools').iterdir()}
    if set(receipt['tools'])!=RUNTIME_TOOLS or actual!=RUNTIME_TOOLS:
        raise ValueError('Runtime tool inventory is incomplete or contains unlisted files')
    for name,digest in receipt['tools'].items():
        if not re.fullmatch(r'[A-Za-z0-9_.-]+',name) or bench.sha((directory/'tools'/name).read_bytes())!=digest:
            raise ValueError('Runtime tool drift')
    for name in ('container.py','landrun-env','policy.json'):
        if (directory/'tools'/name).read_bytes()!=(RUNTIME/name).read_bytes():
            raise ValueError('Runtime source does not match this verifier')
    if (directory/'tools/bench_bounded_io.py').read_bytes()!=(ROOT/'benchmarks/samplingoptimisationgeometrybench/harbor/bench_bounded_io.py').read_bytes():
        raise ValueError('Runtime bounded-input reader is stale')
    return receipt


def read_submission(submission: Path, limit: int) -> tuple[bytes | None, str | None]:
    """Bound even invalid input; never hash/read an entire oversized answer."""
    sys.path.insert(0,str(ROOT/'benchmarks/samplingoptimisationgeometrybench/harbor'))
    from bench_bounded_io import InputRejected, read_bounded
    try:
        raw=read_bounded(submission,limit)
        raw.decode('utf-8',errors='strict')
        return raw,None
    except InputRejected as error:
        return None,str(error)
    except UnicodeDecodeError:
        return None,'invalid-utf8'
    except FileNotFoundError:
        return None,'missing-file'
    except OSError as error:
        return None,'input-os-error-'+str(error.errno)


def run_submission(*, task: Path, stage_dir: Path, submission: Path,
                   runtime: Path, output: Path) -> dict:
    """Fresh Linux container per call; bounded I/O; no host execution fallback.

    This primitive exposes compiler diagnostics for an agent's proof-repair loop.
    It is not a model-run recorder or a benchmark score. Archive trajectories and
    final attempts separately before making a performance claim.
    """
    if sys.platform!='linux' or shutil.which('docker') is None:
        raise RuntimeError('Linux Docker is required; never execute submitted Lean on the host')
    if output.exists(): raise ValueError('A run evidence directory cannot be overwritten')
    check_runtime(runtime)
    core=checked_packet(task)
    desc=json.loads((stage_dir/'stage.json').read_text())
    if desc['binding_sha256']!=core['binding_sha256'] or desc['id']!=core['id']:
        raise ValueError('Stage is bound to a different task')
    for name,digest in desc['files'].items():
        path=Path(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name or bench.sha((stage_dir/path).read_bytes())!=digest:
            raise ValueError('Trusted stage drift: '+name)
    for name in ('Challenge.lean','config.json'):
        if (stage_dir/name).read_bytes()!=(task/'verifier'/name).read_bytes():
            raise ValueError('Trusted challenge/config does not match the current task')
    # Stage and runtime are operator-controlled artifacts, NOT agent directories.
    # The bounded reader is reused, rather than reading a symlink/FIFO or an
    # unbounded file before transfer to the isolated process.
    p=policy();raw,rejection=read_submission(submission,p['limits']['submission_bytes'])
    output.mkdir(parents=True)
    if rejection is not None:
        # Retain the selected attempt without claiming execution, acceptance or
        # a digest of bytes we intentionally did NOT read. Collection/runtime
        # failures must not silently disappear from a model-run denominator.
        report={'schema_version':1,'id':core['id'],'binding_sha256':core['binding_sha256'],
            'task_packet_sha256':bench.sha((task/'operator.json').read_bytes()),
            'policy_sha256':bench.sha(bench.encoded(p)),
            'runtime_receipt_sha256':bench.sha((runtime/'preparation.json').read_bytes()),
            'verifier_source_sha256_lf':bench.text_hash(Path(__file__)),
            'submission_sha256':None,'kind':'invalid-submission','reason':rejection,
            'container_started':False,'model_measurement':False,
            'scoring_scope':'One invalid verification-call input; not a model-run score.'}
        (output/'result.json').write_bytes(bench.encoded(report))
        return report
    assert raw is not None
    frozen=output/'submission.txt';frozen.write_bytes(raw);frozen.chmod(0o444)
    image=(runtime/'image-id').read_text().strip()
    name='sog-lean-'+uuid.uuid4().hex
    argv=docker_command(image=image,name=name,stage_dir=stage_dir,submission=frozen,
        packages=runtime/'packages',toolchain=runtime/'toolchain',tools_dir=runtime/'tools')
    started=time.monotonic();data=bytearray();interrupted=None
    proc=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    try:
        os.set_blocking(proc.stdout.fileno(),False)
        with selectors.DefaultSelector() as selector:
            selector.register(proc.stdout,selectors.EVENT_READ)
            while True:
                if time.monotonic()-started>p['limits']['wall_seconds']:
                    interrupted='wall-time-limit';break
                events=selector.select(timeout=.25)
                if events:
                    chunk=os.read(proc.stdout.fileno(),min(4096,p['limits']['transport_bytes']+1-len(data)))
                    if not chunk: break
                    data.extend(chunk)
                    if len(data)>p['limits']['transport_bytes']:
                        interrupted='output-limit';break
                elif proc.poll() is not None:
                    # Drain remaining pipe bytes rather than losing a final report.
                    continue
        if interrupted:
            subprocess.run(['docker','kill',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
            if proc.poll() is None:proc.kill()
        proc.wait(timeout=15)
        inspection=subprocess.run(['docker','inspect',name],capture_output=True,timeout=10)
        state=json.loads(inspection.stdout)[0]['State'] if inspection.returncode==0 else None
    finally:
        if proc.poll() is None:proc.kill();proc.wait(timeout=10)
        proc.stdout.close()
        # Only this freshly generated, exact container identity is removed.
        subprocess.run(['docker','rm','--force',name],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=10)
    (output/'runtime-output.bin').write_bytes(bytes(data[:p['limits']['transport_bytes']]))
    chunks=[];native,phase=parse_control(bytes(data),diagnostic_chunks=chunks)
    diagnostic=b''.join(chunks)[:p['limits']['diagnostic_bytes']]
    (output/'compiler-diagnostic.bin').write_bytes(diagnostic)
    kind=classify(proc.returncode,native,state,interrupted,phase)
    report={'schema_version':1,'id':core['id'],'binding_sha256':core['binding_sha256'],
        'submission_sha256':bench.sha(raw),'policy_sha256':bench.sha(bench.encoded(p)),
        'task_packet_sha256':bench.sha((task/'operator.json').read_bytes()),
        'runtime_receipt_sha256':bench.sha((runtime/'preparation.json').read_bytes()),
        'verifier_source_sha256_lf':bench.text_hash(Path(__file__)),
        'compiler_diagnostic_sha256':bench.sha(diagnostic),
        'image_id':image,'wall_seconds':time.monotonic()-started,'container_state':state,
        'kind':kind,'interruption':interrupted,'runtime_phase':phase,'native':native,'model_measurement':False,
        'scoring_scope':'One submission-verification call, not a recorded model attempt or suite score.'}
    (output/'result.json').write_bytes(bench.encoded(report))
    return report


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='cmd',required=True)
    x=sub.add_parser('export');x.add_argument('--output',type=Path,required=True);x.add_argument('--task-id',action='append')
    x=sub.add_parser('stage');x.add_argument('--task',type=Path,required=True);x.add_argument('--output',type=Path,required=True)
    x=sub.add_parser('run');x.add_argument('--task',type=Path,required=True);x.add_argument('--stage',type=Path,required=True)
    x.add_argument('--runtime',type=Path,required=True);x.add_argument('--submission',type=Path,required=True);x.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.cmd=='export': print(json.dumps({'exported':export(args.output,args.task_id),'native_acceptance':False}))
    elif args.cmd=='stage': stage(args.task,args.output)
    else:
        result=run_submission(task=args.task,stage_dir=args.stage,submission=args.submission,runtime=args.runtime,output=args.output)
        print(json.dumps(result))
        raise SystemExit(EXIT_CODES[result['kind']])


if __name__=='__main__': main()
