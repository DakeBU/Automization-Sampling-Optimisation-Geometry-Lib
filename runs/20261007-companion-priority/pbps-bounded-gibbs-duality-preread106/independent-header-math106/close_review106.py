from pathlib import Path
import json,hashlib
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;P=O.parent
S=R/'runs/20261007-companion-priority/pbps-actual-countable-endpoint105/next-primary106'
sha=lambda b:hashlib.sha256(b).hexdigest()
def info(p):return dict(path=p.relative_to(R).as_posix(),raw_sha256=sha(p.read_bytes()),bytes=p.stat().st_size)
def load(p):return json.loads(p.read_bytes())
def save(n,v):
 p=O/n;assert not p.exists();p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
freeze=load(O/'input-freeze106.native.json')
for x in freeze['inputs']:assert info(R/x['path'])==x
receipt=load(O/'fresh-typecheck106.receipt.json');assert receipt['exit_code']==0 and receipt['terminal_closed']
root=load(P/'typecheck106/receipt.json');assert root['exit_code']==0 and root['header']['raw_sha256']==info(P/'Header106.lean')['raw_sha256']
save('header-math-decision106.native.json',{
 'decision':'ACCEPT_PROSPECTIVE_EXACT_HEADER_MATHEMATICS_AND_TYPE','reviewer':'/root/exact_verifier96',
 'header':info(P/'Header106.lean'),'fresh_typecheck':info(O/'fresh-typecheck106.receipt.json'),'original_producer':info(R/'AutoSamplingTheory/ExampleCases/ProximalBPS/ActualCountableEndpointLaw.lean'),
 'assumptions':{'original_six_analytic_binders_text_identical_to105':True,'ambient_types_identical':True,'additional_analytic_premises':[],'observable_hypotheses':'F,G are real-valued measurable and bounded pointwise by nonnegative real CF,CG. These are explicitly nested inside the universally quantified observable conclusion after the global process witness and fixed parameters. They do not strengthen the six analytic assumptions.','no_arbitrary_provider':'No supplied process, endpoint law, density, kernel, normalizer, finite mass, integrability or momentum-symmetry hypothesis.'},
 'literal_contract':{'definitions':37,'unchanged_LF_literal_block':True,'global_Z_identification_prefix_exact':True,'same_witness_quantifiers':'One Z exists before every y,xRef,T and observable choice; the same witness is jointly measurable, obeys the raw covering-arc formula and no-cover fallback, and has parameterwise P-a.e. initialization.','nu':'Position tilt of negative actual Vy times standard Gaussian momentum, with normalization derived internally.','P':'Actual countable product Exp(1), no arbitrary clock measure.','endpoint':'Actual Z at the fixed nonnegative T, with domain initial phase first times raw clocks.','op':'Real Bochner clock expectation of G of that same endpoint. Total integral semantics do not remove the obligation to prove signed product and section integrability.'},
 'conclusion_audit':[
  'MeasurePreserving endpoint (nu.prod P) nu asserts global endpoint measurability and actual fixed-time phase marginal invariance; it adds no semigroup or restart conclusion.',
  'Both outer Integrable assertions are explicit. Bounds on F,G and actual probability imply section/product integrability; the proof cannot rely merely on a totalized Bochner integral equality.',
  'The right side is exactly G(R z) times op(F composed R)(z). Endpoint pair reversal J(start,end)=(R end,R start) sends F(start)G(end) to F(R end)G(R start); commutativity and signed Fubini give the written placement. There is no unintended R on the initial argument of op.',
  'The fixed reference xRef is unchanged by momentum reversal, and y,xRef remain independent arbitrary position parameters.',
  'No claim identifies this Z with the independently existential83 kernel witness. Such an identification, Markovness and operator/L2 closure remain later work.'
 ],
 'legitimate_route_at_most_seven_steps':[
  'Extract the one global actual Z from105 once and retain its four identification/measurability clauses; specialize Q probability and J preservation at y,xRef,T.',
  'Use103 for actual nu probability and UnitExponentialProduct for actual P probability. Derive momentum R preservation from standard Gaussian negation plus position-first product mapping.',
  'Derive real strong measurability, section/product integrability bounded by CF*CG, and measurable clock expectations bounded by CG; prove the two outer L1 assertions.',
  'Use measurable integral_map and genuine signed Fubini to identify integral F(start)G(end) under actual Q with the left iterated integral.',
  'Apply J preservation to that product test; repeat the integrable transfer for F(R end)G(R start), obtaining the exact bounded signed duality.',
  'Set F=1, use clock mass1 and actual R symmetry; bounded measurable indicator tests identify the endpoint pushforward with nu. Pair this with endpoint measurability.',
  'Return both conclusions together with the original global witness clauses, without strengthening AE quantifiers or asserting path/semigroup/L2 identities.'
 ],
 'edge_cases':{'T0':'Existing initialization is parameterwise P-a.e.; statement preserves that order. Fixed-time marginal at zero follows through actual105, without a uniform all-initial-state null set.','interval_endpoints':'Raw live-arc condition uses the inherited T_n<=s<T_(n+1) convention and nonnegative elapsed subtraction. Endpoint evaluation may occur at a jump but the theorem is a distributional fixed-time assertion, not pointwise reversed path equality.','rank0':'No dimension positivity. Negation, standard Gaussian, tilted measure and bounded expectations remain valid on the one-point phase.','zero_rate_normal_or_infinite_wait':'Literal total reflection, stopping and fallback are untouched; no division by rate or support positivity.','zero_bounds':'F=0 or G=0 allowed; proofs require no division by bounds.','n0':'No new count index quantified in the export; inherited105 assembly already contains zero count and empty simplex.','signed_values':'Both observables may have either sign; explicit finite bounds discharge signed integrability. Infinite ENNReal tests from105 are used only as upstream measure facts, not substituted for signed Fubini.'},
 'topology_transfer':{'review':info(S/'independent-topology106/topology-admission106.native.json'),'effective_nodes':62,'effective_edges':122,'no_graph_change':True,'three_proposed_direct_parents':['ActualCountableEndpointLaw.actual_countable_endpoint_law','ActualPhaseNormalization.actual_phase_gibbs_normalization','UnitExponentialProduct.unit_exponential_product_laws'],'COUNT93':'Same-Z provenance through105 only; no separate direct93 witness.'},
 'scope':'Independent mathematical/type review of provisional header. Source reviewer owns primary comparison separately. No implementation, proof search, claim, Statement Seal or VERIFIED transition produced.',
 'defects':[],'readiness':'Ready for separate source/header admission and root Statement Seal when its other requirements are satisfied. Implementation and fresh exact sealed proof witness remain future work.'})
save('run106.native.json',{'reviewer':'/root/exact_verifier96','inputs':freeze['inputs'],'checks':['Original six binder block text equality with private105 statement','All37 literal lets and global identification prefix exact LF substring/hash equality with existing105 and source-only context','Global same-Z quantifier nesting and endpoint/observable domains manually inspected','Correct momentum-flip positions derived from actual pair reversal','Actual probability, measurability and signed-integrability prerequisites matched to accepted prospective route','Fresh exact-byte header typecheck under fixed Lean4.33.0, two threads, ELAN_TOOLCHAIN removed'],'result':info(O/'header-math-decision106.native.json'),'proof_compilation':False,'shared_writes':False})
save('closed-RAW106.native.json',{'reviewer':'/root/exact_verifier96','inputs':freeze['inputs'],'outputs':[info(p) for p in sorted(O.iterdir()) if p.is_file()],'no_shared_mutations':True,'no_claim_seal_or_VERIFIED':True})
for n in ['header-math-decision106.native.json','fresh-typecheck106.receipt.json','closed-RAW106.native.json']:print(n,info(O/n)['raw_sha256'])
