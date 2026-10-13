from pathlib import Path
import hashlib,json,sys
sys.path.insert(0,str(Path.cwd()/'tools'))
import astis_semantic_roundtrip as rt,astis_publication as pub,astis_advance as adv
r=Path(__file__).parent;d=r/'independent-source84';load=lambda p:json.loads(Path(p).read_bytes());sha=lambda b:hashlib.sha256(b).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
def new(p,x):assert not Path(p).exists(),p;save(p,x)
def pin(p):p=Path(p);b=p.read_bytes();return dict(path=p.as_posix(),RAW_bytes=len(b),RAW_sha256=sha(b))
n=load(d/'source-review.result84.json');m=load(d/'source-review.run-manifest84.json')
assert sha((d/'source-review.result84.json').read_bytes())==sys.argv[1]
assert sha((d/'source-review.run-manifest84.json').read_bytes())==sys.argv[2]
assert m['status']=='closed'
for group in ['raw_inputs','raw_outputs']:
 for x in m[group]:assert sha(Path(x['path']).read_bytes())==x['raw_sha256'],x['path']
runhash=sha((d/'source-review.run-evidence84.json').read_bytes());assert runhash==n['review_run_sha256']==sys.argv[3]
assert n['verdict']=='equivalent-after-elaboration' and not n['repairs'] and n['no_required_mathematical_repairs']
assert n['independent_from_formalizer'] and n['independent_from_decoder']
assert n['independence']['source_first_chronology']
assert not n['independence']['other_math_review_verdicts_read']
assert not n['independence']['root_adoption_reports_read'] and not n['independence']['blind_files_outside_canonical_packet_read']
assert all(not x['blocking'] for x in n['deltas'])
g=n['source_graph_coverage'];s=n['authored_step_coverage']
assert not g['gaps'] and not g['missing_required_ingredients']
assert g['inventory_expected']==g['inventory_reviewed']==47
assert g['nodes_expected']==g['nodes_reviewed']==23 and g['relations_expected']==g['relations_reviewed']==39
assert g['dependency_edges']==37 and len(g['future_open_dependency_ids'])==5 and len(g['excluded_association_ids'])==2
assert s['gaps']==s['overlaps']==[] and s['expected_steps']==s['reviewed_steps']==s['formula_body_exact_matches']==8
run=load(d/'source-review.run-evidence84.json')
assert run['all26_primary_anchor_hashes_match'] and run['exact_private_prop_matches_preproof_reviewed_successor']
assert all(run['publication_checks'][k] for k in ['full_statement_read','all12_condition_explanation_rows_read','four_public_formula_rows_and_eight_lesson_formula_rows_checked','statement_and_assumptions_identical_to_packet_and_lesson','publication_binding_independently_recomputed'])
assert run['publication_checks']['fake_closure_scan'] is False
ap=Path('research-wiki/semantic-roundtrip/audits/ASTIS-RT-20261011-PBPSActualOuterBoundedL2Continuity.json');a=load(ap);assert a['state']=='blind-reconstructed'
packet=rt.semantic_reviewer_packet(a);assert packet==load(r/'source-review84.packet.json')
assert packet['packet_sha256']==n['reviewer_packet_sha256'] and a['publication_binding_sha256']==n['publication_binding_sha256']
assert sha(Path(a['lean']['file']).read_bytes())==n['full_module_sha256']
assert load(r/'root.math84.adoption.json')['status']=='ACCEPTED_INDEPENDENT_MATH_ONLY'
(r/'audit.before-source84.json').write_bytes(ap.read_bytes())
deltas=[dict(slot=x['slot'],severity='blocking' if x['blocking'] else 'informational',description=x['description'],evidence=f"Native independent review {x['id']} in {d.as_posix()}/source-review.result84.json, exact current module and eight BODY regions bound by run {runhash}.",native_classification=x['classification']) for x in n['deltas']]
assert all(all(v.get(k) for k in ['original','reconstructed','evidence','relation']) for v in n['semantic_slots'].values())
a.update(state='accepted',semantic_slots=n['semantic_slots'],deltas=deltas,verdict=n['verdict'],source_review=dict(state='accepted',reviewer=n['reviewer'],independent_from_formalizer=True,independent_from_decoder=True,evidence=n['verdict_reason'],review_run_sha256=runhash,reviewer_packet_sha256=n['reviewer_packet_sha256'],run_artifact=(d/'source-review.run-evidence84.json').as_posix(),native_manifest=pin(d/'source-review.run-manifest84.json')))
save(ap,a);pub.inputs.cache_clear();pub.load.cache_clear();pub.check_advance([a['lean']['declaration']],reviewed=True)
new(r/'root.source84.adoption.json',dict(status='ACCEPTED_INDEPENDENT_SOURCE_FIDELITY_ONLY',native_result=pin(d/'source-review.result84.json'),native_manifest=pin(d/'source-review.run-manifest84.json'),native_run_evidence=pin(d/'source-review.run-evidence84.json'),canonical_packet_sha256=packet['packet_sha256'],publication_binding_unchanged=True,publication_binding_sha256=a['publication_binding_sha256'],reviewer=n['reviewer'],full_current_module_RAW_sha256=n['full_module_sha256'],semantic_verdict=n['verdict'],source_graph_coverage=g,VERIFIED=False))
claim=load(r/'claim.json');cp=Path('research-wiki/frontier-cells')/(claim['frontier_cell']+'.json');c=load(cp)
c['evidence'].update(proof_review=(r/'independent-math84/decision84.json').as_posix(),source_review=(d/'source-review.result84.json').as_posix())
c['source_proof_coverage'].update(compiled_source_review=(d/'source-review.result84.json').as_posix(),fresh_source_graph='runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84/source_proof_graph84.reviewed-effective.json',fresh_source_inventory='runs/20261007-companion-priority/pbps-outer-bounded-l2-preread84/source_inventory84.reviewed-effective.json',coverage_status='Independent source inventory47/node23/relation39 (37dependencies including5futureOPEN and2excluded associations) and all eight exact formula/BODY regions accepted. Exact conditional phase probability, state-measurable actual clock expectation,4M² square domination/integrability and outer square-integral zero-time convergence only; all-L2/invariance/contraction/density/process/main/implementation/error/unbounded cost/composition remain OPEN.')
c['blocked']['reason']='Focused compile and independent mathematics/blind/source accepted. Exact-commit verification and sole-lane aggregation pending.'
e=dict(result_kind='theorem-edge',theorem_delta=claim['theorem_delta'],lean_declarations=claim['target_declarations'],publication_declarations=claim['target_declarations'],lean_files=claim['proposed_files'],focused_checks=[pin(r/'focused84-attempt2/receipt.json')],truth_boundary=claim['truth_boundary'],conceptual_mirror_audit=c['conceptual_mirror_audit'],statement_seal=c['statement_seal'],source_proof_coverage=c['source_proof_coverage'],proof_digestion=c['proof_digestion'],purification=c['purification'],independent_math=pin(r/'root.math84.adoption.json'),blind_decoder=pin(r/'root.decoder84.adoption.json'),source_review=pin(r/'root.source84.adoption.json'),integration_notes='Retain actual83 physical phase and pointwise clock expectation; derive exact conditional Gibbs and Gaussian product probability internally, parameter-integral measurability and4M² square domination, then finite-probability filter DCT for outer zero-time square-integral limit. Sole existing stabilization lane only; no self-VERIFIED.')
adv.transition_advance(claim['advance_id'],'PROVED_LOCAL',worker_id=claim['created_by'],evidence=e)
c['status']='proved_locally';save(cp,c);new(r/'proved-local84.json',e)
print('PROVED_LOCAL84; independent exact-commit verification pending')
