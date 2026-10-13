"""Claim one sealed actual normalized endpoint measure integration edge."""
from pathlib import Path
import copy
import json
import subprocess
import sys

sys.path.insert(0, str(Path.cwd() / 'tools'))
import astis_advance as adv

pre = Path(__file__).resolve().parent.relative_to(Path.cwd().resolve())
load = lambda p: json.loads(Path(p).read_bytes())
seal_path = pre / 'root.statement-seal106.json'
seal = load(seal_path)
source = pre.parent / 'pbps-actual-countable-endpoint105/next-primary106'
run = pre.parent / 'pbps-actual-bounded-gibbs-duality106'
aid = 'ASTIS-SA-20261012-PBPSActualBoundedGibbsDuality'
cid = 'ASTIS-SW-PBPS-actual-bounded-gibbs-duality'
decl = seal['proposed_public_theorem']
module = decl.rsplit('.', 1)[0]
lean = module.replace('.', '/') + '.lean'
states = adv.current_advances()
assert aid not in states and not run.exists()
assert [a['advance_id'] for a in states.values() if a['state'] == 'STABILIZING'] == ['ASTIS-SA-20261011-PBPSActualPrescribedPathDensity']
assert subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip() == seal['baseline_commit']
assert load(source.parent / 'integration105/postpush-binding105.json')['remote_head'] == seal['baseline_commit']
parents = seal['actual_producer_plan']
checks = ['lake build ' + module]
searched = [str(source / 'retrieval106.native.json'), str(pre / 'independent-header-math106/header-math-decision106.native.json'),
            'Samplinglib actual105/103 and UnitExponentialProduct; fixed Mathlib Gaussian negation, bounded-integrability, signed Fubini, integral-map and bounded indicator extensionality; compatible upstream screened in source retrieval.']
old = load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-countable-endpoint-law.json')
cell = dict(schema_version=3, cell_id=cid, route='samplewiki-route', title='Actual PBPS bounded Gibbs duality and fixed-time invariance',
    mode='faithfulPaper', declaration_level='source-anchor', source_anchor=seal['source_anchor'],
    target_statement=Path(seal['header']['path']).read_text(encoding='utf8'), status='claimed', parents=parents,
    consumers=[seal['consumer']], target_declarations=[decl],
    evidence=dict(owner=seal['owner'], statement_seal=str(seal_path), focused_checks=checks, owned_files=[lean], truth_boundary=seal['truth_boundary']),
    shared_floor_audit=dict(searched=searched, classification='adapt', decision='adapt_existing', canonical_declaration=decl,
        canonical_shared_cell='', reason='Derive bounded signed Gibbs duality and actual fixed-time phase invariance from the same global actual endpoint witness and its flipped reversal.'),
    reuse_plan=dict(searched_existing=searched, reused_declarations=parents, planned_dependencies=[], new_shared_declarations=[], known_consumers=[],
        planned_consumers=[seal['consumer']], no_duplicate_wrapper=True, decision_reason='Actual bounded signed averaging and fixed-time phase invariance; finite signed integrability, momentum symmetry and normalization are internally proved. No arbitrary process or kernel provider.'),
    reader_contract=copy.deepcopy(old['reader_contract']), blocked=dict(status=False, reason='Exact header and source topology independently accepted;105 delivered. New sphere-Rayleigh main changes await safe shared-surface integration.'))
cell['statement_seal'] = dict(evidence=str(seal_path), source_revision=seal['source_revision'], statement_version=1,
    signature_digest=seal['header']['raw_sha256'], binder_audit=['Six original analytic assumptions; finite real Hilbert Borel typing; no extra premises.'], definition_kind=seal['definition_audit'])
cell['source_proof_coverage'] = dict(source_graph=seal['source_graph']['path'], source_inventory=seal['source_coverage']['path'],
    coverage_report=seal['independent_topology']['path'], coverage_status='Prospective source graph independently accepted with counts ' + str(seal['source_topology_counts']) + ';106 theorem unproved.')
cell['source_detail_audit'] = dict(primary_edition=seal['source_revision'], primary_anchor=seal['source_anchor'], fidelity_boundary=seal['truth_boundary'],
    detail_status='omitted', gap='Expand the final Appendix A.1 bounded signed bilinear identity and F=1 fixed-time stationarity argument with explicit signed integrability and phase-flip normalization.',
    consulted=[dict(source='Pinned PBPS v1, actual Samplinglib producers and fixed Mathlib', anchor='Appendix A.1 averaging/change of variables and Eq3.1',
        hypothesis_adapter='Original six assumptions and all actual algorithm definitions retained. Same actual global Z is retained; bounded observable integrability, signed Fubini and actual Gaussian momentum symmetry are internally derived.')])
cell['proof_digestion'] = dict(existing_substrate=parents, bookkeeping=['Actual normalized phase and clock probability plus Gaussian momentum flip',
    'Bounded section/product/outer integrability and signed Fubini for actual Z', 'Use105 flipped endpoint law for bounded duality; F=1 and bounded indicators identify actual fixed-time marginal'],
    new_reusable=[], new_topology=seal['core_delta'])
cell['purification'] = dict(status='pending', dead_code_audit='No implementation yet.', duplicate_semantics_audit='No existing theorem gives this same actual Z bounded signed duality and Gibbs invariance;105 supplies endpoint measure reversal only. Separate83 existential witness is not substituted.',
    canonicalization='Consume actual public105/103 and UnitExponentialProduct producers and fixed Mathlib; no duplicate generic lemmas.', compressed_spine_delta=seal['core_delta'],
    reader_default_view='Full attributed measure statement and adjacent folded Lean; stepwise formula proof.', scope=seal['truth_boundary'])
lc = copy.deepcopy(old['learning_contract'])
lc['parallelism'] = dict(decision='serial', direction_fingerprints=['actual-bounded-gibbs-duality'],
    expected_information_gain='One proving owner and independent mathematics, source-blind decoder and source reviewers.', shared_verified_context_digest=seal['header']['raw_sha256'])
lc['reader_backpressure'] = dict(purification_status='pending', exposition_seal_status='pending', exposition_evidence='',
    source_expansion_nodes=['PHASE-FLIP106', 'SIGNED-FUBINI106', 'AVG100', 'INV100'], lean_expansion_nodes=[decl], assumptions_preserved=False, boundary_preserved=False)
cell['learning_contract'] = lc
cell['graph_contribution'] = dict(lean_view='integration-node', overview_view='no-change-with-reason', functor_view='none-found',
    edge_semantics='formal-solid; overlays-dashed', color_semantics='evidence-status; library-scope', focus_targets=[decl], visual_review='Pending implementation and publication.')
cell['conceptual_mirror_audit'] = dict(status='none-found', reason='Bounded expectation duality and momentum symmetry are existing measure mechanisms; no new conceptual mirror claimed before proof.', discovery_ids=[])
path = Path('research-wiki/frontier-cells') / (cid + '.json')
assert not path.exists()
run.mkdir()
path.write_text(json.dumps(cell, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
proposal = adv.AdvanceProposal(advance_id=aid, task_id='ASTIS-SW-PBPS-2026', goal=seal['core_delta'], source_anchor=seal['source_anchor'],
    theorem_delta=seal['core_delta'], truth_boundary=seal['truth_boundary'], created_by=seal['owner'], dag_inputs=tuple(parents),
    proposed_files=(lean,), focused_checks=tuple(checks), modes=('faithfulPaper',), priority=100, frontier_cell=cid, target_declarations=(decl,))
adv.propose_advance(proposal)
evidence = dict(statement_seal=str(seal_path), source_graph=seal['source_graph']['path'], owner_files=[lean],
    upstream_delivery=str(source.parent / 'integration105/postpush-binding105.json'))
for state in ['CLAIMED', 'EXPLORING']:
    adv.transition_advance(aid, state, worker_id=seal['owner'], modes=['faithfulPaper'], evidence=evidence)
(run / 'claim.json').write_text(json.dumps(proposal.as_event(), ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print('One106 owner claimed; existing sole94 stabilization lane retained.')
