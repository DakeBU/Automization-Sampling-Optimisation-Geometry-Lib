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

