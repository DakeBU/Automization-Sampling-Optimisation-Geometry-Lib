import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.Matrix.HermitianFunctionalCalculus
import Mathlib.Analysis.SpecialFunctions.ContinuousFunctionalCalculus.ExpLog.Basic
import Mathlib.MeasureTheory.Integral.Lebesgue.Markov
import Mathlib.MeasureTheory.Measure.Typeclasses.Probability
import Mathlib.MeasureTheory.Function.StronglyMeasurable.AEStronglyMeasurable

/-! Real finite-dimensional specialization of Tropp, Proposition 3.1
(author preprint, pp. 9–10). The trace is unnormalized and the largest
eigenvalue is algebraic, rather than the operator norm. The scalar expectation
is an extended nonnegative integral, so positive parameters with infinite
expectation remain legitimate terms of the infimum. This domain completion
does not assert existence of a Bochner matrix moment generating function. -/

open MeasureTheory Unitary
open scoped BigOperators Matrix.Norms.L2Operator ENNReal

noncomputable section
universe u v
namespace AutoSamplingTheory.TechnicalLemmas.Probability.MatrixLaplaceTail

private lemma trace_exp_eq_sum
    {ι : Type u} [Fintype ι] [DecidableEq ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian) (s : ℝ) :
    Matrix.trace (NormedSpace.exp (s • A)) =
      ∑ i, Real.exp (s * hA.eigenvalues i) := by
  have heq : cfc (fun x : ℝ => Real.exp (s * x)) A = NormedSpace.exp (s • A) := by
    calc
      _ = cfc Real.exp (s • A) :=
        cfc_comp_const_mul s Real.exp A (by fun_prop) hA.isSelfAdjoint
      _ = _ := CFC.real_exp_eq_normedSpace_exp
        ((IsSelfAdjoint.all s).smul hA.isSelfAdjoint)
  rw [← heq, hA.cfc_eq, Matrix.IsHermitian.cfc,
    conjStarAlgAut_apply, Matrix.trace_mul_cycle, coe_star_mul_self,
    one_mul, Matrix.trace_diagonal]
  simp

private lemma exp_max_eigenvalue_le_trace_exp
    {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (A : Matrix ι ι ℝ) (hA : A.IsHermitian) (s : ℝ) :
    Real.exp (s * sSup (spectrum ℝ A)) ≤ Matrix.trace (NormedSpace.exp (s • A)) := by
  rw [trace_exp_eq_sum A hA s]
  have hmem : sSup (spectrum ℝ A) ∈ spectrum ℝ A := by
    rw [hA.spectrum_real_eq_range_eigenvalues]
    exact (Set.range_nonempty _).csSup_mem (Set.finite_range _)
  rw [hA.spectrum_real_eq_range_eigenvalues] at hmem
  obtain ⟨i, hi⟩ := hmem
  rw [hA.spectrum_real_eq_range_eigenvalues, ← hi]
  exact Finset.single_le_sum
    (f := fun j => Real.exp (s * hA.eigenvalues j))
    (fun j _ => Real.exp_nonneg _) (Finset.mem_univ i)

/-- The matrix Laplace tail bound with AE Hermiticity and extended expectation.
No centering, independence, variance, or one-sided matrix cap is required. -/
theorem max_eigenvalue_tail_le_iInf_trace_exp
    {Ω : Type v} [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    {ι : Type u} [Fintype ι] [DecidableEq ι] [Nonempty ι]
    (X : Ω → Matrix ι ι ℝ)
    (hX : AEStronglyMeasurable X μ)
    (hherm : ∀ᵐ ω ∂μ, (X ω).IsHermitian)
    (t : ℝ) :
    μ {ω | t ≤ sSup (spectrum ℝ (X ω))} ≤
      ⨅ s : {s : ℝ // 0 < s},
        ENNReal.ofReal (Real.exp (-(s.val * t))) *
          ∫⁻ ω, ENNReal.ofReal (Matrix.trace (NormedSpace.exp (s.val • X ω))) ∂μ := by
  classical
  apply le_iInf
  intro s
  let F : Ω → ℝ≥0∞ := fun ω =>
    ENNReal.ofReal (Matrix.trace (NormedSpace.exp (s.val • X ω)))
  have hcontExp : Continuous (NormedSpace.exp : Matrix ι ι ℝ → Matrix ι ι ℝ) :=
    continuous_iff_continuousAt.mpr fun A =>
      (NormedSpace.exp_analytic (𝕂 := ℝ) A).continuousAt
  have hcontTrace : Continuous (Matrix.trace : Matrix ι ι ℝ → ℝ) :=
    (Matrix.traceLinearMap ι ℝ ℝ).continuous_of_finiteDimensional
  have hF : AEMeasurable F μ :=
    ENNReal.measurable_ofReal.comp_aemeasurable
      ((hcontTrace.comp hcontExp).comp_aestronglyMeasurable
        (hX.const_smul s.val)).aemeasurable
  have hinc : {ω | t ≤ sSup (spectrum ℝ (X ω))} ≤ᵐ[μ]
      {ω | ENNReal.ofReal (Real.exp (s.val * t)) ≤ F ω} := by
    filter_upwards [hherm] with ω hh ht
    apply ENNReal.ofReal_le_ofReal
    exact (Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left ht s.property.le)).trans
      (exp_max_eigenvalue_le_trace_exp _ hh s.val)
  calc
    _ ≤ μ {ω | ENNReal.ofReal (Real.exp (s.val * t)) ≤ F ω} := measure_mono_ae hinc
    _ ≤ (∫⁻ ω, F ω ∂μ) / ENNReal.ofReal (Real.exp (s.val * t)) :=
      meas_ge_le_lintegral_div hF
        (by simp only [ne_eq, ENNReal.ofReal_eq_zero]; exact not_le.mpr (Real.exp_pos _))
        ENNReal.ofReal_ne_top
    _ = _ := by
      rw [div_eq_mul_inv, ← ENNReal.ofReal_inv_of_pos (Real.exp_pos _), ← Real.exp_neg]
      exact mul_comm _ _

end AutoSamplingTheory.TechnicalLemmas.Probability.MatrixLaplaceTail
