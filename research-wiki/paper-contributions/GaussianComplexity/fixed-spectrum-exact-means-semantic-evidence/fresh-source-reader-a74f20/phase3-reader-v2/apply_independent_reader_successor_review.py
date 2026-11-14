from pathlib import Path
import hashlib,json,subprocess,sys,copy,tarfile
sys.dont_write_bytecode=True;sys.path.insert(0,'tools')
import astis_publication as pub
import astis_semantic_roundtrip as rt
W=Path('.astis/semantic-neutral-20261110/src_a74f20');F=W/'phase3-reader-v2';E=Path('research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-exact-means-semantic-evidence')
sha=lambda b:hashlib.sha256(b).hexdigest();dump=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
def ref(p):return {'path':str(p),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
def put(p,b):assert not p.exists(),p;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
assert subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()=='64922804e1f7f0927e85bb6a26aeb24d06eea6f7'
assert not subprocess.check_output(['git','diff','HEAD','--name-only']).strip()
assert sha((F/'freeze-manifest.json').read_bytes())=='ad5dabffdb02fc67718a0277bcd40491204c37044dadce967e83345d0c96ffe8'
proposal=F/'canonical-audit-four-field-proposal.json';assert sha(proposal.read_bytes())=='69262bbe7d57b13a7a2ecd98eeeaeaab87e4513e80146d5c24d197c1866d230f'
assert sha((F/'review-run.json').read_bytes())=='52c8c7c1f532cd570bb3687a1fd38664680b450150fb97f456bca136a0eef770'
expected={'phase1':'5afcacc0ea702615faed565f8b99ed770d712c9839c1bedde12f9bd7ca4591db','phase2':'74b7234b3956027167581a37b3f8ddbf59ca62cfdf2a962490d9a548fa31a7ad','phase3':'4932582ef2ff7976624eaf2672910a11aeb447292b1a72e1f84e9b63a67ff621','phase3-reader-v2':'ad5dabffdb02fc67718a0277bcd40491204c37044dadce967e83345d0c96ffe8'}
for folder,h in expected.items():
 p=W/folder/'freeze-manifest.json';assert sha(p.read_bytes())==h
 for row in json.loads(p.read_bytes())['files']:
  f=Path(row['path']);assert sha(f.read_bytes())==row['sha256'] and f.stat().st_size==row['bytes'],f
ap=Path('research-wiki/semantic-roundtrip/audits/huanjian-fixed-spectrum-exact-means.json');old=ap.read_bytes();a=json.loads(old);p=json.loads(proposal.read_bytes())
assert set(p)=={'semantic_slots','deltas','verdict','source_review'}
assert a['state']=='blind-reconstructed' and a['source_review']=={'state':'pending'}
sr=p['source_review'];assert sr['state']=='accepted' and sr['reviewer']=='/root/source_reader_a74f20'
assert sr['publication_binding_sha256']==a['publication_binding_sha256']=='782a2b00ab19c7773c613a275c9371427951632b4f1b1cb974490af25ff70816'
assert sr['reviewer_packet_sha256']=='a5ad7c23afaa9804cdf88c8794e63304d3ed287ff33f0958794fa32190526040'
assert sr['checked_commit']=='64922804e1f7f0927e85bb6a26aeb24d06eea6f7' and sr['source_native_evidence_commit']=='d823dddd8b7f203af3191b94ba2eb763fc0edc9b'
assert sr['fresh_native_at_checked_successor'] is False and sr['static_reader_status']=='ACCEPT_EXACT_SUCCESSOR_BOUNDED_STATIC_REPAIR'
assert sr['review_run_sha256']==sha((F/'review-run.json').read_bytes())
ledger=Path('runs/substantive_advances.jsonl').read_bytes()
out=E/'fresh-source-reader-a74f20/phase3-reader-v2'
files={F/'freeze-manifest.json'}|{Path(row['path']) for row in json.loads((F/'freeze-manifest.json').read_bytes())['files']}
archive=out/'exact-reader-successor-frozen-inputs-and-review.lossless.tar.gz';assert not archive.exists();archive.parent.mkdir(parents=True,exist_ok=True)
with tarfile.open(archive,'w:gz',dereference=True) as t:
 for f in sorted(files):t.add(f,arcname=str(f),recursive=False)
with tarfile.open(archive,'r:gz') as t:
 for f in files:assert t.extractfile(str(f)).read()==f.read_bytes()
put(out/'archive-manifest.json',dump({'archive':ref(archive),'files':[ref(f) for f in sorted(files)],'scope':'Exact29 frozen successor inputs/review/tooling files plus freeze; source/native d823 evidence reused with original HOLD unchanged. No new native/browser/API/sourceV/STAB.'}))
for n in ['freeze-manifest.json','canonical-audit-four-field-proposal.json','review-run.json','independent-successor-review.md','static-reader-checks.json','prior-freezes-reuse-check.json','static-fixture-scope.json']:
 put(out/n,(F/n).read_bytes())
preserved={k:copy.deepcopy(a[k]) for k in ['source','lean','reconstruction','repairs','publication_binding_sha256','publication_context']}
a.update(copy.deepcopy(p));a['state']='source-reviewed';assert all(a[k]==v for k,v in preserved.items());assert rt.semantic_reviewer_packet(a)['packet_sha256']==sr['reviewer_packet_sha256']
put(out/'audit-before-exact-proposal-application.raw.json',old);ap.write_bytes(dump(a));pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
mp=E/'source-to-lean-map-v1.json';m=json.loads(mp.read_bytes());m['prior_map']=ref(mp);m['independent_whole_module_and_correspondence_review']={'reviewer':sr['reviewer'],'checked_current_reader_commit':sr['checked_commit'],'actual_fresh_native_commit':sr['source_native_evidence_commit'],'review_run_sha256':sr['review_run_sha256'],'scope':'Selected actual closed means, all private providers/def/generated auxiliaries, real normalized-bias consumer and bounded current static reader accepted. Canonical prerequisite source reviews reused, uniform alternative unselected, source graph remains independent of compiled graph.'}
# Correct only genuinely stale locator lines, without inventing source-proof nodes.
corrections=[]
for key,row in m['nodes'].items():
 f=Path(row['file']);line=next(i+1 for i,s in enumerate(f.read_text().splitlines()) if row['provider'] in s)
 if line!=row['line']:corrections.append({'node':key,'old':row['line'],'new':line});row['line']=line
m['line_locator_corrections']=corrections;put(E/'source-to-lean-map-v2-reviewed.json',dump(m))
capold=E/'local-proof-capsule.json';cap=json.loads(capold.read_bytes());cap['state']='PROVED_LOCAL_INDEPENDENT_SOURCE_WHOLE_MODULE_STATIC_READER_ACCEPTED_NORMAL_SOURCE_V_PENDING';cap['prior_capsule']=ref(capold);cap['source_to_lean_map']=ref(E/'source-to-lean-map-v2-reviewed.json');cap['independent_source_review']=sr;cap['root_normal_sourceV_calls']=0;put(E/'local-proof-capsule-v2-reviewed.json',dump(cap))
cp=Path('research-wiki/frontier-cells/ASTIS-SW-GAUSSIAN-COMPLEXITY-fixed-spectrum-exact-means.json');oldc=cp.read_bytes();c=json.loads(oldc);assert c['status']=='proved_locally';put(out/'frontier-before-accepted-review-projection.raw.json',oldc)
c['evidence']['independent_source_review']={'reviewer':sr['reviewer'],'checked_reader_commit':sr['checked_commit'],'actual_fresh_native_commit':sr['source_native_evidence_commit'],'reviewer_packet_sha256':sr['reviewer_packet_sha256'],'review_run_sha256':sr['review_run_sha256'],'accepted_report':str(out/'independent-successor-review.md'),'canonical_audit_proposal':ref(out/'canonical-audit-four-field-proposal.json'),'normal_sourceV_transition':'pending; not executed by root'};c['evidence']['local_proof_capsule']=str(E/'local-proof-capsule-v2-reviewed.json');c['statement_seal']['status']='EXACT_ORIGINAL_SIGNATURES_INDEPENDENT_SOURCE_WHOLE_MODULE_STATIC_READER_ACCEPTED_NORMAL_SOURCE_V_PENDING';c['source_proof_coverage']['source_to_lean_map']=ref(E/'source-to-lean-map-v2-reviewed.json');c['source_detail_audit']['gap']='Selected actual closed C8 means and normalized-bias/mean-upper consumer independently accepted with exact current code folds and linked Test source. Normal sourceV, latest-main shared integration, rendered desktop/mobile/graph, remote and purification remain pending; variances/exponential bias/adaptive laws/main bounds remain open.'
cp.write_bytes(dump(c));assert Path('runs/substantive_advances.jsonl').read_bytes()==ledger
put(out/'exact-application-record.json',dump({'proposal':ref(proposal),'public_proposal':ref(out/'canonical-audit-four-field-proposal.json'),'audit_after':ref(ap),'four_fields_applied_exactly':True,'source_Lean_reconstruction_repairs_context_preserved':True,'normal_state':'PROVED_LOCAL','root_sourceV_API_calls':0,'current_reader_checked_commit':sr['checked_commit'],'actual_fresh_native_commit':sr['source_native_evidence_commit'],'new_native_browser_STAB_or_remote_claim':False,'source_map_locator_corrections':corrections}))
print(json.dumps({'audit_state':a['state'],'audit_sha256':sha(ap.read_bytes()),'source_review_state':sr['state'],'four_independent_fields_applied_exactly':True,'root_normalV_calls':0,'normal_state':'PROVED_LOCAL','map_locator_corrections':len(corrections)}))
