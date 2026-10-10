from pathlib import Path
import hashlib,json
r=Path(__file__).parent;d=r/'exact-commit-verification82';sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((d/'closed-manifest82.json').read_bytes())=='09c113d29280d47dba016d8be5772139043b18a9a8560749976888a177f96fb7'
assert sha((d/'verified.json').read_bytes())=='b30f3f391fa144b50c86269b0d86e592ffa82081513241cc9aaf511ef09f3469'
m=json.loads((d/'closed-manifest82.json').read_bytes());checked=[]
def verify(x):
 if isinstance(x,dict):
  h=x.get('RAW_sha256',x.get('raw_sha256'))
  if h and x.get('path'):
   p=Path(x['path']);assert sha(p.read_bytes())==h,p;checked.append(p.as_posix())
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
verify(m)
v=json.loads((d/'verified.json').read_bytes());assert v['verified_commit']=='8e182aeb384e5b9edb922c02fc14ceeca6f9b090'
(r/'root.exact82.adoption.json').write_text(json.dumps(dict(status='ADOPTED_INDEPENDENT_VERIFIED_SCIENCE',checked_commit=v['verified_commit'],verifier='/root/exact_verify77',native_manifest_RAW_sha256=sha((d/'closed-manifest82.json').read_bytes()),all_native_artifacts_RAW_rechecked=True,artifacts_checked=len(checked),local_aggregate='pending',Goal_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Native independent exact-commit evidence checked; no self-verification',len(checked))
