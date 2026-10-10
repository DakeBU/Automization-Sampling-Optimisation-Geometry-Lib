from pathlib import Path
import json,hashlib,datetime
R=Path('E:/Samplinglib');D=Path(__file__).parent
def load(p):return json.loads(p.read_bytes())
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(R)).replace('\\','/'),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def verify(x):
 if isinstance(x,dict):
  h=x.get('raw_sha256',x.get('RAW_sha256'))
  if h and 'path' in x:
   z=pin(R/x['path']);assert z['raw_sha256']==h,x['path']
   n=x.get('bytes',x.get('RAW_bytes'));assert n is None or z['bytes']==n,x['path']
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
def checked(p,h):
 assert pin(p)['raw_sha256']==h,p
 x=load(p);verify(x);return x
math_manifest=D/'header-math86/closed-RAW-manifest86.json'
checked(math_manifest,'1c86c0fbe40c070a472c5bf304b575221fd0b51539451de511aaf6ef4f9a0ea7')
math_decision=D/'header-math86/decision86.json'
m=checked(math_decision,'3fddb04166fb5fb24afa37f74f0007939ea871507fee555043f985a830fb11c8')
assert m['status']=='ACCEPT_WHOLE_HEADER_MATHEMATICS_AND_TYPE_NO_REPAIR' and m['compiler_terminal_exit']==0 and not m['required_repairs']
source_manifest=D/'header-source86/header-source.run-manifest86.json'
checked(source_manifest,'8614eafc574815f1d5f9d53bc7a1bc700d63cbcad032624b13ee8d41c0fa3923')
source_decision=D/'header-source86/header-source.decision86.json'
s=checked(source_decision,'e384ff8591ed32528816f239946e0cd47fa85423ce8fee6d0c09808f92926fb4')
assert s['verdict']=='ACCEPT_PROSPECTIVE_HEADER_SOURCE_SCOPE' and not s['required_repairs']
header=D/'header86.proposed.lean';assert pin(header)['raw_sha256']=='51e925d7a7874083c0802682e7157fcaa2adf6961c2f1ba711d1646ab35e32d8'
top=R/'runs/20261007-companion-priority/pbps-path-law-preread86/root.topology-adoption86.json';t=load(top);verify(t);assert t['accepted'] and t['dependency_DAG_acyclic']
z={'accepted':True,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'accepted_header':pin(header),'whole_header_math_manifest':pin(math_manifest),'whole_header_math_decision':pin(math_decision),'whole_header_source_manifest':pin(source_manifest),'whole_header_source_decision':pin(source_decision),'source_topology_adoption':pin(top),'no_repairs':True,'no_BODY':True,'StatementSeal':False,'proof_credit':False}
p=D/'independent-review-adoption86.json';assert not p.exists();p.write_text(json.dumps(z,indent=2)+'\n',encoding='utf-8')
print('86 full prospective header independently accepted; no proof or state credit')
