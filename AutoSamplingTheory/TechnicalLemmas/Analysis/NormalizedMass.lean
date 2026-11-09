/-
Copyright (c) 2026 Samplinglib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
import Mathlib.Analysis.Real.Sqrt
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!+# A deterministic bound for a normalized bad mass

Zhou–Suzuki, arXiv:2611.05813v1, §6.4, Fact 12, equation (60).
The source is CC BY 4.0; this is an original Lean implementation of its scalar proof.
The consumer is the following proof of Theorem 7 with `g = Z_good / M` and
`b = Z_bad / M`. No assertion about those random quantities or their moments
is made here. Positive total mass rules out the zero-denominator convention.
-/

namespace AutoSamplingTheory.TechnicalLemmas.Analysis.NormalizedMass

/-- The bad fraction is bounded by bad mass plus square-root error, and then by
bad mass plus quadratic error. These are both inequalities of source Fact 12.
The source's nonnegativity condition on `b` is retained even though the first
square identity already holds for real `b` whenever the total mass is positive.
Neither individual mass is required to be strictly positive. -/
theorem bad_mass_ratio_bounds {g b : ℝ} (hg : 0 ≤ g) (hb : 0 ≤ b) (hpos : 0 < g + b) :
    b / (g + b) ≤ b + (1 - Real.sqrt g) ^ 2 ∧
      b + (1 - Real.sqrt g) ^ 2 ≤ b + (1 - g) ^ 2 := by
  have hs := Real.sqrt_nonneg g
  have hs2 := Real.sq_sqrt hg
  constructor
  · have hdiff : b + (1 - Real.sqrt g) ^ 2 - b / (g + b) =
        (g + b - Real.sqrt g) ^ 2 / (g + b) := by
      field_simp
      ring_nf
      rw [hs2]
      ring
    apply sub_nonneg.mp
    rw [hdiff]
    exact div_nonneg (sq_nonneg _) hpos.le
  · have hden : 0 < 1 + Real.sqrt g := by linarith
    have hfactor : (1 - Real.sqrt g) * (1 + Real.sqrt g) = 1 - g := by
      nlinarith [hs2]
    have hid : (1 - Real.sqrt g) ^ 2 = (1 - g) ^ 2 / (1 + Real.sqrt g) ^ 2 := by
      apply (eq_div_iff (pow_ne_zero 2 hden.ne')).2
      rw [← mul_pow, hfactor]
    apply add_le_add le_rfl
    rw [hid]
    exact div_le_self (sq_nonneg _) (by nlinarith)

end AutoSamplingTheory.TechnicalLemmas.Analysis.NormalizedMass
