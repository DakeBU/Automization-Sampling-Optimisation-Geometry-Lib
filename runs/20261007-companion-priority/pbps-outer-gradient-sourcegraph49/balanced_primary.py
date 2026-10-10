# -*- coding: utf-8 -*-
import pathlib,json,hashlib,sys,html,re
from html.parser import HTMLParser
sys.stdout.reconfigure(encoding='utf-8');r=pathlib.Path('E:/Samplinglib');d=r/'runs/20261007-companion-priority/pbps-outer-gradient-sourcegraph49';p=r/'runs/20261007-companion-priority/next-ready-preread47/primary-pbps.raw.snapshot.html';raw=p.read_bytes();text=raw.decode('utf-8');H=lambda b:hashlib.sha256(b).hexdigest();offsets=[0]
for line in text.splitlines(keepends=True):offsets.append(offsets[-1]+len(line))
ids=['S1.p1.1','S1.E1','S2.SS2.p1.1','S2.E6','S2.E7','S2.SS2.p1.3','S2.E8','S2.E14','S2.I1.i3.p1.2','A2.E8','A2.SS2.p2.2','A2.E9','A2.Thmtheorem1.p2.1','A2.E13','A3.SS1.p1.1','A3.Ex1','A3.Ex7','A3.SS1.p3.6','A3.E2','A3.SS1.p3.7']
class Parser(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=False);self.stack=[];self.items={}
 def at(self):a,c=self.getpos();return offsets[a-1]+c
 def handle_starttag(self,tag,attrs):
  if tag in ['meta','link','img','br','hr','input','source','wbr']:return
  self.stack.append((tag,dict(attrs).get('id'),self.at()))
 def handle_startendtag(self,tag,attrs):pass
 def handle_endtag(self,tag):
  for k in range(len(self.stack)-1,-1,-1):
   if self.stack[k][0]==tag:
    for tg,ident,start in self.stack[k:]:
     if ident in ids:
      end=self.at()+len('</'+tag+'>');self.items[ident]=(start,end)
    self.stack=self.stack[:k];break
parser=Parser();parser.feed(text);inventory=[];sd=d/'primary-balanced';sd.mkdir(exist_ok=True)
for ident in ids:
 a,z=parser.items[ident];ba=len(text[:a].encode());bz=len(text[:z].encode());b=raw[ba:bz];stem=ident; (sd/(stem+'.raw.html')).write_bytes(b);(sd/(stem+'.lf.html')).write_bytes(b.replace(b'\r\n',b'\n'));assert b.decode()==text[a:z]
 first=text[:a].count('\n')+1;last=text[:z-1].count('\n')+1
 inventory.append(dict(id=ident,path=str(p),start_utf8_byte0=ba,end_utf8_byte0_exclusive=bz,start_character0=a,end_character0_exclusive=z,physical_lines1=[first,last],fragment_raw_sha256=H(b),fragment_lf_sha256=H(b.replace(b'\r\n',b'\n')),fragment_bytes=len(b),balanced_outer=True,snapshot='primary-balanced/'+ident))
 if ident in ['S2.E14','S2.I1.i3.p1.2','A2.SS2.p2.2','A3.SS1.p3.7']:
  print(ident,first,last,html.unescape(' ; '.join(re.findall(r'<annotation encoding="application/x-tex">(.*?)</annotation>',b.decode()))));print(html.unescape(re.sub(r'<[^>]+>',' ',b.decode()))[:1400])
(d/'primary-balanced-inventory.json').write_text(json.dumps(dict(whole_raw_sha256=H(raw),whole_lf_sha256=H(raw.replace(b'\r\n',b'\n')),scope='Independent exact balanced element extraction. Zero-based UTF8 byte offsets, end exclusive; physical lines one based. Physical row partition later uses union; overlapping anchors do not duplicate rows.',anchors=inventory),indent=2),encoding='utf-8')
