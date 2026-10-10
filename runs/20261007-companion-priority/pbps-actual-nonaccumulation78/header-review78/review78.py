"""Independent prospective-header typecheck and raw-source readback; no theorem proof."""
from pathlib import Path
from html.parser import HTMLParser
import datetime, hashlib, json, os, re, subprocess, sys
ROOT=Path('E:/Samplinglib')
BASE=ROOT/'runs/20261007-companion-priority/pbps-actual-nonaccumulation78'
OUT=BASE/'header-review78'
OUT.mkdir(parents=True,exist_ok=True)
PRIMARY=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
HEADER=BASE/'header78.proposed.lean'
PARENT=ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean'
PRODUCT=ROOT/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean'
PY=sys.executable
os.environ['PYTHONUTF8']='1'
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
    b=Path(p).read_bytes();return {'path':str(p),'RAW_bytes':len(b),'RAW_sha256':sha(b)}
def save(name,x): (OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(p):return json.loads(Path(p).read_text(encoding='utf-8'))
class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.math=False
    def handle_starttag(self,t,a):
        if t=='math':self.parts.append(' '+dict(a).get('alttext','')+' ');self.math=True
        if t in ('p','div','h2','h3','h4','table','section'):self.parts.append('\n')
    def handle_endtag(self,t):
        if t=='math':self.math=False
    def handle_data(self,d):
        if not self.math:self.parts.append(d)
def subtree(s,anchor):
    m=re.search(r'<([a-zA-Z0-9]+)\b[^>]*\bid="'+re.escape(anchor)+r'"[^>]*>',s)
    assert m,anchor
    start=m.start();tag=m.group(1);depth=0
    for t in re.finditer(r'<(/?)'+re.escape(tag)+r'\b[^>]*>',s[start:]):
        depth+=-1 if t.group(1) else 1
        if depth==0:return s[start:start+t.end()]
    raise ValueError(anchor)
raw=PRIMARY.read_bytes();assert sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
s=raw.decode('utf-8');regions=[]
for anchor in ['S1.p1.1','S1.E1','S2.SS1','S2.SS2','S3.SS2','A1.SS1']:
    text=subtree(s,anchor);name=anchor.replace('.','_')
    (OUT/(name+'.independent.raw.html')).write_bytes(text.encode('utf-8'))
    p=Text();p.feed(text);plain=''.join(p.parts)
    (OUT/(name+'.independent.text.txt')).write_text(plain,encoding='utf-8')
    regions.append({'anchor':anchor,'raw':info(OUT/(name+'.independent.raw.html')),'text':info(OUT/(name+'.independent.text.txt'))})
save('independent-source-regions.json',{'reviewer':'/root/exact_verify77','primary':info(PRIMARY),
    'method':'Independently select complete raw primary subtrees by native id, preserve byte text, display math alttext through standard-library HTMLParser.',
    'regions':regions,'proof_BODY_used_for_source_topology':False,
    'chronology_limitation':'Candidate header and bounded extractor synthesis were read before successful independent raw-source extraction; no prior topology acceptance or new implementation proof was read. This is independent raw-source coverage review, not a source-blind decoder or final proof review.'})

header=HEADER.read_text(encoding='utf-8');parent=PARENT.read_text(encoding='utf-8')
assert sha(HEADER.read_bytes())==load(BASE/'header78.prospective-manifest.json')['header_RAW_sha256']
header_binders=header[header.index('    {E : Type*}'):header.index('    let P :')]
parent_binders=parent[parent.index('    {E : Type*}'):parent.index('    let c :')]
assert header_binders==parent_binders
def lets(s):
    found=list(re.finditer(r'^    let (\S+)\s*:',s,re.M));result={}
    for i,m in enumerate(found):
        end=found[i+1].start() if i+1<len(found) else s.index('    (∀ y') if '    (∀ y' in s[m.start():] else s.index('    ∀ y')
        result[m.group(1)]=s[m.start():end]
    return result
parent_prop=parent[:parent.index('\nset_option maxHeartbeats')]
hd=lets(header);pd=lets(parent_prop)
common=['c','Φ','S','rate','Λ','τ','next','record','eventTime']
for key in common:assert hd[key]==pd[key],key
assert len(hd)==11 and set(hd)=={'P','ε',*common}
assert hd['P'].strip()=='let P : Measure (ℕ → ℝ) := Measure.infinitePi (fun _ : ℕ => expMeasure (1 : ℝ))'
assert hd['ε'].strip()=='let ε : (ℕ → ℝ) → ℕ → ℝ≥0 := fun ω k => Real.toNNReal (ω k)'
save('header-definition-binder-readback.json',{'status':'PASS_PROSPECTIVE_SIGNATURE_ONLY','reviewer':'/root/exact_verify77',
    'header':info(HEADER),'parent':info(PARENT),'product':info(PRODUCT),'manifest':info(BASE/'header78.prospective-manifest.json'),
    'six_analytic_source_binder_block_byte_equal_to_parent':True,
    'common_nine_literal_definitions_exact_equal_to_parent':common,'literal_object_count':len(hd),
    'canonical_P_and_epsilon_exact':True,'epsilon_reordering':'epsilon(omega)(k) = parent product epsilon(k)(omega) definitionally',
    'new_provider_premises':[],'H_and_C_are_internal_proof_ingredients':True,
    'prospective_only':True,'proof_credit':False})
frozen=[info(p) for p in [HEADER,BASE/'header78.prospective-manifest.json',PARENT,PRODUCT,ROOT/'lean-toolchain',ROOT/'lake-manifest.json']]
(OUT/'header78.exactraw.lean').write_bytes(HEADER.read_bytes())
lake=str(ROOT/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe');lean=str(ROOT/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe')
command=[lake,'env',lean,str(OUT/'header78.exactraw.lean')]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (OUT/'typecheck.stdout.log').open('wb') as so,(OUT/'typecheck.stderr.log').open('wb') as se:
    child=subprocess.Popen(command,cwd=ROOT,stdout=so,stderr=se,env=os.environ.copy());code=child.wait()
save('typecheck.receipt.json',{'command':command,'cwd':str(ROOT),'started_utc':start,
    'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_foreground_PID':child.pid,
    'terminal_closed':True,'exit_code':code,'inputs':frozen,'stdout':info(OUT/'typecheck.stdout.log'),'stderr':info(OUT/'typecheck.stderr.log'),
    'scope':'Fresh elaboration of the complete prospective named Prop and #check only; no theorem BODY or proof credit.'})
print('PROSPECTIVE HEADER TYPECHECK EXIT',code)
assert code==0
