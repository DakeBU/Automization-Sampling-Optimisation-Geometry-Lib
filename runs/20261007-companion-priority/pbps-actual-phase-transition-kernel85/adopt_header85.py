from pathlib import Path
import hashlib,json
r=Path(__file__).parent
load=lambda p:json.loads(Path(p).read_bytes())
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=hashlib.sha256(b).hexdigest())
def verify(x):
 if isinstance(x,dict):
  h=x.get('RAW_sha256',x.get('raw_sha256'))
  if 'path' in x and h:
   a=pin(x['path']);assert a['RAW_sha256']==h,x['path']
   n=x.get('RAW_bytes',x.get('bytes'))
   if n is not None:assert a['RAW_bytes']==n,x['path']
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
inputs=[]
def checked(name,h):
 p=r/name;assert pin(p)['RAW_sha256']==h,p
 x=load(p);verify(x);inputs.append(pin(p));return x
checked('header-math85/closed-RAW-manifest85.json','8904074b228159edf543efeae16800d107d44bcaf4611312929c807e3e040e33')
checked('header-source85/run-manifest85.json','952a8057eec337bb6408097a4f4007a837373165f3d65dee16e021b7ca1f1645')
m=checked('header-math85/decision85.json','9d0b5ba8bce63f366d760bfe4ef6757a2fabdf27aff33eeff901733a9875794a')
s=checked('header-source85/decision85.json','aaf87c82a03dfe3720a7adf480721e3757ab89dbbceddb3fe28359187913dec6')
assert m['status']=='ACCEPTED_PROSPECTIVE_FULL_PROP_MATHEMATICS_AND_TYPE_ONLY'
assert not m['required_repairs'] and not m['blocking_issues'] and m['header_repair_overlay'] is None
assert m['original_full_header_exit_code']==m['local_full_header_API_exit_code']==0
assert s['verdict']=='ACCEPT_PROSPECTIVE_SOURCE_SCOPE' and not s['blocking_deltas'] and not s['required_mathematical_repairs'] and not s['proposed_repairs']
assert s['coverage_counts']==dict(inventory=16,nodes=21,relations=29,dependencies=26,excluded_associations=3,header_lines=100,literal_definitions=11,gaps=0)
header=r/'header85.proposed.lean';assert pin(header)['RAW_sha256']=='b2e1c43e0f7d3877096546181f06e10177486cf126bc98df16d201d5b040bb04'
inputs.append(pin(header))
target=r/'independent-review-adoption85.json';assert not target.exists()
target.write_text(json.dumps(dict(accepted=True,accepted_header=pin(header),frozen_native_inputs=inputs,whole_header_mathematics_and_type=True,whole_header_source_and_coverage=True,repair_required=False,original_header_unchanged=True,reviewer_only_API_negative_retained=True,StatementSeal=False,proof_BODY_created=False,VERIFIED=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('85 full original header math/type/source adopted; no repair, no proof credit')
