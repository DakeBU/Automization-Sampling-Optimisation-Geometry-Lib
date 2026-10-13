from pathlib import Path
import hashlib,json
r=Path(__file__).parent;d=r/'independent-math86';load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def verify(x):
 if isinstance(x,dict):
  if 'path' in x and ('RAW_sha256' in x or 'raw_sha256' in x):
   assert pin(x['path'])['RAW_sha256']==x.get('RAW_sha256',x.get('raw_sha256')),x
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
assert pin(d/'closed-RAW-manifest86.json')['RAW_sha256']=='e32ee0a619823174891803fb9a7ba26baadf3c581ec7ef4a0cb84d519b5cf077'
assert pin(d/'decision86.json')['RAW_sha256']=='75b2a3a1219e8b7ebdd090a50dd718bcd2714aa1e78182692e0181c6323ecab9'
m=load(d/'closed-RAW-manifest86.json');a=load(d/'decision86.json');assert m['status']=='CLOSED_NONCIRCULAR'
for group in ['frozen_current_inputs','immutable_original_inputs','owned_artifacts']:verify(m[group])
# Historical observations point to explicitly retained original snapshots, not mutable current paths.
assert len(m['original_observation_provenance'])==len(m['immutable_original_inputs'])==3
verify(a)
assert a['status']=='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY' and not a['required_repairs']
assert a['standard_axioms_only'] and a['full_private_statement_seal_exact'] and a['six_original_binders'] and a['all14_literal_definitions']
for name in ['fresh-whole-module.receipt.json','fresh-focused-build.receipt.json']:
 receipt=load(d/name);assert receipt['exit_code']==0 and receipt['terminal_closed']
closure=load(d/'kernel-dependency-summary86.json');assert closure['standard_axioms_only'] and closure['exact_four_public_parents']
c=load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-finite-first-event-law.json')
assert set(a['actual_project_public_parents'])==set(c['parents'])
assert a['kernel_counts']==dict(owned_generated=19,immediate_private_specs=12,transitive_project=39,transitive_edges=44,direct_generic=480)
p=r/'root.math86.adoption.json';assert not p.exists()
p.write_text(json.dumps(dict(status='ACCEPTED_INDEPENDENT_MATH_ONLY',reviewer=a['reviewer_id'],module=a['module'],native_decision=pin(d/'decision86.json'),native_closed_manifest=pin(d/'closed-RAW-manifest86.json'),fresh_compiler_receipt=pin(d/'fresh-whole-module.receipt.json'),kernel_dependency_receipt=pin(d/'kernel-dependency-summary86.json'),canonical_cell_parents_equal_actual_public_kernel_dependencies=True,private_generated_closure_preserved=True,successor_exposition=pin(r/'publication-freeze86.successor.json'),distinct_exact_exposition_repair=pin(r/'root.exposition-repair86.adoption.json'),historical_observations_preserved_as_explicit_immutable_snapshots=True,source_verdict=False,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n')
neutral=Path('.astis/decoder86');neutral.mkdir(exist_ok=False)
(neutral/'anonymous.packet.json').write_bytes((r/'anonymous.decoder86.json').read_bytes())
print('Independent whole mathematics86 adopted; neutral anonymous packet prepared; source/exact-commit admission separate')
