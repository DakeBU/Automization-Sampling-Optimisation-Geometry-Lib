from pathlib import Path
import copy,json,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'))
import astis_publication as pub,astis_semantic_roundtrip as rt,astis_advance as adv
r=root/'runs/20261007-companion-priority/pbps-ambient-adjoint66';load=lambda p:json.loads(Path(p).read_bytes())
def replace(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;replace(p,x)
assert load(r/'root.math66.adoption.json')['native_owned_files']==133
source=load(r/'root.source66.adoption.json');assert source['status']=='INDEPENDENT_SOURCE66_ACCEPTED_SELECTED_BOUNDARY'
assert load(r/'root.decoder66.adoption.json')['native_owned_files']==20
assert load(r/'presentation-overlay66/applied.json')['status']=='EXACT_INDEPENDENTLY_REVIEWED_FOUR_CATALOGUE_FIELDS_APPLIED'
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');aid=plan['audit_ids'][0]
ap=root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json';audit=load(ap)
decision=load(r/'independent-source66/decision.json');packet=load(r/'source.1.reviewer-packet.json')
assert audit['state']=='blind-reconstructed' and rt.semantic_reviewer_packet(audit)==packet
assert packet['packet_sha256']==decision['reviewer_packet_sha256']
pub.inputs.cache_clear();pub.load.cache_clear();item=next(x for x in pub.load() if x['id']==plan['slugs'][0])
assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==audit['publication_binding_sha256']==decision['publication_binding_sha256']
assert decision['verdict']=='equivalent-after-elaboration' and not decision['repairs'] and not decision['deltas']
assert set(decision['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
adapter=copy.deepcopy(decision);adapter['native_complete_RAW_review_sha256']=source['native_complete_RAW_review_sha256'];adapter['native_review_bytes_preserved']=True
target=r/'source.1.review.root-adapter.json';new(target,adapter)
accepted=copy.deepcopy(audit);accepted.update(state='accepted',semantic_slots=decision['semantic_slots'],deltas=[],verdict=decision['verdict'],repairs=[])
accepted['source_review']=dict(state='accepted',reviewer=decision['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=decision['review_evidence'],review_run_sha256=decision['review_run_sha256'],reviewer_packet_sha256=decision['reviewer_packet_sha256'],run_artifact=target.relative_to(root).as_posix())
registry=rt.load_registry();registry['audits']=[accepted if x['id']==aid else x for x in registry['audits']]
errors=rt.validate_registry(registry);assert not errors,errors
(r/'audit.1.before-source-admission.exactraw.snapshot.json').write_bytes(ap.read_bytes());replace(ap,accepted)
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=True)
mirror=load(r/'conceptual-mirror-audit66.json');mirror={k:mirror[k] for k in ['status','discovery_ids','reason']}
boundary=claim['truth_boundary']+' Independent precommit mathematics,fresh blind reconstruction and primary-first whole-module seven-slot source review accepted. The original private literal proposition expansions preserve all callers and conclusions. Exactly four catalogue fields were independently corrected to list two already used ASTIS APIs; formulas and Lean unchanged. Exact SCI66 verification and serialized aggregate/reader admission remain pending.'
cp=root/'research-wiki/frontier-cells'/f"{plan['active_cells'][0]}.json";cell=load(cp);assert cell['status']=='claimed'
e=dict(result_kind='integration-node',theorem_delta=claim['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],lean_files=claim['proposed_files'],focused_checks=[dict(command='lake build Tests.ProximalBPSAmbientAdjointCorrector',result='Root48268 EXIT0/3946,standard3 for both exact public declarations. Independent Lake12908 replay classified; fresh main35940 and Test50788 EXIT0/standard3.'),dict(command='Independent primary-first source review and blind decoder',result=f'CLOSED math133/source{source["native_owned_files"]}/decoder20;310 selected source math items,all6 literal BODY spans,seven slots equivalent-after-elaboration;no source mathematical repair.')],truth_boundary=boundary,conceptual_mirror_audit=mirror,useful_discoveries=['ASTIS-DISC-20261009-DependentPropStatementStaging'],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+plan['slugs'][0]+'.json'],integration_notes='SAME actual root/inverse/polar and exact centered macroscopic/conditional-zero subspaces. Canonical ambient adjoint and every globally centered actual input now have genuine decomposition/norm budget. Private literal Prop definitions supply no mathematical provider or premise. Next live target is full B20 corrector energy; RAW B21 commutation remains unvalidated. Sole existing PhaseKernel stabilization lane; full Exposition/PURIFIED/main/expected costs/composition/Goal unclaimed.')
for k in ['statement_seal','source_proof_coverage','proof_digestion','purification']:
    e[k]=[dict(declaration=plan['mathematical_declarations'][0],declaration_level=cell['declaration_level'],report=cell[k])]
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
(r/'cell.1.before-proved.exactraw.snapshot.json').write_bytes(cp.read_bytes())
cell['status']='proved_locally';cell['conceptual_mirror_audit']=mirror
cell['evidence'].update(proof_review=(r/'independent-math66/mathematical-review.named.raw.json').relative_to(root).as_posix(),source_review=target.relative_to(root).as_posix(),execution_boundary=boundary)
replace(cp,cell);new(r/'proved-local.json',e)
print('PASS66 PROVED_LOCAL: independent math/decoder/whole-module source and real publication admission;6 literal BODY steps. Exact SCI66 verification,aggregate/reader and full papers remain pending.')
