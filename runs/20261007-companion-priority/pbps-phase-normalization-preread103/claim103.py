"""Claim one sealed normalization boundary after verified102 remote delivery."""
from pathlib import Path
import copy, json, subprocess, sys

root = Path.cwd()
sys.path.insert(0, str(root / 'tools'))
import astis_advance as adv

pre = Path(__file__).parent
load = lambda p: json.loads(Path(p).read_bytes())
seal = load(pre / 'root.statement-seal103.json')
previous = pre.parent / 'pbps-actual-weighted-sector102'
source = previous / 'next-primary103'
run = pre.parent / 'pbps-actual-phase-normalization103'
aid = 'ASTIS-SA-20261012-PBPSActualPhaseNormalization'
cid = 'ASTIS-SW-PBPS-actual-phase-normalization'
decl = seal['proposed_public_theorem']
module = decl.rsplit('.', 1)[0]
lean = module.replace('.', '/') + '.lean'
states = adv.current_advances()
assert aid not in states and not run.exists()
assert [a['advance_id'] for a in states.values() if a['state'] == 'STABILIZING'] == ['ASTIS-SA-20261011-PBPSActualPrescribedPathDensity']
assert subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip() == seal['baseline_commit']
assert load(previous / 'integration102/postpush-binding102.json')['remote_head'] == seal['baseline_commit']
parents = seal['actual_producer_plan']
checks = ['lake build ' + module]
searched = ['Samplinglib shared Hessian/Gibbs/Gaussian producers, fixed Mathlib tilted and product density APIs; compatible upstream catalog checked in source retrieval.', str(source / 'retrieval103.native.json'), str(pre / 'independent-header-math103/header-math-decision103.native.json')]
old = load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-weighted-sector.json')
cell = dict(
    schema_version=3, cell_id=cid, route='samplewiki-route', title='Actual PBPS phase Gibbs normalization',
    mode='faithfulPaper', declaration_level='source-anchor', source_anchor=seal['source_anchor'],
    target_statement=Path(seal['header']['path']).read_text(encoding='utf8'), status='claimed',
    parents=parents, consumers=[seal['consumer']], target_declarations=[decl],
    evidence=dict(owner=seal['owner'], statement_seal=str(pre / 'root.statement-seal103.json'), focused_checks=checks, owned_files=[lean], truth_boundary=seal['truth_boundary']),
    shared_floor_audit=dict(searched=searched, classification='adapt', decision='adapt_existing', canonical_declaration=decl, canonical_shared_cell='', reason='Compose canonical shared Hessian/Gibbs tail/Gaussian density producers to identify the actual phase probability law; no new generic copy.'),
    reuse_plan=dict(searched_existing=searched, reused_declarations=parents, planned_dependencies=[], new_shared_declarations=[], known_consumers=[], planned_consumers=[seal['consumer']], no_duplicate_wrapper=True, decision_reason='New exact phase partition and normalized product-law bridge. Independent of102; no supplied normalizer, minimizer or regularity premises.'),
    reader_contract=copy.deepcopy(old['reader_contract']),
    blocked=dict(status=False, reason='Prospective exact statement and source topology independently accepted;102 remotely delivered.'))
cell['statement_seal'] = dict(evidence=str(pre / 'root.statement-seal103.json'), source_revision=seal['source_revision'], statement_version=1, signature_digest=seal['header']['raw_sha256'], binder_audit=['Original six analytic assumptions; finite real Hilbert Borel typing. No excess binders.'], definition_kind=seal['definition_audit'])
cell['source_proof_coverage'] = dict(source_graph=seal['source_graph']['path'], source_graph_overlay=seal['source_graph_overlay']['path'], source_inventory=seal['source_coverage']['path'], coverage_report=seal['independent_topology']['path'], coverage_status='Source-only graph and namespace-only overlay independently accepted; phase normalization unproved.')
cell['source_detail_audit'] = dict(primary_edition=seal['source_revision'], primary_anchor=seal['source_anchor'], fidelity_boundary=seal['truth_boundary'], detail_status='omitted', gap='Source proportionality requires positive finite partition and equality of exact withDensity and product laws.', consulted=[dict(source='Pinned PBPS v1, Samplinglib and fixed Mathlib', anchor='Conditional energy and Eq3.1; Appendix A1 initial averaging as consumer.', hypothesis_adapter='Original six assumptions retained. Actual target energy, position-first phase volume, standard momentum variance and zero-dimensional convention preserved.')])
cell['proof_digestion'] = dict(existing_substrate=parents, bookkeeping=['Proximal domination and all-y positive position mass', 'Gaussian factor and real/ENNReal partition conversion', 'Exact tilted/product density identification'], new_reusable=[], new_topology=seal['core_delta'])
cell['purification'] = dict(status='pending', dead_code_audit='No implementation yet.', duplicate_semantics_audit='Existing Gaussian augmentation uses a different joint law; no duplicate canonical leaf.', canonicalization='Consume shared public producers; no added normalizer or minimizer premise.', compressed_spine_delta=seal['core_delta'], reader_default_view='Complete attributed normalization statement and adjacent folded Lean with stepwise formula proof.', scope=seal['truth_boundary'])
lc = copy.deepcopy(old['learning_contract'])
lc['parallelism'] = dict(decision='serial', direction_fingerprints=['actual-phase-partition-normalization'], expected_information_gain='One implementation owner; independent mathematical, blind and source reviewers.', shared_verified_context_digest=seal['header']['raw_sha256'])
lc['reader_backpressure'] = dict(purification_status='pending', exposition_seal_status='pending', exposition_evidence='', source_expansion_nodes=['NORM'], lean_expansion_nodes=[decl], assumptions_preserved=False, boundary_preserved=False)
cell['learning_contract'] = lc
cell['graph_contribution'] = dict(lean_view='integration-node', overview_view='no-change-with-reason', functor_view='none-found', edge_semantics='formal-solid; overlays-dashed', color_semantics='evidence-status; library-scope', focus_targets=[decl], visual_review='Pending implementation and publication.')
cell['conceptual_mirror_audit'] = dict(status='none-found', reason='Concrete actual phase normalization through existing canonical Gibbs/Gaussian facts; no new cross-domain bridge.', discovery_ids=[])
path = Path('research-wiki/frontier-cells') / (cid + '.json')
assert not path.exists()
run.mkdir()
path.write_text(json.dumps(cell, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
proposal = adv.AdvanceProposal(advance_id=aid, task_id='ASTIS-SW-PBPS-2026', goal=seal['core_delta'], source_anchor=seal['source_anchor'], theorem_delta=seal['core_delta'], truth_boundary=seal['truth_boundary'], created_by=seal['owner'], dag_inputs=tuple(parents), proposed_files=(lean,), focused_checks=tuple(checks), modes=('faithfulPaper',), priority=100, frontier_cell=cid, target_declarations=(decl,))
adv.propose_advance(proposal)
evidence = dict(statement_seal=str(pre / 'root.statement-seal103.json'), source_graph=seal['source_graph']['path'], owner_files=[lean], upstream102_remote_delivery=str(previous / 'integration102/postpush-binding102.json'))
for state in ['CLAIMED', 'EXPLORING']:
    adv.transition_advance(aid, state, worker_id=seal['owner'], modes=['faithfulPaper'], evidence=evidence)
(run / 'claim.json').write_text(json.dumps(proposal.as_event(), ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print('One103 owner claimed; existing sole94 stabilization lane retained.')
