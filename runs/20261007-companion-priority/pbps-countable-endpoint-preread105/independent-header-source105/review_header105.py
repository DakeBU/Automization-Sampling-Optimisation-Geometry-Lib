from pathlib import Path
import json
import hashlib
import re
import gzip

R = Path('E:/Samplinglib')
B = R / 'runs/20261007-companion-priority'
P = B / 'pbps-countable-endpoint-preread105'
O = P / 'independent-header-source105'
SRC = B / 'pbps-actual-normalized-endpoint104/next-primary105'
H = P / 'Header105.lean'
A93 = R / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteCountPath.lean'
A104 = R / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNormalizedEndpointSector.lean'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def ref(p):
    b = p.read_bytes()
    return {'path': p.relative_to(R).as_posix(), 'raw_sha256': sha(b), 'bytes': len(b)}


def put(name, data):
    p = O / name
    assert not p.exists()
    p.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode())
    return ref(p)


header = H.read_text(encoding='utf8')
source = A93.read_text(encoding='utf8')
source = source[source.index('private def actual_finite_count_path_statement'):]
literal_h = header[header.index('    let c :'):header.index('    let R :')]
literal_s = source[source.index('    let c :'):source.index('    ∃ Z :')]
contract_h = header[header.index('    ∃ Z :'):header.index('      (∀ y r : E, ∀ T :')]
contract_s = source[source.index('    ∃ Z :'):source.index('      (∀ n : ℕ, ∀ T :')]
binder_h = header[header.index('    {E :'):header.index(' : Prop := by')]
binder_s = source[source.index('    {E :'):source.index(' : Prop := by')]
assert literal_h == literal_s and contract_h == contract_s and binder_h == binder_s
names = re.findall(r'^    let (\S+)', literal_h, re.M)
assert len(names) == 34
assert len(re.findall(r'^\s+let ', header, re.M)) == 43
receipt = json.loads((P / 'header105.receipt.json').read_text(encoding='utf8'))
assert receipt['exit_code'] == 0 and receipt['terminal_closed'] is True
assert receipt['header_raw_sha256'] == ref(H)['raw_sha256'] == '209ca04935d0dc953d86d334db4e62129642b57b04d18dc4354bbad5e1f0f89d'
cov = json.loads((SRC / 'source-coverage-delta105.native.json').read_text(encoding='utf8'))
primary = R / cov['primary']['path']
raw = primary.read_bytes()
assert sha(raw) == cov['primary']['raw_sha256']
for region in cov['regions']:
    assert sha(raw[region['byte_start']:region['byte_end_exclusive']]) == region['raw_sha256']
expected = json.loads((SRC / 'expected-semantic-slots105.native.json').read_text(encoding='utf8'))['semantic_slots']
findings = {
    'objects': ('Actual finite-clock PBPS, globally identified Z, actual Gamma/rho, normalized position Gibbs times standard Gaussian, phase-initialized endpoint pair Q.', 'Header22-117 reproduces all34 algorithm definitions exactly;118-122 supplies literal R,Vy,nu;123-132 retains actual Z clauses;134-144 supplies endpoint laws.'),
    'domains': ('E finite-dimensional real inner-product Borel space; phase E x E position first; Omega=Nat->real; all n:Nat and T:NNReal, Prefix strict simplex.', 'Header12-14,50,60-64,106,123,133-144. No positive-rank or positive-time restriction. m is exact subtype comap and every measure product is initial phase first.'),
    'quantifiers': ('The six analytic binders precede a single global exists Z. Its joint measurable/arc/fallback/zero clauses precede forall y,r,T; the conclusion sums all n with no cap.', 'Header15-19 binders;123-133 witness and forall order;138 L is Nat-indexed;144 Measure.sum L.'),
    'assumptions': ('Original six assumptions only: hAlpha,hAlphaBeta,hV,paired hH,hEta,hBetaEta, with the same ambient typeclasses. No process, normalizer, finite mass, rate positivity, measurable count, or integrability premise.', 'Entire binder block is LF-text identical to actual93. All43 lets define concrete objects; IsProbabilityMeasure Q and MeasurePreserving J Q Q are conclusions, not inputs.'),
    'conclusion': ('For every y,r,T, Q=Measure.sum L AND IsProbabilityMeasure Q AND MeasurePreserving J Q Q, where Q is the actual Z endpoint pushforward of nu_y.prod P and L_n is the actual normalized count-n endpoint sector.', 'Header134-144 matches expected B,sigma,L,M,Q,J. Q and every L live on (E x E) x (E x E); no equality to a freely chosen law or probability claim for each L_n.'),
    'scopes': ('Equality of measures and momentum-flipped endpoint-pair reversal for the actual countable law, with actual process identification retained. No full-path reversal, Markov/semigroup theorem, signed bilinear result, marginal invariance or cost claim.', 'Z arc and fallback clauses123-132 are identification inherited from93, not jumpwise reversal. The final conclusion144 has exactly the three agreed bounded measure clauses.'),
    'constant_dependencies': ('sqrt(eta) factors in flow/rate, quadratic1/(2eta), standard Gaussian momentum law, exact rate1 exponential clocks, ENNReal q times terminal survival, arbitrary fixed r; no new constants.', 'Header23-38 and50 retain actual mechanics;72-81 and114-117 retain incoming factors and terminal weight;119-122 retains exact Gibbs normalization via tilted volume and stdGaussian.')
}
slots = {key: {'source': expected[key], 'header': pair[0], 'relation': 'matches-frozen-source-boundary', 'evidence': pair[1]} for key, pair in findings.items()}
mechanical = put('literal-comparison105.native.json', {
    'kind': 'exact literal header source-interface comparison', 'header': ref(H), 'actual93': ref(A93), 'actual104': ref(A104),
    'all_six_binders_LF_text_exact_actual93': binder_h == binder_s,
    'all34_algorithm_definitions_LF_text_exact_actual93': literal_h == literal_s,
    'algorithm_definition_names': names, 'algorithm_LF_block_sha256': sha(literal_h.encode()),
    'global_actual_Z_contract_LF_text_exact_actual93': contract_h == contract_s,
    'global_Z_contract_LF_block_sha256': sha(contract_h.encode()),
    'additional_outer_definitions': ['R', 'Vy', 'nu'],
    'additional_inner_definitions': ['B', 'sigma', 'L', 'M', 'Q', 'J'],
    'total_literal_lets': 43, 'header_lines': len(header.splitlines()),
    'public_assumptions': 6, 'terminal_typecheck': ref(P / 'header105.receipt.json'),
    'type_only_no_theorem_proof': True
})
coverage = put('header-source-coverage105.native.json', {
    'kind': 'prospective header source coverage, not compiled proof coverage', 'header': ref(H),
    'frozen_source_graph': ref(SRC / 'source-proof-graph-delta105.native.json'),
    'frozen_source_inventory': ref(SRC / 'source-coverage-delta105.native.json'),
    'primary': ref(primary), 'all21_original_slices_rehashed': True, 'regions': cov['regions'],
    'header_regions': [
        {'lines': [1, 10], 'meaning': 'Imports, namespace and type-only environment; no new mathematical premise.'},
        {'lines': [11, 21], 'meaning': 'Candidate Prop and literal original six binders.'},
        {'lines': [22, 117], 'meaning': 'All34 literal actual93 definitions, including clocks/count/path/density.'},
        {'lines': [118, 122], 'meaning': 'R, exact proximal Vy, normalized nu=tilted-position volume prod stdGaussian.'},
        {'lines': [123, 132], 'meaning': 'Single global actual Z joint measurable, on-arc, fallback and a.e. zero-time contract; all identical to93.'},
        {'lines': [133, 144], 'meaning': 'Universal y,r,T; literal B/sigma/L/M/Q/J; countable assembly/probability/flipped endpoint reversal.'},
        {'lines': [145, 148], 'meaning': 'Type-only #check and namespace closure.'}
    ],
    'source_to_header_boundary': 'A7 and3171-3175 initial Gibbs integration plus3210-3215 nonnegative assembly are the selected source completion. Actual104 supplies each fixed-n reversal. Source3216-3227 signed duality/marginal invariance/L2 remain future; source hypotheses do not include proof ingredients.',
    'graph_read_scope': 'Source creator checks statement against frozen expected graph boundary only; no self-validation of graph topology, edges, sufficiency, or Lean proof.',
    'no_implementation_coverage_claim': True, 'self_topology_validation': False, 'proof_credit': False
})
run = put('header-source-run105.native.json', {
    'kind': 'independent prospective source-header review run', 'reviewer': '/root/source_final96',
    'primary_first_freeze': ref(O / 'primary-expectations-frozen105.native.json'), 'header': ref(H),
    'expected_slots': ref(SRC / 'expected-semantic-slots105.native.json'), 'literal_comparison': mechanical, 'coverage': coverage,
    'typecheck': [ref(P / 'header105.receipt.json'), ref(P / 'header105.stdout.log'), ref(P / 'header105.stderr.log')],
    'read_order': 'Rehashed frozen primary-first packet and all21 source slices; wrote own expected-slot freeze with header_contents_read=false; then inspected Header105 and terminal typecheck.',
    'prior_involvement': 'Author of source-only105 recommendation and graph, prior104 source reviewer. Separate mathematical/topology reviewer required; no independence from own source graph is claimed.',
    'implementation_visible': False, 'prior_semantic_verdict_input': False, 'shared_edits': False, 'proof_credit': False
})
decision = put('header-source-decision105.native.json', {
    'verdict': 'ACCEPT_PROSPECTIVE_SOURCE_HEADER_ONLY', 'reviewer': '/root/source_final96', 'header': ref(H),
    'review_run': run, 'semantic_slots': slots, 'deltas': [
        {'slot': 'conclusion', 'severity': 'informational', 'description': 'The source nonnegative averaging calculation is exposed as equality of the actual endpoint measure with a countable sum, together with probability and reversal of that same law.', 'source': 'AppendixA1 A7,3171-3175,3210-3215.', 'lean': 'Header134-144 concrete laws; no probability-one statement for individual sectors.', 'evidence': 'Matches independently frozen105 recommendation and all three expected conclusions.', 'blocking': False},
        {'slot': 'scopes', 'severity': 'informational', 'description': 'This header selects countable endpoint-law assembly; later signed duality, marginal invariance, L2 and restart/Markov claims remain excluded.', 'source': 'AppendixA1 3216-3227 and later process obligations.', 'lean': 'Header ends with only Q=sum L, probability Q, and J preservation.', 'evidence': 'No all-time path reversal or time-semigroup binder/conclusion appears.', 'blocking': False}
    ], 'repairs': [], 'defects': [],
    'edge_cases': {
        'rank0': 'Allowed by ambient FiniteDimensional E with no positive-rank premise; product Gibbs/Gaussian definitions remain actual singleton laws.',
        'n0': 'Nat sum includes0; Prefix0 is singleton with empty event product1 and terminal survival.',
        'T0': 'NNReal includes0, positive-count strict simplexes empty. Actual Z zero-time property remains P-a.e. for each initial phase; no unjustified all-clock pointwise zero clause is substituted.',
        'zero_rate_infinite_wait': 'Original reflection division convention, hittingAfter top, stopped records and fallback remain literal; no rate positivity added.',
        'jumps': 'Actual path representative is post-event. Endpoint-law reversal does not assert pointwise reversed right-continuous paths at jump instants.',
        'measure_order': 'nu is position Gibbs prod momentum Gaussian; parameter sigma is phase prod simplex; Q source is phase prod clocks; endpoint pair is initial then terminal before J flips and swaps.'
    },
    'source_gap_and_required_internal_work': 'Original A7 bound is fixed-initial and energy dependent. Future proof must establish measurable initial-phase sector integrals using actual93 joint Gamma/rho and sigma-finite simplex, then nonnegative Tonelli/countable exchange. Probability must come from actual103 and actual clock law, not inferred merely from104. No joint count measurability or uniform signed domination is a public assumption.',
    'actual_parent_contract': 'Actual93 supplies the same global Z and count-sector test law;103 supplies actual phase probability; UnitExponentialProduct supplies actual clock probability;104 supplies every finite-sector J reversal.95 fixed-initial signed expansion is an inspected alternative, not an invented direct dependency.',
    'typecheck_scope': 'Terminal PASS of the exact candidate Prop; unused-hypothesis warnings are type-definition lint only and are not proof or theorem completion.',
    'topology_self_validation': False, 'source_graph_status': 'Separate independent mathematical/topology admission remains required.',
    'no_new_Lean_header_or_statement_seal_by_reviewer': True, 'mathematical_completion': False, 'VERIFIED_transition': False
})
inputs = [H, A93, A104, primary, P / 'header105.receipt.json', P / 'header105.stdout.log', P / 'header105.stderr.log']
inputs += [SRC / n for n in ['primary-first-reconstruction105.native.json', 'expected-semantic-slots105.native.json', 'recommendation105.native.json', 'source-proof-graph-delta105.native.json', 'source-coverage-delta105.native.json', 'literal-definition-context105.native.json', 'retrieval105.native.json', 'closed-RAW-preread105.native.json']]
originals = sorted(p for p in O.iterdir() if p.is_file() and not p.name.endswith('.gz'))
archives = []
for p in originals:
    q = Path(str(p) + '.raw.gz')
    assert not q.exists()
    q.write_bytes(gzip.compress(p.read_bytes(), mtime=0))
    assert gzip.decompress(q.read_bytes()) == p.read_bytes()
    archives.append({'original': ref(p), 'archive': ref(q), 'lossless': True})
closure = put('closed-RAW-header-source105.native.json', {
    'kind': 'closed immutable prospective source-header review', 'reviewer': '/root/source_final96',
    'decision': decision, 'header': ref(H), 'selected_inputs': [ref(p) for p in inputs],
    'owned_artifacts': [ref(p) for p in sorted(O.iterdir()) if p.is_file()], 'original_RAW_archives': archives,
    'self_hash_intentionally_omitted': True, 'no_new_full_primary_copy': True, 'graph_self_validation': False, 'proof_credit': False
})
print(json.dumps({'decision': decision, 'coverage': coverage, 'run': run, 'closure': closure}, indent=2))
