from pathlib import Path
import hashlib,json
r=Path(__file__).parent;pre=Path('runs/20261007-companion-priority/pbps-process-regularity-preread82')
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
checked=[]
def verify(x):
 if isinstance(x,dict):
  h=x.get('RAW_sha256',x.get('raw_sha256'))
  if h and x.get('path'):
   p=Path(x['path']);b=p.read_bytes();assert sha(b)==h,(p,h,sha(b));checked.append(str(p))
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
files={r/'header-review82/closed-manifest82.json':'',r/'header-review82/topology-closed-manifest82.json':'afe3d29fed626ff2f46f6c4fdb47ed19003ac4f0ab7555687e9395e814ae4e0c',pre/'header-source-review82/header-source-review82.raw-manifest.json':'945fc4880bdb821af00a3e131427118e4ec48174d79753c1a9c76d53b3af9fb8',pre/'header-source-review82/topology-title-ack82.raw-manifest.json':'27e8096af588b09cc1b3267e490cd00f0f90cd9b4ca73711fb7151d09e8c9a24'}
pins=[]
for p,h in files.items():
 b=p.read_bytes();assert not h or sha(b)==h;verify(load(p));pins.append(dict(path=p.as_posix(),RAW_sha256=sha(b),RAW_bytes=len(b)))
math=load(r/'header-review82/decision82.json');src=load(pre/'header-source-review82/header-source-review82.result.json');top=load(r/'header-review82/topology-review82.json');ack=load(pre/'header-source-review82/topology-title-ack82.json')
assert math['status']=='ACCEPTED_EXACT_PROSPECTIVE_HEADER_MATH_AND_TYPE' and not math['repair_required']
assert src['verdict']=='source-compatible-with-explicit-bounded-refinement' and not src['blocking_deltas']
assert top['status'].startswith('ACCEPTED_SCOPED_TOPOLOGY')
assert ack['title_only_correction']['confirmed'] and not ack['title_only_correction']['mathematical_change']
assert not ack['optional_route_confirmation']['required_for_basic_smalltime_limit']
out=r/'independent-review-adoption82.json';assert not out.exists()
out.write_text(json.dumps(dict(accepted=True,scope='Prospective exact header only; independent mathematics/type/source and distinct primary-first topology; no BODY proof credit.',manifest_RAW_pins=pins,all_native_RAW_pins_rechecked=True,checked_artifact_count=len(checked),reviewed_title_overlay=ack['title_only_correction'],optional_cap_route=ack['optional_route_confirmation'],six_source_standing_binders_retained=True,proof_started=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Independent prospective header/math/source/topology native RAWs accepted; no proof credit',len(checked))
