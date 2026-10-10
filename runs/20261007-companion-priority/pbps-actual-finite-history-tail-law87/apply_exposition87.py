from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_publication as pub,astis_semantic_roundtrip as rt
r=Path(__file__).parent;load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def pin(p):p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=sha(b),bytes=len(b))
# Explicit accepted decision path and RAW hash are supplied by the coordinator
# after distinct native review; no invented/reformatted reviewer verdict.
dp=Path(sys.argv[1]);expected=sys.argv[2];assert sha(dp.read_bytes())==expected
decision=load(dp);assert decision['verdict']=='ACCEPTED_EXACT_THREE_FIELD_EXPOSITION_REPAIR' and decision['decision']=='accepted'
assert decision['reviewer']=='/root/fresh_source86' and decision['independent_from_author_and_stabilizer']
mp=dp.parent/'exposition-repair-review87.closed-RAW-manifest.json'
assert sha(mp.read_bytes())=='710ce5947b9fd15b0245cdbd3da2be5746554b0a9ce54bc3a366db2cfc805d18'
for group in ['inputs','outputs']:
 for x in load(mp)[group]:
  b=Path(x['path']).read_bytes();assert sha(b)==x['raw_sha256'] and len(b)==x['bytes'],x['path']
assert decision['proposal_sha256']=='750c744f686b6db7938cd54cdbabe680027028b1a22fdf5102ec143121e865a3' and decision['changed_field_count']==3
assert sha((dp.parent/'exposition-repair-review87.run.json').read_bytes())==decision['review_run_sha256']=='d63ecc0130cf86d52b6cff7a482de7f528ab60647db7120c19068fb9a1bddfd8'
proposal=r/'independent-math87/proposed-exposition-overlay87.json'
assert sha(proposal.read_bytes())=='750c744f686b6db7938cd54cdbabe680027028b1a22fdf5102ec143121e865a3'
manifest=load(r/'independent-math87/exposition-overlay87.closed-RAW-manifest.json')
for x in manifest['original_inputs']+[manifest['proposal']]:assert sha(Path(x['path']).read_bytes())==x['raw_sha256']
module=Path(load(proposal)['module']['path']);assert sha(module.read_bytes())=='01fcff944f1dbd42be2af30063b9baf4e191e2cde959e008724387cadb4fc899'
for pair in manifest['exact_proposed_successors']:
 original=Path(pair['original']['path']);proposed=Path(pair['proposed']['path'])
 assert sha(original.read_bytes())==pair['original']['raw_sha256']
 assert sha(proposed.read_bytes())==pair['proposed']['raw_sha256']
 original.write_bytes(proposed.read_bytes())
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualFiniteHistoryTailLaw.json');a=load(ap)
assert a['state']=='blind-reconstructed'
assert not (r/'audit.before-exposition87.json').exists();(r/'audit.before-exposition87.json').write_bytes(ap.read_bytes())
pub.inputs.cache_clear();pub.load.cache_clear()
item=next(x for x in pub.load() if x['id']=='pbps-actual-finite-history-tail-law');binding=item['bindings'][0]
a['publication_binding_sha256']=pub.binding_digest(item,binding,pub.inputs())
a['publication_context']=pub.review_context(item,binding,pub.inputs())
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=False)
packet=rt.semantic_reviewer_packet(a);assert not (r/'source-review87.packet.json').exists();save(r/'source-review87.packet.json',packet)
save(r/'root.exposition87.adoption.json',dict(status='DISTINCT_EXACT_EXPOSITION_REPAIR_APPLIED_ONLY',proposal=pin(proposal),independent_decision=pin(dp),module_unchanged=pin(module),successors=[pin(x['original']['path']) for x in manifest['exact_proposed_successors']],audit=pin(ap),publication_binding_sha256=a['publication_binding_sha256'],reviewer_packet_sha256=packet['packet_sha256'],source_review=False,PROVED_LOCAL=False,VERIFIED=False))
print(json.dumps(dict(packet=pin(r/'source-review87.packet.json'),publication_binding_sha256=a['publication_binding_sha256'])))
