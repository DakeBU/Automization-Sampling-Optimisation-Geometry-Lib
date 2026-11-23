import GC44Uniform

/-! At κ = 2, the uniform bound applies to every fixed query index once the
dimension is large. The experiment and its independent Gaussian starts can
be chosen after the dimension. -/

open MeasureTheory ProbabilityTheory Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumTargetEvent
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.KrylovWitness

theorem eventually_fixed_degree_independent_starts (q : ℕ) :
    ∃ D : ℕ, ∀ d ≥ D, ∀ {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
      (g : Fin (q+1) → Ω → Space d),
      (∀ a, MeasurePreserving (g a) μ (stdGaussian (Space d))) → iIndepFun g μ →
      ∃ G : Set Ω, MeasurableSet G ∧ (99/100 : ℝ) ≤ μ.real G ∧
        ∀ ω ∈ G, ∀ u ∈ krylov d q 2 (fun a => g a ω),
        |u ⬝ᵥ (cosineDiag d q *ᵥ u)| ≤ 2*queryThreshold 2048 d q*‖WithLp.toLp 2 u‖^2 := by
  obtain ⟨D,hD⟩ := eventual_source_signal 2048 (by norm_num) (δ := 1/2) (by norm_num) (by norm_num)
  obtain ⟨N, hN⟩ := exists_nat_ge (Real.exp (512*(q:ℝ)))
  refine ⟨max 4 (max D N), ?_⟩
  intro d hd
  have hd4 : 4 ≤ d := (le_max_left ..).trans hd
  have hdD : D ≤ d := (le_max_left ..).trans ((le_max_right ..).trans hd)
  have hdN : N ≤ d := (le_max_right ..).trans ((le_max_right ..).trans hd)
  have hpos : 0 < (d : ℝ) := by exact_mod_cast (show 0 < d by omega)
  have hdim : (2 : ℝ) ≤ (d : ℝ)^(1-(1/2 : ℝ)) := by
    rw [show 1 - (1/2 : ℝ) = 1/2 by norm_num, ← Real.sqrt_eq_rpow]
    apply Real.le_sqrt_of_sq_le
    norm_num
    exact_mod_cast hd4
  have hlog : 512*(q:ℝ) ≤ Real.log (d : ℝ) :=
    (Real.le_log_iff_exp_le hpos).mpr (hN.trans (by exact_mod_cast hdN))
  have hnonneg : 0 ≤ Real.log (d : ℝ) := by linarith [Nat.cast_nonneg (α := ℝ) q]
  have hq : (q : ℝ) ≤ (1/2)/256 * Real.sqrt 2 * Real.log (d : ℝ) := by
    have hs : 1 ≤ Real.sqrt 2 := Real.le_sqrt_of_sq_le (by norm_num)
    nlinarith [mul_nonneg (sub_nonneg.mpr hs) hnonneg]
  obtain ⟨_, _, hmode, _, _, ht, _⟩ := hD d hdD 2 le_rfl hdim q hq
  intro Ω _ μ g hg hi
  exact uniform_bound_independent_gaussian_starts le_rfl hmode ht μ g hg hi

#print axioms eventually_fixed_degree_independent_starts

end AutoSamplingTheory.ExampleCases.GaussianComplexity.KrylovWitness
