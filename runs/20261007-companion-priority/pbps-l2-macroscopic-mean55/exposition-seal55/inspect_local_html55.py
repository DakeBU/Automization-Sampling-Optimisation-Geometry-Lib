from pathlib import Path
from html.parser import HTMLParser
import re,json,hashlib,datetime,subprocess
root=Path(r'E:\Samplinglib');stage=Path(__file__).parent
path=root/'_site/example-cases/samplewiki/companions/proximal-bouncy-particle.html'
with path.open('rb') as handle:raw=handle.read()
s=raw.decode('utf-8');lines=s.splitlines(keepends=True);offsets=[];n=0
for line in lines:offsets.append(n);n+=len(line)
class Node:
 def __init__(self,tag,attrs,start):self.tag=tag;self.attrs=dict(attrs);self.start=start;self.end=None;self.children=[]
 def text(self):return ''.join(x.text() if isinstance(x,Node) else x for x in self.children)
class Parser(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.stack=[Node('root',[],0)];self.ids={}
 def pos(self):l,c=self.getpos();return offsets[l-1]+c
 def handle_starttag(self,tag,attrs):
  a=Node(tag,attrs,self.pos());self.stack[-1].children.append(a)
  if 'id' in a.attrs:self.ids[a.attrs['id']]=a
  if tag not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(a)
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==tag:
    for a in self.stack[i:]:a.end=s.find('>',self.pos())+1
    self.stack=self.stack[:i];break
 def handle_data(self,data):self.stack[-1].children.append(data)
p=Parser();p.feed(s);p.close()
candidates=[(k,a) for k,a in p.ids.items() if 'pbps-l2-macroscopic-mean' in k]
print('SECTION_IDS',[(k,a.tag,a.end-a.start if a.end else None) for k,a in candidates])
assert candidates
key,section=max(candidates,key=lambda ka:ka[1].end-ka[1].start)
fragment=s[section.start:section.end].encode('utf-8')
with (stage/'actual-native-section55.raw.snapshot.html').open('wb') as handle:handle.write(fragment)
details=[]
def walk(a):
 if a.tag=='details':details.append(a)
 for c in a.children:
  if isinstance(c,Node):walk(c)
walk(section)
proof_file=root/'AutoSamplingTheory/ExampleCases/ProximalBPS/L2MacroscopicMean.lean'
with proof_file.open('rb') as handle:production=handle.read()
text=production.decode('utf-8').replace('\r\n','\n');start=text.index('theorem actual_macroscopic_l2_mean');decl=text[start:].strip()
proof_start=start+re.search(r':=\s*by\b',text[start:]).start();statement=text[start:proof_start].strip();proof=text[proof_start+len(':='):text.rfind('end AutoSamplingTheory')].strip()
folds=[]
for i,a in enumerate(details):
 summaries=[];codes=[]
 def content(b):
  if b.tag=='summary':summaries.append(b.text())
  if b.tag=='code':codes.append(b.text())
  for c in b.children:
   if isinstance(c,Node):content(c)
 content(a)
 code='\n'.join(codes).strip()
 folds.append({'index':i,'summary':summaries,'initially_closed':'open' not in a.attrs,'code_utf8_bytes':len(code.encode('utf-8')),'code_raw_text_sha256':hashlib.sha256(code.encode('utf-8')).hexdigest(),'exact_statement_match':code==statement,'exact_proof_match':code==proof,'exact_whole_declaration_match':code==decl,'whole_declaration_match_recipe':'Exact production source suffix from theorem through final namespace end, CRLF to LF, outer whitespace stripped','statement_terminal_LF_sha256':hashlib.sha256((code+'\n').encode('utf-8')).hexdigest() if code==statement else None})
 if any('Lean statement' in x or 'Lean proof' in x for x in summaries):
  with (stage/('folded-code.'+str(i)+'.actual.snapshot.lean')).open('w',encoding='utf-8',newline='\n') as handle:handle.write(code)
with (stage/'actual-native-dom-checks55.json').open('w',encoding='utf-8',newline='\n') as handle:json.dump({'section_id':key,'physical_path':str(path),'whole_html_raw_bytes':len(raw),'whole_html_raw_sha256':hashlib.sha256(raw).hexdigest(),'section_raw_bytes':len(fragment),'section_raw_sha256':hashlib.sha256(fragment).hexdigest(),'details':folds,'production_raw_bytes':len(production),'production_raw_sha256':hashlib.sha256(production).hexdigest(),'production_lf_sha256':hashlib.sha256(production.replace(b'\r\n',b'\n')).hexdigest(),'rendered_math_capture_status':'Actual PNG+DOM reviewed separately; static nativeHTML contains pre-MJX source.','review_scope':'Exposition/display correspondence; full proof reasoning not re-reviewed.'},handle,indent=2);handle.write('\n')
print(json.dumps({'folds':folds,'production_lines':len(text.splitlines()),'exact_statement_matches':sum(x['exact_statement_match'] for x in folds),'exact_proof_matches':sum(x['exact_proof_match'] for x in folds)}))
