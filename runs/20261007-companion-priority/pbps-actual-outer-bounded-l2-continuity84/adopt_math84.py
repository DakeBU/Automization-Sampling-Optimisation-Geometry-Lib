from pathlib import Path
import hashlib,json
r=Path(__file__).parent;d=r/'independent-math84';load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def verify(x):
 if isinstance(x,dict):
  if 'path' in x and ('RAW_sha256' in x or 'raw_sha256' in x):
   q=pin(x['path']);assert q['RAW_sha256']==x.get('RAW_sha256',x.get('raw_sha256')),x
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
assert pin(d/'closed-raw-manifest84.json')['RAW_sha256']=='a97fb0013539363c49961c8b7e2748144ddf64c2a7bf8db42c18a10afa7ef3fe'
assert pin(d/'decision84.json')['RAW_sha256']=='1f82b6ed480302ac3a2f4e1d7981838cc39fb7fcf6377da78fe383bca2306568'
verify(load(d/'closed-raw-manifest84.json'));a=load(d/'decision84.json');verify(a)
assert a['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY'
assert not a['required_repairs'] and not a['fake_closure_hits']
assert a['standard_axioms_only'] and a['whole_statement_and_BODY_accepted'] and a['exposition_eight_regions_accepted']
receipt=load(d/'fresh-whole-module.receipt.json');assert receipt['exit_code']==0 and receipt['terminal_closed']
closure=load(d/'kernel-dependency-summary84.json');assert closure['status']=='PASS'
assert set(closure['axioms'])=={'propext','Classical.choice','Quot.sound'}
c=load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-outer-bounded-l2-continuity.json');assert set(closure['external_ASTIS_dependencies'])==set(c['parents'])
p=r/'root.math84.adoption.json';assert not p.exists()
p.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_MATH_ONLY',reviewer=a['reviewer_id'],module=a['module'],native_decision=pin(d/'decision84.json'),native_closed_manifest=pin(d/'closed-raw-manifest84.json'),fresh_compiler_receipt=pin(d/'fresh-whole-module.receipt.json'),kernel_dependency_receipt=pin(d/'kernel-dependency-summary84.json'),axioms=closure['axioms'],canonical_cell_parents_equal_actual_kernel_dependencies=True,source_verdict=False,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Independent whole mathematics84 adopted; source/exact-commit admission separate')
