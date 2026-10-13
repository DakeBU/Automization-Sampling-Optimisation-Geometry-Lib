import AutoSamplingTheory.TechnicalLemmas.Measure.AffineGibbs
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.FullRangeProximalGaussianOracle
import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.GibbsPositionMoment

/-! Source SPHMC2609.06906v1 Ex8 and only last TWO inequalities4.6.
Literal standardized true RGO, not Gaussian gradient output. Produce actual
normalization, affine law, C2/curvature/stationarity and genuine L2/moments.
First Gaussian Talagrand/LSI/W2 inequality, bias/MGF/fullLemma4.2, actual
algorithms/initialization/main and expected-query-cost composition remain open.
Statement and source-only topology independently sealed before proof search. -/

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOPositionFisher
open MeasureTheory InnerProductSpace Set ProbabilityTheory
open scoped NNReal
noncomputable section
set_option autoImplicit false
set_option backward.isDefEq.respectTransparency false
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

private theorem actual_standardized_calculus {V : E → ℝ} (hV : ContDiff ℝ 2 V)
    (p : E) {η : ℝ} (hη : 0 < η) :
    let rho := fun u : E => V (p+Real.sqrt η • u)-V p-
      Real.sqrt η*inner ℝ (gradient V p) u
    let Q := fun u : E => ‖u‖^2/2+rho u
    ContDiff ℝ 2 rho ∧ ContDiff ℝ 2 Q ∧
      gradient rho 0=0 ∧ gradient Q 0=0 ∧
      (∀ u v, fderiv ℝ (fderiv ℝ rho) u v v =
        η*fderiv ℝ (fderiv ℝ V) (p+Real.sqrt η • u) v v) ∧
      ∀ u v, fderiv ℝ (fderiv ℝ Q) u v v =
        ‖v‖^2+η*fderiv ℝ (fderiv ℝ V) (p+Real.sqrt η • u) v v := by
  let a := Real.sqrt η
  let rho := fun u : E => V (p+a • u)-V p-a*inner ℝ (gradient V p) u
  let Q := fun u : E => ‖u‖^2/2+rho u
  let L : E →L[ℝ] E := a • ContinuousLinearMap.id ℝ E
  have hA (u : E) : HasFDerivAt (fun x : E => p+a • x) L u := by
    convert ((hasFDerivAt_id u).const_smul a).const_add p using 1
    simp
  have hVd : Differentiable ℝ V := hV.differentiable (by norm_num)
  have hVdd : Differentiable ℝ (fderiv ℝ V) :=
    (hV.fderiv_right (m:=1) (by norm_num)).differentiable_one
  let B : E →L[ℝ] ℝ := a • innerSL ℝ (gradient V p)
  have hB (u : E) : HasFDerivAt (fun x : E => a*inner ℝ (gradient V p) x) B u := by
    exact B.hasFDerivAt
  have hrd (u : E) : HasFDerivAt rho
      (a • fderiv ℝ V (p+a • u)-B) u := by
    have he : (fderiv ℝ V (p+a • u)).comp L = a • fderiv ℝ V (p+a • u) := by
      ext v
      simp [L]
    rw [← he]
    exact (((hVd (p+a • u)).hasFDerivAt.comp u (hA u)).sub_const (V p)).sub (hB u)
  have hrfd : fderiv ℝ rho = fun u => a • fderiv ℝ V (p+a • u)-B :=
    funext (fun u => (hrd u).fderiv)
  have hrg (u : E) : gradient rho u = a • (gradient V (p+a • u)-gradient V p) := by
    apply HasGradientAt.gradient
    rw [hasGradientAt_iff_hasFDerivAt]
    have he : toDual ℝ E (a • (gradient V (p+a • u)-gradient V p)) =
        a • fderiv ℝ V (p+a • u)-B := by
      ext v
      simp [B,inner_gradient_left,mul_sub]
    rw [he]
    exact hrd u
  have hρ : ContDiff ℝ 2 rho :=
    ((hV.comp (contDiff_const.add (contDiff_id.const_smul a))).sub contDiff_const).sub
      (contDiff_const.mul (contDiff_const.inner ℝ contDiff_id))
  have hQ : ContDiff ℝ 2 Q :=
    ((contDiff_id.norm_sq (𝕜:=ℝ)).div_const 2).add hρ
  have hgQ (u : E) : gradient Q u = u+gradient rho u := by
    apply HasGradientAt.gradient
    rw [hasGradientAt_iff_hasFDerivAt]
    have hq : HasFDerivAt (fun x : E => ‖x‖^2/2) (innerSL ℝ u) u := by
      convert! ((hasFDerivAt_id u).norm_sq).const_mul (1/2 : ℝ) using 1 <;>
        first | rfl | (funext x; simp only [id_eq]; ring) | (ext v; simp)
    convert! hq.add ((hρ.differentiable (by norm_num) u).hasGradientAt.hasFDerivAt) using 1
    simp only [map_add]
    rfl
  have hrH (u v : E) : fderiv ℝ (fderiv ℝ rho) u v v =
      η*fderiv ℝ (fderiv ℝ V) (p+a • u) v v := by
    rw [hrfd]
    have hdd : HasFDerivAt (fun x => a • fderiv ℝ V (p+a • x)-B)
        (a • (fderiv ℝ (fderiv ℝ V) (p+a • u)).comp L) u := by
      exact (((hVdd (p+a • u)).hasFDerivAt.comp u (hA u)).const_smul a).sub_const B
    rw [hdd.fderiv]
    have ha2 : a*a=η := by simpa only [pow_two] using Real.sq_sqrt hη.le
    simp [L,← mul_assoc,ha2]
  have hqfd (u : E) : fderiv ℝ Q u = innerSL ℝ u+fderiv ℝ rho u := by
    have hq : HasFDerivAt (fun x : E => ‖x‖^2/2) (innerSL ℝ u) u := by
      convert! ((hasFDerivAt_id u).norm_sq).const_mul (1/2 : ℝ) using 1 <;>
        first | rfl | (funext x; simp only [id_eq]; ring) | (ext v; simp)
    exact (hq.add ((hρ.differentiable (by norm_num) u).hasFDerivAt)).fderiv
  have hQH (u v : E) : fderiv ℝ (fderiv ℝ Q) u v v =
      ‖v‖^2+η*fderiv ℝ (fderiv ℝ V) (p+a • u) v v := by
    let J : E →L[ℝ] (E →L[ℝ] ℝ) :=
      {toFun:=fun x=>innerSL ℝ x
       map_add':=by intros;ext;simp
       map_smul':=by intros;ext;simp
       cont:=(innerSL ℝ (E:=E)).continuous}
    have hρdd : Differentiable ℝ (fderiv ℝ rho) :=
      (hρ.fderiv_right (m:=1) (by norm_num)).differentiable_one
    rw [show fderiv ℝ Q=(fun x=>innerSL ℝ x+fderiv ℝ rho x) from funext hqfd]
    have hdd : HasFDerivAt (fun x => innerSL ℝ x+fderiv ℝ rho x)
        (J+fderiv ℝ (fderiv ℝ rho) u) u := J.hasFDerivAt.add (hρdd u).hasFDerivAt
    rw [hdd.fderiv]
    change inner ℝ v v+fderiv ℝ (fderiv ℝ rho) u v v = _
    rw [real_inner_self_eq_norm_sq,hrH]
  change ContDiff ℝ 2 rho ∧ ContDiff ℝ 2 Q ∧ gradient rho 0=0 ∧ gradient Q 0=0 ∧ _
  refine ⟨hρ,hQ,?_,?_,hrH,hQH⟩
  · simp [hrg]
  · simp [hgQ,hrg]

private theorem actual_standardized_law [FiniteDimensional ℝ E]
    [MeasurableSpace E] [BorelSpace E] (V : E → ℝ) {η : ℝ} (hη : 0 < η)
    (p y : E) (heq : p+η • gradient V p=y)
    (hiV : Integrable (fun x => Real.exp (-V x)) (volume : Measure E))
    (hiQ : Integrable (fun u => Real.exp (-(‖u‖^2/2+
      (V (p+Real.sqrt η • u)-V p-Real.sqrt η*inner ℝ (gradient V p) u))))
      (volume : Measure E))
    (hQprob : IsProbabilityMeasure ((volume : Measure E).tilted (fun u =>
      -(‖u‖^2/2+(V (p+Real.sqrt η • u)-V p-
        Real.sqrt η*inner ℝ (gradient V p) u))))) :
    (((volume : Measure E).tilted (fun x => -V x)).tilted
      (fun x => -‖x-y‖^2/(2*η))).map
        (fun x => (Real.sqrt η)⁻¹ • (x-p)) =
      volume.tilted (fun u => -(‖u‖^2/2+
        (V (p+Real.sqrt η • u)-V p-Real.sqrt η*inner ℝ (gradient V p) u))) := by
  let a := Real.sqrt η
  have ha : a ≠ 0 := (Real.sqrt_pos.mpr hη).ne'
  let W := fun x : E => V x+‖x-y‖^2/(2*η)
  let Q := fun u : E => ‖u‖^2/2+V (p+a • u)-V p-a*inner ℝ (gradient V p) u
  let C := V p+‖p-y‖^2/(2*η)
  have hR : ((volume : Measure E).tilted (fun x => -V x)).tilted
      (fun x => -‖x-y‖^2/(2*η)) = volume.tilted (fun x => -W x) := by
    rw [tilted_tilted hiV]
    congr 1
    funext x
    simp only [Pi.add_apply,W]
    ring
  have hF (u : E) : W (p+a • u)=Q u+C := by
    have hpy : p-y=-(η • gradient V p) := by rw [← heq]; abel
    dsimp only [W,Q,C]
    rw [show p+a • u-y=(p-y)+a • u by abel,norm_add_sq_real,
      norm_smul,Real.norm_eq_abs,mul_pow,sq_abs,inner_smul_right]
    rw [show a^2=η from Real.sq_sqrt hη.le]
    rw [hpy,inner_neg_left,inner_smul_left]
    simp only [starRingEnd_apply,star_trivial]
    field_simp [hη.ne']
    ring
  have hmap : (volume.tilted (fun x => -W x)).map (fun x => a⁻¹ • (x-p)) =
      volume.tilted (fun u => -W (p+a • u)) := by
    have h := AutoSamplingTheory.TechnicalLemmas.Measure.AffineGibbs.map_affine_gibbs
      W (-(a⁻¹ • p)) (s:=a⁻¹) (inv_ne_zero ha)
    convert! h using 1
    · congr 1
      funext x
      simp [sub_eq_add_neg,add_comm]
    · congr 1
      funext u
      simp [inv_inv,smul_add,smul_smul,ha,add_comm]
  have hconst : volume.tilted (fun u => -Q u-C) =
      (volume : Measure E).tilted (fun u => -Q u) := by
    have hQi : Integrable (fun u => Real.exp (-Q u)) (volume : Measure E) := by
      convert! hiQ using 1
      funext u
      congr 1
      dsimp [Q,a]
      ring
    have : IsProbabilityMeasure ((volume : Measure E).tilted (fun u => -Q u)) := by
      convert! hQprob using 1
      congr 1
      funext u
      dsimp [Q,a]
      ring
    rw [show (fun u => -Q u-C)=(fun u => -Q u)+(fun _ => -C) by rfl,
      ← tilted_tilted hQi]
    exact tilted_const _ (-C)
  rw [hR,hmap]
  simp_rw [hF,neg_add]
  rw [show (fun u => -Q u+ -C)=(fun u => -Q u-C) by rfl,hconst]
  congr 1
  funext u
  dsimp [Q,a]
  ring

theorem standardized_rgo_position_and_fisher
    {E S : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    [MeasurableSpace S] {V : E → ℝ} {κ : ℝ}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, κ⁻¹*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ V) x v v ∧
      fderiv ℝ (fderiv ℝ V) x v v ≤ ‖v‖^2)
    {eta : S → ℝ} {y : S → E} (heta : Measurable eta) (hy : Measurable y)
    (hpos : ∀ s, 0 < eta s) :
    ∃ p : S → E, Measurable p ∧
      (∀ s, p s+eta s • gradient V (p s)=y s) ∧
      let rho := fun s u => V (p s+Real.sqrt (eta s) • u)-V (p s)-
        Real.sqrt (eta s)*inner ℝ (gradient V (p s)) u
      let Q := fun s u => ‖u‖^2/2+rho s u
      let mu := (volume : Measure E).tilted (fun x => -V x)
      let R := fun s => mu.tilted (fun x => -‖x-y s‖^2/(2*eta s))
      let r := fun s => (R s).map (fun x => (Real.sqrt (eta s))⁻¹ • (x-p s))
      IsProbabilityMeasure mu ∧
        ∀ s, IsProbabilityMeasure (R s) ∧
          ContDiff ℝ 2 (rho s) ∧ ContDiff ℝ 2 (Q s) ∧
          gradient (rho s) 0=0 ∧ gradient (Q s) 0=0 ∧
          (∀ u v : E, 0 ≤ fderiv ℝ (fderiv ℝ (rho s)) u v v ∧
            fderiv ℝ (fderiv ℝ (rho s)) u v v ≤ eta s*‖v‖^2) ∧
          (∀ u v : E, ‖v‖^2 ≤ fderiv ℝ (fderiv ℝ (Q s)) u v v ∧
            fderiv ℝ (fderiv ℝ (Q s)) u v v ≤ (1+eta s)*‖v‖^2) ∧
          r s=(volume : Measure E).tilted (fun u => -Q s u) ∧
          IsProbabilityMeasure (r s) ∧ MemLp id 2 (r s) ∧
          Integrable (fun u => ‖u‖^2) (r s) ∧
          (∫ u, ‖u‖^2 ∂r s) ≤ Module.finrank ℝ E ∧
          MemLp (gradient (rho s)) 2 (r s) ∧
          (∫ u, ‖gradient (rho s) u‖^2 ∂r s) ≤
            (eta s)^2*(∫ u, ‖u‖^2 ∂r s) ∧
          (∫ u, ‖gradient (rho s) u‖^2 ∂r s) ≤
            (eta s)^2*Module.finrank ℝ E := by
  have ha : 0<κ⁻¹ := inv_pos.mpr (lt_of_lt_of_le zero_lt_one hκ)
  have hiV := AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability.integrable_exp_neg_of_strongConvexOn
    ha (hV.differentiable (by norm_num))
    (AutoSamplingTheory.TechnicalLemmas.Analysis.HessianStrongConvexity.strongConvexOn_univ_of_fderiv2_lower hV (fun x v => (hH x v).1))
  let mu := (volume : Measure E).tilted (fun x => -V x)
  have hmu : IsProbabilityMeasure mu := isProbabilityMeasure_tilted hiV
  have : IsProbabilityMeasure mu := hmu
  obtain ⟨p,hpm,heq,_hrest⟩ := FullRangeProximalGaussianOracle.full_range_proximal_gaussian_oracle
    hκ hV hH heta hy hpos
  let rho := fun s u => V (p s+Real.sqrt (eta s) • u)-V (p s)-
    Real.sqrt (eta s)*inner ℝ (gradient V (p s)) u
  let Q := fun s u => ‖u‖^2/2+rho s u
  let R := fun s => mu.tilted (fun x => -‖x-y s‖^2/(2*eta s))
  let r := fun s => (R s).map (fun x => (Real.sqrt (eta s))⁻¹ • (x-p s))
  refine ⟨p,hpm,heq,?_⟩
  change IsProbabilityMeasure mu ∧ _
  refine ⟨hmu,?_⟩
  intro s
  have hη : 0<eta s := hpos s
  obtain ⟨hρ,hQ,hρ0,hQ0,hρdd,hQdd⟩ := actual_standardized_calculus hV (p s) (hpos s)
  have hrhoH : ∀ u v : E, 0 ≤ fderiv ℝ (fderiv ℝ (rho s)) u v v ∧
      fderiv ℝ (fderiv ℝ (rho s)) u v v ≤ eta s*‖v‖^2 := by
    intro u v
    rw [hρdd]
    constructor
    · exact mul_nonneg (hpos s).le ((mul_nonneg ha.le (sq_nonneg ‖v‖)).trans (hH _ v).1)
    · exact mul_le_mul_of_nonneg_left (hH _ v).2 (hpos s).le
  have hQH : ∀ u v : E, ‖v‖^2 ≤ fderiv ℝ (fderiv ℝ (Q s)) u v v ∧
      fderiv ℝ (fderiv ℝ (Q s)) u v v ≤ (1+eta s)*‖v‖^2 := by
    intro u v
    rw [hQdd]
    constructor
    · exact le_add_of_nonneg_right (mul_nonneg (hpos s).le ((mul_nonneg ha.le (sq_nonneg ‖v‖)).trans (hH _ v).1))
    · nlinarith [mul_le_mul_of_nonneg_left (hH (p s+Real.sqrt (eta s) • u) v).2 (hpos s).le]
  let beta : ℝ≥0 := ⟨1+eta s,by positivity⟩
  have hβ : (1:ℝ≥0)≤beta := by change 1≤1+eta s; linarith [hpos s]
  have hHQ : ∀ u v : E, ((1:ℝ≥0):ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ (Q s)) u v v ∧
      fderiv ℝ (fderiv ℝ (Q s)) u v v ≤ (beta:ℝ)*‖v‖^2 := by
    change ∀ u v : E, 1*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ (Q s)) u v v ∧
      fderiv ℝ (fderiv ℝ (Q s)) u v v ≤ (1+eta s)*‖v‖^2
    simpa only [one_mul] using hQH
  obtain ⟨hqp,hiq,_hqpos,hip,_hpair,_heqd,hbd⟩ :=
    GibbsPositionMoment.gibbs_position_moment (by norm_num : (0:ℝ≥0)<1) hβ hQ hHQ (0:E) hQ0
  have hlaw : r s=(volume : Measure E).tilted (fun u => -Q s u) :=
    actual_standardized_law V (hpos s) (p s) (y s) (heq s) hiV hiq hqp
  have hpr : IsProbabilityMeasure (r s) := hlaw.symm ▸ hqp
  have hipos : Integrable (fun u => ‖u‖^2) (r s) := by
    rw [hlaw]
    simpa only [sub_zero] using hip
  have hbound : (∫ u, ‖u‖^2 ∂r s) ≤ Module.finrank ℝ E := by
    rw [hlaw]
    simpa only [sub_zero,NNReal.coe_one,div_one] using hbd
  have hlp : MemLp id 2 (r s) :=
    (memLp_two_iff_integrable_sq_norm (by fun_prop)).mpr hipos
  let b : ℝ≥0 := ⟨eta s,(hpos s).le⟩
  have hHρ : ∀ u v : E, ((0:ℝ≥0):ℝ)*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ (rho s)) u v v ∧
      fderiv ℝ (fderiv ℝ (rho s)) u v v ≤ (b:ℝ)*‖v‖^2 := by
    change ∀ u v : E, 0*‖v‖^2 ≤ fderiv ℝ (fderiv ℝ (rho s)) u v v ∧
      fderiv ℝ (fderiv ℝ (rho s)) u v v ≤ eta s*‖v‖^2
    simpa only [zero_mul] using hrhoH
  have hlip : LipschitzWith b (gradient (rho s)) := by
    simpa only [NNReal.coe_zero,zero_div,zero_mul,add_zero] using (AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
      (r:=0) hρ hHρ (0:E)).2
  have hpoint (u : E) : ‖gradient (rho s) u‖^2 ≤ (eta s)^2*‖u‖^2 := by
    have h := hlip.norm_sub_le u 0
    rw [hρ0,sub_zero,sub_zero] at h
    have hs := (sq_le_sq₀ (norm_nonneg _) (mul_nonneg (hpos s).le (norm_nonneg u))).mpr h
    simpa only [mul_pow] using hs
  have hgcont : Continuous (gradient (rho s)) := hlip.continuous
  have hif : Integrable (fun u => ‖gradient (rho s) u‖^2) (r s) := by
    apply (hipos.const_mul ((eta s)^2)).mono' (by fun_prop)
    filter_upwards with u
    rw [Real.norm_eq_abs,abs_of_nonneg (sq_nonneg _)]
    exact hpoint u
  have hlf : MemLp (gradient (rho s)) 2 (r s) :=
    (memLp_two_iff_integrable_sq_norm hgcont.aestronglyMeasurable).mpr hif
  have hfp : (∫ u, ‖gradient (rho s) u‖^2 ∂r s) ≤
      (eta s)^2*(∫ u, ‖u‖^2 ∂r s) := by
    rw [← integral_const_mul]
    exact integral_mono hif (hipos.const_mul ((eta s)^2)) hpoint
  have hfd : (∫ u, ‖gradient (rho s) u‖^2 ∂r s) ≤ (eta s)^2*Module.finrank ℝ E :=
    hfp.trans (mul_le_mul_of_nonneg_left hbound (sq_nonneg _))
  have hiR : Integrable (fun x => Real.exp (-‖x-y s‖^2/(2*eta s))) mu := by
    apply (integrable_const (1:ℝ)).mono' (by fun_prop)
    filter_upwards with x
    rw [Real.norm_eq_abs,abs_of_nonneg (Real.exp_pos _).le]
    apply Real.exp_le_one_iff.mpr
    exact div_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr (sq_nonneg _)) (by positivity)
  have hRp : IsProbabilityMeasure (R s) := isProbabilityMeasure_tilted hiR
  exact ⟨hRp,hρ,hQ,hρ0,hQ0,hrhoH,hQH,hlaw,hpr,hlp,hipos,hbound,hlf,hfp,hfd⟩

end
end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.StandardizedRGOPositionFisher
