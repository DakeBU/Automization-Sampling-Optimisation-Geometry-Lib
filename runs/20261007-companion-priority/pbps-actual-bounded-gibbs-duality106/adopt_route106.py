from pathlib import Path
import json,hashlib,copy,sys
r=Path(__file__).parent;src=r.parent/'pbps-actual-countable-endpoint105/next-primary106';sys.path.insert(0,str(Path.cwd()/'tools'));import astis_publication as pub;import astis_semantic_roundtrip as rt
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def ref(p):return {'path':p.as_posix(),'raw_sha256':sha(p.read_bytes())}
proposal=r/'source-route106/direct-marginal-overlay106.proposal.native.json';admission=r/'independent-whole-math106/route-topology106/route-topology-admission106.native.json';d=load(admission);assert d['decision']=='ACCEPT_MINIMAL_SELECTED_DIRECT_MARGINAL_OVERLAY';assert d['proposal']['raw_sha256']==sha(proposal.read_bytes())
o=load(proposal);base=Path(o['base_graph']['path']);assert sha(base.read_bytes())==o['base_graph']['raw_sha256'];g=load(base);g['new_edges']+=o['new_edges'];g['AND_route_alternatives']=o['AND_route_alternatives'];g['effective_counts']=o['counts_if_admitted'];g['original_graph']=ref(base);g['independently_admitted_overlay']=ref(proposal);g['independent_overlay_admission']=ref(admission);g['topology_status']='INDEPENDENTLY_ACCEPTED_SOURCE_ROUTES_WITH_SELECTED_DIRECT_MARGINAL_ALTERNATIVE';g['proof_credit']=False
out=r/'source-graph106.effective.json';assert not out.exists();save(out,g)
cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-bounded-gibbs-duality.json');pp=Path('website/content/publications/pbps-actual-bounded-gibbs-duality.json');ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualBoundedGibbsDuality.json')
for p,label in [(cp,'cell'),(pp,'publication'),(ap,'audit')]:
 z=r/(label+'-before-route-overlay106.exactraw.snapshot.json');assert not z.exists();z.write_bytes(p.read_bytes())
cell=load(cp);publication=load(pp);audit=load(ap);packet=rt.decoder_packet(audit)
for x in [cell,publication['items'][0]]:
 x['source_proof_coverage'].update(source_graph=out.as_posix(),coverage_report=admission.as_posix(),coverage_status='Independent prospective topology plus separately admitted direct-marginal route:62 nodes123 edges; compiled final source coverage pending.',route_overlay=ref(proposal),independent_route_admission=ref(admission))
cell['evidence']['selected_invariance_route']=ref(r/'selected-invariance-route106.json');save(cp,cell);save(pp,publication);pub.inputs.cache_clear();pub.load.cache_clear();item=publication['items'][0];audit['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs());audit['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs());assert rt.decoder_packet(audit)==packet;save(ap,audit)
save(r/'route-overlay-adoption106.json',{'effective_graph':ref(out),'proposal':ref(proposal),'independent_admission':ref(admission),'original_seal_unchanged':True,'decoder_packet_unchanged':True,'production_RAW':sha(Path('AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedGibbsDuality.lean').read_bytes()),'publication_binding':audit['publication_binding_sha256']});print('Admitted exact route overlay; frozen header/decoder/production unchanged.')
