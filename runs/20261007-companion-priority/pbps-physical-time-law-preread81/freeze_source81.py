from pathlib import Path
import json,hashlib,datetime
from primary_only81 import SRC,tree
OWN=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj):
 p=OWN/name;p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return p
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
ids={n.attrs.get('id','') for n in tree.elements}
items=[]
def item(anchor,status,role):
 assert anchor in ids,anchor
 items.append({'source_id':anchor,'scope':status,'source_role':role})
item('license-tr','PROVENANCE','arXiv.org perpetual non-exclusive license. Private paraphrases/minimal identifying formulas only; no new full primary-source duplicate.')
item('S1.p1','STANDING','V in C2(R^d), target exp(-V), positive alpha<=beta. Target law is context, not automatically invariant for a new kernel.')
item('S1.E1','STANDING','Global Hessian sandwich alpha I<=Hess V<=beta I, 0<alpha<=beta.')
item('S2.SS2.p1.1','STANDING','eta in(0,1/beta]; six formal analytic binders alpha>0,alpha<=beta,C2,Hessian sandwich,eta>0,beta*eta<=1 preserve this exact source context.')
item('S2.E4','INCLUDED_LITERAL','Reflection R_h and R_0=I; zero normal is identity, not undefined or continuous-bounce premise.')
item('S2.E6','CONTEXT_OPEN_CONDITIONAL_DISTRIBUTION','Augmented law pi_eta(dx,dy) proportional exp(-V(x)-||x-y||^2/(2eta)) dxdy. Normalization/probability realization is needed before claiming actual conditional-reference input.')
item('S2.E7','CONTEXT_OPEN_RANDOM_INITIALIZATION','X~mu and independent standard Gaussian Z, Y=X+sqrt(eta)Z. This is augmentation law, not iid clock input or arbitrary correlated initialization.')
item('S2.E8','CONTEXT_OPEN_CONDITIONAL_DISTRIBUTION','Y|X=x Gaussian(x,eta I); X|Y=y density proportional exp(-V(r)-||r-y||^2/(2eta)). The actual reference law depends on y, not x.')
item('S3.SS1.SSS0.Px3.p1.1','CONTEXT_OPEN_RANDOM_INITIALIZATION','Run starts at position x and independent p0~N(0,I). Momentum discarded on output; source state memory is in X,Y.')
item('S3.SS2.p1.1','CONTEXT_OPEN_CONDITIONAL_DISTRIBUTION','Conditional potential V_y(r)=V(r)+||r-y||^2/(2eta).')
item('S3.Ex5','CONTEXT_OPEN_CONDITIONAL_DISTRIBUTION','Exact density of conditional position law, proportional exp(-V_y).')
item('S3.E1','CONTEXT_OPEN_INVARIANCE','nu_eta,y=pi_eta^(X|Y=y) tensor standard Gaussian momentum. This is named proposed stationary phase law, not a conclusion of mere kernel construction.')
item('S3.SS2.p4.1','CONTEXT_RANDOM_REFERENCE','Draw localized conditional reference independently; source independence must be represented by product/conditional law, never by plugging arbitrary sample-correlated parameters into fixedparam AE statements.')
item('S3.SS2.p4.2','INCLUDED_FIXED_REFERENCE','Condition on reference r; deterministic center and residual maps then use r fixed throughout one run.')
item('S3.E4','INCLUDED_LITERAL','c=y-eta gradV(r), h_r(x)=gradV(x)-gradV(r).')
item('S3.E5','EXCLUDED_OPEN_GENERATOR','Generator is full deterministic plus jump operator; identifying actual kernel as solution of generator/martingale problem is separate.')
item('S3.SS2.p6.1','CONTEXT_CONSUMER','Actual Algorithm1 evolves to pi and returns position only. A physical-time phase probability law is a necessary integration consumer, but not yet full returned-position kernel.')
for n,role in [
 (1,'Input position/auxiliary state (x,y).'),
 (2,'Reference r~pi_eta^(X|Y=y) and p0~standard Gaussian independently. Clock randomness is fresh independent sampling randomness for canonical realization, implicit beyond these two named draws.'),
 (3,'Gradient query/cache action, costs EXCLUDED.'),
 (4,'Position initializes x0=x; full phase z0=(x,p0).'),
 (5,'Actual harmonic ODE at finite times until pi.'),
 (6,'Actual residual-gradient rate controls events.'),
 (7,'Finite event owns postbounce phase R_h p.'),
 (8,'Output x_pi. Actual output law requires averaging reference, momentum and event-clock randomness.')]:item(f'alg1.l{n}','EXCLUDED_OPEN_COST' if n==3 else 'INCLUDED_OR_CONTEXT_BY_CLAUSE',role)
item('S3.E8','INCLUDED_LITERAL','Actual ODE scaling sqrt eta and inverse sqrt eta.')
item('S3.E9','INCLUDED_LITERAL','Actual rate sqrt eta positive-part momentum dot gradient residual.')
item('S3.Thmtheorem1.p1.1','PARTIAL_ONLY_OTHER_CLAUSES_OPEN','For each fixed y,r,z0 source unique nonexplosive time-homogeneous Markov process; nu_eta,y stationary and x_pi well-defined a.s. Current next edge may build actual physical one-time laws/kernel/init only. Markov/global uniqueness/invariance remain OPEN.')
item('S3.Thmtheorem2.p1.1','CONTEXT_LAW_ONLY_REVERSIBILITY_OPEN','H_y(x,.) is law of returned position Algorithm1. Reversibility wrt pi conditional is separate OPEN claim.')
for a,role in [
 ('A1.SS1.p1.1','Fix y,r and actual rate notation.'),('A1.Ex1','Literal nonnegative rate.'),
 ('A1.SS1.p1.2','Actual flow/bounce definitions.'),('A1.Ex2','Literal finite harmonic Phi and Phi0=id.'),
 ('A1.Ex3','Zero-safe bounce R0=I.'),('A1.SS1.p1.3','Possible bounce discontinuity; involution Borel only, rate vanishes at zero normal.'),
 ('A1.SS1.p2.1','Independent Exp1 variables E_j,j>=1; initial zeta0=z0 and T0=0. E_(n+1) drives step n.'),
 ('A1.E1','Wait inf nonnegative integrated-hazard threshold >=E_(n+1). Empty-hit infinity; measurable dependence must be derived.'),
 ('A1.E2','Finite update T_next=T+S and z_next=S_bounce(Phi_S(z)); applies only finite S.'),
 ('A1.SS1.p2.2','Finite qualifier; empty-hit top and stop; half-open arcs zeta_(T_n+u)=Phi_u(zeta_Tn) for0<=u<S_next. Infinite next wait leaves final current live arc at every finite offset.')]:item(a,'INCLUDED_LITERAL',role)
for a in ['A1.SS1.p3.1','A1.Ex4','A1.SS1.p3.2','A1.Ex5','A1.SS1.p3.3','A1.Ex6','A1.SS1.p3.4','A1.Ex7','A1.SS1.p3.5','A1.Ex8','A1.SS1.p3.6','A1.Ex9']:
 item(a,'PARENT_NONACCUMULATION_SOURCE','Exact source energy/layer/cap/hazard/wait/sum ingredient. Positive cap finite wait bound differs from zero cap no jumps; stopping differs from continuing. No energy/cap certificate may become a new public source premise.')
item('A1.SS1.p3.7','PARTIAL_NONACCUMULATION_MARKOV_OPEN','Source direct Exp mean1 SLLN implies nonaccumulation and all finite-time construction. Alternative sufficient SLLN routes must be labelled. Source memoryless=>Markov and Davis identification remain separate OPEN, not consequences of pushforward kernel.')
item('A1.Thmtheorem1.p1.1','EXCLUDED_OPEN_TRANSITION_OPERATOR_IDENTIFICATION','T_t are Markov transition operators of the constructed source process. A physical one-time probability kernel is substrate, not yet this complete Markov/semigroup identification.')
item('A1.E3','EXCLUDED_OPEN_REVERSAL','Momentum-reversed L2 adjoint identity is separate OPEN proof.')
item('A1.I1.i2.p1.1','EXCLUDED_OPEN_SEMIGROUP','Strongly continuous L2 contraction semigroup is not implied by a jointly measurable one-time kernel.')
item('A1.E7','EXCLUDED_OPEN_PATH_DENSITY','Ordered event-time path expansion with survival and jump-rate factors requires separate derivation; actual input kernel may later be its consumer.')
item('A1.SS1.SSS0.Px1.p4.4','BACKGROUND_BOREL_ONLY_OTHER_CLAUSES_OPEN','Borel bounce and affine flow finite composition useful regularity. Measure-preserving inverse/reversal/Jacobian/invariance package remains OPEN.')
item('A1.SS2.p1.1','CONTEXT_GAUSSIAN_REFERENCE_AVERAGE','Fixed-reference time-pi position law/averaging over independent reference; self-adjoint/Markov contraction clauses require source A1 process facts, not merely kernel mass1.')
item('A1.Ex24','CONTEXT_EXACT_DOWNSTREAM_LAW_FORMULA','H_y average over r~pi conditional of Gaussian momentum averaged fixed-reference time-pi phase operator. Actual law identity is a downstream consumer.')
item('A1.SS2.p2.1','CONTEXT_JOINT_KERNEL_MEASURABILITY','Each fixed-y reversibility differs from joint y,x measurability needed on augmented space.')
item('A1.Thmtheorem2.p1.1','PARTIAL_JOINT_KERNEL_ONLY_L2_OPEN','H_y admits version Borel in(y,x) at each Borel set; subsequent augmented L2 self-adjoint contraction separately OPEN.')
item('A1.SS2.p3.1','INCLUDED_SOURCE_EXPLICIT_MEASURABLE_ADAPTER','Joint Borel maps/hazard/recursion and a.s. finite terminal-state limit give Borel version, source chooses zero on nonexistence. Other measurable exceptional convention yields same fixedparam law if proved AE equal, and same independent mixture via Fubini.')
item('A1.SS2.p4.1','INCLUDED_SOURCE_EXPLICIT_LAW_CONSUMER','Joint Borel conditional density and integration of indicator{x_pi in A} against reference, Gaussian momentum and independent event-clock laws gives Borel(y,x)->H_y(x,A). This is exact actual-source reason beyond supplied map measurability.')
item('A1.SS2.p5.1','EXCLUDED_OPEN_L2_CONTRACTION','Integration of conditional contraction requires already established invariance/Markov operator facts.')
item('A1.SS2.p5.2','EXCLUDED_OPEN_L2_SELFADJOINT','Fubini of proved conditional self-adjointness does not establish it from scratch; positivity/unit-preserving kernel alone insufficient.')
exclusions=['Memoryless Markov or strong Markov property; filtrations/adaptedness/stoppingtimes','Semigroup/Chapman-Kolmogorov/restart at deterministic or stopping times','Uniqueness of the full process law/path regularity or martingale/generator characterization','Stationarity/invariance/reversibility/L2 adjoint or contraction/strong continuity','Ordered event density/path expansion A.7','Full Algorithm1 conditional/Gaussian input realization until those exact measures/kernels are constructed','Augmented mixture/reflection composition, convergence/hypocoercivity/numerical error/expected queries/full Goal','Any proof/compiled/VERIFIED/completion credit from this source-only preread']
inventory={
 'schema':'independent-source-first-prospective-preread-v1','created_utc':now,
 'source':{'arxiv':'2609.06905v1','authors':['Fan Chen','Sinho Chewi','Jianfeng Lu','Matthew S. Zhang'],'primary_path':str(SRC),'raw_sha256':sha(SRC),'license':'arXiv.org perpetual non-exclusive license','parser':'Fresh standalone stdlib html.parser and math alttext; no prior extractor imported'},
 'independence':{'primary_read_first':True,'source_only':True,'no_proposed81_lean_or_header_or_lesson_or_review_seen':True,'no80_implementation_or_old_verdicts_reopened':True,'no_production_shared_ledger_cell_site_writes':True,'necessary_same_source_background_A2_explicit_law_integration_read':True},
 'analytic_binders':['Finite Euclidean R^d, possible intrinsic finite-dimensional real inner-product Borel equivalent; rank0 not silently excluded.','V C2;alpha>0;alpha<=beta;global Hessian sandwich;eta>0;beta*eta<=1. Exactly six analytic source conditions; no added higher smoothness.','Fixed deterministic y,r,z0 for source conditional path. Actual P is iid rate1 Exp countable product, index0 realizes source E1.','Finite nonnegative t and stored live time; possible top waits/events; no physical phase at infinity.','Any arbitrary initial probability measure belongs to a separately labelled independent-input mixture elaboration, never replaces source actual conditional/Gaussian law.'],
 'literal_objects':{'phase':'z=(x,p)','center':'c=y-eta gradV(r)','residual':'h_r(x)=gradV(x)-gradV(r)','flow':'Phi_u(z)=(c+cos(u)(x-c)+sqrt(eta)sin(u)p, -sin(u)(x-c)/sqrt(eta)+cos(u)p)','bounce':'S_r(x,p)=(x,R_h p),R0=I','rate':'sqrt(eta) max(0,<p,h_r(x)>)','thresholds':'iid E_j~Exp1,j>=1','recurrence':'Wait S_(n+1)=inf{u>=0:integral_0^u rate(Phi_s(z_Tn))ds>=E_(n+1)}; if finite next T adds S and postphase=S_bounce(Phi_S); otherwise next T,S=top and stop.','interpolation':'For0<=u<S_next, source zeta_(Tn+u)=Phi_u(zeta_Tn); right endpoint belongs to next postbounce live record.','conditional_reference':'pi_eta^(X|Y=y)(dr) proportional exp(-V(r)-||r-y||^2/(2eta)) dr','momentum':'gamma=N(0,I),independent of reference; source clock randomness represented fresh independent of initialization in product construction.','actual_return_law':'H_y(x,A)=integral 1_A(pr_x Z(y,r,(x,p),pi,omega)) pi_eta^(X|Y=y)(dr) gamma(dp) P(domega), after exact normalization/measurability/independence established.'},
 'scope_coverage':items,'excluded_open':exclusions,
 'semantic_boundaries':['Probability kernel means measurable parameter-indexed probability measures; it does not establish Markov conditional law of a path.','One-time K_t laws plus K0=dirac do not establish K_(s+t)=K_s K_t. Restart/memoryless identification is separate.','Fixedparam AE all finite t cannot be substituted at arbitrary sample-correlated randomparams. Independent initialization uses product measure/Fubini and measurability of relevant good relation.','For a fixed finite t, good relation can be built from countable measurable record/interval events. Simultaneous all-time product AE requires countable rational-horizon nonaccumulation/positivity encoding or equivalent measurable good domain; uncountable forall t is not automatically Borel.','A measurable representative may use zero (source A2) or z0 (an explicit ASTIS convention); laws are representative-independent only after AE agreement for fixed parameters, then independent mixtures via Fubini.','Last infinite wait remains covered by current live arc. Stopped next record has no phase; any stopped dummy cannot be used as actual state.','rank0 has zero rate, first positive wait top and degenerate deterministic phase; zero thresholds are exceptional total extension, not actual positive Exp inputs.']
}
write('source_inventory81.json',inventory)
node_specs=[
 ('G81-01','Original analytic conditions and finite-dimensional Borel carrier',['S1.E1','S2.SS2.p1.1'],'SOURCE_STANDING'),
 ('G81-02','Actual normalized conditional reference probability kernel q_y(dr) with source density, jointly measurable in y',['S2.E8','S3.Ex5','A1.SS2.p4.1'],'SOURCE_EXPLICIT_DISTRIBUTION_WITH_NORMALIZATION_OBLIGATION'),
 ('G81-03','Actual standard Gaussian momentum gamma, including rank0 Dirac case',['alg1.l2','S3.E1'],'SOURCE_EXPLICIT_INPUT'),
 ('G81-04','Actual countable iid Exp1 product P, positive support, source E_(n+1) indexing',['A1.SS1.p2.1'],'SOURCE_EXPLICIT_INPUT'),
 ('G81-05','Actual Phi/S/rate/Lambda/tau, Borel dependence, finite guards and zero-normal convention',['A1.Ex1','A1.Ex2','A1.Ex3','A1.E1'],'SOURCE_EXPLICIT_DYNAMICS_MEASURABILITY_ELABORATION'),
 ('G81-06','Actual initialized stopped finite records and jointly measurable event times',['A1.E2','A1.SS1.p2.1','A1.SS1.p2.2','A1.SS2.p3.1'],'SOURCE_RECURSION_INGREDIENT'),
 ('G81-07','Actual nonaccumulation, finite-time half-open cover and last live infinite-wait tail',['A1.Ex4','A1.Ex9','A1.SS1.p3.7','A1.SS1.p2.2'],'SOURCE_NONACCUMULATION_INGREDIENT'),
 ('G81-08','Jointly Borel actual physical phase representative with per-fixedparams common-AE all finite arcs and physical0 initialization',['A1.SS1.p2.2','A1.SS1.p2.1','A1.SS2.p3.1'],'SOURCE_IMPLICIT_TO_EXPLICIT_REPRESENTATIVE_INGREDIENT'),
 ('G81-09','Literal independent input law M_y=q_y tensor gamma tensor P, initial phase=(x,p), reference fixed during run',['alg1.l2','alg1.l4','A1.SS2.p4.1'],'SOURCE_ACTUAL_INPUT_PRODUCT_INTEGRATION'),
 ('G81-10','Measurable source-good relation and product-measure/Fubini lift of per-fixedparam AE to this independent initialization',['A1.SS1.p3.7','A1.SS2.p3.1','A1.SS2.p4.1'],'SOURCE_IMPLICIT_REQUIRED_INDEPENDENCE_ADAPTER'),
 ('G81-11','Actual returned position map F_(y,x)(r,p,omega)=pr_x Z(y,r,(x,p),pi,omega) jointly Borel',['alg1.l8','S3.Thmtheorem2.p1.1','A1.SS2.p4.1'],'SOURCE_ACTUAL_OUTPUT'),
 ('G81-12','Actual probability kernel H_y(x,A)=integral indicator_A(F) dM_y, jointly Borel in(y,x)',['A1.Thmtheorem2.p1.1','A1.SS2.p4.1'],'BOUNDED_PROPOSED_INTEGRATION_CONSUMER'),
 ('G81-13','Under same M_y, physical phase0 law delta_x tensor gamma and position0 law delta_x, derived source initialization',['alg1.l4','A1.SS1.p2.1'],'BOUNDED_PROPOSED_INIT_LAW_CONSUMER'),
 ('G81-14','H_y equals actual Algorithm1 returned law; representative independence via AE actual source arcs and independent input',['alg1.l2','alg1.l8','S3.Thmtheorem2.p1.1','A1.Ex24'],'BOUNDED_PROPOSED_SOURCE_LAW_IDENTIFICATION'),
 ('G81-15','Markov conditional path/restart, semigroup, stationary/reversible/L2/cost/composition package',['S3.Thmtheorem1.p1.1','A1.Thmtheorem1.p1.1','A1.E3','A1.I1.i2.p1.1','S3.Thmtheorem2.p1.1'],'EXCLUDED_OPEN_NOT_KERNEL_IMPLICATION')
]
nodes=[{'id':i,'obligation':o,'source_ids':a,'classification':c,'status':'OPEN_PROSPECTIVE_SOURCE_ONLY_NOT_PROVED'} for i,o,a,c in node_specs]
edge_specs=[
 (1,2,'Strong convexity/quadratic tail bounds and positivity normalize exact conditional density; measurable density normalization derives actual q_y kernel.'),
 (1,5,'C2 gives continuous gradient; actual Phi/rate continuous and bounce Borel, not blanket bounce continuity.'),
 (2,9,'Actual reference distribution, not arbitrary supplied law.'),(3,9,'Actual Gaussian independent momentum law.'),(4,9,'Actual iid clocks independent of initialization in literal product.'),
 (5,6,'Joint Borel clock/flow/bounce plus finite guard derive actual measurable finite records.'),(4,6,'Threshold coordinate n realizes source E_(n+1).'),
 (6,7,'Energy-preserving guarded records and stop absorption.'),(4,7,'Source Exp sum divergence/positive support; source direct mean1 SLLN distinct from sufficient alternatives.'),(5,7,'Energy/cap bounds give nonaccumulation, zero/positive cap separate.'),
 (6,8,'Joint Borel finite records/times permit countable interval selection or bounded-jump limit.'),(7,8,'Actual finite cover supports source arcs and final infinite-wait live interval.'),(5,8,'Finite actual Phi evaluation and Phi0 identity.'),
 (6,10,'Countable measurable rational-horizon escape/live conditions can encode good relation; do not assume uncountable forall t event automatically measurable.'),(7,10,'Each fixed initialization has full-measure good section.'),(8,10,'Source arc agreement and init on each good section.'),(9,10,'Fubini uses literal independent product law, not arbitrary correlated substitution.'),
 (8,11,'Compose joint physical phase with finite pi and initial phase=(x,p), then position projection.'),
 (9,12,'Integrate actual returned indicator against real q_y,gamma,P product; mass1 and joint kernel measurability.'),(11,12,'Measurable actual output, not abstract supplied observable.'),(2,12,'Parameter y dependence of actual reference kernel must enter joint Borel proof.'),
 (8,13,'Physical0 initialization is derived, not assumed.'),(9,13,'Initial position fixed x, actual Gaussian p and independent r/clocks give phase0 law.'),(10,13,'Product-AE init after legitimate Fubini lift; no uniformparams AE.'),
 (10,14,'Actual source agreement under exact product initialization.'),(11,14,'Position output at pi matches Algorithm1 endpoint.'),(12,14,'Actual pushforward probability kernel represents that output law.'),(13,14,'Correct phase initialization anchors actual algorithm law.'),
 (12,15,'Future substrate only: actual probability kernel alone does not imply Markov/restart/semigroup/invariance/reversibility/cost.')
]
edges=[{'ingredient':f'G81-{a:02d}','consumer':f'G81-{b:02d}','reason':reason,'kind':'future-substrate-not-implication' if b==15 else 'planned-source-proof-ingredient','status':'OPEN_PROSPECTIVE_NOT_COMPILED'} for a,b,reason in edge_specs]
graph={'schema':'independent-source-proof-graph-prospective-v1','created_utc':now,'source_raw_sha256':sha(SRC),'candidate_lean_seen':False,'truth_contract':'Independent source topology, not formal DAG truth; every mathematical status is prospective/OPEN. No theorem/source-review/verifier credit.','nodes':nodes,'edges':edges,'coverage_item_count':len(items),'all_source_ids_validated_in_fresh_primary_parser':True,'exclusions':exclusions}
write('source_proof_graph81.json',graph)
candidate={
 'schema':'bounded-prospective-source-candidate-v1','created_utc':now,
 'candidate':'Actual Algorithm1 independent-initialization and returned-position probability kernel',
 'source_reason':'A1.SS2.p3.1-p4.1 explicitly integrates Borel actual terminal position against conditional reference, Gaussian momentum and exponential clocks to obtain jointly Borel H_y(x,A). Algorithm1 lines2,4,8 and Proposition3.2 define the actual returned law. This consumes physical realization beyond mere measurability.',
 'minimal_proposed_statement':[
  'Under exactly the original six analytic conditions and source carrier, define q_y by normalized source2.8 density, gamma=standard Gaussian and P=actual countable Exp1 product. No supplied process/map/kernel/measurability/independence certificates.',
  'Consume the actual physical-phase realization internally, fixing V,alpha,beta,eta. For arbitrary fixed input(x,y), use literal product M_y=q_y(dr) gamma(dp) P(domega), z0=(x,p), with r fixed during each run.',
  'Define H_y(x,A)=integral indicator_A(pr_position Z(y,r,(x,p),pi,omega)) dM_y. Prove probability mass1 and Borel(y,x)->H_y(x,A) for every Borel A, equivalently one probability-kernel object on input(y,x).',
  'Under this exact M_y, derive physical initialization Z(y,r,(x,p),0,omega)=(x,p) AE, so phase0 law=delta_x tensor gamma and position0 law=delta_x. Do not add initialization as premise.',
  'Prove this exact independent-input terminal law is source Algorithm1 returned position law using actual good-path agreement lifted by measurable-section/Fubini reasoning. Different explicit measurable exceptional versions agree in output law.',
  'No invariant law, generator identification, Markov path property, time-semigroup, reversibility, L2 contraction or cost assertion.'
 ],
 'why_not_wrapper_churn':'Construct actual initialized output probability kernel with source-specific independent product randomness and derived initialization law, consuming actual joint physical realization and exact normalized conditional/Gaussian laws. An abstract theorem map(mu,f) with supplied measurable f, or fixedparam pushforward alone, is insufficient for this candidate.',
 'independence_contract':['For each fixed input(x,y), r,p,omega have product law q_y tensor gamma tensor P.','q_y depends on y only; reference is independent of fixed x and Gaussian p, and event clocks are fresh independent of both.','The full stationary cost premise x0|Y~q_Y and reference independent of x0 conditionalY is a different source statement; do not require it for H_y at arbitrary x.','An arbitrary sample-correlated r,p,y,x cannot be substituted into fixedparam AE agreement. Conditional/independent law disintegration is required when input y itself random.'],
 'source_vs_adapter':['Actual independent reference/momentum laws and returned-position indicator integration are explicit Algorithm1/A1.SS2.p4.1 source facts.','Product construction including fresh clocks, kernel typing, measurable good relation, Fubini lift and representative independence are required precise mathematical elaborations.','Source A2 chooses zero where terminal limit fails; another explicit Borel exception value preserves source law only after AE agreement.'],
 'smallest_consumer_output':'One actual returned-position probability kernel H with derived same-input physical initialization law. Fixed-reference phase one-time laws may be internal ingredients, not a standalone wrapper SAU.',
 'rank_zero_and_stopping':['No positive dimension. On zero-dimensional E standard Gaussian/conditional position law are Dirac at unique point; actual rate0, positive first threshold gives infinite wait and live harmonic arc; output is Dirac.','Zero raw thresholds are totalized exceptional inputs; not actual Exp-positive support. Half-open empty intervals need no source output law credit.','Infinite next wait leaves final live arc at every finite time pi; stopped successor has no phase and no dummy may be used as actual source output.'],
 'api_status':'SOURCE-ONLY: root reported existing kernel/GaussianConditionalKernel/GaussianAugmentation retrieval, but no implementation/API/header inspected here. Exact source density, covariance, normalization, parameter Borel and rank0 compatibility remain required API audit; no availability or proof credit asserted.',
 'blockers':'No mathematical source obstruction identified for this bounded integration consumer. If existing conditional-reference/Gaussian APIs do not construct the literal normalized2.8/gamma kernels, that exact distribution adapter is an internal prerequisite or smaller source-cited blocker; do not replace it with a supplied arbitrary probability law.',
 'open_obligations':exclusions,
 'no_sau_claim_or_proof_or_verdict_or_VERIFIED':True
}
write('bounded_candidate81.json',candidate)
md='''# Independent source-only preread81

The smallest meaningful next consumer is the actual Algorithm1 returned-position probability kernel, with its literal independent conditional-reference, Gaussian-momentum and Exp1-clock input. Source A1.SS2.p3.1-p4.1 explicitly supplies this law-integration reason. A fixed-parameter pushforward of an arbitrary supplied measurable map is insufficient.

For each fixed input (x,y), let q_y be the normalized density in source(2.8), gamma the standard Gaussian and P the actual countable Exp1 product. Under M_y=q_y tensor gamma tensor P, initialize z0=(x,p), hold reference r fixed during the run, and evaluate the actual source physical phase at pi. The proposed output is H_y(x,A)=integral indicator_A(pr_x Z(y,r,(x,p),pi,omega)) dM_y, with probability mass1 and joint Borel dependence on (y,x). Physical initialization must be derived under that same product law, giving phase0 law delta_x tensor gamma, rather than assumed.

Per-fixed-parameter AE validity lifts through independent input using measurable sections and Fubini. It cannot be substituted at arbitrary sample-correlated initialization. Simultaneous all-time product validity needs a measurable countable good-domain construction, e.g. rational-horizon event-time escape plus positive inputs; uncountable forall time is not automatically measurable.

The kernel is an actual one-run output law. It supplies no Markov conditional path law, restart identity, Chapman-Kolmogorov/semigroup, invariant or reversible law, L2 properties, or expected cost. Those source clauses remain OPEN. Momentum/reference refresh means a family of position endpoint laws must not silently be called a semigroup.

All six analytic conditions remain. Rank0 is allowed; first positive clock then has infinite wait and retains the sole live phase arc. Infinite waits retain the current live arc, not a stopped dummy or uncovered default. Zero raw thresholds are exceptional deterministic totalization. The source zero exceptional-version convention and another explicit Borel convention have the same actual output law only after AE/Fubini justification.

No proposed81 implementation/header or old verdict was read. Only the pinned primary and its necessary same-source law-integration background were used. No source mathematical blocker identified; exact current conditional/Gaussian API compatibility is uninspected and must be audited before implementation. This is a source inventory/prospective topology, not a theorem, proof, source-review verdict or verification credit.
'''
(OWN/'source_preread81.md').write_text(md,encoding='utf-8')
ordinary=['primary_only81.py','freeze_source81.py','source_inventory81.json','source_proof_graph81.json','bounded_candidate81.json','source_preread81.md']
seal={'schema':'immutable-source-first-prospective-seal-v1','created_utc':now,'primary_raw_sha256':sha(SRC),'no_candidate81_seen':True,'self_hash_omitted':True,'files':{f:sha(OWN/f) for f in ordinary}}
write('source_freeze81.seal.json',seal)
manifest={'schema':'noncircular-source-only-raw-manifest-v1','created_utc':now,'raw_inputs':[{'path':str(SRC),'raw_sha256':sha(SRC)}],'raw_outputs':[{'path':str(OWN/f),'raw_sha256':sha(OWN/f)} for f in ordinary+['source_freeze81.seal.json']],'self_hash_omitted':True,'no_proof_or_verification_credit':True}
write('source_freeze81.raw-manifest.json',manifest)
print('inventory',len(items),'nodes',len(nodes),'edges',len(edges))
for f in ordinary+['source_freeze81.seal.json','source_freeze81.raw-manifest.json']:print(f,sha(OWN/f))
