import GC47Dimension
import GC47Coordinate

/-! Section 4.4: after the Krylov space has full dimension it contains
a fixed unit vector with a large value of the cosine detector. -/
noncomputable section
open MeasureTheory Matrix
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov

theorem saturated_cosine_obstruction {d q : ℕ} {κ : ℝ} (hκ : κ ≠ 1)
    (hn : 2*q+1 < d) (hd : d ≤ (q+1)^2) :
    ∃ u : Fin d → ℝ, ‖WithLp.toLp 2 u‖ = 1 ∧
      1 / Real.sqrt 2 ≤ |u ⬝ᵥ (cosineDiag d q *ᵥ u)| ∧
      ∀ᵐ g ∂gaussianStarts d q, u ∈ krylov d q κ g := by
  obtain ⟨u,hu,hform⟩ := unit_coordinate_obstruction hn
  refine ⟨u,hu,hform,?_⟩
  filter_upwards [gaussian_krylov_eq_top hκ hd] with g hg
  rw [hg]
  exact Submodule.mem_top

#print axioms saturated_cosine_obstruction
end AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
