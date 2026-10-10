from pathlib import Path
import copy,datetime,hashlib,json,sys
R=Path('E:/Samplinglib');r=Path(__file__).parent;sys.path.insert(0,str(R/'tools'))
import astis_publication as pub,astis_semantic_roundtrip as rt
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
def new(p,x):
 assert not p.exists(),p
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def pin(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
d=r/'independent-exposition-repair89'
dp=d/'decision89.native.json';mp=d/'closed-raw-manifest89.json'
assert sha(dp.read_bytes())=='4dc476de282b2754b3fd2ac222c8e0d977fb05556a8b0af886f31850239642e6'
assert sha(mp.read_bytes())=='318e61b2051b906e939e10fde1fb8d034f59577774fad6439a91f9e4a8af5044'
seen=[]
def verify(x):
 if isinstance(x,dict):
  k='raw_sha256' if 'raw_sha256' in x else 'sha256'
  if 'path' in x and k in x:
   p=Path(x.get('closed_snapshot',x['path']));p=p if p.is_absolute() else R/p;b=p.read_bytes()
   assert sha(b)==x[k],p
   if 'bytes' in x:assert len(b)==x['bytes'],p
   seen.append(str(p))
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
verify(load(mp));n=load(dp);verify(n)
assert n['decision']=='ACCEPT_EXACT_ONE_FIELD_EXPOSITION_REPAIR' and n['required_repairs']==[]
lp=R/'website/content/declaration_lessons/pbps-actual-conditional-next-wait-density.json'
pp=R/'website/content/publications/pbps-actual-conditional-next-wait-density.json'
ap=R/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualConditionalNextWaitDensity.json'
p=R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean'
assert sha(lp.read_bytes())=='562710b8e30deeefed6f776ecced00d3fffef15620e29e4b3792fdac460a87ab'
candidate=Path(n['accepted_proposed_lesson']['path']);old=load(lp);updated=load(candidate)
comparison=copy.deepcopy(updated);comparison['units'][0]['steps'][1]['formula']=old['units'][0]['steps'][1]['formula'];assert comparison==old
assert sha(p.read_bytes())=='36813b659cbdbb4b31c6300abd1300858d42afe683046b8c06ff9c22806e8e37'
assert sha(pp.read_bytes())=='7d96cf475f1300cf9e3d95eeacbc936741ec3316eb37ec61575cba3a92a9d66c'
snapshot=r/'audit.before-exposition89.json';assert not snapshot.exists();snapshot.write_bytes(ap.read_bytes())
a=load(ap);before=rt.decoder_packet(a);assert before==load(r/'anonymous.decoder89.json')
lp.write_bytes(candidate.read_bytes())
pub.inputs.cache_clear();pub.load.cache_clear()
item=load(pp)['items'][0];a['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs())
a['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs())
assert rt.decoder_packet(a)==before
ap.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
pub.check_advance([a['lean']['declaration']],reviewed=False)
new(r/'publication-freeze89.after-exposition.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='INDEPENDENT_EXPOSITION_OVERLAY_APPLIED_FINAL_SOURCE_REVIEW_PENDING',inputs=[pin(x) for x in [lp,pp,ap,dp,mp]],module=pin(p),predecessor=pin(r/'publication-freeze89.json'),publication_binding_sha256=a['publication_binding_sha256'],decoder_packet_unchanged=True,only_repaired_pointer=n['accepted_json_pointer'],checked_RAW_descriptors=len(seen),PROVED_LOCAL=False,VERIFIED=False))
new(r/'source-review89.packet.json',rt.semantic_reviewer_packet(a))
print('Exact independently accepted single-field overlay applied; decoder packet unchanged; final source packet frozen.')
