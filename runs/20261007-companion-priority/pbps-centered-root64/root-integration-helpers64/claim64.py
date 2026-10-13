from pathlib import Path
import copy, json, hashlib, sys
root=Path.cwd(); pre=root/'runs/20261007-companion-priority/pbps-centered-root-preproof64'
load=lambda p:json.loads(Path(p).read_bytes())
def w(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
seal=load(pre/'root.statement-seal64.json')
assert seal['status']=='STATEMENT64_SEALED_NOT_PROVED_NOT_CLAIMED'
assert all(hashlib.sha256((pre/f'header{i}.lean').read_bytes()).hexdigest()==seal['headers'][i]['raw_sha256'] for i in range(2))
sys.path.insert(0,str(root/'tools'));import astis_advance as adv
r=root/'runs/20261007-companion-priority/pbps-centered-root64';r.mkdir(exist_ok=False)
aid='ASTIS-SA-20261009-PBPSCenteredRootOrderInverse';cid='ASTIS-SW-PBPS-centered-root-order-inverse';owner='companion_root_20261005'
generic='AutoSamplingTheory.TechnicalLemmas.Measure.L2RealSquareOrder.positive_square_order'
actual='AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredRootOrderInverse.actual_centered_root_order_inverse'
files=['AutoSamplingTheory/TechnicalLemmas/Measure/L2RealSquareOrder.lean','AutoSamplingTheory/ExampleCases/ProximalBPS/CenteredRootOrderInverse.lean','Tests/ProximalBPSCenteredRootOrderInverse.lean']
assert all(not (root/p).exists() for p in files)
parents=['ASTIS-SW-PBPS-unique-macroscopic-defect-root','ASTIS-SW-PBPS-rough-mean-gradient','ASTIS-SHARED-gaussian-marginal-poincare','ASTIS-SW-PBPS-centered-selfadjoint-defect','ASTIS-SHARED-l2-real-complex-positive-lift']
assert all((root/'research-wiki/frontier-cells'/f'{p}.json').exists() for p in parents)
anchor='PBPS arXiv2609.06905v1 AppendixB15, genuine next B16 consumer; C2/C3/C4; exact original C2 and both Hessian bounds, eta cap; D1 real Hilbert order.'
boundary='Same actual centered macro GammaP0 has printed B15 operator order gamma I, derived unit/bounded inverse/norm with gamma=2sqrt(alpha eta)/(1+alpha eta). No full-space inverse, extra gap/onto/unit/root premise, Test import, nontriviality or higher derivative. B16 polar, B13 H1, B14 independent branch, dynamics/main/errors/query cost and actual-input composition remain open.'
delta='Canonical three complex lifts prove arbitrary-real-L2 positive square order; production C4 assembly from actual rough mean gradient and Gaussian marginal Poincare gives same actual GammaP centered order and bounded inverse, a necessary genuine B16 input.'
proposal=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=delta,source_anchor=anchor,theorem_delta=delta,truth_boundary=boundary,created_by=owner,dag_inputs=tuple(parents),proposed_files=tuple(files),focused_checks=('lake build Tests.ProximalBPSCenteredRootOrderInverse',),modes=('faithfulPaper',),priority=100,frontier_cell=cid,target_declarations=(generic,actual))
ledger=root/'runs/substantive_advances.jsonl';raw=ledger.read_bytes();(r/'ledger.before64.exactraw.snapshot').write_bytes(raw)
w(r/'ledger-history.json',dict(original_path=ledger.as_posix(),original_raw_sha256=hashlib.sha256(raw).hexdigest(),exact_snapshot=(r/'ledger.before64.exactraw.snapshot').as_posix()))
adv.propose_advance(proposal)
adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence=dict(preproof_seal=(pre/'root.statement-seal64.json').as_posix(),owned_files=files))
adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence=dict(route=delta,scope=boundary))
c=copy.deepcopy(load(root/'research-wiki/frontier-cells/ASTIS-SW-PBPS-unique-macroscopic-defect-root.json'))
graph=load(pre/'independent-primary64/source-proof-graph.json')
review=load(pre/'independent-header64/independent-header64.review.json')
c.update(cell_id=cid,title='Actual PBPS centered root order and bounded inverse',source_anchor=anchor,target_statement=(pre/'header1.lean').read_text(encoding='utf-8'),status='claimed',parents=parents,consumers=[actual,'Printed B16 normalized leakage V=B0 GammaP0 inverse and polar isometry; next actual consumer, unproved.'],blocked=dict(status=False,reason='Exact source-first independently reviewed and TYPE-elaborated Statement Seal; no64 proof yet.'),evidence=dict(substantive_advance=aid,statement_seal=(pre/'root.statement-seal64.json').as_posix(),focused_checks=[],owned_files=files,truth_boundary=boundary))
searched=['Pinned Mathlib CFC sqrt monotonicity, positivity, norm/inner coercivity units; existing arbitrary-L2 real/complex lift and actual63 canonical macro root; actual RoughMeanGradient/GaussianMarginalPoincare; module cards/source-first independent64 1086-item graph/coverage.']
reused=['AutoSamplingTheory.ExampleCases.ProximalBPS.MacroscopicDefectRoot.actual_unique_positive_macroscopic_defect_root','AutoSamplingTheory.ExampleCases.ProximalBPS.RoughMeanGradient.actual_rough_mean_gradient','AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianMarginalPoincare.actual_gaussian_marginal_centered_poincare','AutoSamplingTheory.ExampleCases.ProximalBPS.CenteredDefectOperator.actual_centered_selfadjoint_defect','AutoSamplingTheory.TechnicalLemmas.Measure.L2RealComplexOperator.exists_positive_complex_lift']
c['shared_floor_audit']=dict(searched=searched,classification='adapt',decision='adapt_existing',canonical_declaration=reused[-1],canonical_shared_cell=parents[-1],reason='Minimal arbitrary-real-L2 order leaf supplies actual printed B15 and same-root inverse for B16; no ambient-subtype CFC assumption.')
c['reuse_plan']=dict(searched_existing=searched,reused_declarations=reused,new_shared_declarations=[generic],known_consumers=[actual],planned_consumers=[c['consumers'][1]],no_duplicate_wrapper=True,decision_reason=c['shared_floor_audit']['reason'])
c['statement_seal']=dict(evidence=(pre/'root.statement-seal64.json').as_posix(),source_revision='2609.06905v1/Lean4.33.0/Mathlibdb584cd6',statement_version=1,signature_digest=seal['headers'][1]['raw_sha256'],binder_audit=(pre/'independent-header64/independent-header64.review.json').as_posix(),definition_kind='Same63 actual root; exact mean kernel HP0; inherited subtype instances; gamma positive derived; bounded inverse only HP0.')
c['source_proof_coverage']=dict(source_graph=(pre/'independent-primary64/source-proof-graph.json').as_posix(),source_inventory=(pre/'independent-primary64/source-coverage-inventory.json').as_posix(),coverage_report=(pre/'independent-header64/independent-header64.review.json').as_posix(),coverage_status='1086 literal items classified, ten primary regions, no missing alttext; independent source topology sealed before exact headers.')
c['source_detail_audit'].update(primary_anchor=anchor,fidelity_boundary=boundary,gap='C4 production join and same-root order/inverse unproved; three-lift real adapter needed rather than extra public CFC/gap hypothesis.',consulted=[dict(source='Exact PBPSv1 primary and pinned Mathlib; source-first independent64',anchor='B15; C2/C3/C4 and B16 actual-input consumer',hypothesis_adapter='Only original C2/two Hessian/positive capped eta; derived subtype norm/inner/complete and quantitative inverse.',expanded_binder_audit=review['recursive_binder_audit'])])
lc=c['learning_contract'];lc['failure_class']='IMPLEMENTATION_FAILED'
lc['salvage']=dict(required=True,status='completed',reason='Preproof TYPE1 inferred nested-subtype instances repaired internally; original theorem assumptions and conclusions unchanged; all negative receipts preserved.',promoted_fragments=[],discarded_fragments=[])
lc['parallelism'].update(decision='serial',direction_fingerprints=['real-L2-square-order/actual-C4/constant-projection/centered-inverse'],shared_verified_context_digest=seal['whole_logical_run_sha256'],expected_information_gain='Sole production writer; mandatory independent review modes remain distinct.')
lc['reader_backpressure'].update(purification_status='pending',exposition_seal_status='pending',exposition_evidence='',source_expansion_nodes=[x['id'] for x in graph['nodes']],lean_expansion_nodes=[generic,actual])
c['graph_contribution'].update(lean_view='integration-node',overview_view='updated',functor_view='none-found',focus_targets=[generic,actual],visual_review='Pending64 proof/publication; no graph work blocks correctness.')
c['proof_digestion']=dict(existing_substrate=reused,bookkeeping=['Canonical actual roots, constants and closed centered mean kernel; SAME witnesses and quantitative gamma.'],new_reusable=[generic],new_topology='Exact real order adapter joins C4 sharp contraction to B15 root order and internally derived bounded inverse for B16.')
c['purification']=dict(status='pending',dead_code_audit='No new proof yet.',duplicate_semantics_audit='Minimal real-L2 order leaf; existing parents reused.',canonicalization='Same actual63 GammaP and exact mean kernel.',compressed_spine_delta=c['proof_digestion']['new_topology'],reader_default_view='Existing companion formula steps and adjacent folded exact Lean.',scope=boundary)
c.pop('conceptual_mirror_audit',None)
w(root/'research-wiki/frontier-cells'/f'{cid}.json',c);w(r/'claim.json',proposal.as_event());w(r/'preproof-admission.json',seal)
print(aid,'EXPLORING; exact64 statements sealed and single owner claimed; no theorem proved. B16 genuine consumer remains open.')
