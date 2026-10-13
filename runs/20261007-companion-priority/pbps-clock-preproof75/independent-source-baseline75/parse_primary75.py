from html.parser import HTMLParser
from pathlib import Path
import html,re,json,os,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib')
PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
class Node:
 def __init__(self,tag,attrs,start,startend,parent): self.tag=tag; self.attrs=dict(attrs); self.start=start; self.startend=startend; self.end=startend; self.parent=parent; self.children=[]
 @property
 def id(self): return self.attrs.get('id','')
 def ancestors(self):
  p=self.parent
  while p: yield p; p=p.parent
 def text(self,math=True):
  if self.tag=='math': return ('$'+self.attrs.get('alttext','')+'$') if math else ''
  if self.tag in ('annotation','annotation-xml'): return ''
  return re.sub(r'\s+',' ',' '.join(x.text(math) if isinstance(x,Node) else html.unescape(x) for x in self.children)).strip()
class Parser(HTMLParser):
 def __init__(self,s):
  super().__init__(convert_charrefs=False); self.s=s; self.offsets=[0]; self.nodes=[]; self.stack=[]
  for m in re.finditer('\n',s): self.offsets.append(m.end())
  self.feed(s)
 def off(self): l,c=self.getpos(); return self.offsets[l-1]+c
 def handle_starttag(self,t,a):
  n=Node(t,a,self.off(),self.off()+len(self.get_starttag_text()),self.stack[-1] if self.stack else None); self.nodes.append(n)
  if self.stack: self.stack[-1].children.append(n)
  if t not in ('area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'): self.stack.append(n)
 def handle_startendtag(self,t,a):
  n=Node(t,a,self.off(),self.off()+len(self.get_starttag_text()),self.stack[-1] if self.stack else None); self.nodes.append(n)
  if self.stack:self.stack[-1].children.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i].tag==t:
    e=self.s.find('>',self.off())+1
    for n in self.stack[i:]:n.end=e
    self.stack=self.stack[:i];return
 def handle_data(self,d):
  if self.stack:self.stack[-1].children.append(d)
 def handle_entityref(self,n):self.handle_data('&'+n+';')
 def handle_charref(self,n):self.handle_data('&#'+n+';')
def primary():
 s=PRIMARY.read_text(encoding='utf-8',newline='') if False else PRIMARY.read_bytes().decode('utf-8'); return s,Parser(s)
def main():
 s,p=primary()
 for n in p.nodes:
  if (n.tag=='p' and n.id in ('S1.p1.1','S2.p1.1','S2.SS1.p1.1')) or (n.tag=='math' and n.start< s.index('id="S3"') and ('\\eta' in n.attrs.get('alttext','') and ('\\leq' in n.attrs.get('alttext','') or '>0' in n.attrs.get('alttext','')))):
   print('SUP',n.tag,n.id,n.start,n.end,n.text())
 for lo,hi in [(250262,284344),(533213,575646),(1445364,1448631)]:
  print('\nREGION',lo,hi)
  clo=len(s.encode()[:lo].decode());chi=len(s.encode()[:hi].decode())
  for n in p.nodes:
   if not (n.tag in ('p','h2','h3','h4','figcaption','math') or ('ltx_listingline' in n.attrs.get('class','')) or n.id.startswith('bib.bib')): continue
   if not (clo<=n.start and n.end<=chi): continue
   bo=len(s[:n.start].encode());be=len(s[:n.end].encode())
   if bo>=lo and be<=hi:
    print(n.tag,n.id,bo,be,n.text())
 for n in p.nodes:
  if n.tag=='p' and n.start< s.index('id="S3"') and any(x in n.text() for x in ('Throughout','throughout','\\eta>0','\\eta\\leq','\\eta \\leq')): print('STANDING',n.id,len(s[:n.start].encode()),len(s[:n.end].encode()),n.text())
 print(json.dumps({'actual_PID':os.getpid(),'actual_EXIT':0}))
if __name__=='__main__':main()
