from pathlib import Path
import json,hashlib,sys
r=Path(__file__).resolve().parent.relative_to(Path.cwd().resolve());sys.path.insert(0,str(Path.cwd()/'tools'));import astis_publication as pub
load=lambda p:json.loads(Path(p).read_bytes())
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
c=load(r/'claim.json');ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualL2Expectation.json');a=load(ap);assert a['state']=='accepted'
cp=Path('research-wiki/frontier-cells')/(c['frontier_cell']+'.json');pp=Path('website/content/publications/pbps-actual-l2-expectation.json');coverage=r/'final-source107/compiled-source-coverage107.native.json';assert coverage.exists()
for p,label in [(cp,'cell'),(pp,'publication')]:
 q=r/(label+'-before-compiled-coverage107.exactraw.snapshot.json');assert not q.exists();q.write_bytes(p.read_bytes())
cell=load(cp);p=load(pp)
for obj in [cell,p['items'][0]]:
 obj['source_proof_coverage']['coverage_report']=coverage.as_posix()
 obj['source_proof_coverage']['coverage_status']='Independently accepted compiled source coverage; full paper boundaries remain open.'
save(cp,cell);save(pp,p);pub.inputs.cache_clear();pub.load.cache_clear();item=p['items'][0];assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==a['publication_binding_sha256'];pub.check_advance(c['target_declarations'],reviewed=True)
save(r/'compiled-coverage-transfer107.json',dict(final_coverage=coverage.as_posix(),RAW_sha256=hashlib.sha256(coverage.read_bytes()).hexdigest(),publication_binding_unchanged=True,source_review_unchanged=True,original_reviewed_publication_and_cell_RAW_saved=True));print('Compiled coverage pointers transferred without altering semantic binding.')
