from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,sys
ROOT=Path(__file__).parent
class Parser(HTMLParser):
 def __init__(self): super().__init__();self.stack=[];self.nodes=[];self.offsets=[]
 def handle_starttag(self,t,a):
  n={'tag':t,'attrs':dict(a),'children':[],'start':self.offsets[self.getpos()[0]-1]+self.getpos()[1]}
  if self.stack:self.stack[-1]['children'].append(n)
  self.nodes.append(n)
  if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i]['tag']==t:
    n=self.stack[i];n['end']=self.offsets[self.getpos()[0]-1]+self.getpos()[1]+len('</'+t+'>');self.stack=self.stack[:i];break
 def handle_data(self,s):
  if self.stack:self.stack[-1]['children'].append(s)
def txt(n):
 if isinstance(n,str):return n
 if n['tag']=='math':return n['attrs'].get('alttext','[math-no-alt]')
 return ' '.join(txt(c) for c in n['children'])
b=(ROOT/'primary-pbps.raw.snapshot.html').read_bytes();s=b.decode('utf-8');p=Parser();position=0
for line in s.splitlines(keepends=True):p.offsets.append(position);position+=len(line)
p.feed(s)
if sys.argv[1]=='index':
 for n in p.nodes:
  if n['tag'] in ['section'] or n['attrs'].get('class','').startswith('ltx_theorem'):
   print(n['attrs'].get('id',''),txt(n)[:150].replace('\n',' '))
else:
 for ident in sys.argv[1:]:
  ns=[n for n in p.nodes if n['attrs'].get('id')==ident];assert len(ns)==1,(ident,len(ns));n=ns[0]
  raw=s[n['start']:n['end']].encode('utf-8');path=ROOT/(ident+'.raw.html');path.write_bytes(raw)
  out=' '.join(txt(n).split());(ROOT/(ident+'.text.txt')).write_text(out,encoding='utf-8',newline='\n')
  print(ident,out)