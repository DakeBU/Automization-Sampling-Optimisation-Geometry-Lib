from pathlib import Path
import json,hashlib,re,base64,os,sys
sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path('E:/Samplinglib');OWN=Path(__file__).resolve().parent;PRE=OWN.parent;BASE=PRE/'independent-source-baseline75'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(ROOT).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_sha256':sha(b.replace(b'\r\n',b'\n'))}
def load(p):return json.loads(p.read_bytes())
def dump(name,x):
 p=OWN/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n').encode());return pin(p)
def main():
 assert not (OWN/'lease.final.json').exists(),'Do not reopen CLOSED'
 before=(PRE/'header75.proposed.lean').read_bytes();after=(PRE/'header75.v2.proposed.lean').read_bytes()
 assert len(before)==4798 and sha(before)=='05ffee849dcf32541a948c1e9539550f122db34274e69d5b64397003de914263'
 assert len(after)==4809 and sha(after)=='00c9f04ff2d9ed037e3d8eab926a1cddc9fe3679a8b320267c641b86a0c243ee'
 proposal=load(PRE/'exact-API-overlay75.source-review-proposal.json')
 assert pin(PRE/'header75.proposed.lean')==proposal['before'] and pin(PRE/'header75.v2.proposed.lean')==proposal['proposed']
 old=proposal['exact_old'].encode();new=proposal['exact_new'].encode();assert before.count(old)==1 and before.replace(old,new)==after
 assert after.count(new)==1 and old not in after and proposal['occurrences']==1
 bl=load(BASE/'lease.final.json');assert bl['status']=='CLOSED_LAST' and bl['owned_count']==53
 for q in bl['all_owned_outputs_except_only_self']:assert pin(ROOT/q['path'])==q,q['path']
 brun=load(BASE/'run75.json');bsha=brun.pop('run_sha256');assert sha(canon(brun))==bsha==bl['whole_logical_run_sha256']
 bfreeze=load(BASE/'stageA.freeze75.json');fsha=bfreeze.pop('freeze_sha256');assert sha(canon(bfreeze))==fsha
 bim=load(BASE/'inputs.manifest75.json');assert bim['input_count']==22
 for q in bim['inputs']:
  assert {k:pin(ROOT/q['path'])[k]for k in ('path','RAW_bytes','RAW_sha256','LF_sha256')}=={k:q[k]for k in ('path','RAW_bytes','RAW_sha256','LF_sha256')}
  if 'snapshot'in q:assert (ROOT/q['path']).read_bytes()==(ROOT/q['snapshot']['path']).read_bytes()
 primary=(ROOT/bim['inputs'][0]['path']).read_bytes();assert sha(primary)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
 inv=load(BASE/'source-coverage-inventory75.json');graph=load(BASE/'source-proof-graph75.json');ex=load(BASE/'source-first.expectations75.json')
 assert inv['item_count']==137 and inv['classifications']=={'EXCLUDED':60,'NODE':77} and graph['node_count']==32 and graph['edge_count']==67
 for row in inv['items']:
  a,b=row['RAW_range'];assert sha(primary[a:b])==row['RAW_sha256']
 inputs=[]
 def add(path,kind,snapshot=False):
  q=pin(path);q['kind']=kind
  if snapshot:
   dst=OWN/'inputs'/f'{len(inputs):02d}.{path.name}.RAW';dst.parent.mkdir(exist_ok=True);dst.write_bytes(path.read_bytes());q['snapshot']=pin(dst)
  inputs.append(q);return q
 candidate=add(PRE/'header75.v2.proposed.lean','EXACT current prospective header',True)
 original=add(PRE/'header75.proposed.lean','EXACT historical API-name preimage only, not a compiled proposition',True)
 pp=add(PRE/'exact-API-overlay75.source-review-proposal.json','Root-authored exact proposal independently reviewed here',True)
 for name in ['stageA.freeze75.json','lease.final.json','run75.json','source-first.expectations75.json','source-proof-graph75.json','source-coverage-inventory75.json','inputs.manifest75.json','future-header-semantic-standards75.json','internal-completion-analysis75.md','source-literal-vs-inherited-bridges75.json','exact-source-formulas75.json','decision75.json','API-bounded-review75.json']:
  add(BASE/name,'Immutable own source-before-candidate CLOSED53 reference',False)
 api_ranges=[
 ('hitting-definition-typing','Mathlib/Probability/Process/HittingTime.lean',44,80,'Generic definition has Preorder/InfSet index only; no WellFoundedLT. NNReal index, lower0 and real target Ici0 preserve exact continuous first crossing.'),
 ('actual-unit-exponential','Mathlib/Probability/Distributions/Exponential.lean',90,100,'ProbabilityTheory.expMeasure (r:Real)=gammaMeasure1r; rate1 probability internally from zero_lt_one. Exact source Exp(1).'),
 ('exact-exponential-CDF','Mathlib/Probability/Distributions/Exponential.lean',163,172,'CDF at positive rate gives actual unit-rate survival and support; no iid/moment premises.'),
 ('gradient-Riesz-definition','Mathlib/Analysis/Calculus/Gradient/Basic.lean',50,84,'Gradient is inverse Riesz of fderiv, requires CompleteSpace. C2 makes derivative genuine; finite-dimensional real completeness is a typing consequence.'),
 ('finite-real-proper-instance','Mathlib/Analysis/Normed/Module/FiniteDimension.lean',550,564,'FiniteDimensional.proper_real supplies ProperSpace over Real without a Nontrivial E requirement.'),
 ('proper-completeness-instance','Mathlib/Topology/MetricSpace/ProperSpace.lean',100,108,'complete_of_proper supplies CompleteSpace from properness internally; not an original caller.'),
 ('WithTop-untopA-dual-definition','Mathlib/Order/WithBot.lean',253,269,'to_dual generates untopA; its arbitrary value at top is irrelevant because equality clause is guarded tau!=top.'),
 ('measure-map-definition','Mathlib/MeasureTheory/Measure/Map.lean',85,96,'Measure.map uses AEMeasurable or zero fallback. Joint Measurable tau plus continuous toNNReal must supply measurable pushforward; probability conclusion forbids accepting zero fallback.'),
 ('real-measure-definition','Mathlib/MeasureTheory/Measure/MeasureSpaceDef.lean',98,107,'Measure.real is toReal of measure; finite probability conclusion prevents infinity-to-zero pathology.'),
 ('real-toNNReal-definition-equation','Mathlib/Data/NNReal/Defs.lean',533,544,'coe_toNNReal=max r0. For nonnegative Lambda, tau(toNNReal r)>t iff r>Lambda(t); zero/nonnegative branches exact.')]
 apis=[]
 for name,path,a,b,meaning in api_ranges:
  parent=ROOT/'.lake/packages/mathlib'/path;whole=pin(parent);raw=parent.read_bytes();d=b''.join(raw.splitlines(keepends=True)[a-1:b]);frag=OWN/'API'/f'{name}.exactraw.lean-fragment';frag.parent.mkdir(exist_ok=True);frag.write_bytes(d)
  apis.append({'name':name,'whole_source':whole,'RAW_line_range':[a,b],'slice_recipe':'RAW splitlines(keepends=True)[start-1:end]; only then LF=CRLF->LF','fragment':pin(frag),'meaning':meaning,'proof_or_compile_credit':False});add(parent,'Fixed necessary Mathlib definition/typeclass parent, opaque whole-file pin',False)
 dump('exact-API-context75.json',{'schema':'pbps75-bounded-exact-API-context/v1','regions':apis,'new_75_implementation_or_proof_read':False,'typing_credit':'Source interpretation only; no fresh elaboration/typecheck/compile.'})
 oldstart=before.index(old);newstart=after.index(new)
 mapping={'schema':'pbps75-exact-one-API-name-overlay-map/v1','proposal':pp,'before':original,'proposed':candidate,'old_RAW_range':[oldstart,oldstart+len(old)],'new_RAW_range':[newstart,newstart+len(new)],'old_literal_UTF8':old.decode(),'new_literal_UTF8':new.decode(),'exact_replacement_occurrences':1,'prefix_RAW_sha256':sha(before[:oldstart]),'suffix_RAW_sha256':sha(before[oldstart+len(old):]),'prefix_identical':before[:oldstart]==after[:newstart],'suffix_identical':before[oldstart+len(old):]==after[newstart+len(new):],'byte_delta':len(after)-len(before),'all_other_bytes_identical':True,'source_law':'Actual fixed rate1 exponential marginal, no time rescaling or additional premise.','not_claimed':'Old unresolved/descriptive expMeasure1 name was not checked as an existing elaborated API; this is source-intent fidelity plus exact actual API verification, not a Lean theorem equivalence.'}
 mappin=dump('exact-API-overlay75.finite-map.json',mapping)
 text=after.decode();lines=text.splitlines(keepends=True)
 def span(a,b):
  start=text.index(a);end=text.index(b,start) if b else len(text);rawpart=text[start:end].encode();return {'RAW_range':[len(text[:start].encode()),len(text[:end].encode())],'line_start':text[:start].count('\n')+1,'line_end':text[:end].count('\n')+(not text[:end].endswith('\n')),'RAW_sha256':sha(rawpart),'LF_sha256':sha(rawpart.replace(b'\r\n',b'\n')),'RAW_bytes':len(rawpart),'literal':rawpart.decode()}
 private=span('private def actual_integrated_hazard_clock_statement','\ntheorem actual_integrated_hazard_clock_laws')
 public=span('theorem actual_integrated_hazard_clock_laws',None)
 assert text.rstrip().endswith(':= by') and 'sorry'not in text and 'axiom'not in text and 'admit'not in text
 pstart=text.index('{E : Type*}');pstop=text.index(' : Prop :=',pstart);pubstart=text.index('{E : Type*}',text.index('\ntheorem actual_integrated_hazard_clock_laws'));pubstop=text.index(' :\n    actual_integrated_hazard_clock_statement',pubstart)
 assert text[pstart:pstop]==text[pubstart:pubstop]
 binderraw=text[pstart:pstop].encode();binders={'private_RAW_range':[len(text[:pstart].encode()),len(text[:pstop].encode())],'public_RAW_range':[len(text[:pubstart].encode()),len(text[:pubstop].encode())],'complete_binder_text_identical':True,'RAW_bytes':len(binderraw),'RAW_sha256':sha(binderraw),'public_exact_private_application':'actual_integrated_hazard_clock_statement hα hαβ hV hH hη hβη','six_callers':['hα','hαβ','hV','hH','hη','hβη'],'five_typing_classes':['NormedAddCommGroup E','InnerProductSpace Real E','FiniteDimensional Real E','MeasurableSpace E','BorelSpace E'],'no_provider_or_extra_public_premise':True}
 lets=list(re.finditer(r'^    let ([^\s:]+)\s*:',text,re.M));assert [m[1]for m in lets]==['c','Φ','rate','H','C','Λ','τ','W']
 definitions=[]
 firstconj=text.index('    Continuous (fun a :')
 meanings=[('c',['N02'],'Exact y-eta gradientVxref.'),('Φ',['N03'],'Exact two actual harmonic components, SAME center; all real flow time inside integrand.'),('rate',['N04'],'Exact sqrteta max0 inner residual; max order commutes with source positive part.'),('H',['N06'],'Exact weighted SUM/2 with eta inverse, not product norm.'),('C',['N08','N17'],'Exact cap evaluated at SAME H(z), no independent E or cap input.'),('Λ',['N09','N10'],'Actual Lebesgue time interval integral with NNReal endpoint, no default arbitrary hazard.'),('τ',['N12'],'Canonical generic hittingAfter at lower0, target Ici0 of Lambda-e, WithTop NNReal; tuple projections correctly select y,xRef,z,e.'),('W',['N20','N21','N22'],'Actual expMeasure rate1 pushforward through tau/toNNReal, no independent random variable or probability premise.')]
 for i,m in enumerate(lets):
  end=lets[i+1].start() if i+1<len(lets) else firstconj;rawpart=text[m.start():end].encode();nm,nn,meaning=meanings[i]
  definitions.append({'name':nm,'RAW_range':[len(text[:m.start()].encode()),len(text[:end].encode())],'line_start':text[:m.start()].count('\n')+1,'line_end':text[:end].count('\n'),'RAW_bytes':len(rawpart),'RAW_sha256':sha(rawpart),'literal':rawpart.decode(),'source_nodes':nn,'decision':'EXACT actual definition, internal value not provider','meaning':meaning})
 conjend=text.index('\ntheorem actual_integrated_hazard_clock_laws');conjtext=text[firstconj:conjend];chunks=[];depth=0;begin=0
 for i,ch in enumerate(conjtext):
  if ch in '([{':depth+=1
  elif ch in ')]}':depth-=1
  elif ch=='∧'and depth==0:chunks.append((begin,i));begin=i+1
  assert depth>=0
 assert depth==0;chunks.append((begin,len(conjtext)));assert len(chunks)==10
 clauseinfo=[
 ('Joint hazard continuity',['N09','N10'],'Continuous in ALL(y,xRef,z,t) with t NNReal; a.1.1.1=y,a.1.1.2=xRef,a.1.2=z,a.2=t.'),
 ('Joint hazard Borel',['N10'],'Measurable same tuple/time. It is a conclusion, no measurable-integrand premise.'),
 ('Finite-interval integrability',['N10'],'All original states and every finite nonnegative endpoint; real Lebesgue intervalIntegral integrand actual rate∘flow.'),
 ('Normalized monotone nonnegative hazard',['N11'],'Lambda0=0, every value>=0, Monotone on NNReal. Real codomain is finite at every finite t.'),
 ('Exact finite-time first-crossing identity',['N13','N15'],'tau<=cast t iff e<=Lambda t, all e,t NNReal, including e0/infinity output.'),
 ('Infinity/attainment/positive/zero branches',['N13','N14','N24'],'top iff ALL finite times have Lambda<e; finite tau equality uses guarded untopA; e>0->tau>0; tau0=0.'),
 ('Joint clock Borel',['N16'],'Measurable on right-associated((y,xRef),(z,e)), matching hittingAfter parameter projections exactly; no clock continuity assumption.'),
 ('Actual one-clock probability and survival',['N20','N21','N22','N23'],'IsProbabilityMeasure W plus real measure of strict Ioi(cast t)=exp(-Lambda t); infinity remains in survival tail.'),
 ('Exact actual cap and integrated bound',['N17','N18'],'C>=0 and Lambda t<=C*t at SAME starting energy H(z), all finite nonnegative times; actual orbit conservation is proof obligation.'),
 ('Extended wait lower bound/zero cap',['N19','N24'],'Positive C is scoped antecedent, not caller; toNNReal ratio equals e/C when C>0. C0 and positive e give top; e0 still0 from clause6.')]
 clauses=[]
 for i,((a,b),(label,nn,meaning))in enumerate(zip(chunks,clauseinfo),1):
  a0=firstconj+a;b0=firstconj+b;rawpart=text[a0:b0].encode()
  clauses.append({'clause_id':f'C{i:02d}','label':label,'RAW_range':[len(text[:a0].encode()),len(text[:b0].encode())],'line_start':text[:a0].count('\n')+1,'line_end':text[:b0].count('\n')+1,'RAW_bytes':len(rawpart),'RAW_sha256':sha(rawpart),'literal':rawpart.decode(),'source_nodes':nn,'independent_source_decision':'PRESERVED prospective source/mathematical-completion contract; unproved','meaning':meaning})
 linecoverage=[]
 for i,line in enumerate(lines,1):
  off=len(''.join(lines[:i-1]).encode());end=off+len(line.encode());refs=[q['name']for q in definitions if q['RAW_range'][0]<end and q['RAW_range'][1]>off]+[q['clause_id']for q in clauses if q['RAW_range'][0]<end and q['RAW_range'][1]>off]
  if i<=6:kind='necessary import declarations; no theorem application/compile credit'
  elif i<17:kind='source-only comment / namespace / typing configuration / private literal record name'
  elif off<definitions[0]['RAW_range'][0]:kind='complete private original six analytic callers and typing'
  elif off>=public['RAW_range'][0]:kind='complete public same six callers/private-literal application; empty by tail is no proof'
  else:kind='full actual definition or full conjunction contract; no75 BODY'
  linecoverage.append({'line':i,'RAW_range':[off,end],'RAW_sha256':sha(line.encode()),'kind':kind,'refs':refs,'reviewed':True})
 statementpin=dump('complete-header-expansion75.json',{'schema':'pbps75-complete-header-definition-expansion/v1','candidate':candidate,'line_count':len(lines),'private_literal':private,'public_header':public,'binders':binders,'eight_let_definitions':definitions,'ten_top_conjunctions':clauses,'all_header_lines':linecoverage,'BODY_absent':True,'prospective_file_end':'Deliberate empty := by tail, no completed theorem/closed sections/typecheck/compile claimed.'})
 overlaydecision={'schema':'pbps75-independent-exact-API-overlay-decision/v1','actor':'/root/independent_primary69','proposal_author':'root sole canonical writer','exact_proposal':pp,'exact_before':original,'exact_proposed':candidate,'finite_byte_map':mappin,'decision':'ACCEPT_EXACT_PROPOSAL_ONLY','source_law_preserved':'The replacement is exactly the pinned existing rate1 exponential law matching A.1 Exp(1). No parameters, binders, cap, survival coefficient, time scale, process or cost statement changes.','required_repair':[],'not_self_authored_proposal':'Source baseline anticipated the actual API, but this concrete byte proposal and candidate are root authored. This actor only independently compares their exact bytes and fixed source/API.','not_a_Lean_equivalence_of_old_unresolved_name':True,'no_75_Lean_compile_or_verification_credit':True,'permitted_root_action':'Apply only these exact proposed header bytes after root admission; no other field/source/topology/mathematical changes authorized by this review.'}
 overlaypin=dump('exact-API-overlay75.decision.json',overlaydecision)
 # Seven source slots are independently authored; no other header-math review loaded.
 sourceids={'objects':['S3.E4','A1.Ex1','A1.Ex2','A1.Ex4','A1.Ex6','A1.E1'],'domains':['S1.p1.1','S2.SS2.p1.1','A1.SS1.p1.1','A1.SS1.p2.2'],'quantifiers':['A1.SS1.p1.1','S3.Thmtheorem1','A1.E1'],'assumptions':['S1.p1.1','S1.E1','S2.SS2.p1.1'],'conclusion':['A1.E1','A1.SS1.p2.2','A1.Ex7','A1.Ex8'],'scopes_senses':['A1.E1','A1.E2','A1.Ex9','A1.SS1.p3.7'],'constant_dependencies':['A1.Ex1','A1.Ex2','A1.Ex4','A1.Ex6','A1.Ex7','A1.Ex8']}
 slottxt={
 'objects':'All eight lets are exact SAME actual values; h residual is inlined in rate. No arbitrary hazard, cap or law supplied; W fixes actual rate1 Exp measure. c/Phi/rate/H/C/Lambda/tau/W preserve source meanings.',
 'domains':'Five ordinary typing classes on one finite real Hilbert/Borel carrier; alpha,beta NNReal are equivalent to source nonnegative constants under0<alpha<=beta. y,xRef,z arbitrary. Continuous-time NNReal, threshold including0, WithTop NNReal wait includingtop; rank0 legal.',
 'quantifiers':'Private/public six analytic binder strings identical. All ten conclusions quantify original y,xRef,z; e,t are nonnegative inputs under conclusions. Positive C, positive e and finite tau are scoped antecedents, not extra public hypotheses; no independence/probability/integrability/provider binder.',
 'assumptions':'Source C2, whole Hessian quadratic bounds,0<alpha<=beta,eta>0,betaeta<=1 exactly retained. Twice fderiv V applied v,v is the real source Hessian quadratic form, not an extra regularity assumption. Completeness follows finite real dimension internally. No Nontrivial, positive energy, unbounded hazard, finite wait or WellFoundedLT premise.',
 'conclusion':'Ten top conjuncts exactly express frozen prospective primitive/clock/survival/bound contract. Finite wait equality uses untopA only under tau!=top. Empty crossing top iff every finite Lambda<e is equivalent; e0=0 and zero cap positive threshold infinity both explicit. This accepts statement meaning only; all proofs remain absent.',
 'scopes_senses':'Generic hittingAfter definition instantiated on NNReal continuous time and actualLambda-e, not discrete theorem. Tuple parameter projections exact. Measure.map default0 cannot legalize nonmeasurability: joint Measurable tau and IsProbabilityMeasure W are conclusions. W.real is probability toReal under finite probability, strict Ioi includes possible infinity. No recursive path, Markov/nonexplosion/kernel/stationarity or reader claim.',
 'constant_dependencies':'Exact sqrteta, -sin/sqrteta, eta inverse, energy half, max0 actual residual, beta and sqrt2 energy radii retained; C uses SAME H(z). Exp rate exactly1, survival exp(-Lambda); lower wait uses e/C only within C>0, with exact toNNReal nonnegative ratio. No refresh, extra2, arbitrary C, cost or source rho.'}
 slots=[{'slot':k,'verdict':'equivalent-after-definition-expansion (prospective header only)','baseline_criterion':load(BASE/'future-header-semantic-standards75.json')[k],'independent_comparison':slottxt[k],'source_anchors':sourceids[k],'candidate_evidence':statementpin,'blocker':False}for k in sourceids]
 obligationlinks={
 'O01':['binders'],'O02':['binders'],'O03':['c','Φ','rate','H','C','Λ','τ','W'],'O04':['Φ'],'O05':['rate'],'O06':['binders','rate'],'O07':['H'],'O08':['C'],'O09':['Φ','H','C','C09'],'O10':['C03'],'O11':['Λ','W'],'O12':['Λ','τ','C05'],'O13':['C01','C02','C03','C04'],'O14':['τ','C06'],'O15':['τ','C05','C06'],'O16':['C05'],'O17':['C06'],'O18':['C06'],'O19':['C07'],'O20':['W','C08'],'O21':['W','C08'],'O22':['C08'],'O23':['C10'],'O24':['C06','C10'],'O25':['binders','H','C06','C10'],'O26':['binders','C06','C10'],'O27':['C06','C10'],'O28':['τ'],'O29':['C08'],'O30':['private_literal','public_header'],'O31':['source_graph','source_inventory'],'O32':['public_header']}
 obligations=[{**q,'header_decision':'SOURCE EXPECTATION PRESERVED; no extra binder/false conclusion','candidate_links':obligationlinks[q['id']],'proof_status':'OPEN / no75 BODY or compile','reader_status':'not admitted; full private record must be exposed adjacent later'if q['id']=='O30'else'no reader credit'}for q in ex['future_header_obligations']]
 noderefs={
 'N01':['binders'],'N02':['c','rate'],'N03':['Φ'],'N04':['rate'],'N05':[],'N06':['H'],'N07':['Φ','H','C09'],'N08':['C'],'N09':['Λ'],'N10':['Λ','C01','C02','C03'],'N11':['C04'],'N12':['τ'],'N13':['τ','C05','C06'],'N14':['C06'],'N15':['C05'],'N16':['C07'],'N17':['C','C09'],'N18':['C09'],'N19':['C10'],'N20':['W'],'N21':['W','C08'],'N22':['W','C08'],'N23':['C08'],'N24':['C06','C10'],'N25':['τ'],'N26':[],'N27':[],'N28':[],'N29':[],'N30':[],'N31':['binders','rate']}
 nodeprojection=[]
 for n in graph['nodes']:
  status='OPEN_DOWNSTREAM_NOT_CLAIMED'if n['kind'].startswith('OPEN')or n['kind']=='EXCLUDED_SOURCE_CONTEXT'else'INHERITED_CONTEXT_ONLY_NO_HEADER_ASSERTION'if n['id']=='N05'else'EXACT_HEADER_CONTRACT_PROOF_OPEN'
  nodeprojection.append({'source_node':n['id'],'source_kind':n['kind'],'candidate_links':noderefs[n['id']],'header_projection':status,'all_source_gaps_unproved':True,'source_graph_unchanged':True})
 projections=[]
 for q in inv['items']:
  projections.append({'item_id':q['item_id'],'source_id':q['source_id'],'source_RAW_range':q['RAW_range'],'source_RAW_sha256':q['RAW_sha256'],'StageA_classification':q['classification'],'StageA_reason_retained':q['reason'],'nodes':q['nodes'],'header_links':list(dict.fromkeys(v for n in q['nodes']for v in noderefs[n])),'decision':'RETAINED EXCLUSION; no candidate credit'if q['classification']=='EXCLUDED'else'SOURCE NODE PROJECTED; prospective definitions/conclusions or explicit open context, not proof completion'})
 edgeprojection=[{'source_edge':e['id'],'producer':e['producer'],'consumer':e['consumer'],'kind':e['kind'],'header_only_status':'SOURCE relation unchanged; no75 formal implication/producer proof credited'}for e in graph['edges']]
 coverage={'schema':'pbps75-exhaustive-prospective-header-source-coverage/v1','baseline_inventory':pin(BASE/'source-coverage-inventory75.json'),'baseline_source_graph':pin(BASE/'source-proof-graph75.json'),'candidate':candidate,'counts':{'source_items':137,'NODE':77,'EXCLUDED':60,'source_nodes':32,'source_edges':67,'future_obligations':32,'internal_bridges_OPEN':13,'public_analytic_callers':6,'private_and_public_typing_classes':5,'let_definitions':8,'top_conjunctions':10,'header_lines':len(lines),'seven_semantic_slots':7},'source_items':projections,'source_nodes':nodeprojection,'source_edges':edgeprojection,'future_obligations':obligations,'candidate_definition_and_full_line_coverage':statementpin,'immutable_source_projection_not_Lean_dependency_graph':True,'new_source_graph_or_classification':False}
 covpin=dump('header-source-coverage75.json',coverage)
 deltas=[
 {'slot':'objects','severity':'informational','description':'Exact root API name overlay replaces descriptive/unresolved expMeasure1 with pinned expMeasure(1). Source unit-rate marginal unchanged.','evidence':'exact-API-overlay75.finite-map.json and fixed Exponential.lean96/98/165'},
 {'slot':'domains','severity':'informational','description':'Finite real Hilbert/Borel type representation and NNReal/WithTop carriers encode source continuous nonnegative time/infinity; no dimension positivity.','evidence':'complete private/public binder and tau definition; StageA O02/O12/O14'},
 {'slot':'assumptions','severity':'informational','description':'Twice real fderiv represents original Hessian quadratic bound; gradient completeness is finite-real typing consequence. Original six assumptions retained, no producer supplied as caller.','evidence':'binders and gradient/proper/complete fixed API fragments'},
 {'slot':'conclusion','severity':'informational','description':'Ten conclusions make suppressed elementary crossing/Borel/probability completions explicit. This is no proof of those thirteen internal bridges.','evidence':'StageA source graph N09–N24 typed internal bridge projection; ten exact header clauses'},
 {'slot':'scopes_senses','severity':'informational','description':'Measure.map/Measure.real default conventions are controlled by explicit measurability/probability conclusions; untopA equality is finite-guarded. No recursive process or a.s.finite clock claim.','evidence':'W,C06,C07,C08 and fixed map/real/untopA definitions'},
 {'slot':'constant_dependencies','severity':'informational','description':'max0 inner equals source positive part; real.toNNReal of e/C under C>0 preserves nonnegative ratio. Exact energy/cap/Exp constants unchanged.','evidence':'rate,C,C10 and NNReal coe_toNNReal definition'}]
 review={'schema':'pbps75-independent-complete-prospective-header-source-review/v1','actor':'/root/independent_primary69','status':'ACCEPT_PROSPECTIVE_HEADER_SOURCE_ONLY','candidate':candidate,'source_before_candidate_freeze':pin(BASE/'stageA.freeze75.json'),'source_before_candidate_logical':fsha,'exposure':{'prior70_74_header_and_BODY_source_exposure':True,'CLOSED86_source_plan_visible_in_StageA':True,'StageA_frozen_before_any75_candidate_hash_or_header_read':True,'current_v2_and_original_header_now_seen':True,'any75_BODY_seen':False,'other_header_math75_decision_verdict_payload_seen':False,'source_blind_claim':False},'semantic_slots':slots,'deltas':deltas,'blocking_deltas':[],'required_source_or_header_repair':[],'complete_header_expansion':statementpin,'coverage':covpin,'exact_API_overlay_independent_decision':overlaypin,'definition_semantics_findings':['Private literal is fully defined actual statement record, no provider/certificate. Public exact six binders only assert it; empty by tail supplies no proof.','SAME tuple groupings correctly thread y/xRef/z/e and time; no argument swap.','Generic hittingAfter definition preserves explicit infinity empty branch; WellFoundedLT theorem is not used or assumed.','Finite equality uses untopA under tau!=top, so arbitrary default is irrelevant.','W joint map measurability and probability must be internally proved; real measure convention matches finite probability survival.','C is actual H(z) cap on one flow segment, not stochastic-path producer or original-energy recursion claim.'],'retained_vs_used':ex['retained_vs_used'],'remaining_OPEN':['all13 internal completion bridges and all75 proof obligations','true postjump input state and A2 measurable recursion','global initial-energy cap through bounce recursion','iid Exp realization/support/moments/SLLN/nonexplosion','memorylessness/Markov/stationarity/reversal/semigroup','actual terminal H/K/r_rho/B27/B28','main/error/cap/query-cost/composition','independent final implementation/source/decoder admission','aggregate/runtime reader/Exposition/PURIFIED/main/live/wholepaper/Goal'],'no_Lean_typecheck_or_compile':True,'no_new_SAU_ledger_Goal_or_canonical_writes':True,'source_attribution':'Frozen StageA exact source URLs and23 source formulas remain authority; future publication attribution not yet supplied or admitted.'}
 reviewpin=dump('review75.json',review)
 decision={'schema':'pbps75-independent-prospective-header-and-exact-API-source-decision/v1','actor':'/root/independent_primary69','verdict':'ACCEPT_PROSPECTIVE_HEADER_SOURCE_AND_EXACT_API_OVERLAY_ONLY','candidate':candidate,'exact_proposal':pp,'exact_overlay_decision':overlaypin,'review':reviewpin,'coverage':covpin,'semantic_slots':slots,'deltas':deltas,'blocking_count':0,'required_repairs':[],'source_graph_unchanged':pin(BASE/'source-proof-graph75.json'),'StageA_inventory_unchanged':pin(BASE/'source-coverage-inventory75.json'),'source_before_candidate_freeze':pin(BASE/'stageA.freeze75.json'),'counts':coverage['counts'],'Statement_Seal_written':False,'Lean_compile':False,'SAU_claim':False,'VERIFIED':False,'reader_Exposition_PURIFIED_main_cost_wholepaper_Goal_credit':False,'prospective_only':'Source meaning/assumption/definition acceptance of this exact unproved v2 header, not a semantic roundtrip on implementation or completion of A1/A2/Proposition3.1.'}
 decpin=dump('decision75.json',decision)
 manifest={'schema':'pbps75-header-source-finite-input-manifest/v1','current_input_count':len(inputs),'current_inputs':inputs,'reused_StageA_input_count':22,'reused_StageA_inputs':bim['inputs'],'prior_CLOSED53_verified_members':52,'source_topology_copied_or_rewritten':False,'fixed_primary_reference':bim['inputs'][0],'bounded_Mathlib_API_context':pin(OWN/'exact-API-context75.json'),'LF_recipe':'ONLY CRLF bytes->LF; preserve bareCR/all other bytes. RAW snapshots authoritative; source/API RAW line slicing precedes LF conversion.','no75_BODY_or_other_math_verdict_input':True}
 dump('inputs.manifest75.json',manifest)
 dump('observer-negatives75.json',{'schema':'pbps75-header-source-observer-negatives/v1','negative_locator_queries':[{'description':'Bounded rg included a guessed nonexistent Order/WithBotTop directory; exact real WithBot.lean to_dual untopA declaration subsequently located.','terminal_PID':'not exposed by shell tool, not guessed','EXIT_credit':'No successful check credited to diagnostic query; exact current fixed-source snapshot independently verified by actual review process.'},{'description':'Guessed Measure/Defs.lean and Basic.lean paths were absent; rg --files then identified actual MeasureSpaceDef.lean, exact Measure.real definition checked.','terminal_PID':'not exposed by shell tool, not guessed','EXIT_credit':'No mathematical negative or compiler failure; locator error only.'}],'canonical_or_candidate_changes':False,'no_proof_or_typecheck_attempt':True})
 dump('terminal.review75.json',{'actual_PID':os.getpid(),'actual_EXIT':0,'phase':'independent whole prospective header and exact API overlay source review','current_input_count':len(inputs),'reused_source_input_count':22,'immutable_StageA53_members_verified':52,'candidate_header_lines':len(lines),'let_defs':8,'conjunctions':10,'source_items':137,'slots':7,'blockers':0,'proof_or_compile_attempt':False})
 print(json.dumps({'actual_PID':os.getpid(),'actual_EXIT':0,'status':decision['verdict'],'candidate':candidate,'exact_API_map':mappin,'review':reviewpin,'decision':decpin,'counts':coverage['counts'],'current_inputs':len(inputs),'reused_inputs':22},ensure_ascii=False,sort_keys=True))
if __name__=='__main__':main()
