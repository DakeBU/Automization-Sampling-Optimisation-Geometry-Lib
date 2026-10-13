from pathlib import Path
import gzip
import hashlib
import json
import re

ROOT = Path('E:/Samplinglib')
PRE = 'runs/20261007-companion-priority/pbps-bounded-gibbs-duality-preread106'
SOURCE = 'runs/20261007-companion-priority/pbps-actual-countable-endpoint105/next-primary106'
OUT = ROOT / PRE / 'independent-header-source106'
inputs = {}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def ref(path):
    p = ROOT / path
    b = p.read_bytes()
    d = {'path': path, 'raw_sha256': sha(b), 'bytes': len(b)}
    inputs[path] = d
    return d


def load(path):
    ref(path)
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def put(name, data):
    p = OUT / name
    assert not p.exists()
    p.write_bytes((json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode())
    b = p.read_bytes()
    return {'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(b), 'bytes': len(b)}


frozen = load(PRE + '/independent-header-source106/primary-expectations-frozen106.native.json')
expect = load(SOURCE + '/expected-semantic-slots106.native.json')
context = load(SOURCE + '/literal-definition-context106.native.json')
coverage = load(SOURCE + '/source-coverage-delta106.native.json')
graph = ref(SOURCE + '/source-proof-graph-delta106.native.json')
recommendation = ref(SOURCE + '/recommendation106.native.json')
original_closure = ref(SOURCE + '/closed-RAW-preread106.native.json')
ref(SOURCE + '/retrieval-label-clarification106/closed-RAW-clarification106.native.json')
primary = ref(coverage['primary']['path'])
assert primary == coverage['primary']
rawprimary = (ROOT / primary['path']).read_bytes()
for region in coverage['regions']:
    assert sha(rawprimary[region['byte_start']:region['byte_end_exclusive']]) == region['raw_sha256']
header = ref(PRE + '/Header106.lean')
assert header['raw_sha256'] == '6e995eb9308bf5c6d09fcd15b6ebb0e120b3fced62202572a4041cbfe19e7b9d'
raw = (ROOT / header['path']).read_bytes()
s = raw.decode('utf-8').replace('\r\n', '\n')
producer = ref(context['producer']['path'])
assert producer == context['producer']
old = (ROOT / producer['path']).read_text(encoding='utf-8')
literal = s[s.index('    let c :'):s.index('    ∃ Z :')]
witness = s[s.index('    ∃ Z :'):s.index('      (∀ y xRef : E, ∀ T : ℝ≥0,')]
binders = s[s.index('    {E : Type*}'):s.index(' : Prop := by')]
oldbinders = old[old.index('    {E : Type*}'):old.index(' : Prop := by')]
assert literal == context['literal37_LF_text']
assert witness == context['global_witness_prefix_LF_text']
assert binders == oldbinders
receipt = load(PRE + '/typecheck106/receipt.json')
stdout = ref(PRE + '/typecheck106/stdout.log')
stderr = ref(PRE + '/typecheck106/stderr.log')
assert receipt['exit_code'] == 0 and receipt['terminal_closed'] and receipt['proof'] is False
assert receipt['header']['raw_sha256'] == header['raw_sha256']
rawlines = raw.splitlines(keepends=True)
lines = s.splitlines(keepends=True)
defs = []
starts = [(i, re.match(r'^    let (\S+)', line).group(1)) for i, line in enumerate(lines) if re.match(r'^    let (\S+)', line)]
assert len(starts) == 37
for k, (a, name) in enumerate(starts):
    b = starts[k + 1][0] if k + 1 < len(starts) else 122
    data = b''.join(rawlines[a:b])
    defs.append({'name': name, 'line_start': a + 1, 'line_end': b, 'header_span_RAW_sha256': sha(data),
                 'comparison': 'Exact LF text equality with unchanged actual105 literal context; original RAWs separately pinned.'})
comparison = put('literal-comparison106.native.json', {
    'header': header, 'producer': producer, 'frozen_literal_context': inputs[SOURCE + '/literal-definition-context106.native.json'],
    'ambient_and_six_analytic_binders_LF_exact': True, 'binders_LF_sha256': sha(binders.encode()),
    'literal37_LF_exact': True, 'literal37_LF_sha256': sha(literal.encode()),
    'global_Z_prefix_LF_exact': True, 'global_Z_prefix_LF_sha256': sha(witness.encode()),
    'individual_definition_spans': defs, 'new_lets': [
        {'name': 'op', 'lines': [134, 135], 'meaning': 'Real Bochner expectation over the actual P of G(Z y xRef z T w).'},
        {'name': 'endpoint', 'lines': [136, 137], 'meaning': 'Actual output from initial phase and clock sample; phase-first product domain.'}],
    'total_let_count': len(re.findall(r'^\s+let ', s, re.M)),
    'typecheck': inputs[PRE + '/typecheck106/receipt.json'], 'compiler_scope': 'Type-only elaboration; six unused-binder linter warnings are not proof discharge and do not authorize removing source conditions.'
})

judgments = {
    'objects': ('equivalent', 'Lines22–122 retain all actual algorithm/density definitions and exact normalized phase law;123–132 produce the actual global Z. Lines134–137 define op and endpoint from that same Z and P.', [22, 137]),
    'domains': ('equivalent', 'Ambient finite-dimensional real inner-product Borel E permits rank0. Every y,xRef and finite NNReal T is included. F,G are arbitrary real Borel measurable bounded functions; no continuity, positive time or positive-rate restriction.', [12, 19, 133, 141]),
    'quantifiers': ('equivalent-after-independent-universal-reordering', 'A single global ∃Z precedes all parameter/time/test quantifiers. Pointwise arc/fallback and parameterwise P-a.e. zero-time contract are unchanged. C_F,C_G are quantified before the measurability implications; these independent universal variables commute with those implications without changing meaning.', [123, 145]),
    'assumptions': ('equivalent', 'Exactly six original analytic hypotheses at15–19; observable measurability and nonnegative finite uniform bounds express the original bounded test class. No supplied Z,Q, probability, integrability, Gaussian symmetry, kernel or Markov property.', [15, 19, 139, 141]),
    'conclusion': ('equivalent', 'Line138 is actual fixed-time phase stationarity as MeasurePreserving endpoint (nu.prod P) nu.142–145 assert both honest real L¹ conclusions and ∫F opG dnu = ∫(G∘R) op(F∘R) dnu, exactly the primary bounded reversal orientation.', [138, 145]),
    'scopes_senses': ('equivalent', 'Full actual measure equality and bounded signed scalar identity only. No L² operator identity, restart, semigroup, arbitrary83 witness identification, all-time jumpwise path reversal or paper completion appears. op is merely a defined expectation.', [123, 145]),
    'constant_dependencies': ('equivalent', 'Exact sqrtη flow/rate and Vy quadratic coefficient1/(2η) survive literal comparison. P rate1 and standard Gaussian momentum remain fixed. C_F,C_G are arbitrary finite nonnegative test bounds, not new analytic restrictions or asymptotic constants.', [23, 38, 50, 118, 122, 139, 145])
}
slots = {k: {'source': expect['slots'][k], 'header': v[1], 'relation': v[0], 'evidence': {'header_lines': v[2], 'literal_comparison': comparison}} for k, v in judgments.items()}
regions = []
for r in coverage['regions']:
    row = dict(r)
    row['header106_disposition'] = (
        'Exact analytic binders12–19.' if r['id'] in ['standing-curvature', 'standing-eta'] else
        'Literal actual definitions22–117 and global witness123–132; unchanged from105.' if r['id'] in ['actual-phase', 'event-convention', 'simplex', 'prescribed'] else
        'Vy/nu118–122; source signed Gibbs averaging interpreted by op134–135 and endpoint136–138.' if r['id'] in ['target-position-energy', 'phase-gibbs-law', 'average'] else
        'Selected signed identity142–145 and F=1 actual marginal138; trailing L² extension explicitly excluded.' if r['id'] == 'weight-matching-and-invariance' else
        'Future L²/operator boundary; no corresponding claimed106 operator conclusion.' if r['id'] == 'A3-boundary' else
        'Existing license reference only; no source copy.' if r['id'] == 'source-license' else
        'Unchanged inherited producer/source mechanism; no new header premise or new completion claim.')
    regions.append(row)
cov = put('header-source-coverage106.native.json', {
    'kind': 'prospective source/header coverage only, not compiled-proof coverage', 'header': header,
    'primary': primary, 'regions': regions, 'all21_RAW_slices_verified': True,
    'source_graph': graph, 'source_graph_creator': '/root/source_final96',
    'topology_review_scope': 'Parent reports independent exact_verifier96 topology acceptance. This source review does not inspect or re-admit its own graph topology.',
    'header_regions': [
        {'lines': [1, 10], 'disposition': 'Imports, namespace and type-only context; not hypotheses or theorem proof.'},
        {'lines': [11, 21], 'disposition': 'Candidate Prop definition and ambient/six original analytic binders.'},
        {'lines': [22, 122], 'disposition': 'All37 literal actual definitions; individually matched and spanned in comparison.'},
        {'lines': [123, 132], 'disposition': 'Same global actual witness contract, no supplied provider.'},
        {'lines': [133, 138], 'disposition': 'Universal parameters/time, actual expectation/endpoint, fixed-time Gibbs phase invariance.'},
        {'lines': [139, 145], 'disposition': 'Exact source bounded signed test class, two integrabilities and flipped bilinear identity.'},
        {'lines': [146, 149], 'disposition': 'Blank/check/section closure, no theorem proof.'}],
    'proof_ingredients_internal_only': ['Same-Z actual105 endpoint law and reversal', 'Actual103 normalized phase probability', 'Actual unit-exponential product probability', 'Bounded real integrability and signed Fubini', 'Gaussian momentum flip and product-measure preservation'],
    'certified_new_Lean_edges': 0, 'implementation_proof_reviewed': False, 'self_topology_validation': False
})
run = put('header-source-run106.native.json', {
    'reviewer': '/root/source_final96', 'role': 'independent primary-facing prospective header review',
    'header': header, 'primary_first_freeze': inputs[PRE + '/independent-header-source106/primary-expectations-frozen106.native.json'],
    'source_recommendation': recommendation, 'original_source_closure': original_closure,
    'literal_comparison': comparison, 'coverage': cov, 'typecheck_receipt': inputs[PRE + '/typecheck106/receipt.json'],
    'typecheck_stdout': stdout, 'typecheck_stderr': stderr,
    'independence': {'formalizer': 'root', 'source_reviewer': '/root/source_final96', 'source_graph_creator': True,
                     'source_graph_self_validated': False, 'new_implementation_seen': False, 'proof_search_performed': False},
    'read_order': 'Frozen106 expected slots and literal context re-read; all21 source slices rehashed; fresh expectation record written; then complete Header106 and its typecheck receipt read.',
    'no_shared_edits': True, 'no_new_full_primary_archive': True
})
decision = put('header-source-decision106.native.json', {
    'verdict': 'ACCEPT_PROSPECTIVE_HEADER_SOURCE_BOUNDARY_ONLY', 'reviewer': '/root/source_final96',
    'header': header, 'review_run': run, 'primary': primary, 'semantic_slots': slots,
    'deltas': [{'slot': 'quantifiers', 'severity': 'informational', 'description': 'Independent universal bound variables are introduced before measurable-test implications.',
                'source': 'The frozen recommendation puts measurable-test implications before the two bound variables.',
                'lean': 'Header139 introduces F,G,C_F,C_G, then140–141 the independent hypotheses.',
                'evidence': 'C_F,C_G do not occur in Measurable F/G. Universal introduction order is logically equivalent.', 'blocking': False}],
    'repairs': [], 'defects': [], 'literal_comparison': comparison, 'source_coverage': cov,
    'edge_cases': {'rank0': 'No dimension lower bound; ambient type remains permitted.', 'T0': 'Finite nonnegative T includes0 and inherited initialization remains parameterwise P-a.e.',
                   'n0': 'Literal empty-prefix/rate-product semantics inherited; final statement has no fixed-count restriction.',
                   'zero_test_bounds': 'Allowed with no division by bounds.', 'zero_normals_rates': 'Literal totalized bounce/rate unchanged.',
                   'jump_values': 'No pointwise time-reversed jump path equality.', 'null_sets': 'No exchange of parameterwise a.e. and a.e. simultaneous all parameters.'},
    'claim_boundary': 'This accepts source-facing candidate semantics and observed type elaboration only. It is not a Statement Seal, claimed SAU, theorem proof, final blind-decoder fidelity, compiled proof-graph review, VERIFIED state, browser acceptance or completion.',
    'remaining_reds': expect['remaining_reds'], 'source_graph_self_validation': False,
    'arbitrary_provider_or_83_identification': False, 'shared_mutations': False
})
archives = []
for p in sorted(OUT.iterdir()):
    if p.is_file():
        b = p.read_bytes()
        a = Path(str(p) + '.raw.gz')
        assert not a.exists()
        a.write_bytes(gzip.compress(b, mtime=0))
        assert gzip.decompress(a.read_bytes()) == b
        archives.append({'raw_path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(b),
                         'archive': a.relative_to(ROOT).as_posix(), 'archive_raw_sha256': sha(a.read_bytes())})
owned = [{'path': p.relative_to(ROOT).as_posix(), 'raw_sha256': sha(p.read_bytes()), 'bytes': p.stat().st_size}
         for p in sorted(OUT.iterdir()) if p.is_file()]
closure = put('closed-RAW-header-source106.native.json', {
    'kind': 'Closed prospective header source review106', 'header': header, 'decision': decision,
    'review_run': run, 'selected_inputs': list(inputs.values()), 'owned_artifacts': owned,
    'original_RAW_archives': archives, 'original_source_packet_unchanged': True,
    'no_new_full_primary_archive': True, 'self_hash_intentionally_omitted': True
})
print(json.dumps({'decision': decision, 'coverage': cov, 'run': run, 'closure': closure}, indent=2))
