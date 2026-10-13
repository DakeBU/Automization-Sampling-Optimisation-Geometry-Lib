from pathlib import Path
import copy,hashlib,json,sys
sys.path.insert(0,'tools')
import astis_publication as pub
r=Path('runs/20261007-companion-priority/pbps-sharp-energy68');d=r/'prose-overlay68';d.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
encode=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
lp=Path('website/content/declaration_lessons/pbps-sharp-corrector-energy.json');lb=lp.read_bytes();lesson=json.loads(lb);after=copy.deepcopy(lesson)
old='use both inverse identities';new='use the right inverse identity twice'
assert after['units'][0]['steps'][1]['text'].count(old)==1
after['units'][0]['steps'][1]['text']=after['units'][0]['steps'][1]['text'].replace(old,new)
data=copy.deepcopy(pub.inputs());decl=after['units'][0]['declaration'];data['lessons'][decl]=after['units'][0]
item=next(x for x in pub.load() if x['id']=='pbps-sharp-corrector-energy')
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSSharpCorrectorEnergy.json');ab=ap.read_bytes();audit=json.loads(ab);aa=copy.deepcopy(audit)
assert audit['state']=='draft'
aa['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],data)
aa['publication_context']=pub.review_context(item,item['bindings'][0],data)
changes=[]
for i,(p,b,x,fields) in enumerate([(lp,lb,after,['units[0].steps[1].text']),(ap,ab,aa,['publication_binding_sha256','publication_context.lesson.steps[1].text'])]):
 a=encode(x);(d/f'{i}.before.exactraw.snapshot.json').write_bytes(b);(d/f'{i}.after.exactraw.snapshot.json').write_bytes(a)
 changes.append(dict(path=p.as_posix(),before_snapshot=f'{i}.before.exactraw.snapshot.json',after_snapshot=f'{i}.after.exactraw.snapshot.json',before_raw_sha256=sha(b),after_raw_sha256=sha(a),changed_fields=fields))
proposal=dict(status='PROPOSED_NOT_APPLIED',kind='NARROW_PROOF_EXPLANATION_AND_BOUND_PUBLICATION_CONTEXT',changes=changes,
 exact_prose_change=dict(before=old,after=new),evidence='Actual coefficient proof hFirst uses hRight twice; hLeft is retained as a conclusion but is not called in this proof.',
 proposed_binding=aa['publication_binding_sha256'],old_binding=audit['publication_binding_sha256'],Lean_header_BODY_private_Prop_source_statement_formulas_unchanged=True,
 anonymous_decoder_packets_unchanged=True,source_mathematical_repair=False,exposition_seal_claim=False,
 renderer_observer_diagnosis='lean_statement is prose explanation; exact folded code is sourced by inline_lean.disclosure. No code is inserted into the explanation field.')
(d/'proposal.json').write_bytes(encode(proposal))
print('Proposed one proof-explanation phrase and its exact binding/context; not applied; proposal RAW',sha((d/'proposal.json').read_bytes()))
