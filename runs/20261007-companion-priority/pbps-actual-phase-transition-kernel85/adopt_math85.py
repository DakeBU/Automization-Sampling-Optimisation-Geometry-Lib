from pathlib import Path
import hashlib,json
r=Path(__file__).parent;d=r/'independent-math85';load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def verify(x):
 if isinstance(x,dict):
  if 'path' in x and ('RAW_sha256' in x or 'raw_sha256' in x):
   assert pin(x['path'])['RAW_sha256']==x.get('RAW_sha256',x.get('raw_sha256')),x
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
assert pin(d/'closed-RAW-manifest85.json')['RAW_sha256']=='f1e548950f55cea39141cbeb7808f09b00d2c770302d351fe9fc7ab59a874a99'
assert pin(d/'decision85.json')['RAW_sha256']=='33fcd293740de4f9ec8169f60424d6a4d4529f9306e23193796fdd8663cf5c81'
verify(load(d/'closed-RAW-manifest85.json'));a=load(d/'decision85.json');verify(a)
assert a['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY'
assert not a['required_repairs'] and not a['fake_closure_hits']
assert a['standard_axioms_only'] and a['whole_statement_and_BODY_accepted'] and a['exposition_six_regions_accepted']
for name in ['fresh-whole-module.receipt.json','fresh-focused-build.receipt.json']:
 receipt=load(d/name);assert receipt['exit_code']==0 and receipt['terminal_closed']
closure=load(d/'kernel-dependency-summary85.json');classification=load(d/'kernel-dependency-classification85.json')
assert set(closure['axioms'])=={'propext','Classical.choice','Quot.sound'}
c=load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-phase-transition-kernel.json')
assert set(classification['actual_public_producer_parents'])==set(c['parents'])
assert classification['no_extra_public_parent'] and classification['public_producer_count']==2 and classification['private_direct_count']==6
p=r/'root.math85.adoption.json';assert not p.exists()
p.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_MATH_ONLY',reviewer=a['reviewer_id'],module=a['module'],native_decision=pin(d/'decision85.json'),native_closed_manifest=pin(d/'closed-RAW-manifest85.json'),fresh_compiler_receipt=pin(d/'fresh-whole-module.receipt.json'),kernel_dependency_receipt=pin(d/'kernel-dependency-summary85.json'),kernel_classification_receipt=pin(d/'kernel-dependency-classification85.json'),axioms=closure['axioms'],canonical_cell_parents_equal_actual_public_kernel_dependencies=True,private_generated_closure_preserved=True,source_verdict=False,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n')
neutral=Path('.astis/decoder85');neutral.mkdir(exist_ok=False)
(neutral/'anonymous.packet.json').write_bytes((r/'anonymous.decoder85.json').read_bytes())
print('Independent whole mathematics85 adopted; neutral anonymous packet prepared; source and exact-commit admission separate')
