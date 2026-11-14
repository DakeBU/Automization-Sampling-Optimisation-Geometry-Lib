from html.parser import HTMLParser
from pathlib import Path
import re

ROOT = Path('/Users/zhouhuanjian/ASTIS-GC')
SOURCE = ROOT / '.astis/huanjian-resume-20261103/2610.20492v1.html'
RAW = SOURCE.read_text()
LINES = RAW.splitlines(keepends=True)
OFFSETS = [0]
for line in LINES:
    OFFSETS.append(OFFSETS[-1] + len(line))

class Node:
    def __init__(self, tag, attrs, start=0):
        self.tag, self.attrs, self.start = tag, dict(attrs), start
        self.end, self.children = start, []

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('root', [])
        self.stack, self.ids = [self.root], {}
    def pos(self):
        line, col = self.getpos()
        return OFFSETS[line - 1] + col
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.pos())
        self.stack[-1].children.append(n)
        if 'id' in n.attrs:
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
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                end = RAW.find('>', self.pos()) + 1
                for n in self.stack[i:]:
                    n.end = end
                del self.stack[i:]
                break
    def handle_data(self, data):
        self.stack[-1].children.append(data)

PARSER = Parser()
PARSER.feed(RAW)

def plain(n):
    if isinstance(n, str):
        return n
    if n.tag == 'math':
        return '$' + n.attrs.get('alttext', '') + '$'
    if n.tag in {'script', 'style', 'annotation'}:
        return ''
    return ''.join(plain(c) for c in n.children)

def blocks(n):
    if n.tag in {'p', 'table', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
        ident = n.attrs.get('id', '(heading)')
        return f'[{ident}] ' + re.sub(r'\s+', ' ', plain(n)).strip() + '\n\n'
    return ''.join(blocks(c) for c in n.children if isinstance(c, Node))

if __name__ == '__main__':
    import sys
    for ident in sys.argv[1:]:
        n = PARSER.ids[ident]
        print('===== ' + ident + ' =====')
        print(blocks(n))
