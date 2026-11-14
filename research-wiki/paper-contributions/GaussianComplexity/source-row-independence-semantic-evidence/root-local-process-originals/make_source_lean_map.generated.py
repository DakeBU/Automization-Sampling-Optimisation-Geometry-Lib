"""Locate source formulas and the exact compiled proof and statement spans."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json

evidence = Path('research-wiki/paper-contributions/GaussianComplexity/source-row-independence-semantic-evidence')
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




P = Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceRowIndependence.lean')
T = Path('Tests/GaussianComplexityFixedSpectrumSourceRowIndependence.lean')


def code_span(path, first, last):
    data = path.read_bytes()
    lines = data.splitlines(keepends=True)
    assert 1 <= first <= last <= len(lines)
    before, body = b''.join(lines[:first-1]), b''.join(lines[first-1:last])
    return {'path': str(path), 'file_sha256': sha(data), 'LF_lines_1based': [first, last],
            'raw_UTF8_byte_span': [len(before), len(before)+len(body)],
            'decoded_char_span': [len(before.decode()), len(before.decode())+len(body.decode())],
            'span_sha256': sha(body)}


def mapping(ids, ranges, meaning):
    return {'source': [source_span(i) for i in ids],
            'lean': [code_span(*r) for r in ranges], 'meaning': meaning}


mappings = [
    mapping(['S4.Thmtheorem4.p1'], [(P, 12, 20), (T, 11, 32)],
            'Exact natural source range2q+1<d, r=q+1, q0 retained. Only canonical definitions and source standing inputs.'),
    mapping(['A3.SS2.p1'], [(P, 14, 19), (P, 21, 57)],
            'Actual same-product coordinate rows. Full physical scalar-coordinate product law follows from the canonical Gaussian product-image equality, internally rather than a new certificate.'),
    mapping(['A3.SS2.p1'], [(P, 59, 86)],
            'Omitted source bridge expanded as full scalar-array flatten/permutation/regroup and Euclidean row wrapping. Exact joint pushforward, no resampling or marginal-only shortcut.'),
    mapping(['A3.SS2.p1'], [(P, 36, 37), (P, 88, 96)],
            'Same compiled canonical row-law node supplies measurable marginal laws; genuine joint product law gives full iIndepFun, not only pairwise independence.'),
    mapping(['S4.E11.m1', 'A3.Ex85.m1', 'A3.SS2.p10.m1', 'A3.SS2.p10.m2'],
            [(T, 19, 24), (T, 42, 47)],
            'Exact half-grid/cosine features and closed radius cutoff2r+3log(1000d), with sourceindex i.val+1 and constant feature one.'),
    mapping(['A3.SS2.p12.1', 'A3.Ex107.m1'], [(T, 25, 32), (T, 48, 59)],
            'Actual Ex107 Yi equals its own fixed row image Fi(rowi) on the identical Omega/mu; inverse-d Gaussian-first matrix tensor and local closed cutoff. Producer and canonical row-law calls are material.'),
    mapping(['A3.SS2.p12.1', 'A3.Ex107.m1'], [(T, 61, 81)],
            'Source-implicit measurability is proved via exact finite entry polynomials and a measurable closed piecewise event. Separate measurable Fi images preserve full independence, with no injectivity or iid claim.'),
]
record = {
    'kind': 'Root-authored exact source/Lean map for independent review',
    'source_sha256': sha(raw),
    'actual_ASTIS_proof_parents': json.loads((evidence / 'publication-draft-record.json').read_bytes())['actual_public_ASTIS_parents'],
    'mappings': mappings,
    'proof_background': [
        {'declaration': 'AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumSourceRowLaw.actual_source_row_marginal_law',
         'source': code_span(Path('AutoSamplingTheory/ExampleCases/GaussianComplexity/FixedSpectrumSourceRowLaw.lean'), 13, 21),
         'consumer': [code_span(P, 36, 37), code_span(P, 88, 96), code_span(T, 56, 57), code_span(T, 76, 79)],
         'meaning': 'The same canonical compiled node supplies row measurability and marginal law wherever actually used.'},
        {'declaration': 'ProbabilityTheory.map_pi_eq_stdGaussian',
         'source': code_span(Path('.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean'), 137, 142),
         'consumer': [code_span(P, 40, 57), code_span(P, 78, 86)],
         'meaning': 'Exact full joint physical-coordinate Gaussian product identification and row wrapping, including unit covariance.'},
        {'declaration': 'MeasureTheory.Measure.infinitePi_eq_pi and finite specialization of curry maps',
         'source': [code_span(Path('.lake/packages/mathlib/Mathlib/Probability/ProductMeasure.lean'), 512, 516),
                    code_span(Path('.lake/packages/mathlib/Mathlib/Probability/ProductMeasure.lean'), 548, 563)],
         'consumer': code_span(P, 60, 77),
         'meaning': 'Finite probability products are exactly the infinite product construction on finite carriers; flatten and regroup have exact map laws.'},
        {'declaration': 'MeasureTheory.measurePreserving_piCongrLeft',
         'source': code_span(Path('.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/Pi.lean'), 732, 739),
         'consumer': code_span(P, 66, 77), 'meaning': 'Exchange the two finite index factors while retaining every scalar factor law.'},
        {'declaration': 'ProbabilityTheory.iIndepFun_iff_map_fun_eq_pi_map',
         'source': code_span(Path('.lake/packages/mathlib/Mathlib/Probability/Independence/Basic.lean'), 860, 878),
         'consumer': code_span(P, 88, 96), 'meaning': 'Full finite-family independence from actual joint product map and actual measurable marginal maps.'},
        {'declaration': 'ProbabilityTheory.iIndepFun.comp',
         'source': code_span(Path('.lake/packages/mathlib/Mathlib/Probability/Independence/Basic.lean'), 670, 673),
         'consumer': code_span(T, 61, 79), 'meaning': 'Arbitrary separate measurable images preserve full family independence; no injectivity or common-image constraint.'},
    ],
    'mathlib_pin': 'db584cd6d46c92f209a44c0f1c829460d327499d',
    'scope': 'Canonical original-column row joint independence and actual measurable independent Ex107 Yi. Ambient transfer, moments/centered variance/concentration, mainbounds and integrated reader remain open.',
}
path = evidence / 'source-lean-map.draft.json'
with path.open('x') as out:
    json.dump(record, out, ensure_ascii=False, indent=2)
    out.write(chr(10))
print(json.dumps({'path': str(path), 'sha256': sha(path.read_bytes()),
                  'source_locator_entries': sum(len(m['source']) for m in mappings),
                  'Lean_spans': sum(len(m['lean']) for m in mappings)}))
