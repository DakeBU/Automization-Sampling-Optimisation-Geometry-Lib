import GC47Limitation

/-! Independent checks of the two sides of the dimension transition in Lemma 4.7. -/
noncomputable section
open MeasureTheory ProbabilityTheory Matrix
open AutoSamplingTheory.ExampleCases.GaussianComplexity.FixedSpectrumKrylov
namespace AutoSamplingTheory.ExampleCases.GaussianComplexity.KrylovDimensionBoundary

/-- One Gaussian start spans a line, even though the spectrum itself has seven nodes. -/
theorem zero_query_line :
    ∀ᵐ g ∂gaussianStarts 7 0, Module.finrank ℝ (krylov 7 0 2 g) = 1 := by
  exact dimension_of_gaussian_krylov (d := 7) (q := 0) (by norm_num : (2 : ℝ) ≠ 1)

/-- The three starts and their first two powers fill both the eight- and nine-dimensional
spaces. At ten dimensions they almost surely miss one dimension. -/
theorem square_transition :
    (∀ᵐ g ∂gaussianStarts 8 2, krylov 8 2 2 g = ⊤) ∧
    (∀ᵐ g ∂gaussianStarts 9 2, krylov 9 2 2 g = ⊤) ∧
    (∀ᵐ g ∂gaussianStarts 10 2, Module.finrank ℝ (krylov 10 2 2 g) = 9 ∧
      krylov 10 2 2 g ≠ ⊤) := by
  refine ⟨gaussian_krylov_eq_top (by norm_num : (2 : ℝ) ≠ 1) (by decide),
    gaussian_krylov_eq_top (by norm_num : (2 : ℝ) ≠ 1) (by decide), ?_⟩
  filter_upwards [dimension_of_gaussian_krylov (d := 10) (q := 2) (by norm_num : (2 : ℝ) ≠ 1)]
    with g hg
  have hdim : Module.finrank ℝ (krylov 10 2 2 g) = 9 := hg
  refine ⟨hdim, ?_⟩
  intro htop
  rw [htop, finrank_top, Module.finrank_pi, Fintype.card_fin] at hdim
  omega

/-- The dimension on the unsaturated side also holds for independent starts carried
by an arbitrary probability space. -/
theorem independent_starts_at_ten {Ω : Type*} [MeasurableSpace Ω]
    (μ : Measure Ω) [IsProbabilityMeasure μ] (g : Fin 3 → Ω → Space 10)
    (hg : ∀ a, MeasurePreserving (g a) μ (stdGaussian (Space 10))) (hi : iIndepFun g μ) :
    ∀ᵐ ω ∂μ, Module.finrank ℝ (krylov 10 2 2 (fun a => g a ω)) = 9 :=
  dimension_of_independent_gaussian_starts (d := 10) (q := 2)
    (by norm_num : (2 : ℝ) ≠ 1) μ g hg hi

/-- Immediately at the square threshold no uniform bound by one half can hold on all
unit vectors of the realized subspace. -/
theorem strict_obstruction_at_equality :
    ∀ᵐ g ∂gaussianStarts 9 2, ∃ u ∈ krylov 9 2 2 g,
      ‖WithLp.toLp 2 u‖ = 1 ∧ (1:ℝ)/2 < |u ⬝ᵥ (cosineDiag 9 2 *ᵥ u)| := by
  have hgap : (1:ℝ)/2 < 1 / Real.sqrt 2 := by
    apply (div_lt_div_iff₀ (by norm_num : (0:ℝ) < 2) (Real.sqrt_pos.2 (by norm_num))).2
    nlinarith [Real.sq_sqrt (by norm_num : (0:ℝ) ≤ 2)]
  obtain ⟨u,hu,hform,hm⟩ := saturated_cosine_obstruction (d := 9) (q := 2)
    (by norm_num : (2 : ℝ) ≠ 1) (by decide) (by decide)
  filter_upwards [hm] with g hmem
  exact ⟨u, hmem, hu, hgap.trans_le hform⟩

#print axioms square_transition
#print axioms strict_obstruction_at_equality
end AutoSamplingTheory.ExampleCases.GaussianComplexity.KrylovDimensionBoundary
