from pathlib import Path
import copy, hashlib, json, sys
sys.path.insert(0,'tools')
import astis_publication as pub, astis_semantic_roundtrip as rt
r=Path('runs/20261007-companion-priority/pbps-sharp-energy68')
d=r/'energy-alias-overlay68';d.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
enc=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
lp=Path('website/content/declaration_lessons/hilbert-sharp-quadratic-corrector-bound.json')
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-HilbertSharpQuadraticCorrectorBound.json')
lesson=json.loads(lp.read_bytes());after=copy.deepcopy(lesson)
step=after['units'][0]['steps'][2]
old=step['text']
prefix='Set S=‖u‖²+‖v‖² and T=‖u-Kv‖²+‖Ku+v‖²=‖Du‖²+‖Dv‖² throughout this five-step proof. '
assert 'Set S=' not in old
step['text']=prefix+old
data=copy.deepcopy(pub.inputs());decl=after['units'][0]['declaration'];data['lessons'][decl]=after['units'][0]
item=next(x for x in pub.load() if x['id']=='hilbert-sharp-quadratic-corrector-bound')
audit=json.loads(ap.read_bytes());aa=copy.deepcopy(audit);assert audit['state']=='accepted'
aa['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],data)
aa['publication_context']=pub.review_context(item,item['bindings'][0],data)
packet=rt.semantic_reviewer_packet(aa)
changes=[]
for i,(path,before,value,fields) in enumerate([(lp,lp.read_bytes(),after,['units[0].steps[2].text']),(ap,ap.read_bytes(),aa,['publication_binding_sha256','publication_context.lesson.steps[2].text'])]):
 b=enc(value);(d/f'{i}.before.exactraw.snapshot.json').write_bytes(before);(d/f'{i}.after.context-only.exactraw.snapshot.json').write_bytes(b)
 changes.append(dict(path=path.as_posix(),before_snapshot=f'{i}.before.exactraw.snapshot.json',proposed_context_snapshot=f'{i}.after.context-only.exactraw.snapshot.json',before_RAW_sha256=sha(before),proposed_context_RAW_sha256=sha(b),changed_fields=fields))
(d/'proposed.reviewer-packet.json').write_bytes(enc(packet))
proposal=dict(status='PROPOSED_READER_ALIAS_ONLY_NOT_APPLIED',changes=changes,old_text=old,new_text=step['text'],old_binding=audit['publication_binding_sha256'],proposed_binding=aa['publication_binding_sha256'],new_reviewer_packet_sha256=packet['packet_sha256'],native_source_limitation='independent-source68/nonblocking-exposition-limitation-S-T.json',source_mathematical_repair=False,Lean_formulas_proof_spans_private_Props_and_blind_reconstruction_unchanged=True,source_review_refresh_required_before_application=True,current_source_review_in_context_snapshot_is_historical_not_new_acceptance=True,full_Exposition_Seal=False,PURIFIED=False,canonical_writes=False)
(d/'proposal.json').write_bytes(enc(proposal))
print('PROPOSED exact S,T reader aliases and refreshed packet only; no canonical mutation',sha((d/'proposal.json').read_bytes()))
