"""Bind the exact actual-matrix statements, source uses and complete proof steps."""
from pathlib import Path

old = Path('.astis/huanjian-gc-source-row-law-20261112/make_source_lean_map.generated.py').read_text()
prefix = old.split('P = Path(', 1)[0]
prefix = prefix.replace('source-row-law-semantic-evidence', 'source-matrix-mean-semantic-evidence')
tail = r'''
P = Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixMean.lean')
T = Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixMean.lean')

def code_span(path, first, last):
    body = path.read_bytes()
    lines = body.splitlines(keepends=True)
    assert 1 <= first <= last <= len(lines)
    before, span = b''.join(lines[:first-1]), b''.join(lines[first-1:last])
    return {'path': str(path), 'file_sha256': sha(body), 'LF_lines_1based': [first, last],
            'raw_UTF8_byte_span': [len(before), len(before) + len(span)],
            'decoded_char_span': [len(before.decode()), len(before.decode()) + len(span.decode())],
            'span_sha256': sha(span)}

def mapping(ids, spans, meaning):
    return {'source': [source_span(x) for x in ids],
            'lean': [code_span(*x) for x in spans], 'meaning': meaning}

mappings = [
    mapping(['S4.Thmtheorem4.p1.1'], [(P, 18, 43), (T, 18, 45)],
            'Exact natural d,q and2q+1<d, includingq0. No row-law, moment, integrability, mean or Gram certificate binder. All local lets are fixed definitions.'),
    mapping(['A3.SS2.p1', 'A3.Ex85'], [(P, 19, 32), (P, 47, 78), (T, 49, 80)],
            'Literal original-column sample space/product Gaussian measure and actual physical rows. Same canonical measurable marginal-law node is reused, without an ambient-transfer or independence prerequisite.'),
    mapping(['A3.SS2.p10', 'A3.Ex107.m1', 'A3.Ex108.m1'],
            [(P, 23, 39), (P, 68, 78), (T, 23, 39)],
            'Exact L and canonical retained-radius coefficient a; actual Gaussian-first closed-cutoff inverse-d matrix entries. Scalar and matrix integrability are supplied internally by the existing canonical radial moment/provider proof, not a Bochner zero default.'),
    mapping(['A3.SS2.p12.2', 'A3.Ex108.m1'], [(P, 74, 78), (P, 79, 89)],
            'Canonical retained outer-product moment and its integrability are matched to the literal cutoff and transported to actual original rows. The common actual row pushforward also identifies the canonical radial coefficient for each physical row.'),
    mapping(['A3.SS2.p12.3', 'A3.SS2.p12.4'], [(P, 79, 89)],
            'Noninjective actual row integral transport uses actual map equality and a.e. strong measurability. No measurable-embedding premise or substituted equal-in-law random variable. The common coefficient remains canonical.'),
    mapping(['A3.Ex107.m1', 'A3.SS2.p12.4'], [(P, 90, 118)],
            'Exact actual Yi equals the fixed continuous tensor image of the actual retained row matrix. Matrix integrability and the genuine Bochner mean follow by the CLM integral rule. The OR entrywise route is unselected, not falsely claimed proved.'),
    mapping(['A3.Ex110.m1'], [(T, 1, 80)],
            'Complete private statement and original-experiment setup materially call the new individual-mean producer. Target includes actual sums, not supplied formal mean matrices.'),
    mapping(['A3.Ex87.m1', 'A3.SS2.p5', 'A3.SS2.p7', 'A3.SS2.p12.4'],
            [(T, 81, 110)],
            'Exact algebraic half-grid normalization and actual canonical cosine-frame theorem yield both deterministic feature sums, includingq0. The source consumer-use site is p12.4.'),
    mapping(['A3.Ex110.m1'], [(T, 111, 143)],
            'Tensor linearity and actual individual means yield both source sums of expectations, with I tensor I equal to the paired identity and nonzero d derived internally.'),
    mapping(['A3.Ex110.m1', 'A3.SS2.p12.5'], [(T, 144, 158)],
            'Both actual random sums are integrable. Internal finite Bochner and scalar exchange derives their expected values aI and0 under the same original product measure. No independence assumption is needed.'),
]
draft = json.loads((evidence / 'publication-draft-record.json').read_bytes())
background = []
for declaration, filename, windows, use, meaning in [
    ('FixedSpectrumSourceRowLaw.actual_source_row_marginal_law',
     'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceRowLaw.lean',
     [(13, 54)], (P, 77, 89), 'Existing same-experiment measurable Gaussian row map; exact canonical identity retained.'),
    ('FixedSpectrumTruncatedRowMoment.actual_truncated_row_second_moment',
     'AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumTruncatedRowMoment.lean',
     [(20, 93)], (P, 74, 89), 'Existing retained moment and its scalar/matrix integrability body, including finite entry-to-L2Operator matrix bridge; complete body is separately supplied for independent review.'),
    ('ProbabilityTheory.map_pi_eq_stdGaussian',
     '.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean',
     [(137, 142)], (P, 77, 89), 'Physical Euclidean Gaussian product specialization used inside the unchanged canonical row-law provider.'),
    ('MeasureTheory.integral_map',
     '.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean',
     [(1043, 1065)], (P, 84, 89), 'General noninjective transport with actual a.e. measurability.'),
    ('ContinuousLinearMap.integral_comp_comm',
     '.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/ContinuousLinearMap.lean',
     [(51, 70)], (P, 109, 118), 'Complete real matrix CLM Bochner commutation with actual integrability.'),
    ('MeasureTheory.integrable_finsetSum',
     '.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean',
     [(440, 450)], (T, 144, 156), 'Finite actual-sum integrability; no independence premise.'),
    ('MeasureTheory.integral_finsetSum',
     '.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean',
     [(242, 251)], (T, 150, 156), 'Finite Bochner exchange after integrability.'),
]:
    background.append({'declaration': declaration,
        'source': [code_span(Path(filename), a, b) for a,b in windows],
        'consumer': code_span(*use), 'meaning': meaning})
record = {
    'kind': 'Root-authored exact source/Lean correspondence for independent review',
    'source_sha256': sha(raw), 'actual_ASTIS_proof_parents': draft['actual_public_ASTIS_parents'],
    'mappings': mappings, 'proof_background': background,
    'closed_source_route': 'Canonical original-row pushforward and canonical retained moment -> actual retained row integrability/mean -> fixed continuous tensor map -> exact actual Yi means -> exact frame tensor sums -> integrability and expectations of both actual finite sums.',
    'OR_route': 'CLM route selected. Entrywise expectation transport remains an unselected alternative, with no false AND or extra hypothesis.',
    'source_topology_originals': '.astis/semantic-neutral-20261112/mm_sg_61c4',
    'topology_challenger': '.astis/semantic-neutral-20261112/mm_tc_7f32/topology-v1',
    'boundary': 'Exact local means and actual-sum consumer only. Full actual/native/source/decoder/reader acceptance remains separate; no ambient, variance, concentration, main-bound, oracle/cost, integration or purification claim.',
}
path = evidence / 'source-lean-map.draft.json'
with path.open('x') as out:
    json.dump(record, out, ensure_ascii=False, indent=2)
    out.write('\n')
print(json.dumps({'path': str(path), 'sha256': sha(path.read_bytes()), 'mappings': len(mappings),
                  'proof_background_entries': len(background), 'actual_compiled_parent_map': draft['actual_public_ASTIS_parents']}))
'''
generated = Path(__file__).resolve().parent / 'make_source_lean_map.generated.py'
with generated.open('x') as out:
    out.write(prefix + tail)
exec(compile(prefix + tail, str(generated), 'exec'))
