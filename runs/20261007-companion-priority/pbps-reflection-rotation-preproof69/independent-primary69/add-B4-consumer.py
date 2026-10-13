import datetime, hashlib, html, json, os, pathlib, re
from html.parser import HTMLParser
out=pathlib.Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def put(n,d): (out/n).write_text(json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
whole=pathlib.Path(r'E:\Samplinglib\runs\20261007-companion-priority\phase-pbps-gamma-preread57\primary-pbps.exactraw.snapshot.html').read_bytes()
assert len(whole)==1482128 and sha(whole)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
a,z=888702,970152
b=whole[a:z]
assert b.startswith(b'<div id="A2.SS3.p8"') and whole[z:].startswith(b'<div id="A2.SS3.p11"')
name='corrector-change-B4-consumer-proof'
(out/('source.'+name+'.RAW.html')).write_bytes(b)
(out/('source.'+name+'.LF.html')).write_bytes(b.replace(b'\r\n',b'\n'))
class Render(HTMLParser):
    def __init__(self): super().__init__(convert_charrefs=True); self.parts=[]; self.math=0
    def handle_starttag(self,t,a):
        a=dict(a)
        if t=='math': self.math+=1; self.parts.append(' ['+a.get('id','')+': '+a.get('alttext','')+'] ')
        elif not self.math and t in ('p','div','table','tr'): self.parts.append('\n')
    def handle_endtag(self,t):
        if t=='math': self.math-=1
        elif not self.math and t in ('p','div','table','tr'): self.parts.append('\n')
    def handle_data(self,d):
        if not self.math:self.parts.append(d)
p=Render();p.feed(b.decode('utf-8'))
(out/('source.'+name+'.rendered.txt')).write_text('\n'.join(s.strip() for s in ''.join(p.parts).splitlines() if s.strip())+'\n',encoding='utf-8')
items=[]
for m in re.finditer(rb'<math\b[^>]*>.*?</math>',b,re.S):
 raw=m.group();tag=raw[:raw.index(b'>')+1]
 at={k.decode():html.unescape(v.decode('utf-8')) for k,v in re.findall(rb'([\w:-]+)="([^"]*)"',tag)}
 an=re.search(rb'<annotation\b[^>]*encoding="application/x-tex"[^>]*>(.*?)</annotation>',raw,re.S)
 tex=html.unescape(an.group(1).decode('utf-8'));assert tex==at['alttext']
 items.append(dict(id=at['id'],region=name,alttext=at['alttext'],annotation_tex=tex,
  RAW_bytes=len(raw),RAW_sha256=sha(raw),source_RAW_range_end_exclusive=[a+m.start(),a+m.end()],
  region_RAW_range_end_exclusive=[m.start(),m.end()],source_role='pending-independent-classification'))
ri=json.loads((out/'source-input-regions.json').read_bytes())
ri['regions']=[x for x in ri['regions'] if x['name']!=name]
ri['regions'].append(dict(name=name,source_RAW_range_end_exclusive=[a,z],RAW_bytes=len(b),
 RAW_sha256=sha(b),LF_sha256=sha(b.replace(b'\r\n',b'\n')),math_count=len(items),
 independently_reparsed_math_count=len(items),bytes_exact=True,reason='Actual Lemma B.4 proof contains explicit B21 consumer outside old six slices'))
put('source-input-regions.json',ri)
iv=json.loads((out/'source-coverage-inventory.json').read_bytes())
iv['math_items']=[x for x in iv['math_items'] if x['region']!=name]
iv['math_items'].extend(items);iv['count']=len(iv['math_items']);iv['schema']='primary69-source-only-reparsed-seven-regions-v1'
put('source-coverage-inventory.json',iv)
put('B4-consumer-read-process.json',dict(actual_pid=os.getpid(),source_before_candidate=True,
 RAW_range=[a,z],RAW_bytes=len(b),RAW_sha256=sha(b),math_count=len(items),read_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 exact_B21_reference_RAW_offset=926328,no_network=True))
print(json.dumps(dict(actual_pid=os.getpid(),B4_consumer_RAW_bytes=len(b),B4_consumer_math_count=len(items),
 total_finite_math_count=iv['count'],RAW_sha256=sha(b)),sort_keys=True))
