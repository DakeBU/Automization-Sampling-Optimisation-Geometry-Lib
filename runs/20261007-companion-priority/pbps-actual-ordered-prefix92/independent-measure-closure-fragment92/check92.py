import hashlib,json,pathlib,subprocess,time
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-measure-closure-fragment92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
source=B/'MeasureClosure92.lean';raw=source.read_bytes();assert bind(source)['raw_sha256']=='0aeb5f6e6ac9b04b0deb724755f2bd241047634b86dc60fadba3f12fecd9b19d'
copy=D/'FreshClosureKernel92.lean';suffix=b'\nset_option pp.deepTerms true\n#check @OrderedMeasureClosure92.law_and_mass_of_all_tests\n#print axioms OrderedMeasureClosure92.law_and_mass_of_all_tests\n'
with copy.open('xb') as f:f.write(raw+suffix)
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(copy.relative_to(R))];start=time.monotonic()
with (D/'kernel.stdout.log').open('xb') as out,(D/'kernel.stderr.log').open('xb') as err:result=subprocess.run(argv,cwd=R,stdout=out,stderr=err)
receipt=dict(argv=argv,cwd=R.as_posix(),exit_code=result.returncode,duration_seconds=time.monotonic()-start,finished_utc=datetime.now(timezone.utc).isoformat(),terminal_closed=True,source=bind(source),copy=bind(copy),lake_manifest=bind(R/'lake-manifest.json'),stdout=bind(D/'kernel.stdout.log'),stderr=bind(D/'kernel.stderr.log'),scope='Generic private conversion of an already-proved all-test law only.')
with (D/'kernel.receipt.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
print(json.dumps(receipt,indent=2));raise SystemExit(result.returncode)
