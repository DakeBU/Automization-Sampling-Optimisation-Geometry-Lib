from pathlib import Path
import hashlib,json,tarfile,re,sys
sys.dont_write_bytecode=True;sys.path.insert(0,'tools')
import astis_publication as pub
import astis_semantic_roundtrip as rt
freeze_sha,proposal_sha,run_sha=sys.argv[1:]
W=Path('.astis/huanjian-gc-fixed-spectrum-bias-20261110')
E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-bias-semantic-evidence')
R=Path('.astis/semantic-neutral-20261110/src_c75d42/phase3')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def put(p,b):
    assert not p.exists(),p
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
frozen=R/'freeze-manifest.json'
assert sha(frozen.read_bytes())==freeze_sha
f=json.loads(frozen.read_bytes())
for row in f['files']:
    p=R/row['path'];raw=p.read_bytes()
    assert sha(raw)==row['sha256'] and len(raw)==row['bytes']
files=[]
for p in sorted(R.rglob('*')):
    if p.is_file():
        assert not p.is_symlink() and '__pycache__' not in p.parts
        assert not re.search(rb'wxid_[a-z0-9]{8,}|/Library/Containers/com\.tencent',p.read_bytes())
        files.append(p)
proposal=R/'canonical_audit_field_proposal.json'
assert sha(proposal.read_bytes())==proposal_sha
p=json.loads(proposal.read_bytes())
assert set(p)=={'state','semantic_slots','deltas','verdict','source_review'}
assert p['state'] in {'source-reviewed','accepted'} and p['source_review']['state']=='accepted'
assert p['source_review']['reviewer']=='/root/source_reader_c75d42'
assert p['source_review']['review_run_sha256']==run_sha
assert not [x for x in p['deltas'] if x['severity']=='blocking']
afile=Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-bias.json')
old=afile.read_bytes();a=json.loads(old)
assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a)
assert packet['packet_sha256']==p['source_review']['reviewer_packet_sha256']=='3b3a570d9aa97fb762a3b7d7770e0d3224bcafa07f5dc968a1c58d4df09ae328'
assert a['publication_binding_sha256']=='dc19f64065d955863ba36af4af522399e32a34a952ff8f6d7fb97456da8921eb'
q=E/'fresh-source-reader-c75d42-phase3-full-proof-exposition.lossless.tar.gz'
assert not q.exists()
with tarfile.open(q,'w:gz') as t:
    for path in files:t.add(path,arcname=str(path.relative_to(R)),recursive=False)
with tarfile.open(q,'r:gz') as t:
    for path in files:assert t.extractfile(str(path.relative_to(R))).read()==path.read_bytes()
put(E/'canonical-audit-before-exact-independent-source-review.raw.json',old)
for key,value in p.items():a[key]=value
for key in set(json.loads(old))-set(p):assert a[key]==json.loads(old)[key]
afile.write_bytes(dump(a))
put(E/'exact-independent-source-audit-proposal.json',proposal.read_bytes())
record={'scope':'Apply ONLY exact5 frozen independent source-audit fields; no source/Lean/reconstruction/context/repair change and NO normal VERIFIED API.','actor':'/root/source_reader_c75d42','proposal_sha256':proposal_sha,'source_review_run_sha256':run_sha,'source_freeze_sha256':freeze_sha,'archive':{'path':str(q),'sha256':sha(q.read_bytes()),'bytes':q.stat().st_size},'applied_fields':sorted(p),'audit_sha256_after':sha(afile.read_bytes()),'mathematical_checked_commit':'300fb6f3e680f5a4585fee2bcf57d1005d57f1fa','native_static_execution':'Separate independent module/native/static reader f35b7d, exact300; source c75 does not claim to have rerun those checks.','native_module_freeze_sha256':'26a5b00f08bddbf3e13c62e495e0ab268eaad341ef6204a2fce1a291a278eb2f','normal_sourceV_pending':True}
put(E/'exact-independent-source-review-application.json',dump(record))
cp=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-bias.json')
c=json.loads(cp.read_bytes());assert c['status']=='proved_locally'
c['evidence']['independent_verification']='Fresh raw-first c75 seven-slot and whole-module/source-map/exposition review accepted the selected exponential-bias slice plus explicitly private local zero-threshold probability application. Separate f35b7d real Lean/native/kernel/static review passed exact300. Normal sourceV remains pending; no latest-main/global/site/browser/public/purification/whole-Goal acceptance.'
c['evidence']['source_review_application']=str(E/'exact-independent-source-review-application.json')
c['evidence']['independent_native_module_static']=str(E/'independent-module-native-static-reader-74e2d8-manifest.json')
c['source_detail_audit']['gap']='Selected actual exponential-bias proof and private zero-threshold application independently source/proof-reviewed. Full original nonzero-threshold detector, rotation/query/domain guards, both main lower bounds and publication/purification remain open. Normal sourceV is a separate pending transition.'
cp.write_bytes(dump(c))
pub.inputs.cache_clear();pub.load.cache_clear()
pub.check_advance([a['lean']['declaration']],reviewed=True)
print(json.dumps({'state':p['state'],'audit_sha256':sha(afile.read_bytes()),'proposal_sha256':proposal_sha,'sourceV':False,'archive':record['archive']}))
