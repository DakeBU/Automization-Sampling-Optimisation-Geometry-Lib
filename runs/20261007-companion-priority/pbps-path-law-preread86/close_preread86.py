"""Close owned source-only preread. Extract statement text, never candidate/proof bodies."""
from pathlib import Path
from html.parser import HTMLParser
import ast, datetime, hashlib, json, re
ROOT=Path('E:/Samplinglib'); OUT=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    p=ROOT/p if not isinstance(p,Path) else p
    b=p.read_bytes(); return dict(path=p.relative_to(ROOT).as_posix(),raw_sha256=sha(b),bytes=len(b))
def readj(p): return json.loads((ROOT/p).read_text(encoding='utf8'))
def put(n,j):
    p=OUT/n; assert not p.exists(), n
    p.write_bytes((json.dumps(j,ensure_ascii=False,indent=2)+'\n').encode('utf8')); return pin(p)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
base='runs/20261007-companion-priority/'
primary=base+'phase-pbps-gamma-preread57/primary-pbps.exactraw.snapshot.html'
frozen={'source-inventory86.json':'2fb4ccca02c99a581fc089da4c48b18c0db62ff7b30144e7bd521801245d66ae','source-proof-graph86.json':'d7c2c2e0bcdfb91ea201c200c6a3b644a0114e1d5567fd36c59b3d0d45551738','source-first-seal86.json':'3a74e62d608d6dd9600466126f6d9991a64f64b4682c70e0e14f7e438ca279d7'}
for name,h in frozen.items(): assert pin(OUT/name)['raw_sha256']==h
assert pin(primary)['raw_sha256']=='d81e929496ff33f8895ebdb45b5b7f3eba89a069806d97d5bbbd7a6c0c032760'
parser_path=base+'pbps-transition-kernel-preread85/freeze_preread85.py'
cl=next(n for n in ast.parse((ROOT/parser_path).read_text(encoding='utf8')).body if isinstance(n,ast.ClassDef) and n.name=='SourceHTML')
ns={'HTMLParser':HTMLParser}; exec(compile(ast.Module(body=[cl],type_ignores=[]),parser_path,'exec'),ns)
h=ns['SourceHTML'](); h.feed((ROOT/primary).read_text(encoding='utf8'))
inventory=readj((OUT/'source-inventory86.json').relative_to(ROOT).as_posix())
for a in inventory['anchors']: assert sha(h.normalized(a['source_id']).encode())==a['normalized_anchor_sha256']
graph=readj((OUT/'source-proof-graph86.json').relative_to(ROOT).as_posix())
assert len(inventory['items'])==40 and len(graph['nodes'])==36 and len(graph['edges'])==66
priorgraph=base+'pbps-transition-kernel-preread85/source-proof-graph85.reviewed-effective.json'
pg=readj(priorgraph); assert pin(priorgraph)['raw_sha256']=='2e075d018bd310a9ecb0068e5d98bdaf01d5cf8e623e986a9b071e82b59f1f04'
assert len(pg['nodes'])==21 and len(pg['edges'])==29
prefix='AutoSamplingTheory/ExampleCases/ProximalBPS/'
files=[prefix+'ActualHazardClock.lean',prefix+'ActualSmallTimeContinuity.lean',prefix+'ActualFiniteJumpRecursion.lean',prefix+'ActualHarmonicFlow.lean',prefix+'ActualBounceRate.lean',prefix+'GaussianReflection.lean',prefix+'GibbsAugmentation.lean','AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
def prop_statement(path):
    s=(ROOT/path).read_text(encoding='utf8'); m=re.search(r'(?m)^private def \w+[^\n]*',s)
    assert m,path
    # All these sealed propositions terminate immediately before their public/auxiliary theorem documentation.
    rest=s[m.start():]; end=re.search(r'(?m)^(?:private )?(?:theorem|lemma)\s',rest)
    assert end,path
    prop=rest[:end.start()]; doc=prop.rfind('/--')
    if doc>=0: prop=prop[:doc]
    return prop.strip()
def theorem_signature(path,name):
    s=(ROOT/path).read_text(encoding='utf8'); m=re.search(r'(?m)^(?:private )?(?:theorem|lemma)\s+'+re.escape(name)+r'\b',s)
    assert m,(path,name); rest=s[m.start():]; end=rest.find(':='); assert end>=0
    return rest[:end].strip()
ml_order='.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/BorelSpace/Order.lean'
ml_ftc='.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/IntervalIntegral/FundThmCalculus.lean'
ml_exp='.lake/packages/mathlib/Mathlib/Probability/Distributions/Exponential.lean'
statements={files[0]:prop_statement(files[0]),files[1]:prop_statement(files[1]),files[-1]:prop_statement(files[-1])}
signatures={
 'MeasureTheory.Measure.ext_of_Iic':theorem_signature(ml_order,'ext_of_Iic'),
 'intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le':theorem_signature(ml_ftc,'integral_eq_sub_of_hasDerivAt_of_le'),
 'intervalIntegral.integral_hasDerivAt_right':theorem_signature(ml_ftc,'integral_hasDerivAt_right'),
 'actual_hazard_primitive_laws_private':theorem_signature(files[0],'actual_hazard_primitive_laws')}
cap=base+'pbps-actual-phase-transition-kernel85/capsule.after-science85.json'; cj=readj(cap)
handoff='docs/companion-papers-handoff.md'; text=(ROOT/handoff).read_text(encoding='utf8')
titles=[m.group() for m in re.finditer(r'(?m)^## .*$',text)][:2]
front='website/content/samplewiki_companion_frontiers.json'; execution=readj(front)['execution']
retrieval=put('statement-api-retrieval86.json',{
 'schema':'astis.source-only-statement-api-retrieval86.v1','status':'SOURCE_ONLY_POST_FREEZE','created_utc':now,
 'source_first_seal':pin(OUT/'source-first-seal86.json'),'independence':{'source_topology_frozen_before_existing_API_retrieval':True,'no_PBPS_implementation_BODIES_used':True,'no_final_review_verdicts_used':True,'no_proof_search_or_compilation':True},
 'retrieval_method':'Bounded rg filenames/declaration names, then Python regex extraction of private Prop and theorem signatures only; full-file bytes are hashed, not interpreted as proofs.',
 'native_observations':['Existing ActualHazardClock sealed Prop supplies joint continuity/measurability of Lambda, monotonicity, wait threshold equivalence, probability W, W.real(Ioi t)=exp(-Lambda t), finite-hitting equality, zero/positive cap cases.','Existing private hazard helper does not export HasDerivAt. Derivative of the explicit integral must be derived from continuous actual rate with generic FTC, not treated as a parent output.','UnitExponentialProduct sealed Prop supplies literal countable product P, coordinate marginal expMeasure1, positivity AE and independence.','ActualSmallTimeContinuity supplies actual no-first-event defect/tail convergence, not a first-event density.','Declaration-name scan found no first-event density/path-law producer among current PBPS exports. This is a bounded duplicate check, not a library-wide nonexistence theorem.'],
 'query_failures_retained':[{'kind':'retrieval-regex','detail':'First helper signature regex required theorem at column0 and missed private theorem; corrected to optional private. No mathematical failure.'},{'kind':'PowerShell-rg-path-glob','detail':'Literal wildcard argument caused rg filename syntax error; corrected using -g patterns. No mathematical failure.'}],
 'incidental_background_output':'One bounded ext_of_Iic/FTC line-range query displayed several Mathlib proof lines after signatures; those lines were not used as source, as a PBPS proof, or to select topology. Final extracted receipts contain signatures only.',
 'sealed_statement_text':statements,'background_contracts':signatures,
 'source_only85_context':{'raw_input':pin(priorgraph),'six_future_open_source_nodes':[n for n in pg['nodes'] if n.get('status') in ['FUTURE_OPEN','EXCLUDED_OPEN_BOUNDARY']]},
 'chronology_only':{'capsule':pin(cap),'generated_at':cj.get('generated_at'),'handoff':pin(handoff),'bounded_headings':titles,'note':'Handoff top checkpoint may advance concurrently. It and capsule are chronology, never source mathematics or an independent verdict.'},
 'priority':execution,'input_pins':[pin(p) for p in files+[ml_order,ml_ftc,ml_exp]]})
candidate=put('candidate-recommendation86.json',{
 'schema':'astis.source-only-candidate-recommendation86.v1','status':'PROSPECTIVE_SOURCE_ONLY_NO_SAU_OR_HEADER','created_utc':now,
 'selected_candidate_count':1,'candidate':'Actual finite first-event density and post-bounce marked law',
 'source_ids':['A1.E1','A1.E2','A1.SS1.p2.1','A1.SS1.SSS0.Px1.p4.2','A1.E7'],
 'source_graph_node':'G86-10','real_consumer':'The n=1 finite-wait factor in A.7, then successive actual finite-event factors G86-13 after separately deriving unused-clock-tail conditioning G86-11. A survival law alone does not supply the time density or marked integration.',
 'exact_boundary':{
  'domains':'Finite-dimensional real inner-product Borel E; fixed y,xRef in E, z in E×E; finite T in NNReal; bounded Borel real h on NNReal×(E×E), global |h|≤M with M≥0.',
  'six_original_hypotheses':['0<alpha','alpha≤beta','V is C2','global Hessian quadratic sandwich alpha≤Hessian V≤beta','0<eta','beta*eta≤1'],
  'literal_objects':'Actual c,Phi, total S (zero normal identity), nonnegative rate, Lambda, stopped hitting wait tau; P=infinitePi expMeasure1; epsilon(omega,0)=toNNReal(omega 0). First source E1 corresponds to actual coordinate0. No supplied process, hazard regularity, law, normalizer, invariance or first-event identity premise.',
  'first_wait':'u(omega)=tau(y,xRef,z,epsilon(omega,0)) in WithTop NNReal; A_T={omega | 0<u(omega) and u(omega)≤T}. On A_T the wait is finite. A finite projection with default0 is harmless only after proving it agrees with u on A_T.',
  'desired_integral':'integral_{A_T} h(u.finite, S_xRef(Phi_{u.finite} z)) dP = integral_{s in (0,T]} h(s.toNNReal,S_xRef(Phi_s z))*rate_xRef(Phi_s z)*exp(-Lambda_z(s.toNNReal)) ds',
  'equivalent_measure_output':'Finite subprobability law of actual first finite waiting time and post-bounce phase up to T equals the map s↦(s.toNNReal,S_xRef(Phi_s z)) of density rate(Phi_s z) exp(-Lambda_z(s.toNNReal)) times Lebesgue restricted (0,T]. The integral statement is its bounded-test consumer, the same mathematical edge.',
  'normalization':'The finite first-event mass is 1-exp(-Lambda_z(T)); missing mass includes waits beyond T or infinite, never silently normalized away.',
  'integrability':'Both bounded-test sides derive integrability from finite subprobability mass and |h|≤M; density continuity on finite interval gives its local integrability. No global exponential-moment hypothesis.',
  'parameter_scope':'Each fixed y,xRef,z and finite T, with any Borel bounded h. No simultaneous all-parameter AE event or substitution of arbitrary correlated random initialization.'},
 'source_vs_ASTIS':'The source gives inverse integrated hazard, actual iid clocks/recursion and A.7 density factors. The explicit finite subprobability/marked-law packaging and generic CDF/FTC justification are ASTIS completion of this implicit step, not a standalone source theorem or complete A.7.',
 'selected_sufficient_route':{'route':'CDF/FTC finite-measure equality, then actual post-bounce marking','AND_ingredients':['Literal coordinate0 marginal from UnitExponentialProduct','Existing actual75 threshold/survival law and probability W','Derived continuity of actual rate along Phi and derivative Lambda=rate from FTC','Finite-measure ext_of_Iic plus chain derivative of 1-exp(-Lambda)','Measurable total bounce/flow and integral-map transfer, finite-event restriction eliminates top/default branches'],
  'OR_alternative':'Monotone-hazard inverse transport remains an unselected sufficient alternative; it is not an additional AND requirement. Neither route may assume strict monotonicity or differentiate an inverse across flat hazard intervals.'},
 'readiness':{'assessment':'Dependency-ready at source/statement-interface level for owner selection and independent topology review; no proof attempt, implementation or theorem acceptance.','known_parent_contracts':['actual_integrated_hazard_clock_laws: wait tail/CDF and continuous Lambda','unit_exponential_product_laws: literal coordinate Exp1 law and positivity AE','actual harmonic flow and total bounce interfaces, plus existing actual finite recursion definition'],
 'remaining_internal_analysis':'Derive continuous free-arc rate and derivative Lambda locally; obtain finite first-event density using generic FTC/measure ext. These are intended mathematical content, not absent public assumptions.'},
 'smaller_fallback_if_marking_tooling_is_too_large':'The exact finite first-wait subprobability density alone, with the same actual product input and literal tau. This strictly advances beyond the proved CDF; a CDF/survival-only theorem is redundant and should be retired.',
 'boundary_cases':['T=0 gives empty finite-event restriction and zero RHS','M=0 gives zero test integrals','Exp threshold0 has probability0; tau0=0 is not a positive first event','Infinite first wait produces no finite event and last live arc persists','Flat hazard/zero cap allowed; density0 there, no division by cap or strict monotonicity','Rank0 and zero bounce normal are retained; total reflection identity convention','Stopped dummy future records do not represent an actual finite bounce'],
 'explicit_OPEN':['Full A.7 event-count expansion','Independent unused-clock tail conditional iteration','Full path measurable space and right/left jump-value reversal adapter','A.8 full product Borel change of variables','A.4 and finite-path Gibbs survival-weight identity','Outer Tonelli/mass-one summation and bounded signed reversal','Actual Gibbs phase invariance','AE-safe L2 operator/Jensen contraction','Independent compact-continuous L2 density and all-L2 strong continuity','Restart/Markov/semigroup/Chapman-Kolmogorov','Main paper rates/costs/actual-input PBPS-SPHMC composition'],
 'critical_source_gaps_retained':inventory['source_gaps'],'license':'arXiv perpetual non-exclusive distribution v1; primary RAW stays private; no wholesale staging.',
 'no_new_public_binder_from_background_ingredient':True,'no_proof_or_state_credit':True})
closure=put('source-only-closure86.json',{
 'schema':'astis.source-only-closure86.v1','status':'CLOSED_SOURCE_ONLY','created_utc':now,
 'frozen_originals':[pin(OUT/n) for n in frozen],'all_56_primary_anchor_hashes_rechecked':True,
 'coverage':{'inventory_items':40,'nodes':36,'relations':66,'dependency_edges':63,'excluded_associations':3,'anchors':56,'all_items_nodes_relations_preserved':True},
 'chronology':['Independent primary-only 40/36/66 topology froze at source-first-seal timestamp before statement APIs.','After freeze, source-only85 six OPEN nodes and permitted chronology/priority were consulted.','After freeze, bounded statement-only API and generic Mathlib retrieval selected the novel density edge and rejected duplicate CDF wrapper.','Closed source-only outputs with exact RAW receipts; no SAU/header/proof/production/claim/ledger/site modification.'],
 'source_topology_not_self_approved':'This is author extraction and prospective recommendation, requiring a distinct topology/source audit if selected; no self-validation of graph or theorem.',
 'retrieval':retrieval,'candidate':candidate,
 'no_PBPS_implementation_proofs_or_final_verdict_basis':True,'no_parallel_Goal_paper_or_implementation':True})
inputs=[primary,parser_path,priorgraph,cap,handoff,front,'lean-toolchain','lake-manifest.json']+files+[ml_order,ml_ftc,ml_exp]
manifest=put('source-only-run-manifest86.json',{
 'schema':'astis.source-only-raw-manifest86.v1','status':'closed','created_utc':now,
 'raw_inputs':[pin(p) for p in dict.fromkeys(inputs)],
 'raw_outputs':[pin(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='source-only-run-manifest86.json'],
 'self_hash_omitted':True,'noncircular_convention':'Manifest lists exact RAW inputs and outputs, excluding itself. Original seal binds only source-first inputs/outputs; later closure references frozen originals and retrieval/candidate; no reverse references. Script source pins are artifacts, not self-hashes in the scripts.',
 'truth_boundary':'Prospective source-only reading, graph and one candidate recommendation; no header/proof/compiler/formalization or SAU state credit.'})
for p in [OUT/'candidate-recommendation86.json',OUT/'source-only-closure86.json',OUT/'source-only-run-manifest86.json']:
 print(json.dumps(pin(p)))
