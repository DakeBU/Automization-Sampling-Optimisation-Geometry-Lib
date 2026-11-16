import AutoSamplingTheory.TechnicalLemmas.Geometry.SphereProjectedNoise
import Mathlib.Analysis.InnerProductSpace.Laplacian

namespace AutoSamplingTheory.TechnicalLemmas.Geometry.SphereDiffusionGenerator

open scoped BigOperators Laplacian
open SphereProjectedNoise

variable {I : Type*} [Fintype I] [DecidableEq I]

local notation "E" => EuclideanSpace ℝ I

/-- The extrinsic unit-sphere Laplacian of a real ambient test. -/
noncomputable def sphereLaplacian (f : E → ℝ) (w : E) : ℝ :=
  (Δ f) w - fderiv ℝ (fderiv ℝ f) w w w -
    ((Fintype.card I - 1 : ℕ) : ℝ) * fderiv ℝ f w w

/-- Contracting with both projected noise arguments removes one radial Hessian
entry from the ambient Laplacian. -/
theorem sum_hessian_projectedNoiseColumn
    (f : E → ℝ) {w : E} (hw : ‖w‖ = 1) :
    (∑ j : I, fderiv ℝ (fderiv ℝ f) w (projectedNoiseColumn j w)
      (projectedNoiseColumn j w)) =
      (Δ f) w - fderiv ℝ (fderiv ℝ f) w w w := by
  let e := EuclideanSpace.basisFun I ℝ
  let H := fderiv ℝ (fderiv ℝ f) w
  have hrepr : (∑ j : I, w j • e j) = w := by
    simpa only [e, EuclideanSpace.basisFun_repr] using e.sum_repr w
  have happly (L : E →L[ℝ] ℝ) : (∑ j : I, w j * L (e j)) = L w := by
    calc
      _ = L (∑ j : I, w j • e j) := by simp only [map_sum, map_smul, smul_eq_mul]
      _ = L w := congrArg L hrepr
  have hright : (∑ j : I, w j * H w (e j)) = H w w := happly (H w)
  have hleft : (∑ j : I, w j * H (e j) w) = H w w := by
    calc
      _ = H (∑ j : I, w j • e j) w := by
        simp only [map_sum, sum_apply, map_smul, smul_apply, smul_eq_mul]
      _ = H w w := congrArg (fun v => H v w) hrepr
  have hsq : (∑ j : I, (w j) ^ 2) = 1 := by
    rw [← one_pow (M := ℝ) 2, ← hw]
    simp only [PiLp.norm_sq_eq_of_L2, Real.norm_eq_abs, sq_abs]
  have hcolumn (j : I) :
      H (projectedNoiseColumn j w) (projectedNoiseColumn j w) =
        H (e j) (e j) - w j * H (e j) w - w j * H w (e j) + (w j) ^ 2 * H w w := by
    simp only [projectedNoiseColumn, ← EuclideanSpace.basisFun_apply, ← show
        EuclideanSpace.basisFun I ℝ = e from rfl, map_sub, map_smul,
      sub_apply, smul_apply, smul_eq_mul]
    ring
  change (∑ j : I, H (projectedNoiseColumn j w) (projectedNoiseColumn j w)) =
    (Δ f) w - H w w
  simp_rw [hcolumn, Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.sum_mul,
    hleft, hright, hsq, one_mul]
  rw [InnerProductSpace.laplacian_eq_iteratedFDeriv_orthonormalBasis f e]
  simp only [iteratedFDeriv_two_apply, Matrix.cons_val_zero, Matrix.cons_val_one, H]
  ring

/-- Pointwise algebraic identity for the total derivative operators, projected
diffusion columns and radial correction. Under C² regularity this gives the
classical generator formula; when `u` is tangent the first term differentiates
the restricted test. -/
theorem ito_generator_eq_sphereLaplacian
    (f : E → ℝ) {w : E} (hw : ‖w‖ = 1) (u : E) {temperature : ℝ}
    (hTemperature : 0 ≤ temperature) :
    let σ := fun j : I => Real.sqrt (2 * temperature) • projectedNoiseColumn j w
    let b := -u - (temperature * ((Fintype.card I - 1 : ℕ) : ℝ)) • w
    fderiv ℝ f w b +
      (1 / 2 : ℝ) * (∑ j : I, fderiv ℝ (fderiv ℝ f) w (σ j) (σ j)) =
      -fderiv ℝ f w u + temperature * sphereLaplacian f w := by
  intro σ b
  have hScale (j : I) :
      fderiv ℝ (fderiv ℝ f) w (σ j) (σ j) = (2 * temperature) *
        fderiv ℝ (fderiv ℝ f) w (projectedNoiseColumn j w) (projectedNoiseColumn j w) := by
    simp only [σ, map_smul, smul_apply, smul_eq_mul, ← mul_assoc,
      ← pow_two, Real.sq_sqrt (by positivity : 0 ≤ 2 * temperature)]
  simp_rw [hScale, ← Finset.mul_sum, sum_hessian_projectedNoiseColumn f hw]
  simp only [b, map_sub, map_neg, map_smul, smul_eq_mul, sphereLaplacian]
  ring

end AutoSamplingTheory.TechnicalLemmas.Geometry.SphereDiffusionGenerator
