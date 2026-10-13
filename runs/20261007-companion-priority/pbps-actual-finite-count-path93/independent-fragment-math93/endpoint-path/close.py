from pathlib import Path
import hashlib,json,re,datetime
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-finite-count-path93';O=B/'independent-fragment-math93/endpoint-path'
def raw(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def write(name,x):
 with (O/name).open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
inputs=json.loads((O/'inputs.native.json').read_text()); receipts=[]
for n in ['ActualEndpointNullity93','ActualPathIdentification93']:
 j=json.loads((O/(n+'.type.receipt.native.json')).read_text());assert j['exit_code']==0 and j['source_unchanged'];s=(O/(n+'.type.stdout.log')).read_text();assert 'sorryAx' not in s
 axioms=re.findall(r'depends on axioms:\s*\[([^]]*)\]',s);assert axioms
 for a in axioms:assert set(re.findall(r'[\w.]+',a))=={'propext','Classical.choice','Quot.sound'}
 assert not (O/(n+'.type.stderr.log')).read_bytes()
 receipts.append({'receipt':raw(O/(n+'.type.receipt.native.json')),'elapsed_seconds':j['elapsed_seconds'],'axiom_sets':[a.split() for a in axioms],'full_type_printed':True})
parents=[R/'AutoSamplingTheory/ExampleCases/ProximalBPS'/n for n in ['ActualOrderedPrefix.lean','ActualFiniteJumpRecursion.lean','ActualPhysicalTimeMeasurability.lean']]+[R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',R/'.lake/packages/mathlib/Mathlib/MeasureTheory/Constructions/Pi.lean']
review={
 'schema':'bounded-independent-endpoint-path-fragment-review93-v1','reviewer':'independent_math91','checked_base_HEAD':inputs['head'],'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'decision':'ACCEPT_BOTH_BOUNDED_PRIVATE_FRAGMENTS','required_corrections':[],
 'scope':{'source_or_decoder_verdict':False,'SAU_verified':False,'proved_local_transition':False,'production_changes':False,'canonical_changes':False,'previous_native_reviews_overwritten':False},
 'exact_targets':[raw(B/'ActualEndpointNullity93.lean'),raw(B/'ActualPathIdentification93.lean')],
 'binder_and_definition_audit':[
  'Both actual wrappers retain precisely the original six analytic conditions hAlpha,hAlphaBeta,hV,hH,hEta,hBetaEta, with finite-dimensional real inner-product Borel infrastructure. No endpoint-nullity, path-equality, density, coverage or independence provider has become an actual theorem premise.',
  'Literal harmonic flow, reflection, integrated rate, hitting clock, live/stopped recursive records, canonical infinite product expMeasure(1), epsilon=toNNReal, and actual finite histories agree with the accepted Header93 context.',
  'Private generic interfaces carry hmono/hstrict/hlaw or hZ only locally. Actual endpoint proof produces them from actual76/77/92; actual path proof produces hZ from actual80 and terminal bound from literal recursion and C survival.'
 ],
 'endpoint_nullity':{
  'conclusion':'For every fixed y,xRef,z0,T, P-almost every w avoids eventTime_j=T for all positive natural j. Parameter and horizon universal quantifiers are outside AE; the countable j universal is inside.',
  'proof_checks':[
   'subtype_coordinate_null bounds comap measure of a subtype coordinate fiber by ambient product-volume hyperplane measure. It works for arbitrary D; no unasserted measurability of D is needed for this upper bound. i:Fin n excludes an illegal zero-dimensional coordinate.',
   'weighted_map_coordinate_null uses withDensity absolute continuity even for extended-valued q, then evaluates measurable history pushforward equality at the observed-coordinate level set. No finiteness or integrability assumption is silently used.',
   'actual76 gives pointwise event-time monotonicity. actual77 supplies AE positivity simultaneously for all exponential coordinates; actual76 then gives strict consecutive live times. Finite endpoint below T+1 forces all previous records live by monotonicity, so the actual strict prefix guard is obtained internally.',
   'The law is applied to n+1 events at horizon T+1, not T. Therefore the possibly occurring T endpoint lies inside the larger strict simplex and is legitimately tested as a coordinate hyperplane. This avoids excluding the endpoint by assumption.',
   'The observed last record under K is exactly the last real simplex coordinate. Strict simplex positivity justifies Real.coe_toNNReal without truncation. A stopped readTime=0 cannot contaminate T=0 because the localized history guard forces the last record live.',
   'The localized zero-measure endpoint events are upgraded using the AE guard, and ae_all_iff takes only a countable intersection over positive event indices. There is no AE intersection over uncountably many T or parameters.'
  ],
  'boundary_cases':'T=0 is included: use the larger horizon1 and positive-index hyperplane at0. j=0 is intentionally excluded since record0 has time0. Stopped event times are top and cannot equal finite T.',
  'consumed_parents':['ActualFiniteJumpRecursion.actual_fixed_reference_finite_jump_recursion','UnitExponentialProduct.unit_exponential_product_laws','ActualOrderedPrefix.actual_ordered_prefix_law']
 },
 'path_identification':{
  'conclusion':'There exists one jointly measurable global Z with actual80 raw covered/fallback formulas and AE initial value, such that for every n,T,y,xRef,z0 and every raw w in C_n, Psi(history(w)) equals the entire coordinate-product path s↦Z(s,w).',
  'proof_checks':[
   'The single Z is obtained before all n,T and parameter quantification from actual80. No separate witness is chosen per horizon or per path coordinate.',
   'finite_history_fold_eq_process selects Nat.findGreatest of eligible times among0..n. record0 at0 ensures eligibility exists; every prefix record is live. The next index is ineligible either by greatestness or, at n, by T<eventTime_(n+1).',
   'The ascending Fin.foldl equals the value at the greatest eligible record, then actual80 raw interval formula identifies that value with Z(s). This argument needs no endpoint nullity and no AE exceptional-set intersection.',
   'terminal_event_after is valid even when lastTime>T, since T<=truncated(T-lastTime)+lastTime; finite q and q=top are handled separately. On actual C the stricter intended time ordering is also present, but no unjustified subtraction cancellation is used.',
   'Literal recursion converts strict residual survival into T<eventTime_(n+1). It handles infinite waiting clock via stopped next record/top eventTime. Thus terminal equality at T cannot enter C.',
   'funext s produces actual equality of the whole function on the horizon subtype. It assumes neither a measurable diagonal in path space nor a stronger Skorokhod/Borel path topology.',
   'The generic hZ scalar formula is supplied internally by actual80, not by an assumption of equality between prescribed and actual paths. The raw C guard provides all live records; extra strict-order/cutoff conjuncts may be unused by this stronger generic finite-fold argument without weakening the final conclusion.'
  ],
  'boundary_cases':['n=0 uses record0 at0 and strict first-clock survival, so equality holds on raw C0 for all s<=T.','At T=0,n>0, actual strict prefix C is empty; at n=0 the only coordinate0 is identified on C0. Zero-clock raw samples can lie outside C0, so AE initial equality is not incorrectly strengthened to a pointwise statement.','At internal bounce times the largest eligible index is selected, hence the post-bounce phase. Future records beyond n do not affect the already covered intervals.'],
  'consumed_parent':'ActualPhysicalTimeMeasurability.actual_physical_time_measurable_phase'
 },
 'fresh_kernel_checks':receipts,
 'negative_diagnostic_preserved':{'receipt':'ActualEndpointNullity93.receipt.native.json','exit_code':4294967295,'reason':'Reviewer used #print with pp.explicit/pp.deepTerms, unnecessarily requesting the full large proof. Stopped only independently verified owned PID38520 after65.297s, retained command-line snapshot and receipt, then used #check full types in successor files. This is a reviewer diagnostic, not a mathematical or source compile failure.','root_process_touched':False},
 'fake_closure_scan':'No axiom/sorry/admit/Prop:=True/:=trivial source closure; fresh declarations report only propext, Classical.choice, Quot.sound.',
 'remaining_boundary':['These private fragments close fixed-T endpoint avoidance and raw C path identification; they do not themselves close the sealed whole93 proposition.','Still assemble and verify AE C_n iff literal Nat.find N=n, raw C disjointness, union mass1 and finite strict/weak cardinality conclusions using the actual interval/coverage interfaces.','Transfer compiled terminal-weighted C joint law to this same actual Z and count event N=n; retain all ENNReal tests, joint pushforward and density/mass conclusions.','Final public assembly, sealed-statement equality, source/decoder and canonical acceptance remain separate future checks.'],
 'parent_source_hashes':[raw(p) for p in parents]
}
write('endpoint-path-review93.native.json',review)
write('closed-RAW93.native.json',{'schema':'closed-raw-input-output-manifest-v1','inputs':inputs['inputs']+[raw(p) for p in parents],'outputs':[raw(p) for p in sorted(O.iterdir()) if p.is_file()],'self_excluded':True,'scope':'bounded private endpoint/path ingredients; no canonical transition'})
print(json.dumps({'review':raw(O/'endpoint-path-review93.native.json'),'manifest':raw(O/'closed-RAW93.native.json')},indent=2))