from pathlib import Path
import copy,hashlib,json,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'))
import astis_publication as pub,astis_semantic_roundtrip as rt,astis_advance as adv
r=root/'runs/20261007-companion-priority/pbps-polar65';load=lambda p:json.loads(Path(p).read_bytes())
def replace(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;replace(p,x)
assert load(r/'root.math65.adoption.json')['native_owned_files']==40
source=load(r/'root.source65.adoption.json');assert source['native_owned_files']==117
assert load(r/'root.decoder65.adoption.json')['native_owned_files']==20
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');aid=plan['audit_ids'][0];ap=root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json';a=load(ap)
decision=load(r/'independent-source65/semantic-decision.json');packet=load(r/'source.0.reviewer-packet.json')
assert a['state']=='blind-reconstructed' and rt.semantic_reviewer_packet(a)==packet
assert packet['packet_sha256']==decision['reviewer_packet_sha256']
pub.inputs.cache_clear();pub.load.cache_clear();item=next(x for x in pub.load() if x['id']==plan['slugs'][0])
assert pub.binding_digest(item,item['bindings'][0],pub.inputs())==a['publication_binding_sha256']==decision['publication_binding_sha256']
assert decision['verdict']=='equivalent-after-elaboration' and not decision['repairs'] and not decision['deltas']
assert set(decision['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
adapter=copy.deepcopy(decision);adapter['native_complete_RAW_review_sha256']=source['native_complete_RAW_review_sha256'];adapter['native_review_bytes_preserved']=True
target=r/'source.0.review.root-adapter.json';new(target,adapter)
b=copy.deepcopy(a);b.update(state='accepted',semantic_slots=decision['semantic_slots'],deltas=[],verdict=decision['verdict'],repairs=[])
b['source_review']=dict(state='accepted',reviewer=decision['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=decision['review_evidence'],review_run_sha256=decision['review_run_sha256'],reviewer_packet_sha256=decision['reviewer_packet_sha256'],run_artifact=target.relative_to(root).as_posix())
registry=rt.load_registry();registry['audits']=[b if x['id']==aid else x for x in registry['audits']];errors=rt.validate_registry(registry);assert not errors,errors
(r/'audit.0.before-source-admission.exactraw.snapshot.json').write_bytes(ap.read_bytes());replace(ap,b)
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=True)
mirror=load(r/'conceptual-mirror-audit65.json');mirror={k:mirror[k] for k in ['status','discovery_ids','reason']}
boundary=claim['truth_boundary']+' Independent precommit mathematics, fresh source-blind decoder and primary-first seven-slot source review accepted. The compiled adjoint action is typed B0*:kerP->HP0; full ambient B* transport/global-centered decomposition/full projector extraction are separate next edges. Exact science commit verification and serialized aggregate/reader acceptance remain pending.'
cp=root/'research-wiki/frontier-cells'/f"{plan['active_cells'][0]}.json";cell=load(cp);assert cell['status']=='claimed'
e=dict(result_kind='integration-node',theorem_delta=claim['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],lean_files=claim['proposed_files'],focused_checks=[dict(command='lake build Tests.ProximalBPSPolarIsometry',result='Root36260 and independent23980 EXIT0/3945; both exact public headers, standard3 axioms; original-input typed polar and genuine adjoint/contraction/residual consumer.'),dict(command='Independent primary-first source review and source-blind decoder',result='CLOSED math40/source117/decoder20;280/280 source items;all5 literal BODY spans;seven slots equivalent-after-elaboration, no mathematical repair.')],truth_boundary=boundary,conceptual_mirror_audit=mirror,useful_discoveries=[],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+plan['slugs'][0]+'.json'],integration_notes='SAME actual root/inverse and exact HP0/kerP. No onto/reverse-product identity or new hypothesis. Next minimal live consumer adapter is ambient B* compatibility and actual globally centered decomposition; RAW B21 commutation discovery is retained unvalidated. Sole existing PhaseKernel stabilization lane. No full Exposition/PURIFIED/paper/Goal completion.')
for k in ['statement_seal','source_proof_coverage','proof_digestion','purification']:e[k]=[dict(declaration=plan['mathematical_declarations'][0],declaration_level=cell['declaration_level'],report=cell[k])]
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
(r/'cell.0.before-proved.exactraw.snapshot.json').write_bytes(cp.read_bytes());cell['status']='proved_locally';cell['conceptual_mirror_audit']=mirror
cell['evidence'].update(proof_review=(r/'independent-math65/mathematical-review.named.raw.json').relative_to(root).as_posix(),source_review=target.relative_to(root).as_posix(),execution_boundary=boundary)
replace(cp,cell);new(r/'proved-local.json',e)
print('PASS65 PROVED_LOCAL: closed independent math/decoder/source,280 items,5 literal BODY steps,reviewed publication admission. Exact SCI65 verification and integration pending.')
