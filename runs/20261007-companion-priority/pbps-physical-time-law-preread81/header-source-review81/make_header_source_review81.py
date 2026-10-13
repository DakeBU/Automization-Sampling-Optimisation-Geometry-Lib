from pathlib import Path
import json,hashlib,datetime
ROOT=Path('E:/Samplinglib')
BASE=ROOT/'runs/20261007-companion-priority/pbps-physical-time-law-preread81'
OWN=Path(__file__).resolve().parent
HEADER=ROOT/'runs/20261007-companion-priority/pbps-actual-physical-time-law81/header81.proposed.lean'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,obj):
 p=OWN/name;p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return p
assert sha(HEADER)=='c3d1ad6107ad0aa812a99461d7dc48720ba83709104f699a908a77a89bec1e76'
complete=BASE/'source_freeze81.complete-raw-manifest.json'
assert sha(complete)=='37eac290b63a76e10cba820d1f29a6e1da7b0f4fbd5ca4041769817993fdaca1'
old=json.loads(complete.read_text(encoding='utf-8'))
for x in old['raw_inputs']+old['raw_outputs']:assert sha(Path(x['path']))==x['raw_sha256'],x['path']
inv=json.loads((BASE/'source_inventory81.json').read_text(encoding='utf-8'))
graph=json.loads((BASE/'source_proof_graph81.json').read_text(encoding='utf-8'))
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
comparisons={
 'objects':{'relation':'source-compatible-explicit-elaboration','finding':'Header20-52 repeats actual Exp1/clamp/center/Phi/reflection/rate/integrated-hazard/finite guarded stopped recursion.53-57 add literal normalized source conditional tilt q_y, standard Gaussian gamma, independent product M_y and finite pi.58-94 constrain a single actual Z and source returned-position kernel H; no arbitrary supplied map/kernel.'},
 'domains':{'relation':'source-compatible-explicit-elaboration','finding':'Finite-dimensional real inner-product Borel E including rank0 preserves Euclidean source formulas. Stored/physical time NNReal finite, event/wait WithTop. Gamma is orthonormal-coordinate standard Gaussian, no rank>0 premise. Input kernel parameter (y,x) explicitly reorders source input(x,y).'},
 'quantifiers':{'relation':'source-compatible-bounded-refinement','finding':'One existential Z chosen before R,H; inherits allsample deterministic covered/fallback rules plus forall fixed y,r,z0 AE clocksample forall finite t/init. Final product claim is forall fixed y,x AE w~M_y jointly initialization0 and live source arc at pi only. No product-AE forall times, no uniform-parameter sample event and no arbitrary correlated initialization substitution.'},
 'assumptions':{'relation':'source-equivalent','finding':'Exactly six original analytic binders: alpha>0,alpha<=beta,C2,Hessian sandwich,eta>0,beta*eta<=1. beta>0 follows, so scale equals eta<=1/beta. q_y probability and joint Borel/kernel construction are conclusions via R, not supplied distribution/measurability/cap/trajectory/independence certificates.'},
 'conclusion':{'relation':'source-compatible-bounded-refinement','finding':'Existence of exact q_y probability kernel R and H:(y,x)->law returned actual position at pi under M_y, plus phase0 law delta_x tensor gamma and common product-AE0/pi source witnesses. Meaningful actual-input integration beyond a map-measurability wrapper. Does not include separately quantified version-independence theorem or full random all-time process law.'},
 'scopes':{'relation':'source-compatible-explicit-elaboration','finding':'q_y is exact ideal conditional reference, not approximate sampler output. IsMarkovKernel only fiber probability. Source A2 zero exceptional version differs from explicit z0 fallback but header promises actual covered arcs; final product AE0/pi removes exceptional influence at used times. Infinite next wait retains live arc, stopped_n cannot have time<=finite pi; no phase at top. Zero clocks remain raw exceptional totalization; positive clock support must derive init.'},
 'constant_dependencies':{'relation':'source-equivalent','finding':'E,V,alpha,beta,eta fixed before Z/R/H; q depends on V,eta,y only, gamma on E, P rate1 constant, M_y product independent of x. H displayed args(y,x); null events may depend on fixed input. pi finite fixed horizon; reflection multiplier2 and eta scale unchanged. No numerical/query/dimension constant added.'}
}
node_notes={
 1:('HEADER_RETAINED_OBLIGATION','Header12-19 exact carrier and six conditions.'),
 2:('HEADER_EXACT_Q_KERNEL_CONCLUSION','Header53-54 is volume.tilted(-V-||r-y||²/(2eta));79 demands probability kernel R with every fiber equal q_y. Tilted totalization cannot hide zero/nonintegrable density because Markov R forces q_y mass1. Proof must derive normalization and equality to actual source conditional law.'),
 3:('HEADER_LITERAL_INPUT','Header55 stdGaussian E: orthonormal-coordinate iid N(0,1), including empty-coordinate rank0 Dirac.'),
 4:('HEADER_LITERAL_INPUT','Header20-21 actual rate1 infinite product and coordinate clamp. Source threshold E_(n+1) is index n; no supplied iid/support premise.'),
 5:('HEADER_LITERAL_OBLIGATION','Header22-45 actual source maps/clock and guarded finite extraction. No bounce continuity, division by positive dimension or unconditional finite waiting.'),
 6:('HEADER_INHERITED_ACTUAL_RECORD_SEMANTICS','Header46-52 initialized finite record recursion/eventTime; source recurrence literal. Measurability itself will be consumed from current parents, not asserted as premise.'),
 7:('HEADER_INHERITED_FIXEDPARAM_SCOPE','Header68-78 retains actual AE allfinite cover/live elapsed/init for each fixed triple. No new nonexplosion premise.'),
 8:('HEADER_INHERITED_ACTUAL80_SEMANTICS','Header58-78 includes joint Borel Z, allsample covered/fallback equations, per-fixedparam AE allfinite source interpolation and init. No new all-product-path claim.'),
 9:('HEADER_LITERAL_INDEPENDENT_PRODUCT','Header56 ((q_y prod gamma) prod P); fixedx enters initialphase(x,p), r held fixed. It encodes exact independent reference/momentum/clocks; q_y not replaced by an arbitrary certificate.'),
 10:('HEADER_REFINED_TO_FINITE_HORIZONS','Header87-94 asks one product-AE event for0 andpi. Measurability requires only countable existence n,a (a can be replaced by measurable record projection) at pi plus measurable initialization equality. Stronger product-good-domain forall finite time variant remains OPEN, not needed.'),
 11:('HEADER_EXACT_ACTUAL_RETURN_MAP','Header81-83 pr1 Z(y,r,(x,p),pi,omega) under exact M_y.'),
 12:('HEADER_ACTUAL_KERNEL_CONCLUSION','Header80-83 H probability kernel with exact fiber pushforward. Kernel structure implies Borel(y,x)->H_y(x,A) for Borel A. No arbitrary supplied measurable output premise.'),
 13:('HEADER_INIT_LAW_CONCLUSION','Header84-89 phase0 pushforward=dirac_x prod gamma and joint M_y-AE physical init withpi source arc. Position0 Dirac is immediate measurable marginal, not separately required public theorem here.'),
 14:('HEADER_SOURCE_LAW_IDENTIFICATION_PARTIAL','Exact actual pushforward plus product-AE source init/pi live witness identifies ideal Algorithm1 returned-position law. Separate theorem comparing all possible Borel versions is deliberately OPEN/deferred; no blocker for this actual chosen representative.'),
 15:('EXCLUDED_OPEN','No path Markov/restart/semigroup, invariant/reversible/L2, implemented sampling producer, numerical or expected-query cost, composition or full source completion clause.')
}
nodes=[]
for i,n in enumerate(graph['nodes'],1):
 st,ev=node_notes[i];nodes.append({'id':n['id'],'source_obligation':n['obligation'],'status':st,'evidence':ev,'proved':False})
edges=[]
for e in graph['edges']:
 a=int(e['ingredient'][-2:]);b=int(e['consumer'][-2:])
 if b==15:status='EXCLUDED_OPEN_FUTURE_SUBSTRATE_NOT_IMPLICATION';note='Retained exclusion; probability H is not proof of Markov path, semigroup or invariance.'
 elif b==10:status='REFINED_HEADER_OBLIGATION_0_AND_PI';note='Source-first stronger simultaneous-product alltime variant is deferred. Current independent-product Fubini bridge targets only init0 and terminalpi on one AE event.'
 elif b==14:status='PARTIAL_HEADER_OBLIGATION_OTHER_VERSION_THEOREM_OPEN';note='Actual chosen representative source law at pi/init is retained. Separate version-uniqueness remains OPEN.'
 else:status='HEADER_OBLIGATION_RETAINED_NOT_PROVED';note=node_notes[b][1]
 edges.append({**e,'header_status':status,'header_evidence':note,'proof_credit':False})
coverage=[]
for item in inv['scope_coverage']:
 st=item['scope'];a=item['source_id']
 if st.startswith('EXCLUDED'):review='EXCLUDED_OPEN';ev='Not part of proposed header; source process/law/cost package remains OPEN.'
 elif a=='license-tr':review='PROVENANCE_RETAINED';ev='Same pinned primary/license; no full-source reproduction.'
 elif a in ['A1.SS1.p3.7','S3.Thmtheorem1.p1.1','S3.Thmtheorem2.p1.1','A1.Thmtheorem2.p1.1']:
  review='PARTIAL_BOUNDED_REFINEMENT';ev='Actual source terminal law/initialization/measurability substrate retained; Markov/fullpath/invariance/reversibility/L2 clauses excluded, separate version uniqueness deferred.'
 elif a in ['A1.SS2.p3.1','A1.SS2.p4.1','A1.Ex24','A1.SS2.p1.1']:
  review='ACTUAL_LAW_CONSUMER_RETAINED';ev='Header exact q_y/gamma/P integration and product-AEpi/init aligns with explicit source ideal kernel construction. No source self-adjoint/Markov process/cost inference.'
 elif st=='CONTEXT_OPEN_INVARIANCE':review='CONTEXT_ONLY_INVARIANCE_OPEN';ev='Named stationary density is context; H invariant/stationary not claimed.'
 else:review='SOURCE_ROLE_RETAINED_AS_HEADER_OR_PARENT_OBLIGATION';ev='Compare literal dynamics/input/initialization at header20-94 and six conditions12-19. No proof of this source ingredient is credited by header review.'
 coverage.append({**item,'header_review':review,'header_evidence':ev})
inputs=[HEADER,complete]+[Path(x['path']) for x in old['raw_inputs']+old['raw_outputs']]+[
 ROOT/'AutoSamplingTheory/TechnicalLemmas/Probability/GaussianConditionalKernel.lean',
 ROOT/'AutoSamplingTheory/ExampleCases/ProximalBPS/GibbsAugmentation.lean',
 ROOT/'.lake/packages/mathlib/Mathlib/MeasureTheory/Measure/Tilted.lean',
 ROOT/'.lake/packages/mathlib/Mathlib/Probability/Distributions/Gaussian/Multivariate.lean',
 ROOT/'.lake/packages/mathlib/Mathlib/Probability/Kernel/Defs.lean']
inputs=list(dict.fromkeys(inputs))
raw_inputs=[{'path':str(x),'raw_sha256':sha(x)} for x in inputs]
result={
 'schema':'independent-header-source-scope-review-v1','created_utc':now,
 'reviewer':'/root/fresh_source78 independent source reviewer81',
 'header_path':str(HEADER),'full_header_raw_sha256':sha(HEADER),'full_header_lines':98,
 'source_raw_sha256':inv['source']['raw_sha256'],
 'source_first_complete_manifest_raw_sha256':sha(complete),
 'independence':{'own_source65items_15nodes_29edges_frozen_before_header':True,'no_math_review_verdict_or_other_reviewer_or_root_adoption_read':True,'entire_literal_header_read':True,'necessary_current_tilted_gaussian_kernel_definitions_audited':True,'original_source_freeze_files_unchanged':True,'only_owned_header_review_directory_written':True},
 'verdict':'source-compatible-with-explicit-bounded-refinement',
 'blocking_deltas':[],'required_mathematical_repairs':[],
 'semantic_comparison':comparisons,
 'scope_refinements':[
  {'from':'Source-first G81-10 possible alltime product-good relation','to':'Common product AE physical0 initialization and live terminalpi only','classification':'admissible-bounded-refinement','blocking':False,'remaining':'Full random-initialized allfinite path law remains OPEN; no uncountable AE interchange needed for this header.'},
  {'from':'Source-first G81-14 possible independent-version uniqueness theorem','to':'One internally produced actual Z and exact H with product-AE source agreement at used times','classification':'admissible-bounded-refinement','blocking':False,'remaining':'Separate universal version-equivalence/uniqueness theorem OPEN.'},
  {'from':'Full source Proposition3.1/3.2/A.1/A.2','to':'Ideal exact-reference returned-position probability kernel and derived independent input phase0 law','classification':'strict-source-boundary','blocking':False,'remaining':'Markov path/semigroup/invariance/reversibility/L2/cost/composition all OPEN.'}
 ],
 'normalization_audit':{'literal_q':'volume.tilted(fun r=>-V r-||r-y||²/(2eta))','meaning':'withDensity(exp(f)/integral exp(f)); otherwise zero in totalized Mathlib definition','source_match':'Exactly normalized source2.8 everywhere-defined density; no extra Gaussian normalization constant needed because tilt normalizes whole conditional density.','nonvacuity':'Header R Markov with R y=q_y forces probability q_y. Cannot satisfy via zero/nonintegrable tilt. Proof must derive positive finite normalizer from analytic source assumptions.','potential_parent_route':'GibbsAugmentation derives integrability/positive Gibbs mass; GaussianConditionalKernel constructs quadratic tilt kernel of Gibbs probability; tilted_tilted identifies literal volume tilt. This is API/source shape inspection, no new proof or compilation claim.','rank_zero':'Canonical volume/standard Gaussian definitions have no rank>0 premise; rank0 law is Dirac on unique point. No unsupported higher derivative bound.'},
 'independence_exception_audit':{'input':'For each fixed(y,x), M_y=((q_y prod gamma) prod P), source exact r,p,clock independence.','fixedparam':'Inherited Z has AEforallfinite t/init per fixed(y,r,z0).','product_scope':'Only AE under M_y of init0 and live source pi arc simultaneously; source agreement at arbitrary sample-correlated parameters is not asserted.','last_live':'tau=top makes next clock top; every finite pi>=current stored time is in current live interval and uses actual Phi. Stopped record never supplies phase.','fallback':'Uncovered Z=z0 is explicit inherited ASTIS representative convention; source A2 used zero. No separate equality of all versions claimed; current product-AEpi/init guarantees fallback irrelevant to actual law at used times.','zero_wait':'Exceptional zero raw clocks may cause empty half-open intervals and do not promise physical init pointwise. Actual Exp positive support must supply source physical initialization.'},
 'source_inventory_coverage':{'count':65,'items':coverage},
 'source_graph_coverage':{'node_count':15,'nodes':nodes,'edge_count':29,'edges':edges,'unmapped_nodes':[],'unmapped_edges':[]},
 'proof_status':'NO81_PROOF_PRESENT_OR_REVIEWED. This checks only full proposed statement/source scope before seal, not Lean elaboration, theorem proof, blind reconstruction, final source review, SAU admission or VERIFIED.',
 'publication_boundary':'Call H the ideal exact-reference auxiliary returned-position probability kernel. Constructing q_y probability law is not an implemented exact/approx conditional sampler or cost producer. IsMarkovKernel means only fibers probability; never claim path Markov/semigroup/invariance from it.',
 'raw_inputs':raw_inputs
}
assert len(coverage)==65 and len(nodes)==15 and len(edges)==29
out=write('header-source-review81.result.json',result)
outputs=[Path(__file__).resolve(),out]
manifest={'schema':'noncircular-header-source-review-raw-manifest-v1','created_utc':now,'header_raw_sha256':sha(HEADER),'raw_inputs':raw_inputs,'raw_outputs':[{'path':str(x),'raw_sha256':sha(x)} for x in outputs],'self_hash_omitted':True,'no_proof_or_verification_credit':True}
man=write('header-source-review81.raw-manifest.json',manifest)
print('verdict',result['verdict'],'blocking',len(result['blocking_deltas']))
print(out.name,sha(out));print(man.name,sha(man))
