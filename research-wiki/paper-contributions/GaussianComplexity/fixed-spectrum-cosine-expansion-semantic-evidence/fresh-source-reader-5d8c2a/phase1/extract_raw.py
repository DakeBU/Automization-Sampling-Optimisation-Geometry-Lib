from pathlib import Path
from html.parser import HTMLParser
import hashlib
import json
import sys

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
SOURCE = ROOT / '.astis/huanjian-resume-20261103/2610.20492v1.html'
OUT = ROOT / '.astis/semantic-neutral-20261109/src_cosine_5d8c2a/phase1'
raw = SOURCE.read_bytes()
assert len(raw) == 951991
assert hashlib.sha256(raw).hexdigest() == '6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'
source = raw.decode('utf-8')
line_offsets = [0]
for line in source.splitlines(keepends=True):
    line_offsets.append(line_offsets[-1] + len(line))

class Node:
    def __init__(self, tag, attrs, start, parent=None):
        self.tag, self.attrs, self.start, self.parent = tag, dict(attrs), start, parent
        self.end = None
        self.children = []

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('ROOT', [], 0)
        self.root.end = len(source)
        self.stack = [self.root]
        self.ids = {}
    def pos(self):
        line, col = self.getpos()
        return line_offsets[line - 1] + col
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.pos(), self.stack[-1])
        self.stack[-1].children.append(n)
        if n.attrs.get('id'):
            self.ids[n.attrs['id']] = n
        if tag in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}:
            n.end = self.pos() + len(self.get_starttag_text())
        else:
            self.stack.append(n)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack[-1].tag == tag:
            self.stack.pop().end = self.pos() + len(self.get_starttag_text())
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                end = source.find('>', self.pos()) + 1
                for node in self.stack[i:]:
                    node.end = end
                del self.stack[i:]
                return
    def handle_data(self, data):
        self.stack[-1].children.append(data)

p = Parser()
p.feed(source)

def render(n):
    if isinstance(n, str):
        return n
    if n.tag == 'math':
        return '$' + n.attrs.get('alttext', '') + '$'
    if n.tag in {'script', 'style'}:
        return ''
    text = ''.join(render(c) for c in n.children)
    if n.tag in {'section','div','p','table','tbody','tr','h1','h2','h3','h4','h5','h6','li'}:
        text = '\n' + text.strip() + '\n'
    return text

def record(ident):
    n = p.ids[ident]
    assert n.end is not None
    fragment = source[n.start:n.end].encode('utf-8')
    start_byte = len(source[:n.start].encode('utf-8'))
    return {
        'id': ident, 'tag': n.tag,
        'start_byte_inclusive': start_byte,
        'end_byte_exclusive': start_byte + len(fragment),
        'raw_fragment_bytes': len(fragment),
        'raw_fragment_sha256': hashlib.sha256(fragment).hexdigest(),
        'parent_id': n.parent.attrs.get('id'),
    }

if __name__ == '__main__':
    ids = sys.argv[1:]
    for ident in ids:
        n = p.ids[ident]
        print('\n===== ' + ident + ' =====')
        print(json.dumps(record(ident), ensure_ascii=False))
        print(render(n).strip())
