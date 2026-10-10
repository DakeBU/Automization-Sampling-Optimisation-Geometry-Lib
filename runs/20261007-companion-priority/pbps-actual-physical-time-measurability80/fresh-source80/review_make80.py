from pathlib import Path
import json,hashlib,datetime
ROOT=Path('E:/Samplinglib')
RUN=ROOT/'runs/20261007-companion-priority/pbps-actual-physical-time-measurability80'
OWN=RUN/'fresh-source80'
PKT=RUN/'source-review80.packet.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(o):return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
def write(name,o):
 p=OWN/name;p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return p
p=json.loads(PKT.read_text(encoding='utf-8'));q=dict(p);q.pop('packet_sha256')
assert canon(q)==p['packet_sha256']=='fc8686899804419df91ce35606537e02e11f0ff1d63b0d6d9808c9e4539d855e'
assert p['publication_binding_sha256']=='d85b866ee0c62651a1a4cecd2db69ae8cf62f244fe547f1baee4bf00eef90eaa'
module=ROOT/p['lean']['file'];code=module.read_text(encoding='utf-8');lines=code.splitlines(keepends=True)
assert sha(module)=='bf8f66a8484fa82c46b26ac6b66a6c8484e6dd6465ac8587d7e27b2489e73a5c'
assert p['candidate_publication_context']['current_lean_module']==code
for field,key in [('lean','statement'),('source','original_text'),('blind_reconstruction','text')]:
 hashkey='statement_sha256' if field=='lean' else 'text_sha256'
 assert hashlib.sha256(p[field][key].encode()).hexdigest()==p[field][hashkey]
seal=json.loads((OWN/'source_freeze80.seal.json').read_text(encoding='utf-8'))
for f,h in seal['files'].items():assert sha(OWN/f)==h,(f,'original freeze changed')
assert sha(OWN/'source_freeze80.seal.json')=='4fd2be40a745c8a3c9ed93e4065131a27be267ae0290561379013e5dfadf615f'
assert sha(OWN/'source_freeze80.raw-manifest.json')=='d84522e4944d096f7054fd3710e00823ef46bb4e35688017c754226a53c9bf07'
inv=json.loads((OWN/'source_inventory80.json').read_text(encoding='utf-8'));graph=json.loads((OWN/'source_proof_graph80.json').read_text(encoding='utf-8'))
SRC=Path(inv['source']['pinned_local_raw_path']);assert sha(SRC)==inv['source']['raw_sha256']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
independence={
 'reviewer':'/root/fresh_source78 (independent source reviewer80)',
 'source_first_freeze_created_utc':seal['created_utc'],
 'source_first_seal_raw_sha256':sha(OWN/'source_freeze80.seal.json'),
 'source_first_raw_manifest_sha256':sha(OWN/'source_freeze80.raw-manifest.json'),
 'original_source_freeze_unchanged':True,
 'candidate_not_seen_before_source_inventory_and_topology_freeze':True,
 'fresh_stdlib_html_parser_only_for_primary_source':True,
 'final_review_started_only_after_canonical_packet_authorized':True,
 'formalizer_and_decoder_distinct_from_this_reviewer':True,
 'no_prior80_header_scope_math_review_verdicts_root_adoption_or_other_source_extractor_consulted':True,
 'no_previous78_or79_verdict_used_as_evidence':True,
 'all_candidate_packet_claims_treated_as_untrusted_and_compared_to_pinned_primary_and_current_exact_bodies':True,
 'writes_limited_to_owned_fresh_source80_directory':True,
 'no_production_shared_cell_registry_ledger_site_or_VERIFIED_transition':True
}
slots={}
def slot(k,original,reconstructed,relation,evidence):slots[k]={'original':original,'reconstructed':reconstructed,'relation':relation,'evidence':evidence}
slot('objects',
 'Primary A1.Ex1-3, A1.E1/E2 and p2.1-p2.2 specify actual rate, harmonic Phi, zero-safe reflection, iid Exp1 thresholds, finite postbounce recursion and physical half-open interpolation. No phase at infinity is specified.',
 'Blind OBJECTS and literal private Prop use the same c,Phi,S,rate,Lambda,tau; product P and coordinate clamp epsilon realize source E_(n+1) at Lean index n. Sum finite records plus absorbing Unit retain the finite guard. One total Z is assembled by countable branch gluing, with explicit initial-phase value on the uncovered complement.',
 'explicit-elaboration',
 'Main private Prop lines16-77 and BODY93-126 repeat literal definitions, matching actual76/77/79. HittingAfter is the infimum of the exact threshold-hit set, with empty-set top. Real total division gives R0=I. The zero branch L on stopped records is only auxiliary; T_n=top cannot satisfy T_n<=finite t. Uncovered Z=z0 is labelled ASTIS, not a source-prescribed state.')
slot('domains',
 'Source uses R^d, fixed y,xRef and phase z0; finite nonnegative physical/local times, positive finite Exp1 clocks and potentially infinite event waits.',
 'Blind DOMAINS correctly reconstruct arbitrary finite-dimensional real inner-product Borel E including dimension zero; NNReal finite times/thresholds and WithTop event times. Raw real sequences are totalized by NNReal clamp. Z jointly measurable on ((E×E)×(E×E))×(NNReal×(N→R)), while V,alpha,beta,eta are fixed.',
 'explicit-elaboration',
 'Finite-dimensional real inner-product coordinates preserve Euclidean formulas, Hessian and Borel structure without a positive-dimension premise. rank0 has zero rate, first positive wait top and the sole live arc; no division by dimension/cap is added. Source agreement applies to the Exp1 full-measure support. No infinite physical time, or varying potential/eta measurability is asserted.')
slot('quantifiers',
 'Source fixes deterministic y,xRef,z0, builds from countable iid clocks, and after nonaccumulation defines the phase for all finite t on an a.s. valid path.',
 'Blind QUANTIFIERS match one existential Z chosen for all y,xRef,z0,t,sample; its deterministic covered and uncovered clauses hold for every raw sample. Last clause is forall fixed(y,xRef,z0), AE sample, ((forall finite t, exists n,a satisfying live arc agreement) and Z0=z0).',
 'equivalent',
 'Main lines57-77 and BODY217-249: intro parameters before filter_upwards[hc,hp]; time is introduced inside the same good-event proof. No interchange to AE sample forall uncountably many triples, or forall t AE with different null sets. Measurable substitution alone does not justify source agreement at arbitrarily sample-correlated parameters.')
slot('assumptions',
 'Standing source V in C2(R^d), 0<alpha<=beta, Hessian sandwich, eta in(0,1/beta]; fixed reference and phase with iid Exp(rate1) input.',
 'Blind ASSUMPTIONS identify exactly six analytic binders h_alpha,h_alpha_beta,h_V,h_H,h_eta,h_beta_eta, the ambient finite-dimensional inner-product/Borel typing, and literal product input. No supplied selector/process/nonexplosion/measurability/energy/cap/support certificates.',
 'equivalent',
 'Main lines17-25 and81-91. beta>0 follows from alpha>0 and alpha<=beta, so beta*eta<=1 and eta>0 are exactly the source scale. hH universally quantifies x,v and both bounds. C2 has no higher derivative addition. Positivity and cover are consumed dependency conclusions; parameterized flow/record measurability is derived in parents.')
slot('conclusion',
 'Bounded source piece: literal between-jump phase at every finite time for each fixed triple on a common a.s. nonaccumulating sample, with physical initialization zeta0=z0. Measurability is implicit in defining this random process, not a displayed standalone joint theorem.',
 'Blind CONCLUSION matches all four conjuncts: jointly measurable total Z; deterministic actual covered-arc equality; uncovered z0 convention; per-fixedparams AE all-finite-time live witness with true elapsed<tau and initialization.',
 'explicit-elaboration',
 'BODY127-210 proves joint Borel countable gluing from actual measurable finite records and flow. BODY211-216 certifies only uncovered complement convention. BODY217-249 obtains all-time actual agreement and initialization. Stronger explicit measurable adapter structure is labelled, with no changed source path on good inputs; full Proposition3.1 is not claimed.')
slot('scopes',
 'Primary finite wait update, empty-set stop and half-open local arcs are distinct branches. Nonaccumulation pertains to actual Exp1 input; Markov/stationarity/algorithm law and costs are other source clauses.',
 'Blind SCOPES_SENSES correctly separate globally total/pointwise Borel and conditional rules from per-fixedparams AE all-time agreement and initialization; NNReal truncation, top guard and zero thresholds are literal. Last infinite-wait live interval remains covered; stopped next record has no phase.',
 'equivalent',
 'On D_n, T_n<=finite t forces inl a and a.time<=t; NNReal tsub is true nonnegative elapsed. D_n is empty for zero increments and disjoint by monotonicity. For tau=top next T=top, so every finite offset remains in D_n, excluding fallback. Positive clocks give T1>0 (or stopped1 top), hence source physical0 selects initial live record and Phi0=id. Exceptional zero clocks are not promised source initialization. Global process/law/cost clauses excluded.')
slot('constant_dependencies',
 'Source constants: Exp rate1, clock index1 onwards, initial time0, reflection multiplier2, scale beta*eta<=1; c depends on eta,V,y,xRef and cap on fixed initial energy/reference.',
 'Blind CONSTANT_DEPENDENCIES correctly place E,V,alpha,beta,eta outside existential Z; P and epsilon fixed. y,xRef,z0,t,sample are arguments of one map; per-triple null sets depend on fixed triple/outer data but not t. n,a depend on sample/time. No unspecified cost/uniform dimension bound.',
 'equivalent',
 'Definitions93-126 and private Prop26-77. alpha/beta enter analytic hypotheses/witness construction, not changed rate. No cap binder; cap and indicator-SLLN alternative are parent edges. Joint measurability is not asserted in V,eta or hypothesis witnesses.')
assert list(slots)==p['review_contract']['semantic_slots']
step_comments=[
 'All eleven literal objects retained. Guard precedes finite untopD; epsilon_n is source E_(n+1).',
 'h76 supplies exact initialization, record/time measurability, monotonicity and strict positive increments; harmonic laws supply joint measurable Phi and Phi0. Clamp/projections correctly typed on A.',
 'D_n Borel by comparisons. n<m implies T_(n+1)<=T_m, contradicting T_m<=t<T_(n+1). No nonaccumulation/positive-wait premise for disjointness.',
 'L is everywhere Borel with dummy zero branch. Stopped_n impossible on D_n. Finite NNReal subtraction and hPhiM prove branch measurable; covered rule removes dummy via live equality.',
 'Option Nat disjoint countable sets include measurable union-complement none, whose z0 value is Borel. Compatibility is vacuous on empty intersections. Pinned piecewise theorem produces total f.',
 'Curry f to Z. Membership some n and live-record rewrite yield true harmonic interpolation for every raw sample. No unproved measurable classical selector.',
 'No bracket implies membership none; hf none gives z0. Last infinite-wait live D_n is not none.',
 'Intersect parent79 all-time cover and canonical support once per fixed triple. Cover supplies n,live a,stored_time<=t,elapsed<tau simultaneously forall finite t. hZ gives actual phase; no uniform-parameter AE inference.',
 'Record0 and T0 initialized. epsilon0>0 AE. stopped1 gives T1=top; live1 strictly increases by76. Thus0 in D0 and Phi0 gives physical initialization AE; no every-raw-sample initialization.'
]
steps=[];covered=[]
for i,(s,comment) in enumerate(zip(p['candidate_publication_context']['lesson']['steps'],step_comments),1):
 r=s['lean_source_region'];chunk=''.join(lines[r['start_line']-1:r['end_line']]);assert chunk==s['lean'];assert hashlib.sha256(chunk.encode()).hexdigest()==r['exact_code_raw_sha256']
 covered.extend(range(r['start_line'],r['end_line']+1));steps.append({'step':i,'title':s['title'],'start_line':r['start_line'],'end_line':r['end_line'],'exact_code_raw_sha256':r['exact_code_raw_sha256'],'formula_review':'consistent with bounded source adapter and exact BODY','body_review':comment,'status':'covered','blocking':False})
assert covered==list(range(93,250))
node_evidence={
 1:('COVERED_PARENT_AND_LITERAL','Private Prop17-55; actual harmonic/bounce parents; six conditions and source maps retained.'),
 2:('COVERED_PARENT','UnitExponentialProduct complete BODY: product/laws/iIndepFun, coordinate measurability, common-AE positivity and clamp equality. Main136-137,221-222,233.'),
 3:('COVERED_PARENT','ActualHazardClock complete BODY: continuous parametric primitive, closed-hit attainment/sublevel identity, empty top/finite/zero/positive waits, measurable_of_Iic.'),
 4:('COVERED_PARENT_AND_PULLBACK','ActualFiniteJumpRecursion complete BODY: measurable guarded next using Borel S/Phi/tau; induction records and Sum-elim times. Main127-146 pulls back clamped sample.'),
 5:('COVERED_PARENT_AND_INIT','Actual76 initialization/monotonicity/strict positive finite increment. Main151-158 disjointness;228-249 physical T0=0<T1.'),
 6:('COVERED_PARENT_ALTERNATIVE_ROUTE','Actual78 complete BODY: energy/cap ancestors; zero cap stops1, positive cap bounds all Tn by sums/C. Product bounded-indicator SLLN proves divergence. Original source Exp mean1 route OPEN alternative.'),
 7:('COVERED_PARENT_AND_CONSUMER','Actual79 complete BODY: first-crossing Nat.find, initialized predecessor/monotone uniqueness; stopped_n excluded by finite t; finite elapsed bound or top-wait tail. Main223-227 consumes.'),
 8:('COVERED_EQUIVALENT_COUNTABLE_GLUE','Main147-210 measurable disjoint D_n and countable piecewise values implement selected-value measurability without exporting a separate measurable Nat selector.'),
 9:('COVERED_ASTIS_EXTENSION','Main171-216 measurable uncovered complement/z0 extension; fixedparam good event is covered at all finite times. No uncountable-quantifier good-set Borel premise.'),
 10:('COVERED_SOURCE_IMPLICIT_ADAPTER','Main159-227 finite NNReal elapsed, joint Phi composition, countable gluing, source arc agreement common-AE all finite times.'),
 11:('COVERED_PHYSICAL_INIT','Main228-249 positive epsilon0; actual76 strict finite increment or stopped1 top; D0,record0,Phi0 imply physical Z0=z0.'),
 12:('COVERED_PARENT_AND_ARC_EQUALITY','Actual76 guard and79 top-wait branch: next time top, current record remains live. Main covered equality evaluates all finite elapsed; neither stopped dummy nor none supplies last arc.')
}
nodes=[]
for i,n in enumerate(graph['nodes'],1):
 status,evidence=node_evidence[i];nodes.append({'id':n['id'],'source_obligation':n['obligation'],'source_anchors':n['anchors'],'status':status,'evidence':evidence,'blocking':False})
edge_notes={
 (1,3):'77 continuous rate along joint continuous Phi gives continuous Lambda/closed-hit sublevels.',
 (2,3):'77 deterministic clock measurable for all NNReal e; coordinate clamp supplies actual measurable threshold. Positivity used only in positive branches.',
 (1,4):'Borel zero-safe S and measurable Phi compose in guarded next76.',
 (3,4):'Measurable tau/top-test/untopD give next76 and record induction.',
 (2,5):'Canonical common-positive support yields epsilon0>0 main233 without premise.',
 (3,5):'tau(e)>0 from Lambda0 and sublevel identity; finite guard gives strict increment76.',
 (4,5):'Initialized record and Sum-elim event time give T0=0/monotonicity including top.',
 (1,6):'Actual energy conservation and beta-Lipschitz cap consumed in76/78.',
 (2,6):'Actual threshold sums diverge via bounded-indicator SLLN OR-route; direct Exp mean1 route remains OPEN.',
 (4,6):'Zero-cap stop/absorption and positive-cap increments give escape78.',
 (5,7):'Initialized monotone T gives first-crossing predecessor/unique half-open interval79.',
 (6,7):'AE escape gives some clock above each finite t in79.',
 (4,7):'Live/time equality and guarded next give stored_time<=t,elapsed<wait; stopped_n impossible.',
 (4,8):'Actual measurable finite records/times compose with clamp; D_n comparisons Borel.',
 (7,8):'Equivalent measurable countable branch values replace exported selector; monotonicity gives disjointness, AE79 supplies cover.',
 (2,9):'Canonical support distinguishes actual source samples from totalized nonpositive raw sequences.',
 (6,9):'AE escape guarantees no finite uncovered source-good point.',
 (7,9):'Simultaneous all-time cover ensures no fallback on same good event.',
 (8,9):'Countable Borel union complement none with Borel z0 coordinate.',
 (1,10):'Joint measurable literal Phi from73 with fixed outer V/eta.',
 (4,10):'L_n finite stored phase/time measurable; covered live equality removes dummy.',
 (7,10):'79 ensures actual nonnegative finite elapsed below wait.',
 (8,10):'Option Nat piecewise theorem yields jointly Borel selected flow.',
 (9,10):'none provides total measurable map without changing covered arcs.',
 (1,11):'Phi0=id from73 consumed249.',
 (2,11):'Common positivity at0 gives epsilon0>0.',
 (3,11):'Positive first threshold cannot hit at0; passed through strict76.',
 (5,11):'T0=0/live record0 and T1>0 or top establish D0.',
 (7,11):'Direct bracket D0/live record0 invokes hZ, no classical arbitrary index.',
 (10,11):'hZ at0 plus Phi0 gives source initialization AE.',
 (4,12):'tau=top sets next stopped but retains current live record.',
 (7,12):'79 top-wait branch allows all finite elapsed<top, T_n<=t<top.',
 (10,12):'hZ gives Phi finite elapsed on last live D_n; no dummy/fallback phase.'
}
edges=[]
for e in graph['edges']:
 a=int(e['ingredient'][-2:]);b=int(e['consumer'][-2:]);edges.append({**e,'status':'covered-with-explicit-route-elaboration' if (a,b) in [(2,3),(7,8),(2,6)] else 'covered','evidence':edge_notes[(a,b)],'blocking':False})
coverage=[]
for item in inv['source_scope_coverage']:
 a=item['anchor'];cl=item['classification'];entry={**item,'blocking':False}
 if cl=='EXCLUDED':entry.update(status='EXCLUDED',evidence=item.get('reason','Outside bounded adapter.'))
 elif a=='license-tr':entry.update(status='COVERED_PROVENANCE',evidence='Pinned license read; only paraphrased inventory/bounded formulas produced, no full-source duplicate.')
 elif a=='A1.SS1.p3.7':entry.update(status='PARTIAL_COVERED_WITH_OPEN_EXCLUSIONS',evidence='Nonaccum parent consumed via79 and source-compressed measurable phase unfolded. Direct Exp mean1 route OPEN; labelled indicator-SLLN alternative. Global unique Markov/Davis/memoryless package EXCLUDED/OPEN.')
 elif 'defines-unique-process' in a:entry.update(status='PARTIAL_COVERED_OTHER_CLAUSES_OPEN',evidence='Only jointly Borel actual finite-time phase and physical initialization; full global uniqueness/Markov/stationarity/law OPEN.')
 elif a=='A1.SS1.p2.2':entry.update(status='COVERED_FINITE_STOP_AND_LAST_LIVE_ARCS',evidence='Finite guard, empty-hit top stop and half-open Phi retained in76/79/hZ80. Infinite wait leaves current live arc all finite offsets; no phase at infinity.')
 elif 'p4.4:Borel' in a:entry.update(status='COVERED_BACKGROUND_ONLY',evidence='Borel bounce/measurable flow parents; countable random-time gluing proved separately. No bounce continuity or measure-preservation/Jacobian claim.')
 elif a.startswith('A1.Ex') and int(a[5:])>=4 or a.startswith('A1.SS1.p3.'):
  entry.update(status='COVERED_PARENT_INGREDIENT',evidence='Complete harmonic/bounce/hazard/finite-recursion/nonaccum bodies checked. Source energy/layer/cap, zero vs positive cap, stopped vs continuing separate.79 consumes actual escape;80 consumes79 without new certificate binder.')
 else:entry.update(status='COVERED_LITERAL_OR_STANDING',evidence='Frozen source role checked against literal definitions/six conditions/private Prop/BODY/exact parents; dynamics, endpoint convention, eta scale retained. See slots/nodes.')
 coverage.append(entry)
assert len(coverage)==41 and len(nodes)==12 and len(edges)==33
parents=[
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHarmonicFlow.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualBounceRate.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualHazardClock.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualFiniteJumpRecursion.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualNonaccumulation.lean',
 'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualPhysicalTimeCover.lean',
 'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
mathlibs=['.lake/packages/mathlib/Mathlib/MeasureTheory/MeasurableSpace/Constructions.lean','.lake/packages/mathlib/Mathlib/Probability/Process/HittingTime.lean']
inputs=[SRC,PKT,module]+[ROOT/x for x in parents+mathlibs]+[ROOT/'lean-toolchain',ROOT/'lake-manifest.json']+[OWN/x for x in list(seal['files'])+['source_freeze80.seal.json','source_freeze80.raw-manifest.json']]
raw_inputs=[{'path':str(x.relative_to(ROOT)).replace('\\','/'),'raw_sha256':sha(x),'bytes':x.stat().st_size} for x in inputs]
freeze_checks={'seal_files':seal['files'],'seal_raw_sha256':sha(OWN/'source_freeze80.seal.json'),'raw_manifest_sha256':sha(OWN/'source_freeze80.raw-manifest.json'),'unchanged':True}
evidence={
 'schema':'independent-source-review-run-evidence-v1','reviewer':'/root/fresh_source78 for80','created_utc':now,
 'reviewer_packet_sha256':p['packet_sha256'],'reviewer_packet_raw_sha256':sha(PKT),
 'publication_binding_sha256':p['publication_binding_sha256'],'full_module_sha256':sha(module),
 'input_hash_convention':'raw_inputs are exact byte SHA256. Packet canonical hash removes only packet_sha256, then JSON dumps ensure_ascii=False sort_keys=True separators comma colon.',
 'canonical_packet_validated':True,'exact_current_module_matches_packet':True,
 'statement_source_blind_text_hashes_validated':True,'source_first_chronology':independence,
 'freeze_unchanged_checks':freeze_checks,'raw_inputs':raw_inputs,
 'review_actions':['Re-read own source-first inventory/graph, then only canonical packet.','Read entire exact main private Prop and BODY, all nine prose/formula/BODY regions.','Read complete actual harmonic/bounce/finite-recursion/hazard/nonaccumulation/cover and UnitExponentialProduct current bodies/typing.','Read pinned Mathlib piecewise theorem and hittingAfter definition.','Account individually for41 coverage items,12nodes,33edges, including explicit source/implicit adapter/alternative/OPEN/excluded.','Validate canonical packet/text/module/region hashes and unchanged original source freeze.'],
 'compiler_status':'Packet compiled=true is supplied lane evidence. Source reviewer does not rerun Lean/gate or confer compiler/VERIFIED credit.',
 'no_circular_hash':'Standalone evidence omits its own hash and result/manifest hashes. Result review_run_sha256 binds its RAW bytes; final manifest binds all outputs and omits only selfhash.'
}
ev=write('source-review.run-evidence80.json',evidence)
result={
 'schema_version':1,'task':p['task'],'packet_id':p['packet_id'],
 'reviewer':'independent anti-anchored source reviewer80 (/root/fresh_source78)',
 'independent_from_formalizer':True,'independent_from_decoder':True,'independence':independence,
 'reviewer_packet_sha256':p['packet_sha256'],'reviewer_packet_raw_sha256':sha(PKT),
 'publication_binding_sha256':p['publication_binding_sha256'],'full_module_sha256':sha(module),
 'source_raw_sha256':sha(SRC),'review_run_sha256':sha(ev),'semantic_slots':slots,
 'deltas':[
 {'slot':'objects','classification':'notation-resolution','blocking':False,'description':'Product/clamp, zero-index epsilon_n=source E_(n+1), Sum stopped coding, WithTop and guarded finite extraction explicitly realize source input/recursion.'},
 {'slot':'domains','classification':'domain-clarification','blocking':False,'description':'Finite-dimensional inner-product Borel carrier including rank0 explicitly generalizes Euclidean coordinates; all physical time/elapsed finite NNReal; no dimension positivity.'},
 {'slot':'conclusion','classification':'source-implicit','blocking':False,'description':'Proved joint parameter/time/sample Borel realization completes source-compressed construction; labelled ASTIS adapter, no supplied selector/process/measurability premise and no verbatim-source joint theorem claim.'},
 {'slot':'scopes','classification':'formalization-artifact-risk','blocking':False,'description':'Explicit uncovered Z=z0 convention, stopped L dummy only auxiliary. Actual good arcs including infinite-wait last live arc covered and use Phi; no phase at top or every-sample initialization claimed.'},
 {'slot':'quantifiers','classification':'quantifier-clarification','blocking':False,'description':'One global measurable Z, common-AE forall finite t/init for each fixed triple. Uniform-parameter AE and arbitrary sample-correlated random-parameter source laws require separate arguments and remain excluded.'},
 {'slot':'scopes','classification':'open-source-route','blocking':False,'description':'Direct Exp first-moment/mean1 SLLN source route stays OPEN alternative; parent bounded-indicator SLLN suffices for current actual divergence without extra binder.'}
 ],
 'verdict':'equivalent-after-elaboration','blocking_deltas':[],'repairs':[],
 'no_required_mathematical_repairs':True,
 'review_evidence':'Source inventory/topology independently froze before candidate. Exact primary and current entire private Prop/BODY/parents reviewed. All7 slots/41items/12nodes/33edges accounted;9 exact authored regions cover main proof93-249 without gap. Verdict applies only to bounded source-implicit actual phase realization and initialization.',
 'authored_step_coverage':{'expected_steps':9,'reviewed_steps':9,'steps':steps,'full_module_lines':len(lines),'private_statement_lines':[16,77],'theorem_header_lines':[81,91],'proof_body_lines':[93,249],'covered_body_line_count':157,'gaps':[],'overlaps':[],'formula_body_exact_matches':True,'all_step_prose_and_formulas_independently_reviewed':True,'full_module_reviewed':True},
 'source_graph_coverage':{'inventory_item_count':41,'inventory_items':coverage,'node_count':12,'nodes':nodes,'edge_count':33,'edges':edges,'unmapped_scoped_items':[],'unmapped_nodes':[],'unmapped_edges':[],'source_scope_exclusions':inv['scope']['excluded'],'route_note':'Equivalent countable branch-glue instead of exported selector. Actual cap/nonaccum parents consumed. Direct Exp mean1 route OPEN. Full global unique process and Markov/law/cost clauses OPEN/excluded.'},
 'truth_boundary':{
  'accepted_bounded_edge':'One jointly Borel total actual physical-time phase representative, deterministic covered-arc agreement/uncovered initial-phase convention, per-fixedparams common-AE all-finite-time live arc realization and physical initialization.',
  'source_direct':'Actual Phi/rate/R0/A.1/A.2, fixedparams/init, finite-guard/empty-stop, half-open interpolation and original six analytic conditions.',
  'astis_implicit_adapter':'Canonical product/clamp and record coding; countable measurable piecewise selection; finite elapsed evaluation; joint parameter/time/sample map; explicit uncovered z0 convention.',
  'compiled_parent_edges_inspected':parents,
  'not_inferred':['Uniform AE event over all parameter triples','Source agreement after arbitrary sample-correlated random-parameter substitution','Full Algorithm1 conditional/Gaussian initialization and x_pi law','Global unique/cadlag/adapted/stoppingtime process','Markov/strong Markov/memoryless conditional law','Stationarity/invariance/reversibility/transition kernel/semigroup','Hypocoercivity/convergence/error/query/expected-event costs','PBPS-SPHMC or later-paper composition/full Goal completion'],
  'last_live_arc':'Infinite next wait retains current finite live phase for all finite t>=stored_time; neither stopped dummy nor uncovered z0 supplies it.',
  'rank_zero_zero_waits':'No rank>0 premise. Zero thresholds exceptional total extension; monotone half-open empty intervals handled. AE strict positivity proves init. rank0 rate0 gives first top wait/live flow.',
  'remaining_source_open':'Direct Exp mean1/moment-SLLN route and excluded global/process/law/cost clauses separate obligations; no whole-source completion credit.',
  'review_not_proof_or_VERIFIED_transition':True
 }
}
res=write('source-review.result80.json',result)
outputs=sorted(x for x in OWN.iterdir() if x.is_file() and x.name!='source-review.run-manifest80.json')
manifest={'schema':'noncircular-exact-raw-run-manifest-v1','created_utc':now,'reviewer':'/root/fresh_source78 for80','reviewer_packet_sha256':p['packet_sha256'],'publication_binding_sha256':p['publication_binding_sha256'],'full_module_sha256':sha(module),'original_source_first_chronology':independence,'raw_inputs':raw_inputs,'raw_outputs':[{'path':str(x.relative_to(ROOT)).replace('\\','/'),'raw_sha256':sha(x),'bytes':x.stat().st_size} for x in outputs],'hash_convention':'Exact RAW SHA256 for all inputs/outputs. Result.review_run_sha256=standalone evidence RAW SHA256. Manifest binds evidence/final result, omits only own output/selfhash; manifest hash externally reported.','selfhash_omitted':True}
ma=write('source-review.run-manifest80.json',manifest)
for name in ['source-review.result80.json','source-review.run-evidence80.json','source-review.run-manifest80.json']:print(name,sha(OWN/name))
print('VERDICT',result['verdict'],'blocking',len(result['blocking_deltas']),'coverage',len(coverage),len(nodes),len(edges),'steps',len(steps),'BODY',len(covered))
