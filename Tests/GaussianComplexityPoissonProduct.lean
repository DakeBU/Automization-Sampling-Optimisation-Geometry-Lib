import AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LaplacianProduct
import AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactPoissonSmoothGraph
import Mathlib.Analysis.InnerProductSpace.Calculus
import Mathlib.Analysis.InnerProductSpace.PiL2

open AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus

/- The literal spherical Poisson kernel is smooth locally inside the ball.
Its pole is not globally C2; no global smoothness premise is supplied.
This is the product expansion used before the still-open harmonicity and
mean-value/normalization calculations. The source n>=3 is included. -/
example {n : ℕ} {ζ x : EuclideanSpace ℝ (Fin n)}
    (hζ : ‖ζ‖ = 1) (hx : ‖x‖ < 1) :
    let u : EuclideanSpace ℝ (Fin n) → ℝ := fun z => 1 - ‖z‖ ^ 2
    let v : EuclideanSpace ℝ (Fin n) → ℝ := fun z => (‖z - ζ‖ ^ n)⁻¹
    let P : EuclideanSpace ℝ (Fin n) → ℝ :=
      fun z => (1 - ‖z‖ ^ 2) / ‖z - ζ‖ ^ n
    Laplacian.laplacian P x =
      u x * Laplacian.laplacian v x +
      2 * inner ℝ (gradient u x) (gradient v x) +
      v x * Laplacian.laplacian u x := by
  have hne : x - ζ ≠ 0 := by
    apply sub_ne_zero.mpr
    intro h
    rw [h, hζ] at hx
    exact (lt_irrefl (1 : ℝ)) hx
  dsimp only
  simp only [div_eq_mul_inv]
  apply LaplacianProduct.laplacian_mul
  · exact contDiffAt_const.sub (contDiffAt_id.norm_sq ℝ)
  · exact (((contDiffAt_id.sub contDiffAt_const).norm ℝ hne).pow n).inv
      (pow_ne_zero n (norm_ne_zero_iff.mpr hne))

#print axioms AutoSamplingTheory.TechnicalLemmas.Analysis.Calculus.LaplacianProduct.laplacian_mul
#print axioms AutoSamplingTheory.TechnicalLemmas.FunctionalInequalities.CompactPoissonSmoothGraph.compact_weak_poisson_smooth_graph_approximation
