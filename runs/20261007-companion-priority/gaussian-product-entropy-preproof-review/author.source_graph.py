from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
R=Path('E:/Samplinglib');O=R/'runs/20261007-companion-priority/gaussian-product-entropy-source-graph';O.mkdir(exist_ok=False)
H=lambda b:hashlib.sha256(b).hexdigest()
def enc(o):return (json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode()
def put(n,o):
 b=o if isinstance(o,bytes) else enc(o)
 with (O/n).open('xb') as f:f.write(b)
 return H(b)
lease={'actor':'gaussian_domain_preproof_reviewer_29','role':'Source graph AUTHOR, not topology validator','status':'ACTIVE','read_lease':'ACTIVE','write_lease':'ACTIVE','Python_lease':'ACTIVE','compiler_lease':'CLOSED','compiler_started':False,'opened_utc':datetime.now(timezone.utc).isoformat()};(O/'lease.json').write_bytes(enc(lease))
P='runs/20261007-companion-priority/gaussian-functional-availability/'
paths={
 'PRIMARY-E6':'runs/20261007-companion-priority/gaussian-clt-entropy-preread/primary.S4.E6.raw.snapshot.html',
 'PRIMARY-LSI':'runs/20261007-companion-priority/gaussian-clt-entropy-preread/primary.S4.SS1.p4.3.raw.snapshot.html',
 'SLT-BASIC':P+'SLT__GaussianLSI__SubAddEnt__Basic.lean.raw.snapshot',
 'SLT-CHAIN':P+'SLT__GaussianLSI__SubAddEnt__Decomposition.lean.raw.snapshot',
 'SLT-MAIN':P+'SLT__GaussianLSI__SubAddEnt__Subadditivity.lean.raw.snapshot',
 'SLT-DUAL':P+'SLT__GaussianLSI__DualEntApp.lean.raw.snapshot',
 'SLT-GAUSSIAN':P+'SLT__GaussianLSI__TensorizedGLSI.lean.raw.snapshot',
 'SLT-ENTROPY':P+'SLT__GaussianLSI__Entropy.lean.raw.snapshot',
 'SLT-CONDEXP':P+'SLT__EfronStein.lean.raw.snapshot',
 'API-PROD':'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Prod.lean',
 'API-LOG':'.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Log/NegMulLog.lean',
 'API-DCT':'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DominatedConvergence.lean',
 'API-L1':'.lake/packages/mathlib/Mathlib/MeasureTheory/Function/L1Space/Integrable.lean',
 'API-PROB':'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Prod.lean',
 'TARGET':'runs/20261007-companion-priority/gaussian-product-entropy-preproof/signature.prospective.txt',
 'PREREAD':'runs/20261007-companion-priority/gaussian-product-entropy-preread/source-dependency.packet.json',
 'PRIMARY-CONTRACT':'runs/20261007-companion-priority/gaussian-product-entropy-preproof-review/primary.contract.json',
 'STATEMENT-REVIEW':'runs/20261007-companion-priority/gaussian-product-entropy-preproof-review/statement.review.json'}
pins=[];lines={}
for i,(k,p) in enumerate(paths.items()):
 b=(R/p).read_bytes();l=b.replace(b'\r\n',b'\n').replace(b'\r',b'\n');n=f'input.{i:02d}'
 put(n+'.raw.snapshot',b);put(n+'.lf.snapshot',l);lines[k]=l.decode().splitlines()
 pins.append({'id':k,'path':p,'raw_sha256':H(b),'lf_sha256':H(l),'bytes':len(b),'raw_snapshot':n+'.raw.snapshot','lf_snapshot':n+'.lf.snapshot','role':'prospective_target_identity_only_not_topology_driver' if k=='TARGET' else 'bounded_source_API_context' if k not in ['PREREAD','PRIMARY-CONTRACT','STATEMENT-REVIEW'] else 'prior_frozen_contract_context'})
assert next(x for x in pins if x['id']=='TARGET')['lf_sha256']=='4c3634612a055d16e4aec0516823192db42307ac1330ae4bddb88b959a436b0d'
nodes=[];edges=[];regions=[]
def node(i,kind,formula,anchors=None,boundary=None):
 nodes.append({'id':i,'kind':kind,'formula_or_contract':formula,'source_anchors':anchors or [],'boundary':boundary,'status':'SOURCE_ONLY_NOT_COMPILED'})
def edge(a,b,ingredient,kind='AUTHORED_DEPENDENCY',anchor=None):
 edges.append({'id':f'e{len(edges)+1:03d}','from':a,'to':b,'ingredient':ingredient,'kind':kind,'caller_anchor':anchor or 'author.route.json (explicit mathematical dependency, no source attribution)','compiled':False})
def region(k,a,b,ids,reason=None):
 assert 1<=a<=b<=len(lines[k]),(k,a,b)
 span=('\n'.join(lines[k][a-1:b])+'\n').encode();n=f'source.region.{len(regions)+1:03d}.raw.snapshot'
 put(n,span);regions.append({'id':f'r{len(regions)+1:03d}','pin':k,'path':paths[k],'line_start':a,'line_end':b,'line_count':b-a+1,'disposition':'NODE' if ids else 'EXCLUDED','nodes':ids,'reason':reason,'span_lf_sha256':H(span),'snapshot':n})
def anchored(i,kind,formula,k,a,b,boundary=None):
 node(i,kind,formula,[{'pin':k,'lines':[a,b]}],boundary);region(k,a,b,[i])
anchored('PRIMARY-E6','PRIMARY_CONTEXT','First4.6 W2(r,gamma)<=sqrt(Fisher); other two bounds belong to neighboring source context.','PRIMARY-E6',1,len(lines['PRIMARY-E6']),'No W2/T2/paper proof credit in this packet.')
anchored('PRIMARY-LSI','PRIMARY_OMITTED_BACKGROUND','First bound combines standard Gaussian T2 and Gaussian LSI.','PRIMARY-LSI',1,len(lines['PRIMARY-LSI']),'Continuous product entropy is background reconstructed externally, not printed here; remaining gradient/moment sentences context only.')
node('PROB','SOURCE_BACKGROUND','Actual μ,ν probability measures on arbitrary measurable X,Y; finite/SFinite and mass1 derived.')
node('CLASS','AUTHORED_CLASS','Measurable real F, pointwise nonnegative, existential finite upper bound; choose max(C,0) internally. Stronger pointwise/narrower bounded class than SLT.')
node('PHI','DEFINITION','Phi(t)=t*Real.log(t); Phi(0)=0, no normalized density requirement.')
node('MARGINALS','DEFINITION','A(x)=∫F(x,y)dν, B(y)=∫F(x,y)dμ, m=∫F d(μ.prodν).')
anchored('API-PROBP','MATHLIB_API','prod.instIsProbabilityMeasure: genuine product probability from two probability instances.','API-PROB',322,325)
anchored('API-L1-DOM','MATHLIB_API','Integrable.mono: actual AEStronglyMeasurable function norm dominated by true integrable function.','API-L1',83,103)
anchored('API-CONST','MATHLIB_API','integrable_const under IsFiniteMeasure.','API-L1',158,164)
anchored('API-MEAS-R','MATHLIB_API','StronglyMeasurable.integral_prod_right and right-prime: actual measurable marginal.','API-PROD',68,79)
anchored('API-MEAS-L','MATHLIB_API','StronglyMeasurable.integral_prod_left and left-prime via swap.','API-PROD',81,92)
region('API-PROD',93,97,[], 'Namespace end and section marker, no additional mathematical primitive.')
anchored('API-SLICES','MATHLIB_API','Integrable.prod_left_ae/prod_right_ae provide AE slices only; pointwise bounded class independently produces ALL slices.','API-PROD',231,258)
anchored('API-MARG-L1','MATHLIB_API','Integrable.integral_prod_left/right give true integrable marginals from joint L1.','API-PROD',335,344)
anchored('API-FUBINI','MATHLIB_API','integral_prod, integral_prod_symm and reversed integral identities require actual L1.','API-PROD',444,478)
anchored('API-PRODMUL','MATHLIB_API','integral_prod_mul factors actual product integral; true positive R domains independently established.','API-PROD',539,541)
anchored('API-LOGSUM','MATHLIB_API','x-1<=x logx for nonnegative x; fixed-n u/v yields u log(u/v)-u+v>=0.','API-LOG',33,42)
anchored('API-TLOGT','MATHLIB_API','Real.continuous_mul_log and Continuous.mul_log, including zero.','API-LOG',44,63)
anchored('API-DCT','MATHLIB_API','DCT requires actual measurable sequence, integrable bound, AE domination and AE convergence.','API-DCT',52,74)
anchored('SLT-ENTROPY','EXTERNAL_DEFINITION','Ent_mu F = ∫FlogF-Phi(∫F); constant entropy0 under probability.','SLT-ENTROPY',36,62)
anchored('SLT-CONDEXP','EXTERNAL_DEFINITION','E^i f(x)=∫f(update x i y)dμ_i; no abstract supplied conditional representative.','SLT-CONDEXP',31,44)
anchored('SLT-FIRSTK','EXTERNAL_DEFINITION','E_k f integrates actual coordinates j>=k under homogeneous finite pi law.','SLT-CONDEXP',258,260)
anchored('SLT-CONDENT','EXTERNAL_DEFINITION','condEntExceptCoord=E^i(flogf)-Phi(E^i f), source probability pi binders.','SLT-BASIC',33,46)
anchored('SLT-COND-L1','EXTERNAL_SOURCE','Conditional marginal L1 from actual update measure-preserving law and Fubini.','SLT-BASIC',118,138)
anchored('SLT-SLICE-L1','EXTERNAL_SOURCE','Actual source slices L1 only AE, with update map law.','SLT-BASIC',140,160)
anchored('SLT-NONNEG','EXTERNAL_SOURCE','Conditional nonnegativity AE derived from source nonnegative AE.','SLT-BASIC',198,204)
anchored('SLT-MARG-PHI-L1','EXTERNAL_SOURCE','Marginal Phi integrability needs source measurable/nonnegative/L1/PhiL1; Jensen proof background not imported to target.','SLT-BASIC',206,218,'Selected header only; remaining Jensen closure is outside bounded source slice.')
anchored('SLT-PHI-TOWER','EXTERNAL_SOURCE','∫E^i(flogf)=∫flogf using actual PhiL1.','SLT-BASIC',279,283)
anchored('SLT-CONDENT-L1','EXTERNAL_SOURCE','Conditional entropy L1 requires conditional PhiL1 before integral subtraction.','SLT-BASIC',289,300)
anchored('SLT-CHAIN','EXTERNAL_SOURCE','Actual entropy-chain cancellation: Ent f=E condEnt+Ent E^if, with true F and Phi/marginalPhi L1.','SLT-CHAIN',31,87)
anchored('SLT-TELE','EXTERNAL_PRIMITIVE_HEADER','Pointwise log first-k telescoping; source calls at main1301.','SLT-CHAIN',151,155,'Body beyond header not imported/proved in this bounded task.')
anchored('SLT-FIRSTK-L1','EXTERNAL_PRIMITIVE_HEADER','Actual f*log(E_kf) L1 under source measurable/AE nonnegative/F L1/Phi L1.','SLT-MAIN',310,316)
anchored('SLT-TOWER','EXTERNAL_PRIMITIVE_HEADER','Actual first-k tower AE under source true measurability and L1.','SLT-MAIN',666,671)
anchored('SLT-CROSS-L1','EXTERNAL_PRIMITIVE_HEADER','Actual f*log(E^iE_(i+1)f) L1 from source first-k tower.','SLT-MAIN',712,728)
anchored('SLT-TERM','EXTERNAL_SOURCE','First-k increment bounded by expected coordinate entropy via slice duality.','SLT-MAIN',1030,1045,'Only selected source declaration/domain calls and actual duality-use region; full external proof closure not ported.')
anchored('SLT-DUAL-USE','EXTERNAL_SOURCE','Source positive test mean branch uses actual entropy duality and positivity-on-Y to turn EReal quantity into Bochner integral.','SLT-MAIN',1110,1158)
anchored('SLT-DUAL','EXTERNAL_SOURCE','entropy_ge_integral_log_real requires true Y/T measurability/L1, YlogY L1, Tmean>0 and AE Y>0->T>0.','SLT-DUAL',450,468)
anchored('SLT-SUBADD','EXTERNAL_SOURCE','Finite homogeneous probability-product entropy_subadditive with measurable F, AE F>=0, F L1 and PhiF L1.','SLT-MAIN',1264,1274)
anchored('SLT-ZERO','EXTERNAL_SOURCE','Source n0 singleton law: constant entropy0, empty sum0; not an assumption n>0.','SLT-MAIN',1276,1298)
region('SLT-MAIN',1275,1275,[], 'Blank separator only.')
region('SLT-MAIN',1299,1299,[], 'Blank separator only.')
anchored('SLT-SUBADD-PROOF','EXTERNAL_SOURCE','n>0 first-k telescoping + term bounds, actual crosslog L1, finite integral sum, real subtraction and constants.','SLT-MAIN',1300,1368)
anchored('SLT-GAUSSIAN','EXTERNAL_CONSUMER_ONLY','Tensorized gaussian W12 pi LSI consumes actual source entropy_subadditive and separate slice energy bounds.','SLT-GAUSSIAN',459,486,'Classical differentiable+continuous partials+separate Phi(g²)L1; no GaussianLSI theorem credit or pointwise RN derivative in this packet.')
node('SLT-IMPORTS','SOURCE_GAP','Unexpanded imported source primitives: condExpExceptCoord_expectation, map_update_prod_pi, condExpFirstK endpoint/positivity and entropy_ge_integral_log/integralYLogT proof closures. Explicit external primitives, not authored independence CF or local APIs.','', 'Full external closure not claimed; source headers/caller evidence only.')
node('HETERO-ADAPTER','SOURCE_GAP','Heterogeneous binary X×Y to homogeneous SLT Fin2→Ω pi-carrier/measure/conditional entropy adapter absent; must produce actual law/entropy transports, no certificate binder.')
for i,formula in [
 ('DOMAIN','All joint and ALL sections are measurable, nonnegative bounded; true F/PhiF L1. A/B in [0,C0], measurable; true marginal Phi L1.'),
 ('DELTA','δn=1/(n+1)>0, δn<=1 and tends0; Fn=F+δn; An=A+δn, Bn=B+δn,mn=m+δn via true L1 and probability/Fubini.'),
 ('POSITIVE','For fixed n Fn,An,Bn,mn∈[δn,C0+δn], no original positive mass/fiber binder.'),
 ('R-DENSITY','Rn=An*Bn/mn; δn²/(C0+δn)<=Rn<=(C0+δn)²/δn; ∫Rn=mn by true product factorization and matching marginal masses.'),
 ('LOG-DOMAIN','All fixed-n logs/log ratios/products integrable via positive lower/upper bounds; Fubini cross-log terms justified before algebra.'),
 ('LOGSUM','Pointwise Fn log(Fn/Rn)-Fn+Rn>=0; integrate true L1, ∫Fn=∫Rn cancels.'),
 ('EXPAND','logRn=logAn+logBn-logmn; Fubini ∫Fn logAn=∫An logAn, similarly Bn; exact inequality J_An+J_Bn<=J_Fn+Phi(mn).'),
 ('DCT','Pass four Phi entropy terms only using uniform bounded domination on [0,C0+1], true measurability/L1, δn->0 and continuous tlogt; no cross-log zero-fiber passage.'),
 ('TARGET','True joint/slice/marginal L1 outputs and loss-free J_A+J_B<=J_F+Phi(m), including m0/F0/zero fibers.'),
 ('ENTROPY-CHAIN','With true L1/Fubini, Entjoint=EνEntμ(slice)+Entν(B)=EμEntν(slice)+Entμ(A); marginal inequality implies entropy subadditivity. Conditional outer entropy L1 bounded and internally derivable, not a supplied assumption.'),
 ('FINITE-ITERATION','Future actual finite-coordinate entropy contraction/iteration and coordinate measure transport assembly remain open.'),
 ('GAUSSIAN-CONSUMER','Future compact squared C2 observer internally produces measurable/nonnegative/bounded class; scalar compact LSI applied to original coordinate slices, not assumed C2 RMS marginal square roots.'),
 ('RESIDUAL','Finite-Hilbert energy/basis transport, noncompact actual32 cutoff entropy/energy convergence, Gaussian T2/FIRST4.6/paper main/cost remain open.')]:
  node(i,'SOURCE_GAP' if i in ['FINITE-ITERATION','GAUSSIAN-CONSUMER','RESIDUAL'] else 'AUTHORED_MATHEMATICAL_ROUTE',formula)
edge('PRIMARY-LSI','PRIMARY-E6','printed first inequality invokes GaussianLSI/T2','PRIMARY_SOURCE_USE','S4.SS1.p4.3 first sentence')
edge('SLT-GAUSSIAN','PRIMARY-LSI','external GaussianLSI background candidate only','DEPENDENCY_BOUNDARY','SPHMC S4.SS1.p4.3; SLT TensorizedGLSI459-486')
for a,b,ing,k,an in [
 ('SLT-ENTROPY','SLT-CONDENT','same homogeneous entropy convention','EXTERNAL_SOURCE_USE','Basic43-46'),
 ('SLT-CONDEXP','SLT-CONDENT','actual E^i definition','EXTERNAL_SOURCE_USE','Basic45-46'),
 ('SLT-CONDEXP','SLT-COND-L1','actual update marginal','EXTERNAL_SOURCE_USE','Basic121,137'),
 ('SLT-IMPORTS','SLT-COND-L1','update pushforward measure law','DEPENDENCY_BOUNDARY','Basic123-136 map_update_prod_pi134'),
 ('API-MARG-L1','SLT-COND-L1','integral_prod_left use','EXTERNAL_SOURCE_USE','Basic138'),
 ('API-SLICES','SLT-SLICE-L1','prod_right_ae','EXTERNAL_SOURCE_USE','Basic160'),
 ('SLT-IMPORTS','SLT-SLICE-L1','actual update pushforward','DEPENDENCY_BOUNDARY','Basic146-159'),
 ('SLT-CONDEXP','SLT-MARG-PHI-L1','actual conditional marginal Phi','EXTERNAL_SOURCE_USE','Basic207-213'),
 ('SLT-IMPORTS','SLT-PHI-TOWER','condExpExceptCoord_expectation','DEPENDENCY_BOUNDARY','Basic283'),
 ('SLT-COND-L1','SLT-CONDENT-L1','conditional Phi first-term L1','EXTERNAL_SOURCE_USE','Basic298'),
 ('SLT-CONDENT','SLT-CONDENT-L1','exact difference definition','EXTERNAL_SOURCE_USE','Basic295'),
 ('SLT-MARG-PHI-L1','SLT-CONDENT-L1','marginal Phi L1 must be available, signature hEf','EXTERNAL_SOURCE_USE','Basic292-300'),
 ('SLT-PHI-TOWER','SLT-CHAIN','Phi tower','EXTERNAL_SOURCE_USE','Decomposition57'),
 ('SLT-COND-L1','SLT-CHAIN','true L1 before subtraction','EXTERNAL_SOURCE_USE','Decomposition59'),
 ('SLT-CONDENT','SLT-CHAIN','conditional entropy definition','EXTERNAL_SOURCE_USE','Decomposition54,78-80'),
 ('SLT-ENTROPY','SLT-CHAIN','actual homogeneous entropy','EXTERNAL_SOURCE_USE','Decomposition68,86'),
 ('SLT-IMPORTS','SLT-CHAIN','F tower expectation','DEPENDENCY_BOUNDARY','Decomposition70'),
 ('SLT-FIRSTK','SLT-TELE','actual first-k family','EXTERNAL_SOURCE_USE','Decomposition154-155'),
 ('SLT-FIRSTK','SLT-FIRSTK-L1','actual first-k log-domain','EXTERNAL_SOURCE_USE','Subadditivity311-316'),
 ('SLT-CONDEXP','SLT-TOWER','tower right actual coordinate marginal','EXTERNAL_SOURCE_USE','Subadditivity670-671'),
 ('SLT-FIRSTK','SLT-TOWER','tower first-k objects','EXTERNAL_SOURCE_USE','Subadditivity670-671'),
 ('SLT-TOWER','SLT-CROSS-L1','AE first-k equality','EXTERNAL_SOURCE_USE','Subadditivity719-728'),
 ('SLT-FIRSTK-L1','SLT-TERM','f log first-k L1','EXTERNAL_SOURCE_USE','Subadditivity1043'),
 ('SLT-FIRSTK','SLT-TERM','increment definition','EXTERNAL_SOURCE_USE','Subadditivity1038-1040'),
 ('SLT-CONDEXP','SLT-DUAL-USE','actual slice test','EXTERNAL_SOURCE_USE','Subadditivity1112-1117'),
 ('SLT-IMPORTS','SLT-DUAL-USE','positivity on Y and actual EReal duality','DEPENDENCY_BOUNDARY','Subadditivity1111,1149-1152'),
 ('SLT-DUAL','SLT-DUAL-USE','real duality contract correspondence; caller uses EReal plus conversion','DEPENDENCY_BOUNDARY','Subadditivity1149-1154 versus DualEntApp453-468'),
 ('API-MEAS-R','SLT-DUAL-USE','integral_prod_right','EXTERNAL_SOURCE_USE','Subadditivity1141'),
 ('SLT-DUAL-USE','SLT-TERM','slice entropy duality route','EXTERNAL_SOURCE_USE','Subadditivity1110-1158'),
 ('SLT-ENTROPY','SLT-SUBADD','homogeneous entropy definition','EXTERNAL_SOURCE_USE','Subadditivity1274'),
 ('SLT-CONDENT','SLT-SUBADD','conditional entropy conclusion','EXTERNAL_SOURCE_USE','Subadditivity1273'),
 ('SLT-ZERO','SLT-SUBADD','zero-dimensional law branch','EXTERNAL_SOURCE_USE','Subadditivity1276-1298'),
 ('SLT-TELE','SLT-SUBADD-PROOF','pointwise telescoping','EXTERNAL_SOURCE_USE','Subadditivity1301'),
 ('SLT-TERM','SLT-SUBADD-PROOF','term bound','EXTERNAL_SOURCE_USE','Subadditivity1308'),
 ('SLT-TOWER','SLT-SUBADD-PROOF','AE first-k tower','EXTERNAL_SOURCE_USE','Subadditivity1323'),
 ('SLT-FIRSTK-L1','SLT-SUBADD-PROOF','true log integrability','EXTERNAL_SOURCE_USE','Subadditivity1338'),
 ('SLT-CROSS-L1','SLT-SUBADD-PROOF','true cross-log integrability','EXTERNAL_SOURCE_USE','Subadditivity1339'),
 ('SLT-ENTROPY','SLT-SUBADD-PROOF','real entropy integral expansion','EXTERNAL_SOURCE_USE','Subadditivity1344'),
 ('SLT-SUBADD-PROOF','SLT-SUBADD','positive-n proof branch','EXTERNAL_SOURCE_USE','Subadditivity1300-1368'),
 ('SLT-SUBADD','SLT-GAUSSIAN','actual entropy_subadditive call','EXTERNAL_SOURCE_USE','TensorizedGLSI475-477')]:edge(a,b,ing,k,an)
for a,b,ing in [
 ('PROB','DOMAIN','finite probability laws'),('CLASS','DOMAIN','pointwise measurable bounded nonnegative observer'),('PHI','DOMAIN','exact tlogt'),('MARGINALS','DOMAIN','actual marginal objects'),
 ('API-PROBP','DOMAIN','actual product finite measure'),('API-CONST','DOMAIN','true constant L1 domination'),('API-L1-DOM','DOMAIN','derive all domains'),('API-TLOGT','DOMAIN','continuous Phi bounded on compact interval'),('API-MEAS-R','DOMAIN','measurable A'),('API-MEAS-L','DOMAIN','measurable B'),('API-MARG-L1','DOMAIN','actual marginal L1'),
 ('DOMAIN','DELTA','L1 before adding constants'),('PROB','DELTA','mass1'),('MARGINALS','DELTA','matching integral definitions'),('API-FUBINI','DELTA','actual equal marginal/product masses'),
 ('DELTA','POSITIVE','strict δ>0'),('CLASS','POSITIVE','0<=F<=C0'),('POSITIVE','R-DENSITY','positive quotient bounds'),('MARGINALS','R-DENSITY','actual product of marginals'),('API-PRODMUL','R-DENSITY','integral R=mn'),
 ('R-DENSITY','LOG-DOMAIN','fixed-n upper/lower bound'),('POSITIVE','LOG-DOMAIN','fixed-n F,A,B,m lower bound'),('API-L1-DOM','LOG-DOMAIN','bounded actual log-weighted L1'),('API-CONST','LOG-DOMAIN','finite probability dominator'),
 ('API-LOGSUM','LOGSUM','genuine scalar inequality'),('R-DENSITY','LOGSUM','positive v and equal mass'),('POSITIVE','LOGSUM','positive u/v'),('LOG-DOMAIN','LOGSUM','actual real integration of nonnegative logsum'),
 ('LOGSUM','EXPAND','integrated inequality'),('LOG-DOMAIN','EXPAND','legal log algebra/Fubini/subtraction'),('API-FUBINI','EXPAND','actual cross-log marginal identities'),('PHI','EXPAND','exact entropy integrands'),
 ('EXPAND','DCT','four positive-regularized entropy terms only'),('API-DCT','DCT','genuine dominated convergence'),('API-TLOGT','DCT','zero-safe scalar continuity'),('DOMAIN','DCT','true limit domains and finite law domination'),('DELTA','DCT','δn tends0 and <=1'),
 ('DCT','TARGET','closed real order under finite limits'),('DOMAIN','TARGET','all actual L1 outputs'),('PHI','TARGET','zero safe definition'),('MARGINALS','TARGET','same actual A/B/m'),
 ('TARGET','ENTROPY-CHAIN','loss-free marginal inequality'),('API-FUBINI','ENTROPY-CHAIN','actual chain identity'),('DOMAIN','ENTROPY-CHAIN','subtraction and conditional outer L1'),
 ('ENTROPY-CHAIN','FINITE-ITERATION','genuine binary contraction'),('FINITE-ITERATION','GAUSSIAN-CONSUMER','actual finite product entropy assembly'),('GAUSSIAN-CONSUMER','RESIDUAL','later actual32/33 paper consumer'),
 ('SLT-SUBADD','HETERO-ADAPTER','different carrier/scope transport'),('HETERO-ADAPTER','TARGET','source route must adapt carrier plus derive actual bounded all-slice domains')]:edge(a,b,ing,'DEPENDENCY_BOUNDARY' if a in ['HETERO-ADAPTER','FINITE-ITERATION','GAUSSIAN-CONSUMER'] else 'AUTHORED_DEPENDENCY')
# Explicit mathematical primitive use sites within selected external proof regions.
for dest,anchor,ingredient in [('SLT-CHAIN','Decomposition55','integral_sub with actual L1'),('SLT-SUBADD-PROOF','Subadditivity1340','integral_finsetSum with each true term L1'),('SLT-SUBADD-PROOF','Subadditivity1352','integral_const_mul'),('SLT-SUBADD-PROOF','Subadditivity1355','integral_sub true PhiF L1 and F times constant'),('SLT-ZERO','Subadditivity1287,1291,1296','integral_eq_const on singleton law')]:
 edge('SLT-IMPORTS',dest,ingredient,'DEPENDENCY_BOUNDARY',anchor)
routes=[{'id':'OR-SOURCE-CONDITIONAL','provenance':'PINNED_EXTERNAL_SOURCE_ROUTE_WITH_EXPLICIT_ADAPTER_GAPS','inputs':['SLT-SUBADD','HETERO-ADAPTER','DOMAIN'],'output':'TARGET','truth_boundary':'External unbounded homogeneous Fin n product source plus missing heterogeneous carrier/domain adapter; not a callable local producer.'},
 {'id':'OR-AUTHORED-REGULARIZATION','provenance':'AUTHORED_SUFFICIENT_BACKGROUND_NOT_PRINTED_SPHMC_OR_SLT_ROUTE','inputs':['DOMAIN','DELTA','POSITIVE','R-DENSITY','LOG-DOMAIN','LOGSUM','EXPAND','DCT'],'output':'TARGET','truth_boundary':'Mathematical dependency design only, no implementation/compiled proof or selfvalidation.'}]
selected={}
for reg in regions:
 selected.setdefault(reg['pin'],[]).extend(range(reg['line_start'],reg['line_end']+1))
for k,ls in selected.items():assert len(ls)==len(set(ls)),k
inventory={'schema_version':1,'scope':'Exhaustive disjoint dispositions for SELECTED physical source regions only; not entire SLT project/proof closure. Headers are explicitly external primitives with unexpanded source gaps. Full-file raw pins do not imply full-file reading.',
 'regions':regions,'region_count':len(regions),'physical_lines':sum(r['line_count'] for r in regions),'selected_partitions':{k:sorted(v) for k,v in selected.items()},'not_selected':'All full-file lines outside listed selected partitions are outside this bounded contract, not silently verified. Future Gaussian/noncompact/Hilbert/T2 source regions not selected for theorem proof credit.'}
review=json.loads((R/paths['STATEMENT-REVIEW']).read_text(encoding='utf8'))
contract={'schema_version':1,'mode':'SOURCE_ONLY_AUTHORING','primary_first_contract':paths['PRIMARY-CONTRACT'],'seven_slots':review['seven_slots'],'binder_classification':review['binder_classification'],
 'source_hypothesis_binder_invariant':'Generic bounded class disclosed as authored restriction; later compact C2 squared consumer must produce it internally. No added L1/positive mass/fiber/normalization/entropy certificate public binder.',
 'definition_audit':'Phi literal real tlogt including0; A/B actual Bochner slice integrals, m actual product mass; no arbitrary RN representative derivative.',
 'mathematical_routes':routes,'compiled_edges':[],'remaining_boundary':review['remaining_boundary'],'external_pin':{'SLT':'d0f506f0a695018265dccb33bcb05e2f5ca1c876','license':'Apache-2.0 in actual frozen headers','toolchain':'upstream4.32/mathlib81a5d257 versus local4.33/db584cd6'},
 'target_identity':'Exact prospective1029-byte signature; root anonymous Prop typecheck only, no named declaration elaboration, proof or SAU claim.'}
graph={'schema_version':1,'author':'gaussian_domain_preproof_reviewer_29','status':'AUTHORED_SOURCE_GRAPH_AWAITING_DISTINCT_TOPOLOGY_REVIEW','scope':'Bounded continuous binary product entropy background for prospective39; independently reconstructed from fixed primary/external/API contracts, no implementation exists/read.',
 'nodes':nodes,'edges':edges,'or_routes':routes,'compiled_edges':[],'source_inventory':'source.inventory.json','source_contract':'source.contract.json','inputs':'input-bindings.json',
 'author_does_not_validate_own_graph':True,'residuals':['unexpanded SLT external primitive closures and heterogeneous carrier source alternative','actual implementation/source/math/independent topology admission','finite tensorization','compact Gaussian product/Hilbert/cutoff/noncompact LSI','Gaussian T2/FIRST4.6/paper main/cost'],
 'no_proof_or_implementation_credit':True}
dig={'synthesis_first':'Prospective bounded binary marginal entropy inequality is sound and sufficient for compact squared observers. Internally produce all L1; positive δ regularization plus genuine scalar logsum and four-term tlogt DCT includes zero fibers/mass. External conditional-entropy route remains distinct and needs heterogeneous carrier/domain adapters.',
 'route_at_most_seven_steps':review['authored_route_at_most_seven_steps'],'nodes':len(nodes),'edges':len(edges),'or_routes':len(routes),'selected_regions':len(regions),'selected_physical_lines':inventory['physical_lines'],'compiler_started':False,'topology_validation':'PENDING_DISTINCT_REVIEW','statement_review':paths['STATEMENT-REVIEW'],'compiled_edges':[]}
outs={}
for name,obj in [('input-bindings.json',pins),('source.contract.json',contract),('source.inventory.json',inventory),('source-proof-graph.independent.json',graph),('bounded-synthesis.json',dig),('author.route.json',{'route':review['authored_route_at_most_seven_steps'],'note':'Explicit authored mathematical dependency anchors; never primary/source proof attribution.'})]:outs[name]=put(name,obj)
run={'schema_version':1,'inputs':[{'path':p['path'],'raw_sha256':p['raw_sha256'],'lf_sha256':p['lf_sha256']} for p in pins],'outputs':outs,'compiler_started':False,'canonical_mutations':False};run['run_sha256']=H(enc(run));put('run.json',run)
lease.update({'status':'CLOSED','read_lease':'CLOSED','write_lease':'CLOSED','Python_lease':'CLOSED','compiler_lease':'CLOSED','closed_utc':datetime.now(timezone.utc).isoformat(),'run_sha256':run['run_sha256'],'source_graph_sha256':outs['source-proof-graph.independent.json']});(O/'lease.json').write_bytes(enc(lease))
print(json.dumps({'source_graph_sha256':outs['source-proof-graph.independent.json'],'run_sha256':run['run_sha256'],'nodes':len(nodes),'edges':len(edges),'regions':len(regions),'physical_lines':inventory['physical_lines'],'pins':len(pins),'leases':'CLOSED','topology_validation':'PENDING_DISTINCT_REVIEW'}))
