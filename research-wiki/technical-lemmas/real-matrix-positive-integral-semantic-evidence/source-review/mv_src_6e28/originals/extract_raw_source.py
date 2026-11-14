from html.parser import HTMLParser
from pathlib import Path
import re

SOURCE = Path('.astis/huanjian-resume-20261103/2610.20492v1.html')

class Node:
    def __init__(self, tag, attrs=None, parent=None, start=0):
        self.tag, self.attrs, self.parent, self.start = tag, dict(attrs or []), parent, start
        self.end = start
        self.children = []
    def walk(self):
        yield self
        for x in self.children:
            if isinstance(x, Node):
                yield from x.walk()
    def text(self):
        if self.tag == 'math' and self.attrs.get('alttext'):
            return ' $' + self.attrs['alttext'] + '$ '
        return ''.join(x.text() if isinstance(x, Node) else x for x in self.children)

class Parser(HTMLParser):
    void = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self, data):
        super().__init__(convert_charrefs=True)
        self.data = data
        self.lines = [0]
        self.lines += [m.end() for m in re.finditer('\n', data)]
        self.root = Node('root')
        self.stack = [self.root]
        self.feed(data)
    def pos(self):
        line, col = self.getpos()
        return self.lines[line-1]+col
    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.stack[-1], self.pos())
        self.stack[-1].children.append(n)
        n.end = n.start + len(self.get_starttag_text())
        if tag not in self.void:
            self.stack.append(n)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if self.stack[-1].tag == tag:
            self.stack.pop()
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                end = self.data.find('>', self.pos())+1
                for n in self.stack[i:]:
                    n.end = end
                self.stack = self.stack[:i]
                return
    def handle_data(self, data):
        self.stack[-1].children.append(data)

def load():
    raw = SOURCE.read_bytes().decode('utf-8')
    parser = Parser(raw)
    ids = {n.attrs['id']:n for n in parser.root.walk() if 'id' in n.attrs}
    return raw, parser, ids

def readable(n):
    return re.sub(r'\s+', ' ', n.text()).strip()

if __name__ == '__main__':
    import sys
    raw, parser, ids = load()
    if len(sys.argv)>1:
        for key in sys.argv[1:]:
            n = ids[key]
            print('\nID', key, 'TAG', n.tag, 'CHARS', n.start, n.end)
            print(readable(n))
    else:
        for n in parser.root.walk():
            if n.tag in {'h1','h2','h3','h4','h5','h6'}:
                t=readable(n)
                if 'C.' in t or '4.4' in t or 'Gaussian' in t:
                    print(n.parent.attrs.get('id'), n.attrs.get('id'), t)
