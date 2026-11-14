import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineExpansion

open scoped BigOperators
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumCosineExpansion

private theorem actual_inverse_grid_cosine_series {d : ℕ} (hd : 2 ≤ d) {κ : ℝ} (hκ : 2 ≤ κ) (n : ℕ) :
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  (∑ i : Fin d, Real.cos ((n : ℝ) * θ i) / eigenvalue i) =
    (1 / Real.sqrt κ) *
      ((∑ i : Fin d, Real.cos ((n : ℝ) * θ i)) +
        2 * ∑' j : ℕ, (-r) ^ (j + 1) *
          (∑ i : Fin d, Real.cos ((n : ℝ) * θ i) *
            Real.cos (((j + 1 : ℕ) : ℝ) * θ i))) := by
  let θ : Fin d → ℝ := fun i => ((i.val : ℝ) + 1 / 2) * Real.pi / (d : ℝ)
  let eigenvalue : Fin d → ℝ := fun i => (κ + 1) / 2 + (κ - 1) / 2 * Real.cos (θ i)
  let r : ℝ := (Real.sqrt κ - 1) / (Real.sqrt κ + 1)
  let w : Fin d → ℝ := fun i => Real.cos ((n : ℝ) * θ i)
  let f : Fin d → ℕ → ℝ := fun i j =>
    (-r) ^ (j + 1) * Real.cos (((j + 1 : ℕ) : ℝ) * θ i)
  let g : Fin d → ℕ → ℝ := fun i j =>
    (-r) ^ (j + 1) * (w i * Real.cos (((j + 1 : ℕ) : ℝ) * θ i))
  change (∑ i : Fin d, w i / eigenvalue i) =
    (1 / Real.sqrt κ) * ((∑ i : Fin d, w i) +
      2 * ∑' j : ℕ, (-r) ^ (j + 1) *
        (∑ i : Fin d, w i * Real.cos (((j + 1 : ℕ) : ℝ) * θ i)))
  obtain ⟨heq, habs, _⟩ := actual_inverse_spectrum_cosine_expansion hκ
  have hs (i : Fin d) : Summable (f i) := (habs (θ i)).of_norm
  have hsg (i : Fin d) : Summable (g i) :=
    ((hs i).mul_left (w i)).congr (fun j => by dsimp [g, f]; ring)
  have hlin (i : Fin d) : (∑' j : ℕ, g i j) = w i * (∑' j : ℕ, f i j) := by
    calc
      _ = ∑' j : ℕ, w i * f i j := tsum_congr (fun j => by dsimp [g, f]; ring)
      _ = _ := (hs i).tsum_mul_left (w i)
  have heigen (i : Fin d) : (eigenvalue i)⁻¹ =
      (1 / Real.sqrt κ) * (1 + 2 * ∑' j : ℕ, f i j) := by
    have htwice : 2 * eigenvalue i = κ + 1 + (κ - 1) * Real.cos (θ i) := by
      dsimp [eigenvalue]
      ring
    have hrecip : (eigenvalue i)⁻¹ = 2 / (κ + 1 + (κ - 1) * Real.cos (θ i)) := by
      rw [← htwice, div_mul_eq_div_div]
      norm_num
    have h := heq (θ i)
    change 2 / (κ + 1 + (κ - 1) * Real.cos (θ i)) =
      (1 / Real.sqrt κ) * (1 + 2 * ∑' j : ℕ, f i j) at h
    exact hrecip.trans h
  have hscalar (i : Fin d) : w i / eigenvalue i =
      (1 / Real.sqrt κ) * (w i + 2 * ∑' j : ℕ, g i j) := by
    rw [div_eq_mul_inv, heigen, hlin]
    ring
  have hexchange : (∑' j : ℕ, ∑ i : Fin d, g i j) =
      ∑ i : Fin d, ∑' j : ℕ, g i j :=
    Summable.tsum_finsetSum (fun i _ => hsg i)
  have hfactor (j : ℕ) : (∑ i : Fin d, g i j) =
      (-r) ^ (j + 1) * (∑ i : Fin d, w i * Real.cos (((j + 1 : ℕ) : ℝ) * θ i)) := by
    dsimp [g]
    rw [Finset.mul_sum]
  calc
    _ = ∑ i : Fin d, (1 / Real.sqrt κ) * (w i + 2 * ∑' j : ℕ, g i j) :=
      Finset.sum_congr rfl (fun i _ => hscalar i)
    _ = (1 / Real.sqrt κ) * ((∑ i : Fin d, w i) +
        2 * (∑ i : Fin d, ∑' j : ℕ, g i j)) := by
      rw [← Finset.mul_sum, Finset.sum_add_distrib, ← Finset.mul_sum]
    _ = (1 / Real.sqrt κ) * ((∑ i : Fin d, w i) +
        2 * (∑' j : ℕ, ∑ i : Fin d, g i j)) := by rw [hexchange]
    _ = _ := by simp_rw [hfactor]
