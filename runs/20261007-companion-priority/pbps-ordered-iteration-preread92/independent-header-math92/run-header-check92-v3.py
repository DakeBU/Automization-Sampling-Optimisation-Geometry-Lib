import hashlib,json,pathlib,subprocess,time
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib')
D=R/'runs/20261007-companion-priority/pbps-ordered-iteration-preread92/independent-header-math92'
H=R/'runs/20261007-companion-priority/pbps-ordered-iteration-preread92/prospective-header/Header92.lean'
raw=H.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='9ad92c3ba89af78f3096342f7663bc547e6c03b6ce8173645cc13030d24bcd1f'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
suffix=b'''\nset_option pp.deepTerms true\nset_option pp.universes true\n#print Header92.actual_ordered_prefix_statement\n#print axioms Header92.actual_ordered_prefix_statement\n#check map_comap_subtype_coe\n#check MeasureTheory.Measure.volume_pi_eq_dirac\n#check Fin.induction_zero\n#check Fin.induction_succ\n#print MeasureTheory.hittingAfter\n'''
copy=D/'FreshHeaderKernel92v3.lean'
with copy.open('xb') as f:f.write(raw+suffix)
args=[str(R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe'),'env','lean',str(copy.relative_to(R))]
start=time.monotonic();utc=datetime.now(timezone.utc).isoformat()
with (D/'kernel-v3.stdout.log').open('xb') as out,(D/'kernel-v3.stderr.log').open('xb') as err:
 p=subprocess.run(args,cwd=R,stdout=out,stderr=err)
receipt=dict(argv=args,cwd=R.as_posix(),exit_code=p.returncode,started_utc=utc,finished_utc=datetime.now(timezone.utc).isoformat(),duration_seconds=time.monotonic()-start,terminal_closed=True,header=bind(H),checked_copy=bind(copy),manifest=bind(R/'lake-manifest.json'),stdout=bind(D/'kernel-v3.stdout.log'),stderr=bind(D/'kernel-v3.stderr.log'),scope='Elaboration and kernel printing of a proposition definition, not theorem proof.',predecessor_failure='Two inspection suffix attempts misqualified map_comap_subtype_coe; source declares it at root namespace. First also used unsupported pp.width. Original header and both negative attempts retained.')
with (D/'kernel-v3.receipt.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
print(json.dumps(receipt,indent=2));raise SystemExit(p.returncode)
