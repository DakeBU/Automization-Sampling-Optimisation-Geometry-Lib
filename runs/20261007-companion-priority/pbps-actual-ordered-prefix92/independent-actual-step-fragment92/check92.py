import hashlib,json,pathlib,subprocess,time
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-actual-step-fragment92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
source=B/'Integrals92.lean';raw=source.read_bytes();assert bind(source)['raw_sha256']=='7a14a8e37213b002f91902f1e8baa247d9242a6e984b524ca302a00aed82f6a3'
copy=D/'FreshActualStepKernel92.lean';suffix=b'\nset_option pp.deepTerms true\n#check @OrderedIntegral92.actual_prefix_step_integral\n#print axioms OrderedIntegral92.actual_prefix_step_integral\n'
with copy.open('xb') as f:f.write(raw+suffix)
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(copy.relative_to(R))];start=time.monotonic()
with (D/'kernel.stdout.log').open('xb') as out,(D/'kernel.stderr.log').open('xb') as err:result=subprocess.run(argv,cwd=R,stdout=out,stderr=err)
receipt=dict(argv=argv,cwd=R.as_posix(),exit_code=result.returncode,duration_seconds=time.monotonic()-start,finished_utc=datetime.now(timezone.utc).isoformat(),terminal_closed=True,source=bind(source),copy=bind(copy),lake_manifest=bind(R/'lake-manifest.json'),stdout=bind(D/'kernel.stdout.log'),stderr=bind(D/'kernel.stderr.log'),scope='Actual one-step integral recurrence fragment; not the all-n density law.')
with (D/'kernel.receipt.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
print(json.dumps(receipt,indent=2));raise SystemExit(result.returncode)
