"""Claim one independently sealed deterministic PBPS source edge."""
from pathlib import Path
import json,hashlib,sys
R=Path(__file__).resolve().parents[3];sys.path.insert(0,str(R))
from tools import astis_advance as adv
r=Path(__file__).resolve().parent;pre=r.parent/'pbps-prescribed-path-density-preread94';old=r.parent/'pbps-actual-finite-count-path93'
load=lambda p:json.loads(Path(p).read_bytes())
def rel(p):return Path(p).relative_to(R).as_posix()
def pin(p):
    p=Path(p);return dict(path=rel(p),raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):
    assert not p.exists(),p
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
seal=load(pre/'root.statement-seal94.json')
for row in seal['all_review_bound_inputs_rehashed']:
    assert hashlib.sha256((R/row['path']).read_bytes()).hexdigest()==row['raw_sha256'],row['path']
assert pin(pre/'Header94.lean')['raw_sha256']==seal['header']['raw_sha256']
for row in load(old/'exact-commit-verification93/closed-RAW-manifest93.json')['preserved_collaborator_inputs']:
    assert hashlib.sha256((R/row['path']).read_bytes()).hexdigest()==row['raw_sha256'],row['path']
aid='ASTIS-SA-20261011-PBPSActualPrescribedPathDensity';cid='ASTIS-SW-PBPS-actual-prescribed-path-density'
module='AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPrescribedPathDensity.lean'
decl=seal['proposed_public_theorem'];owner='companion_root_20261005'
assert aid not in adv.current_advances() and not (R/module).exists()
assert [v['advance_id'] for v in adv.current_advances().values() if v['state']=='STABILIZING']==['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
parents=['AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_laws','AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock.actual_integrated_hazard_clock_laws']
anchor='Chen-Chewi-Lu-Zhang arXiv2609.06905v1 Appendix A.1 (A.1),(A.2), prescribed trajectories and (A.7) finite-sector density. Source graph DENSITY94/HAZARD93/LEFT93/TERM93.'
delta='For every finite prescribed strict event tuple, derive rate integrability, the n+1-arc integrated-hazard identity, incoming phase and rate left limits, and exact rewriting of rho as whole-path survival times all incoming rates.'
boundary='Same six source analytic assumptions and finite-dimensional real Hilbert Borel phase, including rank zero. Twenty literal definitions from actual93 plus finite grid and clamped real-time extension; every finite n and NNReal T including zero. Integrability, left limits and density rewriting are conclusions, not supplied providers. Clamping agrees on [0,T] and is locally inactive at each interior jump; no Skorokhod claim. Full A7 countable assembly/signed tests, restart/Markovness, invariance, hypocoercivity, errors, expected costs, main results, actual-input composition and four full papers remain open.'
search=[rel(p) for p in sorted((r/'retrieval94').glob('*.log'))]
cell=dict(schema_version=3,cell_id=cid,route='samplewiki-route',title='Actual PBPS prescribed-path hazard and density identity',mode='faithfulPaper',source_anchor=anchor,target_statement=(pre/'Header94.lean').read_text(encoding='utf8'),status='claimed',parents=parents,consumers=['PBPS A1.E7 finite-sector expression TERM93, composing already verified JOINT93 (planned integration, unproved)'],source_targets=[decl],declaration_level='source-anchor',blocked=dict(status=False,reason='Exact independent pre-proof statement seal accepted; one writer starting implementation.'),
 evidence=dict(substantive_advance=aid,statement_seal=rel(pre/'root.statement-seal94.json'),focused_checks=[],owned_files=[module],truth_boundary=boundary),
 shared_floor_audit=dict(searched=search+['Libraries/shared-foundations.yml','Libraries/frontloaded-shared-spine.json'],classification='adapt',decision='adapt_existing',canonical_declaration=decl,canonical_shared_cell='',reason='Reuse actual93 pointwise interpolation and pinned finite-interval/topology APIs; one deterministic density identification consumer.'),
 reuse_plan=dict(searched_existing=search,reused_declarations=[],planned_dependencies=parents,new_shared_declarations=[],known_consumers=[],planned_consumers=['PBPS A1.E7 finite-sector expression'],no_duplicate_wrapper=True,decision_reason='Missing hazard/left-limit identification is a genuine mathematical bridge, not a restatement of an assumed density.'),
 reader_contract=dict(reference_standard='textbook/chapter-01/section-1-3.html',source_ordered=True,source_statement_adjacent=True,natural_language_formula_proof=True,hidden_assumptions_visible=True,lean_collapsed=True,external_dependencies_visible=True),
 statement_seal=dict(evidence=rel(pre/'root.statement-seal94.json'),source_revision=seal['source_revision'],statement_version=1,signature_digest=seal['header']['raw_sha256'],binder_audit=['hα,hαβ,hV,hH,hη,hβη are the original six analytic assumptions.','Finite Hilbert/Borel structure includes disclosed rank zero.','Integrability, phase/rate left limits and density equality are conclusions.'],definition_kind='20 unchanged literal lets and two internal representation lets (finite grid and clamped real extension); no provider hypothesis.'),
 source_proof_coverage=dict(source_graph=seal['source_graph']['path'],source_inventory=seal['source_coverage']['path'],coverage_report=seal['independent_source_header']['path'],coverage_status='Independent pre-proof graph and prospective statement audit only; no proof coverage admission.'),
 source_detail_audit=dict(primary_edition=seal['source_revision'],primary_anchor=anchor,fidelity_boundary=boundary,detail_status='omitted',gap='Finite piecewise integration and pre-jump left-limit justification implicit in the printed path density.',consulted=[dict(source='Pinned PBPS v1 and fixed Lean/Mathlib',anchor='A1.E1; A1.E2; A1.E7; prescribed-path paragraph',hypothesis_adapter='Six analytic binders retained. Pointwise clamping is an auxiliary extension; endpoint null sets justify integration only.')]),
 proof_digestion=dict(existing_substrate=parents,bookkeeping=['Finite grid and clamped real extension'],new_reusable=[],new_topology=delta),
 purification=dict(status='pending',dead_code_audit='Proof not implemented.',duplicate_semantics_audit='Local, fixed Mathlib, shared frontier and compatible upstream inventory searches recorded.',canonicalization='Reuse existing literal path93 interpolation and rate/flow calculus.',compressed_spine_delta=delta,reader_default_view='Attributed statement and formula proof with adjacent folded exact Lean.',scope=boundary),
 learning_contract=dict(control_plane_math_authority=False,process_memory_checked=True,process_memory_ids=[],failure_class='NONE',salvage=dict(required=False,status='not-applicable',reason='No proof route has failed or been discarded.',promoted_fragments=[],discarded_fragments=[]),parallelism=dict(decision='serial',direction_fingerprints=['prescribed-path/hazard-splitting/left-limits/density'],expected_information_gain='One proof writer; independent mathematical and source statement uncertainty already reviewed.',shared_verified_context_digest=seal['header']['raw_sha256']),cross_route_blind_spot_audit=dict(required=False,status='not-applicable',evidence='',canonical_route='samplewiki-route',selection_reason='Single implementation route; source OR alternatives for later A7 retained.'),reader_backpressure=dict(purification_status='pending',exposition_seal_status='pending',exposition_evidence='',source_expansion_nodes=['A1.E1','A1.E2','A1.E7'],lean_expansion_nodes=[decl],assumptions_preserved=False,boundary_preserved=False)),
 graph_contribution=dict(lean_view='integration-node',overview_view='no-change-with-reason',functor_view='none-found',edge_semantics='formal-solid; overlays-dashed',color_semantics='evidence-status; library-scope',focus_targets=[decl],visual_review='Pending implementation and publication; existing PBPS route retained.'))
write(R/'research-wiki/frontier-cells'/f'{cid}.json',cell)
p=adv.AdvanceProposal(advance_id=aid,task_id='ASTIS-SW-PBPS-2026',goal=delta,source_anchor=anchor,theorem_delta=delta,truth_boundary=boundary,created_by=owner,dag_inputs=tuple(parents),proposed_files=(module,),focused_checks=('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity',),modes=('faithfulPaper',),priority=100,frontier_cell=cid,target_declarations=(decl,))
adv.propose_advance(p);write(r/'claim.json',p.as_event())
adv.transition_advance(aid,'CLAIMED',worker_id=owner,evidence={'statement_seal':pin(pre/'root.statement-seal94.json')})
adv.transition_advance(aid,'EXPLORING',worker_id=owner,evidence={'proof_route':'Reuse pointwise finite-path arcs, derive interval integration and one-sided limits, then rewrite finite density algebraically.'})
print(aid,'EXPLORING; no proof completion credit')
