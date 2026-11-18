import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialPotentialSmooth

open MeasureTheory ProbabilityTheory
open scoped ENNReal InnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialPotentialSmooth

-- Two different parameter laws share one third-derivative bound.
example {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]
    (P : Measure (E × ℝ)) [IsProbabilityMeasure P]
    (hGaussian : P.map Prod.fst = stdGaussian E)
    (p : Polynomial ℝ) (hlabel : MemLp (fun z : E × ℝ => z.2) 2 P) (R : ℝ) :
    let S := {w : E // ‖w‖ = 1}
    let V : Measure S → E → ℝ := fun ρ w =>
      2 * ∫ z : E × ℝ,
        ((∫ v : S, p.eval ⟪(v : E), z.1⟫_ℝ ∂ρ) - z.2) *
          p.eval ⟪w, z.1⟫_ℝ ∂P
    ∃ C : ℝ, 0 ≤ C ∧ ∀ (ρ ν : Measure S),
      IsProbabilityMeasure ρ → IsProbabilityMeasure ν →
      ∀ w : E, ‖w‖ ≤ R →
        ‖iteratedFDeriv ℝ 3 (V ρ) w‖ + ‖iteratedFDeriv ℝ 3 (V ν) w‖ ≤ 2 * C := by
  intro S V
  obtain ⟨C, hC, hbound⟩ :=
    (gaussian_polynomial_joint_potential_smooth_uniform_derivatives P hGaussian p hlabel).2 R 3
  refine ⟨C, hC, ?_⟩
  intro ρ ν hρ hν w hw
  exact (add_le_add (hbound ρ hρ w hw) (hbound ν hν w hw)).trans_eq (two_mul C).symm

#check gaussian_polynomial_joint_potential_smooth_uniform_derivatives
#print axioms gaussian_polynomial_joint_potential_smooth_uniform_derivatives
