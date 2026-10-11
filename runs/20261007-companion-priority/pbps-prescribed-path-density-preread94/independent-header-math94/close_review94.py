from pathlib import Path
import json, hashlib, datetime
ROOT=Path('E:/Samplinglib')
OUT=ROOT/'runs/20261007-companion-priority/pbps-prescribed-path-density-preread94/independent-header-math94'
def sha(b):return hashlib.sha256(b).hexdigest()
def info(p):
    b=p.read_bytes()
    return {'path':p.relative_to(ROOT).as_posix(),'raw_sha256':sha(b),'bytes':len(b)}
def write(name,x):
    p=OUT/name
    assert not p.exists(),str(p)
    p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
comparison=json.loads((OUT/'literal-compatibility94.native.json').read_bytes())
inputs=comparison['all_inputs']
for i in inputs:assert info(ROOT/i['path'])==i,i['path']
elaboration=json.loads((OUT/'header-elaboration94.native.json').read_bytes())
assert elaboration['exit_code']==0
assert elaboration['mathlib_commit']=='db584cd6d46c92f209a44c0f1c829460d327499d'
graphbase=ROOT/'runs/20261007-companion-priority/pbps-actual-finite-count-path93/next-source-graph94'
graphmanifest=json.loads((graphbase/'closed-RAW-manifest94.native.json').read_bytes())
for row in graphmanifest['outputs']:assert info(ROOT/row['path'])==row
audit={
 'schema_version':1,
 'kind':'INDEPENDENT_PREPROOF_MATHEMATICAL_STATEMENT_AUDIT',
 'reviewer':'/root/independent_whole_math93',
 'author_distinct_from_reviewer':True,
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'decision':'ACCEPT_PREPROOF_STATEMENT_NO_REQUIRED_MATHEMATICAL_REPAIR',
 'target':inputs[0],
 'compatibility_target':inputs[1],
 'truth_boundary':{'candidate_is':'A prospective Prop definition with four conjunctive mathematical conclusions, not an inhabitant of that proposition.','elaboration':'Fresh fixed-toolchain EXIT0 establishes well-formedness only. Axiom output [propext, Classical.choice, Quot.sound] pertains to the definition, not a proved density theorem.','mathematical_review':'Independent analytic and indexing review supports the proposed proposition; Lean proof remains outstanding.','source_role':'Compare to the independently source-derived local graph94; no replacement of independent primary-source fidelity review.','completion_credit':False,'source_or_theorem_seal_created':False,'production_or_canonical_changes':False,'proof_search_performed':False,'SAU_transition_performed':False},
 'literal_compatibility':{'status':'PASS','shared_lets':20,'binder_text':'Six analytic proof binders plus all ambient typeclass and parameter binders agree with path93.','comparison':'All20 shared let definitions equal exactly after newline decoding; original byte hashes independently pinned.','new_representation':'Only the extended endpoint grid and clamped real-time path are introduced after the same finite-path and rho definitions.','rho':'Exactly the existing q times terminal survival weight at the last prescribed record. No provider, alternate kernel, or assumed density introduced.'},
 'quantifier_audit':[
  'For each admissible finite tuple the statement is deterministic and pointwise: all y, xRef, z0, n, T and t in Prefix n T. There is no probability-space almost-everywhere quantifier and hence no exchange of all-T AE with AE all-T.',
  'Prefix requires strict ordering of [0,t1,...,tn] and each event strictly below T. No extra realizability, positive-rate, finite-clock, non-explosion or nonzero-rank premise is imposed.',
  'Continuity/integrability/left limits are conclusions or consequences of C2 and the finite construction, not extra theorem binders. The proof-valued binders being unused in the Prop definition is ordinary: the future proof must use their content as needed.'
 ],
 'finite_index_audit':{
  'notation':'Write a0=0, a_(k+1)=t(k), a_(n+1)=T, and z_j=zAt(j).',
  'grid':'grid:Fin(n+2)->R is [a0,...,a_(n+1)] via snoc(cons 0 t,T).',
  'hazard_sum':'j:Fin(n+1) has j.castSucc value j and j.succ value j+1; the summand is Lambda(z_j,a_(j+1)-a_j), including terminal j=n.',
  'jump_factor':'i:Fin n has value i; i.castSucc:Fin(n+1) selects z_i, and i.castSucc.castSucc:Fin(n+2) selects a_i. Thus t(i)-grid(i.castSucc.castSucc)=a_(i+1)-a_i, the incoming arc length.',
  'nonnegative_coercions':'All event and segment times are nonnegative, strictly positive except the permitted n=0,T=0 segment; toNNReal and truncated NNReal subtraction therefore agree with real durations. The terminal d is T-a_n.'
 },
 'clamp_and_left_limit_audit':{
  'agreement':'For any real s with0<=s<=T, coercing min(toNNReal s,T) back to R gives s, so gamma is exactly the prescribed Gamma at that physical time.',
  'outside_domain':'The extension is constant at Gamma(0) for s<0 and Gamma(T) for s>T. No behavior outside the physical interval enters the interval integral.',
  'extension_independence':'For any event a_(i+1), strict0<a_(i+1)<T supplies an open neighborhood inside (0,T). Every extension agreeing on [0,T] coincides there, so its left limits at that event agree with this clamped extension. This follows from the specified definition; no additional premise is necessary.',
  'incoming_neighborhood':'On (a_i,a_(i+1)), the final eligible record is i; gamma(s)=Phi(s-a_i,z_i). Continuity in s gives the stated phase left limit, and continuity of rate gives its rate left limit.',
  'jump_value':'At an event the <= selection chooses the reflected post-state. The header correctly uses the incoming limit, not rate(gamma(event)). No continuity across bounces is asserted.',
  'endpoints':'No left-limit demand at initial0 or terminalT. The final arc includesT; finite endpoint values do not change its interval integral.',
  'proof_exposition_obligation':'When this proposition is proved and explained, make the clamp agreement and interior-neighborhood equivalence explicit to discharge graph94 extension convention. This is not a requested header repair.'
 },
 'integrability_and_density_audit':[
  'C2 implies continuous gradient. The displayed rate is continuous and nonnegative, and each fixed-state harmonic arc is continuous. Reflection need not be a globally continuous map: each finite prescribed post-state is fixed while traversing an arc.',
  'There are n+1 finite compact arcs. Their rate compositions are integrable on their compact intervals. Finite endpoint modifications identify their joined function with the clamped-path rate, giving interval integrability without a global energy bound or an uncountable evaluation-measurability premise.',
  'Translate each arc integral by a_j, then add the finite partition. This gives exactly the sum over n+1 Lambda terms and includes terminal survival.',
  'The original qReal is the finite product of incoming nonnegative rate factors times exp(-Lambda_j), j=0,...,n-1. Multiplying terminal weight contributes exp(-Lambda_n). Nonnegativity permits multiplication through ENNReal.ofReal; exponential addition gives exp(-sum Lambda_j) times the product of incoming rates. Substituting the integral sum gives the exact proposed rho identity.',
  'No cancellation, division by a rate, logarithm of a rate, or strict rate positivity is needed. All finite real integrals and exponential factors are finite. Zero-rate factors remain zero.',
  'The rate normalization sqrt(eta), harmonic scaling, reflection coefficient2 and negative sign in the exponential are unchanged from path93. This is the full density of the prescribed finite-count path term, including survival after the last jump.'
 ],
 'degenerate_cases':{
  'n_zero_T_positive':'Fin0 product is1, left-limit conjunction is vacuous, grid=[0,T], Gamma(s)=Phi(s,z0). Density is exp(-Lambda(z0,T)), generally not1.',
  'n_zero_T_zero':'grid=[0,0]; no strict-grid assertion is made. The integral and sole hazard are0; rho=1. Clamped gamma is constant at z0.',
  'n_positive_T_zero':'Prefix is empty since its first event must satisfy0<t0<T=0; universal conclusion is vacuous.',
  'rank_zero':'The phase space is singleton, gradients and rates vanish. Prescribed paths still exist. n=0 density1 and n>0 density0. No nontriviality assumption is smuggled in.',
  'zero_normal':'The Lean reflection formula is total under division by0 and leaves momentum unchanged when the normal is0. The associated rate is0. The candidate introduces no singular inverse assumption.',
  'zero_rate_or_infinite_actual_wait':'A prescribed tuple is defined even when its actual-clock probability is0. Zero incoming rate kills the density; actual infinite waits are not forbidden by this deterministic statement.',
  'raw_zero_clocks':'No raw clock is quantified here. Positive ordered tuples are the same support parameterization as path93; its separately accepted AE endpoint/zero-clock analysis is neither strengthened nor bypassed.'
 },
 'scope_against_graph94':{'matched_nodes':['PATHINT94','STITCH94','LEFT94','RHO94','ALG94','DENSITY94','ZERO94'],'SIGMA94':'No stronger path-space topology or joint evaluation measurability is assumed. Only the explicit finite path receives a scalar rate integral.','not_delivered':['Lean proof of candidate','TERM93 substitution into actual finite-count law','countable assembly and full A7','signed or arbitrary unbounded test extension','whole paper or Goal completion'],'source_graph_outputs_rehashed':True},
 'issues':[],
 'counterexamples_to_candidate_found':[],
 'necessary_repairs':[],
 'retained_trial':'trial1 bookkeeping expected21 shared lets instead of20; retained script/snapshot/failure receipt. Trial2 fixed reviewer count only and passed; no candidate modification.',
 'evidence':{'literal_comparison':info(OUT/'literal-compatibility94.native.json'),'fresh_elaboration':info(OUT/'header-elaboration94.native.json'),'inputs':inputs}
}
write('header-math-audit94.native.json',audit)
outputs=[info(p) for p in sorted(OUT.iterdir()) if p.is_file()]
manifest={'schema_version':1,'kind':'CLOSED_RAW_PREPROOF_MATH_AUDIT_MANIFEST','hash_recipe':'SHA256 of exact bytes before parsing, newline decoding or normalization. Manifest excludes itself; RAW reported externally.','reviewer':'/root/independent_whole_math93','status':'PREPROOF_AUDIT_ACCEPTED_NO_THEOREM_COMPLETION','inputs':inputs,'outputs':outputs,'closure':'All files in the owned directory before creation of this manifest are enumerated. Failed trial artifacts retained. Only owned-directory files written.'}
write('closed-RAW-manifest94.native.json',manifest)
print(json.dumps({'audit':info(OUT/'header-math-audit94.native.json'),'manifest':info(OUT/'closed-RAW-manifest94.native.json')},indent=2))
