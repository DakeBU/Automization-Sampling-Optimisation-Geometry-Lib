from pathlib import Path
import json, hashlib, datetime
task=Path(__file__).parent
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(data):return hashlib.sha256(data).hexdigest()
def load(name):
    with (task/name).open('r',encoding='utf-8') as handle:return json.load(handle)
def save(name,obj):
    with (task/name).open('w',encoding='utf-8',newline='\n') as handle:json.dump(obj,handle,indent=2,ensure_ascii=False);handle.write('\n')
def byte_record(path):
    with path.open('rb') as handle:data=handle.read()
    lf=data.replace(b'\r\n',b'\n')
    return {'path':str(path),'raw_bytes':len(data),'raw_sha256':digest(data),'lf_bytes':len(lf),'lf_sha256':digest(lf),'normalization':'replace literal CRLF bytes by LF; no decode/reencode'}
source=load('source-first-proof-graph.json'); inventory=load('primary-source-anchor-inventory.json')
providers=load('provider-contract-snapshots.json'); contexts=load('external-semantic-context-snapshots.json')
statement=byte_record(task/'prospective-statement.target.raw.snapshot.txt')
assert statement['lf_bytes']==1755 and statement['lf_sha256']=='fea2c3ade170bc0526d659f8c51abedaa0ce1a6186e75f0d8a2532b6608e94d8'
freeze=byte_record(task/'primary-before-signature.freeze.json')
assert freeze['raw_sha256']=='031343dd45d286aef4a97771cb95b8c2a4e48285abd92faca12466d3663cbe88'
limitation={
 'primary_first_freeze_precedes_exposure':True,
 'strict_provider_body_blindness':False,
 'existing_provider_incidental_body_lines':[
  {'file':'AutoSamplingTheory/ExampleCases/ProximalBPS/L2MacroscopicMean.lean','line':62,'text':'    MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks hα hαβ hV hH hη hβη'},
  {'file':'AutoSamplingTheory/ExampleCases/ProximalBPS/SourceMeanGradientDomain.lean','line':66,'text':'    MacroscopicEnergy.actual_macroscopic_gradient_energy_blocks hα hαβ hV hH hη hβη'}],
 'chronology':'After primary-first stage and before header-only extraction, one broad rg printed the two call-site lines. No surrounding proof transcript was opened. Subsequent provider extraction stopped physically before := by. These call sites are observability only and are not source edges.',
 'mathlib_typing_definition_observation':'A requested Lp structural definition range 89-93 also displayed zero_mem and add_mem typing fields at lines92-93; current context is corrected to definition/carrier lines89-91. Superseded lexical snapshots remain evidence, not mathematical proof routes.',
 'candidate56_implementation_seen':False,'other_target_review_verdict_seen':False,
 'source_topology_derived_from':'Previously frozen primary-only 22-node graph, balanced source anchors and blueprint; not provider call sites, imports, proof bodies or a verdict.'}
save('read-isolation-and-chronology56.json',limitation)
rows=[]
def row(item,classification,expansion,anchor,dependency=None):
 rows.append({'item':item,'classification':classification,'semantic_expansion':expansion,'source_anchors':anchor,'proof_dependencies':dependency or [],'disposition':'EXPANDED' if classification!='DEEP_EXTERNAL_TYPING_BOUNDARY' else 'TYPED_DEEP_EXTERNAL_BOUNDARY'})
row('E : Type*','TYPING','One finite-dimensional real inner-product carrier; not a hidden model law',['S1.p1'])
row('NormedAddCommGroup E','DEEP_EXTERNAL_TYPING_BOUNDARY','Additive abelian group, metric norm and norm compatibility; supplies vector subtraction, scalar/vector L2 Banach carrier after completeness derivation',['S1.p1'])
row('InnerProductSpace ℝ E','DEEP_EXTERNAL_TYPING_BOUNDARY','Real module with positive-definite symmetric bilinear inner product and induced norm; Riesz identification used only for genuine differentiable compact core',['S1.p1'])
row('FiniteDimensional ℝ E','TYPING','Finite real dimension; equivalent Euclidean presentation after orthonormal coordinates. Includes rank0 as an explicit presentation extension; no nontriviality binder',['S1.p1'])
row('MeasurableSpace E; BorelSpace E','TYPING','Measurable sets are the Borel sigma algebra of the norm topology; not arbitrary measurable structure',['S1.p1','S2.E6'])
row('generated CompleteSpace/Module/topological/Borel/product instances','DEEP_EXTERNAL_TYPING_BOUNDARY','Real is complete; finite-dimensional real normed space is complete. Scalar/vector Lp2 are complete normed real modules. Product measurability, standard-Borel/second-countable instances support actual kernel disintegration. These are typing-derived, never caller-supplied theorem estimates',['S1.p1','A3.SS1.p1.1'])
row('V : E → ℝ','STANDING','Potential of mu, an actual real function on whole E',['S1.p1','S1.E1'])
row('α β : ℝ≥0; hα; hαβ','STANDING','0<alpha<=beta, coercions to reals preserve order; beta>0 derived',['S1.p1','S1.E1'])
row('hV : ContDiff ℝ 2 V','STANDING','Twice continuously Frechet differentiable potential globally; no higher derivatives',['S1.p1'])
row('hH : ∀ x v, alpha||v||²≤D²V(x)[v,v]≤beta||v||²','STANDING','Every point and vector, both quadratic Hessian bounds; source alpha I≼Hess V≼beta I. Real C2 gives symmetric Hessian; its spectral consequences are proof ingredients',['S1.E1'])
row('hη : 0<eta; hβη : beta*eta≤1','SOURCE','Positive proximal scale capped at1/beta; division/square-root denominators positive; alpha eta≤1 derived inside',['S2.SS2.p1.1','A2.Thmtheorem1.p1.1'])
row('mu = volume.tilted(-V)','DEFINITION','Lebesgue exponential tilt exp(-V)/integral exp(-V). Totalized zero law if normalization fails; actual probability provided from source curvature/producer55, never taken from definition alone',['S1.p1','S2.E6'],['provider55'])
row('J = map (x,z)↦(x,x+sqrt(eta)z) (mu.prod stdGaussian)','DEFINITION','Independent X~mu and standard Gaussian Z, forward joint pi_eta; raw density and generative law are source (2.6)/(2.7). Positive eta essential',['S2.E6','S2.E7'],['provider55'])
row('nu=J.snd','DEFINITION','Same Y+ marginal throughout scalar/vector Lp, norms, AE assertions and energy. Reflected Y- law matches nu through actual exchangeability',['S2.SS2.p1.3','A2.SS2.p2.2'],['provider55'])
row('S y = volume.tilted[-V((y+x)/2)-||y-x||²/(8eta)]','DEFINITION','Every-y literal source reflected conditional law p_y; normalized probability and measurable Markov kernel are produced, not assumed. Actual disintegration is only an AE identifying property',['A3.Ex1','A2.E8'],['provider50','provider55'])
row('Lp ℝ 2 nu and Lp E 2 nu','DEEP_EXTERNAL_TYPING_BOUNDARY','AE strongly measurable functions modulo nu-AE equality with finite squared norm integral. p=2 is ENNReal coercion, >=1 finite and nonzero. Canonical function representative need not preserve operations pointwise; addition/subtraction/scalar identities hold nu-AE. toLp needs real MemLp, not fabricated witnesses',['A2.SS2.p2.2'])
row('IsProbabilityMeasure nu','CONCLUSION','nu total mass1, finite; not a public assumption',['S2.E7'],['provider55','provider54'])
row('∃ G : Lp ℝ 2 nu →ₗ.[ℝ] Lp E 2 nu','CONCLUSION','Partial linear map with a genuine submodule domain and linear function from it; one G chosen before T,K and all inputs',['A3.SS1.p1.1'],['provider54'])
row('Dense G.domain; G.IsClosable; G.closure.IsClosed','CONCLUSION','Topological density of genuine compact gradient core. Closability means graph topological closure is graph of one partial linear map; closure fallback cannot matter because closability is output. Closedness is product L2 graph closedness',['A3.SS1.p1.1'],['provider54'])
row('∀u v, graph iff ∃phi smooth compact with u AE phi and v AE gradient phi','CONCLUSION','Exhaustive original compact-gradient graph characterization; rules out arbitrary finite-rank/zero substitute. gradient(phi) is classical Riesz derivative because phi smooth; equivalence-class pair defined via AE equality',['A3.SS1.p1.1'],['provider54'])
row('∃T continuous real linear scalar-L2 endomorphism','CONCLUSION','One uniform actual conditional-mean T selected before every rough u; not a per-input operator or witness',['A2.E1','A2.E9'],['provider55'])
row('∃K continuous real linear scalar-to-vector L2 map','CONCLUSION','One uniformly bounded derivative-of-mean extension K before every u; output not input convergence/graph certificate',['A3.SS1.p1.1'],['route56:bounded-extension'])
row('∀u : Lp ℝ 2 nu','SOURCE_SCOPE','Every rough L2 input; no H1, smoothness, compactness or mean-zero restriction; mean-zero starts only B.14',['A2.Thmtheorem1.p2.1','A2.E13'])
row('(T u,K u)∈G.closure.graph','CONCLUSION','Actual closed compact-gradient graph pair for every input. Tf compact support is not claimed; closure admits noncompact differentiable means. Separately defined weak-H1 equivalence remains open',['A3.SS1.p1.1'],['route56:closed-graph'])
row('||Tu||≤||u||','CONCLUSION','Actual same-law L2 contraction, not a provider assumption passed as binder',['A2.E1','A2.E9'],['provider55'])
row('Tu AE integral u(x)dS_y','CONCLUSION','Representative equality nu-AE; literal S is every-y, but rough integrability/mean identification only nu-AE. Bochner integral totalization off admissible fibers gives no pointwise rough promise',['A2.E9'],['provider55'])
row('AEy Integrable u S_y and Integrable u² S_y','CONCLUSION','Both fiber L1 moments genuinely derived from rough L2 and same-law disintegration; simultaneous AE-domain supports representative substitutions and variance identities',['A2.E9'],['provider55'])
row('eta||Ku||²≤[(1-alpha eta)²/(4(1+alpha eta))](||u||²-||Tu||²)','CONCLUSION','Exact C.2 sharp coefficient, no tunable constant, same-law norm defect. Norm-defect nonnegative by contraction; continuous density passage is a proof edge',['A3.EGx25','A3.SS1.p1.1'],['provider50','provider55','route56:sharp-energy'])
row('4eta||Ku||²≤||u||²-||Tu||²','CONCLUSION','Source B.13 coarse bound follows alpha eta in(0,1], no division by1-alpha eta; alpha eta=1 forces K=0 for eta>0',['A2.E13','A3.SS1.p3.7'],['route56:source-cap'])
save('target-binder-semantic-expansion56.json',{'target':statement,'rows':rows,'implicit_or_alias_status':'Every target slot listed; external typing primitives terminate as named typed boundaries, not invented source assumptions','EXCESS_public_binders':[],'unresolved_count':0,'zero_unresolved_meaning':'Every slot has an explicit disposition/semantic boundary; not a claim of completed proof or deep dependency formalization.'})
provider_rows=[]
def provider(label,clauses,use,status):
 record=next(p for p in providers if p['declaration']==label)
 for clause,semantics,anchors in clauses:
  provider_rows.append({'provider':label,'physical_header':record,'clause':clause,'semantic_expansion':semantics,'source_anchors':anchors,'caller_use':use,'body_status':'OPAQUE_EXCEPT_DISCLOSED_TWO_INITIAL_CALL_SITE_LINES','truth_status':status,'disposition':'OPAQUE_PUBLIC_PROVIDER_CONTRACT'})
provider('literal_source_mean_in_closed_gradient',[
 ('nu probability','Actual same-law Y marginal finite probability',['S2.E7']),
 ('uniform genuine G/dense/closable/closed','Original graph iff actual smooth compact representatives and classical gradients, uniform core independent of target input',['A3.SS1.p1.1']),
 ('for each compact f literal Tf graph pair','Tf and grad Tf possess real MemLp and their toLp pair belongs to G.closure.graph; Tf itself need not compact',['A3.SS1.p1.1','A3.E1'])],
 'Construct derivative of actual T on original dense core; ensure canonical G is used at compact and rough stages','EXISTING_OPAQUE_PROVIDER; no prior verification verdict read')
provider('actual_macroscopic_l2_mean',[
 ('mu,J,nu probabilities','Actual normalized mu and forward independent-Gaussian joint/marginal',['S2.E6','S2.E7']),
 ('S Markov every-y literal, Λ disintegration and both marginals nu','Λ is pair(Y+,Y-); IsCondKernel means nu ⊗ S=Λ; both marginals same nu, not unrelated kernel',['A2.E8','A2.E9','A3.Ex1']),
 ('U pullback involutive selfadjoint isometry','Actual reflection F(x,y)=(x,2x-y), encoded J-AE; no supplied abstract reflection',['A2.E4','A2.E5']),
 ('M actual macro isometric embedding; P M u=M u','M u(x,y)=u(y) J-AE; P genuine conditional expectation projection; actual macro subspace',['A2.E1','A2.E2']),
 ('T fixed bounded mean and A representation/contraction','A=PUP and M(Tu)=A(Mu), ||Tu||≤||u||',['A2.E9']),
 ('rough AE means and fiber first/squared integrability','Canonical u representative may be substituted only through AE-preserving disintegration; all claims on nu-AE fibers',['A2.E9']),
 ('integrable variance, microscopic energy and norm-defect equality','variance S_y u=integral(u-integral u)²; ∫variance=||B(Mu)||²=||u||²-||Tu||², B=(I-P)UP',['A2.E9','A2.E5'])],
 'Identify smooth Tf with same T input class, remove microscopic intermediate from sharp50 using actual defect, and retain all rough-law conclusions','PROVED_LOCAL per parent message; independent science source/math accepted; exact-science verifier ACTIVE; NOT VERIFIED')
provider('actual_macroscopic_gradient_energy_blocks',[
 ('R,S genuine conditional kernels','R is actual X|Y, S_y=(R_y).map(x↦2x-y), every-y explicit tilt, Λ.IsCondKernel S',['S2.E8','A3.Ex1']),
 ('U and P actual reflection/projection and blocks','U actual J-AE pullback; A=PUP, B=(I-P)UP, D=(I-P)U(I-P), starB B=P-A²; do not construct Gamma from these words',['A2.E1','A2.E3','A2.E4','A2.E5']),
 ('compact f differentiability and scalar/vector MemLp','Compact smooth input; literal Tf differentiable, f/Tf/gradTf square integrable. No compactness conclusion for Tf',['A3.E1','A3.EGx25']),
 ('compact macro g representatives and norm integrals','g=f(y) J-AE, Pg=g, Ag=Tf(y) J-AE, ||g||²=∫f²dnu and ||Ag||²=∫Tf²dnu; compare to55 actual M,T via AE uniqueness',['A2.E9','A3.EGx25']),
 ('sharp energy against compact variance','∫Var S_y f=||Bg||² and eta∫||gradTf||²≤c||Bg||²; exact c source C.2, no public smooth-energy binder',['A3.EGx25'])],
 'Supply core sharp bound after identifying identical literal kernels/projection/representation; all normalization/regularity estimates are internal source edges','EXISTING_OPAQUE_PROVIDER; no prior verification verdict read')
save('opaque-provider-semantic-expansion56.json',{'rows':provider_rows,'proof_body_expansion':'NOT PERFORMED; mathematically deep internal routes remain opaque contracts','caller_symbol_provenance':'Exact existing declaration name + source physical header range + source source-use anchor, not import adjacency','unresolved_count':0})
routes=[
 ('same-law','Use actual55 to obtain one T with actual nu, literal S, contraction, AE fiber moments and norm defect.','A2.E9',['provider55']),
 ('core-gradient','Use actual54 one genuine dense compact-gradient G. On its true domain each compact phi has literal Tphi closure-gradient pair; representative/kernel equality identifies it with T applied to input class. Closed graph uniqueness makes this gradient independent of phi.','A3.SS1.p1.1',['provider54','provider55','external:AE-disintegration']),
 ('core-linear-bound','Use uniqueness and linear graph to form a linear derivative map D on G.domain. Compact50 plus55 actual variance/norm matching yields eta||D v||²≤c(||v||²-||T v||²)≤c||v||². eta>0 gives a genuine uniform norm bound; no graph/certificate public binder.','A3.EGx25',['provider50','provider54','provider55','external:partial-linear-graph']),
 ('bounded-extension','Extend D from dense G.domain inclusion to one continuous real linear K on scalar Lp2 with values in complete vector Lp2. extendOfNorm, extendOfNorm_eq and norm_extendOfNorm_apply_le are opaque Mathlib candidate contracts with genuine dense and norm-bound obligations.','A3.SS1.p1.1',['external:bounded-extension','external:Lp-completeness']),
 ('closed-graph','For all input u use density and continuity of u↦(T u,K u). The preimage of G.closure.graph is closed, contains true dense G.domain, hence all scalar Lp2. No particular convergence sequence is required from caller.','A3.SS1.p1.1',['provider54','route56:bounded-extension','external:dense-closed-property']),
 ('sharp-energy','The inequality eta||Ku||²≤c(||u||²-||Tu||²) defines a closed property because T,K continuous and squared norms continuous. It holds on dense true core by exact50/55 so holds everywhere.','A3.EGx25',['route56:core-linear-bound','route56:bounded-extension','external:dense-closed-property']),
 ('source-cap','From alpha>0, alpha<=beta, eta>0, beta eta<=1 derive0<alpha eta<=1, c≤1/4 and coarse source4eta bound. No inverse1-alpha eta or dimension factor is needed.','A3.SS1.p3.7',['route56:sharp-energy','pbps:standing-curvature'])]
extra=[]
def boundary(id,semantics,source_anchors,context):extra.append({'id':id,'kind':'TYPED_DEEP_OPAQUE_BOUNDARY','mathematics':semantics,'source_anchors':source_anchors,'lexical_context':context,'admission':'SEMANTICS_BOUNDARY_ONLY_NOT_COMPILED_OR_REVIEWED_HERE'})
boundary('external:AE-disintegration','Disintegration and nu-AE substitution imply S_y-AE substitution for nu-a.e. y; Lp coercion operations are only AE. For compact phi and canonical u, derive actual mean equality by disintegration and then Lp class equality.',['A2.E9'],'disintegration; Lp; provider55')
boundary('external:partial-linear-graph','Partial linear map graph has unique output for a fixed input, is a submodule closed under add/smul, closure is an actual partial linear map once closability supplied; zero-fallback semantics cannot be used.',['A3.SS1.p1.1'],'partial-linear-graph; closed-gradient; provider54')
boundary('external:Lp-completeness','Lp2 scalar/vector are complete normed real modules. Finite-dimensional E completeness follows from real completeness; not an extra source assumption.',['A3.SS1.p1.1'],'Lp; finite-dimensional typing')
boundary('external:bounded-extension','Given f core-linear into complete F, dense inclusion e and uniform ||f x||≤C||e x||, bounded extension is equal to f on core and obeys same norm bound. Candidate API is support for unnamed density passage, not an author citation.',['A3.SS1.p1.1'],'bounded-extension ranges178-190,194-196,201-203')
boundary('external:dense-closed-property','Closed preimage under continuous pair-map or continuous scalar norm expressions, containing dense subset, is whole space. Both graph identification and sharp energy require their own closed property.',['A3.SS1.p1.1'],'external general topology boundary; no compilation or proof implementation read')
boundary('external:normalized-differentiation','Differentiation of normalized actual conditional density requires finite positive normalization and domination/score moments; all are source proof ingredients retained behind compact50.',['A3.Ex1','A3.Ex2','A3.E1'],'OPAQUE provider50 and source formula')
boundary('external:weighted-poincare-domain','Conditional Poincare extends to unbounded score with square integrability; covariance CS and vector duality apply on actual conditional law. Source curvature controls it, not a caller premise.',['A3.EGx24','A3.Ex5','A3.Ex6','A3.Ex7'],'OPAQUE provider50 and D.6')
graph={'schema_version':1,'kind':'SOURCE_PROOF_GRAPH_CREATOR56','status':'CREATOR_COMPLETE_PENDING_INDEPENDENT_TOPOLOGY_REVIEW','target':statement,'primary_first_freeze':freeze,'read_isolation_limitation':limitation,'source_nodes':source['nodes']+extra,'source_edges':source['edges'],'unnamed_source_step_refinement':[{'id':'route56:'+id,'mathematics':math,'consumer_use_site':site,'required_inputs':parents,'semantics':'SOURCE_DENSITY_CLOSEDNESS_STEP_REALIZATION; ingredients are edges, not public binders'} for id,math,site,parents in routes],'opaque_provider_binding':'opaque-provider-semantic-expansion56.json','binder_expansion':'target-binder-semantic-expansion56.json','physical_source_inventory':'primary-source-anchor-inventory.json','coverage':{'source_inventory_items':len(inventory['inventory']),'dispositions':['NODE','EXCLUDED_WITH_EXPLICIT_SCOPE_REASON','TYPED_DEEP_OPAQUE_BOUNDARY'],'unresolved':0,'independent_review':'PENDING','zero_unresolved_does_not_mean_deep_proof_completed':True},'truth_separation':{'Lean_dependency_graph':False,'author_source_graph':'original source topology retained; Mathlib realization bindings separately labeled','compiled_target56':False,'provider55':'PROVED_LOCAL, exact verifier active, NOT VERIFIED'},'boundaries_open':['separately defined weak-H1 equivalence','Gamma_P and microscopic block norm identity for complete B.13','B.14/B.15 spectral conclusions','half-turn/hypocoercivity','dynamics/nonexplosion/implementation/errors/caps/main/cost','PBPS-SPHMC actual-input composition','four-paper completion']}
save('sourceproofgraph56.json',graph)
save('endpoint-and-definition-audit56.json',{
 'rank0':'Finite-dimensional Hilbert extension includes zero-dimensional E. Gaussian is empty-coordinate product mapped to singleton. volume/tilts must still have actual probability from opaque providers. Vector Lp is zero; K=0 follows target typing, no nonzero dimension source premise.',
 'alpha_eta_one':'Sharp c=0; eta>0 forces ||Ku||=0. Do not divide by1-alpha eta or assume strict cap.',
 'noncompact_mean':'Smooth compact input phi does not imply compact Tf. Use G.closure.graph from54, never apply original G graph iff to Tf.',
 'every_y_vs_AE':'S literal every-y normalized kernel; rough u first/squared fiber integrability and integral representative identity only nu-AE. Kernel uniqueness from disintegration only AE; literal equality supplied from producers identifies the selected kernel globally.',
 'Lp_difference':'Canonical representative (u-v)(x) is not definitionally u(x)-v(x); difference substitutions require nu-AE equality and actual disintegration to fibers, hence no pointwise subtraction shortcut.',
 'totalized_definitions':'Tilted laws and Bochner integrals have off-domain totalized semantics. Producer probability and actual AE integrability exclude those fallbacks at advertised source uses. gradient phi legitimate on compact smooth core; K rough output is not classical derivative of arbitrary canonical representative.',
 'original_compact_gradient_closure':'G core graph iff actual compact gradients; G.IsClosable ensures closure is real graph closure despite Mathlib if-not-closable fallback; arbitrary weak-H1 convention identification is OPEN.',
 'constant':'c=(1-alpha eta)^2/(4*(1+alpha eta)); fixed exact coefficient, all norms on same nu; denominator positive from alpha eta>0.',
 'unresolved_count':0,'status':'CREATOR_AUDIT_PENDING_INDEPENDENT_REVIEW'})
save('creator-complete56.json',{'schema_version':1,'creator':'/root/sourcegraph_creator56','status':'COMPLETE_PENDING_INDEPENDENT_SOURCE_TOPOLOGY_REVIEW','utc':utc(),'target_lf_bytes':1755,'target_lf_sha256':statement['lf_sha256'],'primary_first_freeze_raw_sha256':freeze['raw_sha256'],'plan_steps':len(routes),'binder_rows':len(rows),'provider_clause_rows':len(provider_rows),'source_nodes':len(graph['source_nodes']),'source_inventory_items':len(inventory['inventory']),'unresolved':0,'body_exposure_limitation':'read-isolation-and-chronology56.json','compiler':'NOT_STARTED_CLOSED','target_implementation_seen':False,'canonical_mutations':False,'reviewer_instructions':'Independently re-read raw primary/target/header contracts. Creator source topology is not self-approved. Incidental initial provider call sites and Lp typing-field range are disclosed; no proof transcript or prior verdict is input.'})
print(json.dumps({'creator_graph':'sourceproofgraph56.json','source_nodes':len(graph['source_nodes']),'binder_rows':len(rows),'provider_clause_rows':len(provider_rows),'plan_steps':len(routes),'unresolved':0,'status':'PENDING_INDEPENDENT_REVIEW'}))
