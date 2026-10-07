import json, hashlib, re, datetime
from pathlib import Path

ROOT = Path('E:/Samplinglib')
BASE = ROOT / 'runs/20261007-companion-priority/gaussian-compact-entropy-source-graph'
PR = 'runs/20261007-companion-priority/gaussian-compact-entropy-preread/'
EXT = 'runs/20261007-companion-priority/gaussian-functional-availability/'
ML = '.lake/packages/mathlib/Mathlib/'
def sha(b): return hashlib.sha256(b).hexdigest()
def lf(b): return b.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
def write(name, value):
    b = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    with (BASE / name).open('xb') as f: f.write(b)
    return {'path': str((BASE/name).relative_to(ROOT)).replace('\\','/'), 'raw_sha256': sha(b), 'lf_sha256': sha(lf(b)), 'bytes': len(b)}

packet = json.loads((ROOT / (PR+'source-detail-packet.json')).read_text(encoding='utf-8'))
inputs = []
def bind(path, expected=None):
    b = (ROOT/path).read_bytes(); x = {'path':path,'raw_sha256':sha(b),'lf_sha256':sha(lf(b)),'bytes':len(b)}
    if expected:
        for k in ['raw_sha256','lf_sha256','bytes']: assert x[k] == expected[k], (path,k)
    i=len(inputs)
    for typ, val in [('raw',b),('lf',lf(b))]:
        p=BASE/('input.%03d.%s.snapshot'%(i,typ))
        with p.open('xb') as f:f.write(val)
        x[typ+'_snapshot']=str(p.relative_to(ROOT)).replace('\\','/')
    inputs.append(x)
    return i
for x in packet['input_artifacts']: bind(x['path'],x)
for p in [PR+'source-detail-packet.json',PR+'lease.closed.json',PR+'run.closed.json',
          EXT+'SLT__GaussianPoincare__TaylorBound.lean.raw.snapshot',
          ML+'MeasureTheory/Measure/Typeclasses/Probability.lean',
          ML+'Topology/ContinuousMap/Bounded/Normed.lean',
          EXT+'LICENSE.raw.snapshot',EXT+'lean-toolchain.raw.snapshot',EXT+'lake-manifest.json.raw.snapshot']:
    bind(p)
by_path={x['path']:i for i,x in enumerate(inputs)}
N=[]; E=[]; blocks=[]; windows={}
def node(id,kind,formula,classification,provenance, boundary=None):
    N.append({'id':id,'kind':kind,'formula_or_contract':formula,'binder_classification':classification,
              'provenance':provenance,'truth_boundary':boundary or 'Source/API reconstruction only; no new compiled producer or independent validation.'})
def edge(src,dst,why,kind='SOURCE_USE',anchor=None):
    E.append({'id':'e%03d'%(len(E)+1),'from':src,'to':dst,'kind':kind,'ingredient':why,'anchor':anchor})
def src(id,path,a,b):
    blocks.append((path,a,b,id)); windows.setdefault(path,[]).append((a,b))
def footprint(path,a,b):windows.setdefault(path,[]).append((a,b))

node('P-RHO','SOURCE_CONTEXT','rho_y(u)=V(p+sqrt(eta)u)-V(p)-sqrt(eta)<grad V(p),u>; true r_y has density proportional to exp(-|u|^2/2-rho_y(u))','SOURCE','SPHMC S4.Ex8 and S4.SS1.p4.2','Context only; no theorem36 assumption about V, eta, rho or r is introduced.')
node('P-FIRST','ULTIMATE_SOURCE_CONSUMER','W2(r_y,N(0,I)) <= sqrt(E_r_y ||grad rho_y||^2)','SOURCE','SPHMC FIRST S4.E6 and S4.SS1.p4.3','OPEN: printed Gaussian T2 plus Gaussian LSI background; this compact scalar convergence delta is neither inequality nor full paper proof.')
node('F-CLASS','SOURCE_DEFINITION','CompactlySupportedSmooth f := ContDiff Real 2 f AND HasCompactSupport f','SOURCE_DEFINITION','SLT EfronSteinApp47-48','Exactly C2 plus compact support, not C-infinity; authored compact background restriction relative to SPHMC full LSI.')
node('OBSERVERS','AUTHORED_DEFINITION','A(x)=f(x)^2; T(t)=t*Real.log t; B(x)=T(A(x)); C(x)=(deriv f(x))^2','DEFINITION','Literal functions retained from SLT Limit and Entropy; no supplied representatives.')
node('ENTROPY','SOURCE_DEFINITION','Ent_mu(g)=integral(g*log g,mu)-(integral(g,mu))*log(integral(g,mu)); entropySquare_mu(f)=Ent_mu(f^2)','DEFINITION','SLT LogSobolev.entropy48-49, entropySquare124-125','Homogeneous entropy, not normalized KL. No mass-one or positive-mass premise; T(0)=0.')
node('COUNT-SUM','AUTHORED_DEFINITION','Omega_N=Fin N -> Bool; mu_N=(card Omega_N : ENNReal)^(-1) smul count; sigma(true)=1, sigma(false)=-1; S_N=1/sqrt(N) sum sigma','DEFINITION','Exact borrowed35 sealed signature','All N including zero: empty sum0, inverse sqrt0=0, card Omega_0=1, mu_0 mass1.')
node('PARENT35','BORROWED_SEALED_INTERFACE','exists laws:N->ProbabilityMeasure Real, all N laws_N=map S_N mu_N; laws_0=dirac0; laws_(n+1) -> gaussianReal0(varianceNNReal1) weakly','DERIVED_PARENT','Frozen573-byte35 public signature, not35 proof body','Interface only in this source packet. Actual independent compiled admission of35 is an implementation prerequisite, not certified here.')
node('GAUSSIAN','PINNED_API','gamma=gaussianReal (0:Real) (1:NNReal); canonical probability measure; variance=1 not standard deviation parameter','DEFINITION_TYPECLASS','Mathlib Gaussian.Real219-233')
node('PROB-STRUCTURE','PINNED_API','ProbabilityMeasure is subtype of Measure with IsProbabilityMeasure; real weak topology induced from finite measures','TYPECLASS_DEFINITION','Mathlib ProbabilityMeasure101-121,286-290')
node('PROB-FINITE','PINNED_API','Probability -> zero-or-probability -> IsFiniteMeasure; finite -> locally finite -> finite on compacts','TYPECLASS_DERIVED','Mathlib Probability52-54,63-76; Finite291-293,552-555')
node('MAP-PROB','PINNED_API','IsProbabilityMeasure(map S mu) -> IsProbabilityMeasure mu; measurable S maps probability to probability','DERIVED_API','Mathlib Probability124-133','Used internally with actual35 output; not an extra count-probability binder.')
node('FINITE-MEAS','PINNED_API','Every map from Fin N->Bool to Real is measurable under canonical finite measurable-singleton structure','TYPECLASS_DERIVED','Mathlib measurable_of_finite291-292','Finite/Fintype/nonempty/card positive and measurable-singleton structures are canonical, no caller certificates.')
node('C2-CONT','PINNED_API','C2 f -> Continuous f; C2 f -> Continuous(deriv f)','DERIVED_API','ContDiff.continuous inherited imported primitive; Mathlib ContDiff.continuous_deriv108-110')
node('SUPPORT-COMP','PINNED_API','HasCompactSupport f and g(0)=0 -> HasCompactSupport(g o f)','DERIVED_API','Mathlib Support271-284 via generated additive comp_left','Applied square and T; T(0)=0 is internally computed, not positivity.')
node('SUPPORT-DERIV','PINNED_API','tsupport(deriv f) subset tsupport f; HasCompactSupport f -> HasCompactSupport(deriv f)','DERIVED_API','Mathlib Deriv.Support38-62','Derivative support does not require a new differentiability or compact-derivative binder.')
node('T-CONT','PINNED_API','Continuous T on all Real, including0; Continuous h -> Continuous(T o h)','DERIVED_API','Real.continuous_mul_log45-59 and Continuous.mul_log62-63','No log singularity at zero for the product; Real.log convention retained.')
node('REG-A','AUTHORED_INTERNAL_ADAPTER','Continuous A and HasCompactSupport A','DERIVED','C2 continuity, square continuity, compact-support composition')
node('REG-B','AUTHORED_INTERNAL_ADAPTER','Continuous B and HasCompactSupport B','DERIVED','Continuous T o A, support composition using T(0)=0')
node('REG-C','AUTHORED_INTERNAL_ADAPTER','Continuous C and HasCompactSupport C','DERIVED','Continuous deriv f, compact derivative, square composition')
node('ROOT-BCF','PINNED_API','root ofCompactSupport g hgContinuous hgCompact : Real -> bounded-continuous Real; literal toFun=g','DERIVED_API','Mathlib BoundedCompactlySupported83-93','Namespace is root, not BoundedContinuousFunction.ofCompactSupport. Empty support branch is retained internally.')
for x in 'ABC':node('ROOT-'+x,'AUTHORED_INTERNAL_ADAPTER','Actual bounded continuous function with literal observer '+x,'DERIVED','root ofCompactSupport applied to REG-'+x,'OPEN authored assembly; no new observer/BCF certificate public premise.')
node('COMPACT-L1','PINNED_API','Continuous g and HasCompactSupport g and IsFiniteMeasureOnCompacts mu -> Integrable g mu','DERIVED_API','Mathlib LocallyIntegrable622-625; actual Real Borel/topological compatibility','Real normed additive target, canonical Borel/opens-measurable structure; finite-on-compacts obtained internally for gamma and actual laws.')
node('TRUE-L1','AUTHORED_INTERNAL_ADAPTER','For each X in A,B,C: Integrable X gamma AND forall N Integrable X laws_N','DERIVED','Actual continuous compact observers and actual probability measures','Genuine domains, not merely totalized integral equalities.')
node('MAP-L1','PINNED_API','Integrable g (map S mu) iff Integrable(g o S) mu with AEStronglyMeasurable g and AEMeasurable S','DERIVED_API','Mathlib integrable_map_measure356-360')
node('MAP-INTEGRAL','PINNED_API','integral g (map S mu) = integral(g o S)mu with actual measurability/strong measurability','DERIVED_API','Mathlib integral_map_of_stronglyMeasurable1032-1041 and integral_map1043-1053','API itself totalizes undefined integrals. This packet separately requires TRUE-L1 and COUNT-L1 consumers.')
node('COUNT-L1','AUTHORED_INTERNAL_ADAPTER','forall N, each A(S_N), B(S_N), C(S_N) is Bochner Integrable under actual mu_N','DERIVED','TRUE-L1 transported through actual35 map identity and MAP-L1')
node('ACTUAL-MAP-IDENTITIES','AUTHORED_INTERNAL_ADAPTER','forall N and X in A,B,C, integral X laws_N = integral X(S_N) mu_N; same identity for both homogeneous entropy terms','DERIVED','Parent35 literal map equality + MAP-INTEGRAL with genuine domains','Same law, same map, same observer; no law-selector binder or posterior reinterpretation.')
node('WEAK-BCF','PINNED_API','Weak Tendsto probability laws iff integral Tendsto for every actual real bounded continuous function','DERIVED_API','Mathlib ProbabilityMeasure.tendsto_iff_forall_integral_tendsto346-352','Pointwise weak convergence is not unbounded moment convergence.')
for x in 'ABC':
    node('LAW-LIMIT-'+x,'AUTHORED_INTERNAL_ADAPTER','integral '+x+' laws_(n+1) -> integral '+x+' gamma','DERIVED','Parent35 + literal observer BCF + WEAK-BCF')
    node('COUNT-LIMIT-'+x,'AUTHORED_INTERNAL_ADAPTER','integral '+x+'(S_(n+1)) mu_(n+1) -> integral '+x+' gamma','DERIVED','Actual law limit and actual integral-map identity')
node('ENTROPY-LIMIT','AUTHORED_INTERNAL_ADAPTER','Ent_mu_(n+1)((f o S_(n+1))^2) -> Ent_gamma(f^2)','DERIVED','COUNT-LIMIT-B minus T(COUNT-LIMIT-A); true L1 and entropy definition','Includes zero function and zero Gaussian mass. No division by mass or positivity assumption. Constant is exact coefficient1 in both entropy terms.')
node('ZERO-N0','AUTHORED_BOUNDARY','S_0=0; A integral=f(0)^2; B integral=T(f(0)^2); C integral=(deriv f(0))^2; entropy_mu0=0; f identically0 makes all integrals0','DERIVED','Parent35 dirac0, actual definitions','Derivative-square N0 need not be0. Successor limit deliberately uses n+1.')
node('EXT-IMPORTS','IMPORTED_PRIMITIVE_BOUNDARY','Standard real algebra/order, compact interval norm-bound, support/deriv local equality, ContDiff.iterate_deriv\', continuity composition/powers, Tendsto.comp/sub; primitive law CLT parents','TYPECLASS_DERIVED','Pinned SLT import/header context plus explicit API blocks','Atomic imported primitive boundary only, not claimed ASTIS port or exhaustive transitive theorem proof. Relevant direct imported use edges are retained.')
node('SLT-F-CONT','EXTERNAL_SOURCE','CompactlySupportedSmooth f -> Continuous f','DERIVED','EfronSteinApp51-53')
node('SLT-F-BOUND','EXTERNAL_SOURCE','Continuous compact f -> exists uniform norm bound; CompactlySupportedSmooth.bounded','DERIVED','EfronSteinApp58-66')
node('SLT-DERIV-CONT','EXTERNAL_SOURCE','CompactlySupportedSmooth -> continuous deriv via iterate_deriv\'1 1','DERIVED','TaylorBound161-164','External source route; root route instead uses pinned ContDiff.continuous_deriv.')
node('SLT-DERIV-SUPPORT','EXTERNAL_SOURCE','Compact support of deriv from local equality to zero off tsupport f','DERIVED','TaylorBound167-197')
node('SLT-DERIV-BOUND','EXTERNAL_SOURCE','exists C>=0 forall x abs(deriv f x)<=C','DERIVED','TaylorBound200-209')
node('NORM-BCF','PINNED_API','BCF.ofNormedAddCommGroup from continuous literal function and produced uniform norm bound; coe equality','DERIVED_API','Mathlib Bounded.Normed118-125')
for x in 'ABC':node('SLT-BCF-'+x,'EXTERNAL_SOURCE','Bespoke literal '+x+' bounded continuous observer and apply equality','DERIVED','SLT Limit square266-283, derivative316-333, log-square1174-1185','External-reference source mathematics, not an ASTIS callable producer.')
node('SLT-T-BOUND','EXTERNAL_SOURCE','T bounded on [0,C^2] by continuity on compact interval','DERIVED','Limit1129-1139')
node('SLT-B-BOUND','EXTERNAL_SOURCE','B bounded by bounding f and T on [0,C^2]','DERIVED','Limit1143-1165')
node('SLT-B-CONT','EXTERNAL_SOURCE','B continuous through Continuous.mul_log','DERIVED','Limit1168-1170')
node('SLT-REAL-LAW','EXTERNAL_SOURCE','rademacherLaw n=[NeZero n] real-product Rademacher pushforward; stdGaussian=ProbabilityMeasure gaussianReal0 1; weak successor CLT header','DEFINITION_DERIVED','Limit39-40,92-94,149-151,220-221','Different carrier from actual count law. CLT proof body excluded from36; imported upstream law primitive dependencies named, not revalidated here.')
node('SLT-WEAK-HELPER','EXTERNAL_SOURCE','Weak convergence -> real BCF integral convergence','DERIVED','Limit244-249 actual direct use of Mathlib weak-integral iff')
for x in 'ABC':node('SLT-LIMIT-'+x,'EXTERNAL_SOURCE','External real-product law successor '+x+' integral -> Gaussian integral','DERIVED','Limit347-353,1188-1194,356-362','This source statement is not automatically actual finite Bool-count output.')
node('SLT-ENTROPY-LIMIT','EXTERNAL_SOURCE','External real-product law entropy(f^2) -> Gaussian entropy(f^2)','DERIVED','Limit1213-1234')
node('GAP-REAL-COUNT','SOURCE_GAP','Genuine equality/transport from external real-product Rademacher law to literal Bool normalized count S_N law if reusing external law limits','AUTHORED_MISSING','No such adapter is supplied by these bounded source regions','Not needed by authored root route which consumes parent35 directly. Not a public law equality certificate.')
node('GAP-ASSEMBLY36','SOURCE_GAP','ASTIS actual three BCF constructions, genuine domains, actual map transport and homogeneous entropy assembly remain unproved','AUTHORED_MISSING','Implementation-independent prospective36 boundary','Available Mathlib endpoints do not constitute new compiled theorem36.')
node('GAP-FLIP4','SOURCE_GAP','Full normalized Boolean flip energy limit -> 4 integral(deriv f)^2 gamma','SOURCE_GAP','SLT OneDimGLSICompSmo58-62 and Limit separate full flip-energy theorem outside this delta','Derivative-square observer convergence alone does not prove flip energy. Factor4 separate.')
node('COMPACT-LSI-CONSUMER','FUTURE_EXTERNAL_SOURCE_CONSUMER','Ent_gamma(f^2)<=2 integral(deriv f)^2 gamma for C2 compact f','SOURCE_CONTEXT','SLT OneDimGLSICompSmo50-82','OPEN here: also needs genuine Bernoulli LSI and full flip-energy4, not just current entropy convergence.')
node('GAP-BERNOULLI-TRANSPORT','SOURCE_GAP','Genuine Bernoulli function LSI on identical actual Boolean carrier and transport of external real-product source formulation if used','DERIVED_PARENT_MISSING','SLT OneDimGLSICompSmo77-80','Existing34 is a potential admitted parent; no34 body/graph read or newly certified here.')
node('GAP-NONCOMPACT','SOURCE_GAP','Positive noncompact actual32 sqrt density needs genuine cutoff/W12 entropy and energy approximation','SOURCE_GAP','SPHMC actual r density and prior dependency-readiness scope','Compact observer node cannot replace literal sqrtRN; arbitrary canonical RN has no pointwise gradient certificate.')
node('GAP-HILBERT','SOURCE_GAP','Finite-dimensional Gaussian product/tensorization plus metric and Fisher/Dirichlet adapters','SOURCE_GAP','Full SPHMC first inequality background','No dimension extension or covariance scaling theorem credited.')
node('GAP-T2','SOURCE_GAP','Actual Gaussian T2/KL weak-RN/finite-W2 and same-r LSI connection','SOURCE_GAP','SPHMC S4.SS1.p4.3','No optimal-coupling value definition implies T2. Full first4.6, bias, main, work and composition OPEN.')

# Root alternative: every producer ingredient is explicitly a dependency edge.
for a,b,w in [
 ('P-RHO','P-FIRST','same true standardized RGO context'),('GAUSSIAN','PARENT35','exact Gaussian target variance1'),('PROB-STRUCTURE','PARENT35','probability subtype and weak topology'),('COUNT-SUM','PARENT35','exact all-N actual map interface'),
 ('PROB-STRUCTURE','PROB-FINITE','probability coercion structure'),('PARENT35','MAP-PROB','actual laws map equality and probability'),('FINITE-MEAS','MAP-PROB','actual map measurability, including N0'),('PARENT35','TRUE-L1','same actual laws for every N'),('GAUSSIAN','TRUE-L1','actual gamma probability'),('PROB-FINITE','TRUE-L1','actual laws and gamma finite on compacts'),('COMPACT-L1','TRUE-L1','continuous compact true Bochner domains'),
 ('F-CLASS','C2-CONT','C2 field'),('F-CLASS','SUPPORT-DERIV','compact support field'),('F-CLASS','REG-A','continuous f and compact f'),('C2-CONT','REG-A','power continuity'),('SUPPORT-COMP','REG-A','square vanishes0'),('OBSERVERS','REG-A','literal square'),('REG-A','REG-B','A continuous and compact'),('T-CONT','REG-B','T continuous at0/allReal'),('SUPPORT-COMP','REG-B','T(0)=0'),('OBSERVERS','REG-B','literal T o A'),('C2-CONT','REG-C','continuous derivative'),('SUPPORT-DERIV','REG-C','compact derivative'),('SUPPORT-COMP','REG-C','square composition'),('OBSERVERS','REG-C','literal derivative square'),
 ('PARENT35','COUNT-L1','actual map equality'),('FINITE-MEAS','COUNT-L1','S_N measurable'),('TRUE-L1','COUNT-L1','actual map-domain L1'),('MAP-L1','COUNT-L1','internal composition domain transport'),('TRUE-L1','ACTUAL-MAP-IDENTITIES','real target integrability'),('COUNT-L1','ACTUAL-MAP-IDENTITIES','real count domains'),('FINITE-MEAS','ACTUAL-MAP-IDENTITIES','S_N measurable'),('PARENT35','ACTUAL-MAP-IDENTITIES','exact actual map identity'),('MAP-INTEGRAL','ACTUAL-MAP-IDENTITIES','same genuine integrals'),('ENTROPY','ACTUAL-MAP-IDENTITIES','both same homogeneous terms'),
 ('COUNT-LIMIT-A','ENTROPY-LIMIT','mass limit'),('COUNT-LIMIT-B','ENTROPY-LIMIT','log-square integral limit'),('T-CONT','ENTROPY-LIMIT','continuous T mass composition, includes0'),('ENTROPY','ENTROPY-LIMIT','subtract exact entropy terms'),('COUNT-L1','ENTROPY-LIMIT','finite actual entropy inputs'),('TRUE-L1','ENTROPY-LIMIT','finite Gaussian entropy inputs'),('ACTUAL-MAP-IDENTITIES','ENTROPY-LIMIT','same-law count entropy identity'),('PARENT35','ZERO-N0','true dirac0 law'),('COUNT-SUM','ZERO-N0','actual empty sum/count'),('OBSERVERS','ZERO-N0','literal values'),('ENTROPY','ZERO-N0','T(a)-T(a)=0'),('T-CONT','ZERO-N0','zero product convention'),
 ('ENTROPY-LIMIT','GAP-ASSEMBLY36','proposed target not implemented'),('ENTROPY-LIMIT','COMPACT-LSI-CONSUMER','necessary entropy passage only'),('GAP-FLIP4','COMPACT-LSI-CONSUMER','full energy4 passage'),('GAP-BERNOULLI-TRANSPORT','COMPACT-LSI-CONSUMER','finite LSI half constant'),('F-CLASS','COMPACT-LSI-CONSUMER','exact compactC2 source class'),('COMPACT-LSI-CONSUMER','GAP-NONCOMPACT','compact core insufficient for actual32 f'),('GAP-NONCOMPACT','GAP-HILBERT','genuine noncompact scalar route before product domain extension'),('GAP-HILBERT','GAP-T2','full LSI consumer adapters'),('GAP-T2','P-FIRST','omitted Gaussian LSI+T2 source background')]:edge(a,b,w,'AUTHORED_DERIVATION' if a.startswith(('REG-','ROOT-','COUNT-','LAW-')) or b.startswith(('REG-','ROOT-','COUNT-','LAW-','ENTROPY-LIMIT','TRUE-')) else 'DEPENDENCY_BOUNDARY')
for x in 'ABC':
    for a,b,w in [('REG-'+x,'ROOT-'+x,'actual regularity'),('ROOT-BCF','ROOT-'+x,'literal root constructor'),('REG-'+x,'TRUE-L1','continuous compact observer'),('PARENT35','LAW-LIMIT-'+x,'actual successor weak limit'),('ROOT-'+x,'LAW-LIMIT-'+x,'literal observer BCF'),('WEAK-BCF','LAW-LIMIT-'+x,'actual weak-integral characterization'),('TRUE-L1','LAW-LIMIT-'+x,'true finite domains'),('LAW-LIMIT-'+x,'COUNT-LIMIT-'+x,'actual law limit'),('ACTUAL-MAP-IDENTITIES','COUNT-LIMIT-'+x,'actual count equality'),('COUNT-L1','COUNT-LIMIT-'+x,'actual count L1')]:edge(a,b,w,'AUTHORED_DERIVATION')
# External SLT direct uses, with imported primitive and distinct law boundaries.
for a,b,w in [
 ('F-CLASS','SLT-F-CONT','hf.1.continuous'),('F-CLASS','SLT-F-BOUND','hf.2 compact'),('SLT-F-CONT','SLT-F-BOUND','actual hf.continuous'),('EXT-IMPORTS','SLT-F-BOUND','compact continuous bound primitive'),('F-CLASS','SLT-DERIV-CONT','hf.1 C2'),('EXT-IMPORTS','SLT-DERIV-CONT','actual iterate_deriv prime and ContDiff.continuous'),('F-CLASS','SLT-DERIV-SUPPORT','hf.2 compact tsupport'),('EXT-IMPORTS','SLT-DERIV-SUPPORT','support compact/local zero/eventual equality deriv primitive'),('SLT-DERIV-CONT','SLT-DERIV-BOUND','continuous deriv'),('SLT-DERIV-SUPPORT','SLT-DERIV-BOUND','compact deriv'),('EXT-IMPORTS','SLT-DERIV-BOUND','compact bound/max0/real norm primitives'),
 ('SLT-F-BOUND','SLT-BCF-A','chosen f bound'),('SLT-F-CONT','SLT-BCF-A','continuous f square'),('NORM-BCF','SLT-BCF-A','literal BCF constructor and coe_apply'),('EXT-IMPORTS','SLT-BCF-A','square norm arithmetic'),('F-CLASS','SLT-BCF-A','source public hf'),('SLT-DERIV-BOUND','SLT-BCF-C','chosen nonnegative derivative bound'),('SLT-DERIV-CONT','SLT-BCF-C','continuous deriv square'),('NORM-BCF','SLT-BCF-C','constructor and coe_apply'),('EXT-IMPORTS','SLT-BCF-C','square norm arithmetic'),('F-CLASS','SLT-BCF-C','source public hf'),
 ('T-CONT','SLT-T-BOUND','actual Real.continuous_mul_log'),('EXT-IMPORTS','SLT-T-BOUND','isCompact_Icc and exists_bound_of_continuousOn'),('SLT-T-BOUND','SLT-B-BOUND','bound T on range[0,C2]'),('SLT-F-BOUND','SLT-B-BOUND','hf.bounded'),('F-CLASS','SLT-B-BOUND','same hf'),('EXT-IMPORTS','SLT-B-BOUND','abs/square interval arithmetic'),('SLT-F-CONT','SLT-B-CONT','hf.continuous.pow2'),('T-CONT','SLT-B-CONT','actual Continuous.mul_log'),('F-CLASS','SLT-B-CONT','same source hf'),('SLT-B-BOUND','SLT-BCF-B','chosen uniform B bound'),('SLT-B-CONT','SLT-BCF-B','actual continuous B'),('NORM-BCF','SLT-BCF-B','constructor and coe equality'),('F-CLASS','SLT-BCF-B','same source hf'),
 ('GAUSSIAN','SLT-REAL-LAW','same Gaussian0 NNReal1'),('PROB-STRUCTURE','SLT-REAL-LAW','actual probability subtype'),('MAP-PROB','SLT-REAL-LAW','Measure.isProbabilityMeasure_map in source92-94'),('EXT-IMPORTS','SLT-REAL-LAW','real-product law+measurable normalizedSum and upstream CLT imported-header primitive'),('WEAK-BCF','SLT-WEAK-HELPER','direct Mathlib tendsto_iff_forall_integral_tendsto248'),('PROB-STRUCTURE','SLT-WEAK-HELPER','source weak probability semantics'),('ENTROPY','SLT-ENTROPY-LIMIT','source unfold entropy1218'),('SLT-LIMIT-A','SLT-ENTROPY-LIMIT','source h2'),('SLT-LIMIT-B','SLT-ENTROPY-LIMIT','source h1'),('T-CONT','SLT-ENTROPY-LIMIT','source exact continuousAt.tendsto.comp h2'),('EXT-IMPORTS','SLT-ENTROPY-LIMIT','Tendsto composition/subtraction'),('F-CLASS','SLT-ENTROPY-LIMIT','same source hf'),('SLT-ENTROPY-LIMIT','COMPACT-LSI-CONSUMER','exact source entropy dependency54-56'),('SLT-ENTROPY-LIMIT','GAP-REAL-COUNT','external law entropy requires actual carrier connection'),('PARENT35','GAP-REAL-COUNT','actual count-law interface to connect'),('COUNT-SUM','GAP-REAL-COUNT','same literal signs/card map')]:edge(a,b,w,'EXTERNAL_SOURCE_USE')
for x in 'ABC':
    for a,w in [('SLT-REAL-LAW','source successor weak law'),('SLT-WEAK-HELPER','source weak-integral theorem'),('SLT-BCF-'+x,'source literal BCF and apply lemma'),('F-CLASS','same source hf'),('GAUSSIAN','same source Gaussian measure')]:edge(a,'SLT-LIMIT-'+x,w,'EXTERNAL_SOURCE_USE')
    edge('SLT-LIMIT-'+x,'GAP-REAL-COUNT','external observer limit is not actual count transport','DEPENDENCY_BOUNDARY')
for a,b,w in [('SLT-REAL-LAW','COMPACT-LSI-CONSUMER','source actual Gaussian/real-product law expressions'),('ENTROPY','COMPACT-LSI-CONSUMER','source literal homogeneous entropy'),('EXT-IMPORTS','COMPACT-LSI-CONSUMER','source Tendsto.const_mul and le_of_tendsto_of_tendsto; half times four algebra'),('SLT-REAL-LAW','GAP-FLIP4','source real-product normalized sum/shifted sum and Gaussian law'),('F-CLASS','GAP-FLIP4','source exact compactC2 prerequisite'),('SLT-REAL-LAW','GAP-BERNOULLI-TRANSPORT','source real-product law entropy/flip expressions'),('ENTROPY','GAP-BERNOULLI-TRANSPORT','source homogeneous entropy'),('F-CLASS','GAP-BERNOULLI-TRANSPORT','source Bernoulli application hf')]:edge(a,b,w,'EXTERNAL_SOURCE_USE')

# Exact reviewed regions. All lines in declared windows receive a NODE or a justified EXCLUDED.
L=EXT+'SLT__GaussianPoincare__Limit.lean.raw.snapshot'
for a,b,id in [(39,40,'SLT-REAL-LAW'),(92,94,'SLT-REAL-LAW'),(149,151,'SLT-REAL-LAW'),(220,221,'SLT-REAL-LAW'),(244,249,'SLT-WEAK-HELPER'),(266,283,'SLT-BCF-A'),(316,333,'SLT-BCF-C'),(347,353,'SLT-LIMIT-A'),(356,362,'SLT-LIMIT-C'),(1129,1139,'SLT-T-BOUND'),(1143,1165,'SLT-B-BOUND'),(1168,1170,'SLT-B-CONT'),(1174,1185,'SLT-BCF-B'),(1188,1194,'SLT-LIMIT-B'),(1196,1234,'SLT-ENTROPY-LIMIT')]:src(id,L,a,b)
for a,b in [(1,40),(88,94),(146,151),(220,249),(254,362),(1125,1244)]:footprint(L,a,b)
Q=EXT+'SLT__GaussianPoincare__EfronSteinApp.lean.raw.snapshot'
for a,b,id in [(47,48,'F-CLASS'),(51,53,'SLT-F-CONT'),(58,66,'SLT-F-BOUND')]:src(id,Q,a,b)
footprint(Q,36,67)
Q=EXT+'SLT__GaussianPoincare__TaylorBound.lean.raw.snapshot'
for a,b,id in [(161,164,'SLT-DERIV-CONT'),(167,197,'SLT-DERIV-SUPPORT'),(200,209,'SLT-DERIV-BOUND')]:src(id,Q,a,b)
footprint(Q,1,37);footprint(Q,158,209)
Q=EXT+'SLT__GaussianLSI__Entropy.lean.raw.snapshot'
src('ENTROPY',Q,48,49);src('ENTROPY',Q,124,125);footprint(Q,30,52);footprint(Q,122,125)
Q=EXT+'SLT__GaussianLSI__OneDimGLSICompSmo.lean.raw.snapshot'
src('COMPACT-LSI-CONSUMER',Q,50,56);src('GAP-FLIP4',Q,58,62);src('COMPACT-LSI-CONSUMER',Q,64,75);src('GAP-BERNOULLI-TRANSPORT',Q,77,80);src('COMPACT-LSI-CONSUMER',Q,82,82);footprint(Q,1,101)
Q=ML+'MeasureTheory/Measure/ProbabilityMeasure.lean'
src('PROB-STRUCTURE',Q,101,121);src('PROB-STRUCTURE',Q,286,290);src('WEAK-BCF',Q,343,352)
Q=ML+'Topology/ContinuousMap/BoundedCompactlySupported.lean';src('ROOT-BCF',Q,83,93);footprint(Q,1,107)
Q=ML+'Topology/Algebra/Support.lean';src('SUPPORT-COMP',Q,271,284);footprint(Q,205,228);footprint(Q,265,289)
Q=ML+'Analysis/Calculus/Deriv/Support.lean';src('SUPPORT-DERIV',Q,38,62);footprint(Q,25,62)
Q=ML+'Analysis/Calculus/ContDiff/Deriv.lean';src('C2-CONT',Q,108,110);footprint(Q,87,114)
Q=ML+'Analysis/SpecialFunctions/Log/NegMulLog.lean';src('T-CONT',Q,45,63);footprint(Q,28,65)
Q=ML+'MeasureTheory/Function/LocallyIntegrable.lean';src('COMPACT-L1',Q,622,625);footprint(Q,33,40);footprint(Q,551,595);footprint(Q,611,639)
Q=ML+'MeasureTheory/Function/L1Space/Integrable.lean';src('MAP-L1',Q,356,368);footprint(Q,162,169);footprint(Q,340,380)
Q=ML+'MeasureTheory/Integral/Bochner/Basic.lean';src('MAP-INTEGRAL',Q,1032,1053);footprint(Q,1029,1055)
Q=ML+'MeasureTheory/MeasurableSpace/Basic.lean';src('FINITE-MEAS',Q,287,292);footprint(Q,283,298)
Q=ML+'MeasureTheory/Measure/Typeclasses/Finite.lean';src('PROB-FINITE',Q,291,293);src('PROB-FINITE',Q,552,555);footprint(Q,281,302);footprint(Q,332,343);footprint(Q,545,556)
Q=ML+'Probability/Distributions/Gaussian/Real.lean';src('GAUSSIAN',Q,219,233);footprint(Q,215,239)
Q=ML+'MeasureTheory/Measure/Typeclasses/Probability.lean';src('PROB-FINITE',Q,52,54);src('PROB-FINITE',Q,63,76);src('MAP-PROB',Q,124,133);footprint(Q,35,84);footprint(Q,115,136)
Q=ML+'Topology/ContinuousMap/Bounded/Normed.lean';src('NORM-BCF',Q,118,125);footprint(Q,115,125)
Q='runs/20261007-companion-priority/balanced-rademacher-clt/preproof/signature.prospective.txt';src('PARENT35',Q,1,10)

# Range exclusions describe the actual reason, including concrete distinct omitted mathematics.
def exclusion(p,a,b):
    if p==L:
        if a>=222 and b<=242:return 'Upstream characteristic-function CLT proof is outside observer-delta36; only its exact weak-law header is borrowed as external primitive; no old sourcegraph validation.'
        if a>=254 and b<=265:return 'Unsquared f BCF wrapper is not one of the three required observers.'
        if a>=284 and b<=315:return 'First derivative and absolute-derivative BCF wrappers are unused by derivative-square observer.'
        if a>=334 and b<=346:return 'Unsquared-f limit and contextual comments are outside A/B/C observer target.'
        if a>=1235:return 'Entropy notation alias and namespace closure add no producer.'
    if 'OneDimGLSICompSmo' in p and a>=84:return 'Later fderiv norm/gradient reformulation and namespace closure excluded; no compact-LSI credit in current36.'
    return 'Import/namespace/comment/typeclass context or neighboring unused lemma outside the explicitly assigned producer block; imported primitive boundaries remain explicit and are not expanded into project closure.'
inventory=[]
for p,ws in windows.items():
    raw=(ROOT/p).read_bytes();lines=raw.splitlines(keepends=True); selected=set()
    for a,b in ws:
        assert 1<=a<=b<=len(lines),(p,a,b,len(lines));selected.update(range(a,b+1))
    labels={}
    for pp,a,b,id in blocks:
        if pp==p:
            for k in range(a,b+1):assert k not in labels,(p,k);labels[k]=id
    ss=sorted(selected);groups=[]
    for k in ss:
        lab=labels.get(k)
        if groups and groups[-1][1]+1==k and groups[-1][2]==lab:groups[-1]=(groups[-1][0],k,lab)
        else:groups.append((k,k,lab))
    for a,b,id in groups:
        rb=b''.join(lines[a-1:b]);rid='R%03d'%(len(inventory)+1)
        rp=BASE/(rid+'.raw.snapshot');lp=BASE/(rid+'.lf.snapshot')
        with rp.open('xb') as f:f.write(rb)
        with lp.open('xb') as f:f.write(lf(rb))
        inventory.append({'id':rid,'input_index':by_path[p],'path':p,'lines':[a,b],
          'raw_start':sum(map(len,lines[:a-1])),'raw_end':sum(map(len,lines[:b])),
          'raw_sha256':sha(rb),'lf_sha256':sha(lf(rb)),'raw_snapshot':str(rp.relative_to(ROOT)).replace('\\','/'),'lf_snapshot':str(lp.relative_to(ROOT)).replace('\\','/'),
          'disposition':'NODE' if id else 'EXCLUDED','node_ids':[id] if id else [],'reason':None if id else exclusion(p,a,b)})
    assert sum(b-a+1 for a,b,_ in groups)==len(selected)
    # Outside declared windows is explicitly outside bounded source-review claim.
    missing=sorted(set(range(1,len(lines)+1))-selected)
    ranges=[]
    for k in missing:
        if ranges and ranges[-1][1]+1==k:ranges[-1][1]=k
        else:ranges.append([k,k])
    # Pin scope exclusions separately, without pretending they were inspected region by region.
    windows[p]={'selected_lines':len(selected),'selected_intervals':ws,'outside_declared_footprint':ranges,
                'outside_reason':'Outside bounded actual observer/entropy dependency slice; no exhaustive whole-file/project semantic-review assertion.'}

whole=(ROOT/packet['primary_first']['source']['path']).read_bytes()
primary_inventory=[]
for i,x in enumerate(packet['primary_first']['outer_fragments']):
    p=x['snapshot']['path'];rb=(ROOT/p).read_bytes();a=x['UTF8_start'];b=x['UTF8_end'];assert whole[a:b]==rb
    primary_inventory.append({'id':x['id'],'input_index':by_path[p],'whole_byte_interval':[a,b],'raw_sha256':sha(rb),'lf_sha256':sha(lf(rb)),
      'disposition':'NODE','node_ids':['P-FIRST'] if x['id'] in ['S4.E6','S4.SS1.p4.3'] else ['P-RHO'],
      'mixed_scope_exclusions':'FIRST inequality only: second eta sqrt(E||U||^2), last eta sqrt d, bias/main/numerical/work statements excluded.' if x['id'] in ['S4.E6','S4.SS1.p4.3'] else 'Retained as ultimate source consumer context, not36 public analytic binders.'})

nodeids={x['id'] for x in N}
assert len(nodeids)==len(N)
for x in E:assert x['from'] in nodeids and x['to'] in nodeids
assert len({(x['from'],x['to']) for x in E})==len(E)
for x in N:
    x['source_regions']=[r['id'] for r in inventory if x['id'] in r['node_ids']]+[r['id'] for r in primary_inventory if x['id'] in r['node_ids']]
    if x['kind']=='AUTHORED_INTERNAL_ADAPTER':assert any(e['to']==x['id'] for e in E),x['id']
scan=[]
for r in inventory:
    if r['disposition']=='NODE' and r['path'].endswith(('.lean','.raw.snapshot')):
        t=(BASE/Path(r['raw_snapshot']).name).read_text(encoding='utf-8')
        hits=re.findall(r'\b(?:sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial\b',t)
        if hits:scan.append({'region':r['id'],'hits':hits})

route=[
 'Obtain actual all-N laws and successor weak Gaussian0,variance1 limit internally from borrowed35 interface; retain N0 dirac0 and exact finite count/card/S_N.',
 'From exact C2 plus compact support derive continuous compact A=f², B=f²log f², C=(deriv f)²; T continuous at0 and derivative support internal.',
 'Produce literal three BCFs using root ofCompactSupport; external SLT bespoke constructors are a distinct authored-port OR with their true source parents retained.',
 'Derive actual gamma and all-law Bochner L1 through compact continuity plus finite-on-compacts; transport to actual count domains by measurable S_N and integrable_map_measure.',
 'Apply pinned weak probability BCF-integral characterization to all three literal observers; rewrite actual map integrals to actual count successor integral limits.',
 'Combine B-limit minus continuous T of A-limit for exact homogeneous entropy limit with genuine L1, including zero function/zero mass without normalization.',
 'Stop at observer/entropy convergence; full flip-energy4 plus Bernoulli LSI are still needed for compact Gaussian LSI, then cutoff/W12/product/metric/T2 for actual SPHMC FIRST4.6.'
]
contract={'schema_version':1,'kind':'PRIMARY_SOURCE_API_CONTRACT','status':'FROZEN_AUTHORED_UNREVIEWED','actor':'gaussian_domain_preproof_reviewer_29',
 'primary_source':packet['primary_first']['source'],'primary_scope':primary_inventory,'scope':'Actual scalar compact-C2 three observer Bochner domains and successor integral/entropy limits, authored omitted-Gaussian-LSI background. Not a printed SPHMC theorem.',
 'source_assumptions_vs_public_contract':{'SPHMC_context':'Same true standardized r, eta>0 and source potential remain later source-consumer assumptions; none is added to scalar compact core.',
 'external_background_public_inputs':['f:Real->Real','ContDiff Real 2 f','HasCompactSupport f'],
 'no_extra_public_inputs':['laws','weak convergence','probability','measurability','integrability','BCF/bound','positive mass','normalized L2 norm','entropy or desired inequality certificates'],
 'canonical_classes':'Real field/norm/topology/Borel/opens-measurable; Fin N->Bool Fintype/Finite/nonempty/measurable singletons; ProbabilityMeasure subtype; inherited probability/finite/local-finite/finite-on-compacts; no supplied class binder beyond fixed canonical structures.'},
 'exact_definitions':{'count_sum':next(n['formula_or_contract'] for n in N if n['id']=='COUNT-SUM'),'observers':next(n['formula_or_contract'] for n in N if n['id']=='OBSERVERS'),'entropy':next(n['formula_or_contract'] for n in N if n['id']=='ENTROPY'),'Gaussian':'gaussianReal (0:Real) (1:NNReal), mean0 variance1'},
 'boundaries':{'N0':'A integral=f0², B integral=T(f0²), C integral=deriv f0² need not vanish; entropy0; limit uses successor.',
 'zero_mass':'T continuous0; no mass division or positivity.', 'signed_f':'Allowed; source observers use f², Real log conventions exactly retained.',
 'noncompact_counterexample':'Weak mu_n=(1-1/n)dirac0+(1/n)dirac n tends to dirac0 while second moment=n; individual L1 does not authorize unbounded weak-integral passage.'},
 'history_and_independence':json.loads((BASE/'author.lease.json').read_text())['history'],
 'exposure':{'candidate36':False,'implementation36':False,'current35_body':False,'sourcegraph35_validation':False},
 'route_at_most_seven_steps':route,'compiler_started':False}
cr=write('source.contract.json',contract)
iv=write('source.inventory.json',{'schema_version':1,'status':'AUTHORED_UNREVIEWED','coverage_contract':'Every physical source line in the explicit selected intervals has exactly one NODE or reasoned EXCLUDED disposition. Whole raw sources are pinned; unselected intervals are explicitly outside semantic coverage. Not a whole upstream project inventory.',
 'input_binding_count':len(inputs),'regions':inventory,'primary_balanced_regions':primary_inventory,'footprints':windows,
 'counts':{'regions':len(inventory),'selected_lines':sum(x['lines'][1]-x['lines'][0]+1 for x in inventory),'primary_balanced_regions':len(primary_inventory),'node_regions':sum(x['disposition']=='NODE' for x in inventory),'excluded_regions':sum(x['disposition']=='EXCLUDED' for x in inventory)},
 'direct_placeholder_scan':{'scope':'Exact selected NODE raw regions only; comments may match lexical tokens; no transitive whole-project completion claim.','hits':scan}})
graph={'schema_version':1,'artifact_kind':'INDEPENDENT_SOURCE_PROOF_GRAPH','status':'AUTHORED_UNREVIEWED','author':'gaussian_domain_preproof_reviewer_29',
 'not_topology_validation':True,'target_boundary':contract['scope'],'source_contract':cr,'source_inventory':iv,'nodes':N,'edges':E,'compiled_edges':[],
 'truth_contract':'SOURCE_USE means an ingredient directly used by the pinned source block, not a compiled ASTIS dependency. AUTHORED_DERIVATION/DEPENDENCY_BOUNDARY identify proposed internal adapters and honest residuals. External source/borrowed35 API atoms have explicit admission boundaries. No public ingredient certificate is authorized.',
 'or_routes':[{'id':'OR-BCF-CONSTRUCTION','target_nodes':['LAW-LIMIT-A','LAW-LIMIT-B','LAW-LIMIT-C'],
 'alternatives':[{'id':'AUTHORED-ROOT-BCF','provenance':'Authored Mathlib root ofCompactSupport adapter, not printed SPHMC proof or SLT chosen implementation.','required_nodes':['REG-A','REG-B','REG-C','ROOT-BCF','ROOT-A','ROOT-B','ROOT-C','PARENT35','WEAK-BCF']},
 {'id':'EXTERNAL-SLT-BESPOKE-BCF-PORT','provenance':'Pinned SLT bespoke literal observers; actual35 laws can consume ported BCFs without external real-product law reuse. External observers remain references until genuine ASTIS port.','required_nodes':['SLT-F-BOUND','SLT-DERIV-BOUND','SLT-T-BOUND','SLT-B-BOUND','SLT-B-CONT','NORM-BCF','SLT-BCF-A','SLT-BCF-B','SLT-BCF-C','PARENT35','WEAK-BCF']}]},
 {'id':'OR-LIMIT-LAW-LINEAGE','target_nodes':['ENTROPY-LIMIT'],
 'alternatives':[{'id':'DIRECT-ACTUAL35','provenance':'Authored actual count law route via35, Mathlib weak tests and actual-map domain transfer.','required_nodes':['PARENT35','WEAK-BCF','ACTUAL-MAP-IDENTITIES','COUNT-L1','T-CONT','ENTROPY']},
 {'id':'EXTERNAL-SLT-LAW-TRANSPORT','provenance':'External source real-product limit route plus missing authored real-product-to-count adapter; not an already supplied source identity.','required_nodes':['SLT-LIMIT-A','SLT-LIMIT-B','SLT-LIMIT-C','SLT-ENTROPY-LIMIT','GAP-REAL-COUNT','ACTUAL-MAP-IDENTITIES','COUNT-L1']}]}],
 'residuals':[n['id'] for n in N if n['kind']=='SOURCE_GAP'],'counts':{'nodes':len(N),'edges':len(E),'or_routes':2,'compiled_edges':0},
 'seven_step_route':route,'source_exclusions':'No full flip-energy proof, noncompact literal32 density, finite-Hilbert LSI, T2/W2, source first4.6, bias, paper main/cost/composition completion.'}
gr=write('source-proof-graph.independent.json',graph)
digest=write('bounded-synthesis.json',{'status':'AUTHORED_UNREVIEWED_SOURCE_ONLY','finding':'Actual35 + three literal compact BCFs + genuine domain and actual map adapters suffice for compact scalar observer/entropy convergence. Zero mass requires only continuity T(0), no extra binder.',
 'first_required_unmet_dependency':{'class':'AUTHORED_INTERNAL_ADAPTER_NOT_COMPILED','node':'GAP-ASSEMBLY36','residual':'Genuine three-observer compact regularity/BCF/L1/count-map/entropy assembly still needs a sealed independently admitted statement and actual proof; available APIs are not that producer.'},
 'next_independent_action':'Distinct phase source-topology review of this authored graph before candidate/proof exposure. Author does not validate.',
 'route':route,'exact_constants':{'Gaussian_variance':1,'normalization':'sqrt(N)^(-1), normalized count/card','entropy_terms':[1,-1],'future_flip_factor_not_proved':4,'future_compact_Gaussian_LSI_constant_not_proved':2},
 'source_graph':gr,'source_inventory':iv,'source_contract':cr,'source_pins':{'SLT_commit':'d0f506f0a695018265dccb33bcb05e2f5ca1c876','SLT_toolchain':'leanprover/lean4:v4.32.0','SLT_mathlib':'81a5d257c8e410db227a6665ed08f64fea08e997','license':'Apache2 raw pin retained; external sources not local callable truth','ASTIS_toolchain':'leanprover/lean4:v4.33.0','ASTIS_mathlib':'db584cd6d46c92f209a44c0f1c829460d327499d'},
 'truth_boundary':graph['source_exclusions'],'conceptual_mirror_validation':False,'compiler_started':False})
bindings=write('input-bindings.json',{'normalization':'raw.replace(CRLF,LF).replace(CR,LF); hashes exact snapshot bytes, no JSON reserialization for input pins','inputs':inputs,'old28_pins_unchanged':True,'primary_balanced_original_byte_intervals_verified':True})
for x in inputs:
    assert sha((ROOT/x['path']).read_bytes())==x['raw_sha256'],x['path']
outs=[cr,iv,gr,digest,bindings]
run_id=sha(json.dumps({'inputs':[{k:x[k] for k in ['path','raw_sha256','lf_sha256']} for x in inputs],'outputs':outs},sort_keys=True,separators=(',',':')).encode())
run=write('run.closed.json',{'deterministic_run_sha256':run_id,'actor':'gaussian_domain_preproof_reviewer_29','outputs':outs,'inputs_unchanged_at_close':True,'counts':graph['counts'],'inventory_counts':json.loads((BASE/'source.inventory.json').read_text())['counts'],'no_compiler_no_claim_no_production_shared_edits':True,'not_self_validation':True})
lease=json.loads((BASE/'author.lease.json').read_text())
lease.update(status='CLOSED',read_lease='CLOSED',write_lease='CLOSED',compiler_lease='CLOSED',compiler_started=False,closed_utc=datetime.datetime.utcnow().isoformat()+'Z',run=run,deterministic_run_sha256=run_id)
(BASE/'author.lease.json').write_bytes((json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'graph':gr,'inventory':iv,'contract':cr,'run':run,'run_id':run_id,'counts':graph['counts'],'inventory_counts':json.loads((BASE/'source.inventory.json').read_text())['counts'],'inputs':len(inputs),'all_leases':'CLOSED','placeholder_hits':scan},indent=2))
