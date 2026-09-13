import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalGaussianEstimator

/-!
# Input stability of the actual proximal Gaussian estimator

Chen, Chewi, Lu and Zhang, arXiv:2609.06906v1, Lemma 4.2 (4.4)-(4.5).
The genuine proximal equation and gradient monotonicity imply nonexpansiveness;
the already derived gradient Lipschitz bound then controls both inputs.

The range `0 < eta ≤ 1/2` comes from the existing measurable proximal
construction, not a necessary restriction for nonexpansiveness or a correction
to the source. The theorem retains unique-minimum identification. It concerns
the exact proximal oracle, not its finite-query implementation. Neither bias,
Gaussian concentration, Picard accuracy, nor either full paper is proved here.
-/

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalEstimatorLipschitz

open InnerProductSpace
open scoped NNReal RealInnerProductSpace

private theorem nonexpansive_of_monotone_optimality
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {g p : E → E} {eta : ℝ} (heta : 0 ≤ eta)
    (hmono : ∀ x y, 0 ≤ inner ℝ (g x - g y) (x - y))
    (heq : ∀ y, p y + eta • g (p y) = y) : LipschitzWith 1 p := by
  apply LipschitzWith.of_dist_le_mul
  intro x y
  simp only [NNReal.coe_one, one_mul, dist_eq_norm]
  have hsub : x - y = (p x - p y) + eta • (g (p x) - g (p y)) := by
    calc
      x - y = (p x + eta • g (p x)) - (p y + eta • g (p y)) :=
        congrArg₂ (fun a b : E => a - b) (heq x).symm (heq y).symm
      _ = _ := by module
  have hpair : ‖p x - p y‖ ^ 2 ≤ inner ℝ (x - y) (p x - p y) := by
    calc
      _ ≤ ‖p x - p y‖ ^ 2 + eta * inner ℝ (g (p x) - g (p y)) (p x - p y) :=
        le_add_of_nonneg_right (mul_nonneg heta (hmono (p x) (p y)))
      _ = inner ℝ (x - y) (p x - p y) := by
        conv_rhs => rw [hsub]
        rw [inner_add_left, real_inner_smul_left, real_inner_self_eq_norm_sq]
  have hbound := hpair.trans (real_inner_le_norm (x - y) (p x - p y))
  by_cases hzero : ‖p x - p y‖ = 0
  · simpa only [hzero] using norm_nonneg (x - y)
  · have hpos : 0 < ‖p x - p y‖ := lt_of_le_of_ne (norm_nonneg _) (Ne.symm hzero)
    nlinarith

/-- The actual exact proximal estimator is nonexpansive in its center and
`sqrt eta`-Lipschitz in its noise input, on the existing construction range.
The proximal map is constructed, not assumed Lipschitz; its equation and unique
global minimum bind the bounds to the source's actual oracle. -/
theorem proximal_estimator_lipschitz
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    {V : E → ℝ} {κ : ℝ≥0} (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (κ : ℝ)⁻¹ * ‖v‖ ^ 2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖ ^ 2)
    {eta : ℝ} (hpos : 0 < eta) (hsmall : eta ≤ 1 / 2) :
    let F := fun y x => V x + eta⁻¹ / 2 * ‖x - y‖ ^ 2
    ∃ p : E → E, Measurable p ∧
      (∀ y, p y + eta • gradient V (p y) = y) ∧
      (∀ y z, F y (p y) + ((κ : ℝ)⁻¹ + eta⁻¹) / 2 * ‖z - p y‖ ^ 2 ≤ F y z ∧
        (F y z ≤ F y (p y) ↔ z = p y)) ∧
      LipschitzWith 1 p ∧
      (∀ y y' G, ‖gradient V (p y + Real.sqrt eta • G) -
        gradient V (p y' + Real.sqrt eta • G)‖ ≤ ‖y - y'‖) ∧
      (∀ y G G', ‖gradient V (p y + Real.sqrt eta • G) -
        gradient V (p y + Real.sqrt eta • G')‖ ≤ Real.sqrt eta * ‖G - G'‖) := by
  obtain ⟨p, hp, heq, hmin, _⟩ :=
    ProximalGaussianEstimator.proximal_gaussian_estimator hκ hV hH
      (eta := fun _ : E => eta) (y := id) measurable_const measurable_id
      (fun _ => hpos) (fun _ => hsmall)
  have hH' : ∀ x v : E, ((κ⁻¹ : ℝ≥0) : ℝ) * ‖v‖ ^ 2 ≤
      (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ (1 : ℝ≥0) * ‖v‖ ^ 2 := by
    simpa only [NNReal.coe_inv, NNReal.coe_one, one_mul] using hH
  have hreg :=
    AutoSamplingTheory.TechnicalLemmas.Analysis.QuadraticRegularization.strongConvexOn_and_lipschitzWith_gradient_add_quadratic
      (r := 0) hV hH' (0 : E)
  have hLip : LipschitzWith 1 (gradient V) := by simpa using hreg.2
  have hsc : StrongConvexOn Set.univ ((κ : ℝ)⁻¹) V := by simpa using hreg.1
  have hmono (x y : E) : 0 ≤ inner ℝ (gradient V x - gradient V y) (x - y) := by
    have hb :=
      AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder.gradient_inner_lower_bound_of_strongConvexOn hsc
          (fun z _ => (hV.differentiable (by norm_num) z).hasGradientAt)
          (x := y) (y := x) (Set.mem_univ _) (Set.mem_univ _)
    exact (mul_nonneg (inv_nonneg.mpr (NNReal.coe_nonneg κ)) (sq_nonneg _)).trans hb
  have hpLip := nonexpansive_of_monotone_optimality hpos.le hmono heq
  refine ⟨p, hp, heq, hmin, hpLip, ?_, ?_⟩
  · intro y y' G
    have hg := hLip.dist_le_mul (p y + Real.sqrt eta • G) (p y' + Real.sqrt eta • G)
    have hy := hpLip.dist_le_mul y y'
    simp only [NNReal.coe_one, one_mul, dist_eq_norm, add_sub_add_right_eq_sub] at hg hy
    exact hg.trans hy
  · intro y G G'
    have hg := hLip.dist_le_mul (p y + Real.sqrt eta • G) (p y + Real.sqrt eta • G')
    simpa only [NNReal.coe_one, one_mul, dist_eq_norm, add_sub_add_left_eq_sub,
      ← smul_sub, norm_smul, Real.norm_eq_abs, abs_of_nonneg (Real.sqrt_nonneg eta)] using hg

end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalEstimatorLipschitz
