import datetime,hashlib,json,os,pathlib,subprocess,sys
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def wr(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
m=json.loads((O/'input.manifest.json').read_bytes());pairs=m['qualified_raw_LF_pairs']
before=[pin(R/x['original']['path']) for x in pairs[:27]];assert before==[x['original'] for x in pairs[:27]]
assert not (O/'focused.receipt.json').exists(),'Exactly one NONFORCED focused compiler permitted'
wr('compiler.inputs.before.json',dict(actual_runner_pid=os.getpid(),original27=before,prerun_raw_LF_snapshots=[dict(raw=x['raw_snapshot'],LF=x['lf_snapshot']) for x in pairs[:27]],start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
cmd=['lake','build','Tests.ProximalBPSRealDefectRootUnique']
with (O/'focused.stdout.log').open('wb') as a,(O/'focused.stderr.log').open('wb') as b:
 p=subprocess.Popen(cmd,cwd=R,stdout=a,stderr=b);ec=p.wait()
after=[pin(R/x['original']['path']) for x in pairs[:27]];assert after==before,'Pinned source/math inputs changed during focused build'
wr('compiler.inputs.after.json',dict(original27=after,unchanged_exactly=True))
log=(O/'focused.stdout.log').read_bytes().decode('utf-8',errors='strict')+(O/'focused.stderr.log').read_bytes().decode('utf-8',errors='strict')
receipt=dict(command=cmd,actual_runner_pid=os.getpid(),actual_foreground_pid=p.pid,exit_code=ec,terminal_closed=True,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=pin(O/'focused.stdout.log'),stderr=pin(O/'focused.stderr.log'),inputs_before=pin(O/'compiler.inputs.before.json'),inputs_after=pin(O/'compiler.inputs.after.json'),original27_unchanged=True,nonforced=True,compiler_runs=1,decoder_read=False,gate_scope='Exactly one lake build Tests.ProximalBPSRealDefectRootUnique; no full/root gate, no generator',build_job_summary=[x for x in log.splitlines() if 'Build completed successfully' in x],axiom_lines=[x for x in log.splitlines() if 'depends on axioms:' in x and 'SquareRootUnique' in x or 'depends on axioms:' in x and 'DefectRootUnique' in x])
wr('focused.receipt.json',receipt)
print(json.dumps(dict(actual_runner_pid=os.getpid(),actual_foreground_pid=p.pid,exit_code=ec,terminal_closed=True,original27_unchanged=True,build_summary=receipt['build_job_summary'],axiom_lines=receipt['axiom_lines'],compiler_runs=1)))
assert ec==0,'Focused build failed; retain exact negative evidence and do not rerun'
