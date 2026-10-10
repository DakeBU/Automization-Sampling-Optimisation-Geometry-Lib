from pathlib import Path
import copy, datetime, hashlib, json, subprocess, sys

R = Path('E:/Samplinglib')
pre = Path(__file__).parent
r = pre.parent / 'pbps-actual-conditional-next-wait-density89'
load = lambda p: json.loads(p.read_bytes())

def pin(p):
    b = p.read_bytes()
    return dict(path=p.relative_to(R).as_posix(), raw_sha256=hashlib.sha256(b).hexdigest(), bytes=len(b))

def new(p, value):
    assert not p.exists(), p
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')

def verify(value):
    if isinstance(value, dict):
        if 'path' in value and 'raw_sha256' in value:
            p = Path(value['path'])
            p = p if p.is_absolute() else R / p
            assert pin(p)['raw_sha256'] == value['raw_sha256'], p
            if 'bytes' in value:
                assert p.stat().st_size == value['bytes'], p
        for v in value.values():
            verify(v)
    elif isinstance(value, list):
        for v in value:
            verify(v)

# This authorization manifest is written only after BOTH independent header
# decisions close; running this preparation script earlier fails before mutation.
authorization = load(pre / 'root.preproof89.authorization.json')
assert authorization['all_independent_reviews_accepted'] is True
for evidence in authorization['closed_evidence']:
    verify(evidence)
    verify(load(R / evidence['path']))
header = pre / 'header89.proposed.lean'
assert pin(header)['raw_sha256'] == authorization['accepted_header_raw_sha256']
baseline = load(pre / 'pre-fetch89.workspace-RAW.json')['tracked_modified']
for path, digest in baseline.items():
    assert pin(R / path)['raw_sha256'] == digest

sys.path.insert(0, str(R / 'tools'))
import astis_advance as adv

aid = 'ASTIS-SA-20261011-PBPSActualConditionalNextWaitDensity'
cid = 'ASTIS-SW-PBPS-actual-conditional-next-wait-density'
owner = 'companion_root_20261005'
file = 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualConditionalNextWaitDensity.lean'
decl = 'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitDensity.actual_conditional_next_wait_density'
states = adv.current_advances()
assert aid not in states and not (R / file).exists()
assert states['ASTIS-SA-20261011-PBPSActualFiniteHistoryTailLaw']['state'] == 'VERIFIED'
assert [k for k, v in states.items() if v['state'] == 'STABILIZING'] == ['ASTIS-SA-20261005-SPHMCImplementedPhaseKernel']
parents = [
    'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteHistoryTailLaw.actual_finite_history_tail_law',
    'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualFiniteFirstEventLaw.actual_finite_first_event_law',
    'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHazardClock.actual_integrated_hazard_clock_laws',
    'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualHarmonicFlow.actual_harmonic_flow_laws',
    'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualBounceRate.actual_bounce_rate_energy_laws',
    'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws',
]
delta = 'Derive the strict positive finite next-wait joint history/time density for actual deterministic-depth PBPS histories, a jointly Borel all-history subprobability kernel, and all jointly Borel nonnegative extended tests with history-dependent finite cutoff.'
anchor = 'Chen-Chewi-Lu-Zhang arXiv2609.06905v1 Appendix A.1 (A.1),(A.2),(A.7) strict ordered-event density factor and Appendix A.2 joint Borel recursion; attributed ASTIS source-implicit completion.'
boundary = 'Original six analytic hypotheses unchanged. Fixed deterministic depth n, complete stopped actual history, raw unused Exp1 coordinate n. Fixed Borel finite-valued cutoff d may be unbounded across histories. Strict positive finite wait guard 0<tau<d(H), no endpoint-mass equivalence or no-atom premise. Real Lebesgue time on Ioo is the existing86 Ioc density measure restricted by Iio. Stopped histories have zero kernel; infinity mass is retained outside this finite component without normalization. All abstract histories, null A, n0, rank0, d0 and all jointly Borel ENNReal tests included. Only density component of S87-I5 closes if proved; ordered-time iteration, final survival/path factor, full A7/global G86-11, physical-time residual memorylessness/random restart/Markovness, nonexplosion/invariance/hypocoercivity/implementation/errors/unbounded costs/main/composition/wholepaper/Goal remain OPEN. Survival88 is adjacent, not a fabricated AND parent.'
r.mkdir(exist_ok=False)
seal = dict(status='SEALED_BEFORE_BODY_AFTER_DISTINCT_PREPROOF_MATH_SOURCE_AND_TOPOLOGY_ACCEPTANCE', sealed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), statement_version=1, header=pin(header), expanded_literal_Prop=header.read_text(encoding='utf8').split('private def ', 1)[1].split('\n#check', 1)[0], public_theorem=decl, primary_first_freeze=pin(pre / 'independent-source-first89/source-first89.native.json'), source_graph=pin(pre / 'independent-source-first89/source-proof-graph89.native.json'), source_coverage=pin(pre / 'independent-source-first89/source-coverage89.native.json'), independent_authorization=pin(pre / 'root.preproof89.authorization.json'), reuse_search=[pin(pre / 'retrieval89.json'), pin(pre / 'retrieval89.kernel-addendum.json')], toolchain=pin(R / 'lean-toolchain'), lake_manifest=pin(R / 'lake-manifest.json'), truth_boundary=boundary, proof_BODY_created=False, collaborator_RAW_preservation_count=len(baseline), chronology_disclosure='Both source-graph author and distinct topology reviewer froze direct primary reconstructions before reading any89 candidate or implementation. Header V1 parser-scope error was preserved and corrected before Seal; independent current-header review is mandatory. Generic APIs were retrieved before Seal without theorem proof credit.')
new(r / 'root.statement-seal89.json', seal)
p = adv.AdvanceProposal(advance_id=aid, task_id='ASTIS-SW-PBPS-2026', goal=delta, source_anchor=anchor, theorem_delta=delta, truth_boundary=boundary, created_by=owner, dag_inputs=tuple(parents), proposed_files=(file,), focused_checks=('lake build AutoSamplingTheory.ExampleCases.ProximalBPS.ActualConditionalNextWaitDensity',), modes=('faithfulPaper',), priority=100, frontier_cell=cid, target_declarations=(decl,))
adv.propose_advance(p)
adv.transition_advance(aid, 'CLAIMED', worker_id=owner, evidence=dict(statement_seal=str(r / 'root.statement-seal89.json'), owned_files=[file]))
adv.transition_advance(aid, 'EXPLORING', worker_id=owner, evidence=dict(route='Actual86 deterministic density restricted to Iio; actual87 history/tail product; internally derived joint density/clock measurability, kernel fibers and product nonnegative integration.', truth_boundary=boundary))
new(r / 'claim.json', p.as_event())
c = copy.deepcopy(load(R / 'research-wiki/frontier-cells/ASTIS-SW-PBPS-actual-conditional-next-wait-survival.json'))
c.update(cell_id=cid, title='Actual PBPS conditional finite next-wait density', source_anchor=anchor, target_statement=header.read_text(encoding='utf8'), status='claimed', parents=parents, consumers=['PBPS A.7 actual ordered-event-time conditional density iteration and prescribed path functional assembly'], source_targets=[decl], blocked=dict(status=False, reason='Distinct source topology, whole-header mathematical/type and source reviews accepted; proof pending.'))
c['evidence'] = dict(substantive_advance=aid, statement_seal=str(r / 'root.statement-seal89.json'), focused_checks=[], owned_files=[file], truth_boundary=boundary)
reason = 'Actual86/87/75/73/74/77 supply exact producers. Generic measure restriction, density kernels and product integration already belong to pinned Mathlib. No copied generic conditional-kernel adapter or upstream port; survival88 is not a proof dependency.'
searches = [str(pre / 'retrieval89.json'), str(pre / 'retrieval89.kernel-addendum.json')] + [x['path'] for x in load(pre / 'retrieval89.kernel-addendum.json')['files']]
c['shared_floor_audit'] = dict(searched=searches, classification='adapt', decision='adapt_existing', canonical_declaration=decl, canonical_shared_cell='', reason=reason)
c['reuse_plan'] = dict(searched_existing=searches, reused_declarations=parents, new_shared_declarations=[], known_consumers=[], planned_consumers=c['consumers'], no_duplicate_wrapper=True, decision_reason=reason)
c['statement_seal'] = dict(evidence=str(r / 'root.statement-seal89.json'), source_revision='arXiv2609.06905v1/Lean4.33.0/Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d', statement_version=1, signature_digest=pin(header)['raw_sha256'], binder_audit=['Six original analytic hypotheses unchanged.', 'Borel duration/history events/joint ENNReal functions are admissible deterministic tests.', 'No density, independence, measurability, no-atom or finite-wait provider premise.'], definition_kind='Eleven literal actual algorithm/input/history definitions; guarded total clock/time and finite density observables. Mathlib density-kernel measurable branch must be identified, stopped kernel zero.')
c['source_proof_coverage'] = dict(source_graph=str(pre / 'independent-source-first89/source-proof-graph89.native.json'), source_inventory='runs/20261007-companion-priority/pbps-actual-finite-first-event-law86/independent-source86/source-inventory86.exhaustive-successor.json', coverage_report=str(pre / 'header-math89/source-topology89.decision.json'), reviewed_adapter_overlay=authorization['source_decision'], coverage_status='Independent primary-first8nodes/11edges/4AND/18dispositions and distinct topology/whole-header reviews accepted. Unchanged global inventory retained; only conditional finite-density component of S87-I5 targeted. No BODY credit.')
c['source_detail_audit'] = dict(primary_edition=c['statement_seal']['source_revision'], primary_anchor=anchor, fidelity_boundary=boundary, detail_status='omitted', gap='Authors iterate finite density factors without an explicit all-history Borel conditional subprobability/joint-test construction. Ordered-time/final factor/full A7 remain separate.', consulted=[dict(source='Pinned primary A.1/A.2, compiled actual86/87/75/73/74/77 and pinned Mathlib', anchor='A1.E1;A1.E2;A1.E7;A1.SS2', hypothesis_adapter='No added analytic premise; exact strict measure restriction and admissible Borel tests explicit.')])
c['proof_digestion'] = dict(existing_substrate=parents, bookkeeping=['Derive joint Borel density/guarded clock and actual all-history kernel.', 'Restrict86 Ioc finite density law by Iio for each fixed history.', 'Integrate exact fixed-history fibers using87 history/tail product and Tonelli.', 'Derive all-history kernel mass and nonnegative joint-test identities internally.'], new_reusable=[], new_topology=delta)
c['purification'] = dict(status='pending', dead_code_audit='Proof pending', duplicate_semantics_audit='No exact actual conditional density duplicate found.', canonicalization=reason, compressed_spine_delta=delta, reader_default_view='Complete attributed statement/formula proof with exact folded Lean adjacent.', scope=boundary)
c['learning_contract']['salvage'].update(required=False, status='not-applicable', reason='No BODY before Seal; prospective header parser correction preserved.', promoted_fragments=[], discarded_fragments=[])
c['learning_contract']['parallelism'].update(decision='serial', direction_fingerprints=['actual-history/strict-finite-density/joint-kernel/product-sections'], shared_verified_context_digest=seal['primary_first_freeze']['raw_sha256'])
c['learning_contract']['reader_backpressure'].update(purification_status='pending', exposition_seal_status='pending', exposition_evidence='', source_expansion_nodes=['S89-A1', 'S89-A2', 'S89-P1', 'S89-P2', 'S89-T:TARGET', 'S87-I5-assembly:OPEN'], lean_expansion_nodes=[decl], assumptions_preserved=False, boundary_preserved=False)
c['graph_contribution'].update(focus_targets=[decl], lean_view='new-node', overview_view='no-change-with-reason', functor_view='none-found', visual_review='Pending proof/publication and inspectable affected branch; source overlays never formal credit.')
c['conceptual_mirror_audit'] = dict(status='pending', discovery_ids=[], reason='Required before PROVED_LOCAL; no transport asserted.')
new(R / 'research-wiki/frontier-cells' / (cid + '.json'), c)
for label, args in [('publication-packet-before-proof89', ['tools/astis_publication.py', 'packet', '--cell', cid]), ('frontier-before-proof89', ['tools/astis_frontier_cells.py', 'check'])]:
    q = subprocess.run([sys.executable, '-X', 'utf8', *args], cwd=R, capture_output=True)
    (r / (label + '.stdout.json')).write_bytes(q.stdout)
    (r / (label + '.stderr.log')).write_bytes(q.stderr)
    new(r / (label + '.receipt.json'), dict(exit_code=q.returncode, terminal_closed=True))
    assert q.returncode == 0, (q.stdout + q.stderr).decode(errors='replace')[-3000:]
print('89 sealed/claimed, bounded publication and frontier PASS; no proof credit, sole lane unchanged.')
