import AutoSamplingTheory.TechnicalLemmas.Analysis.StrongConvexFirstOrder
import Mathlib.Analysis.Calculus.LocalExtr.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt

/-!
# Finite restart reduction

Chewi arXiv2605.07006v1 Section4.1 Lemma4.1: the prescribed radius schedule,
its radius-halving induction, and final polishing call. The base solver accepts
an upper radius certificate and returns an output plus a certified natural cost.
This is finite composition of that source-assumed solver contract, not a formal
first-order oracle machine or a logarithmic asymptotic theorem. C1 Hilbert
regularity is sufficient for the sharp quadratic-growth argument.
-/
namespace AutoSamplingTheory.TechnicalLemmas.Analysis.RestartReduction
open Set
variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [CompleteSpace E]

/-- Actual scheduled restart states halve their certified radius; one final
polishing call reaches the requested accuracy with the exact finite budget. -/
theorem radius_accuracy_and_cost {f : E → ℝ} {α β R ε : ℝ}
    (hf : ContDiff ℝ 1 f) (hsc : StrongConvexOn univ α f)
    (hα : 0 < α) (hβ : 0 < β) (hR : 0 < R) (hε : 0 < ε)
    {z x₀ : E} (hmin : IsMinOn f univ z) (hx₀ : ‖x₀-z‖ ≤ R)
    (A : E → ℝ → ℝ → E × ℕ) (φ : ℝ → ℕ)
    (hA : ∀ y r δ, 0 < r → 0 < δ → ‖y-z‖ ≤ r →
      f (A y r δ).1 - f z ≤ δ ∧ (A y r δ).2 ≤ φ (β*r^2/δ))
    (N : ℕ) (hN : α * (R / (2:ℝ)^N)^2 ≤ ε) :
    let r := fun k : ℕ => R / (2:ℝ)^k
    let run : ℕ → E × ℕ := Nat.rec (x₀, 0) (fun k p =>
      let w := A p.1 (r k) (α*(r k)^2/8)
      (w.1, p.2 + w.2))
    let last := A (run N).1 (Real.sqrt (ε/α)) ε
    ‖(run N).1-z‖ ≤ r N ∧ (run N).2 ≤ N * φ (8*(β/α)) ∧
      f last.1 - f z ≤ ε ∧ (run N).2 + last.2 ≤ N * φ (8*(β/α)) + φ (β/α) := by
  let r := fun k : ℕ => R / (2:ℝ)^k
  let run : ℕ → E × ℕ := Nat.rec (x₀, 0) (fun k p =>
    let w := A p.1 (r k) (α*(r k)^2/8)
    (w.1, p.2 + w.2))
  change ‖(run N).1-z‖ ≤ r N ∧ (run N).2 ≤ N * φ (8*(β/α)) ∧ _
  have hr (k : ℕ) : 0 < r k := div_pos hR (pow_pos (by norm_num) _)
  have hgrad : gradient f z = 0 := by
    simp [gradient, (hmin.isLocalMin Filter.univ_mem).fderiv_eq_zero]
  have hqg (y : E) : α/2 * ‖y-z‖^2 ≤ f y - f z := by
    have h := StrongConvexFirstOrder.firstOrder_lower_bound_of_strongConvexOn hsc
      (fun x _ => (hf.differentiable_one x).hasGradientAt) (mem_univ z) (mem_univ y)
    rw [hgrad, inner_zero_left] at h
    linarith
  have hind (k : ℕ) : ‖(run k).1-z‖ ≤ r k ∧ (run k).2 ≤ k * φ (8*(β/α)) := by
    induction k with
    | zero => simpa [run, r] using hx₀
    | succ k ih =>
      have hδ : 0 < α*(r k)^2/8 := by positivity
      have hw := hA (run k).1 (r k) (α*(r k)^2/8) (hr k) hδ ih.1
      have hid : β*(r k)^2 / (α*(r k)^2/8) = 8*(β/α) := by
        field_simp [ne_of_gt (hr k)]
      rw [hid] at hw
      have hs : r (k+1) = r k / 2 := by dsimp [r]; rw [pow_succ, div_mul_eq_div_div]
      constructor
      · change ‖(A (run k).1 (r k) (α*(r k)^2/8)).1-z‖ ≤ r (k+1)
        rw [hs]
        have hg := (hqg (A (run k).1 (r k) (α*(r k)^2/8)).1).trans hw.1
        have hsquare : ‖(A (run k).1 (r k) (α*(r k)^2/8)).1-z‖^2 ≤ (r k/2)^2 := by
          nlinarith
        nlinarith [norm_nonneg ((A (run k).1 (r k) (α*(r k)^2/8)).1-z), hr k]
      · change (run k).2 + (A (run k).1 (r k) (α*(r k)^2/8)).2 ≤ (k+1) * φ (8*(β/α))
        simpa only [Nat.add_mul, Nat.one_mul] using Nat.add_le_add ih.2 hw.2
  have hs : r N ≤ Real.sqrt (ε/α) := by
    apply Real.le_sqrt_of_sq_le
    exact (le_div_iff₀ hα).mpr (by nlinarith [hN])
  have hlast := hA (run N).1 (Real.sqrt (ε/α)) ε
    (Real.sqrt_pos.mpr (div_pos hε hα)) hε ((hind N).1.trans hs)
  have hid : β * (Real.sqrt (ε/α))^2 / ε = β/α := by
    rw [Real.sq_sqrt (div_nonneg hε.le hα.le)]
    field_simp
  rw [hid] at hlast
  exact ⟨(hind N).1, (hind N).2, hlast.1, Nat.add_le_add (hind N).2 hlast.2⟩
end AutoSamplingTheory.TechnicalLemmas.Analysis.RestartReduction
