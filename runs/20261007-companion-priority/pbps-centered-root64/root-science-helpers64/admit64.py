from pathlib import Path
import json,hashlib,copy,sys
root=Path.cwd();sys.path.insert(0,str(root/'tools'));import astis_publication as pub,astis_semantic_roundtrip as rt,astis_advance as adv
r=root/'runs/20261007-companion-priority/pbps-centered-root64';load=lambda p:json.loads(Path(p).read_bytes())
def replace(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;replace(p,x)
assert load(r/'root.math64.adoption.json')['status']=='INDEPENDENT_PRECOMMIT_MATHEMATICS64_ACCEPTED_WITH_STEP6_PUBLICATION_BLOCKER'
assert load(r/'root.source64.original-adoption.json')['native_owned_files']==97
assert load(r/'root.decoder64.adoption.json')['native_owned_files']==18
overlay=load(r/'root.source64.overlay-adoption.json');assert overlay['accepted'] and not overlay['source_statement_mathematical_repair']
plan=load(r/'publication-plan.json');claim=load(r/'claim.json');pub.inputs.cache_clear();pub.load.cache_clear();data=pub.inputs();updates=[]
for i,aid in enumerate(plan['audit_ids']):
 ap=root/'research-wiki/semantic-roundtrip/audits'/f'{aid}.json';a=load(ap);assert a['state']=='blind-reconstructed'
 decision=load(Path(overlay['decision_path'])) if i==0 else load(r/'independent-source64/decision.1.json')
 packet=load(r/'auxiliary-metadata-overlay64/fresh-reviewer-packet.json') if i==0 else load(r/'source.1.reviewer-packet.json')
 assert rt.semantic_reviewer_packet(a)==packet and packet['packet_sha256']==decision['reviewer_packet_sha256']
 item=next(x for x in pub.load() if x['id']==plan['slugs'][i]);assert pub.binding_digest(item,item['bindings'][0],data)==a['publication_binding_sha256']==decision['publication_binding_sha256']
 assert decision['verdict']=='equivalent-after-elaboration' and decision['independent_from_formalizer'] and decision['independent_from_decoder'] and not decision['repairs']
 assert set(decision['semantic_slots'])==set(rt.SEMANTIC_SLOTS)
 assert all(x['relation']!='not-audited' and x['evidence'] for x in decision['semantic_slots'].values())
 assert not decision['deltas'],decision['deltas']
 adapter=copy.deepcopy(decision);adapter['native_complete_RAW_review_sha256']=overlay['native_complete_RAW_review_sha256'] if i==0 else load(r/'root.source64.original-adoption.json')['native_complete_named_RAW_REVIEW_sha256'];adapter['native_review_bytes_preserved']=True
 target=r/f'source.{i}.review.root-adapter.json';new(target,adapter)
 b=copy.deepcopy(a);b.update(state='accepted',semantic_slots=decision['semantic_slots'],deltas=[],verdict=decision['verdict'],repairs=[])
 b['source_review']=dict(state='accepted',reviewer=decision['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=decision['review_evidence'],review_run_sha256=decision['review_run_sha256'],reviewer_packet_sha256=decision['reviewer_packet_sha256'],run_artifact=target.relative_to(root).as_posix())
 updates.append((ap,b));(r/f'audit.{i}.before-source-admission.exactraw.snapshot.json').write_bytes(ap.read_bytes())
registry=rt.load_registry();byid={b['id']:b for _,b in updates};registry['audits']=[byid.get(a['id'],a) for a in registry['audits']];errors=rt.validate_registry(registry);assert not errors,errors
for ap,b in updates:replace(ap,b)
pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance(plan['mathematical_declarations'],reviewed=True)
mirror=load(r/'conceptual-mirror-audit64.json');mirror={k:mirror[k] for k in ['status','discovery_ids','reason']}
boundary=claim['truth_boundary']+' Independent mathematics, fresh source-blind reconstruction, primary-first seven-slot source review, all12 literal proof-body excerpts and separate auxiliary attribution/dependency overlay accepted. Exact science commit review, serialized aggregate and rendered reader acceptance remain separate.'
e=dict(result_kind='integration-node',theorem_delta=claim['theorem_delta'],lean_declarations=plan['mathematical_declarations'],publication_declarations=plan['mathematical_declarations'],lean_files=claim['proposed_files'],focused_checks=[dict(command='lake build Tests.ProximalBPSCenteredRootOrderInverse',result='Root28796 and independent12600 EXIT0 PASS3944; two exact sealed public statements, standard3, zero private providers; original-input normalized actual leakage norm and kerP consumer.'),dict(command='Independent source-first seven-slot review and finite metadata overlay',result='321 source items, all12 exact proof-body excerpts; no additional source assumption or mathematical repair. Shared leaf explicitly ASTIS auxiliary; unrelated unit/norm APIs removed from generic lesson.')],truth_boundary=boundary,conceptual_mirror_audit=mirror,useful_discoveries=[],active_cells=plan['active_cells'],reader_lesson=['website/content/declaration_lessons/'+slug+'.json' for slug in plan['slugs']],integration_notes='Same actual GammaP restricted to exact inherited HP0. Arbitrary-real-L2 square order plus SAME rough/marginal-Poincare gradient closure yields C4 and printed B15; internally derives unit/both inverse cancellations/norm. Genuine B16 input consumer has no extra premise. Next public typed polar factorization/isometry, H1/B13/B14, dynamics/main/errors/expected costs/composition remain open. Existing sole PhaseKernel stabilization lane; no full paper/Exposition/PURIFIED/Goal claim.')
cells=[]
for i,cid in enumerate(plan['active_cells']):
 cp=root/'research-wiki/frontier-cells'/f'{cid}.json';c=load(cp);assert c['status']=='claimed';cells.append((cp,c))
 for k in ['statement_seal','source_proof_coverage','proof_digestion','purification']:e.setdefault(k,[]).append(dict(declaration=plan['mathematical_declarations'][i],declaration_level=c['declaration_level'],report=c[k]))
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
for i,(cp,c) in enumerate(cells):
 (r/f'cell.{i}.before-proved.exactraw.snapshot.json').write_bytes(cp.read_bytes());c['status']='proved_locally';c['conceptual_mirror_audit']=mirror;c['evidence'].update(proof_review=(r/'independent-math64/native.receipt.json').relative_to(root).as_posix(),source_review=(r/f'source.{i}.review.root-adapter.json').relative_to(root).as_posix(),execution_boundary=boundary);replace(cp,c)
new(r/'proved-local.json',e)
print('PASS64 PROVED_LOCAL: independent math/decoder/source,12 literal proofs,separate metadata overlay and real reviewed publication admission. Exact science VERIFIED and serialized aggregate pending.')
