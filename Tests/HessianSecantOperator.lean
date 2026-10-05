import AutoSamplingTheory.TechnicalLemmas.Analysis.HessianSecantOperator
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Deriv

open InnerProductSpace MeasureTheory
open scoped RealInnerProductSpace
open AutoSamplingTheory.TechnicalLemmas.Analysis.HessianSecantOperator

-- Genuine nonconstant Hessian: signed bounds survive integration. The operator
-- identity holds for all endpoints, including coincident ones; no strong
-- convexity is needed for this background interface.
example (x y : ℝ) :
    let H := ∫ t : ℝ in 0..1, continuousLinearMapOfBilin
      (fderiv ℝ (fderiv ℝ Real.sin) (y + t * (x - y)))
    Real.cos x - Real.cos y = H (x - y) ∧ H.IsSymmetric ∧ ‖H‖ ≤ 1 := by
  have hD : fderiv ℝ Real.sin = fun z =>
      Real.cos z • ContinuousLinearMap.id ℝ ℝ := by
    funext z
    ext
    simp [fderiv_eq_smul_deriv]
  have hD2 (z v : ℝ) : (fderiv ℝ (fderiv ℝ Real.sin) z v) v =
      -Real.sin z * v ^ 2 := by
    rw [hD, fderiv_eq_smul_deriv,
      ((Real.hasDerivAt_cos z).smul_const (ContinuousLinearMap.id ℝ ℝ)).deriv]
    simp
    ring
  have hlo (z v : ℝ) : (-1 : ℝ) * ‖v‖ ^ 2 ≤
      (fderiv ℝ (fderiv ℝ Real.sin) z v) v := by
    rw [hD2]
    simp only [Real.norm_eq_abs, sq_abs]
    nlinarith [Real.sin_le_one z, sq_nonneg v]
  have hup (z v : ℝ) : (fderiv ℝ (fderiv ℝ Real.sin) z v) v ≤ 1 * ‖v‖ ^ 2 := by
    rw [hD2]
    simp only [Real.norm_eq_abs, sq_abs]
    nlinarith [Real.neg_one_le_sin z, sq_nonneg v]
  have h := hessian_secant_operator Real.contDiff_sin hlo hup x y
  have hg (z : ℝ) : gradient Real.sin z = Real.cos z :=
    (Real.hasDerivAt_sin z).hasGradientAt.gradient
  exact ⟨by simpa [hg] using h.2.1, h.2.2.1, by simpa using h.2.2.2.2⟩

-- Empty Hilbert space: there is no nonzero direction or hidden nonempty
-- hypothesis; even inverted signed moduli are consistent on the zero space.
example (x y : EuclideanSpace ℝ (Fin 0)) :
    let φ := fun t : ℝ => continuousLinearMapOfBilin
      (fderiv ℝ (fderiv ℝ (fun _ : EuclideanSpace ℝ (Fin 0) => (7 : ℝ)))
        (y + t • (x - y)))
    IntervalIntegrable φ volume 0 1 ∧ ‖∫ t : ℝ in 0..1, φ t‖ ≤ 3 := by
  have hlo (z v : EuclideanSpace ℝ (Fin 0)) : (3 : ℝ) * ‖v‖ ^ 2 ≤
      (fderiv ℝ (fderiv ℝ (fun _ : EuclideanSpace ℝ (Fin 0) => (7 : ℝ))) z v) v := by
    have hv : v = 0 := Subsingleton.elim _ _
    simp [hv]
  have hup (z v : EuclideanSpace ℝ (Fin 0)) :
      (fderiv ℝ (fderiv ℝ (fun _ : EuclideanSpace ℝ (Fin 0) => (7 : ℝ))) z v) v ≤
      (-2 : ℝ) * ‖v‖ ^ 2 := by
    have hv : v = 0 := Subsingleton.elim _ _
    simp [hv]
  have h := hessian_secant_operator contDiff_const hlo hup x y
  exact ⟨h.1, by simp⟩

#check @hessian_secant_operator
#print axioms hessian_secant_operator
