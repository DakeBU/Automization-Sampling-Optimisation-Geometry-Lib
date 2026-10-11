from pathlib import Path
import hashlib,json,datetime
R=Path('E:/Samplinglib');D=R/'runs/20261007-companion-priority/pbps-actual-prescribed-path-density94/independent-whole-math94'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def js(n,x):
 p=D/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return info(p)
c=json.loads((D/'literal-transfer94.native.json').read_bytes());f=json.loads((D/'fresh-checks94.native.json').read_bytes())
inputs=c['inputs']+[info(R/'.lake/packages/mathlib/Mathlib/Data/ENNReal/Real.lean')]
for i in inputs:assert info(R/i['path'])==i,i['path']
assert all(r['exit_code']==0 for r in f['checks'])
assert f['mathlib_commit']=='db584cd6d46c92f209a44c0f1c829460d327499d'
audit={
 'schema_version':1,'kind':'INDEPENDENT_WHOLE_MATHEMATICS_KERNEL_REVIEW',
 'reviewer':'/root/independent_whole_math93','formalizer':'companion_root_20261005','independent_of_proof_author':True,
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'decision':'ACCEPT_EXACT_WHOLE_MATHEMATICAL_THEOREM',
 'production':inputs[0],
 'public_theorem':'AutoSamplingTheory.ExampleCases.ProximalBPS.ActualPrescribedPathDensity.actual_prescribed_path_density_rewrite',
 'checked_commit_boundary':{'head_observed':f['checked_head'],'theorem_at_review':'Exact worktree RAW snapshot; new production is not claimed committed by this review.','credit_binding':'RAW5065f542feea7024214159903ad3e7b81f6df9a6fcbf46afecace49397d786a0,40379 bytes.'},
 'accepted_statement':{'assumptions':'Exactly the original six analytic assumptions and finite-dimensional real Hilbert/Borel typing, including rank zero. No rate-positivity, integrability, left-limit, stochastic-provider, or density identity premise added.','quantification':'For all y,xRef,z0,n,T and every strict prescribed tuple0<t1<...<tn<T, using the same20 literal definitions as path93 and the sealed clamped real extension.','conclusions':['IntervalIntegrable of the path rate on0..T.','Its integral equals the sum of the n+1 translated arc hazards, including the terminal arc.','At every prescribed event, the phase and scalar rate left limits are the incoming arc phase and rate.','The existing rho=q times terminal survival equals ENNReal.ofReal(exp(-integral0..T rate(gamma))*product of incoming rates).'],'literal_seal':'Complete expanded public theorem type equals the original Header94 statement after newline decoding and changing the Prop-definition wrapper to a theorem colon; all binders and20 definitions unchanged. Fresh literal kernel witness closes by the public theorem.'},
 'fresh_kernel_checks':{'exact_production_snapshot_exit':0,'exact_sealed_whole_witness_exit':0,'inventory':'Six private theorems and one public theorem. All seven plus independent witness printed axioms.','axioms':['propext','Classical.choice','Quot.sound'],'fake_closure':'Lexical scan and full relevant source review found no sorry/admit/axiom declarations/Prop:=True/:=trivial/native_decide/unsafe/implemented_by, hidden conclusion provider, or self-justifying wrapper. Public theorem combines genuine analysis and algebra.','environment':'Pinned bundled Lean4.33.0 lake, ELAN_TOOLCHAIN removed, fixed lake-manifest, Mathlibdb584cd6d46c92f209a44c0f1c829460d327499d.','retained_negative_trial':'First reviewer witness was placed outside production namespace without re-opening notation scopes and failed parsing at NNReal notation. Retained exact witness/log/receipt; trial2 adds only opens to the witness environment. Production compilation passed initially; no production or statement repair was needed.'},
 'fragment_transfer':{'accepted_fragment_raw':'ff2a0d8881e34e3ff9d7f9c8397a4cf4e7fa8f915f988e955e0f6f5e65ced18f','accepted_decision_raw':'9534ad803ef25cb44a62832e96de173483f25972caa6ed8f57ebb9d2db980027','method':'Exact comparison of each of arc_integral, incoming_left_limit, finite_arc_integral, actual_arc and actual_analysis, after newline decoding and only removing private modifier/scratch namespace qualifiers. No proof-body or theorem-type edits.','result':'PASS; previous mathematical reasoning transfers, and all five bodies were freshly elaborated in the complete production snapshot.','analysis_summary':'Finite-null endpoint congruence gives each arc integral. Induction stitches the finite partition. Path93 maximum-eligible-record interpolation identifies the clamped path on each open arc. Flow/rate continuity yields integrability and incoming left limits. No continuous-across-bounce assumption.'},
 'new_algebra_review':[
  {'component':'product_survival','result':'PASS','detail':'The real identity holds for arbitrary finite rate and hazard arrays: distribute product(r_i*exp(-h_i)), replace the exponential product by exp(sum(-h_i)), combine the terminal exponential, split Fin(n+1) sum into castSucc terms plus last, and commute real multiplication. No sign assumption, cancellation, rate division or logarithm is required. The n=0 identity retains exactly its terminal exponential.'},
  {'component':'r and h indexing','result':'PASS','detail':'r_i is rate(Phi(t_(i+1)-a_i,z_i)); h_j is Lambda(z_j,a_(j+1)-a_j), for a=[0,t1,...,tn,T]. hstep identifies grid(i.castSucc.succ) with t.val i. hq then matches each original qReal product term to r_i*exp(-h_(i.castSucc)) using snoc_castSucc. No shifted or omitted arc.'},
  {'component':'terminal duration hlast0/hlastT/htail','result':'PASS','detail':'Monotonicity of cons0 t gives a_n>=0. For n=0 a_n=0<=T; for n=k+1 a_n=t_k<T. Hence toNNReal a_n<=T and NNReal subtraction is genuine real T-a_n. NNReal.eq, coe_sub and coe_toNNReal prove T-toNNReal(a_n)=toNNReal(T-a_n). This treats n=0 and T=0 without requiring positive T.'},
  {'component':'hweight','result':'PASS','detail':'The last K record is live with state z_n and timestamp toNNReal(a_n). Unfolding weight,d,K selects exp(-Lambda(z_n,T-a_n)); htail and succ_last/snoc_last/snoc_castSucc identify this exactly with exp(-h(last n)). No stopped/dead-record branch is silently substituted: prescribed K consists of live records by definition.'},
  {'component':'ENNReal transport and final assembly','result':'PASS','detail':'ENNReal.ofReal_mul\u0027 requires only nonnegativity of the second real factor, supplied by exp_pos. Thus the product of existing prefix density and survival weight equals ofReal of their real product. Apply hq, product_survival and the already proved hsum. This is the original rho, not a newly defined density. Zero incoming rates remain zero, and the exponential sign and sqrt(eta) rate normalization are unchanged.'}
 ],
 'edge_case_and_path_review':{
  'n_zero':'Empty rate product1, grid[0,T], phase Phi_s(z0), rho=exp(-Lambda(z0,T)); it is generally not1 for positive T.',
  'n_zero_T_zero':'Single zero-length arc, integral0, terminal duration0, empty rate product1 and rho1. No strict-grid assertion is introduced.',
  'n_positive_T_zero':'No Prefix tuple exists because its first event must lie strictly between0 andT=0.',
  'rank_zero':'Rates and hazards vanish; n=0 density1 and n>0 density0. No nontriviality assumption appears.',
  'zero_rates_zero_normal_infinite_waits':'Formula remains valid with zero incoming rate. Total reflection at zero normal is preserved. A prescribed finite tuple need not be achievable by actual clocks; no finite-wait hypothesis is introduced.',
  'endpoint_convention':'At jump times the actual prescribed path is post-bounce. Incoming limits are taken through the preceding open arc. Finite endpoint values do not alter hazard integration. Terminal T is included as the final integral endpoint.',
  'clamp':'The clamp agrees with Gamma on[0,T]. At each strict event it is locally inactive, so left limits are independent of how the path is extended outside[0,T]. No left-limit requirement is made at0 orT.',
  'coordinate_sigma':'Path carrier remains coordinate-product. The proof concerns explicit fixed finite paths and finite-dimensional phase continuity; it adds no Skorokhod/Borel-on-path-space or uncountable joint evaluation measurability premise.',
  'quantifiers':'This is a deterministic pointwise tuple theorem. No all-T/AE interchange and no change to path93 fixed-horizon stochastic assertions.'
 },
 'actual_dependencies':[
  {'declaration':'ActualFiniteCountPath.actual_finite_count_path_law','use':'Its existing prescribed-path last-eligible-record formula establishes actual_arc. No new arbitrary path-law provider.'},
  {'declaration':'ActualHarmonicFlow.actual_harmonic_flow_laws','use':'Joint finite-dimensional flow continuity supplies fixed-state arc continuity.'},
  {'declaration':'ActualBounceRate.actual_bounce_rate_energy_laws','use':'Rate continuity supplies continuous arc rates and passage to the incoming rate limit.'},
  {'declaration':'Mathlib interval-integral, finite sum/product, Real.exp and ENNReal APIs','use':'Finite-null endpoint congruence, left-neighborhood transfer, interval translation/addition, finite exponential product algebra and nonnegative ofReal multiplication.'}
 ],
 'source_and_delivery_boundaries':{'source_fidelity_verdict':False,'authored_exposition_review':'Pending separate scope-bounded request and exact bytes.','not_delivered':['countable summation over all finite counts giving full A7','signed-observable convergence or arbitrary path functional extension','new stochastic law beyond prior path93','Skorokhod identification','whole PBPS paper or four-paper Goal completion'],'SAU_VERIFIED_transition':False,'ledger_changed':False,'production_modified_by_reviewer':False},
 'issues':[],'necessary_repairs':[],
 'evidence':{'inputs':inputs,'literal_transfer':info(D/'literal-transfer94.native.json'),'fresh_checks':info(D/'fresh-checks94.native.json'),'all_axioms':info(D/'sealed-whole-trial2.axioms.native.json')}
}
a=js('whole-math-decision94.native.json',audit)
manifest={'schema_version':1,'kind':'CLOSED_RAW_WHOLE_MATHEMATICS_KERNEL_REVIEW','reviewer':'/root/independent_whole_math93','status':'ACCEPT_EXACT_WHOLE_MATH_NO_SOURCE_OR_SAU_TRANSITION','hash_recipe':'SHA256 of exact bytes before parsing or newline normalization. Manifest excludes itself; external RAW reported.','inputs':inputs,'outputs':[info(p) for p in sorted(D.iterdir()) if p.is_file()],'closure':'Every file in owned directory before manifest creation enumerated, including failed reviewer witness trial. No production/canonical/ledger writes.'}
m=js('closed-RAW-whole94.native.json',manifest)
for row in manifest['inputs']+manifest['outputs']:assert info(R/row['path'])==row
assert {p.name for p in D.iterdir() if p.is_file()}=={Path(r['path']).name for r in manifest['outputs']}|{'closed-RAW-whole94.native.json'}
print(json.dumps(dict(status='PASS',audit=a,manifest=m),indent=2))
