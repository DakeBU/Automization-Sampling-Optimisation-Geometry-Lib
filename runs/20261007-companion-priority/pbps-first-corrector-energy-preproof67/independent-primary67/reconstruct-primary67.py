from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,re,html,os,datetime,collections
O=Path(__file__).parent;P=Path('E:/Samplinglib/runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html')
H=lambda b:hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def put(n,d):(O/n).write_bytes((json.dumps(d,sort_keys=True,indent=2,ensure_ascii=True)+'\n').encode())
def pin(p):
 b=p.read_bytes();return dict(path=str(p).replace('\\','/'),RAW_bytes=len(b),RAW_sha256=H(b),LF_bytes=len(b.replace(b'\r\n',b'\n')),LF_sha256=H(b.replace(b'\r\n',b'\n')))
class Render(HTMLParser):
 def __init__(self):super().__init__();self.out=[];self.math=0
 def handle_starttag(self,t,a):
  if t=='math':self.math+=1;v=dict(a);self.out.append(' [MATH '+v.get('id','')+': '+v.get('alttext','')+'] ')
  elif not self.math and t in ['p','div','h3','h6','table','tr']:self.out.append('\n')
 def handle_endtag(self,t):
  if t=='math':self.math-=1
 def handle_data(self,t):
  if not self.math:self.out.append(t)
class Attr(HTMLParser):
 def __init__(self):super().__init__();self.attrs={}
 def handle_starttag(self,t,a):
  if t=='math':self.attrs=dict(a)
started=now();b=P.read_bytes();assert H(b)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
regions=[('global-assumptions',46982,73369),('actual-joint-law',95318,130557),('conditional-reflection-blocks-B1',708167,758371),('same-root-polar-B2',758371,801184),('corrector-sharp-energy-and-consumers-B3',801184,888702),('real-L2-spectral-conventions-D1',1348892,1372364)]
def role(id,region):
 if region=='global-assumptions':return 'source-original-conditions' if id.startswith('Thmunnumberedtheoremx1.') or id in ['S1.Ex1.m1','S1.Ex2.m1'] else 'whole-paper-introduction-context-excluded'
 if region=='actual-joint-law':return 'actual-law-reflection-prerequisite' if id.startswith('S2.SS2.p1.') or id in ['S2.E6.m1','S2.E7.m1','S2.E8.m1'] else 'algorithm-oracle-context-excluded'
 if region=='conditional-reflection-blocks-B1':return 'actual-P-subspaces-reflection-blocks-prerequisite' if id.startswith('A2.SS1.p1.') or id.startswith('A2.SS1.p3.') or id in ['A2.Ex1.m1','A2.Ex2.m1','A2.E1.m1','A2.E2.m1','A2.E4.m1','A2.Ex3.m1','A2.E5.m1'] else 'halfturn-Markov-process-context-excluded'
 if region=='same-root-polar-B2':
  if id.startswith('A2.Thmtheorem2.') or id=='A2.E17.m1' or id in ['A2.SS2.p5.m6','A2.SS2.p5.m7','A2.SS2.p7.m1']:return 'B17-halfturn-smallstep-context-excluded'
  if id in ['A2.Thmtheorem1.p2.m1','A2.Thmtheorem1.p2.m2','A2.E13.m1']:return 'B13-H1-context-not-new-premise'
  if id=='A2.E14.m1':return 'B14-source-upstream-not-new-floor-premise'
  return 'same-A-Gamma-gap-inverse-polar-prerequisite'
 if region=='real-L2-spectral-conventions-D1':return 'real-L2-spectral-adjoint-order-background' if not id.startswith('A4.Thmtheorem2.') and not id.startswith('A4.SS1.p3.') and id not in ['A4.E4.m1','A4.E5.m1'] else 'density-dynamics-context-excluded'
 if id.startswith('A2.SS3.p1.') or id.startswith('A2.SS3.p3.') or id in ['A2.Ex6.m1','A2.Ex8.m1']:return 'actual-centered-micro-macro-input-prerequisite'
 if id.startswith('A2.SS3.p4.') or id in ['A2.E19.m1','A2.E20.m1']:return 'B19-Lyapunov-B20-corrector-definition'
 if id.startswith('A2.SS3.p7.') or id in ['A2.Ex19.m1','A2.Ex20.m1','A2.Ex20.m2','A2.Ex21.m1','A2.Ex22.m1','A2.E23.m1']:return 'B23-sharp-energy-proof-target'
 if id.startswith('A2.Thmtheorem3.') or id.startswith('A2.E22.') or id.startswith('A2.E24.'):return 'B22-B24-genuine-energy-consumer'
 if id.startswith('A2.Thmtheorem4.') or id in ['A2.E25.m1','A2.E26.m1']:return 'B4-decay-consumer-excluded-smallstep-dynamics'
 if id.startswith('A2.SS3.p5.') or id.startswith('A2.Ex1') or id.startswith('A2.E21.'):return 'B21-distinct-commutation-consumer-not-energy-premise'
 return 'B18-rho-contraction-context-excluded'
maps=[];items=[]
for name,a,z in regions:
 t=now();raw=b[a:z];(O/('source.'+name+'.RAW.html')).write_bytes(raw);(O/('source.'+name+'.LF.html')).write_bytes(raw.replace(b'\r\n',b'\n'));r=Render();r.feed(raw.decode());(O/('source.'+name+'.rendered.txt')).write_bytes(''.join(r.out).encode());count=0
 for m in re.finditer(rb'<math\b[^>]*>[\s\S]*?</math>',raw):
  x=m.group();ap=Attr();ap.feed(x[:x.index(b'>')+1].decode());at=ap.attrs;annotations=re.findall(rb'<annotation\b[^>]*encoding="application/x-tex"[^>]*>([\s\S]*?)</annotation>',x);tex=html.unescape(annotations[0].decode()) if annotations else None;alt=at.get('alttext');assert alt is not None and tex is not None and alt==tex
  items.append(dict(id=at['id'],region=name,source_RAW_range_end_exclusive=[a+m.start(),a+m.end()],RAW_sha256=H(x),RAW_bytes=len(x),alttext=alt,annotation_tex=tex,alt_annotation_exact=True,classification=role(at['id'],name),candidate67_seen=False,proof_or_compilation_claim=False));count+=1
 maps.append(dict(name=name,source_RAW_range_end_exclusive=[a,z],RAW_bytes=len(raw),RAW_sha256=H(raw),LF_sha256=H(raw.replace(b'\r\n',b'\n')),math_count=count,read_start_utc=t,read_end_utc=now()))
assert len(items)==344 and len(set(i['id'] for i in items))==344
prior=Path('E:/Samplinglib/runs/20261007-companion-priority/pbps-ambient-adjoint-preproof66/independent-primary66');old=json.loads((prior/'source-coverage-inventory.json').read_bytes());olditems=old.get('math_items',old.get('items'));new={tuple(x['source_RAW_range_end_exclusive']):x for x in items};reused=0
for x in olditems:
 key=tuple(x['RAW_byte_range']);assert key in new
 assert x['raw_math_sha256']==new[key]['RAW_sha256'];reused+=1
assert reused==310
put('source-input-regions.json',dict(schema='primary67-exact-six-region-RAW-LF-map-v1',whole_primary=pin(P),regions=maps,regions_end_exclusive=True,source_before_candidate=True))
put('source-coverage-inventory.json',dict(schema='primary67-complete-selected-source-inventory-v1',math_items=items,count=344,all_classified=True,missing_items=0,missing_alttext=0,missing_annotation=0,annotation_mismatch=0,classification_counts=dict(collections.Counter(x['classification'] for x in items)),reused_exact_primary66_items=310,new_selected_items=34,whole_paper_inventory_claim=False,candidate67_seen=False))
nodes=[
 ('source-inputs','C2 V; 0<alpha<=beta; global Hessian sandwich; eta>0,beta eta<=1 inclusive; original Euclidean source.',[],'source-hypotheses'),
 ('actual-joint-P','Actual pi_eta law; P conditional expectation given Y,HP=ranP,Hperp=kerP,HP0=HP intersect global meanzero.',['source-inputs'],'definition-prerequisite'),
 ('reflection-A','U actual selfadjoint involution, A=U_PP on HP; A selfadjoint, fixes constants, preserves HP0; block identities B5.',['actual-joint-P'],'derived-operator-prerequisite'),
 ('same-positive-root','SAME GammaP=(I-A^2)^(1/2), canonical positive root, B10/B11; D1 spectral calculus/unique nonnegative root.',['reflection-A'],'canonical-definition'),
 ('centered-inverse','B12/B15: gamma_gap=2sqrt(alpha eta)/(1+alpha eta)>0; Gamma0 exact HP0 restriction, Gamma0>=gamma I. Inv genuine two-sided bounded inverse HP0 only.',['same-positive-root','source-inputs'],'inherited-producer-conclusion'),
 ('same-polar-V','B16 B0=V0 Gamma0,V0=B0 Inv,V0*V0=I; no onto Hperp.',['centered-inverse','reflection-A'],'inherited-producer-conclusion'),
 ('actual-fP-fperp-fV','Every globally centered joint f: fP=Pf in SAME HP0,fperp=(I-P)f in kerP,fV=V0*fperp in SAME HP0; ambient/intrinsic adjoint adapter and norm budget.',['same-polar-V','actual-joint-P'],'inherited-SCI66-interface'),
 ('commute-root','A GammaP=GammaP A from GammaP spectral function of A; centered A0 Gamma0=Gamma0 A0 via exact invariance/restriction.',['same-positive-root','reflection-A'],'missing-compiled-boundary-source-backed'),
 ('commute-inverse','A0 Inv=Inv A0 internally from commute-root and genuine two-sided inverse; Inv selfadjoint. No full-space inverse.',['commute-root','centered-inverse'],'derived-prerequisite-not-public-premise'),
 ('X-centered','X=A0 Inv on HP0 is selfadjoint; I+X^2=Inv^2 using A0^2+Gamma0^2=I.',['commute-inverse','same-positive-root'],'sharp-bound-ingredient'),
 ('B20-C-definition','C(u,v)=1/2(||u||^2-||v||^2)-<A0 Inv u,v>, u,v in SAME HP0. B20 is definition, not bound.',['centered-inverse','reflection-A'],'target-definition'),
 ('Q-block','Q=[[I,-X],[-X,-I]] on HP0 direct-sum HP0; Q selfadjoint,Q^2=diag(Inv^2,Inv^2),||Q||=||Inv||<=1/gamma.',['X-centered','centered-inverse'],'sharp-bound-ingredient'),
 ('B23-sharp-pair','2C=< (u,v),Q(u,v)>; |C(u,v)|<=1/(2gamma)(||u||^2+||v||^2).',['Q-block','B20-C-definition'],'next-sharp-energy-target'),
 ('B23-actual-f','For actual globally centered f, |C(fP,fV)|<=1/(2gamma)||f||^2 via actual norm budget.',['B23-sharp-pair','actual-fP-fperp-fV'],'genuine-original-input-target'),
 ('B19-L-definition','L_omega(f)=||f||^2+omega C(fP,fV), initially omega>0.',['B20-C-definition','actual-fP-fperp-fV'],'definition-consumer'),
 ('B22-B24','If 0<omega<=gamma, |L_omega(f)-||f||^2|<=omega/(2gamma)||f||^2<=1/2||f||^2; hence 1/2||f||^2<=L<=3/2||f||^2.',['B23-actual-f','B19-L-definition'],'genuine-paper-energy-consumer'),
 ('B21-separate-consumer','Same root commutation allows centered inverse cancellation in V* U_perpperp=-A V*, idealized rotation and C change=-||fP||^2+||fV||^2. Not a parent of B23.',['commute-root','commute-inverse','same-polar-V','reflection-A','B20-C-definition'],'distinct-downstream-consumer-excluded-from-target'),
 ('B4-decay','B25/B26 later one-step Lyapunov decay adds universal constants, beta eta<=c0,halfturn/dynamics estimates.',['B22-B24','B21-separate-consumer'],'outbound-consumer-no-acceptance')]
graph=dict(schema='primary67-source-proof-graph-before-candidate-v1',built_utc=now(),actual_source_graph_pid=os.getpid(),source_before_candidate=True,independent_of_Lean_topology=True,nodes=[dict(id=i,statement=s,parents=parents,role=role) for i,s,parents,role in nodes],edges=[dict(parent=p,child=i,kind='source-proof-ingredient-not-caller-premise') for i,s,parents,role in nodes for p in parents],next_minimal_boundary='Derive SAME actual A/Gamma commutation, restrict to exact HP0 and derive SAME Inv commutation internally, with original caller inputs only. Sharp B23 remains downstream; B20 is its corrector definition.',no_candidate_verdict=True,no_mathematical_completion_claim=True)
put('source-proof-graph.json',graph)
put('primary-first-process.json',dict(schema='primary67-timed-primary-first-process-v1',started_utc=started,finished_utc=now(),actual_source_reconstruction_pid=os.getpid(),first_primary_read=json.loads((O/'first-primary-read.json').read_bytes()),whole_primary=pin(P),regions=maps,source_graph_written_before_current_shared_node_read=True,candidate67_seen=False,header67_seen=False,Lean67_seen=False,proof_search=False,prior_source_only_reuse=dict(source_inventory=pin(prior/'source-coverage-inventory.json'),source_graph=pin(prior/'source-proof-graph.json'),lease=pin(prior/'lease.final.json'),rechecked_exact_RAW_math_items=310),negative=dict(initial_tool_chunk='a619c2',initial_observer_exit=0,raw_source_console_truncated=True,resolution='Exact six RAW/LF regions, rendered transcripts and all344 alttext/annotation items retained; no missing source coverage or mathematical failure')))
print(json.dumps(dict(actual_pid=os.getpid(),source_items=len(items),regions=len(maps),graph_nodes=len(nodes),source_graph_RAW_sha256=H((O/'source-proof-graph.json').read_bytes()),inventory_RAW_sha256=H((O/'source-coverage-inventory.json').read_bytes()),source_graph_before_candidate=True),sort_keys=True))
