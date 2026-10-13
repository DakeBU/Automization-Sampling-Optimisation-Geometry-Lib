from pathlib import Path
import datetime, hashlib, json

R = Path('E:/Samplinglib')
B = R/'runs/20261007-companion-priority/pbps-actual-small-time-continuity82'
O = B/'independent-math82'
M = R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualSmallTimeContinuity.lean'

def info(p):
    p = Path(p)
    b = p.read_bytes()
    return dict(path=p.relative_to(R).as_posix(), RAW_bytes=len(b), RAW_sha256=hashlib.sha256(b).hexdigest())

def load(p):
    return json.loads(p.read_text(encoding='utf8'))

def save(name, data):
    with (O/name).open('x', encoding='utf8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

freeze = load(O/'input-freeze82.json')
for e in freeze['inputs']:
    assert info(R/e['path']) == e
receipt = load(O/'fresh-whole-module.receipt.json')
assert receipt['exit_code'] == 0 and receipt['terminal_closed']
kernel = load(O/'kernel-dependency-summary82.json')
assert kernel['status'] == 'PASS' and kernel['expected_four_parent_frontier_exact']
assert load(O/'fake-closure-scan82.json')['hits'] == []
assert load(O/'exposition-body-audit82.json')['status'] == 'PASS'
old = (B/'focused82-attempt5/source.snapshot.lean').read_bytes()
new = M.read_bytes()
assert old.replace(b'/-! Prospective exact statement82 only; no theorem proof or admission.',
                   b'/-! Actual PBPS short-time probability prerequisite, with its proof below.') == new

checks = [
    dict(id='M82-01', region=[15, 101], verdict='PASS',
         finding='The complete private proposition equals the pre-proof reviewed header and root seal. Six analytic source binders, eleven actual definitions and all four existing actual80 Z clauses are preserved exactly. Public theorem uses the same six binders; no public firstwait, cap, nonexplosion, process, independence or continuity provider is added.'),
    dict(id='M82-02', region=[106, 161], verdict='PASS',
         finding='BODY definitions agree with the sealed private proposition and actual80; deterministic covered and fallback statements are returned unchanged. Product tuple association in joint Z measurability is (((y,xRef),z0),t,sample). Pullback to fixed parameters is measurable; defect is complement of equality of a measurable phase and a constant.'),
    dict(id='M82-03', region=[162, 184], verdict='PASS',
         finding='w is precisely actual tau(y,xRef,z0,toNNReal(sample0)); g has the identical clamping and fixed-parameter association. Joint tau measurability pulls back to g; w=g composed with coordinate0. map_map and the actual UnitExponentialProduct coordinate0 law give P.map w = expMeasure(1).map g. No merely identically distributed abstract replacement or new independence assumption is used. Mapping measurable Ioi and actual75 strict survival gives P(t<w)=exp(-Lambda_t).'),
    dict(id='M82-04', region=[185, 203], verdict='PASS',
         finding='Direct literal recurrence unfolding proves eventTime1=w for every raw sample. The top case gives a stopped next record with time infinity; the finite case untopD_coe and zero_add recover exactly the first wait, including zero. Index0 is the live record (0,z0). For finite t<w, T0<=t<T1 and the deterministic actual80 covered property give Zt=Phi_t(z0). An infinite first wait retains the live index0 arc at every finite t; no stopped phase or fallback is substituted. At t=w the strict no-event hypothesis is false, consistent with half-open intervals.'),
    dict(id='M82-05', region=[204, 217], verdict='PASS',
         finding='Only defect subset complement of strict survival is proved. Equality with the first-event event is neither needed nor asserted, allowing ineffective jumps and later returns. Probability P is supplied by actual77, so measureReal monotonicity has its finite-measure condition and measureReal_compl is applicable to measurable Ioi preimage. Thus P(defect)<=1-exp(-Lambda_t). Zero waits lie in the complement; infinity waits do not. At t=0, Lambda0=0 yields a zero defect probability without asserting equality for all exceptional raw samples.'),
    dict(id='M82-06', region=[218, 223], verdict='PASS',
         finding='The actual product phase norm is a measurable real-valued function. Its closed positive-threshold tail {delta<=norm(Zt-z0)} is measurable for every finite t. There is no moment or integrability requirement hidden in this probability event.'),
    dict(id='M82-07', region=[224, 250], verdict='PASS',
         finding='actual73 joint Phi continuity restricts along ((y,xRef),real(t),z0); actual75 joint Lambda continuity restricts along (((y,xRef),z0),t). Phi0=z0 makes the harmonic displacement norm tend to zero on the ordinary NNReal neighborhood filter. delta>0 gives eventual strict norm<delta. Lambda0=0 and continuous exponential make 1-exp(-Lambda_t) tend to zero. The optional linear cap route is not consumed; no positivity of energy, cap or phase norm is assumed.'),
    dict(id='M82-08', region=[251, 260], verdict='PASS',
         finding='Eventually the deterministic harmonic displacement is strictly below delta. Any actual phase at distance at least delta must therefore differ from the no-jump phase; this is the exact tail subset used by monotonicity and the defect bound. Nonnegative probability and the vanishing bound give the ordinary-filter squeeze, including t=0. This proves stochastic continuity at zero for every fixed deterministic parameter triple and every real delta>0, with no parameter-uniform nullset/limit or arbitrary correlated parameter substitution.'),
    dict(id='M82-09', region=[15, 260], verdict='PASS',
         finding='No nonempty/rank-positive assumption occurs. In dimension zero the phase is the singleton, rate and Lambda are zero, actual positive exponential waits are infinite, and defect/tails vanish. More generally zero rate/energy is handled through survival and continuity without division by a cap. Exceptional raw nonpositive samples are totalized by toNNReal and inherited actual80 uncovered fallback; their possible zero-time bounces are not erased from deterministic definitions. Probability claims use the actual law, and retained per-parameter common AE all-finite-time realization and initialization are returned from actual80.'),
    dict(id='M82-10', region=[106, 260], verdict='PASS',
         finding='All nine published BODY regions are contiguous, exact raw source slices covering the complete public BODY. Corrected step4 formula states survival only; first-arc reasoning follows in step5, and the defect-probability bound is justified in step6. This sequencing correction and the one-line production docstring successor change neither the private proposition nor any BODY byte or line number.'),
]

save('whole-proof-mathematics82.json', dict(
    schema_version=1, status='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY',
    reviewer_id='/root/exact_verify77', utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    module=info(M), original_frozen_module=info(B/'focused82-attempt5/source.snapshot.lean'),
    original_RAW_sha256='a5d0303f2f426e0029ddec2fbd56ba8f95670ce533e560d18e473c6111ef74d0',
    successor_RAW_sha256='f2bbb2a495ff6af2f2d1d73f77c498ccf16406bb0b07d20b8437631afb1a7bde',
    documentation_only_successor_independently_checked=True,
    original_statement_and_BODY_byte_identical_to_successor=True,
    initial_hash_negative=info(O/'initial-hash-negative82.json'),
    header=info(B/'header82.proposed.lean'), seal=info(B/'root.statement-seal82.json'),
    findings=checks, mathematical_repairs_required=[], new_public_provider_premises=[],
    actual_ASTIS_frontier=kernel['external_ASTIS_dependencies'],
    closure=dict(local_generated_proof_constant_count=kernel['local_proof_constant_count'],
                 transitive_ASTIS_kernel_constant_count=len(kernel['transitive_imported_ASTIS_kernel_constants']),
                 transitive_ASTIS_kernel_edge_count=len(kernel['transitive_imported_ASTIS_kernel_edges']),
                 axioms=kernel['axioms'],
                 note='Kernel closure follows generated target proof values and imported ASTIS proof values. Full theorem #print axioms covers imported Mathlib transitively as well. This is actual emitted proof dependency evidence, not an import graph.'),
    mathlib_APIs_inspected=[
        dict(path='Mathlib/MeasureTheory/Measure/Real.lean', lines=[79, 91], declarations=['map_measureReal_apply', 'measureReal_mono'], conditions='Measurable function and measurable target set for map; finite upper set measure for real monotonicity, supplied by P probability.'),
        dict(path='Mathlib/MeasureTheory/Measure/Real.lean', lines=[409, 412], declarations=['measureReal_compl'], conditions='IsFiniteMeasure and measurable survival event.'),
        dict(path='Mathlib/Topology/Order/Basic.lean', lines=[225, 229], declarations=["tendsto_of_tendsto_of_tendsto_of_le_of_le'"], conditions='Order topology, same limiting value and eventually lower/upper inequalities; no punctured-filter side condition.')],
    evidence=dict(full_source_foreground_receipt=info(O/'fresh-whole-module.receipt.json'),
                  kernel=info(O/'kernel-dependency-summary82.json'), fake_closure=info(O/'fake-closure-scan82.json'),
                  literal_audit=info(O/'statement-definition-audit82.json'), exposition=info(O/'exposition-body-audit82.json')),
    role_limits=dict(blind_or_source_verdict_read=False, source_final_acceptance=False, VERIFIED=False,
                     exact_science_commit_admission=False, production_or_shared_edits=False,
                     ledger_or_cell_writes=False, aggregate_gate_run=False),
    remaining_boundary=['Distinct source and blind-decoder acceptance and later committed exact verification.',
                        'Serialized aggregation/publication/reader/main/purification remain separate.',
                        'Full source Ex22 L2 strong continuity requires further invariant/semigroup/density arguments; Markov, restart, process semigroup, invariance, hypocoercivity, implementation, cost, composition and whole Goal remain open.'],
    native_evidence_note='Scripts, raw logs, receipts and exact source probes are native artifacts. No native private reasoning trajectory is invented.'))

save('decision82.json', dict(status='ACCEPTED_INDEPENDENT_MATHEMATICS_ONLY', reviewer_id='/root/exact_verify77',
    module=info(M), header=info(B/'header82.proposed.lean'),
    mathematics=info(O/'whole-proof-mathematics82.json'),
    full_source_receipt=info(O/'fresh-whole-module.receipt.json'),
    standard_axioms_only=kernel['axioms'], expected_four_parent_kernel_frontier_exact=True,
    generated_local_proof_constant_count=kernel['local_proof_constant_count'],
    complete_transitive_ASTIS_constants=len(kernel['transitive_imported_ASTIS_kernel_constants']),
    fake_closure='PASS', exact_sealed_private_Prop='PASS', documentation_only_successor='PASS',
    nine_BODY_regions_and_corrected_exposition_sequence='PASS',
    mathematical_blockers=[], mathematical_repairs=[], VERIFIED=False,
    scope='Independent mathematics of frozen SAU82 source only; no blind/source/exact-commit/integration/reader/main/PURIFIED/fullpaper/Goal acceptance.'))

lesson=R/'website/content/declaration_lessons/pbps-actual-small-time-continuity.json'
assert info(lesson)['RAW_sha256']==load(O/'exposition-body-audit82.json')['lesson_RAW_sha256']
inputs=[R/e['path'] for e in freeze['inputs']]
inputs += [B/'focused82-attempt5/source.snapshot.lean', lesson,
    R/'website/content/publications/pbps-actual-small-time-continuity.json',
    R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Real.lean',
    R/'.lake/packages/mathlib/Mathlib/Topology/Order/Basic.lean']
artifacts=sorted(p for p in O.iterdir() if p.is_file())
save('closed-manifest82.json',dict(status='CLOSED_RAW_NONCIRCULAR',reviewer_id='/root/exact_verify77',
    module_RAW_sha256=info(M)['RAW_sha256'], fixed_mathlib=freeze['fixed_mathlib'],
    frozen_inputs=[info(p) for p in dict.fromkeys(inputs)], owned_artifacts=[info(p) for p in artifacts],
    self_hash_excluded=True, dependency_direction='Manifest hashes closed decision and native artifacts; no artifact hashes this manifest.',
    initial_negative_retained=True, all_terminal_children_closed=True, VERIFIED=False))
print(json.dumps({n:info(O/n)['RAW_sha256'] for n in ['decision82.json','whole-proof-mathematics82.json','fresh-whole-module.receipt.json','closed-manifest82.json']},indent=2))
