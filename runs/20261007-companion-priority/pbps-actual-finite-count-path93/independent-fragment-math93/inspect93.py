from pathlib import Path
import hashlib,json,subprocess,datetime,time,difflib
R=Path('E:/Samplinglib'); B=R/'runs/20261007-companion-priority/pbps-actual-finite-count-path93'; O=B/'independent-fragment-math93'
def raw(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
inputs=[B/'CountInterfaces93.lean',B/'InterpolationFormula93.lean',B/'WeightedPrefix93.lean',B/'focused93/weighted-prefix3-explicit-test/input.exactraw.snapshot.lean',B/'focused93/weighted-prefix5-typed-joint-map/input.exactraw.snapshot.lean',R/'lake-manifest.json',R/'runs/20261007-companion-priority/pbps-finite-count-path-preread93/Header93.lean']
for name in ['count-interfaces7-instance-transport','interpolation-formula1','weighted-prefix3-explicit-test']:
 for f in ['receipt.json','stdout.log','stderr.log']:inputs.append(B/'focused93'/name/f)
for p in inputs[:3]:
 (O/(p.stem+'.reviewed.exactraw.lean')).write_bytes(p.read_bytes())
with (O/'inputs93.native.json').open('x',encoding='utf-8') as f:json.dump({'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'inputs':[raw(p) for p in inputs]},f,indent=2)
a=inputs[3].read_text(encoding='utf-8-sig');b=inputs[2].read_text(encoding='utf-8-sig')
with (O/'weighted-extension93.diff').open('x',encoding='utf-8') as f:f.write(''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),fromfile='passed-weighted-prefix3',tofile='reviewed-live-weighted-prefix5')))
cmd=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str((O/'GenericDiagnostic93.lean').relative_to(R))]
start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
with (O/'generic.stdout.log').open('xb') as out,(O/'generic.stderr.log').open('xb') as err:p=subprocess.run(cmd,cwd=R,stdout=out,stderr=err)
receipt={'argv':cmd,'started_utc':start,'elapsed_seconds':time.monotonic()-t,'exit_code':p.returncode,'terminal_closed':True,'scope':'Independent generic API diagnostic only; not a repeat of live WeightedPrefix compilation','input':raw(O/'GenericDiagnostic93.lean')}
with (O/'generic.receipt.native.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
print(json.dumps(receipt));print((O/'generic.stdout.log').read_text())