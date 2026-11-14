"""Seal exact actual-matrix means and two actual sum integrals before proof search."""
from pathlib import Path

previous = Path('.astis/huanjian-gc-source-row-law-20261112/make_source_lean_map.generated.py').read_text()
prefix = previous.split('P = Path(', 1)[0]
prefix = prefix.replace('source-row-law-semantic-evidence', 'source-matrix-mean-semantic-evidence')
tail = r'''
from datetime import datetime, timezone
import subprocess

workspace = Path(__file__).resolve().parent.relative_to(Path.cwd())
paper = Path('research-wiki/paper-contributions/GaussianComplexity')
runner = Path('.astis/huanjian-resume-20261103')
dump = lambda x: (json.dumps(x, ensure_ascii=False, indent=2) + chr(10)).encode()

def create(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as out:
        out.write(data)

def checked(stem):
    path = runner / (stem + '.receipt.json')
    receipt_raw = path.read_bytes()
    receipt = json.loads(receipt_raw)
    log = Path(receipt['log']).read_bytes()
    assert receipt['exit_code'] == 0 and sha(log) == receipt['log_sha256']
    return {'receipt': str(path), 'sha256': sha(receipt_raw), 'log_sha256': sha(log)}, log

formation, formation_log = checked('20261112T122228147517Z-source-matrix-mean-literal-Prop-formation')
meaning, meaning_log = checked('20261112T122316201034Z-source-matrix-mean-definition-meaning')
environment_receipt, _ = checked('20261112T122316201097Z-source-matrix-mean-exact-environment-before-seal')
assert b'def producerProp' in formation_log and b'def consumerProp' in formation_log
for token in (b'AEStronglyMeasurable', b'HasFiniteIntegral', b'Matrix.instL2OpNormedAddCommGroup',
              b'Matrix.kroneckerMap', b'Measure.pi.instIsProbabilityMeasure'):
    assert token in meaning_log
producer = (workspace / 'producer-signature.original.txt').read_bytes()
consumer = (workspace / 'consumer-signature.original.txt').read_bytes()
assert not any(token in producer + consumer for token in (b':= by', b'sorry', b'axiom', b'admit'))
P = Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixMean.lean')
T = Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixMean.lean')
assert not P.exists() and not T.exists()
excerpts = []
for filename, windows in [
    ('.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/Pi.lean', [(99, 106), (208, 212)]),
    ('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean', [(154, 160)]),
    ('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/Matrix.lean', [(137, 144), (175, 183), (270, 274)]),
]:
    path = Path(filename)
    body = path.read_bytes()
    lines = body.splitlines(keepends=True)
    for first, last in windows:
        span = b''.join(lines[first-1:last])
        excerpts.append({'file': str(path), 'file_sha256': sha(body), 'lines_1based': [first, last],
                         'literal_source': span.decode(), 'literal_source_sha256': sha(span)})
context = {
    'allowed_only': 'Exact standard definition semantics and actual instance prints, no new target proof or certificate.',
    'mathlib_pin': 'db584cd6d46c92f209a44c0f1c829460d327499d',
    'literal_current_prints_and_instances': meaning_log.decode(),
    'literal_current_prints_sha256': sha(meaning_log), 'actual_current_print_receipt': meaning,
    'literal_definition_excerpts': excerpts,
    'definition_kinds': [
        {'object': 'D,E,Omega,mu,row', 'kind': 'literal', 'meaning': 'The original product experiment of q+1 standard d-dimensional Gaussian columns; row i collects their physical coordinate i in Euclidean(q+1)-space, under the same literal product measure.'},
        {'object': 'r,L,a', 'kind': 'literal', 'meaning': 'r=q+1; L=2r+3log(1000d); a is the retained canonical row radial second moment divided by r. This scalar is a definition under stdGaussian E, not a supplied actual-row moment certificate. Its equality to every actual-row retained moment must follow internally from the canonical row law.'},
        {'object': 'theta,t,Y', 'kind': 'literal', 'meaning': 'Source index i.val+1, midpoint angle (i.val+1-1/2)pi/d, feature0=1 and featurek=sqrt2cos(k theta). Yi is inverse-d times actual-row outer product Kronecker feature outer product when the actual row norm squared<=L; outside this closed cutoff it is zero.'},
        {'object': 'Matrix carrier and norm', 'kind': 'standard definitions and actual synthesized scope', 'meaning': 'Paired indices are Gaussian-first in both positions. Matrix is a finite two-entry function. Integrability and Bochner integrals use the actual Matrix.Norms.L2Operator instance, identified with operators on finite Euclidean space; completeness is internally synthesized, not an extra input.'},
        {'object': 'Integrable', 'kind': 'expanded target predicate', 'meaning': 'AEStronglyMeasurable and finite integral of the extended norm; the former is existence of an almost-everywhere equal strongly measurable representative. These are output obligations, never assumed. Integral notation is the Bochner integral, whose definition defaults to zero outside complete/integrable cases. The literal integrable outputs prevent using that default as a fake mean identity.'},
        {'object': 'producer conjunction', 'kind': 'target conclusions', 'meaning': 'Every actual Yi is integrable and its exact matrix expectation is a/d times I tensor ti ti-transpose. This gives no scalar bias/range estimate for a, no iid claim, and no new public row-law or radial-moment theorem.'},
        {'object': 'private consumer conjunction', 'kind': 'target conclusions', 'meaning': 'Both actual finite sums on the same outcome space are integrable; their Bochner expectations are a times identity and zero. The weighted sum uses precisely cos((2q+1)theta_i). These are actual integrals of sums, requiring internal integral exchange, and not caller-supplied formal mean matrices.'},
    ],
}
exposure = json.loads((workspace / 'preseal-exposure.original.json').read_bytes())
exposure['definition_lookup_exposure'] = {
    'standard_prints': meaning,
    'tool_chunks': ['9c0494', 'dd19cf', 'c25eab', '6d1d69', 'f53882', '4d1834', '5ee8cf', 'a945c5'],
    'honest_scope': 'An overbroad definition-location rg also returned existing Bochner integral theorem headers and one-line proof fragments, with output truncation; the subsequent source windows exposed adjacent standard product-measure/norm construction proof lines. These were definition-meaning lookups, not a new-target proof attempt. No unobserved full historical stdout/hash is fabricated. Existing integral APIs and these incidental exposures are disclosed, so no pristine API claim is made.',
}
exposure['new_target_proof_implementation_attempts'] = 0
seal = {
    'schema_version': 1, 'seal_id': 'GAUSSIAN-COMPLEXITY-SOURCE-MATRIX-MEAN-20261112-v1',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'state': 'EXACT_LITERAL_PROPS_FORMED;UNPROVED;INDEPENDENT_TYPE_GRAPH_TOPOLOGY_PENDING',
    'current_HEAD': subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip(),
    'source': {'version': 'arXiv2610.20492v1', 'raw': '.astis/huanjian-resume-20261103/2610.20492v1.html',
               'raw_sha256': sha(raw), 'anchors': [source_span(x) for x in [
                   'S4.Thmtheorem4.p1', 'A3.SS2.p1', 'A3.SS2.p10', 'A3.SS2.p12',
                   'A3.Ex107.m1', 'A3.Ex108.m1', 'A3.Ex110.m1']],
               'scope': 'Exact actual original-experiment Yi first moments and two finite-sum expectations from C.2 p12/Ex110.'},
    'producer': {
        'name': 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means',
        'planned_file': str(P), 'signature': producer.decode(), 'signature_sha256': sha(producer),
    },
    'actual_private_consumer': {
        'name': 'AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixMean.actual_source_truncated_sum_means',
        'planned_file': str(T), 'signature': consumer.decode(), 'signature_sha256': sha(consumer),
        'consumer_edge': 'Use exact actual Yi integrability and first moments with the existing canonical cosine Gram identities to derive actual unweighted and cos(n theta)-weighted sum integrability and expectations. No second canonical row-moment node.',
    },
    'binder_audit': [
        {'binder': 'd q : Nat', 'class': 'TYPING', 'meaning': 'Natural physical dimension and query count, q=0 retained.'},
        {'binder': 'hq : 2*q+1<d', 'class': 'STANDING', 'meaning': 'Exact source range; all positive dimension/denominator facts derive internally.'},
        {'binder': 'all local lets', 'class': 'DEFINITION', 'meaning': 'Fixed actual experiment, cutoff coefficient, features and Yi; no extra data or proof certificate.'},
    ],
    'output_bundle_audit': {'input_bundle': False,
        'producer': {'all_actual_Y_integrable': 'TARGET_CONCLUSION', 'all_actual_Y_first_moments': 'TARGET_CONCLUSION'},
        'private_consumer': {'both_actual_sums_integrable': 'TARGET_CONCLUSION', 'actual_integral_sum_identities': 'TARGET_CONCLUSION'}},
    'EXCESS_public_binders': [],
    'proof_components_forbidden_as_extra_binders': [
        'Actual row Gaussian pushforward, measurability or independence certificates',
        'Truncated row/matrix integrability, radial moment identity, a-range or bias estimate',
        'Feature Gram identities, expected summand matrices or expected sum identities',
        'Positive-query, tau-smallness, kappa or arbitrary ambient-transfer hypotheses',
    ],
    'shared_floor_audit': {
        'known_canonical_nodes': [
            'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw.actual_source_row_marginal_law',
            'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTruncatedRowMoment.actual_truncated_row_second_moment',
            'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineGram.actual_cosine_frame_gram'],
        'decision': 'Source-specific actual-experiment transport and material mean-sum assembly. Reuse the existing canonical row law and radial moment; retain old private canonical-row matrix application as immutable history, with no duplicated public lemma credit.',
        'actual_compiled_parent_edges': 'Pending actual proof and kernel extraction, never guessed from imports.',
    },
    'scope_boundary': 'Canonical original independent-column experiment only. Independence is separate existing credit and not needed to infer these first moments. No arbitrary ambient transfer, scalar a bias/range extension, centered variance or matrix concentration, full Lemma4.4, main bounds or oracle/TV/precision/cap/cost result. Serialized integration, actual reader/browser/globalgraph and purification remain open.',
    'actual_statement_formation': formation, 'actual_definition_meaning': meaning,
    'actual_environment': json.loads((workspace / 'actual-environment-before-seal.json').read_bytes()),
    'actual_environment_receipt': environment_receipt,
    'process_memory_readback': json.loads((workspace / 'process-memory-readback.json').read_bytes()),
    'preseal_exposure': exposure, 'formalizer_API_pristine': False,
    'new_target_proof_implementation_attempts': 0,
    'minimal_definition_context_sha256': sha(dump(context)),
    'source_preparation_chronology': 'Independent raw reading may precede the seal. Formal type/graph/topology admission begins only after this exact seal and literal binder/definition packet; raw notes are not recertified as accepted topology.',
}
assert not evidence.exists()
evidence.mkdir()
for name, data in [
    ('minimal-definition-context.json', dump(context)),
    ('actual-definition-meaning.log', meaning_log),
    ('StatementFormation.lean.raw.txt', (workspace / 'StatementFormation.lean').read_bytes()),
    ('DefinitionMeaning.lean.raw.txt', (workspace / 'DefinitionMeaning.lean').read_bytes()),
]:
    create(evidence / name, data)
seal_raw = dump(seal)
seal_path = paper / 'source-matrix-mean-statement-seal.json'
for path in (seal_path, workspace / 'statement-seal-v1.json'):
    create(path, seal_raw)
    path.chmod(0o444)
create(workspace / 'preseal-exposure.json', dump(exposure))
packet = {
    'roles': 'Sealed exact types, binders, literal definition semantics only. No new-target proof or prior-review verdict.',
    'producer': seal['producer'], 'actual_private_consumer': seal['actual_private_consumer'],
    'binder_audit': seal['binder_audit'], 'output_bundle_audit': seal['output_bundle_audit'],
    'EXCESS_public_binders': [], 'minimal_definition_context': context,
    'source': seal['source'], 'statement_seal_sha256': sha(seal_raw),
    'minimal_definition_context_sha256': sha(dump(context)), 'formalizer_API_pristine': False,
}
create(workspace / 'selective-type-definition-packet.json', dump(packet))
print(json.dumps({'seal': str(seal_path), 'seal_sha256': sha(seal_raw),
                  'producer_signature_sha256': sha(producer), 'consumer_signature_sha256': sha(consumer),
                  'context_sha256': sha(dump(context)), 'packet_sha256': sha(dump(packet)),
                  'new_target_proof_implementation_attempts': 0, 'topology_accepted': False}))
'''
generated = Path(__file__).resolve().parent / 'seal_literal_statements.generated.py'
with generated.open('x') as out:
    out.write(prefix + tail)
exec(compile(prefix + tail, str(generated), 'exec'))
