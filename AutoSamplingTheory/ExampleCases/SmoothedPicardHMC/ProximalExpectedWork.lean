import AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ApproximateProximalExecution
import Mathlib.Analysis.Convex.Integral
import Mathlib.Analysis.Convex.SpecificFunctions.Basic
import Mathlib.Probability.Moments.Variance
import Mathlib.MeasureTheory.Function.SpecialFunctions.Basic

/-!
# Expected work of actual stopped proximal execution

Chen--Chewi--Lu--Zhang, arXiv:2609.06906v1, Appendix D.2, Lemma D.4:
the Jensen step after (D.7), not the Picard input-moment estimate or total
run cost (D.8). The input law's second moment remains an explicit dependency.
-/

noncomputable section
open MeasureTheory Filter InnerProductSpace
open scoped Topology NNReal

namespace AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalExpectedWork

private theorem log_work_integral {α : Type*} [MeasurableSpace α]
    {μ : Measure α} [IsProbabilityMeasure μ] {g : α → ℝ}
    (hg : Measurable g) (hgn : ∀ x, 0 ≤ g x)
    (hgs : Integrable (fun x => g x ^ 2) μ) {eps : ℝ} (heps : 0 < eps) :
    Integrable (fun x => Real.log (1 + g x / eps)) μ ∧
    (∫ x, Real.log (1 + g x / eps) ∂μ) ≤
      Real.log (1 + Real.sqrt (∫ x, g x ^ 2 ∂μ) / eps) := by
  have hLp : MemLp g 2 μ := (memLp_two_iff_integrable_sq hg.aestronglyMeasurable).mpr hgs
  have hgi : Integrable g μ := hLp.integrable (by norm_num)
  have hpos (x) : 0 < 1 + g x / eps := by have := hgn x; positivity
  have hlog : Integrable (fun x => Real.log (1 + g x / eps)) μ := by
    apply (hgi.div_const eps).mono'
      ((measurable_const.add (hg.div_const eps)).log.aestronglyMeasurable)
    filter_upwards [] with x
    change ‖Real.log (1 + g x / eps)‖ ≤ g x / eps
    rw [Real.norm_of_nonneg (Real.log_nonneg (le_add_of_nonneg_right
      (div_nonneg (hgn x) heps.le)))]
    have := Real.log_le_sub_one_of_pos (hpos x)
    linarith
  refine ⟨hlog, ?_⟩
  have hconc : ConcaveOn ℝ (Set.Ici (1 : ℝ)) Real.log :=
    strictConcaveOn_log_Ioi.concaveOn.subset
      (by intro x hx; exact lt_of_lt_of_le (by norm_num : (0 : ℝ) < 1) hx)
      (convex_Ici 1)
  have hj := hconc.le_map_integral
    (Real.continuousOn_log.mono (fun x hx => ne_of_gt (lt_of_lt_of_le zero_lt_one hx)))
    isClosed_Ici (Filter.Eventually.of_forall (fun x => by
      change 1 ≤ 1 + g x / eps
      exact le_add_of_nonneg_right (div_nonneg (hgn x) heps.le)))
      ((integrable_const 1).add (hgi.div_const eps)) hlog
  have hmean : (∫ x, g x ∂μ) ≤ Real.sqrt (∫ x, g x ^ 2 ∂μ) := by
    have hv := ProbabilityTheory.variance_nonneg g μ
    rw [ProbabilityTheory.variance_eq_sub hLp] at hv
    have hs := Real.sq_sqrt (integral_nonneg (μ := μ) (fun x => sq_nonneg (g x)))
    have hn := Real.sqrt_nonneg (∫ x, g x ^ 2 ∂μ)
    change 0 ≤ (∫ x, g x ^ 2 ∂μ) - (∫ x, g x ∂μ)^2 at hv
    nlinarith
  change (∫ x, Real.log (1 + g x / eps) ∂μ) ≤ Real.log (∫ x, 1 + g x / eps ∂μ) at hj
  simp only [integral_add (integrable_const 1) (hgi.div_const eps),
    integral_const, probReal_univ, smul_eq_mul, one_mul, integral_div] at hj
  exact hj.trans (Real.log_le_log (by
    have hn : 0 ≤ ∫ x, g x ∂μ := integral_nonneg hgn
    positivity) (by gcongr))

section
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [CompleteSpace E] [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

/-- The actual stopped gradient program has integrable query count under an
input law with square-integrable gradient, with the D.4 Jensen work bound.
This does not identify that law with the realized Picard centers or prove D.7. -/
theorem approximate_proximal_expected_work {V : E → ℝ} {κ : ℝ≥0}
    (hκ : 1 ≤ κ) (hV : ContDiff ℝ 2 V)
    (hH : ∀ x v : E, (κ : ℝ)⁻¹ * ‖v‖^2 ≤ (fderiv ℝ (fderiv ℝ V) x v) v ∧
      (fderiv ℝ (fderiv ℝ V) x v) v ≤ ‖v‖^2)
    {eta c eps : ℝ} (heta : 0 < eta) (hec : eta ≤ c) (hc : c < 1) (heps : 0 < eps)
    (ν : Measure E) [IsProbabilityMeasure ν]
    (hmoment : Integrable (fun y => ‖gradient V y‖^2) ν) :
    let T := fun y x : E => y - eta • gradient V x
    let C := 2 + (1 + Real.log ((1-c)⁻¹)) / (-Real.log c)
    ∃ p : E → E, ∃ N : E → ℕ,
      Measurable p ∧ Measurable N ∧ Measurable (fun y => (T y)^[N y] y) ∧
      (∀ y, p y + eta • gradient V (p y) = y ∧
        ‖(T y)^[N y] y - p y‖ ≤ eps ∧
        ApproximateProximalExecution.proximalQuery (gradient V) eta eps y (N y+1) y =
          some ((T y)^[N y] y, N y+1)) ∧
      Integrable (fun y => (N y : ℝ) + 1) ν ∧
      (∫ y, (N y : ℝ) + 1 ∂ν) ≤
        C * (1 + Real.log (1 + Real.sqrt (∫ y, ‖gradient V y‖^2 ∂ν) / eps)) := by
  dsimp only
  obtain ⟨p, N, hp, hN, hout, hall⟩ :=
    ApproximateProximalExecution.approximate_proximal_execution hκ hV hH heta hec hc heps
  have hgcont : Continuous (gradient V) := by
    unfold gradient
    exact (InnerProductSpace.toDual ℝ E).symm.continuous.comp
      (hV.continuous_fderiv (by norm_num))
  have hg : Measurable (fun y => ‖gradient V y‖) := hgcont.norm.measurable
  obtain ⟨hlog, hj⟩ := log_work_integral hg (fun y => norm_nonneg _) hmoment heps
  let C := 2 + (1 + Real.log ((1-c)⁻¹)) / (-Real.log c)
  have hC : 0 ≤ C := by
    have hcp : 0 < c := heta.trans_le hec
    have hd : 0 < 1-c := sub_pos.mpr hc
    have ha : 0 < -Real.log c := neg_pos.mpr (Real.log_neg hcp hc)
    have hb : 0 ≤ Real.log ((1-c)⁻¹) := Real.log_nonneg (by
      have hm := mul_nonneg (inv_nonneg.mpr hd.le) hcp.le
      have hi := inv_mul_cancel₀ hd.ne'
      nlinarith)
    dsimp [C]
    positivity
  have hbound (y) : (N y : ℝ)+1 ≤ C*(1+Real.log (1+‖gradient V y‖/eps)) :=
    (hall y).2.2.2.2.2.1
  have hdom : Integrable (fun y => C*(1+Real.log (1+‖gradient V y‖/eps))) ν :=
    ((integrable_const 1).add hlog).const_mul C
  have hcount : Integrable (fun y => (N y : ℝ)+1) ν := by
    apply hdom.mono' (by fun_prop)
    filter_upwards [] with y
    rw [Real.norm_of_nonneg (by positivity)]
    exact hbound y
  refine ⟨p, N, hp, hN, hout, fun y => ⟨(hall y).1, (hall y).2.2.2.2.1,
    (hall y).2.2.2.2.2.2⟩, hcount, ?_⟩
  calc
    (∫ y, (N y : ℝ)+1 ∂ν) ≤ ∫ y, C*(1+Real.log (1+‖gradient V y‖/eps)) ∂ν :=
      integral_mono hcount hdom hbound
    _ = C*(1+∫ y, Real.log (1+‖gradient V y‖/eps) ∂ν) := by
      rw [integral_const_mul, integral_add (integrable_const 1) hlog]
      simp
    _ ≤ _ := mul_le_mul_of_nonneg_left (add_le_add_right hj 1) hC

end
end AutoSamplingTheory.ExampleCases.SmoothedPicardHMC.ProximalExpectedWork
