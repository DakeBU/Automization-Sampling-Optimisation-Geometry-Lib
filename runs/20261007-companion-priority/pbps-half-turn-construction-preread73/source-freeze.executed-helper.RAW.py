from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, sys, re, os, subprocess, datetime

ROOT = Path('E:/Samplinglib')
OWN = ROOT / 'runs/20261007-companion-priority/pbps-half-turn-construction-preread73'
PRIMARY = ROOT / 'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
PY = 'C:/Users/admin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'

def sha(b): return hashlib.sha256(b).hexdigest()
def enc(j): return (json.dumps(j,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode('utf-8')
def put(n,j):
    assert not (OWN/'lease.final.json').exists(), 'CLOSED scope'
    (OWN/n).write_bytes(enc(j) if not isinstance(j,bytes) else j)
def pin(p):
    b=p.read_bytes(); return {'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'raw_sha256':sha(b),'lf_sha256':sha(b.replace(b'\r\n',b'\n')),'lf_recipe':'replace CRLF byte pair only with LF; preserve bare CR and every other byte'}

class N:
    def __init__(self,tag,attrs,start,parent=None):
        self.tag=tag; self.a=dict(attrs); self.start=start; self.end=None; self.parent=parent; self.children=[]
    def text(self):
        if self.tag=='math': return self.a.get('alttext','')
        return ' '.join(c if isinstance(c,str) else c.text() for c in self.children)
class Tree(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=True); self.s=s; self.lines=[0]; self.nodes=[]; self.stack=[]
        for m in re.finditer('\n',s): self.lines.append(m.end())
        self.feed(s)
    def charpos(self):
        l,c=self.getpos(); return self.lines[l-1]+c
    def handle_starttag(self,t,a):
        n=N(t,a,self.charpos(),self.stack[-1] if self.stack else None); self.nodes.append(n)
        if self.stack: self.stack[-1].children.append(n)
        if t not in {'br','img','meta','link','hr','input','source','wbr','area','base','embed','param','track','col'}: self.stack.append(n)
        else: n.end=n.start+len(self.get_starttag_text())
    def handle_startendtag(self,t,a):
        self.handle_starttag(t,a)
        if self.stack and self.stack[-1].tag==t: self.stack[-1].end=self.charpos()+len(self.get_starttag_text()); self.stack.pop()
    def handle_endtag(self,t):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i].tag==t:
                for n in self.stack[i:]: n.end=self.s.find('>',self.charpos())+1
                self.stack=self.stack[:i]; return
    def handle_data(self,s):
        if self.stack: self.stack[-1].children.append(s)

def tree():
    b=PRIMARY.read_bytes(); assert sha(b)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'; s=b.decode('utf-8'); return b,s,Tree(s)

def discover():
    b,s,t=tree()
    for n in t.nodes:
        if n.tag in {'section','figure'} and (n.a.get('id','').startswith('S3') or n.a.get('id','').startswith('A1')):
            print('REGION',n.a.get('id'),n.tag, n.start,n.end)
            if n.a.get('id') in {'S3','A1.SS1','A1.SS2','A1.SS3'}: print(re.sub(r'\s+',' ',n.text()))

def catalogue():
    b,s,t=tree()
    for n in t.nodes:
        sid=n.a.get('id',''); txt=re.sub(r'\s+',' ',n.text()).strip()
        if (sid.startswith('A1.SS1') and n.tag in {'p','div'} and 'ltx_para' in n.a.get('class','')) or (sid.startswith('S3') and n.tag=='math' and any(k in txt for k in ['c_{y,','Phi','lambda','dot{x}','x_{\\pi}'])) or (sid.startswith('S2') and n.tag in {'p','div'} and any(k in txt for k in ['Assumption','Hessian','C^{2}','reflection','R_{h}'])):
            print(sid,n.tag,n.start,n.end,txt[:6500])

def source_freeze():
    b,s,t=tree(); (OWN/'source-slices').mkdir(exist_ok=True)
    ids=['S1.p1','S2.SS2.p1','S2.E4.m1','S3.E4.m1','S3.E6.m1','S3.E7.m1','alg1','S3.Thmtheorem1','S4.E5.m1','A1.SS1.p1','A1.SS1.p2','A1.SS1.p3','A1.Thmtheorem2']
    rows=[]; formula=[]
    for sid in ids:
        ns=[n for n in t.nodes if n.a.get('id')==sid]; assert len(ns)==1,sid
        n=ns[0]; assert n.end
        lo=len(s[:n.start].encode('utf-8')); hi=len(s[:n.end].encode('utf-8'))
        raw=b[lo:hi]; assert raw.decode('utf-8')==s[n.start:n.end]
        file='source-slices/'+sid+'.exactraw.html'; put(file,raw)
        rows.append({'source_id':sid,'source_path':pin(PRIMARY)['path'],'whole_source_raw_sha256':sha(b),'raw_byte_start_inclusive':lo,'raw_byte_end_exclusive':hi,'bytes':len(raw),'literal_span_raw_sha256':sha(raw),'snapshot':file,'readview':re.sub(r'\s+',' ',n.text()).strip()})
    for n in t.nodes:
        if n.tag=='math' and (n.a.get('display')=='block' or n.a.get('id') in ['S1.E1.m1','S2.E4.m1']) and any(n.start>=x.start and n.end<=x.end for x in t.nodes if x.a.get('id') in ids):
            lo=len(s[:n.start].encode('utf-8')); hi=len(s[:n.end].encode('utf-8'))
            formula.append({'source_id':n.a.get('id'),'formula_alttext':n.a.get('alttext'), 'raw_byte_start_inclusive':lo,'raw_byte_end_exclusive':hi,'literal_span_raw_sha256':sha(b[lo:hi]),'bytes':hi-lo})
    put('source.regions.json',{'primary':pin(PRIMARY),'interval_policy':'0-based RAW UTF-8 byte offsets, start inclusive/end exclusive; hashes are literal source bytes, not normalized HTML or readview','region_count':len(rows),'regions':rows,'formula_count':len(formula),'formulas':formula})
    put('source-expectations.json',{
      'status':'SOURCE_FIRST_EXPECTATIONS_FROZEN_BEFORE_ANY_73_HEADER','authority':'fixed PBPS arXiv2609.06905v1 primary only; not an existing72 source review','primary_raw_sha256':sha(b),
      'source_boundary':['Algorithm1','Proposition3.1','AppendixA.1 explicit construction, energy and nonexplosion paragraph','(2.4),(3.4),(3.6)-(3.9),(4.5),(A.1)-(A.2)'],
      'original_inputs':{'space':'finite real inner-product space E with Borel measurable structure, including finrank0','six_callers':['0 < α','α ≤ β','ContDiff ℝ 2 V','∀ x v, α‖v‖² ≤ D²V(x)[v,v] ≤ β‖v‖²','0 < η','βη ≤ 1'],'no_strict_endpoint':'αη=1 is allowed; deterministic construction uses only positive η and actual gradient value'},
      'actual_objects':{'c':'y − η • gradient V xRef','h':'gradient V x − gradient V xRef','flow':'Φ_t(x,p) = (c + cos(t) • (x−c) + (sqrt(η)*sin(t)) • p, (−sin(t)/sqrt(η)) • (x−c) + cos(t) • p)','bounce':'S_xRef(x,p) = (x, R_(h(x)) p)','reflection':'R_h p = p − (2*inner ℝ h p / ‖h‖²) • h, R_0 = id','rate':'λ(x,p) = sqrt(η)*max 0 (inner ℝ p (h x))','energy':'H(x,p) = (η⁻¹*‖x−c‖²+‖p‖²)/2'},
      'construction_order':[
       'Produce the SAME explicit harmonic flow and residual bounce maps, not a supplied arbitrary kernel.',
       'For independent Exp(1) E_(n+1), S_(n+1)=inf{u≥0: integral_0^u λ(Φ_s ζ_Tn) ds ≥ E_(n+1)} with infinity when empty; T_(n+1)=T_n+S_(n+1).',
       'At each finite clock hit use S_xRef(Φ_S ζ_Tn); use Φ_t between hits.',
       'Flow and bounce preserve H; let energy E0=H(initial), obtain ‖p‖≤sqrt(2E0), ‖x−c‖≤sqrt(2ηE0).',
       'Derive gradient β-Lipschitzness internally from genuine C2/two Hessians; then λ≤sqrt(η)*β*sqrt(2E0)*(sqrt(2ηE0)+‖c−xRef‖).',
       'Zero rate envelope means no events; positive envelope gives each finite S_(n+1)≥E_(n+1)/envelope. IID clocks plus SLLN give T_n→∞, then all-time path construction and memoryless Markov property.',
       'Stationarity is a separate path-reversal proof; the paper itself labels bare formal generator exponentiation heuristic.'
      ],
      'must_not_add':['probability/reference-law normalization premise','gradient-Lipschitz/regularity premise in actual caller','already existing PDMP, endpoint H or nonexplosion premise','onto polar map','nonzero normal or positive dimension','strict αη<1','higher derivatives'],
      'remaining':['full Borel bounce dependence at vanishing normal (not joint continuity)','integrated hazard time integrability, continuity, monotonicity and threshold measurability','canonical iid exponential clock probability space and all recursion states','a.s. nonexplosion and uniqueness','time-homogeneous Markov property','stationarity/path reversal','jointly measurable terminal kernel H and half-turn operator','H1/B2/B4 dynamics, main theorem, caps/errors and actual-input cost/composition'],
      'coverage_exclusions':{'AppendixA.1 remainder':'stationarity/path-reversal/semigroup proof remains future; no endpoint or invariant law credit here','AppendixA.2':'kernel measurability/operator assembly remains future','AppendixA.3':'stationary rate tails/capping/costs excluded','AppendixB':'existing corrector algebra is not a dynamics existence proof'}
    })
    put('lease.open.json',{'state':'OPEN','actor':'/root/exact_science63','scope':OWN.relative_to(ROOT).as_posix(),'task':'independent source-first next-edge planning73 only','source_expectations_written_before_any73_header':True,'canonical_write_authorized':False,'compiler_run':False})
    put('observer-negatives.json',{'typed_observer_limitations':[
      {'stage':'initial direct source parser probe','tool_chunk':'56fa74','exit_code':1,'diagnosis':'bs4 unavailable; switched to Python standard-library HTMLParser; no source/math change','raw_tool_error':'ModuleNotFoundError: No module named \'bs4\'','pid_not_exposed_by_tool':True},
      {'stage':'discover','pid':42768,'exit_code':1,'diagnosis':'HTMLParser owns integer offset; helper method collision, repaired by charpos method name; exact stderr retained','failed_helper_not_frozen_before_repair':True,'scope':'observer failure only'},
      {'stage':'bounded path discovery','tool_chunks':['25db8e','a05aed','915fdb'],'diagnosis':'guessed AmbientReflection/ReflectedMeanGeometry/InnerProductSpace.Reflection/Data.Complex.Exponential paths absent; corrected by rg --files and exact existing paths','mathematical_blocker':False,'no_api_absence_inferred_from_bad_paths':True}
    ]})
    print(json.dumps({'pid':os.getpid(),'primary_bytes':len(b),'primary_raw_sha256':sha(b),'source_regions':len(rows),'formula_count':len(formula),'source_expectations':pin(OWN/'source-expectations.json')}))

def runner(label,mode):
    assert not (OWN/'lease.final.json').exists()
    command=[PY,'-B','-X','utf8',str(OWN/'preread73.py'),mode]
    put(label+'.executed-helper.RAW.py',(OWN/'preread73.py').read_bytes())
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with (OWN/(label+'.stdout.log')).open('wb') as out,(OWN/(label+'.stderr.log')).open('wb') as err:
        p=subprocess.Popen(command,cwd=ROOT,stdout=out,stderr=err)
        print(json.dumps({'runner_pid':os.getpid(),'child_pid':p.pid,'command':command}),flush=True)
        ec=p.wait()
    receipt={'label':label,'runner_pid':os.getpid(),'pid':p.pid,'exit_code':ec,'terminal_closed':True,'started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':command,'stdout':pin(OWN/(label+'.stdout.log')),'stderr':pin(OWN/(label+'.stderr.log'))}
    put(label+'.receipt.json',receipt); print(json.dumps(receipt),flush=True)
    sys.exit(ec)

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='run': runner(sys.argv[2],sys.argv[3])
    elif mode=='discover': discover()
    elif mode=='catalogue': catalogue()
    elif mode=='source-freeze': source_freeze()
