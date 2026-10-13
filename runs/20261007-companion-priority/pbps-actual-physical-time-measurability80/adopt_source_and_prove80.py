from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'));import astis_semantic_roundtrip as rt,astis_publication as pub,astis_advance as adv
r=Path('runs/20261007-companion-priority/pbps-actual-physical-time-measurability80');d=r/'fresh-source80'
load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;save(p,x)
def pin(p):p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b))
native=load(d/'source-review.result80.json');m=load(d/'source-review.run-manifest80.json')
assert sha((d/'source-review.result80.json').read_bytes())=='98630d82df884de6a3a5cd01929e66b9c5df3353b18ca9f81bc3ff565c8de6c0'
assert sha((d/'source-review.run-manifest80.json').read_bytes())=='8a73fcd81f8d47db8488f1fabae08ab79e06293e4b60c66acd0764174f2ccff3'
for group in ['raw_inputs','raw_outputs']:
 for item in m[group]:assert sha(Path(item['path']).read_bytes())==item['raw_sha256'],item['path']
runhash=sha((d/'source-review.run-evidence80.json').read_bytes());assert runhash==native['review_run_sha256']=='851df6819e602fb254fb553e2ce9a23a035b949da14b5a9f1c65241481df4f16'
assert native['verdict']=='equivalent-after-elaboration' and not native['repairs'] and native['no_required_mathematical_repairs']
assert native['independence']['candidate_not_seen_before_source_inventory_and_topology_freeze'] and native['independence']['original_source_freeze_unchanged'] and native['independence']['no_prior80_header_scope_math_review_verdicts_root_adoption_or_other_source_extractor_consulted']
assert all(not x['blocking'] for x in native['deltas'])
assert not native['source_graph_coverage']['unmapped_scoped_items'] and not native['source_graph_coverage']['unmapped_nodes'] and not native['source_graph_coverage']['unmapped_edges']
assert native['authored_step_coverage']['gaps']==[] and native['authored_step_coverage']['expected_steps']==native['authored_step_coverage']['reviewed_steps']==9 and native['authored_step_coverage']['overlaps']==[] and native['authored_step_coverage']['formula_body_exact_matches']
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261010-PBPSActualPhysicalTimeMeasurability.json');a=load(ap);assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a);assert packet==load(r/'source-review80.packet.json')
assert packet['packet_sha256']==native['reviewer_packet_sha256'] and a['publication_binding_sha256']==native['publication_binding_sha256']
assert sha(Path(a['lean']['file']).read_bytes())==native['full_module_sha256']
(r/'audit.before-source80.json').write_bytes(ap.read_bytes())
deltas=[dict(slot=x['slot'],severity='blocking' if x['blocking'] else 'informational',description=x['description'],evidence=f"Native independent source review {x.get('id', 'slot:'+x['slot']+';classification:'+x['classification'])} in {d.as_posix()}/source-review.result80.json; exact current module and nine proof regions bound by run {runhash}.",native_classification=x['classification']) for x in native['deltas']]
a.update(state='accepted',semantic_slots=native['semantic_slots'],deltas=deltas,verdict=native['verdict'],source_review=dict(state='accepted',reviewer=native['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=native['review_evidence'],review_run_sha256=runhash,reviewer_packet_sha256=native['reviewer_packet_sha256'],run_artifact=(d/'source-review.run-evidence80.json').as_posix(),native_manifest=pin(d/'source-review.run-manifest80.json')))
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
new(r/'root.source80.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY',native_result=pin(d/'source-review.result80.json'),native_manifest=pin(d/'source-review.run-manifest80.json'),native_run_evidence=pin(d/'source-review.run-evidence80.json'),canonical_packet_sha256=packet['packet_sha256'],publication_binding_unchanged=True,publication_binding_sha256=a['publication_binding_sha256'],reviewer=native['reviewer'],full_current_module_RAW_sha256=native['full_module_sha256'],semantic_verdict=native['verdict'],source_graph_coverage=native['source_graph_coverage'],VERIFIED=False))
claim=load(r/'claim.json');cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');c=load(cp)
c['evidence'].update(proof_review=(r/'independent-math80/decision80.json').as_posix(),source_review=(d/'source-review.result80.json').as_posix())
c['source_proof_coverage'].update(compiled_source_review=(d/'source-review.result80.json').as_posix(),fresh_source_graph=(d/'source_proof_graph80.json').as_posix(),fresh_source_inventory=(d/'source_inventory80.json').as_posix(),coverage_status='Independent 41-item inventory, 12-node/33-edge source graph and all nine BODY/formula regions accepted for joint actual physical-time measurable representative and per-fixed-parameter common-AE all-time interpolation/initialization. Path regularity/adaptedness/Markov/kernel/invariance/main/error/cost/composition remain OPEN; uniform-parameter AE and arbitrary correlated random-parameter substitution excluded.')
c['blocked']['reason']='Joint actual physical-time phase/interpolation/initialization focused compile, independent mathematics/blind/source accepted; exact-commit verification and serialized aggregation pending.'
evidence=dict(result_kind='integration-node',theorem_delta=claim['theorem_delta'],lean_declarations=claim['target_declarations'],publication_declarations=claim['target_declarations'],lean_files=claim['proposed_files'],focused_checks=[pin(r/'focused80-attempt3/receipt.json')],truth_boundary=claim['truth_boundary'],conceptual_mirror_audit=c['conceptual_mirror_audit'],statement_seal=c['statement_seal'],source_proof_coverage=c['source_proof_coverage'],proof_digestion=c['proof_digestion'],purification=c['purification'],independent_math=pin(r/'root.math80.adoption.json'),blind_decoder=pin(r/'root.decoder80.adoption.json'),source_review=pin(r/'root.source80.adoption.json'),integration_notes='One joint measurable actual phase consumer joining actual finite recursion, harmonic flow, interval coverage and positive actual input support. Existing sole stabilization lane reused later; no new lane or self-VERIFIED transition.')
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=evidence)
c['status']='proved_locally';save(cp,c);new(r/'proved-local80.json',evidence)
print('PROVED_LOCAL80: jointly measurable actual phase and AE initialization; independent exact-commit verification pending.')
