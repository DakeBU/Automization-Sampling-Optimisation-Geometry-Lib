from pathlib import Path
import json,hashlib,datetime,re
R=Path('E:/Samplinglib');O=Path(__file__).resolve().parent;B=O.parent;P=B.parent/'pbps-finite-path-reversal-preread100'
def info(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def load(p):return json.loads(p.read_bytes())
def save(n,x):
 p=O/n;assert not p.exists();p.write_bytes((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
 return info(p)
prep=load(O/'prepared-inputs100.native.json')
for r in prep['inputs']:
 assert info(R/r['path'])['raw_sha256']==r['raw_sha256']
 assert (R/r['path']).read_bytes()==(R/r['snapshot']).read_bytes()
reused=[]
for manifest in [B/'independent-fragment-math100/arc/closed-RAW-arc100.native.json',P/'independent-header-math100/closed-RAW-original100.native.json',P/'independent-header-math100/topology-overlay100/closed-RAW-topology-admission100.native.json']:
 d=load(manifest)
 for r in d.get('inputs',[])+d.get('files',[]):
  assert info(R/r['path'])['raw_sha256']==r['raw_sha256'],r['path']
 reused.append(info(manifest))
receipt=load(O/'fresh-kernel-receipt100.native.json');assert receipt['exit_code']==0
assert load(O/'fake-closure-and-axioms100.native.json')['status']=='PASS'
M=R/prep['production']['path'];src=M.read_text(encoding='utf8')
decls=re.findall(r'^(private )?(theorem|def) ([A-Za-z_]+)',src,re.M)
assert [x[2] for x in decls]==['active_arc','path_reversal','scalar_reflection','actual_prescribed_path_reversal_statement','actual_prescribed_path_reversal_and_survival']
parents=[
 ('ActualPrescribedStateReversal.actual_prescribed_state_reversal_and_rate_product','Single rho witness, coordinate equation and intermediate reverse post/arrival state laws; first state pair used.'),
 ('ActualFiniteCountPath.actual_finite_count_path_law','Actual prescribed Gamma live-arc evaluation, applied to the original and reversed literal arrays.'),
 ('ActualHarmonicFlow.actual_harmonic_flow_laws','All-real flow composition with the exact actual Phi.'),
 ('ActualPhaseReversalVolume.actual_phase_reversal_volume_laws','Momentum reversal involution and R Phi R = Phi(-time).'),
 ('ActualPrescribedPathDensity.actual_prescribed_path_density_rewrite','Forward interval-integrability projection on reversed actual input.')]
decision={
 'kind':'independent-whole-mathematical-review100',
 'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'reviewer':'/root/exact_verifier96',
 'decision':'ACCEPT_WHOLE_MATHEMATICS_AND_EXACT_SEALED_KERNEL_TARGET',
 'production':info(M),'header':prep['header'],'statement_seal':prep['seal'],
 'exact_target':{'literal_binders_and_Prop_equal_to_header_and_seal':True,'fresh_kernel_witness_applies_public_theorem_to_original_expanded_Header_candidate':True,'target_module_not_imported':True,'entire_production_freshly_elaborated_as_exact_byte_prefix':True,'six_source_binders':['hα','hαβ','hV','hH','hη','hβη'],'typing':'Finite-dimensional real inner product space with its Borel measurable structure, including rank zero.','excess_public_premises':[]},
 'private_module_ownership':[
  {'declaration':'active_arc','lines':[15,24],'status':'Reused unchanged accepted fragment, apart from private visibility and namespace. Maximum finite index selects the last eligible arc; no hidden monotonicity premise.'},
  {'declaration':'path_reversal','lines':[26,74],'status':'Reused unchanged accepted fragment. Closed-horizon off-event reversal follows from grid complements, states, actual arc equations, flow group and involutive reversal. No arbitrary path/provider premise escapes the private helper.'},
  {'declaration':'scalar_reflection','lines':[76,92],'status':'New helper independently reviewed. Finite N is null even for restricted Lebesgue measure; AE restriction to uIoc is within Icc because T>=0. Integrability transfers by AE congruence, then comp_sub_left and symmetry remove time reflection. Integral substitution has bounds T-T=0 and T-0=T, so no negative sign remains.'},
  {'declaration':'actual_prescribed_path_reversal_statement','lines':[95,153],'status':'Exact sealed literal, with actual c/Phi/S/Rec/Hist/Delta/Prefix/m/zAt/K/Path/Psi/Gamma/R/rate and clamped original/reversed real paths. The unused measure m remains exact source context; no volume assertion is silently added.'},
  {'declaration':'actual_prescribed_path_reversal_and_survival','lines':[156,254],'status':'All generic premises discharged internally by literal arrays and the five public producers listed below. The actual terminal A is Gamma(T), never an arbitrary endpoint provider.'}
 ],
 'actual_discharge_audit':[
  {'lines':[168,179],'finding':'A single actual99 application returns rho, hrho and h99. The public conclusion reuses that rho and hrho; hpair is the first pair from h99 at j. Thus coordinate and state laws cannot accidentally concern different reversal maps.'},
  {'lines':[180,189],'finding':'Local hbl/hbr use Fin.cases/lastCases, rev_succ/rev_castSucc and the exact hrho equation. Initial and terminal complement cases reduce to 0 and T; no private99 name is called.'},
  {'lines':[190,205],'finding':'The snoc grid is monotone because the prefix cons grid is strictly monotone, every event is below T, and 0<=T. Last-index cases and castSucc comparisons are explicitly covered.'},
  {'lines':[206,224],'finding':'Actual93 supplies Gamma live-arc interpretation. On Icc(0,T), toNNReal(s)<=T and its real coercion is s, so the clamp is exactly s. harc applies the producer to any actual start w and prefix u; original z,t and reverse R A,rho t are then substituted.'},
  {'lines':[225,245],'finding':'ActualFlow supplies all-real hgroup; actual96 supplies hR and hrev in the required order. path_reversal receives the literal Phi, R, actual post arrays, actual gamma/barGamma and their harc laws. The helper event condition reduces exactly to s!=(rho t).val i.'},
  {'lines':[246,254],'finding':'Actual94 first projection gives interval integrability of rate(barGamma), with exactly the same real clamp. The finite set is range((rho t).val); nonmembership yields every off-event inequality with correct equality orientation. Applying scalar_reflection to f(s)=rate(R(gamma(s))) and g(s)=rate(barGamma(s)) proves the second integrability and the stated whole integral equality.'}
 ],
 'direct_consumed_public_producers':[{'declaration':'AutoSamplingTheory.ExampleCases.ProximalBPS.'+n,'use':why} for n,why in parents],
 'direct_parent_count':5,
 'no_direct97_or98_theorem_use':True,
 'scalar_measure_and_sign_checks':{'measure':'Lebesgue volume on real time, restricted to the interval for AE transfer. Finite event set is null, with no density or jump-rate positivity premise.','integrability':'The real-valued function has finite endpoint norm, satisfying comp_sub_left default finiteness. Reflection twice reduces to the original function and interval symmetry changes T..0 to 0..T.','integral':'integral_comp_sub_left f T gives integral of f(T-s) over 0..T equal to integral f over 0..T; no Jacobian factor other than absolute one.','T_zero':'uIoc is empty and both integrals are zero. No division by T occurs.'},
 'endpoint_and_degenerate_cases':{'s_zero_and_T':'Both are included in the helper and actual harc discharge. Strict prefixes have no endpoint events; at zero the reversed path starts at R Gamma(T), while at T the reverse terminal equals R of the original start. No timepoint outside Icc is asserted.','n_zero':'One arc remains and event range is empty. The argument requires no positive event count.','T_zero_positive_n':'Strict prefix is empty, so the universally quantified input case is vacuous; n=0 still gives its single endpoint.','rank_zero':'No positive dimension assumption.','zero_normal':'Literal total Lean division in S is unchanged; no nonzero normal is introduced by this proof.','zero_rate':'No rate division or positivity premise is used.'},
 'source_alignment':'Exact accepted Header100 and base-plus-overlay topology retained. The event exclusion preserves the right-continuous jump convention. This is the off-event path and survival-integral component needed by later weighted A8 assembly, not weighted invariance itself.',
 'fresh_kernel':info(O/'fresh-kernel-receipt100.native.json'),
 'fake_closure_and_axioms':info(O/'fake-closure-and-axioms100.native.json'),
 'reuse':reused,
 'defects_found':[],
 'remaining_truth_boundary':'Independent final source/exposition/decoder admission and exact-science-commit verification are still separate. No weighted density/sector, invariant probability, restart, whole-paper or Goal completion follows from this review.',
 'no_VERIFIED_transition':True,'no_shared_or_production_edit':True,'no_new_full_primary_archive':True
}
save('whole-math-decision100.native.json',decision)
files=[info(x) for x in sorted(O.rglob('*')) if x.is_file()]
manifest=save('closed-RAW-manifest100.native.json',dict(kind='closed-independent-whole-math-review100',inputs=[{k:v for k,v in r.items() if k!='snapshot'} for r in prep['inputs']],reused_closed_manifests=reused,files=files,closed=True,hash_algorithm='SHA256 exact original bytes',self_hash_intentionally_omitted=True))
print(json.dumps({'decision':info(O/'whole-math-decision100.native.json'),'kernel':info(O/'fresh-kernel-receipt100.native.json'),'manifest':manifest},indent=2))
