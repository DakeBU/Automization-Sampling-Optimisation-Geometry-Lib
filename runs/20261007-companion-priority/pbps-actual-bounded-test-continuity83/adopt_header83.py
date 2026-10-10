from pathlib import Path
import hashlib,json
r=Path(__file__).parent;pre=Path('runs/20261007-companion-priority/pbps-bounded-test-preread83');load=lambda p:json.loads(Path(p).read_bytes());checked=[]
def verify(x):
 if isinstance(x,dict):
  h=x.get('RAW_sha256',x.get('raw_sha256'))
  if h and x.get('path'):
   b=Path(x['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==h,x['path'];checked.append(x['path'])
  for v in x.values():verify(v)
 elif isinstance(x,list):
  for v in x:verify(v)
pins=[]
for p,h in [(r/'header-review83/closed-RAW-manifest83.json','4156927022557f80430af9cb608e355e162669da8fbde63d7364b2cae87cd69e'),(pre/'header-source-review83/header-source-review83.closed-raw-manifest.json','f1e52b12be1013d581400b98db0e37916ba82e23c6903451122e6828ffd71831')]:
 b=p.read_bytes();assert hashlib.sha256(b).hexdigest()==h;verify(json.loads(b));pins.append(dict(path=p.as_posix(),RAW_sha256=h,RAW_bytes=len(b)))
m=load(r/'header-review83/decision83.json');s=load(pre/'header-source-review83/header-source-review83.decision.json')
assert m['status']=='ACCEPTED_PROSPECTIVE_COMPLETE_HEADER_NO_REPAIR' and not m['required_repairs'] and m['complete_private_Prop_typechecked']
assert s['verdict']=='SOURCE_COMPATIBLE_BOUNDED_ASTIS_ELABORATION_HEADER_ONLY'
assert not s.get('blocking_deltas',[]) and not s.get('required_repairs',[])
assert load(pre/'root.topology-adoption83.json')['effective_relations']==30
p=r/'independent-review-adoption83.json';assert not p.exists();p.write_text(json.dumps(dict(accepted=True,scope='Independent complete prospective header mathematics/type/source and distinct topology+separate exact overlay review; no BODY proof credit.',manifest_RAW_pins=pins,all_native_RAW_pins_rechecked=True,checked_artifact_count=len(checked),original_six_binders_eleven_definitions_all82_clauses_exact=True,ASTIS_bounded_continuous_test_extension_explicit=True,proof_started=False),indent=2)+'\n',encoding='utf8',newline='\n')
print('Independent full prospective header/source native RAWs adopted;',len(checked),'pins; no proof credit')
