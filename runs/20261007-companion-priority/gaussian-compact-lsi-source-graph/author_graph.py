from pathlib import Path
import json, hashlib, datetime

ROOT=Path('E:/Samplinglib')
OUT=ROOT/'runs/20261007-companion-priority/gaussian-compact-lsi-source-graph'
PRE=ROOT/'runs/20261007-companion-priority/gaussian-compact-lsi-preread'
def sha(b): return hashlib.sha256(b).hexdigest()
def lf(b): return b.replace(b'\r\n',b'\n').replace(b'\r',b'\n')
def write(name,obj):
    b=(json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    if (OUT/name).exists():
        assert (OUT/name).read_bytes()==b, 'Immutable output differs: '+name
    else:
        with (OUT/name).open('xb') as f:f.write(b)
    return {'path':str((OUT/name).relative_to(ROOT)).replace('\\','/'),'raw_sha256':sha(b),'lf_sha256':sha(lf(b)),'bytes':len(b)}

prior=json.loads((PRE/'inputs.json').read_text(encoding='utf-8'))['inputs']
roles=['primary_whole','primary_first','primary_explanation','parent34_signature','parent34_verified_provenance','parent36_signature','parent36_verified_provenance','prospective37_signature_only','local_order_limit','local_multiplication_limit','local_square_sign','local_zero_mass_continuity','local_gaussian_definition','local_toolchain','local_mathlib_pin','external_compact_lsi','external_entropy_definition','external_C2_definition','external_gaussian_definition','external_license','external_toolchain','external_mathlib_pin','external_closure_historical']
data={}; bindings=[]
def add(role,path,raw,observed_path=None):
    i=len(bindings); names={'raw':'input.%03d.raw.snapshot'%i,'lf':'input.%03d.lf.snapshot'%i}
    for key,b in [('raw',raw),('lf',lf(raw))]:
        if (OUT/names[key]).exists():assert (OUT/names[key]).read_bytes()==b
        else:
            with (OUT/names[key]).open('xb') as f:f.write(b)
    data[role]=lf(raw)
    bindings.append({'role':role,'path':path,'observed_path':observed_path or path,'raw_sha256':sha(raw),'lf_sha256':sha(lf(raw)),'bytes':len(raw),'raw_snapshot':names['raw'],'lf_snapshot':names['lf']})
for role in roles:
    x=next(x for x in prior if x['role']==role)
    observed=PRE/x['raw_snapshot']; b=observed.read_bytes()
    assert sha(b)==x['raw_sha256'] and sha(lf(b))==x['lf_sha256']
    add(role,x['path'],b,str(observed.relative_to(ROOT)).replace('\\','/'))
extra=[('preread_packet',str((PRE/'source-detail-packet.json').relative_to(ROOT))),('preread_run',str((PRE/'run.json').relative_to(ROOT))),('preread_lease',str((PRE/'lease.json').relative_to(ROOT))),('primary_first_contract',str((OUT/'primary-first.contract.json').relative_to(ROOT))),('root38_signature','.astis/compact-lsi38/signature.prospective.txt'),('root38_typeprobe','.astis/compact-lsi38/StatementProbe.lean'),('root38_typelog','.astis/compact-lsi38/typecheck.0.log'),('root38_typestatus','.astis/compact-lsi38/typecheck.0.status.json'),('local_eventual','.lake/packages/mathlib/Mathlib/Order/Filter/Basic.lean'),('external_Bernoulli_app','runs/20261007-companion-priority/gaussian-functional-availability/SLT__GaussianLSI__BernoulliLSI.lean.raw.snapshot'),('external_Rademacher_measure','runs/20261007-companion-priority/gaussian-functional-availability/SLT__GaussianPoincare__RademacherApprox.lean.raw.snapshot')]
for role,path in extra:
    add(role,path.replace('\\','/'),(ROOT/path).read_bytes())
assert sha(data['primary_whole'])=='ec485cdad5fe140114be35eef93d19398e0cafcf21abb3fff1bdbbf462e5f94d'
assert len(data['root38_signature'])==308
assert data['root38_signature']==(PRE/'signature.prospective.txt').read_bytes()
assert json.loads(data['preread_lease'])['status']=='CLOSED'
input_receipt=write('inputs.json',{'inputs':bindings,'history':'Primary-first contract froze before root38 type-only exposure. Parent bodies/Tests and37/38 blind/implementation/compiler evidence were not read. Prior CLOSED raw snapshots are the exact mathematical source/API pins.'})

def lines(role):return data[role].decode('utf-8').splitlines()
def find(role,token):
    found=[i+1 for i,s in enumerate(lines(role)) if token in s]
    assert found,(role,token)
    return found[0]
def last(role,token):
    found=[i+1 for i,s in enumerate(lines(role)) if token in s]
    assert found,(role,token)
    return found[-1]
def anchor(role,a,b=None):
    b=a if b is None else b
    ls=data[role].splitlines(keepends=True)
    assert 1<=a<=b<=len(ls),(role,a,b,len(ls))
    raw=b''.join(ls[a-1:b])
    return {'input_role':role,'start_line':a,'end_line':b,'literal_LF_sha256':sha(raw),'literal':raw.decode('utf-8')}
nodes=[]; ids=set()
def node(id,kind,formula,anchors,classification,**extra):
    assert id not in ids;ids.add(id)
    nodes.append({'id':id,'kind':kind,'formula':formula,'classification':classification,'anchors':anchors,**extra})
node('P-FIRST','PRIMARY_CONTEXT','W2(r_y,N(0,I)) <= sqrt(E_r|grad rho|²); only FIRST inequality', [anchor('primary_first',5)],'SOURCE_CONTEXT',mixed_scope='Same physical line also contains2nd/last inequalities, excluded from this bounded delta.')
node('P-OMITTED-LSI','SOURCE_GAP','Printed first inequality combines Gaussian Talagrand and Gaussian LSI but supplies no analytic proof.',[anchor('primary_explanation',1,2)],'SOURCE_GAP')
node('GAP-NONCOMPACT','SOURCE_GAP','Compact scalar C2 theorem alone cannot apply to literal32 positive noncompact sqrt-density; cutoff/W12 extension remains.',[anchor('primary_explanation',1,2)],'RESIDUAL_NOT_PUBLIC_BINDER')
node('GAP-HILBERT','SOURCE_GAP','Tensorization/finiteHilbert Gaussian LSI with actual Sobolev/domain conventions remains.',[anchor('primary_first',5)],'RESIDUAL_NOT_PUBLIC_BINDER')
node('GAP-T2','SOURCE_GAP','TrueGaussian Talagrand/metric/weakRN/Fisher adapters remain; no FIRST4.6 completion.',[anchor('primary_explanation',1,2)],'RESIDUAL_NOT_PUBLIC_BINDER')
node('S-C2','DEFINITION','CompactlySupportedSmooth f = ContDiff Real2 f AND HasCompactSupport f',[anchor('external_C2_definition',44,48)],'EXTERNAL_SOURCE')
node('S-ENT','DEFINITION','Entropy μ g = integral g logg - (integral g) log(integral g)',[anchor('external_entropy_definition',34,49)],'EXTERNAL_SOURCE')
node('S-RAD','DEFINITION','Real Rademacher measure=(1/2)dirac(-1)+(1/2)dirac1',[anchor('external_Rademacher_measure',43,45)],'EXTERNAL_SOURCE')
node('S-RAD-PROB','BACKGROUND_PREREQUISITE','Actual upstream instance IsProbabilityMeasure rademacherMeasure',[anchor('external_Rademacher_measure',47)],'EXTERNAL_HEADER_CUT',proof_boundary='Probability instance provider proof outside compact38 integration; no supplied probability binder in target.')
node('S-PI-PROB','API_PRIMITIVE','Measure.pi.instIsProbabilityMeasure: probability of finite product from coordinate probabilities',[anchor('external_C2_definition',357,359)],'EXTERNAL_IMPORTED_PRIMITIVE',local_callable_credit=False)
node('S-AEMEAS','API_PRIMITIVE','Measurable.aemeasurable used for actual map',[anchor('external_gaussian_definition',94)],'EXTERNAL_IMPORTED_PRIMITIVE',local_callable_credit=False)
node('S-PROB-MAP','API_PRIMITIVE','Measure.isProbabilityMeasure_map on actual probability product and measurable sum',[anchor('external_gaussian_definition',94)],'EXTERNAL_IMPORTED_PRIMITIVE',local_callable_credit=False)
node('S-CARRIER','DEFINITION','RademacherSpace n=Fin n -> Real',[anchor('external_C2_definition',350,351)],'EXTERNAL_SOURCE')
node('S-PRODUCT','DEFINITION','rademacherProductMeasure n=Measure.pi constant Rademacher measure',[anchor('external_C2_definition',353,359)],'EXTERNAL_SOURCE')
node('S-SUM','DEFINITION','rademacherSumProd n x=(sqrt n)^-1 * sum_i x_i',[anchor('external_C2_definition',386,388)],'EXTERNAL_SOURCE')
node('S-SUM-MEAS','BACKGROUND_PRIMITIVE','Measurable rademacherSumProd n',[anchor('external_C2_definition',390,391)],'EXTERNAL_HEADER_CUT',proof_boundary='Measurability proof392-396 is imported provider substrate, excluded from integration delta.')
node('S-LAW','DEFINITION','For NeZero n, actual probability law is product measure.map rademacherSumProd',[anchor('external_gaussian_definition',90,94)],'EXTERNAL_SOURCE')
node('S-GAUSS','DEFINITION','stdGaussian is ProbabilityMeasure gaussianReal0 variance1',[anchor('external_gaussian_definition',38,40)],'EXTERNAL_SOURCE')
node('S-GAUSS-MEASURE','DEFINITION','stdGaussianMeasure=stdGaussian.toMeasure with actual probability instance',[anchor('external_gaussian_definition',149,151)],'EXTERNAL_SOURCE')
node('S-SHIFT','DEFINITION','NeZero n: shifted sum=S_n-2*x_i/sqrt n',[anchor('external_gaussian_definition',945,948)],'EXTERNAL_SOURCE')
node('S-ENTROPY-LIMIT','BACKGROUND_PREREQUISITE','For C2compact, successor product-law homogeneous entropy converges to Gaussian entropy',[anchor('external_gaussian_definition',1213,1215)],'EXTERNAL_HEADER_CUT',proof_boundary='Provider proof1216-1234 is outside integration delta; existing actual36 count-law interface is the authored alternative. No upstream local callable claim.')
node('S-ENERGY-LIMIT','BACKGROUND_PREREQUISITE','Successor sum of real-product squared shifted-coordinate integrals tends to4*Gaussian derivative energy',[anchor('external_gaussian_definition',1030,1034)],'EXTERNAL_HEADER_CUT',proof_boundary='Full energy proof belongs to37 source background, not38; excluded1035-1131.')
node('S-BERNOULLI-APP','BACKGROUND_PREREQUISITE','For C2compact, entropy of real-product sum law <=half sum of shifted squared integrals',[anchor('external_Bernoulli_app',1600,1613)],'EXTERNAL_HEADER_CUT',proof_boundary='Transfer/Bernoulli assembly1614-1634 excluded; actual34 count theorem is genuine local alternative.')
node('S-LHS','SOURCE_PROOF_NODE','h_lhs: successor source entropy tends toGaussian entropy by tendsto_entropy_f_sq hf',[anchor('external_compact_lsi',53,56)],'EXTERNAL_SOURCE')
node('S-HSUM','SOURCE_PROOF_NODE','h_sum: successor source full energy tends to4*Dirichlet by tendsto_sum_sq_shifted_four_deriv_sq hf',[anchor('external_compact_lsi',57,63)],'EXTERNAL_SOURCE')
node('S-HRHS','SOURCE_PROOF_NODE','h_rhs: half-energy limit by h_sum.const_mul(1/2)',[anchor('external_compact_lsi',64,69)],'EXTERNAL_SOURCE')
node('S-CONSTANT','SOURCE_PROOF_NODE','h_rhs_prime: (1/2)*4*E=2*E by convert and ring',[anchor('external_compact_lsi',70,75)],'EXTERNAL_SOURCE')
node('S-INEQ','SOURCE_PROOF_NODE','Each successor source entropy <=half-energy by bernoulli_logSobolev_app hf n',[anchor('external_compact_lsi',76,80)],'EXTERNAL_SOURCE')
node('S-FINAL','SOURCE_CONCLUSION','gaussian_logSobolev_CompSmo: homogeneousGaussian entropy(f²)<=2 integralderiv²',[anchor('external_compact_lsi',45,52),anchor('external_compact_lsi',81,82)],'EXTERNAL_SOURCE_NOT_LOCAL_PRODUCER')
node('API-SQUARE','API_PRIMITIVE','CommRing: (a-b)²=(b-a)²',[anchor('local_square_sign',199,215)],'PINNED_LOCAL_API')
node('API-CONSTMUL','API_PRIMITIVE','Tendsto.const_mul: under SeparatelyContinuousMul, multiply actual limit by fixed scalar',[anchor('local_multiplication_limit',112,134)],'PINNED_LOCAL_API')
node('API-ORDER','API_PRIMITIVE','OrderClosedTopology/Preorder: two Tendsto and eventual<= on NeBot filter imply limit<=',[anchor('local_order_limit',420,424),anchor('local_order_limit',466,482)],'PINNED_LOCAL_API')
node('API-EVENTUAL','API_PRIMITIVE','Eventually.of_forall turns every-index inequality into eventual inequality',[anchor('local_eventual',655,656)],'PINNED_LOCAL_API')
node('API-XLOGX','API_PRIMITIVE','continuous x*logx including0; parent36 zero-mass domain/convergence retained',[anchor('local_zero_mass_continuity',29,63)],'PINNED_LOCAL_API')
node('TYPE-REAL','TYPECLASS','Canonical real Borel/topology/order/field with continuous multiplication and closed order; fixed variance NNReal1',[anchor('root38_signature',2,len(lines('root38_signature'))),anchor('local_gaussian_definition',209,233)],'CANONICAL_TYPECLASS_CONTEXT')
node('TYPE-FILTER','TYPECLASS','Nat atTop is nontrivial; successor n+1 internally nonzero. No public NeBot/NeZero binder.',[anchor('local_order_limit',472,474),anchor('root38_typeprobe',5,8)],'INTERNAL_CANONICAL_TYPECLASS_CONTEXT')
node('A-F','SOURCE_ASSUMPTION','f:Real->Real; signed f allowed',[anchor('root38_signature',2)],'QUANTIFIED_OBSERVER')
node('A-C2','SOURCE_ASSUMPTION','hf:ContDiff Real2 f',[anchor('root38_signature',2),anchor('external_C2_definition',47,48)],'SOURCE_EXTERNAL_COMPACT_SCOPE')
node('A-COMPACT','SOURCE_ASSUMPTION','hs:HasCompactSupport f',[anchor('root38_signature',2),anchor('external_C2_definition',47,48)],'SOURCE_EXTERNAL_COMPACT_SCOPE')
node('A-COUNT','DEFINITION','mu_N=inverse ENNReal card(Fin N->Bool) smulcount; same literal law34/36/37, allN',[anchor('parent34_signature',2,3),anchor('parent36_signature',3,4),anchor('prospective37_signature_only',3,4)],'ACTUAL_PARENT_DEFINITION')
node('A-SUM','DEFINITION','S_N=(sqrt(N:Real))^-1 * sum_j ifepsj then1else-1; same actual36/37',[anchor('parent36_signature',5,6),anchor('prospective37_signature_only',5,6)],'ACTUAL_PARENT_DEFINITION')
node('A-GAMMA','DEFINITION','gamma=gaussianReal0(1:NNReal), variance1',[anchor('root38_signature',3),anchor('parent36_signature',7),anchor('prospective37_signature_only',7)],'ACTUAL_FIXED_DEFINITION')
node('A-ENT','DEFINITION','Literal homogeneous entropy of f²; no normalization or division bymass',[anchor('root38_signature',4,6),anchor('parent34_signature',10,12)],'ACTUAL_FIXED_DEFINITION')
node('A-FLIP','DEFINITION','Function.update eps j(!epsj), actual coordinate flip; not posterior reinterpretation',[anchor('parent34_signature',4,5),anchor('prospective37_signature_only',10,11)],'ACTUAL_FIXED_DEFINITION')
node('A-OBSERVER','AUTHORED_ADAPTER','Set h_N(eps)=f(S_N eps) internally;34 has arbitrary signed real h and no regularity binder.',[anchor('parent34_signature',1),anchor('parent36_signature',11,14)],'AUTHORED_MATHEMATICAL_ROUTE_NOT_PRINTED_SOURCE')
node('P34','EXISTING_COMPILED_SUBSTRATE','Actual half Bernoulli count LSI/probability/L1 for everyN andh',[anchor('parent34_signature',1,len(lines('parent34_signature')))],'SEALED_PARENT_ONLY',state='verified receipt provenance frozen; body not read')
node('P36','EXISTING_COMPILED_SUBSTRATE','Actual count3observer/entropy limits and true domains for C2compact',[anchor('parent36_signature',1,len(lines('parent36_signature')))],'SEALED_PARENT_ONLY',state='verified421496a5 provenance frozen; body not read')
node('P37','CONDITIONAL_PREREQUISITE','Actual full Boolean energy L1/allN and successor4 limit for C2compact',[anchor('prospective37_signature_only',1,len(lines('prospective37_signature_only')))],'SEALED_INTERFACE_ONLY',state='NOT VERIFIED in this graph; requires genuine compiled producer plus independent admission, not a public supplied premise')
node('GAP-P37','SOURCE_GAP','First unmet local dependency is actual37 admitted fullflip producer; its type/seal alone gives no limit truth.',[anchor('prospective37_signature_only',9,len(lines('prospective37_signature_only')))],'CONDITIONAL_INTERNAL_DEPENDENCY_NOT_PUBLIC_BINDER')
node('A-DOMAINS','DERIVED_DOMAIN','TrueGaussian L1 f²,f²logf²,deriv²; actual count domains and energies from34/36/37',[anchor('parent34_signature',6,9),anchor('parent36_signature',8,14),anchor('prospective37_signature_only',8,11)],'INTERNAL_PARENT_OUTPUT_NOT_CERTIFICATE_INPUT')
node('A-ENT-LIMIT','AUTHORED_PROOF_NODE','Actual36 successor homogeneous entropy limit',[anchor('parent36_signature',last('parent36_signature','Tendsto (fun n : ℕ =>'),len(lines('parent36_signature')))],'INTERNAL_PARENT_OUTPUT')
node('A-ENERGY-LIMIT','AUTHORED_PROOF_NODE','Actual37 successor integral-of-full-sum energy tends to4*actualgamma derivative energy',[anchor('prospective37_signature_only',find('prospective37_signature_only','Tendsto'),len(lines('prospective37_signature_only')))],'CONDITIONAL_INTERNAL_PARENT_OUTPUT')
node('A-SIGN-ALIGN','AUTHORED_ADAPTER','PointwiseD34=D37 by sub_sq_comm for each coordinate; no sum/integral swap needed',[anchor('parent34_signature',4,5),anchor('prospective37_signature_only',10,11),anchor('local_square_sign',214,215)],'AUTHORED_MATHEMATICAL_ROUTE')
node('A-FINITE-INEQ','AUTHORED_PROOF_NODE','Every successor actualcount entropy <=(1/2)*integralD37 by34 and sign equality',[anchor('parent34_signature',10,12),anchor('prospective37_signature_only',10,11)],'AUTHORED_MATHEMATICAL_ROUTE')
node('A-HALF-LIMIT','AUTHORED_PROOF_NODE','(1/2)*actual37 energy tends to2*sameGaussian energy; (1/2)*4=2',[anchor('external_compact_lsi',64,75),anchor('prospective37_signature_only',find('prospective37_signature_only','Tendsto'),len(lines('prospective37_signature_only')))],'AUTHORED_MATHEMATICAL_ROUTE')
node('A-EVENTUAL','AUTHORED_PROOF_NODE','Successor34 inequalities yield eventual inequality at Nat atTop',[anchor('local_eventual',655,656),anchor('external_compact_lsi',80,82)],'AUTHORED_MATHEMATICAL_ROUTE')
node('A-ORDER','AUTHORED_PROOF_NODE','Closed-order passage on actual entropy and half-energy limits',[anchor('local_order_limit',472,474),anchor('external_compact_lsi',82)],'AUTHORED_MATHEMATICAL_ROUTE')
node('TARGET','PROSPECTIVE_CONCLUSION','Every signed C2compact scalar f: literal Ent_gaussianReal0,1(f²)<=2 integral(derivf)²',[anchor('root38_signature',1,len(lines('root38_signature')))],'PROSPECTIVE_STATEMENT_ONLY',status='not proved/claimed; independent statement review is separate')
node('A-ZERO','BOUNDARY_CONVENTION','f0/zero Gaussian mass allowed:0log0=0; no mass division; parent36 genuine entropy convergence includes0',[anchor('local_zero_mass_continuity',45,63),anchor('parent36_signature',last('parent36_signature','Tendsto (fun n : ℕ =>'),len(lines('parent36_signature')))],'DERIVED_BOUNDARY_NOT_NEW_BINDER')
node('A-N0','BOUNDARY_CONVENTION','FiniteN0 singletoncount,S0=0,entropy0,empty fullflip0; derivative observer atN0 may be(derivf0)²; limits are only successors',[anchor('parent34_signature',1,5),anchor('parent36_signature',5,6),anchor('prospective37_signature_only',10,len(lines('prospective37_signature_only')))],'AUTHORED_DEFINITION_BOUNDARY')
node('GAP-CARRIER-TRANSPORT','SOURCE_GAP','Printed real-product/sum-of-integrals route is not interchangeable with actual count route without a genuine measure-map/L1 finite-sum adapter. Direct authored route avoids needing that transport.',[anchor('external_Bernoulli_app',1609,1613),anchor('prospective37_signature_only',10,len(lines('prospective37_signature_only')))],'SOURCE_REPRESENTATION_BOUNDARY_NOT_PUBLIC_BINDER')

edges=[]
def edge(fr,to,tag,role,a,b=None,ingredient=None):
    assert fr in ids and to in ids
    semantics='PRINTED_SOURCE_CALLER_OR_SIGNATURE_COMPONENT' if tag in ['EXTERNAL_SOURCE_USE','SOURCE_DIRECT_PROOF_USE'] or role=='external_compact_lsi' else 'AUTHORED_COMPONENT_FORMULA_OR_PINNED_API_DECLARATION_SUPPORT'
    edges.append({'id':'e%03d'%(len(edges)+1),'from':fr,'to':to,'tag':tag,'ingredient':ingredient or next(n['formula'] for n in nodes if n['id']==fr),'caller_anchor':anchor(role,a,b),'anchor_semantics':semantics,'truth_contract':'source/API ingredient dependency only; authored edges cite exact supporting component formulas, not a nonexistent future implementation caller; no compiled dependency or proof-completion claim'})
def uses(parents,to,role,a,b=None,tag='EXTERNAL_SOURCE_USE'):
    for fr in parents:edge(fr,to,tag,role,a,b)
# Direct external definition dependencies, including all imported law objects.
uses(['S-RAD','S-CARRIER'],'S-PRODUCT','external_C2_definition',354,359)
uses(['S-RAD'],'S-RAD-PROB','external_Rademacher_measure',47)
uses(['S-RAD-PROB','S-PI-PROB'],'S-PRODUCT','external_C2_definition',357,359)
uses(['S-CARRIER'],'S-SUM','external_C2_definition',387,388)
uses(['S-SUM','S-CARRIER'],'S-SUM-MEAS','external_C2_definition',391,391)
uses(['S-PRODUCT','S-SUM','S-SUM-MEAS'],'S-LAW','external_gaussian_definition',92,94)
uses(['S-AEMEAS','S-PROB-MAP'],'S-LAW','external_gaussian_definition',94)
uses(['S-GAUSS'],'S-GAUSS-MEASURE','external_gaussian_definition',149,151)
uses(['S-SUM','S-CARRIER'],'S-SHIFT','external_gaussian_definition',947,948)
uses(['S-C2','S-LAW','S-ENT','S-GAUSS-MEASURE'],'S-ENTROPY-LIMIT','external_gaussian_definition',1213,1215)
uses(['S-C2','S-PRODUCT','S-SUM','S-SHIFT','S-GAUSS-MEASURE'],'S-ENERGY-LIMIT','external_gaussian_definition',1030,1034)
uses(['S-C2','S-LAW','S-ENT','S-PRODUCT','S-SUM','S-SHIFT'],'S-BERNOULLI-APP','external_Bernoulli_app',1609,1613)
uses(['S-C2','S-ENTROPY-LIMIT','S-LAW','S-ENT','S-GAUSS-MEASURE'],'S-LHS','external_compact_lsi',54,56)
uses(['S-C2','S-ENERGY-LIMIT','S-PRODUCT','S-SUM','S-SHIFT','S-GAUSS-MEASURE'],'S-HSUM','external_compact_lsi',58,62)
uses(['S-HSUM','S-PRODUCT','S-SUM','S-SHIFT','S-GAUSS-MEASURE'],'S-HRHS','external_compact_lsi',64,69)
uses(['API-CONSTMUL'],'S-HRHS','external_compact_lsi',69,tag='PINNED_API_USE')
uses(['S-HRHS','S-PRODUCT','S-SUM','S-SHIFT','S-GAUSS-MEASURE'],'S-CONSTANT','external_compact_lsi',70,75)
uses(['S-C2','S-BERNOULLI-APP','S-LAW','S-ENT','S-PRODUCT','S-SUM','S-SHIFT'],'S-INEQ','external_compact_lsi',77,80)
uses(['S-LHS','S-CONSTANT','S-INEQ','API-EVENTUAL','API-ORDER'],'S-FINAL','external_compact_lsi',82,tag='SOURCE_DIRECT_PROOF_USE')
uses(['S-C2','S-ENT','S-GAUSS-MEASURE'],'S-FINAL','external_compact_lsi',50,52)
edge('S-FINAL','TARGET','SOURCE_CORRESPONDENCE','root38_signature',1,len(lines('root38_signature')),'Same compact scalar mathematical conclusion after unfolding entropy/C2/Gaussian aliases, not local implication or certified carrier transport.')
# Authored count route. Caller anchors are sealed interface or literal adapter API.
uses(['A-F','A-SUM','A-COUNT'],'A-OBSERVER','parent34_signature',1,5,tag='AUTHORED_DEFINITION_USE')
uses(['A-F','A-OBSERVER','A-COUNT','A-FLIP','A-ENT'],'P34','parent34_signature',1,len(lines('parent34_signature')),tag='AUTHORED_INTERFACE_SPECIALIZATION')
uses(['A-F','A-C2','A-COMPACT','A-COUNT','A-SUM','A-GAMMA','A-ENT'],'P36','parent36_signature',1,len(lines('parent36_signature')),tag='SEALED_INTERFACE_DEFINITION_USE')
uses(['A-F','A-C2','A-COMPACT','A-COUNT','A-SUM','A-GAMMA','A-FLIP'],'P37','prospective37_signature_only',1,len(lines('prospective37_signature_only')),tag='CONDITIONAL_INTERFACE_DEFINITION_USE')
edge('GAP-P37','P37','CONDITIONAL_PRODUCER_BOUNDARY','prospective37_signature_only',1,len(lines('prospective37_signature_only')))
uses(['P34'],'A-DOMAINS','parent34_signature',6,9,tag='DERIVED_DOMAIN_DEPENDENCY')
uses(['P36','A-COUNT','A-SUM','A-GAMMA'],'A-DOMAINS','parent36_signature',8,14,tag='DERIVED_DOMAIN_DEPENDENCY')
uses(['P37'],'A-DOMAINS','prospective37_signature_only',8,11,tag='CONDITIONAL_DERIVED_DOMAIN_DEPENDENCY')
uses(['P36','A-COUNT','A-SUM','A-GAMMA','A-ENT'],'A-ENT-LIMIT','parent36_signature',last('parent36_signature','Tendsto (fun n : ℕ =>'),len(lines('parent36_signature')),tag='AUTHORED_PARENT_OUTPUT_USE')
uses(['P37','A-COUNT','A-SUM','A-GAMMA','A-FLIP'],'A-ENERGY-LIMIT','prospective37_signature_only',find('prospective37_signature_only','Tendsto'),len(lines('prospective37_signature_only')),tag='CONDITIONAL_PARENT_OUTPUT_USE')
uses(['A-FLIP','A-SUM','A-OBSERVER'],'A-SIGN-ALIGN','parent34_signature',4,5,tag='AUTHORED_DEFINITION_USE')
edge('API-SQUARE','A-SIGN-ALIGN','PINNED_API_USE','local_square_sign',214,215)
uses(['P34','A-OBSERVER','A-SIGN-ALIGN','A-COUNT','A-ENT'],'A-FINITE-INEQ','parent34_signature',10,12,tag='AUTHORED_MATHEMATICAL_ROUTE')
uses(['A-ENERGY-LIMIT','A-GAMMA'],'A-HALF-LIMIT','prospective37_signature_only',find('prospective37_signature_only','Tendsto'),len(lines('prospective37_signature_only')),tag='AUTHORED_MATHEMATICAL_ROUTE')
edge('API-CONSTMUL','A-HALF-LIMIT','PINNED_API_USE','local_multiplication_limit',132,134)
edge('S-CONSTANT','A-HALF-LIMIT','AUTHORED_ARITHMETIC_RECONSTRUCTION','external_compact_lsi',70,75,'Exact(1/2)*4=2 ring identity; source formula reused, no external theorem call.')
uses(['A-FINITE-INEQ','API-EVENTUAL'],'A-EVENTUAL','local_eventual',655,656,tag='AUTHORED_MATHEMATICAL_ROUTE')
uses(['A-ENT-LIMIT','A-HALF-LIMIT','A-EVENTUAL','API-ORDER','TYPE-REAL','TYPE-FILTER'],'A-ORDER','local_order_limit',472,474,tag='AUTHORED_MATHEMATICAL_ROUTE')
uses(['A-ORDER','A-DOMAINS','A-F','A-C2','A-COMPACT','A-GAMMA','A-ENT'],'TARGET','root38_signature',1,len(lines('root38_signature')),tag='AUTHORED_INGREDIENT_DEPENDENCY')
uses(['P36','API-XLOGX'],'A-ZERO','local_zero_mass_continuity',45,63,tag='PARENT_BOUNDARY_RETENTION')
uses(['A-COUNT','A-SUM','A-FLIP','P34','P36','P37'],'A-N0','prospective37_signature_only',10,len(lines('prospective37_signature_only')),tag='AUTHORED_BOUNDARY_AUDIT')
uses(['A-ZERO','A-N0'],'TARGET','root38_signature',2,len(lines('root38_signature')),tag='DOMAIN_SCOPE_BOUNDARY')
uses(['TARGET'],'GAP-NONCOMPACT','primary_explanation',1,2,tag='DEPENDENCY_BOUNDARY')
uses(['GAP-NONCOMPACT','GAP-HILBERT','GAP-T2'],'P-OMITTED-LSI','primary_explanation',1,2,tag='OPEN_SOURCE_OBLIGATION')
uses(['P-OMITTED-LSI','GAP-T2'],'P-FIRST','primary_first',5,tag='OPEN_SOURCE_OBLIGATION')
uses(['S-LAW','S-PRODUCT','S-SUM','S-SHIFT','A-COUNT','A-SUM','A-FLIP'],'GAP-CARRIER-TRANSPORT','external_Bernoulli_app',1609,1613,tag='DEPENDENCY_BOUNDARY')
edge('TYPE-REAL','API-SQUARE','CANONICAL_TYPECLASS_DEPENDENCY','local_square_sign',199,200,'Canonical Real CommRing instance; not an added source premise.')
edge('TYPE-REAL','API-CONSTMUL','CANONICAL_TYPECLASS_DEPENDENCY','local_multiplication_limit',114,121,'Canonical Real topological multiplication, SeparatelyContinuousMul.')
edge('TYPE-REAL','API-ORDER','CANONICAL_TYPECLASS_DEPENDENCY','local_order_limit',424,424,'Canonical Real Preorder/OrderClosedTopology.')
edge('TYPE-FILTER','A-EVENTUAL','CANONICAL_FILTER_DEFINITION','local_eventual',655,656,'All successor indices Nat; eventual inequality at Nat atTop.')
uses(['TYPE-REAL','TYPE-FILTER'],'S-FINAL','external_compact_lsi',82,tag='CANONICAL_API_CONTEXT')
uses(['A-C2','A-COMPACT'],'S-C2','external_C2_definition',47,48,tag='SOURCE_BINDER_EXPANSION')
edge('S-GAUSS-MEASURE','A-GAMMA','DEFINITION_CORRESPONDENCE','external_gaussian_definition',38,40,'Both are the same actual gaussianReal0 variance1; no algorithm/law-transport assertion.')
edge('S-ENT','A-ENT','DEFINITION_CORRESPONDENCE','external_entropy_definition',48,49,'Same literal homogeneous entropy after substituting g=f²; no RN representative or mass normalization.')

# Exhaustive disjoint physical-line partitions of every explicitly selected window.
selections=[]
def select(role,a,b,disposition,nodeids=None,reason=None,mixed=None):
    selections.append({'input_role':role,'start_line':a,'end_line':b,'disposition':disposition,'nodes':nodeids or [],'reason':reason,'mixed_scope_exclusions':mixed})
select('primary_first',1,4,'EXCLUDED',reason='HTML equation scaffolding/blank lines')
select('primary_first',5,5,'NODE',['P-FIRST'],mixed='First inequality retained; same line second/last eta/moment bounds excluded.')
select('primary_first',6,8,'EXCLUDED',reason='HTML label/scaffolding, no new proof ingredient')
select('primary_explanation',1,2,'NODE',['P-OMITTED-LSI'],mixed='Only first GaussianTalagrand+LSI sentence retained; second-bound introduction excluded.')
select('primary_explanation',3,5,'EXCLUDED',reason='Second/last4.6 Lipschitz/mode/IBP proof beyond compactLSI integration')
# Complete external integration file, including explicit exclusions of unrelated wrappers.
select('external_compact_lsi',1,40,'EXCLUDED',reason='License/imports/overview/notation; import pin retained separately; summary proof duplicates exact formal body50-82')
select('external_compact_lsi',41,49,'NODE',['S-FINAL'],mixed='Mathematical exposition of identical compact entropy definition, no additional premise')
for a,b,ns in [(50,52,['S-FINAL']),(53,56,['S-LHS']),(57,63,['S-HSUM']),(64,69,['S-HRHS']),(70,75,['S-CONSTANT']),(76,80,['S-INEQ']),(81,82,['S-FINAL'])]:select('external_compact_lsi',a,b,'NODE',ns)
select('external_compact_lsi',83,101,'EXCLUDED',reason='Blank lines, scalar deriv/fderiv norm equality and alternate wrapper; target uses deriv, no need to port')
for role,a,b,ns in [('external_entropy_definition',34,49,['S-ENT']),('external_C2_definition',44,48,['S-C2']),('external_Rademacher_measure',43,45,['S-RAD']),('external_Rademacher_measure',47,47,['S-RAD-PROB']),('external_C2_definition',350,355,['S-CARRIER','S-PRODUCT']),('external_C2_definition',357,359,['S-PRODUCT','S-PI-PROB']),('external_C2_definition',386,391,['S-SUM','S-SUM-MEAS']),('external_gaussian_definition',38,40,['S-GAUSS']),('external_gaussian_definition',90,94,['S-LAW','S-AEMEAS','S-PROB-MAP']),('external_gaussian_definition',149,151,['S-GAUSS-MEASURE']),('external_gaussian_definition',945,948,['S-SHIFT']),('external_gaussian_definition',1030,1034,['S-ENERGY-LIMIT']),('external_gaussian_definition',1213,1215,['S-ENTROPY-LIMIT']),('external_Bernoulli_app',1600,1613,['S-BERNOULLI-APP']),('local_square_sign',199,215,['API-SQUARE']),('local_multiplication_limit',112,134,['API-CONSTMUL']),('local_order_limit',420,424,['API-ORDER']),('local_order_limit',466,482,['API-ORDER']),('local_eventual',655,656,['API-EVENTUAL']),('local_zero_mass_continuity',29,63,['API-XLOGX']),('local_gaussian_definition',209,233,['TYPE-REAL'])]:select(role,a,b,'NODE',ns)
select('external_C2_definition',392,396,'EXCLUDED',reason='Imported measurable-sum provider proof; outside compact38 integration delta. Its explicit actual header391 is retained.')
select('external_gaussian_definition',1035,1131,'EXCLUDED',reason='Observed external upstream energy proof plus next entropy-bound lemma introduction: separate37 source prerequisite proof, outside minimal38 integration delta; no local producer claim')
select('external_gaussian_definition',1216,1234,'EXCLUDED',reason='Existing entropy provider internal observer-limit/mulLog composition proof: domain preserved via36; not repeated in38 integration')
select('external_Bernoulli_app',1614,1634,'EXCLUDED',reason='External count-to-realproduct entropy/gradient transport proof outside direct count route. Conditional representation adapter gap explicit.')
for role,ns in [('parent34_signature',['P34','A-COUNT','A-FLIP','A-ENT']),('parent36_signature',['P36','A-COUNT','A-SUM','A-GAMMA','A-DOMAINS','A-ENT-LIMIT']),('prospective37_signature_only',['P37','GAP-P37','A-COUNT','A-SUM','A-GAMMA','A-FLIP','A-ENERGY-LIMIT']),('root38_signature',['TARGET','A-F','A-C2','A-COMPACT','A-GAMMA','A-ENT'])]:
    select(role,1,len(lines(role)),'NODE',ns,mixed='Full sealed interface including blank tail; no body or theorem proof.')
select('root38_typeprobe',1,len(lines('root38_typeprobe')),'EXCLUDED',reason='Type-only forall/Prop probe is target context evidence, not source proof or graph dependency; no theorem body.')
seen={}; inventory=[]
for i,s in enumerate(selections):
    for k in range(s['start_line'],s['end_line']+1):
        key=(s['input_role'],k);assert key not in seen,key;seen[key]=s['disposition']
    ar=anchor(s['input_role'],s['start_line'],s['end_line']); name='source.region.%03d.LF.snapshot'%i
    with (OUT/name).open('xb') as f:f.write(ar['literal'].encode('utf-8'))
    inventory.append(dict(s,region_id='R%03d'%(i+1),raw_LF_sha256=ar['literal_LF_sha256'],snapshot=name,selected_physical_lines=s['end_line']-s['start_line']+1))
windows={}
for role,k in seen:windows.setdefault(role,[]).append(k)
contract={
 'artifact_kind':'source-only compact scalar GaussianLSI integration contract','actor':'gaussian_domain_preproof_reviewer_29','status':'AUTHOR_FROZEN_NOT_SELFVALIDATED',
 'primary_first':'primary-first.contract.json','target':{'name':'AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.GaussianCompactLogSobolev.compact_gaussian_logSobolev','raw_LF_sha256':sha(data['root38_signature']),'bytes':308,'seven_slots':json.loads(data['preread_packet'])['seven_slots']},
 'assumptions':[{'input':'f:Real->Real','classification':'QUANTIFIED_OBSERVER'},{'input':'ContDiff Real2 f','classification':'EXTERNAL_SOURCE_COMPACT_BACKGROUND'},{'input':'HasCompactSupport f','classification':'EXTERNAL_SOURCE_COMPACT_BACKGROUND'}],
 'internal_ingredients':['Actual fixed variance1Gaussian','Same actual inverse-card normalizedcount/S_N','Signed square equality','Real closed-order and continuous scalar multiplication','True36Gaussian observer L1','AllN34/36/37actual count domains','Actual36entropy and conditional37fullenergy successor limits'],
 'no_extra_public_premise':['normalization/positive mass','positivef','Integrable/law/probability','LSI','entropy/energy/weaklaw convergence','Lipschitz/energy/limit certificate'],
 'definition_scope':json.loads(data['preread_packet'])['fixed_definitions'],'boundary_cases':json.loads(data['preread_packet'])['boundary_cases'],
 'source_truth':'SPHMC printed FIRST4.6 omits analytic GaussianLSI/Talagrand proof. SLT compact C2 scalar consumer is external source background, not a theorem printed by SPHMC. Direct Boolean count route is explicitly authored. No source theorem premise is broadened.',
 'API_boundary':'Pinned Mathlib primitives are retained as declaration semantics/context and prior library substrate, not new proof claims or a recursive all-Mathlib proof reconstruction. External imported primitives are explicitly marked reference-only. Parent provider proof bodies beyond the sealed/header dependency cut are excluded.',
 'parent_status':{'34':'Existing independently VERIFIED/public sealed interface only; body not read','36':'Existing independently VERIFIED421496a5/public sealed interface only; body not read','37':'Conditional sealed877-byte interface only, NOT VERIFIED in this packet; no desired result supplied as public binder'},
 'typecheck':'Root308-byte forallProp probe log/status type-only context; no named theorem declaration was elaborated. Independent StatementSeal review belongs to picard, not this author. Root later reports independent accepted archive; current graph binds earlier immutable signature/proposition evidence and does not use that verdict as topology truth.',
 'remaining_open':json.loads(data['preread_packet'])['remaining_open'],'compiler_started':False,'compiled_edges':[], 'self_validation':False
}
contract_receipt=write('source.contract.json',contract)
inventory_receipt=write('source.inventory.json',{'scope':'Every physical line of explicitly selected disjoint windows assigned NODE or EXCLUDED; excludes all other source regions/project. Complete compact consumer file1-101 selected; only exact needed dependency headers/definitions/API windows elsewhere. Mixed originalHTML lines have explicit semantic exclusions. No whole upstream proof claim.','input_bindings':input_receipt,'regions':inventory,'selected_input_count':len(windows),'selected_physical_lines':len(seen),'regions_count':len(inventory),'duplicate_selected_lines':0,'source_excess_public_binders':0,'construction_checks':'Author enumeration invariants only; independently reviewed topology remains pending.'})
alternatives=[
 {'id':'OR-ACTUAL-BOOL','kind':'AUTHORED_ALTERNATIVE','inputs':['P34','P36','P37','A-SIGN-ALIGN','API-CONSTMUL','API-ORDER','API-EVENTUAL','TYPE-REAL','TYPE-FILTER'],'output':'TARGET','route':'Same literal count entropy and integral-of-full-sum; square signs only, half*4=2, closed-order limit','prerequisite_boundary':'P37 producer admission is OPEN; no internal source gap becomes a public premise','source_attribution':'Authored generic omitted-background integration, not printedSPHMC proof or external product-law transport'},
 {'id':'OR-EXTERNAL-PRODUCT','kind':'EXTERNAL_SOURCE_ROUTE','inputs':['S-ENTROPY-LIMIT','S-ENERGY-LIMIT','S-BERNOULLI-APP','API-CONSTMUL','API-ORDER','API-EVENTUAL'],'output':'S-FINAL','route':'Literal pinned SLT50-82 product-law/sum-of-integrals compact consumer','prerequisite_boundary':'External source only, not local callable producer. Reusing this carrier to prove actual ASTIS count intermediary would require GAP-CARRIER-TRANSPORT; direct alternative does not need it.'}
]
graph={
 'schema_version':1,'artifact_kind':'independent-source-proof-graph','actor':'gaussian_domain_preproof_reviewer_29','role':'SOURCE_GRAPH_AUTHOR','status':'AUTHOR_FROZEN_AWAITING_DISTINCT_TOPOLOGY_REVIEW','source_governed':True,
 'provenance':'Reconstructed from original primary context, literal pinned SLT compact consumer and dependency headers, local API declarations and already sealed interfaces only. No38implementation/Test/blind/proof and no37implementation/Test/blind/compiler evidence exposure. Root38 type-only target does not drive dependency route; primary/preread froze first.',
 'source_contract':contract_receipt,'source_inventory':inventory_receipt,'input_bindings':input_receipt,'nodes':nodes,'edges':edges,'or_routes':alternatives,'compiled_edges':[],
 'truth_contract':{'nodes':'Source/background/API/prospective mathematical ingredients, no new theorem truth','edges':'Ingredient dependencies with exact literal caller lines; no compiled edge inference','existing_parents':'34/36 seal+verification provenance frozen only','conditional37':'Genuine producer/admission required before future38 proof; sealed type is not a certificate','author_self_validation':False,'no_convenience_premises':True},
 'source_gaps':['P-OMITTED-LSI','GAP-P37','GAP-CARRIER-TRANSPORT','GAP-NONCOMPACT','GAP-HILBERT','GAP-T2'],
 'counts':{'nodes':len(nodes),'edges':len(edges),'or_routes':len(alternatives),'selected_regions':len(inventory),'selected_physical_lines':len(seen),'input_pins':len(bindings)},
 'remaining_truth_boundary':contract['remaining_open'],'no_compiler_or_claim':True
}
graph_receipt=write('source-proof-graph.independent.json',graph)
digest={'synthesis_first':'Minimal future38 consumer: actual34 half fullflip count inequality + literal sign-square adapter + actual36 zero-mass-safe homogeneous entropy convergence + conditional37 truefullenergy4 limit ->half limit2->closed-order limit. No additional analytic binder or carrier transport needed on direct count route.37 remains not VERIFIED.','route_at_most_seven_steps':json.loads(data['preread_packet'])['route_at_most_seven_steps'],'source_contract':contract_receipt,'graph':graph_receipt,'inventory':inventory_receipt,'independent_topology_review':'PENDING distinctphase; this source author cannot validate own graph','remaining_open':contract['remaining_open'],'leases':{'read':'CLOSED','write':'CLOSED','compiler':'CLOSED'},'compiler_started':False}
digest_receipt=write('bounded-synthesis.json',digest)
payload={'inputs':input_receipt,'contract':contract_receipt,'inventory':inventory_receipt,'graph':graph_receipt,'digest':digest_receipt,'actor':graph['actor'],'counts':graph['counts'],'scope':'immutable implementation-independent source authoring only'}
runsha=sha(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8'))
write('author.run.json',{'deterministic_run_sha256':runsha,'deterministic_payload':payload,'leases':{'read':'CLOSED','write':'CLOSED','compiler':'CLOSED'},'compiler_started':False})
for b in bindings:
    observed=(ROOT/b['observed_path']).read_bytes()
    assert sha(observed)==b['raw_sha256'] and sha(lf(observed))==b['lf_sha256'],b['observed_path']
lease=json.loads((OUT/'author.lease.json').read_text(encoding='utf-8'))
lease.update({'status':'CLOSED','read':'CLOSED','write':'CLOSED','compiler':'CLOSED','compiler_started':False,'closed_utc':datetime.datetime.utcnow().isoformat()+'Z','deterministic_run_sha256':runsha,'all_observed_input_raw_LF_rechecked_unchanged':True,'no_selfvalidation':True,'counts':graph['counts']})
(OUT/'author.lease.json').write_bytes((json.dumps(lease,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'graph':graph_receipt,'contract':contract_receipt,'inventory':inventory_receipt,'counts':graph['counts'],'run_sha256':runsha,'status':'CLOSED','compiler_started':False},indent=2))
