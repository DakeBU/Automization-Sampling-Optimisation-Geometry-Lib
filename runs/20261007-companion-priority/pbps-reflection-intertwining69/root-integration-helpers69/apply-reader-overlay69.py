from pathlib import Path
import copy, hashlib, json, sys
root = Path.cwd(); sys.path.insert(0, str(root/'tools'))
import astis_publication as pub, astis_semantic_roundtrip as rt
r = root/'runs/20261007-companion-priority/pbps-reflection-intertwining69'
owned = r/'independent-source69'
load = lambda p: json.loads(Path(p).read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
def pin(p):
 p=Path(p);b=p.read_bytes();return dict(path=p.resolve().as_posix(),raw_bytes=len(b),raw_sha256=sha(b),lf_sha256=sha(b.replace(b'\r\n',b'\n')))
def write(p,x):
 Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
out=r/'reader-api-overlay69';out.mkdir(exist_ok=False)
proposal=owned/'reader-api-metadata-overlay.proposal.json'
decision=owned/'reader-api-metadata-overlay.decision.json'
assert sha(proposal.read_bytes())=='85cfec574019132c82244c1536a6ffb1b018e7932aefd825d3e05530be5f815d'
assert sha(decision.read_bytes())=='06004dd5b90ae25e85346f9494f2943a087f5252003053d824d13709f59e9e5b'
q=load(proposal);d=load(decision)
assert d['decision']=='APPROVE_EXACT_TWO_METADATA_FIELDS' and not d['mathematical_repair']
lp=root/q['target'];before=lp.read_bytes();assert sha(before)==q['base_RAW_sha256']
lesson=load(lp);prior=copy.deepcopy(lesson);u=lesson['units'][0]
assert 'helpers' not in u and u['mathlib_dependencies'][6]==q['operations'][1]['old']
u['helpers']=q['operations'][0]['value'];u['mathlib_dependencies'][6]=q['operations'][1]['value']
restored=copy.deepcopy(lesson);del restored['units'][0]['helpers'];restored['units'][0]['mathlib_dependencies'][6]=q['operations'][1]['old']
assert restored==prior
ap=root/'research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSActualReflectionIntertwining.json'
audit=load(ap);audit_before=copy.deepcopy(audit);assert audit['state']=='blind-reconstructed'
neutral_before=rt.decoder_packet(audit)
assert neutral_before==load(root/'.astis/decoder-69/packet0.json')
module=root/audit['lean']['file'];module_before=pin(module)
(out/'lesson.before.exactraw.json').write_bytes(before)
(out/'audit.before.exactraw.json').write_bytes(ap.read_bytes())
write(lp,lesson);pub.inputs.cache_clear();pub.load.cache_clear()
pp=root/'website/content/publications/pbps-actual-reflection-intertwining.json'
item=load(pp)['items'][0];binding=item['bindings'][0]
audit['publication_binding_sha256']=pub.binding_digest(item,binding,pub.inputs())
audit['publication_context']=pub.review_context(item,binding,pub.inputs())
assert rt.decoder_packet(audit)==neutral_before and pin(module)==module_before
audit_restored=copy.deepcopy(audit)
for k in ['publication_binding_sha256','publication_context']:audit_restored[k]=audit_before[k]
assert audit_restored==audit_before
write(ap,audit)
packet=rt.semantic_reviewer_packet(audit);dest=r/'source.0.reviewer-packet.json';assert not dest.exists();write(dest,packet)
write(out/'application.json',dict(status='EXACT_TWO_REVIEWED_METADATA_FIELDS_APPLIED',proposal=pin(proposal),independent_decision=pin(decision),before=[pin(out/'lesson.before.exactraw.json'),pin(out/'audit.before.exactraw.json')],after=[pin(lp),pin(ap)],finite_changes=q['operations'],audit_refresh_only=['publication_binding_sha256','publication_context'],module_unchanged=module_before,neutral_packet_unchanged=pin(root/'.astis/decoder-69/packet0.json'),official_reviewer_packet=pin(dest),official_packet_sha256=packet['packet_sha256'],no_mathematical_repair=True,source_fidelity_accepted=False,PROVED_LOCAL=False,VERIFIED=False))
print('PASS exact two independently reviewed metadata fields applied; module and neutral packet unchanged; official source packet '+packet['packet_sha256'])
