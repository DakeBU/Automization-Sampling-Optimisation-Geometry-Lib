"""Seal the independently accepted exact Prop before creating any proof body."""
from pathlib import Path
import datetime, hashlib, json, sys

R = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(R))
from tools import astis_advance as advance

pre = Path(__file__).resolve().parent
run = R / 'runs/20261007-companion-priority/pbps-actual-finite-count-path93'
old = R / 'runs/20261007-companion-priority/pbps-actual-ordered-prefix92'
cid = 'ASTIS-SW-PBPS-actual-finite-count-path'
aid = 'ASTIS-SA-20261011-PBPSActualFiniteCountPath'
module = 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean'
decl = 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath.actual_finite_count_path_law'
owner = 'companion_root_20261005'
load = lambda p: json.loads(Path(p).read_bytes())

def pin(p):
    p = Path(p)
    if not p.is_absolute(): p = R / p
    b = p.read_bytes()
    return dict(path=p.relative_to(R).as_posix(), raw_sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))

checked = {}
def check_tree(x):
    if isinstance(x, dict):
        if 'path' in x and 'raw_sha256' in x:
            p = pin(x['path'])
            if 'header_raw_sha256' in x and 'start_line' in x and 'end_line' in x:
                assert p['raw_sha256'] == x['header_raw_sha256'], x['path']
                b = (R / p['path']).read_bytes()
                region = b''.join(b.splitlines(keepends=True)[x['start_line']-1:x['end_line']])
                assert hashlib.sha256(region).hexdigest() == x['raw_sha256'], x
                checked[p['path'] + ':' + str(x['start_line']) + '-' + str(x['end_line'])] = x
            else:
                assert p['raw_sha256'] == x['raw_sha256'], x['path']
                if 'bytes' in x: assert p['bytes'] == x['bytes'], x['path']
            checked[p['path']] = p
        for v in x.values(): check_tree(v)
    elif isinstance(x, list):
        for v in x: check_tree(v)

def write(p, value):
    assert not p.exists(), p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')

header = pre / 'Header93.lean'
math = pre / 'independent-header-math93/header-math-review93.native.json'
source = pre / 'independent-header-source93/source-decision93.native.json'
topology = pre / 'independent-header-math93/topology-crosscheck93.native.json'
assert pin(header)['raw_sha256'] == '90bca17fbb11d9a8fea226bd0dca6494ef9a61f3db31beaf52c0ef2999cf9cfe'
assert pin(math)['raw_sha256'] == '3fcfe3724bce7e4a3ff340e289e669773fae65646ba44c19af9af2124a089163'
assert pin(source)['raw_sha256'] == '17a81e8d3d9506a3931dd75b54c35c7efc06f36f9353f8526bdc50e1234051c8'
assert load(math)['decision'] == 'ACCEPT_PROSPECTIVE_HEADER_MATHEMATICS_NO_REQUIRED_CORRECTION'
assert load(source)['source_side_decision'] == 'ACCEPT_EXACT_HEADER_FOR_PREPROOF_SOURCE_BOUNDARY'
# The root must inspect the independent cross-check before executing this script.
assert pin(topology)['raw_sha256'] == 'aaa2b09454968419994ed6dc72164155f6b4fcf18a9a9f45f8bf794af49f9bb7'
assert load(topology)['decision'] == 'ACCEPT_BOUNDED_TOPOLOGY_COVERAGE_CROSSCHECK'
for p in [math, source, topology,
          pre / 'independent-header-math93/closed-RAW93.native.json',
          pre / 'independent-header-math93/closed-RAW93.topology-successor.native.json',
          pre / 'independent-header-source93/closed-RAW-header-source93.native.json',
          old / 'next-source-graph93/closed-RAW-source-graph93.v2.native.json']:
    check_tree(load(p))
saved = load(old / 'exact-commit-verification92/closed-RAW-manifest92.json')['preserved_collaborator_inputs']
check_tree(saved)
assert len(saved) == 21 and not (R / module).exists()
states = advance.current_advances()
assert aid not in states
assert [s['advance_id'] for s in states.values() if s['state'] == 'STABILIZING'] == ['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
text = header.read_text(encoding='utf8')
literal = text.split('def candidate_finite_count_path_statement', 1)[1].split('\n#check', 1)[0]
anchor = 'Chen-Chewi-Lu-Zhang arXiv2609.06905v1 Appendix A.1 (A.1),(A.2),(A.7), half-open arcs and prescribed-path paragraph; Appendix A.2 measurable realization. Source-implicit finite-count path ingredient with explicit ASTIS completions.'
delta = 'Derive the terminally survived finite-count complete-history and whole coordinate-measurable path law from the actual iid exponential-clock recursion, including fixed-horizon endpoint nullity, measurable count, total history interpolation and all nonnegative extended joint tests.'
boundary = ('Exactly six source analytic hypotheses. Literal actual stopped recurrence and canonical iid Exp(1) product; all finite n and NNReal T including zero. '
            'One jointly measurable actual phase Z with pointwise covered-arc and explicit uncovered fallback semantics; fixed-T coordinate-product path carrier. '
            'Total count is Nat.find of the half-open interval index, with zero fallback. Total history interpolation is an increasing-index Fin.foldl; its measurability and path identification are conclusions. '
            'Density is the ordered-prefix q times terminal survival, with unnormalized joint history/path pushforward, all ENNReal tests and exact count-event mass. '
            'Fixed-T endpoint nullity and simultaneous all-count/cardinality interpretation are AE, not a common no-jump event over all T. Raw C events are disjoint and their union has full measure. '
            'No law, positivity, independence, nonexplosion, measurable witness or integrability provider is a public premise. '
            'Hazard stitching, pre-jump left limits, infinite full A7 assembly/absolute convergence, Skorokhod compatibility, restart/Markovness, invariance, hypocoercivity, implementation errors, expected costs, main results, actual-input composition and full papers remain OPEN.')
parents = [
    'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualOrderedPrefix.actual_ordered_prefix_law',
    'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitSurvival.actual_conditional_next_wait_survival',
    'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase',
    'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPhysicalTimeCover.actual_fixed_reference_physical_time_cover',
    'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion',
    'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws']
search = [p.relative_to(R).as_posix() for p in sorted((pre / 'retrieval93').glob('*.txt'))]
seal = dict(status='SEALED_BEFORE_PROOF_BODY_AFTER_INDEPENDENT_MATH_SOURCE_AND_TOPOLOGY_REVIEW',
    sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), statement_version=1,
    header=pin(header), expanded_literal_Prop=literal, public_theorem=decl,
    production_name_visibility_change_only=True,
    source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d',
    primary=pin(R / 'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'),
    source_graph=pin(old / 'next-source-graph93/candidate-source-proof-graph93.v2.native.json'),
    source_coverage=pin(old / 'next-source-graph93/candidate-source-coverage93.v2.native.json'),
    source_topology_review=pin(topology), independent_math_header=pin(math), independent_source_header=pin(source),
    all_review_bound_inputs_rehashed=list(checked.values()), toolchain=pin('lean-toolchain'), lake_manifest=pin('lake-manifest.json'),
    truth_boundary=boundary, proof_BODY_created=False, collaborator_RAW_preservation_count=21,
    binder_audit=['hα,hαβ,hV,hH,hη,hβη are the six source assumptions.',
        'Finite-dimensional real Hilbert/Borel structure includes the disclosed rank-zero extension.',
        'Measurable F specifies the admissible nonnegative extended test class.',
        'All process, count, density, endpoint, path and measurability obligations are conclusions or internal dependencies.'],
    definition_kind='36 literal lets: 34 outer objects plus local H and ZT. Existential Z retains proved covered/fallback characterization; no extra provider.')
write(run / 'root.statement-seal93.json', seal)
proposal = advance.AdvanceProposal(advance_id=aid, task_id='ASTIS-SW-PBPS-2026', goal=delta,
    source_anchor=anchor, theorem_delta=delta, truth_boundary=boundary, created_by=owner,
    dag_inputs=tuple(parents), proposed_files=(module,),
    focused_checks=('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteCountPath',),
    modes=('faithfulPaper',), priority=100, frontier_cell=cid, target_declarations=(decl,))
cell = dict(schema_version=3, cell_id=cid, route='samplewiki-route', title='Actual PBPS terminally survived finite-count complete-path law',
    mode='faithfulPaper', source_anchor=anchor, target_statement=text, status='claimed', parents=parents,
    consumers=['PBPS A1.E7 after hazard stitching and countable path-law assembly (planned, unproved)'],
    source_targets=[decl], declaration_level='source-anchor', blocked=dict(status=False, reason='Sealed exact statement; implementation starting.'),
    evidence=dict(substantive_advance=aid, statement_seal=pin(run / 'root.statement-seal93.json')['path'], focused_checks=[], owned_files=[module], truth_boundary=boundary),
    shared_floor_audit=dict(searched=search+['Libraries/shared-foundations.yml','Libraries/frontloaded-shared-spine.json'], classification='adapt', decision='adapt_existing', canonical_declaration=decl, canonical_shared_cell='', reason='Join existing actual PBPS parents with pinned measurable selection/product-measure APIs; no duplicate process construction.'),
    reuse_plan=dict(searched_existing=search, reused_declarations=[], planned_dependencies=parents, new_shared_declarations=[], known_consumers=[], planned_consumers=['PBPS A1.E7 whole-path formula'], no_duplicate_wrapper=True, decision_reason='Terminal survival, count and path adapters are missing genuine joins; no new public premise.'),
    reader_contract=dict(reference_standard='textbook/chapter-01/section-1-3.html', source_ordered=True, source_statement_adjacent=True, natural_language_formula_proof=True, hidden_assumptions_visible=True, lean_collapsed=True, external_dependencies_visible=True),
    statement_seal=dict(evidence=pin(run / 'root.statement-seal93.json')['path'], source_revision=seal['source_revision'], statement_version=1, signature_digest=pin(header)['raw_sha256'], binder_audit=seal['binder_audit'], definition_kind=seal['definition_kind']),
    source_proof_coverage=dict(source_graph=seal['source_graph']['path'], source_inventory=seal['source_coverage']['path'], coverage_report=seal['source_topology_review']['path'], coverage_status='Independently reviewed pre-proof coverage only; no proof coverage credit.'),
    source_detail_audit=dict(primary_edition=seal['source_revision'], primary_anchor=anchor, fidelity_boundary=boundary, detail_status='omitted', gap='Source-implicit terminal weighting, fixed-horizon endpoint/count and measurable whole-path adapters.', consulted=[dict(source='Pinned PBPS v1 and fixed Lean/Mathlib', anchor='A1.E1; A1.E2; A1.E7; A1.SS2', hypothesis_adapter='Six binders unchanged; explicit coordinate-path carrier and rank-zero/ENNReal extensions.')]),
    proof_digestion=dict(existing_substrate=parents, bookkeeping=['Total history interpolation and measurable count representation.'], new_reusable=[], new_topology=delta),
    purification=dict(status='pending', dead_code_audit='Proof not implemented.', duplicate_semantics_audit='Bounded retrieval found no actual terminally survived whole-path law.', canonicalization='Reuse existing actual phase and probability leaves.', compressed_spine_delta=delta, reader_default_view='Full attributed statement/formula proof with adjacent initially folded exact Lean.', scope=boundary),
    learning_contract=dict(control_plane_math_authority=False, process_memory_checked=True, process_memory_ids=[], failure_class='NONE',
        salvage=dict(required=False, status='not-applicable', reason='Only pre-proof declaration elaboration corrections; no proof fragments discarded.', promoted_fragments=[], discarded_fragments=[]),
        parallelism=dict(decision='serial', direction_fingerprints=['actual-count-path/terminal-weight/total-history-interpolation'], expected_information_gain='One writer; independent mathematical and source uncertainties reviewed separately.', shared_verified_context_digest=pin(header)['raw_sha256']),
        cross_route_blind_spot_audit=dict(required=False, status='not-applicable', evidence='', canonical_route='samplewiki-route', selection_reason='One implementation route; source OR branches retained without proof credit.'),
        reader_backpressure=dict(purification_status='pending', exposition_seal_status='pending', exposition_evidence='', source_expansion_nodes=['A1.E1','A1.E2','A1.E7'], lean_expansion_nodes=[decl], assumptions_preserved=False, boundary_preserved=False)),
    graph_contribution=dict(lean_view='integration-node', overview_view='no-change-with-reason', functor_view='none-found', edge_semantics='formal-solid; overlays-dashed', color_semantics='evidence-status; library-scope', focus_targets=[decl], visual_review='Pending proof/publication; reuse existing paper route.'))
write(R / f'research-wiki/frontier-cells/{cid}.json', cell)
advance.propose_advance(proposal)
write(run / 'claim.json', proposal.as_event())
advance.transition_advance(aid, 'CLAIMED', worker_id=owner, evidence={'statement_seal':pin(run / 'root.statement-seal93.json')})
advance.transition_advance(aid, 'EXPLORING', worker_id=owner, evidence={'proof_route':'Terminally weight actual prefix law, factor paths through total history interpolation, derive fixed-horizon endpoint/count identification.'})
print(json.dumps(dict(advance=aid, state='EXPLORING', header=pin(header), rehashed_inputs=len(checked), proof_body_created=False)))
