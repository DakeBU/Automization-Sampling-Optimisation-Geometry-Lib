from pathlib import Path
import gzip,hashlib,json,subprocess,sys,tarfile
sys.dont_write_bytecode=True
sys.path.insert(0,'tools');import astis_publication as pub;import astis_semantic_roundtrip as rt
W=Path('.astis/semantic-neutral-20261109/src_82a91d')
E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-grid-alias-semantic-evidence')
sha=lambda b:hashlib.sha256(b).hexdigest()
dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def ref(p):
 b=p.read_bytes();return {'path':str(p),'sha256':sha(b),'bytes':len(b)}
def put(p,b):
 assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='93a7005b3e861ddc58484fb3a21abd83ad44722b'
assert not subprocess.check_output(['git','diff','HEAD','--name-only']).strip()
F=W/'phase3-successor';assert sha((F/'FREEZE.json').read_bytes())=='5af2348f0fbcd2d15fb8e95f59a4e803c6484c53ea1f6d45a70f274a27ede95b'
proposal=F/'canonical-audit-update-proposal.json';assert sha(proposal.read_bytes())=='9928c983a96785c105fff93a6311b05fc0a79d35aa877a39ca6b6e61445d2eb5'
for base in [W/'phase1',W/'phase2',W/'phase3',F]:
 for row in json.loads((base/'FREEZE.json').read_text())['files']:
  p=base/row['path'];assert sha(p.read_bytes())==row['sha256'] and p.stat().st_size==row['bytes'],p
out=E/'fresh-source-reader-82a91d';out.mkdir()
payload=[p for p in sorted(W.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
archive=out/'all-phases-exact-inputs-runtime-HOLD-and-successor.lossless.tar.gz'
with tarfile.open(archive,'w:gz',dereference=True) as t:
 for p in payload:t.add(p,arcname=str(p),recursive=False)
with tarfile.open(archive,'r:gz') as t:
 for p in payload:assert t.extractfile(str(p)).read()==p.read_bytes(),p
put(out/'archive-manifest.json',dump({'archive':ref(archive),'files':[ref(p) for p in payload],'scope':'Actual independent source cognition, filename-exposure limitation, blind statement comparison, cbf3 fresh native proof/runtime, reader HOLD and93a exact accepted exposition successor. No sourceV/API/aggregate/site/UI/remote or Goal claim.'}))
for base,names in [(W/'phase1',['FREEZE.json','source-cognition.md','raw-input-exposure-manifest.json']),(W/'phase2',['FREEZE.json','decision.json','semantic-review.md']),(W/'phase3',['FREEZE.json','decision.json','review-report.md']),(F,['FREEZE.json','decision.json','review-report.md','canonical-audit-update-proposal.json','comparison-checks.json','final-verification-receipt.json'])]:
 for n in names:put(out/base.name/n,(base/n).read_bytes())
ap=Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-grid-alias.json');old=ap.read_bytes();a=json.loads(old);p=json.loads(proposal.read_text())
assert set(p)=={'id','state','semantic_slots','deltas','verdict','source_review','repairs','publication_binding_sha256','publication_context'}
assert p['id']==a['id'] and p['state']=='source-reviewed' and p['source_review']['state']=='accepted'
assert p['source_review']['reviewer']=='/root/source_reader_82a91d' and p['source_review']['review_run_sha256']=='2f6adfb5ca211aa4d480b28750734f84e917d6ff16358e60ca53f5516f4aef62'
assert p['publication_binding_sha256']==a['publication_binding_sha256']=='c7b557be6ccb8b31fb252c496a4f5535d950fddd8ff3d06a6029527cbdee3f5d'
assert p['publication_context']==a['publication_context']
before_source=a['source'];before_lean=a['lean'];before_reconstruction=a['reconstruction']
for k,v in p.items():a[k]=v
assert a['source']==before_source and a['lean']==before_lean and a['reconstruction']==before_reconstruction
assert rt.semantic_reviewer_packet(a)['packet_sha256']=='f381a1ca1e1aa488cc8cc259e0bae1f9d00a2b391e9ff4966cc64e0ae57875bb'
put(out/'audit-before-applying-exact-independent-proposal.raw.json',old)
ap.write_bytes(dump(a))
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
cp=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-grid-alias.json');old_c=cp.read_bytes();c=json.loads(old_c);assert c['status']=='proved_locally'
put(out/'frontier-before-source-review-projection.raw.json',old_c)
c['evidence']['independent_source_review']={'reviewer':'/root/source_reader_82a91d','checked_reader_commit':'93a7005b3e861ddc58484fb3a21abd83ad44722b','actual_fresh_Lean_core_commit':'cbf3c22b901a484c463f417a3e206bb200622294','same_production_Test_bytes':True,'reviewer_packet_sha256':p['source_review']['reviewer_packet_sha256'],'review_run_sha256':p['source_review']['review_run_sha256'],'accepted_report':str(out/'phase3-successor/review-report.md'),'actual_native_report':str(out/'phase3/review-report.md'),'canonical_audit_proposal':ref(out/'phase3-successor/canonical-audit-update-proposal.json'),'normal_sourceV_transition':'pending; not executed by root'}
c['evidence']['reader_definition_successor']['state']='EXACT_INDEPENDENT_STATIC_READER_SUCCESSOR_ACCEPTED_NORMAL_SOURCE_V_PENDING'
c['statement_seal']['status']='EXACT_ORIGINAL_SIGNATURES_INDEPENDENT_SOURCE_WHOLE_MODULE_STATIC_READER_ACCEPTED_NORMAL_SOURCE_V_PENDING'
cp.write_bytes(dump(c))
put(out/'applied-independent-review-record.json',dump({'proposal':ref(proposal),'public_exact_proposal_copy':ref(out/'phase3-successor/canonical-audit-update-proposal.json'),'audit_after':ref(ap),'source_lean_reconstruction_fields_preserved':True,'reviewed_publication_binding':p['publication_binding_sha256'],'actual_new_Lean_or_UI_or_sourceV_credit':False,'normal_state_remains':'PROVED_LOCAL','runtime_core_commit':'cbf3c22b901a484c463f417a3e206bb200622294','reader_reviewed_commit':'93a7005b3e861ddc58484fb3a21abd83ad44722b'}))
print(json.dumps({'audit_state':a['state'],'source_review_state':a['source_review']['state'],'audit_sha256':sha(ap.read_bytes()),'proposal_applied_exactly':True,'normal_sourceV_called_by_root':False,'normal_state':'PROVED_LOCAL'}))
