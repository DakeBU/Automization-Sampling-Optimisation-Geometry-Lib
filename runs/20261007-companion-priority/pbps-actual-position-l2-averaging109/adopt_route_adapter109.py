from pathlib import Path
import copy,hashlib,json,sys
r=Path(__file__).parent;sys.path.insert(0,str(Path.cwd()/'tools'));import astis_publication as pub;import astis_semantic_roundtrip as rt
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
decision=Path(sys.argv[1]);d=load(decision);assert d.get('decision','').startswith('ACCEPT'),d
assert d.get('reviewer')=='/root/blind_decoder106'
proposal=r/'route-adapter109/route-adapter-proposal109.native.json';v=load(proposal)
assert sha(proposal.read_bytes())=='71c00d981894e0b24da6def9020c6e1a520e6852dd1acb03c17981c7bd59401c'
assert '71c00d981894e0b24da6def9020c6e1a520e6852dd1acb03c17981c7bd59401c' in decision.read_text(encoding='utf8')
for key in ['proposed_graph','coverage_overlay','production','sealed_header_unchanged','pinned_API_evidence']:
 x=v[key];assert sha(Path(x['path']).read_bytes())==x['raw_sha256']
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualPositionL2Averaging.json');a=load(ap);before_packet=rt.decoder_packet(a)
cp=Path('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-position-l2-averaging.json');pp=Path('website/content/publications/pbps-actual-position-l2-averaging.json');cell=load(cp);p=load(pp)
for path,label in [(cp,'cell'),(pp,'publication'),(ap,'audit')]:
 snap=r/(label+'-before-adapter109.exactraw.json');assert not snap.exists();snap.write_bytes(path.read_bytes())
for obj in [cell,p['items'][0]]:
 cov=obj['source_proof_coverage'];cov['sealed_prospective_source_graph']=copy.deepcopy(cov['source_graph']);cov['source_graph']=v['proposed_graph']['path'];cov['coverage_report']=v['coverage_overlay']['path'];cov['implementation_adapter_admission']=decision.as_posix();cov['coverage_status']='Independently reviewed namespace and L1-indicator adapter; original sealed graph and header retained. Final compiled source coverage pending.'
save(cp,cell);save(pp,p);pub.inputs.cache_clear();pub.load.cache_clear();item=p['items'][0]
a['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs());a['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs());assert rt.decoder_packet(a)==before_packet;save(ap,a)
packet=rt.semantic_reviewer_packet(a);out=r/'reviewer109.input.json';assert not out.exists();save(out,packet)
save(r/'route-adapter-admission109.json',dict(proposal=proposal.as_posix(),proposal_raw_sha256=sha(proposal.read_bytes()),independent_decision=decision.as_posix(),independent_decision_raw_sha256=sha(decision.read_bytes()),production_unchanged=True,statement_seal_unchanged=True,blind_packet_unchanged=True,publication_binding_sha256=a['publication_binding_sha256'],reviewer_packet_sha256=packet['packet_sha256']))
print(json.dumps(dict(packet=out.as_posix(),packet_sha256=packet['packet_sha256'],publication_binding_sha256=a['publication_binding_sha256'])))
