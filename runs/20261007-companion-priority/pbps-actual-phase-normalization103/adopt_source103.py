from pathlib import Path
import json,hashlib,sys,copy
r=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_semantic_roundtrip as rt
import astis_publication as pub
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPhaseNormalization.json')
a=load(ap);assert a['state']=='draft'
native=r/'final-source103/source-review103.native.json';v=load(native)
assert v['verdict'] in ['equivalent','equivalent-after-elaboration']
assert v['source_review']['state']=='accepted' and not any(d.get('blocking') for d in v['deltas'])
assert not v['repairs']
assert v['reviewer_packet_sha256']==rt.semantic_reviewer_packet(a)['packet_sha256']
assert v['publication_binding_sha256']==a['publication_binding_sha256']
assert sha(Path(v['source_review']['run_artifact']).read_bytes())==v['review_run_sha256']
before=r/'audit-before-source103.json';assert not before.exists();before.write_bytes(ap.read_bytes())
for k in ['semantic_slots','deltas','verdict','repairs','source_review']:a[k]=copy.deepcopy(v[k])
a['source_review']['native_evidence_summary']=a['source_review']['evidence']
a['source_review']['evidence']=native.as_posix();a['state']='accepted'
save(ap,a)
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
save(r/'source-admission103.json',dict(source_native=native.as_posix(),source_native_RAW_sha256=sha(native.read_bytes()),run_RAW_sha256=v['review_run_sha256'],publication_binding_sha256=a['publication_binding_sha256'],reviewer_packet_sha256=v['reviewer_packet_sha256'],canonical_audit_RAW_sha256=sha(ap.read_bytes()),state='accepted',VERIFIED=False))
print('Native independent source decision transferred exactly; exact-commit admission remains pending.')
