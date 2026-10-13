"""Small deterministic DOM test double for exact inventory/open assertions.

Not a browser, layout engine, CSS general implementation or click visibility test.
Supports only the selectors used by the reviewed companion loop. HTML fixtures
are parsed, descendant code nodes deduplicated, and summary toggles its parent.
"""
from html.parser import HTMLParser
class Node:
 def __init__(self,tag='',attrs=(),parent=None):self.tag=tag;self.attrs=dict(attrs);self.parent=parent;self.children=[]
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.root=Node();self.stack=[self.root]
 def handle_starttag(self,tag,attrs):
  n=Node(tag,attrs,self.stack[-1]);self.stack[-1].children.append(n)
  if tag not in {'meta','link','img','input','br','hr'}:self.stack.append(n)
 def handle_endtag(self,tag):
  assert self.stack[-1].tag==tag;self.stack.pop()
def walk(n):
 for c in n.children:yield c;yield from walk(c)
def proof(n):return n.tag=='details' and 'inline-lean-proof' in n.attrs.get('class','').split()
def statement(n):return n.tag=='details' and 'inline-lean-statement' in n.attrs.get('class','').split()
class Locator:
 def __init__(self,nodes):self.nodes=nodes
 def count(self):return len(self.nodes)
 def evaluate_all(self,js):
  assert "getAttribute('data-inline-lean')" in js
  return [n.attrs.get('data-inline-lean') for n in self.nodes]
 def all(self):return [Locator([n]) for n in self.nodes]
 @property
 def last(self):return Locator(self.nodes[-1:])
 def click(self):
  assert len(self.nodes)==1 and self.nodes[0].tag=='summary';p=self.nodes[0].parent;assert p.tag=='details'
  if self.nodes[0].attrs.get('onclick')=='event.preventDefault()':return
  if 'open' in p.attrs:del p.attrs['open']
  else:p.attrs['open']=''
 def scroll_into_view_if_needed(self):pass
class Page:
 def set_content(self,content,**kwargs):p=Parser();p.feed(content);p.close();self.root=p.root
 def locator(self,css):
  nodes=list(walk(self.root))
  if css=='[data-authored-declaration]':out=[n for n in nodes if 'data-authored-declaration' in n.attrs]
  elif css=='details.inline-lean-statement':out=[n for n in nodes if statement(n)]
  elif css=='details.inline-lean-statement:not([open])':out=[n for n in nodes if statement(n) and 'open' not in n.attrs]
  elif css=='details.inline-lean-proof':out=[n for n in nodes if proof(n)]
  elif css=='details.inline-lean-proof:not([open])':out=[n for n in nodes if proof(n) and 'open' not in n.attrs]
  elif css=='details.inline-lean-proof[open]':out=[n for n in nodes if proof(n) and 'open' in n.attrs]
  elif css=='details.inline-lean-proof > summary':out=[n for n in nodes if n.tag=='summary' and proof(n.parent)]
  elif css=='details.inline-lean-proof[open] code.language-lean':
   out=[]
   for n in nodes:
    if n.tag!='code' or 'language-lean' not in n.attrs.get('class','').split():continue
    p=n.parent
    while p:
     if proof(p) and 'open' in p.attrs:out.append(n);break
     p=p.parent
  else:raise AssertionError('Unsupported selector in bounded test double: '+css)
  return Locator(out)
 def evaluate(self,js):
  assert js=='document.documentElement.scrollWidth > innerWidth + 1'
  return False # Layout is deliberately outside this deterministic fixture test.
 def screenshot(self,**kwargs):pass # No screenshot/visual evidence is manufactured.
