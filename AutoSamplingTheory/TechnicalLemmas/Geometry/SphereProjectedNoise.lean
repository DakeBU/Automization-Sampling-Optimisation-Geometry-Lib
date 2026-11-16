import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.Calculus.FDeriv.Mul
import Mathlib.Tactic.Ring

namespace AutoSamplingTheory.TechnicalLemmas.Geometry.SphereProjectedNoise

open scoped BigOperators RealInnerProductSpace

variable {ι : Type*} [Fintype ι] [DecidableEq ι]
local notation "V" => EuclideanSpace ℝ ι

/-- The column of the ambient rank-one sphere projection formula. -/
noncomputable def projectedNoiseColumn (j : ι) (x : V) : V :=
  EuclideanSpace.single j 1 - (x j) • x

/-- The radial component of a projected coordinate column. -/
theorem inner_projectedNoiseColumn (j : ι) (x : V) :
    inner ℝ x (projectedNoiseColumn j x) = (1 - ‖x‖ ^ 2) * x j := by
  simp only [projectedNoiseColumn, inner_sub_right, EuclideanSpace.inner_single_right,
    real_inner_smul_right, conj_trivial, one_mul, real_inner_self_eq_norm_sq]
  ring

/-- The sum of column norms is the ambient Frobenius square. -/
theorem sum_norm_sq_projectedNoiseColumn (x : V) :
    (∑ j : ι, ‖projectedNoiseColumn j x‖ ^ 2) =
      (Fintype.card ι : ℝ) - 2 * ‖x‖ ^ 2 + ‖x‖ ^ 4 := by
  have hOne (j : ι) : ‖projectedNoiseColumn j x‖ ^ 2 =
      1 - 2 * (x j) ^ 2 + ‖x‖ ^ 2 * (x j) ^ 2 := by
    rw [projectedNoiseColumn, norm_sub_sq_real, norm_smul, mul_pow,
      Real.norm_eq_abs, sq_abs, PiLp.norm_single, norm_one, one_pow,
      real_inner_smul_right, EuclideanSpace.inner_single_left]
    simp only [conj_trivial, one_mul]
    ring
  have hSq : (∑ j : ι, (x j) ^ 2) = ‖x‖ ^ 2 := by
    simp only [PiLp.norm_sq_eq_of_L2, Real.norm_eq_abs, sq_abs]
  simp_rw [hOne]
  rw [Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum,
    ← Finset.mul_sum, hSq]
  simp
  ring

/-- The derivative of one projected coordinate field in an ambient direction. -/
theorem fderiv_projectedNoiseColumn_apply (j : ι) (x u : V) :
    fderiv ℝ (projectedNoiseColumn j) x u = -(x j • u + u j • x) := by
  let L : V →L[ℝ] ℝ := PiLp.proj (p := 2) (𝕜 := ℝ) (β := fun _ : ι => ℝ) j
  have h := L.hasFDerivAt.smul (hasFDerivAt_id (𝕜 := ℝ) x)
  have hF := ((hasFDerivAt_const (𝕜 := ℝ) (EuclideanSpace.single j (1 : ℝ)) x).sub h).fderiv
  change fderiv ℝ (projectedNoiseColumn j) x =
    0 - (L x • ContinuousLinearMap.id ℝ V + L.smulRight x) at hF
  rw [hF]
  simp [L]

/-- The column derivative contraction is the geometric Stratonovich correction
before multiplication by half the squared noise amplitude. -/
theorem sum_fderiv_projectedNoiseColumn_apply (x : V) :
    (∑ j : ι, fderiv ℝ (projectedNoiseColumn j) x (projectedNoiseColumn j x)) =
      (2 * ‖x‖ ^ 2 - ((Fintype.card ι : ℝ) + 1)) • x := by
  have hSq : (∑ j : ι, (x j) ^ 2) = ‖x‖ ^ 2 := by
    simp only [PiLp.norm_sq_eq_of_L2, Real.norm_eq_abs, sq_abs]
  have hTerm (j k : ι) :
      (fderiv ℝ (projectedNoiseColumn j) x (projectedNoiseColumn j x)) k =
        (2 * (x j) ^ 2) * x k - (if k = j then x j else 0) - x k := by
    rw [fderiv_projectedNoiseColumn_apply]
    simp only [projectedNoiseColumn, PiLp.neg_apply, PiLp.add_apply, PiLp.sub_apply,
      PiLp.smul_apply, smul_eq_mul, PiLp.single_apply]
    by_cases h : k = j
    · simp [h]
      ring
    · simp [h]
      ring
  ext k
  let L : V →L[ℝ] ℝ := PiLp.proj (p := 2) (𝕜 := ℝ) (β := fun _ : ι => ℝ) k
  change L (∑ j : ι, fderiv ℝ (projectedNoiseColumn j) x (projectedNoiseColumn j x)) = _
  rw [map_sum]
  change (∑ j : ι, (fderiv ℝ (projectedNoiseColumn j) x (projectedNoiseColumn j x)) k) =
    (2 * ‖x‖ ^ 2 - ((Fintype.card ι : ℝ) + 1)) * x k
  simp_rw [hTerm]
  simp only [Finset.sum_sub_distrib, ← Finset.sum_mul, ← Finset.mul_sum, hSq,
    Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  simp only [Finset.sum_ite_eq, Finset.mem_univ, if_true]
  ring

end AutoSamplingTheory.TechnicalLemmas.Geometry.SphereProjectedNoise
