from html.parser import HTMLParser
import re
class Parser(HTMLParser):

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.nodes = []
        self.math = 0

    def handle_starttag(self, tag, attrs):
        at = dict(attrs)
        n = dict(tag=tag, id=at.get('id'), text=[])
        self.stack.append(n)
        if tag == 'math':
            if self.math == 0:
                for q in self.stack:
                    q['text'].append(at.get('alttext', ''))
            self.math += 1
        if tag in {'br', 'hr', 'img', 'meta', 'link', 'input', 'source', 'wbr', 'area', 'base', 'col', 'embed', 'param', 'track'}:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == 'math':
            self.math = max(0, self.math - 1)
        found = next((i for i in range(len(self.stack) - 1, -1, -1) if self.stack[i]['tag'] == tag), None)
        if found is None:
            return
        ended = self.stack[found:]
        self.stack = self.stack[:found]
        for n in ended:
            if n['id']:
                self.nodes.append(dict(id=n['id'], tag=n['tag'], text=re.sub('\\s+', ' ', ' '.join(n['text'])).strip()))

    def handle_data(self, data):
        if not self.math:
            for q in self.stack:
                q['text'].append(data)
