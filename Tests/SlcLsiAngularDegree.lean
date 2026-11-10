import AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegree
import Mathlib.Tactic.Positivity

open MeasureTheory ProbabilityTheory
open scoped BigOperators NNReal
open AutoSamplingTheory.ExampleCases.SlcLsiQueryComplexity.AngularDegree

-- Exact source-law interface: no supplied tensor norm or Gaussian-law witness.
example (n : ℕ+) (h : ℕ) (i : Fin (h + 1))
    (p : {p : ℕ // Even p ∧ 4 ≤ p ∧ p ≤ 2 ^ (64 * (h + 1))})
    (u : Fin (h - i.val + 1) → EuclideanSpace ℝ (Fin n.val))
    (hu : ∀ j, ‖u j‖ = 1) :
    let S : ℕ := ∑ j : Fin (h - i.val + 1), (2 ^ (74 * (h + 1))) ^ j.val
    let a : ℝ := 1 / ((p.val : ℝ) ^ 4 * (S : ℝ) ^ 2 *
      Real.sqrt ((h - i.val + 1 : ℕ) * Real.log (2 * (2 : ℝ) ^ (64 * (h + 1)) * S)))
    HasLaw (angularDegreeComponent n h i p u)
      (gaussianReal 0 (((n.val : ℝ) * a ^ 2).toNNReal)) (stdGaussian _) :=
  angularDegreeComponent_hasLaw n h i p u hu

-- The coefficient index really has the source dimension n^(p*S_i).
-- This is a semantic representation check, not an additional Registry leaf.
example (n : ℕ+) (h : ℕ) (i : Fin (h + 1)) (p : ℕ) :
    Fintype.card ((Fin p × (Σ j : Fin (h - i.val + 1),
        Fin ((2 ^ (74 * (h + 1))) ^ j.val))) → Fin n.val) =
      n.val ^ (p * ∑ j : Fin (h - i.val + 1), (2 ^ (74 * (h + 1))) ^ j.val) := by
  simp [Fintype.card_sigma]

-- The source amplitude is genuinely positive; totalized division does not
-- introduce a fallback value on the admitted parameter domain.
example (h : ℕ) (i : Fin (h + 1))
    (p : {p : ℕ // Even p ∧ 4 ≤ p ∧ p ≤ 2 ^ (64 * (h + 1))}) :
    let S : ℕ := ∑ j : Fin (h - i.val + 1), (2 ^ (74 * (h + 1))) ^ j.val
    0 < 1 / ((p.val : ℝ) ^ 4 * (S : ℝ) ^ 2 *
      Real.sqrt ((h - i.val + 1 : ℕ) * Real.log (2 * (2 : ℝ) ^ (64 * (h + 1)) * S))) := by
  let S : ℕ := ∑ j : Fin (h - i.val + 1), (2 ^ (74 * (h + 1))) ^ j.val
  have hS : 1 ≤ S := by
    have hterm := Finset.single_le_sum (f := fun j : Fin (h - i.val + 1) ↦
      (2 ^ (74 * (h + 1))) ^ j.val) (fun _ _ ↦ Nat.zero_le _)
      (Finset.mem_univ (⟨0, Nat.zero_lt_succ _⟩ : Fin (h - i.val + 1)))
    simpa [S] using hterm
  have hSr : (1 : ℝ) ≤ S := by exact_mod_cast hS
  have hpr : (0 : ℝ) < p.val := by
    exact_mod_cast (lt_of_lt_of_le (by decide : 0 < 4) p.property.2.1)
  have hP : (1 : ℝ) ≤ (2 : ℝ) ^ (64 * (h + 1)) := one_le_pow₀ (by norm_num)
  have harg : (1 : ℝ) < 2 * (2 : ℝ) ^ (64 * (h + 1)) * S := by
    calc
      (1 : ℝ) < 2 := by norm_num
      _ ≤ 2 * (2 : ℝ) ^ (64 * (h + 1)) * S := by nlinarith
  have hlog := Real.log_pos harg
  change 0 < 1 / ((p.val : ℝ) ^ 4 * (S : ℝ) ^ 2 *
    Real.sqrt ((h - i.val + 1 : ℕ) * Real.log (2 * (2 : ℝ) ^ (64 * (h + 1)) * S)))
  positivity

-- NNReal variance transport is exact, not truncation of a negative expression.
example (n : ℕ+) (a : ℝ) :
    ((((n.val : ℝ) * a ^ 2).toNNReal : ℝ≥0) : ℝ) = (n.val : ℝ) * a ^ 2 := by
  exact Real.coe_toNNReal _ (mul_nonneg (Nat.cast_nonneg _) (sq_nonneg _))

#print axioms angularDegreeComponent_hasLaw
#check @angularDegreeComponent
#check @angularDegreeComponent_hasLaw
