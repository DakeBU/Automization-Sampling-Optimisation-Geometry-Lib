import pathlib,json,hashlib,subprocess,os,shutil,datetime,re
ROOT=pathlib.Path('E:/Samplinglib');R=ROOT/'runs/20261007-companion-priority/pbps-real-complex-lift60';D=R/'independent-math60'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,q):p.write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode())
def load(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def frozen():
 f=load(R/'math-freeze.json');assert len(f['inputs'])==31
 rows=[]
 for x in f['inputs']:
  a=pin(pathlib.Path(x['path']));assert a['bytes']==x['raw_bytes'] and a['raw_sha256']==x['raw_sha256'] and a['lf_sha256']==x['lf_sha256'];rows.append(a)
 return rows
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip();assert head==load(R/'math-freeze.json')['checked_base_commit']
before=frozen();env=dict(os.environ);previous=env.pop('ELAN_TOOLCHAIN',None);env['LEAN_NUM_THREADS']='2';env['PYTHONUTF8']='1';env['PYTHONDONTWRITEBYTECODE']='1'
assert (ROOT/'lean-toolchain').read_text().strip()=='leanprover/lean4:v4.33.0'
manifest=load(ROOT/'lake-manifest.json');mathlib=next(x for x in manifest['packages'] if x['name']=='mathlib');assert mathlib['rev'].startswith('db584')
lake=shutil.which('lake');assert lake
write(D/'inputs.before.json',dict(checked_base_commit=head,frozen=before,count=31,math_freeze=pin(R/'math-freeze.json'),lake_executable=pin(pathlib.Path(lake)),mathlib_revision=mathlib['rev'],inherited_ELAN_TOOLCHAIN_removed=previous is not None,environment=dict(LEAN_NUM_THREADS='2',PYTHONUTF8='1',PYTHONDONTWRITEBYTECODE='1'),pin_timing='All actual bytes read and checked before invoking focused lake build'))
with (D/'toolchain.stdout.log').open('wb') as out,(D/'toolchain.stderr.log').open('wb') as err:
 p=subprocess.Popen([lake,'env','lean','--version'],cwd=ROOT,env=env,stdout=out,stderr=err);toolpid=p.pid;code=p.wait()
assert code==0 and '4.33.0' in (D/'toolchain.stdout.log').read_text()
command=[lake,'build','Tests.ProximalBPSDefectComplexLift'];started=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (D/'compiler.stdout.log').open('wb') as out,(D/'compiler.stderr.log').open('wb') as err:
 p=subprocess.Popen(command,cwd=ROOT,env=env,stdout=out,stderr=err)
 write(D/'compiler.lease.open.json',dict(status='OPEN',actor='/root/whole_math52/independent-math60',actual_compiler_PID=p.pid,command=command,started_utc=started,pre_run_inputs=pin(D/'inputs.before.json')))
 pid=p.pid;exitcode=p.wait()
write(D/'compiler.status.json',dict(command=command,cwd=ROOT.as_posix(),actual_PID=pid,exit_code=exitcode,terminal_closed=True,started_utc=started,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout=pin(D/'compiler.stdout.log'),stderr=pin(D/'compiler.stderr.log'),toolchain_check_actual_PID=toolpid,toolchain_check_exit_code=code,toolchain_stdout=pin(D/'toolchain.stdout.log'),toolchain_stderr=pin(D/'toolchain.stderr.log'),forced_rebuild=False,focused_build_invocation_count=1))
after=frozen();assert before==after;write(D/'inputs.after.json',dict(frozen=after,count=31,all_equal_pre_run=True,math_freeze=pin(R/'math-freeze.json')))
assert exitcode==0
print(json.dumps(dict(status='ACTUAL_FOCUSED_EXIT0_AND31_PREPOST_INPUT_PINS_PASS',compiler_PID=pid,reader_PID=os.getpid(),toolchain_PID=toolpid,checked_base=head)),flush=True)
