import GC13KnownMinimum

/-! The constant-accuracy logarithmic lower bound in Remark 1.3, at κ=2. -/
noncomputable section
open scoped ENNReal
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.LogConcaveSubclass

universe u v

theorem known_min_condition_two :
    ∃ d₀ : ℕ, ∀ d ≥ d₀, ENNReal.ofReal (Real.sqrt 2 / 512 * Real.log (d : ℝ)) ≤
      knownMinQueryComplexity.{u,v} d 2 (1/10) := by
  obtain ⟨D,hD⟩ := known_min_query_bound_general_condition.{u,v} (δ := 1/2) (by norm_num) (by norm_num)
  refine ⟨max D 4,?_⟩
  intro d hd
  have hd4 := (le_max_right D 4).trans hd
  have hk : (2 : ℝ) ≤ (d : ℝ)^(1-(1/2:ℝ)) := by
    rw [show 1-(1/2:ℝ) = 1/2 by norm_num, ← Real.sqrt_eq_rpow]
    apply Real.le_sqrt_of_sq_le
    norm_num
    exact_mod_cast hd4
  have h := hD d ((le_max_left D 4).trans hd) 2 le_rfl hk (1/10) (by norm_num) le_rfl
  convert h using 2
  ring

/-- Every feasible natural query cap obeys the logarithmic bound, including
algorithms that can stop earlier on a particular input or seed. -/
theorem known_min_cap_condition_two :
    ∃ d₀ : ℕ, ∀ d ≥ d₀, ∀ q : ℕ, FeasibleWithKnownMin.{u,v} d 2 (1/10) q →
      Real.sqrt 2 / 512 * Real.log (d : ℝ) ≤ (q : ℝ) := by
  obtain ⟨D,hD⟩ := known_min_condition_two.{u,v}
  refine ⟨D,?_⟩
  intro d hd q hq
  apply ENNReal.ofReal_le_natCast.mp
  exact (hD d hd).trans (iInf_le (fun t : {t : ℕ // FeasibleWithKnownMin.{u,v} d 2 (1/10) t} =>
    (t.val : ℝ≥0∞)) ⟨q,hq⟩)

#print axioms known_min_condition_two
end AutoSamplingTheory.ExampleCases.GaussianComplexity.LogConcaveSubclass
