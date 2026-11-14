from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re

ROOT=Path('/Users/zhouhuanjian/ASTIS-GC')
OUT=ROOT/'.astis/semantic-neutral-20261109/src_9a6d2f/phase1'
SOURCE=ROOT/'.astis/huanjian-resume-20261103/2610.20492v1.html'
b=SOURCE.read_bytes(); s=b.decode('utf-8')
assert len(b)==951991
assert hashlib.sha256(b).hexdigest()=='6bc5ddc1e19cea9ba1dfe862fa79bc69fe861dff045d6ad1c7baa4a113c37915'

class Readable(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True);self.parts=[];self.math=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='math':
            if not self.math:self.parts.append(' $'+a.get('alttext','[MISSING ALTTEXT]')+'$ ')
            self.math+=1;return
        if self.math:return
        if tag in ('section','div','p','table','h2','h3','h4','h5','h6','li'):
            self.parts.append('\n\n')
            if a.get('id'):self.parts.append('[['+a['id']+']] ')
        if tag=='br':self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag=='math':self.math-=1;return
        if self.math:return
        if tag in ('section','div','p','table','h2','h3','h4','h5','h6','li','tr'):self.parts.append('\n\n')
        elif tag in ('td',):self.parts.append(' ')
    def handle_data(self,data):
        if not self.math:self.parts.append(data)
    def result(self):
        return '\n\n'.join(re.sub(r'\s+',' ',p).strip() for p in ''.join(self.parts).split('\n\n') if p.strip())+'\n'

def span(anchor):
    m=re.search(r'<([A-Za-z0-9]+)\b[^>]*\bid="'+re.escape(anchor)+r'"[^>]*>',s)
    if not m:raise ValueError(anchor)
    tag=m.group(1);depth=0
    for t in re.finditer(r'</?'+re.escape(tag)+r'\b[^>]*>',s[m.start():]):
        tok=t.group()
        depth+= -1 if tok.startswith('</') else 1
        if depth==0:return m.start(),m.start()+t.end()
    raise ValueError('unclosed '+anchor)

records=[]
def extract(anchor,label=None,stop_before=None):
    i,j=span(anchor)
    if stop_before:j=s.index('<section id="'+stop_before+'"',i,j)
    name=label or anchor
    raw=s[i:j].encode('utf-8')
    rp=OUT/(name+'.raw.html');rp.write_bytes(raw)
    p=Readable();p.feed(raw.decode('utf-8'));txt=p.result().encode()
    tp=OUT/(name+'.readable.txt');tp.write_bytes(txt)
    rec={'anchor':anchor,'source_char_start':i,'source_char_end_exclusive':j,'source_byte_start':len(s[:i].encode()),'source_byte_end_exclusive':len(s[:j].encode()),'stop_before':stop_before,'raw_file':rp.name,'raw_sha256':hashlib.sha256(raw).hexdigest(),'readable_file':tp.name,'readable_sha256':hashlib.sha256(txt).hexdigest()}
    records.append(rec)
    return txt.decode()

for anchor,label,stop in [('S2',None,None),('S4','S4.intro','S4.SS1'),('S4.SS1',None,None),('S4.SS2',None,None),('A3.SS4',None,None),('S4.SS3',None,None),('bib.bib3',None,None)]:
    text=extract(anchor,label,stop)
    if anchor in ('S4.SS3','bib.bib3'): print(text)
(OUT/'excerpt_index.json').write_text(json.dumps({'source':str(SOURCE.relative_to(ROOT)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'excerpts':records},indent=2)+'\n')
