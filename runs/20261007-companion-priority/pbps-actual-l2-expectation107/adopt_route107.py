from pathlib import Path
import hashlib, json, sys

r = Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
sys.path.insert(0, str(Path.cwd()/'tools'))
import astis_publication as pub
import astis_semantic_roundtrip as rt
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
ref = lambda p: dict(path=p.as_posix(),raw_sha256=sha(p.read_bytes()))
save = lambda p,d: p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
proposal=r/'source-route107/quotient-identification107.proposal.native.json'
admission=r/'independent-route107/route-admission107.native.json'
d,o=load(admission),load(proposal)
assert d['decision']=='ACCEPT_EXACT_QUOTIENT_IDENTIFICATION_OR_OVERLAY'
assert d['reviewer']!=o['creator']
assert d['proposal_raw_sha256']==sha(proposal.read_bytes())
base=Path(o['base_graph']['path'])
assert sha(base.read_bytes())==o['base_graph']['raw_sha256']
g=load(base)
g['edges'] += [dict(source=a,target=b,scope='current107-selected-quotient-consequence') for a,b in o['new_edges']]
assert len(g['nodes'])==85 and len(g['edges'])==161
assert len({(e['source'],e['target']) for e in g['edges']})==161
for n in g['nodes']:
    if n['id']=='AE-REP107':
        n['meaning']=o['refined_node_meaning']['meaning']
        n['old_mechanism_preserved_in']=o['refined_node_meaning']['old_mechanism_preserved_in']
old_groups=[x for x in g['AND_groups'] if x['target']=='AE-REP107']
assert len(old_groups)==1
g['superseded_single_route_AND_groups']=old_groups
g['AND_groups']=[x for x in g['AND_groups'] if x['target']!='AE-REP107']
g['AND_route_alternatives']=o['AND_route_alternatives']
g['OR_semantics']=o['OR_semantics']
g['selected_route']='universal-quotient-identification107'
g['counts']=dict(nodes=85,edges=161)
g['original_graph']=ref(base)
g['independently_admitted_overlay']=ref(proposal)
g['independent_overlay_admission']=ref(admission)
g['independent_topology_admission']=True
g['kind']='independently admitted effective source graph107; mathematical route coverage, not new Lean declarations'
out=r/'source-graph107.effective.json'
assert not out.exists()
save(out,g)
cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-l2-expectation.json')
pp=Path('website/content/publications/pbps-actual-l2-expectation.json')
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualL2Expectation.json')
for p,label in [(cp,'cell'),(pp,'publication'),(ap,'audit')]:
    snap=r/(label+'-before-route-overlay107.exactraw.snapshot.json')
    assert not snap.exists()
    snap.write_bytes(p.read_bytes())
cell,publication,audit=load(cp),load(pp),load(ap)
packet=rt.decoder_packet(audit)
for x in [cell,publication['items'][0]]:
    x['source_proof_coverage'].update(source_graph=out.as_posix(),coverage_report=admission.as_posix(),coverage_status='Independent v2 topology plus separately admitted universal-quotient representative-independence alternative:85 nodes161 edges. Compiled final source coverage pending.',route_overlay=ref(proposal),independent_route_admission=ref(admission))
save(cp,cell)
save(pp,publication)
pub.inputs.cache_clear()
pub.load.cache_clear()
item=publication['items'][0]
audit['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs())
audit['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs())
audit['lean']['statement_representation']['kernel_header_and_literal_expansion_checked']=True
audit['lean']['statement_representation']['independent_check']=(r/'independent-whole-math107/whole-math-decision107.native.json').as_posix()
assert rt.decoder_packet(audit)==packet
save(ap,audit)
reviewer=rt.semantic_reviewer_packet(audit)
rp=r/'reviewer-packet107.json'
assert not rp.exists()
save(rp,reviewer)
save(r/'route-overlay-adoption107.json',dict(effective_graph=ref(out),proposal=ref(proposal),independent_admission=ref(admission),original_seal_unchanged=True,decoder_packet_unchanged=True,production_RAW=o['production']['raw_sha256'],publication_binding=audit['publication_binding_sha256'],reviewer_packet=ref(rp),reviewer_packet_sha256=reviewer['packet_sha256']))
print(json.dumps(dict(graph=ref(out),reviewer_packet=ref(rp),canonical_reviewer_packet_sha256=reviewer['packet_sha256'],publication_binding=audit['publication_binding_sha256'])))
