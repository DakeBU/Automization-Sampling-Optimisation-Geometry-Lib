"""Independent local source/coverage comparison; no proof or implementation input."""
from pathlib import Path
from html.parser import HTMLParser
from hashlib import sha256
import json
from bs4 import BeautifulSoup

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
BASE = ROOT / 'research-wiki/paper-contributions/GaussianComplexity/fixed-spectrum-geometry-semantic-evidence'
SOURCE = ROOT / '.astis/huanjian-resume-20261103/2610.20492v1.html'
raw = SOURCE.read_bytes()
assert sha256(raw).hexdigest() == '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
source = raw.decode()
line_offsets = [0]
for line in source.splitlines(keepends=True):
    line_offsets.append(line_offsets[-1] + len(line))


class Spans(HTMLParser):
    void = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}

    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.ids = {}
        self.links = {}

    def charpos(self):
        line, col = self.getpos()
        return line_offsets[line-1] + col

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        begin = self.charpos()
        if tag not in self.void:
            self.stack.append((tag, attrs, begin))

    def handle_startendtag(self, tag, attrs):
        return

    def handle_endtag(self, tag):
        match = next((i for i in range(len(self.stack)-1, -1, -1) if self.stack[i][0] == tag), None)
        if match is None:
            return
        _, attrs, begin = self.stack[match]
        del self.stack[match:]
        end = self.charpos() + len('</' + tag + '>')
        if attrs.get('id'):
            self.ids[attrs['id']] = (begin, end)
        if tag == 'a':
            self.links[begin] = (begin, end)


p = Spans()
p.feed(source)
coverage_path = BASE / 'source-only-review/phase1/source-coverage.json'
coverage = json.loads(coverage_path.read_text())
records = []
failures = []
for item in coverage['paragraph_and_display_inventory']:
    ident = item['anchor']
    span = p.ids.get(ident)
    assert span is not None, ident
    original = source[slice(*span)]
    computed = sha256(original.encode()).hexdigest()
    row = {'kind': 'unit', 'id': ident, 'raw_hash_matches': computed == item['raw_sha256'], 'disposition': item['disposition']}
    records.append(row)
    if not row['raw_hash_matches']:
        failures.append({'record': row, 'expected': item['raw_sha256'], 'actual': computed})

for atom in coverage['formula_and_citation_inventory']:
    ident = atom['atom_id']
    span = p.links.get(int(ident.split('@')[1])) if atom['kind'] == 'a' else p.ids.get(ident)
    assert span is not None, ident
    original = source[slice(*span)]
    computed = sha256(original.encode()).hexdigest()
    e = BeautifulSoup(original, 'html.parser').find(atom['kind'])
    text = e.get('alttext') if atom['kind'] == 'math' else e.get_text(' ', strip=True)
    row = {'kind': 'atom', 'id': ident, 'raw_hash_matches': computed == atom['raw_sha256'], 'text_matches': text == atom['text'], 'disposition': atom['disposition']}
    records.append(row)
    if not row['raw_hash_matches'] or not row['text_matches']:
        failures.append({'record': row, 'expected': atom['raw_sha256'], 'actual': computed, 'actual_text': text})

# Reconstruct coverage membership independently from the source-region DOMs.
soup = BeautifulSoup(raw, 'html.parser')
regions = ['S2','S4.SS1','S4.Thmtheorem6','A3.SS4','S4.SS2.SSS0.Px4.p1.1','S4.Thmtheorem1','bib.bib3']
expected_math_ids = {m['id'] for region in regions for m in soup.find(id=region).find_all('math', id=True)}
recorded_math_ids = {a['atom_id'] for a in coverage['formula_and_citation_inventory'] if a['kind'] == 'math'}
missing_math_ids = sorted(expected_math_ids-recorded_math_ids)
extra_math_ids = sorted(recorded_math_ids-expected_math_ids)
expected_units = set()
for region in regions:
    elem = soup.find(id=region)
    for candidate in [elem, *elem.find_all(id=True)]:
        cls = candidate.get('class', [])
        if candidate.get('id') and (candidate.name == 'p' and 'ltx_p' in cls or
                                   candidate.name == 'div' and 'ltx_theorem' in cls or
                                   candidate.name == 'table' and 'ltx_equation' in cls or
                                   candidate.get('id') == 'bib.bib3'):
            expected_units.add(candidate['id'])
recorded_units = {item['anchor'] for item in coverage['paragraph_and_display_inventory']}
expected_links = {f'link@{begin}' for begin, end in p.links.values()
                  if any(p.ids[region][0] <= begin and end <= p.ids[region][1] for region in regions)}
recorded_links = {a['atom_id'] for a in coverage['formula_and_citation_inventory'] if a['kind'] == 'a'}
out = {
    'purpose': 'Independent exact raw source matching and mathematical-formula membership only; does not certify topology by counts.',
    'source_sha256': sha256(raw).hexdigest(),
    'coverage_sha256': sha256(coverage_path.read_bytes()).hexdigest(),
    'unit_records': len(coverage['paragraph_and_display_inventory']),
    'atom_records': len(coverage['formula_and_citation_inventory']),
    'raw_match_failures': failures,
    'missing_math_ids': missing_math_ids,
    'extra_math_ids': extra_math_ids,
    'missing_unit_ids': sorted(expected_units-recorded_units),
    'extra_unit_ids': sorted(recorded_units-expected_units),
    'missing_link_ids': sorted(expected_links-recorded_links),
    'extra_link_ids': sorted(recorded_links-expected_links),
    'records': records,
}
out_path = BASE / 'topology-challenge/phase2/raw-source-comparison.json'
out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k:v for k,v in out.items() if k != 'records'}, ensure_ascii=False, indent=2))
print('RESULT_SHA256', sha256(out_path.read_bytes()).hexdigest())
