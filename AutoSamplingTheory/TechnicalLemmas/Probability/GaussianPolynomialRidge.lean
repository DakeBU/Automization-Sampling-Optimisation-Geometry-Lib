import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.Analysis.Polynomial.Basic
import Mathlib.Tactic.Linarith

open MeasureTheory ProbabilityTheory
open scoped ENNReal InnerProductSpace

namespace AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRidge

theorem standard_gaussian_polynomial_ridge_uniform_L2
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (p : Polynomial ℝ) :
    let phi : ℝ → ℝ := fun z => p.eval z
    ∃ hbase : MemLp phi 2 (ProbabilityTheory.gaussianReal 0 1),
      let b : ℝ := ‖hbase.toLp phi‖ + 1
      (0 < b) ∧
      ∃ hfeature : ∀ w : {w : E // ‖w‖ = 1},
        MemLp (fun x : E => phi ⟪w.1, x⟫_ℝ) 2 (ProbabilityTheory.stdGaussian E),
        ∀ w : {w : E // ‖w‖ = 1},
          ‖(hfeature w).toLp (fun x : E => phi ⟪w.1, x⟫_ℝ)‖ = ‖hbase.toLp phi‖ ∧
          ‖(hfeature w).toLp (fun x : E => phi ⟪w.1, x⟫_ℝ)‖ ≤ b := by
  let phi : ℝ → ℝ := fun z => p.eval z
  have hpow : ∀ n : ℕ,
      MemLp (fun z : ℝ => z ^ n) 2 (gaussianReal 0 1) := by
    intro n
    apply (memLp_two_iff_integrable_sq (by fun_prop)).2
    have hid : MemLp (id : ℝ → ℝ) (↑(2 * n) : ℝ≥0∞) (gaussianReal 0 1) :=
      memLp_id_gaussianReal' (↑(2 * n) : ℝ≥0∞) (ENNReal.natCast_ne_top (2 * n))
    have hi := hid.integrable_norm_pow' (p := 2 * n)
    convert hi using 1
    funext z
    change (z ^ n) ^ 2 = ‖z‖ ^ (2 * n)
    rw [Nat.mul_comm 2 n, pow_mul, ← norm_pow, Real.norm_eq_abs, sq_abs]
  have hbase : MemLp phi 2 (gaussianReal 0 1) := by
    change MemLp (fun z : ℝ => p.eval z) 2 (gaussianReal 0 1)
    induction p using Polynomial.induction_on' with
    | add p q hp hq => simpa only [Polynomial.eval_add, Pi.add_def] using hp.add hq
    | monomial n a => simpa only [Polynomial.eval_monomial] using (hpow n).const_mul a
  have hmap : ∀ w : {w : E // ‖w‖ = 1},
      (stdGaussian E).map (fun x : E => ⟪w.1, x⟫_ℝ) = gaussianReal 0 1 := by
    intro w
    change (stdGaussian E).map (innerSL ℝ w.1) = _
    rw [IsGaussian.map_eq_gaussianReal, integral_strongDual_stdGaussian,
      variance_dual_stdGaussian, innerSL_apply_norm, w.2]
    norm_num
  let mp : ∀ w : {w : E // ‖w‖ = 1},
      MeasurePreserving (fun x : E => ⟪w.1, x⟫_ℝ) (stdGaussian E) (gaussianReal 0 1) :=
    fun w => ⟨by fun_prop, hmap w⟩
  let hfeature : ∀ w : {w : E // ‖w‖ = 1},
      MemLp (fun x : E => phi ⟪w.1, x⟫_ℝ) 2 (stdGaussian E) :=
    fun w => hbase.comp_measurePreserving (mp w)
  refine ⟨hbase, ?_, hfeature, ?_⟩
  · exact add_pos_of_nonneg_of_pos (norm_nonneg _) zero_lt_one
  · intro w
    have hn : ‖(hfeature w).toLp (fun x : E => phi ⟪w.1, x⟫_ℝ)‖ = ‖hbase.toLp phi‖ := by
      change ‖Lp.compMeasurePreserving (fun x : E => ⟪w.1, x⟫_ℝ) (mp w)
        (hbase.toLp phi)‖ = ‖hbase.toLp phi‖
      exact Lp.norm_compMeasurePreserving _ _
    exact ⟨hn, hn.trans_le (le_add_of_nonneg_right zero_le_one)⟩

end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRidge
