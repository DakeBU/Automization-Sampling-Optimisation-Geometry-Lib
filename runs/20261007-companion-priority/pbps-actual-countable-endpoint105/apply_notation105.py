from pathlib import Path
import json,hashlib,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_publication as pub
import astis_semantic_roundtrip as rt
r=Path(__file__).parent;d=r/'exposition-notation-repair105'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
proposal=load(d/'proposal105.json')
decision_path=d/'independent-review/decision105.native.json'
v=load(decision_path)
assert v.get('decision',v.get('verdict'))=='ACCEPT_AUTHORED_NOTATION_CLARIFICATION_ONLY'
assert sha((d/'proposal105.json').read_bytes())=='ac12387956c9cf61bbd51f440643335d719394c59df10d749262e22d500ca18d'
lp=Path(proposal['target']);assert sha(lp.read_bytes())==proposal['before_raw_sha256']
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261012-PBPSActualCountableEndpointLaw.json')
pp=Path('website/content/publications/pbps-actual-countable-endpoint-law.json')
packet=r/'reviewer-packet105.json'
for p,name in [(ap,'audit.before-apply.exactraw.snapshot'),(packet,'reviewer.before-apply.exactraw.snapshot')]:
 q=d/name;assert not q.exists();q.write_bytes(p.read_bytes())
lesson=load(lp);assert lesson['units'][0]['steps'][1]['text']==proposal['before']
lesson['units'][0]['steps'][1]['text']=proposal['after'];save(lp,lesson)
a=load(ap);oldbinding=a['publication_binding_sha256'];decoder=rt.decoder_packet(a)
pub.inputs.cache_clear();pub.load.cache_clear();item=load(pp)['items'][0]
a['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],pub.inputs())
a['publication_context']=pub.review_context(item,item['bindings'][0],pub.inputs())
assert rt.decoder_packet(a)==decoder;save(ap,a)
review=rt.semantic_reviewer_packet(a);save(packet,review)
save(d/'applied105.json',dict(proposal_raw=sha((d/'proposal105.json').read_bytes()),independent_decision_raw=sha(decision_path.read_bytes()),old_publication_binding=oldbinding,new_publication_binding=a['publication_binding_sha256'],reviewer_packet_sha256=review['packet_sha256'],decoder_unchanged=True,Lean_unchanged=True,source_theorem_unchanged=True,old_packet_preserved=True))
print(a['publication_binding_sha256'],review['packet_sha256'])
