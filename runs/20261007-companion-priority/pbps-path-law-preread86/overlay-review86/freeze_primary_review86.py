"""Fresh primary-only reconstruction for the distinct exact-overlay audit."""
from pathlib import Path
from html.parser import HTMLParser
import datetime,hashlib,json,re
ROOT=Path('E:/Samplinglib'); OUT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),raw_sha256=sha(b),bytes=len(b))
def put(n,j):
 p=OUT/n;assert not p.exists();p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode());return pin(p)
class X(HTMLParser):
 def __init__(self):super().__init__();self.st=[];self.d={};self.math=0
 def handle_starttag(self,t,a):
  a=dict(a);i=a.get('id');self.st.append((t,i))
  if i:self.d.setdefault(i,[])
  if t=='math':
   for _,k in self.st:
    if k:self.d[k].append(a.get('alttext',''))
   self.math+=1
 def handle_endtag(self,t):
  if t=='math':self.math=max(0,self.math-1)
  for i in range(len(self.st)-1,-1,-1):
   if self.st[i][0]==t:self.st=self.st[:i];break
 def handle_data(self,d):
  if not self.math:
   for _,k in self.st:
    if k:self.d[k].append(d)
 def norm(self,i):return re.sub(r'\s+',' ',' '.join(self.d[i])).strip()
p=ROOT/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
assert pin(p)['raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
x=X();x.feed(p.read_text(encoding='utf8'))
ids=['license-tr','S1.p1.1','S1.E1','S2.SS2.p1.1','S2.E8','S3.E1','A1.SS1.p1.1','A1.SS1.p2.1','A1.SS1.p2.2','A1.SS1.p3.7','A1.Thmtheorem1','A1.SS2.p3.1']+[f'A1.E{i}' for i in range(1,9)]+[f'A1.Ex{i}' for i in range(1,24)]+[f'A1.SS1.SSS0.Px1.p{i}' for i in ['2.1','3.1','3.2','3.3','3.4','4.1','4.2','4.3','4.4','5.1','5.2','5.3','6.1','6.2']]
assert len(ids)==57 and all(x.norm(i) for i in ids)
nodes=[
 ('P01','Six original analytic hypotheses; finite real phase and fixed parameters',['S1.p1.1','S1.E1','S2.SS2.p1.1']),
 ('P02','Literal continuous flow/rate, Borel total bounce R0=I',['A1.Ex1','A1.Ex2','A1.Ex3']),
 ('P03','Independent Exp1 clocks, inverse hazard and actual finite update',['A1.E1','A1.E2','A1.SS1.p2.1']),
 ('P04','Positive finite wait law density from integrated hazard; source implicit',['A1.E1','A1.E7']),
 ('P05','Borel time/post-bounce marking, necessary to marked-law statement',['A1.Ex2','A1.Ex3','A1.E2']),
 ('P06','Unused-clock independence and conditional transition from current post-state',['A1.SS1.p2.1','A1.SS1.SSS0.Px1.p4.2']),
 ('P07','Residual survival conditioned on current state/history and unused next clock',['A1.E1','A1.E7']),
 ('P08','Simplex prescribed finite paths with explicit prejump/postjump conventions',['A1.Ex19','A1.SS1.SSS0.Px1.p4.2']),
 ('P09','Successive n-event density and last-arc survival',['A1.E7']),
 ('P10','Nonaccumulation; stopping and infinite last live arc',['A1.SS1.p2.2','A1.Ex4','A1.Ex5','A1.Ex6','A1.Ex7','A1.Ex8','A1.Ex9','A1.SS1.p3.7']),
 ('P11','Actual A7 expansion over finite event count',['A1.E7']),
 ('P12','Fixed-state absolute summability, not uniform outer exponential envelope',['A1.SS1.SSS0.Px1.p4.3']),
 ('P13','Positive mass-one Tonelli then signed bounded decomposition',['A1.SS1.SSS0.Px1.p5.2']),
 ('P14','Exact normalized phase density',['S2.E8','S3.E1','A1.Ex11']),
 ('P15','Reflection preserves phase density pointwise: position fixed, momentum norm preserved',['A1.Ex3','S3.E1','A1.SS1.SSS0.Px1.p5.1']),
 ('P16','A4 log-density derivative along deterministic arcs',['A1.E4']),
 ('P17','Finite-path rho-survival identity',['A1.Ex20','A1.SS1.SSS0.Px1.p5.1']),
 ('P18','R flow/bounce algebra and jump-rate matching',['A1.Ex18','A1.E5']),
 ('P19','Borel volume-preserving flow/S/R; reverse-time simplex measure preservation',['A1.E6','A1.E8','A1.SS1.SSS0.Px1.p4.4']),
 ('P20','A8 joint reversal with explicit finite jump-value convention',['A1.E8','A1.SS1.SSS0.Px1.p4.4']),
 ('P21','Weighted n-event reversal, bounded endpoint tests',['A1.Ex21','A1.SS1.SSS0.Px1.p5.2']),
 ('P22','Actual invariance F=1, AE-safe L2/Jensen, independent Cc density, allL2',['A1.SS1.SSS0.Px1.p5.3','A1.SS1.SSS0.Px1.p6.1','A1.SS1.SSS0.Px1.p6.2']),
 ('P23','Generator formal adjoint is heuristic only; Markov restart separate',['A1.Ex12','A1.Ex13','A1.Ex14','A1.Ex15','A1.Ex16','A1.Ex17','A1.SS1.SSS0.Px1.p2.1','A1.SS1.p3.7']),
 ('P24','Source Cc bounded-test limit and compression remain separate',['A1.Ex22','A1.Ex23']),
 ('P25','CDF/FTC sufficient density route: coordinate law AND continuous rate AND CDF/finite measure ext',['A1.E1','A1.E7']),
 ('P26','Alternative monotone-hazard transport route: coordinate law AND continuous hazard AND transport theorem',['A1.E1','A1.E7'])]
edges=[('P01','P02'),('P02','P03'),('P03','P25'),('P02','P25'),('P03','P26'),('P02','P26'),('P25','P04'),('P26','P04'),('P02','P05'),('P04','P09'),('P05','P09'),('P06','P07'),('P03','P06'),('P06','P09'),('P07','P09'),('P08','P09'),('P09','P11'),('P10','P11'),('P08','P11'),('P11','P13'),('P14','P13'),('P02','P15'),('P14','P15'),('P15','P17'),('P16','P17'),('P08','P17'),('P18','P20'),('P19','P20'),('P08','P20'),('P17','P21'),('P18','P21'),('P20','P21'),('P11','P21'),('P13','P21'),('P21','P22')]
freeze=put('fresh-primary-topology86.json',{
 'status':'FROZEN_PRIMARY_ONLY_BEFORE_EXACT_OVERLAY','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raw_inputs':[pin(p)],
 'independence_disclosure':'Reviewer authored original86 extraction, not the distinct overlay. This fresh source-only reconstruction was made without consulting original graph, overlay, proposer decision, implementation or prior verdict during this phase. It is not self-approval of original extraction.',
 'anchors':[dict(source_id=i,normalized_sha256=sha(x.norm(i).encode())) for i in ids],
 'nodes':[dict(id=i,title=t,source_ids=a,status='SOURCE_ONLY_NOT_PROVED') for i,t,a in nodes],
 'ingredient_edges':[dict(source=a,target=b) for a,b in edges],
 'junctions':[{'target':'P04','OR':['P25','P26'],'each_route_is_AND':True},{'target':'P17','AND':['P15','P16','P08']},{'target':'P09','AND':['P04','P05','P06','P07','P08']},{'target':'P21','AND':['P17','P18','P20','P11','P13']}],
 'optional':'P12 fixed-state summability is a sufficient analytic route, never a global outer integrable envelope.',
 'critical_distinctions':['Borel marking is an ingredient for marked-law integration even if unmarked wait CDF exists.','Conditional last survival must use current poststate/remaining horizon and an unused independent clock; fixed-state law cannot be substituted under arbitrary correlated clocks.','Bounce rho preservation is separate from A4 arc derivative and from Lebesgue measure preservation.','Both density routes require explicit ingredients within their branch; branches are OR, not AND together.','No new dynamics binder; regularity, measurability and probability are derived from literal objects and original six assumptions.','All full A7/reversal/invariance/L2/Markov/cost/composition conclusions remain OPEN.']})
print(json.dumps(freeze))
