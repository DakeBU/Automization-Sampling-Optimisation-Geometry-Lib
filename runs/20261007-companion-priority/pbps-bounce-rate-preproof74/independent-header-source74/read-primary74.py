from pathlib import Path
import hashlib,json,os,sys,re
from html.parser import HTMLParser
sys.stdout.reconfigure(encoding='utf-8')

ROOT=Path('E:/Samplinglib')
OWN=Path(__file__).resolve().parent
PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
MAP=ROOT/'runs/20261007-companion-priority/pbps-harmonic-flow-preproof73/independent-header-source73/source13-region51-block.finite-RAW-LF-map73.json'
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
    b=p.read_bytes(); return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(b.replace(b'\r\n',b'\n')),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))}
class View(HTMLParser):
    def __init__(self): super().__init__();self.math=0;self.s=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='math':
            self.math+=1;self.s.append(' [MATH '+a.get('id','')+': '+a.get('alttext','')+'] ')
        elif tag in ('p','tr','div','section') and not self.math:self.s.append('\n')
    def handle_endtag(self,tag):
        if tag=='math':self.math-=1
    def handle_data(self,data):
        if not self.math:self.s.append(data)
    def result(self):return re.sub(r'[ \t]+',' ',''.join(self.s)).strip()
def view(b):
    q=View();q.feed(b.decode('utf-8'));return q.result()

b=PRIMARY.read_bytes()
assert len(b)==1482128 and sha(b)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
m=json.loads(MAP.read_bytes())
regions=[]
for old in m['regions']:
    a,z=old['RAW_start_inclusive'],old['RAW_end_exclusive'];sl=b[a:z]
    assert sha(sl)==old['RAW_sha256']
    r=dict(old);r['read_view']=view(sl);regions.append(r)
# The old math-only R_h range omits the surrounding literal R_0=I convention.
i=b.index(b'id="S2.E4.m1"')
par=b.rfind(b'<p ',0,i)
end=b.index(b'</p>',i)+4
# Equation is a separate table; source convention occurs in following paragraph.
if end-par>15000:
    par=b.rfind(b'<div ',0,i);end=b.index(b'</div>',i)+6
reflection_context=b[max(0,i-2500):i+5000]
start=b.rfind(b'<p ',0,i-200)
if start<0 or i-start>7000:start=i-2000
end=b.index(b'</p>',i)+4
assert end-start<20000
sl=b[start:end]
supp={'source_id':'S2.E4.context74','RAW_start_inclusive':start,'RAW_end_exclusive':end,'RAW_bytes':len(sl),'RAW_sha256':sha(sl),'LF_sha256':sha(sl.replace(b'\r\n',b'\n')),'read_view':view(sl)}
dump(OWN/'source-primary-readviews74.json',{'primary':pin(PRIMARY),'locator_map':pin(MAP),'locator_only_no_old_verdict_reuse':True,'LF_recipe':'Replace CRLF byte pairs with LF only; preserve bare CR and every other byte','regions':regions,'supplemental_regions':[supp]})
print(json.dumps({'pid':os.getpid(),'EXIT':0,'primary_sha256':sha(b),'regions':len(regions),'blocks':sum(len(r.get('blocks',[])) for r in regions),'supplemental_range':[start,end]}))
for key in sys.argv[1:]:
    for r in regions+[supp]:
        if r['source_id']==key:print('\nSOURCE '+key+'\n'+r['read_view'])
dump(OWN/'terminal.primary-read74.receipt.json',{'pid':os.getpid(),'EXIT':0,'argv':sys.argv,'primary':pin(PRIMARY),'locator_map':pin(MAP),'regions_verified':len(regions),'blocks_verified':sum(len(r.get('blocks',[])) for r in regions),'candidate_reads':0,'own_scope':OWN.relative_to(ROOT).as_posix(),'prior_negative':{'pid':2396,'EXIT':1,'class':'terminal-encoding-gbk-UnicodeEncodeError','premature_receipt_not_exit_evidence':True}})
