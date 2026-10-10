from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_semantic_roundtrip as rt, astis_publication as pub, astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-law81');d=r/'fresh-source81'
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;save(p,x)
def pin(p):p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b))
n=load(d/'source-review.result81.json');m=load(d/'source-review.run-manifest81.json')
assert sha((d/'source-review.result81.json').read_bytes())=='c5f6f755aea3f75fd45420848dfbafe2a4a680a0e664ff32bf238f2f8cfae060'
assert sha((d/'source-review.run-manifest81.json').read_bytes())=='4c5b3db4fa08e1846665d518f9ab3f82a536ae2daff208898f3134af761ca55d'
assert m['status']=='closed'
for group in ['raw_inputs','raw_outputs']:
 for item in m[group]:assert sha(Path(item['path']).read_bytes())==item['raw_sha256'],item['path']
runhash=sha((d/'source-review.run-evidence81.json').read_bytes())
assert runhash==n['review_run_sha256']=='29f08fa35a746fd274f917499f370e494e1d674c60aed710f94ef7d193a125eb'
assert n['verdict']=='equivalent-after-elaboration' and not n['repairs'] and n['no_required_mathematical_repairs']
assert n['independence']['source_freeze_verified_before_candidate_body'] and n['independence']['source_freeze_original_bytes_unchanged'] and n['independence']['prohibited_materials_read']==[]
assert all(not x['blocking'] for x in n['deltas'])
g=n['source_graph_coverage'];s=n['authored_step_coverage']
assert not g['unmapped_inventory_items'] and not g['unmapped_nodes'] and not g['unmapped_edges']
assert g['inventory_expected']==g['inventory_reviewed']==65
assert s['gaps']==s['overlaps']==[] and s['expected_steps']==s['reviewed_steps']==s['formula_body_exact_matches']==10
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSIdealHalfTurnKernel.json');a=load(ap)
if a['state']=='accepted':
 assert not (r/'root.source81.adoption.json').exists()
 a=load(r/'audit.before-source81.json')
assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a)
assert packet==load(r/'source-review81.packet.json')
assert packet['packet_sha256']==n['reviewer_packet_sha256'] and a['publication_binding_sha256']==n['publication_binding_sha256']
assert sha(Path(a['lean']['file']).read_bytes())==n['full_module_sha256']
assert load(r/'root.math81.adoption.json')['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
if not (r/'audit.before-source81.json').exists():(r/'audit.before-source81.json').write_bytes(ap.read_bytes())
deltas=[dict(slot=x['slot'],severity='blocking' if x['blocking'] else 'informational',description=x['description'],evidence=f"Native independent source review {x.get('id',x['slot'])} in {d.as_posix()}/source-review.result81.json; exact current module and ten proof regions bound by run {runhash}.",native_classification=x['classification']) for x in n['deltas']]
slots={k:dict(v,original=v['source'],reconstructed=v['blind'],evidence=v['assessment']+f" Native source review: {d.as_posix()}/source-review.result81.json; run RAW {runhash}.") for k,v in n['semantic_slots'].items()}
a.update(state='accepted',semantic_slots=slots,deltas=deltas,verdict=n['verdict'],source_review=dict(state='accepted',reviewer=n['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=n['verdict_reason'],review_run_sha256=runhash,reviewer_packet_sha256=n['reviewer_packet_sha256'],run_artifact=(d/'source-review.run-evidence81.json').as_posix(),native_manifest=pin(d/'source-review.run-manifest81.json')))
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
new(r/'root.source81.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY',native_result=pin(d/'source-review.result81.json'),native_manifest=pin(d/'source-review.run-manifest81.json'),native_run_evidence=pin(d/'source-review.run-evidence81.json'),canonical_packet_sha256=packet['packet_sha256'],publication_binding_unchanged=True,publication_binding_sha256=a['publication_binding_sha256'],reviewer=n['reviewer'],full_current_module_RAW_sha256=n['full_module_sha256'],semantic_verdict=n['verdict'],source_graph_coverage=g,VERIFIED=False))
claim=load(r/'claim.json');cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');c=load(cp)
c['evidence'].update(proof_review=(r/'independent-math81/decision81.json').as_posix(),source_review=(d/'source-review.result81.json').as_posix())
c['source_proof_coverage'].update(compiled_source_review=(d/'source-review.result81.json').as_posix(),fresh_source_graph='runs/20261007-companion-priority/pbps-physical-time-law-preread81/source_proof_graph81.json',fresh_source_inventory='runs/20261007-companion-priority/pbps-physical-time-law-preread81/source_inventory81.json',coverage_status='Independent 65-item inventory, 15-node/29-edge source graph and all ten BODY/formula regions accepted for exact-reference ideal half-turn returned-position probability kernel, actual independent product initialization and terminal live-arc agreement. Actual joint phase and fixed-parameter common-AE all-time properties retained. Random-input all-time/version uniqueness, process Markov/semigroup/invariance/reversibility/implementation/main/error/cost/composition remain OPEN.')
c['blocked']['reason']='Ideal exact-reference returned-position kernel and actual independent product initialization focused compile, independent mathematics/blind/source accepted; exact-commit verification and serialized aggregation pending.'
e=dict(result_kind='integration-node',theorem_delta=claim['theorem_delta'],lean_declarations=claim['target_declarations'],publication_declarations=claim['target_declarations'],lean_files=claim['proposed_files'],focused_checks=[pin(r/'focused81-attempt5/receipt.json')],truth_boundary=claim['truth_boundary'],conceptual_mirror_audit=c['conceptual_mirror_audit'],statement_seal=c['statement_seal'],source_proof_coverage=c['source_proof_coverage'],proof_digestion=c['proof_digestion'],purification=c['purification'],independent_math=pin(r/'root.math81.adoption.json'),blind_decoder=pin(r/'root.decoder81.adoption.json'),source_review=pin(r/'root.source81.adoption.json'),integration_notes='Actual ideal H_y integration consumer joining joint phase, Gibbs normalization and everywhere Gaussian conditional-reference kernel; full measurable good event precedes product Fubini. Existing sole stabilization lane reused later; no new lane or self-VERIFIED transition.')
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
c['status']='proved_locally';save(cp,c);new(r/'proved-local81.json',e)
print('PROVED_LOCAL81: exact-reference ideal half-turn probability kernel and actual product initialization; independent exact-commit verification pending.')
