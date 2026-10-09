import datetime,hashlib,json,os,pathlib,subprocess
R=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();l=b.replace(b'\r\n',b'\n');return dict(path=p.relative_to(R).as_posix(),bytes=len(b),lf_bytes=len(l),raw_sha256=sha(b),lf_sha256=sha(l))
def wr(n,x):(O/n).write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
m=json.loads((O/'input.manifest.json').read_bytes());expected=[x['original'] for x in m['qualified_raw_LF_pairs']]
before=[pin(R/x['path']) for x in expected];assert before==expected
wr('compiler.inputs.before.json',dict(original30=before[:30],all58=before,snapshots_frozen_before_compile=True))
start=datetime.datetime.now(datetime.timezone.utc).isoformat();cmd=['lake','build','Tests.ProximalBPSMacroscopicDefectRoot']
with (O/'focused.stdout.log').open('wb') as a,(O/'focused.stderr.log').open('wb') as b:
 p=subprocess.Popen(cmd,cwd=R,stdout=a,stderr=b);pid=p.pid;ec=p.wait()
after=[pin(R/x['path']) for x in expected];assert before==after
wr('compiler.inputs.after.json',dict(original30=after[:30],all58=after,all_inputs_unchanged=True))
receipt=dict(actual_runner_pid=os.getpid(),actual_foreground_pid=pid,command=cmd,checked_science_base=m['checked_parent'],started_utc=start,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=ec,terminal_closed=True,compiler_runs=1,nonforced=True,inputs_before=pin(O/'compiler.inputs.before.json'),inputs_after=pin(O/'compiler.inputs.after.json'),stdout=pin(O/'focused.stdout.log'),stderr=pin(O/'focused.stderr.log'),original30_and_all58_unchanged=True,decoder_not_read=True)
wr('focused.receipt.json',receipt);print(json.dumps(receipt),flush=True);assert ec==0
