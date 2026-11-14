from pathlib import Path
from html.parser import HTMLParser
import hashlib
import html
import json
import re

REPO = Path('/Users/zhouhuanjian/ASTIS-GC')
OUT = REPO / '.astis/semantic-neutral-20261112/ri_src_5ab9'
SOURCE = REPO / '.astis/huanjian-resume-20261103/2610.20492v1.html'
b = SOURCE.read_bytes()
s = b.decode('utf-8')
assert hashlib.sha256(b).hexdigest() == '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
line_starts = [0] + [m.end() for m in re.finditer('\n', s)]

class Elements(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.stack = []
        self.found = {}
    def pos(self):
        line, col = self.getpos()
        return line_starts[line - 1] + col
    def handle_starttag(self, tag, attrs):
        start = self.pos()
        ident = dict(attrs).get('id')
        if tag in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            if ident:
                self.found[ident] = (start, start + len(self.get_starttag_text()))
            return
        self.stack.append((tag, ident, start))
    def handle_endtag(self, tag):
        pos = self.pos()
        end = s.index('>', pos) + 1
        for j in range(len(self.stack) - 1, -1, -1):
            if self.stack[j][0] == tag:
                closing = self.stack[j:]
                self.stack = self.stack[:j]
                for _, ident, start in closing:
                    if ident:
                        self.found[ident] = (start, end)
                return

parser = Elements()
parser.feed(s)
ids = ['S4.Thmtheorem4', 'S4.Thmtheorem4.p1.1', 'S4.E11',
       'A3.SS2.p1', 'A3.Ex85', 'A3.SS2.p1.2', 'A3.SS2.p4.m2',
       'A3.SS2.p10.m1', 'A3.SS2.p10.m2', 'A3.SS2.p12.1', 'A3.Ex107']

def readable(raw):
    maths = []
    def protect(m):
        maths.append(html.unescape(re.search(r'alttext="([^"]*)"', m[1])[1]))
        return ' MATHPLACEHOLDER' + str(len(maths)-1) + 'END '
    raw = re.sub(r'<math\b([^>]*)>.*?</math>', protect, raw, flags=re.S)
    raw = re.sub(r'<[^>]+>', ' ', raw)
    raw = html.unescape(raw)
    for index, math in enumerate(maths):
        raw = raw.replace('MATHPLACEHOLDER' + str(index) + 'END', '$' + math + '$')
    return re.sub(r'\s+', ' ', raw).strip()

def loc(a, z):
    start_line = s.count('\n', 0, a) + 1
    end_line = s.count('\n', 0, z - 1) + 1
    return {'utf8_byte_start_0': len(s[:a].encode('utf-8')),
            'utf8_byte_end_exclusive_0': len(s[:z].encode('utf-8')),
            'unicode_char_start_0': a, 'unicode_char_end_exclusive_0': z,
            'lf_line_start_1': start_line, 'lf_column_start_0': a-line_starts[start_line-1],
            'lf_line_end_inclusive_1': end_line,
            'lf_column_end_exclusive_0': z-line_starts[end_line-1]}

items = []
for ident in ids:
    a, z = parser.found[ident]
    raw = s[a:z]
    name = 'raw_' + ident.replace('.', '_') + '.html'
    (OUT / name).write_bytes(raw.encode('utf-8'))
    item = {'id': ident, 'raw_extract_file': name, **loc(a,z),
            'raw_extract_sha256': hashlib.sha256(raw.encode('utf-8')).hexdigest(),
            'readable_source_text': readable(raw)}
    items.append(item)

record = {'source_path': str(SOURCE.relative_to(REPO)), 'source_sha256': hashlib.sha256(b).hexdigest(),
          'source_utf8_bytes':len(b), 'source_unicode_chars':len(s), 'source_lf_count':s.count('\n'),
          'locator_convention':'Raw original UTF-8 bytes, Unicode code points, and LF-delimited lines. Byte and character intervals are zero-based half-open; line numbers are one-based, columns zero-based. No newline normalization.',
          'items':items}
(OUT / 'source_locators.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
for item in items:
    print(json.dumps(item, ensure_ascii=False))
