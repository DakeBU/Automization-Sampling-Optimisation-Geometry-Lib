from pathlib import Path
import hashlib,json,datetime,re
ROOT=Path('E:/Samplinglib'); P='runs/20261007-companion-priority/'
OUT=ROOT/(P+'gaussian-flip-energy-source-graph'); OLD=ROOT/(P+'gaussian-flip-energy-preread')
A=P+'gaussian-functional-availability/'; M='.lake/packages/mathlib/Mathlib/'
def lf(b):return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def sha(b):return hashlib.sha256(b).hexdigest()
def emit(name,obj):
 b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode();(OUT/name).open('xb').write(b);return sha(b)
bindings=[]; pinned={}
def bind(path,b=None,kind='FROZEN_SOURCE_OR_API'):
 if path in pinned:return pinned[path]
 if b is None:b=(ROOT/path).read_bytes()
 i=len(bindings);rn='input.%03d.raw.snapshot'%i;ln='input.%03d.lf.snapshot'%i
 (OUT/rn).open('xb').write(b);(OUT/ln).open('xb').write(lf(b))
 e=dict(path=path,raw_sha256=sha(b),lf_sha256=sha(lf(b)),bytes=len(b),raw_snapshot=rn,lf_snapshot=ln,kind=kind)
 bindings.append(e);pinned[path]=e;return e
prior=json.loads((OLD/'inputs.json').read_text())
for e in prior['raw_LF_bound_inputs']:
 b=(OLD/e['raw_snapshot']).read_bytes();assert sha(b)==e['raw_sha256'] and sha(lf(b))==e['lf_sha256']
 bind(e['path'],b,e['kind'])
for name in ['source-detail-packet.json','source-regions.json','inputs.json','run.closed.json','lease.json']:
 bind(P+'gaussian-flip-energy-preread/'+name,kind='CLOSED_PRIMARY_FIRST_PREREAD_EVIDENCE')
target='.astis/flip-energy37/signature.prospective.txt';bind(target,kind='ROOT_PROSPECTIVE_TARGET_SHAPE_ONLY_NO_IMPLEMENTATION')
for path in [A+'SLT__GaussianPoincare__RademacherApprox.lean.raw.snapshot',M+'MeasureTheory/Constructions/Pi.lean',M+'Analysis/Calculus/Deriv/Basic.lean']:bind(path)
closure=json.loads((OUT/pinned[A+'import-closure-audit.json']['raw_snapshot']).read_text())
for e in closure['files']:
 if e['local_snapshot'] in pinned:assert pinned[e['local_snapshot']]['raw_sha256']==e['raw_sha256']

nodes=[];edges=[]
def node(id,kind,formula,scope='BACKGROUND',anchors=None):
 nodes.append(dict(id=id,kind=kind,formula_or_contract=formula,scope=scope,anchors=anchors or []))
def use(dst,parents,kind='EXTERNAL_SOURCE_USE',anchor=None,ingredient=None):
 for parent in parents.split():
  edges.append(dict(id='e%03d'%(len(edges)+1),from_node=parent,to_node=dst,kind=kind,anchor=anchor,ingredient=ingredient or ('Actual direct ingredient '+parent+' for '+dst),truth_contract='source/API ingredient edge only; no compiled dependency certification'))

for args in [
 ('FIRST','PRINTED_SOURCE','W2(r_y,N(0,I))<=sqrt(E_r_y||grad rho_y||²); FIRST S4.E6 uses GaussianLSI AND TalagrandT2','PAPER'),
 ('FULL-LSI-GAP','SOURCE_GAP','Full Gaussian LSI for actual noncompact square-root density32 remains open','PAPER'),
 ('T2-GAP','SOURCE_GAP','Gaussian Talagrand with genuine metric/moment/KL adapters remains open','PAPER'),
 ('COMPACT','SOURCE_EXTERNAL_ASSUMPTIONS','f:Real->Real; ContDiff Real2 f AND HasCompactSupport f; unrestricted sign, no normalized mass','GENERIC'),
 ('CUBE','AUTHORED_DEFINITION','B_N=Fin N->Bool, canonical finite measurable cube, decidable equality and nonempty','AUTHORED'),
 ('COUNT','AUTHORED_DEFINITION','mu_N=card(B_N)^(-1) smul count, ENNReal coefficient','AUTHORED'),
 ('SUM','AUTHORED_DEFINITION','S_N=1/sqrtN * sum_j sigma(eps_j); sigma(true)=1,false=-1','AUTHORED'),
 ('FLIP','AUTHORED_DEFINITION','flip_j eps=Function.update eps j (!eps_j)','AUTHORED'),
 ('GAMMA','DEFINITION','gamma=gaussianReal0(1:NNReal), mean0 scalar variance1','GENERIC'),
 ('ENERGY','AUTHORED_DEFINITION','D_N=sum_j (f(S_N flip_j eps)-f(S_N eps))², full flip and integral-of-sum','AUTHORED'),
 ('API-DERIV','LOCAL_PINNED_API','ContDiff.deriv\u0027/iterate_deriv\u0027/differentiable_deriv_two and continuous_deriv; specialize all scalar normed classes to Real'),
 ('API-SUPPORT','LOCAL_PINNED_API','HasCompactSupport.deriv twice; support_deriv subset tsupport'),
 ('API-BOUND','LOCAL_PINNED_API','Generated additive HasCompactSupport.exists_bound_of_continuous, choose max0 of bound'),
 ('API-MVT','LOCAL_PINNED_API','exists_deriv_eq_slope: ordered a<b, ContinuousOn Icc, DifferentiableOn Ioo; specialize scalarReal'),
 ('API-LIP','LOCAL_PINNED_API','Convex.norm_image_sub_le_of_norm_deriv_le on univ; optional root LipschitzWith NNReal wrapper'),
 ('API-SUM','LOCAL_PINNED_API','Generated additive sum_update_of_mem / sum_erase_add; finite sum algebra'),
 ('API-FINITE','LOCAL_PINNED_API','Fintype.card_pos; count.isFiniteMeasure/count_univ; Measure.smul_finite requires coefficient!=top'),
 ('API-L1','LOCAL_PINNED_API','Integrable.of_finite requires Finite cube, measurable singletons AND IsFiniteMeasure mu'),
 ('API-INTEGRAL','LOCAL_PINNED_API','integral_finsetSum, integral_sub, norm_integral_le_of_norm_le_const, integral_const; every required L1 and actual mass retained'),
 ('API-FINITE-FORMULA','LOCAL_PINNED_API','integral_fintype still requires Integrable, no totalized-integral fake closure'),
 ('API-LIMIT','LOCAL_PINNED_API','Real.tendsto_sqrt_atTop and tendsto_inv_atTop_zero, successor cast divergence'),
 ('API-PERM','LOCAL_PINNED_API','measurePreserving_piCongrLeft on finite products; permutation pullback integral primitive'),
 ('REGULARITY','DERIVED','C2 -> fprime continuous/differentiable, fsecond continuous; support twice compact, no fthird'),
 ('B','DERIVED','Internally exists B>=0, everyx |fprime x|<=B'),
 ('K','DERIVED','Internally exists K>=0, everyx |fsecond x|<=K'),
 ('LIP-PRIME','AUTHORED_DERIVED','Global |fprime a-fprime b|<=K|a-b| from C2 and K, never public Lipschitz certificate','AUTHORED'),
 ('MASS1','AUTHORED_DERIVED','Actual count cardinal>0 finite; mu_N univ=1 and finite measure for EVERY N including0','AUTHORED'),
 ('L1-COUNT','AUTHORED_DERIVED','Every finite coordinate square, full sum, fprime(S_N)² and their difference Bochner L1','AUTHORED'),
 ('N0','AUTHORED_DERIVED','N0 cube singleton, mu0 mass1, S0=0, D0 empty sum=0 genuine L1','AUTHORED'),
 ('N-POS','DERIVED','Only successor N=n+1>0: sqrtN>0 and sqrtN²=N, no public NeZero N premise'),
 ('BOOL-STEP','SOURCE_GAP_AUTHORED_ADAPTER','Actual pointwise S_N(flip_j eps)-S_N eps=-2 sigma(eps_j)/sqrtN; |step|=2/sqrtN','AUTHORED'),
 ('BOOL-SECANT','SOURCE_GAP_AUTHORED_ADAPTER','MVT at signed step gives a_j=fprime(xi_j), |xi_j-S_N|<=delta and |a_j|<=B','AUTHORED'),
 ('BOOL-SQERROR','SOURCE_GAP_AUTHORED_ADAPTER','|a_j²-fprime(S_N)²|<=2BKdelta=4BK/sqrtN','AUTHORED'),
 ('BOOL-SUMERROR','SOURCE_GAP_AUTHORED_ADAPTER','Ndelta²=4; pointwise |D_N-4 fprime(S_N)²|<=16BK/sqrtN','AUTHORED'),
 ('BOOL-INTERROR','SOURCE_GAP_AUTHORED_ADAPTER','Actual mu_N integral difference bounded16BK/sqrtN, error tends0 on successor','AUTHORED'),
 ('PARENT36','FORMAL_CANDIDATE_INTERFACE','Exact sealed36 same count/S/gamma derivative-square successor limit AND Gaussian derivative-square L1; independent admitted state pending/not certified by author','AUTHORED'),
 ('ACTUAL-LIMIT','SOURCE_GAP_AUTHORED_ADAPTER','Actual integral-of-fullsum successor ->4 integral fprime² gamma; domains output not hypotheses','AUTHORED'),
 ('SLT-MEASURE','EXTERNAL_DEFINITION','rademacherMeasure=(1/2)dirac(-1)+(1/2)dirac1, real measure probability'),
 ('SLT-PRODUCT','EXTERNAL_DEFINITION','RademacherSpaceN=FinN->Real; Measure.pi of identical actual Rademacher measures, probability'),
 ('SLT-SUM','EXTERNAL_DEFINITION','rademacherSumProdN x=inverse sqrtN * sum_i x_i; measurable'),
 ('SLT-AE','EXTERNAL_DERIVED','Every coordinate ±1 AE under real-product measure, not pointwise for arbitrary real x'),
 ('SLT-ENDPOINTS','EXTERNAL_DEFINITION','aPlus=S+(1-x_i)/sqrtN; aMinus=S-(1+x_i)/sqrtN, difference2/sqrtN'),
 ('SLT-GAUSSIAN','EXTERNAL_DEFINITION','stdGaussian=ProbabilityMeasure(gaussianReal0 1); stdGaussianMeasure=stdGaussian.toMeasure'),
 ('SLT-LAW','EXTERNAL_DEFINITION','rademacherLawN=(product measure).map actual S, for NeZeroN source standing scope'),
 ('SLT-BCF','EXTERNAL_DERIVED','derivSqToBCF genuine continuous bounded fprime² using B'),
 ('SLT-WEAK','IMPORTED_BACKGROUND_BOUNDARY','rademacherLaw_tendsto_stdGaussian and weak-integral primitive imported/caller-reference; earlier law/observer packet, not new CLT credit'),
 ('SLT-OBSERVER','EXTERNAL_DERIVED','tendsto_integral_deriv_sq on actual law with derivative BCF, then product map integral transport'),
 ('SLT-L1-BOUND','EXTERNAL_DERIVED','integrable_sq_of_bounded: actual finite measure + AEStronglyMeasurable + bound C>=0'),
 ('SLT-DERIV-L1','EXTERNAL_DERIVED','Actual product fprime(S)² L1 from continuous derivative, measurable S, bound B'),
 ('SLT-SECANT','EXTERNAL_DEFINITION_DERIVED','rescaledDiff=sqrtN/2*(f(aPlus)-f(aMinus))=fprime(xi) with xi between endpoints'),
 ('SLT-SQERROR','EXTERNAL_DERIVED','AE sign identifies S with endpoint; secant-square error<=4KB/sqrtN, MVT for fprime'),
 ('SLT-N4','EXTERNAL_DERIVED','N integral endpoint-difference²=4 integral rescaledDiff² using sqrtN²=N'),
 ('SLT-INTERROR','EXTERNAL_DERIVED','Genuine rescaled/derivative L1, integral_sub, abs/integral monotonicity, probability mass; error16KB/sqrtN ->0'),
 ('SLT-NLIMIT','EXTERNAL_DERIVED','N times single endpoint-difference integral ->4 Gaussian derivative-square integral using observer'),
 ('SLT-PERM','EXTERNAL_DERIVED','Coordinate swaps preserve actual product law and S; endpoints/shift intertwine, all coordinate integrals equal'),
 ('SLT-SUMLIMIT','EXTERNAL_DERIVED','Source sum of endpoint-difference integrals ->4 Gaussian derivative-square integral'),
 ('SLT-SHIFT','EXTERNAL_DEFINITION','rademacherSumShiftedN i x=S_N x-2*x_i/sqrtN; measurable'),
 ('SLT-SHIFT-AE','EXTERNAL_DERIVED','Plus/minus square equals S/shift square for ±1 coordinate, hence AE then integral_congr_ae'),
 ('SLT-ENERGY-LIMIT','EXTERNAL_DERIVED','Source sum_i integral (f(S)-f(shift_i))² ->4 integral fprime² stdGaussianMeasure'),
 ('CARRIER-ADAPTER','SOURCE_GAP_AUTHORED_ADAPTER','Bool normalizedcount pushforward to actual real product, same S/flip intertwining and gamma identity required if source route reused','AUTHORED'),
 ('FINITE-SUM-ADAPTER','SOURCE_GAP_AUTHORED_ADAPTER','Actual fullsum integral equals sum of actual coordinate integrals using each L1; reverse square sign is algebra','AUTHORED'),
 ('BERNOULLI34','FORMAL_CANDIDATE_INTERFACE','Actual34 fullflip Bernoulli inequality for arbitrary h on true mu_N, domains internally produced, exact1/2'),
 ('ENTROPY36','FORMAL_CANDIDATE_INTERFACE','Same actual mu/S/gamma homogeneous entropy successor limit incl f=0/zero mass; not a new source completion'),
 ('COMPACT-LSI','SOURCE_GAP','Later compact scalar Ent_gamma(f²)<=2 integral fprime² gamma from34,36,37; not produced in this graph'),
 ('NONCOMPACT-HILBERT-GAP','SOURCE_GAP','Cutoff/W12 for actual32 sqrt-RN and finite Hilbert extension still open'),
 ('IMPORTED-L1-PRIMITIVES','IMPORTED_PRIMITIVE_BOUNDARY','Integrable.of_bound, AEStronglyMeasurable composition/pow/sub, integral_mono_ae, abs_integral_le_integral_abs, integral_congr_ae, integral_map. Caller-anchored source primitive group; no new ASTIS compilation certificate.'),
 ('IMPORTED-SUPPORT-PRIMITIVES','IMPORTED_PRIMITIVE_BOUNDARY','HasCompactSupport.of_support_subset_isCompact, closed tsupport and local-zero neighborhood, Filter.EventuallyEq.deriv applied twice; source support proof primitives.'),
 ('IMPORTED-LIMIT-PRIMITIVES','IMPORTED_PRIMITIVE_BOUNDARY','Real algebra/sqrt_sq, finite-sum/cardinality algebra, Tendsto.add/const_mul and squeeze, successor nat casts. Actual source-called background, not new producer.')]:node(*args)

use('FIRST','FULL-LSI-GAP T2-GAP','PRINTED_SOURCE_USE','S4.E6 / S4.SS1.p4.3')
use('FULL-LSI-GAP','COMPACT-LSI NONCOMPACT-HILBERT-GAP','DEPENDENCY_BOUNDARY')
use('COMPACT-LSI','BERNOULLI34 ENTROPY36 ACTUAL-LIMIT','AUTHORED_DEPENDENCY','SLT OneDimGLSICompSmo50-82','Actual same-family limits and half*4=2; no theorem credit')
use('COUNT','CUBE','AUTHORED_DEFINITION_USE');use('SUM','CUBE','AUTHORED_DEFINITION_USE');use('FLIP','CUBE','AUTHORED_DEFINITION_USE')
use('ENERGY','COMPACT SUM FLIP CUBE','AUTHORED_DEFINITION_USE')
use('REGULARITY','COMPACT API-DERIV API-SUPPORT','AUTHORED_DERIVED_USE')
use('B','REGULARITY API-BOUND','EXTERNAL_SOURCE_USE','TaylorBound158-221')
use('K','REGULARITY API-BOUND','EXTERNAL_SOURCE_USE','TaylorBound77-156')
use('LIP-PRIME','REGULARITY K API-LIP','AUTHORED_DERIVED_USE')
use('MASS1','CUBE COUNT API-FINITE','AUTHORED_DERIVED_USE')
use('L1-COUNT','CUBE COUNT MASS1 ENERGY SUM REGULARITY API-L1','AUTHORED_DERIVED_USE')
use('N0','CUBE COUNT SUM ENERGY MASS1 L1-COUNT','AUTHORED_DERIVED_USE')
use('N-POS','API-LIMIT','AUTHORED_DERIVED_USE',ingredient='Internal positive successor cast and sqrt identities; API source background')
use('BOOL-STEP','FLIP SUM CUBE API-SUM N-POS','AUTHORED_ADAPTER_USE')
use('BOOL-SECANT','BOOL-STEP COMPACT REGULARITY API-MVT B N-POS','AUTHORED_ADAPTER_USE')
use('BOOL-SQERROR','BOOL-SECANT LIP-PRIME B K BOOL-STEP','AUTHORED_ADAPTER_USE')
use('BOOL-SUMERROR','BOOL-SQERROR BOOL-STEP N-POS ENERGY API-SUM','AUTHORED_ADAPTER_USE')
use('BOOL-INTERROR','BOOL-SUMERROR MASS1 L1-COUNT API-INTEGRAL API-LIMIT','AUTHORED_ADAPTER_USE')
use('PARENT36','COMPACT COUNT SUM GAMMA','INTERFACE_DEFINITION_USE',ingredient='Exact public interface inputs/literal definitions only; pending admission, no body read')
use('ACTUAL-LIMIT','BOOL-INTERROR PARENT36 N0 L1-COUNT API-LIMIT','AUTHORED_ADAPTER_USE')
use('SLT-PRODUCT','SLT-MEASURE','EXTERNAL_SOURCE_USE','EfronSteinApp351-359')
use('SLT-SUM','SLT-PRODUCT','EXTERNAL_SOURCE_USE','EfronSteinApp387-401')
use('SLT-AE','SLT-PRODUCT SLT-MEASURE','EXTERNAL_SOURCE_USE','EfronSteinApp324-346,366-406','Actual coordinate marginal pushforward and measure-map/AE support primitive')
use('SLT-ENDPOINTS','SLT-SUM N-POS','EXTERNAL_SOURCE_USE','EfronSteinApp409-414 / TaylorBound42-45')
use('SLT-LAW','SLT-PRODUCT SLT-SUM','EXTERNAL_SOURCE_USE','Limit90-94')
use('SLT-BCF','REGULARITY B','EXTERNAL_SOURCE_USE','Limit316-333')
use('SLT-OBSERVER','SLT-LAW SLT-BCF SLT-WEAK SLT-GAUSSIAN','EXTERNAL_SOURCE_USE','Limit355-362')
use('REGULARITY','IMPORTED-SUPPORT-PRIMITIVES API-DERIV','EXTERNAL_SOURCE_USE','TaylorBound81-128,161-197','Actual external C2 derivative/support derivation; API-SUPPORT is separate authored local shortcut')
use('SLT-L1-BOUND','IMPORTED-L1-PRIMITIVES IMPORTED-LIMIT-PRIMITIVES','EXTERNAL_SOURCE_USE','EfronSteinApp83-96','Integrable.of_bound, AEStronglyMeasurable pow and nonnegative real square bound')
use('SLT-DERIV-L1','SLT-PRODUCT SLT-SUM REGULARITY B SLT-L1-BOUND API-BOUND','EXTERNAL_SOURCE_USE','TaylorBound553-564')
use('SLT-SECANT','SLT-ENDPOINTS COMPACT REGULARITY N-POS API-MVT B','EXTERNAL_SOURCE_USE','Limit597-634')
use('SLT-SQERROR','SLT-SECANT SLT-AE SLT-ENDPOINTS K B REGULARITY API-MVT','EXTERNAL_SOURCE_USE','Limit638-725')
use('SLT-N4','SLT-SECANT N-POS API-INTEGRAL','EXTERNAL_SOURCE_USE','Limit728-742')
use('SLT-INTERROR','SLT-SQERROR SLT-N4 SLT-L1-BOUND SLT-DERIV-L1 SLT-PRODUCT SLT-SUM B API-INTEGRAL API-LIMIT','EXTERNAL_SOURCE_USE','Limit749-832')
use('SLT-INTERROR','IMPORTED-L1-PRIMITIVES IMPORTED-LIMIT-PRIMITIVES','EXTERNAL_SOURCE_USE','Limit749-832')
use('SLT-NLIMIT','SLT-INTERROR SLT-OBSERVER SLT-LAW SLT-SUM SLT-PRODUCT API-INTEGRAL','EXTERNAL_SOURCE_USE','Limit840-881','Actual product map integral transport and add/const_mul limits')
use('SLT-NLIMIT','IMPORTED-L1-PRIMITIVES IMPORTED-LIMIT-PRIMITIVES','EXTERNAL_SOURCE_USE','Limit840-881')
use('SLT-PERM','SLT-PRODUCT SLT-SUM SLT-ENDPOINTS API-PERM API-SUM','EXTERNAL_SOURCE_USE','Limit904-941,1046-1115')
use('SLT-SUMLIMIT','SLT-PERM SLT-NLIMIT API-SUM','EXTERNAL_SOURCE_USE','Limit891-943')
use('SLT-SHIFT','SLT-SUM N-POS','EXTERNAL_SOURCE_USE','Limit947-955')
use('SLT-SHIFT-AE','SLT-SHIFT SLT-ENDPOINTS SLT-AE SLT-SUM API-INTEGRAL','EXTERNAL_SOURCE_USE','Limit958-1019')
use('SLT-SHIFT-AE','IMPORTED-L1-PRIMITIVES','EXTERNAL_SOURCE_USE','Limit1014-1019')
use('SLT-ENERGY-LIMIT','SLT-SUMLIMIT SLT-SHIFT-AE SLT-PERM SLT-SHIFT SLT-GAUSSIAN API-SUM','EXTERNAL_SOURCE_USE','Limit1030-1123')
use('CARRIER-ADAPTER','CUBE COUNT MASS1 SUM FLIP GAMMA SLT-PRODUCT SLT-SUM SLT-SHIFT SLT-GAUSSIAN','DEPENDENCY_BOUNDARY',ingredient='Authored representation adapter absent from source; cannot mark external proven')
use('FINITE-SUM-ADAPTER','L1-COUNT MASS1 ENERGY API-INTEGRAL API-FINITE-FORMULA','AUTHORED_ADAPTER_USE')
use('ACTUAL-LIMIT','SLT-ENERGY-LIMIT CARRIER-ADAPTER FINITE-SUM-ADAPTER N0','AUTHORED_ALTERNATIVE_ROUTE_USE')

idset={n['id'] for n in nodes}; assert all(e['from_node'] in idset and e['to_node'] in idset for e in edges)
selected=json.loads((OLD/'source-regions.json').read_text())['regions']
# Disjoint per-file selected physical line sets, reusing unchanged preread regions.
spanmap={}
for r in selected:spanmap.setdefault(r['path'],set()).update(range(r['lines'][0],r['lines'][1]+1))
def add(path,a,z):spanmap.setdefault(path,set()).update(range(a,z+1))
add(A+'SLT__GaussianPoincare__RademacherApprox.lean.raw.snapshot',43,57)
add(A+'SLT__GaussianPoincare__RademacherApprox.lean.raw.snapshot',118,122)
for a,z in [(54,96),(322,414)]:add(A+'SLT__GaussianPoincare__EfronSteinApp.lean.raw.snapshot',a,z)
for a,z in [(38,45),(90,94),(148,151),(286,336),(355,362)]:add(A+'SLT__GaussianPoincare__Limit.lean.raw.snapshot',a,z)
add(A+'SLT__GaussianPoincare__TaylorBound.lean.raw.snapshot',550,660)
add(M+'MeasureTheory/Constructions/Pi.lean',732,739)
add(M+'MeasureTheory/Integral/Bochner/Basic.lean',944,945)
add(M+'MeasureTheory/Integral/Bochner/Basic.lean',1032,1053)
add(M+'Analysis/Calculus/Deriv/Basic.lean',641,656)

default={
 'ContDiff/Deriv.lean':'API-DERIV','Deriv/Support.lean':'API-SUPPORT','Deriv/Basic.lean':'IMPORTED-SUPPORT-PRIMITIVES','Normed/Group/Bounded.lean':'API-BOUND','Calculus/MeanValue.lean':'API-LIP','Deriv/MeanValue.lean':'API-MVT','Finset/Piecewise.lean':'API-SUM','Finset/Basic.lean':'API-SUM','Fintype/Card.lean':'API-FINITE','Measure/Count.lean':'API-FINITE','Typeclasses/Finite.lean':'API-FINITE','L1Space/Integrable.lean':'API-L1','Bochner/Basic.lean':'API-INTEGRAL','Bochner/SumMeasure.lean':'API-FINITE-FORMULA','Real/Sqrt.lean':'API-LIMIT','Order/Field.lean':'API-LIMIT','Constructions/Pi.lean':'API-PERM'}
special={
 A+'SLT__GaussianPoincare__RademacherApprox.lean.raw.snapshot':[(43,57,'SLT-MEASURE'),(118,122,'SLT-AE')],
 A+'SLT__GaussianPoincare__EfronSteinApp.lean.raw.snapshot':[(47,48,'COMPACT'),(54,81,'B'),(83,96,'SLT-L1-BOUND'),(322,346,'SLT-AE'),(348,359,'SLT-PRODUCT'),(361,373,'SLT-AE'),(386,401,'SLT-SUM'),(403,406,'SLT-AE'),(408,414,'SLT-ENDPOINTS')],
 A+'SLT__GaussianPoincare__TaylorBound.lean.raw.snapshot':[(35,45,'SLT-ENDPOINTS'),(78,87,'REGULARITY'),(88,128,'REGULARITY'),(130,156,'K'),(158,198,'REGULARITY'),(199,221,'B'),(230,239,'REGULARITY'),(550,564,'SLT-DERIV-L1')],
 A+'SLT__GaussianPoincare__Limit.lean.raw.snapshot':[(38,40,'SLT-GAUSSIAN'),(42,45,'API-LIMIT'),(90,94,'SLT-LAW'),(148,151,'SLT-GAUSSIAN'),(286,298,'SLT-BCF'),(315,333,'SLT-BCF'),(355,362,'SLT-OBSERVER'),(593,626,'SLT-SECANT'),(628,634,'SLT-SECANT'),(637,725,'SLT-SQERROR'),(727,742,'SLT-N4'),(744,832,'SLT-INTERROR'),(834,881,'SLT-NLIMIT'),(883,943,'SLT-SUMLIMIT'),(945,955,'SLT-SHIFT'),(957,1019,'SLT-SHIFT-AE'),(1021,1123,'SLT-ENERGY-LIMIT')],
 A+'SLT__GaussianLSI__BernoulliLSI.lean.raw.snapshot':[(1600,1632,'BERNOULLI34')],
 A+'SLT__GaussianLSI__OneDimGLSICompSmo.lean.raw.snapshot':[(45,82,'COMPACT-LSI')],
 A+'SLT__GaussianLSI__Entropy.lean.raw.snapshot':[(34,49,'ENTROPY36')]}
exclusions={
 M+'Analysis/Calculus/ContDiff/Deriv.lean':[(87,89,'Tail of on-set derivative theorem not needed in global scalar target'),(103,107,'Infinity regularity specialization unnecessary for C2'),(120,124,'WithinAt/on-set variant unused'),(129,134,'C-infinity iterate not required'),(140,141,'Section closing context')],
 M+'Analysis/Calculus/MeanValue.lean':[(697,728,'Within-set variants not used by chosen global derivative bound; retained exact context only')],
 M+'MeasureTheory/Integral/Bochner/Basic.lean':[(252,260,'Integral_neg variants not needed by difference route')],
 A+'SLT__GaussianPoincare__TaylorBound.lean.raw.snapshot':[(47,61,'Selected prefix of variance-specific squared deviation lemma, unused by full energy/secant route; remainder outside selected slice'),(223,228,'IteratedDeriv/Taylor preliminaries unnecessary for this direct MVT energy increment'),(240,241,'Start of separate Taylor remainder proof, excluded'),(566,660,'Derivative-absolute and EfronStein variance/Taylor consumers, not fullenergy producer')],
 A+'SLT__GaussianPoincare__EfronSteinApp.lean.raw.snapshot':[(54,81,'General f boundedness/composition helper context not called by selected rescaled/secant energy proof; first derivative bound is retained separately'),(375,384,'Coordinate independence not used by energy symmetry proof, earlier law/CLT boundary')],
 A+'SLT__GaussianPoincare__Limit.lean.raw.snapshot':[(286,314,'First-derivative and absolute-derivative BCFs are not called by direct derivSqToBCF constructor')],
 A+'SLT__GaussianLSI__BernoulliLSI.lean.raw.snapshot':[(1633,1634,'Namespace closing context')]
}
inventory=[]
for path,linenos in spanmap.items():
 b=(OUT/pinned[path]['raw_snapshot']).read_bytes(); lines=b.splitlines(keepends=True)
 assignments={}
 for i in sorted(linenos):
  assert i<=len(lines)
  label=None
  for a,z,reason in exclusions.get(path,[]):
   if a<=i<=z:label=('EXCLUDED',reason);break
  if label is None:
   for a,z,n in special.get(path,[]):
    if a<=i<=z:label=('NODE',n);break
  if label is None:
   n=next((v for k,v in default.items() if path.endswith(k)),None)
   label=('NODE',n) if n else ('EXCLUDED','Blank/comment/section context outside selected required theorem statements and proofs')
  assignments[i]=label
 ordered=sorted(assignments);start=prev=ordered[0];label=assignments[start]
 def flush(a,z,tag):
  rb=b''.join(lines[a-1:z]);i=len(inventory);rn='region.%03d.raw.snapshot'%i;ln=rn.replace('.raw.','.lf.')
  (OUT/rn).open('xb').write(rb);(OUT/ln).open('xb').write(lf(rb))
  q=dict(id='r%03d'%i,path=path,lines=[a,z],disposition=tag[0],node_ids=[tag[1]] if tag[0]=='NODE' else [],exclusion_reason=tag[1] if tag[0]=='EXCLUDED' else None,raw_sha256=sha(rb),lf_sha256=sha(lf(rb)),raw_snapshot=rn,lf_snapshot=ln)
  inventory.append(q)
  if tag[0]=='NODE':next(n for n in nodes if n['id']==tag[1])['anchors'].append(dict(path=path,lines=[a,z],raw_sha256=q['raw_sha256']))
 for i in ordered[1:]:
  if i!=prev+1 or assignments[i]!=label:flush(start,prev,label);start=i;label=assignments[i]
  prev=i
 flush(start,prev,label)
 # Mechanical author inventory construction check, explicitly NOT independent topology validation.
 covered=[i for x in inventory if x['path']==path for i in range(x['lines'][0],x['lines'][1]+1)]
 assert len(covered)==len(set(covered)) and set(covered)==linenos

for id,path in [('PARENT36',P+'gaussian-compact-entropy/preproof/signature.prospective.txt'),('BERNOULLI34',P+'bernoulli-function-lsi/preproof/bernoulli.signature.txt')]:
 next(n for n in nodes if n['id']==id)['anchors'].append(dict(path=path,raw_sha256=pinned[path]['raw_sha256'],kind='exact public signature, no body'))
primary=[dict(anchor='S4.E6',path=P+'gaussian-clt-entropy-preread/primary.S4.E6.raw.snapshot.html',node_ids=['FIRST'],disposition='NODE',raw_sha256=pinned[P+'gaussian-clt-entropy-preread/primary.S4.E6.raw.snapshot.html']['raw_sha256'],exclusions='Second eta-Lipschitz and last eta sqrt d inequalities excluded from37 credit'),dict(anchor='S4.SS1.p4.3',path=P+'gaussian-clt-entropy-preread/primary.S4.SS1.p4.3.raw.snapshot.html',node_ids=['FIRST','FULL-LSI-GAP','T2-GAP'],disposition='NODE',raw_sha256=pinned[P+'gaussian-clt-entropy-preread/primary.S4.SS1.p4.3.raw.snapshot.html']['raw_sha256'],exclusions='Neighboring mode/IBP and Lipschitz steps excluded')]
contract=dict(schema_version=1,kind='SOURCE_ONLY_AUTHORED_BACKGROUND_CONTRACT',status='FROZEN_NOT_INDEPENDENTLY_VALIDATED',printed_scope='SPHMC FIRST4.6 cites GaussianLSI+Talagrand and omits this Bernoulli/flip-energy background;37 is NOT a separately printed paper theorem.',target_name='AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianFlipEnergy.compact_count_gaussian_flip_energy_limit',target_path=target,target_raw_sha256=pinned[target]['raw_sha256'],target_lf_sha256=pinned[target]['lf_sha256'],seven_slots=dict(space_metric='Real scalar variance1 Gaussian; actual finite Bool cube, full coordinate flip, no altered metric',inputs='Only f, C2 and compact support; external CompactlySupportedSmooth expands precisely to these two assumptions',domains='All finite L1 and Gaussian derivative-square L1 produced internally; mass1 and measurable cube/S retained',laws='Actual count/card normalized mu_N, exact signed sum S_N, gamma=gaussianReal0(1:NNReal)',representatives='Bool route signs true at every point; source real-product signs only AE, never arbitrary real-point identity',quantifiers='allN output finite domain incl0; limit successor n+1 positive internally, no public NeZeroN',constant_zero='Fullflip delta2/sqrtN, Ndelta²=4, uniformerror16BK/sqrtN, unrestricted sign, B/K=0 and f=0/no positive entropy mass'),binder_classification=[dict(binder='f:Real->Real',kind='DEFINITION_INPUT'),dict(binder='hf:ContDiff Real2 f',kind='EXTERNAL_SOURCE_ASSUMPTION',retained_source='EfronSteinApp47-48'),dict(binder='hs:HasCompactSupport f',kind='EXTERNAL_SOURCE_ASSUMPTION',retained_source='EfronSteinApp47-48')],canonical_typeclass_expansion='Real canonical normed field/additive group/complete space/Borel measurable topology; FinN Fintype/Finite/DecidableEq/Nonempty; Bool standard discrete measurable singleton and finite instances; Pi finite cube measurable structure; Gaussian probability instance. These are canonical carrier instances, not supplied probability/L1/limit certificates.',derived_internal=['positive finite card, inverse coefficient finite, actual mu_N mass1','everyN energy/summand/error genuine Bochner L1','fprime/fsecond continuous and compact, internal B,K>=0','positive successor sqrt, pointwise signed Bool displacement','36 same-count derivative observer when actually called internally'],excess_binders=[],definition_audit='Mu coefficient is inverse ENNReal cardinal, not arbitrary weights; S has sigma(true)=+1,false=-1, sqrt scaling; flip toggles literal coordinate, no divided gradient. Actual energy is integral of sum; source final theorem sum of integrals requires finite integral-sum adapter and square sign reversal. Gamma variance parameter is NNReal1, not stddev2.',parent_truth='36 exact sealed interface only; root reports focused pass/review active. Admission/compiled producer certification remains distinct. It becomes a genuine formal parent only if future37 proof calls it.',no_C3_or_mass_or_certificate=True,primary=primary,compiled_edges=[],independent_validation='REQUIRED_DISTINCT_PHASE_NO_AUTHOR_SELFVALIDATION')
emit('source.contract.json',contract)
graph=dict(schema_version=1,artifact_kind='implementation-independent-source-proof-graph',status='AUTHORED_FROZEN_PENDING_DISTINCT_TOPOLOGY_REVIEW',author='gaussian_domain_preproof_reviewer_29',target=contract['target_name'],source_contract='source.contract.json',target_exact_binding=pinned[target],nodes=nodes,edges=edges,OR_routes=[dict(id='OR-DIRECT-BOOL',provenance='AUTHORED_MATHEMATICAL_BACKGROUND_NOT_PRINTED_SOURCE',terminal='ACTUAL-LIMIT',requires=['BOOL-INTERROR','PARENT36','N0','L1-COUNT'],route='Per-coordinate exact Boolean fullflip + uniform secant error + SAME derivative-square observer36. Does not need realproduct symmetry/carrier transport.'),dict(id='OR-SLT-REALPRODUCT',provenance='EXTERNAL_SOURCE_ROUTE_PLUS_EXPLICIT_AUTHORED_ADAPTERS',terminal='ACTUAL-LIMIT',requires=['SLT-ENERGY-LIMIT','CARRIER-ADAPTER','FINITE-SUM-ADAPTER','N0'],route='Source full shift energy on real product; then genuine Boolcount carrier/flip/pushforward and sum integral adapters, no given law/domain/energy certificate.')],compiled_edges=[],source_inventory='source.inventory.json',external_imported_primitive_annotations=['measurePreserving_piCongrLeft/MeasurePreserving.integral_comp\u0027 and pi_map_eval/AE support are source-used primitives, not newly proved ASTIS results.','SLT weak-law/BCF integral and integral_map imported background remains caller-anchored boundary, not re-proven or certified here.','Limit stdGaussian38-40 and stdGaussianMeasure149-151 identify exact mean0 variance1 canonical Gaussian, no inferred posterior or covariance transport.'],remaining_truth_boundary=['compactGaussianLSI final34+36+37 comparison','noncompact32 sqrt-RN cutoff/W12','finiteHilbert dimension extension','GaussianLSI','GaussianTalagrandT2','SPHMC FIRST4.6','bias/main/work/cost/composition'],no_implementation_exposure=True,no_compiler=True,no_statementseal_or_SAU_claim=True)
emit('source-proof-graph.independent.json',graph)
emit('source.inventory.json',dict(status='AUTHOR_MECHANICAL_ENUMERATION_NOT_TOPOLOGY_ACCEPTANCE',scope='Every selected physical line of bounded pinned37/unchanged36 background/API slices; no entire upstream project coverage claim',primary_balanced_spans=primary,selected_files=[dict(path=p,selected_lines=len(s)) for p,s in spanmap.items()],regions=inventory,coverage_count=len(inventory),physical_lines=sum(map(len,spanmap.values())),outside_selected='All remaining upstream file/project regions including EfronStein variance, other observers, CLT proof, GaussianLSI extensions/cutoff/T2/paper main are excluded from this increment; frozen full source files serve bytepins, not completion credit.'))
oldpacket=json.loads((OLD/'source-detail-packet.json').read_text())
emit('bounded-synthesis.json',dict(status='CLOSED_SOURCE_AUTHORING_REQUIRES_DISTINCT_REVIEW',synthesis_first='Two distinct OR routes reach the same actual fullflip energy factor4; direct Bool route requires authored pointwise flip/secant/integral adapters and internally reused36 derivative observer, source realproduct route retains AE/permutation/measure domains plus authored carrier/finite-sum adapters.',route_at_most_seven_steps=oldpacket['route_at_most_seven_steps'],counts=dict(nodes=len(nodes),edges=len(edges),OR_routes=2,regions=len(inventory),physical_lines=sum(map(len,spanmap.values())),inputs=len(bindings)),first_unmet_dependency=oldpacket['typed_blockers'][0],parent36_truth=contract['parent_truth'],remaining_open=graph['remaining_truth_boundary'],author_not_validator=True,compiled_edges=[]))
emit('bindings.json',dict(inputs=bindings,raw_LF_checked=True,source_pins_match_reused_closure=True))
# Check frozen originals again without reading future implementation or active compiler artifacts.
for e in bindings:
 b=(ROOT/e['path']).read_bytes();assert sha(b)==e['raw_sha256'] and sha(lf(b))==e['lf_sha256']
outs=[]
for f in ['source.contract.json','source-proof-graph.independent.json','source.inventory.json','bounded-synthesis.json','bindings.json','author.py']:
 b=(OUT/f).read_bytes();outs.append(dict(path=P+'gaussian-flip-energy-source-graph/'+f,raw_sha256=sha(b),lf_sha256=sha(lf(b))))
runid=sha(json.dumps(dict(inputs=bindings,outputs=outs),sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())
emit('run.closed.json',dict(deterministic_run_sha256=runid,inputs_count=len(bindings),outputs=outs,mechanical_author_checks=['All selected physical lines assigned exactly once NODE or EXCLUDED','All declared edge endpoints are known nodes','All bound originals raw/LF unchanged; original preread immutable','Checks are author construction invariants, NOT independent source/topology acceptance'],read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False))
lease=json.loads((OUT/'lease.json').read_text());lease.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,closed_utc=datetime.datetime.utcnow().isoformat()+'Z',deterministic_run_sha256=runid)
(OUT/'lease.json').write_bytes((json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(dict(run=runid,nodes=len(nodes),edges=len(edges),regions=len(inventory),physical_lines=sum(map(len,spanmap.values())),inputs=len(bindings),graph_sha256=sha((OUT/'source-proof-graph.independent.json').read_bytes()),status='CLOSED')))
