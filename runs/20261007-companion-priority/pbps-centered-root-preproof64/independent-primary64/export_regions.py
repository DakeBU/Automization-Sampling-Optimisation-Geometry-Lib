from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,re,datetime
out=Path(r'E:/Samplinglib/runs/20261007-companion-priority/pbps-centered-root-preproof64/independent-primary64')
idx=json.loads((out/'source-index.json').read_text(encoding='utf8'));raw=Path(idx['source']).read_bytes();s=raw.decode('utf8')
class Readable(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.bits=[];self.mathdepth=0;self.alts=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='math':self.bits.append('`'+a.get('alttext','[MATH WITHOUT ALTTEXT]')+'`');self.alts.append({'id':a.get('id'),'alttext':a.get('alttext')});self.mathdepth+=1
  elif self.mathdepth:return
  elif tag in ['p','div','table','tr','h1','h2','h3','h4','h5','br','li']:self.bits.append('\n')
 def handle_endtag(self,tag):
  if tag=='math':self.mathdepth-=1
  elif not self.mathdepth and tag in ['p','div','table','tr','h1','h2','h3','h4','h5','li']:self.bits.append('\n')
 def handle_data(self,d):
  if not self.mathdepth:self.bits.append(d)
 def text(self):return re.sub(r'\n[ \t]*\n(?:[ \t]*\n)*','\n\n',''.join(self.bits)).strip()+'\n'
ids=['S1.p1','S2.SS2','A2.SS1','A2.SS2','A3.SS1','A3.SS2','A3.SS3','A4.SS1','A4.SS2','A4.SS3']
regions=[]
for id in ids:
 e=idx['nodes'][id];a=len(s[:e['start_char']].encode('utf8'));b=len(s[:e['end_char']].encode('utf8'));chunk=raw[a:b];lf=chunk.replace(b'\r\n',b'\n').replace(b'\r',b'\n');base=out/id
 Path(str(base)+'.raw.html').write_bytes(chunk);Path(str(base)+'.lf.html').write_bytes(lf)
 p=Readable();p.feed(chunk.decode('utf8'));plain=p.text().encode('utf8');Path(str(base)+'.readable.md').write_bytes(plain)
 alts=(json.dumps(p.alts,ensure_ascii=False,indent=2)+'\n').encode('utf8');Path(str(base)+'.alttext.json').write_bytes(alts)
 regions.append({'source_region':id,'byte_range_zero_based_half_open':[a,b],'source_lines_1_based':[s.count('\n',0,e['start_char'])+1,s.count('\n',0,e['end_char'])+1],'source_raw_sha256':idx['raw_sha256'],'raw_file':str(Path(str(base)+'.raw.html')),'raw_sha256':hashlib.sha256(chunk).hexdigest(),'lf_file':str(Path(str(base)+'.lf.html')),'lf_sha256':hashlib.sha256(lf).hexdigest(),'readable_file':str(Path(str(base)+'.readable.md')),'readable_sha256':hashlib.sha256(plain).hexdigest(),'alttext_file':str(Path(str(base)+'.alttext.json')),'alttext_sha256':hashlib.sha256(alts).hexdigest(),'math_count':len(p.alts),'missing_alttext_count':sum(x['alttext'] is None for x in p.alts)})
manifest={'schema':1,'source':idx['source'],'source_bytes':len(raw),'source_raw_sha256':hashlib.sha256(raw).hexdigest(),'actual_region_read_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'byte_range_convention':'zero-based half-open literal UTF-8 source bytes','normalization':'CRLF/CR to LF only; no HTML or JSON reserialization for raw/LF hashes','regions':regions}
(out/'primary-regions-receipt.json').write_bytes((json.dumps(manifest,indent=2)+'\n').encode('utf8'))
print(json.dumps([{'id':r['source_region'],'range':r['byte_range_zero_based_half_open'],'raw':r['raw_sha256'],'math':r['math_count'],'missing':r['missing_alttext_count']} for r in regions],indent=2))
