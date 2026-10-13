from pathlib import Path
import gzip
import hashlib
import json
import re

ROOT = Path('E:/Samplinglib')
PRE = ROOT / 'runs/20261007-companion-priority/pbps-actual-l2-expectation-preread107'
OUT = PRE / 'independent-header-source107'
SRC = ROOT / 'runs/20261007-companion-priority/pbps-actual-bounded-gibbs-duality106/next-primary107'


def ref(p):
    b = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}


def load(p):
    return json.loads(p.read_text(encoding='utf8'))


def put(name, x):
    p = OUT / name
    assert not p.exists()
    p.write_bytes((json.dumps(x, ensure_ascii=False, indent=2) + '\n').encode())
    return ref(p)


header = PRE / 'Header107.lean'
assert ref(header)['raw_sha256'] == 'cd447dcfc7bbff5045c9fd99d190b72a154f1443d4793c82c728dc4313612352'
h = header.read_text(encoding='utf8')
prod = ROOT / 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBoundedGibbsDuality.lean'
s = prod.read_text(encoding='utf8')
start = '    {E : Type*}'
old = s[s.index(start):s.index('\n\n\nset_option maxHeartbeats')].rstrip()
inherited = h[h.index(start):h.index('      (∀ G : (E × E) → ℝ, Measurable G →')].rstrip()
assert inherited.endswith(' ∧')
assert inherited[:-2].rstrip() == old
literal = h[h.index('    let c :'):h.index('    ∃ Z :')]
assert len(re.findall(r'^    let ', literal, re.M)) == 37
assert len(re.findall(r'^\s*let ', h, re.M)) == 40
assert (PRE / 'type-only1/input.exactraw.lean').read_bytes() == header.read_bytes()
receipt = load(PRE / 'type-only1/receipt.json')
assert receipt == {'exit_code': 0, 'header_RAW_sha256': ref(header)['raw_sha256'], 'type_only': True, 'no_proof': True}
assert not (PRE / 'type-only1/stderr.log').read_bytes()
freeze = load(OUT / 'primary-first-header107.native.json')
primary = ROOT / freeze['source']['path']
assert ref(primary) == freeze['source']
for r in freeze['source_regions']:
    assert hashlib.sha256(primary.read_bytes()[r['byte_start']:r['byte_end_exclusive']]).hexdigest() == r['raw_sha256']
admission = SRC / 'independent-topology107/v2-admission/admission107.v2.native.json'
a = load(admission)
assert ref(admission)['raw_sha256'] == '01bc9afe03cdc354296be98d94d27beea6ad9bed6aa50c938988347799930d38'
assert a['decision'] == 'ACCEPT_EXACT_V2_PROPOSAL_FOR_PROSPECTIVE_STATEMENT_SEAL'
assert a['graph_raw_sha256'] == ref(SRC / 'graph-expansion107/source-proof-graph-delta107.v2.native.json')['raw_sha256']

slots = {
    'objects': {'source': 'Actual harmonic flow/bounce/hazard/clock construction and normalized phase law; extend its actual expectation to real L2.', 'header': 'Lines23-123 preserve37 actual definitions; lines124-146 preserve same Z and106 outputs. Lines155-162 produce actual real Lp continuous linear maps with expectation identity.', 'relation': 'equivalent-after-explicit-elaboration', 'evidence': 'Exact LF inherited106 substring equality; no arbitrary process/kernel/operator binder. Operator A at155 locally shadows the history-set A at83 without altering earlier lexical references.'},
    'domains': {'source': 'Finite-dimensional real phase H=E×E, position first; nonnegative finite time. Borel bounded tests first, then real L2 equivalence classes.', 'header': 'Lines13-15 finite-dimensional real Hilbert/Borel E including rank0; T:NNReal; lines147-153 Borel G; lines158-162 arbitrary MemLp G2(nu y).', 'relation': 'equivalent-after-explicit-elaboration', 'evidence': 'MemLp does not impose pointwise Borel representatives. Arbitrary-L2 section integrability is only nu-a.e.; no hidden pointwise or joint operator topology condition.'},
    'quantifiers': {'source': 'Actual single process construction fixed before parameters and observables; later L2 operator must act independently of selected observable.', 'header': 'Global ∃Z124 before all y,xRef,z,T,G; ∀y xRef154 then ∃A155 indexed by all T before ∀G,hG158. Borel G147 precedes joint parameter measurability148-149.', 'relation': 'same', 'evidence': 'One same-Z inheritance and one family per y,xRef; no function-dependent operator or swapped existential. Null sets may depend on parameters and G.'},
    'assumptions': {'source': 'hα,hαβ,hV,hH,hη,hβη under original ambient setting. Measurability, normalization, integrability, contraction and representative facts are proof obligations.', 'header': 'Lines16-20 retain exactly six binders. All process/operator facts are conclusions. hG at158 is the quantified observable domain MemLp, C at150 only an observable bound.', 'relation': 'same', 'evidence': 'Exact inherited binder substring checked. Type-only linter unused-proof-variable warnings are expected for a Prop definition, not removed source conditions.'},
    'conclusion': {'source': 'A strict analytic prerequisite of the density step to A.3: actual expectation induces an L2 contraction. Retain bounded duality as same-witness future consumer input.', 'header': 'Inherited endpoint preservation and signed bounded duality134-146; joint Borel total expectation147-149 and every bounded section L1150-153; A0=id156, norm≤1157, arbitrary-L2 a.e. sections160, existential output MemLp and toLp identity161, square contraction162.', 'relation': 'equivalent-after-explicit-elaboration', 'evidence': 'Both terms of square inequality are finite from input/output MemLp. Norm bound and identification concern actual P expectation; no total-integral convention used to assert every unbounded section integrable.'},
    'scopes': {'source': 'Fixed-time L2 extension preparation, independently of restart/semigroup. Printed A.3 and all-L2 strong continuity are subsequent obligations.', 'header': 'No adjoint reversal, Chapman-Kolmogorov, Markov, strong continuity or operator-family measurability predicate. Pointwise actual arc/fallback inherited, clock-a.e. zero-time retained, L2 equality is quotient equality.', 'relation': 'same', 'evidence': 'A:NNReal→CLM is only a family; its codomain CLM asserts linear boundedness at each time, not continuity in T. Only genuinely measurable G gets joint Borel expectation.'},
    'constant_dependencies': {'source': 'Contraction1 from normalized initial/clock probabilities and stationarity; bounded expectation preserves its test boundC.', 'header': 'Norm≤1 and square inequality coefficient1; sameC in bounded bound. V/alpha/beta/eta restrictions retained; no new dimension or time factor.', 'relation': 'same', 'evidence': 'Rank0 and time0 remain admitted. Eta scaling and rate normalization unchanged in literal definitions; no added normalizer, minimizer, moment or invariant-provider assumption.'}
}
span_specs = [(1, 12, 'imports, namespace and type-only candidate label'), (13, 20, 'ambient setting and six source binders'), (21, 22, 'classical Prop elaboration, no theorem proof'), (23, 123, '37 exact definitions'), (124, 133, 'same global actualZ joint/arc/fallback/zero contract'), (134, 146, 'all106 inherited bounded duality and endpoint stationarity'), (147, 153, 'joint Borel expectation and bounded sections'), (154, 162, 'actual L2 family, zero identity, norm, AE sections and representative/square claims'), (163, 167, 'typecheck and namespace closure')]
rawlines = header.read_bytes().splitlines(keepends=True)
spans = []
for lo, hi, scope in span_specs:
    b = b''.join(rawlines[lo - 1:hi])
    spans.append({'line_start': lo, 'line_end': hi, 'scope': scope, 'raw_sha256': hashlib.sha256(b).hexdigest()})
coverage = put('header-source-coverage107.native.json', {
    'header': ref(header), 'all167_header_lines': spans,
    'all21_source_regions_rehashed': freeze['source_regions'],
    'inherited_source_coverage': ref(SRC / 'source-coverage107.native.json'),
    'v2_source_coverage': ref(SRC / 'graph-expansion107/source-coverage107.v2-overlay.native.json'),
    'graph_v2': ref(SRC / 'graph-expansion107/source-proof-graph-delta107.v2.native.json'),
    'separate_topology_admission': ref(admission), 'graph_counts': {'nodes': 85, 'edges': 160},
    'selected_header_source_mapping': {'BOREL-OP107': [147, 153], 'L2-LIFT107': [154, 162], 'COUNT93': [124, 133], 'AVG100/INV100': [134, 146], 'NORM/clock': 'actual definitions121-123/51; probability is an internal producer obligation, not an extra binder', 'L2-CONSTRUCT107/PRODUCT-L1-FUBINI107/L2-IDENTIFY107/AE-REP107': 'Required internal proof ingredients for154-162; not supplied by typecheck or additional assumptions.', 'L2A3/PHASE-FLIP106 future incidence': 'Excluded future consumer, not a header conclusion.', 'RESTART': 'Excluded independent source boundary.'},
    'literal_global_definitions': 37, 'all_statement_lets': 40,
    'source_graph_creator_not_self_validator': True, 'compiled_proof_coverage': False})
run = put('header-source-run107.native.json', {
    'reviewer': '/root/source_final96', 'primary_first': ref(OUT / 'primary-first-header107.native.json'),
    'header': ref(header), 'receipt': ref(PRE / 'type-only1/receipt.json'), 'stdout': ref(PRE / 'type-only1/stdout.log'),
    'exact_compiler_input': ref(PRE / 'type-only1/input.exactraw.lean'),
    'coverage': coverage, 'prior_involvement': freeze['prior_involvement'],
    'mathematical_proof_review': False, 'own_topology_admission': False,
    'no_source_or_Lean_or_shared_edits': True, 'source_license': freeze['source_license']})
decision = put('header-source-decision107.native.json', {
    'decision': 'ACCEPT_PROSPECTIVE_EXACT_HEADER_SOURCE_BOUNDARY', 'reviewer': '/root/source_final96',
    'header': ref(header), 'primary_first': ref(OUT / 'primary-first-header107.native.json'),
    'semantic_slots': slots, 'deltas': [], 'repairs': [], 'blocking_findings': [],
    'type_only_status': 'PASS, exact input equals currentHeader; this is not proof or final fidelity admission',
    'inherited106_exact_LF_substring': True, 'literal_definitions_exact': 37,
    'all_statement_lets': 40, 'source_binders': 6, 'header_lines': 167,
    'coverage': coverage, 'run': run, 'separate_graph_admission': ref(admission),
    'source_gap_handled_as_obligation': 'A.3 density step suppresses the L2 operator/domain construction. Header exports that construction as an obligation, not a premise. Required Hilbert averaging/L1/Fubini/representative edges are separately admitted prospective topology.',
    'no_proof_or_seal_or_claim_credit': True, 'no_topology_self_validation': True,
    'remaining_reds': ['proof of candidate107', 'L2 adjoint reversal A.3', 'strong continuity', 'same-witness alignment with older kernel/small-time results', 'restart/Markov/semigroup', 'hypocoercivity, implementation/costs, composition and main paper results']})
inputs = [header, prod, primary, PRE / 'type-only1/receipt.json', PRE / 'type-only1/stdout.log', PRE / 'type-only1/stderr.log', PRE / 'type-only1/input.exactraw.lean', admission, SRC / 'recommendation107.native.json', SRC / 'literal-context107.native.json', SRC / 'source-coverage107.native.json', SRC / 'graph-expansion107/source-proof-graph-delta107.v2.native.json', SRC / 'graph-expansion107/source-coverage107.v2-overlay.native.json']
archives = []
for p in sorted(OUT.iterdir()):
    if p.is_file() and not p.name.endswith('.gz'):
        a = p.with_name(p.name + '.raw.gz')
        assert not a.exists()
        a.write_bytes(gzip.compress(p.read_bytes(), mtime=0))
        assert gzip.decompress(a.read_bytes()) == p.read_bytes()
        archives.append({'raw': ref(p), 'archive': ref(a)})
closure = put('closed-RAW-header-source107.native.json', {
    'decision': decision, 'coverage': coverage, 'run': run,
    'selected_inputs': [ref(p) for p in inputs], 'owned_artifacts': [ref(p) for p in sorted(OUT.iterdir()) if p.is_file()],
    'raw_archives': archives, 'no_full_primary_archive': True,
    'self_hash_omitted': True, 'no_shared_mutation': True})
print(json.dumps({'decision': decision, 'coverage': coverage, 'run': run, 'closure': closure}, indent=2))
