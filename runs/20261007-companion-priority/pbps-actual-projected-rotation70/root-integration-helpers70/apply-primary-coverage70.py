from pathlib import Path
import copy,hashlib,json,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_publication as pub
r=Path('runs/20261007-companion-priority/pbps-actual-projected-rotation70');o=r/'independent-source70'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(Path(p).read_bytes())
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def snapshot(p,label):
 q=r/label;assert not q.exists();q.write_bytes(p.read_bytes())
pins={
 'stageA.source-expectations70.before-current-BODY.frozen.json':'a1257be6ef44d34f268e7297044392d3a288c5ddb62f38e67cdab33e70fe6c1f',
 'stageA.source-proof-graph70.frozen.json':'f23f7c687517e9b65de67c549e8cf5e11328d01fea6f8b35236a14679f68dc26',
 'stageA.primary419-NODE-EXCLUDED70.frozen.json':'db38a7ebb0629284461a88bad537795e6d6f98156674f54b93d79e848c6bad62',
 'stageA.exhaustive-finite-obligations70.frozen.json':'0b271370ae5721c98eb3c6c66551ebfacd4cbf82408ba0ac69c67ff2e32c12a3'}
for n,h in pins.items():assert sha((o/n).read_bytes())==h
inventory=load(o/'stageA.primary419-NODE-EXCLUDED70.frozen.json');assert inventory['count']==419 and inventory['counts']=={'NODE':175,'EXCLUDED':244} and inventory['unclassified']==0
assert inventory['current_source_only_promotions']==['A2.SS3.p8.m5','A2.SS3.p8.m6']
cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-projected-rotation.json')
pp=Path('website/content/publications/pbps-actual-projected-rotation.json')
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualProjectedRotation.json')
for p,label in [(cp,'cell.before-primary-coverage70.json'),(pp,'publication.before-primary-coverage70.json'),(ap,'audit.before-primary-coverage70.json')]:snapshot(p,label)
cell=load(cp);coverage=dict(source_graph=(o/'stageA.source-proof-graph70.frozen.json').as_posix(),
 source_inventory=(o/'stageA.primary419-NODE-EXCLUDED70.frozen.json').as_posix(),
 coverage_report=(o/'stageA.exhaustive-finite-obligations70.frozen.json').as_posix(),
 coverage_status='Independent primary-first StageA:419/419 math items,175 NODE244 EXCLUDED,7 RAW regions,22 source nodes49 edges and24 finite obligations. Two actual B4 component-definition consumer anchors newly classified. Current whole BODY/source review pending; this is not a verdict or proof badge.')
cell['source_proof_coverage']=coverage;save(cp,cell)
publication=load(pp);publication['items'][0]['source_proof_coverage']=copy.deepcopy(coverage);save(pp,publication)
pub.inputs.cache_clear();pub.load.cache_clear();item=publication['items'][0];binding=item['bindings'][0]
audit=load(ap);assert audit['state']=='draft'
audit['publication_binding_sha256']=pub.binding_digest(item,binding,pub.inputs())
audit['publication_context']=pub.review_context(item,binding,pub.inputs());save(ap,audit)
dest=r/'primary-coverage70.pre-review-overlay.json';assert not dest.exists()
save(dest,dict(status='PRIMARY_FIRST_EXPECTATION_METADATA_ONLY_WHOLE_SOURCE_REVIEW_PENDING',
 exact_stageA_pins=pins,prior_header_classification_preserved_in_old_native_CLOSED83=True,
 current_NODE=175,current_EXCLUDED=244,source_or_mathematical_statement_changed=False,
 source_verdict=False,stageA_owned_bundle_still_OPEN=True,closed_native_admission_pending=True,
 canonical_Lean_changed=False,formal_Lean_dependency_changed=False))
print('PASS primary-first expected coverage metadata419=175+244 and24 obligations frozen for the subsequent official whole-source packet; no source verdict inferred from OPEN preparation.')
