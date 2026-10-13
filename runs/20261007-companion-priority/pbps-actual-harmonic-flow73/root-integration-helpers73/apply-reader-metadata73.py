from pathlib import Path
import hashlib,json,os,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_publication as pub
import astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-actual-harmonic-flow73');o=r/'independent-reader-metadata-repair73'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
can=lambda x:json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def check(z):
 b=Path(z['path']).read_bytes();lf=b.replace(b'\r\n',b'\n');assert len(b)==z['RAW_bytes'] and sha(b)==z['RAW_sha256'] and sha(lf)==z['LF_sha256'],z['path']
 if 'LF_bytes' in z:assert len(lf)==z['LF_bytes']
 return b
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')))
lp=o/'lease.final.json';assert sha(lp.read_bytes())=='e4328779062b83d430eee59aefa82eeb3f49cae0e6518f2fd0089f27b2ac13f8'
l=load(lp);assert l['status']=='CLOSED_LAST' and l['owned_files']==17 and l['reviewer']=='/root/header_math72'
check(l['manifest']);m=load(l['manifest']['path']);rows=m['owned_files'];assert len(rows)==15
assert {p.resolve() for p in o.rglob('*') if p.is_file()}=={Path(z['path']).resolve() for z in rows}|{lp.resolve(),Path(l['manifest']['path']).resolve()}
for z in rows:
 check(z);assert Path(z['path']).stat().st_mtime_ns<=lp.stat().st_mtime_ns
run=load(o/'run.json');h=sha(can({k:v for k,v in run.items() if k!='run_sha256'}));assert h==run['run_sha256']==l['run_sha256']=='6344a0270c950b855a34e5915e4906cf65015dec05e9dd9f32903d4fb915edba'
assert run['checks_terminal']['terminal_EXIT']==0 and run['checks_terminal']['actual_foreground_PID']==46000
assert len(run['inputs'])==27
for z in run['inputs']:check(z)
check(l['complete_named']);check(l['decision']);d=load(l['decision']['path'])
assert d['verdict']=='ACCEPT_EXACT_METADATA_ONLY_PROPOSAL' and d['proposer']!=d['reviewer']
assert d['native_binding_payload_equal'] and d['native_review_context_equal'] and d['native_semantic_reviewer_packet_exact'] and d['native_anonymous_packet_exact']
approved=d['approved_rows'];assert len(approved)==2
names=['website/content/publications/pbps-actual-harmonic-flow.json','research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-harmonic-flow.json']
pointers=['/items/0/purification/dead_code_audit','/purification/dead_code_audit']
for z,name,ptr in zip(approved,names,pointers):
 assert z['canonical_path']==name and z['JSON_pointer']==ptr and check(z['canonical_current'])==check(z['before'])
 assert len(z['exhaustive_JSON_diff'])==1 and z['exhaustive_JSON_diff'][0]['pointer']==ptr
 before=check(z['before']);after=check(z['after']);diff=z['exhaustive_JSON_diff'][0]
 assert before.count(json.dumps(diff['before']).encode())==1
 assert before.replace(json.dumps(diff['before']).encode(),json.dumps(diff['after']).encode(),1)==after
auditp=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualHarmonicFlow.json');audit=load(auditp)
packet=load(r/'source-review.packet.json');assert rt.semantic_reviewer_packet(audit)==packet
item=next(x for x in pub.load() if x['id']=='pbps-actual-harmonic-flow')
binding=pub.binding_digest(item,item['bindings'][0],pub.inputs());context=pub.review_context(item,item['bindings'][0],pub.inputs())
assert binding=='627cae79b09fa7c73f90020fcc85081a9ba134ac778d47871f3a10f4a18250ea' and sha(can(context))=='1722badb9a3f7ec13118dcb9017be0a02276777610ce582769f436bee2bd0370'
unchanged=[pin(p) for p in ['AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean','website/content/declaration_lessons/pbps-actual-harmonic-flow.json',auditp,r/'source-review.packet.json']]
for z in approved:Path(z['canonical_path']).write_bytes(check(z['after']))
pub.load.cache_clear();pub.inputs.cache_clear();item=next(x for x in pub.load() if x['id']=='pbps-actual-harmonic-flow')
assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==binding and pub.review_context(item,item['bindings'][0],pub.inputs())==context
assert rt.semantic_reviewer_packet(load(auditp))==packet
for z in unchanged:check(z)
dest=r/'root.reader-metadata-overlay73.adoption.json';assert not dest.exists()
dest.write_text(json.dumps(dict(status='APPLIED_DISTINCT_REVIEWED_EXACT_TWO_METADATA_FIELDS_ONLY',actual_root_PID=os.getpid(),native_whole_logical_run_sha256=h,native_lease=pin(lp),approved_rows=approved,exact_current=[pin(p) for p in names],unchanged=unchanged,publication_binding_sha256=binding,publication_context_sha256=sha(can(context)),source_packet_sha256=packet['packet_sha256'],mathematical_repair=False,source_review=False,VERIFIED=False,Goal_complete=False),ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS CLOSED17/27inputs: exact2 metadata-only strings applied; module/lesson/audit/binding/context/packet unchanged.')
