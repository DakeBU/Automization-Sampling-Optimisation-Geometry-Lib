from pathlib import Path
from html.parser import HTMLParser
import datetime,hashlib,json,re
R=Path('E:/Samplinglib');O=Path(__file__).parent
P=R/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
raw=P.read_bytes();assert hashlib.sha256(raw).hexdigest()=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
class Reader(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.stack=[];self.active=[];self.records=[];self.math=0
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t in ['meta','link','img','br','hr','input','wbr','source']:return
  i=a.get('id','');inside=any(x[1]=='A1.SS1' for x in self.stack)
  self.stack.append((t,i))
  if t=='math':
   self.math+=1
   if self.math==1:
    for e in self.active:e['chunks'].append(' '+a.get('alttext','')+' ')
  paragraph=t=='p' and re.fullmatch(r'A1\.SS1(?:\.SSS0\.Px1)?\.p\d+\.\d+',i)
  eq=inside and t in ['table','tbody'] and re.fullmatch(r'A1\.(?:E|Ex)\d+',i)
  background=i in ['S1.p1.1','S1.E1','S2.SS2.p1.1','S2.E8','S3.E1','A1.Thmtheorem1','A1.SS2.p3.1','license-tr']
  if paragraph or eq or background:self.active.append(dict(id=i,depth=len(self.stack),tag=t,scope='SS1' if inside else 'standing/context',chunks=[]))
 def handle_data(self,d):
  if not self.math:
   for e in self.active:e['chunks'].append(d)
 def handle_endtag(self,t):
  tags=[x[0] for x in self.stack]
  if t not in tags:return
  depth=len(tags)-tags[::-1].index(t)
  for e in self.active[:]:
   if e['depth']>=depth:
    text=' '.join(' '.join(e['chunks']).split());self.records.append(dict(id=e['id'],tag=e['tag'],scope=e['scope'],text=text,normalized_sha256=hashlib.sha256(text.encode()).hexdigest()));self.active.remove(e)
  self.stack=self.stack[:depth-1]
  if t=='math':self.math=max(0,self.math-1)
p=Reader();p.feed(raw.decode('utf8'))
out=dict(status='FROZEN_PRIMARY_FIRST_BEFORE_NEW_PROPOSAL',reviewer_id='/root/exact_verify77',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),primary=dict(path=P.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw)),new_proposal_or_successor_or_verdict_read=False,all_records=p.records,
 independent_reconstruction=[
 'A1.SS1 entire construction includes literal flow/S/rate, integratedhazard clocks and stopped recursion, energycap/nonexplosion, then pathreversal/invariance/operatorL2 assertions.',
 'Heuristic generator block defines A and J, computes log-density derivative, formal Aadjoint/Jadjoint, momentum conjugacy and formal exponentiation. Source explicitly labels this heuristic because bounce discontinuity prevents immediate generator/domain arguments. Retain all atomic definitions/formulas as EXCLUDED_UNJUSTIFIED_ROUTE; do not turn formal exponentiation into a sufficient rigorous OR route.',
 'Rigorous path route AND-needs finitefirsttime density+actualmark, unused-tail conditional iteration, ordered-simplex/path convention, residualsurvival, nonexplosion/summability; then finite Borelvolumechangevars, arcwise densitysurvival including rho(Sz)=rho(z), jump-factor match, Tonelli/signed extension.',
 'Termwise endpoint reversal gives T*=R T R. F1 plus preservation of constants gives phaseinvariance; Jensen plus invariance gives L2 contraction. Independent Cc density plus bounded continuity extends to allL2. Restart/Markov/CK is separately asserted and needs rigorous derivation.',
 'Final p7.1/Ex23 proves Gaussian momentum lift/average intertwining Pi_p R=Pi_p and R Pi_p*=Pi_p*, using even Gaussian momentum. With bounded maps and adjoints of lift/average, phase operator adjoint reversal yields position average selfadjointness.',
 'Final p7.2 also asserts position average is Markov and contractive. Selfadjointness alone does NOT give positivity or preservation of1. Inherited Markov needs phase positivity/constantpreservation (or actual probabilityfiber pushforward), and lift/averaging positivity/unitpreservation. L2 contraction needs phase contraction plus bounded contraction of lift/average. Full averaged Markov contraction remains OPEN until ALL these requirements are linked.',
 'Time t, y/reference fixed in averaging. This is Gaussian average of phase transition at each fixedtime, not reference-randomized halfturn law81, not restart/CK semigroup on position. Source mentions no necessity of a typedkernel representation.',
 'Finitefirstevent86 does not discharge any global path law/reversal/invariance/Markov/averaging requirements. Every such future node must stay OPEN.'
 ])
with (O/'primary-first-reconstruction86.json').open('x',encoding='utf8',newline='\n') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
print('PRIMARY_RECORDS',len(p.records),'SS1',sum(x['scope']=='SS1' for x in p.records))
for x in p.records:
 print(x['id'],x['tag'],x['text'])
