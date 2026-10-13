import sys
sys.dont_write_bytecode=True
sys.stdout.reconfigure(encoding='utf-8')
import pathlib,json,hashlib,re,os,datetime
B=pathlib.Path('E:/Samplinglib');O=pathlib.Path(__file__).resolve().parent;REL=O.relative_to(B).as_posix()
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def pin(p):
 b=p.read_bytes();lf=b.replace(b'\r\n',b'\n');return {'path':p.relative_to(B).as_posix(),'RAW_bytes':len(b),'RAW_sha256':sha(b),'LF_bytes':len(lf),'LF_sha256':sha(lf)}
rawpath=B/'runs/20261007-companion-priority/phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html';raw=rawpath.read_bytes();assert len(raw)==1482128 and sha(raw)=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
primary=json.loads((O/'stageA.primary255.independent-inventory72.json').read_bytes())['entries'];b1=json.loads((O/'stageA.supplement-B1-framework.inventory72.json').read_bytes());b2=json.loads((O/'stageA.supplement-B2-domain.inventory72.json').read_bytes());discovery=json.loads((O/'stageA.supplementary-discovery72.json').read_bytes())
supp={x['math_id']:x for x in [*b1['entries'],*b2['entries'],*[x for x in discovery['items'] if re.match(r'A2\.E1[2-6]\.',x['math_id'])]]};supp=sorted(supp.values(),key=lambda x:x['RAW_start']);assert len(primary)==255 and len(supp)==106
for x in [*primary,*supp]:assert sha(raw[x['RAW_start']:x['RAW_end_exclusive']])==x['RAW_sha256']
prior= B/'runs/20261007-companion-priority/pbps-actual-corrector-change71/independent-source71'
priorpins=[pin(prior/n) for n in ['lease.final.json','owned-manifest.json','stageA.source-expectations71.before-current-BODY.frozen.json','stageA.source-proof-graph71.before-current-BODY.frozen.json','stageA.primary255.reparsed-inventory.json']]
# Opaque prior closure/graph pins support immutable reuse and exposure disclosure, never a72 verdict.
assert priorpins[0]['RAW_sha256']=='0a87027cc6ecc00329097327a66026d2b4ac4afc46005fd4e3351c17632fd187'
write('stageA.prior71-readonly-pins72.json',{'schema':'source72-prior-exposure-and-immutable-anchor-pins-v1','inputs':priorpins,'prior71_verdict_used_as72_acceptance':False,'prior_closed_files_written':False,'reuse':'Same fixed primary and unchanged six-caller/twelve-witness source background; new target graph and classification independently authored from RAW before72header.'})
nodespec=[
('S00','Real AE L2 and centered HP0','definition',['A4.E1.m1','A4.E2.m1'],'Real Hilbert equivalence classes; inverse/perturbations stay on the same centered macro space.'),
('S01','PBPS analytic hypothesis background','source-hypotheses',['S1.p1.m3','S1.p1.m4','S1.E1.m1','A2.Thmtheorem1.p1.m1'],'Same C2 potential,alpha>0,alpha<=beta,both Hessian bounds,eta>0,beta eta<=1; six existing analytic callers retained.'),
('S02','Actual P, residual, macro/micro domains','definition',['A2.E1.m1','A2.E2.m1','A2.SS1.p1.m13'],'P=conditional expectation given Y,R=Pperp; micro is all kerP, not ranV.'),
('S03','Same actual reflection U','retained-ingredient',['A2.E4.m1','A2.E5.m1'],'AE pullback by(x,2x-y),self-adjoint/unitary,not arbitrary coefficient operator.'),
('S04','Same centered compression A','retained-ingredient',['A2.E3.m1','A2.SS3.p5.m12'],'Restriction/transport of PUP to the same HP0,real self-adjoint.'),
('S05','Same positive root Gamma and centered inverse J','retained-ingredient',['A2.E12.m1','A2.E15.m1','A2.SS3.p4.m2','A2.SS3.p4.m3'],'Gamma=(I-A²)^1/2; bounded two-sided inverse on HP0 only; no inverse across constants.'),
('S06','Self-adjointness, commutation and squaresum','proof-ingredient',['A2.SS3.p5.m20','A2.SS3.p7.m1','A2.SS3.p7.m2','A2.SS3.p7.m3'],'A,Gamma,J self-adjoint; A commutes withGamma andJ; A²+Gamma²=I; inverse SA/commutation are internal functional-calculus/inverse consequences.'),
('S07','Same polar isometric embedding V','retained-ingredient',['A2.E16.m1','A2.Ex8.m1'],'V:HP0->allkerP isometric,not onto; adjoint maps microscopic vectors into HP0.'),
('S08','Actual centered f and actual ideal g components','actual-input',['A2.Ex6.m1','A2.Ex10.m1','A2.Ex11.m1','A2.SS3.p5.m7'],'f globally centered; g=U(Pf-(f-Pf)),gP=Pg,gV=V*Rg; mean_g internal reflection-law/conditional-integral completion.'),
('S09','Exact B20 corrector','definition',['A2.E20.m1'],'C(u,v)=(||u||²-||v||²)/2-inner(A(Ju),v); same A/J and same HP0.'),
('S10','Arbitrary centered perturbation pair','algebraic-abstraction',['A2.E27.m1','A2.Ex28.m1'],'For u,v,r in the same real H,form u+Gamma r and v-A r; r here is an arbitrary perturbation vector,not source residual r orrrho.'),
('S11','Full norm/cross expansion','proof-step',['A2.Ex28.m1','A2.Ex29.m1','A2.Ex30.m1'],'Expand B20 at the perturbed pair,using JGamma=I.'),
('S12','Cancellation of v terms','proof-step',['A2.Ex31.m1'],'Real inner symmetry cancels +inner(v,Ar)-inner(Ar,v).'),
('S13','Linear terms become inner(u,Jr)','proof-step',['A2.Ex32.m1','A2.Ex33.m1'],'A/Gamma/J self-adjoint commutation and squaresum give Gamma+J A²=J.'),
('S14','Quadratic terms become norm(r)^2/2','proof-step',['A2.Ex34.m1'],'||Gamma r||²+||Ar||²=||r||²,with exact positive half.'),
('S15','Generic Hilbert perturbation leaf','prospective-target',['A2.Ex28.m1','A2.Ex33.m1','A2.Ex34.m1'],'C(u+Gamma r,v-A r)-C(u,v)=inner(u,Jr)+||r||²/2; independent of B21.'),
('S16','Actual PBPS original-input specialization','prospective-target',['A2.Ex11.m1','A2.Ex28.m1','A2.Ex33.m1','A2.Ex34.m1'],'Specialize generic identity to already produced actual gP,gV and same root/inverse. If still forallr:HP0,this is a bounded perturbation consumer,not actualK orrrho construction.'),
('S17','Actual half-turn H and Markov K difference','open-actual-adapter',['A2.E6.m1','A2.E7.m1','A2.Ex23.m2','A2.Ex24.m1'],'H is source conditional half-turn/Markov operator; K=U[P+(1-rho)Hmicro]. Need actual semantics,not arbitrary H.'),
('S18','Actual residual rrho and centeredness','open-actual-adapter',['A2.Ex27.m1'],'rrho=V*[I+(1-rho)Hmicro]fperp=rho fV+(1-rho)r_source; r_source=V*(I+Hmicro)fperp; both centered by codomain.'),
('S19','B27 actual output components','open-actual-adapter',['A2.Ex25.m2','A2.Ex26.m2','A2.E27.m1'],'(Kf)P=gP+Gamma rrho,(Kf)V=gV-A rrho via same polar and all-micro intertwining.'),
('S20','Actual ideal B21 change','retained-separate-edge',['A2.Ex16.m1','A2.Ex17.m1','A2.E21.m1'],'C(gP,gV)-C(fP,fV)=-||fP||²+||fV||²; inherited actual edge,not parent of S15.'),
('S21','B28 combined real consumer','open-real-consumer',['A2.Ex35.m1','A2.Ex36.m1','A2.E28.m1'],'Combine actual B27/S15 at rrho with actual B21; adds inner(gP,Jrrho)+||rrho||²/2.'),
('S22','Residual norm/Young bounds','open-real-consumer',['A2.E29.m1','A2.E30.m1','A2.Ex38.m1','A2.E31X.m2'],'B29/B30/B31 use separate B17 error,centered gap and rho/constant bounds; outside prospective perturbation header.'),
('S23','Full B4 Lyapunov decay/main boundary','open-real-consumer',['A2.E25.m1','A2.E26.m1','A2.Ex45.m1'],'FullB4 needs ordinary norm decay,norm equivalence,smallc0,omega/rho/Lambda estimates; no whole-paper/main/errors/cost/Goal credit.')]
nodes=[{'id':a,'label':b,'kind':c,'source_math_ids':d,'meaning':e} for a,b,c,d,e in nodespec]
edgepairs=[('S00','S02'),('S01','S03'),('S02','S03'),('S02','S04'),('S03','S04'),('S00','S05'),('S01','S05'),('S04','S05'),('S04','S06'),('S05','S06'),('S00','S07'),('S03','S07'),('S05','S07'),('S00','S08'),('S02','S08'),('S03','S08'),('S07','S08'),('S04','S09'),('S05','S09'),('S00','S10'),('S09','S10'),('S09','S11'),('S10','S11'),('S05','S11'),('S11','S12'),('S00','S12'),('S06','S13'),('S12','S13'),('S06','S14'),('S13','S15'),('S14','S15'),('S08','S16'),('S15','S16'),('S02','S17'),('S03','S17'),('S07','S18'),('S08','S18'),('S17','S18'),('S03','S19'),('S07','S19'),('S17','S19'),('S18','S19'),('S08','S20'),('S09','S20'),('S06','S20'),('S15','S21'),('S18','S21'),('S19','S21'),('S20','S21'),('S21','S22'),('S05','S22'),('S17','S22'),('S22','S23')]
edges=[{'id':f'E{i:02}','from':a,'to':z,'relation':'source-proof-ingredient-or-explicit-open-adapter','reason':next(x['meaning'] for x in nodes if x['id']==z),'Lean_dependency_claim':False} for i,(a,z) in enumerate(edgepairs)]
graph={'schema':'source72-primary-first-independent-source-proof-graph-v1','nodes':nodes,'edges':edges,'node_count':len(nodes),'edge_count':len(edges),'generic_leaf_node':'S15','actual_original_input_node':'S16','generic_leaf_has_B21_dependency':False,'forbidden_edges':[{'from':'S20','to':'S15','reason':'B21 concerns the ideal rotation change and is not used by arbitrary perturbation algebra.'},{'from':'S16','to':'S19','reason':'An arbitrary centered perturbation identity does not construct rrho,actualH/K orB27 components.'}],'graph_layer':'Source mathematics and explicit obligations,not implementation Lean DAG or proof-completion graph.','candidate72_read':False}
write('stageA.source-proof-graph72.before-header.frozen.json',graph)
byid={x['math_id']:x for x in [*primary,*supp]}
for n in nodes:
 for mid in n['source_math_ids']:assert mid in byid,mid
def classify(x,is_supp):
 mid=x['math_id'];role=[];reason=''
 if is_supp:
  if mid.startswith('A2.SS2.p4.') or mid=='A2.E13.m1':return 'EXCLUDED',[],'Separate conditional-variance/gradient/Poincare proof detail; not required for this perturbation leaf or original-input header. Existing quantitative parent facts remain retained,not re-proved.'
  if x.get('supplement_region')=='B1-framework':role=['S02','S03','S04','S17'];reason='Exact B1 operator/kernel/half-turn/micro-macro context for SAME actual-input adapters; attribution only,actualH/K obligations stay open.'
  else:role=['S04','S05','S07'];reason='Exact retained B2 reflection/root/gap/polar domain background. No sharp-energy estimate is made a dependency.'
 elif x['region']=='global-assumptions':
  if mid in {'S1.p1.m1','S1.p1.m2','S1.p1.m3','S1.p1.m4','S1.E1.m1'}:role=['S01'];reason='Original normalized potential/space/C2/curvature hypotheses; six analytic caller background retained.'
  else:return 'EXCLUDED',[],'Introduction main-sampling/warm-start/query-complexity/comparison material; no role in the bounded perturbation header.'
 elif x['region']=='real-L2-spectral-conventions-D1':
  if mid.startswith(('A4.Thmtheorem1.','A4.SS1.p1.','A4.SS1.p2.')) or mid in {'A4.E1.m1','A4.E2.m1','A4.E3.m1'}:role=['S00','S06'];reason='Real AE Hilbert,projection,adjoint/self-adjoint/spectral conventions for same centered operators and inner transport.'
  elif mid in {'A4.Thmtheorem2.p1.m1','A4.Thmtheorem2.p1.m2','A4.Thmtheorem2.p1.m3','A4.E4.m1'}:role=['S17'];reason='Observable Markov operator definition distinguishes actual K from arbitrary coefficient operations; remains actual-update adapter.'
  else:return 'EXCLUDED',[],'Density evolution/chi-square contraction consumer,not required by perturbation algebra or this prospective header.'
 elif x['region']=='corrector-sharp-energy-and-consumers-B3':
  if mid.startswith('A2.SS3.p1.') or mid in {'A2.SS3.m1','A2.Ex6.m1'}:role=['S00','S08'];reason='Actual globally centered observable and genuine conditional/residual components.'
  elif mid.startswith('A2.SS3.p3.') or mid=='A2.Ex8.m1':role=['S07','S08'];reason='Same polar component/centered codomain and non-onto distinction; full microscopic domain retained.'
  elif mid=='A2.E20.m1' or mid in {'A2.SS3.p4.m2','A2.SS3.p4.m3','A2.SS3.p4.m4'}:role=['S05','S09'];reason='Exact B20 definition and SAME centered inverse domain; no extension across constants.'
  elif mid.startswith('A2.SS3.p5.') and mid not in {'A2.SS3.p5.m22','A2.SS3.p5.m23','A2.SS3.p5.m24'}:role=['S08','S06','S20'];reason='Actual ideal-input construction,rotation and inherited B21 ingredients; B21 is separate from generic perturbation leaf.'
  elif re.match(r'A2\.(Ex(9|1[0-7])|E21)\.',mid):role=['S08','S20'];reason='Retained actual ideal reflection/rotation/B21 source chain; not a generic-leaf parent.'
  elif mid in {'A2.SS3.p2.m1','A2.SS3.p2.m3','A2.SS3.p2.m4'}:role=['S17','S23'];reason='Source actual-refreshment regime and same U/H context; rho bound does not become a pure-algebra requirement.'
  elif mid in {'A2.SS3.p7.m1','A2.SS3.p7.m2','A2.SS3.p7.m3','A2.SS3.p7.m4','A2.SS3.p7.m5','A2.SS3.p7.m6'}:role=['S05','S06'];reason='Explicit same A/Gamma commutation,AInv self-adjointness,squaresum and centered gap; proof ingredients remain internally produced.'
  else:return 'EXCLUDED',[],'B18 ordinary decay,B19/B22-B24 Lyapunov norm equivalence,weight choice or fullB4 constants/decay; separate consumer estimates,not this algebra leaf. No68 sharp-energy parent invented.'
 else:
  if mid in {'A2.SS3.p8.m1','A2.SS3.p8.m2','A2.SS3.p8.m3'}:return 'EXCLUDED',[],'Smallc0/gamma<=1/2/Lambda>=log2 conditions are for fullB4 decay,not exact perturbation algebra; endpoint alpha eta=1 remains legal.'
  if x['RAW_start']<932584:
   role=['S17','S18','S19','S11','S12','S13','S14','S21'];reason='Exact B4 actual residual/adapter/expansion/cancellation/linear/quadratic/B28 chain,with open adapters and combined consumer explicitly distinguished.'
  else:return 'EXCLUDED',[],'Subsequent residual estimates B29-B31,Young/Lyapunov constants and fullB4 contraction are open consumers outside the prospective perturbation header.'
 return 'NODE',role,reason
def coverage(entries,is_supp):
 out=[]
 for x in entries:
  c,ns,reason=classify(x,is_supp);out.append({**x,'classification':c,'source_graph_nodes':ns,'reason':reason,'candidate_Lean_or_header_evidence_used':False})
 return out
maincov=coverage(primary,False);suppcov=coverage(supp,True)
counts=lambda xs:{k:sum(q['classification']==k for q in xs) for k in ['NODE','EXCLUDED']}
cov={'schema':'source72-primary-first-complete-finite-NODE-EXCLUDED-v1','primary_four_region_count':255,'primary_counts':counts(maincov),'primary_entries':maincov,'supplemental_unique_count':len(suppcov),'supplemental_counts':counts(suppcov),'supplemental_entries':suppcov,'combined_count':len(maincov)+len(suppcov),'unclassified':0,'NODE_contract':'Source attribution includes retained background and explicitly OPEN actual adapters/real consumers. NODE never means Lean proved,header accepted orfullB4complete.','B1_supplement_range':{k:b1[k] for k in ['RAW_start','RAW_end_exclusive','RAW_bytes','RAW_sha256']},'no_full_source_replay_claim':True}
write('stageA.finite-source255-plus-supplemental-coverage72.frozen.json',cov)
targetids=['A2.E20.m1','A2.Ex23.m1','A2.Ex23.m2','A2.Ex24.m1','A2.Ex25.m1','A2.Ex25.m2','A2.Ex26.m1','A2.Ex26.m2','A2.Ex27.m1','A2.E27.m1',*[f'A2.Ex{i}.m1' for i in range(28,37)],'A2.E28.m1']
write('stageA.target20-exact-RAW-formulas72.frozen.json',{'schema':'source72-target-exact-RAW-formulas-v1','count':len(targetids),'entries':[byid[x] for x in targetids],'authority':'Exact math element RAW byte ranges/hashes from fixed primary; decoded alttext only display aid.'})
ob_specs=[
('O00','source','Fixed primary version/RAW hashes and all255+106 item classifications must precede any72 candidate header.'),
('O01','exposure','Disclose71 complete source/BODY/publication and prior70/header exposure;72 source-blind=false;72header/BODY/sourceplan verdict unread atfreeze.'),
('O02','definition','B20 same C exactly half norm difference minus inner(A(Invu),v),sameA,sameInv,real HP0.'),
('O03','domain','Generic leaf vectors u,v,r inhabit ONE real Hilbert space; no uncentered constants/inverse extension in actual specialization.'),
('O04','generic-hypotheses','Explicit generic algebra primitives may be hypotheses of a pure Hilbert leaf,with source provenance; no provider certificate/corrector identity assumption that restates result.'),
('O05','ingredient','Same Gamma inverse left/right,Inv self-adjointness and commutation are derived or inherited internal source ingredients for original analytic theorem,never extra callers.'),
('O06','ingredient','SameA/Gamma self-adjointness and squaresum must imply quadratic energy identity,not any positive-rank/onto premise.'),
('O07','sign','Perturbation has PLUS Gamma r in first component and MINUS A r in second.'),
('O08','expansion','Full B20 expansion uses JGamma=I; v-inner terms cancel by REAL symmetry.'),
('O09','linear','Linear terms must be exactly inner(u,Inv r),same inverse,with no factorGamma orA remaining.'),
('O10','quadratic','Quadratic term must be exactly +normr²/2,not negative or fullnorm².'),
('O11','dependency','Generic perturbation leaf does not depend on B21,actual rotation,source corrector-change certificate orsharp-energy68.'),
('O12','actual-input','A real source-backed consumer must specialize to actual original PBPS gP/gV already produced from sameU/P/f; arbitraryu/v alone is insufficient for original-input credit.'),
('O13','quantifier','Original6analyticcallers and12commonwitnesses plusallparent71 conclusions must persist,without new original-input binders.'),
('O14','definition','g=U(Pf-(f-Pf)),gP=actualconditionalexpectationg,gV=V*Rg; components cannot be defined by rotation RHS.'),
('O15','centering','mean_g must remain internal reflection-preserved-law and conditional integral consequence; no caller premise.'),
('O16','definition','An arbitrary perturbation vector namedr is distinct from source r=V*(I+Hmicro)fperp and rrho=V*[I+(1-rho)Hmicro]fperp.'),
('O17','actual-adapter','Actual rrho requires SAME actualconditionalhalfturnH/microrestriction andsource K=B7; no arbitrary operator relabeled as actual H/K.'),
('O18','domain','Actualr_source/rrho centeredness must follow from V* codomain or internal adapter,not extraoriginalcaller.'),
('O19','actual-adapter','B27 outputs require actual sameP(Kf) andV*R(Kf) plus polar/all-kerP intertwining; universalr identity alone does not establish them.'),
('O20','consumer','B28 combined change separately consumes B21 and B27/rrho specialization; it cannot be claimed complete from pure leaf or actualg/forallr consumer alone.'),
('O21','constants','No rho/c0/omega/Lambda restriction is needed for abstractperturbation algebra; source0<rho<=1/2 pertainsactualMarkov/fullB4regime,notinventedanalyticcaller.'),
('O22','endpoints','Retain rank0 and alphaeta=1; no ontoV/higherregularity/strictendpoint/positive-rank assumption.'),
('O23','inverse','Inv applies onlyHP0; SAME positive root,conditional isometrye andpolarV cannot be independently substituted.'),
('O24','boundary','B29/B30/B31residualestimates,B17errors,B18decay,B22normequiv,fullB4/main/errors/cost/composition remainopen.'),
('O25','representation','Private literal ifused is propositiondefinition/nonprovider,complete original public content must remain inspectable; representation never supplies math ingredient.'),
('O26','scope','StageA freeze is prospective source expectations only; no header acceptance,proof,compile,SAUclaim,SCI,VERIFIED orwholepaper badge.')]
obligations=[{'id':a,'type':b,'expectation':c,'status':'FROZEN_SOURCE_EXPECTATION_NOT_YET_CANDIDATE_CHECKED'} for a,b,c in ob_specs]
write('stageA.all27-source-header-obligations72.frozen.json',{'schema':'source72-source-first-review-obligations-v1','count':len(obligations),'entries':obligations,'current72candidate_read':False})
exposure={'schema':'source72-honest-preheader-exposure-v1','source_blind':False,'prior_exposure':['Same PBPSv1 primary regions and source graphs in69/70/71','Complete70and71 Lean BODY,71public/private statement andeight-steppublication','71anonymousreconstruction/sourceaudit authored by thisreviewer'], 'not_read_before_this_freeze':['Any72prospectiveheader/proposal','Any72implementationBODY','Otheragent72sourceplan/verdict','Root72mathematicalverdict'], 'prior71closed_immutable':True,'prior_science_acceptance_not_substitute_for72sourcecomparison':True,'fresh_current_source_reads':['B20andB4Ex23-36/B27-B28','four255mathregions','exactB1framework74mathitems','selectedB2domain/root32mathitems'],'same6caller12witnessbackground_honestly_reused':True}
write('stageA.anti-anchoring-exposure72.frozen.json',exposure)
expect={'schema':'source72-independent-primary-first-header-expectations-v1','primary':pin(rawpath),'target':'Prospective exact B20 B4 perturbation algebra plus genuine original-input PBPS specialization; notactualK/B27/fullB28byalgebraalone.','generic_formula':'For u,v,r in one REAL Hilbert space,C(u+Gamma r,v-A r)-C(u,v)=inner(u,Inv r)+norm(r)^2/2.','actual_specialization':'For actual produced gP,gV of samegloballycenteredf andsame U/P/V/root/Inv,forall centered perturbationvector r:C(gP+Gamma r,gV-A r)-C(gP,gV)=inner(gP,Inv r)+norm(r)^2/2. This does not identify r with actualrrho or prove Koutput semantics.','source_real_residual':'r_source=V*(I+Hmicro)fperp;rrho=V*[I+(1-rho)Hmicro]fperp=rho fV+(1-rho)r_source.','source_B27':'(Kf)P=gP+Gamma rrho;(Kf)V=gV-A rrho,with same actual K/H andmicrodomain adapters.','source_B28':'C((Kf)P,(Kf)V)-C(fP,fV)=-normfP²+normfV²+inner(gP,Inv rrho)+normrrho²/2,consuming separate actualB21edge.','six_callers_background':['C2V','0<alpha','alpha<=beta','bothHessianbounds','0<eta','beta eta<=1'],'twelve_witnesses_background':['S','e','U','T','Gamma','q','GammaP0','Inv','A0','B0','V0','R'],'same_root_inverse_and_actualg_required':True,'all_parent71_clauses_retained_required':True,'generic_leaf_no_B21_parent':True,'mean_g_internal_required':True,'rank0_alphaeta1_noontoV_no68_nohigherregularity':True,'obligations':'stageA.all27-source-header-obligations72.frozen.json','source_graph':'stageA.source-proof-graph72.before-header.frozen.json','complete_finite_source_coverage':'stageA.finite-source255-plus-supplemental-coverage72.frozen.json','source_graph_nodes':len(nodes),'source_graph_edges':len(edges),'primary_math_count':255,'supplemental_unique_math_count':106,'target_formula_count':20,'source_header_verdict':'NOT_ISSUED_HEADER_UNREAD','proof_compile_SAU_SCI_VERIFIED_credit':False}
write('stageA.source-expectations72.before-header.frozen.json',expect)
synthesis={'schema':'source72-bounded-primary-first-StageA-synthesis-v1','status':'STAGEA_FROZEN_HEADER_UNREAD_SCOPE_OPEN','generic_delta':expect['generic_formula'],'actual_input_minimum':expect['actual_specialization'],'primary_counts':cov['primary_counts'],'supplement_counts':cov['supplemental_counts'],'math_total':361,'source_nodes':len(nodes),'source_edges':len(edges),'formulas':20,'obligations':27,'B21_generic_parent':False,'actual_rrho_B27_B28_separate_open_adapters':True,'sourceblind':False,'source_acceptance_proof_compile_verified':False}
write('stageA.bounded-synthesis72.frozen.json',synthesis)
records=['stageA.primary-input-manifest72.json','stageA.primary255.independent-inventory72.json','stageA.supplement-B1-framework.inventory72.json','stageA.supplement-B2-domain.inventory72.json','stageA.supplementary-discovery72.json','stageA.supplementary-prose-anchors72.json','stageA.prior71-readonly-pins72.json','stageA.source-proof-graph72.before-header.frozen.json','stageA.finite-source255-plus-supplemental-coverage72.frozen.json','stageA.target20-exact-RAW-formulas72.frozen.json','stageA.all27-source-header-obligations72.frozen.json','stageA.anti-anchoring-exposure72.frozen.json','stageA.source-expectations72.before-header.frozen.json','stageA.bounded-synthesis72.frozen.json']
run={'schema':'source72-native-primary-first-StageA-freeze-run-v1','actual_pid':os.getpid(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':[pin(O/n) for n in records],'primary_RAW_sha256':sha(raw),'source_only':True,'future72_header_proposal_BODY_and_other_sourceplan_verdict_unread':True,'closure_status':'OPEN_STAGEA_FROZEN_AWAITING_ROOT_HEADER','whole_logical_recipe':'Canonical sorted compact UTF8 JSON deleting ONLY top-level run_sha256; no other field removed.'};run['run_sha256']=sha(canon(run));write('stageA.freeze.run72.json',run)
payload={'schema':'source72-small-complete-named-StageA-expectation-input-payload-v1','expectations_complete':expect,'source_graph_complete':graph,'source_coverage_RAW_LF_ref':pin(O/'stageA.finite-source255-plus-supplemental-coverage72.frozen.json'),'target20_formulas_complete':json.loads((O/'stageA.target20-exact-RAW-formulas72.frozen.json').read_bytes()),'all27_obligations_complete':obligations,'exposure_complete':exposure,'primary_exact_input_manifest_complete':json.loads((O/'stageA.primary-input-manifest72.json').read_bytes()),'prior_immutable_anchors_complete':json.loads((O/'stageA.prior71-readonly-pins72.json').read_bytes()),'native_run_complete':run,'all_named_records_RAW_LF':[pin(O/n) for n in records],'materialization':'4regionsRAW/LF+B1boundedframeworkRAW/LF+finiteB2exactmath/prose files available inowned scope;fullprimary andoldnative pinned withoutrecursivehistory/base64 duplication.','closure':'StageA only OPEN; finalnativeCLOSED_LAST only after separately authorized prospectiveheader review.'}
write('stageA.complete-named-expectations-input-payload72.json',payload)
print(json.dumps({'actual_pid':os.getpid(),'status':synthesis['status'],'primary255':cov['primary_counts'],'supplement106':cov['supplemental_counts'],'source_nodes_edges':[len(nodes),len(edges)],'formulas_obligations':[20,27],'expectations':pin(O/'stageA.source-expectations72.before-header.frozen.json'),'source_graph':pin(O/'stageA.source-proof-graph72.before-header.frozen.json'),'coverage':pin(O/'stageA.finite-source255-plus-supplemental-coverage72.frozen.json'),'whole_logical_run_sha256':run['run_sha256'],'small_named_payload':pin(O/'stageA.complete-named-expectations-input-payload72.json')},ensure_ascii=False,indent=2))
