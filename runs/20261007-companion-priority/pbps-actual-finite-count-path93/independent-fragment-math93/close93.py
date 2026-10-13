from pathlib import Path
import hashlib,json,datetime,re
R=Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-finite-count-path93';O=B/'independent-fragment-math93'
def raw(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'raw_sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def write(name,x):
 with (O/name).open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
record=json.loads((O/'inputs93.native.json').read_text()); original=record['inputs']
assert original[0]['raw_sha256']=='4a297d7d9308a5e9d0d263e3a38894db00e245d992289f7a014335458477b296'
assert original[1]['raw_sha256']=='80db6075c4c13954abedb36e7196e61a741d486ab83e78c916a8e80ff239310a'
assert original[3]['raw_sha256']=='b2349689fb4884f8dba8941fe7d5ce5cb52bdd4862722fa0f3785bb8c543097a'
assert original[2]['raw_sha256']==original[4]['raw_sha256']
checks=[]
for lane,idx in [('count-interfaces7-instance-transport',0),('interpolation-formula1',1),('weighted-prefix3-explicit-test',3)]:
 d=B/'focused93'/lane;j=json.loads((d/'receipt.json').read_text());assert j['exit_code']==0 and j['terminal_closed'] and j['source_raw_sha256']==original[idx]['raw_sha256'];s=(d/'stdout.log').read_text();assert 'depends on axioms:' in s and 'sorryAx' not in s
 checks.append({'lane':lane,'exit_code':0,'native_receipt_hash_bound':True,'source_hash_bound':True,'reported_axioms':['propext','Classical.choice','Quot.sound'],'reviewer_recompiled_whole_file':False})
scans={}
for p in [O/'CountInterfaces93.reviewed.exactraw.lean',O/'InterpolationFormula93.reviewed.exactraw.lean',R/original[3]['path'],O/'WeightedPrefix93.reviewed.exactraw.lean']:
 hits=[{'line':i,'text':s} for i,s in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1) if re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',s)];assert not hits;scans[p.name]=hits
parents=[R/'AutoSamplingTheory/ExampleCases/ProximalBPS'/f for f in ['ActualOrderedPrefix.lean','ActualConditionalNextWaitSurvival.lean','ActualFiniteHistoryTailLaw.lean','ActualFiniteJumpRecursion.lean','ActualHarmonicFlow.lean','ActualHazardClock.lean']]+[R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean']
report={
 'schema':'bounded-independent-private-fragment-review93-v1','reviewer':'independent_math91','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checked_base_HEAD':record['head'],
 'decision':'ACCEPT_COMPILED_BOUNDED_FRAGMENTS; LIVE_JOINT_RHO_EXTENSION_MATHEMATICALLY_SOUND_BUT_NOT_COMPILE_ACCEPTED',
 'scope':{'count_interfaces':'measurable literal actual Nat.find selector; generic interval uniqueness and cardinality with explicit private premises','interpolation_formula':'prescribed Gamma greatest-eligible coordinate formula','weighted_passed_snapshot':'terminal-survival weighted actual history / history-interpolated path joint law, all ENNReal tests and mass on C','live_extension':'read-only mathematical and performance review of joint rho measurability; no full fresh compile, no interaction with root process','canonical_changes':False,'SAU93_completion':False,'source_or_decoder_acceptance':False},
 'count_audit':[
  'find_decidable_eq proves independence of DecidablePred by Subsingleton.elim and transport; this repairs kernel-instance identity rather than imposing a new model premise.',
  'measurable_first_available works on measurable countable union U and its subtype with measurable_find, then extends by zero via dite. It requires neither coverage nor uniqueness to prove measurability.',
  'actual selector uses literal eventTime from record/epsilon and I={T_n<=T<T_(n+1)}, with fallback zero. Actual76 supplies joint eventTime measurability; only original six analytic binders are present.',
  'monotone_intervals_unique is pointwise and allows equal successive times/top. It does not prove raw C disjointness until the actual C-to-interval implication is established.',
  'interval_count_cardinality identifies positive indices satisfying <=T with Ioc 0 N. Strict version uses hno for positive indices. hno is still a private conditional input, not an internally proved atomlessness theorem.',
  'At T=0 zero-clock raw samples can have N>0; no pointwise N(0)=0 claim occurs. n=0 intervals imply empty positive-index time sets under hno; stopped top values cause no count inflation.'
 ],
 'interpolation_audit':[
  'finite_fold_last_eligible follows ascending Fin.foldl_succ_last. Later ineligible records retain the accumulator; the largest eligible live record supplies the coordinate.',
  'real_time_history_fold requires all prescribed times nonnegative. The actual wrapper derives this from strict monotonicity of Fin.cons 0 t, avoiding toNNReal truncation errors.',
  'At eligible j, NNReal.coe_sub uses toNNReal(t_j)<=s, giving the real duration s-t_j. At a jump boundary the post-bounce state at j is selected.',
  'n=0 leaves record0 at time0 and yields the flow from z0; T=0 with n>0 has empty Prefix. Quantification over empty subtypes is legitimate.',
  'Gamma is the total history interpolation applied to K. The proof has no actual Z identification or count law, and needs no hidden equality assumption.'
 ],
 'weighted_audit':[
  'actual_terminal_survival_history_tests internally instantiates actual88 with measurable d(h)=T-liveTime(last h). It derives hset from actual88; generic hset is not promoted to the actual theorem binder.',
  'The private residual d is NNReal truncated subtraction on all abstract histories. On strict actual prefix C the last live time is <=T, so it has the intended elapsed-to-terminal meaning. Abstract off-support histories remain total.',
  'Stopped records contribute false survival and zero weight. Strict d<tau excludes a jump exactly at T; replacing it by <= would invalidate raw path identification later.',
  'Localization to A uses map history of P restricted to H^-1(A) intersect S. All-tests then pulls F(h,Psi(h))*W(h) through actual92 and rearranges products to q*W(K); no integrability or finite-valued-test hypothesis is needed in ENNReal.',
  'Joint history/path measure equality follows all measurable ENNReal tests and measurable graph maps, using the coordinate-product path sigma algebra. This requires no path-space measurable diagonal.',
  'Mass follows F=1 and canonical UnitExponentialProduct probability normalization. It is P(C)<=1, not a normalized conditional distribution or a count distribution.',
  'The passed snapshot contains Gamma joint measurability, and fixed-parameter rho measurability. The live extension additionally proposes joint rho measurability for each fixed n,T; it does not assert joint measurability across varying dependent Path T.',
  'At n=0,T=0 the density is 1 and empty-product comap mass is 1; raw zero clocks may fail C0 but form a canonical-P null event. No contradiction or stronger pointwise claim is introduced.'
 ],
 'live_extension_audit':{'captured_raw_sha256':original[2]['raw_sha256'],'diff':'weighted-extension93.diff','mathematics':'Joint Lambda measurability + sum-product measurable equivalence + measurable last-record evaluation yields joint W. Composing W with joint K and multiplying by joint q yields joint rho. No new premise is mathematically necessary.','additional_delta':'Adds generic terminal-record weight helper and previously reviewed real_time_history_fold; retains prior weighted all-test/map/mass proof with typed joint-map elaboration.','compile_status_at_review':'Root weighted-prefix5 process live; stdout empty at read-only snapshot. No terminal receipt observed or accepted.','process_snapshot':{'pid':48276,'cpu_seconds':351.75,'working_set_bytes':10756657152,'intervention':False},'performance_diagnosis':'Static suspicion only: convert followed by cases of p.2 last in a large literal-let theorem may generate expensive dependent abstraction/definitional reductions. Empty stdout is not a profiler location. No proven bottleneck claim.','concrete_alternative':'GenericDiagnostic93.lean proves terminal_elim_identity for independent r and terminal_measurable_transport via funext/rw. Instantiate g(p,z,u)=ofReal(exp(-Lambda(p parameters,z,u))) and r(p)=p.history(last); use the already built hg. This moves Sum case analysis outside the large actual context. No Measurable.congr API is presumed.','diagnostic_compile':json.loads((O/'generic.receipt.native.json').read_text())},
 'remaining_obligations':['Derive fixed-parameter fixed-T positive-index eventTime atomlessness; no uniform-in-T AE assertion.','Construct/use the single actual jointly measurable Z and prove raw C path equality for every coordinate.','Prove actual C implies interval membership and use positive clocks/coverage/endpoint nulls to establish AE C_n iff N=n.','Derive raw pairwise C disjointness, union probability1 and transfer the weighted C law to actual Z and N=n.','Assemble the sealed public statement and independently compile/review it before any SAU completion claim.'],
 'counterexample_guards':['Zero first clock gives a raw time0 jump: do not infer pointwise initial Z0=z0 or N0=0.','A jump at fixed horizon T selects the post-bounce phase for actual interpolation; strict terminal survival is essential for C path identity.','AE no jump at each fixed T does not imply AE no jump at every T.','Zero-count mass is generally exp(-Lambda(z0,T)); it equals1 automatically at T=0, not all T.'],
 'focused_evidence':checks,'fake_closure_source_scan':scans,'parent_interfaces_bound':[raw(p) for p in parents],
 'required_mathematical_corrections':[],'nonblocking_notes':['Count has an unused literal P let; this is harmless for selector measurability.','Interpolation wrapper retains six source assumptions although the deterministic fold identity does not use them. This is not an extra-provider binder.']}
write('fragment-math-review93.native.json',report)
outputs=[raw(p) for p in sorted(O.iterdir()) if p.is_file()]
write('closed-RAW93.native.json',{'schema':'closed-raw-input-output-manifest-v1','review_scope':'Private fragments only, no canonical or theorem completion','input_bindings':original,'parent_interfaces':[raw(p) for p in parents],'outputs':outputs,'self_exclusion':'This manifest is hashed externally; avoids recursive self-hash','mutable_input_resolution':'WeightedPrefix captured SHA is retained losslessly in owned WeightedPrefix93.reviewed.exactraw.lean and root weighted-prefix5 input snapshot; future root changes do not invalidate this captured-input review.'})
print(json.dumps({'report':raw(O/'fragment-math-review93.native.json'),'manifest':raw(O/'closed-RAW93.native.json')},indent=2))