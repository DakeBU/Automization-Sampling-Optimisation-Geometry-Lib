from pathlib import Path
from html.parser import HTMLParser
import json

SOURCE=Path('.astis/huanjian-resume-20261103/2610.20492v1.html')
RAW=SOURCE.read_bytes()
TEXT=RAW.decode('utf-8')
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class NodeParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.nodes={}; self.lines=[0]
        for i,c in enumerate(TEXT):
            if c=='\n': self.lines.append(i+1)
    def pos(self):
        line,col=self.getpos(); return self.lines[line-1]+col
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        node={'tag':tag,'id':attrs.get('id'),'start':self.pos(),'attrs':attrs,'children':[]}
        if self.stack: self.stack[-1]['children'].append(node)
        if node['id']: self.nodes[node['id']]=node
        if tag in VOID: node['end']=self.pos()+len(self.get_starttag_text())
        else: self.stack.append(node)
    def handle_endtag(self,tag):
        if self.stack and self.stack[-1]['tag']==tag:
            self.stack[-1]['end']=self.pos()+len(tag)+3; self.stack.pop()
class TextParser(HTMLParser):
    def __init__(self): super().__init__(); self.parts=[]; self.math=0
    def handle_starttag(self,tag,attrs):
        if tag=='math': self.parts.append('$'+dict(attrs).get('alttext','')+'$'); self.math+=1
        elif tag in {'div','p','table','h1','h2','h3','h4','h5','h6','tr'} and not self.math: self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag=='math': self.math-=1
        elif tag in {'div','p','table','h1','h2','h3','h4','h5','h6','tr'} and not self.math: self.parts.append('\n')
    def handle_data(self,data):
        if not self.math: self.parts.append(data)

def text_of(raw):
    p=TextParser(); p.feed(raw); return '\n'.join(x.strip() for x in ''.join(p.parts).splitlines() if x.strip())
P=NodeParser(); P.feed(TEXT)
def exact(anchor):
    n=P.nodes[anchor]; return TEXT[n['start']:n['end']]
if __name__=='__main__':
    import sys
    for anchor in sys.argv[1:]:
        n=P.nodes[anchor]
        print('ANCHOR',anchor,'CHARSPAN',n['start'],n.get('end'))
        print(text_of(exact(anchor)))
