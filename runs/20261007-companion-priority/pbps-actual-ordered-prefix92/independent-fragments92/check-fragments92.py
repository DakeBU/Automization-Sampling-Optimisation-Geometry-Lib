import hashlib,json,pathlib,subprocess,time
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib')
B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92'
D=B/'independent-fragments92'
G=B/'Geometry92.lean'
raw=G.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='a415510aa496843c723f7dea200a1532714277db9e026cabec4b521efd3c6dd4'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
suffix=b'''\nset_option pp.deepTerms true\n#check @OrderedPrefix92.ordered_prefix_borel_data\n#check @OrderedPrefix92.actual_prefix_identification\n#print axioms OrderedPrefix92.ordered_prefix_borel_data\n#print axioms OrderedPrefix92.actual_prefix_identification\n'''
p=D/'FreshGeometryKernel92.lean'
with p.open('xb') as f:f.write(raw+suffix)
argv=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(p.relative_to(R))]
start=time.monotonic()
with (D/'kernel.stdout.log').open('xb') as out,(D/'kernel.stderr.log').open('xb') as err:
 result=subprocess.run(argv,cwd=R,stdout=out,stderr=err)
receipt=dict(argv=argv,cwd=R.as_posix(),exit_code=result.returncode,duration_seconds=time.monotonic()-start,finished_utc=datetime.now(timezone.utc).isoformat(),terminal_closed=True,geometry=bind(G),checked_copy=bind(p),seal=bind(B/'root.statement-seal92.json'),lake_manifest=bind(R/'lake-manifest.json'),stdout=bind(D/'kernel.stdout.log'),stderr=bind(D/'kernel.stderr.log'),scope='Fresh compilation and kernel axiom/type inspection of two internal proof fragments; no whole sealed theorem or SAU acceptance.')
with (D/'kernel.receipt.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
print(json.dumps(receipt,indent=2));raise SystemExit(result.returncode)
