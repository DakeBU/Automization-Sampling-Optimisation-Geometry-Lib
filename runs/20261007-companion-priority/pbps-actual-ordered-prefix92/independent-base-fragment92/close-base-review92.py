import hashlib,json,pathlib,re,subprocess
from datetime import datetime,timezone
R=pathlib.Path('E:/Samplinglib');B=R/'runs/20261007-companion-priority/pbps-actual-ordered-prefix92';D=B/'independent-base-fragment92'
def bind(p):
 b=p.read_bytes();return dict(path=p.as_posix(),raw_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def put(name,v):
 p=D/name
 with p.open('x',encoding='utf-8',newline='\n') as f:
  if isinstance(v,str):f.write(v)
  else:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
 return p
source=B/'Base92.lean';assert bind(source)['raw_sha256']=='52a2f48c6fe64d18b7f408cf0c9b18d89d2d4fa3612b44fea5c93bab5e7b71f2'
s=source.read_text(encoding='utf-8');seal=read(B/'root.statement-seal92.json');prop=seal['expanded_literal_Prop']
assert s[s.index('    let c :'):s.index('    ∀ T :')]==prop[prop.index('    let c :'):prop.index('    ∀ n :')]
assert re.findall(r'\((h[^\s:]+)\s*:',s[:s.index('    let c :')])==['hα','hαβ','hV','hH','hη','hβη']
clean=re.sub(r'/\-[\s\S]*?\-/','',s);assert not re.search(r'\b(sorry|admit|axiom)\b|Prop\s*:=\s*True|:=\s*trivial',clean)
receipt=read(D/'kernel.receipt.json');assert receipt['exit_code']==0
log=(D/'kernel.stdout.log').read_text();assert ': error' not in log
assert 'depends on axioms: [propext,\n Classical.choice,\n Quot.sound]' in log
paths=[source,B/'root.statement-seal92.json',B/'focused/base2-subtype-domain/receipt.json',R/'AutoSamplingTheory/TechnicalLemmas/Probability/UnitExponentialProduct.lean',R/'lake-manifest.json',R/'lean-toolchain',R/'.astis/toolchain/lean-4.33.0-windows/bin/lake.exe',R/'.astis/toolchain/lean-4.33.0-windows/bin/lean.exe']
inputs=[bind(p) for p in paths]
report={
 'schema_version':1,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),
 'decision':'ACCEPT_INTERNAL_N0_ALL_ENNREAL_TEST_INTEGRAL_BASE_ONLY',
 'checked_HEAD':subprocess.run(['git','rev-parse','HEAD'],cwd=R,capture_output=True,text=True,check=True).stdout.strip(),
 'inputs':inputs,'source':bind(source),
 'statement_scope':'actual_prefix_base_integral proves the sealed integral identity only at n=0, for every NNReal T, y,xRef,z0 and every measurable F:Hist0->ENNReal. Complete induction, measure equality and all-n law remain unaccepted here.',
 'seal_audit':{'22_outer_literal_lets_exact':True,'original_six_analytic_binders_retained':True,'extra_density_or_probability_provider':False,'same_literal_H_B_K_q_m_P':True},
 'proof_audit':[
  {'step':'actual history','finding':'h0 is the one-record history with live(0,z0). Every j:Fin1 equals0, and Nat.rec at0 establishes history(w)=h0 pointwise for every raw w. No clock-support assumption or supplied process-law equality is used.'},
  {'step':'actual prefix event','finding':'hA proves h0 lies in A0T: live is explicit, strict monotonicity on Fin1 is vacuous, and all horizon tests range over empty Fin0. hB therefore proves the actual pullback event equals univ for every T, including0.'},
  {'step':'simplex','finding':'hDelta proves Delta0T=univ in the ambient type Fin0->Real by the same vacuity. No condition0<T enters the base case.'},
  {'step':'subtype measure','finding':'hm starts from map_comap_subtype_coe for the original subtype Delta0T and finite-product volume. Delta measurability follows hDelta. Applying both measures to univ and map_apply with measurable_subtype_coe derives the original m0T(univ)=volume(Delta0T). Only conv_rhs at hmass rewrites Delta0T to univ. The subtype-domain of m0T is never replaced with the different subtype Set.univ.'},
  {'step':'empty-product mass','finding':'Ambient volume on Fin0->Real is definitionally Measure.pi of real volume over empty Fin0. Measure.pi_univ and Fin.prod_univ_zero give mass1. The subtype mass is derived, not stipulated.'},
  {'step':'prescribed history','finding':'For every t:Prefix0T, all j:Fin1 are0, so Fin.cons0 and Fin.induction base give K(t)=h0 exactly, including both time and phase.'},
  {'step':'density','finding':'q0T(t)=ENNReal.ofReal of the empty real product=1, by unfolding q and qReal. There is no rate factor, final-survival factor, normalization or density-law premise at n0.'},
  {'step':'canonical probability','finding':'P remains literal Measure.infinitePi(fun _:Nat=>expMeasure1). Its IsProbabilityMeasure instance is obtained from UnitExponentialProduct.unit_exponential_product_laws.1, which has exactly the same literal P. Only probability normalization is consumed; positive-clock support, independence and divergence are not needed for the base proof.'},
  {'step':'all tests','finding':'With B=univ, H=K=h0, q=1 and both masses1, lintegral_const reduces both sides to F(h0). The theorem retains measurable F as the sealed admissibility condition, although constancy makes that witness unnecessary in this proof. Values infinity or0 are valid; no integrability, boundedness, finite-value, or positive-event-probability assumption appears.'}
 ],
 'boundary_cases':[
  'T0 has the same empty simplex coordinate and initial history as any T>=0. The strict-prefix convention is E0=Omega, not a0<T survival condition.',
  'All raw clock sequences are allowed, including zero/negative coordinates; no event clock is consumed at n0.',
  'Rank0 E and zero hazard remain covered because only the initial phase appears.',
  'The result concerns the complete initial tagged history, not an endpoint-position substitute.',
  'The local hm equality is true for the original comap measure. The proof does not silently redefine Prefix0T or declare an arbitrary singleton measure.'
 ],
 'direct_ASTIS_proof_ingredient':{'name':'AutoSamplingTheory.TechnicalLemmas.Probability.UnitExponentialProduct.unit_exponential_product_laws','projection':'.1','use':'IsProbabilityMeasure of literal canonical infinite Exp(1) product'},
 'kernel':{'receipt':bind(D/'kernel.receipt.json'),'exit_code':0,'duration_seconds':receipt['duration_seconds'],'full_private_type_printed':True,'axioms':['propext','Classical.choice','Quot.sound'],'no_placeholder_closure':True},
 'mathematical_repair_required':False,'findings_requiring_changes':[],
 'remaining_open':'The successor integral step, literal concrete recursion/density adapters, complete all-n integral theorem, measure pushforward equality and final sealed-public-theorem assembly remain outside this acceptance. This is not a whole-SA U/proof/source/publication acceptance.',
 'canonical_or_production_changes':False
}
decision=put('base-fragment-review92.native.json',report)
put('base-fragment-review92.md','''# Independent n=0 integral-base review92

Accepted the frozen Base92.lean fragment for every horizon T>=0, including0, and every measurable ENNReal test of the complete initial history. All22 outer definitions exactly match the seal; no probability or density provider was added.

The proof derives H0=K0=live(0,z0), B0=univ, Delta0=univ and q0=1. It derives m0(univ)=1 from map/comap, restricted volume and the empty finite product. The rewrite of Delta0 to univ is restricted to the right-hand measure expression; the original simplex subtype remains the domain of m0. Canonical P normalization uses only UnitExponentialProduct.unit_exponential_product_laws.1. Both integrals reduce to F(initial history), including when that value is infinity.

Fresh pinned Lean compilation and full type/axiom inspection passed (exit0,11.109s), using only propext, Classical.choice and Quot.sound. No repairs needed. The successor step, all-n density law and measure equality remain open. No canonical or production changes were made.
''')
outputs=[bind(p) for p in sorted(D.iterdir()) if p.is_file()]
manifest=put('base-review-closed-RAW92.native.json',{'schema_version':1,'closed':True,'reviewer':'/root/independent_math91','utc':datetime.now(timezone.utc).isoformat(),'inputs':inputs,'outputs':outputs,'closure':'Owned base-fragment review and fresh check outputs only; excludes own bytes. Input/canonical files unchanged. Internal n0 acceptance only.'})
print(json.dumps({'decision':bind(decision),'manifest':bind(manifest)},indent=2))
