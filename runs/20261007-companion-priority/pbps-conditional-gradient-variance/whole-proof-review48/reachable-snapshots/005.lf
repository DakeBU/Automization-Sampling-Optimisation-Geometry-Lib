import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel
import AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar
import Mathlib.Tactic.Module
import Mathlib.Probability.Kernel.Composition.Prod
import AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization
import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexGibbsIntegrability
import Mathlib.Analysis.Calculus.ParametricIntegral
import Mathlib.Analysis.Calculus.Deriv.Inv

/-!
# Reflected Gaussian conditional expectation and its derivative

Source: arXiv:2609.06905v1, Appendix C.1, the conditional density and
the differentiation step preceding the conditional variance estimate.
The score below differentiates the unnormalized log weight. Its centered
covariance is the derivative of the normalized conditional expectation.
This does not prove conditional Poincare, the L2 extension or coercivity.
-/

open MeasureTheory ProbabilityTheory
open MeasureTheory InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Analysis
open scoped RealInnerProductSpace NNReal
open scoped RealInnerProductSpace
open scoped ContDiff

namespace AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScore

universe u

/-- The reflected actual backward Gaussian conditional kernel has the stated
normalized density, and expectations of smooth compactly supported tests have
the centered score derivative. Normalization and domination are consequences
of the genuine Hessian bounds. Only positive eta is needed for this edge. -/
theorem reflected_conditional_covariance {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
    (hα : 0 < (α : ℝ)) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E,
      (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2) (hη : 0 < η) :
    let μ := (volume : Measure E).tilted (fun x => -V x)
    let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
      (μ.prod (stdGaussian E))
    let s := fun y u : E => -(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) -
      (1/(4*η)) • innerSL ℝ (y-u)
    ∃ R S : Kernel E E, IsMarkovKernel R ∧ IsMarkovKernel S ∧
      (J.map Prod.swap).IsCondKernel R ∧
      (∀ y, S y = (R y).map (fun x => (2:ℝ) • x-y)) ∧
      (∀ y, S y = (volume : Measure E).tilted
        (fun u => -V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))) ∧
      ∀ (f : E → ℝ), ContDiff ℝ ∞ f → HasCompactSupport f →
        ∀ y, Integrable (s y) (S y) ∧ Integrable (fun u => f u • s y u) (S y) ∧
          HasFDerivAt (fun z => ∫ u, f u ∂S z)
            ((∫ u, f u • s y u ∂S y) -
              (∫ u, f u ∂S y) • (∫ u, s y u ∂S y)) y := by
  have map_tilt {E F : Type u} [MeasurableSpace E] [MeasurableSpace F]
      (μ : Measure E) (e : E ≃ᵐ F) (f : E → ℝ) (hf : Measurable f) :
      (μ.tilted f).map e = (μ.map e).tilted (f ∘ e.symm) := by
    unfold Measure.tilted
    rw [AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym.measurableEquiv_map_withDensity e _ (by fun_prop)]
    congr 1
    funext y
    have hi : (∫ y, Real.exp (f (e.symm y)) ∂(μ.map e)) = ∫ x, Real.exp (f x) ∂μ := by
      rw [integral_map_equiv e]
      simp only [e.symm_apply_apply]
    simp only [Function.comp_apply, hi]

  have smul_tilt {E : Type u} [MeasurableSpace E] (μ : Measure E) (f : E → ℝ)
      (hf : Measurable f) {c : ℝ} (hc : 0 < c) :
      (ENNReal.ofReal c • μ).tilted f = μ.tilted f := by
    unfold Measure.tilted
    rw [integral_smul_measure, ENNReal.toReal_ofReal hc.le, smul_eq_mul,
      withDensity_smul_measure, ← withDensity_smul _ (by fun_prop)]
    congr 1
    funext x
    simp only [Pi.smul_apply, smul_eq_mul]
    rw [← ENNReal.ofReal_mul hc.le]
    congr 1
    by_cases hz : (∫ x, Real.exp (f x) ∂μ) = 0
    · simp [hz]
    · field_simp

  have reflection_affine {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] (y : E) :
      ∃ e : E ≃ᵐ E,
        (∀ x, e x = (2:ℝ) • x-y) ∧
        (∀ u, e.symm u = (1/2:ℝ) • (u+y)) ∧
        Measure.map e (volume : Measure E) =
          ENNReal.ofReal (abs ((2:ℝ)^Module.finrank ℝ E)⁻¹) • volume := by
    let e : E ≃ᵐ E :=
      { toFun := fun x => (2:ℝ) • x-y
        invFun := fun u => (1/2:ℝ) • (u+y)
        left_inv := by intro x; simp [smul_smul]
        right_inv := by intro u; simp [smul_smul]
        measurable_toFun := by
          change Measurable (fun x : E => (2:ℝ) • x-y)
          fun_prop
        measurable_invFun := by
          change Measurable (fun u : E => (1/2:ℝ) • (u+y))
          fun_prop }
    refine ⟨e, fun _ => rfl, fun _ => rfl, ?_⟩
    change Measure.map (fun x : E => (2:ℝ) • x-y) volume = _
    simp only [sub_eq_add_neg]
    change Measure.map ((fun x : E => x + -y) ∘ (fun x : E => (2:ℝ) • x)) volume = _
    rw [← Measure.map_map (by fun_prop) (by fun_prop),
      Measure.map_addHaar_smul volume (by norm_num : (2:ℝ) ≠ 0),
      Measure.map_smul, map_add_right_eq_self]

  have reflected_exponent {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      (V : E → ℝ) (η : ℝ) (y u : E) :
      -V ((1/2:ℝ) • (u+y)) - ‖(1/2:ℝ) • (u+y)-y‖^2/(2*η) =
        -V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η) := by
    rw [show (1/2:ℝ) • (u+y)-y = (1/2:ℝ) • (u-y) by module]
    rw [norm_smul, Real.norm_eq_abs, norm_sub_rev u y, add_comm u y]
    norm_num
    simp only [div_eq_mul_inv, mul_inv_rev]
    ring

  have actual_reflected_density {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
      {V : E → ℝ} {α η : ℝ} (hα : 0 < α) (hV : ContDiff ℝ 2 V)
      (hH : ∀ x v : E, α*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v)
      (hη : 0 < η) :
      let μ := (volume : Measure E).tilted (fun x => -V x)
      let J := Measure.map (fun p : E × E => (p.1,p.1+Real.sqrt η • p.2))
        (μ.prod (stdGaussian E))
      ∃ R : Kernel E E, IsMarkovKernel R ∧ (J.map Prod.swap).IsCondKernel R ∧
        ∀ y, Measure.map (fun x => (2:ℝ) • x-y) (R y) =
          (volume : Measure E).tilted
            (fun u => -V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η)) := by
    have density := AutoSamplingTheory.ExampleCases.ProximalBPS.GibbsAugmentation.normalized_augmentation_density
       hα hV hH hη
    have hi : Integrable (fun x => Real.exp (-V x)) (volume : Measure E) := by
      by_contra hn
      exact (ne_of_gt density.1) (integral_undef hn)
    have : IsProbabilityMeasure ((volume : Measure E).tilted (fun x => -V x)) :=
      isProbabilityMeasure_tilted hi
    have hVm : Measurable V := hV.continuous.measurable
    obtain ⟨R,hR,hRf,hcond⟩ :=
      AutoSamplingTheory.TechnicalLemmas.Probability.GaussianConditionalKernel.exists_tilted_isCondKernel
        ((volume : Measure E).tilted (fun x => -V x)) hη
    refine ⟨R,hR,hcond,?_⟩
    intro y
    rw [hRf y, tilted_tilted hi]
    obtain ⟨e,he,heinv,hemap⟩ := reflection_affine y
    rw [show (fun x => (2:ℝ) • x-y) = e from (funext he).symm]
    rw [map_tilt _ e _ (by fun_prop), hemap,
      smul_tilt _ _ (by fun_prop) (by positivity)]
    congr 1
    funext u
    simp only [Function.comp_apply, Pi.add_apply, heinv]
    simpa only [neg_div, sub_eq_add_neg] using reflected_exponent V η y u

  have reflected_kernel {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E] (R : Kernel E E) [IsMarkovKernel R] :
      ∃ S : Kernel E E, IsMarkovKernel S ∧
        ∀ y, S y = (R y).map (fun x => (2:ℝ) • x-y) := by
    let F := fun p : E × E => (2:ℝ) • p.2-p.1
    have hF : Measurable F := by fun_prop
    let S := (Kernel.id ×ₖ R).map F
    have : IsMarkovKernel S := Kernel.IsMarkovKernel.map _ hF
    refine ⟨S, inferInstance, ?_⟩
    intro y
    change ((Kernel.id ×ₖ R).map F) y = _
    rw [Kernel.map_apply _ hF, Kernel.prod_apply, Kernel.id_apply,
      Measure.dirac_prod, Measure.map_map hF (by fun_prop)]
    rfl



  have potential_controls {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] {V : E → ℝ} {α β : ℝ≥0}
      (hα : 0 < (α : ℝ)) (hV : ContDiff ℝ 2 V)
      (hH : ∀ x v : E,
        (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
        (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2) :
      (∀ x, V 0 - (α : ℝ)⁻¹/2*‖gradient V 0‖^2 ≤ V x) ∧
      (∀ x, ‖fderiv ℝ V x‖ ≤ ‖gradient V 0‖ + (β : ℝ)*‖x‖) := by
    have hd : Differentiable ℝ V := hV.differentiable (by norm_num)
    have hreg := QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
      hV hH (r := 0) (0 : E)
    simp only [NNReal.coe_zero, zero_div, zero_mul, add_zero] at hreg
    constructor
    · intro x
      have hfirst := StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn hreg.1
          (fun z _ => (hd z).hasGradientAt) (x := 0) (y := x)
          (Set.mem_univ _) (Set.mem_univ _)
      simp only [sub_zero] at hfirst
      have hinner := (abs_le.mp (abs_real_inner_le_norm (gradient V 0) x)).1
      have hyoung := two_mul_le_add_mul_sq (a := ‖x‖) (b := ‖gradient V 0‖) hα
      nlinarith
    · intro x
      rw [← toDual_gradient]
      rw [(toDual ℝ E).norm_map]
      calc
        ‖gradient V x‖ ≤ ‖gradient V x - gradient V 0‖ + ‖gradient V 0‖ :=
          norm_le_norm_sub_add _ _
        _ ≤ (β : ℝ)*‖x‖ + ‖gradient V 0‖ := by
          apply add_le_add _ (le_refl _)
          simpa using hreg.2.norm_sub_le x 0
        _ = _ := add_comm _ _

  have weight_envelope {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      (V : E → ℝ) {m η R : ℝ} (hV : ∀ x, m ≤ V x) (hη : 0 < η)
      (y u : E) (hy : ‖y‖ ≤ R) :
      Real.exp (-V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η)) ≤
        Real.exp (-m+R^2/(8*η)) * Real.exp (-(1/(16*η))*‖u‖^2) := by
    have hR : 0 ≤ R := (norm_nonneg y).trans hy
    have htri : ‖u‖ ≤ ‖y-u‖ + R := by
      have h := norm_le_norm_sub_add u y
      rw [norm_sub_rev u y] at h
      linarith
    have hsq : ‖u‖^2 ≤ 2*‖y-u‖^2 + 2*R^2 := by
      have ht := (sq_le_sq₀ (norm_nonneg u) (by positivity)).mpr htri
      nlinarith [sq_nonneg (‖y-u‖-R)]
    have hq := div_le_div_of_nonneg_right hsq (by positivity : 0 ≤ 16*η)
    have hdiv : ‖u‖^2/(16*η) ≤ ‖y-u‖^2/(8*η) + R^2/(8*η) := by
      have heq : (2*‖y-u‖^2+2*R^2)/(16*η) = ‖y-u‖^2/(8*η)+R^2/(8*η) := by
        field_simp
        ring
      rw [heq] at hq
      exact hq
    rw [← Real.exp_add]
    apply Real.exp_le_exp.mpr
    have hv := hV ((1/2:ℝ) • (y+u))
    simp only [div_eq_mul_inv, one_mul] at hdiv ⊢
    nlinarith

  have score_envelope {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [CompleteSpace E] (V : E → ℝ) {G β η R : ℝ}
      (hG : ∀ x, ‖fderiv ℝ V x‖ ≤ G+β*‖x‖) (hβ : 0 ≤ β) (hη : 0 < η)
      (y u : E) (hy : ‖y‖ ≤ R) :
      ‖-(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) -
        (1/(4*η)) • innerSL ℝ (y-u)‖ ≤
        G/2 + ((β+η⁻¹)/4)*R + ((β+η⁻¹)/4)*‖u‖ := by
    have hmid : ‖(1/2:ℝ) • (y+u)‖ ≤ (R+‖u‖)/2 := by
      rw [norm_smul, Real.norm_eq_abs]
      norm_num
      have h := norm_add_le y u
      linarith
    have hfd : ‖fderiv ℝ V ((1/2:ℝ) • (y+u))‖ ≤ G+β*((R+‖u‖)/2) :=
      (hG _).trans (add_le_add (le_refl _) (mul_le_mul_of_nonneg_left hmid hβ))
    have hdiff : ‖y-u‖ ≤ R+‖u‖ := (norm_sub_le _ _).trans (add_le_add hy (le_refl _))
    calc
      _ ≤ ‖-(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u))‖ +
          ‖(1/(4*η)) • innerSL ℝ (y-u)‖ := norm_sub_le _ _
      _ = (1/2:ℝ)*‖fderiv ℝ V ((1/2:ℝ) • (y+u))‖ + (1/(4*η))*‖y-u‖ := by
        simp only [norm_smul, Real.norm_eq_abs, innerSL_apply_norm]
        rw [abs_of_pos (by positivity : 0 < 1/(4*η))]
        norm_num
      _ ≤ (1/2:ℝ)*(G+β*((R+‖u‖)/2)) + (1/(4*η))*(R+‖u‖) := by
        gcongr
      _ = _ := by simp only [div_eq_mul_inv, mul_inv_rev]; ring

  have absorb_linear {a A b r : ℝ} (ha : 0 < a) (hA : 0 ≤ A) (hb : 0 ≤ b) (hr : 0 ≤ r) :
      (A+b*r)*Real.exp (-a*r^2) ≤
        (A+b*(1+2/a))*Real.exp (-(a/2)*r^2) := by
    let t := a/2*r^2
    have ht : 0 ≤ t := by dsimp [t]; positivity
    have he1 : 1 ≤ Real.exp t := Real.one_le_exp_iff.mpr ht
    have he2 : t ≤ Real.exp t := by linarith [Real.add_one_le_exp t]
    have hr2 : r^2 ≤ (2/a)*Real.exp t := by
      have hh : r^2*a ≤ 2*Real.exp t := by dsimp [t] at he2; nlinarith
      calc
        r^2 ≤ (2*Real.exp t)/a := (le_div_iff₀ ha).2 hh
        _ = _ := by ring
    have hrb : r ≤ (1+2/a)*Real.exp t := by
      nlinarith [sq_nonneg (r-1)]
    have hcoef : A+b*r ≤ (A+b*(1+2/a))*Real.exp t := by
      have h1 := mul_le_mul_of_nonneg_left he1 hA
      have h2 := mul_le_mul_of_nonneg_left hrb hb
      nlinarith
    have h := mul_le_mul_of_nonneg_right hcoef (Real.exp_nonneg (-a*r^2))
    rw [mul_assoc, ← Real.exp_add] at h
    have heq : t + -a*r^2 = -(a/2)*r^2 := by dsimp [t]; ring
    rw [heq] at h
    exact h



  have weight_derivative {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] {V : E → ℝ} (hV : Differentiable ℝ V)
      (η : ℝ) (y u : E) :
      HasFDerivAt
        (fun z => Real.exp (-V ((1/2:ℝ) • (z+u)) - ‖z-u‖^2/(8*η)))
        (Real.exp (-V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η)) •
          (-(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) -
            (1/(4*η)) • innerSL ℝ (y-u))) y := by
    have hv := (hV ((1/2:ℝ) • (y+u))).hasFDerivAt.comp y
      (((hasFDerivAt_id y).add_const u).const_smul (1/2:ℝ))
    have hq := (((hasFDerivAt_id y).sub_const u).norm_sq).const_mul (8*η)⁻¹
    convert (hv.neg.sub hq).exp using 1 <;>
      first | (congr 1; ext z; simp [div_eq_mul_inv]; ring) |
        (ext v; simp [div_eq_mul_inv, mul_inv_rev]; ring)



  have quotient_derivative {E : Type u} [NormedAddCommGroup E] [NormedSpace ℝ E]
      {N Z : E → ℝ} {DN DZ : E →L[ℝ] ℝ} {y : E}
      (hN : HasFDerivAt N DN y) (hZ : HasFDerivAt Z DZ y) (hz : Z y ≠ 0) :
      HasFDerivAt (fun z => N z/Z z)
        ((Z y)⁻¹ • DN - (N y/Z y) • ((Z y)⁻¹ • DZ)) y := by
    have hi := (hasFDerivAt_inv hz).comp y hZ
    have hp := hN.mul hi
    convert! hp using 1
    ext v
    simp [div_eq_mul_inv, pow_two]
    ring


  have local_controls {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
      {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
      (hα : 0 < (α : ℝ)) (hV : ContDiff ℝ 2 V)
      (hH : ∀ x v : E,
        (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
        (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2) (hη : 0 < η) :
      let w := fun y u : E => Real.exp (-V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))
      let dw := fun y u : E => w y u •
        (-(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) - (1/(4*η)) • innerSL ℝ (y-u))
      (∀ y, Integrable (w y) (volume : Measure E)) ∧
        ∀ y₀, ∃ bound : E → ℝ, Integrable bound (volume : Measure E) ∧
          (∀ u, 0 ≤ bound u) ∧
          ∀ y ∈ Metric.ball y₀ 1, ∀ u, ‖dw y u‖ ≤ bound u := by
    let w := fun y u : E => Real.exp (-V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))
    let dw := fun y u : E => w y u •
      (-(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) - (1/(4*η)) • innerSL ℝ (y-u))
    let m := V 0 - (α : ℝ)⁻¹/2*‖gradient V 0‖^2
    let G := ‖gradient V 0‖
    let a := 1/(16*η)
    have ha : 0 < a := by dsimp [a]; positivity
    obtain ⟨hlower,hgrowth⟩ := potential_controls hα hV hH
    have hVc : Continuous V := hV.continuous
    have hgauss : Integrable (fun u : E => Real.exp (-a*‖u‖^2)) volume :=
      Integrability.integrable_exp_neg_mul_norm_sq ha
    constructor
    · intro y
      refine (hgauss.const_mul (Real.exp (-m+‖y‖^2/(8*η)))).mono' (by dsimp [w]; fun_prop) ?_
      filter_upwards with u
      rw [Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
      exact weight_envelope V hlower hη y u (le_refl _)
    · intro y₀
      let R := ‖y₀‖+1
      let b := ((β : ℝ)+η⁻¹)/4
      let A := G/2+b*R
      let C := Real.exp (-m+R^2/(8*η))
      let bound := fun u : E => C*(A+b*(1+2/a))*Real.exp (-(a/2)*‖u‖^2)
      have hR : 0 ≤ R := by dsimp [R]; positivity
      have hb : 0 ≤ b := by dsimp [b]; positivity
      have hA : 0 ≤ A := by dsimp [A,G]; positivity
      have hC : 0 ≤ C := Real.exp_nonneg _
      refine ⟨bound, (Integrability.integrable_exp_neg_mul_norm_sq
        (E := E) (a := a/2) (by positivity)).const_mul _, ?_, ?_⟩
      · intro u
        dsimp [bound]
        positivity
      · intro y hy u
        have hyR : ‖y‖ ≤ R := by
          have ht := norm_le_norm_sub_add y y₀
          have hd : ‖y-y₀‖ < 1 := by simpa only [Metric.mem_ball, dist_eq_norm] using hy
          dsimp [R]
          linarith
        have hw : w y u ≤ C*Real.exp (-a*‖u‖^2) := weight_envelope V hlower hη y u hyR
        have hs : ‖-(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) -
            (1/(4*η)) • innerSL ℝ (y-u)‖ ≤ A+b*‖u‖ :=
          score_envelope V hgrowth β.coe_nonneg hη y u hyR
        have hp := absorb_linear ha hA hb (norm_nonneg u)
        change ‖dw y u‖ ≤ bound u
        dsimp only [dw]
        rw [norm_smul, Real.norm_eq_abs, abs_of_pos (Real.exp_pos _)]
        calc
          _ ≤ w y u*(A+b*‖u‖) := mul_le_mul_of_nonneg_left hs (Real.exp_nonneg _)
          _ ≤ (C*Real.exp (-a*‖u‖^2))*(A+b*‖u‖) :=
            mul_le_mul_of_nonneg_right hw (by positivity)
          _ = C*((A+b*‖u‖)*Real.exp (-a*‖u‖^2)) := by ring
          _ ≤ C*((A+b*(1+2/a))*Real.exp (-(a/2)*‖u‖^2)) :=
            mul_le_mul_of_nonneg_left hp hC
          _ = bound u := by dsimp [bound]; ring



  have unnormalized_derivative {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
      {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
      (hα : 0 < (α : ℝ)) (hV : ContDiff ℝ 2 V)
      (hH : ∀ x v : E,
        (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
        (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2) (hη : 0 < η)
      (f : E → ℝ) (hf : Continuous f) {M : ℝ} (hM : 0 ≤ M) (hMf : ∀ u, ‖f u‖ ≤ M) :
      let w := fun y u : E => Real.exp (-V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))
      let dw := fun y u : E => w y u •
        (-(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) - (1/(4*η)) • innerSL ℝ (y-u))
      ∀ y, Integrable (fun u => f u*w y u) (volume : Measure E) ∧
        Integrable (fun u => f u • dw y u) (volume : Measure E) ∧
        HasFDerivAt (fun z => ∫ u, f u*w z u ∂(volume : Measure E))
          (∫ u, f u • dw y u ∂(volume : Measure E)) y := by
    let w := fun y u : E => Real.exp (-V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))
    let dw := fun y u : E => w y u •
      (-(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) - (1/(4*η)) • innerSL ℝ (y-u))
    have hVc : Continuous V := hV.continuous
    have hVdc : Continuous (fderiv ℝ V) := (hV.fderiv_right (m := 1) (by norm_num)).continuous
    have hVd : Differentiable ℝ V := hV.differentiable (by norm_num)
    obtain ⟨hwI,hcontrols⟩ := local_controls hα hV hH hη
    have hfwI (y : E) : Integrable (fun u => f u*w y u) (volume : Measure E) := by
      refine ((hwI y).const_mul M).mono' (by dsimp [w]; fun_prop) ?_
      filter_upwards with u
      rw [norm_mul, Real.norm_eq_abs (w y u), abs_of_pos (Real.exp_pos _)]
      exact mul_le_mul_of_nonneg_right (hMf u) (Real.exp_nonneg _)
    dsimp only
    intro y
    obtain ⟨B,hBI,hB0,hB⟩ := hcontrols y
    have hbound : ∀ u, ∀ z ∈ Metric.ball y 1, ‖f u • dw z u‖ ≤ M*B u := by
      intro u z hz
      rw [norm_smul]
      exact mul_le_mul (hMf u) (hB z hz u) (norm_nonneg _) hM
    have hfdI : Integrable (fun u => f u • dw y u) (volume : Measure E) := by
      refine (hBI.const_mul M).mono' (by dsimp [dw,w]; fun_prop) ?_
      exact ae_of_all _ (fun u => hbound u y (Metric.mem_ball_self zero_lt_one))
    refine ⟨hfwI y,hfdI,?_⟩
    apply hasFDerivAt_integral_of_dominated_of_fderiv_le
      (F' := fun z u => f u • dw z u) (bound := fun u => M*B u)
      (Metric.ball_mem_nhds y zero_lt_one)
    · exact Filter.Eventually.of_forall (fun z => by fun_prop)
    · exact hfwI y
    · exact hfdI.aestronglyMeasurable
    · exact ae_of_all _ hbound
    · exact hBI.const_mul M
    · filter_upwards with u
      intro z _
      exact (weight_derivative hVd η z u).const_mul (f u)



  have normalized_tilt_integral {E F : Type u} [MeasurableSpace E]
      [NormedAddCommGroup F] [NormedSpace ℝ F] (μ : Measure E) (W : E → ℝ) (g : E → F) :
      ∫ u, g u ∂(μ.tilted W) = (∫ u, Real.exp (W u) ∂μ)⁻¹ •
        ∫ u, Real.exp (W u) • g u ∂μ := by
    rw [integral_tilted]
    simp only [div_eq_inv_mul, mul_smul]
    rw [integral_smul]

  have normalized_covariance {E : Type u} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
      [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
      {V : E → ℝ} {α β : ℝ≥0} {η : ℝ}
      (hα : 0 < (α : ℝ)) (hV : ContDiff ℝ 2 V)
      (hH : ∀ x v : E,
        (α : ℝ)*‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
        (fderiv ℝ (fderiv ℝ V) x v) v ≤ (β : ℝ)*‖v‖^2) (hη : 0 < η)
      (f : E → ℝ) (hf : Continuous f) {M : ℝ} (hM : 0 ≤ M) (hMf : ∀ u, ‖f u‖ ≤ M) :
      let ν := fun y : E => (volume : Measure E).tilted
        (fun u => -V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))
      let s := fun y u : E => -(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) -
        (1/(4*η)) • innerSL ℝ (y-u)
      ∀ y, Integrable (s y) (ν y) ∧ Integrable (fun u => f u • s y u) (ν y) ∧
        HasFDerivAt (fun z => ∫ u, f u ∂ν z)
          ((∫ u, f u • s y u ∂ν y) - (∫ u, f u ∂ν y) • (∫ u, s y u ∂ν y)) y := by
    let ν := fun y : E => (volume : Measure E).tilted
      (fun u => -V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))
    let s := fun y u : E => -(1/2:ℝ) • fderiv ℝ V ((1/2:ℝ) • (y+u)) -
      (1/(4*η)) • innerSL ℝ (y-u)
    let w := fun y u : E => Real.exp (-V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η))
    let dw := fun y u : E => w y u • s y u
    let Z := fun y => ∫ u, w y u ∂(volume : Measure E)
    let N := fun y => ∫ u, f u*w y u ∂(volume : Measure E)
    let DZ := fun y => ∫ u, dw y u ∂(volume : Measure E)
    let DN := fun y => ∫ u, f u • dw y u ∂(volume : Measure E)
    have hN := unnormalized_derivative hα hV hH hη f hf hM hMf
    have hZraw := unnormalized_derivative hα hV hH hη (fun _ : E => (1:ℝ))
      continuous_const (M := 1) (by norm_num) (fun _ => by norm_num)
    have hZ : ∀ y, Integrable (w y) (volume : Measure E) ∧
        Integrable (dw y) (volume : Measure E) ∧ HasFDerivAt Z (DZ y) y := by
      intro y
      simpa only [one_mul, one_smul] using hZraw y
    have hTf (y : E) : (∫ u, f u ∂ν y) = N y/Z y := by
      have hscalar (μ : Measure E) (W g : E → ℝ) :
          ∫ u, g u ∂(μ.tilted W) = (∫ u, Real.exp (W u) ∂μ)⁻¹ •
            ∫ u, Real.exp (W u) • g u ∂μ := by
        rw [integral_tilted]
        simp only [div_eq_inv_mul, mul_smul]
        rw [integral_smul]
      rw [hscalar]
      change (Z y)⁻¹ * (∫ u, w y u * f u ∂(volume : Measure E)) = N y / Z y
      rw [div_eq_mul_inv, mul_comm (N y)]
      congr 1
      apply integral_congr_ae
      filter_upwards with u
      exact mul_comm _ _
    have hTs (y : E) : (∫ u, s y u ∂ν y) = (Z y)⁻¹ • DZ y := by
      exact normalized_tilt_integral _ _ _
    have hTfs (y : E) : (∫ u, f u • s y u ∂ν y) = (Z y)⁻¹ • DN y := by
      rw [normalized_tilt_integral]
      congr 1
      apply integral_congr_ae
      filter_upwards with u
      simp only [dw, smul_smul]
      rw [mul_comm]
    dsimp only
    intro y
    have hsI : Integrable (s y) (ν y) := by
      rw [integrable_tilted_iff (hZ y).1]
      exact (hZ y).2.1
    have hfsI : Integrable (fun u => f u • s y u) (ν y) := by
      rw [integrable_tilted_iff (hZ y).1]
      apply (hN y).2.1.congr
      filter_upwards with u
      simp only [smul_smul]
      rw [mul_comm]
    refine ⟨hsI,hfsI,?_⟩
    change HasFDerivAt (fun z => ∫ u, f u ∂ν z)
      ((∫ u, f u • s y u ∂ν y) - (∫ u, f u ∂ν y) • (∫ u, s y u ∂ν y)) y
    rw [show (fun z => ∫ u, f u ∂ν z) = (fun z => N z/Z z) from funext hTf,
      hTf y,hTs y,hTfs y]
    exact quotient_derivative (hN y).2.2 (hZ y).2.2 (ne_of_gt (integral_exp_pos (hZ y).1))
  dsimp only
  obtain ⟨R,hR,hcond,hν⟩ := actual_reflected_density hα hV (fun x v => (hH x v).1) hη
  let : IsMarkovKernel R := hR
  obtain ⟨S,hS,hSR⟩ := reflected_kernel R
  have hSν (y : E) : S y = (volume : Measure E).tilted
      (fun u => -V ((1/2:ℝ) • (y+u)) - ‖y-u‖^2/(8*η)) :=
    (hSR y).trans (hν y)
  refine ⟨R,S,hR,hS,hcond,hSR,hSν,?_⟩
  intro f hf hfc y
  obtain ⟨M,hM⟩ := hf.continuous.norm.bddAbove_range_of_hasCompactSupport hfc.norm
  have hMf (u : E) : ‖f u‖ ≤ M := hM (Set.mem_range_self u)
  have hM0 : 0 ≤ M := (norm_nonneg (f 0)).trans (hMf 0)
  simpa only [hSν] using normalized_covariance hα hV hH hη f hf.continuous hM0 hMf y


end AutoSamplingTheory.ExampleCases.ProximalBPS.ConditionalScore
