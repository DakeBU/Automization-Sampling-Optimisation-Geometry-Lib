from pathlib import Path
import hashlib,json,sys
r=Path(__file__).parent;d=r/'independent-math83';load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def verify(x):
 if isinstance(x,dict):
  if 'path' in x and ('RAW_sha256' in x or 'raw_sha256' in x):
   q=pin(x['path']);assert q['RAW_sha256']==x.get('RAW_sha256',x.get('raw_sha256')),x
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
assert pin(d/'closed-manifest83.json')['RAW_sha256']==sys.argv[1]
verify(load(d/'closed-manifest83.json'));a=load(d/'decision83.json');verify(a)
assert a['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY'
assert not a['mathematical_blockers'] and not a['required_repairs']
assert set(a['standard_axioms_only'])=={'propext','Classical.choice','Quot.sound'}
receipt=load(d/'fresh-whole-module.receipt.json');assert receipt['exit_code']==0 and receipt['terminal_closed'] and receipt['full_source_prefix_exact']
closure=load(d/'kernel-dependency-summary83.json');assert closure['status']=='PASS'
c=load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounded-test-continuity.json');assert set(closure['external_ASTIS_dependencies'])==set(c['parents'])
p=r/'root.math83.adoption.json';assert not p.exists()
p.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_MATH_ONLY',reviewer=a['reviewer_id'],module=a['module'],native_decision=pin(d/'decision83.json'),native_closed_manifest=pin(d/'closed-manifest83.json'),fresh_compiler_receipt=pin(d/'fresh-whole-module.receipt.json'),kernel_dependency_receipt=pin(d/'kernel-dependency-summary83.json'),axioms=a['standard_axioms_only'],canonical_cell_parents_equal_actual_kernel_dependencies=True,source_verdict=False,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Independent mathematics83 adopted; source/exact-commit admission separate')
