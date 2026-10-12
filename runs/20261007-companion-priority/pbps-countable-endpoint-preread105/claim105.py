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
seal_path = pre / 'root.statement-seal105.json'
seal = load(seal_path)
source = pre.parent / 'pbps-actual-normalized-endpoint104/next-primary105'
run = pre.parent / 'pbps-actual-countable-endpoint105'
aid = 'ASTIS-SA-20261012-PBPSActualCountableEndpointLaw'
cid = 'ASTIS-SW-PBPS-actual-countable-endpoint-law'
decl = seal['proposed_public_theorem']
module = decl.rsplit('.', 1)[0]
lean = module.replace('.', '/') + '.lean'
states = adv.current_advances()
assert aid not in states and not run.exists()
assert [a['advance_id'] for a in states.values() if a['state'] == 'STABILIZING'] == ['ASTIS-SA-20261011-PBPSActualPrescribedPathDensity']
assert subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip() == seal['baseline_commit']
assert load(source.parent / 'integration104/postpush-binding104.json')['remote_head'] == seal['baseline_commit']
parents = seal['actual_producer_plan']
checks = ['lake build ' + module]
searched = [str(source / 'retrieval105.native.json'), str(pre / 'independent-header-math105/header-math-decision105.native.json'),
            'Samplinglib actual93/103/104 and UnitExponentialProduct; fixed Mathlib nonnegative count partition, Tonelli, countable measure sum, sigma-finiteness, lintegral/map and measure extensionality APIs; compatible upstream searched in retrieval.']
old = load('research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-normalized-endpoint-sector.json')
cell = dict(schema_version=3, cell_id=cid, route='samplewiki-route', title='Actual normalized PBPS countable endpoint law',
    mode='faithfulPaper', declaration_level='source-anchor', source_anchor=seal['source_anchor'],
    target_statement=Path(seal['header']['path']).read_text(encoding='utf8'), status='claimed', parents=parents,
    consumers=[seal['consumer']], target_declarations=[decl],
    evidence=dict(owner=seal['owner'], statement_seal=str(seal_path), focused_checks=checks, owned_files=[lean], truth_boundary=seal['truth_boundary']),
    shared_floor_audit=dict(searched=searched, classification='adapt', decision='adapt_existing', canonical_declaration=decl,
        canonical_shared_cell='', reason='Assemble the actual Gibbs-initialized clock-process endpoint law from all finite-count sectors and transfer their common reversal.'),
    reuse_plan=dict(searched_existing=searched, reused_declarations=parents, planned_dependencies=[], new_shared_declarations=[], known_consumers=[],
        planned_consumers=[seal['consumer']], no_duplicate_wrapper=True, decision_reason='New actual process endpoint probability law. Joint measurability, nonnegative countable assembly and exact sector normalization are internal dependencies, never provider hypotheses.'),
    reader_contract=copy.deepcopy(old['reader_contract']), blocked=dict(status=False, reason='Exact header and source topology independently accepted;104 delivered. New sphere-gradient main changes await safe shared-surface integration.'))
cell['statement_seal'] = dict(evidence=str(seal_path), source_revision=seal['source_revision'], statement_version=1,
    signature_digest=seal['header']['raw_sha256'], binder_audit=['Six original analytic assumptions; finite real Hilbert Borel typing; no extra premises.'], definition_kind=seal['definition_audit'])
cell['source_proof_coverage'] = dict(source_graph=seal['source_graph']['path'], source_inventory=seal['source_coverage']['path'],
    coverage_report=seal['independent_topology']['path'], coverage_status='Prospective source graph independently accepted with counts ' + str(seal['source_topology_counts']) + ';105 theorem unproved.')
cell['source_detail_audit'] = dict(primary_edition=seal['source_revision'], primary_anchor=seal['source_anchor'], fidelity_boundary=seal['truth_boundary'],
    detail_status='omitted', gap='Expand source initial-phase averaging and nonnegative Tonelli into the actual countable endpoint-pair probability law.',
    consulted=[dict(source='Pinned PBPS v1, actual Samplinglib producers and fixed Mathlib', anchor='Appendix A.1 averaging/change of variables and Eq3.1',
        hypothesis_adapter='Original six assumptions and all actual algorithm definitions retained. Joint endpoint/density measurability, simplex sigma-finiteness, measurable parameter integrals and countable exchange are internally derived.')])
cell['proof_digestion'] = dict(existing_substrate=parents, bookkeeping=['Simplex sigma-finiteness and actual endpoint/density measurability',
    'Partition fixed-initial count fibers and exchange nonnegative sums with initial-phase integration', 'Identify Q=sum L_n; probability from actual product and reversal from104 plus map_sum'],
    new_reusable=[], new_topology=seal['core_delta'])
cell['purification'] = dict(status='pending', dead_code_audit='No implementation yet.', duplicate_semantics_audit='No existing actual normalized countable endpoint law found;104 concerns fixed count only.',
    canonicalization='Consume actual public93/103/104 and UnitExponentialProduct producers and fixed Mathlib; no duplicate generic lemmas.', compressed_spine_delta=seal['core_delta'],
    reader_default_view='Full attributed measure statement and adjacent folded Lean; stepwise formula proof.', scope=seal['truth_boundary'])
lc = copy.deepcopy(old['learning_contract'])
lc['parallelism'] = dict(decision='serial', direction_fingerprints=['actual-countable-endpoint-law'],
    expected_information_gain='One proving owner and independent mathematics, source-blind decoder and source reviewers.', shared_verified_context_digest=seal['header']['raw_sha256'])
lc['reader_backpressure'] = dict(purification_status='pending', exposition_seal_status='pending', exposition_evidence='',
    source_expansion_nodes=['SECTOR-INTEGRAL-MEAS105', 'ASSEMBLY105', 'ENDPOINT-LAW105'], lean_expansion_nodes=[decl], assumptions_preserved=False, boundary_preserved=False)
cell['learning_contract'] = lc
cell['graph_contribution'] = dict(lean_view='integration-node', overview_view='no-change-with-reason', functor_view='none-found',
    edge_semantics='formal-solid; overlays-dashed', color_semantics='evidence-status; library-scope', focus_targets=[decl], visual_review='Pending implementation and publication.')
cell['conceptual_mirror_audit'] = dict(status='none-found', reason='Nonnegative count partition, Tonelli and measure pushforward are already canonical mechanisms; no new conceptual mirror claimed.', discovery_ids=[])
path = Path('research-wiki/frontier-cells') / (cid + '.json')
assert not path.exists()
run.mkdir()
path.write_text(json.dumps(cell, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
proposal = adv.AdvanceProposal(advance_id=aid, task_id='ASTIS-SW-PBPS-2026', goal=seal['core_delta'], source_anchor=seal['source_anchor'],
    theorem_delta=seal['core_delta'], truth_boundary=seal['truth_boundary'], created_by=seal['owner'], dag_inputs=tuple(parents),
    proposed_files=(lean,), focused_checks=tuple(checks), modes=('faithfulPaper',), priority=100, frontier_cell=cid, target_declarations=(decl,))
adv.propose_advance(proposal)
evidence = dict(statement_seal=str(seal_path), source_graph=seal['source_graph']['path'], owner_files=[lean],
    upstream_delivery=str(source.parent / 'integration104/postpush-binding104.json'))
for state in ['CLAIMED', 'EXPLORING']:
    adv.transition_advance(aid, state, worker_id=seal['owner'], modes=['faithfulPaper'], evidence=evidence)
(run / 'claim.json').write_text(json.dumps(proposal.as_event(), ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
print('One105 owner claimed; existing sole94 stabilization lane retained.')
