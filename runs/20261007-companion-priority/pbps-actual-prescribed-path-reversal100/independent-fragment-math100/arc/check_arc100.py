from pathlib import Path
import os, subprocess, json, hashlib, datetime
ROOT=Path('E:/Samplinglib')
OWN=Path(__file__).resolve().parent
RUN=ROOT/'runs/20261007-companion-priority/pbps-actual-prescribed-path-reversal100'
src=RUN/'ArcReversal100.lean'
b=src.read_bytes()
assert hashlib.sha256(b).hexdigest()=='f41c9907b77abe7f17c7c94bd78bfe86176dcdc9effb379fd08d0ab27a59be5d'
for trial in ['arc1-closed-horizon','arc2-explicit-involution']:
    d=RUN/'focused100'/trial
    receipt=json.loads((d/'receipt.json').read_text())
    assert hashlib.sha256((d/'input.exactraw.lean').read_bytes()).hexdigest()==receipt['input_raw_sha256']
assert (RUN/'focused100/arc2-explicit-involution/input.exactraw.lean').read_bytes()==b
w=OWN/'Arc100.IndependentKernel.lean'
assert not w.exists()
w.write_bytes(b+b'\n#print axioms PBPSArcReversal100.active_arc\n')
env=os.environ.copy()
env['PATH']=str(ROOT/'.astis/toolchain/lean-4.33.0-windows/bin')+os.pathsep+env['PATH']
env.pop('ELAN_TOOLCHAIN',None)
env['LEAN_NUM_THREADS']='2'
env['PYTHONUTF8']='1'
argv=[str(ROOT/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(w)]
p=subprocess.run(argv,cwd=ROOT,env=env,capture_output=True)
(OWN/'kernel.stdout.log').write_bytes(p.stdout)
(OWN/'kernel.stderr.log').write_bytes(p.stderr)
receipt=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=argv,exit_code=p.returncode,terminal_closed=True,fragment_raw_sha256=hashlib.sha256(b).hexdigest(),witness_raw_sha256=hashlib.sha256(w.read_bytes()).hexdigest(),exact_fragment_prefix=True,appended_only='print axioms active_arc',complete_SAU=False)
(OWN/'kernel-receipt100.native.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8',newline='\n')
print(p.stdout.decode('utf-8',errors='replace'))
print(p.stderr.decode('utf-8',errors='replace'))
raise SystemExit(p.returncode)
