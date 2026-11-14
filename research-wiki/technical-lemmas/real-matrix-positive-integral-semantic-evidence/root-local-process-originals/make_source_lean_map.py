"""Pin exact upstream/application source spans and all authored code correspondence."""
from pathlib import Path

previous = Path('.astis/huanjian-gc-source-row-law-20261112/make_source_lean_map.generated.py').read_text()
prefix = previous.split('P = Path(', 1)[0]
tail = r'''
shared = Path('research-wiki/technical-lemmas/real-matrix-positive-integral-semantic-evidence')
route = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
S = Path('AutoSamplingTheory/TechnicalLemmas/Probability/RealMatrixPositiveIntegral.lean')
P = Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixVariance.lean')
upstream = Path('.lake/packages/mathlib/Mathlib/Analysis/Convex/Integral.lean')
upraw = upstream.read_bytes()
assert sha(upraw) == '1b3115887fabf0dccc2fed689d1f1ddc7a114b5de4594e752c02908a445aafb4'

def code_span(path, first, last):
    data = path.read_bytes()
    lines = data.splitlines(keepends=True)
    assert 1 <= first <= last <= len(lines)
    prefix_bytes, span = b''.join(lines[:first-1]), b''.join(lines[first-1:last])
    return {'path': str(path), 'file_sha256': sha(data), 'LF_lines_1based': [first, last],
            'raw_UTF8_byte_span': [len(prefix_bytes), len(prefix_bytes) + len(span)],
            'decoded_char_span': [len(prefix_bytes.decode()), len(prefix_bytes.decode()) + len(span.decode())],
            'span_sha256': sha(span)}

def primary(identifier):
    return {**source_span(identifier), 'file': '.astis/huanjian-resume-20261103/2610.20492v1.html',
            'file_sha256': sha(raw), 'origin': 'PRIMARY_APPLICATION'}

def external(first, last, identifier):
    lines = upraw.splitlines(keepends=True)
    pre, span = b''.join(lines[:first-1]), b''.join(lines[first-1:last])
    return {'source_id': identifier, 'file': str(upstream), 'file_sha256': sha(upraw),
            'origin': 'EXTERNAL_BACKGROUND', 'raw_utf8_start': len(pre), 'raw_utf8_end': len(pre) + len(span),
            'char_start': len(pre.decode()), 'char_end': len(pre.decode()) + len(span.decode()),
            'lf_line_start': first, 'lf_line_end': last, 'span_sha256': sha(span)}

def mapping(sources, code, meaning, attribution):
    return {'source': sources, 'lean': [code_span(*entry) for entry in code],
            'meaning': meaning, 'attribution': attribution}

shared_maps = [
    mapping([external(46, 58, 'Mathlib.Convex.integral_mem.contract')], [(S, 18, 26)],
            'Explicit authored finite-real-matrix specialization of a complete-real-normed closed-convex probability expectation theorem. Generic probability/hf/hpos are genuine arbitrary-f contracts; no new Gaussian binder.', 'ASTIS_AUTHORED_SPECIALIZATION_NOT_PRINTED_GENERAL_PAPER_THEOREM'),
    mapping([external(57, 58, 'Mathlib.Convex.integral_mem.closed_cone_obligation')], [(S, 27, 38)],
            'The upstream closed-set requirement is discharged internally by continuous Hermitian equalizer and all finite quadratic inequalities in the actual L2Operator topology. This cone geometry is new authored applicability work.', 'AUTHORED_INTERNAL_GEOMETRY'),
    mapping([external(57, 58, 'Mathlib.Convex.integral_mem.convex_and_AE_contract')], [(S, 39, 42)],
            'Prove convexity by full PSD scalar/add closure, then apply the canonical upstream theorem to the actual AE/integrable contracts. Empty indices are retained.', 'AUTHORED_INTERNAL_APPLICATION_OF_EXISTING_UPSTREAM_THEOREM'),
    mapping([primary('A3.SS2.p14.3'), primary('A3.Ex115.m1')], [(P, 147, 178)],
            'Material source consumer proves integrability and pointwise full PSD of the actual majorant-minus-square residual, then calls the one shared compiled node. The paper application is not the arbitrary-f background theorem.', 'PRIMARY_APPLICATION_WITH_AUTHORED_ANALYTIC_EXPANSION'),
]
route_maps = [
    mapping([primary('S4.Thmtheorem4.p1'), primary('A3.SS2.p1'), primary('A3.SS2.p10'), primary('A3.Ex107.m1')], [(P, 20, 65), (P, 67, 84)],
            'Same source natural range, actual column-product/physical-row realization, inclusive local cutoff, Gaussian-first tensor indices and ordinary matrix square; no extra certificates and q0 retained.', 'EXACT_CONCRETE_SOURCE_REALIZATION'),
    mapping([primary('A3.SS2.p1'), primary('A3.Ex113.m1')], [(P, 86, 107)],
            'Canonical actual-row law and radial fourth-moment application, actual noninjective integral_map, genuine transported integrability and fixed CLM majorant. Source omissions remain internal applicability proofs.', 'SOURCE_SUPPORTED_INTERNAL_APPLICABILITY'),
    mapping([primary('A3.SS2.p14.2'), primary('A3.Ex114.m1')], [(P, 109, 145)],
            'Both ordinary rank-one square identities, Kronecker multiplication, exact inverse-d squared and per-row closed indicator give actual squared-map integrability.', 'SOURCE_ORDERED_ALGEBRA_WITH_INTERNAL_INTEGRABILITY'),
    mapping([primary('A3.SS2.p14.3'), primary('A3.Ex115.m1')], [(P, 147, 178)],
            'Untruncated actual majorant is a nonnegative rank-one tensor matrix; its actual residual is PSD. Finite sum integrability is proved before the shared PSD integral call. The final pointwise CI-minus-random-square assertion is never assumed.', 'SOURCE_PSD_COMPARISON_WITH_AUTHORED_SHARED_BRIDGE'),
    mapping([primary('A3.Ex113.m1'), primary('A3.Ex115.m1')], [(P, 180, 200)],
            'Exact actual fourth moment and fixed tensor/scalar maps commute with the Bochner integrals; justify both individual and sum algebra.', 'SOURCE_EXPECTATION_ASSEMBLY_WITH_INTERNAL_BOCHNER_CONTRACTS'),
    mapping([primary('A3.Ex116.m1'), primary('A3.Ex117.m1'), primary('A3.SS2.p14.4')], [(P, 201, 214)],
            'Normalize equal midpoint grids and reuse the same canonical weighted coefficient bound. Add the integrated actual residual to derive the full source uncentered PSD bound.', 'EXACT_SOURCE_CONSTANT_AND_CANONICAL_FRAME_APPLICATION'),
]
source_package = {
    'kind': 'Author source/Lean correspondence for independent anti-anchored review; not a prior fidelity verdict',
    'primary_source_sha256': sha(raw), 'external_convex_integral_source_sha256': sha(upraw),
    'external_convex_integral_source': str(upstream),
    'mappings': shared_maps,
    'backgrounds': [
        {'role': 'Literal full PSD, integrability/Bochner and actual norm meanings', 'file': str(shared / 'minimal-definition-context.json'), 'sha256': sha((shared / 'minimal-definition-context.json').read_bytes())},
        {'role': 'The concrete consumer has its separate complete source map, rather than treating this generic node as its whole Gaussian proof', 'file': str(route / 'source-lean-map.draft.json'), 'sha256_bound_separately': True},
    ],
    'route_selection': {'selected': 'closed-convex probability integral application', 'unselected_OR_alternative': 'direct Hermitian and quadratic evaluation transport', 'planned_not_completed': 'centered/weighted squared consumer family'},
    'boundary': 'Full generic bridge and a real uncentered consumer only. No centered variance/concentration/main-result or publication/integration/purification grant.',
}
route_package = {
    'kind': 'Author exact source/Lean correspondence for actual original-experiment uncentered second moments; not a prior fidelity verdict',
    'primary_source_sha256': sha(raw), 'mappings': route_maps,
    'backgrounds': [
        {'role': 'Shared PSD integration is explicitly authored general background with its own exact source binding', 'file': str(shared / 'source-lean-map.draft.json')},
        {'role': 'Actual canonical proof-parent identities, not inferred from imports', 'declarations': json.loads((shared / 'coupled-publication-draft-record.json').read_bytes())['actual_public_ASTIS_parents']},
    ],
    'boundary': 'Uncentered squared-map integrability and C I PSD domination only. R9 full centered/weighted consumer is still unimplemented. Source implicit proof ingredients remain internal, never added binders.',
}
for path, obj in [(shared / 'source-lean-map.draft.json', source_package), (route / 'source-lean-map.draft.json', route_package)]:
    with path.open('x') as out:
        json.dump(obj, out, ensure_ascii=False, indent=2)
        out.write('\n')
print(json.dumps({'shared_map_sha256': sha((shared / 'source-lean-map.draft.json').read_bytes()),
                  'actual_consumer_map_sha256': sha((route / 'source-lean-map.draft.json').read_bytes()),
                  'shared_mappings': len(shared_maps), 'consumer_mappings': len(route_maps)}))
'''
generated = Path(__file__).resolve().parent / 'make_source_lean_map.generated.py'
with generated.open('x') as out:
    out.write(prefix + tail)
exec(compile(prefix + tail, str(generated), 'exec'))
