import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianHermiteGram
import AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRidgeSmooth

open MeasureTheory ProbabilityTheory Polynomial
open scoped ENNReal InnerProductSpace BigOperators

namespace AutoSamplingTheory.TechnicalLemmas.Probability.GaussianHermiteFeatures

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
  [FiniteDimensional ℝ E] [MeasurableSpace E] [BorelSpace E]

noncomputable def gaussianHermiteRidgeL2 (j : ℕ) (w : E) : Lp ℝ 2 (stdGaussian E) :=
  let p := (hermite j).map (algebraMap ℤ ℝ)
  (Classical.choose
    (AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRidgeSmooth.standard_gaussian_polynomial_ridge_L2_smooth (E := E) p) w).toLp
      (fun x : E => p.eval ⟪w,x⟫_ℝ)

noncomputable def finiteGaussianHermiteRidgeL2 (s : Finset ℕ) (c : ℕ → ℝ)
    (w : E) : Lp ℝ 2 (stdGaussian E) :=
  ∑ j ∈ s, c j • gaussianHermiteRidgeL2 j w

theorem gaussianHermiteRidgeL2_contDiff (j : ℕ) :
    ContDiff ℝ 2 (gaussianHermiteRidgeL2 (E := E) j) := by
  exact (Classical.choose_spec
    (AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRidgeSmooth.standard_gaussian_polynomial_ridge_L2_smooth
      (E := E) ((hermite j).map (algebraMap ℤ ℝ)))).of_le (ENat.natCast_le_of_coe_top_le_withTop le_rfl 2)

theorem gaussianHermiteRidgeL2_ae (j : ℕ) (w : E) :
    (gaussianHermiteRidgeL2 j w : E → ℝ) =ᵐ[stdGaussian E]
      fun x => aeval ⟪w,x⟫_ℝ (hermite j) := by
  unfold gaussianHermiteRidgeL2
  filter_upwards [MemLp.coeFn_toLp (f := fun x : E =>
    ((hermite j).map (algebraMap ℤ ℝ)).eval ⟪w,x⟫_ℝ)
    (Classical.choose
      (AutoSamplingTheory.TechnicalLemmas.Probability.GaussianPolynomialRidgeSmooth.standard_gaussian_polynomial_ridge_L2_smooth
        (E := E) ((hermite j).map (algebraMap ℤ ℝ))) w)] with x hx
  rw [hx]
  exact eval_map_algebraMap _ _

theorem finiteGaussianHermiteRidgeL2_inner
    (S : Finset ℕ) (c : ℕ → ℝ) (w z : E) (hw : ‖w‖ = 1) (hz : ‖z‖ = 1) :
    ⟪finiteGaussianHermiteRidgeL2 S c w, finiteGaussianHermiteRidgeL2 S c z⟫_ℝ =
      ∑ j ∈ S, ((j.factorial : ℝ) * (c j)^2) * ⟪w,z⟫_ℝ ^ j := by
  let k : ℕ → ℝ := fun j => ((j.factorial : ℝ) * (c j)^2) * ⟪w,z⟫_ℝ ^ j
  have hinner (i j : ℕ) : ⟪gaussianHermiteRidgeL2 i w, gaussianHermiteRidgeL2 j z⟫_ℝ =
      if i = j then (i.factorial : ℝ) * ⟪w,z⟫_ℝ ^ i else 0 := by
    rw [MeasureTheory.L2.inner_def]
    calc
      _ = ∫ x, aeval ⟪w,x⟫_ℝ (hermite i) * aeval ⟪z,x⟫_ℝ (hermite j)
          ∂stdGaussian E := by
        apply integral_congr_ae
        filter_upwards [gaussianHermiteRidgeL2_ae i w, gaussianHermiteRidgeL2_ae j z] with x h1 h2
        rw [Real.inner_apply, h1, h2]
      _ = _ :=
        (AutoSamplingTheory.TechnicalLemmas.Probability.GaussianHermiteGram.gaussian_hermite_ridge_gram
          w z hw hz i j).2
  have hdiag (i j : ℕ) :
      ⟪c i • gaussianHermiteRidgeL2 i w, c j • gaussianHermiteRidgeL2 j z⟫_ℝ =
        if i = j then k i else 0 := by
    rw [real_inner_smul_left, inner_smul_right, hinner]
    by_cases h : i = j
    · subst j
      simp [k]
      ring
    · simp [h]
  unfold finiteGaussianHermiteRidgeL2
  rw [sum_inner]
  apply Finset.sum_congr rfl
  intro i hi
  rw [inner_sum]
  simp_rw [hdiag]
  rw [Finset.sum_eq_single_of_mem i hi]
  · simp [k]
  · intro j _ hij
    simp [Ne.symm hij]

theorem finiteGaussianHermiteRidgeL2_contDiff (s : Finset ℕ) (c : ℕ → ℝ) :
    ContDiff ℝ 2 (finiteGaussianHermiteRidgeL2 (E := E) s c) := by
  unfold finiteGaussianHermiteRidgeL2
  exact ContDiff.sum fun j _ => (gaussianHermiteRidgeL2_contDiff j).const_smul (c j)

#print axioms gaussianHermiteRidgeL2_ae
#print axioms finiteGaussianHermiteRidgeL2_inner
#print axioms finiteGaussianHermiteRidgeL2_contDiff

end AutoSamplingTheory.TechnicalLemmas.Probability.GaussianHermiteFeatures
