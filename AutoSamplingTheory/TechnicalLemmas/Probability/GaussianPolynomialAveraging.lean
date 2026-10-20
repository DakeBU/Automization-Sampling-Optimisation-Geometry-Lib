import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRidge
import Mathlib.Probability.Distributions.Gaussian.Fernique
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.MeasureTheory.Integral.Prod
import Mathlib.Tactic

open MeasureTheory ProbabilityTheory Filter
open scoped ENNReal InnerProductSpace Topology

namespace AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialAveraging

private theorem polynomial_norm_envelope
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (p : Polynomial ℝ) :
    ∃ B : E → ℝ, MemLp B 2 (stdGaussian E) ∧ (∀ x, 0 ≤ B x) ∧
      ∀ (w : {w : E // ‖w‖ = 1}) x, ‖p.eval ⟪w.1,x⟫_ℝ‖ ≤ B x := by
  classical
  letI : CompleteSpace E := FiniteDimensional.complete ℝ E
  letI : SecondCountableTopology E := inferInstance
  let μ := stdGaussian E
  have hpow (n : ℕ) : MemLp (fun x : E => ‖x‖ ^ n) 2 μ := by
    apply (memLp_two_iff_integrable_sq (by fun_prop)).2
    have hi := (IsGaussian.memLp_id μ ((2 * n : ℕ) : ℝ≥0∞) (ENNReal.natCast_ne_top (2*n))).integrable_norm_pow' (p := 2*n)
    convert hi using 1
    funext x
    simp only [id_eq, ← pow_mul, Nat.mul_comm n 2]
  have henv : ∃ B : E → ℝ, MemLp B 2 μ ∧ (∀ x, 0 ≤ B x) ∧
      ∀ (w : {w : E // ‖w‖ = 1}) x, ‖p.eval ⟪w.1, x⟫_ℝ‖ ≤ B x := by
    induction p using Polynomial.induction_on' with
    | add p q hp hq =>
      obtain ⟨B, hB, hBpos, hBp⟩ := hp
      obtain ⟨C, hC, hCpos, hCq⟩ := hq
      refine ⟨B+C, hB.add hC, fun x => add_nonneg (hBpos x) (hCpos x), ?_⟩
      intro w x
      simpa only [Polynomial.eval_add, Pi.add_apply] using
        (norm_add_le (p.eval ⟪w.1,x⟫_ℝ) (q.eval ⟪w.1,x⟫_ℝ)).trans
          (add_le_add (hBp w x) (hCq w x))
    | monomial n a =>
      refine ⟨fun x => ‖a‖ * ‖x‖^n, (hpow n).const_mul ‖a‖,
        fun x => mul_nonneg (norm_nonneg _) (pow_nonneg (norm_nonneg _) _), ?_⟩
      intro w x
      simp only [Polynomial.eval_monomial, norm_mul, norm_pow]
      apply mul_le_mul_of_nonneg_left _ (norm_nonneg a)
      apply pow_le_pow_left₀ (norm_nonneg _) _
      simpa only [w.2, one_mul] using norm_inner_le_norm (𝕜 := ℝ) w.1 x
  exact henv

theorem continuous_gaussian_polynomial_ridge_L2
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (p : Polynomial ℝ) :
    ∃ hfeature : ∀ w : {w : E // ‖w‖ = 1},
      MemLp (fun x : E => p.eval ⟪w.1, x⟫_ℝ) 2 (ProbabilityTheory.stdGaussian E),
      Continuous (fun w : {w : E // ‖w‖ = 1} =>
        (hfeature w).toLp (fun x : E => p.eval ⟪w.1, x⟫_ℝ)) := by
  classical
  letI : CompleteSpace E := FiniteDimensional.complete ℝ E
  letI : SecondCountableTopology E := inferInstance
  let μ := stdGaussian E
  obtain ⟨B,hB,hBpos,hBbound⟩ := polynomial_norm_envelope (E := E) p
  obtain ⟨hb, hbpos, hf, hnorm⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRidge.standard_gaussian_polynomial_ridge_uniform_L2 (E := E) p
  refine ⟨hf, ?_⟩
  let F := fun w : {w : E // ‖w‖ = 1} => (hf w).toLp (fun x => p.eval ⟪w.1,x⟫_ℝ)
  change Continuous F
  apply continuous_iff_continuousAt.2
  intro w₀
  have hBsq : Integrable (fun x => 4 * (B x)^2) μ :=
    ((memLp_two_iff_integrable_sq hB.1).1 hB).const_mul 4
  have hn (w) : ‖F w - F w₀‖^2 =
      ∫ x, (p.eval ⟪w.1,x⟫_ℝ - p.eval ⟪w₀.1,x⟫_ℝ)^2 ∂μ := by
    rw [← real_inner_self_eq_norm_sq, L2.inner_def]
    apply integral_congr_ae
    filter_upwards [Lp.coeFn_sub (F w) (F w₀), (hf w).coeFn_toLp, (hf w₀).coeFn_toLp] with x hx hw hw₀
    simp only [hx, Pi.sub_apply, F] at *
    rw [hw,hw₀]
    simp [real_inner_self_eq_norm_sq, Real.norm_eq_abs, sq_abs]
  have hc : ContinuousAt (fun w : {w : E // ‖w‖ = 1} =>
      ∫ x, (p.eval ⟪w.1,x⟫_ℝ - p.eval ⟪w₀.1,x⟫_ℝ)^2 ∂μ) w₀ := by
    apply continuousAt_of_dominated (bound := fun x => 4 * (B x)^2)
    · exact Eventually.of_forall fun w => by fun_prop
    · exact Eventually.of_forall fun w => ae_of_all _ fun x => by
        rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _)]
        have h := (norm_sub_le (p.eval ⟪w.1,x⟫_ℝ) (p.eval ⟪w₀.1,x⟫_ℝ)).trans
          (add_le_add (hBbound w x) (hBbound w₀ x))
        have hs := (sq_le_sq₀ (norm_nonneg _) (add_nonneg (hBpos x) (hBpos x))).2 h
        simpa only [Real.norm_eq_abs, sq_abs] using hs.trans_eq (by ring)
    · exact hBsq
    · exact ae_of_all _ fun x => by fun_prop
  have hsq : ContinuousAt (fun w => ‖F w - F w₀‖^2) w₀ := by
    simpa only [← hn] using hc
  rw [ContinuousAt, tendsto_iff_dist_tendsto_zero]
  simpa only [Function.comp_def, Real.sqrt_sq (norm_nonneg _), sub_self, norm_zero, zero_pow (by decide : 2 ≠ 0),
    Real.sqrt_zero, dist_eq_norm] using
    (Real.continuous_sqrt.continuousAt.comp hsq).tendsto

theorem gaussian_polynomial_parameter_average_L2
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (p : Polynomial ℝ) :
    ∃ hfeature : ∀ w : {w : E // ‖w‖ = 1},
      MemLp (fun x : E => p.eval ⟪w.1, x⟫_ℝ) 2 (ProbabilityTheory.stdGaussian E),
      Continuous (fun w : {w : E // ‖w‖ = 1} =>
        (hfeature w).toLp (fun x : E => p.eval ⟪w.1, x⟫_ℝ)) ∧
      ∀ rho : Measure {w : E // ‖w‖ = 1}, IsProbabilityMeasure rho →
        (∀ x : E, Integrable (fun w : {w : E // ‖w‖ = 1} => p.eval ⟪w.1, x⟫_ℝ) rho) ∧
        Integrable (fun w : {w : E // ‖w‖ = 1} =>
          (hfeature w).toLp (fun x : E => p.eval ⟪w.1, x⟫_ℝ)) rho ∧
        ∃ hmean : MemLp (fun x : E => ∫ w : {w : E // ‖w‖ = 1},
            p.eval ⟪w.1, x⟫_ℝ ∂rho) 2 (ProbabilityTheory.stdGaussian E),
          hmean.toLp (fun x : E => ∫ w : {w : E // ‖w‖ = 1}, p.eval ⟪w.1, x⟫_ℝ ∂rho) =
            ∫ w : {w : E // ‖w‖ = 1},
              (hfeature w).toLp (fun x : E => p.eval ⟪w.1, x⟫_ℝ) ∂rho := by
  classical
  letI : CompleteSpace E := FiniteDimensional.complete ℝ E
  letI : SecondCountableTopology E := inferInstance
  let μ := stdGaussian E
  obtain ⟨B,hB,hBpos,hBbound⟩ := polynomial_norm_envelope (E := E) p
  obtain ⟨hf,hcont⟩ := AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialAveraging.continuous_gaussian_polynomial_ridge_L2 (E := E) p
  obtain ⟨hb, hbpos, hf8, hnorm⟩ :=
    AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRidge.standard_gaussian_polynomial_ridge_uniform_L2 (E := E) p
  let U := {w : E // ‖w‖ = 1}
  let K : U → E → ℝ := fun w x => p.eval ⟪w.1,x⟫_ℝ
  let F := fun w : U => (hf w).toLp (K w)
  have hFcont : Continuous F := hcont
  have hFbound (w : U) : ‖F w‖ ≤ ‖hb.toLp (fun z : ℝ => p.eval z)‖ + 1 :=
    (hnorm w).2
  have hKcont : Continuous (fun z : U × E => K z.1 z.2) := by
    change Continuous (fun z : {w : E // ‖w‖ = 1} × E => p.eval ⟪z.1.1,z.2⟫_ℝ)
    fun_prop
  refine ⟨hf, hcont, ?_⟩
  intro rho hrho
  letI : IsProbabilityMeasure rho := hrho
  have hscalar (x : E) : Integrable (fun w : U => K w x) rho := by
    apply (integrable_const (B x)).mono' (by fun_prop)
    exact ae_of_all _ fun w => hBbound w x
  have hFint : Integrable F rho := by
    apply (integrable_const (‖hb.toLp (fun z : ℝ => p.eval z)‖ + 1)).mono'
      hFcont.aestronglyMeasurable
    exact ae_of_all _ hFbound
  let mean : E → ℝ := fun x => ∫ w, K w x ∂rho
  have hmeanmeas : StronglyMeasurable mean :=
    hKcont.stronglyMeasurable.integral_prod_left'
  have hmeanbound (x : E) : ‖mean x‖ ≤ B x := by
    have h := norm_integral_le_of_norm_le_const (μ := rho) (f := fun w : U => K w x)
      (ae_of_all _ fun w => hBbound w x)
    simpa only [probReal_univ, mul_one] using h
  have hmean : MemLp mean 2 μ := hB.mono' hmeanmeas.aestronglyMeasurable
    (ae_of_all _ hmeanbound)
  refine ⟨hscalar,hFint,hmean,?_⟩
  apply ext_inner_left ℝ
  intro g
  have hC : Integrable (fun x : E => ‖g x‖ * B x) μ :=
    (Lp.memLp g).norm.integrable_mul hB
  have hHmeas : AEStronglyMeasurable (fun z : U × E => g z.2 * K z.1 z.2) (rho.prod μ) :=
    (Lp.aestronglyMeasurable g).comp_snd.mul hKcont.aestronglyMeasurable
  have hHint : Integrable (fun z : U × E => g z.2 * K z.1 z.2) (rho.prod μ) := by
    apply (hC.comp_snd rho).mono' hHmeas
    exact ae_of_all _ fun z => by
      rw [norm_mul]
      exact mul_le_mul_of_nonneg_left (hBbound z.1 z.2) (norm_nonneg _)
  have hin (w : U) : ⟪g,F w⟫_ℝ = ∫ x, g x * K w x ∂μ := by
    rw [L2.inner_def]
    apply integral_congr_ae
    filter_upwards [(hf w).coeFn_toLp] with x hx
    change inner ℝ (g x) ((hf w).toLp (K w) x) = _
    rw [hx]
    simp only [RCLike.inner_apply, conj_trivial, K, mul_comm]
  calc
    ⟪g,hmean.toLp mean⟫_ℝ = ∫ x, g x * mean x ∂μ := by
      rw [L2.inner_def]
      apply integral_congr_ae
      filter_upwards [hmean.coeFn_toLp] with x hx
      rw [hx]
      simp only [RCLike.inner_apply, conj_trivial, K, mul_comm]
    _ = ∫ x, ∫ w, g x * K w x ∂rho ∂μ := by
      apply integral_congr_ae
      exact ae_of_all _ fun x => (integral_const_mul (g x) (fun w : U => K w x)).symm
    _ = ∫ w, ∫ x, g x * K w x ∂μ ∂rho := (integral_integral_swap hHint).symm
    _ = ∫ w, ⟪g,F w⟫_ℝ ∂rho := integral_congr_ae (ae_of_all _ fun w => (hin w).symm)
    _ = ⟪g,∫ w, F w ∂rho⟫_ℝ := integral_inner hFint g

end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialAveraging
