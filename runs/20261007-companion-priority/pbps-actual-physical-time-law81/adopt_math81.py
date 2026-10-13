from pathlib import Path
import json,hashlib
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81');d=r/'independent-math81'
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def verify(x):
 if isinstance(x,dict):
  if 'path' in x and ('RAW_sha256' in x or 'raw_sha256' in x):
   p=pin(x['path']);assert p['RAW_sha256']==x.get('RAW_sha256',x.get('raw_sha256')),x
   if 'RAW_bytes' in x:assert p['RAW_bytes']==x['RAW_bytes']
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
assert pin(d/'closed-manifest81.json')['RAW_sha256']=='5cc045a4388f984b826f3492487824d1357049fb6574a66e7592abc5d9d738da'
verify(load(d/'closed-manifest81.json'));a=load(d/'decision81.json');verify(a)
assert a['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY' and not a['repair_required']
assert set(a['standard_axioms'])=={'propext','Classical.choice','Quot.sound'}
receipt=load(d/'fresh-whole-module.receipt.json');assert receipt['exit_code']==0 and receipt['terminal_closed'] and receipt['actual_foreground_PID']>0 and receipt['full_source_prefix_exact']
closure=load(d/'kernel-dependency-summary81.json');assert closure['status']=='PASS'
c=load('research-wiki/frontier-cells/ASTIS-SW-PBPS-ideal-half-turn-kernel.json')
assert set(closure['external_ASTIS_dependencies'])==set(c['parents'])
p=r/'root.math81.adoption.json';assert not p.exists();p.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_MATH_ONLY',reviewer=a['reviewer'],module=a['module'],native_decision=pin(d/'decision81.json'),native_closed_manifest=pin(d/'closed-manifest81.json'),fresh_compiler_receipt=pin(d/'fresh-whole-module.receipt.json'),kernel_dependency_receipt=pin(d/'kernel-dependency-summary81.json'),axioms=a['standard_axioms'],canonical_cell_parents_equal_actual_kernel_dependencies=True,source_verdict=False,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Independent whole-source mathematics81 adopted; source/exact-commit admission separate')
