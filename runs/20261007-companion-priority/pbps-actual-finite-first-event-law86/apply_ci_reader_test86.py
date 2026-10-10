from pathlib import Path
import json,hashlib,sys,subprocess,os,datetime
R=Path('E:/Samplinglib');r=Path(__file__).parent/'ci-reader-order-repair86';review=r/'independent-review'
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(R)).replace('\\','/'),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def verify(x):
 if isinstance(x,dict):
  if 'path' in x and 'raw_sha256' in x:
   p=Path(x['path']);p=p if p.is_absolute() else R/p
   assert pin(p)['raw_sha256']==x['raw_sha256'],p
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
expected={'independent-ci-review86.decision.json':'85d364224bc00e55d4e87019b90cad0b16df17ceb39b4c3e8b565c086dec9b7d','independent-ci-review86.run.json':'6112ba2ec8e4db97d4a5ab1788854d85f2311e764d1819ca4d06c34be9d7874b','independent-ci-review86.RAW-manifest.json':'544264a559d4433b7f82b7dd15331c539268b778969b3aabfe9de5cb9679f500'}
for name,h in expected.items():
 p=review/name;assert pin(p)['raw_sha256']==h;verify(json.loads(p.read_bytes()))
sys.path.insert(0,str(R/'tools'));import astis_advance
lane=astis_advance.current_advances()['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel'];assert lane['state']=='STABILIZING'
proposal=json.loads((r/'proposal86.json').read_bytes());p=R/'tools/tests/test_astis_publication.py'
assert pin(p)['raw_sha256']==proposal['before']['raw_sha256']
candidate=r/'test.proposed.exactraw.snapshot';assert pin(candidate)['raw_sha256']==proposal['proposed']['raw_sha256']
receipt=r/'root.application86.json';assert not receipt.exists()
p.write_bytes(candidate.read_bytes())
receipt.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'exact_proposed_test_applied':pin(p),'independent_review':[pin(review/n) for n in expected],'sole_stabilization_lane':'ASTIS-SA-20261005-SPHMCImplementedPhaseKernel','renderer_math_source_audits_unchanged':True,'remote_CI_pass':False},indent=2)+'\n',encoding='utf-8',newline='\n')
print('Exact independently reviewed test repair applied in sole stabilization lane; gates pending.')
