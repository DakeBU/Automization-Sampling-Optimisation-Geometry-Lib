from pathlib import Path
import copy,hashlib,json,sys
sys.path.insert(0,'tools')
import astis_publication as pub
r=Path('runs/20261007-companion-priority/pbps-sharp-energy68');d=r/'prose-and-span-overlay68-v2';d.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
encode=lambda x:(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode()
lp=Path('website/content/declaration_lessons/pbps-sharp-corrector-energy.json');lb=lp.read_bytes();lesson=json.loads(lb);after=copy.deepcopy(lesson)
old='use both inverse identities';new='use the right inverse identity twice'
assert after['units'][0]['steps'][1]['text'].count(old)==1
after['units'][0]['steps'][1]['text']=after['units'][0]['steps'][1]['text'].replace(old,new)
for i,before_line,after_line in [(4,413,412),(5,421,420)]:
 step=after['units'][0]['steps'][i];region=step['lean_source_region'];assert region['end_line']==before_line
 region['end_line']=after_line
 lines=Path(region['path']).read_text(encoding='utf-8').splitlines(keepends=True)
 exact=''.join(lines[region['start_line']-1:region['end_line']])
 assert exact==step['lean'] and sha(exact.encode())==region['exact_code_raw_sha256']
data=copy.deepcopy(pub.inputs());decl=after['units'][0]['declaration'];data['lessons'][decl]=after['units'][0]
item=next(x for x in pub.load() if x['id']=='pbps-sharp-corrector-energy')
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261009-PBPSSharpCorrectorEnergy.json');ab=ap.read_bytes();audit=json.loads(ab);aa=copy.deepcopy(audit)
assert audit['state']=='draft'
aa['publication_binding_sha256']=pub.binding_digest(item,item['bindings'][0],data)
aa['publication_context']=pub.review_context(item,item['bindings'][0],data)
changes=[]
for i,(p,b,x,fields) in enumerate([(lp,lb,after,['units[0].steps[1].text','units[0].steps[4].lean_source_region.end_line','units[0].steps[5].lean_source_region.end_line']),(ap,ab,aa,['publication_binding_sha256','publication_context.lesson.steps[1].text','publication_context.lesson.steps[4].lean_source_region.end_line','publication_context.lesson.steps[5].lean_source_region.end_line'])]):
 a=encode(x);(d/f'{i}.before.exactraw.snapshot.json').write_bytes(b);(d/f'{i}.after.exactraw.snapshot.json').write_bytes(a)
 changes.append(dict(path=p.as_posix(),before_snapshot=f'{i}.before.exactraw.snapshot.json',after_snapshot=f'{i}.after.exactraw.snapshot.json',before_raw_sha256=sha(b),after_raw_sha256=sha(a),changed_fields=fields))
proposal=dict(status='PROPOSED_NOT_APPLIED',kind='NARROW_PROOF_EXPLANATION_TWO_RAW_SPAN_ENDPOINTS_AND_BOUND_CONTEXT',changes=changes,
 supersedes_unapplied_proposal='prose-overlay68/proposal.json',superseded_proposal_RAW_sha256=sha((r/'prose-overlay68/proposal.json').read_bytes()),
 exact_prose_change=dict(before=old,after=new),exact_span_changes=[dict(step=5,before=413,after=412),dict(step=6,before=421,after=420)],
 evidence='The coefficient proof uses hRight twice. Two span endpoints contained one extra blank LF; exact Lean/code hashes remain unchanged.',
 proposed_binding=aa['publication_binding_sha256'],old_binding=audit['publication_binding_sha256'],Lean_header_BODY_private_Prop_source_statement_formulas_unchanged=True,
 anonymous_decoder_packets_unchanged=True,source_mathematical_repair=False,exposition_seal_claim=False,
 renderer_observer_diagnosis='lean_statement is prose explanation; actual folded code is sourced independently by inline_lean.disclosure. No code is inserted into the explanation field.')
(d/'proposal.json').write_bytes(encode(proposal))
helper=Path('.astis/pbps-sharp-energy68/freeze-reader68.py');(d/'freeze-reader68.original-executed-helper.raw.py').write_bytes(helper.read_bytes())
print('V2 proposed:1 explanation phrase,2 exact interval endpoints and bound context; NOT APPLIED; proposal RAW',sha((d/'proposal.json').read_bytes()))
