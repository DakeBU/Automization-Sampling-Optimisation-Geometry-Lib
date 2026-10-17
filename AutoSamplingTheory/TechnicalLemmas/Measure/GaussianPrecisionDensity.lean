import AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity
import Mathlib.Analysis.Matrix.Order
import Mathlib.MeasureTheory.Measure.Lebesgue.EqHaar
import Mathlib.LinearAlgebra.Determinant
import Mathlib.Tactic.Ring

/-!
# Canonical volume density of a Gaussian with SPD precision

Standard nondegenerate Gaussian background, including dimension zero. The actual
existing multivariateGaussian covariance-square-root pushforward is identified
with the exact precision density. No new Gaussian constructor is introduced.
-/

open Matrix MeasureTheory ProbabilityTheory
open scoped MatrixOrder
open AutoSamplingTheory.TechnicalLemmas.Measure.IsotropicGaussianDensity
open AutoSamplingTheory.TechnicalLemmas.Measure.RadonNikodym

namespace AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity

private lemma exists_matrix_linearEquiv {n : ℕ} (B : Matrix (Fin n) (Fin n) ℝ)
    (hB : B.det ≠ 0) :
    ∃ e : EuclideanSpace ℝ (Fin n) ≃ₗ[ℝ] EuclideanSpace ℝ (Fin n),
      (∀ x, WithLp.ofLp (e x) = B *ᵥ WithLp.ofLp x) ∧
      (∀ x, WithLp.ofLp (e.symm x) = B⁻¹ *ᵥ WithLp.ofLp x) ∧
      LinearMap.det e.toLinearMap = B.det := by
  let e : EuclideanSpace ℝ (Fin n) ≃ₗ[ℝ] EuclideanSpace ℝ (Fin n) :=
    { toLinearMap := Matrix.toEuclideanLin B
      invFun := Matrix.toEuclideanLin B⁻¹
      left_inv := by
        intro x
        apply WithLp.ofLp_injective
        change B⁻¹ *ᵥ (B *ᵥ WithLp.ofLp x) = WithLp.ofLp x
        rw [Matrix.mulVec_mulVec, Matrix.nonsing_inv_mul _ (isUnit_iff_ne_zero.mpr hB),
          Matrix.one_mulVec]
      right_inv := by
        intro x
        apply WithLp.ofLp_injective
        change B *ᵥ (B⁻¹ *ᵥ WithLp.ofLp x) = WithLp.ofLp x
        rw [Matrix.mulVec_mulVec, Matrix.mul_nonsing_inv _ (isUnit_iff_ne_zero.mpr hB),
          Matrix.one_mulVec] }
  refine ⟨e, fun _ => rfl, fun _ => rfl, ?_⟩
  change LinearMap.det (Matrix.toEuclideanLin B) = B.det
  rw [Matrix.toEuclideanLin_eq_toLin_orthonormal]
  exact LinearMap.det_toLin _ _

theorem multivariateGaussian_eq_withDensity_of_posDef {n : ℕ}
    (A : Matrix (Fin n) (Fin n) ℝ) (hA : A.PosDef) :
    ProbabilityTheory.multivariateGaussian (0 : EuclideanSpace ℝ (Fin n)) A⁻¹ =
      (volume : Measure (EuclideanSpace ℝ (Fin n))).withDensity (fun x =>
        ENNReal.ofReal (Real.sqrt A.det / (2 * Real.pi) ^ ((n : ℝ) / 2) *
          Real.exp (-((WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x)) / 2))) := by
  classical
  let B : Matrix (Fin n) (Fin n) ℝ := CFC.sqrt A⁻¹
  have hAi : A⁻¹.PosDef := hA.inv
  have hBd : B.det = Real.sqrt A⁻¹.det := by
    simpa only [B, RCLike.sqrt_of_nonneg hAi.posSemidef.det_nonneg, RCLike.re_to_real,
      RCLike.ofReal_real_eq_id, id_eq] using
      hAi.posSemidef.det_sqrt
  have hBpos : 0 < B.det := by rw [hBd]; exact Real.sqrt_pos.2 hAi.det_pos
  have hBpsd : B.PosSemidef := (CFC.sqrt_nonneg A⁻¹).posSemidef
  have hBsq : B * B = A⁻¹ := CFC.sqrt_mul_sqrt_self A⁻¹ hAi.posSemidef.nonneg
  have hBinvsq : B⁻¹ * B⁻¹ = A := by
    rw [← Matrix.mul_inv_rev, hBsq,
      Matrix.nonsing_inv_nonsing_inv _ (isUnit_iff_ne_zero.mpr hA.det_pos.ne')]
  have hBts : (B⁻¹).transpose = B⁻¹ := by
    rw [Matrix.transpose_nonsing_inv,
      (Matrix.isHermitian_iff_isSymm.mp hBpsd.isHermitian)]
  obtain ⟨e, he, hei, hedet⟩ := exists_matrix_linearEquiv B hBpos.ne'
  let em : EuclideanSpace ℝ (Fin n) ≃ᵐ EuclideanSpace ℝ (Fin n) :=
    e.toContinuousLinearEquiv.toHomeomorph.toMeasurableEquiv
  have hnorm (x : EuclideanSpace ℝ (Fin n)) :
      ‖em.symm x‖ ^ 2 = (WithLp.ofLp x) ⬝ᵥ (A *ᵥ WithLp.ofLp x) := by
    calc
      _ = (WithLp.ofLp (e.symm x)) ⬝ᵥ (WithLp.ofLp (e.symm x)) := by
        rw [EuclideanSpace.real_norm_sq_eq]
        simp only [dotProduct, pow_two]
        rfl
      _ = _ := by
        rw [hei, dotProduct_comm, ← Matrix.dotProduct_transpose_mulVec,
          hBts, Matrix.mulVec_mulVec, hBinvsq]
  have hdetfactor : |(B.det)⁻¹| = Real.sqrt A.det := by
    rw [hBd, Matrix.det_nonsing_inv, Ring.inverse_eq_inv, Real.sqrt_inv, inv_inv,
      abs_of_nonneg (Real.sqrt_nonneg _)]
  have hmap : (volume : Measure (EuclideanSpace ℝ (Fin n))).map em =
      ENNReal.ofReal |(B.det)⁻¹| • volume := by
    change (volume : Measure (EuclideanSpace ℝ (Fin n))).map e.toLinearMap = _
    simpa only [hedet] using
      (Measure.map_linearMap_addHaar_eq_smul_addHaar (volume : Measure (EuclideanSpace ℝ (Fin n)))
        (f := e.toLinearMap) (by rw [hedet]; exact hBpos.ne'))
  have hstd : stdGaussian (EuclideanSpace ℝ (Fin n)) =
      (volume : Measure (EuclideanSpace ℝ (Fin n))).withDensity (fun x =>
        ENNReal.ofReal (((Real.sqrt (2 * Real.pi))⁻¹) ^ n * Real.exp (-‖x‖ ^ 2 / 2))) := by
    simpa only [Real.sqrt_one, one_smul, Measure.map_id', mul_one,
      finrank_euclideanSpace, Fintype.card_fin] using
      (map_sqrt_smul_stdGaussian_eq_withDensity (E := EuclideanSpace ℝ (Fin n))
        (1 : ℝ) zero_lt_one)
  have hnormalizer : ((Real.sqrt (2 * Real.pi))⁻¹) ^ n =
      1 / (2 * Real.pi) ^ ((n : ℝ) / 2) := by
    rw [inv_pow, ← Real.rpow_natCast, Real.sqrt_eq_rpow,
      ← Real.rpow_mul (by positivity : 0 ≤ 2 * Real.pi)]
    simp only [show (2 : ℝ)⁻¹ * (n : ℝ) = (n : ℝ) / 2 by ring, one_div]
  have hem : (fun x : EuclideanSpace ℝ (Fin n) => Matrix.toEuclideanCLM (𝕜 := ℝ) B x) =
      (em : EuclideanSpace ℝ (Fin n) → EuclideanSpace ℝ (Fin n)) := by
    funext x
    apply WithLp.ofLp_injective
    exact (he x).symm
  rw [multivariateGaussian]
  simp only [zero_add]
  change (stdGaussian (EuclideanSpace ℝ (Fin n))).map (fun x => Matrix.toEuclideanCLM (𝕜 := ℝ) B x) = _
  rw [hem]
  rw [hstd, measurableEquiv_map_withDensity em volume (by fun_prop), hmap,
    withDensity_smul_measure, ← withDensity_smul _ (by fun_prop)]
  apply withDensity_congr_ae
  exact Filter.Eventually.of_forall fun x => by
    change ENNReal.ofReal |(B.det)⁻¹| *
      ENNReal.ofReal (((Real.sqrt (2 * Real.pi))⁻¹) ^ n *
        Real.exp (-‖em.symm x‖ ^ 2 / 2)) = _
    rw [← ENNReal.ofReal_mul (abs_nonneg _), hdetfactor, hnorm, hnormalizer]
    congr 1
    ring

end AutoSamplingTheory.TechnicalLemmas.Measure.GaussianPrecisionDensity
