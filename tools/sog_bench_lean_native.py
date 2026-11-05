"""Prepare trusted tools and run controlled Linux Docker fixtures, not models."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import stat

sys.path.insert(0,str(Path(__file__).resolve().parent))
import sog_bench_lean as runtime


def command(argv,cwd=None):
    print(json.dumps({'trusted_preparation_command':[str(a) for a in argv]}),flush=True)
    subprocess.run([str(a) for a in argv],cwd=cwd,check=True,timeout=1200)


def clone(url,commit,dest):
    if not dest.exists():
        command(['git','clone','--filter=blob:none','--no-checkout',url,dest])
        command(['git','checkout','--detach',commit],dest)
    actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=dest,text=True).strip()
    if actual!=commit: raise ValueError('External checkout pin mismatch: '+str(dest))


def public_cache_file(source,destination,stats=None):
    """Do not chmod a shared inode: copy private-mode PUBLIC build artifacts.

    Lake's trace reader uses ordinary IO.FS.readFile. CI-created 0600 files
    cannot be read by container UID1000. Keep the original cache untouched;
    duplicate only these small files and make the snapshot readable.
    """
    mode=stat.S_IMODE(os.stat(source).st_mode)
    if not mode & stat.S_IROTH:
        shutil.copy2(source,destination)
        os.chmod(destination,mode|0o444)
        if stats is not None:
            stats['copied_for_read']+=1
            if len(stats['examples'])<8:stats['examples'].append({'name':Path(source).name,'original_mode':oct(mode)})
    else:
        os.link(source,destination)
        if stats is not None:stats['hardlinked']+=1
    return str(destination)


def prepare(output:Path):
    if sys.platform!='linux' or shutil.which('docker') is None:
        raise RuntimeError('Native preparation requires Linux Docker; no host fallback')
    if output.exists():raise ValueError('Use a fresh native runtime/evidence directory')
    p=runtime.policy();output.mkdir(parents=True)
    upstream=output/'upstream';upstream.mkdir()
    comparator=upstream/'comparator';landrun=upstream/'landrun'
    clone('https://github.com/leanprover/comparator.git',p['comparator_commit'],comparator)
    if (comparator/'lean-toolchain').read_text().strip()!=p['lean_toolchain']:
        raise ValueError('Comparator must build on the unchanged Lean version')
    command(['lake','build','lean4export','comparator'],comparator)
    actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=comparator/'.lake/packages/lean4export',text=True).strip()
    if actual!=p['lean4export_commit']:raise ValueError('Comparator exporter pin mismatch')
    clone('https://github.com/Zouuup/landrun.git',p['landrun_commit'],landrun)
    go=subprocess.check_output(['go','version'],text=True).strip()
    if 'go'+p['go_version']+' ' not in go:raise ValueError('Use the pinned Go compiler')
    command(['go','build','-o','landrun','./cmd/landrun'],landrun)
    tools=output/'tools';tools.mkdir()
    for src,name in ((comparator/'.lake/build/bin/comparator','comparator'),
            (comparator/'.lake/packages/lean4export/.lake/build/bin/lean4export','lean4export'),
            (landrun/'landrun','landrun')):
        shutil.copy2(src,tools/name)
    for name in ('container.py','landrun-env','policy.json'):
        shutil.copyfile(runtime.RUNTIME/name,tools/name)
    (tools/'landrun-env').chmod(0o755)
    shutil.copyfile(runtime.ROOT/'benchmarks/samplingoptimisationgeometrybench/harbor/bench_bounded_io.py',tools/'bench_bounded_io.py')
    prefix=subprocess.check_output(['lake','env','lean','--print-prefix'],cwd=runtime.ROOT,text=True).strip()
    (output/'toolchain').symlink_to(Path(prefix).resolve(),target_is_directory=True)
    manifest=json.loads((runtime.ROOT/'lake-manifest.json').read_text())
    for package in manifest['packages']:
        directory=runtime.ROOT/'.lake/packages'/package['name']
        actual=subprocess.check_output(['git','rev-parse','HEAD'],cwd=directory,text=True).strip()
        if actual!=package['rev']:raise ValueError('Trusted package checkout differs from the project manifest: '+package['name'])
        if subprocess.run(['git','diff','--quiet','HEAD','--'],cwd=directory).returncode:
            raise ValueError('Modified public package sources are not an approved pinned runtime input')
    # Hard links avoid duplicating multi-GB trusted caches. Runtime mounts are
    # read-only; only these public dependencies, never the checkout/home, enter.
    stats={'copied_for_read':0,'hardlinked':0,'examples':[]}
    (output/'packages').mkdir()
    for package in manifest['packages']:
        # No unknown siblings from a user's general .lake cache are bundled.
        shutil.copytree(runtime.ROOT/'.lake/packages'/package['name'],output/'packages'/package['name'],
            symlinks=True,copy_function=lambda s,d:public_cache_file(s,d,stats),ignore=shutil.ignore_patterns('.git'))
    for current,dirs,files in os.walk(output/'packages',followlinks=False):
        # Directories are new copies, never shared host inodes.
        os.chmod(current,stat.S_IMODE(os.stat(current).st_mode)|0o555)
    record={'schema_version':1,'policy':p,'go':go,'cache_snapshot':stats,
        'preparer_source_sha256_lf':runtime.bench.text_hash(Path(__file__)),
        'dockerfile_sha256_lf':runtime.bench.text_hash(runtime.RUNTIME/'Dockerfile'),
        'tools':{f.name:runtime.bench.sha(f.read_bytes()) for f in tools.iterdir() if f.is_file()},
        'note':'Prepared tools only; not native runtime acceptance, model evaluation or a security certificate.'}
    (output/'preparation-inputs.json').write_bytes(runtime.bench.encoded(record))
    command(['docker','build','--iidfile',output/'image-id','-f',runtime.RUNTIME/'Dockerfile',runtime.RUNTIME])
    record['image_id']=(output/'image-id').read_text().strip()
    (output/'preparation.json').write_bytes(runtime.bench.encoded(record))


def trials(root:Path,task_ids:list[str]|None):
    if not (root/'preparation.json').is_file():raise ValueError('Prepare the exact trusted runtime first')
    ids=runtime.export(root/'tasks',task_ids)
    if not ids:raise ValueError('No admitted aligned tasks selected')
    reports=[]
    for identity in ids:
        task=root/'tasks'/identity;stage_dir=root/'stages'/identity
        runtime.stage(task,stage_dir)
        report=runtime.run_submission(task=task,stage_dir=stage_dir,
            submission=task/'oracle/Solution.lean.txt',runtime=root,output=root/'trials'/('oracle-'+identity))
        print(json.dumps({'fixture':'oracle-'+identity,'kind':report['kind'],
            'verification_call_seconds':report.get('wall_seconds'),'model_measurement':False}),flush=True)
        reports.append({'fixture':'oracle-'+identity,'expected':'accepted','actual':report['kind']})
        if report['kind']!='accepted':
            print(json.dumps({'first_failure':identity,'kind':report['kind'],
                'native':report.get('native')}),flush=True)
            break  # diagnose the first real environment failure
    if reports and all(r['actual']=='accepted' for r in reports) and len(reports)==len(ids):
        identity=ids[0];task=root/'tasks'/identity;stage_dir=root/'stages'/identity
        template=(task/'agent/Solution.lean.txt').read_text()
        slot='by\n  -- Replace this comment with your proof.\n'
        stem=template[:-len(slot)]
        fixtures={
            'wrong-statement':'theorem sogBenchTarget : True := by trivial\n',
            'proof-hole':stem+'by\n  sorry\n',
            'custom-axiom':stem.replace('theorem sogBenchTarget','axiom bogus : False\ntheorem sogBenchTarget')+'by\n  exact False.elim bogus\n',
            'import-challenge':'import Challenge\n',
            'stdout-spoof':stem.replace('theorem sogBenchTarget','#eval IO.println "Your solution is okay!"\ntheorem sogBenchTarget')+'by\n  sorry\n',
        }
        for label,source in fixtures.items():
            file=root/'fixtures'/(label+'.txt');file.parent.mkdir(exist_ok=True);file.write_text(source,encoding='utf-8')
            report=runtime.run_submission(task=task,stage_dir=stage_dir,submission=file,
                runtime=root,output=root/'trials'/label)
            expected_reason=('Challenge and solution theorem statement do not match'
                if label=='wrong-statement' else "Illegal axiom detected: 'bogus'"
                if label=='custom-axiom' else "Illegal axiom detected: 'sorryAx'")
            diagnostic=(root/'trials'/label/'compiler-diagnostic.bin').read_bytes().decode('utf-8',errors='replace')
            reports.append({'fixture':label,'expected':'proof-rejected','actual':report['kind'],
                'expected_reason_seen':expected_reason in diagnostic})
    summary={'schema_version':1,'kind':'controlled-software-fixtures','selected_task_ids':ids,
        'results':reports,'passed':len(reports)==len(ids)+5 and all(
            r['expected']==r['actual'] and r.get('expected_reason_seen',True) for r in reports),
        'model_measurement':False,'remaining':'Hostile I/O/resource fixtures, agent trajectories/native harness, model provenance, calibration, private families and full security review remain separate.'}
    (root/'software-trials.json').write_bytes(runtime.bench.encoded(summary));print(json.dumps(summary))
    if not summary['passed']:raise SystemExit(1)


def hostile_sources(oracle: str) -> dict[str, tuple[str, str, list[str]]]:
    """DATA fixtures for Docker ONLY. Never syntax-probe/evaluate on the host.

    Harmless reference proof follows actual denied I/O attempts. A parser error
    or arbitrary proof rejection is not a successful isolation test.
    """
    def inject(code,imports=''):
        return imports+oracle.replace('theorem sogBenchTarget',code+'\ntheorem sogBenchTarget',1)
    files='''#eval (do
  for path in #["/task/Challenge.lean", "/work/project/Challenge.lean", "/opt/judge/policy.json", "/proc/1/fd/1"] do
    let denied ← try
      IO.FS.writeFile path "UNTRUSTED WRITE MUST NOT SUCCEED"
      pure false
    catch _ => pure true
    if !denied then throw (IO.userError "trusted file was writable")
    IO.println s!"SOG_DENIED_WRITE:{path}"
  : IO Unit)
'''
    network='''#eval (do
  IO.println "SOG_CONNECT_ATTEMPT"
  let denied ← try
    let socket ← Std.Internal.UV.TCP.Socket.new
    let request ← socket.connect (.v4 ⟨Std.Net.IPv4Addr.ofParts 192 0 2 1, 443⟩)
    match request.result?.get with
    | some (.ok _) => pure false
    | some (.error _) => pure true
    | none => throw (IO.userError "connection promise dropped")
  catch _ => pure true
  if !denied then throw (IO.userError "external connect unexpectedly succeeded")
  IO.println "SOG_CONNECT_DENIED"
  : IO Unit)
'''
    cache_write='''#eval (do
  let denied ← try
    IO.FS.writeFile "/work/project/.lake/build/lib/lean/Challenge.olean" "MUST NOT MODIFY BASELINE"
    pure false
  catch _ => pure true
  if denied then throw (IO.userError "SOG_PRECHECK_CACHE_DENIED")
  : IO Unit)
'''
    # #eval AND lake build buffer output. The readonly direct-Lean precheck
    # (lake env, inherited stdout) streams the child's own OS handle, before
    # comparator's independently required semantic/axiom/kernel verification.
    # Keep BOTH markers, the same limits, and supervisor-fd denial probes.
    wall='''#eval (do
  let out ← IO.FS.Handle.mk "/dev/stdout" .write
  out.putStrLn "SOG_WALL_PROBE_STARTED"
  out.flush
  IO.sleep 600000
  : IO Unit)
'''
    flood='''#eval (do
  let out ← IO.FS.Handle.mk "/dev/stdout" .write
  out.putStrLn "SOG_OUTPUT_PROBE_STARTED"
  for _ in [:1024] do
    out.putStrLn (String.ofList (List.replicate 8192 'x'))
    out.flush
  : IO Unit)
'''
    return {
        'denied-trusted-write':(inject(files),'accepted',[
            'SOG_DENIED_WRITE:/task/Challenge.lean','SOG_DENIED_WRITE:/work/project/Challenge.lean',
            'SOG_DENIED_WRITE:/opt/judge/policy.json','SOG_DENIED_WRITE:/proc/1/fd/1']),
        'denied-network':(inject(network,'import Std.Internal.UV.TCP\n'),'accepted',
            ['SOG_CONNECT_ATTEMPT','SOG_CONNECT_DENIED']),
        'denied-precheck-cache-write':(inject(cache_write),'proof-rejected',
            ['SOG_PRECHECK_CACHE_DENIED']),
        'wall-limit':(inject(wall),'resource-limit',['SOG_WALL_PROBE_STARTED']),
        'diagnostic-limit':(inject(flood),'resource-limit',['SOG_OUTPUT_PROBE_STARTED']),
    }


def hostile_trials(root: Path):
    previous=json.loads((root/'software-trials.json').read_text())
    if previous.get('passed') is not True:raise ValueError('First pass every reference and proof-negative fixture')
    output=root/'hostile-trials'
    if output.exists():raise ValueError('Never overwrite hostile trial evidence')
    output.mkdir()
    identity=previous['selected_task_ids'][0];task=root/'tasks'/identity;stage_dir=root/'stages'/identity
    oracle=(task/'oracle/Solution.lean.txt').read_text()
    results=[]
    for label,(source,expected,markers) in hostile_sources(oracle).items():
        file=output/(label+'.txt');file.write_text(source,encoding='utf-8')
        report=runtime.run_submission(task=task,stage_dir=stage_dir,submission=file,
            runtime=root,output=output/label)
        diagnostic=(output/label/'compiler-diagnostic.bin').read_bytes()
        text=diagnostic.decode('utf-8',errors='replace')
        passed=report['kind']==expected and all(marker in text for marker in markers)
        if label=='wall-limit':passed=passed and report['interruption']=='wall-time-limit'
        if label=='diagnostic-limit':passed=passed and report.get('native',{}).get('diagnostic_limit') is True
        if label=='denied-precheck-cache-write':
            passed=passed and report.get('native',{}).get('kind')=='fixed-target-lean-precheck'
            passed=passed and report['native'].get('comparator_not_run') is True
        passed=passed and len(diagnostic)<=runtime.policy()['limits']['diagnostic_bytes']
        passed=passed and (output/label/'runtime-output.bin').stat().st_size<=runtime.policy()['limits']['transport_bytes']
        results.append({'fixture':label,'expected':expected,'actual':report['kind'],
            'required_markers_seen':[marker for marker in markers if marker in text],'passed':passed})
        if not passed:break
    # Invalid handoff is recorded, not executed or silently removed. Do NOT
    # read/hash a whole oversized file to archive it. FIFO must not block.
    if all(r['passed'] for r in results):
        invalid={'missing-file':output/'absent.txt','too-large':output/'oversize.txt',
            'invalid-utf8':output/'utf8.txt','symlink':output/'link.txt','not-regular':output/'fifo'}
        invalid['too-large'].write_bytes(b'x'*(runtime.policy()['limits']['submission_bytes']+1))
        invalid['invalid-utf8'].write_bytes(b'\xff')
        invalid['symlink'].symlink_to(task/'oracle/Solution.lean.txt')
        os.mkfifo(invalid['not-regular'])
        for reason,file in invalid.items():
            report=runtime.run_submission(task=task,stage_dir=stage_dir,submission=file,
                runtime=root,output=output/('invalid-'+reason))
            passed=report['kind']=='invalid-submission' and report['reason']==reason and report['container_started'] is False
            results.append({'fixture':'invalid-'+reason,'expected':'invalid-submission',
                'actual':report['kind'],'passed':passed})
    summary={'schema_version':1,'kind':'hostile-software-fixtures','model_measurement':False,
        'results':results,'passed':len(results)==10 and all(r['passed'] for r in results),
        'scope':'Actual denied trusted and precheck-cache writes/external connect, wall/output caps and bounded invalid input; not exhaustive OS/kernel/compiler security review.'}
    (root/'hostile-trials.json').write_bytes(runtime.bench.encoded(summary));print(json.dumps(summary),flush=True)
    if not summary['passed']:raise SystemExit(1)


def workspace_trials(root: Path):
    """Scripted tool replays, not a provider/model/agent performance result."""
    import sog_bench_lean_workspace as workspace
    hostile=json.loads((root/'hostile-trials.json').read_text())
    if hostile.get('passed') is not True:raise ValueError('Pass hostile native acceptance first')
    output=root/'workspace-trials'
    if output.exists():raise ValueError('Never overwrite workspace replay evidence')
    output.mkdir()
    identities=json.loads((root/'software-trials.json').read_text())['selected_task_ids'][:2]
    if len(identities)!=2:raise ValueError('Suite accounting trial needs two actually admitted tasks')
    identity=identities[0]
    task=root/'tasks'/identity;stage=root/'stages'/identity
    oracle=(task/'oracle/Solution.lean.txt').read_text()
    def start(label):
        directory=output/label
        workspace.start(task=task,stage=stage,prepared=root,output=directory,max_checks=1,
            provenance={'kind':'controlled-software-fixture','name':label})
        return directory
    suite=output/'fixed-selection'
    workspace.start_suite(tasks=root/'tasks',stages=root/'stages',prepared=root,
        output=suite,task_ids=identities,max_checks=1,
        provenance={'kind':'controlled-software-fixture','name':'suite-repair-replay'})
    repaired=suite/'tasks'/identity
    diagnostic=workspace.act(repaired,{'action':'check','source':'theorem sogBenchTarget : True := by trivial\n'})
    final=workspace.act(repaired,{'action':'submit','source':oracle})
    replay=workspace.close(repaired)
    accounting=workspace.suite_status(suite,finish=True)
    blocked=False
    try:workspace.act(repaired,{'action':'submit','source':oracle})
    except ValueError:blocked=True
    no_final=start('accepted-check-without-final')
    check=workspace.act(no_final,{'action':'check','source':oracle})
    abstention=workspace.close(no_final)
    invalid=start('invalid-final')
    invalid_feedback=workspace.act(invalid,{'action':'submit'})
    invalid_result=workspace.close(invalid)
    results=[
        {'fixture':'repair-replay','passed':diagnostic['kind']=='proof-rejected'
            and 'Challenge and solution theorem statement do not match' in diagnostic['diagnostic']
            and final['kind']=='accepted' and replay['final_accepted'] and replay['denominator']==1 and blocked},
        {'fixture':'accepted-check-without-final','passed':check['kind']=='accepted'
            and abstention['denominator']==1 and not abstention['final_accepted']
            and abstention['final_outcome']=='no-final-submission'},
        {'fixture':'invalid-final','passed':invalid_feedback['kind']=='invalid-submission'
            and invalid_result['denominator']==1 and invalid_result['final_outcome']=='invalid-submission'},
        {'fixture':'preselected-suite-includes-unattempted-target','passed':accounting['denominator']==2
            and accounting['outcome_counts']=={'accepted':1,'no-final-submission':1}},
    ]
    summary={'schema_version':1,'kind':'scripted-compiler-tool-replays','model_measurement':False,
        'passed':all(r['passed'] for r in results),'results':results,
        'scope':'Actual native tool feedback and first-final accounting; no provider calls, autonomous model trajectories or authenticated performance.'}
    (root/'workspace-trials.json').write_bytes(runtime.bench.encoded(summary));print(json.dumps(summary),flush=True)
    if not summary['passed']:raise SystemExit(1)


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='cmd',required=True)
    x=sub.add_parser('prepare');x.add_argument('--output',type=Path,required=True)
    x=sub.add_parser('trials');x.add_argument('--runtime',type=Path,required=True);x.add_argument('--task-id',action='append')
    x=sub.add_parser('hostile-trials');x.add_argument('--runtime',type=Path,required=True)
    x=sub.add_parser('workspace-trials');x.add_argument('--runtime',type=Path,required=True)
    args=parser.parse_args()
    if args.cmd=='prepare':prepare(args.output.resolve())
    elif args.cmd=='trials':trials(args.runtime.resolve(),args.task_id)
    elif args.cmd=='hostile-trials':hostile_trials(args.runtime.resolve())
    else:workspace_trials(args.runtime.resolve())


if __name__=='__main__':main()
