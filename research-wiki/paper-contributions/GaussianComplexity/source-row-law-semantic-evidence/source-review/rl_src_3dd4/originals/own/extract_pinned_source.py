from html.parser import HTMLParser
from pathlib import Path
import hashlib
import json
import re

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
OUT = ROOT / '.astis/semantic-neutral-20261112/rl_src_3dd4'
SOURCE = ROOT / '.astis/huanjian-resume-20261103/2610.20492v1.html'
EXPECTED_SIZE = 951991
EXPECTED_SHA = '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
raw_bytes = SOURCE.read_bytes()
assert len(raw_bytes) == EXPECTED_SIZE
assert hashlib.sha256(raw_bytes).hexdigest() == EXPECTED_SHA
raw = raw_bytes.decode('utf-8')
line_starts = [0]
for match in re.finditer('\n', raw):
    line_starts.append(match.end())

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.nodes = {}
    def handle_starttag(self, tag, attrs):
        line, column = self.getpos()
        node = {'tag': tag, 'attrs': dict(attrs), 'children': [],
                'start': line_starts[line - 1] + column, 'start_line': line}
        if self.stack:
            self.stack[-1]['children'].append(node)
        if node['attrs'].get('id'):
            self.nodes[node['attrs']['id']] = node
        if tag not in {'meta','link','img','br','hr','input','source','area','base','embed','param','track','wbr'}:
            self.stack.append(node)
    def handle_endtag(self, tag):
        line, column = self.getpos()
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index]['tag'] == tag:
                node = self.stack[index]
                node['end'] = raw.find('>', line_starts[line - 1] + column) + 1
                node['end_line'] = line
                self.stack = self.stack[:index]
                break
    def handle_data(self, data):
        if self.stack:
            self.stack[-1]['children'].append(data)

def render(node):
    if isinstance(node, str):
        return node
    if node['tag'] == 'math':
        return '$' + node['attrs'].get('alttext', '[math]') + '$'
    return ''.join(render(child) for child in node['children'])

parser = Parser()
parser.feed(raw)
regions = []
# Only bounded source supports of the assigned row-law/cutoff fragment.
for identity, role in [
    ('S4.SS1.p1', 'Standing integer dimension, source construction context; broader spectral/Haar context excluded from target'),
    ('S4.Thmtheorem3', 'Corroborating integer q range and independent original Gaussian columns'),
    ('S4.Thmtheorem4', 'Primary standing original column experiment and q/d range; full uniform-Krylov conclusion excluded'),
    ('A3.SS2.p1', 'Assigned row definition and row-independence assertion; tensor-row dimension context'),
    ('A3.SS2.p9', 'Nearby concentration motivation only; excluded from target'),
    ('A3.SS2.p10', 'Assigned original-experiment cutoff, strict tail, closed all-good event and printed probability'),
]:
    node = parser.nodes[identity]
    fragment = raw[node['start']:node['end']]
    filename = 'source_' + identity.replace('.', '_') + '.html'
    (OUT / filename).write_text(fragment, encoding='utf-8')
    text = re.sub(r'\s+', ' ', render(node)).strip()
    regions.append({
        'id': identity, 'role': role, 'source_path': str(SOURCE.relative_to(ROOT)),
        'source_sha256': EXPECTED_SHA, 'start_line': node['start_line'], 'end_line': node['end_line'],
        'byte_start_0based': len(raw[:node['start']].encode('utf-8')),
        'byte_end_exclusive_0based': len(raw[:node['end']].encode('utf-8')),
        'source_fragment_file': filename,
        'source_fragment_sha256': hashlib.sha256(fragment.encode('utf-8')).hexdigest(),
        'extracted_display_math_uses': 'source math alttext verbatim; surrounding whitespace normalized only',
        'text': text,
    })
(OUT / 'source_locators.json').write_text(json.dumps({
    'source_title': 'On Complexity of Gaussian Sampling',
    'source_revision': 'arXiv:2610.20492v1',
    'source_size_bytes': EXPECTED_SIZE, 'source_sha256': EXPECTED_SHA,
    'scope': 'Appendix C.2 p1 original Gaussian physical rows and p10 cutoff event, necessary standing support only',
    'regions': regions,
}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
(OUT / 'source_extracts.txt').write_text('\n\n'.join(
    item['id'] + ' (lines ' + str(item['start_line']) + '-' + str(item['end_line']) + ')\n' + item['text']
    for item in regions
) + '\n', encoding='utf-8')
print(json.dumps([{'id': item['id'], 'lines': [item['start_line'],item['end_line']], 'sha256': item['source_fragment_sha256']} for item in regions], indent=2))
