"""Locate source formulas and the exact compiled proof and statement spans."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json

evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-row-law-semantic-evidence')
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



P = Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceRowLaw.lean')
T = Path('Tests/GaussianComplexityFixedSpectrumSourceRowLaw.lean')


def code_span(path, first, last):
    raw_code = path.read_bytes()
    lines = raw_code.splitlines(keepends=True)
    assert 1 <= first <= last <= len(lines)
    prefix, body = b''.join(lines[:first - 1]), b''.join(lines[first - 1:last])
    return {'path': str(path), 'file_sha256': sha(raw_code),
            'LF_lines_1based': [first, last],
            'raw_UTF8_byte_span': [len(prefix), len(prefix) + len(body)],
            'decoded_char_span': [len(prefix.decode()), len(prefix.decode()) + len(body.decode())],
            'span_sha256': sha(body)}


def mapping(identifiers, ranges, meaning):
    return {'source': [source_span(x) for x in identifiers],
            'lean': [code_span(*entry) for entry in ranges], 'meaning': meaning}


mappings = [
    mapping(['S4.Thmtheorem3.p1', 'S4.Thmtheorem4.p1'],
            [(P, 13, 21), (T, 14, 25)],
            'Standing natural d,q and exact 2q+1<d; includes q=0. No tau/kappa or moment estimate is an added binder.'),
    mapping(['A3.SS2.p1'], [(P, 15, 21), (P, 22, 42)],
            'Literal independent-column product realization and one physical-coordinate Gaussian marginal. Source p1 joint-row independence is explicitly excluded from this marginal obligation.'),
    mapping(['A3.SS2.p1'], [(P, 43, 52)],
            'Collect each coordinate across independent columns and wrap the row in Euclidean space. Both measurable and Gaussian map_eq are outputs.'),
    mapping(['A3.SS2.p1', 'A3.SS2.p10'], [(T, 14, 25), (T, 26, 53)],
            'Same concrete outcome space/product law and literal row radius; exact source closed cutoff with log(1000d). No arbitrary extended ambient-law transfer is claimed.'),
    mapping(['A3.Ex104.m1'], [(T, 48, 65)],
            'The existing canonical exponential node supplies integrability and the exact moment. General noninjective integral_map transports the mean to the actual row on the same original experiment.'),
    mapping(['A3.Ex105.m1'], [(T, 67, 85), (T, 87, 109)],
            'Source exponential Markov bound specialized to log(1000d), with actual transported integrability, exact moment, log3 calibration and strict bad-row event.'),
    mapping(['A3.SS2.p10'], [(T, 111, 145)],
            'Source prints the simultaneous good probability>=0.999. Finite-union expansion is explicitly source-supported inference, not claimed verbatim. Measurable closed-event complement and exact ENNReal999/1000 normalization are internal.'),
]
draft = json.loads((evidence / 'publication-draft-record.json').read_bytes())
record = {
    'kind': 'Root-authored exact source/Lean map for independent review',
    'source_sha256': sha(raw),
    'actual_ASTIS_proof_parents': draft['actual_public_ASTIS_parents'],
    'mappings': mappings,
    'proof_background': [
        {'declaration': 'ProbabilityTheory.map_pi_eq_stdGaussian',
         'source': code_span(Path('.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean'), 137, 142),
         'consumer': code_span(P, 29, 32), 'meaning': 'The standard Euclidean Gaussian is the Euclidean image of the scalar Gaussian product.'},
        {'declaration': 'MeasureTheory.measurePreserving_eval',
         'source': code_span(Path('.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/Pi.lean'), 402, 408),
         'consumer': code_span(P, 33, 42), 'meaning': 'Each evaluation under a probability product has its corresponding factor law.'},
        {'declaration': 'MeasureTheory.measurePreserving_pi',
         'source': code_span(Path('.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/Pi.lean'), 908, 917),
         'consumer': code_span(P, 43, 52), 'meaning': 'Finite product of measure-preserving component maps, then Euclidean wrapping.'},
        {'declaration': 'AutoSamplingTheory.TechnicalLemmas.Probability.StdGaussianRadialExponential.integrable_exp_norm_sq_div_three_and_integral_stdGaussian',
         'source': code_span(Path('AutoSamplingTheory/TechnicalLemmas/Probability/StdGaussianRadialExponential.lean'), 21, 29),
         'consumer': code_span(T, 48, 65), 'meaning': 'One existing compiled canonical node supplies both genuine integrability and exact exponential moment.'},
        {'declaration': 'MeasureTheory.MeasurePreserving.integrable_comp_of_integrable',
         'source': code_span(Path('.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean'), 388, 394),
         'consumer': code_span(T, 55, 59), 'meaning': 'Integrability transports through a measure-preserving map without an injectivity premise.'},
        {'declaration': 'MeasureTheory.integral_map',
         'source': code_span(Path('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Bochner/Basic.lean'), 1043, 1051),
         'consumer': code_span(T, 59, 65), 'meaning': 'General measurable pushforward integral, with explicit target AEStronglyMeasurable evidence; no embedding restriction.'},
        {'declaration': 'MeasureTheory.meas_ge_le_lintegral_div',
         'source': code_span(Path('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Markov.lean'), 104, 110),
         'consumer': code_span(T, 87, 109), 'meaning': 'Nonnegative exponential Markov on the original product probability space.'},
    ],
    'mathlib_pin': 'db584cd6d46c92f209a44c0f1c829460d327499d',
    'scope': 'Canonical independent-column experiment, each marginal row and actual simultaneous cutoff consumer. Joint-row independence, arbitrary ambient-law transfer, original matrix expectations, centered variance/concentration/main bounds and integrated reader remain open.',
}
path = evidence / 'source-lean-map.draft.json'
with path.open('x') as out:
    json.dump(record, out, ensure_ascii=False, indent=2)
    out.write(chr(10))
print(json.dumps({'path': str(path), 'sha256': sha(path.read_bytes()),
                  'source_locator_entries': sum(len(m['source']) for m in mappings),
                  'Lean_spans': sum(len(m['lean']) for m in mappings)}))
