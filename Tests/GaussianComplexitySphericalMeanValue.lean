import AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.SphericalMeanValue
import AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic.PoissonKernel

open MeasureTheory Metric Set
open scoped RealInnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Analysis.Harmonic

noncomputable section
attribute [local instance] Classical.propDecidable

-- A genuine Poisson consumer: both regularity and pole exclusion are derived.
-- The result is still a focused test, not a published Appendix A1 evaluation.
example {n : ℕ} (hn : 2 ≤ n) (ζ₀ : EuclideanSpace ℝ (Fin n)) (hζ₀ : ‖ζ₀‖ = 1)
    (r : ℝ) (hr : 0 < r) (hr1 : r < 1) :
    let τ := (volume : Measure (EuclideanSpace ℝ (Fin n))).toSphere
    (∫ ζ : sphere (0 : EuclideanSpace ℝ (Fin n)) 1,
      (1 - ‖r • ζ.1‖ ^ 2) / ‖r • ζ.1 - ζ₀‖ ^ n ∂((τ univ)⁻¹ • τ)) = 1 := by
  let P : EuclideanSpace ℝ (Fin n) → ℝ := fun x => (1 - ‖x‖ ^ 2) / ‖x - ζ₀‖ ^ n
  have hpole : closedBall (0 : EuclideanSpace ℝ (Fin n)) r ⊆ {ζ₀}ᶜ := by
    intro x hx heq
    have hxnorm : ‖x‖ ≤ r := mem_closedBall_zero_iff.mp hx
    have he : x = ζ₀ := Set.mem_singleton_iff.mp heq
    rw [he, hζ₀] at hxnorm
    exact (not_le.mpr hr1) hxnorm
  have hP : InnerProductSpace.HarmonicOnNhd P (closedBall 0 r) :=
    (PoissonKernel.poissonKernel_harmonicOnNhd hn ζ₀ hζ₀).mono hpole
  have hm := SphericalMeanValue.harmonic_closedBall_mean_value hn P 0 r hr
    ⟨P, hP, fun _ _ => rfl⟩
  simpa [P, hζ₀] using hm

-- Original data can jump outside the selected closed ball, at any center.
example (a : EuclideanSpace ℝ (Fin 2)) :
    let u : EuclideanSpace ℝ (Fin 2) → ℝ := fun x =>
      if x ∈ closedBall a 2 then 1 else 17
    let τ := (volume : Measure (EuclideanSpace ℝ (Fin 2))).toSphere
    (∫ ζ : sphere (0 : EuclideanSpace ℝ (Fin 2)) 1,
      u (a + (2 : ℝ) • ζ.1) ∂((τ univ)⁻¹ • τ)) = 1 := by
  let u : EuclideanSpace ℝ (Fin 2) → ℝ := fun x =>
    if x ∈ closedBall a 2 then 1 else 17
  have hu : ∃ v : EuclideanSpace ℝ (Fin 2) → ℝ,
      InnerProductSpace.HarmonicOnNhd v (closedBall a 2) ∧ EqOn v u (closedBall a 2) := by
    refine ⟨fun _ => 1, InnerProductSpace.harmonicOnNhd_const 1, ?_⟩
    intro x hx
    simp only [u, if_pos hx]
  have hm := SphericalMeanValue.harmonic_closedBall_mean_value (by norm_num) u a 2
    (by norm_num) hu
  simpa [u] using hm

#print axioms SphericalMeanValue.harmonic_closedBall_mean_value

end
