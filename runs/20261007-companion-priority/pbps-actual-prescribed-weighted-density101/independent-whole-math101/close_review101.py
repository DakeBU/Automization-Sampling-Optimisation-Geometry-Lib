from pathlib import Path
import hashlib,json,re,datetime
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;P=B.parent/'pbps-weighted-density-preread101'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def load(p):return json.loads(p.read_bytes())
def save(n,x):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode());return info(p)
prep=load(O/'prepared-inputs101.native.json')
for r in prep['inputs']:
 assert info(R/r['path'])['raw_sha256']==r['raw_sha256'],r['path']
 assert (R/r['path']).read_bytes()==(R/r['snapshot']).read_bytes()
old=P/'independent-header-math101/closed-RAW-review101.native.json';prior=load(old)
for r in prior['inputs']+prior['files']:assert info(R/r['path'])['raw_sha256']==r['raw_sha256'],r['path']
assert load(O/'fresh-kernel-receipt101.native.json')['exit_code']==0
assert load(O/'fake-closure-and-axioms101.native.json')['status']=='PASS'
M=R/prep['production']['path'];src=M.read_text(encoding='utf8')
decls=re.findall(r'^(private )?(theorem|def) ([A-Za-z_]+)',src,re.M)
assert decls==[('private ','def','actual_prescribed_weighted_density_statement'),('','theorem','actual_prescribed_weighted_density_balance')]
parents=[('ActualPrescribedPathReversal.actual_prescribed_path_reversal_and_survival','100: rho coordinates and reversed survival integral.'),('ActualPrescribedStateReversal.actual_prescribed_state_reversal_and_rate_product','99: rho99 coordinates and incoming-rate product equality.'),('ActualPrescribedGibbsSurvival.actual_prescribed_gibbs_survival_balance','98: Gibbs weight times forward survival equals terminal Gibbs weight times momentum-reversed survival.'),('ActualPrescribedPathDensity.actual_prescribed_path_density_rewrite','94: actual q*terminalweight equals ofReal(exp(-I)*P), used at both original and reversed inputs.')]
decision={
 'kind':'independent-whole-mathematical-review101',
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'reviewer':'/root/exact_verifier96',
 'decision':'ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL_TARGET',
 'production':info(M),'header':prep['header'],'statement_seal':prep['seal'],
 'exact_target':{'literal_binders_and_Prop_equal_to_header_and_seal':True,'fresh_kernel_witness_applies_public_theorem_to_original_expanded_Header_candidate':True,'entire_production_freshly_elaborated_as_exact_byte_prefix':True,'target_module_not_imported':True,'six_source_binders':['hα','hαβ','hV','hH','hη','hβη'],'typing':'Finite-dimensional real inner-product space with Borel measurable structure, including rank zero.','excess_public_premises':[]},
 'module_ownership':{'top_level_declarations':[dict(kind=k,private=bool(p),name=n) for p,k,n in decls],'new_auxiliary_helpers':0,'private_statement':'Literal Header101 proposition; exact first20 public94 definitions retained. The public theorem is the sole proof export.','local_ingredients':'halign,hprod,hint,hbal,hw,hs,hreal,hd are actual internally proved ingredients, not supplied hypotheses. No dead top-level helper or mangled private producer API.'},
 'definition_audit':{'rho_density':'The original actual density remains q(y,r,z,n,T,t)*weight(y,r,K(last),d). It has not been redefined as ofReal(dReal); hd proves the bridge from actual94.','dynamics':'Literal c,Phi,S,rate,Lambda,Rec,Hist,Delta,Prefix,zAt,K,qReal,q,liveTime,d,weight,Path,Psi,Gamma,rhoDensity match public94 and sealed Header101.','products':'P uses exactly n incoming pre-bounce arrival rates. The terminal arc contributes survival through I but has no additional event-rate factor.','target_energy':'U=V(x)+||x-y||²/(2η)+||p||²/2, w=exp(-U); no shifted conserved harmonic energy or omitted η factor.','path_integral':'I uses the same clamped actual Gamma on real time and real Lebesgue interval integral as94/98/100.','endpoint':'A is the actual Gamma at T, including the final harmonic arc; reverse initial phase is R A.'},
 'proof_audit':[
 {'lines':[118,132],'finding':'Obtain rho from100 and rho99 from99. halign proves equality by function extensionality, subtype extensionality and both public coordinate equations. After substitution all later projections use one common witness. This does not rely on implementation transparency of100 or add a compatibility premise.'},
 {'lines':[134,136],'finding':'hprod projects99 incoming product equality. Fin.succ_castSucc, Fin.snoc_castSucc and Fin.cons_succ identify its explicit arc-grid factors with literal P in both directions. No post-bounce-rate substitution or final arrival factor appears.'},
 {'lines':[138,142],'finding':'The fourth conjunction from100 is exactly I(reverse)=integral rate(R Gamma(s)). Correct clamp, horizon, original terminal A and common rho are retained. It is the integral conclusion, not an invalid pointwise assertion at jumps.'},
 {'lines':[143,150],'finding':'The fourth98 conclusion gives exp(-U(z))*exp(-Iforward)=exp(-U(A))*exp(-Iminus). hw derives w(RA)=w(A) using unchanged position and norm_neg on momentum. Rewriting hw and hint gives hs with correct negative signs and weights.'},
 {'lines':[152,156],'finding':'Unfold dReal, rewrite reversed P to original P and reassociate products. hs then yields real weighted density equality. This remains valid when one or every event rate is zero, since no factor is divided or cancelled.'},
 {'lines':[158,164],'finding':'hd selects actual94 fourth right-associated conjunct .2.2.2, which is rhoDensity=ofReal(exp(-whole integral)*incoming product). Fin.snoc_castSucc closes its exact P adapter. Applying it at both inputs and ofReal_mul with Real.exp_nonneg converts the real equality to the requested actual ENNReal equality. No positivity of P or dReal is required by that API.'}
 ],
 'direct_consumed_public_producers':[{'declaration':'AutoSamplingTheory.ExampleCases.ProximalBPS.'+n,'use':why} for n,why in parents],
 'direct_parent_count':4,
 'scope_and_constants':'Unnormalized pointwise real and ENNReal weighted densities under the same complemented/reversed finite event tuple. All six assumptions and sqrtη, inverse sqrtη, bounce2, kinetic1/2, proximal1/(2η), survival negative exponent and T-t_rev are exact. No measure equality, Jacobian, normalizer, n! or stationary invariance is asserted.',
 'degenerate_cases':{'n_zero':'Fin0 product is1 and all coordinate alignment proofs remain valid by empty function extensionality. The density is the terminal survival factor, and the nontrivial survival balance is supplied by98/100.','T_zero':'For n=0, A=z, I=0, density1 and the identity reduces to weight parity; for n>0 Prefix is empty. No T>0 binder is added.','rank_zero':'Allowed; momentum flip and energy parity still hold. For n>0 rate factors vanish and both products/densities are0; n=0 remains valid.','zero_normal':'Literal total bounce is unchanged; no division by a nonzero normal is introduced in the assembly.','zero_rate':'Products may vanish; every algebraic step uses multiplication/equality only.','endpoints_and_jumps':'Original strict event times stay interior. Only100 survival integrals are consumed; no all-time path identity at genuine jumps or outside the horizon is claimed.'},
 'negative_trial_and_visibility':{'evidence':info(O/'preserved-trials101.native.json'),'first_failure':'Incorrect94 conjunction projection is retained as a failed elaboration trial with its sorryAx diagnostic. It is not accepted proof evidence.','corrected_projection':'assembly2 .2.2.2 and production2-private both match the actual public94 density clause.','visibility_change':'production1 differs from reviewed production2 only by making the literal statement def private. No proof, header or formula changed.'},
 'fresh_kernel':info(O/'fresh-kernel-receipt101.native.json'),
 'fake_closure_and_axioms':info(O/'fake-closure-and-axioms101.native.json'),
 'reused_header_and_topology_manifest':info(old),
 'defects_found':[],
 'remaining_truth_boundary':'Mathematical acceptance only. Independent final source/exposition and anonymous decoder admission, exact science commit verification, sole-lane integration, reader acceptance and purification remain separate. Weighted sector measure/integral substitution, normalized stationary averaging, invariance and the whole paper/Goal remain outside this theorem.',
 'no_VERIFIED_transition':True,'no_shared_or_production_edit':True,'no_new_full_primary_archive':True
}
result=save('whole-math-decision101.native.json',decision)
files=[info(x) for x in sorted(O.rglob('*')) if x.is_file()]
manifest=save('closed-RAW-manifest101.native.json',dict(kind='closed-independent-whole-math-review101',inputs=[{k:v for k,v in r.items() if k!='snapshot'} for r in prep['inputs']],reused_closed_manifests=[info(old)],files=files,closed=True,hash_algorithm='SHA256 exact original bytes',self_hash_intentionally_omitted=True))
print(json.dumps(dict(decision=result,kernel=info(O/'fresh-kernel-receipt101.native.json'),manifest=manifest),indent=2))
