import hashlib,json,pathlib,subprocess,time
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-subtype-fragment92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
source=B/'SubtypeCoordinates92.lean';raw=source.read_bytes();assert bind(source)['raw_sha256']=='c4e7dc7915012fdb81228bb5c4cad6eeca533d977a5192e9d9a72e80d680037a'
suffix=b'\nset_option pp.deepTerms true\n#check @OrderedSubtype92.snocPrefix\n#check @OrderedSubtype92.subtype_simplex_lintegral_snoc\n#print axioms OrderedSubtype92.subtype_simplex_lintegral_snoc\n'
copy=D/'FreshSubtypeKernel92.lean'
with copy.open('xb') as f:f.write(raw+suffix)
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(copy.relative_to(R))]
start=time.monotonic()
with (D/'kernel.stdout.log').open('xb') as out,(D/'kernel.stderr.log').open('xb') as err:result=subprocess.run(argv,cwd=R,stdout=out,stderr=err)
receipt=dict(argv=argv,cwd=R.as_posix(),exit_code=result.returncode,duration_seconds=time.monotonic()-start,finished_utc=datetime.now(timezone.utc).isoformat(),terminal_closed=True,source=bind(source),copy=bind(copy),lake_manifest=bind(R/'lake-manifest.json'),stdout=bind(D/'kernel.stdout.log'),stderr=bind(D/'kernel.stderr.log'),scope='Subtype coordinate adapter only; no actual probability law.')
with (D/'kernel.receipt.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
print(json.dumps(receipt,indent=2));raise SystemExit(result.returncode)
