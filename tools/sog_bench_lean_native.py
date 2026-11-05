"""Prepare trusted tools and run controlled Linux Docker fixtures, not models."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

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
    # Hard links avoid duplicating multi-GB trusted caches. Runtime mounts are
    # read-only; only these public dependencies, never the checkout/home, enter.
    shutil.copytree(runtime.ROOT/'.lake/packages',output/'packages',symlinks=True,
        copy_function=os.link,ignore=shutil.ignore_patterns('.git'))
    command(['docker','build','--iidfile',output/'image-id','-f',runtime.RUNTIME/'Dockerfile',runtime.RUNTIME])
    record={'schema_version':1,'policy':p,'go':go,'image_id':(output/'image-id').read_text().strip(),
        'tools':{f.name:runtime.bench.sha(f.read_bytes()) for f in tools.iterdir() if f.is_file()},
        'note':'Prepared tools only; not native runtime acceptance, model evaluation or a security certificate.'}
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
        reports.append({'fixture':'oracle-'+identity,'expected':'accepted','actual':report['kind']})
        if report['kind']!='accepted':break  # diagnose the first real environment failure
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
            reports.append({'fixture':label,'expected':'proof-rejected','actual':report['kind']})
    summary={'schema_version':1,'kind':'controlled-software-fixtures','selected_task_ids':ids,
        'results':reports,'passed':len(reports)==len(ids)+5 and all(r['expected']==r['actual'] for r in reports),
        'model_measurement':False,'remaining':'Hostile I/O/resource fixtures, agent trajectories/native harness, model provenance, calibration, private families and full security review remain separate.'}
    (root/'software-trials.json').write_bytes(runtime.bench.encoded(summary));print(json.dumps(summary))
    if not summary['passed']:raise SystemExit(1)


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='cmd',required=True)
    x=sub.add_parser('prepare');x.add_argument('--output',type=Path,required=True)
    x=sub.add_parser('trials');x.add_argument('--runtime',type=Path,required=True);x.add_argument('--task-id',action='append')
    args=parser.parse_args()
    if args.cmd=='prepare':prepare(args.output.resolve())
    else:trials(args.runtime.resolve(),args.task_id)


if __name__=='__main__':main()
