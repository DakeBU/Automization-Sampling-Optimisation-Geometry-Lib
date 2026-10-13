from pathlib import Path
r=Path(__file__).parent
s=Path('runs/20261007-companion-priority/pbps-actual-bounded-test-continuity83/adopt_source_and_prove83.py').read_text(encoding='utf8')
for a,b in [('independent-source83','independent-source84'),('source-review.result83','source-review.result84'),('source-review.run-manifest83','source-review.run-manifest84'),('source-review.run-evidence83','source-review.run-evidence84'),('source-review83.packet','source-review84.packet'),('root.math83.adoption','root.math84.adoption'),('root.source83.adoption','root.source84.adoption'),('root.decoder83.adoption','root.decoder84.adoption'),('audit.before-source83','audit.before-source84'),('independent-math83/decision83','independent-math84/decision84'),('ASTIS-RT-20261010-PBPSActualBoundedTestContinuity','ASTIS-RT-20261011-PBPSActualOuterBoundedL2Continuity'),('focused83-attempt3','focused84-attempt2'),('proved-local83','proved-local84'),('PROVED_LOCAL83','PROVED_LOCAL84'),('pbps-bounded-test-preread83','pbps-outer-bounded-l2-preread84'),('source_proof_graph83.reviewed-effective','source_proof_graph84.reviewed-effective'),('source_inventory83.json','source_inventory84.reviewed-effective.json')]:
 assert a in s,a;s=s.replace(a,b)
s=s.replace(" and n['no_required_exposition_repairs']",'')
a=s.index("assert n['independence']['source_first_graph_frozen_before_any83header']")
b=s.index("ap=Path(",a)
s=s[:a]+'''assert n['independent_from_formalizer'] and n['independent_from_decoder']
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
'''+s[b:]
s=s.replace('Independent source inventory30/node17/relation30 (29dependencies and1excluded-boundary association) and alleight exact formula/BODY regions accepted. Actual bounded-test measurable integrable clock pullbacks,2M defect estimate and fixedparameter expectation continuity only; full L2/Markov/restart/semigroup/invariance/main/implementation/error/cost/composition remain OPEN.','Independent source inventory47/node23/relation39 (37dependencies including5futureOPEN and2excluded associations) and all eight exact formula/BODY regions accepted. Exact conditional phase probability, state-measurable actual clock expectation,4M² square domination/integrability and outer square-integral zero-time convergence only; all-L2/invariance/contraction/density/process/main/implementation/error/unbounded cost/composition remain OPEN.')
s=s.replace('Actual bounded-test integrability and integrated2M indicator discrepancy under the actual clock probability law, consuming actual82 phase-defect bound; flow/hazard continuity and squeeze yield expectation limit; retain complete actual phase semantics.','Retain actual83 physical phase and pointwise clock expectation; derive exact conditional Gibbs and Gaussian product probability internally, parameter-integral measurability and4M² square domination, then finite-probability filter DCT for outer zero-time square-integral limit.')
p=r/'adopt_source_and_prove84.py';assert not p.exists();p.write_text(s,encoding='utf8',newline='\n')
