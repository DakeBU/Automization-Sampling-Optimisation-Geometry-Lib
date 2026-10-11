from pathlib import Path
import hashlib,json,datetime
R=Path('E:/Samplinglib');D=R/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94/independent-fragment-math94'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def js(n,x):
 p=D/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return info(p)
c=json.loads((D/'input-and-literal-check94.native.json').read_bytes())
f=json.loads((D/'fresh-checks94.native.json').read_bytes())
for row in c['inputs']:assert info(R/row['path'])==row,row['path']
assert f['mathlib_commit']=='db584cd6d46c92f209a44c0f1c829460d327499d'
assert all(r['exit_code']==0 for r in f['checks'])
audit={
 'schema_version':1,'kind':'INDEPENDENT_PARTIAL_MATHEMATICS_AND_KERNEL_REVIEW',
 'reviewer':'/root/independent_whole_math93','author':'companion_root_20261005',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'decision':'ACCEPT_EXACT_ANALYSIS_FRAGMENT',
 'source':f['source'],'checked_head':f['checked_head'],
 'scope':'Three generic finite-arc lemmas; actual93 to clamped open-arc adapter; actual_analysis proving exactly the sealed94 interval-integrability, n+1 hazard-sum and incoming phase/rate left-limit conjuncts.',
 'not_a_whole_SAU_verdict':True,
 'statement_seal':'Header94 remains RAW283fef6c66240aec21c4f34c72442d85e25db3f95dde1104a96cb3fe7d04e832. Independent extraction from frozen header agrees character-for-character with actual_analysis type after newline decoding and removal of only the final density conjunct.',
 'kernel':{'fragment_fresh_compile_exit':0,'literal_sealed_first_three_witness_exit':0,'witness_method':'Append the independently extracted literal sealed first-three statement to the exact scratch snapshot; close with exact actual_analysis under the same six hypotheses. No target edits or additional premise.','all_five_fragment_theorem_axioms':['propext','Classical.choice','Quot.sound'],'witness_axioms':['propext','Classical.choice','Quot.sound'],'source_scan':'No sorry, admit, axiom declaration, native_decide, unsafe or implemented_by found. Full source inspected for hidden conclusion providers and fake closures.','standard_environment':'Pinned Lean4.33.0 via bundled lake; ELAN_TOOLCHAIN removed; pinned manifest and Mathlib db584cd6d46c92f209a44c0f1c829460d327499d.'},
 'mathematical_review':[
  {'declaration':'PBPSFiniteArcAnalysis94.arc_integral','result':'PASS','reason':'For a<=b, continuous g is interval integrable. EqOn on Ioo transfers integrability via congr_uIoo after uIoo_of_le and transfers the integral via integral_congr_Ioo_of_le. Lebesgue endpoints have zero measure; arbitrary f endpoint values and a=b cause no missing premise.'},
  {'declaration':'PBPSFiniteArcAnalysis94.incoming_left_limit','result':'PASS','reason':'For a<b, Ioo(a,b) is a left neighborhood of b. Continuity of g gives its left limit g(b), and eventual equality transfers it to f. This is valid for arbitrary target topology, without Hausdorff or endpoint-agreement assumptions.'},
  {'declaration':'PBPSFiniteArcAnalysis94.finite_arc_integral','result':'PASS','reason':'Induction includes the zero-arc base. In the successor step, castSucc restricts the first n arcs and last n gives the final arc. Monotonicity supplies ordered endpoints. IntervalIntegrable.trans and adjacent integral addition join the pieces; Fin.sum_univ_castSucc exactly splits the finite sum. Repeated partition points are allowed.'},
  {'declaration':'PBPSActualArc94.actual_arc','result':'PASS','reason':'The adapter derives monotonicity of snoc(cons0 t,T) from Prefix strict ordering and all t_i<T, with only nonnegative T needed for the initial point. For s in each open arc, hgrid bounds0<=s<=T, hclipcoe removes the clamp, and hafter establishes that every later record is ineligible. It then consumes precisely the maximum-eligible-record path clause of accepted actual_finite_count_path_law. It does not assume open-arc agreement or an actual-path provider as a binder.'},
  {'declaration':'PBPSActualAnalysis94.actual_analysis','result':'PASS','reason':'Imported actual harmonic-flow and bounce-rate theorems provide ordinary finite-dimensional phase continuity under the original six assumptions. Composition yields continuous fixed-state arc rates. finite_arc_integral supplies interval integrability and the finite arc integral sum. integral_comp_sub_right translates each arc to0 and coe_toNNReal uses nonnegative duration. Strict Prefix spacing selects the incoming arc for each left limit; composition with continuous rate gives the rate limit.'}
 ],
 'index_and_endpoint_review':{
  'grid':'grid has n+2 entries [0,t1,...,tn,T]; j:Fin(n+1) indexes n+1 arcs. grid(j.castSucc)=a_j and grid(j.succ)=a_(j+1). Last arc is from t_n toT.',
  'incoming':'i:Fin n selects event t_(i+1); i.castSucc selects z_i; i.castSucc.castSucc selects a_i. hnext uses succ_castSucc, snoc_castSucc and cons_succ to identify the following endpoint exactly with t.val i.',
  'n_zero':'The actual proof invokes finite_arc_integral with one arc, from0 toT. No event left limits are demanded. The generic zero-arc case is also sound.',
  'T_zero':'For n=0, both endpoints coincide and interval integrability and zero hazard identity hold. For n>0 Prefix is empty. No proof step incorrectly assumes T>0 globally.',
  'jump_endpoints':'No equality with an incoming arc is demanded at an event; Gamma chooses the post-bounce state there. Finite-null endpoint changes justify the hazard integral, while a genuine left neighborhood gives the incoming phase/rate limit.',
  'terminal_endpoint':'T enters the final integral endpoint. Open-arc agreement is sufficient and does not omit terminal survival time from the hazard sum.',
  'rank_zero_zero_rate':'Neither the generic argument nor the adapters divide by a rate or assume nontrivial E. Continuous zero rates and singleton phase spaces are included. Zero-normal reflection remains the already fixed total Lean definition.',
  'coordinate_path_semantics':'The same coordinate-product path carrier and pointwise interpolation from93 are used. No Skorokhod topology, continuous full path, measurable joint evaluation on the uncountable path carrier, or new path-space regularity premise appears. The only continuity is that of finite-dimensional flow/rate and each fixed arc.',
  'clock_cases':'The conclusion is deterministic for prescribed positive ordered tuples. No AE quantifier change, actual finite-wait premise, raw zero-clock exclusion or new stochastic assumption is introduced.'
 },
 'dependency_truth_boundary':{'actual93':'Consumes the already accepted exact finite-count path theorem only for its prescribed path formula; accepted source RAW5467078f497e0d40e1916550b2e5e9a5be992a69b20fc143bda06dd988d86d9d rehashed.','continuity':'ActualHarmonicFlow.actual_harmonic_flow_laws and ActualBounceRate.actual_bounce_rate_energy_laws supply continuity, not hidden public hypotheses. Both exact dependency files are hashed.','prior_header_audit':'Reused only after exact header/production comparison and pinned prior audit/manifest hashes; fresh fragment proof review and kernel witness are new evidence.'},
 'mathematical_defects':[], 'necessary_repairs':[], 'API_polish_blockers':[],
 'remaining_outside_review':['final density exponential/product algebra','production assembly and exact complete public statement','whole module/source-blind decoding and primary-source review','publication and full SAU94 independent verification','countable A7 assembly and whole Goal'],
 'transfer_condition':'This credit applies to exact fragment RAWff2a0d8881e34e3ff9d7f9c8397a4cf4e7fa8f915f988e955e0f6f5e65ced18f. Later production reuse requires exact-body/type transfer or a fresh delta review; this partial audit is not a whole-SAU VERIFIED event.',
 'ledger_changed':False,'production_written':False,'outputs_only_owned_directory':True,
 'evidence':{'inputs':c['inputs'],'fresh_checks':info(D/'fresh-checks94.native.json'),'literal_match':info(D/'input-and-literal-check94.native.json'),'axioms':[info(D/'fragment.axioms.native.json'),info(D/'sealed-first-three.axioms.native.json')]}
}
a=js('fragment-math-decision94.native.json',audit)
manifest={'schema_version':1,'kind':'CLOSED_RAW_INDEPENDENT_FRAGMENT_REVIEW','hash_recipe':'SHA256 of exact bytes before parsing/newline normalization. Manifest excludes itself and is externally reported.','decision':'ACCEPT_EXACT_PARTIAL_FRAGMENT_ONLY','inputs':c['inputs'],'outputs':[info(p) for p in sorted(D.iterdir()) if p.is_file()],'closure':'All files in owned directory prior to manifest creation enumerated; no production or canonical writes. Kernel trials both passed.'}
m=js('closed-RAW-fragment94.native.json',manifest)
for row in manifest['inputs']+manifest['outputs']:assert info(R/row['path'])==row
assert {p.name for p in D.iterdir() if p.is_file()}=={Path(r['path']).name for r in manifest['outputs']}|{'closed-RAW-fragment94.native.json'}
print(json.dumps(dict(status='PASS',audit=a,manifest=m),indent=2))
