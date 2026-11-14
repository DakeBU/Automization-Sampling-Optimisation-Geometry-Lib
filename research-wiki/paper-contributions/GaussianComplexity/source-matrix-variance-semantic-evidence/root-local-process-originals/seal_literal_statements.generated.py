"""Locate source formulas and the exact compiled proof and statement spans."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json

evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-matrix-variance-semantic-evidence')
raw = Path('.astis/huanjian-resume-20261103/2610.20492v1.html').read_bytes()
text = raw.decode()
sha = lambda data: hashlib.sha256(data).hexdigest()
assert sha(raw) == '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
offsets = [0] + [i + 1 for i, char in enumerate(text) if char == '\n']


class SourceElements(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.elements = {}

    def source_offset(self):
        line, col = self.getpos()
        return offsets[line - 1] + col

    def handle_starttag(self, tag, attrs):
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.stack.append((tag, dict(attrs).get('id'), self.source_offset()))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                _, identifier, start = self.stack[i]
                if identifier:
                    self.elements[identifier] = (start, text.index('>', self.source_offset()) + 1)
                del self.stack[i:]
                return


parser = SourceElements()
parser.feed(text)


def source_span(identifier):
    first, last = parser.elements[identifier]
    data = text[first:last].encode()
    a, b = len(text[:first].encode()), len(text[:last].encode())
    assert raw[a:b] == data and f'id="{identifier}"'.encode() in data
    return {
        'source_id': identifier, 'char_start': first, 'char_end': last,
        'raw_utf8_start': a, 'raw_utf8_end': b,
        'lf_line_start': text.count('\n', 0, first) + 1,
        'lf_column0_start': first - text.rfind('\n', 0, first) - 1,
        'lf_line_end': text.count('\n', 0, last) + 1, 'span_sha256': sha(data),
    }




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

formation, formation_log = checked('20261112T133317277564Z-source-matrix-variance-literal-Prop-formation')
meaning, meaning_log = checked('20261112T133710785116Z-source-matrix-variance-complete-definition-meaning-v2')
environment_receipt, _ = checked('20261112T133604214657Z-source-matrix-variance-exact-environment-before-seal')
assert b'def producerProp' in formation_log and b'def consumerProp' in formation_log
for token in (b'Matrix.instMulOfFintypeOfAddCommMonoid', b'Matrix.PosSemidef', b'Finsupp.sum',
              b'AEStronglyMeasurable', b'HasFiniteIntegral', b'Matrix.instL2OpNormedRing',
              b'Matrix.instL2OpNormedSpace', b'Measure.pi.instIsProbabilityMeasure'):
    assert token in meaning_log
producer = (workspace / 'producer-signature.original.txt').read_bytes()
consumer = (workspace / 'consumer-signature.original.txt').read_bytes()
assert not any(token in producer + consumer for token in (b':= by', b'sorry', b'axiom', b'admit'))
P = Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceMatrixVariance.lean')
T = Path('Tests/GaussianComplexityFixedSpectrumSourceMatrixVariance.lean')
assert not P.exists() and not T.exists()
excerpts = []
for filename, windows in [
    ('.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/Pi.lean', [(99, 106), (208, 212)]),
    ('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean', [(154, 160)]),
    ('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/Matrix.lean', [(137, 144), (175, 183), (270, 274)]),
    ('.lake/packages/mathlib/Mathlib/Data/Matrix/Mul.lean', [(69, 73), (286, 305)]),
]:
    path = Path(filename)
    body = path.read_bytes()
    lines = body.splitlines(keepends=True)
    for first, last in windows:
        span = b''.join(lines[first-1:last])
        excerpts.append({'file': str(path), 'file_sha256': sha(body), 'lines_1based': [first, last],
                         'literal_source': span.decode(), 'literal_source_sha256': sha(span)})
context = {
    'allowed_only': 'Exact standard definition semantics and actual instance prints; no new-target proof, API-selection verdict or certificate.',
    'mathlib_pin': 'db584cd6d46c92f209a44c0f1c829460d327499d',
    'literal_current_prints_and_instances': meaning_log.decode(),
    'literal_current_prints_sha256': sha(meaning_log), 'actual_current_print_receipt': meaning,
    'literal_definition_excerpts': excerpts,
    'definition_kinds': [
        {'object': 'D,E,Omega,mu,row', 'kind': 'literal', 'meaning': 'The same original experiment of q+1 independent standard d-dimensional Gaussian columns; physical row i collects coordinate i of all columns as Euclidean(q+1)-space. All expectations use that exact product measure.'},
        {'object': 'r,L,theta,t,Y', 'kind': 'literal', 'meaning': 'r=q+1; L=2r+3log(1000d); theta=(i.val+1-1/2)pi/d; feature0=1 and featurek=sqrt2cos(k theta). Yi is inverse-d times the actual-row outer product Kronecker feature outer product on the closed norm-squared cutoff, and zero outside. Paired indices are Gaussian-first in both positions.'},
        {'object': 'Matrix product and operator norm', 'kind': 'standard definitions and actual scope', 'meaning': 'Matrix is a finite two-entry function. The actual Mul instance is ordinary matrix multiplication: (MN)ij=sum_k Mik Nkj, not entrywise multiplication. Under Matrix.Norms.L2Operator the norm is the induced Euclidean operator norm. Actual NormedRing, NormedSpace and completeness instances are synthesized, not supplied.'},
        {'object': 'Integrable and integral', 'kind': 'expanded standard predicates', 'meaning': 'Integrable means an almost-everywhere strongly measurable representative and finite extended-norm integral. Bochner integral defaults to zero outside complete/integrable cases. The explicit integrability conclusions for all squared variables prevent a vacuous second-moment bound from that default. Integrability of Yi and centered algebraic terms, and all finite-sum/integral exchanges required by the proof, must be established internally.'},
        {'object': 'Matrix.PosSemidef', 'kind': 'expanded output predicate', 'meaning': 'M is Hermitian (conjugate transpose M=M) and the quadratic form sum_i,j star(x_i) Mij x_j is nonnegative for every finitely supported x. Since the index set is finite, this is the usual finite-dimensional positive-semidefinite matrix condition. It is a conclusion, not an extra hypothesis. The displayed P difference expresses the Loewner upper bound.'},
        {'object': 'mean,Z,w,C', 'kind': 'literal definitions', 'meaning': 'mean_i is the actual Bochner expectation of Yi under mu; Zi=Yi-mean_i; wi=cos((2q+1)theta_i); C=2r(r+2)/d. No formal mean matrix, supplied variance, or symbolic random variable substitutes for these definitions.'},
        {'object': 'producer', 'kind': 'target conclusions', 'meaning': 'Every actual Yi squared is integrable and C I minus the sum of their actual second moments is positive semidefinite. The source uncentered bound is a material input for the actual centered variance consumer.'},
        {'object': 'private consumer', 'kind': 'target conclusions', 'meaning': 'Every Zi squared and every (wi Zi) squared is integrable. Both actual sums of centered second moments have Euclidean operator norm at most C. Hermitian/PSD facts, centered moment identity and weighted comparison needed to obtain these actual norm bounds are internal proof obligations.'},
    ],
}
exposure = json.loads((workspace / 'preseal-exposure.original.json').read_bytes())
exposure['definition_lookup_exposure'] = {
    'successful_standard_prints': meaning,
    'failed_definition_print': '20261112T133604214657Z-source-matrix-variance-definition-meaning (exit1 only unknown Matrix.mul; original retained)',
    'literal_source_lookup': 'Exact standard-definition location rg included one nonexistent guessed Defs path; actual Mul lines286-309 additionally exposed the adjacent mul_apply and mul_apply-prime one-line rfl theorem bodies. These are disclosed standard multiplication semantics, not a new-target proof attempt. No pristine API claim.',
    'tool_chunks': ['fd149c', 'ead58b', '4d4add', '1a1b11'],
}
exposure['new_target_proof_implementation_attempts'] = 0
memory_path = Path('research-wiki/process-memory.json')
memory_raw = memory_path.read_bytes()
memory = json.loads(memory_raw)
readback = {
    'source': str(memory_path), 'source_sha256': sha(memory_raw),
    'control_plane_math_authority': False,
    'entries_read': [x['id'] for x in memory['entries']],
    'applicable_standing_or_negative_entry_ids': [],
    'decision': 'All current entries were read. No source-matrix-variance-specific standing/negative entry applies; actual measure roles remain explicit. No mathematical route is retired by process memory.',
}
create(workspace / 'process-memory-readback.json', dump(readback))
seal = {
    'schema_version': 1, 'seal_id': 'GAUSSIAN-COMPLEXITY-SOURCE-MATRIX-VARIANCE-20261112-v1',
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'state': 'EXACT_LITERAL_PROPS_FORMED;UNPROVED;INDEPENDENT_TYPE_GRAPH_TOPOLOGY_PENDING',
    'current_HEAD': subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip(),
    'source': {'version': 'arXiv2610.20492v1', 'raw': '.astis/huanjian-resume-20261103/2610.20492v1.html',
               'raw_sha256': sha(raw), 'anchors': [source_span(x) for x in [
                   'S4.Thmtheorem4.p1', 'A3.SS2.p1', 'A3.SS2.p10', 'A3.Ex107.m1',
                   'A3.SS2.p13', 'A3.Ex113.m1', 'A3.Ex114.m1', 'A3.SS2.p14']],
               'scope': 'Actual uncentered matrix squared-moment domination and both actual centered/cosine-weighted variance operator-norm bounds. Z definition is p13, Ex113/114 and comparisons p14. Entire Bernstein p15 excluded.'},
    'producer': {
        'name': 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixVariance.actual_source_truncated_matrix_second_moments',
        'planned_file': str(P), 'signature': producer.decode(), 'signature_sha256': sha(producer),
    },
    'actual_private_consumer': {
        'name': 'AutoSamplingTheory.Tests.GaussianComplexityFixedSpectrumSourceMatrixVariance.actual_source_centered_variance_bounds',
        'planned_file': str(T), 'signature': consumer.decode(), 'signature_sha256': sha(consumer),
        'consumer_edge': 'Use the actual uncentered second moments to prove integrability and genuine operator-norm bounds for the actual centered and cosine-weighted centered second moments on the identical experiment. PSD comparison alone is not this norm conclusion.',
    },
    'binder_audit': [
        {'binder': 'd q : Nat', 'class': 'TYPING', 'meaning': 'Natural physical dimension and query count, including q=0.'},
        {'binder': 'hq : 2*q+1<d', 'class': 'STANDING', 'meaning': 'Exact source range; d>0 and all denominator facts must follow internally.'},
        {'binder': 'all local lets', 'class': 'DEFINITION', 'meaning': 'Literal original experiment, closed cutoff, features, matrices, actual means, centering, weights and explicit bound; no proof/data certificate.'},
    ],
    'output_bundle_audit': {'input_bundle': False,
        'producer': {'all_actual_Y_squared_integrable': 'TARGET_CONCLUSION', 'uncentered_second_moment_PSD_domination': 'TARGET_CONCLUSION'},
        'private_consumer': {'both_actual_centered_squared_variables_integrable': 'TARGET_CONCLUSION', 'both_actual_variance_operator_norm_bounds': 'TARGET_CONCLUSION'}},
    'EXCESS_public_binders': [],
    'proof_components_forbidden_as_extra_binders': [
        'Actual row Gaussian law, independence or measurability certificates',
        'Yi/mean/Z integrability, Hermitian or PSD certificates and centered variance identity',
        'Radial fourth moment, weighted frame/Gram identity or norm-comparison lemma',
        'Supplied first-moment matrices, squared-moment bounds, scalar a bounds or variance estimates',
        'Positive-query restriction, tau/kappa restrictions or arbitrary ambient-law adapter',
    ],
    'shared_floor_audit': {
        'known_canonical_nodes': [
            'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw.actual_source_row_marginal_law',
            'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumRadialFourthMoment.actual_radial_fourth_moment_matrix',
            'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumWeightedFrameBound.actual_weighted_cosine_coefficient_bound',
            'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceMatrixMean.actual_source_truncated_matrix_means'],
        'decision': 'Reuse the compiled canonical source-row, radial-fourth and weighted-frame nodes; no second public canonical-row aggregate. Actual declarations/API applicability and generic variance/PSD norm infrastructure are searched only after seal and source-topology admission. If a missing generic lemma has multiple realistic consumers, name one shared cell before advancing that shared proof; no private route copy.',
        'known_names_checked_from_existing_publication_metadata_without_new_proof_retrieval': True,
        'actual_compiled_parent_edges': 'Pending actual proof and kernel extraction, never inferred from imports.',
    },
    'scope_boundary': 'Same canonical original independent-column Gaussian experiment only; q=0 retained (C=6/d). No arbitrary ambient transfer, bounded-summand radius R*, matrix Bernstein/concentration, full Lemma4.4, either main lower bound or oracle/TV/precision/cap/cost result. Serialized integration, actual browser/site/globalgraphs and purification remain open.',
    'actual_statement_formation': formation, 'actual_definition_meaning': meaning,
    'actual_environment': json.loads((workspace / 'actual-environment-before-seal.json').read_bytes()),
    'actual_environment_receipt': environment_receipt,
    'process_memory_readback': readback, 'preseal_exposure': exposure,
    'formalizer_API_pristine': False, 'new_target_proof_implementation_attempts': 0,
    'minimal_definition_context_sha256': sha(dump(context)),
    'source_preparation_chronology': 'Independent raw source freezes precede first exposure to this packet. No raw note is retroactively recertified as accepted type/graph/topology. Actual formal type/graph review starts after this exact seal.',
}
assert not evidence.exists()
evidence.mkdir()
for name, data in [
    ('minimal-definition-context.json', dump(context)),
    ('actual-definition-meaning.log', meaning_log),
    ('StatementFormation.lean.raw.txt', (workspace / 'StatementFormation.lean').read_bytes()),
    ('DefinitionMeaning.lean.raw.txt', (workspace / 'DefinitionMeaning.lean').read_bytes()),
    ('DefinitionMeaningV2.lean.raw.txt', (workspace / 'DefinitionMeaningV2.lean').read_bytes()),
]:
    create(evidence / name, data)
seal_raw = dump(seal)
seal_path = paper / 'source-matrix-variance-statement-seal.json'
for path in (seal_path, workspace / 'statement-seal-v1.json'):
    create(path, seal_raw)
    path.chmod(0o444)
create(workspace / 'preseal-exposure.json', dump(exposure))
packet = {
    'roles': 'Sealed exact types, binders and literal definition semantics only; no new-target proof or prior-review verdict.',
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
